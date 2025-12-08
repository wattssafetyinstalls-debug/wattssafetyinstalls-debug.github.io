#!/usr/bin/env python3
"""
seo_audit_fix.py
----------------
Comprehensive SEO audit & fix utility for WattsATPContractor static site.

Usage:
    python seo_audit_fix.py

Creates *.bak backups before in–place modifications and logs every change
to changes.log in project root. Produces audit_report.txt summarising
all actions + remaining issues.

Requires:
    pip install beautifulsoup4 pillow
"""
import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup, Comment  # type: ignore
from PIL import Image  # type: ignore

# CONFIG ---------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
BASE_URL = "https://wattsatpcontractor.com"
CHANGELOG = PROJECT_ROOT / "changes.log"
REPORT    = PROJECT_ROOT / "audit_report.txt"
HTACCESS  = PROJECT_ROOT / ".htaccess"
BACKUP_EXT = ".bak"

SERVICE_DIR = PROJECT_ROOT / "services"
SERVICE_KEYWORDS = {"installation", "repair", "service", "maintenance", "construction", "remodel"}

# SECURITY HEADERS to enforce in .htaccess
SECURITY_HEADERS_BLOCK = (
    "# === SECURITY HEADERS ADDED BY seo_audit_fix.py ===\n"
    "<IfModule mod_headers.c>\n"
    "    Header always set Strict-Transport-Security \"max-age=31536000; includeSubDomains\"\n"
    "    Header set X-Content-Type-Options \"nosniff\"\n"
    "    Header set X-Frame-Options \"SAMEORIGIN\"\n"
    "    Header set Referrer-Policy \"strict-origin-when-cross-origin\"\n"
    "    Header set Content-Security-Policy \"default-src 'self' https:; img-src 'self' data: https:;\"\n"
    "    Header set Permissions-Policy \"geolocation=(), microphone=(), camera=()\"\n"
    "</IfModule>\n"
)

# LOGGING --------------------------------------------------------------------

def log(msg: str) -> None:
    with CHANGELOG.open("a", encoding="utf-8") as fh:
        fh.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")

# UTILS ----------------------------------------------------------------------

def backup_file(path: Path) -> None:
    bak_path = path.with_suffix(path.suffix + BACKUP_EXT)
    if not bak_path.exists():
        bak_path.write_bytes(path.read_bytes())
        log(f"Backup created: {bak_path.relative_to(PROJECT_ROOT)}")


def canonical_from_path(path: Path) -> str:
    rel = path.relative_to(PROJECT_ROOT)
    if rel.parent == Path('.'):  # root file
        if rel.stem == "index":
            return BASE_URL + "/"  # homepage
        return f"{BASE_URL}/{rel.stem}"
    return f"{BASE_URL}/{rel.with_suffix('').as_posix()}"


def ensure_canonical(soup: BeautifulSoup, url: str) -> bool:
    head = soup.head or soup.new_tag("head")
    link = head.find("link", attrs={"rel": "canonical"})
    if link and link.get("href") == url:
        return False  # already correct
    if link:
        link["href"] = url
    else:
        new_link = soup.new_tag("link", rel="canonical", href=url)
        # insert after meta description if present
        meta_desc = head.find("meta", attrs={"name": "description"})
        if meta_desc:
            meta_desc.insert_after(new_link)
        else:
            head.append(new_link)
    return True


def ensure_meta_description(soup: BeautifulSoup, title_text: str) -> bool:
    head = soup.head or soup.new_tag("head")
    meta_desc = head.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        return False
    template = f"Professional {title_text} by Watts ATP. Serving Northeast Nebraska. Contact (405) 410-6402."
    if meta_desc:
        meta_desc["content"] = template
    else:
        new_meta = soup.new_tag("meta", attrs={"name": "description", "content": template})
        head.insert(0, new_meta)
    return True


def looks_like_service_page(path: Path) -> bool:
    if SERVICE_DIR in path.parents:
        return True
    stem = path.stem.lower()
    return any(kw in stem for kw in SERVICE_KEYWORDS)


SERVICE_SCHEMA_TEMPLATE = {
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "{title}",
    "provider": {
        "@type": "LocalBusiness",
        "name": "Watts ATP",
        "telephone": "(405) 410-6402",
        "priceRange": "$$",
        "areaServed": {
            "@type": "GeoCircle",
            "geoMidpoint": {
                "@type": "GeoCoordinates",
                "latitude": 42.032,
                "longitude": -97.418
            },
            "geoRadius": 80000
        }
    }
}

BRAND_LIST = ["Trane", "Carrier", "Lennox"]


def ensure_service_schema(soup: BeautifulSoup, title_text: str) -> bool:
    """Add Service JSON-LD if absent (even when other JSON-LD blocks exist)."""
    existing_ld = soup.find_all("script", attrs={"type": "application/ld+json"})
    for tag in existing_ld:
        try:
            data = json.loads(tag.string or "{}")
        except Exception:
            continue
        # normalize to list for inspection
        blocks = data if isinstance(data, list) else [data]
        for block in blocks:
            if isinstance(block, dict) and block.get("@type", "").lower() == "service":
                return False  # Service already present
    schema = SERVICE_SCHEMA_TEMPLATE.copy()
    schema["name"] = title_text
    for brand in BRAND_LIST:
        if brand.lower() in title_text.lower():
            schema["brand"] = {"@type": "Brand", "name": brand}
            break
    script_tag = soup.new_tag("script", type="application/ld+json")
    script_tag.string = json.dumps(schema, indent=2)
    if soup.body:
        soup.body.append(script_tag)
    else:
        soup.append(script_tag)
    return True


def process_images(soup: BeautifulSoup, html_path: Path, remaining_images: List[Path]) -> int:
    modified = 0
    for img in soup.find_all("img"):
        if img.get("width") and img.get("height"):
            continue
        src = img.get("src", "")
        # local path?
        if not src or src.startswith("http"):
            remaining_images.append(Path(src))
            continue
        img_path = (html_path.parent / src).resolve()
        if img_path.exists():
            try:
                with Image.open(img_path) as im:
                    w, h = im.size
                img["width"] = str(w)
                img["height"] = str(h)
                modified += 1
            except Exception:
                remaining_images.append(img_path)
        else:
            remaining_images.append(img_path)
    return modified


def hash_content(text: str) -> str:
    return hashlib.md5(re.sub(r"\s+", "", text).encode("utf-8")).hexdigest()

# MAIN -----------------------------------------------------------------------

def update_htaccess() -> None:
    if HTACCESS.exists():
        content = HTACCESS.read_text(encoding="utf-8")
        if "SECURITY HEADERS ADDED BY" in content:
            return  # already updated
        backup_file(HTACCESS)
        HTACCESS.write_text(SECURITY_HEADERS_BLOCK + "\n" + content, encoding="utf-8")
        log(".htaccess: security headers added")
    else:
        HTACCESS.write_text(SECURITY_HEADERS_BLOCK, encoding="utf-8")
        log(".htaccess created with security headers")


def main():
    total_files = 0
    fixes = {"canonicals": 0, "meta": 0, "schema": 0, "img_dims": 0}
    remaining_imgs: List[Path] = []
    hashes: Dict[str, List[Path]] = {}

    update_htaccess()

    html_files = list(PROJECT_ROOT.rglob("*.html"))
    total_files = len(html_files)

    for html_path in html_files:
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        orig_hash = hash_content(text)
        soup = BeautifulSoup(text, "html.parser")
        title_tag = soup.title
        page_title = title_tag.text.strip() if title_tag else html_path.stem.replace("-", " ").title()

        changed = False
        # canonical
        if ensure_canonical(soup, canonical_from_path(html_path)):
            fixes["canonicals"] += 1
            changed = True
        # meta description
        if ensure_meta_description(soup, page_title):
            fixes["meta"] += 1
            changed = True
        # schema for service pages
        if looks_like_service_page(html_path):
            if ensure_service_schema(soup, page_title):
                fixes["schema"] += 1
                changed = True
        # images
        if process_images(soup, html_path, remaining_imgs):
            fixes["img_dims"] += 1
            changed = True

        if changed:
            backup_file(html_path)
            html_path.write_text(str(soup), encoding="utf-8")
            log(f"Updated {html_path.relative_to(PROJECT_ROOT)}")

        # duplicate detection
        new_hash = hash_content(str(soup))
        hashes.setdefault(new_hash, []).append(html_path)

    duplicates = [paths for paths in hashes.values() if len(paths) > 1]

    # performance images >100KB
    large_imgs = [p for p in PROJECT_ROOT.rglob("*.*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"} and p.stat().st_size > 100_000]

    # write report
    with REPORT.open("w", encoding="utf-8") as fh:
        fh.write("SEO AUDIT REPORT\n================\n")
        fh.write(f"Files scanned: {total_files}\n")
        for k, v in fixes.items():
            fh.write(f"{k.capitalize()} fixed: {v}\n")
        fh.write(f"Duplicate pages found: {len(duplicates)}\n")
        if duplicates:
            fh.write("\nDuplicates detail:\n")
            for group in duplicates:
                fh.write(", ".join(str(p.relative_to(PROJECT_ROOT)) for p in group) + "\n")
        fh.write(f"\nImages missing dimensions remaining: {len(remaining_imgs)}\n")
        fh.write(f"Images >100KB: {len(large_imgs)}\n")

    log("Audit complete. See audit_report.txt for summary")

if __name__ == "__main__":
    main()
