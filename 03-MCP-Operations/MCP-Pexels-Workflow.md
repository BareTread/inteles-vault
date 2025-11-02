# MCP Pexels Workflow

Scop: găsește imagini premium, relevante, apoi încarcă în WordPress cu alt corect.

Brief de căutare (exemplu):
- „Caută 5–8 imagini pentru [temă], orientare landscape, ton natural, compoziție clară, fără clișee.”

Criterii de selecție:
- Relevanță puternică pentru temă
- Emoție + claritate, nu stock generic
- Consistență cromatică cu articolul

Pași:
1) Caută și deschide 5–8 rezultate; alege 2–4 cele mai potrivite (notează ID‑urile).
2) Rulează pipeline‑ul de procesare (standardizează și unifică imaginile — WebP, fără EXIF, mici variații unice):
   ```bash
   # cu PEXELS_API_KEY în .env
   python scripts/images/pexels_pipeline.py \
     --query "[tema]" --per 6 --pick 4 \
     --topic "[context RO]" --slug a[POSTID]-[slug scurt] \
     --out-dir 10-Assets/pexels
   ```
   Rezultat: 10-Assets/pexels/processed/ + manifest JSON cu alt/caption.
3) Încarcă în WordPress (MCP): setează title/alt/caption din manifest; atașează la post.
4) Plasează imaginile în conținut (după intro, mijloc, înainte de FAQ) — doar unde ajută.

Best practices:
- Dimensiuni standard export:
  - hero: 1200x675 (featured)
  - inline: 1200x800 (corp)
  - square: 1200x1200 (secțiuni mici / social)
- Format: WebP (quality ~84), fără EXIF (re-encodat implicit)
- Denumire fișier: `a[POSTID]-[slug]-[tip]-[pexelsID].webp`
- 1 imagine / ~400–600 cuvinte, doar dacă adaugă valoare

MCP (Pexels) — comenzi utile
- Set API key: folosește `PEXELS_API_KEY` și salvează-l în .env
- Căutare (MCP server Pexels): `searchPhotos(query="[tema]", perPage=6, orientation="landscape")`
- Download: `downloadPhoto(id=<pexels_id>, size="original")`
- Apoi rulează pipeline‑ul pe fișierele din `10-Assets/pexels/raw/`
