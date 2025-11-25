# verify_redirects.py
import os

print("=== VERIFYING REDIRECTS AND LINKS ===")

# Check if grouped service pages exist
grouped_pages = [
    'services/accessibility-safety-solutions.html',
    'services/home-remodeling-renovation.html',
    'services/tv-home-theater-installation.html', 
    'services/property-maintenance-services.html',
    'services/handyman-repair-services.html'
]

print("\nChecking grouped service pages:")
for page in grouped_pages:
    if os.path.exists(page):
        print(f"✓ {page} - EXISTS")
    else:
        print(f"✗ {page} - MISSING")

# Check redirects file
print("\nChecking _redirects file:")
if os.path.exists('_redirects'):
    with open('_redirects', 'r') as f:
        redirect_count = len(f.readlines())
    print(f"✓ _redirects exists with {redirect_count} rules")
else:
    print("✗ _redirects file missing")

# Test a few key redirects
print("\nTesting key redirect mappings:")
test_redirects = {
    '/service-pages/ada-compliant-showers.html': '/services/accessibility-safety-solutions',
    '/service-pages/kitchen-renovations.html': '/services/home-remodeling-renovation',
    '/service-pages/tv-mounting-residential.html': '/services/tv-home-theater-installation',
    '/service-pages/lawn-maintenance.html': '/services/property-maintenance-services'
}

with open('_redirects', 'r') as f:
    redirect_content = f.read()

for old_url, new_url in test_redirects.items():
    if f"{old_url} {new_url}" in redirect_content:
        print(f"✓ {old_url} → {new_url}")
    else:
        print(f"✗ {old_url} → {new_url}")

print("\n=== VERIFICATION COMPLETE ===")