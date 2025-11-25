# diagnose_current_state.py
import os
import re

def diagnose_current_state():
    print("DIAGNOSING CURRENT WEBSITE STATE...")
    
    # Check if key files exist
    print("1. CHECKING KEY FILES:")
    key_files = ['index.html', 'services.html']
    for file in key_files:
        if os.path.exists(file):
            print(f"   FOUND: {file}")
        else:
            print(f"   MISSING: {file}")
    
    # Check service pages
    print("\n2. CHECKING SERVICE PAGES:")
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    print(f"   Found {len(service_files)} service pages")
    
    # Check index.html structure
    print("\n3. CHECKING INDEX.HTML STRUCTURE:")
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Check for navigation
    if '<nav' in index_content:
        print("   FOUND: Navigation menu")
    else:
        print("   MISSING: Navigation menu")
    
    # Check for header image
    if 'header' in index_content.lower() or 'banner' in index_content.lower():
        print("   FOUND: Header/banner section")
    else:
        print("   MISSING: Header/banner section")
    
    # Check for dropdown
    if 'dropdown' in index_content:
        print("   FOUND: Dropdown menu")
    else:
        print("   MISSING: Dropdown menu")
    
    # Check services.html
    print("\n4. CHECKING SERVICES.HTML:")
    with open('services.html', 'r', encoding='utf-8') as f:
        services_content = f.read()
    
    # Check service cards/grid
    service_links = re.findall(r'href="[^"]*service[^"]*"', services_content)
    print(f"   Found {len(service_links)} service links")
    
    # Check a few service pages
    print("\n5. CHECKING SERVICE PAGE TEMPLATES:")
    sample_services = ['driveway-installation.html', 'concrete-pouring.html', 'hardwood-flooring.html']
    for service in sample_services:
        service_path = f"services/{service}"
        if os.path.exists(service_path):
            with open(service_path, 'r', encoding='utf-8') as f:
                service_content = f.read()
            
            has_header = '<header' in service_content or 'nav' in service_content
            has_footer = '<footer' in service_content
            has_return_link = 'services.html' in service_content
            
            print(f"   {service}:")
            print(f"     Header: {'YES' if has_header else 'NO'}")
            print(f"     Footer: {'YES' if has_footer else 'NO'}")
            print(f"     Return link: {'YES' if has_return_link else 'NO'}")

if __name__ == "__main__":
    diagnose_current_state()