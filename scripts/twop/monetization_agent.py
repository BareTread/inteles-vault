#!/usr/bin/env python3
"""
Monetization Agent (partner-only, clean URLs)

Goal
- Select 1–3 products from OUR APPROVED PARTNERS only
- Prefer higher commissions and strong topical relevance
- Verify URLs are live (2xx). If product URL fails, fall back to merchant homepage
- Output compact JSON and an HTML resource box using clean merchant URLs

Inputs (CLI)
- --topic "..." (required unless --article is provided)
- --keywords "k1,k2,k3" (optional)
- --article path/to/article.md (optional; derives topic/keywords if present)

Data sources (expected but script works with graceful fallbacks):
- 04-Monetization/MASTER-PRODUCTS-LIST.ACCEPTED.md (preferred)
- 04-Monetization/MASTER-PRODUCTS-LIST.md (fallback)
- 04-Monetization/Approved-Merchant-Homepages.md (fallback for homepages)
- affiliate_merchants_2performant.csv (at repo root) — partner status + commission/cookie (if present)

Outputs
- 04-Monetization/selected-products.<slug>.json
- 04-Monetization/resource-box.<slug>.html

Repo guidelines
- Python 3, PEP8, pathlib, requests, minimal deps
- Idempotent & safe re-runs
- All outputs under 04-Monetization/
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


VAULT_ROOT = Path(__file__).resolve().parents[2]
MON_DIR = VAULT_ROOT / "04-Monetization"
ROOT_AFF_CSV = VAULT_ROOT / "affiliate_merchants_2performant.csv"

MASTER_ACCEPTED = MON_DIR / "MASTER-PRODUCTS-LIST.ACCEPTED.md"
MASTER_ALL = MON_DIR / "MASTER-PRODUCTS-LIST.md"
APPROVED_HOMEPAGES = MON_DIR / "Approved-Merchant-Homepages.md"
CURATED_JSON = MON_DIR / "curated-products.json"


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
)


# ----------------------------- Data structures ----------------------------- #


@dataclass
class MerchantInfo:
    merchant: str  # usually a domain like libris.ro
    status: str = ""
    commission_str: str = ""
    cookie_str: str = ""
    homepage_url: Optional[str] = None

    def commission_pct(self) -> float:
        # Try to parse e.g. "18%" → 18.0 ; "1–10%" → ~10 ; "See grid" → 0
        s = (self.commission_str or "").strip()
        if not s:
            return 0.0
        # pick the max percentage mentioned
        nums = re.findall(r"(\d+(?:\.\d+)?)%", s)
        if nums:
            try:
                return max(float(n) for n in nums)
            except Exception:
                return 0.0
        return 0.0

    def cookie_days(self) -> int:
        s = (self.cookie_str or "").lower()
        # Try to capture number like "30 days", "30 zile", "1 month (30 days)"
        m = re.search(r"(\d+)[\s-]*(day|days|zile|month)", s)
        if m:
            try:
                n = int(m.group(1))
                # if "month", assume 30
                if "month" in s and n == 1:
                    return 30
                return n
            except Exception:
                return 0
        return 0


@dataclass
class Product:
    name: str
    merchant: str  # domain
    url: str  # clean merchant URL (no quicklink)
    category: Optional[str] = None
    tags: Tuple[str, ...] = ()
    commission_hint: Optional[float] = None  # from MD if present
    cookie_hint: Optional[int] = None  # from MD if present


# ------------------------------ Helper utils ------------------------------ #


def slugify(text: str) -> str:
    s = re.sub(r"[\s_+/]+", "-", text.strip().lower())
    s = re.sub(r"[^a-z0-9\-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "article"


def extract_redirect_to_url(quicklink: str) -> Optional[str]:
    """Given a 2Performant quicklink, return the decoded redirect_to URL.
    Example:
        https://event.2performant.com/events/click?...&redirect_to=https%3A%2F%2Flibris.ro%2Fxyz
    """
    try:
        # simple parse without full urlparse to avoid encoding pitfalls
        m = re.search(r"redirect_to=([^&]+)", quicklink)
        if not m:
            return None
        from urllib.parse import unquote

        return unquote(m.group(1))
    except Exception:
        return None


def _normalize_host(host: str) -> str:
    host = host.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def hostname_from_url(url: str) -> str:
    try:
        from urllib.parse import urlparse

        netloc = urlparse(url).netloc
        return _normalize_host(netloc)
    except Exception:
        return ""


def http_ok(url: str, timeout: int = 5) -> Tuple[bool, int, str]:
    """HEAD first; if blocked, GET with stream=True. Returns (ok, status, final_url)."""
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": USER_AGENT})
        code = r.status_code
        if 200 <= code < 300:
            return True, code, r.url
        # Some sites block HEAD; try GET lightweight
        r = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": USER_AGENT}, stream=True)
        code = r.status_code
        return (200 <= code < 300), code, r.url
    except Exception:
        return False, 0, url


# ---------------------------- Loading data files --------------------------- #


def load_affiliates_csv(path: Path) -> Dict[str, MerchantInfo]:
    partners: Dict[str, MerchantInfo] = {}
    if not path.exists():
        return partners
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = (row.get("Merchant") or "").strip().lower()
            # Extract a domain-like token from the merchant field
            m = re.search(r"([a-z0-9][a-z0-9\.-]*\.[a-z]{2,})", raw)
            merchant = _normalize_host(m.group(1)) if m else _normalize_host(raw)
            if not merchant:
                continue
            status = (row.get("Status") or "").strip()
            # Treat "Approved" as partner
            is_partner = status.lower().startswith("approved")
            mi = MerchantInfo(
                merchant=merchant,
                status=status,
                commission_str=(row.get("Commission") or "").strip(),
                cookie_str=(row.get("Cookie / Recurrence") or "").strip(),
                homepage_url=None,
            )
            if is_partner:
                partners[merchant] = mi
    return partners


def load_homepages(path: Path) -> Dict[str, str]:
    """Parse Approved-Merchant-Homepages.md and return merchant → clean homepage URL."""
    mapping: Dict[str, str] = {}
    if not path.exists():
        return mapping
    text = path.read_text(encoding="utf-8")
    # Entries like:
    # - libris.ro\n  https://event.2performant.com/...redirect_to=https%3A%2F%2Flibris.ro
    blocks = re.split(r"\n- ", text)
    for blk in blocks:
        m = re.match(r"([\w\.-]+)\n\s+(https?://[^\s]+)", blk.strip())
        if not m:
            continue
        merchant = m.group(1).strip().lower()
        ql = m.group(2).strip()
        url = extract_redirect_to_url(ql) or ql
        mapping[merchant] = url
    return mapping


def parse_master_products(paths: List[Path]) -> List[Product]:
    products: List[Product] = []
    current_category = None
    current_tags: Tuple[str, ...] = ()

    for p in paths:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            # Category heading
            if line.startswith("## "):
                current_category = line[3:].strip()
                current_tags = ()
                # Next lines may include *Tags: ...*
                j = i + 1
                if j < len(lines) and lines[j].strip().lower().startswith("*tags:"):
                    t = re.sub(r"^\*tags:\s*", "", lines[j].strip(), flags=re.I)
                    current_tags = tuple([s.strip().lower() for s in re.split(r"[,|]", t) if s.strip()])
                    i = j
            # Product heading (### Title (Merchant))
            if line.startswith("### "):
                title = line[4:].strip()
                # Look ahead for commission/cookie lines and code fence with quicklink
                commission_hint: Optional[float] = None
                cookie_hint: Optional[int] = None
                ql: Optional[str] = None
                k = i + 1
                # capture up to next heading/code fence end
                while k < len(lines) and not lines[k].startswith("### ") and not lines[k].startswith("## "):
                    l2 = lines[k].strip()
                    if l2.lower().startswith("**comision:**"):
                        # **Comision:** 18% | **Cookie:** 30 zile | ...
                        m = re.search(r"comision:\s*([\d\.]+)%", l2, flags=re.I)
                        if m:
                            try:
                                commission_hint = float(m.group(1))
                            except Exception:
                                pass
                        mc = re.search(r"cookie:\s*(\d+)", l2, flags=re.I)
                        if mc:
                            try:
                                cookie_hint = int(mc.group(1))
                            except Exception:
                                pass
                    if l2.startswith("```"):
                        # quicklink likely next lines until closing fence
                        k += 1
                        while k < len(lines) and not lines[k].startswith("```"):
                            if lines[k].strip().startswith("http"):
                                ql = lines[k].strip()
                                break
                            k += 1
                    k += 1
                if ql:
                    clean = extract_redirect_to_url(ql) or ql
                    host = hostname_from_url(clean)
                    prod = Product(
                        name=title,
                        merchant=host,
                        url=clean,
                        category=current_category,
                        tags=current_tags,
                        commission_hint=commission_hint,
                        cookie_hint=cookie_hint,
                    )
                    products.append(prod)
                i = k - 1  # continue after block
            i += 1

    return products


def parse_curated_products_json(path: Path) -> List[Product]:
    products: List[Product] = []
    if not path.exists():
        return products
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return products
    items = data.get("items") or []
    for it in items:
        name = (it.get("name") or "").strip()
        url = (it.get("url") or "").strip()
        merchant = hostname_from_url(url) or (it.get("merchant") or "").strip()
        category = it.get("category") or None
        if not (name and url and merchant):
            continue
        products.append(Product(name=name, merchant=merchant, url=url, category=category))
    return products


# ----------------------------- Scoring heuristic --------------------------- #


def relevance_score(prod: Product, topic: str, keywords: List[str]) -> int:
    score = 0
    t = (topic or "").lower()
    kws = [k.lower() for k in keywords if k]
    text = (prod.name or "").lower() + " " + " ".join(prod.tags)
    for k in kws:
        if k and k in text:
            score += 1
    # category-level nudge
    if prod.category:
        if any(k in (prod.category.lower()) for k in kws):
            score += 1
    if t:
        # lightweight fuzzy: count shared tokens
        for tok in re.split(r"\W+", t):
            if tok and tok in text:
                score += 0.5
    # Intent nudges based on common site patterns
    if any(k in (kws + [t]) for k in ["somn", "insomnie", "coșmar", "cosmar", "anxietate"]):
        if any(s in prod.category.lower() for s in ["somn", "sănătate", "sanatate", "dispozitive"] if prod.category):
            score += 2
    if any(k in (kws + [t]) for k in ["vise", "interpretare", "jung", "freud", "simbol"]):
        if any(s in prod.category.lower() for s in ["cărți", "carti", "psihologie"] if prod.category):
            score += 2
    return int(score)


def choose_products(
    products: List[Product],
    partners: Dict[str, MerchantInfo],
    homepages: Dict[str, str],
    topic: str,
    keywords: List[str],
    limit: int = 3,
) -> List[Product]:
    # Filter to partner merchants only
    part_hosts = set(partners.keys())
    candidates = [p for p in products if p.merchant in part_hosts]

    # Build a lookup for merchant commission/cookie
    def commission_for(p: Product) -> float:
        if p.commission_hint is not None:
            return p.commission_hint
        mi = partners.get(p.merchant)
        return mi.commission_pct() if mi else 0.0

    def cookie_for(p: Product) -> int:
        if p.cookie_hint is not None:
            return p.cookie_hint
        mi = partners.get(p.merchant)
        return mi.cookie_days() if mi else 0

    scored: List[Tuple[float, Product]] = []
    for p in candidates:
        rel = relevance_score(p, topic, keywords)
        com = commission_for(p)
        cookie = cookie_for(p)
        # score: relevance (0–?) + commission weight + cookie weight
        score = rel + (com / 5.0) + (cookie / 30.0)
        scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Diversity: avoid selecting all from same merchant
    chosen: List[Product] = []
    seen_merchants: set[str] = set()
    for _, p in scored:
        if len(chosen) >= limit:
            break
        if p.merchant in seen_merchants and len(chosen) < limit - 1:
            # try to keep diversity until near the cap
            continue
        chosen.append(p)
        seen_merchants.add(p.merchant)

    # Verify URLs; if product fails, try homepage; drop if both fail
    verified: List[Product] = []
    for p in chosen:
        ok, code, final = http_ok(p.url)
        if ok:
            verified.append(Product(**{**p.__dict__, "url": final}))
            continue
        # homepage attempt
        home = homepages.get(p.merchant) or f"https://{p.merchant}"
        ok2, code2, final2 = http_ok(home)
        if ok2:
            verified.append(Product(**{**p.__dict__, "url": final2}))
        # else drop
    return verified[:limit]


# ------------------------------- HTML builder ------------------------------ #


def build_html_box(products: List[Product], topic: str) -> str:
    # Clean URLs only; WP plugin will convert to affiliate links.
    items = []
    for p in products:
        url = html.escape(p.url, quote=True)
        name = html.escape(p.name)
        items.append(
            f"    <li><a href=\"{url}\" target=\"_blank\" rel=\"nofollow sponsored noopener\">{name}</a></li>"
        )
    topic_short = html.escape(topic)
    return (
        "<div style=\"background:#F3F7EE;border-left:4px solid #3B7C2A;padding:20px;"
        "margin:24px 0;border-radius:10px\">\n"
        "  <h3 style=\"margin:0 0 10px;color:#2B5E1E\">📚 Resurse utile</h3>\n"
        f"  <p style=\"margin:0 0 8px\">Selecție scurtă, relevantă pentru: {topic_short}.</p>\n"
        "  <ul style=\"margin:0 0 10px;padding-left:18px\">\n"
        + "\n".join(items)
        + "\n  </ul>\n"
        "  <p style=\"font-size:.85rem;color:#5a5a5a;margin:0\"><em>"
        "Linkuri afiliate — comision mic, fără costuri pentru tine.</em></p>\n"
        "</div>\n"
    )


# --------------------------------- CLI main -------------------------------- #


def derive_keywords_from_article(text: str) -> Tuple[str, List[str]]:
    # Title as topic (first H1 or first non-empty line), naive keyword extraction
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    topic = lines[0].lstrip("# ") if lines else "Articol"
    words = re.findall(r"[A-Za-zĂÂÎȘȚăâîșț\-]{4,}", text)
    # frequent words heuristic
    freq: Dict[str, int] = {}
    for w in words:
        wl = w.lower()
        freq[wl] = freq.get(wl, 0) + 1
    # top 8 words excluding very common ones
    stop = {"este", "care", "pentru", "cu", "din", "și", "si", "că", "ca", "despre", "unei", "unei", "în", "in"}
    ranked = [w for w, c in sorted(freq.items(), key=lambda x: x[1], reverse=True) if w not in stop]
    return topic, ranked[:8]


def main() -> None:
    ap = argparse.ArgumentParser(description="Select and verify partner products for an article")
    ap.add_argument("--topic", help="Article topic/title")
    ap.add_argument("--keywords", help="Comma-separated keywords", default="")
    ap.add_argument("--article", help="Path to article markdown (derive topic/keywords)")
    ap.add_argument("--limit", type=int, default=3, help="Max products to return (default 3)")
    ap.add_argument("--out_json", help="Output JSON path")
    ap.add_argument("--out_html", help="Output HTML path")
    args = ap.parse_args()

    topic = (args.topic or "").strip()
    kw_list = [k.strip() for k in (args.keywords or "").split(",") if k.strip()]

    if args.article:
        art_path = Path(args.article)
        if art_path.exists():
            text = art_path.read_text(encoding="utf-8")
            topic2, kws2 = derive_keywords_from_article(text)
            topic = topic or topic2
            if not kw_list:
                kw_list = kws2

    if not topic:
        print("ERROR: --topic or --article is required", file=sys.stderr)
        sys.exit(2)

    slug = slugify(topic)
    out_json = Path(args.out_json) if args.out_json else (MON_DIR / f"selected-products.{slug}.json")
    out_html = Path(args.out_html) if args.out_html else (MON_DIR / f"resource-box.{slug}.html")

    # Load data
    partners = load_affiliates_csv(ROOT_AFF_CSV)
    homepages = load_homepages(APPROVED_HOMEPAGES)
    prods = []
    # Prefer curated products if available, then augment with master lists
    prods.extend(parse_curated_products_json(CURATED_JSON))
    prods.extend(parse_master_products([MASTER_ACCEPTED, MASTER_ALL]))

    # Choose
    chosen = choose_products(prods, partners, homepages, topic=topic, keywords=kw_list, limit=args.limit)

    # Build outputs
    items = []
    for p in chosen:
        mi = partners.get(p.merchant)
        commission = p.commission_hint if p.commission_hint is not None else (mi.commission_pct() if mi else 0.0)
        cookie = p.cookie_hint if p.cookie_hint is not None else (mi.cookie_days() if mi else 0)
        items.append(
            {
                "name": p.name,
                "merchant": p.merchant,
                "url": p.url,
                "commission": (f"{commission:.0f}%" if commission else ""),
                "cookie_days": cookie,
                "reasoning": "Relevanță ridicată pentru subiect; partener aprobat.",
            }
        )

    result = {"products": items}
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    box_html = build_html_box(chosen, topic)
    out_html.write_text(box_html, encoding="utf-8")

    # Also print the JSON to stdout for agent consumption
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
