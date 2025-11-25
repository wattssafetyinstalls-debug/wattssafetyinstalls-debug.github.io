# fix_all_services_dropdown_final.py
import os
import re

def fix_all_services_dropdown():
    print("FIXING DROPDOWN TO INCLUDE ALL SERVICES...")
    
    # Get ALL service files
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    services = []
    for file in service_files:
        slug = file.replace('.html', '')
        title = slug.replace('-', ' ').title()
        services.append((slug, title))
    
    print(f"Processing ALL {len(services)} services")
    
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
    
    # First, let's check what the actual navigation looks like in index.html
    print("\n1. ANALYZING CURRENT NAVIGATION...")
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Find the navigation section
    nav_pattern = r'<nav[^>]*>.*?</nav>'
    nav_match = re.search(nav_pattern, index_content, re.DOTALL | re.IGNORECASE)
    
    if nav_match:
        nav_content = nav_match.group(0)
        print("Found navigation. Looking for Services link...")
        
        # Find all links in navigation
        nav_links = re.findall(r'<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', nav_content)
        for href, text in nav_links:
            print(f"  Nav link: '{text.strip()}' -> {href}")
    
    # Files to update - focus on main pages first
    main_files = ['index.html', 'services.html']
    
    updated_count = 0
    
    for filename in main_files:
        if not os.path.exists(filename):
            continue
            
        print(f"\n2. UPDATING {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try multiple patterns to find the Services link
        services_patterns = [
            r'<li>\s*<a href="services\.html">Services</a>\s*</li>',
            r'<li>\s*<a href="/services\.html">Services</a>\s*</li>',
            r'<li>\s*<a href="services">Services</a>\s*</li>',
            r'<a href="services\.html">Services</a>',
            r'<a href="/services\.html">Services</a>'
        ]
        
        replaced = False
        for pattern in services_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                content = content.replace(match.group(0), dropdown_structure)
                print(f"  SUCCESS: Replaced Services link with dropdown containing {len(services)} services")
                replaced = True
                break
        
        if not replaced:
            # If we can't find a Services link, let's add the dropdown to the navigation
            print("  Could not find Services link. Adding dropdown to navigation...")
            
            # Find the navigation and insert the dropdown
            nav_pattern = r'<nav[^>]*>.*?</nav>'
            nav_match = re.search(nav_pattern, content, re.DOTALL | re.IGNORECASE)
            
            if nav_match:
                nav_content = nav_match.group(0)
                
                # Find the ul that contains navigation items
                ul_pattern = r'<ul[^>]*class="[^"]*nav[^"]*"[^>]*>.*?</ul>'
                ul_match = re.search(ul_pattern, nav_content, re.DOTALL | re.IGNORECASE)
                
                if ul_match:
                    ul_content = ul_match.group(0)
                    
                    # Insert the dropdown before the closing ul tag
                    new_ul_content = ul_content.replace('</ul>', dropdown_structure + '\n                    </ul>')
                    content = content.replace(ul_content, new_ul_content)
                    print(f"  SUCCESS: Added dropdown with {len(services)} services to navigation")
                    replaced = True
        
        if replaced:
            # Add CSS for dropdown
            if '.nav-dropdown' not in content:
                print("  Adding dropdown CSS...")
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
                    # Insert after opening style tag
                    style_pos = content.find('<style>') + 7
                    content = content[:style_pos] + dropdown_css + content[style_pos:]
                elif '</head>' in content:
                    # Add style block before closing head
                    content = content.replace('</head>', '<style>' + dropdown_css + '</style>\n</head>')
            
            # Add JavaScript redirects
            if 'const redirects = {' not in content:
                print("  Adding JavaScript redirects...")
                js_redirects = '\n    <!-- Pretty URL Redirect System -->\n    <script>\n    const redirects = {'
                
                for slug, title in services:
                    js_redirects += f"\n        '/{slug}': '/services/{slug}.html',"
                
                js_redirects += '''\n    };\n\n    const currentPath = window.location.pathname;\n    if (redirects[currentPath]) {\n        window.location.href = redirects[currentPath];\n    }\n    </script>'''
                
                if '</head>' in content:
                    content = content.replace('</head>', js_redirects + '\n</head>')
            
            # Write updated content
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            updated_count += 1
    
    print(f"\n3. UPDATING SERVICE PAGES...")
    # Now update service pages to have consistent navigation
    service_files_to_update = service_files[:10]  # Update first 10 service pages
    
    for service_file in service_files_to_update:
        filepath = f"services/{service_file}"
        print(f"  Updating {service_file}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # For service pages, we want to replace any existing Services link with the dropdown
        replaced = False
        for pattern in services_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                content = content.replace(match.group(0), dropdown_structure)
                replaced = True
                break
        
        if replaced:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
    
    print(f"\nCOMPLETE: Updated {updated_count} files")
    print(f"Dropdown now includes ALL {len(services)} services")
    print("All services are now accessible from the navigation dropdown")

if __name__ == "__main__":
    fix_all_services_dropdown()