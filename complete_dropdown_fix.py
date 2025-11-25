# complete_dropdown_fix.py
import os
import re

def complete_fix():
    print("COMPLETE DROPDOWN FIX - ADDING ALL 62 SERVICES...")
    
    # Get ALL services
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    services = []
    for file in service_files:
        slug = file.replace('.html', '')
        title = slug.replace('-', ' ').title()
        services.append((slug, title))
    
    print(f"Adding ALL {len(services)} services to dropdown...")
    
    # Build the complete dropdown HTML
    dropdown_items = ''
    for slug, title in services:
        dropdown_items += f'                        <li><a href="/{slug}">{title}</a></li>\n'
    
    # The complete dropdown structure
    dropdown_html = f'''                <li class="nav-dropdown">
                    <a href="services.html">Services</a>
                    <ul class="dropdown">
{dropdown_items}                    </ul>
                </li>'''
    
    # Fix both main pages
    for filename in ['index.html', 'services.html']:
        print(f"Fixing {filename}...")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove any existing dropdown and replace with complete one
        content = re.sub(
            r'<li class="nav-dropdown">.*?</ul>\s*</li>',
            dropdown_html,
            content,
            flags=re.DOTALL
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Updated {filename} with {len(services)} services")
    
    print(f"\nSUCCESS: Both pages now have dropdown with ALL {len(services)} services")

if __name__ == "__main__":
    complete_fix()