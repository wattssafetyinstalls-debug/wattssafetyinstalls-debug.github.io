# fix_complete_dropdown.py
import os
import re

def get_all_services():
    """Get ALL service pages that exist"""
    services = []
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    
    for file in service_files:
        service_slug = file.replace('.html', '')
        # Convert slug to readable title
        service_title = service_slug.replace('-', ' ').title()
        services.append((service_slug, service_title))
    
    return services

def create_complete_dropdown():
    """Create the full dropdown HTML with ALL services"""
    services = get_all_services()
    
    dropdown_html = ''
    for service_slug, service_title in services:
        dropdown_html += f'                        <li><a href="/{service_slug}">{service_title}</a></li>\n'
    
    return dropdown_html

def fix_dropdown_in_file(filename):
    """Replace the dropdown content in a file"""
    print(f"Fixing dropdown in {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the dropdown section
    dropdown_pattern = r'(<ul class="dropdown">)(.*?)(</ul>)'
    match = re.search(dropdown_pattern, content, re.DOTALL)
    
    if not match:
        print(f"  ERROR: Could not find dropdown in {filename}")
        return False
    
    full_dropdown = create_complete_dropdown()
    new_dropdown = match.group(1) + '\n' + full_dropdown + '                    ' + match.group(3)
    
    content = content.replace(match.group(0), new_dropdown)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  SUCCESS: Updated dropdown with {len(get_all_services())} services")
    return True

def main():
    print("FIXING COMPLETE DROPDOWN NAVIGATION...")
    print("This will add ALL your services to the dropdown menu")
    
    all_services = get_all_services()
    print(f"Found {len(all_services)} service pages:")
    
    for i, (slug, title) in enumerate(all_services[:10], 1):  # Show first 10
        print(f"  {i}. {title}")
    
    if len(all_services) > 10:
        print(f"  ... and {len(all_services) - 10} more services")
    
    # Fix main pages
    files_to_fix = ['index.html', 'services.html']
    success_count = 0
    
    for file in files_to_fix:
        if os.path.exists(file):
            if fix_dropdown_in_file(file):
                success_count += 1
        else:
            print(f"SKIPPING: {file} not found")
    
    # Also fix service pages navigation
    print("\nUpdating service page navigation...")
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    
    for service_file in service_files[:5]:  # Update first 5 service pages
        filepath = f"services/{service_file}"
        if fix_dropdown_in_file(filepath):
            success_count += 1
    
    print(f"\nCOMPLETE: Updated {success_count} files")
    print(f"Dropdown now shows ALL {len(all_services)} services")
    print("\nDeploy with:")
    print("git add index.html services.html services/*.html")
    print('git commit -m "Fix complete dropdown navigation with all services"')
    print("git push origin main")

if __name__ == "__main__":
    main()