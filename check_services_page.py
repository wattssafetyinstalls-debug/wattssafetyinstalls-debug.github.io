# check_services_page.py
import re

def check_services_page():
    print("CHECKING SERVICES.HTML PAGE STRUCTURE...")
    
    with open('services.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for service cards or service listings
    print("1. LOOKING FOR SERVICE CARDS/SECTIONS...")
    
    # Common patterns for service listings
    patterns = [
        r'<div[^>]*class="[^"]*service[^"]*"[^>]*>(.*?)</div>',
        r'<section[^>]*class="[^"]*service[^"]*"[^>]*>(.*?)</section>',
        r'<div[^>]*class="[^"]*card[^"]*"[^>]*>(.*?)</div>',
        r'<li[^>]*class="[^"]*service[^"]*"[^>]*>(.*?)</li>'
    ]
    
    service_sections = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            service_sections.extend(matches)
    
    print(f"Found {len(service_sections)} potential service sections")
    
    # Extract links from service sections
    service_links = []
    for section in service_sections:
        links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', section)
        service_links.extend(links)
    
    if service_links:
        print("Service links found in sections:")
        for href, text in service_links:
            print(f"  '{text.strip()}' -> {href}")
    else:
        print("No service links found in sections")
    
    # Look for any grid or container that might hold services
    print("\n2. LOOKING FOR SERVICE GRIDS/CONTAINERS...")
    grid_patterns = [
        r'<div[^>]*class="[^"]*grid[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*container[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*row[^"]*"[^>]*>(.*?)</div>'
    ]
    
    for pattern in grid_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            print(f"Found grid/container with {len(matches)} sections")
            # Check if these contain service links
            for i, match in enumerate(matches[:2]):  # Check first 2
                links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', match)
                service_links_in_grid = [link for link in links if any(service in link[0] or any(keyword in link[1].lower() for keyword in ['driveway', 'concrete', 'hardwood']) for service in ['driveway', 'concrete', 'hardwood'])]
                if service_links_in_grid:
                    print(f"  Grid {i+1} contains service links:")
                    for href, text in service_links_in_grid:
                        print(f"    '{text.strip()}' -> {href}")

if __name__ == "__main__":
    check_services_page()