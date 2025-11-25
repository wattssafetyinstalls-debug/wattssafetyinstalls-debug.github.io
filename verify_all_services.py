# verify_all_services.py
import os
import re

def verify_all():
    print("VERIFYING ALL SERVICES IN DROPDOWN...")
    
    # Get all service files
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    expected_count = len(service_files)
    
    print(f"Expected services: {expected_count}")
    
    # Check index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count service links in dropdown
    dropdown_match = re.search(r'<ul class="dropdown">(.*?)</ul>', content, re.DOTALL)
    if dropdown_match:
        dropdown_content = dropdown_match.group(1)
        service_links = re.findall(r'href="/([^"]*)"', dropdown_content)
        found_count = len(service_links)
        
        print(f"Services in dropdown: {found_count}")
        
        if found_count == expected_count:
            print("SUCCESS: All services are in the dropdown!")
        else:
            print(f"PROBLEM: Missing {expected_count - found_count} services")
            
        # Show first 10 services as sample
        print("Sample of services in dropdown:")
        for link in service_links[:10]:
            print(f"  - {link.replace('-', ' ').title()}")
    else:
        print("ERROR: Could not find dropdown in index.html")

if __name__ == "__main__":
    verify_all()