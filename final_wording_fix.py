# final_wording_fix.py
import os

# List all service pages
all_service_pages = [
    "ada-compliant-showers-bathrooms",
    "grab-bar-installation", 
    "wheelchair-ramp-installation",
    "stairlift-elevator-installation",
    "non-slip-flooring-solutions",
    "kitchen-renovations",
    "bathroom-remodels",
    "room-additions",
    "flooring-installation",
    "painting-drywall",
    "tv-mounting",
    "home-theater-installation",
    "sound-system-setup",
    "cable-management",
    "lawn-maintenance",
    "pressure-washing",
    "gutter-cleaning",
    "fence-repair",
    "handyman-services"
]

# Countertop replacement mapping
countertop_replacements = {
    'quartz and granite countertops': 'custom countertops',
    'Quartz and granite countertops': 'Custom countertops', 
    'quartz & granite countertops': 'custom countertops',
    'granite countertops': 'custom countertops',
    'quartz countertops': 'custom countertops',
    'marble countertops': 'custom countertops',
    'stone countertops': 'custom countertops'
}

for slug in all_service_pages:
    page_path = f'services/{slug}.html'
    
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply all countertop replacements
        for old, new in countertop_replacements.items():
            content = content.replace(old, new)
        
        # Write the updated content back
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Checked and updated: {page_path}")

print("All service pages now use 'custom countertops' instead of specific material names")