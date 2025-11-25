# verify_design_integrity.py
import os
import re

def verify_design():
    print("VERIFYING PROFESSIONAL DESIGN INTEGRITY...")
    
    print("\n1. CHECKING MAIN PAGES:")
    main_pages = ['index.html', 'services.html']
    
    for page in main_pages:
        if os.path.exists(page):
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for design elements
            checks = {
                'CSS Styling': '<style>' in content or 'stylesheet' in content,
                'Navigation': 'nav' in content or 'navbar' in content,
                'Dropdown': 'dropdown' in content,
                'Footer': '<footer' in content,
                'Professional Layout': 'container' in content or 'main-content' in content
            }
            
            print(f"\n{page}:")
            for check, result in checks.items():
                status = "PASS" if result else "FAIL"
                print(f"  {check}: {status}")
    
    print("\n2. CHECKING SERVICE PAGES:")
    service_files = [f for f in os.listdir('services') if f.endswith('.html')[:3]]
    
    for service_file in service_files:
        filepath = f"services/{service_file}"
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Key design elements for service pages
        has_design = all([
            'service-title' in content,
            'service-description' in content,
            'back-button' in content or 'Back to Services' in content,
            '<footer' in content
        ])
        
        status = "PROFESSIONAL" if has_design else "NEEDS FIXING"
        print(f"  {service_file}: {status}")
    
    print("\n3. DROPDOWN FUNCTIONALITY:")
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    dropdown_links = re.findall(r'href="/([^"]*)"', content)
    service_links = [link for link in dropdown_links if any(service in link for service in ['driveway', 'concrete', 'hardwood'])]
    
    print(f"  Found {len(service_links)} service links in dropdown")
    print(f"  Dropdown working: {'YES' if len(service_links) > 5 else 'NO'}")

if __name__ == "__main__":
    verify_design()