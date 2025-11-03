# Quick Reference — inteles.ro

MCP (WordPress):
- Listează articole scurte (cat. 5): "Lista postări categoria 5, per_page=50, orderby=id desc; arată wordCount; filtrează <1000w"
- Preia post: "Arată postarea ID [id] (conținut + schema wordCount)"
- Actualizează: "Actualizează post ID [id] cu [HTML], status publish"
- Media: "Urcă imagine [fișier] cu alt '[text]' și atașeaz-o la [id]"

Pexels:
- Caută: "Găsește 5–8 imagini pentru [temă], landscape, ton natural, compoziție clară"
- Alege 2–4; încarcă în WP; setează alt/caption

Pipeline imagini (automat):
- `PEXELS_API_KEY` în `.env`
- `pip install -r scripts/images/requirements.txt`
- `python scripts/images/pexels_pipeline.py --query "[tema]" --per 6 --pick 4 --topic "[context RO]" --slug a[POSTID]-[slug] --out-dir 10-Assets/pexels`
- Folosește manifestul generat pentru alt/caption + upload în WP

⭐ **Monetizare — Link2 Plugin (AUTO):**
- **Writing:** Match topic → Copy URL from [[04-Monetization/PRODUCT-URLS|Product URLs]] → Paste
- **Link2 converts:** Regular URL → affiliate link (100% tracking)
- **10 products:** Manuka (18%), Libris books (8%), Librex journal (10%), SpringFarma (3.5%)
- Format link: `rel="nofollow sponsored noopener"`
- Disclosure: <em>Link afiliat — câștigăm un mic comision fără costuri pentru tine.</em>

Șabloane:
- [[07-Templates/TPL-Vis-Interpretare]]
- [[07-Templates/TPL-Ce-Inseamna]]
- [[07-Templates/HTML-Resource-Box]]
- [[07-Templates/HTML-Resource-Box-2Links]]

Docs sursă: [[11-Source-Docs/INDEX]]
