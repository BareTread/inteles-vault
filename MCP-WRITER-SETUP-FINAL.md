# ✅ Claude Pro MCP Writer — Setup Complete

**Research Finding:** When MCP servers are launched via integration (like from mcp.json), they **do NOT inherit working directory**. You **MUST set CLAUDE_WORK_DIR explicitly** with absolute paths.

---

## 📦 What Was Created

### 1. Updated `.claude/mcp.json`

```json
{
  "mcpServers": {
    "claude-pro-writer": {
      "command": "bash",
      "args": [
        "-lc",
        "cd /home/alin/claude-pro-writer && env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN claude mcp serve"
      ],
      "env": {
        "CLAUDE_WORK_DIR": "/home/alin/claude-pro-writer"
      },
      "description": "Claude Pro MCP server for premium Romanian writing"
    }
  }
}
```

**Key elements:**
- ✅ `cd /home/alin/claude-pro-writer` — Changes to working directory first
- ✅ `CLAUDE_WORK_DIR` env var — Explicitly sets working directory
- ✅ Unsets API keys — Ensures Pro subscription is used
- ✅ Absolute paths — Required for integration launches

### 2. Created Working Directory Structure

```
/home/alin/claude-pro-writer/
├── README.md                  — Overview
├── romanian-style.md          — Language, tone, structure
├── quality-checklist.md       — 10-point scoring rubric
└── avoid.md                   — AI tells & anti-patterns
```

**Total size:** ~5KB — ultra-lean, focused context

---

## 📝 Context Files Content

### `romanian-style.md`
**What it includes:**
- Diacritics requirements (ă, î, â, ș, ț)
- Tone guidelines (professional, empathetic, tu form)
- Structure template (Intro → Psihologie → Scenarii → Concluzie)
- Paragraph rules (2-3 sentences max)
- H2/H3 placement (~300-400 words)
- Voice guidelines (specific > vague)

### `quality-checklist.md`
**10 scoring categories (0-10 each):**
1. Intent Match — Quick answer first
2. Depth & Insight — Real psychological value
3. Structure & Readability — Headings, short paragraphs
4. Length & Substance — 900-1200 words, no filler
5. Mobile UX — Easy scanning
6. Credibility — Sources, professional disclaimers
7. Language Quality — Perfect Romanian
8. User Value — Genuinely helpful
9. SEO Alignment — Informational, not sales
10. Polish — No errors, consistent formatting

### `avoid.md`
**AI tells to avoid:**
- "În concluzie, putem spune..."
- "Este important de menționat..."
- "delve", "utilize", "it's important to note"
- Long paragraphs, em-dash overuse
- Keyword stuffing, vague generalities
- Corporate or manipulative tone

**Plus:** Examples of good vs bad writing

---

## 🧪 How to Test

### Step 1: Verify Directory Exists

```bash
ls -la /home/alin/claude-pro-writer/
```

Should show:
- README.md
- romanian-style.md
- quality-checklist.md
- avoid.md

### Step 2: Test MCP Config

```bash
cd /home/alin/DATA/OBSIDIAN/inteles-vault
cat .claude/mcp.json
```

Should show CLAUDE_WORK_DIR set to `/home/alin/claude-pro-writer`

### Step 3: Start GLM Claude

```bash
cd /home/alin/DATA/OBSIDIAN/inteles-vault
claude
```

Inside Claude:
```
/mcp
```

Should show `claude-pro-writer` as configured.

### Step 4: Test Writer Connection

```
@writer-coordinator Test the Claude Pro MCP connection.

Call @claude-pro-writer with this prompt:
"Scrie 2 paragrafe în română despre semnificația viselor cu apă. Include diacritice. Folosește ton empatic. Maxim 150 cuvinte. Structură: 1) semnificație de bază, 2) perspectivă psihologică Jung."

Return only the Romanian text, no analysis.
```

If successful, you'll see:
- Romanian text with perfect diacritics
- Short paragraphs (2-3 sentences)
- Empathetic, professional tone
- Jung reference
- No AI tells

---

## 🎯 Why This Setup Works

### Working Directory Behavior (Research-Backed)

| Launch Method | Working Directory | CLAUDE_WORK_DIR Needed? |
|---------------|-------------------|-------------------------|
| Direct CLI (`claude mcp serve`) | Inherits from shell | No (but recommended) |
| Via integration (mcp.json) | Undefined/root | **YES** (mandatory) |

**Source:** Model Context Protocol debugging docs + Claude Code behavior

### Our Setup

- ✅ Uses integration launch (mcp.json)
- ✅ Sets explicit CLAUDE_WORK_DIR
- ✅ Changes to directory before serving (`cd ...`)
- ✅ Uses absolute paths throughout
- ✅ Unsets API keys for Pro auth

**Result:** Reliable, deterministic context every time.

---

## 💡 Context Philosophy

**Minimal, Focused, Essential**

Only 4 files, ~5KB total. No bloat.

**What's included:**
- Language requirements (diacritics, tone)
- Structure template (proven format)
- Quality checklist (objective scoring)
- Anti-patterns (what to avoid)

**What's NOT included:**
- Product lists (handled by monetization-specialist)
- SEO keywords (provided in prompts)
- Image guidelines (handled by image-curator)
- WordPress details (handled by publisher)

Each agent has **only the context it needs**. No pollution.

---

## 🚀 Ready to Create Agents

Now that the MCP writer is configured, proceed with agent creation:

1. Open Global Claude Code
2. Use prompts from `00-AGENT-CONTEXT/AGENT-CREATION-PROMPTS.md`
3. Create all 5 agents
4. Move to vault `.claude/agents/`
5. Test in GLM instance

**Next file to read:** `00-AGENT-CONTEXT/AGENT-CREATION-PROMPTS.md`

---

## 🔍 Troubleshooting

### MCP Server Won't Start

**Check:**
```bash
# Test manually
cd /home/alin/claude-pro-writer
unset ANTHROPIC_API_KEY ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN
claude mcp serve
```

Should start without errors.

### Context Files Not Found

**Verify absolute path:**
```bash
cat ~/.claude/debug.log | grep CLAUDE_WORK_DIR
```

Should show `/home/alin/claude-pro-writer`

### Still Using API Key

**Ensure unset is working:**
```bash
# In the bash command, we use:
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN
```

This removes all API env vars before launching MCP.

---

## ✅ Checklist

Before creating agents:
- [x] `.claude/mcp.json` configured with absolute path
- [x] `/home/alin/claude-pro-writer/` directory created
- [x] 4 context files present (README, style, checklist, avoid)
- [x] CLAUDE_WORK_DIR set to absolute path
- [x] API key unset commands in bash wrapper

Ready to proceed:
- [ ] Create 5 agents in Global Claude
- [ ] Move agents to vault
- [ ] Test in GLM instance
- [ ] Run first full workflow

**Status: READY** 🎉
