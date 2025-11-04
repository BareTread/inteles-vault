## Monetization Agent (partner-only, clean URLs)

Purpose
- Picks 1–3 relevant products from approved 2Performant partners
- Prefers higher commission and cookie window when relevance ties
- Verifies URLs (2xx). If product URL fails, falls back to merchant homepage
- Outputs both compact JSON and a ready-to-embed HTML resource box

Data sources
- `04-Monetization/MASTER-PRODUCTS-LIST.ACCEPTED.md` (preferred)
- `04-Monetization/MASTER-PRODUCTS-LIST.md` (fallback)
- `04-Monetization/Approved-Merchant-Homepages.md` (fallback homepages)
- `affiliate_merchants_2performant.csv` (root; partner status + commission/cookie)

Outputs
- `04-Monetization/selected-products.<slug>.json`
- `04-Monetization/resource-box.<slug>.html`

CLI usage
```
.venv/bin/python scripts/twop/monetization_agent.py \
  --topic "Ce înseamnă când visezi șerpi" \
  --keywords "vise,șerpi,simbolism,psihologie" \
  --limit 3
```

or derive topic/keywords from a draft:
```
.venv/bin/python scripts/twop/monetization_agent.py \
  --article 11-Source-Docs/Samples/draft.md
```

Contract (JSON)
```
{
  "products": [
    {
      "name": "Product Name (with merchant)",
      "merchant": "libris.ro",
      "url": "https://libris.ro/…",              // clean merchant URL (WP plugin will convert)
      "commission": "8%",                          // best-known estimate (may be empty)
      "cookie_days": 30,
      "reasoning": "Relevanță ridicată pentru subiect; partener aprobat."
    }
  ]
}
```

Notes
- Uses clean merchant URLs only — auto-affiliate plugin in WordPress will convert them on publish
- Idempotent: safe to re-run; files are overwritten for the same slug
- Minimal dependencies: relies on `requests` (already in `scripts/twop/requirements.txt`)

