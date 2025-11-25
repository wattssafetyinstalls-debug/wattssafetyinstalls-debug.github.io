# find_remaining_direct_links_clean.py
import os
import re

def find_direct_links():
    print("CHECKING FOR REMAINING DIRECT HTML LINKS...")
    
    files_to_check = ['index.html', 'services.html']
    
    for filename in files_to_check:
        print(f"\nChecking {filename}:")
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find any remaining direct service HTML links
        direct_links = re.findall(r'href="[^"]*services/[^"]*\.html"', content)
        if direct_links:
            print(f"FOUND - {len(direct_links)} direct HTML links:")
            for link in direct_links[:5]:  # Show first 5
                print(f"  {link}")
        else:
            print("OK - No direct HTML links found")
        
        # Find anchor links
        anchor_links = re.findall(r'href="[^"#]*#[^"]*"', content)
        service_anchor_links = [link for link in anchor_links if any(service in link for service in ['driveway', 'concrete', 'hardwood', 'garden'])]
        if service_anchor_links:
            print(f"FOUND - {len(service_anchor_links)} anchor links:")
            for link in service_anchor_links[:3]:
                print(f"  {link}")
        else:
            print("OK - No service anchor links found")

if __name__ == "__main__":
    find_direct_links()