#!/usr/bin/env python3
"""Simple processor for TVA Guide 2025 images - generate metadata and optimize."""

import json
import csv
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import random

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "raw"
OUT_DIR = BASE_DIR / "processed"

# Create processed directory
OUT_DIR.mkdir(exist_ok=True)

# TVA Guide 2025 Image Specifications
IMAGES = [
    {
        "filename": "tva-ghid-ero-calcul-formula-birou-profesional.webp",
        "alt": "Birou profesional organizat cu laptop, documente financiare și calculator pentru calcul TVA, reprezentând ghidul complet fiscal 2025",
        "caption": "TVA reprezintă un pilon fundamental al sistemului fiscal românesc, afectând atât antreprenorii, cât și consumatorii finali.",
        "placement": "Imediat după titlul H1, introducere",
        "keywords": ["TVA", "calcul fiscal", "ghid TVA 2025", "documentație financiară", "birou contabilitate"],
        "role": "hero",
        "priority": "1",
    },
    {
        "filename": "tva-calcul-cote-procente-financiare-business.webp",
        "alt": "Calcul TVA cu cote procente pe fond roșu, monede și grafice financiare pentru businessul românesc",
        "caption": "Modificările cotelor TVA din 2025 impun recalcularea prețurilor și adaptarea sistemelor de facturare.",
        "placement": "Secțiunea 'Cotele TVA în România' după prezentarea modificărilor 2025",
        "keywords": ["cote TVA", "procente TVA", "calcul TVA 2025", "modificări fiscale", "finanțe business"],
        "role": "inline",
        "priority": "2",
    },
    {
        "filename": "tva-formulare-declaratii-documentatie-conformitate.webp",
        "alt": "Formulare TVA și documente de conformitate fiscală cu peniță și ochelari pe birou, simbolizând obligațiile antreprenorilor",
        "caption": "Obligațiile de declarare TVA necesită atenție la detalii și respectarea termenelor limită pentru evitarea sancțiunilor.",
        "placement": "Secțiunea 'Obligațiile Antreprenorilor'",
        "keywords": ["declarații TVA", "formulare fiscale", "conformitate TVA", "obligații antreprenori", "documentație fiscală"],
        "role": "inline",
        "priority": "3",
    },
    {
        "filename": "tva-efactura-digitalizare-sistem-modern-facturare-electronica.webp",
        "alt": "Sistem modern e-Factura cu laptop și smartphone, reprezentând digitalizarea facturării și sistemul TVA electronic",
        "caption": "Sistemul e-Factura elimină birocrația și combate evaziunea fiscală prin automatizarea proceselor de facturare.",
        "placement": "Secțiunea 'Sistemul e-Factura'",
        "keywords": ["e-Factura", "facturare electronică", "digitalizare TVA", "sistem fiscal modern", "ANAF electronic"],
        "role": "inline",
        "priority": "4",
    },
    {
        "filename": "tva-comert-international-export-import-container-european.webp",
        "alt": "Containere maritime colorate în port internațional, simbolizând comerțul UE și reglementările TVA la export-import",
        "caption": "Regulamentările TVA în comerțul internațional facilitează scutirile la export și taxarea la import în Uniunea Europeană.",
        "placement": "Secțiunea 'TVA în Comerțul Internațional'",
        "keywords": ["TVA internațional", "export import UE", "comerț european", "containere maritime", "reglementări TVA UE"],
        "role": "inline",
        "priority": "5",
    },
    {
        "filename": "tva-consultanta-negocii-planificare-strategie-2025.webp",
        "alt": "Ședință de consultanță de afaceri pentru planificarea strategică a modificărilor TVA 2025",
        "caption": "Consultanța specializată și planificarea strategică asigură tranziția lină către noile reglementări TVA din 2025.",
        "placement": "Secțiunea 'Pregătirea pentru Schimbările din 2025'",
        "keywords": ["consultanță TVA", "planificare fiscală 2025", "strategie business", "modificări TVA", "consultanță afaceri"],
        "role": "inline",
        "priority": "6",
    },
]

def process_images():
    """Process images and generate metadata."""
    results = []

    for img_data in IMAGES:
        src_path = RAW_DIR / img_data["filename"]
        out_path = OUT_DIR / img_data["filename"]

        if src_path.exists():
            # Copy to processed directory (images already optimized as WebP)
            with Image.open(src_path) as img:
                # Get image dimensions
                width, height = img.size

                # Generate title slug
                title_slug = img_data["filename"].replace(".webp", "").replace("-", " ")

                # Create result entry
                result = {
                    "status": "ok",
                    "file": img_data["filename"],
                    "role": img_data["role"],
                    "width": width,
                    "height": height,
                    "alt": img_data["alt"],
                    "caption": img_data["caption"],
                    "placement": img_data["placement"],
                    "keywords": img_data["keywords"],
                    "priority": img_data["priority"],
                    "recommended": True,
                    "final_size_bytes": src_path.stat().st_size,
                    "final_quality": "optimized",
                    "title_slug": title_slug,
                }

                results.append(result)

                # Copy file to processed directory
                import shutil
                shutil.copy2(src_path, out_path)

                print(f"✅ Processed: {img_data['filename']} ({width}x{height}, {src_path.stat().st_size:,} bytes)")
        else:
            print(f"❌ Missing: {img_data['filename']}")
            result = {
                "status": "missing",
                "file": img_data["filename"],
                "src": str(src_path),
            }
            results.append(result)

    # Write metadata files
    metadata_json = OUT_DIR / "tva_article_metadata.json"
    metadata_csv = OUT_DIR / "tva_article_metadata.csv"

    # JSON metadata
    with open(metadata_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # CSV metadata
    with open(metadata_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "filename", "alt", "caption", "placement", "keywords",
            "role", "priority", "recommended", "final_size_bytes",
            "final_quality", "title_slug"
        ])

        for result in results:
            if result.get("status") == "ok":
                writer.writerow([
                    result["file"],
                    result["alt"],
                    result["caption"],
                    result["placement"],
                    "; ".join(result["keywords"]),
                    result["role"],
                    result["priority"],
                    "da" if result["recommended"] else "nu",
                    result["final_size_bytes"],
                    result["final_quality"],
                    result["title_slug"],
                ])

    print(f"\n📄 Metadata saved to:")
    print(f"   - JSON: {metadata_json}")
    print(f"   - CSV: {metadata_csv}")
    print(f"   - Images: {OUT_DIR}")

    return results

if __name__ == "__main__":
    print("🎨 TVA Guide 2025 - Simple Image Processor")
    print("=" * 50)
    results = process_images()

    ok_count = len([r for r in results if r.get("status") == "ok"])
    print(f"\n✅ Successfully processed {ok_count} images for TVA Guide 2025 article")