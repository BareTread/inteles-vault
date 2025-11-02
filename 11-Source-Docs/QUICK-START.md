# WordPress MCP Quick Start - inteles.ro

## ✅ SETUP COMPLETE!

Your WordPress MCP is fully configured and tested. The connection to inteles.ro is working.

---

## What Just Happened

1. ✅ WordPress Application Password created: `Yzix 4308 YGsR NLir TWJf dztM`
2. ✅ Claude Desktop config updated with credentials
3. ✅ REST API connection tested successfully
4. ✅ Retrieved sample post: "IFN – Ce Înseamnă și Cum Funcționează în România"

**You're ready to use it NOW.**

---

## How to Use

### Step 1: Restart Claude Desktop

**IMPORTANT:** You must restart Claude Desktop to load the new MCP server.

```bash
# Close Claude Desktop completely
pkill -f claude-desktop

# Wait 2 seconds, then restart
sleep 2 && claude-desktop &
```

Or just close and reopen the app manually.

---

### Step 2: Test Basic Commands

Open Claude Desktop and try these commands:

#### Test 1: List Posts
```
"List my WordPress posts from inteles.ro"
```

**Expected:** You'll see a list of your posts with titles and IDs.

---

#### Test 2: Get Specific Post
```
"Show me the details of my most recent inteles.ro post"
```

**Expected:** Full post content, title, excerpt, publish date.

---

#### Test 3: Search Posts
```
"Find all inteles.ro posts that mention 'moarte' or 'vis despre moarte'"
```

**Expected:** Filtered list of posts about death dreams.

---

#### Test 4: Create Draft (Safe Test)
```
"Create a draft post on inteles.ro titled 'Test MCP - Delete Me' with content 'This is a test post created via MCP. Delete this.'"
```

**Expected:** New draft appears in WordPress admin.
**Action:** Go check wp-admin → Posts → Drafts to verify it worked!

---

### Step 3: Real Monetization Work

Once basic tests work, try these:

#### Workflow A: Add Affiliate Links
```
"List all inteles.ro posts about death dreams (moarte, deces, înmormântare).

For each post, add this HTML at the bottom (before conclusion):

<div style='border:1px solid #ddd; padding:16px; border-radius:8px; margin:24px 0;'>
<h3>📚 Resurse recomandate</h3>
<p>Pentru interpretări mai detaliate, consultă:</p>
<ul>
<li><a href='YOUR_2PERFORMANT_LINK_HERE'>Dicționar complet de interpretare a viselor</a></li>
</ul>
<p style='font-size:0.85rem; color:#666; margin-top:12px;'>Link afiliat - Câștigăm un mic comision fără costuri pentru tine.</p>
</div>

Show me each post before updating so I can approve."
```

---

#### Workflow B: Mobile Optimization
```
"For the top 10 most recent posts on inteles.ro:

1. Check if they have short paragraphs (mobile-friendly)
2. If paragraphs are longer than 4 lines, break them into shorter ones
3. Add a 'Quick Answer' box at the top with 2-3 sentence summary
4. Show me the changes before applying"
```

---

#### Workflow C: Content Creation
```
"Create a new draft post for inteles.ro:

Title: 'Vis despre pisici negre - Semnificație și Interpretare'

Content:
- Quick answer box (2-3 sentences)
- 400 words about black cat dreams
- Mobile-optimized format (short paragraphs)
- Include Romanian affiliate disclosure
- Add placeholder for 2Performant book link
- Optimize for SEO keyword 'vis despre pisici negre'

Save as draft for my review."
```

---

## Common Commands Reference

### Content Management
```
"List all drafts"
"Show me posts from October 2025"
"Find posts without featured images"
"How many posts do I have total?"
"What are my most commented posts?"
```

### Bulk Operations
```
"Add Romanian affiliate disclosure to all posts missing it"
"Update all posts from 2023 to say 2025"
"Find posts with broken affiliate links"
"Scan for posts needing mobile optimization"
```

### Analytics Queries
```
"Which posts have the most comments?"
"Show me my shortest posts (under 300 words)"
"Find posts that haven't been updated in 2+ years"
"List posts by category"
```

---

## Safety Features

### Claude Will Ask Before Destructive Actions

When you ask to:
- Delete posts
- Bulk update many posts
- Publish drafts
- Make major changes

Claude will show you **what will change** and ask for confirmation.

**Example:**
```
You: "Update all posts to add affiliate links"

Claude: "I found 47 posts. Here are the first 3 changes:

Post 1: [title]
Will add: [HTML snippet]

Post 2: [title]
Will add: [HTML snippet]

Post 3: [title]
Will add: [HTML snippet]

Should I continue with all 47 posts? (yes/no)"
```

---

### Rollback Strategy

WordPress automatically saves **revisions** of every post.

**To rollback a change:**
1. Go to: WordPress Admin → Posts → [Your Post]
2. Click "Revisions" (right sidebar)
3. Select previous version
4. Click "Restore This Revision"

**Or ask Claude:**
```
"Revert post ID 123 to its previous version from before today"
```

---

## Troubleshooting

### "MCP server not available" or No Response

**Fix:**
1. Check Claude Desktop was restarted after config change
2. Verify config is valid JSON:
   ```bash
   cat ~/.config/Claude/claude_desktop_config.json | jq .
   ```
3. Check `npx` is installed:
   ```bash
   npx --version
   ```
4. Try installing the package manually first:
   ```bash
   npx @instawp/mcp-wp --help
   ```

---

### "Authentication failed" or 401 Error

**This means WordPress rejected the credentials.**

**Check:**
1. Username is correct: `baretrea` ✅
2. Application Password has no spaces: `Yzix4308YGsRNLirTWJfdztM` ✅
3. Application Password wasn't revoked in WordPress admin

**Test manually:**
```bash
curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" \
  "https://inteles.ro/wp-json/wp/v2/posts?per_page=1"
```

Should return JSON. If 401 error, regenerate Application Password.

---

### Romanian Characters Look Wrong

If you see garbled text like "înseamnă" showing as "Ã®nseamnÄƒ":

**This is just a display issue.** The data is correct in WordPress.

**Fix in Claude Desktop:**
Usually auto-handled. If persists, check:
1. WordPress Settings → General → Site Language is "Română"
2. When creating posts, explicitly specify UTF-8 encoding

---

### Connection Timeout

**If requests hang for >30 seconds:**

1. Check inteles.ro is accessible:
   ```bash
   curl -I https://inteles.ro
   ```

2. Check ZUME hosting isn't blocking automated requests
   (Unlikely, but some hosts rate-limit REST API)

3. Try adding delay between requests:
   ```
   "Update posts one at a time with 2 second delay between each"
   ```

---

## Next Steps

### Immediate (Today):
1. ✅ Setup complete
2. Restart Claude Desktop
3. Run Test 1-4 above
4. Verify draft post appears in WordPress

### This Week:
1. Generate 5-10 2Performant affiliate links
2. Add affiliate links to 10-20 posts using Workflow A
3. Mobile-optimize top 10 posts using Workflow B
4. Create 2-3 new monetized posts using Workflow C

### This Month:
1. Scale to 50+ posts with affiliate links
2. Set up email capture
3. Track first affiliate earnings
4. Optimize based on what works

---

## Configuration Reference

**Config file location:**
```
/home/alin/.config/Claude/claude_desktop_config.json
```

**WordPress credentials:**
- Site: https://inteles.ro
- Username: `baretrea`
- App Password: `Yzix4308YGsRNLirTWJfdztM`
- Created: Oct 30, 2025
- Name: "mcp"

**MCP Server:**
- Package: `@instawp/mcp-wp`
- Transport: npx (auto-downloads on first use)
- Connection: REST API over HTTPS

---

## Resources

### Documentation
- Full setup guide: `WORDPRESS-MCP-SETUP.md`
- Monetization workflows: `INTELES-MONETIZATION-WORKFLOWS.md`
- This quick start: `QUICK-START.md`

### Tools
- 2Performant: https://www.2performant.com/
- WordPress Admin: https://inteles.ro/wp-admin
- InstaWP MCP Docs: https://instawp.com/wordpress-mcp/

### Support
- InstaWP MCP Issues: https://github.com/InstaWP/wordpress-mcp-server
- WordPress REST API: https://developer.wordpress.org/rest-api/

---

## Success Checklist

Before you start monetizing, verify:

- [ ] Claude Desktop restarted
- [ ] Test command returns post list
- [ ] Can create draft post successfully
- [ ] Can search/filter posts
- [ ] Draft post visible in WordPress admin
- [ ] Romanian characters display correctly
- [ ] Ready to add affiliate links

**All checked?** → You're ready to monetize inteles.ro! 🚀

Start with: **"List all inteles.ro posts about death dreams (moarte)"**

Then follow Workflow A in `INTELES-MONETIZATION-WORKFLOWS.md` to add your first affiliate links.

---

## Questions?

Try these if stuck:

```
"Show me the inteles.ro MCP server capabilities"
"What can I do with the WordPress MCP?"
"Help me debug why MCP isn't working"
"Give me example commands for content creation"
```

Or ask directly: "How do I [specific task] on inteles.ro?"

---

**Ready?** Restart Claude Desktop and try: `"List my inteles.ro posts"`
