# AI Agent Prompts — Ready to Use

Standard templates for writing + evaluation aligned to SOP.

Reference docs:
- `SOP-INTeles.ro-Content-Operations.md`
- `04-SEO-RUBRIC.md`
- `MASTER-PRODUCTS-LIST.md` (affiliate products)

---

## 1) Write Article (Informational)

**Prompt to agent:**

"Write an article in Romanian, mobile-first, on topic: [TITLE]. Strictly follow:
- SOP structure ('Ce înseamnă X' or 'Dream Interpretation'), quick answer in first 2 paragraphs
- H2/H3 every 300-400 words, short paragraphs, lists
- 6+ FAQ questions with schema.org (Question/Answer microdata)
- 1-2 relevant images (correct alt), discreet style
- Balanced monetization: max 2 affiliate links (exceptional 3), only in 'Resources' boxes; informative tone, no pressure
- 1-2 credible sources (WHO/Wikipedia-RO) + 1-2 relevant internal links
- No gradient/emoji-spam; sober, readable design
- At the end, self-evaluate with 100-point rubric (10 categories) and list 3 quick-fixes under 5 minutes

Return: Clean HTML + score table + quick-fixes."

---

## 2) Compare and Score 2 Versions (0-100)

**Prompt to agent:**

"You are a direct SEO evaluator. Compare Version A and Version B (Romanian) and score on 10 categories (10pts/category):
1) Content; 2) Intent; 3) E-E-A-T; 4) Readability; 5) Engagement; 6) Links; 7) Conversion; 8) Mobile UX; 9) Search intent; 10) Technical SEO.

Return:
- Score table per category + total
- 5 critical failures (if any) + justification (max 1 sentence each)
- 3 quick actions under 5 minutes that raise total score by 10-20 points
- Clear verdict (e.g., 'Version A wins'), no hesitation

Notes:
- Explicitly mark penalty risks (affiliate-heavy, manipulation, missing sources)
- If you see CTA/emoji/gradient-spam, lower score on Readability/UX/Links
- Maintain professional, concise tone, no hedging."

---

## 3) One-Pass Polish (5 minutes)

**Prompt to agent:**

"Look at article X. Without major rewrite, apply only '5-minute fixes':
1) Move affiliate to green box, max 2 links
2) Add 1 credible source
3) Clarify intro (2 paragraphs, quick answer)
4) Add 2-4 FAQ
5) Check image alt text

Return the diff in a single HTML block."

---

## 4) Pick Affiliate Products

**Prompt to agent:**

"I'm writing an article about [TOPIC]. Scan `MASTER-PRODUCTS-LIST.md` and recommend 1-2 best-fit products with reasoning. Include ready affiliate links."

**Example:**
- Topic: nightmares → "Magneziu glicinat" + "Ceai de lavandă"
- Topic: Jung psychology → "Analiza viselor — C.G. Jung"
- Topic: dream journaling → "Jurnal de vise (Librex)"
