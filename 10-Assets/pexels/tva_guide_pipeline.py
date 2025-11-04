#!/usr/bin/env python3
"""TVA Ghid Complet 2025 - Image Pipeline for inteles.ro

Processes TVA guide images with Romanian metadata and SEO optimization.
Images for comprehensive VAT guide covering rates, calculations, compliance.
"""

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
    # Hero Image - Professional accountant with documents and calculator
    ImageSpec(
        src="pexels_8296970_original.jpeg",
        out="tva-ghid-contabilitate-profesionala-calculator-documente.webp",
        role="hero",
        target_width=1600,
        target_height=900,
        alt="Contabil profesionist analizând documente financiare și calculând TVA cu calculatorul pe birou, reprezentând expertiză în fiscalitate românească",
        caption="TVA în România necesită cunoștințe specializate și atenție la detalii pentru calcul corect și conformare legală.",
        placement="Imediat după H1, introducere",
        keywords=["tva", "contabilitate", "documente fiscale", "calculator", "expertiza"],
        priority="1",
    ),

    # Inline 1 - Tax documents with smartphone (e-Factura concept)
    ImageSpec(
        src="pexels_8962519_original.jpeg",
        out="tva-efactura-digitalizare-documente-fiscale-smartphone.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Documente fiscale și smartphone pe birou, ilustrând sistemul modern e-Factura pentru TVA digitalizat în România",
        caption="Sistemul e-Factura digitalizează procesul de facturare TVA, reducând birocrația și erorile umane.",
        placement="După secțiunea Sistemul e-Factura",
        keywords=["efactura", "digitalizare", "documente fiscale", "tva digital", "smartphone"],
        priority="2",
    ),

    # Inline 2 - Financial charts with magnifying glass (tax analysis)
    ImageSpec(
        src="pexels_7948002_original.jpeg",
        out="tva-analiza-financiara-graficuri-lupa-calcul-procente.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Graficuri financiare cu lupă de analiză, reprezentând calculul detaliat al cotelor de TVA și analiza fiscală",
        caption="Analiza atentă a cotelor de TVA (19%, 9%, 5%) și modificările din 2025 (21%, 11%) asigură conformarea corectă.",
        placement="După secțiunea Calculul TVA-ului",
        keywords=["tva calcul", "cote", "procente", "analiza financiara", "graficuri"],
        priority="3",
    ),

    # Inline 3 - Business meeting discussing taxes
    ImageSpec(
        src="pexels_8353799_original.jpeg",
        out="tva-consultanta-business-meeting-discutie-strategie-fiscala.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Echipă de afaceri discutând strategii fiscale și TVA în ședință profesională, planificare optimizare taxe",
        caption="Consultanța fiscală profesională ajută companiile să navigheze complexitatea sistemului TVA și să se pregătească pentru modificările din 2025.",
        placement="După secțiunea Obligațiile Antreprenorilor",
        keywords=["consultanta tva", "business meeting", "strategie fiscala", "optimizare", "discutie"],
        priority="4",
    ),

    # Inline 4 - Digital tax system on monitor
    ImageSpec(
        src="pexels_7567222_original.jpeg",
        out="tva-sistem-digital-monitor-analiza-date-fiscalitate-moderna.webp",
        role="inline",
        target_width=1200,
        target_height=675,
        alt="Monitor cu sistem digital de analiză fiscală și date TVA, reprezentând transformarea digitală în administrarea taxelor",
        caption="Sistemele digitale moderne pentru administrarea TVA oferă eficiență, transparență și control îmbunătățit asupra conformității fiscale.",
        placement="După secțiunea Pregătirea pentru Schimbările din 2025",
        keywords=["sistem digital", "monitor", "date fiscale", "modernizare", "digitalizare tva"],
        priority="5",
    ),
]


def load_dedupe_db() -> Dict[str, str]:
    """Load existing perceptual hash database."""
    if DEDUPE_DB.exists():
        return json.loads(DEDUPE_DB.read_text())
    return {}


def save_dedupe_db(db: Dict[str, str]) -> None:
    """Save perceptual hash database."""
    DEDUPE_DB.write_text(json.dumps(db, indent=2))


def romanian_slug(text: str) -> str:
    """Convert text to Romanian-friendly slug."""
    if HAS_UNIDECODE:
        text = unidecode(text)
    # Remove non-alphanumeric characters, replace spaces with hyphens
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    return text.lower()


def apply_subtle_adjustments(img: Image.Image, seed: int | None = None) -> Image.Image:
    """Apply micro-adjustments for uniqueness while maintaining quality."""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Smart crop to target aspect ratio (16:9 for hero, 16:9 for inline)
    target_ratio = 16 / 9
    current_ratio = img.width / img.height

    if current_ratio > target_ratio:
        # Image is wider - crop height
        new_height = int(img.width / target_ratio)
        crop_top = random.randint(0, max(0, img.height - new_height))
        img = img.crop((0, crop_top, img.width, crop_top + new_height))
    else:
        # Image is taller - crop width
        new_width = int(img.height * target_ratio)
        crop_left = random.randint(0, max(0, img.width - new_width))
        img = img.crop((crop_left, 0, crop_left + new_width, img.height))

    # Very subtle rotation (-1 to 1 degree)
    angle = random.uniform(-1.0, 1.0)
    if abs(angle) > 0.1:  # Only rotate if meaningful
        img = img.rotate(angle, expand=True, fillcolor='white')

    # Micro color adjustments (±3%)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(random.uniform(0.97, 1.03))

    # Micro brightness (±2%)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(random.uniform(0.98, 1.02))

    # Micro contrast (±3%)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(random.uniform(0.97, 1.03))

    # Very subtle sharpness (±1%)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(random.uniform(0.99, 1.01))

    # Optional: very subtle grain (35% chance)
    if random.random() < 0.35:
        # Add minimal noise
        noise = np.random.normal(0, 2, (img.height, img.width, 3))
        img_array = np.array(img)
        img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(img_array)

    return img


def calculate_perceptual_hash(img: Image.Image) -> str:
    """Calculate perceptual hash for deduplication."""
    if not HAS_DEDUPE:
        return ""

    # Convert to RGB and resize for consistent hashing
    img_rgb = img.convert('RGB')
    img_small = img_rgb.resize((64, 64), Image.Resampling.LANCZOS)
    return str(imagehash.phash(img_small))


def generate_lqip(img: Image.Image, size: int = 32) -> str:
    """Generate Low Quality Image Placeholder as data URI."""
    # Create tiny version
    img_small = img.copy()
    img_small.thumbnail((size, size), Image.Resampling.LANCZOS)

    # Convert to WebP bytes
    buffer = io.BytesIO()
    img_small.save(buffer, format='WEBP', quality=60, method=6)
    img_bytes = buffer.getvalue()

    # Encode as base64 data URI
    base64_str = base64.b64encode(img_bytes).decode()
    return f"data:image/webp;base64,{base64_str}"


def generate_blurhash(img: Image.Image) -> str:
    """Generate BlurHash for instant placeholders."""
    if not HAS_BLURHASH:
        return ""

    img_rgb = img.convert('RGB')
    return blurhash_encode(img_rgb, x_components=4, y_components=3)


def optimize_webp(img: Image.Image, target_bytes: int, quality: int = 82) -> bytes:
    """Optimize WebP to target file size with quality fallback."""
    buffer = io.BytesIO()

    # Try initial quality
    img.save(buffer, format='WEBP', quality=quality, method=6)
    result = buffer.getvalue()

    # If too large, reduce quality progressively
    current_quality = quality
    while len(result) > target_bytes and current_quality > 30:
        current_quality -= 5
        buffer.seek(0)
        buffer.truncate()
        img.save(buffer, format='WEBP', quality=current_quality, method=6)
        result = buffer.getvalue()

    return result


def process_image(spec: ImageSpec, seed: int | None = None, quality: int = 82) -> Dict[str, Any]:
    """Process single image according to specification."""
    result = {
        "status": "ok",
        "spec": {
            "src": spec.src,
            "out": spec.out,
            "role": spec.role,
            "alt": spec.alt,
            "caption": spec.caption,
            "placement": spec.placement,
            "keywords": spec.keywords,
            "priority": spec.priority,
        }
    }

    # Check source file exists
    src_path = RAW_DIR / spec.src
    if not src_path.exists():
        result["status"] = "missing_src"
        result["error"] = f"Source file not found: {src_path}"
        return result

    try:
        # Load image
        img = Image.open(src_path)

        # Apply subtle adjustments for uniqueness
        if seed is not None:
            img = apply_subtle_adjustments(img, seed + hash(spec.src) % 10000)
        else:
            img = apply_subtle_adjustments(img)

        # Check for duplicates
        if HAS_DEDUPE:
            phash = calculate_perceptual_hash(img)
            dedupe_db = load_dedupe_db()

            for existing_file, existing_hash in dedupe_db.items():
                if existing_hash:
                    existing_phash = imagehash.hex_to_hash(existing_hash)
                    current_phash = imagehash.hex_to_hash(phash)
                    distance = existing_phash - current_phash

                    if distance <= 5:  # Very similar images
                        result["status"] = "duplicate_like"
                        result["similar_to"] = existing_file
                        result["distance"] = distance
                        return result

            # Add to dedupe database
            dedupe_db[spec.out] = phash
            save_dedupe_db(dedupe_db)

            result["phash"] = phash

        # Resize to target dimensions
        img = img.resize((spec.target_width, spec.target_height), Image.Resampling.LANCZOS)

        # Generate LQIP and BlurHash
        result["lqip_data_uri"] = generate_lqip(img)
        if HAS_BLURHASH:
            result["blurhash"] = generate_blurhash(img)

        # Optimize and save WebP
        target_bytes = 180000 if spec.role == "hero" else 140000  # 180KB hero, 140KB inline
        webp_bytes = optimize_webp(img, target_bytes, quality)

        out_path = OUT_DIR / spec.out
        out_path.write_bytes(webp_bytes)

        result.update({
            "file": spec.out,
            "final_size_bytes": len(webp_bytes),
            "final_width": spec.target_width,
            "final_height": spec.target_height,
            "title_slug": romanian_slug(spec.out.replace('.webp', '')),
        })

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def save_metadata_csv(results: List[Dict[str, Any]]) -> None:
    """Save results as CSV for WordPress import."""
    csv_path = OUT_DIR / "metadata.csv"

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'filename', 'alt', 'caption', 'title_slug', 'keywords', 'role',
            'priority', 'placement', 'final_size_bytes', 'blurhash'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            if result["status"] == "ok" and "spec" in result:
                spec = result["spec"]
                writer.writerow({
                    'filename': result.get("file", ""),
                    'alt': spec.get("alt", ""),
                    'caption': spec.get("caption", ""),
                    'title_slug': result.get("title_slug", ""),
                    'keywords': ';'.join(spec.get("keywords", [])),
                    'role': spec.get("role", ""),
                    'priority': spec.get("priority", ""),
                    'placement': spec.get("placement", ""),
                    'final_size_bytes': result.get("final_size_bytes", 0),
                    'blurhash': result.get("blurhash", ""),
                })


def main() -> None:
    """Process all TVA guide images."""
    parser = argparse.ArgumentParser(description="TVA Ghid Complet 2025 Image Pipeline")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible results")
    parser.add_argument("--quality", type=int, default=82, help="WebP quality (30-100)")

    args = parser.parse_args()

    # Ensure output directory exists
    OUT_DIR.mkdir(exist_ok=True)

    print("🎨 TVA Ghid Complet 2025 - Image Pipeline")
    print(f"   Pipeline Features:")
    print(f"     - Dedupe: {'✅' if HAS_DEDUPE else '❌ (install python-imagehash)'}")
    print(f"     - BlurHash: {'✅' if HAS_BLURHASH else '❌ (install python-blurhash)'}")
    print(f"     - Romanian Slugs: {'✅' if HAS_UNIDECODE else '❌ (install unidecode)'}")
    print()

    results = []

    for i, spec in enumerate(SPECS):
        print(f"Processing {i+1}/{len(SPECS)}: {spec.out}")
        result = process_image(spec, seed=args.seed, quality=args.quality)
        results.append(result)

        if result["status"] == "ok":
            print(f"  ✅ {result['file']} ({result['final_size_bytes']} bytes)")
        elif result["status"] == "duplicate_like":
            print(f"  ⚠️  Similar to {result['similar_to']} (distance: {result['distance']})")
        else:
            print(f"  ❌ {result['status']}: {result.get('error', 'Unknown error')}")

    # Save metadata
    metadata_path = OUT_DIR / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    save_metadata_csv(results)

    print(f"\n✅ Pipeline complete!")
    print(f"   📁 Processed images: {OUT_DIR}")
    print(f"   📄 Metadata JSON: {metadata_path}")
    print(f"   📊 Metadata CSV: {OUT_DIR / 'metadata.csv'}")

    # Summary
    ok_count = sum(1 for r in results if r["status"] == "ok")
    duplicate_count = sum(1 for r in results if r["status"] == "duplicate_like")
    error_count = len(results) - ok_count - duplicate_count

    print(f"\n📈 Summary:")
    print(f"   ✅ Successful: {ok_count}")
    if duplicate_count > 0:
        print(f"   ⚠️  Duplicates: {duplicate_count}")
    if error_count > 0:
        print(f"   ❌ Errors: {error_count}")


if __name__ == "__main__":
    main()