#!/usr/bin/env python3
"""
Harvest 200+ verified product links from approved partners.

Sources
- 2Performant Advertiser Promotions API (per accepted program)
- Curated MASTER lists (redirect_to extracted from quicklinks)

Outputs
- 04-Monetization/curated-products.json
- 04-Monetization/curated-products.csv

Requirements
- Env: TWO_P_EMAIL, TWO_P_PASSWORD (optional TWO_P_BASE)
- Minimal deps (requests)
"""
from __future__ import annotations

import os
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

from pathlib import Path as _P
import sys as _sys
_sys.path.append(str(_P(__file__).resolve().parents[2]))

try:
    from dotenv import load_dotenv  # optional
except Exception:  # pragma: no cover
    def load_dotenv(*a, **k):
        return None

from scripts.twop.two_performant_client import TwoPerformantClient
from scripts.twop.monetization_agent import (
    parse_master_products as _parse_master_products,
    hostname_from_url as _hostname_from_url,
    http_ok as _http_ok,
)


VAULT_ROOT = Path(__file__).resolve().parents[2]
MON_DIR = VAULT_ROOT / "04-Monetization"
AFF_CSV = MON_DIR / "affiliates.csv"
AFF_CSV_EXTRA = MON_DIR / "affiliates-COMPLETE.csv"
MASTER_ACCEPTED = MON_DIR / "MASTER-PRODUCTS-LIST.ACCEPTED.md"
MASTER_ALL = MON_DIR / "MASTER-PRODUCTS-LIST.md"
FEEDS_CSV = MON_DIR / "product_feeds.csv"  # optional config: domain,feed_url,format


def load_affiliates_domains(path: Path) -> Dict[str, Dict[str, str]]:
    domains: Dict[str, Dict[str, str]] = {}
    if not path.exists():
        return domains
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("merchant_name") or "").strip()
            domain = (row.get("domain") or "").strip().lower()
            category = (row.get("category") or "").strip()
            if not domain:
                continue
            domains[domain] = {"name": name or domain, "category": category}
    return domains


def map_program_domain(p: dict) -> Optional[str]:
    # Try common fields for program main domain
    for key in ("base_url", "main_url", "website", "url"):
        v = p.get(key)
        if v:
            import re, urllib.parse
            host = urllib.parse.urlparse(v).netloc.lower()
            host = host[4:] if host.startswith("www.") else host
            if re.search(r"\.[a-z]{2,}$", host):
                return host
    return None


def harvest_from_promotions(client: TwoPerformantClient, domains_whitelist: set[str], limit_per_merchant: int = 50) -> List[dict]:
    # List accepted programs and collect promotions per program
    try:
        programs = client.list_all_affiliate_programs(relation="accepted")
    except Exception:
        programs = []

    domain_to_programs: Dict[str, List[int]] = {}
    for p in programs:
        dom = map_program_domain(p) or ""
        pid = p.get("id") or p.get("program", {}).get("id")
        if not dom or not pid:
            continue
        domain_to_programs.setdefault(dom, []).append(int(pid))

    items: List[dict] = []
    for dom, pids in domain_to_programs.items():
        if domains_whitelist and dom not in domains_whitelist:
            continue
        taken = 0
        for pid in pids:
            page = 1
            while True:
                try:
                    data = client.list_advertiser_promotions(page=page, per_page=50, program_id=pid)
                except Exception:
                    break
                promos = data.get("advertiser_promotions") or data.get("data") or []
                if not promos:
                    break
                for pr in promos:
                    url = pr.get("landing_page_link") or pr.get("url") or ""
                    name = pr.get("name") or pr.get("title") or "Promoție"
                    if not url:
                        continue
                    items.append({
                        "name": name,
                        "url": url,
                        "merchant": dom,
                        "source": "promotion",
                    })
                    taken += 1
                    if taken >= limit_per_merchant:
                        break
                if taken >= limit_per_merchant:
                    break
                page += 1
                time.sleep(0.2)
    return items


def harvest_from_master_lists() -> List[dict]:
    prods = _parse_master_products([MASTER_ACCEPTED, MASTER_ALL])
    out: List[dict] = []
    for p in prods:
        out.append({
            "name": p.name,
            "url": p.url,
            "merchant": p.merchant,
            "source": f"master:{'accepted' if 'ACCEPTED' in (p.category or '') else 'all'}",
        })
    return out


def load_product_feeds(path: Path) -> List[dict]:
    feeds: List[dict] = []
    if not path.exists():
        return feeds
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dom = (row.get("domain") or "").strip().lower()
            url = (row.get("feed_url") or "").strip()
            fmt = (row.get("format") or "csv").strip().lower()
            if dom and url:
                feeds.append({"domain": dom, "feed_url": url, "format": fmt})
    return feeds


def harvest_from_csv_feed(feed_url: str, domain: str, limit: int = 200) -> List[dict]:
    items: List[dict] = []
    try:
        import io
        r = requests.get(feed_url, timeout=30)
        r.raise_for_status()
        text = r.text
        f = io.StringIO(text)
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            # Try common fields
            url = row.get("link") or row.get("url") or row.get("product_url") or ""
            name = row.get("name") or row.get("title") or row.get("product_name") or ""
            if not url:
                continue
            items.append({
                "name": name or domain,
                "url": url,
                "merchant": domain,
                "source": "feed",
            })
    except Exception as e:
        print(f"WARN: feed fetch failed for {domain}: {e}")
    return items


def _verify_candidate(item: dict, timeout: float) -> Tuple[bool, str, int]:
    """Return (ok, final_url, status_code)."""
    url = (item.get("url") or "").strip()
    if not url:
        return False, "", 0
    ok, code, final = _http_ok(url, timeout=timeout)
    if not ok:
        dom = item.get("merchant") or _hostname_from_url(url)
        if dom:
            home = f"https://{dom}"
            ok2, code2, final2 = _http_ok(home, timeout=timeout)
            if ok2:
                return True, final2, code2
    return ok, final, code


def verify_and_dedupe(candidates: List[dict], category_by_domain: Dict[str, str], allowed_domains: set[str]) -> List[dict]:
    seen: set[str] = set()
    out: List[dict] = []
    timeout = float(os.getenv("HARVEST_VERIFY_TIMEOUT", "3"))
    workers = int(os.getenv("HARVEST_VERIFY_WORKERS", "16"))
    target = int(os.getenv("HARVEST_TARGET_TOTAL", "600"))

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        future_map = {pool.submit(_verify_candidate, item, timeout): item for item in candidates}
        for fut in as_completed(future_map):
            item = future_map[fut]
            try:
                ok, final, code = fut.result()
            except Exception:
                continue
            if not ok:
                continue
            key = final.strip()
            if not key or key in seen:
                continue
            dom2 = _hostname_from_url(final)
            if allowed_domains and dom2 not in allowed_domains:
                continue
            seen.add(key)
            out.append({
                "name": item.get("name") or dom2,
                "url": final,
                "merchant": dom2,
                "category": category_by_domain.get(dom2, ""),
                "source": item.get("source") or "",
                "status": code,
            })
            if len(out) >= target:
                break
    return out


def main() -> None:
    load_dotenv()
    # Aff whitelist
    aff = load_affiliates_domains(AFF_CSV)
    if AFF_CSV_EXTRA.exists():
        extra = load_affiliates_domains(AFF_CSV_EXTRA)
        aff.update(extra)
    domains_whitelist = set(aff.keys())
    category_by_domain = {d: v.get("category", "") for d, v in aff.items()}

    # 2Performant promotions
    items: List[dict] = []
    email = os.getenv("TWO_P_EMAIL")
    password = os.getenv("TWO_P_PASSWORD")
    base = os.getenv("TWO_P_BASE", "https://api.2performant.com")
    promo_limit = int(os.getenv("HARVEST_PROMO_LIMIT", "80"))
    if email and password:
        client = TwoPerformantClient(base_url=base, email=email, password=password)
        try:
            client.login()
            items += harvest_from_promotions(client, domains_whitelist, limit_per_merchant=promo_limit)
        except Exception as e:
            print(f"WARN: promotions harvest failed: {e}")
    else:
        print("WARN: Missing TWO_P_EMAIL/PASSWORD; skipping promotions harvest")

    # Curated master lists
    items += harvest_from_master_lists()

    # Optional: product feeds (CSV)
    feeds = load_product_feeds(FEEDS_CSV)
    for fd in feeds:
        if domains_whitelist and fd["domain"] not in domains_whitelist:
            continue
        items += harvest_from_csv_feed(fd["feed_url"], fd["domain"], limit=300)

    # Verify & dedupe
    verified = verify_and_dedupe(items, category_by_domain, domains_whitelist)

    # Rank roughly by category priority then by source
    # Books, Supplements, Organic/Bio, Food/Honey, etc.
    cat_order = {
        "Books": 0,
        "Supplements": 1,
        "Organic/Bio": 2,
        "Food/Honey": 3,
        "Pharmacy": 4,
        "Beauty/Nails": 5,
        "Cosmetics": 6,
        "Hair Care": 7,
        "Tools/DIY": 8,
        "Fitness": 9,
        "Accessories": 10,
    }
    verified.sort(key=lambda x: (cat_order.get(x.get("category") or "~", 99), x.get("merchant", "")))

    # Keep top N overall if huge
    N = 600
    verified = verified[:N]

    # Write outputs
    out_json = MON_DIR / "curated-products.json"
    out_csv = MON_DIR / "curated-products.csv"
    out_json.write_text(json.dumps({"total": len(verified), "items": verified}, ensure_ascii=False, indent=2), encoding="utf-8")
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "url", "merchant", "category", "source"]) 
        for it in verified:
            w.writerow([it["name"], it["url"], it["merchant"], it.get("category", ""), it.get("source", "")])

    print(json.dumps({"harvested": len(items), "verified": len(verified)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
