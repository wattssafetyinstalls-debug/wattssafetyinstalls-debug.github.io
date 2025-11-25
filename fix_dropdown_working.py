# fix_dropdown_working.py
import os
import re

def find_and_fix_dropdown():
    print("FINDING AND FIXING DROPDOWN MENU...")
    
    # Get all services
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    services = []
    for file in service_files:
        slug = file.replace('.html', '')
        title = slug.replace('-', ' ').title()
        services.append((slug, title))
    
    print(f"Found {len(services)} services")
    
    # Files to update
    files_to_update = ['index.html', 'services.html']
    
    for filename in files_to_update:
        if not os.path.exists(filename):
            continue
            
        print(f"\nProcessing {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Build the complete dropdown HTML
        dropdown_html = ''
        for slug, title in services:
            dropdown_html += f'<li><a href="/{slug}">{title}</a></li>\n'
        
        # Find the navigation section - look for any dropdown-like structure
        # Common patterns for dropdowns
        dropdown_patterns = [
            r'<ul[^>]*class="[^"]*dropdown[^"]*"[^>]*>.*?</ul>',
            r'<div[^>]*class="[^"]*dropdown[^"]*"[^>]*>.*?</div>',
            r'<ul[^>]*class="[^"]*nav[^"]*"[^>]*>.*?</ul>'
        ]
        
        found_dropdown = False
        
        for pattern in dropdown_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            if matches:
                print(f"Found dropdown structure with pattern: {pattern[:50]}...")
                
                # For each dropdown found, replace its content with our services
                for match in matches:
                    # Extract just the list items if it's a UL
                    if '<ul' in match:
                        # Replace the content between <ul> and </ul>
                        new_dropdown = re.sub(r'<ul[^>]*>.*?</ul>', 
                                            f'<ul class="dropdown">\n{dropdown_html}</ul>', 
                                            match, 
                                            flags=re.DOTALL)
                    else:
                        # For other structures, replace the entire thing
                        new_dropdown = f'<ul class="dropdown">\n{dropdown_html}</ul>'
                    
                    content = content.replace(match, new_dropdown)
                    found_dropdown = True
                    print(f"Replaced dropdown with {len(services)} services")
                    break
            
            if found_dropdown:
                break
        
        if not found_dropdown:
            print("No dropdown found. Let me check the navigation structure...")
            
            # Look for navigation and see where services should go
            nav_pattern = r'<nav[^>]*>.*?</nav>'
            nav_match = re.search(nav_pattern, content, re.DOTALL | re.IGNORECASE)
            
            if nav_match:
                print("Found navigation. Let me add a dropdown to it...")
                
                # Create a simple dropdown structure
                dropdown_structure = f'''
                <li class="nav-dropdown">
                    <a href="services.html">Services</a>
                    <ul class="dropdown">
                        {dropdown_html}
                    </ul>
                </li>
                '''
                
                # Try to insert after existing navigation items
                if '<li><a href="services.html">Services</a></li>' in content:
                    content = content.replace(
                        '<li><a href="services.html">Services</a></li>',
                        dropdown_structure
                    )
                    found_dropdown = True
                    print("Added dropdown structure to navigation")
        
        if found_dropdown:
            # Write the updated content
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully updated {filename}")
        else:
            print(f"Could not find or create dropdown in {filename}")
    
    print(f"\nCOMPLETE: Processed {len(files_to_update)} files")
    print(f"Dropdown should now show all {len(services)} services")

if __name__ == "__main__":
    find_and_fix_dropdown()