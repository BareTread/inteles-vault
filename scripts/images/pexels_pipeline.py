#!/usr/bin/env python3
import os
import io
import json
import math
import random
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

try:
    from dotenv import load_dotenv  # optional
except Exception:  # pragma: no cover
    def load_dotenv(*a, **k):
        return None

import requests
from PIL import Image, ImageEnhance, ImageFilter

try:
    from slugify import slugify
except Exception:
    # Fallback: simple slugify
    import re
    def slugify(value: str) -> str:
        v = re.sub(r"[^\w\-\s]", "", value.lower()).strip()
        v = re.sub(r"[\s\-]+", "-", v)
        return v[:60]


# Default output sizes
HERO_SIZE = (1200, 675)     # 16:9, featured/hero
INLINE_SIZE = (1200, 800)   # 3:2, inline body
SQUARE_SIZE = (1200, 1200)  # square, social/inline


def ensure_dirs(base: Path) -> Dict[str, Path]:
    raw_dir = base / "raw"
    proc_dir = base / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    proc_dir.mkdir(parents=True, exist_ok=True)
    return {"raw": raw_dir, "processed": proc_dir}


def pexels_search(api_key: str, query: str, per_page: int = 10, orientation: str = "landscape") -> Dict[str, Any]:
    url = "https://api.pexels.com/v1/search"
    params = {"query": query, "per_page": per_page, "orientation": orientation}
    r = requests.get(url, params=params, headers={"Authorization": api_key}, timeout=60)
    r.raise_for_status()
    return r.json()


def choose_src(photo: Dict[str, Any]) -> Tuple[str, str]:
    """Return (best_url, file_ext). Prefer large2x/original JPGs."""
    src = photo.get("src") or {}
    for key in ("large2x", "original", "large", "medium"):
        u = src.get(key)
        if isinstance(u, str) and u.startswith("http"):
            ext = ".jpg"
            if ".png" in u.lower():
                ext = ".png"
            return u, ext
    # Fallback to any top-level url if present
    u = photo.get("url") or ""
    return u, ".jpg"


def download_file(url: str, dest: Path) -> None:
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def center_crop_to_aspect(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    target_ratio = target_w / target_h
    w, h = img.size
    src_ratio = w / h
    if abs(src_ratio - target_ratio) < 1e-3:
        return img
    # crop to match aspect
    if src_ratio > target_ratio:
        # too wide -> crop width
        new_w = int(h * target_ratio)
        x1 = (w - new_w) // 2
        box = (x1, 0, x1 + new_w, h)
    else:
        # too tall -> crop height
        new_h = int(w / target_ratio)
        y1 = (h - new_h) // 2
        box = (0, y1, w, y1 + new_h)
    return img.crop(box)


def apply_small_variations(img: Image.Image, seed: int) -> Image.Image:
    """Apply very subtle, human-imperceptible changes to increase uniqueness."""
    rng = random.Random(seed)
    img = img.convert("RGB")
    # Subtle rotation (±0.2°)
    angle = rng.uniform(-0.2, 0.2)
    bg = tuple(int(x) for x in img.resize((1, 1)).getpixel((0, 0)))  # dominant-ish average
    img = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=bg)
    # micro contrast/brightness tweaks
    contrast = 1.0 + rng.uniform(-0.02, 0.02)
    brightness = 1.0 + rng.uniform(-0.02, 0.02)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    # minute sharpness change
    sharpness = 1.0 + rng.uniform(-0.05, 0.05)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    # tiny Gaussian blur to smooth pixel-level artifacts
    sigma = rng.uniform(0.0, 0.2)
    if sigma > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=sigma))
    return img


def to_webp(img: Image.Image, size: Tuple[int, int], quality: int = 84) -> Image.Image:
    # Crop to aspect, resize, ensure RGB
    target = center_crop_to_aspect(img, *size)
    target = target.resize(size, Image.LANCZOS).convert("RGB")
    # Ensure metadata stripped by saving to in-memory WebP
    out = io.BytesIO()
    target.save(out, format="WEBP", quality=quality, method=6)
    out.seek(0)
    return Image.open(out)


def build_alt_text_ro(topic: str, pexels_alt: str) -> str:
    topic = (topic or "imagine").strip()
    base = pexels_alt.strip() if pexels_alt else "fotografie relevantă"
    # Keep short, descriptive, Romanian context-first
    return f"Imagine pentru articol despre {topic}: {base}"


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Pexels → Unique WebP pipeline (search, download, transform, manifest)")
    parser.add_argument("--query", action="append", default=[], help="Search query (can repeat)")
    parser.add_argument("--per", type=int, default=6, help="Results per query")
    parser.add_argument("--topic", default="vise", help="Context topic for alt text (RO)")
    parser.add_argument("--slug", default="generic", help="Post/article slug for filenames")
    parser.add_argument("--out-dir", default="10-Assets/pexels", help="Base output directory")
    parser.add_argument("--seed", type=int, default=None, help="Global seed for deterministic transforms")
    parser.add_argument("--no-download", action="store_true", help="Skip Pexels download; transform existing files in raw/")
    parser.add_argument("--pick", type=int, default=None, help="Pick top N from each query (by pexels relevance order)")
    args = parser.parse_args()

    api_key = os.getenv("PEXELS_API_KEY")
    if not args.no_download and not api_key:
        raise SystemExit("Missing PEXELS_API_KEY in environment (.env).")

    base = Path(args.out_dir)
    dirs = ensure_dirs(base)

    photos: List[Dict[str, Any]] = []
    if not args.no_download:
        for q in args.query:
            data = pexels_search(api_key, q, per_page=args.per, orientation="landscape")
            items = data.get("photos") or []
            if args.pick and args.pick > 0:
                items = items[: args.pick]
            photos.extend(items)

        # Download raw files
        for ph in photos:
            best_url, ext = choose_src(ph)
            pid = ph.get("id")
            fn = f"pexels-{pid}{ext}"
            dest = dirs["raw"] / fn
            if not dest.exists():
                try:
                    download_file(best_url, dest)
                except Exception as e:
                    print(f"Skip {pid}: download failed: {e}")

    # Transform raw images → WebP sizes
    manifest: List[Dict[str, Any]] = []
    raw_files = sorted(dirs["raw"].glob("*.*"))
    if not raw_files:
        print("No raw files found to process. Place images in 10-Assets/pexels/raw/")
        return

    for rf in raw_files:
        try:
            img = Image.open(rf)
        except Exception as e:
            print(f"Skip {rf.name}: cannot open ({e})")
            continue

        # Seed per file (stable uniqueness)
        base_seed = args.seed if args.seed is not None else int(hashlib.md5(rf.name.encode()).hexdigest(), 16) % (2**31)
        varied = apply_small_variations(img, base_seed)

        sizes = {
            "hero": HERO_SIZE,
            "inline": INLINE_SIZE,
            "square": SQUARE_SIZE,
        }

        outputs: Dict[str, str] = {}
        for label, size in sizes.items():
            out_img = to_webp(varied, size)
            pid = ""  # infer pexels id from filename if present
            parts = rf.stem.split("-")
            for p in parts:
                if p.isdigit():
                    pid = p
            name = f"{slugify(args.slug)}-{label}-{pid or rf.stem}.webp"
            out_path = dirs["processed"] / name
            try:
                out_img.save(out_path, format="WEBP", quality=84, method=6)
            except Exception:
                # Already WebP Image instance; ensure proper save path
                out_img.convert("RGB").save(out_path, format="WEBP", quality=84, method=6)
            outputs[label] = str(out_path)

        # Retrieve rough meta from Pexels page if available
        p_meta: Dict[str, Any] = {}
        if photos:
            # map by id
            by_id = {str(ph.get("id")): ph for ph in photos}
            p = by_id.get(pid or "") if pid else None
            if p:
                p_meta = {
                    "pexels_id": p.get("id"),
                    "pexels_url": p.get("url"),
                    "photographer": p.get("photographer"),
                    "photographer_url": p.get("photographer_url"),
                    "alt": p.get("alt"),
                    "avg_color": p.get("avg_color"),
                    "license": "Pexels License",
                }

        alt_ro = build_alt_text_ro(args.topic, (p_meta.get("alt") or "").strip())
        credit_text = "Fotografie: Pexels"
        if p_meta.get("photographer"):
            credit_text = f"Foto: {p_meta['photographer']} / Pexels"

        record = {
            "source": str(rf),
            "outputs": outputs,
            "topic": args.topic,
            "slug": args.slug,
            "alt_text_ro": alt_ro,
            "caption_ro": credit_text,
            "pexels": p_meta,
        }
        manifest.append(record)

    # Write manifest
    man_path = base / "processed" / f"manifest-{slugify(args.slug)}.json"
    man_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote manifest: {man_path} ({len(manifest)} items)")
    print("Example HTML for WordPress:")
    if manifest:
        m0 = manifest[0]
        print("<figure>\n  <img src=\"" + m0["outputs"]["hero"] + f"\" alt=\"{m0['alt_text_ro']}\">\n  <figcaption>{m0['caption_ro']}</figcaption>\n</figure>")


if __name__ == "__main__":
    main()

