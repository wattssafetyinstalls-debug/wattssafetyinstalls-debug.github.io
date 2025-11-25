# fix_all_python_scripts.py
import os
import re

def fix_python_scripts():
    print("🛠️ UPDATING ALL PYTHON SCRIPTS FOR CONSISTENT URLS...")
    
    python_scripts = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                python_scripts.append(os.path.join(root, file))
    
    url_replacements = {
        # Replace file paths with pretty URLs in Python scripts
        'href="/ada-compliant-showers"': 'href="/ada-compliant-showers"',
        'href="/grab-bar-installation"': 'href="/grab-bar-installation"',
        'href="/wheelchair-ramps"': 'href="/wheelchair-ramps"',
        'href="/stairlift-installation"': 'href="/stairlift-installation"',
        'href="/non-slip-flooring"': 'href="/non-slip-flooring"',
        'href="/kitchen-renovations"': 'href="/kitchen-renovations"',
        'href="/bathroom-remodels"': 'href="/bathroom-remodels"',
        'href="/room-additions"': 'href="/room-additions"',
        'href="/flooring-installation"': 'href="/flooring-installation"',
        'href="/painting-services"': 'href="/painting-services"',
        'href="/tv-mounting"': 'href="/tv-mounting"',
        'href="/home-theater-installation"': 'href="/home-theater-installation"',
        'href="/sound-system-setup"': 'href="/sound-system-setup"',
        'href="/cable-management"': 'href="/cable-management"',
        'href="/lawn-maintenance"': 'href="/lawn-maintenance"',
        'href="/pressure-washing"': 'href="/pressure-washing"',
        'href="/gutter-cleaning"': 'href="/gutter-cleaning"',
        'href="/fence-repair"': 'href="/fence-repair"',
        'href="/handyman-services"': 'href="/handyman-services"',
        
        # Navigation links
        'href="/"': 'href="/"',
        'href="/services"': 'href="/services"',
        'href="/service-area"': 'href="/service-area"',
        'href="/about"': 'href="/about"',
        'href="/referrals"': 'href="/referrals"',
        'href="/contact"': 'href="/contact"',
        'href="/sitemap"': 'href="/sitemap"',
        
        # File extensions
        'href="/"': 'href="/"',
        'href="/services"': 'href="/services"',
        'href="/service-area"': 'href="/service-area"',
        'href="/about"': 'href="/about"',
        'href="/referrals"': 'href="/referrals"',
        'href="/contact"': 'href="/contact"',
        'href="/sitemap"': 'href="/sitemap"'
    }
    
    for script_path in python_scripts:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        old_content = content
        
        # Apply all URL replacements
        for old_url, new_url in url_replacements.items():
            content = content.replace(old_url, new_url)
            # Also handle single quotes
            content = content.replace(old_url.replace('"', "'"), new_url.replace('"', "'"))
        
        if old_content != content:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ UPDATED: {script_path}")
        else:
            print(f"✅ ALREADY OK: {script_path}")

fix_python_scripts()