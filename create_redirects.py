# create_redirects.py
import os

# Map pretty URLs to actual service pages
redirect_map = {
    # TV & Audio Services - Pretty URLs
    "tv-mounting": "service-pages/tv-mounting-service.html",
    "home-theater": "service-pages/home-theater-installation.html",
    "audio-visual": "service-pages/audio-visual-setup.html", 
    "projector-installation": "service-pages/projector-mounting.html",
    
    # Bathroom Services - Pretty URLs
    "bathroom-remodeling": "service-pages/bathroom-remodeling.html",
    "walk-in-showers": "service-pages/walk-in-shower-installation.html",
    "accessible-bathrooms": "service-pages/bathroom-accessibility-modifications.html",
    
    # Kitchen Services - Pretty URLs
    "kitchen-remodeling": "service-pages/kitchen-remodeling.html",
    "cabinet-installation": "service-pages/cabinet-installation.html",
    "countertop-installation": "service-pages/countertop-installation.html",
    
    # Accessibility Services - Pretty URLs  
    "ada-ramps": "service-pages/ada-ramp-installation.html",
    "wheelchair-ramps": "service-pages/wheelchair-ramp-construction.html",
    "grab-bars": "service-pages/grab-bar-installation.html",
    "stairlifts": "service-pages/stairlift-installation.html",
    
    # Maintenance Services - Pretty URLs
    "snow-removal": "service-pages/snow-removal-service.html",
    "lawn-care": "service-pages/lawn-maintenance.html",
    "landscaping": "service-pages/landscape-design.html",
    "emergency-repairs": "service-pages/emergency-repair-services.html",
    
    # Handyman Services - Pretty URLs
    "handyman-services": "service-pages/handyman-services-hourly.html",
    "small-repairs": "service-pages/small-home-repairs.html"
}

# Create .htaccess for Apache servers
htaccess_content = "RewriteEngine On\n"
for pretty_url, actual_file in redirect_map.items():
    htaccess_content += f"RewriteRule ^{pretty_url}/?$ {actual_file} [L,QSA]\n"

with open('.htaccess', 'w') as f:
    f.write(htaccess_content)

# Create _redirects for Netlify
redirects_content = ""
for pretty_url, actual_file in redirect_map.items():
    redirects_content += f"/{pretty_url}    /{actual_file}    200\n"

with open('_redirects', 'w') as f:
    f.write(redirects_content)

print("Created .htaccess and _redirects files!")
print("Now use these pretty URLs in your main page:")
for pretty_url in redirect_map.keys():
    print(f"  /{pretty_url}")