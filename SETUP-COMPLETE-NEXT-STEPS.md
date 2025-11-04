# ✅ Hybrid Workflow Setup — READY TO BUILD

**Status:** All configuration and prompts prepared. Ready for agent creation.

---

## 📦 What Was Created

### 1. `.claude/mcp.json` ✅
MCP server configuration for Claude Pro writer:
- Sets CLAUDE_WORK_DIR to absolute path (required for integration launches)
- Changes to working directory before serving
- Unsets API env vars so Claude Pro MCP uses your subscription
- Keeps GLM as the main orchestrator
- Located: `/home/alin/DATA/OBSIDIAN/inteles-vault/.claude/mcp.json`

**Research finding:** MCP servers launched via integration do NOT inherit cwd. You MUST set CLAUDE_WORK_DIR explicitly with absolute paths.

### 1b. `/home/alin/claude-pro-writer/` ✅
Working directory with essential Romanian writing context:
- `romanian-style.md` — Diacritics, tone, structure template
- `quality-checklist.md` — 10-point scoring rubric
- `avoid.md` — AI tells and anti-patterns to avoid
- Total: 4 files, ~5KB (ultra-lean, focused)

**See:** `MCP-WRITER-SETUP-FINAL.md` for complete details

### 2. `00-AGENT-CONTEXT/AGENT-CREATION-PROMPTS.md` ✅
Complete agent creation prompts with all context needed:
- **Writer Coordinator** — Calls Claude Pro MCP with perfect Romanian style context
- **Monetization Specialist** — Finds 2-3 products from MASTER-PRODUCTS-LIST
- **Image Curator** — Searches Pexels, generates Romanian alt/caption
- **Kadence Block Engineer** — Converts markdown to WordPress blocks
- **WordPress Publisher** — Publishes via WordPress MCP

Each prompt includes:
- Exact role and responsibilities
- All necessary context from vault files
- Input/output contracts
- Critical rules and guardrails
- No unnecessary information (lean and focused)

### 3. `HYBRID-WORKFLOW-SETUP.md` ✅
Complete setup and usage guide:
- Step-by-step setup instructions
- How to run the workflow
- Example conversation flow
- Cost estimates (~$0.048 per article)
- Troubleshooting section
- Performance monitoring tips

---

## 🎯 Immediate Next Steps

### Step 1: Create Agents (5-10 minutes)

Open **Global Claude Code** (not GLM):
```bash
# In any directory
claude
```

Inside Claude, type:
```
/agents
```

Then create each agent by copying the full system prompt from:
**`00-AGENT-CONTEXT/AGENT-CREATION-PROMPTS.md`**

Create in this order:
1. ✅ **writer-coordinator**
2. ✅ **monetization-specialist**
3. ✅ **image-curator**
4. ✅ **kadence-block-engineer**
5. ✅ **wordpress-publisher**

### Step 2: Move Agents to Vault (30 seconds)

```bash
# Create agents directory in vault
mkdir -p /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/

# Copy all agents from global to vault
cp ~/.claude/agents/writer-coordinator.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
cp ~/.claude/agents/monetization-specialist.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
cp ~/.claude/agents/image-curator.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
cp ~/.claude/agents/kadence-block-engineer.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
cp ~/.claude/agents/wordpress-publisher.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
```

### Step 3: Test GLM Instance (1 minute)

```bash
# Start GLM Claude in vault
cd /home/alin/DATA/OBSIDIAN/inteles-vault
claude
```

Inside GLM Claude:
```
/agents list
```

Should show all 5 agents.

```
/mcp
```

Should show:
- claude-pro-writer ✅
- inteles-wordpress ✅
- pexels-mcp-server ✅
- perplexity-ask ✅

### Step 4: Test Writer Coordinator (2 minutes)

```
@writer-coordinator Test connection to Claude Pro MCP. Call @claude-pro-writer with this simple prompt:

"Scrie 2 paragrafe în română despre semnificația viselor cu apă din perspectivă psihologică. Include diacritice. Maxim 150 cuvinte."

Return only the Romanian text generated, no analysis.
```

If this works, **you're golden**! 🎉

### Step 5: Run First Full Workflow (15 minutes)

Follow the example in `HYBRID-WORKFLOW-SETUP.md` section "Typical Workflow":
- Research topic
- Call writer-coordinator
- Call monetization-specialist + image-curator in parallel
- Call kadence-block-engineer
- Call wordpress-publisher

---

## 📊 Expected Results

### Token Usage Per Article
- **Claude Pro MCP (writer):** ~8K tokens → $0 (covered by subscription)
- **GLM (all other agents):** ~16K tokens → ~$0.048

### Quality Targets
- SEO Score: ≥80/100
- Romanian quality: Native-level with diacritics
- Mobile UX: Optimized
- Monetization: 2-3 contextual links max
- Images: 2-4 relevant, WebP optimized

### Speed
- First article (learning): ~30 minutes
- Subsequent articles: ~15-20 minutes
- Parallel processing: 10-15 articles per day possible

---

## 🎓 Learning Resources

**Essential Files to Reference:**
- `00-AGENT-CONTEXT/AGENT-CREATION-PROMPTS.md` — Agent specs
- `HYBRID-WORKFLOW-SETUP.md` — Complete guide
- `SOP.md` — Content philosophy and style
- `04-Monetization/MASTER-PRODUCTS-LIST.md` — All products
- `00-AGENT-CONTEXT/04-SEO-RUBRIC.md` — Quality checklist

**Quick Reference:**
- `00-Quick-Reference.md` — One-line commands
- `START-HERE.md` — Writer agent guide

---

## 🚨 Critical Reminders

### For Claude Pro MCP
- ✅ MCP server automatically unsets API keys (via mcp.json config)
- ✅ Uses your Pro subscription (no extra API costs)
- ✅ Only called for Romanian writing (minimal token usage)
- ✅ Returns compact output (no context pollution)

### For Agent Creation
- ✅ Create with Global Claude (best quality)
- ✅ Copy full system prompt exactly (includes all context)
- ✅ Name exactly as specified (agents reference each other)
- ✅ Move to vault after creation

### For Workflow Execution
- ✅ Run in vault directory (GLM auto-loads)
- ✅ Keep outputs compact (avoid context bloat)
- ✅ Verify each step before proceeding
- ✅ Monitor token usage and costs

---

## ✅ Checklist

Before starting agent creation, verify:
- [ ] `.claude/mcp.json` exists in vault
- [ ] `.claude/settings.json` has GLM configuration
- [ ] Global Claude Code is working (test with `claude --version`)
- [ ] MCP servers are configured (WordPress, Pexels, Perplexity)
- [ ] You have access to both Global and GLM Claude instances

After creating agents, verify:
- [ ] All 5 agent .json files in vault `.claude/agents/` directory
- [ ] `/agents list` shows all 5 agents in GLM instance
- [ ] `/mcp` shows claude-pro-writer server in GLM instance
- [ ] Test writer-coordinator successfully calls Claude Pro MCP

Ready to scale:
- [ ] First article completed successfully
- [ ] Cost tracking set up (optional but recommended)
- [ ] Workflow documented with any custom tweaks
- [ ] Team trained (if applicable)

---

## 🎉 You're Ready!

**Your vault is perfectly set up.** All context is organized, all prompts are prepared, and the architecture is sound.

**Next action:** Start creating those 5 agents in Global Claude Code using the prompts from `AGENT-CREATION-PROMPTS.md`.

**Estimated time to first article:** 30 minutes (including agent creation and testing).

---

**Questions or issues?** Check `HYBRID-WORKFLOW-SETUP.md` troubleshooting section.

**Good luck!** 🚀
