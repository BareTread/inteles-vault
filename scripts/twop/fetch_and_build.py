import os
import argparse
from pathlib import Path
from typing import Dict, List

try:
    from dotenv import load_dotenv  # optional
except Exception:  # pragma: no cover
    load_dotenv = lambda *a, **k: None

import sys
from pathlib import Path as _P
sys.path.append(str(_P(__file__).resolve().parents[2]))
from scripts.twop.two_performant_client import TwoPerformantClient
from scripts.twop.product_sources import curated_product_urls
from scripts.twop.quicklink import build_quicklink


def pick_relevant_merchants(programs: List[Dict]) -> Dict[str, Dict]:
    want = {"libris.ro", "springfarma.com", "manukashop.ro", "evomag.ro", "flanco.ro", "librex.ro"}
    found: Dict[str, Dict] = {}
    for p in programs:
        base = (p.get("base_url") or "").lower()
        for w in want:
            if w in base or w in (p.get("main_url") or "").lower():
                found[w] = p
    return found


def generate_markdown(aff_code: str, merchant_urls: Dict[str, List[str]], promo_urls: Dict[str, List[Dict[str, str]]] | None = None) -> str:
    lines: List[str] = []
    lines.append("# Auto-Generated Affiliate Links (2Performant)\n")
    lines.append("Sursa: API 2Performant (programe acceptate) + mapare produse curată.\n")
    lines.append("Atribute recomandate: `rel=\"nofollow sponsored noopener\"` + disclosure ANPC.\n")

    sections = [
        ("Cărți (Libris)", "libris.ro"),
        ("Suplimente Somn & Relaxare (SpringFarma)", "springfarma.com"),
        ("Miere Manuka (ManukaShop)", "manukashop.ro"),
        ("Dispozitive Somn (evoMAG / Flanco)", "evomag.ro"),
        ("Dispozitive Somn (evoMAG / Flanco)", "flanco.ro"),
        ("Jurnale de vise / mindfulness (Librex)", "librex.ro"),
    ]

    for title, domain in sections:
        urls = merchant_urls.get(domain, [])
        if not urls:
            continue
        lines.append(f"\n## {title}\n")
        for u in urls:
            q = build_quicklink(aff_code, u, unique=None)
            lines.append(f"- {u}\n  {q}")

        # Add promo links if available for this domain
        if promo_urls and promo_urls.get(domain):
            lines.append("\nPromoții relevante:")
            for promo in promo_urls.get(domain, [])[:10]:
                pu = promo.get("url") or promo.get("landing_page_link") or ""
                if not pu:
                    continue
                label = promo.get("name") or promo.get("title") or "Promoție"
                coupon = promo.get("coupon")
                meta = f" — cupon: {coupon}" if coupon else ""
                q = build_quicklink(aff_code, pu, unique=None)
                lines.append(f"- {label}{meta}\n  {pu}\n  {q}")

    return "\n".join(lines) + "\n"


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Fetch 2Performant programs and build quicklinks")
    parser.add_argument("--out", default="04-Monetization/Auto-Generated-Affiliate-Links.md")
    parser.add_argument("--relation", default="accepted", help="Affiliate-program relation filter")
    args = parser.parse_args()

    email = os.getenv("TWO_P_EMAIL")
    password = os.getenv("TWO_P_PASSWORD")
    base = os.getenv("TWO_P_BASE", "https://api.2performant.com")
    aff_code = os.getenv("TWO_P_AFF_CODE")

    if not (email and password and aff_code):
        raise SystemExit("Missing TWO_P_EMAIL, TWO_P_PASSWORD or TWO_P_AFF_CODE env vars. See .env.example")

    client = TwoPerformantClient(base_url=base, email=email, password=password)
    merchants = {}
    try:
        client.login()
        programs = client.list_all_affiliate_programs(relation=args.relation)
        merchants = pick_relevant_merchants(programs)
    except Exception as e:
        # Fallback to all curated merchants in offline mode
        merchants = {k: {} for k in curated_product_urls().keys()}
        print("Warning: API login/list failed. Falling back to curated merchants only.")

    curated = curated_product_urls()
    available_urls: Dict[str, List[str]] = {k: curated.get(k, []) for k in merchants.keys()}

    # Promo enrichment via API (if available)
    promo_urls: Dict[str, List[Dict[str, str]]] = {}
    if merchants:
        try:
            # Pull a few pages of network-wide promos, then filter by program domain
            aggregated: List[Dict] = []
            for page in range(1, 6):  # up to ~250 promos
                data = client.list_advertiser_promotions(page=page, per_page=50)
                items = data.get("advertiser_promotions") or data.get("promotions") or data.get("data") or []
                if not items:
                    break
                aggregated.extend(items)
            for domain in merchants.keys():
                norm: List[Dict[str, str]] = []
                for it in aggregated:
                    pr = it.get("program") or {}
                    pname = (pr.get("name") or pr.get("base_url") or pr.get("main_url") or "").lower()
                    if domain not in pname:
                        continue
                    url = it.get("landing_page_link") or it.get("landing_url") or it.get("url")
                    if not url:
                        continue
                    name = it.get("name") or it.get("title") or "Promoție"
                    coupon = it.get("coupon") or ""
                    norm.append({"url": url, "name": name, "coupon": coupon})
                if norm:
                    promo_urls[domain] = norm[:20]
        except Exception:
            # silently continue; promos are optional
            pass

    header_note = ""
    if not merchants or all(not v for v in merchants.values()):
        header_note = "\n> NOTĂ: Generare offline (API indisponibil). Folosim produse curate din vault.\n"
    md = ("# Auto-Generated Affiliate Links (2Performant)\n" + header_note + "\n") + generate_markdown(aff_code, available_urls, promo_urls)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {out_path} with {sum(len(v) for v in available_urls.values())} links.")


if __name__ == "__main__":
    main()
