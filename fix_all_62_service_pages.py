import os
import re

def fix_service_page_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        replacements = 0
        
        # Specific fixes (most common ones)
        specific_fixes = {
            '.html"': '"',  # removes .html from any /services/…html link in one sweep
        }
        
        for old, new in specific_fixes.items():
            new_content, count = re.subn(r'href="/services/[^"]+\.html"', lambda m: m.group(0).replace('.html"', '"'), content)
            content = new_content
            replacements += count
        
        # Catch-all regex for any remaining /services/xyz.html
        content, count = re.subn(r'href="/services/([^"/]+)\.html"', r'href="/services/\1"', content)
        replacements += count
        
        # Also fix absolute URLs if they exist
        content, count2 = re.subn(r'href="https?://[^/]+/services/([^"/]+)\.html"', r'href="/services/\1"', content)
        replacements += count2
        
        # Fix og:url meta tag if present
        content, count3 = re.subn(r'(og:url" content="[^"]+)/services/([^"/]+)\.html(")', r'\1/services/\2\3', content)
        replacements += count3
        
        if replacements > 0:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        
        return True, replacements
    
    except Exception as e:
        print(f"ERROR on {file_path}: {e}")
        return False, 0

def main():
    print("FIXING PRETTY URLS ON ALL 62 INDIVIDUAL SERVICE PAGES")
    print("=" * 70)
    
    # Full list of your 62 service pages (add/remove if you have slight name differences)
    service_pages = [
        "ada-compliant-showers.html", "grab-bars.html", "non-slip-flooring.html", "custom-ramps.html",
        "senior-safety.html", "bathroom-accessibility.html", "kitchen-renovations.html", "deck-construction.html",
        "siding-replacement.html", "home-remodeling.html", "basement-finishing.html", "window-doors.html",
        "fence-installation.html", "drywall-repair.html", "painting-services.html", "concrete-pouring.html",
        "driveway-installation.html", "patio-construction.html", "floor-refinishing.html", "hardwood-flooring.html",
        "concrete-repair.html", "custom-cabinets.html", "cabinet-refacing.html", "onyx-countertops.html",
        "kitchen-cabinetry.html", "custom-storage.html", "countertop-repair.html", "property-maintenance-routine.html",
        "emergency-repairs.html", "snow-removal.html", "seasonal-prep.html", "tree-trimming.html",
        "emergency-snow.html", "lawn-maintenance.html", "fertilization.html", "landscape-design.html",
        "seasonal-cleanup.html", "garden-maintenance.html", "tv-mounting-residential.html", "home-theater.html",
        "soundbar-setup.html", "cable-management.html", "smart-audio.html", "projector-install.html",
        "home-audio.html", "audio-visual.html", "bathroom-remodels.html", "fence-repair.html",
        "gutter-cleaning.html", "handyman-services.html", "pressure-washing.html", "room-additions.html",
        "stairlift-elevator-installation.html", "wheelchair-ramp-installation.html",
        # extra common ones just in case
        "tv-mounting.html", "lawn-care.html", "general-contractor.html", "accessibility-modifications.html",
        "safety-installations.html", "remodeling-services.html", "ada-ramps.html", "emergency-services.html"
    ]
    
    updated = 0
    total_fixed = 0
    
    for page in service_pages:
        if os.path.exists(page):
            print(f"Processing {page} ... ", end="")
            success, fixed = fix_service_page_links(page)
            if success and fixed > 0:
                print(f"Fixed {fixed} links")
                updated += 1
                total_fixed += fixed
            elif success:
                print("No changes needed")
            else:
                print("FAILED")
        else:
            print(f"NOT FOUND → {page}")
    
    print("=" * 70)
    print(f"DONE! Updated {updated} files • Total links fixed: {total_fixed}")
    
    if updated > 0:
        print("\nNOW DEPLOY:")
        print("git add .")
        print('git commit -m "fix: Remove .html from all 62 individual service pages (pretty URLs)"')
        print("git push origin main")
        print("\nAfter this, every single service page will use clean pretty URLs everywhere.")

if __name__ == "__main__":
    main()