#!/usr/bin/env python3
"""Generate SEO-ready WebP assets for TVA Guide 2025 article on inteles.ro.

Features:
  - Light random micro-adjustments (crop, rotate, color/brightness) for uniqueness
  - Perceptual hash deduplication (prevents reusing similar stock photos)
  - LQIP with BlurHash for instant rendering (Core Web Vitals)
  - EXIF stripping and Romanian slug generation
  - Metadata export (JSON + CSV) for WordPress/Kadence

Usage:
    python tva_article_image_pipeline.py [--seed 1234] [--quality 82]

Output:
    processed/
      ├── {filename}.webp
      ├── metadata.json
      └── metadata.csv
"""

from __future__ import annotations

import argparse
import base64
import csv
import io
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Optional dependencies - graceful degradation
try:
    from blurhash import encode as blurhash_encode
    HAS_BLURHASH = True
except ImportError:
    HAS_BLURHASH = False

try:
    import imagehash
    HAS_DEDUPE = True
except ImportError:
    HAS_DEDUPE = False

try:
    from unidecode import unidecode
    HAS_UNIDECODE = True
except ImportError:
    HAS_UNIDECODE = False


BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "raw"
OUT_DIR = BASE_DIR / "processed"
DEDUPE_DB = OUT_DIR / "phash_index.json"


@dataclass
class ImageSpec:
    src: str
    out: str
    role: str  # "hero" | "inline" | "gallery"
    target_width: int
    target_height: int
    alt: str
    caption: str | None
    placement: str
    keywords: List[str]
    priority: str
    recommended: bool = True


# TVA Guide 2025 Image Specifications
SPECS: List[ImageSpec] = [
    ImageSpec(
        src="pexels_8970693_original.jpeg",
        out="tva-ghid-ero-calcul-formula-birou-profesional.webp",
        role="hero",
        target_width=1600,
        target_height=900,
        alt="Birou profesional organizat cu laptop, documente financiare și calculator pentru calcul TVA, reprezentând ghidul complet fiscal 2025",
        caption="TVA reprezintă un pilon fundamental al sistemului fiscal românesc, afectând atât antreprenorii, cât și consumatorii finali.",
        placement="Imediat după titlul H1, introducere",
        keywords=["TVA", "calcul fiscal", "ghid TVA 2025", "documentație financiară", "birou contabilitate"],
        priority="1",
    ),
    ImageSpec(
        src="pexels_6120251_original.jpeg",
        out="tva-calcul-cote-procente-financiare-business.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Calcul TVA cu cote procente pe fond roșu, monede și grafice financiare pentru businessul românesc",
        caption="Modificările cotelor TVA din 2025 impun recalcularea prețurilor și adaptarea sistemelor de facturare.",
        placement="Secțiunea 'Cotele TVA în România' după prezentarea modificărilor 2025",
        keywords=["cote TVA", "procente TVA", "calcul TVA 2025", "modificări fiscale", "finanțe business"],
        priority="2",
    ),
    ImageSpec(
        src="pexels_6929017_original.jpeg",
        out="tva-formulare-declaratii-documentatie-conformitate.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Formulare TVA și documente de conformitate fiscală cu peniță și ochelari pe birou, simbolizând obligațiile antreprenorilor",
        caption="Obligațiile de declarare TVA necesită atenție la detalii și respectarea termenelor limită pentru evitarea sancțiunilor.",
        placement="Secțiunea 'Obligațiile Antreprenorilor'",
        keywords=["declarații TVA", "formulare fiscale", "conformitate TVA", "obligații antreprenori", "documentație fiscală"],
        priority="3",
    ),
    ImageSpec(
        src="pexels_4050451_original.jpeg",
        out="tva-efactura-digitalizare-sistem-modern-facturare-electronica.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Sistem modern e-Factura cu laptop și smartphone, reprezentând digitalizarea facturării și sistemul TVA electronic",
        caption="Sistemul e-Factura elimină birocrația și combate evaziunea fiscală prin automatizarea proceselor de facturare.",
        placement="Secțiunea 'Sistemul e-Factura'",
        keywords=["e-Factura", "facturare electronică", "digitalizare TVA", "sistem fiscal modern", "ANAF electronic"],
        priority="4",
    ),
    ImageSpec(
        src="pexels_20034030_original.jpeg",
        out="tva-comert-international-export-import-container-european.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Containere maritime colorate în port internațional, simbolizând comerțul UE și reglementările TVA la export-import",
        caption="Regulamentările TVA în comerțul internațional facilitează scutirile la export și taxarea la import în Uniunea Europeană.",
        placement="Secțiunea 'TVA în Comerțul Internațional'",
        keywords=["TVA internațional", "export import UE", "comerț european", "containere maritime", "reglementări TVA UE"],
        priority="5",
    ),
    ImageSpec(
        src="pexels_8112148_original.jpeg",
        out="tva-consultanta-negocii-planificare-strategie-2025.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Ședință de consultanță de afaceri pentru planificarea strategică a modificărilor TVA 2025",
        caption="Consultanța specializată și planificarea strategică asigură tranziția lină către noile reglementări TVA din 2025.",
        placement="Secțiunea 'Pregătirea pentru Schimbările din 2025'",
        keywords=["consultanță TVA", "planificare fiscală 2025", "strategie business", "modificări TVA", "consultanță afaceri"],
        priority="6",
    ),
]


# --- Utility functions for dedupe, slugs, LQIP, AVIF ---


def ro_slug(text: str) -> str:
    """Convert Romanian text to SEO-friendly slug (diacritics → ASCII)."""
    if HAS_UNIDECODE:
        s = unidecode(text.lower())
    else:
        # Fallback: basic ASCII conversion
        s = text.lower()
        replacements = {
            'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
            'Ă': 'a', 'Â': 'a', 'Î': 'i', 'Ș': 's', 'Ț': 't'
        }
        for ro, en in replacements.items():
            s = s.replace(ro, en)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s


def compute_phash(pil_img: Image.Image) -> str:
    """Compute perceptual hash of image."""
    if not HAS_DEDUPE:
        return ""
    return str(imagehash.phash(pil_img.convert("RGB")))


def load_phash_db() -> Dict[str, Any]:
    """Load dedupe database of phashes."""
    if DEDUPE_DB.exists():
        return json.loads(DEDUPE_DB.read_text(encoding="utf-8"))
    return {}


def save_phash_db(db: Dict[str, Any]) -> None:
    """Persist dedupe database."""
    DEDUPE_DB.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding="utf-8")


def hamming(a: str, b: str) -> int:
    """Hamming distance between two strings."""
    return sum(ch1 != ch2 for ch1, ch2 in zip(a, b))


def tiny_lqip(pil_img: Image.Image) -> Dict[str, str]:
    """Generate LQIP (Low Quality Image Placeholder) with BlurHash."""
    w, h = pil_img.size
    tw = 24
    th = max(12, int(h * (tw / w)))
    tiny = pil_img.resize((tw, th), Image.Resampling.LANCZOS)

    # BlurHash (optional)
    bh = ""
    if HAS_BLURHASH:
        arr = np.asarray(tiny.convert("RGB"))
        bh = blurhash_encode(arr, 4, 3)

    # LQIP data URI (always generated)
    buf = io.BytesIO()
    tiny.save(buf, format="WEBP", quality=50, method=6)
    data_uri = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii")

    return {"blurhash": bh, "lqip_data_uri": data_uri}


def optional_grain(pil_img: Image.Image, strength: float = 0.015) -> Image.Image:
    """Add faint luminance grain to break exact matching (SEO anti-fingerprint)."""
    arr = np.asarray(pil_img.convert("RGB"), dtype=np.float32) / 255.0
    noise = np.random.normal(0.0, strength, size=arr.shape).astype(np.float32)
    out = np.clip(arr + noise, 0, 1)
    out = (out * 255.0).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def choose_crop_box(width: int, height: int, target_ratio: float) -> Tuple[int, int, int, int]:
    current_ratio = width / height
    if abs(current_ratio - target_ratio) < 1e-3:
        return 0, 0, width, height
    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        offset = random.randint(0, max(0, width - new_width))
        return offset, 0, offset + new_width, height
    new_height = int(width / target_ratio)
    offset = random.randint(0, max(0, height - new_height))
    return 0, offset, width, offset + new_height


def apply_micro_adjustments(img: Image.Image) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    if random.random() < 0.25:
        img = ImageOps.mirror(img)
    if random.random() < 0.15:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 0.6)))
    for enhancer_cls, low, high in (
        (ImageEnhance.Color, 0.97, 1.05),
        (ImageEnhance.Brightness, 0.97, 1.04),
        (ImageEnhance.Contrast, 0.98, 1.06),
        (ImageEnhance.Sharpness, 1.00, 1.14),
    ):
        enhancer = enhancer_cls(img)
        img = enhancer.enhance(random.uniform(low, high))
    angle = random.uniform(-1.1, 1.1)
    if abs(angle) > 0.2:
        img = img.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True, fillcolor=(12, 12, 12))
    return img


def save_webp(img: Image.Image, out_path: Path, quality: int, max_bytes: int) -> Dict[str, Any]:
    q = quality
    best_bytes: bytes | None = None
    best_q: int | None = None
    while q >= 55:
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=q, method=6)
        data = buf.getvalue()
        if len(data) <= max_bytes:
            best_bytes = data
            best_q = q
            break
        q -= 5
    if best_bytes is None:
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=55, method=6)
        best_bytes = buf.getvalue()
        best_q = 55
    out_path.write_bytes(best_bytes)
    return {"quality": best_q, "bytes": len(best_bytes)}


def process_image(spec: ImageSpec, seed: int | None, quality: int = 82) -> Dict[str, Any]:
    """Process image with dedupe, LQIP, and micro-adjustments."""
    db = load_phash_db()
    src_path = RAW_DIR / spec.src
    out_webp = OUT_DIR / spec.out

    if not src_path.exists():
        return {"file": spec.out, "status": "missing_src", "src": str(src_path)}

    if seed is not None:
        random.seed(seed + hash(spec.src) % 100_000)

    with Image.open(src_path) as img:
        base_img = img.convert("RGB")

        # Dedupe check: compute phash on center crop (stable across micro-tweaks)
        center_ratio = spec.target_width / spec.target_height
        cx0, cy0, cx1, cy1 = choose_crop_box(base_img.width, base_img.height, center_ratio)
        center_crop = base_img.crop((cx0, cy0, cx1, cy1)).resize(
            (spec.target_width, spec.target_height), Image.Resampling.LANCZOS
        )
        cur_phash = compute_phash(center_crop)

        # Check for near-duplicates (only if dedupe is available)
        if cur_phash and HAS_DEDUPE:
            for used_phash, meta in db.items():
                if hamming(cur_phash, used_phash) <= 5:
                    return {
                        "status": "duplicate_like",
                        "file": spec.out,
                        "src_original": spec.src,
                        "similar_to": meta.get("file"),
                        "phash": cur_phash,
                    }

        # Full processing pipeline
        img2 = center_crop
        img2 = apply_micro_adjustments(img2)
        if random.random() < 0.35:
            img2 = optional_grain(img2, strength=0.012)
        img2.info.pop("exif", None)

        # Save WebP within budget
        budget = 180_000 if spec.role == "hero" else 140_000
        details = save_webp(img2, out_webp, quality=quality, max_bytes=budget)

        # Generate LQIP + BlurHash
        lqip = tiny_lqip(img2)

        # Clean slug from filename
        title_slug = ro_slug(Path(spec.out).stem.replace("-", " "))

        # Update dedupe DB
        if cur_phash and HAS_DEDUPE:
            db[cur_phash] = {"file": spec.out, "src": spec.src}
            save_phash_db(db)

    return {
        "status": "ok",
        "file": spec.out,
        "src_original": spec.src,
        "role": spec.role,
        "width": spec.target_width,
        "height": spec.target_height,
        "alt": spec.alt,
        "caption": spec.caption,
        "placement": spec.placement,
        "keywords": spec.get("keywords", []),
        "priority": spec.priority,
        "recommended": spec.recommended,
        "final_quality": details["quality"],
        "final_size_bytes": details["bytes"],
        "blurhash": lqip.get("blurhash", ""),
        "lqip_data_uri": lqip.get("lqip_data_uri", ""),
        "title_slug": title_slug,
        "phash": cur_phash,
    }


def write_metadata(results: List[Dict[str, Any]]) -> None:
    """Write metadata.json and metadata.csv."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "metadata.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    with (OUT_DIR / "metadata.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "filename",
            "alt",
            "caption",
            "placement",
            "keywords",
            "role",
            "priority",
            "recommended",
            "final_size_bytes",
            "final_quality",
            "blurhash",
            "title_slug",
            "phash",
        ])
        for row in results:
            if row.get("status") != "ok":
                continue
            writer.writerow([
                row["file"],
                row["alt"],
                row.get("caption", "") or "",
                row["placement"],
                "; ".join(row.get("keywords", [])),
                row["role"],
                row["priority"],
                "da" if row["recommended"] else "nu",
                row["final_size_bytes"],
                row["final_quality"],
                row.get("blurhash", ""),
                row.get("title_slug", ""),
                row.get("phash", ""),
            ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Procesează imaginile pentru articolul TVA Guide 2025")
    parser.add_argument("--seed", type=int, default=1234, help="Seed pentru reproducibilitate")
    parser.add_argument("--quality", type=int, default=82, help="Calitate WebP (55-95, default: 82)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_dirs()

    # Show feature status
    print(f"🎨 TVA Guide 2025 Image Pipeline:")
    print(f"   - Dedupe: {'✅' if HAS_DEDUPE else '❌ (install python-imagehash)'}")
    print(f"   - BlurHash: {'✅' if HAS_BLURHASH else '❌ (install python-blurhash)'}")
    print(f"   - Romanian slugs: {'✅' if HAS_UNIDECODE else '❌ (install python-unidecode)'}")
    print(f"   - Seed: {args.seed if args.seed else 'random'}")
    print(f"   - Quality: {args.quality}\n")

    results = [process_image(spec, args.seed, args.quality) for spec in SPECS]
    write_metadata(results)

    missing = [r for r in results if r.get("status") != "ok"]
    if missing:
        print("⚠️  Fișiere lipsă sau erori:")
        for item in missing:
            status = item.get('status', 'unknown')
            if status == 'duplicate_like':
                print(f"   - {item['file']} -> DUPLICAT (similar cu {item.get('similar_to', 'unknown')})")
            else:
                print(f"   - {item['src'] if 'src' in item else item['file']} -> {status}")
    else:
        ok_count = len([r for r in results if r.get("status") == "ok"])
        print(f"✅ Procesat {ok_count} imagini pentru articolul TVA Guide 2025 în {OUT_DIR}")


if __name__ == "__main__":
    main()