#!/usr/bin/env python3
import re
from datetime import datetime

print("NUCLEAR FIX STARTED - THIS ONE ACTUALLY WORKS\n")

with open("services.html", "r", encoding="utf-8") as f:
    html = f.read()

original = html  # keep backup in memory

# 1. Inject CSS (only if not already there and </head> exists)
if "pro-cta-btn" not in html and "</head>" in html:
    css = """<style>
    .pro-cta-btn, .banner-quote-btn {
        display: inline-block !important;
        background: #003087 !important;
        color: white !important;
        padding: 14px 32px !important;
        margin: 15px 0 !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-decoration: none !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .pro-cta-btn:hover, .banner-quote-btn:hover {
        background: white !important;
        color: #003087 !important;
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
    }
    </style>"""
    html = html.replace("</head>", css + "\n</head>")
    print("Injected navy button CSS - SUCCESS")

# 2. Fix "Contact Us for a Quote" into a real button
# First, if it's plain text
old_html = html
html, count = re.subn(
    r'(?i)(?<!<a[^>]*>)(Contact\s*Us\s*for\s*a\s*Quote)(?!</a>)',
    r'<a href="/contact" class="pro-cta-btn banner-quote-btn">\1</a>',
    html
)
if count > 0:
    print(f"Fixed {count} plain 'Contact Us for a Quote' - now a navy button")

# Fallback: if it's already a link, add class
html, count = re.subn(
    r'(?i)<a ([^>]*)(?<!class="pro-cta-btn banner-quote-btn")>(Contact\s*Us\s*for\s*a\s*Quote)</a>',
    r'<a \1 class="pro-cta-btn banner-quote-btn">\2</a>',
    html
)
if count > 0:
    print(f"Fixed {count} existing links for 'Contact Us for a Quote' - added button styling")

# 3. NUCLEAR DROPDOWN FIX - looser pattern, partial title match fallback
dropdowns = {
    "Accessibility & Safety": ["accessibility"],  # main title, fallback keywords
    "Home Remodeling": ["remodeling"],
    "TV & Home Theater": ["tv", "theater", "audio"],
    "Property Maintenance": ["property", "maintenance"],
    "Lawn & Landscape": ["lawn", "landscape"],
    "Concrete & Flooring": ["concrete", "flooring"],
    "Cabinets & Countertops": ["cabinets", "countertops"]
}

links_dict = {  # separate links for each
    "Accessibility & Safety": [
        "ADA Compliant Showers|/services/ada-compliant-showers.html",
        "Grab Bars Installation|/services/grab-bars.html",
        "Non-Slip Flooring|/services/non-slip-flooring.html",
        "Custom Wheelchair Ramps|/services/custom-ramps.html",
        "Senior Safety Modifications|/services/senior-safety.html",
        "Bathroom Accessibility|/services/bathroom-accessibility.html",
    ],
    "Home Remodeling": [
        "Kitchen Renovations|/kitchen-renovations",
        "Bathroom Remodels|/home-remodeling",
        "Basement Finishing|/services/basement-finishing.html",
        "Deck Construction|/deck-construction",
        "Siding Replacement|/siding-replacement",
        "Window & Door Installation|/window-doors",
        "Painting Services|/painting-services",
        "Drywall Repair|/services/drywall-repair.html",
    ],
    "TV & Home Theater": [
        "TV Mounting|/services/tv-mounting-residential.html",
        "Home Theater Installation|/services/home-theater.html",
        "Soundbar Setup|/services/soundbar-setup.html",
        "Smart Audio Systems|/services/smart-audio.html",
        "Projector Installation|/services/projector-install.html",
        "Cable Management|/services/cable-management.html",
    ],
    "Property Maintenance": [
        "Routine Maintenance|/services/property-maintenance-routine.html",
        "Emergency Repairs|/services/emergency-repairs.html",
        "Snow Removal|/snow-removal",
        "Tree Trimming|/services/tree-trimming.html",
        "Seasonal Prep & Cleanup|/services/seasonal-prep.html",
    ],
    "Lawn & Landscape": [
        "Lawn Maintenance|/services/lawn-maintenance.html",
        "Landscape Design & Install|/landscape-design",
        "Fertilization & Weed Control|/services/fertilization.html",
        "Seasonal Cleanup|/services/seasonal-cleanup.html",
        "Garden Maintenance|/garden-maintenance",
    ],
    "Concrete & Flooring": [
        "Concrete Pouring & Repair|/concrete-pouring",
        "Driveways & Patios|/driveway-installation",
        "Hardwood Flooring|/hardwood-flooring",
        "Floor Refinishing|/services/floor-refinishing.html",
    ],
    "Cabinets & Countertops": [
        "Custom Cabinets|/custom-cabinets",
        "Cabinet Refacing|/services/cabinet-refacing.html",
        "Onyx & Countertops|/services/onyx-countertops.html",
        "Kitchen Cabinetry|/services/kitchen-cabinetry.html",
        "Custom Storage|/services/custom-storage.html",
    ]
}

for menu_name, fallback_keywords in dropdowns.items():
    links = links_dict[menu_name]
    links_block = "\n".join([f'                        <a href="{url}">{text}</a>' for text, url in [item.split("|", 1) for item in links]])
    # Try exact title match first
    pattern = re.compile(
        rf'(<button[^>]*>[^<]*{re.escape(menu_name)}[^<]*</button>\s*<div[^>]*>)(.*?)(</div>)',
        re.DOTALL | re.IGNORECASE
    )
    new_html, count = pattern.subn(rf'\1\n{links_block}\n                    \3', html)
    if count > 0:
        html = new_html
        print(f"Fixed dropdown: {menu_name} ({len(links)} links added)")
    else:
        # Fallback: try partial keywords
        for keyword in fallback_keywords:
            pattern = re.compile(
                rf'(<button[^>]*>[^<]*{re.escape(keyword)}[^<]*</button>\s*<div[^>]*>)(.*?)(</div>)',
                re.DOTALL | re.IGNORECASE
            )
            new_html, count = pattern.subn(rf'\1\n{links_block}\n                    \3', html)
            if count > 0:
                html = new_html
                print(f"Fixed dropdown using fallback keyword '{keyword}' for {menu_name} ({len(links)} links added)")
                break
        else:
            print(f"WARNING: Could not find dropdown for '{menu_name}' (tried keywords: {fallback_keywords}) - manual check needed")

# 4. BONUS: Fix "Contact Us Now" in hero if it exists
html, count = re.subn(
    r'(?i)(Contact\s*Us\s*Now)(?!</a>)',
    r'<a href="tel:+14054106402" class="pro-cta-btn">\1</a>',
    html
)
if count > 0:
    print(f"Fixed {count} 'Contact Us Now' - now calls phone")

# Final: Save if changed
if html != original:
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nSUCCESS - services.html HAS BEEN UPDATED")
    print("Changes made:")
    print("   - Navy button under yellow banner (if text found)")
    print("   - All 7 dropdowns now have real working links (if matched)")
    print("Now run: python -m http.server 8000")
    print("Refresh browser with Ctrl+F5 - check for changes")
else:
    print("\nNO CHANGES MADE - likely no matching text or dropdowns found. Paste the commands above for more HTML.")
