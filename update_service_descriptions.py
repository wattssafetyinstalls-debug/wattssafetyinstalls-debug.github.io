# update_service_descriptions.py
import os

# Update the kitchen renovations description
kitchen_page = 'services/kitchen-renovations.html'

if os.path.exists(kitchen_page):
    with open(kitchen_page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the description
    old_description = "Complete kitchen remodeling services in Norfolk NE including cabinet installation, countertop replacement, and appliance setup. We create functional, beautiful kitchens."
    new_description = "Complete kitchen remodeling services in Norfolk NE including cabinet installation, custom countertops, and appliance setup. We create functional, beautiful kitchens."
    content = content.replace(old_description, new_description)
    
    # Update the details
    old_details = "Cabinet refacing or replacement, quartz and granite countertops, tile backsplashes, flooring installation, lighting upgrades, and appliance installation with full plumbing and electrical."
    new_details = "Cabinet refacing or replacement, custom countertops, tile backsplashes, flooring installation, lighting upgrades, and appliance installation with full plumbing and electrical."
    content = content.replace(old_details, new_details)
    
    with open(kitchen_page, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Updated kitchen renovations page with custom countertops")

# Also update any other pages that might reference countertops
other_pages = [
    "bathroom-remodels",
    "home-remodeling-renovation"
]

for slug in other_pages:
    page_path = f'services/{slug}.html'
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace any countertop references
        content = content.replace('quartz and granite', 'custom')
        content = content.replace('granite countertops', 'custom countertops')
        content = content.replace('quartz countertops', 'custom countertops')
        
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated: {page_path}")

print("All countertop references updated to 'custom countertops'")