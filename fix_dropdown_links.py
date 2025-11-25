# fix_dropdown_links.py
import re

def fix_dropdown_links():
    print("FIXING DROPDOWN LINKS TO USE PRETTY URLS...")
    
    # List of services and their pretty URLs
    services = [
        'driveway-installation',
        'concrete-pouring',
        'hardwood-flooring',
        'garden-maintenance',
        'landscape-design',
        'painting-services',
        'snow-removal',
        'custom-cabinets',
        'deck-construction',
        'home-remodeling',
        'bathroom-remodels',
        'kitchen-renovations',
        'fence-installation',
        'patio-construction',
        'window-doors',
        'siding-replacement',
        'roofing-repair',
        'electrical-services',
        'plumbing-services',
        'hvac-services'
    ]
    
    # Fix index.html
    print("\n1. FIXING INDEX.HTML DROPDOWN LINKS...")
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    changes_made_index = 0
    for service in services:
        # Look for any link that contains the service slug and replace with pretty URL
        pattern = f'href="[^"]*{service}[^"]*"'
        matches = re.findall(pattern, index_content)
        for match in matches:
            # Only replace if it's not already a pretty URL
            if not match.startswith('href="/' + service):
                new_link = f'href="/{service}"'
                index_content = index_content.replace(match, new_link)
                changes_made_index += 1
                print(f"   Changed {match} to {new_link}")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"   Made {changes_made_index} changes in index.html")
    
    # Fix services.html
    print("\n2. FIXING SERVICES.HTML DROPDOWN LINKS...")
    with open('services.html', 'r', encoding='utf-8') as f:
        services_content = f.read()
    
    changes_made_services = 0
    for service in services:
        pattern = f'href="[^"]*{service}[^"]*"'
        matches = re.findall(pattern, services_content)
        for match in matches:
            if not match.startswith('href="/' + service):
                new_link = f'href="/{service}"'
                services_content = services_content.replace(match, new_link)
                changes_made_services += 1
                print(f"   Changed {match} to {new_link}")
    
    with open('services.html', 'w', encoding='utf-8') as f:
        f.write(services_content)
    print(f"   Made {changes_made_services} changes in services.html")
    
    print("\nDONE! Dropdown links now use pretty URLs.")

if __name__ == "__main__":
    fix_dropdown_links()