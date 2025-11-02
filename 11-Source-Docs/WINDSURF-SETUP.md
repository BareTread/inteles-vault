# Windsurf WordPress MCP Setup

## ✅ Config File Fixed

The `windsurf-mcp-config.json` has been updated with the correct environment variable format.

---

## How to Apply to Windsurf (3 Steps)

### Step 1: Find Your Windsurf Config Location

**Try these locations:**
```bash
# Option 1: Codeium directory
find ~/.codeium -name "mcp_settings.json" 2>/dev/null

# Option 2: Windsurf config directory
find ~/.config/Windsurf -name "mcp_settings.json" 2>/dev/null

# Option 3: Search entire home directory
find ~ -name "mcp_settings.json" 2>/dev/null
```

**Most common location:**
```
~/.codeium/windsurf/mcp_settings.json
```

---

### Step 2: Update the Config

**Option A: Replace Entire File (Easiest)**

```bash
# Backup your current config first
cp ~/.codeium/windsurf/mcp_settings.json ~/.codeium/windsurf/mcp_settings.json.backup

# Copy the fixed config
cp /mnt/data/Work/inteles-ro/windsurf-mcp-config.json ~/.codeium/windsurf/mcp_settings.json
```

**Option B: Manual Edit (Safer if you have custom settings)**

1. Open your Windsurf config:
   ```bash
   nano ~/.codeium/windsurf/mcp_settings.json
   ```

2. Find the `"inteles-wordpress"` section (if it exists) or add it

3. Replace with this:
   ```json
   "inteles-wordpress": {
     "command": "npx",
     "args": [
       "-y",
       "@instawp/mcp-wp"
     ],
     "env": {
       "WORDPRESS_API_URL": "https://inteles.ro",
       "WORDPRESS_USERNAME": "baretrea",
       "WORDPRESS_PASSWORD": "Yzix4308YGsRNLirTWJfdztM"
     },
     "disabled": false
   }
   ```

4. Save (Ctrl+X, Y, Enter)

---

### Step 3: Restart Windsurf

Close Windsurf completely and reopen it.

---

## Testing in Windsurf

1. Open Windsurf
2. Open the AI chat panel (usually Ctrl+L or Cmd+L)
3. Type: **"List my WordPress posts from inteles.ro"**

**Expected:** You should see a list of your posts

**If it works:** 🎉 Done!

**If it doesn't work:** See troubleshooting below

---

## What Changed (The Fix)

**OLD (Wrong):**
```json
"args": [
  "-y",
  "@instawp/mcp-wp",
  "--url=https://inteles.ro",        ← Command-line args (wrong)
  "--username=baretrea",
  "--appPassword=..."
]
```

**NEW (Correct):**
```json
"args": [
  "-y",
  "@instawp/mcp-wp"
],
"env": {                              ← Environment variables (correct)
  "WORDPRESS_API_URL": "https://inteles.ro",
  "WORDPRESS_USERNAME": "baretrea",
  "WORDPRESS_PASSWORD": "..."
}
```

---

## Your Full Windsurf Config

The fixed config includes all your existing MCP servers PLUS inteles-wordpress:

```json
{
  "mcpServers": {
    "perplexity-ask": { ... },           ← Your existing Perplexity MCP
    "memory": { ... },                   ← Your existing Memory MCP
    "sequential-thinking": { ... },      ← Your existing Thinking MCP
    "claude-code": { ... },              ← Your existing Claude Code MCP
    "chrome-devtools": { ... },          ← Your existing Chrome DevTools
    "inteles-wordpress": { ... }         ← NEW: WordPress MCP (FIXED)
  }
}
```

All your existing MCPs are preserved!

---

## Commands You Can Use in Windsurf

Once it's working, try these in Windsurf's AI chat:

### Basic WordPress Operations
```
"List my recent WordPress posts"

"Show me all posts about death dreams (moarte)"

"Create a draft post titled 'Test from Windsurf'"

"Get post ID 123 and show its content"

"Find posts without featured images"
```

### Code Generation with WordPress Context
```
"Generate Python code to add affiliate links to all posts about sleep (somn)"

"Write a script that finds posts older than 1 year and flags them for update"

"Create a function that inserts Romanian affiliate disclosure at the bottom of all posts"
```

### Workflow Automation
```
"Show me all posts from October 2025, then generate code to add affiliate links to them"

"Find the top 10 most commented posts and create a content calendar based on those topics"
```

---

## Troubleshooting

### "MCP server not found" or "inteles-wordpress not available"

1. **Check config file exists:**
   ```bash
   ls -la ~/.codeium/windsurf/mcp_settings.json
   ```

2. **Validate JSON syntax:**
   ```bash
   cat ~/.codeium/windsurf/mcp_settings.json | jq .
   ```
   If error: JSON syntax is broken, restore from backup

3. **Check package is available:**
   ```bash
   npm view @instawp/mcp-wp
   ```
   Should show package info

### "Authentication failed" or 401 Error

1. **Test credentials manually:**
   ```bash
   curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" \
     "https://inteles.ro/wp-json/wp/v2/posts?per_page=1"
   ```
   Should return JSON

2. **If 401 error:**
   - Regenerate Application Password in WordPress
   - Update config with new password

### Windsurf Shows "Connection timeout"

1. **Check inteles.ro is accessible:**
   ```bash
   curl -I https://inteles.ro
   ```

2. **Check REST API is enabled:**
   ```bash
   curl https://inteles.ro/wp-json/
   ```

---

## Quick Reference

**Config file location (most common):**
```
~/.codeium/windsurf/mcp_settings.json
```

**WordPress credentials:**
- URL: `https://inteles.ro`
- Username: `baretrea`
- Password: `Yzix4308YGsRNLirTWJfdztM`

**Fixed config available at:**
```
/mnt/data/Work/inteles-ro/windsurf-mcp-config.json
```

---

## Differences: Windsurf vs Claude Desktop

Both use the same MCP server, just different config files:

| Tool | Config File | Format | Status |
|------|------------|--------|--------|
| **Claude Desktop** | `~/.config/Claude/claude_desktop_config.json` | JSON | ✅ Fixed |
| **Windsurf** | `~/.codeium/windsurf/mcp_settings.json` | JSON | ✅ Fixed |
| **Codex CLI** | Custom script or Python wrapper | Various | 📝 See MULTI-TOOL-SETUP.md |

---

## Next Steps

1. **Apply config:** Copy `windsurf-mcp-config.json` to Windsurf config location
2. **Restart Windsurf:** Close completely and reopen
3. **Test:** "List my WordPress posts from inteles.ro"
4. **Start using:** See `INTELES-MONETIZATION-WORKFLOWS.md` for monetization strategies

---

## Support

**Still not working?**

1. Check Windsurf logs:
   - Help → Toggle Developer Tools → Console
   - Look for MCP-related errors

2. Verify package installation:
   ```bash
   npx @instawp/mcp-wp --version
   ```

3. Test REST API manually:
   ```bash
   curl https://inteles.ro/wp-json/wp/v2/posts?per_page=1
   ```

4. Check for typos in config file (common with manual edits)

---

**Ready?** Find your config location, copy the fixed file, restart Windsurf, and test!
