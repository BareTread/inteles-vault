# ✅ FIXED WordPress MCP Setup - inteles.ro

## What Was Wrong

The previous configuration used **command-line arguments** when `@instawp/mcp-wp` expects **environment variables**.

**OLD (Wrong):**
```json
"args": [
  "-y",
  "@instawp/mcp-wp",
  "--url=https://inteles.ro",      ← Wrong format
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
"env": {                             ← Environment variables
  "WORDPRESS_API_URL": "https://inteles.ro",
  "WORDPRESS_USERNAME": "baretrea",
  "WORDPRESS_PASSWORD": "..."
}
```

---

## ✅ Current Status

- Configuration **FIXED** ✅
- JSON validated ✅
- Ready to test ✅

---

## How to Test (3 Steps)

### Step 1: Restart Claude Desktop

```bash
# Close Claude Desktop completely
pkill -f claude-desktop

# Wait 2 seconds
sleep 2

# Restart
claude-desktop &
```

Or manually: Close Claude Desktop app completely, then reopen it.

---

### Step 2: Test Basic Command

Open Claude Desktop and type:

```
"List my WordPress posts from inteles.ro"
```

**Expected result:** You should see a list of your posts with titles, IDs, and excerpts.

**If it works:** 🎉 You're done! Skip to "What You Can Do Now" section below.

**If it doesn't work:** Continue to Step 3 for debugging.

---

### Step 3: Debug (If Needed)

#### Check MCP Server Status

In Claude Desktop, look for the MCP servers panel (usually bottom-left or in developer tools).

**Expected:** `inteles-wordpress` should show as "Running" or "Connected"

#### Check Logs

If there's an error, Claude Desktop will show it. Common issues:

**"Cannot find module '@instawp/mcp-wp'"**
```bash
# Install it manually first
npm install -g @instawp/mcp-wp
```

**"Authentication failed" or "401 Unauthorized"**
- Application Password might be wrong
- Regenerate in WordPress: Users → Your Profile → Application Passwords
- Update config with new password

**"Connection timeout" or "Cannot reach https://inteles.ro"**
- Check inteles.ro is accessible
- Test manually: `curl https://inteles.ro/wp-json/`

---

## What You Can Do Now

Once it's working, you can use natural language commands:

### Basic Operations

```
"Show me my 10 most recent posts"

"Find all posts about death dreams (moarte)"

"Create a draft post titled 'Test from Claude' with content 'This is a test'"

"Get post ID 123 and show me its content"

"How many posts do I have total?"
```

### Monetization Workflows

```
"Find all posts mentioning 'vis despre moarte' and list them so I can add affiliate links"

"Create 3 new draft posts about popular dream topics with placeholders for affiliate links"

"Search for posts without any links and show me the top 10"

"Show me all posts from October 2025"
```

### Content Analysis

```
"Which posts are my longest?"

"Find posts with no featured image"

"Show me posts that haven't been updated in over a year"

"List all my draft posts"
```

---

## Current Configuration Reference

**File:** `/home/alin/.config/Claude/claude_desktop_config.json`

```json
{
  "preferences": {
    "menuBarEnabled": false,
    "legacyQuickEntryEnabled": false
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/alin/DATA/OBSIDIAN/Baretread-Vault"
      ]
    },
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
      }
    }
  }
}
```

---

## To Answer Your Question: Is the Official Adapter Better?

**Short answer:** Not for your use case.

**The community package we set up is perfect because:**

1. ✅ **Simpler:** Zero WordPress changes, just config file
2. ✅ **Sufficient:** REST API does everything you need for monetization
3. ✅ **Works now:** Already configured and ready
4. ✅ **Shared hosting compatible:** No SSH or WP-CLI required

**The official `WordPress/mcp-adapter` is overkill because:**

1. ❌ **Complex:** Requires installing WordPress plugin
2. ❌ **Requires SSH/proxy:** Harder to connect remotely
3. ❌ **Unnecessary power:** You don't need Abilities API for basic post editing
4. ❌ **More maintenance:** Another plugin to update

**Use the official adapter only if:**
- You need custom WordPress abilities
- You want plugin-specific functionality
- You need enterprise features (observability, monitoring)
- You're building WordPress tooling for multiple sites

**For monetizing inteles.ro with affiliate links:** Community package is ideal.

---

## Quick Comparison

| Task | Community Package | Official Adapter |
|------|------------------|------------------|
| Create posts | ✅ Easy | ✅ Easy |
| Edit posts | ✅ Easy | ✅ Easy |
| Add affiliate links | ✅ Easy | ✅ Easy |
| Upload images | ✅ Easy | ✅ Easy |
| Bulk operations | ✅ Easy | ✅ Easy |
| Custom abilities | ❌ No | ✅ Yes |
| Plugin integration | ❌ Limited | ✅ Full |
| Setup complexity | ⭐ Low | ⭐⭐⭐ High |
| Maintenance | ⭐ Low | ⭐⭐⭐ Medium |

---

## Next Steps

1. **NOW:** Restart Claude Desktop
2. **Test:** "List my WordPress posts from inteles.ro"
3. **If it works:** Start monetizing! Follow `INTELES-MONETIZATION-WORKFLOWS.md`
4. **If it fails:** Check error message and debug (see Step 3 above)

---

## Files in This Project

```
/mnt/data/Work/inteles-ro/
├── FIXED-QUICK-START.md                  ← YOU ARE HERE (start here!)
├── README.md                             ← Project overview
├── INTELES-MONETIZATION-WORKFLOWS.md     ← Monetization strategies
├── WORDPRESS-MCP-SETUP.md                ← Technical details
├── MULTI-TOOL-SETUP.md                   ← Windsurf + Codex setup
├── CORRECT-SETUP.md                      ← Official adapter comparison
└── windsurf-mcp-config.json              ← Windsurf configuration
```

**Read next:** Once this works, open `INTELES-MONETIZATION-WORKFLOWS.md` for 7 monetization workflows.

---

## Support

**If still not working:**

1. Check REST API is accessible:
   ```bash
   curl https://inteles.ro/wp-json/wp/v2/posts?per_page=1
   ```

2. Test authentication:
   ```bash
   curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" \
     "https://inteles.ro/wp-json/wp/v2/posts?per_page=1"
   ```

3. Verify package exists:
   ```bash
   npm view @instawp/mcp-wp
   ```

All three should work. If any fails, we'll debug that specific issue.

---

**Ready? Restart Claude Desktop and test:** `"List my WordPress posts"`
