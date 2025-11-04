#!/bin/bash
# Clean up 04-Monetization/ bloat - keep only 8 essential files
set -e

MONETIZATION_DIR="04-Monetization"
cd "$(dirname "$0")/.."

echo "🧹 Cleaning up ${MONETIZATION_DIR}/"
echo ""

# Create archive directory
mkdir -p "${MONETIZATION_DIR}/.archive"

# Archive large dumps
echo "📦 Archiving large JSON dumps..."
[ -f "${MONETIZATION_DIR}/.archive-programs-dump.json" ] && mv "${MONETIZATION_DIR}/.archive-programs-dump.json" "${MONETIZATION_DIR}/.archive/" 2>/dev/null || true
[ -f "${MONETIZATION_DIR}/Programs-Dump.json" ] && mv "${MONETIZATION_DIR}/Programs-Dump.json" "${MONETIZATION_DIR}/.archive/" 2>/dev/null || true

# Delete generated outputs
echo "🗑️  Removing generated outputs..."
rm -f "${MONETIZATION_DIR}/AI-AGENT-QUICK-PICKS.md"
rm -f "${MONETIZATION_DIR}/Affiliate-Audit-Report.md"
rm -f "${MONETIZATION_DIR}/Affiliate-Links-Quicklist.md"
rm -f "${MONETIZATION_DIR}/Auto-Generated-Affiliate-Links.md"
rm -f "${MONETIZATION_DIR}/Category-Packs.md"
rm -rf "${MONETIZATION_DIR}/category-packs/"

# Delete redundant indexes
echo "🗑️  Removing redundant indexes..."
rm -f "${MONETIZATION_DIR}/Affiliate-Programs-Index.md"
rm -f "${MONETIZATION_DIR}/Best-Opportunities.md"
rm -f "${MONETIZATION_DIR}/Best-Opportunities.ACCEPTED.md"
rm -f "${MONETIZATION_DIR}/CSV-API-Programs-Delta.md"
rm -f "${MONETIZATION_DIR}/Female-Audience-Picks.md"
rm -f "${MONETIZATION_DIR}/Female-Audience-Picks.ACCEPTED.md"
rm -f "${MONETIZATION_DIR}/High-ROI-Merchants.md"
rm -f "${MONETIZATION_DIR}/MERCHANT-HOMEPAGES.md"
rm -f "${MONETIZATION_DIR}/Opportunity-Matrix.md"
rm -f "${MONETIZATION_DIR}/PRODUCT-URLS.md"
rm -f "${MONETIZATION_DIR}/Product-Mapping.md"

# Delete testing artifacts
echo "🗑️  Removing testing artifacts..."
rm -f "${MONETIZATION_DIR}/LINK2-SETUP-TEST.md"
rm -f "${MONETIZATION_DIR}/LINK2-VERIFICATION-CHECKLIST.md"
rm -f "${MONETIZATION_DIR}/SETUP-COMPLETE.md"
rm -f "${MONETIZATION_DIR}/Unique-Tagging-Guide.md"
rm -f "${MONETIZATION_DIR}/Vault-Wide-Affiliate-Audit.md"

# Delete temp outputs
echo "🗑️  Removing temporary outputs..."
rm -f "${MONETIZATION_DIR}"/resource-box.*.html
rm -f "${MONETIZATION_DIR}"/selected-products.*.json
rm -f "${MONETIZATION_DIR}/curated-products.SAMPLE.csv"

# Archive old README
echo "📦 Archiving old README..."
[ -f "${MONETIZATION_DIR}/README.md" ] && mv "${MONETIZATION_DIR}/README.md" "${MONETIZATION_DIR}/.archive/README.old.md" 2>/dev/null || true

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Remaining files:"
ls -1 "${MONETIZATION_DIR}" | grep -v "^\.archive$" | wc -l
echo ""
echo "📁 Essential files kept:"
ls -1 "${MONETIZATION_DIR}" | grep -v "^\.archive$"
echo ""
echo "💾 Archived files:"
ls -1 "${MONETIZATION_DIR}/.archive/" 2>/dev/null | wc -l
echo ""
