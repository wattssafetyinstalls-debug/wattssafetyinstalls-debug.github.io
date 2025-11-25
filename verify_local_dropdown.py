# verify_local_dropdown.py
import re

def verify_local():
    print("VERIFYING DROPDOWN ON LOCAL FILES...")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for dropdown elements
    has_dropdown = 'nav-dropdown' in content
    has_dropdown_class = 'dropdown' in content
    has_css = '.nav-dropdown' in content
    has_js = 'const redirects = {' in content
    
    print("index.html checks:")
    print(f"  nav-dropdown class: {'YES' if has_dropdown else 'NO'}")
    print(f"  dropdown menu: {'YES' if has_dropdown_class else 'NO'}")
    print(f"  CSS styles: {'YES' if has_css else 'NO'}")
    print(f"  JavaScript redirects: {'YES' if has_js else 'NO'}")
    
    # Count service links
    service_links = re.findall(r'href="/([^"]*)"', content)
    service_count = len([link for link in service_links if 'services' not in link and '#' not in link and link != ''])
    
    print(f"  Service links found: {service_count}")
    
    if service_count > 50:
        print("  SUCCESS: Dropdown should be working with all services!")
    else:
        print("  WARNING: Dropdown may not have all services")

if __name__ == "__main__":
    verify_local()