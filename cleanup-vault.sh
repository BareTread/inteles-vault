#!/bin/bash
set -e

echo "🧹 Cleaning up vault bloat..."

# Create archive directory
mkdir -p _archive-old-docs
mkdir -p _archive-old-docs/obsolete-setup-docs

# Move obsolete setup docs
echo "📦 Archiving obsolete setup documentation..."
mv -v HYBRID-WORKFLOW-SETUP.md _archive-old-docs/obsolete-setup-docs/ 2>/dev/null || true
mv -v MCP-WRITER-SETUP-FINAL.md _archive-old-docs/obsolete-setup-docs/ 2>/dev/null || true
mv -v SETUP-COMPLETE-NEXT-STEPS.md _archive-old-docs/obsolete-setup-docs/ 2>/dev/null || true
mv -v VAULT-AUDIT-COMPLETE.md _archive-old-docs/obsolete-setup-docs/ 2>/dev/null || true
mv -v VAULT-OPTIMIZATION-COMPLETE.md _archive-old-docs/obsolete-setup-docs/ 2>/dev/null || true

# Move old workflow docs
echo "📦 Archiving old workflow documentation..."
mv -v AI-AGENT-WORKFLOW.md _archive-old-docs/ 2>/dev/null || true
mv -v CLAUDE.md _archive-old-docs/ 2>/dev/null || true
mv -v GEMINI.md _archive-old-docs/ 2>/dev/null || true
mv -v SUCCESS-GUARANTEE.md _archive-old-docs/ 2>/dev/null || true
mv -v 🎯-SOP-BRILLIANCE.md _archive-old-docs/ 2>/dev/null || true
mv -v 🎯-WRITER-AGENT-READY.md _archive-old-docs/ 2>/dev/null || true

# Move old files
echo "📦 Archiving old backup files..."
mv -v .archive-old-sop.md _archive-old-docs/ 2>/dev/null || true
mv -v mcp.json _archive-old-docs/ 2>/dev/null || true
mv -v .mcp.json.backup _archive-old-docs/ 2>/dev/null || true

# Compress large history file
if [ -f "history.md" ]; then
    echo "📦 Compressing history.md..."
    gzip -9 history.md
    mv history.md.gz _archive-old-docs/
fi

# Summary
echo ""
echo "=========================================="
echo "✅ Cleanup complete!"
echo "=========================================="
echo ""
echo "Archived files moved to: _archive-old-docs/"
echo ""
echo "Current vault structure:"
echo "├── FINAL-SOLUTION-SUMMARY.md (START HERE)"
echo "├── SOLUTION-AGENT-IN-AGENT.md (technical guide)"
echo "├── QUICK-START-AGENT-IN-AGENT.md (daily workflow)"
echo "├── setup-agent-in-agent.sh (one-time setup)"
echo "├── 00-AGENT-CONTEXT/"
echo "│   └── AGENTS-FINAL-INTELLIGENT.md (NEW! production agents)"
echo "├── SOP.md (content philosophy)"
echo "├── START-HERE.md (entry point)"
echo "├── AGENTS.md (coding guidelines)"
echo "└── [numbered folders] (actual content)"
echo ""
echo "To restore archived files if needed:"
echo "  cp _archive-old-docs/[file] ./"
echo ""
