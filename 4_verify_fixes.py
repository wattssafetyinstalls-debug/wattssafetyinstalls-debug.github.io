# 4_verify_fixes.py
import re
import os

def verify_fixes():
    print("STEP 4: VERIFYING ALL FIXES...")
    
    # Check 1: Dropdown structure in index.html
    print("\n1. CHECKING INDEX.HTML DROPDOWN:")
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    dropdown_links = re.findall(r'<a href="/([^"]*)">([^<]*)</a>', index_content)
    service_links = [link for link in dropdown_links if any(service in link[0] for service in ['driveway', 'concrete', 'hardwood'])]
    
    print(f"Found {len(service_links)} service links in dropdown")
    for href, text in service_links:
        print(f"  ✓ {text} -> /{href}")
    
    # Check 2: Services page dropdown
    print("\n2. CHECKING SERVICES.HTML DROPDOWN:")
    with open('services.html', 'r', encoding='utf-8') as f:
        services_content = f.read()
    
    dropdown_links_services = re.findall(r'<a href="/([^"]*)">([^<]*)</a>', services_content)
    service_links_services = [link for link in dropdown_links_services if any(service in link[0] for service in ['driveway', 'concrete', 'hardwood'])]
    
    print(f"Found {len(service_links_services)} service links in services.html dropdown")
    
    # Check 3: Service pages exist
    print("\n3. CHECKING SERVICE PAGES EXIST:")
    required_pages = ['driveway-installation', 'concrete-pouring', 'hardwood-flooring']
    for page in required_pages:
        if os.path.exists(f'services/{page}.html'):
            print(f"  ✓ services/{page}.html exists")
        else:
            print(f"  ✗ services/{page}.html MISSING")
    
    print("\n4. GIT STATUS:")
    print("Run these commands to deploy:")
    print("git add index.html services.html")
    print('git commit -m "Fix dropdown menu structure and navigation"')
    print("git push origin main")

if __name__ == "__main__":
    verify_fixes()