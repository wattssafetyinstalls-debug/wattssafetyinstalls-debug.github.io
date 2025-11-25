# update_redirects_fixed.py

# Map all old URLs to the new individual service pages
redirect_mapping = {
    # Accessibility & Safety
    '/service-pages/ada-compliant-showers.html': '/services/ada-compliant-showers-bathrooms',
    '/service-pages/grab-bars.html': '/services/grab-bar-installation',
    '/service-pages/non-slip-flooring.html': '/services/non-slip-flooring-solutions',
    '/service-pages/custom-ramps.html': '/services/wheelchair-ramp-installation',
    '/service-pages/senior-safety.html': '/services/stairlift-elevator-installation',
    
    # Home Remodeling
    '/service-pages/kitchen-renovations.html': '/services/kitchen-renovations',
    '/service-pages/bathroom-remodels.html': '/services/bathroom-remodels',
    '/service-pages/deck-construction.html': '/services/room-additions',
    '/service-pages/siding-replacement.html': '/services/flooring-installation',
    '/service-pages/home-remodeling.html': '/services/painting-drywall',
    '/service-pages/basement-finishing.html': '/services/room-additions',
    
    # TV & Audio Visual
    '/service-pages/tv-mounting-residential.html': '/services/tv-mounting',
    '/service-pages/home-theater.html': '/services/home-theater-installation',
    '/service-pages/soundbar-setup.html': '/services/sound-system-setup',
    '/service-pages/cable-management.html': '/services/cable-management',
    '/service-pages/smart-audio.html': '/services/sound-system-setup',
    '/service-pages/projector-install.html': '/services/home-theater-installation',
    
    # Property Maintenance
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

# Create the redirects file
with open('_redirects', 'w') as f:
    for old_url, new_url in redirect_mapping.items():
        f.write(f"{old_url} {new_url}\n")

print("Updated redirects for individual service pages")
print(f"Added {len(redirect_mapping)} redirect rules")