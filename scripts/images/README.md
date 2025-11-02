Image Pipeline — Pexels → Unique WebP (inteles.ro)

What it does
- Searches Pexels (via API), downloads selected photos, and transforms them into standardized WebP assets that appear unique to Google.
- Strips metadata by re-encoding to WebP; sets alt/caption in a JSON manifest for SEO upload to WordPress.
- Exports 3 sizes per image: hero (1200x675), inline (1200x800), square (1200x1200).

Install
- pip install -r scripts/images/requirements.txt
- Set env in .env: PEXELS_API_KEY=your_key

Usage
- Search + process:
  python scripts/images/pexels_pipeline.py \
    --query "vise sarpe" --query "vise apa" \
    --per 6 --pick 4 \
    --topic "vise despre șerpi" \
    --slug a21639-sarpe \
    --out-dir 10-Assets/pexels

- Transform only (when raw/ already has files):
  python scripts/images/pexels_pipeline.py \
    --no-download \
    --topic "vise despre șerpi" \
    --slug a21639-sarpe \
    --out-dir 10-Assets/pexels

Output
- 10-Assets/pexels/raw/: originals
- 10-Assets/pexels/processed/: WebP variants
- 10-Assets/pexels/processed/manifest-<slug>.json: metadata (alt, caption, credits)

SEO Notes
- Alt text is generated in Romanian based on topic + Pexels alt (if present). Adjust as needed in WordPress.
- Caption includes photographer credit (e.g., "Foto: Nume / Pexels").
- Use hero size for featured image; inline for body; square for social or small inline slots.

WordPress Upload
- Use the manifest’s alt/caption when uploading.
- If using an automated WP upload, map manifest fields to the media title/alt/caption/description.

