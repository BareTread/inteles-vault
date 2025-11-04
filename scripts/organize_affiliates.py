#!/usr/bin/env python3
"""
Organize approved affiliates from 04-Monetization/affiliates.csv into JSON groups.

Outputs:
  - 04-Monetization/affiliates.json

Notes:
  - Robust commission parsing (handles ranges like "8-30", decimals, words like "Varies/Variable")
  - Sorts each category by highest commission value detected
  - Idempotent and safe to re-run
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Dict, Any


CSV_PATH = Path("04-Monetization/affiliates.csv")
OUT_PATH = Path("04-Monetization/affiliates.json")


def parse_commission_to_float(value: str | None) -> float:
    if not value:
        return 0.0
    s = str(value).strip()
    # Find all numeric parts (supports ranges and decimals)
    nums = re.findall(r"\d+(?:\.\d+)?", s)
    if not nums:
        return 0.0
    try:
        # Use the maximum figure present (e.g. "8-30" -> 30.0)
        return max(float(n) for n in nums)
    except Exception:
        return 0.0


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"Missing {CSV_PATH}")

    affiliates: Dict[str, Dict[str, Any]] = {}
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("merchant_name") or "").strip()
            if not name:
                continue
            affiliates[name] = {
                "domain": (row.get("domain") or "").strip(),
                "status": (row.get("status") or "").strip(),
                "commission": (row.get("commission_percent") or "").strip(),
                "cookie_days": (row.get("cookie_days") or "").strip(),
                "category": (row.get("category") or "").strip(),
                "aov": (row.get("avg_order_value") or "").strip(),
                "conversion": (row.get("conversion_rate") or "").strip(),
                "target": (row.get("target_audience") or "").strip(),
                "approved": (row.get("approved_date") or "").strip(),
                "advantage": (row.get("key_advantage") or "").strip(),
                "restriction": (row.get("restriction") or "").strip(),
            }

    # Group by category
    by_category: Dict[str, list[Dict[str, Any]]] = {}
    for name, data in affiliates.items():
        cat = data.get("category") or "Uncategorized"
        by_category.setdefault(cat, []).append({"name": name, **data})

    # Sort each category by commission (highest numeric found first)
    for cat, items in by_category.items():
        items.sort(key=lambda x: parse_commission_to_float(x.get("commission")), reverse=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(
            {
                "total": len(affiliates),
                "by_category": by_category,
                "all": affiliates,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    cats = ", ".join(sorted(by_category.keys()))
    print(f"✅ Organized {len(affiliates)} merchants")
    print(f"Categories: {cats}")


if __name__ == "__main__":
    main()

