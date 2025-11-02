# Technical Reference

**Last Updated:** November 2, 2025

## Quick Reference

| Need | Command/Info | See Section |
|------|-------------|-------------|
| Test connection | `curl https://inteles.ro/wp-json/` | [REST API](#rest-api) |
| List posts | `"List my inteles.ro posts"` | [Commands](#commands) |
| Update post | `"Update post ID 3423..."` | [Commands](#commands) |
| Fix auth error | Regenerate app password | [Troubleshooting](#troubleshooting) |
| Add affiliate link | See template | [Snippets](#html-snippets) |

---

## Site Information

### inteles.ro Stats

**WordPress:**
- Version: Latest (auto-updates enabled)
- Theme: Kadence
- Hosting: ZUME.ro (shared hosting)
- Language: Română

**Traffic:**
- Daily: ~437 visitors
- Monthly: ~13,100 visitors
- CTR: 30.67% (very high!)
- Mobile: 97.5%

**Content:**
- Total posts: ~546
- Categories: Dreams, Everyday Meanings, Psychology
- Main focus: Romanian dream interpretation

**Revenue:**
- Current: €300-700/month (balanced approach)
- Potential: €500-1000/month (optimized)

### WordPress Credentials

**Admin Access:**
- URL: https://inteles.ro/wp-admin
- Username: `baretrea`
- Password: [separate secure storage]

**Application Password (MCP):**
- Name: "mcp"
- Password: `Yzix4308YGsRNLirTWJfdztM`
- Created: Oct 30, 2025
- Status: Active

**2Performant:**
- Dashboard: https://event.2performant.com/
- Affiliate Code: `80f42fe2f`
- Username: [email]
- Active merchants: Libris.ro, Librex.ro, SpringFarma, etc.

---

## REST API

### Endpoints

**Base URL:** `https://inteles.ro/wp-json/wp/v2/`

**Common Endpoints:**
```
GET    /posts              # List posts
GET    /posts/{id}         # Get post
POST   /posts              # Create post
PUT    /posts/{id}         # Update post
DELETE /posts/{id}         # Delete post
GET    /categories         # List categories
GET    /tags               # List tags
POST   /media              # Upload media
GET    /comments           # List comments
```

### Authentication

**Format:**
```bash
curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" \
  "https://inteles.ro/wp-json/wp/v2/posts"
```

**Headers:**
```
Authorization: Basic base64(username:password)
```

### Query Parameters

**Common filters:**
```
?per_page=20          # Results per page (max 100)
?page=2               # Pagination
?search=burnout       # Search term
?categories=5         # Filter by category ID
?status=draft         # Post status
?orderby=date         # Sort by date/title/modified
?order=desc           # Sort direction
?after=2025-01-01     # Posts after date
?before=2025-12-31    # Posts before date
```

**Example:**
```bash
curl "https://inteles.ro/wp-json/wp/v2/posts?per_page=10&search=vis&orderby=date&order=desc"
```

### Response Format

**Post Object:**
```json
{
  "id": 3423,
  "date": "2024-03-07T00:07:25",
  "modified": "2025-11-02T00:25:57",
  "slug": "ce-inseamna-burnout",
  "status": "publish",
  "type": "post",
  "link": "https://inteles.ro/ce-inseamna-burnout/",
  "title": {
    "rendered": "Ce Înseamnă Burnout"
  },
  "content": {
    "rendered": "<p>...</p>"
  },
  "excerpt": {
    "rendered": "..."
  },
  "categories": [6],
  "tags": [],
  "featured_media": 3424
}
```

---

## MCP Commands

### Basic Operations

**List Posts:**
```
"List my WordPress posts from inteles.ro"
"Show me recent posts from inteles.ro"
"List all published posts"
```

**Get Specific Post:**
```
"Show me post ID 3423"
"Get the details of the burnout article"
"Display post titled 'Kind Reminder'"
```

**Search Posts:**
```
"Find all posts about dreams"
"Search for posts mentioning 'burnout'"
"Show me posts in category 'Vise'"
```

### Content Creation

**Create Draft:**
```
"Create a draft post on inteles.ro:
Title: [title]
Content: [content]
Category: [category]
Tags: [tags]
Save as draft"
```

**Create from Template:**
```
"Create a new article following the balanced approach from 
[[02-CONTENT-STRATEGY]]:
Topic: [topic]
Keywords: [keywords]
Include FAQ schema with 6 questions
Add 1 contextual affiliate link for [type] books"
```

### Content Updates

**Simple Update:**
```
"Update post ID 3423 by adding this paragraph: [text]"
"Add this FAQ section to the burnout article: [HTML]"
```

**Complex Update:**
```
"Update article 3423:
1. Add credible sources (WHO, Jung)
2. Include FAQ schema (6 questions)
3. Add 1 affiliate link in green resource box
4. Remove any aggressive monetization
5. Ensure mobile-optimized"
```

**Bulk Update:**
```
"Find all posts in category 'Vise' and:
1. Add FAQ schema if missing
2. Ensure 2,000+ words
3. Add 1 contextual affiliate link (dream books)
4. Update one at a time with my approval"
```

### Advanced Queries

**Traffic Analysis:**
```
"Which of my posts have the most comments?"
"Find posts published in 2023"
"Show me posts under 1000 words"
```

**Quality Audit:**
```
"Find posts without FAQ schema"
"List posts with >5 affiliate links (need balance fix)"
"Show me posts without featured images"
```

---

## HTML Snippets

### Resource Box (Green - Balanced Monetization)

```html
<div style="background: #E8F5E9; border-left: 4px solid #4CAF50; 
padding: 20px; margin: 25px 0; border-radius: 4px;">
<h3 style="margin-top: 0; color: #2E7D32;">
📚 Resurse pentru aprofundare</h3>
<p style="margin-bottom: 0;">Pentru cei interesați să aprofundeze 
[TOPIC], <a href="[AFFILIATE_LINK]" target="_blank" rel="noopener">
[RESOURCE_NAME]</a> oferă [VALUE_PROPOSITION].</p>
<p style="font-size: 0.85rem; color: #666; margin-top: 12px;">
<em>Link afiliat - Câștigăm un mic comision fără costuri 
suplimentare pentru tine.</em></p>
</div>
```

### Info Box (Orange - Learning)

```html
<div style="background: #FFF3E0; border-left: 4px solid #FF6F00; 
padding: 20px; margin: 25px 0; border-radius: 4px;">
<h3 style="margin-top: 0; color: #E65100;">
📋 Ce veți învăța din acest articol:</h3>
<ul style="line-height: 1.8; margin-bottom: 0;">
<li>Point 1</li>
<li>Point 2</li>
<li>Point 3</li>
</ul>
</div>
```

### FAQ Schema (Single Question)

```html
<div itemscope itemprop="mainEntity" 
itemtype="https://schema.org/Question" 
style="background: #FAFAFA; padding: 20px; margin: 15px 0; 
border-radius: 4px;">
<h3 itemprop="name" style="color: #424242; margin-top: 0;">
[QUESTION]</h3>
<div itemscope itemprop="acceptedAnswer" 
itemtype="https://schema.org/Answer">
<div itemprop="text">
<p>[COMPREHENSIVE ANSWER 150-250 words]</p>
</div>
</div>
</div>
```

### FAQ Section (Complete)

```html
<section>
<h2>Întrebări frecvente (FAQ)</h2>

<!-- Repeat this block 6 times -->
<div itemscope itemprop="mainEntity" 
itemtype="https://schema.org/Question" 
style="background: #FAFAFA; padding: 20px; margin: 15px 0; 
border-radius: 4px;">
<h3 itemprop="name" style="color: #424242; margin-top: 0;">
[Question]</h3>
<div itemscope itemprop="acceptedAnswer" 
itemtype="https://schema.org/Answer">
<div itemprop="text">
<p>[Answer]</p>
</div>
</div>
</div>

</section>
```

### 2Performant Affiliate Link

```html
<a href="https://event.2performant.com/events/click?ad_type=quicklink&aff_code=80f42fe2f&unique=[TAG]&redirect_to=[URL_ENCODED]" 
target="_blank" rel="noopener">[ANCHOR_TEXT]</a>
```

**Variables:**
- `[TAG]` - Tracking tag (e.g., `article_3423_burnout_book`)
- `[URL_ENCODED]` - Product URL (URL encoded)
- `[ANCHOR_TEXT]` - Link text (e.g., "Ghiduri de psihologie")

---

## Troubleshooting

### Connection Issues

**Problem:** Can't connect to inteles.ro

**Diagnosis:**
```bash
# Test site accessibility
curl -I https://inteles.ro

# Test REST API
curl https://inteles.ro/wp-json/

# Test authentication
curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" \
  "https://inteles.ro/wp-json/wp/v2/posts?per_page=1"
```

**Solutions:**
1. Site down → Wait or contact ZUME
2. REST API disabled → Enable in WordPress settings
3. Auth failed → Regenerate application password

### Authentication Errors

**Problem:** 401 Unauthorized

**Cause:** Invalid credentials

**Fix:**
1. WordPress Admin → Users → Your Profile
2. Application Passwords section
3. Revoke old "mcp" password
4. Create new application password
5. Update config files:
   - `~/.config/Claude/claude_desktop_config.json`
   - `/home/alin/.codeium/windsurf/mcp_config.json`
6. Restart Claude Desktop/Windsurf

### MCP Server Issues

**Problem:** MCP server not available in Claude

**Diagnosis:**
```bash
# Check config is valid JSON
cat ~/.config/Claude/claude_desktop_config.json | jq .

# Test npx works
npx --version

# Test MCP package
npx @instawp/mcp-wp --help
```

**Solutions:**
1. Invalid JSON → Fix syntax errors
2. npx not installed → Install Node.js
3. Package error → Clear npm cache: `npm cache clean --force`
4. Not restarted → Kill and restart Claude Desktop

### Slow Performance

**Problem:** Commands take >30 seconds

**Causes:**
1. Large bulk operations
2. Shared hosting limitations
3. Network issues

**Solutions:**
```
"Process posts one at a time with 2 second delay"
"Batch updates in groups of 10"
"Show me preview before updating all"
```

### Romanian Characters

**Problem:** Garbled text (Ã®nseamnÄƒ instead of înseamnă)

**Status:** Visual issue only - data is correct

**Fix:**
- Usually auto-handled
- If persists: WordPress → Settings → Site Language = "Română"
- Ensure UTF-8 encoding when creating content

---

## Config Files

### Claude Desktop

**Location:** `/home/alin/.config/Claude/claude_desktop_config.json`

```json
{
  "preferences": {
    "menuBarEnabled": false,
    "legacyQuickEntryEnabled": false
  },
  "mcpServers": {
    "inteles-wordpress": {
      "command": "npx",
      "args": ["-y", "@instawp/mcp-wp"],
      "env": {
        "WORDPRESS_API_URL": "https://inteles.ro",
        "WORDPRESS_USERNAME": "baretrea",
        "WORDPRESS_PASSWORD": "Yzix4308YGsRNLirTWJfdztM"
      }
    }
  }
}
```

### Windsurf

**Location:** `/home/alin/.codeium/windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "inteles-wordpress": {
      "command": "npx",
      "args": ["-y", "@instawp/mcp-wp"],
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
- Use `env` for credentials (NOT `args`)
- Package: `@instawp/mcp-wp`
- Same credentials for both tools

---

## Useful Scripts

### Test REST API Connection

```bash
#!/bin/bash
# test-wp-api.sh

API_URL="https://inteles.ro/wp-json/wp/v2"
USERNAME="baretrea"
PASSWORD="Yzix4308YGsRNLirTWJfdztM"

echo "Testing WordPress REST API..."

# Test unauthenticated
echo -n "Unauthenticated access: "
curl -s -o /dev/null -w "%{http_code}" "$API_URL/posts?per_page=1"
echo

# Test authenticated
echo -n "Authenticated access: "
curl -s -o /dev/null -w "%{http_code}" \
  -u "$USERNAME:$PASSWORD" "$API_URL/posts?per_page=1"
echo

# Get actual post
echo -e "\nFirst post:"
curl -s -u "$USERNAME:$PASSWORD" "$API_URL/posts?per_page=1" | \
  jq '.[] | {id, title: .title.rendered, date}'
```

### Validate Config JSON

```bash
#!/bin/bash
# validate-config.sh

CONFIG="$HOME/.config/Claude/claude_desktop_config.json"

echo "Validating $CONFIG..."

if jq empty "$CONFIG" 2>/dev/null; then
    echo "✓ Valid JSON"
    echo -e "\nMCP Servers configured:"
    jq -r '.mcpServers | keys[]' "$CONFIG"
else
    echo "✗ Invalid JSON"
    echo "Run: cat $CONFIG | jq ."
    exit 1
fi
```

### Count Articles by Category

```bash
#!/bin/bash
# count-by-category.sh

API_URL="https://inteles.ro/wp-json/wp/v2"
USERNAME="baretrea"
PASSWORD="Yzix4308YGsRNLirTWJfdztM"

# Get categories
curl -s -u "$USERNAME:$PASSWORD" "$API_URL/categories" | \
  jq -r '.[] | "\(.id) \(.name) (\(.count) posts)"'
```

---

## Performance Optimization

### Rate Limiting

**ZUME Shared Hosting:**
- No official rate limit
- Recommended: <10 requests/second
- For bulk ops: Add delays

**Implementation:**
```
"Update posts with 1 second delay between each"
"Process in batches of 10 with 5 second delay between batches"
```

### Caching

**WordPress Caching:**
- ZUME uses server-level caching
- REST API responses not cached by default
- Consider WordPress caching plugin for frontend

**Client-Side:**
- MCP doesn't cache (always fresh data)
- Consider caching for read-heavy operations

### Large Operations

**Best Practices:**
1. **Preview first:** "Show me what will change"
2. **Batch processing:** Groups of 10-20
3. **Add delays:** 1-2 seconds between requests
4. **Monitor progress:** "Update one at a time and show status"
5. **Error handling:** "Stop if any update fails"

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Wrong credentials | Regenerate app password |
| 403 Forbidden | Insufficient permissions | Check user role (should be admin) |
| 404 Not Found | Post doesn't exist | Verify post ID |
| 500 Server Error | WordPress issue | Check error logs, contact ZUME |
| Timeout | Large operation | Add delays, batch process |
| JSON parse error | Invalid response | Check WordPress REST API status |

---

## FAQ

**Q: How do I restart Claude Desktop after config change?**
A: `pkill -f claude-desktop && sleep 2 && claude-desktop &`

**Q: How do I test if WordPress REST API is working?**
A: `curl https://inteles.ro/wp-json/`

**Q: How do I generate a new 2Performant affiliate link?**
A: Dashboard → Linkuri Rapide → Search product → Generate

**Q: How do I rollback a post to previous version?**
A: WordPress Admin → Post → Revisions (right sidebar)

**Q: What's the max affiliate links per article?**
A: 1-2 (balanced approach) - see [[03-MONETIZATION-GUIDE]]

**Q: How often should I check 2Performant stats?**
A: Weekly for tracking, monthly for analysis

---

## Resources

### Documentation
- WordPress REST API: https://developer.wordpress.org/rest-api/
- MCP Protocol: https://modelcontextprotocol.io/
- @instawp/mcp-wp: https://www.npmjs.com/package/@instawp/mcp-wp

### Tools
- 2Performant: https://event.2performant.com/
- WordPress Admin: https://inteles.ro/wp-admin
- ZUME cPanel: Via email link

### Support
- ZUME Hosting: support@zume.ro
- WordPress Forums: https://wordpress.org/support/
- MCP Community: GitHub issues

---

**See also:**
- [[01-SETUP-GUIDE]] - Initial setup instructions
- [[02-CONTENT-STRATEGY]] - Content creation standards
- [[03-MONETIZATION-GUIDE]] - Affiliate best practices
- [[04-ARTICLE-TRACKING]] - Current article status
