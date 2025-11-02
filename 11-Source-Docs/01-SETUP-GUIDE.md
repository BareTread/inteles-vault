# Technical Setup Guide

**Last Updated:** November 2, 2025

## Overview

This guide consolidates all setup information for the inteles.ro WordPress automation system using MCP (Model Context Protocol).

**Current Status:** ✅ Fully configured and working

---

## System Architecture

```
AI Tool (Claude/Windsurf)
    ↓
MCP Server (@instawp/mcp-wp)
    ↓
WordPress REST API (HTTPS)
    ↓
inteles.ro (ZUME.ro hosting)
```

**Benefits:**
- Natural language WordPress management
- No WordPress plugin installation needed
- Works on any hosting (shared hosting OK)
- Secure (HTTPS + Application Password)
- Free and open source

---

## WordPress Configuration

### Application Password

**Created:** October 30, 2025  
**Name:** "mcp"  
**Password:** `Yzix4308YGsRNLirTWJfdztM`  
**Username:** `baretrea`

**How to Regenerate (if needed):**
1. WordPress Admin → Users → Your Profile
2. Scroll to "Application Passwords"
3. Enter name (e.g., "mcp-new")
4. Click "Add New Application Password"
5. Copy password immediately (shown only once)
6. Update config file with new password

**Security Notes:**
- Application passwords ONLY work for REST API
- Cannot be used for WordPress admin login
- Can be revoked anytime without affecting admin access
- Never commit to public repositories

### REST API Status

**Endpoint:** `https://inteles.ro/wp-json/wp/v2/`

**Test Connection:**
```bash
curl "https://inteles.ro/wp-json/wp/v2/posts?per_page=1"
```

**Test Authentication:**
```bash
curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" \
  "https://inteles.ro/wp-json/wp/v2/posts?per_page=1"
```

**Should return:** JSON with post data

---

## Claude Desktop Setup

### Configuration File

**Location:** `/home/alin/.config/Claude/claude_desktop_config.json`

**Current Configuration:**
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

**Key Points:**
- Uses `env` variables (NOT command-line args)
- Package: `@instawp/mcp-wp`
- Transport: `npx` (auto-installs on first use)

### Restart Claude Desktop

**After any config change:**
```bash
# Kill current Claude Desktop process
pkill -f claude-desktop

# Wait 2 seconds
sleep 2

# Restart
claude-desktop &
```

Or manually close and reopen the app.

---

## Windsurf Setup

### Configuration File

**Location:** `/home/alin/DATA/Work/inteles-ro/windsurf-mcp-config.json`

**Content:**
```json
{
  "mcpServers": {
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

**Windsurf Config Location:**
`/home/alin/.codeium/windsurf/mcp_config.json`

**Same credentials,** different config file location.

---

## Testing & Verification

### Basic Tests

**1. List Posts:**
```
"List my WordPress posts from inteles.ro"
```
Expected: List of posts with titles and IDs

**2. Get Specific Post:**
```
"Show me post ID 3423 from inteles.ro"
```
Expected: Full post content

**3. Search Posts:**
```
"Find all inteles.ro posts mentioning 'burnout'"
```
Expected: Filtered list

**4. Create Draft (Safe):**
```
"Create a draft post on inteles.ro titled 'MCP Test - Delete Me' 
with content 'Testing MCP connection'"
```
Expected: Draft appears in WordPress admin

### Verify in WordPress

1. Go to: https://inteles.ro/wp-admin
2. Navigate to: Posts → All Posts
3. Check for test draft
4. Delete test post after verification

---

## Available Operations

### Content Management

**Posts:**
- List, search, filter posts
- Create new posts (draft or publish)
- Update existing posts
- Delete posts (with confirmation)
- Manage categories and tags

**Pages:**
- Same operations as posts
- Custom page templates supported

**Media:**
- Upload images
- Attach to posts
- Update alt text and captions

**Comments:**
- Read comments
- Moderate (approve/spam/trash)

### Bulk Operations

**Examples:**
```
"Find all posts from 2023 and update the year to 2025"
"Add affiliate disclosure to all posts containing affiliate links"
"Mobile-optimize top 20 articles"
"Update all posts in category 'Vise' with new FAQ structure"
```

**Safety:** Claude will preview changes and ask for confirmation

### Limitations

**What MCP CAN'T do:**
- Install plugins
- Change themes
- Access file system directly
- Modify database directly
- Change WordPress settings (most)

**Workaround:** Use WordPress admin panel for these tasks

---

## Troubleshooting

### "MCP server not available"

**Causes:**
1. Claude Desktop not restarted
2. Invalid JSON config
3. Package not installed

**Solutions:**
```bash
# 1. Restart Claude Desktop
pkill -f claude-desktop && sleep 2 && claude-desktop &

# 2. Validate JSON
cat ~/.config/Claude/claude_desktop_config.json | jq .

# 3. Install package manually
npx @instawp/mcp-wp --help
```

### "Authentication failed" (401)

**Causes:**
1. Wrong username
2. Wrong password
3. Application password revoked

**Solutions:**
```bash
# Test authentication manually
curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" \
  "https://inteles.ro/wp-json/wp/v2/posts?per_page=1"

# If fails, regenerate application password in WordPress
```

### "Connection timeout"

**Causes:**
1. inteles.ro is down
2. ZUME hosting blocking requests
3. Network issues

**Solutions:**
```bash
# Check site accessibility
curl -I https://inteles.ro

# Check REST API specifically
curl https://inteles.ro/wp-json/

# If both work but MCP doesn't, contact ZUME support
```

### Romanian Characters Display Wrong

**Example:** "înseamnă" shows as "Ã®nseamnÄƒ"

**This is visual only** - data is correct in WordPress.

**Fix:**
- Usually auto-handled by Claude
- If persists: WordPress → Settings → General → Site Language = "Română"

### Slow Response Times

**Causes:**
1. Large bulk operations
2. Shared hosting limitations
3. Complex queries

**Solutions:**
```
"Process posts one at a time with 2 second delay"
"Batch update in groups of 10"
```

---

## REST API Reference

### Endpoints Used

**Posts:**
- GET `/wp-json/wp/v2/posts` - List posts
- GET `/wp-json/wp/v2/posts/{id}` - Get specific post
- POST `/wp-json/wp/v2/posts` - Create post
- PUT `/wp-json/wp/v2/posts/{id}` - Update post
- DELETE `/wp-json/wp/v2/posts/{id}` - Delete post

**Categories:**
- GET `/wp-json/wp/v2/categories` - List categories

**Media:**
- POST `/wp-json/wp/v2/media` - Upload image

**Full API Docs:** https://developer.wordpress.org/rest-api/

### Rate Limiting

**ZUME Hosting:**
- No official rate limit published
- Recommended: Max 10 requests/second
- For bulk operations: Add delays

**Implementation:**
```
"Update 50 posts with 1 second delay between each"
```

---

## Security Best Practices

### Application Passwords

✅ **Do:**
- Use descriptive names ("mcp", "mobile-app")
- Revoke unused passwords
- Rotate passwords every 6 months
- Keep config file in home directory (~/.config/)

❌ **Don't:**
- Share passwords publicly
- Commit to Git
- Use for multiple sites
- Reuse admin passwords

### Config File Security

**Permissions:**
```bash
# Config should be readable only by your user
chmod 600 ~/.config/Claude/claude_desktop_config.json
```

**Git Ignore:**
```
# Add to .gitignore
claude_desktop_config.json
windsurf-mcp-config.json
```

### WordPress Security

**Recommendations:**
1. Keep WordPress updated
2. Use strong admin password (different from app password)
3. Enable 2FA for WordPress admin
4. Regular backups via ZUME cPanel
5. Monitor application password usage

---

## Upgrading (Future Options)

### Option 1: Official WordPress MCP Adapter

**Package:** `WordPress/mcp-adapter`

**Pros:**
- Official WordPress support
- Access to WordPress Abilities API
- Can create custom MCP tools
- Better observability

**Cons:**
- Requires WordPress plugin installation
- More complex setup
- Needs SSH/proxy for remote access
- Overkill for basic post management

**When to upgrade:**
- Need features beyond REST API
- Want custom WordPress abilities
- Enterprise-level usage

### Option 2: WP-CLI MCP Server

**Requires:** SSH access to ZUME server

**Pros:**
- Most powerful option
- Full server control
- Can run any WP-CLI command

**Cons:**
- Needs reliable SSH access
- More complex configuration
- Potential security concerns

**When to upgrade:**
- Have dedicated server (not shared hosting)
- Need server-level operations
- Maximum control required

### Current Recommendation

**Stick with community package (@instawp/mcp-wp)**

**Reasons:**
- Perfectly sufficient for content management
- No WordPress changes needed
- Works on shared hosting
- Simple and reliable
- Free and well-maintained

---

## Common Commands

### Content Creation

```
"Create a new draft post on inteles.ro:
Title: [title]
Content: [content]
Category: [category]
Save as draft"

"Create article following [[02-CONTENT-STRATEGY]] template"
```

### Content Updates

```
"Update post ID 3423 by adding this content: [content]"

"Find post titled '[title]' and update the FAQ section"

"Add this resource box to all posts in category 'Vise'"
```

### Content Search

```
"Find all posts about burnout"

"Show me posts published in October 2025"

"List posts with >1000 words"

"Find posts without affiliate links"
```

### Bulk Operations

```
"Update all posts from 2023 to say 2025"

"Add balanced affiliate links to top 10 traffic posts"

"Mobile-optimize all posts in 'Vise' category"
```

---

## Next Steps

1. **Verify setup** - Run basic tests above
2. **Learn workflows** - Read [[03-MONETIZATION-GUIDE]]
3. **Create content** - Follow [[02-CONTENT-STRATEGY]]
4. **Track progress** - Use [[04-ARTICLE-TRACKING]]

---

## FAQ

**Q: Do I need to install anything on inteles.ro?**
A: No! MCP runs locally. WordPress just needs REST API (enabled by default).

**Q: Can I use this with other sites?**
A: Yes! Add another MCP server config with different credentials.

**Q: What if I make a mistake?**
A: WordPress keeps revisions. You can rollback via admin panel or ask Claude to revert.

**Q: Is this free?**
A: Yes! All tools are free and open source.

**Q: Can I use this with Codex CLI?**
A: Yes! Same MCP configuration works with any MCP-compatible tool.

**Q: Will this work if I change hosting?**
A: Yes! As long as new host allows REST API (most do).

---

**Need more help?** Check [[05-TECHNICAL-REFERENCE]] or ask Claude directly.
