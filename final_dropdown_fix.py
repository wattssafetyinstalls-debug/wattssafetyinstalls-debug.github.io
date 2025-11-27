import os
import re

def fix_all_dropdown_links_final(file_path):
    """FINAL FIX: Ensure ALL dropdown service links use pretty URLs"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix ALL service dropdown links - comprehensive list
        dropdown_fixes = {
            # Fix the remaining .html links in dropdowns
            'href="/services/ada-compliant-showers.html"': 'href="/services/ada-compliant-showers"',
            'href="/services/grab-bars.html"': 'href="/services/grab-bars"',
            'href="/services/non-slip-flooring.html"': 'href="/services/non-slip-flooring"',
            'href="/services/custom-ramps.html"': 'href="/services/custom-ramps"',
            'href="/services/senior-safety.html"': 'href="/services/senior-safety"',
            'href="/services/bathroom-accessibility.html"': 'href="/services/bathroom-accessibility"',
            'href="/services/basement-finishing.html"': 'href="/services/basement-finishing"',
            'href="/services/drywall-repair.html"': 'href="/services/drywall-repair"',
            'href="/services/floor-refinishing.html"': 'href="/services/floor-refinishing"',
            'href="/services/concrete-repair.html"': 'href="/services/concrete-repair"',
            'href="/services/countertop-repair.html"': 'href="/services/countertop-repair"',
            'href="/services/property-maintenance-routine.html"': 'href="/services/property-maintenance-routine"',
            'href="/services/emergency-repairs.html"': 'href="/services/emergency-repairs"',
            'href="/services/seasonal-prep.html"': 'href="/services/seasonal-prep"',
            'href="/services/emergency-snow.html"': 'href="/services/emergency-snow"',
            'href="/services/lawn-maintenance.html"': 'href="/services/lawn-maintenance"',
            'href="/services/seasonal-cleanup.html"': 'href="/services/seasonal-cleanup"',
            'href="/services/garden-maintenance.html"': 'href="/services/garden-maintenance"',
            'href="/services/tv-mounting-residential.html"': 'href="/services/tv-mounting-residential"',
            'href="/services/soundbar-setup.html"': 'href="/services/soundbar-setup"',
            'href="/services/cable-management.html"': 'href="/services/cable-management"',
            'href="/services/smart-audio.html"': 'href="/services/smart-audio"',
            'href="/services/projector-install.html"': 'href="/services/projector-install"',
            'href="/services/home-audio.html"': 'href="/services/home-audio"',
            'href="/services/audio-visual.html"': 'href="/services/audio-visual"',
        }
        
        replacements = 0
        for old_link, new_link in dropdown_fixes.items():
            if old_link in content:
                content = content.replace(old_link, new_link)
                replacements += 1
        
        # Also fix any absolute URLs that still have .html
        absolute_url_pattern = r'href="https://wattsatpcontractor\.com/services/([^"]+)\.html"'
        
        def replace_absolute_links(match):
            service_name = match.group(1)
            return f'href="/services/{service_name}"'
        
        content = re.sub(absolute_url_pattern, replace_absolute_links, content)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True, replacements
        
    except Exception as e:
        print(f"ERROR: {file_path} - {str(e)}")
        return False, 0

def main():
    print("FINAL DROPDOWN LINK FIX")
    print("=" * 60)
    
    files_to_fix = ["services.html"]
    updated_count = 0
    total_replacements = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"Processing: {file_path}")
            success, replacements = fix_all_dropdown_links_final(file_path)
            if success:
                if replacements > 0:
                    print(f"SUCCESS: {file_path} - {replacements} dropdown links fixed")
                    updated_count += 1
                    total_replacements += replacements
                else:
                    print(f"NO CHANGES: {file_path} - all dropdown links already correct")
            else:
                print(f"FAILED: {file_path}")
        else:
            print(f"NOT FOUND: {file_path}")
    
    print("-" * 60)
    print("FINAL RESULTS:")
    print(f"  Files updated: {updated_count}")
    print(f"  Total dropdown links fixed: {total_replacements}")
    
    if updated_count > 0:
        print("\nFINAL FIX COMPLETE! All dropdown links now use pretty URLs.")
        print("This should be the last fix needed.")
        print("\nDeploy now:")
        print("git add services.html")
        print('git commit -m "fix: Final dropdown links - all service links use pretty URLs"')
        print("git push origin main")
    else:
        print("All dropdown links were already correct!")

if __name__ == "__main__":
    main()