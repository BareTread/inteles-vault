# 🚀 Hybrid Workflow Setup — Claude Pro + GLM

Complete setup guide for dual-instance architecture with sub-agents.

---

## ✅ What You Already Have

- ✅ Global Claude Code (Pro) — works anywhere
- ✅ GLM Claude Code in vault — auto-loads GLM models
- ✅ MCP servers configured (WordPress, Pexels, Perplexity)
- ✅ `.claude/mcp.json` — Claude Pro MCP server config
- ✅ Agent prompts ready in `00-AGENT-CONTEXT/AGENT-CREATION-PROMPTS.md`

---

## 🔧 Setup Steps

### Step 1: Create Agents (Use Global Claude Pro)

**Why Global Claude?** Create agents with Sonnet for best quality, then move them to vault for GLM execution.

```bash
# Terminal 1 - Start global Claude Code
claude
```

Inside Claude, type `/agents` and create each agent using the prompts from:
`00-AGENT-CONTEXT/AGENT-CREATION-PROMPTS.md`

Create these 5 agents in order:
1. **writer-coordinator** — Calls Claude Pro MCP for Romanian content
2. **monetization-specialist** — Finds affiliate products
3. **image-curator** — Finds Pexels images
4. **kadence-block-engineer** — Converts to WordPress HTML
5. **wordpress-publisher** — Publishes via WordPress MCP

### Step 2: Move Agents to Vault

```bash
# After creating all agents in global Claude
mkdir -p /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/

# Copy agents
cp ~/.claude/agents/writer-coordinator.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
cp ~/.claude/agents/monetization-specialist.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
cp ~/.claude/agents/image-curator.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
cp ~/.claude/agents/kadence-block-engineer.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
cp ~/.claude/agents/wordpress-publisher.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
```

### Step 3: Verify MCP Configuration

Check that `.claude/mcp.json` exists:

```bash
cat /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/mcp.json
```

Should show:
```json
{
  "mcpServers": {
    "claude-pro-writer": {
      "command": "bash",
      "args": ["-lc", "env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN claude mcp serve"],
      "description": "Claude Pro MCP server for premium Romanian writing"
    }
  }
}
```

---

## 🏃 Running the Workflow

### Terminal Setup (2 Terminals)

**Terminal 1: Claude Pro MCP Server** (optional if using mcp.json config)
```bash
# If you want to run manually for debugging
unset ANTHROPIC_API_KEY ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN
claude mcp serve
```

**Terminal 2: GLM Orchestrator**
```bash
cd /home/alin/DATA/OBSIDIAN/inteles-vault
claude
```

### Inside GLM Claude Code

1. **Verify agents loaded:**
   ```
   /agents list
   ```
   Should show all 5 agents.

2. **Verify MCP servers:**
   ```
   /mcp
   ```
   Should show:
   - claude-pro-writer (via mcp.json)
   - inteles-wordpress
   - pexels-mcp-server
   - perplexity-ask

3. **Test writer coordinator:**
   ```
   @writer-coordinator I need you to test the connection to Claude Pro MCP. Try calling @claude-pro-writer with a simple test prompt.
   ```

---

## 📝 Typical Workflow

### 1. Research Phase (Manual or Perplexity)

Gather insights for the article:
- Topic: "Ce înseamnă când visezi șerpi"
- Keywords: vise, șerpi, psihologie, Jung, simboluri
- Key insights: transformare, vindecarea, înțelepciune, teamă

### 2. Call Writer Coordinator

```
@writer-coordinator Write article about "ce înseamnă când visezi șerpi"

Input:
{
  "topic": "Ce înseamnă când visezi șerpi - Interpretare și semnificație",
  "keywords": ["vise", "șerpi", "interpretare", "Jung", "simboluri"],
  "outline": [
    "Introducere: Semnificația viselor cu șerpi",
    "Perspectivă psihologică: Jung și simbolismul șarpelui",
    "Scenarii comune: șarpe negru, verde, care mușcă",
    "Context cultural românesc",
    "Resurse pentru aprofundare",
    "FAQ",
    "Concluzie"
  ],
  "insights": [
    "Șarpele în psihologia jungiană reprezintă transformare și vindecarea",
    "Culoarea șarpelui modifică interpretarea",
    "Contextul emoțional din vis e crucial",
    "Legătură cu inconștientul colectiv"
  ]
}
```

### 3. Parallel Processing

**Get products:**
```
@monetization-specialist Find products for article about dream interpretation with snakes

Input:
{
  "keywords": ["vise", "Jung", "interpretare", "psihologie"],
  "topic": "Ce înseamnă când visezi șerpi",
  "article_context": "Interpretare psihologică a viselor cu șerpi din perspectivă jungiană"
}
```

**Get images:**
```
@image-curator Find images for snake dream article

Input:
{
  "title": "Ce înseamnă când visezi șerpi",
  "keywords": ["snake", "psychology", "dream", "transformation"],
  "topic_context": "Articol despre interpretarea psihologică a viselor cu șerpi"
}
```

### 4. Assemble HTML

```
@kadence-block-engineer Convert content to Kadence blocks

Input:
{
  "markdown": "[content from writer-coordinator]",
  "products": "[products from monetization-specialist]",
  "images": "[images from image-curator]",
  "title": "Ce înseamnă când visezi șerpi",
  "excerpt": "[excerpt from writer-coordinator]"
}
```

### 5. Publish to WordPress

```
@wordpress-publisher Publish the article

Input:
{
  "title": "Ce înseamnă când visezi șerpi — Interpretare și semnificație",
  "slug": "ce-inseamna-cand-visezi-serpi",
  "html": "[HTML from kadence-block-engineer]",
  "images": "[images array]",
  "excerpt": "[excerpt text]",
  "keywords": ["vise", "șerpi", "interpretare", "Jung"],
  "update_existing": false
}
```

---

## 💰 Cost Estimate Per Article

| Component | Model | Tokens | Cost |
|-----------|-------|--------|------|
| Writer (Romanian content) | Claude Pro via MCP | ~8K | $0 (Pro) |
| Research + Coordination | GLM-4.6 | ~5K | ~$0.015 |
| Monetization | GLM-4.6 | ~2K | ~$0.006 |
| Images | GLM-4.6 | ~3K | ~$0.009 |
| Blocks | GLM-4.6 | ~4K | ~$0.012 |
| Publisher | GLM-4.6 | ~2K | ~$0.006 |
| **Total** | | **~24K** | **~$0.048** |

**vs Claude Pro alone:** Would hit daily limits after 2-3 articles
**With hybrid:** Can process 10-15 articles per day at ~$0.50 total

---

## 🔍 Troubleshooting

### Claude Pro MCP Not Working

**Symptom:** `@claude-pro-writer` not available

**Fix:**
```bash
# Check mcp.json exists
ls -la /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/mcp.json

# Test manual MCP server
unset ANTHROPIC_API_KEY ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN
claude mcp serve
# Should start without errors
```

### Agents Not Loading

**Symptom:** `/agents list` shows empty

**Fix:**
```bash
# Check agents directory
ls -la /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/

# Should have 5 .json files
# If missing, copy from global Claude
cp ~/.claude/agents/*.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
```

### GLM Not Loading in Vault

**Symptom:** Still using Claude Pro models

**Fix:**
```bash
# Check settings.json
cat /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/settings.json

# Should have ANTHROPIC_API_KEY and ANTHROPIC_BASE_URL set to GLM
# Verify by checking model in Claude Code prompt
```

### MCP Servers Not Connecting

**Symptom:** `/mcp` shows servers as "stopped"

**Fix:**
```bash
# Run Claude debug mode
cd /home/alin/DATA/OBSIDIAN/inteles-vault
claude --debug

# Check logs
tail -f ~/.claude/debug.log

# Common issues:
# - Missing node_modules (run: npm install in MCP server dir)
# - Wrong paths in config
# - Missing API keys in environment
```

---

## 📊 Monitoring & Optimization

### Track Performance

Create a simple log file:
```bash
echo "Date,Article,Writer_Tokens,GLM_Tokens,Total_Cost" > workflow-log.csv
```

After each article:
```bash
echo "2025-11-03,serpi,8000,16000,0.048" >> workflow-log.csv
```

### Optimize Token Usage

**Writer Coordinator:**
- Keep prompts tight (no verbose instructions)
- Return only content, not analysis
- Use outline structure to guide

**Other Agents:**
- Read only necessary context files
- Return structured JSON, not prose
- Avoid re-reading same files

**Total Session:**
- Clear context between articles if needed
- Use `/reset` to start fresh session

---

## 🎯 Success Metrics

After 10 articles, you should see:
- ✅ Average cost: $0.03-0.05 per article
- ✅ Pro limits: Not hit (only ~8K tokens per article)
- ✅ Quality: Equal to full Claude Pro articles
- ✅ Speed: 15-20 minutes per article (including research)
- ✅ Consistency: All articles follow style guide

---

## 🚀 Next Steps

1. ✅ Create all 5 agents in global Claude
2. ✅ Move agents to vault
3. ✅ Test each agent individually
4. ✅ Run first full workflow
5. ✅ Monitor costs and optimize
6. ✅ Scale to 10-15 articles per day

---

**Questions?** Check:
- `00-AGENT-CONTEXT/AGENT-CREATION-PROMPTS.md` — Agent specs
- `VAULT-AUDIT-COMPLETE.md` — Vault structure
- `SOP.md` — Content philosophy
- `START-HERE.md` — Quick reference
