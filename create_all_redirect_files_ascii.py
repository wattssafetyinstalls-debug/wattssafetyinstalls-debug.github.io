# create_all_redirect_files_ascii.py
import os

def create_redirect_files():
    print("CREATING PRETTY URL REDIRECT FILES...")
    
    redirect_pairs = {
        # Main pages
        "index": "index.html",
        "services": "services.html", 
        "service-area": "service-area.html",
        "about": "about.html",
        "referrals": "referrals.html",
        "contact": "contact.html",
        "sitemap": "sitemap.html",
        
        # Service pages
        "ada-compliant-showers": "services/ada-compliant-showers-bathrooms.html",
        "grab-bar-installation": "services/grab-bar-installation.html",
        "wheelchair-ramps": "services/wheelchair-ramp-installation.html",
        "stairlift-installation": "services/stairlift-elevator-installation.html",
        "non-slip-flooring": "services/non-slip-flooring-solutions.html",
        "kitchen-renovations": "services/kitchen-renovations.html",
        "bathroom-remodels": "services/bathroom-remodels.html",
        "room-additions": "services/room-additions.html",
        "flooring-installation": "services/flooring-installation.html",
        "painting-services": "services/painting-drywall.html",
        "tv-mounting": "services/tv-mounting.html",
        "home-theater-installation": "services/home-theater-installation.html",
        "sound-system-setup": "services/sound-system-setup.html",
        "cable-management": "services/cable-management.html",
        "lawn-maintenance": "services/lawn-maintenance.html",
        "pressure-washing": "services/pressure-washing.html",
        "gutter-cleaning": "services/gutter-cleaning.html",
        "fence-repair": "services/fence-repair.html",
        "handyman-services": "services/handyman-services.html"
    }
    
    for pretty_url, target_file in redirect_pairs.items():
        if os.path.exists(target_file):
            redirect_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=/{target_file}">
    <link rel="canonical" href="https://wattsatpcontractor.com/{target_file}">
    <title>Redirecting to {pretty_url.replace('-', ' ').title()}</title>
    <script>
        window.location.href = "/{target_file}";
    </script>
</head>
<body>
    <p>Redirecting to <a href="/{target_file}">{pretty_url.replace('-', ' ').title()}</a>...</p>
</body>
</html>"""
            
            with open(f"{pretty_url}.html", 'w', encoding='utf-8') as f:
                f.write(redirect_html)
            print(f"CREATED: {pretty_url}.html -> {target_file}")
        else:
            print(f"TARGET MISSING: {target_file}")

create_redirect_files()