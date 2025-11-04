#!/usr/bin/env python3
"""
Clean affiliate link database builder.

Parses MASTER-PRODUCTS-LIST files, validates URLs, outputs structured JSON database.
Zero hallucinations - only uses verified links from curated sources.
"""
from __future__ import annotations

import json
import re
import requests
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urlparse, parse_qs, unquote

# Paths
ROOT = Path(__file__).resolve().parents[2]
MON_DIR = ROOT / "04-Monetization"
MASTER_ALL = MON_DIR / "MASTER-PRODUCTS-LIST.md"
MASTER_ACCEPTED = MON_DIR / "MASTER-PRODUCTS-LIST.ACCEPTED.md"
AFFILIATES_CSV = ROOT / "affiliate_merchants_2performant.csv"
OUTPUT_JSON = MON_DIR / "affiliate-database.json"

USER_AGENT = "Mozilla/5.0 (compatible; IntelesMon/1.0)"


@dataclass
class Product:
    """Single affiliate product with verified link"""
    name: str
    merchant: str
    category: str
    commission: Optional[str]
    cookie_days: Optional[int]
    quicklink: str
    destination_url: str
    tags: List[str]
    use_cases: List[str]
    verified: bool
    last_checked: str
    source: str  # 'accepted' or 'all'


def extract_redirect_url(quicklink: str) -> Optional[str]:
    """Extract destination URL from 2Performant quicklink"""
    try:
        parsed = urlparse(quicklink)
        params = parse_qs(parsed.query)
        if "redirect_to" in params:
            return unquote(params["redirect_to"][0])
    except Exception:
        pass
    return None


def verify_url(url: str, timeout: int = 6) -> bool:
    """Check if URL returns 200 OK"""
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": USER_AGENT})
        if 200 <= r.status_code < 300:
            return True
        r = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": USER_AGENT}, stream=True)
        return 200 <= r.status_code < 300
    except Exception:
        return False


def parse_master_list(path: Path, source: str) -> List[Product]:
    """Parse MASTER-PRODUCTS-LIST markdown file"""
    if not path.exists():
        return []
    
    products: List[Product] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    
    current_category: Optional[str] = None
    current_tags: List[str] = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Category header
        if line.startswith("## ") and not line.startswith("## ✨"):
            current_category = line[3:].strip()
            # Look for tags on next line
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("*Tags:"):
                tags_line = lines[i + 1].strip()
                tag_match = re.search(r"\*Tags:\s*(.+)\*", tags_line)
                if tag_match:
                    current_tags = [t.strip() for t in tag_match.group(1).split(",")]
        
        # Product section
        elif line.startswith("### ") and current_category:
            title = line[4:].strip()
            commission: Optional[str] = None
            cookie_days: Optional[int] = None
            use_cases: List[str] = []
            quicklink: Optional[str] = None
            
            # Scan ahead for metadata and quicklink
            j = i + 1
            while j < len(lines):
                l = lines[j].strip()
                
                # Stop at next section
                if l.startswith("###") or l.startswith("##") or l.startswith("---"):
                    break
                
                # Extract commission & cookie
                if l.startswith("**Comision:**"):
                    comm_match = re.search(r"(\d+(?:\.\d+)?%)", l)
                    if comm_match:
                        commission = comm_match.group(1)
                    cookie_match = re.search(r"Cookie:\*?\*?\s*(\d+)\s*zile", l, flags=re.I)
                    if cookie_match:
                        cookie_days = int(cookie_match.group(1))
                    # Extract use cases
                    use_match = re.search(r"Potrivit pentru:\*?\*?\s*(.+?)(?:\*\*|$)", l, flags=re.I)
                    if use_match:
                        use_cases = [u.strip() for u in use_match.group(1).split(",")]
                
                # Find quicklink in fenced code block
                if l == "```":
                    j += 1
                    while j < len(lines) and lines[j].strip() != "```":
                        candidate = lines[j].strip()
                        if candidate.startswith("http") and "2performant.com" in candidate:
                            quicklink = candidate
                            break
                        j += 1
                
                j += 1
            
            # If we found a valid quicklink, add the product
            if quicklink and current_category:
                dest_url = extract_redirect_url(quicklink) or quicklink
                merchant_domain = urlparse(dest_url).netloc.replace("www.", "")
                
                products.append(Product(
                    name=title,
                    merchant=merchant_domain,
                    category=current_category,
                    commission=commission,
                    cookie_days=cookie_days,
                    quicklink=quicklink,
                    destination_url=dest_url,
                    tags=current_tags.copy(),
                    use_cases=use_cases,
                    verified=False,  # Will verify later
                    last_checked="",
                    source=source
                ))
            
            i = j - 1
        
        i += 1
    
    return products


def build_database() -> Dict:
    """Build complete affiliate link database"""
    print("📖 Parsing MASTER lists...")
    
    # Parse both sources (ACCEPTED has priority)
    accepted_products = parse_master_list(MASTER_ACCEPTED, "accepted")
    all_products = parse_master_list(MASTER_ALL, "all")
    
    # Deduplicate (accepted wins)
    seen_names = {p.name for p in accepted_products}
    unique_all = [p for p in all_products if p.name not in seen_names]
    products = accepted_products + unique_all
    
    print(f"✅ Parsed {len(products)} unique products")
    print(f"   - {len(accepted_products)} from ACCEPTED")
    print(f"   - {len(unique_all)} from ALL")
    
    # Verify URLs
    print("\n🔍 Verifying URLs...")
    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    verified_count = 0
    
    for i, prod in enumerate(products, 1):
        if i % 5 == 0:
            print(f"   Checked {i}/{len(products)}...")
        prod.verified = verify_url(prod.destination_url)
        prod.last_checked = now
        if prod.verified:
            verified_count += 1
    
    print(f"✅ Verified {verified_count}/{len(products)} URLs\n")
    
    # Group by category
    by_category: Dict[str, List[Dict]] = {}
    for prod in products:
        cat = prod.category or "Uncategorized"
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(asdict(prod))
    
    # Build database
    database = {
        "meta": {
            "generated": now,
            "total_products": len(products),
            "verified_products": verified_count,
            "categories": len(by_category),
            "sources": ["MASTER-PRODUCTS-LIST.ACCEPTED.md", "MASTER-PRODUCTS-LIST.md"]
        },
        "by_category": by_category,
        "all_products": [asdict(p) for p in products]
    }
    
    return database


def main() -> None:
    """Build and save affiliate database"""
    database = build_database()
    
    # Save JSON
    OUTPUT_JSON.write_text(json.dumps(database, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"💾 Saved to {OUTPUT_JSON.relative_to(ROOT)}")
    
    # Print summary
    print(f"\n📊 Database summary:")
    print(f"   Total products: {database['meta']['total_products']}")
    print(f"   Verified URLs: {database['meta']['verified_products']}")
    print(f"   Categories: {database['meta']['categories']}")
    print(f"\n📂 Categories:")
    for cat, items in sorted(database['by_category'].items()):
        verified = sum(1 for item in items if item['verified'])
        print(f"   - {cat}: {len(items)} products ({verified} verified)")


if __name__ == "__main__":
    main()
