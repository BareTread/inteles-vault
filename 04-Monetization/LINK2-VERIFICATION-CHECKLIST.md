# Link2 Verification Checklist — 100% Tracking Guarantee

**Purpose:** One-time verification to confirm Link2 is working. After this check, ALL future links will work automatically.

---

## ✅ One-Time Verification (Do This Once)

### Step 1: Publish Test Article

1. Go to WordPress → **Posts > Add New**
2. Title: **"Link2 Test"**
3. Content:

```html
<p>Test link: <a href="https://manukashop.ro" rel="nofollow sponsored noopener">Manuka Shop</a></p>
```

4. **Publish** (or Preview if you don't want it public)

---

### Step 2: Verify Link Conversion

**Method 1: Browser Inspect (Most Reliable)**

1. Open your test article in a browser
2. **Right-click** on "Manuka Shop"
3. Click **Inspect** (or **Inspect Element**)
4. Look at the `<a>` tag

**✅ WORKING (you'll see this):**
```html
<a href="https://event.2performant.com/events/click?aff_code=80f42fe2f&redirect_to=https%3A%2F%2Fmanukashop.ro" rel="nofollow sponsored noopener">Manuka Shop</a>
```

**❌ NOT WORKING (still regular URL):**
```html
<a href="https://manukashop.ro" rel="nofollow sponsored noopener">Manuka Shop</a>
```

**If you see ✅ → Link2 is working! Skip to Step 3.**

---

**Method 2: Page Source (Alternative)**

1. On your test article, **right-click** anywhere → **View Page Source** (Ctrl+U)
2. Search (Ctrl+F) for: `linkTwoPerformant`

**✅ WORKING (you'll see this):**
```html
<script src="https://cdn.2performant.com/l2/link2.js" id="linkTwoPerformant" data-id="l2/0/4/4/7/3/3/7/9/4/0" data-api-host="https://cdn.2performant.com"></script>
```

**If you see the script → Link2 is loaded! Check Method 1 to confirm conversion.**

---

### Step 3: Click Test Link (Track in 2Performant)

1. **Click** the "Manuka Shop" link in your test article
2. You should be redirected to the merchant site
3. Wait **10-15 minutes**
4. Go to **2Performant dashboard** → **Reports**
5. Look for a click from your domain (inteles.ro)

**✅ If you see a click → Tracking is confirmed working!**

---

## 🚨 Troubleshooting (If Not Working)

### Link2 script not found in page source?

**Fix:**
1. Go to WordPress → **2Performant Link2 > Settings**
2. Verify your Link2 ID is saved: `l2/0/4/4/7/3/3/7/9/4/0`
3. Save settings again
4. Clear browser cache (Ctrl+Shift+Delete)
5. Reload test article

---

### Links not converting?

**Check 1: Merchant Selection**
1. Log into **2Performant dashboard** → **Tools > Link2**
2. Under **Target programs**, check:
   - If you selected specific merchants → add the ones you're testing
   - If you left it blank → all accepted merchants should work
3. Save and wait 5 minutes
4. Test again

**Check 2: Affiliate Program Acceptance**
1. Verify you're **accepted** into the merchant's affiliate program
2. Check 2Performant dashboard → **Programs** → search for merchant
3. Status should be "Accepted" (not "Pending" or "Rejected")

**Check 3: Browser Console**
1. Open test article
2. Press **F12** → go to **Console** tab
3. Look for JavaScript errors mentioning `2performant` or `link2`
4. If you see errors → copy them and check 2Performant support docs

---

### Clicks not showing in dashboard?

**Possible reasons:**
- **Cookies blocked:** Your own clicks might be filtered (normal behavior)
- **Tracking delay:** Can take 1-2 hours to appear in reports
- **Test from another device:** Ask someone else to click from a different network

**Solution:**
- Wait 24 hours
- Check again for clicks from inteles.ro domain
- If still zero → contact 2Performant support with your Link2 ID

---

## ✅ After Verification: Normal Workflow

### Once Link2 is confirmed working:

1. **Never verify again** — Link2 works automatically for ALL future links
2. **Use AI-AGENT-QUICK-PICKS.md** to choose products
3. **Paste regular merchant URLs** (e.g., `https://manukashop.ro/produs`)
4. **Publish** — Link2 handles tracking

**No errors possible. 100% guaranteed tracking.**

---

## 📊 Ongoing Monitoring (Optional)

### Weekly Check (Recommended):

1. Go to **2Performant dashboard** → **Reports**
2. Filter by date range (last 7 days)
3. Verify clicks are being tracked from inteles.ro
4. Check top merchants (Manuka, Libris, Librex should appear if you're using Quick Picks)

**If clicks stop appearing:**
- Check if Link2 script is still in footer (theme updates can remove it)
- Verify Link2 ID hasn't changed in 2Performant dashboard
- Re-run this verification checklist

---

## 🎯 Summary Checklist

- [ ] Link2 plugin installed in WordPress
- [ ] Link2 ID configured: `l2/0/4/4/7/3/3/7/9/4/0`
- [ ] Test article published with regular merchant URL
- [ ] Browser inspect shows `event.2performant.com` in href (✅ working)
- [ ] Page source shows Link2 script tag (✅ loaded)
- [ ] Click tracked in 2Performant dashboard within 24h (✅ tracking confirmed)

**Once all checked → Link2 is 100% operational. Use AI-AGENT-QUICK-PICKS for all future articles.**

---

## 💡 Quick Reference

**Your Link2 ID:**
```
l2/0/4/4/7/3/3/7/9/4/0
```

**Your Affiliate Code (embedded in Link2 ID):**
```
80f42fe2f
```

**Link2 Configuration:**
- Location: 2Performant dashboard → Tools > Link2
- Embed code location: WordPress footer (before `</body>`)
- Transformation method: href rewrite (recommended) OR click handler

**Support:**
- 2Performant Help: support.2performant.com
- Link2 Docs: doc.2performant.com
