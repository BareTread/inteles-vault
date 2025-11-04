# Pexels Image Pipeline for inteles.ro

Intelligent, minimal pipeline for converting raw Pexels downloads into SEO-optimized WebP images with WordPress-ready metadata.

---

## Quick Start

```bash
# 1. Install (see INSTALL.md for Arch-specific instructions)
sudo pacman -S python-pillow python-numpy
python -m venv venv && source venv/bin/activate
pip install imagehash unidecode blurhash

# 2. Place raw Pexels images in ./raw/

# 3. Update SPECS in pexels_image_pipeline.py with Romanian metadata

# 4. Run
python pexels_image_pipeline.py --seed 42 --quality 82

# 5. Outputs appear in ./processed/
```

---

## What It Does

### Core Features
- **Smart cropping** — Random 16:9 crop with micro-rotation (±1°) for uniqueness
- **Micro-adjustments** — Color, brightness, contrast, sharpness variations (±3-5%)
- **Optional grain** — 35% chance of invisible noise overlay (breaks fingerprinting)
- **EXIF stripping** — Clean metadata
- **Size control** — Auto-quality fallback to hit target bytes (<180KB hero, <140KB inline)

### Optional Features (graceful degradation)
- **Dedupe** — Perceptual hash prevents reusing similar Pexels images (needs `imagehash`)
- **LQIP + BlurHash** — Instant placeholders for Core Web Vitals (needs `blurhash`)
- **Romanian slugs** — Diacritics → ASCII conversion (needs `unidecode`)

---

## File Structure

```
10-Assets/pexels/
├── pexels_image_pipeline.py    # Main script
├── INSTALL.md                  # Arch Linux install guide
├── AGENT_CHEATSHEET.md         # Quick reference for IMAGE AGENT
├── requirements.txt            # Python dependencies
├── raw/                        # Place Pexels downloads here
└── processed/                  # Output folder
    ├── {filename}.webp         # Optimized images
    ├── metadata.json           # Full spec + LQIP data URIs
    ├── metadata.csv            # WordPress batch import
    └── phash_index.json        # Dedupe database (auto-managed)
```

---

## SPECS Configuration

Edit the `SPECS` list in the script:

```python
ImageSpec(
    src="pexels-woman-sleeping-123456.jpg",  # raw filename
    out="femeie-dormind-vise-somn.webp",     # output name
    role="hero",                              # "hero" (1600x900) or "inline" (1200x675)
    target_width=1600,
    target_height=900,
    alt="Femeie dormind liniștită, reprezentând importanța somnului pentru vise",
    caption="Somul de calitate este esențial pentru procesarea emoțiilor.",
    placement="Imediat după H1, înainte de introducere",
    keywords=["somn", "vise", "odihnă", "subconștient"],
    priority="1",                             # Display order
    recommended=True,
),
```

**Key fields:**
- `role`: Controls dimensions (hero=1600×900, inline=1200×675)
- `alt`: Romanian description (critical for SEO)
- `keywords`: 3-5 Romanian keywords for image search
- `placement`: ACF field reference
- `priority`: "1" = featured image, "2" = second, etc.

---

## Usage

### Basic Run
```bash
python pexels_image_pipeline.py
```

### With Seed (reproducible results)
```bash
python pexels_image_pipeline.py --seed 42
```

### Custom Quality
```bash
python pexels_image_pipeline.py --quality 85  # Higher quality (bigger files)
python pexels_image_pipeline.py --quality 75  # Lower quality (smaller files)
```

---

## Output Formats

### metadata.json (full detail)
```json
{
  "status": "ok",
  "file": "femeie-dormind-vise-somn.webp",
  "alt": "Femeie dormind liniștită...",
  "blurhash": "UQF^~toK$zR+Ro#jENv~",
  "lqip_data_uri": "data:image/webp;base64,...",
  "title_slug": "femeie-dormind-vise-somn",
  "final_size_bytes": 76234,
  "phash": "0f0f0f0f0f0f0f0f"
}
```

### metadata.csv (WordPress import)
| filename | alt | caption | keywords | role | priority | final_size_bytes | blurhash | title_slug |
|----------|-----|---------|----------|------|----------|------------------|----------|------------|
| femeie-dormind... | Femeie... | Somul... | somn;vise | hero | 1 | 76234 | UQF^~... | femeie-dormind... |

---

## Status Codes

| Status | Meaning | Action |
|--------|---------|--------|
| `ok` | Processed successfully | Use it |
| `missing_src` | Raw file not found in `raw/` | Check filename or re-download |
| `duplicate_like` | Too similar to existing image (Hamming ≤ 5) | Use different Pexels image or delete old one |

---

## For IMAGE AGENT

### Programmatic Use

```python
import subprocess
from pathlib import Path

# Add specs programmatically (or update SPECS list in script)
# ... download Pexels images to raw/ ...

# Run pipeline
result = subprocess.run([
    "python", "pexels_image_pipeline.py",
    "--seed", "42",
    "--quality", "82"
], cwd="/home/alin/DATA/OBSIDIAN/inteles-vault/10-Assets/pexels", capture_output=True)

# Check for duplicates
import json
metadata = json.loads(Path("processed/metadata.json").read_text())
duplicates = [img for img in metadata if img.get("status") == "duplicate_like"]

if duplicates:
    # Rotate to different Pexels images
    for dup in duplicates:
        print(f"⚠️  {dup['file']} is similar to {dup['similar_to']}")
```

### Workflow
1. Download 5-8 images from Pexels API → save to `raw/`
2. Build SPECS list with Romanian metadata
3. Run pipeline
4. Check `metadata.json` for `duplicate_like` status
5. Import `metadata.csv` to WordPress
6. Use LQIP data URIs in Kadence Blocks for instant placeholders

---

## Tips

### Avoid Duplicates
- Dedupe database (`phash_index.json`) persists across runs
- Don't delete it unless you want to allow reuse
- If duplicate detected, swap to different Pexels image

### Reproducibility
- Use `--seed` for consistent results across runs
- Same seed + same source = identical output
- Omit seed for random variations

### Quality vs. Size
- Default 82 balances quality/size well (~80KB hero, ~60KB inline)
- Hero images: 84-86 for featured content
- Inline images: 75-80 for faster loading

### BlurHash Usage
- Decode with `blurhash.js` client-side for instant placeholders
- Or use LQIP data URI directly in `<img style="background: url(...)">`

---

## Performance

- **Time:** ~2-3s per image (dedupe + LQIP + WebP)
- **5 images:** ~15s total
- **8 images:** ~25s total
- **Disk:** ~80KB per hero, ~60KB per inline

---

## Future Enhancements

- Async processing for 8+ images in parallel
- Similarity scoring to prevent picking visually similar images in same article
- Direct WordPress API integration via WP-CLI
- Automated Pexels search + download based on keywords

---

**See also:**
- `INSTALL.md` — Arch Linux installation
- `AGENT_CHEATSHEET.md` — Quick reference for IMAGE AGENT
