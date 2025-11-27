import os
import re

def fix_dropdown_links(file_path):
    """Fix ALL dropdown service links to use pretty URLs"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix ALL service dropdown links - remove .html from service URLs
        dropdown_links_to_fix = {
            # Accessibility & Safety Services
            'href="/services/ada-compliant-showers.html"': 'href="/services/ada-compliant-showers"',
            'href="/services/grab-bars.html"': 'href="/services/grab-bars"',
            'href="/services/non-slip-flooring.html"': 'href="/services/non-slip-flooring"',
            'href="/services/custom-ramps.html"': 'href="/services/custom-ramps"',
            'href="/services/senior-safety.html"': 'href="/services/senior-safety"',
            'href="/services/bathroom-accessibility.html"': 'href="/services/bathroom-accessibility"',
            
            # Home Remodeling Services
            'href="/services/kitchen-renovations.html"': 'href="/services/kitchen-renovations"',
            'href="/services/deck-construction.html"': 'href="/services/deck-construction"',
            'href="/services/siding-replacement.html"': 'href="/services/siding-replacement"',
            'href="/services/home-remodeling.html"': 'href="/services/home-remodeling"',
            'href="/services/basement-finishing.html"': 'href="/services/basement-finishing"',
            'href="/services/window-doors.html"': 'href="/services/window-doors"',
            'href="/services/fence-installation.html"': 'href="/services/fence-installation"',
            'href="/services/drywall-repair.html"': 'href="/services/drywall-repair"',
            'href="/services/painting-services.html"': 'href="/services/painting-services"',
            
            # Concrete & Flooring Services
            'href="/services/concrete-pouring.html"': 'href="/services/concrete-pouring"',
            'href="/services/driveway-installation.html"': 'href="/services/driveway-installation"',
            'href="/services/patio-construction.html"': 'href="/services/patio-construction"',
            'href="/services/floor-refinishing.html"': 'href="/services/floor-refinishing"',
            'href="/services/hardwood-flooring.html"': 'href="/services/hardwood-flooring"',
            'href="/services/concrete-repair.html"': 'href="/services/concrete-repair"',
            
            # Cabinets & Countertops
            'href="/services/custom-cabinets.html"': 'href="/services/custom-cabinets"',
            'href="/services/cabinet-refacing.html"': 'href="/services/cabinet-refacing"',
            'href="/services/onyx-countertops.html"': 'href="/services/onyx-countertops"',
            'href="/services/kitchen-cabinetry.html"': 'href="/services/kitchen-cabinetry"',
            'href="/services/custom-storage.html"': 'href="/services/custom-storage"',
            'href="/services/countertop-repair.html"': 'href="/services/countertop-repair"',
            
            # Property Maintenance
            'href="/services/property-maintenance-routine.html"': 'href="/services/property-maintenance-routine"',
            'href="/services/emergency-repairs.html"': 'href="/services/emergency-repairs"',
            'href="/services/snow-removal.html"': 'href="/services/snow-removal"',
            'href="/services/seasonal-prep.html"': 'href="/services/seasonal-prep"',
            'href="/services/tree-trimming.html"': 'href="/services/tree-trimming"',
            'href="/services/emergency-snow.html"': 'href="/services/emergency-snow"',
            
            # Lawn & Landscape
            'href="/services/lawn-maintenance.html"': 'href="/services/lawn-maintenance"',
            'href="/services/fertilization.html"': 'href="/services/fertilization"',
            'href="/services/landscape-design.html"': 'href="/services/landscape-design"',
            'href="/services/seasonal-cleanup.html"': 'href="/services/seasonal-cleanup"',
            'href="/services/garden-maintenance.html"': 'href="/services/garden-maintenance"',
            
            # TV & Audio Visual Services
            'href="/services/tv-mounting-residential.html"': 'href="/services/tv-mounting-residential"',
            'href="/services/home-theater.html"': 'href="/services/home-theater"',
            'href="/services/soundbar-setup.html"': 'href="/services/soundbar-setup"',
            'href="/services/cable-management.html"': 'href="/services/cable-management"',
            'href="/services/smart-audio.html"': 'href="/services/smart-audio"',
            'href="/services/projector-install.html"': 'href="/services/projector-install"',
            'href="/services/home-audio.html"': 'href="/services/home-audio"',
            'href="/services/audio-visual.html"': 'href="/services/audio-visual"',
            
            # Additional Services
            'href="/services/bathroom-remodels.html"': 'href="/services/bathroom-remodels"',
            'href="/services/fence-repair.html"': 'href="/services/fence-repair"',
            'href="/services/gutter-cleaning.html"': 'href="/services/gutter-cleaning"',
            'href="/services/handyman-services.html"': 'href="/services/handyman-services"',
            'href="/services/pressure-washing.html"': 'href="/services/pressure-washing"',
            'href="/services/room-additions.html"': 'href="/services/room-additions"',
            'href="/services/stairlift-elevator-installation.html"': 'href="/services/stairlift-elevator-installation"',
            'href="/services/wheelchair-ramp-installation.html"': 'href="/services/wheelchair-ramp-installation"',
        }
        
        replacements = 0
        for old_link, new_link in dropdown_links_to_fix.items():
            if old_link in content:
                content = content.replace(old_link, new_link)
                replacements += 1
        
        # Also fix any other service links with a catch-all pattern
        service_link_pattern = r'href="/services/([^"]+)\.html"'
        
        def replace_service_links(match):
            service_name = match.group(1)
            return f'href="/services/{service_name}"'
        
        content = re.sub(service_link_pattern, replace_service_links, content)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True, replacements
        
    except Exception as e:
        print(f"ERROR: {file_path} - {str(e)}")
        return False, 0

def main():
    print("FIXING ALL DROPDOWN SERVICE LINKS")
    print("=" * 60)
    
    # Files that contain service card dropdowns
    files_to_fix = ["services.html", "index.html"]
    updated_count = 0
    total_replacements = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"Processing: {file_path}")
            success, replacements = fix_dropdown_links(file_path)
            if success:
                if replacements > 0:
                    print(f"SUCCESS: {file_path} - {replacements} dropdown links fixed")
                    updated_count += 1
                    total_replacements += replacements
                else:
                    print(f"NO CHANGES: {file_path} - dropdown links already correct")
            else:
                print(f"FAILED: {file_path}")
        else:
            print(f"NOT FOUND: {file_path}")
    
    print("-" * 60)
    print("RESULTS:")
    print(f"  Files updated: {updated_count}")
    print(f"  Total dropdown links fixed: {total_replacements}")
    
    if updated_count > 0:
        print("\nSUCCESS! All dropdown service links now point to pretty URLs")
        print("Deploy now:")
        print("git add services.html index.html")
        print('git commit -m "fix: Update ALL dropdown service links to use pretty URLs"')
        print("git push origin main")
    else:
        print("No dropdown links needed fixing")

if __name__ == "__main__":
    main()