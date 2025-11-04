# Installation Guide (Arch Linux)

## Quick Install (Recommended)

```bash
# Install core dependencies via pacman
sudo pacman -S python-pillow python-numpy

# Install optional features (dedupe + Romanian slugs) via venv
cd /home/alin/DATA/OBSIDIAN/inteles-vault/10-Assets/pexels
python -m venv venv
source venv/bin/activate
pip install imagehash unidecode blurhash
```

Then run with:
```bash
source venv/bin/activate
python pexels_image_pipeline.py --seed 42
```

---

## What Each Package Does

| Package | Feature | Fallback if Missing |
|---------|---------|---------------------|
| `python-pillow` | Image processing (required) | Script fails |
| `python-numpy` | Array operations for LQIP | Script fails |
| `imagehash` | Dedupe (prevents reusing similar Pexels images) | Dedupe disabled, all images processed |
| `unidecode` | Romanian → ASCII slugs (`"Femeie zâmbind"` → `"femeie-zambind"`) | Basic Romanian conversion fallback |
| `blurhash` | BlurHash placeholders for Core Web Vitals | Only LQIP data URI generated (still works) |

**Script runs with partial features if optional packages are missing.**

---

## Check What's Installed

Run the script once to see feature status:

```bash
python pexels_image_pipeline.py
```

Output:
```
🎨 Pipeline Features:
   - Dedupe: ✅
   - BlurHash: ✅
   - Romanian slugs: ✅
   - Seed: random
   - Quality: 82
```

---

## For IMAGE AGENT: Programmatic Use

If your agent needs to install dependencies:

```python
import subprocess

# Check if venv exists, create if not
venv_path = "/home/alin/DATA/OBSIDIAN/inteles-vault/10-Assets/pexels/venv"
if not os.path.exists(venv_path):
    subprocess.run(["python", "-m", "venv", venv_path])
    subprocess.run([f"{venv_path}/bin/pip", "install", "imagehash", "unidecode", "blurhash"])

# Run pipeline
subprocess.run([
    f"{venv_path}/bin/python",
    "pexels_image_pipeline.py",
    "--seed", "42",
    "--quality", "82"
], cwd="/home/alin/DATA/OBSIDIAN/inteles-vault/10-Assets/pexels")
```

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'PIL'"**
→ Install: `sudo pacman -S python-pillow`

**"ModuleNotFoundError: No module named 'numpy'"**
→ Install: `sudo pacman -S python-numpy`

**Dedupe/BlurHash features disabled**
→ Not critical; script works without them
→ To enable: Activate venv and install optional packages

**"externally-managed-environment" error**
→ You tried `pip install` outside venv on Arch
→ Solution: Use venv as shown above or `pipx`
