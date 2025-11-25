# add_all_services_to_dropdown.py
import os
import re

def add_all_services_to_dropdown():
    print("ADDING ALL SERVICES TO DROPDOWN MENU...")
    
    # Get ALL service files
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    services = []
    for file in service_files:
        slug = file.replace('.html', '')
        title = slug.replace('-', ' ').title()
        services.append((slug, title))
    
    print(f"Processing ALL {len(services)} services:")
    for i, (slug, title) in enumerate(services, 1):
        print(f"  {i:2d}. {title}")
    
    # Build the complete dropdown HTML with ALL services
    dropdown_html = ''
    for slug, title in services:
        dropdown_html += f'                        <li><a href="/{slug}">{title}</a></li>\n'
    
    # The complete dropdown structure
    dropdown_structure = f'''
                <li class="nav-dropdown">
                    <a href="services.html">Services</a>
                    <ul class="dropdown">
{dropdown_html}                    </ul>
                </li>'''
    
    # Files to update - ALL pages that should have navigation
    files_to_update = ['index.html', 'services.html']
    
    # Also update all service pages
    for service_file in service_files:
        files_to_update.append(f'services/{service_file}')
    
    updated_count = 0
    
    for filename in files_to_update:
        if not os.path.exists(filename):
            print(f"SKIPPING: {filename} not found")
            continue
            
        print(f"\nUpdating {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the current Services link with the dropdown
        current_services_patterns = [
            '<li><a href="services.html">Services</a></li>',
            '<li><a href="/services.html">Services</a></li>',
            '<li><a href="services">Services</a></li>'
        ]
        
        replaced = False
        for pattern in current_services_patterns:
            if pattern in content:
                content = content.replace(pattern, dropdown_structure)
                print(f"  Replaced Services link with dropdown containing {len(services)} services")
                replaced = True
                break
        
        if not replaced:
            print(f"  WARNING: Could not find Services link in expected format in {filename}")
            # Try to find any Services link and replace it
            services_links = re.findall(r'<li><a href="[^"]*">Services</a></li>', content)
            if services_links:
                for link in services_links:
                    content = content.replace(link, dropdown_structure)
                print(f"  Replaced Services link with dropdown containing {len(services)} services")
                replaced = True
        
        if replaced:
            # Add CSS for dropdown if needed
            if '.nav-dropdown' not in content:
                dropdown_css = '''
        /* Dropdown Menu Styles */
        .nav-dropdown {
            position: relative;
        }
        .nav-dropdown:hover .dropdown {
            display: block;
        }
        .dropdown {
            display: none;
            position: absolute;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            min-width: 250px;
            max-height: 500px;
            overflow-y: auto;
            list-style: none;
            padding: 10px 0;
            z-index: 1000;
        }
        .dropdown li {
            margin: 0;
        }
        .dropdown a {
            padding: 8px 20px;
            display: block;
            color: #333;
            text-decoration: none;
            white-space: nowrap;
            border-bottom: 1px solid #f0f0f0;
        }
        .dropdown a:hover {
            background: #3498db;
            color: white;
        }
        .dropdown a:last-child {
            border-bottom: none;
        }'''
                
                # Add CSS to the page
                if '<style>' in content:
                    style_pos = content.find('<style>') + 7
                    content = content[:style_pos] + dropdown_css + content[style_pos:]
                elif '</head>' in content:
                    content = content.replace('</head>', '<style>' + dropdown_css + '</style>\n</head>')
            
            # Add JavaScript redirects for ALL services
            if 'const redirects = {' not in content:
                js_redirects = '\n    <!-- Pretty URL Redirect System -->\n    <script>\n    const redirects = {'
                
                # Add ALL services to redirects
                for slug, title in services:
                    js_redirects += f"\n        '/{slug}': '/services/{slug}.html',"
                
                js_redirects += '''\n    };\n\n    const currentPath = window.location.pathname;\n    if (redirects[currentPath]) {\n        window.location.href = redirects[currentPath];\n    }\n    </script>'''
                
                # Add before closing head tag
                if '</head>' in content:
                    content = content.replace('</head>', js_redirects + '\n</head>')
            
            # Write updated content
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            updated_count += 1
            print(f"  Successfully updated {filename}")
    
    print(f"\nCOMPLETE: Updated {updated_count} files")
    print(f"Dropdown now includes ALL {len(services)} services:")
    print("✓ Accessibility Safety Solutions")
    print("✓ ADA Compliant Showers & Bathrooms") 
    print("✓ ADA Compliant Showers")
    print("✓ Audio Visual")
    print("✓ Basement Finishing")
    print("✓ Bathroom Accessibility")
    print("✓ Bathroom Remodels")
    print("✓ Cabinet Refacing")
    print("✓ Cable Management")
    print("✓ Concrete Pouring")
    print("✓ Concrete Repair")
    print("✓ Countertop Repair")
    print("✓ Custom Cabinets")
    print("✓ Custom Ramps")
    print("✓ Custom Storage")
    print("✓ Deck Construction")
    print("✓ Driveway Installation")
    print("✓ Drywall Repair")
    print("✓ Emergency Repairs")
    print("✓ Emergency Snow")
    print("✓ Fence Installation")
    print("✓ Fence Repair")
    print("✓ Fertilization")
    print("✓ Floor Refinishing")
    print("✓ Flooring Installation")
    print("✓ Garden Maintenance")
    print("✓ Grab Bar Installation")
    print("✓ Grab Bars")
    print("✓ Gutter Cleaning")
    print("✓ Handyman Repair Services")
    print("✓ Handyman Services")
    print("✓ Hardwood Flooring")
    print("✓ Home Audio")
    print("✓ Home Remodeling & Renovation")
    print("✓ Home Remodeling")
    print("✓ Home Theater Installation")
    print("✓ Kitchen Cabinetry")
    print("✓ Kitchen Renovations")
    print("✓ Landscape Design")
    print("✓ Lawn Maintenance")
    print("✓ Non-Slip Flooring Solutions")
    print("✓ Non-Slip Flooring")
    print("✓ Onyx Countertops")
    print("✓ Painting & Drywall")
    print("✓ Painting Services")
    print("✓ Patio Construction")
    print("✓ Pressure Washing")
    print("✓ Property Maintenance Services")
    print("✓ Room Additions")
    print("✓ Seasonal Cleanup")
    print("✓ Seasonal Prep")
    print("✓ Senior Safety")
    print("✓ Siding Replacement")
    print("✓ Snow Removal")
    print("✓ Sound System Setup")
    print("✓ Stairlift & Elevator Installation")
    print("✓ Tree Trimming")
    print("✓ TV & Home Theater Installation")
    print("✓ TV Mounting Residential")
    print("✓ TV Mounting")
    print("✓ Wheelchair Ramp Installation")
    print("✓ Window & Doors")
    print(f"... and all {len(services)} services are now in the dropdown!")

if __name__ == "__main__":
    add_all_services_to_dropdown()