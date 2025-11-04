# ✅ REAL SOLUTION: Agent-in-Agent with Claude Code MCP

**Problem Solved:** You were using the wrong MCP server. There are TWO Claude Code MCP implementations.

---

## The Confusion

### ❌ What You Tested: `claude mcp serve` (Official Anthropic)

**Capabilities:**
- File operations (read, write, list)
- Command execution (bash)
- **NO LLM text generation**

**Why it failed:**
- When you asked it to "write a sentence in Romanian", GLM just used local `echo` to fake it
- This server is for workspace automation, not LLM calls

### ✅ What You Need: `steipete/claude-code-mcp` or `grahama1970/claude-code-mcp-enhanced`

**Capabilities:**
- **`claude_code` tool** that takes a prompt and returns LLM-generated text
- Executes Claude Code CLI with `--dangerously-skip-permissions`
- **TRUE agent-in-agent automation**

**How it works:**
```json
{
  "tool": "claude_code",
  "arguments": {
    "prompt": "Scrie 3 paragrafe în română despre semnificația viselor cu apă. Include diacritice. Ton empatic. 200 cuvinte.",
    "workFolder": "/home/alin/claude-pro-writer"
  }
}
```

Claude Code executes this prompt and returns the Romanian text!

---

## Complete Setup

### Step 1: Install the Right MCP Server

**Option A: steipete/claude-code-mcp** (simpler, proven)
```bash
cd /home/alin
git clone https://github.com/steipete/claude-code-mcp.git
cd claude-code-mcp
npm install
npm run build
```

**Option B: grahama1970/claude-code-mcp-enhanced** (more features)
```bash
cd /home/alin
git clone https://github.com/grahama1970/claude-code-mcp-enhanced.git
cd claude-code-mcp-enhanced
npm install
npm run build
```

### Step 2: Configure MCP in GLM Vault

**Edit `/home/alin/DATA/OBSIDIAN/inteles-vault/.mcp.json`:**

```json
{
  "mcpServers": {
    "claude-code-writer": {
      "command": "node",
      "args": [
        "/home/alin/claude-code-mcp/build/index.js"
      ],
      "env": {
        "CLAUDE_CLI_PATH": "/home/alin/.local/bin/claude",
        "CLAUDE_WORK_DIR": "/home/alin/claude-pro-writer"
      },
      "description": "Claude Code as agent-in-agent for Pro writing"
    },
    "inteles-wordpress": {
      "command": "npx",
      "args": ["-y", "@instawp/mcp-wp"],
      "env": {
        "WORDPRESS_URL": "https://inteles.ro",
        "WORDPRESS_USERNAME": "${WORDPRESS_USERNAME}",
        "WORDPRESS_APP_PASSWORD": "${WORDPRESS_APP_PASSWORD}"
      }
    },
    "pexels-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@CaullenOmdahl/pexels-mcp-server",
        "--key",
        "${PEXELS_API_KEY}"
      ]
    },
    "perplexity-ask": {
      "command": "npx",
      "args": ["-y", "server-perplexity-ask"],
      "env": {
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
      }
    }
  }
}
```

### Step 3: Accept Permissions (One-Time)

**Run Claude Code once with skip permissions:**
```bash
cd /home/alin/claude-pro-writer
unset ANTHROPIC_API_KEY ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN
claude --dangerously-skip-permissions
```

Type "yes" when prompted to accept. Then exit.

### Step 4: Create Writer Context

**Already done!** You have:
- `/home/alin/claude-pro-writer/romanian-style.md`
- `/home/alin/claude-pro-writer/quality-checklist.md`
- `/home/alin/claude-pro-writer/avoid.md`

---

## Fully Automated Workflow

### In GLM Orchestrator (Vault Session)

```bash
cd /home/alin/DATA/OBSIDIAN/inteles-vault
claude
```

**Full workflow example:**

```
Task: Write article "Ce înseamnă când visezi șerpi"

Step 1: Research (use Perplexity MCP)
@perplexity-ask Search for: "dream interpretation snakes Jung Freud symbolism Romanian culture"

Step 2: Call Claude Pro Writer via MCP
Use @claude-code-writer with this prompt:

{
  "prompt": "Citește context din /home/alin/claude-pro-writer/romanian-style.md.

Scrie un articol de 900-1200 cuvinte în română despre 'Ce înseamnă când visezi șerpi'.

Structură:
- Introducere: Quick answer în primele 2-3 paragrafe
- Perspectivă psihologică: Jung și simbolismul șarpelui
- Scenarii comune: șarpe negru, verde, care mușcă
- Context românesc: tradiții și credințe
- Resurse pentru aprofundare
- FAQ: 6+ întrebări
- Concluzie: Acțiuni practice

Reguli stricte:
- Diacritice mandatory (ă, î, â, ș, ț)
- Paragrafe scurte (2-3 propoziții)
- Ton empatic, professional
- Quick answer în primele 2-3 paragrafe
- H2/H3 la fiecare 300-400 cuvinte
- Fără AI tells ('În concluzie...', 'delve', etc)

La final adaugă:
Excerpt: [25-35 cuvinte]
Keywords: [vise, șerpi, interpretare, Jung, etc]",
  "workFolder": "/home/alin/claude-pro-writer"
}

Step 3: Parallel - Get Products
@monetization-specialist Find 2-3 products for snake dreams article

Step 4: Parallel - Get Images
@image-curator Find 3 images for snake dreams article

Step 5: Assemble Kadence Blocks
@kadence-block-engineer Convert content + products + images to WordPress HTML

Step 6: Publish
@wordpress-publisher Publish to inteles.ro
```

---

## Why This Works

### Authentication Flow

1. **GLM (vault):** Uses API key (cheap GLM tokens)
2. **Claude Code MCP server:** Spawns Claude CLI with Pro auth
   - Server automatically unsets API keys when spawning Claude CLI
   - Claude Code uses your Pro subscription
   - Returns text to GLM

### Token Efficiency

| Step | Model | Tokens | Cost |
|------|-------|--------|------|
| Research | Perplexity | ~3K | ~$0.01 |
| **Writing (via MCP)** | **Claude Pro** | **~8K** | **$0 (Pro)** |
| Monetization | GLM | ~2K | ~$0.006 |
| Images | GLM | ~3K | ~$0.009 |
| Blocks | GLM | ~4K | ~$0.012 |
| Publisher | GLM | ~2K | ~$0.006 |
| **Total** | | **~22K** | **~$0.043** |

**vs Claude Pro alone:** Would hit daily limits after 2-3 articles
**With this setup:** 10-15 articles/day at ~$0.50 total

### Quality

- ✅ Romanian writing: Claude Pro quality (native-level)
- ✅ All other tasks: GLM is perfectly capable
- ✅ No context pollution: Clean input/output contracts
- ✅ No manual steps: Fully automated

---

## Testing the Real MCP

### Step 1: Start GLM Vault Session

```bash
cd /home/alin/DATA/OBSIDIAN/inteles-vault
claude
```

### Step 2: Check MCP Status

```
/mcp
```

Should show:
- `claude-code-writer` ✓ Connected
- `inteles-wordpress` ✓ Connected
- `pexels-mcp-server` ✓ Connected
- `perplexity-ask` ✓ Connected

### Step 3: Test Writer (Real LLM Call)

```
Use @claude-code-writer to execute this prompt:

{
  "prompt": "Scrie 2 paragrafe în română despre semnificația viselor cu apă din perspectivă psihologică. Include diacritice. Maxim 150 cuvinte. Folosește ton empatic și profesional.",
  "workFolder": "/home/alin/claude-pro-writer"
}

Return ONLY the Romanian text generated, nothing else.
```

**Expected result:**
- Real Romanian text with perfect diacritics
- Generated by Claude Pro (not echo/fake)
- 2 paragraphs, empathetic tone
- No AI tells

**If you see this, IT WORKS!** 🎉

---

## Troubleshooting

### MCP Server Not Connecting

**Check:**
```bash
# Test the server manually
cd /home/alin/claude-code-mcp
node build/index.js
```

Should output: "Claude Code MCP Server running..."

### Claude CLI Not Found

**Set explicit path in .mcp.json:**
```json
"env": {
  "CLAUDE_CLI_PATH": "/home/alin/.local/bin/claude"
}
```

**Verify path:**
```bash
which claude
# Should output: /home/alin/.local/bin/claude
```

### Still Using API Key

**The MCP server should automatically unset API keys**, but verify:

```bash
# In the MCP server logs, you should see:
# "Unsetting ANTHROPIC_API_KEY before spawning Claude CLI"
```

### Text Looks Fake (echo)

You're still connected to the WRONG MCP server. Double-check:
- ❌ NOT: `"command": "claude", "args": ["mcp", "serve"]`
- ✅ YES: `"command": "node", "args": ["/home/alin/claude-code-mcp/build/index.js"]`

---

## Next Steps

1. **Install the MCP server:**
   ```bash
   cd /home/alin
   git clone https://github.com/steipete/claude-code-mcp.git
   cd claude-code-mcp
   npm install
   npm run build
   ```

2. **Update .mcp.json** (replace old config)

3. **Restart GLM vault session**

4. **Test with `/mcp` and a real prompt**

5. **Create your 5 agents** (they can now call @claude-code-writer)

6. **Run first full article workflow**

---

## The Key Insight

**You can't call Claude Pro's LLM via the official `claude mcp serve`.**

**But you CAN call it via community MCP servers that spawn Claude CLI as a subprocess!**

This is the ONLY way to:
- Use Pro subscription (not API)
- Fully automate (no manual steps)
- Keep token costs low (GLM orchestrates)
- Maintain quality (Pro writes)

**This is exactly what you need.** 🚀
