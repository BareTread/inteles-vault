# AI Agent Quick Picks — Revenue-Optimized Product Selection

**Purpose:** ZERO decision fatigue. Match article keywords → pick product → paste URL → done.

**Link2 Plugin:** Automatically converts regular URLs to affiliate links. Just paste the merchant URL!

---

## 🎯 Decision Flowchart (Use This First)

```
Article mentions...
├─ Energy/morning/vitalitate → Manuka honey (18% commission) ⭐⭐⭐
├─ Books/Jung/Freud/psychology → Libris books (8% commission) ⭐⭐
├─ Dream journal/tracking → Librex journal (10% commission) ⭐⭐
├─ Sleep issues/insomnia/stress → SpringFarma supplements (3.5%) ⭐
└─ Technology/devices/gadgets → evoMAG/Flanco (1%) ⭐
```

**Rule of Thumb:**
- 1 product per article = HIGHEST commission tier available
- 2 products = Primary (high commission) + Secondary (contextual fit)

---

## 💰 TIER 1: Highest Revenue (18% Commission)

### Manuka Honey (ManukaShop.ro)

**When to use:**
- Article mentions: energie, dimineață, vitalitate, sistem imunitar, sănătate, oboseală
- Dream topics: waking up, morning, energy, vitality, health themes

**Products:**
1. **MGO 550+ (most popular)** → `https://manukashop.ro/miere-de-manuka-mgo-550-500g.html`
2. **MGO 850+ (premium)** → `https://manukashop.ro/miere-de-manuka-mgo-850-250g.html`

**Paste (generic homepage if no specific product):** `https://manukashop.ro`

**HTML snippet:**
```html
<p>Pentru energie naturală și susținerea sistemului imunitar, <a href="https://manukashop.ro/miere-de-manuka-mgo-550-500g.html" rel="nofollow sponsored noopener">mierea de Manuka MGO 550+</a> este recunoscută pentru proprietățile sale premium.</p>
```

---

## 💎 TIER 2: High Revenue (8-10% Commission)

### Books — Psychology/Dreams (Libris.ro — 8%)

**When to use:**
- Article mentions: Jung, Freud, psihologie, cărți, lectură, simboluri, arhetipuri, inconștient
- Any dream interpretation article (fits naturally)

**Products:**
1. **Jung — Analiza viselor** → `https://www.libris.ro/analiza-viselor-c-g-jung-TRE978-606-40-0393-5--p1258533.html`
2. **Freud — Interpretarea visurilor** → `https://www.libris.ro/interpretarea-visurilor-sigmund-freud-TRE978-973-50-6328-0--p1153026.html`
3. **Dream dictionaries** → `https://www.libris.ro/dictionar-de-vise-a120422--p27597066.html`

**Paste (generic):** `https://www.libris.ro`

**HTML snippet:**
```html
<p>Pentru aprofundare, lucrarea <a href="https://www.libris.ro/analiza-viselor-c-g-jung-TRE978-606-40-0393-5--p1258533.html" rel="nofollow sponsored noopener">Analiza viselor de C.G. Jung</a> oferă perspective valoroase asupra simbolurilor onirice.</p>
```

---

### Dream Journals (Librex.ro — 10%)

**When to use:**
- Article mentions: jurnal de vise, înregistrare, notițe, tipare, tracking, monitorizare
- Article suggests keeping a dream journal or recording dreams

**Products:**
1. **Jurnal de vise** → `https://librex.ro/jurnal-vise`
2. **Caiet mindfulness** → `https://librex.ro/caiet-mindfulness`

**Paste (generic):** `https://librex.ro`

**HTML snippet:**
```html
<p>Păstrarea unui <a href="https://librex.ro/jurnal-vise" rel="nofollow sponsored noopener">jurnal dedicat viselor</a> poate ajuta la identificarea tiparelor și înțelegerea mai profundă.</p>
```

---

## ⚡ TIER 3: Moderate Revenue (3.5% Commission)

### Sleep Supplements (SpringFarma.com)

**When to use:**
- Article mentions: insomnie, somn, anxietate, stres, coșmaruri, treziri nocturne, relaxare
- Sleep quality issues, nightmares, stress-related dreams

**Products (by problem):**
- **Insomnia/trouble falling asleep** → `https://www.springfarma.com/melatonina-pura-5-mg-60-tablete.html`
- **Nightmares/anxiety** → `https://www.springfarma.com/ashwagandha`
- **Restless sleep** → `https://www.springfarma.com/complex-pentru-somn`
- **Stress/tension** → `https://www.springfarma.com/magneziu-glicinat-60-capsule-nutrific.html`
- **General relaxation** → `https://www.springfarma.com/ceai-de-lavanda-n-146-20-plicuri-fares.html`

**Paste (generic):** `https://www.springfarma.com`

**HTML snippet:**
```html
<p>În cazul dificultăților de adormire, suplimente naturale precum <a href="https://www.springfarma.com/melatonina-pura-5-mg-60-tablete.html" rel="nofollow sponsored noopener">melatonina</a> pot ajuta la reglarea ciclului somn-veghe.</p>
```

---

## 📱 TIER 4: Lower Revenue (1% Commission)

### Sleep Technology (evoMAG.ro / Flanco.ro)

**When to use:**
- Article mentions: dispozitive, tehnologie, ceas de trezire, umiditate, aer, lumină
- Only use if technology is HIGHLY relevant (weak revenue)

**Products:**
- **Wake-up light** → `https://www.evomag.ro/electronice/alarme/ceas-beurer-wl-50.html`
- **Air quality** → `https://www.flanco.ro/umidificator-ecg-ah-d501-t.html`
- **Aromatherapy** → `https://www.flanco.ro/difuzor-uleiuri-esentiale`

**Paste (generic):** `https://www.evomag.ro` OR `https://www.flanco.ro`

---

## 🤖 AI Agent Workflow (Copy-Paste This)

### Step 1: Match Article Topic

Scan article for primary keywords:

```
IF article contains: ["energie", "dimineață", "vitalitate", "sănătate"]
  → USE: Manuka honey (Tier 1)

ELSE IF article contains: ["Jung", "Freud", "carte", "psihologie", "simboluri"]
  → USE: Libris books (Tier 2)

ELSE IF article contains: ["jurnal", "înregistrare", "notițe", "tracking"]
  → USE: Librex journal (Tier 2)

ELSE IF article contains: ["insomnie", "somn", "anxietate", "stres", "coșmaruri"]
  → USE: SpringFarma supplements (Tier 3)

ELSE IF article contains: ["dispozitiv", "tehnologie", "ceas", "umiditate"]
  → USE: evoMAG/Flanco (Tier 4)

ELSE
  → DEFAULT: Libris homepage (fits all dream articles)
```

### Step 2: Copy Product URL

From the tiers above, copy the **regular merchant URL** (not the long affiliate link).

**Example:** `https://manukashop.ro/miere-de-manuka-mgo-550-500g.html`

### Step 3: Paste in Resource Box

Use this HTML template:

```html
<div style="background:#E8F5E9;border-left:4px solid #4CAF50;padding:20px;margin:25px 0;border-radius:8px;box-shadow:0 3px 12px rgba(0,0,0,0.06)">
  <h3 style="margin:0 0 10px;color:#2E7D32">📚 Resurse pentru aprofundare</h3>
  <p style="margin:0 0 6px">Pentru aprofundare, vezi <a href="[PASTE_URL_HERE]" rel="nofollow sponsored noopener">[product name]</a>.</p>
  <p style="font-size:.85rem;color:#666;margin:10px 0 0"><em>Link afiliat — câștigăm un mic comision fără costuri pentru tine.</em></p>
</div>
```

### Step 4: Verify (Auto-Check)

After publishing, check ONE article:
1. Right-click link → Inspect
2. Verify `href` shows `event.2performant.com/events/click?aff_code=80f42fe2f`
3. If YES → Link2 is working, all future links will work automatically
4. If NO → Check Link2 plugin settings in WordPress

---

## ⚡ Quick Reference Table

| Article Topic | Product | Commission | URL |
|---------------|---------|-----------|-----|
| Energy/morning | Manuka MGO 550+ | 18% | `manukashop.ro/miere-de-manuka-mgo-550-500g.html` |
| Psychology/Jung/Freud | Analiza viselor (Jung) | 8% | `libris.ro/analiza-viselor-c-g-jung-TRE978-606-40-0393-5--p1258533.html` |
| Dream journal | Jurnal de vise | 10% | `librex.ro/jurnal-vise` |
| Insomnia | Melatonina | 3.5% | `springfarma.com/melatonina-pura-5-mg-60-tablete.html` |
| Anxiety/stress | Ashwagandha | 3.5% | `springfarma.com/ashwagandha` |
| Default (any dream article) | Libris homepage | 8% | `libris.ro` |

---

## 🚨 Rules to NEVER Break

1. **Max 2 products per article** (1 is better for €5,000/month strategy)
2. **Higher commission = priority** (Manuka 18% > Libris 8% > SpringFarma 3.5%)
3. **Paste regular URLs only** (Link2 adds tracking automatically)
4. **Always add `rel="nofollow sponsored noopener"`**
5. **Always include disclosure** ("Link afiliat — câștigăm un mic comision fără costuri pentru tine.")
6. **Place resource box AFTER main content, BEFORE FAQ**

---

## 💡 Pro Tips for Maximum Revenue

### Single Product Strategy (€5,000/month proven)
- **Dream interpretation article** → 1 x Manuka honey (18%) OR 1 x Libris book (8%)
- **Better conversion** than cramming multiple products
- Builds trust, feels like helpful suggestion

### Two Product Strategy (when contextual fit is strong)
- **Primary:** Manuka honey (18%) for energy mention in conclusion
- **Secondary:** Libris dream dictionary (8%) for deeper learning
- **Place separately:** Primary in main content, secondary before FAQ

### Always Prefer Higher Tiers
- If article mentions BOTH "energy" AND "books" → choose Manuka (18%) over Libris (8%)
- Revenue > variety

---

## 🔒 100% Tracking Guarantee

**With Link2 plugin installed:**
1. You paste: `https://manukashop.ro/produs`
2. Link2 converts to: `https://event.2performant.com/events/click?aff_code=80f42fe2f&redirect_to=https%3A%2F%2Fmanukashop.ro%2Fprodus`
3. Tracking works automatically
4. Zero errors possible

**Verification (do once):**
- Publish test article with any merchant URL from this list
- Right-click link → Inspect element
- See `event.2performant.com` in href → confirmed working
- All future links will work the same way

---

## 🎯 Summary: AI Agent Decision in 10 Seconds

1. **Scan article for keywords**
2. **Match to tier** (Manuka > Librex/Libris > SpringFarma > evoMAG)
3. **Copy regular URL** from this file
4. **Paste in resource box template**
5. **Done** — Link2 handles tracking

**No thinking. No manual link generation. Maximum revenue.**
