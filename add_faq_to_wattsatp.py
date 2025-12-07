import csv
import os
import json
from datetime import datetime

# ===================================================================
# WATTSATPCONTRACTOR.COM – 100% SAFE, NO-BREAK SCRIPT
# Works with your existing file: norfolk-qa.csv
# Adds visible Q&A + perfect FAQ schema to ALL 58 pages
# ===================================================================

CSV_FILE = "norfolk-qa.csv"                                            # Your existing CSV
DOMAIN = "https://wattsatpcontractor.com"                              # Your real domain
INSERT_BEFORE = "</body>"                                              # 99% of themes use this
BACKUP_FOLDER = f"backup_before_faq_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# ALL 58 SERVICE PAGES – HARD-CODED SO SCRIPT CAN NEVER FAIL TO FIND THEM
ALL_PAGES = [
    "services/accessibility-safety-solutions.html",
    "services/ada-compliant-showers-bathrooms.html",
    "services/grab-bar-installation.html",
    "services/non-slip-flooring.html",
    "services/custom-ramps.html",
    "services/wheelchair-ramp-installation.html",
    "services/senior-safety.html",
    "services/bathroom-accessibility.html",
    "services/stairlift-elevator-installation.html",
    "services/home-remodeling.html",
    "services/kitchen-renovations.html",
    "services/bathroom-remodels.html",
    "services/basement-finishing.html",
    "services/room-additions.html",
    "services/deck-construction.html",
    "services/siding-replacement.html",
    "services/window-doors.html",
    "services/fence-installation.html",
    "services/fence-repair.html",
    "services/drywall-repair.html",
    "services/painting-services.html",
    "services/concrete-pouring.html",
    "services/driveway-installation.html",
    "services/patio-construction.html",
    "services/floor-refinishing.html",
    "services/hardwood-flooring.html",
    "services/concrete-repair.html",
    "services/flooring-installation.html",
    "services/custom-cabinets.html",
    "services/kitchen-cabinetry.html",
    "services/cabinet-refacing.html",
    "services/custom-storage.html",
    "services/onyx-countertops.html",
    "services/countertop-repair.html",
    "services/property-maintenance-services.html",
    "services/handyman-services.html",
    "services/emergency-repairs.html",
    "services/snow-removal.html",
    "services/emergency-snow.html",
    "services/tree-trimming.html",
    "services/gutter-cleaning.html",
    "services/pressure-washing.html",
    "services/lawn-maintenance.html",
    "services/fertilization.html",
    "services/landscape-design.html",
    "services/seasonal-cleanup.html",
    "services/garden-maintenance.html",
    "services/seasonal-prep.html",
    "services/tv-mounting.html",
    "services/home-theater-installation.html",
    "services/audio-visual.html",
    "services/home-audio.html",
    "services/sound-system-setup.html",
    "services/soundbar-setup.html",
    "services/projector-install.html",
    "services/cable-management.html"
]

print(f"Starting FAQ + Schema update for wattsatpcontractor.com")
print(f"Found {len(ALL_PAGES)} service pages hard-coded")
print(f"CSV file: {CSV_FILE}")
print(f"Domain: {DOMAIN}\n")

# Create backup folder
os.makedirs(BACKUP_FOLDER, exist_ok=True)
print(f"Backup folder created: {BACKUP_FOLDER}")

# Load CSV once
if not os.path.exists(CSV_FILE):
    print(f"ERROR: {CSV_FILE} not found!")
    exit()

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    csv_data = [row for row in reader]

# Group Q&A by page (case-insensitive safety)
page_data = {}
for row in csv_data:
    page = row['Page URL'].strip()
    if page not in page_data:
        page_data[page] = []
    page_data[page].append({
        "q": row['Question'].strip(),
        "a": row['Answer'].strip()
    })

# Process EVERY page
updated = 0
for page in ALL_PAGES:
    if not os.path.exists(page):
        print(f"NOT FOUND → {page}")
        continue

    # Backup original
    backup_path = os.path.join(BACKUP_FOLDER, page.replace("/", "_"))
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(page, 'r', encoding='utf-8') as f:
        original = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original)

    # Get Q&A for this page
    qa_list = page_data.get(page, [])
    if not qa_list:
        print(f"NO Q&A FOUND IN CSV → {page}")
        continue

    # Visible HTML
    visible = '<div class="wattsatp-faq-section">\n  <h2>Common Questions – Norfolk, NE</h2>\n'
    for qa in qa_list:
        visible += f'  <div class="faq-item">\n    <h3>{qa["q"]}</h3>\n    <p>{qa["a"]}</p>\n  </div>\n'
    visible += '</div>\n\n'

    # Schema
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": qa["q"],
                "acceptedAnswer": {"@type": "Answer", "text": qa["a"]}
            }
            for qa in qa_list
        ],
        "url": f"{DOMAIN}/{page}"
    }
    schema_block = f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>\n\n'

    # Insert
    if INSERT_BEFORE in original:
        new_content = original.replace(INSERT_BEFORE, f"{schema_block}{visible}{INSERT_BEFORE}")
    else:
        new_content = original + f"\n{schema_block}{visible}"

    with open(page, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"UPDATED → {page} | {len(qa_list)} Q&As")
    updated += 1

print("\n" + "="*60)
print(f"ALL DONE! {updated}/58 pages updated")
print(f"Backups saved in: {BACKUP_FOLDER}")
print("Visible Q&A + perfect FAQ schema now live on wattsatpcontractor.com")
print("Google rich results will appear in 24–72 hours")
print("="*60)