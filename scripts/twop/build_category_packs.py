#!/usr/bin/env python3
"""
Build Category Packs (10–20 items/category)

Purpose
- Parse MASTER-PRODUCTS-LIST (and ACCEPTED) to compile 10–20 ready products per category
- Prefer items from ACCEPTED; verify URLs (2xx) and fall back to merchant homepage when needed
- Rank by relevance signals embedded in the docs (commission/cookie hints) + partner program data
- Output JSON packs per category and a Markdown summary under 04-Monetization/

Usage
  .venv/bin/python scripts/twop/build_category_packs.py \
    --min 10 --max 20 \
    --out_dir 04-Monetization/category-packs

Notes
- No external deps beyond requests (already in requirements)
- Safe to re-run; overwrites outputs idempotently
- Clean merchant URLs only (WP plugin will convert to affiliate links)
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


VAULT_ROOT = Path(__file__).resolve().parents[2]
MON_DIR = VAULT_ROOT / "04-Monetization"
MASTER_ACCEPTED = MON_DIR / "MASTER-PRODUCTS-LIST.ACCEPTED.md"
MASTER_ALL = MON_DIR / "MASTER-PRODUCTS-LIST.md"
APPROVED_HOMEPAGES = MON_DIR / "Approved-Merchant-Homepages.md"
ROOT_AFF_CSV = VAULT_ROOT / "affiliate_merchants_2performant.csv"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
)


# ----------------------------- Data structures ----------------------------- #


@dataclass
class MerchantInfo:
    merchant: str
    status: str = ""
    commission_str: str = ""
    cookie_str: str = ""
    homepage_url: Optional[str] = None

    def commission_pct(self) -> float:
        s = (self.commission_str or "").strip()
        if not s:
            return 0.0
        nums = re.findall(r"(\d+(?:\.\d+)?)%", s)
        if nums:
            try:
                return max(float(n) for n in nums)
            except Exception:
                return 0.0
        return 0.0

    def cookie_days(self) -> int:
        s = (self.cookie_str or "").lower()
        m = re.search(r"(\d+)[\s-]*(day|days|zile|month)", s)
        if m:
            try:
                n = int(m.group(1))
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
    url: str       # clean merchant URL (no quicklink)
    category: Optional[str] = None
    commission_hint: Optional[float] = None
    cookie_hint: Optional[int] = None
    source: str = "all"  # "accepted" or "all"


# ------------------------------ Helper utils ------------------------------ #


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


def extract_redirect_to_url(quicklink: str) -> Optional[str]:
    try:
        m = re.search(r"redirect_to=([^&]+)", quicklink)
        if not m:
            return None
        from urllib.parse import unquote

        return unquote(m.group(1))
    except Exception:
        return None


def http_ok(url: str, timeout: int = 6) -> Tuple[bool, int, str]:
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": USER_AGENT})
        code = r.status_code
        if 200 <= code < 300:
            return True, code, r.url
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
            m = re.search(r"([a-z0-9][a-z0-9\.-]*\.[a-z]{2,})", raw)
            merchant = _normalize_host(m.group(1)) if m else _normalize_host(raw)
            if not merchant:
                continue
            mi = MerchantInfo(
                merchant=merchant,
                status=(row.get("Status") or "").strip(),
                commission_str=(row.get("Commission") or "").strip(),
                cookie_str=(row.get("Cookie / Recurrence") or "").strip(),
                homepage_url=None,
            )
            partners[merchant] = mi
    return partners


def load_homepages(path: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not path.exists():
        return mapping
    text = path.read_text(encoding="utf-8")
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
    current_category: Optional[str] = None
    current_source = "all"

    for p in paths:
        if not p.exists():
            continue
        current_source = "accepted" if p.name.endswith("ACCEPTED.md") else "all"
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            if line.startswith("## "):
                current_category = line[3:].strip()
            if line.startswith("### "):
                title = line[4:].strip()
                commission_hint: Optional[float] = None
                cookie_hint: Optional[int] = None
                ql: Optional[str] = None
                k = i + 1
                while k < len(lines) and not lines[k].startswith("### ") and not lines[k].startswith("## "):
                    l2 = lines[k].strip()
                    if l2.lower().startswith("**comision:**"):
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
                    # Check for fenced code block first
                    if l2.startswith("```"):
                        k += 1
                        while k < len(lines) and not lines[k].strip().startswith("```"):
                            link_candidate = lines[k].strip()
                            if link_candidate.startswith("http") and "2performant.com" in link_candidate:
                                ql = link_candidate
                                break
                            k += 1
                    # Also capture inline quicklinks (not in fenced blocks)
                    elif "https://event.2performant.com/events/click?" in l2 and l2.startswith("http"):
                        ql = l2
                    k += 1
                if ql:
                    clean = extract_redirect_to_url(ql) or ql
                    host = hostname_from_url(clean)
                    products.append(
                        Product(
                            name=title,
                            merchant=host,
                            url=clean,
                            category=current_category,
                            commission_hint=commission_hint,
                            cookie_hint=cookie_hint,
                            source=current_source,
                        )
                    )
                i = k - 1
            i += 1
    return products


# ----------------------------- Scoring heuristic --------------------------- #


def score_product(p: Product, partners: Dict[str, MerchantInfo]) -> float:
    mi = partners.get(p.merchant)
    commission = p.commission_hint if p.commission_hint is not None else (mi.commission_pct() if mi else 0.0)
    cookie = p.cookie_hint if p.cookie_hint is not None else (mi.cookie_days() if mi else 0)
    # Base: commission and cookie
    score = (commission / 5.0) + (cookie / 30.0)
    # Preferred source gets a bonus
    if p.source == "accepted":
        score += 2.0
    # Very low commission slight penalty
    if commission and commission < 4.0:
        score -= 0.5
    return score


# --------------------------------- Builder -------------------------------- #


def build_category_packs(products: List[Product], partners: Dict[str, MerchantInfo], homepages: Dict[str, str], rng: Tuple[int, int]) -> Dict[str, List[Dict]]:
    cat_map: Dict[str, List[Product]] = {}
    for p in products:
        if not p.category:
            continue
        cat_map.setdefault(p.category, []).append(p)

    min_k, max_k = rng
    out: Dict[str, List[Dict]] = {}
    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    for cat, items in cat_map.items():
        # Keep only partners
        part_items = [p for p in items if p.merchant in partners]
        # Score & sort
        ranked = sorted(part_items, key=lambda x: score_product(x, partners), reverse=True)

        # Verify URLs and build payload
        pack: List[Dict] = []
        for p in ranked:
            if len(pack) >= max_k:
                break
            ok, code, final = http_ok(p.url)
            url = final
            if not ok:
                home = homepages.get(p.merchant) or f"https://{p.merchant}"
                ok2, code2, final2 = http_ok(home)
                if not ok2:
                    continue
                url = final2

            mi = partners.get(p.merchant)
            commission = p.commission_hint if p.commission_hint is not None else (mi.commission_pct() if mi else 0.0)
            cookie = p.cookie_hint if p.cookie_hint is not None else (mi.cookie_days() if mi else 0)
            pack.append(
                {
                    "name": p.name,
                    "merchant": p.merchant,
                    "url": url,
                    "commission": (f"{commission:.0f}%" if commission else ""),
                    "cookie_days": cookie,
                    "category": cat,
                    "source": p.source,
                    "last_verified": now,
                }
            )

        # Enforce minimum: if below min_k, keep as-is but record anyway
        out[cat] = pack[:max_k]
    return out


def slugify(text: str) -> str:
    s = re.sub(r"[\s_+/]+", "-", text.strip().lower())
    s = re.sub(r"[^a-z0-9\-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "categorie"


def write_outputs(packs: Dict[str, List[Dict]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    # Index
    index = {
        "last_built": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "categories": [
            {"name": cat, "slug": slugify(cat), "count": len(items)} for cat, items in sorted(packs.items())
        ],
    }
    (out_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    # Per-category JSON
    for cat, items in packs.items():
        (out_dir / f"{slugify(cat)}.json").write_text(json.dumps({"category": cat, "items": items}, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown summary
    lines: List[str] = []
    lines.append("# Category Packs — Ready Products\n")
    lines.append(f"Last Built: {index['last_built']}\n")
    for cat, items in sorted(packs.items()):
        lines.append(f"\n## {cat} ({len(items)})\n")
        for it in items:
            lines.append(f"- {it['name']} — {it['merchant']}\n  {it['url']}")
    (out_dir.parent / "Category-Packs.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build 10–20 item product packs per category from master lists")
    ap.add_argument("--min", type=int, default=10, help="Minimum target per category (soft)")
    ap.add_argument("--max", type=int, default=20, help="Maximum items per category")
    ap.add_argument("--out_dir", default=str(MON_DIR / "category-packs"), help="Output directory for JSON packs")
    args = ap.parse_args()

    partners = load_affiliates_csv(ROOT_AFF_CSV)
    homepages = load_homepages(APPROVED_HOMEPAGES)
    products = parse_master_products([MASTER_ACCEPTED, MASTER_ALL])

    packs = build_category_packs(products, partners, homepages, (args.min, args.max))
    write_outputs(packs, Path(args.out_dir))

    # Print quick summary
    total = sum(len(v) for v in packs.values())
    print(json.dumps({"categories": len(packs), "total_items": total}, ensure_ascii=False))


if __name__ == "__main__":
    main()
