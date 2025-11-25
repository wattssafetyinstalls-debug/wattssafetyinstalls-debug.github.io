# fix_pretty_urls_clean.py
import os
import re

def check_current_setup():
    print("CHECKING CURRENT PRETTY URL SETUP...")
    
    # Read index.html to see what's actually there
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("1. CHECKING DROPDOWN LINKS IN INDEX.HTML:")
    # Look for any links that might be service links
    all_links = re.findall(r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>', content)
    
    service_links = []
    for href, text in all_links:
        if any(service in text.lower() for service in ['driveway', 'concrete', 'hardwood', 'garden', 'landscape', 'paint', 'snow', 'cabinet', 'deck', 'remodel']):
            service_links.append((href, text))
    
    print(f"Found {len(service_links)} potential service links:")
    for href, text in service_links:
        print(f"  '{text}' -> {href}")
    
    print("\n2. CHECKING JAVASCRIPT REDIRECT SYSTEM:")
    if 'redirects = {' in content:
        print("FOUND redirects object")
        # Extract redirects
        redirects_match = re.search(r'redirects\s*=\s*{([^}]+)}', content)
        if redirects_match:
            redirects_text = redirects_match.group(1)
            print("Redirects found:")
            redirects = re.findall(r"'/([^']+)':\s*'([^']+)'", redirects_text)
            for pretty_url, actual_url in redirects:
                print(f"  /{pretty_url} -> {actual_url}")
    else:
        print("NO redirects object found!")

def fix_pretty_urls():
    print("\nFIXING PRETTY URL SETUP...")
    
    # Read current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the correct pretty URLs for each service
    service_urls = {
        'driveway-installation': '/driveway-installation',
        'concrete-pouring': '/concrete-pouring', 
        'hardwood-flooring': '/hardwood-flooring',
        'garden-maintenance': '/garden-maintenance',
        'landscape-design': '/landscape-design',
        'painting-services': '/painting-services',
        'snow-removal': '/snow-removal',
        'custom-cabinets': '/custom-cabinets',
        'deck-construction': '/deck-construction',
        'home-remodeling': '/home-remodeling'
    }
    
    # First, let's see what links currently exist and replace them
    changes_made = 0
    for service_slug, pretty_url in service_urls.items():
        # Look for any existing links to this service
        old_pattern = f'href="[^"]*{service_slug}[^"]*"'
        matches = re.findall(old_pattern, content)
        if matches:
            for match in matches:
                new_link = f'href="{pretty_url}"'
                content = content.replace(match, new_link)
                print(f"Changed {match} to {new_link}")
                changes_made += 1
    
    # If no changes were made, the links might be using different format
    if changes_made == 0:
        print("No direct service links found. Checking for pretty URLs that need redirects...")
    
    # Ensure JavaScript redirect system exists and is correct
    if 'redirects = {' not in content:
        print("Adding missing redirects system...")
        redirects_script = """
<!-- Pretty URL Redirects -->
<script>
const redirects = {
    '/driveway-installation': '/services/driveway-installation.html',
    '/concrete-pouring': '/services/concrete-pouring.html',
    '/hardwood-flooring': '/services/hardwood-flooring.html',
    '/garden-maintenance': '/services/garden-maintenance.html', 
    '/landscape-design': '/services/landscape-design.html',
    '/painting-services': '/services/painting-services.html',
    '/snow-removal': '/services/snow-removal.html',
    '/custom-cabinets': '/services/custom-cabinets.html',
    '/deck-construction': '/services/deck-construction.html',
    '/home-remodeling': '/services/home-remodeling.html'
};

const currentPath = window.location.pathname;
if (redirects[currentPath]) {
    window.location.href = redirects[currentPath];
}
</script>
"""
        # Add before closing head tag
        content = content.replace('</head>', redirects_script + '\n</head>')
        print("Added redirects script to index.html")
    
    # Write fixed content
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed index.html pretty URLs")
    
    # Also fix services.html
    with open('services.html', 'r', encoding='utf-8') as f:
        services_content = f.read()
    
    changes_made_services = 0
    for service_slug, pretty_url in service_urls.items():
        old_pattern = f'href="[^"]*{service_slug}[^"]*"'
        matches = re.findall(old_pattern, services_content)
        if matches:
            for match in matches:
                new_link = f'href="{pretty_url}"'
                services_content = services_content.replace(match, new_link)
                changes_made_services += 1
    
    with open('services.html', 'w', encoding='utf-8') as f:
        f.write(services_content)
    
    print(f"Fixed services.html pretty URLs ({changes_made_services} changes)")

if __name__ == "__main__":
    check_current_setup()
    
    response = input("\nApply pretty URL fixes? (y/n): ")
    if response.lower() == 'y':
        fix_pretty_urls()
        
        print("\nDEPLOYMENT COMMANDS:")
        print("git add index.html services.html")
        print('git commit -m "Fix pretty URL system - correct service links and JavaScript redirects"')
        print("git push origin main")
        print("\nTest these pretty URLs after deployment:")
        print("https://wattsatpcontractor.com/driveway-installation")
        print("https://wattsatpcontractor.com/concrete-pouring")
    else:
        print("No changes made.")