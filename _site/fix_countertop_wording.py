# fix_countertop_wording.py
import os

# Service pages that might have countertop references
service_pages = [
    "kitchen-renovations",
    "bathroom-remodels",
    "home-remodeling-renovation"  # if this grouped page exists
]

# Fix the countertop wording in each page
for slug in service_pages:
    page_path = f'services/{slug}.html'
    
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace "quartz and granite countertops" with "custom countertops"
        content = content.replace('quartz and granite countertops', 'custom countertops')
        content = content.replace('Quartz and granite countertops', 'Custom countertops')
        content = content.replace('quartz & granite countertops', 'custom countertops')
        
        # Also fix any other variations
        content = content.replace('granite countertops', 'custom countertops')
        content = content.replace('quartz countertops', 'custom countertops')
        
        # Write the updated content back
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated countertop wording: {page_path}")

print("Fixed all countertop references to say 'custom countertops'")