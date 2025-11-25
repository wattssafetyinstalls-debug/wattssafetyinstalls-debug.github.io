# verify_all_services_in_dropdown.py
import os
import re

def verify_all_services():
    print("VERIFYING ALL SERVICES ARE IN DROPDOWN...")
    
    # Get all services that should exist
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    expected_services = [f.replace('.html', '') for f in service_files]
    
    print(f"Expected {len(expected_services)} services in dropdown")
    
    # Check index.html dropdown
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all service links in dropdown
    dropdown_links = re.findall(r'href="/([^"]*)"', content)
    
    # Filter to only service pages
    found_services = [link for link in dropdown_links if link in expected_services]
    
    print(f"Found {len(found_services)} services in dropdown")
    
    # Check for missing services
    missing_services = [service for service in expected_services if service not in found_services]
    
    if missing_services:
        print(f"\nMISSING {len(missing_services)} SERVICES FROM DROPDOWN:")
        for service in missing_services[:10]:  # Show first 10 missing
            print(f"  - {service}")
        if len(missing_services) > 10:
            print(f"  ... and {len(missing_services) - 10} more")
    else:
        print("\nSUCCESS: All services are in the dropdown!")
    
    # Show some examples of services found
    print(f"\nSAMPLE OF SERVICES IN DROPDOWN ({len(found_services)} total):")
    for service in found_services[:15]:
        print(f"  ✓ {service.replace('-', ' ').title()}")
    if len(found_services) > 15:
        print(f"  ... and {len(found_services) - 15} more")

if __name__ == "__main__":
    verify_all_services()