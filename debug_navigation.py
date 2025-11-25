# debug_navigation.py
import re

def debug_navigation():
    print("DEBUGGING NAVIGATION STRUCTURE...")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("1. FINDING NAVIGATION SECTIONS...")
    
    # Find all navigation-related sections
    nav_patterns = [
        r'<nav[^>]*>(.*?)</nav>',
        r'<ul[^>]*class="[^"]*nav[^"]*"[^>]*>(.*?)</ul>',
        r'<div[^>]*class="[^"]*nav[^"]*"[^>]*>(.*?)</div>',
        r'<li[^>]*class="[^"]*dropdown[^"]*"[^>]*>(.*?)</li>'
    ]
    
    for i, pattern in enumerate(nav_patterns):
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            print(f"\nFound navigation section (pattern {i+1}):")
            for match in matches[:2]:  # Show first 2 matches
                # Extract links from this section
                links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', match)
                if links:
                    print("Links in this section:")
                    for href, text in links[:5]:  # Show first 5 links
                        print(f"  '{text.strip()}' -> {href}")
    
    print("\n2. FINDING ALL SERVICE LINKS IN THE ENTIRE FILE...")
    all_links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', content)
    
    service_keywords = ['driveway', 'concrete', 'hardwood', 'garden', 'landscape', 'paint', 'snow', 'cabinet', 'deck', 'remodel']
    service_links = []
    
    for href, text in all_links:
        if any(keyword in text.lower() or keyword in href for keyword in service_keywords):
            service_links.append((href, text))
    
    print(f"Found {len(service_links)} service-related links:")
    for href, text in service_links:
        print(f"  '{text.strip()}' -> {href}")

if __name__ == "__main__":
    debug_navigation()