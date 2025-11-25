# diagnose_github_pages_issue.py
import os
import requests

def diagnose_github_pages():
    print("DIAGNOSING GITHUB PAGES ISSUE...")
    
    # Check if service files exist locally
    print("\n1. CHECKING LOCAL SERVICE FILES:")
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    print(f"Found {len(service_files)} service pages locally")
    
    # Check a few specific service files
    test_files = ['driveway-installation.html', 'concrete-pouring.html', 'hardwood-flooring.html']
    for file in test_files:
        if os.path.exists(f'services/{file}'):
            print(f"  OK: services/{file} exists locally")
        else:
            print(f"  MISSING: services/{file} not found locally")
    
    # Check index.html for correct links
    print("\n2. CHECKING INDEX.HTML LINKS:")
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Look for service links in index.html
    import re
    service_links = re.findall(r'href="[^"]*service[^"]*"', index_content)
    print(f"Found {len(service_links)} service-related links in index.html")
    
    for link in service_links[:5]:  # Show first 5
        print(f"  Link: {link}")
    
    # Check if links are using correct case and paths
    print("\n3. CHECKING LINK PATHS:")
    # Look for service page links specifically
    service_page_links = re.findall(r'href="[^"]*services/[^"]*\.html"', index_content)
    for link in service_page_links[:5]:
        print(f"  Service link: {link}")
    
    # Test a few live URLs
    print("\n4. TESTING LIVE URLS (this may take a moment)...")
    base_url = "https://wattsatpcontractor.com"
    test_urls = [
        "/",
        "/services.html", 
        "/services/driveway-installation.html",
        "/services/concrete-pouring.html"
    ]
    
    for url in test_urls:
        full_url = base_url + url
        try:
            response = requests.get(full_url, timeout=10)
            status = "LIVE" if response.status_code == 200 else f"BROKEN ({response.status_code})"
            print(f"  {full_url} - {status}")
        except Exception as e:
            print(f"  {full_url} - ERROR: {e}")
    
    print("\n5. COMMON GITHUB PAGES FIXES:")
    print("   - Ensure all file names are lowercase")
    print("   - Use relative paths like '../services.html' not '/services.html'")
    print("   - Wait 5-10 minutes after deployment for GitHub Pages to update")
    print("   - Clear browser cache or test in incognito mode")
    print("   - Check GitHub repository settings for Pages configuration")

def fix_github_pages_links():
    print("\nAPPLYING GITHUB PAGES FIXES...")
    
    # Fix index.html links
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix service page links to use correct relative paths
    old_links = [
        'href="/services/driveway-installation.html"',
        'href="/services/concrete-pouring.html"',
        'href="/services/hardwood-flooring.html"'
    ]
    
    new_links = [
        'href="services/driveway-installation.html"',
        'href="services/concrete-pouring.html"', 
        'href="services/hardwood-flooring.html"'
    ]
    
    for old, new in zip(old_links, new_links):
        if old in content:
            content = content.replace(old, new)
            print(f"Fixed: {old} -> {new}")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Fix services.html links
    with open('services.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in zip(old_links, new_links):
        if old in content:
            content = content.replace(old, new)
            print(f"Fixed: {old} -> {new}")
    
    with open('services.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("All links fixed for GitHub Pages deployment")

if __name__ == "__main__":
    diagnose_github_pages()
    
    # Ask if user wants to apply fixes
    response = input("\nApply GitHub Pages link fixes? (y/n): ")
    if response.lower() == 'y':
        fix_github_pages_links()
        print("\nNow run these Git commands to deploy fixes:")
        print("git add .")
        print('git commit -m "Fix GitHub Pages links - use relative paths"')
        print("git push origin main")