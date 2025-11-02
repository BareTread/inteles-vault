# inteles.ro - WordPress MCP Automation Setup

## 🎉 Setup Complete!

Your Claude Desktop can now edit inteles.ro WordPress posts directly via natural language commands.

---

## What Was Configured

✅ **WordPress MCP Server** installed and configured
✅ **Application Password** created: `Yzix 4308 YGsR NLir TWJf dztM`
✅ **REST API connection** tested and working
✅ **Claude Desktop config** updated with credentials

**Status:** Ready to use (just restart Claude Desktop)

---

## Quick Reference

### 📋 Documents Created

1. **`QUICK-START.md`** ← **START HERE**
   - How to test the setup
   - Basic commands to try first
   - Troubleshooting common issues

2. **`WORDPRESS-MCP-SETUP.md`**
   - Complete technical documentation
   - Security notes
   - Configuration reference
   - Advanced troubleshooting

3. **`INTELES-MONETIZATION-WORKFLOWS.md`**
   - 7 monetization workflows
   - 2Performant affiliate integration
   - Content creation templates
   - Revenue projections
   - Romanian legal compliance

4. **`README.md`** (this file)
   - Quick overview
   - Links to other docs

---

## Your Site Stats (Context)

- **URL:** https://inteles.ro
- **Traffic:** 437 clicks/day (~13,100/month)
- **CTR:** 30.67% (very high engagement!)
- **Device:** 97.5% mobile
- **Language:** Romanian + diaspora

**Revenue Potential:** €600-1,200/month with proper monetization

---

## How to Start (3 Steps)

### Step 1: Restart Claude Desktop
```bash
pkill -f claude-desktop
sleep 2
claude-desktop &
```

### Step 2: Test Connection
Open Claude Desktop, type:
```
"List my WordPress posts from inteles.ro"
```

### Step 3: Start Monetizing
Pick a workflow from `INTELES-MONETIZATION-WORKFLOWS.md`:
```
"Find all inteles.ro posts about death dreams and add affiliate links for dream interpretation books"
```

---

## Configuration Details

**Location:**
```
/home/alin/.config/Claude/claude_desktop_config.json
```

**WordPress Credentials:**
- Username: `baretrea`
- App Password: `Yzix4308YGsRNLirTWJfdztM`
- Site: https://inteles.ro

**MCP Server:**
- Package: `@instawp/mcp-wp`
- Connection: WordPress REST API (HTTPS)
- Transport: npx (auto-installs on first use)

---

## What You Can Do

### Content Management
- Create, edit, delete posts
- Search by keyword, date, category
- Manage drafts and published content
- Update metadata (titles, excerpts, etc.)

### Bulk Operations
- Add affiliate links to multiple posts
- Update old content with new information
- Mobile-optimize entire site
- Add disclosure text site-wide

### Monetization
- Insert 2Performant affiliate links
- Add email capture forms
- Optimize for Romanian market
- Create new monetized content

---

## Example Commands

```
"Show me my 10 most recent posts"

"Find posts about 'vis despre moarte' and add this affiliate link: [link]"

"Create a new draft post about cat dreams with Romanian affiliate disclosure"

"Mobile-optimize all posts published this month"

"Add email signup form to posts with >50 comments"

"Generate content calendar for next 4 weeks"
```

---

## 2Performant Affiliate Accounts

Your active merchants:
- **Libris.ro** - Books (8% commission)
- **Librex.ro** - Journals, stationery
- **SpringFarma.com** - Health supplements (6%)
- **evoMAG.ro** - Electronics (4%)
- **Flanco.ro** - Home appliances (4%)
- **Manukashop.ro** - Honey products

**Login:** https://event.2performant.com/

---

## Revenue Model

### Month 1-2 (Setup):
- 20-30 posts with affiliate links
- €150-300/month

### Month 3-4 (Growth):
- 50-80 posts with affiliate links
- Email list building
- €300-600/month

### Month 6+ (Optimized):
- 100+ monetized posts
- 500-1,000 email subscribers
- €600-1,200/month

**Time investment:** ~2 hours/week after initial setup

---

## File Structure

```
/mnt/data/Work/inteles-ro/
├── README.md                              ← You are here
├── QUICK-START.md                        ← Read this first
├── WORDPRESS-MCP-SETUP.md                ← Technical docs
└── INTELES-MONETIZATION-WORKFLOWS.md     ← Monetization guide
```

---

## Next Actions (Priority Order)

### Today:
1. [ ] Restart Claude Desktop
2. [ ] Test: "List my inteles.ro posts"
3. [ ] Create test draft post
4. [ ] Verify it appears in WordPress admin

### This Week:
1. [ ] Generate 5-10 2Performant affiliate links
2. [ ] Add affiliate links to 10-20 posts
3. [ ] Mobile-optimize top 10 posts
4. [ ] Create 2-3 new monetized posts

### This Month:
1. [ ] 50+ posts with affiliate links
2. [ ] Email capture form installed
3. [ ] Content calendar for next quarter
4. [ ] First affiliate earnings tracked

---

## Support & Resources

### Documentation
- WordPress REST API: https://developer.wordpress.org/rest-api/
- InstaWP MCP: https://instawp.com/wordpress-mcp/
- 2Performant: https://www.2performant.com/

### Troubleshooting
1. Check `QUICK-START.md` troubleshooting section
2. Test REST API manually: `curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" "https://inteles.ro/wp-json/wp/v2/posts?per_page=1"`
3. Verify config JSON is valid: `cat ~/.config/Claude/claude_desktop_config.json | jq .`

### Legal Compliance (Romanian)
- ANPC requirements for affiliate disclosure
- GDPR for tracking cookies
- See `INTELES-MONETIZATION-WORKFLOWS.md` for details

---

## Security Notes

### Application Password
- **ONLY works for REST API** (not WordPress admin login)
- Can be revoked anytime: WordPress → Users → Your Profile
- Stored securely in `~/.config/Claude/` (only readable by your user)
- Never commit to public Git repos

### Best Practices
✅ Use descriptive names for app passwords ("mcp", "mobile-app", etc.)
✅ Revoke unused passwords regularly
✅ Keep config file in your home directory (not in project root)
❌ Don't share passwords publicly
❌ Don't commit credentials to Git

---

## Technical Details

### MCP Protocol
- **What it is:** Model Context Protocol - standardized way for AI to access external systems
- **How it works:** Claude Desktop → MCP Server → WordPress REST API → inteles.ro
- **Transport:** npx runs Node.js MCP server locally on your machine
- **Security:** HTTPS + WordPress authentication

### REST API Capabilities
✅ Posts, pages, custom post types
✅ Categories, tags, taxonomies
✅ Media uploads
✅ Comments
✅ User data (limited by permissions)
✅ Site settings (read-only)

❌ Plugin installation
❌ Theme changes
❌ File system access
❌ Database direct access

---

## Upgrading Options (Future)

### Option A: Official WordPress MCP Adapter
- Plugin: `WordPress/mcp-adapter`
- More powerful than REST API
- Access to WordPress Abilities API
- Can create custom MCP tools

**When to upgrade:**
- Need features beyond REST API
- Want custom abilities (auto-affiliate insertion)
- Want official WordPress support

### Option B: WP-CLI MCP Server
- Requires SSH access to ZUME hosting
- Most powerful option (full server control)
- More complex setup

**When to upgrade:**
- Have reliable SSH access
- Need server-level operations
- Want maximum control

**Current setup (REST API) is sufficient for 90% of use cases.**

---

## FAQ

**Q: Do I need to install anything on inteles.ro?**
A: No! MCP server runs on your local machine. WordPress just needs REST API enabled (it is by default).

**Q: Can I use this with Codex CLI too?**
A: Yes! Both Claude Code and Codex can use the same MCP configuration.

**Q: Will this work with ZUME shared hosting?**
A: Yes! Uses standard WordPress REST API over HTTPS - works on any host.

**Q: What if I mess something up?**
A: WordPress keeps revisions. You can rollback any post to previous version via admin panel.

**Q: How much does this cost?**
A: $0. All tools are free and open source.

**Q: Can I use this for BareTread too?**
A: Yes! Add another MCP server config with BareTread credentials.

---

## Success Metrics to Track

### Weekly:
- Posts with affiliate links added: Target +5-10
- New content published: Target 1-2 posts
- Affiliate link CTR: Target 2-5%

### Monthly:
- Total monetized posts: Target 50+ (Month 1), 100+ (Month 3)
- Email subscribers: Target +100/month
- 2Performant earnings: Target €300-700
- Mobile bounce rate: Target <60%

---

## Change Log

**Oct 30, 2025:**
- ✅ Initial setup complete
- ✅ WordPress Application Password created
- ✅ Claude Desktop configured
- ✅ REST API connection tested
- ✅ Documentation created
- ⏭️ Ready to start monetizing

---

## Credits & Tools Used

- **WordPress MCP Server:** [@instawp/mcp-wp](https://www.npmjs.com/package/@instawp/mcp-wp)
- **MCP Protocol:** [Anthropic Model Context Protocol](https://modelcontextprotocol.io/)
- **WordPress REST API:** [developer.wordpress.org/rest-api](https://developer.wordpress.org/rest-api/)
- **Hosting:** ZUME.ro (shared hosting with cPanel)
- **Affiliate Network:** 2Performant

---

**Ready to monetize?** → Open `QUICK-START.md` and follow Step 1-3!

Good luck with inteles.ro! 🚀
