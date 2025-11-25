# fix_all_dropdown_links.py
import os
import re

def fix_dropdown_links_in_file(filename):
    """Fix dropdown links in a single file to use pretty URLs"""
    print(f"Checking {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the services and their pretty URLs
    services = [
        ('driveway-installation', 'Driveway Installation'),
        ('concrete-pouring', 'Concrete Pouring'),
        ('hardwood-flooring', 'Hardwood Flooring'),
        ('garden-maintenance', 'Garden Maintenance'),
        ('landscape-design', 'Landscape Design'),
        ('painting-services', 'Painting Services'),
        ('snow-removal', 'Snow Removal'),
        ('custom-cabinets', 'Custom Cabinets'),
        ('deck-construction', 'Deck Construction'),
        ('home-remodeling', 'Home Remodeling')
    ]
    
    changes_made = 0
    
    # Fix each service link in the dropdown
    for service_slug, service_name in services:
        # Pattern to find this service in dropdown (various possible formats)
        patterns = [
            f'<a href="[^"]*{service_slug}[^"]*">[^<]*{service_name}[^<]*</a>',
            f'<a href="[^"]*{service_slug}[^"]*">[^<]*</a>',
            f'href="[^"]*{service_slug}[^"]*"'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Only replace if it's not already a pretty URL
                if not match.startswith('href="/' + service_slug):
                    new_link = f'href="/{service_slug}">{service_name}</a>'
                    # Extract just the href part to replace
                    old_href = re.search(r'href="[^"]*"', match).group()
                    new_full_link = match.replace(old_href, f'href="/{service_slug}"')
                    content = content.replace(match, new_full_link)
                    print(f"  Fixed: {service_name} -> /{service_slug}")
                    changes_made += 1
                    break  # Move to next service after fixing this one
    
    # Write back if changes were made
    if changes_made > 0:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Made {changes_made} changes to {filename}")
    
    return changes_made

def fix_all_dropdown_links():
    print("FIXING DROPDOWN LINKS ACROSS ALL PAGES...")
    
    # Files to check (all HTML files that might have navigation)
    files_to_check = []
    
    # Add root level HTML files
    for file in os.listdir('.'):
        if file.endswith('.html'):
            files_to_check.append(file)
    
    # Add service pages
    for file in os.listdir('services'):
        if file.endswith('.html'):
            files_to_check.append(f'services/{file}')
    
    total_changes = 0
    files_updated = 0
    
    for file in files_to_check:
        if os.path.exists(file):
            changes = fix_dropdown_links_in_file(file)
            if changes > 0:
                total_changes += changes
                files_updated += 1
    
    print(f"\nSUMMARY:")
    print(f"Updated {files_updated} files")
    print(f"Made {total_changes} total changes")
    print(f"All dropdown links now use pretty URLs")

if __name__ == "__main__":
    fix_all_dropdown_links()