#!/usr/bin/env bash
set -euo pipefail

# One-click refresh of monetization assets using 2Performant credentials + CSV
# Prereq: .env with TWO_P_EMAIL, TWO_P_PASSWORD, TWO_P_AFF_CODE

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT_DIR/.venv/bin/python"

if [ ! -x "$VENV" ]; then
  echo "[!] Python venv not found at .venv. Please create it and install deps."
  echo "    python3 -m venv .venv && .venv/bin/python -m pip install -r scripts/twop/requirements.txt"
  exit 1
fi

echo "[1/5] Dump accepted programs from API"
"$VENV" scripts/twop/dump_programs.py

echo "[2/5] Generate curated quicklinks (auto)"
"$VENV" scripts/twop/fetch_and_build.py --out 04-Monetization/Auto-Generated-Affiliate-Links.md

echo "[3/5] Audit and build ACCEPTED master list + reports"
"$VENV" scripts/twop/audit_and_fix_affiliates.py

echo "[4/5] Filter additional guides to ACCEPTED variants"
"$VENV" scripts/twop/filter_md_by_csv.py 04-Monetization/Best-Opportunities.md 04-Monetization/Best-Opportunities.ACCEPTED.md --level 2 || true
"$VENV" scripts/twop/filter_md_by_csv.py 04-Monetization/Female-Audience-Picks.md 04-Monetization/Female-Audience-Picks.ACCEPTED.md --level 1 || true

echo "[5/5] Done. Use the ACCEPTED files for publishing:"
echo " - 04-Monetization/MASTER-PRODUCTS-LIST.ACCEPTED.md"
echo " - 04-Monetization/Approved-Merchant-Homepages.md"
echo " - 04-Monetization/Best-Opportunities.ACCEPTED.md (if exists)"
echo "Reports:"
echo " - 04-Monetization/Affiliate-Audit-Report.md"
echo " - 04-Monetization/CSV-API-Programs-Delta.md"
echo " - 04-Monetization/Vault-Wide-Affiliate-Audit.md"

