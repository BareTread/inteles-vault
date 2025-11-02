# AI Agent Workflow — Inevitable Success System

**Purpose:** Foolproof, linear workflow. Follow these steps → success guaranteed.

**Entry Point:** This file. Load ONLY the files referenced in each step.

---

## 🎯 Before You Start

### Load These Files (In Order):

1. **This file** (`AI-AGENT-WORKFLOW.md`) — You are here
2. **`00-AGENT-CONTEXT/02-WRITING-RUBRIC.md`** — Quality standards (score ≥7/10)
3. **`04-Monetization/AI-AGENT-QUICK-PICKS.md`** — Product selection (10 seconds)
4. **`07-Templates/[template-name]`** — Article structure (load when writing)

**DO NOT load:** `11-Source-Docs/` (bloat), `history.md`, full MASTER-PRODUCTS-LIST

---

## 📋 Workflow: Write & Publish Article

### STEP 1: Receive Task

**Input formats:**
- "Write article about [topic]"
- "Update article ID [number]"
- "Create dream interpretation for [symbol]"

**Extract:**
- Main topic/keyword
- Article type (dream interpretation, "ce înseamnă", general)
- Target word count (default: 2,000-2,500 words)

---

### STEP 2: Choose Template

**Load the correct template based on topic:**

| Topic Type | Template to Load |
|------------|------------------|
| Dream symbol (vis cu...) | `07-Templates/TPL-Vis-Interpretare.md` |
| Definition (ce înseamnă...) | `07-Templates/TPL-Ce-Inseamna.md` |
| General psychology | `07-Templates/TPL-Vis-Interpretare.md` (adapt) |

**Load ONLY the template you need.** Don't load all templates.

---

### STEP 3: Select Product (10 Seconds)

**Open:** `04-Monetization/AI-AGENT-QUICK-PICKS.md` (already loaded)

**Scan article topic for keywords:**

```
IF topic contains: ["energie", "dimineață", "trezire", "vitalitate"]
  → Product: Manuka honey (18% commission)
  → URL: https://manukashop.ro/miere-de-manuka-mgo-550-500g.html

ELSE IF topic contains: ["Jung", "Freud", "carte", "psihologie", "simboluri", "arhetipuri"]
  → Product: Jung - Analiza viselor (8% commission)
  → URL: https://www.libris.ro/analiza-viselor-c-g-jung-TRE978-606-40-0393-5--p1258533.html

ELSE IF topic contains: ["jurnal", "înregistrare", "notițe", "tracking"]
  → Product: Jurnal de vise (10% commission)
  → URL: https://librex.ro/jurnal-vise

ELSE IF topic contains: ["insomnie", "somn", "anxietate", "stres", "coșmaruri"]
  → Product: Melatonină (3.5% commission)
  → URL: https://www.springfarma.com/melatonina-pura-5-mg-60-tablete.html

ELSE (default for ANY dream article)
  → Product: Libris homepage (8% commission)
  → URL: https://www.libris.ro
```

**Copy the URL.** You'll use it in Step 5.

**Rule:** Only 1 product per article (€5,000/month proven strategy).

---

### STEP 4: Write Article

**Follow the template structure exactly.**

**Example for Dream Interpretation:**

```markdown
# [Symbol] în vise: Semnificație și interpretare

[Intro paragraph - 2-3 sentences with quick answer]

## Semnificația de bază

[Plain language explanation - 150-200 words]

## Perspectiva psihologică

[Jung/Freud insights - 200-300 words]
[Cite: "După Carl Jung, visele cu [symbol]..."]

## Scenarii comune

[3-6 concrete scenarios, each 50-80 words]

### Dacă visezi [scenario 1]
[Interpretation]

### Dacă visezi [scenario 2]
[Interpretation]

### Dacă visezi [scenario 3]
[Interpretation]

## Tradiții românești (optional if relevant)

[Cultural context - 100-150 words]

## Resurse pentru aprofundare

[PASTE RESOURCE BOX HERE - see Step 5]

## Întrebări frecvente

[6-8 FAQ with schema markup - see Step 6]

## Concluzie

[Brief recap - 80-100 words]
[Cite 1-2 credible sources: Jung, Wikipedia-RO, etc.]
```

**Writing Guidelines:**
- Mobile-first: Short paragraphs (2-3 sentences max)
- Use H2/H3 every 300-400 words
- Professional tone, empathetic, no AI tells
- Romanian diacritics mandatory
- No filler phrases: "It's important to note", "In conclusion"
- Quick answer in first 2-3 paragraphs

---

### STEP 5: Insert Resource Box

**Use this exact HTML template:**

```html
<div style="background:#E8F5E9;border-left:4px solid #4CAF50;padding:20px;margin:25px 0;border-radius:8px;box-shadow:0 3px 12px rgba(0,0,0,0.06)">
  <h3 style="margin:0 0 10px;color:#2E7D32">📚 Resurse pentru aprofundare</h3>
  <p style="margin:0 0 6px">Pentru aprofundare, vezi <a href="[PASTE_URL_FROM_STEP_3]" rel="nofollow sponsored noopener">[product name]</a>.</p>
  <p style="font-size:.85rem;color:#666;margin:10px 0 0"><em>Link afiliat — câștigăm un mic comision fără costuri pentru tine.</em></p>
</div>
```

**Replace:**
- `[PASTE_URL_FROM_STEP_3]` → URL you copied in Step 3
- `[product name]` → Product name from Step 3

**Example:**
```html
<p style="margin:0 0 6px">Pentru aprofundare, vezi <a href="https://www.libris.ro/analiza-viselor-c-g-jung-TRE978-606-40-0393-5--p1258533.html" rel="nofollow sponsored noopener">Analiza viselor de C.G. Jung</a>.</p>
```

**Placement:** AFTER main content, BEFORE FAQ section.

---

### STEP 6: Add FAQ Section

**Minimum 6 questions. Use this schema.org markup:**

```html
<div itemscope itemtype="https://schema.org/FAQPage">

  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">Ce înseamnă când visezi [symbol]?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <div itemprop="text">
        <p>[Answer - 2-3 sentences]</p>
      </div>
    </div>
  </div>

  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">Este un vis bun sau rău?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <div itemprop="text">
        <p>[Answer - 2-3 sentences]</p>
      </div>
    </div>
  </div>

  <!-- Repeat for 6-8 total questions -->

</div>
```

**Common FAQ patterns for dream interpretation:**
1. Ce înseamnă când visezi [symbol]?
2. Este un vis bun sau rău?
3. Ce spune psihologia despre acest vis?
4. Cum interpretează Jung/Freud acest simbol?
5. Ar trebui să fiu îngrijorat/ă?
6. Ce pot face după ce am visat acest lucru?

---

### STEP 7: Quality Check (Score ≥7/10)

**Load:** `00-AGENT-CONTEXT/02-WRITING-RUBRIC.md`

**Check each criterion (1-10 scale):**

1. **Intent** — Quick answer in first 2-3 paragraphs? [Score: __/10]
2. **Depth** — Real psychological/cultural insight? [Score: __/10]
3. **Structure** — H2/H3 every 300-400 words? [Score: __/10]
4. **Length** — 2,000-2,500 words, no filler? [Score: __/10]
5. **Mobile** — Short paragraphs, clear spacing? [Score: __/10]
6. **Credibility** — Cited 1-2 sources? [Score: __/10]
7. **FAQs** — ≥6 Q&A with schema? [Score: __/10]
8. **Images** — 1-2 helpful visuals planned? [Score: __/10]
9. **Monetization** — 1 contextual link in resource box? [Score: __/10]
10. **Language** — Romanian diacritics, professional tone? [Score: __/10]

**Total: __/100**

**If <70 → Fix issues before Step 8**
**If ≥70 → Proceed to Step 8**

---

### STEP 8: Publish to WordPress (Optional - If MCP Available)

**If WordPress MCP is configured:**

Use MCP WordPress tools to:
1. Create new post
2. Set category (5 for dream interpretations)
3. Set status: `publish`
4. Add featured image (if available)

**If MCP not available:**
- Copy HTML to clipboard
- User will paste manually

---

### STEP 9: Verification Checklist

**Before marking task complete, verify:**

- [ ] Article follows template structure
- [ ] Quick answer in first 2-3 paragraphs
- [ ] 1 product from Step 3 included in resource box
- [ ] Resource box uses regular merchant URL (Link2 converts automatically)
- [ ] `rel="nofollow sponsored noopener"` on affiliate link
- [ ] Disclosure text present
- [ ] 6+ FAQ with schema.org markup
- [ ] Quality score ≥70/100
- [ ] Romanian diacritics used throughout
- [ ] No AI filler phrases

**Once all checked → Task complete ✅**

---

## 🚨 Common Mistakes to AVOID

### ❌ Don't:
1. Load `11-Source-Docs/` files (bloat, outdated info)
2. Use manual 2Performant quicklinks (use regular URLs + Link2)
3. Add more than 1 product (1 product = €5,000/month proven)
4. Skip quality check (must score ≥70/100)
5. Use complex tables (mobile users = 97.5% traffic)
6. Write AI filler ("It's important to note...", "In conclusion...")
7. Forget Romanian diacritics (ă, â, î, ș, ț)
8. Place product before main content (value first, monetization after)

### ✅ Do:
1. Follow this linear workflow step-by-step
2. Load only files mentioned in each step
3. Use templates exactly as provided
4. Verify quality score before publishing
5. Use 1 high-commission product (Manuka 18% > Libris 8%)
6. Place resource box AFTER content, BEFORE FAQ
7. Include disclosure on all affiliate links

---

## 📊 Success Metrics

**If you followed this workflow correctly:**

✅ Article structure matches template (100%)
✅ Quality score ≥70/100 (target: 80+)
✅ Mobile-optimized (short paragraphs, H2/H3 breaks)
✅ 1 contextual affiliate link with disclosure
✅ Link2 auto-converts URL (verified working)
✅ 6+ FAQ with schema markup
✅ Credible sources cited
✅ Romanian diacritics throughout
✅ No AI tells or filler

**This workflow = inevitable success. No exceptions.**

---

## 🎯 Quick Reference Card

```
STEP 1: Receive task → Extract topic
STEP 2: Load template (TPL-Vis-Interpretare or TPL-Ce-Inseamna)
STEP 3: Select product from AI-AGENT-QUICK-PICKS (10 sec)
STEP 4: Write article following template structure
STEP 5: Insert resource box with regular URL
STEP 6: Add 6+ FAQ with schema
STEP 7: Quality check (score ≥70/100)
STEP 8: Publish (MCP or manual)
STEP 9: Verify checklist
```

**Time:** 15-20 minutes per article (high quality, no errors)

---

## 🔄 Update Workflow (Existing Articles)

**If task is to UPDATE existing article:**

1. Fetch article from WordPress (use MCP or manual)
2. Load `07-Templates/TPL-Audit-Articol.md`
3. Follow audit template to identify gaps
4. Apply fixes from this workflow (Steps 4-7)
5. Publish updated version
6. Verify checklist (Step 9)

---

## 💡 Pro Tips

### Maximum Revenue:
- Energy/morning topics → Always use Manuka (18%)
- Psychology topics → Always use Libris Jung/Freud (8%)
- Sleep issues → SpringFarma (3.5%)
- Default → Libris homepage (8%)

### Quick Quality Boost:
- Add Jung/Freud citation → +2 credibility points
- Add Romanian tradition section → +1 cultural relevance
- Use concrete scenarios → +2 depth points
- Short paragraphs (2-3 sentences) → +2 mobile points

### Common Quick Wins:
- Replace "Este important de menționat" → Delete, state directly
- Replace "În concluzie putem spune" → Delete, conclude directly
- Add line breaks between paragraphs → Better mobile spacing
- Use lists instead of long paragraphs → Easier scanning

---

## 🆘 Troubleshooting

### "Quality score <70"
→ Check Writing Rubric, fix weakest criterion
→ Most common: Missing quick answer, no sources cited, long paragraphs

### "Don't know which product to choose"
→ Use default: Libris homepage (fits ALL dream articles)
→ URL: `https://www.libris.ro`

### "Template unclear"
→ Look at existing article as example (ask user for article ID)
→ Follow structure exactly, adapt content only

### "Link2 not converting"
→ Verify you used REGULAR URL (not quicklink)
→ Check Link2 verification checklist if needed
→ User already verified it works (confirmed in this session)

---

## 📝 Files Reference

**Core Workflow Files (Load These):**
- `AI-AGENT-WORKFLOW.md` ← YOU ARE HERE
- `00-AGENT-CONTEXT/02-WRITING-RUBRIC.md` — Quality standards
- `04-Monetization/AI-AGENT-QUICK-PICKS.md` — Product selection
- `07-Templates/TPL-Vis-Interpretare.md` — Dream template
- `07-Templates/TPL-Ce-Inseamna.md` — Definition template

**Reference (Load If Needed):**
- `07-Templates/HTML-Resource-Box.md` — Resource box variants
- `07-Templates/HTML-FAQ-Block.md` — FAQ markup examples
- `04-Monetization/LINK2-VERIFICATION-CHECKLIST.md` — If tracking issues

**DO NOT Load (Bloat):**
- `11-Source-Docs/*` — Outdated, token-heavy
- `history.md` — Session logs
- `MASTER-PRODUCTS-LIST.md` — Use Quick Picks instead
- Any file in `.archive/` directories

---

**SUCCESS IS INEVITABLE. Follow steps 1-9. No shortcuts. No exceptions.**
