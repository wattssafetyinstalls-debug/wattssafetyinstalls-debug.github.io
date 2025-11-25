# verify_dropdown_links.py
import os
import re

def verify_dropdown_links():
    print("VERIFYING DROPDOWN LINKS USE PRETTY URLS...")
    
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
        'home-remodeling'
    ]
    
    # Check main pages
    main_pages = ['index.html', 'services.html']
    
    for page in main_pages:
        print(f"\nChecking {page}:")
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        correct_links = 0
        incorrect_links = 0
        
        for service in services:
            # Look for this service in dropdown
            patterns = [
                f'href="/{service}"',
                f'href="[^"]*{service}[^"]*"'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if match == f'href="/{service}"':
                        correct_links += 1
                    else:
                        incorrect_links += 1
                        print(f"  INCORRECT: {match} should be: href=\"/{service}\"")
        
        print(f"  Correct links: {correct_links}")
        print(f"  Incorrect links: {incorrect_links}")
    
    print("\nOVERALL STATUS:")
    if incorrect_links == 0:
        print("ALL DROPDOWN LINKS ARE USING PRETTY URLS!")
    else:
        print(f"Found {incorrect_links} links that need to be fixed")

if __name__ == "__main__":
    verify_dropdown_links()