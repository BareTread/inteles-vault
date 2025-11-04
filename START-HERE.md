# 🚀 START HERE - Production Agent System

**Status:** ✅ AGENT-IN-AGENT MCP WORKING!  
**Date:** 2025-11-03  
**System:** Intelligent orchestration with Claude Pro writer

---

## ⚡ Quick Start

### First Time Setup
```bash
cd /home/alin/DATA/OBSIDIAN/inteles-vault
chmod +x setup-agent-in-agent.sh
./setup-agent-in-agent.sh
```

### Daily Workflow
```bash
cd /home/alin/DATA/OBSIDIAN/inteles-vault
claude

# Verify MCP servers
/mcp

# Write article (one command)
@research-orchestrator Write article about "Ce înseamnă când visezi șerpi"
```

---

## 📚 Essential Documentation

| File | Purpose |
|------|---------|
| **`FINAL-SOLUTION-SUMMARY.md`** | ⭐ Read this first - the breakthrough |
| **`00-AGENT-CONTEXT/AGENTS-FINAL-INTELLIGENT.md`** | ⭐ Agent prompts - copy to create agents |
| **`QUICK-START-AGENT-IN-AGENT.md`** | Daily workflow reference |
| **`SOLUTION-AGENT-IN-AGENT.md`** | Technical deep dive |
| **`SOP.md`** | Content philosophy |
| **`AGENTS.md`** | Coding guidelines |

---

## 🎯 The 5 Intelligent Agents

### 1. Research-Orchestrator ⭐
**Access:** Perplexity MCP + Claude Code Writer MCP  
**Intelligence:**
- 3-4 targeted Perplexity queries (psychology + SEO gaps + culture + practical)
- Synthesizes specific insights (not generic)
- Builds ONE perfect prompt with all research embedded
- Calls Claude Pro writer via MCP
- Returns compact JSON (no article reposting)

### 2. Monetization-Specialist
**Access:** Product catalog + URL verification  
**Intelligence:**
- Reads MASTER-PRODUCTS-LIST intelligently
- Matches by theme, not just keywords
- Verifies all URLs live with curl
- Max 2-3 products, diverse merchants
- Returns verified products + HTML box

### 3. Image-Curator  
**Access:** Pexels MCP  
**Intelligence:**
- Searches with psychology keywords (English)
- Selects for visual consistency
- Generates Romanian alt text with diacritics
- Includes photographer credit
- Suggests strategic placement

### 4. Kadence-Block-Engineer
**Access:** Templates  
**Intelligence:**
- Converts markdown → WordPress Kadence blocks
- Inserts images at strategic points
- Adds affiliate box before FAQ
- Proper schema.org markup for FAQ
- Mobile-optimized HTML

### 5. WordPress-Publisher
**Access:** WordPress MCP  
**Intelligence:**
- Checks for existing posts (idempotent)
- Uploads images with Romanian metadata
- Sets category 5 automatically
- Updates or creates as needed
- Returns live URL

---

## 🔥 Why This Works

### The Breakthrough
**Community MCP server** (`steipete/claude-code-mcp`) exposes `claude_code` tool:
- Takes prompt → spawns Claude CLI → returns LLM text
- Claude CLI uses **Pro subscription** (no API billing)
- Fully automated, no manual steps

### Architecture
```
GLM Orchestrator (cheap API tokens)
    ↓
Research-Orchestrator
├─ Perplexity research (3-4 queries)
├─ Build intelligent prompt
└─ Call @claude-code-writer MCP
    ↓
    Claude Pro (Pro subscription)
    Generates Romanian article
    ↓
    Returns Markdown to GLM
    ↓
[Parallel: Monetization + Images]
    ↓
Kadence Blocks
    ↓
WordPress Publish
```

### Cost Per Article
- Claude Pro: ~8K tokens → **$0 (subscription)**
- GLM: ~16K tokens → **~$0.04-0.05**
- **Total:** ~$0.04-0.05 per article

### Capacity
- **10-15 articles/day** within Pro limits
- **Batch:** 5 articles in 60-75 minutes
- **Quality:** Native Romanian, SEO-optimized

---

## 📋 Critical Rules

### Romanian Quality (Non-Negotiable)
✓ Diacritice: ă, î, â, ș, ț (pe tot)  
✓ Paragrafe scurte: 2-3 propoziții max  
✓ Quick answer în primele 2-3 paragrafe  
✓ Ton: empatic, profesional, tu form  

### Structure (SEO-Optimized)
✓ H2/H3 la fiecare 300-400 cuvinte  
✓ FAQ: minim 6 întrebări cu schema  
✓ Imagini: 2-3 cu alt text românesc  
✓ Lungime: 900-1200 cuvinte (no hard limit, let Claude decide)

### Monetization (Proven Formula)
✓ Max 2-3 produse afiliate  
✓ Disclosure: "Link afiliat — câștigăm un mic comision fără costuri pentru tine"  
✓ rel="nofollow sponsored noopener"  
✓ Plasare naturală, nu forțată

### AI Tells (Zero Tolerance)
❌ "În concluzie, putem spune..."  
❌ "Este important de menționat..."  
❌ "delve", "utilize", "it's important to note"  
❌ Em-dashes excesive  

---

## 🎓 Quality Scoring (Target: 8+/10)

1. **Intent Match** - Quick answer first  
2. **Depth** - Real psychological insights  
3. **Structure** - H2/H3, scurte paragrafe  
4. **Length** - 900-1200w, no filler  
5. **Mobile** - Easy scanning  
6. **Credibility** - Cite sources  
7. **Language** - Perfect diacritics  
8. **Value** - Genuinely helpful  
9. **SEO** - Natural keywords  
10. **Polish** - No errors  

---

## 🚀 Complete Workflow Example

```
Task: "Ce înseamnă când visezi șerpi"

Step 1: Start GLM in vault
$ cd /home/alin/DATA/OBSIDIAN/inteles-vault
$ claude

Step 2: Call research-orchestrator
> @research-orchestrator Write comprehensive article about "Ce înseamnă când visezi șerpi - Interpretare psihologică"

[Agent executes automatically:]

2a) Perplexity research:
- Query 1: "snake dreams Jung Freud psychology symbolism"
- Query 2: "Romanian dream interpretation snake serpent culture"
- Query 3: "snake dreams SEO content gaps competitors"
- Query 4: "snake symbolism practical psychology therapeutic"

2b) Synthesize insights:
- Jung: snake = transformation, healing, primordial energy
- Freud: sexual symbolism, repressed desires
- Romanian culture: snake = wisdom, danger, warning
- SEO gap: lack of practical therapeutic approaches
- PAA questions identified: 6+ common questions

2c) Build intelligent prompt:
"Citește /home/alin/claude-pro-writer/romanian-style.md + avoid.md

Scrie articol 1000+ cuvinte: 'Ce înseamnă când visezi șerpi'

PERSPECTIVE PSIHOLOGICĂ:
- Jung: șarpele simbolizează transformare și energia vitală primordială
- În mitologie universală: înțelepciune, vindecare, reînnoire
- Context emoțional crucial: teamă vs fascinație

UNGHIURI UNICE:
- Leg ătura cu procesul de individuare (Jung)
- Diferența dintre șarpe negru (inconștient) și șarpe verde (vindecare)
- Context românesc: credințe populare vs interpretare modernă

STRUCTURĂ:
1. Intro + quick answer (2-3 paragrafe)
2. Semnificație psihologică (Jung/Freud)
3. Scenarii comune (negru, verde, care mușcă, șarpe mort)
4. Context românesc
5. Când să cauți ajutor profesional
6. FAQ (6+ întrebări)
7. Concluzie acționabilă

REGULI:
✓ Diacritice pe tot
✓ Paragrafe 2-3 propoziții
✓ H2/H3 la 300-400w
✓ Zero AI tells
✓ Ton empatic, tu form
✓ Quick answer FIRST

OUTPUT: Doar Markdown, nimic altceva.
---
Excerpt: [25-35 cuvinte]
Keywords: [listă]
---"

2d) Call Claude Pro writer via MCP:
{
  "prompt": "[intelligent prompt above]",
  "workFolder": "/home/alin/claude-pro-writer"
}

2e) Receive article:
Article returned in Markdown with perfect Romanian

2f) Extract & pass forward (compact JSON):
{
  "article_markdown": "# Title\n\n[full article]",
  "excerpt": "...",
  "keywords": ["vise", "șerpi", ...],
  "slug": "ce-inseamna-cand-visezi-serpi"
}

Step 3: Parallel processing (automatic)

3a) Monetization:
- Finds "Omul și simbolurile sale" (Jung) - Libris 8%
- Finds "Interpretarea viselor" (Freud) - Bookzone 8%
- Verifies URLs live
- Builds HTML affiliate box

3b) Images:
- Searches Pexels: "snake symbolic", "dream psychology"
- Selects 3 consistent images
- Generates Romanian alt text
- Maps placement points

Step 4: Assemble Kadence blocks
- Converts markdown to Kadence HTML
- Inserts hero image after title
- Places 2 inline images strategically
- Adds affiliate box before FAQ
- FAQ with schema.org markup

Step 5: Publish to WordPress
- Uploads 3 images with Romanian metadata
- Creates post in category 5
- Sets featured image
- Status: publish

Done! Live at: https://inteles.ro/ce-inseamna-cand-visezi-serpi

Time: ~15-20 minutes
Cost: ~$0.04
Quality: Native Romanian, SEO-ready
```

---

## 🔧 Troubleshooting

### "MCP not connected"
```bash
/mcp  # Check status
# If claude-code-writer shows stopped, restart session
```

### "No diacritics"
Add to prompt: "MANDATORY: ă, î, â, ș, ț pe tot textul"

### "Text looks fake"
Wrong MCP server. Check `.mcp.json`:
- ✅ GOOD: `"command": "node", "args": ["/home/alin/claude-code-mcp/build/index.js"]`
- ❌ BAD: `"command": "claude", "args": ["mcp", "serve"]`

---

## 📊 Key Resources

### Content Context
- **Philosophy:** `SOP.md`
- **Style Rules:** `00-AGENT-CONTEXT/07-STYLE-GUARDRAILS.md`
- **SEO Rubric:** `00-AGENT-CONTEXT/04-SEO-RUBRIC.md`
- **Writing Rubric:** `00-AGENT-CONTEXT/02-WRITING-RUBRIC.md`

### Operations
- **Products:** `04-Monetization/MASTER-PRODUCTS-LIST.md`
- **Pexels:** `03-MCP-Operations/MCP-Pexels-Workflow.md`
- **WordPress:** `03-MCP-Operations/MCP-WordPress-Guide.md`

### Templates
- **HTML Templates:** `07-Templates/`
- **Article Brief:** `00-AGENT-CONTEXT/06-ARTICLE-BRIEF-TEMPLATE.md`

---

## 💡 Pro Tips

### Token Optimization
- Research-orchestrator returns compact JSON only
- Don't repost full articles in chat
- Use `/reset` between large batches

### Quality Optimization
- Track which SEO angles convert best
- Iterate on research-orchestrator prompts
- Maintain product list (verify quarterly)

### Batch Processing
1. Research 5 topics → save briefs
2. Write all 5 (parallel MCP calls possible)
3. Process monetization/images bulk
4. Assemble all blocks
5. Publish batch

**Time:** ~60-75 min for 5 articles

---

## ✅ You're Ready!

**Setup complete?**
- [x] Ran `setup-agent-in-agent.sh`
- [x] MCP test successful (Romanian sentence worked)
- [ ] Created 5 agents from `AGENTS-FINAL-INTELLIGENT.md`
- [ ] Wrote first test article

**Next:** Copy agent prompts and create them in Global Claude:
```bash
claude  # Global instance
/agents  # Create new agent
# Copy prompt from AGENTS-FINAL-INTELLIGENT.md
```

Then move to vault:
```bash
cp ~/.claude/agents/*.json /home/alin/DATA/OBSIDIAN/inteles-vault/.claude/agents/
```

**You're ready to scale to 10-15 articles/day!** 🚀
