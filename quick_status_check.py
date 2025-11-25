# quick_status_check.py
import os
import re

def quick_status():
    print("QUICK STATUS CHECK - CURRENT STATE...")
    
    # Check if main pages have dropdown
    main_pages = ['index.html', 'services.html']
    
    for page in main_pages:
        if os.path.exists(page):
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for dropdown elements
            has_dropdown = 'nav-dropdown' in content
            has_services_list = 'dropdown' in content
            
            # Count service links
            service_links = re.findall(r'href="/([^"]*)"', content)
            service_count = len([link for link in service_links if any(s in link for s in ['driveway', 'concrete', 'hardwood'])])
            
            print(f"{page}:")
            print(f"  Dropdown structure: {'YES' if has_dropdown else 'NO'}")
            print(f"  Services in dropdown: {service_count}")
    
    # Check if we have uncommitted changes
    print("\nGIT STATUS:")
    import subprocess
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print("There are uncommitted changes:")
        print(result.stdout)
    else:
        print("No uncommitted changes")
    
    print("\nRECOMMENDATION:")
    print("Run the final fix script below, then commit and push ALL changes")

if __name__ == "__main__":
    quick_status()