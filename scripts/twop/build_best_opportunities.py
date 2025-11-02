import os
from pathlib import Path
from typing import Dict, List, Any

try:
    from dotenv import load_dotenv  # optional
except Exception:  # pragma: no cover
    load_dotenv = lambda *a, **k: None

import sys
from pathlib import Path as _P
sys.path.append(str(_P(__file__).resolve().parents[2]))
from scripts.twop.two_performant_client import TwoPerformantClient
from scripts.twop.quicklink import build_quicklink


def score_program(p: Dict[str, Any]) -> float:
    """Heuristic score tuned for inteles.ro audience (dreams, sleep, lifestyle)."""
    name = (p.get("name") or "").lower()
    cat = (p.get("category", {}) or {}).get("name") or ""
    cat_l = cat.lower()
    cookie = float(p.get("cookie_life") or 0)
    try:
        rate = float(p.get("default_sale_commission_rate") or 0)
    except Exception:
        rate = 0.0

    # Base on commission rate + cookie life
    score = rate * 2.0 + (cookie / 30.0)

    # Category fit boosts
    if any(k in cat_l for k in ["book", "education"]):
        score += 4.0
    if any(k in cat_l for k in ["health", "beauty", "pharma", "supplement"]):
        score += 3.5
    if any(k in cat_l for k in ["electronics", "home", "appliance"]):
        score += 2.0

    # Known brand fit boosts
    boost_brands = ["libris", "librex", "carturesti", "springfarma", "evomag", "flanco", "manuka", "somproduct", "dormeo"]
    if any(b in name for b in boost_brands):
        score += 2.5

    # Product availability
    if int(p.get("products_count") or 0) > 1000:
        score += 1.0

    return score


def main():
    load_dotenv()
    email = os.getenv("TWO_P_EMAIL")
    password = os.getenv("TWO_P_PASSWORD")
    base = os.getenv("TWO_P_BASE", "https://api.2performant.com")
    aff_code = os.getenv("TWO_P_AFF_CODE")
    if not (email and password and aff_code):
        raise SystemExit("Missing TWO_P_EMAIL, TWO_P_PASSWORD or TWO_P_AFF_CODE env vars. See .env.example")

    client = TwoPerformantClient(base_url=base, email=email, password=password)
    client.login()
    programs = client.list_all_affiliate_programs(relation="accepted")

    # Keep RO country programs primarily
    def sells_in_ro(p: Dict[str, Any]) -> bool:
        for c in p.get("selling_countries") or []:
            if (c.get("code") or "").upper() == "RO":
                return True
        # fallback: base_url endswith .ro
        b = (p.get("base_url") or p.get("main_url") or "").lower()
        return b.endswith(".ro")

    programs = [p for p in programs if sells_in_ro(p)]

    # Score and sort
    scored = sorted(programs, key=score_program, reverse=True)
    top = scored[:25]

    # Build markdown
    lines: List[str] = []
    lines.append("# Best Monetization Opportunities — inteles.ro (2Performant)\n")
    lines.append("Criterii: rata comision, cookie life, potrivire categorie, brand & volum produse (RO).\n")
    lines.append("Fiecare link este pre-compus ca 2Performant Quicklink (nofollow+sponsored).\n")

    for p in top:
        name = p.get("name") or p.get("login") or "Program"
        base_url = p.get("main_url") or ("https://" + (p.get("base_url") or "").lstrip("/"))
        if not base_url.startswith("http"):
            base_url = f"https://{base_url}"
        cat = (p.get("category", {}) or {}).get("name") or "—"
        cookie = p.get("cookie_life") or "—"
        comm = p.get("default_sale_commission_rate") or "—"
        comm_type = p.get("default_sale_commission_type") or "percent"
        products = p.get("products_count") or 0
        feeds = p.get("product_feeds_count") or 0

        quick = build_quicklink(aff_code, base_url)

        lines.append(f"\n## {name.strip()}\n")
        lines.append(f"Categorie: {cat} • Comision: {comm}{'%' if comm_type=='percent' else ''} • Cookie: {cookie} zile • Produse: {products} • Feed-uri: {feeds}")
        lines.append(f"- Pagina principală\n  {base_url}\n  {quick}")

    out = Path("04-Monetization/Best-Opportunities.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} with {len(top)} programs.")


if __name__ == "__main__":
    main()

