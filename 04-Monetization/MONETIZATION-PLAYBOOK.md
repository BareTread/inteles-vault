# Monetization Playbook for Inteles.ro

**Purpose:** Quick reference for selecting affiliates for dream interpretation articles
**Last Updated:** November 3, 2025
**Status:** Ready for agent integration

---

## QUICK DECISION FLOWCHART

```
START: New article about "[dream topic]"
  │
  ├─ Is it about a BOOK/KNOWLEDGE topic?
  │   └─> USE: Libris.ro (8%, 10d) or LibrariaDelfin.ro (9%, 10d)
  │
  ├─ Is it about SLEEP/NIGHTMARES/ANXIETY?
  │   └─> USE: Herbagetica (10%, 30d) + Vitamix.ro (8-30%, 60d)
  │
  ├─ Is it about STRESS/WELLNESS/MENTAL HEALTH?
  │   └─> USE: Organicsfood.ro (9%, 60d) + Minunea Naturii (10%)
  │
  ├─ Is it about NATURAL REMEDIES/PSYCHOLOGY?
  │   └─> USE: Pansiprod.ro (10%) or Mendo.ro (10%, traditional medicine)
  │
  ├─ Is it a longer-cycle decision (luxury product)?
  │   └─> USE: Topstar.ro (10%, 90-day cookie) ← LONGEST CONVERSION WINDOW
  │
  └─ Default: Organicsfood.ro (9%, 60d, psychology-friendly)
```

---

## ARTICLE TYPE → AFFILIATE MAPPING

### 📖 Dream Interpretation Articles
**Examples:** "Ce înseamnă când visezi șerpi", "Vise cu apă", "Interpretare vis cu moarte"

**Primary Affiliate:** Libris.ro (8%, 10d) OR LibrariaDelfin.ro (9%, 10d)
**Secondary:** Organicsfood.ro (9%, 60d) - for wellness angle
**Tertiary:** Herbagetica (10%, 30d) - if article mentions sleep/anxiety

**Rationale:** Psychology books convert best for interpretation-focused content

---

### 💤 Sleep & Nightmare Articles
**Examples:** "De ce visezi rău", "Coșmaruri recurente", "Somn mai bun"

**Primary:** Herbagetica (10%, 30d) + Vitamix.ro (8-30%, 60d)
**Secondary:** Minunea Naturii (10%) - for natural sleep aids
**Tertiary:** Pansiprod.ro (10%) - medical devices for sleep

**Rationale:** Supplements convert best; offer multiple complementary merchants

---

### 🧠 Mental Health & Stress Articles
**Examples:** "Vise cu anxietate", "Interpretation viselor stresante"

**Primary:** Organicsfood.ro (9%, 60d) + Minunea Naturii (10%)
**Secondary:** Pansiprod.ro (10%) - medical angle
**Tertiary:** Springfarma.com (3.5-15%) - competitive pricing

**Rationale:** Wellness products + long cookie = better conversion

---

### 🎯 Transformation/Change Articles
**Examples:** "Vise cu transformare", "Symbolism în vise"

**Primary:** Libris.ro (8%, 10d) - Jung/psychology books
**Secondary:** Organicsfood.ro (9%, 60d) - personal development
**Tertiary:** Herbagetica (10%, 30d) - wellness during change

**Rationale:** Blend knowledge + wellness + health

---

### 💃 Beauty/Appearance Dream Articles
**Examples:** "Ce înseamnă când visezi frumusețe", "Vise despre transformare fizică"

**Primary:** Topstar.ro (10%, 90d) ⭐ - LONGEST COOKIE
**Secondary:** Organicsfood.ro (9%, 60d) - natural beauty
**Tertiary:** Luxurybeauty.ro - premium positioning

**Rationale:** 90-day cookie matches decision cycles for cosmetics

---

### 🔨 Work/Career Dream Articles
**Examples:** "Vise cu muncă", "Job interpretation"

**Primary:** Scule365.ro (7%, 60d) - DIY/professional tools
**Secondary:** Organicsfood.ro (9%, 60d) - stress management at work
**Tertiary:** Any tier 1 supplement

**Rationale:** Tools affiliate for practical articles; supplements for stress angle

---

### 🌿 Natural/Holistic Articles
**Examples:** "Natural dream interpretation", "Herbal approaches to better sleep"

**Primary:** Minunea Naturii (10%) - naturopath angle
**Secondary:** Organicsfood.ro (9%, 60d) - organic/BIO focus
**Tertiary:** Pansiprod.ro (10%) - medical + natural

**Rationale:** All three emphasize natural/holistic approach

---

## MONETIZATION AGENT INSTRUCTIONS

### Input Format
```json
{
  "article_topic": "Ce înseamnă când visezi șerpi",
  "article_keywords": ["vise", "șerpi", "simbolism", "psihologie"],
  "article_category": "interpretation",
  "target_length": "2000-2500 words"
}
```

### Selection Algorithm

1. **Match category to mapping above** → identify primary affiliate
2. **Check restrictions** (PPC, platforms, keywords)
3. **Verify merchant is tier 1 or tier 2** (avoid other tier unless desperate)
4. **Pick 2-3 products maximum:**
   - Primary (75% weight)
   - Secondary (20% weight)
   - Tertiary (5% weight if needed)
5. **Diversify merchants** (don't use 3 from same merchant)
6. **Output compact JSON:**

```json
{
  "products": [
    {
      "merchant": "Libris.ro",
      "commission": "8%",
      "cookie_days": 10,
      "reasoning": "Psychology books match dream interpretation content"
    },
    {
      "merchant": "Organicsfood.ro",
      "commission": "9%",
      "cookie_days": 60,
      "reasoning": "Wellness angle for holistic dream interpretation"
    }
  ]
}
```

---

## TACTICAL TIPS FOR EACH TIER

### TIER 1 Merchants (Always Prioritize)
- **Libris/LibrariaDelfin/Librex:** Use for ANY knowledge-focused article
- **Herbagetica:** Use whenever article mentions sleep, stress, anxiety
- **Vitamix.ro:** Use for weight loss, energy, mood-related dream articles
- **Organicsfood.ro:** Use as fallback for psychology articles (safe default)
- **Minunea Naturii:** Use when natural/holistic angle is present
- **Pansiprod.ro:** Use medical/health dream interpretations

### TIER 2 Merchants (Secondary Options)
- **Mendo.ro:** Use for traditional medicine angle, women 35-55 audience
- **Springfarma.com:** Use for medical/pharmacy angle, competitive price mention
- **Manukashop.ro:** Use ONLY for energy/immunity-related dream articles

### TIER 3 Merchants (Niche Fit)
- **Topstar.ro:** Use for beauty/appearance dreams (90-day cookie is gold)
- **Otter.ro:** Use for fashion/identity dreams
- **Scule365.ro:** Use for work/career/DIY dreams (no restrictions = flexible)
- **Nailshop.ro:** Use for beauty/self-care dreams (watch keyword restrictions)

---

## ANTI-HALLUCINATION CHECKLIST

Before outputting any affiliate recommendation, verify:

- [ ] Merchant is in Tier 1, 2, or 3 (not "Other")
- [ ] Commission % is clearly stated (not "varies" without details)
- [ ] No PPC restrictions are violated (check Libris, LibrariaDelfin)
- [ ] Keyword restrictions aren't triggered (check Nailshop)
- [ ] Merchant is not Powerlaptop (closing 30.08.2025)
- [ ] Article topic logically matches merchant category
- [ ] Max 3 merchants selected (2 is ideal)
- [ ] Merchants are diverse (not 3 from same merchant)

---

## REAL EXAMPLES

### Example 1: "Ce înseamnă când visezi șerpi"
**Analysis:**
- Topic: Interpretation + symbolism
- Keywords: vise, șerpi, psihologie, frică, transformare
- Best fit: Books + psychology + natural remedies

**Recommendation:**
1. **Libris.ro** (primary) - Psychology books on dream symbolism
2. **Organicsfood.ro** (secondary) - Natural remedies for anxiety about nightmares

---

### Example 2: "De ce visezi rău - Coșmaruri și soluții"
**Analysis:**
- Topic: Sleep quality + nightmares + solutions
- Keywords: somn, coșmar, anxietate, soluții naturale
- Best fit: Supplements + sleep aids + wellness

**Recommendation:**
1. **Herbagetica** (primary) - Stress management + natural sleep supplements
2. **Vitamix.ro** (secondary) - Sleep-focused supplements (if available)
3. **Organicsfood.ro** (tertiary) - Wellness angle for better sleep

---

### Example 3: "Frumusețea în vise - Transformare și autoacceptare"
**Analysis:**
- Topic: Beauty/appearance psychology
- Keywords: frumusețe, transformare, autoacceptare
- Best fit: Beauty products + wellness + long cookie window

**Recommendation:**
1. **Topstar.ro** (primary) - 90-day cookie perfect for cosmetics decision
2. **Organicsfood.ro** (secondary) - Natural beauty angle

---

### Example 4: "Muncă și carieră în vise - Ce spun visele mele"
**Analysis:**
- Topic: Work psychology
- Keywords: muncă, carieră, creștere, stres profesional
- Best fit: DIY/professional tools + stress management

**Recommendation:**
1. **Scule365.ro** (primary) - Professional/DIY tool angle (no restrictions)
2. **Herbagetica** (secondary) - Work stress management

---

## PERFORMANCE TRACKING (To Add Later)

Once articles are live, track these metrics per merchant:

- Monthly clicks
- Monthly conversions
- Monthly commission earned
- Average order value
- Conversion rate
- Cookie utilization rate

This will help refine the mapping over time.

---

## NEXT STEPS

1. ✅ **Master Database created** → AFFILIATES-MASTER-DATABASE.md
2. ✅ **CSV created** → affiliates-COMPLETE.csv
3. ⏳ **Wire into monetization agent** → Update monetization-specialist system prompt
4. ⏳ **Create category packs** → Run build_category_packs.py
5. ⏳ **Set up performance dashboard** → Track metrics over 30 days

---

**Ready to use with monetization agents. All merchant data validated as of November 3, 2025.**
