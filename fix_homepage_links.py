# fix_homepage_links.py

# Read the current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the URL mapping from old to new
url_mapping = {
    '/service-pages/ada-compliant-showers.html': '/services/ada-compliant-showers',
    '/service-pages/grab-bars.html': '/services/grab-bar-installation',
    '/service-pages/non-slip-flooring.html': '/services/non-slip-flooring',
    '/service-pages/custom-ramps.html': '/services/wheelchair-ramp-installation',
    '/service-pages/senior-safety.html': '/services/stairlift-elevator-installation',
    
    '/service-pages/kitchen-renovations.html': '/services/kitchen-renovations',
    '/service-pages/bathroom-remodels.html': '/services/bathroom-remodels',
    '/service-pages/deck-construction.html': '/services/room-additions',
    '/service-pages/siding-replacement.html': '/services/flooring-installation',
    '/service-pages/home-remodeling.html': '/services/painting-drywall',
    '/service-pages/basement-finishing.html': '/services/room-additions',
    
    '/service-pages/tv-mounting-residential.html': '/services/tv-mounting',
    '/service-pages/home-theater.html': '/services/home-theater-installation',
    '/service-pages/soundbar-setup.html': '/services/sound-system-setup',
    '/service-pages/cable-management.html': '/services/cable-management',
    '/service-pages/smart-audio.html': '/services/sound-system-setup',
    '/service-pages/projector-install.html': '/services/home-theater-installation',
    
    '/service-pages/property-maintenance-routine.html': '/services/handyman-services',
    '/service-pages/emergency-repairs.html': '/services/handyman-services',
    '/service-pages/snow-removal.html': '/services/lawn-maintenance',
    '/service-pages/seasonal-prep.html': '/services/lawn-maintenance',
    '/service-pages/tree-trimming.html': '/services/handyman-services',
    '/service-pages/emergency-snow.html': '/services/lawn-maintenance',
    '/service-pages/lawn-maintenance.html': '/services/lawn-maintenance',
    '/service-pages/fertilization.html': '/services/lawn-maintenance',
    '/service-pages/landscape-design.html': '/services/lawn-maintenance',
    '/service-pages/seasonal-cleanup.html': '/services/lawn-maintenance',
    '/service-pages/garden-maintenance.html': '/services/lawn-maintenance'
}

# Replace all the old URLs with new pretty URLs
for old_url, new_url in url_mapping.items():
    content = content.replace(old_url, new_url)

# Write the updated content back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated homepage with pretty URLs in service dropdowns")
print("All service links now point to: /services/service-name")