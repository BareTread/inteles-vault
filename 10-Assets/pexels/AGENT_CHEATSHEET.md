# IMAGE AGENT: Cheatsheet

**Purpose:** Turn Pexels downloads into unique, SEO-ready WebP images with WordPress metadata.

---

## One-Liner

```bash
cd /home/alin/DATA/OBSIDIAN/inteles-vault/10-Assets/pexels && python pexels_image_pipeline.py --seed 42
```

---

## Workflow (5 Steps)

### 1. Download Images

```python
# Fetch from Pexels API → save to raw/
# Filename example: ce-inseamna-cand-visezi-morti-hero.jpg
```

### 2. Update SPECS

```python
ImageSpec(
    src="pexels-raw-filename.jpg",
    out="articol-cuvant-cheie-hero.webp",
    role="hero",  # or "inline"
    target_width=1600,   # 1600 for hero, 1200 for inline
    target_height=900,   # 900 for hero, 675 for inline
    alt="Romanian alt text for SEO",
    caption="Optional Romanian caption",
    placement="After H1, before intro",
    keywords=["keyword1", "keyword2", "keyword3"],
    priority="1",  # "1" = featured, "2" = second, etc.
),
```

### 3. Run Pipeline

```bash
python pexels_image_pipeline.py --seed 42 --quality 82
```

### 4. Check for Duplicates

```python
import json
from pathlib import Path

metadata = json.loads(Path("processed/metadata.json").read_text())
duplicates = [img for img in metadata if img["status"] == "duplicate_like"]

if duplicates:
    print(f"⚠️  Rotate these images: {[d['file'] for d in duplicates]}")
```

### 5. Use Outputs

- **metadata.csv** → WordPress batch import
- **metadata.json** → Full spec + LQIP data URIs
- **{filename}.webp** → Upload to WordPress

---

## SPECS Field Reference

| Field           | Example                          | Required | Notes                            |
| --------------- | -------------------------------- | -------- | -------------------------------- |
| `src`           | `"pexels-woman-sleep.jpg"`       | ✅        | Raw filename in `raw/`           |
| `out`           | `"femeie-dormind-somn.webp"`     | ✅        | Output filename                  |
| `role`          | `"hero"` or `"inline"`           | ✅        | Controls dimensions              |
| `target_width`  | `1600` (hero) or `1200` (inline) | ✅        | Final width in pixels            |
| `target_height` | `900` (hero) or `675` (inline)   | ✅        | Final height in pixels           |
| `alt`           | `"Femeie dormind..."`            | ✅        | Romanian alt text (SEO critical) |
| `caption`       | `"Somul de calitate..."`         | ❌        | Optional Romanian caption        |
| `placement`     | `"After H1, before intro"`       | ✅        | ACF field reference              |
| `keywords`      | `["somn", "vise", "odihnă"]`     | ✅        | 3-5 Romanian keywords            |
| `priority`      | `"1"`, `"2"`, `"3"`              | ✅        | Display order (string)           |
| `recommended`   | `True` or `False`                | ❌        | Default: True                    |

---

## Output Files

| File               | Use                                   |
| ------------------ | ------------------------------------- |
| `{filename}.webp`  | Upload to WordPress                   |
| `metadata.csv`     | WordPress batch import (ACF fields)   |
| `metadata.json`    | Full spec + LQIP data URIs + BlurHash |
| `phash_index.json` | Dedupe database (don't edit)          |

---

## Status Codes

| Status             | Meaning                   | Action                         |
| ------------------ | ------------------------- | ------------------------------ |
| `"ok"`             | Success                   | Use it                         |
| `"missing_src"`    | Raw file not found        | Check filename or re-download  |
| `"duplicate_like"` | Similar to existing image | Swap to different Pexels image |

---

## metadata.csv Columns

| Column             | Example                    | WordPress Use                 |
| ------------------ | -------------------------- | ----------------------------- |
| `filename`         | `femeie-dormind-somn.webp` | Upload reference              |
| `alt`              | `Femeie dormind...`        | Alt text field                |
| `caption`          | `Somul de calitate...`     | Caption field                 |
| `title_slug`       | `femeie-dormind-somn`      | Image post_title              |
| `keywords`         | `somn;vise;odihnă`         | Image search metadata         |
| `role`             | `hero` or `inline`         | Layout reference              |
| `priority`         | `1`, `2`, `3`              | Display order                 |
| `blurhash`         | `UQF^~toK$zR+...`          | Placeholder decode (optional) |
| `final_size_bytes` | `76234`                    | File size tracking            |

---

## Programmatic Use

```python
import subprocess
import json
from pathlib import Path

# Run pipeline
subprocess.run([
    "python", "pexels_image_pipeline.py",
    "--seed", "42",
    "--quality", "82"
], cwd="/home/alin/DATA/OBSIDIAN/inteles-vault/10-Assets/pexels")

# Check results
metadata_path = Path("processed/metadata.json")
results = json.loads(metadata_path.read_text())

for img in results:
    if img["status"] == "duplicate_like":
        print(f"⚠️  {img['file']} similar to {img['similar_to']}")
    elif img["status"] == "ok":
        print(f"✅ {img['file']} ({img['final_size_bytes']} bytes)")
```

---

## Common Patterns

### Hero Image (Featured)

```python
ImageSpec(
    src="pexels-dream-interpretation.jpg",
    out="interpretare-vise-featured.webp",
    role="hero",
    target_width=1600,
    target_height=900,
    alt="...",
    keywords=["vise", "interpretare", "psihologie"],
    priority="1",
)
```

### Inline Image (Content)

```python
ImageSpec(
    src="pexels-therapist-session.jpg",
    out="terapie-vise-consiliere.webp",
    role="inline",
    target_width=1200,
    target_height=675,
    alt="...",
    keywords=["terapie", "consiliere"],
    priority="2",
)
```

---

## Tips

**Avoid duplicates:**

- Dedupe database persists across runs
- If duplicate found, use different Pexels image

**Reproducible results:**

- Same `--seed` = identical output
- Omit seed for random variations

**Quality control:**

- Default 82 works well (~80KB hero)
- Increase to 85-90 for featured images
- Decrease to 75-80 for faster loading

**LQIP usage:**

- BlurHash in `metadata.csv` for client-side decode
- LQIP data URI in `metadata.json` for instant background

---

## Troubleshooting

**"missing_src"**
→ Raw file not in `raw/` folder

**"duplicate_like"**
→ Similar to existing image; rotate to different Pexels result

**Script slow**
→ Normal; ~2-3s per image for dedupe + LQIP + WebP

**Features disabled**
→ Check output:

```
🎨 Pipeline Features:
   - Dedupe: ❌ (install python-imagehash)
   - BlurHash: ❌ (install python-blurhash)
```

→ See `INSTALL.md` for Arch Linux setup

---

**Full docs:** `README.md`
**Installation:** `INSTALL.md`
