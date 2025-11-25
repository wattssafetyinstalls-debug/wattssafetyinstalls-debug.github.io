# setup_pretty_urls_complete.py
import os
import re

def setup_complete_pretty_urls():
    print("SETTING UP COMPLETE PRETTY URL SYSTEM...")
    
    # List of all services with their pretty URLs
    services = {
        'driveway-installation': 'Driveway Installation',
        'concrete-pouring': 'Concrete Pouring',
        'hardwood-flooring': 'Hardwood Flooring',
        'garden-maintenance': 'Garden Maintenance',
        'landscape-design': 'Landscape Design',
        'painting-services': 'Painting Services',
        'snow-removal': 'Snow Removal',
        'custom-cabinets': 'Custom Cabinets',
        'deck-construction': 'Deck Construction',
        'home-remodeling': 'Home Remodeling',
        'bathroom-remodels': 'Bathroom Remodels',
        'kitchen-renovations': 'Kitchen Renovations',
        'fence-installation': 'Fence Installation',
        'patio-construction': 'Patio Construction',
        'window-doors': 'Window & Door Installation',
        'siding-replacement': 'Siding Replacement',
        'roofing-repair': 'Roofing Repair',
        'electrical-services': 'Electrical Services',
        'plumbing-services': 'Plumbing Services',
        'hvac-services': 'HVAC Services'
    }
    
    # 1. FIX INDEX.HTML
    print("\n1. UPDATING INDEX.HTML...")
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Remove any existing redirects script
    index_content = re.sub(r'<!-- Pretty URL Redirects -->.*?</script>', '', index_content, flags=re.DOTALL)
    
    # Add the JavaScript redirect system to index.html
    redirects_script = """
<!-- Pretty URL Redirects -->
<script>
const redirects = {
"""
    
    for service_slug, service_name in services.items():
        redirects_script += f"    '/{service_slug}': '/services/{service_slug}.html',\n"
    
    redirects_script += """};

// Handle pretty URL redirects
const currentPath = window.location.pathname;
if (redirects[currentPath]) {
    window.location.href = redirects[currentPath];
}
</script>
"""
    
    # Insert before closing head tag
    index_content = index_content.replace('</head>', redirects_script + '</head>')
    
    # Update dropdown links to use pretty URLs
    for service_slug, service_name in services.items():
        # Replace any existing links to this service
        old_patterns = [
            f'href="services.html#{service_slug}"',
            f'href="/services/{service_slug}.html"',
            f'href="services/{service_slug}.html"',
            f'href="#{service_slug}"'
        ]
        
        for old_pattern in old_patterns:
            if old_pattern in index_content:
                index_content = index_content.replace(old_pattern, f'href="/{service_slug}"')
                print(f"  Updated {service_name} link in index.html")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # 2. FIX SERVICES.HTML
    print("\n2. UPDATING SERVICES.HTML...")
    with open('services.html', 'r', encoding='utf-8') as f:
        services_content = f.read()
    
    # Remove any existing redirects script
    services_content = re.sub(r'<!-- Pretty URL Redirects -->.*?</script>', '', services_content, flags=re.DOTALL)
    
    # Add redirects script
    services_content = services_content.replace('</head>', redirects_script + '</head>')
    
    # Update dropdown links to use pretty URLs
    for service_slug, service_name in services.items():
        old_patterns = [
            f'href="services.html#{service_slug}"',
            f'href="/services/{service_slug}.html"',
            f'href="services/{service_slug}.html"',
            f'href="#{service_slug}"'
        ]
        
        for old_pattern in old_patterns:
            if old_pattern in services_content:
                services_content = services_content.replace(old_pattern, f'href="/{service_slug}"')
                print(f"  Updated {service_name} link in services.html")
    
    with open('services.html', 'w', encoding='utf-8') as f:
        f.write(services_content)
    
    # 3. ADD REDIRECTS TO ALL SERVICE PAGES
    print("\n3. UPDATING SERVICE PAGES WITH REDIRECTS...")
    
    for service_slug, service_name in services.items():
        service_file = f"services/{service_slug}.html"
        if os.path.exists(service_file):
            with open(service_file, 'r', encoding='utf-8') as f:
                service_content = f.read()
            
            # Remove any existing redirects script
            service_content = re.sub(r'<!-- Pretty URL Redirects -->.*?</script>', '', service_content, flags=re.DOTALL)
            
            # Add redirects script
            service_content = service_content.replace('</head>', redirects_script + '</head>')
            
            with open(service_file, 'w', encoding='utf-8') as f:
                f.write(service_content)
            
            print(f"  Added redirects to {service_name}")
    
    print("\n4. CREATING .HTACCESS FOR APACHE SERVERS (Backup)...")
    # Create .htaccess for Apache servers as backup
    htaccess_content = """# Pretty URL Rewrites
RewriteEngine On

# Redirect pretty URLs to actual HTML files
"""
    
    for service_slug in services.keys():
        htaccess_content += f"RewriteRule ^{service_slug}/?$ services/{service_slug}.html [L,QSA]\n"
    
    with open('.htaccess', 'w') as f:
        f.write(htaccess_content)
    
    print("COMPLETED! Pretty URL system is now set up.")
    print("\nTEST THESE PRETTY URLs:")
    for service_slug, service_name in list(services.items())[:5]:
        print(f"  https://wattsatpcontractor.com/{service_slug}")
    
    print("\nThe JavaScript redirect system will:")
    print("  - Intercept requests to pretty URLs like /driveway-installation")
    print("  - Redirect to the actual HTML file at /services/driveway-installation.html")
    print("  - Work on all pages (index, services, and individual service pages)")

if __name__ == "__main__":
    setup_complete_pretty_urls()
    
    print("\n" + "="*60)
    print("DEPLOYMENT COMMANDS:")
    print("git add index.html services.html services/*.html .htaccess")
    print('git commit -m "Implement complete pretty URL system with JavaScript redirects"')
    print("git push origin main")
    print("="*60)