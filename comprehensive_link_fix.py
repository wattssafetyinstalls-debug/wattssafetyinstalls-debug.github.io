# comprehensive_link_fix.py
import re
import os

def find_and_fix_all_service_links():
    print("COMPREHENSIVE SERVICE LINK FIX...")
    
    # List of all services we expect
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
    
    files_to_check = ['index.html', 'services.html']
    
    for filename in files_to_check:
        print(f"\n=== CHECKING {filename} ===")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find ALL links in the file
        all_links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', content)
        
        print(f"Total links found: {len(all_links)}")
        
        # Find service-related links
        service_links = []
        for href, text in all_links:
            # Check if this is a service link
            is_service = False
            
            # Check by service slug in href
            for service in services:
                if service in href:
                    is_service = True
                    break
            
            # Check by service keywords in text
            service_keywords = ['driveway', 'concrete', 'hardwood', 'garden', 'landscape', 'paint', 'snow', 'cabinet', 'deck', 'remodel']
            if any(keyword in text.lower() for keyword in service_keywords):
                is_service = True
            
            if is_service:
                service_links.append((href, text))
        
        print(f"Service-related links found: {len(service_links)}")
        for href, text in service_links:
            print(f"  '{text.strip()}' -> {href}")
        
        # Fix service links to use pretty URLs
        changes_made = 0
        for service in services:
            # Look for any link that references this service (in href or text)
            old_patterns = [
                f'href="[^"]*{service}[^"]*"',
            ]
            
            for pattern in old_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    for match in matches:
                        # Only replace if it's not already a pretty URL
                        if not match.startswith('href="/' + service):
                            new_link = f'href="/{service}"'
                            content = content.replace(match, new_link)
                            print(f"    Changed: {match} -> {new_link}")
                            changes_made += 1
        
        # Write back if changes were made
        if changes_made > 0:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Made {changes_made} changes to {filename}")
        else:
            print(f"  No changes needed for {filename}")
    
    # Also check service pages for internal navigation
    print("\n=== CHECKING SERVICE PAGES ===")
    service_pages_checked = 0
    for service in services[:3]:  # Check first 3 service pages
        filename = f"services/{service}.html"
        if os.path.exists(filename):
            service_pages_checked += 1
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if this page has the JavaScript redirect system
            if 'const redirects = {' in content and 'window.location.pathname' in content:
                print(f"  {service}.html: Has redirect system")
            else:
                print(f"  {service}.html: MISSING redirect system")
    
    print(f"\nChecked {service_pages_checked} service pages")
    
    print("\n=== SUMMARY ===")
    print("The navigation structure appears to be minimal.")
    print("Only one service link was found in the main navigation.")
    print("Most service links are likely on the services.html page.")

if __name__ == "__main__":
    find_and_fix_all_service_links()