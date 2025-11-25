# check_navigation_structure.py
import re

def check_navigation():
    print("CHECKING CURRENT NAVIGATION STRUCTURE...")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("1. LOOKING FOR NAVIGATION...")
    
    # Find all navigation elements
    nav_elements = re.findall(r'<nav[^>]*>.*?</nav>', content, re.DOTALL | re.IGNORECASE)
    print(f"Found {len(nav_elements)} navigation elements")
    
    for i, nav in enumerate(nav_elements):
        print(f"\nNavigation {i+1}:")
        # Extract all links from this navigation
        links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', nav)
        print(f"  Contains {len(links)} links:")
        for href, text in links:
            print(f"    '{text.strip()}' -> {href}")
    
    print("\n2. LOOKING FOR DROPDOWNS...")
    dropdowns = re.findall(r'<ul[^>]*class="[^"]*dropdown[^"]*"[^>]*>.*?</ul>', content, re.DOTALL | re.IGNORECASE)
    print(f"Found {len(dropdowns)} dropdown menus")
    
    for i, dropdown in enumerate(dropdowns):
        print(f"\nDropdown {i+1}:")
        # Count items in dropdown
        items = re.findall(r'<li>', dropdown)
        print(f"  Contains {len(items)} items")
        # Show first few items
        links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', dropdown)
        for href, text in links[:5]:  # Show first 5
            print(f"    '{text.strip()}' -> {href}")
        if len(links) > 5:
            print(f"    ... and {len(links) - 5} more items")
    
    print("\n3. LOOKING FOR SERVICES IN NAVIGATION...")
    all_links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', content)
    service_links = []
    
    for href, text in all_links:
        if any(service in href or service in text.lower() for service in ['driveway', 'concrete', 'hardwood', 'garden', 'landscape', 'paint', 'snow', 'cabinet', 'deck', 'remodel']):
            service_links.append((href, text))
    
    print(f"Found {len(service_links)} service-related links in entire page:")
    for href, text in service_links:
        print(f"  '{text.strip()}' -> {href}")

if __name__ == "__main__":
    check_navigation()