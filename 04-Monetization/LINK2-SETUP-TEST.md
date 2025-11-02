# Link2 Setup & Test — Step-by-Step

## Why Link2 is Better

**Before (Manual):**
- Generate each affiliate link manually
- Copy complex 2Performant URLs
- Easy to make mistakes
- Time-consuming

**After (Link2):**
- Paste regular merchant URLs
- Link2 auto-converts → affiliate links
- Zero errors
- Instant

---

## Step 1: Add Link2 Script (One-Time)

### Option A: WordPress Plugin Settings

If you have the 2Performant Link2 plugin installed:
1. Go to WordPress admin → **2Performant Link2 > Settings**
2. Your Link2 ID should already be saved
3. Done!

### Option B: Manual Footer Paste

If you don't have the plugin (or want manual control):
1. Go to **Appearance > Theme File Editor**
2. Find **footer.php** in your theme files
3. Scroll to the bottom, find `</body>`
4. Paste this **RIGHT BEFORE** `</body>`:

```html
<script src="https://cdn.2performant.com/l2/link2.js" id="linkTwoPerformant" data-id="l2/0/4/4/7/3/3/7/9/4/0" data-api-host="https://cdn.2performant.com"></script>
```

5. **Save Changes**

---

## Step 2: Configure Target Merchants

1. Go to **2Performant dashboard** → **Tools > Link2**
2. Under **Target programs**, select which merchants to include:
   - If you select specific merchants → only those will be converted
   - If you leave it blank → ALL accepted merchants will be converted (recommended)
3. Under **Links Transformation**, choose:
   - **✓ href attribute rewrite** (recommended for desktop)
   - OR **Click event handler** (better for status bar privacy)
4. Copy the embed code (it should match what you pasted above)
5. **Save**

---

## Step 3: Test Link2 Works

### Create a Test Article

1. Go to WordPress → **Posts > Add New**
2. Title: "Test Link2"
3. Add this content:

```html
<p>Pentru somn mai bun, vezi produsele de la <a href="https://intimax.ro">Intimax</a>.</p>
<p>Sau caută cărți la <a href="https://libris.ro">Libris</a>.</p>
```

4. **Publish** (or Preview)

### Verify It's Working

**Method 1: Browser Inspect (Best)**
1. Open your test article in a browser
2. Right-click on the "Intimax" link
3. Click **Inspect** (or **Inspect Element**)
4. Look at the `<a>` tag's `href` attribute

**You should see:**
```html
<a href="https://event.2performant.com/events/click?aff_code=80f42fe2f&redirect_to=https%3A%2F%2Fintimaxro&...">Intimax</a>
```

**If you see this → Link2 is working! ✓**

**Method 2: Page Source**
1. On your test article, right-click → **View Page Source** (Ctrl+U)
2. Search (Ctrl+F) for `linkTwoPerformant`
3. You should find the script tag with `data-id="l2/0/4/4/7/3/3/7/9/4/0"`

**If you see this → Link2 script is loaded! ✓**

**Method 3: Browser Console**
1. Open your test article
2. Press **F12** (or Ctrl+Shift+I) → open Developer Tools
3. Go to **Console** tab
4. Type: `document.getElementById('linkTwoPerformant')`
5. Press Enter

**You should see:** The script element object (not null)

**If you see this → Link2 is active! ✓**

---

## Step 4: Check 2Performant Dashboard

1. Wait 10-15 minutes after clicking your test link
2. Go to **2Performant dashboard** → **Reports**
3. Look for clicks from your domain (inteles.ro)

**If you see clicks → Tracking is working! ✓**

---

## Troubleshooting

### Link2 script not loading?
- Check footer.php → script should be before `</body>`
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console (F12) for JavaScript errors

### Links not converting?
- Verify you selected merchants in 2Performant > Tools > Link2
- Make sure you're accepted into those affiliate programs
- Check the merchant URL is correct (https://merchant.ro not http://)

### Status bar shows original URL?
- This is normal if you chose "Click event handler" method
- The link will still redirect through 2Performant when clicked
- Switch to "href attribute rewrite" if you prefer

### Zero clicks in dashboard?
- Wait longer (tracking can be delayed 1-2 hours)
- Clear browser cookies (your own clicks might be filtered)
- Ask a friend to click from a different device/network

---

## After Testing: Clean Workflow

### For New Articles:

1. **Choose product:** Check [[MASTER-PRODUCTS-LIST.ACCEPTED]]
2. **Paste URL:** Use regular merchant URL (e.g., `https://intimax.ro/produs`)
3. **Add disclosure:** "Link afiliat — câștigăm un mic comision fără costuri pentru tine."
4. **Publish:** Link2 handles the rest!

### Product List Updates (Monthly):

```bash
bash scripts/monetization-refresh.sh
```

This refreshes your accepted merchants and product recommendations.

---

## Your Link2 ID

For reference, your unique Link2 configuration is:

```
l2/0/4/4/7/3/3/7/9/4/0
```

This encodes:
- Your affiliate code (`80f42fe2f`)
- Which merchants you selected
- Transformation method

If you change settings in 2Performant > Tools > Link2, you'll get a new ID.

---

## Summary

✅ **Setup:** Add Link2 script to footer (once)
✅ **Configure:** Select merchants in 2Performant dashboard
✅ **Test:** Create test article, inspect link, verify conversion
✅ **Write:** Paste regular merchant URLs, Link2 converts automatically
✅ **Track:** Check 2Performant dashboard for clicks & conversions

**No more manual quicklink generation!**
