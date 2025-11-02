2Performant API Automation — inteles.ro

What this does
- Logs in to 2Performant API (affiliate user) via `/users/sign_in.json`.
- Lists your accepted affiliate programs via `/affiliate/programs`.
- Optionally fetches advertiser promotions via `/affiliate/advertiser_promotions`.
- Builds ready‑to‑paste 2Performant quicklinks for relevant products mapped to inteles.ro topics.
- Writes a curated Markdown to `04-Monetization/Auto-Generated-Affiliate-Links.md`.

Requirements
- Python 3.9+
- `pip install -r scripts/twop/requirements.txt`
- Create `.env` at repo root (see `.env.example`)

Env vars
- `TWO_P_EMAIL` — 2Performant login email (affiliate)
- `TWO_P_PASSWORD` — 2Performant password
- `TWO_P_BASE` — default `https://api.2performant.com`
- `TWO_P_AFF_CODE` — your affiliate code (e.g., `80f42fe2f`)

Run
```
python scripts/twop/fetch_and_build.py \
  --topics dream,sleep \
  --out 04-Monetization/Auto-Generated-Affiliate-Links.md
```

Notes
- Product Store endpoints are not public in this doc bundle. The current pipeline uses:
  - Affiliate Programs (to confirm active merchants)
  - Known curated products for key merchants (Libris, SpringFarma, ManukaShop, evoMAG, Flanco, Librex)
  - Advertiser Promotions as an additional source of deeplink targets
- When 2Performant Product Store endpoints are provided, plug them into `product_sources.py` (placeholder).

