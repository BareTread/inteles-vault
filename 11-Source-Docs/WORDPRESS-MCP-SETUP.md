# WordPress MCP Setup for inteles.ro

## Status: CONFIGURED (Needs Credentials)

Your Claude Desktop is now configured to connect to inteles.ro via the WordPress MCP server. You just need to add your WordPress credentials.

---

## Quick Start (5 Minutes)

### Step 1: Create WordPress Application Password

1. **Log into WordPress Admin:**
   - Go to: https://inteles.ro/wp-admin
   - Navigate to: **Users → Your Profile**

2. **Scroll to "Application Passwords" section** (usually near bottom)

3. **Create new password:**
   - Name: `Claude MCP Server`
   - Click **"Add New Application Password"**
   - WordPress will generate a password like: `AbCd 1234 EfGh 5678 IjKl 9012`

4. **IMPORTANT:** Copy this password immediately! WordPress only shows it once.

---

### Step 2: Update Configuration

1. **Open the config file:**
   ```bash
   nano ~/.config/Claude/claude_desktop_config.json
   ```

2. **Replace these two lines** (around line 21-22):
   ```json
   "--username=YOUR_USERNAME_HERE",
   "--appPassword=YOUR_APP_PASSWORD_HERE"
   ```

   With your actual credentials:
   ```json
   "--username=your_wordpress_username",
   "--appPassword=AbCd1234EfGh5678IjKl9012"
   ```

   **IMPORTANT:** Remove spaces from the Application Password!
   - WordPress shows: `AbCd 1234 EfGh 5678 IjKl 9012`
   - You enter: `AbCd1234EfGh5678IjKl9012`

3. **Save and close** (Ctrl+X, then Y, then Enter)

---

### Step 3: Restart Claude Desktop

```bash
# Close Claude Desktop completely, then restart it
killall claude-desktop 2>/dev/null
claude-desktop &
```

Or just close and reopen the Claude Desktop app.

---

### Step 4: Test It

Open Claude Desktop and try these commands:

```
"List my WordPress posts from inteles.ro"

"Show me the 5 most recent posts"

"How many posts do I have about death dreams?"
```

If it works, you'll see your actual posts. If not, check the troubleshooting section below.

---

## What You Can Do Now

### Content Management

```
"List all posts published in October 2025"

"Show me draft posts"

"Find posts that mention 'moarte' or 'înmormântare'"

"Create a new draft post titled 'Vis despre pisici negre'"

"Update post ID 123 to add this text at the bottom: [your text]"

"Delete post ID 456"
```

### Bulk Operations

```
"Find all posts without featured images"

"List posts longer than 1000 words"

"Show me posts that need updating (older than 1 year)"

"Which posts have the most comments?"
```

### SEO & Analytics

```
"What are my top 10 most viewed posts?"
(Note: This requires analytics plugin with REST API support)

"Find posts missing meta descriptions"

"List posts with broken internal links"
```

---

## IMPORTANT: Security Notes

### Application Password Security

- **This password ONLY works for REST API access**
- It does NOT work for normal WordPress admin login
- You can revoke it anytime: Users → Your Profile → Revoke
- Create separate passwords for different tools

### Best Practices

1. **Name your passwords descriptively:**
   - "Claude MCP Server"
   - "Mobile App"
   - "Automation Script"

2. **Revoke unused passwords regularly**

3. **Never share your Application Password publicly**
   - Don't commit it to Git
   - Don't share screenshots with it visible
   - Don't paste it in public chat

4. **The config file is secure:**
   - Located in `~/.config/Claude/` (your home directory)
   - Only readable by your user account
   - BUT: Still avoid committing it to public repos

---

## Configuration File Reference

Your current Claude Desktop config at:
`~/.config/Claude/claude_desktop_config.json`

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
        "@instawp/mcp-wp",
        "--url=https://inteles.ro",
        "--username=YOUR_USERNAME_HERE",
        "--appPassword=YOUR_APP_PASSWORD_HERE"
      ]
    }
  }
}
```

**You already have:**
- Filesystem MCP server (Obsidian vault access) ✅
- WordPress MCP server configured (needs credentials) ⚠️

---

## Troubleshooting

### "Error: Unable to connect to WordPress"

**Check:**
1. Is inteles.ro accessible? Try: `curl https://inteles.ro/wp-json/wp/v2/posts`
2. Is the username correct?
3. Did you remove spaces from the Application Password?
4. Did you restart Claude Desktop after config change?

**Test manually:**
```bash
curl -u "username:password" https://inteles.ro/wp-json/wp/v2/posts
```

If this returns JSON, your credentials work. If 401 error, credentials are wrong.

---

### "MCP server not found" or "inteles-wordpress not available"

**Check:**
1. Is the config file valid JSON? Test:
   ```bash
   cat ~/.config/Claude/claude_desktop_config.json | jq .
   ```
   If error, you have a syntax error (missing comma, bracket, etc.)

2. Is `npx` available?
   ```bash
   npx --version
   ```
   If not installed: `npm install -g npx`

3. Try installing the package manually first:
   ```bash
   npx @instawp/mcp-wp --help
   ```

---

### "Application Passwords not available"

**Requirements:**
- WordPress 5.6+ (inteles.ro should have this)
- HTTPS enabled (inteles.ro has this)
- Not disabled by host (rare on ZUME)

**If missing:**
1. Check WordPress version: Dashboard → Updates
2. Contact ZUME support if feature is disabled

**Alternative:**
Use plugin password manager or OAuth plugins.

---

### Romanian Characters (ă, â, î, ș, ț) Look Broken

**This is usually a display issue, not a data issue.**

When creating/updating posts with Romanian text, Claude should handle UTF-8 correctly. If you see garbled text in WordPress admin:

1. Check WordPress Settings → General → Site Language is "Română"
2. Check database collation is `utf8mb4_unicode_ci`
3. Usually not an issue with REST API (it handles UTF-8 natively)

---

## WordPress REST API Capabilities

### What You CAN Do (via @instawp/mcp-wp):

✅ Posts: Create, read, update, delete
✅ Pages: Full CRUD operations
✅ Categories & Tags: Manage taxonomies
✅ Media: Upload images, manage library
✅ Comments: Read, moderate, reply
✅ Users: List, read (limited by permissions)
✅ Settings: Read site settings
✅ Custom Post Types: If exposed to REST API

### What You CANNOT Do (REST API limitations):

❌ Install/activate plugins
❌ Change theme
❌ Edit theme files directly
❌ Direct database access
❌ Server file system access
❌ WP-CLI operations

**For these, you'd need:**
- SSH access + WP-CLI MCP server (Option A from plan)
- OR manual admin panel work
- OR custom WordPress plugin (advanced)

---

## Upgrading to Official WordPress MCP Adapter (Later)

Once you've validated this workflow works, you can upgrade to the official adapter for more power:

**Official WordPress MCP Adapter:**
- Plugin: `WordPress/mcp-adapter`
- GitHub: https://github.com/WordPress/mcp-adapter
- Gives access to WordPress Abilities API (more powerful than REST API)
- Allows custom abilities (e.g., auto-insert affiliate links)

**When to upgrade:**
- You need capabilities beyond REST API
- You want to create custom WordPress MCP tools
- You need better performance
- You want official WordPress support/updates

---

## Next Steps for inteles.ro Monetization

Once MCP is working, use it for:

### 1. Affiliate Link Automation
```
"Find all posts mentioning books about dreams and add affiliate links to:
- Libris.ro: [2Performant link]
- Include Romanian disclosure: 'Link afiliat - câștigăm un mic comision'"
```

### 2. Content Optimization
```
"Review posts for mobile optimization:
- Short paragraphs (3-4 lines max)
- Clear headings
- Add featured images if missing"
```

### 3. Bulk Updates
```
"Add this email capture HTML to all posts with >100 views:
[your email capture code]"
```

### 4. Content Creation
```
"Create 5 new posts about popular dream topics:
- Format for mobile (97.5% mobile traffic)
- Include 2Performant affiliate links
- Romanian SEO optimization
- Publish as drafts for review"
```

---

## Advanced: 2Performant Workflow

### Getting Your Affiliate Links

1. **Log into 2Performant:**
   - Dashboard: https://event.2performant.com/

2. **Find merchants you're approved for:**
   - Libris.ro
   - SpringFarma.com
   - evoMAG.ro
   - Flanco.ro

3. **Generate tracking links:**
   - Campaign: inteles-ro
   - Each product gets unique tracking

### Template for Claude

Create a reusable template in your Obsidian vault or here:

```markdown
# 2Performant Affiliate Template for inteles.ro

## Standard Disclosure (Romanian)
"Acest articol conține linkuri afiliate. Câștigăm un mic comision dacă achiziționați produse prin aceste linkuri, fără costuri suplimentare pentru dvs."

## Common Products

### Books (Libris.ro - 8% commission)
- Dicționar de vise: [2Performant link]
- Interpretarea viselor - Carl Jung: [link]

### Sleep Products (SpringFarma - 6% commission)
- Magneziu glicinat: [link]
- Ceai de lavandă: [link]

### Electronics (evoMAG - 4% commission)
- Ceas cu lumină de răsărit: [link]
- Umidificator: [link]

## Usage in WordPress MCP

"Add this affiliate block to post about death dreams:
[paste appropriate product + disclosure]"
```

Then tell Claude:
```
"Read my affiliate template and add relevant products to this post"
```

---

## Maintenance

### Weekly
- Check affiliate links still work
- Review new post performance
- Add affiliate links to trending posts

### Monthly
- Audit all affiliate disclosures present
- Check 2Performant earnings report
- Optimize underperforming posts

### Quarterly
- Review overall strategy
- Test new affiliate merchants
- A/B test affiliate placement

---

## Support Resources

### WordPress REST API
- Official Docs: https://developer.wordpress.org/rest-api/
- Handbook: https://developer.wordpress.org/rest-api/reference/

### MCP for WordPress
- InstaWP MCP: https://instawp.com/wordpress-mcp/
- Official adapter: https://github.com/WordPress/mcp-adapter

### Romanian Affiliate Marketing
- 2Performant: https://www.2performant.com/
- ANPC Guidelines: https://anpc.ro/

---

## Questions?

Common questions answered:

**Q: Can I use this with Codex CLI too?**
A: Yes! Configure Codex to read the same `~/.config/Claude/claude_desktop_config.json` or create a separate config.

**Q: Will this work on ZUME shared hosting?**
A: Yes! Uses REST API over HTTPS - no special server requirements.

**Q: Can I use this for multiple WordPress sites?**
A: Yes! Add more MCP servers:
```json
"inteles-wordpress": { ... },
"baretread-wordpress": { ... },
"another-site": { ... }
```

**Q: Is this safe for production site?**
A: Yes - uses WordPress's built-in secure API. Same security as WordPress mobile app.

**Q: Cost?**
A: $0. All tools are free and open source.

---

## Summary

✅ MCP server configured in Claude Desktop
⚠️ Needs WordPress credentials (5 minute setup)
📋 Documentation complete
🚀 Ready to automate inteles.ro

**Next action:** Create Application Password and update config file (Step 1-2 above)
