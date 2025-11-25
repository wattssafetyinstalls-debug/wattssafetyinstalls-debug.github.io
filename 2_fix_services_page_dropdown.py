# 2_fix_services_page_dropdown.py
import re

def fix_services_page_dropdown():
    print("STEP 2: FIXING SERVICES PAGE DROPDOWN...")
    
    # Read services.html
    with open('services.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Services dropdown section
    dropdown_pattern = r'<li class="nav-dropdown">.*?<ul class="dropdown">(.*?)</ul>.*?</li>'
    dropdown_match = re.search(dropdown_pattern, content, re.DOTALL)
    
    if not dropdown_match:
        print("ERROR: Could not find dropdown menu structure in services.html")
        return
    
    current_dropdown = dropdown_match.group(1)
    
    # Define the services we want in the dropdown (same as index.html)
    services = [
        ('/driveway-installation', 'Driveway Installation'),
        ('/concrete-pouring', 'Concrete Pouring'),
        ('/hardwood-flooring', 'Hardwood Flooring'),
        ('/garden-maintenance', 'Garden Maintenance'),
        ('/landscape-design', 'Landscape Design'),
        ('/painting-services', 'Painting Services'),
        ('/snow-removal', 'Snow Removal'),
        ('/custom-cabinets', 'Custom Cabinets'),
        ('/deck-construction', 'Deck Construction'),
        ('/home-remodeling', 'Home Remodeling')
    ]
    
    # Build new dropdown content
    new_dropdown = ''
    for href, text in services:
        new_dropdown += f'    <li><a href="{href}">{text}</a></li>\n'
    
    # Replace the dropdown content
    new_content = content.replace(current_dropdown, new_dropdown)
    
    with open('services.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("SUCCESS: Services page dropdown menu fixed")

if __name__ == "__main__":
    fix_services_page_dropdown()