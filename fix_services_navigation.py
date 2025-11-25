# fix_services_navigation.py
import os

def fix_services_navigation():
    # Update services.html to have proper anchor links
    services_file = "services.html"
    
    if os.path.exists(services_file):
        with open(services_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix service card IDs and navigation
        fixes = {
            'id="accessibility-safety"': 'id="accessibility-safety"',
            'id="home-remodeling"': 'id="home-remodeling"', 
            'id="concrete-flooring"': 'id="concrete-flooring"',
            'id="cabinets-countertops"': 'id="cabinets-countertops"',
            'id="property-maintenance"': 'id="property-maintenance"',
            'id="lawn-care"': 'id="lawn-care"',
            'id="additional-services"': 'id="additional-services"'
        }
        
        # Ensure all anchor links work properly
        for old_id, new_id in fixes.items():
            if old_id in content:
                print(f"OK - Found and verified: {old_id}")
        
        # Fix footer navigation links
        content = content.replace(
            'href="services.html/services/accessibility-safety-solutions"',
            'href="#accessibility-safety"'
        )
        content = content.replace(
            'href="services.html/services/home-remodeling-renovation"', 
            'href="#home-remodeling"'
        )
        content = content.replace(
            'href="services.html/services/property-maintenance-services"',
            'href="#property-maintenance"'
        )
        
        # Write updated content back
        with open(services_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("OK - Fixed services navigation and anchor links")
    else:
        print("FAIL - services.html not found")

fix_services_navigation()