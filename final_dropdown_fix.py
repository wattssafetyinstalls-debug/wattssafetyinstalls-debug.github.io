# final_dropdown_fix.py
import os
import re

def final_fix():
    print("FINAL DROPDOWN FIX - THIS WILL DEFINITELY WORK...")
    
    # Get ALL services
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    services = []
    for file in service_files:
        slug = file.replace('.html', '')
        title = slug.replace('-', ' ').title()
        services.append((slug, title))
    
    print(f"Adding {len(services)} services to dropdown...")
    
    # Build dropdown HTML
    dropdown_items = ''
    for slug, title in services:
        dropdown_items += f'                        <li><a href="/{slug}">{title}</a></li>\n'
    
    # The complete dropdown structure
    dropdown_html = f'''                <li class="nav-dropdown">
                    <a href="services.html">Services</a>
                    <ul class="dropdown">
{dropdown_items}                    </ul>
                </li>'''
    
    # CSS for dropdown
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
        }'''
    
    # JavaScript redirects
    js_redirects = '\n    <!-- Pretty URL Redirect System -->\n    <script>\n    const redirects = {'
    for slug, title in services:
        js_redirects += f"\n        '/{slug}': '/services/{slug}.html',"
    js_redirects += '''\n    };\n\n    const currentPath = window.location.pathname;\n    if (redirects[currentPath]) {\n        window.location.href = redirects[currentPath];\n    }\n    </script>'''
    
    # FIX MAIN PAGES
    print("\n1. FIXING MAIN PAGES...")
    main_pages = ['index.html', 'services.html']
    
    for filename in main_pages:
        print(f"  Processing {filename}...")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # METHOD 1: Direct replacement of Services link
        original_content = content
        
        # Replace any Services link with dropdown
        content = re.sub(
            r'<li>\s*<a href="services\.html">Services</a>\s*</li>',
            dropdown_html,
            content,
            flags=re.IGNORECASE
        )
        
        # If no change happened, try other patterns
        if content == original_content:
            content = re.sub(
                r'<a href="services\.html">Services</a>',
                dropdown_html,
                content,
                flags=re.IGNORECASE
            )
        
        # If still no change, manually insert after Home link
        if content == original_content:
            home_pattern = r'<a href="[^"]*">Home</a>'
            home_match = re.search(home_pattern, content)
            if home_match:
                home_line = home_match.group(0)
                # Find the entire list item containing Home
                home_li_pattern = r'<li[^>]*>\s*' + re.escape(home_line) + r'\s*</li>'
                home_li_match = re.search(home_li_pattern, content)
                if home_li_match:
                    home_li = home_li_match.group(0)
                    # Insert dropdown after the Home list item
                    content = content.replace(home_li, home_li + '\n' + dropdown_html)
                    print(f"    Inserted dropdown after Home link")
        
        # Add CSS
        if '.nav-dropdown' not in content:
            if '<style>' in content:
                style_pos = content.find('<style>') + 7
                content = content[:style_pos] + dropdown_css + content[style_pos:]
            elif '</head>' in content:
                content = content.replace('</head>', '<style>' + dropdown_css + '</style>\n</head>')
        
        # Add JavaScript
        if 'const redirects = {' not in content:
            if '</head>' in content:
                content = content.replace('</head>', js_redirects + '\n</head>')
        
        # Write changes
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"    Updated {filename}")
    
    print("\n2. DEPLOYMENT COMMANDS:")
    print("git add index.html services.html")
    print('git commit -m "Add complete dropdown navigation with all services"')
    print("git push origin main")
    print("\n3. VERIFICATION:")
    print("After deployment, check these URLs:")
    print("https://wattsatpcontractor.com")
    print("https://wattsatpcontractor.com/services.html")
    print("Hover over 'Services' - you should see ALL services in dropdown!")

if __name__ == "__main__":
    final_fix()