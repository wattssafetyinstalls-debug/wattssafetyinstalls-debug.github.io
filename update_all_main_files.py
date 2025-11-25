# update_all_main_files.py
import os
import re

def update_main_files():
    # List all main HTML files
    main_files = [
        "index.html",
        "services.html", 
        "service_area.html",
        "referrals.html",
        "contact.html",
        "sitemap.html"
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
    
    for file_name in main_files:
        if os.path.exists(file_name):
            print(f"\nUpdating: {file_name}")
            
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply countertop replacements
            old_content = content
            for old, new in countertop_replacements.items():
                content = content.replace(old, new)
            
            # Fix any broken service links
            content = re.sub(r'href="services\.html#', 'href="#', content)
            content = re.sub(r'href="services/services/', 'href="services/', content)
            
            # Ensure proper navigation links
            content = content.replace('href="/"', 'href="/"')
            content = content.replace('href="/services"', 'href="/services"')
            content = content.replace('href="/service-area"', 'href="service_area.html"')
            content = content.replace('href="/referrals"', 'href="/referrals"')
            content = content.replace('href="/contact"', 'href="/contact"')
            
            # Write updated content back
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Check if changes were made
            if old_content != content:
                print(f"OK - Updated: {file_name}")
            else:
                print(f"NO CHANGE - No changes needed: {file_name}")
                
        else:
            print(f"FAIL - File not found: {file_name}")

# Run the updates
update_main_files()
print("\nAll main files updated!")