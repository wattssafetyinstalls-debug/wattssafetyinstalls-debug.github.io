#!/usr/bin/env python3
import re

print("FINAL POLISH - FIXING DROPDOWNS & REMOVING DUPLICATES\n")

with open("services.html", "r", encoding="utf-8") as f:
    html = f.read()

original = html

# 1. REMOVE the duplicate service grid at the bottom
if 'services-grid' in html:
    # Find and remove the entire services-grid section
    grid_pattern = r'<section[^>]*class="[^"]*services-grid-section[^"]*"[^>]*>.*?</section>'
    html = re.sub(grid_pattern, '', html, flags=re.DOTALL)
    print("REMOVED duplicate service grid at bottom")

# 2. UPDATE ALL dropdown menus with complete service links
dropdown_updates = {
    "Accessibility & Safety": [
        ("ADA Compliant Showers", "/services/ada-compliant-showers.html"),
        ("Grab Bars Installation", "/services/grab-bars.html"), 
        ("Non-Slip Flooring", "/services/non-slip-flooring.html"),
        ("Wheelchair Ramps", "/services/custom-ramps.html"),
        ("Senior Safety", "/services/senior-safety.html"),
        ("Bathroom Accessibility", "/services/bathroom-accessibility.html")
    ],
    "Home Remodeling": [
        ("Kitchen Renovations", "/kitchen-renovations"),
        ("Bathroom Remodels", "/home-remodeling"),
        ("Basement Finishing", "/services/basement-finishing.html"),
        ("Deck Construction", "/deck-construction"),
        ("Room Additions", "/room-additions"),
        ("Painting Services", "/painting-services")
    ],
    "TV & Home Theater": [
        ("TV Mounting", "/services/tv-mounting-residential.html"),
        ("Home Theater", "/services/home-theater.html"),
        ("Sound Systems", "/services/sound-system-setup.html"),
        ("Smart Audio", "/services/smart-audio.html"),
        ("Cable Management", "/services/cable-management.html")
    ],
    "Property Maintenance": [
        ("Emergency Repairs", "/services/emergency-repairs.html"),
        ("Snow Removal", "/snow-removal"),
        ("Tree Trimming", "/services/tree-trimming.html"),
        ("Seasonal Prep", "/services/seasonal-prep.html"),
        ("Gutter Cleaning", "/services/gutter-cleaning.html")
    ],
    "Lawn & Landscape": [
        ("Lawn Maintenance", "/services/lawn-maintenance.html"),
        ("Landscape Design", "/landscape-design"),
        ("Fertilization", "/services/fertilization.html"),
        ("Seasonal Cleanup", "/services/seasonal-cleanup.html"),
        ("Garden Maintenance", "/garden-maintenance")
    ],
    "Concrete & Flooring": [
        ("Concrete Pouring", "/concrete-pouring"),
        ("Driveways", "/driveway-installation"),
        ("Hardwood Flooring", "/hardwood-flooring"),
        ("Floor Refinishing", "/services/floor-refinishing.html"),
        ("Patio Construction", "/patio-construction")
    ],
    "Cabinets & Countertops": [
        ("Custom Cabinets", "/custom-cabinets"),
        ("Cabinet Refacing", "/services/cabinet-refacing.html"),
        ("Countertops", "/services/onyx-countertops.html"),
        ("Kitchen Cabinetry", "/services/kitchen-cabinetry.html"),
        ("Custom Storage", "/services/custom-storage.html")
    ]
}

# Update each dropdown
for service_name, links in dropdown_updates.items():
    # Build the new dropdown content
    new_dropdown = '\n'
    for text, url in links:
        new_dropdown += f'                                <a href="{url}">{text}</a>\n'
    
    # Find and replace the dropdown for this service
    pattern = rf'<button[^>]*>[^<]*{re.escape(service_name)}[^<]*</button>\s*<div[^>]*dropdown[^>]*>.*?</div>'
    replacement = rf'<button class="dropdown-toggle">View Services <i class="fas fa-chevron-down"></i></button>\n                            <div class="dropdown">{new_dropdown}                            </div>'
    
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    print(f"UPDATED dropdown: {service_name}")

# 3. Add CSS to make dropdowns scrollable if they're too tall
dropdown_css = '''
    <style>
    /* Make dropdowns scrollable */
    .dropdown {
        max-height: 300px;
        overflow-y: auto;
        scrollbar-width: thin;
    }
    
    .dropdown::-webkit-scrollbar {
        width: 6px;
    }
    
    .dropdown::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .dropdown::-webkit-scrollbar-thumb {
        background: var(--teal);
        border-radius: 3px;
    }
    
    .dropdown::-webkit-scrollbar-thumb:hover {
        background: var(--navy);
    }
    </style>
'''

if '.dropdown::-webkit-scrollbar' not in html:
    html = html.replace('</head>', dropdown_css + '\n</head>')
    print("ADDED scrollable dropdown CSS")

# Save the file
if html != original:
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nPOLISHING COMPLETE!")
    print(" Removed duplicate service grid")
    print(" Updated ALL dropdowns with complete service links") 
    print(" Added scrollable dropdowns for long menus")
    print("\nRun: python -m http.server 8000")
    print("Refresh with Ctrl+F5")
else:
    print("No changes needed")