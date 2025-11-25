# verify_dropdown_simple.py
import os
import re

def verify_dropdown():
    print("VERIFYING DROPDOWN...")
    
    # Get all services
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    expected_services = [f.replace('.html', '') for f in service_files]
    
    print(f"Expected {len(expected_services)} services in dropdown")
    
    # Check index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find services in dropdown
    dropdown_links = re.findall(r'href="/([^"]*)"', content)
    found_services = [link for link in dropdown_links if link in expected_services]
    
    print(f"Found {len(found_services)} services in dropdown")
    
    if len(found_services) == len(expected_services):
        print("SUCCESS: All services are in the dropdown!")
    else:
        print(f"PROBLEM: Missing {len(expected_services) - len(found_services)} services from dropdown")
    
    # Check if dropdown CSS exists
    if '.nav-dropdown' in content:
        print("Dropdown CSS: FOUND")
    else:
        print("Dropdown CSS: MISSING")
    
    # Check if JavaScript redirects exist
    if 'const redirects = {' in content:
        print("JavaScript redirects: FOUND")
    else:
        print("JavaScript redirects: MISSING")

if __name__ == "__main__":
    verify_dropdown()