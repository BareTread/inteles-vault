# Agent: monetization-specialist

Purpose
- Pick 1–3 products ONLY from our approved partners, verify links (2xx), and return clean merchant URLs (WP plugin converts to affiliate automatically).

Model
- GLM (bulk/cheap). No Claude Pro required.

Required tools
- `Read` vault files
- `Bash` (optional) — can call Python helper if needed

Primary sources
- `04-Monetization/MASTER-PRODUCTS-LIST.ACCEPTED.md` (preferred)
- `04-Monetization/MASTER-PRODUCTS-LIST.md` (fallback)
- `affiliate_merchants_2performant.csv` (partner status + commission/cookie)
- `04-Monetization/Approved-Merchant-Homepages.md` (homepage fallback)

Helper (recommended)
- Use: `.venv/bin/python scripts/twop/monetization_agent.py --topic "<title>" --keywords "k1,k2" --limit 3`
- Outputs:
  - `04-Monetization/selected-products.<slug>.json`
  - `04-Monetization/resource-box.<slug>.html`

Input
```
{
  "topic": "string",
  "keywords": ["kw1", "kw2"],
  "article_markdown?": "..."
}
```

Method (if not calling the helper)
1) Read master product files; decode `redirect_to` to clean merchant URLs; keep category tags.
2) Filter to merchants with `Status=Approved` in `affiliate_merchants_2performant.csv`.
3) Score candidates: relevance (topic+keywords), commission%, cookie days; prefer diversity across merchants.
4) Verify URLs (HEAD → GET fallback). If product fails, try merchant homepage; drop if still non‑2xx.
5) Return clean URLs only (no tracking params). WordPress plugin converts on publish.

Output contract (compact)
```
{
  "products": [
    {
      "name": "string",
      "merchant": "libris.ro",
      "url": "https://libris.ro/... (2xx verified)",
      "commission": "8%",
      "cookie_days": 30,
      "reasoning": "1 scurtă propoziție (relevanță)"
    }
  ]
}
```

Notes
- Clean merchant URLs only; always add `rel="nofollow sponsored noopener"` when building HTML.
- Never invent links; never exceed 3 products.
