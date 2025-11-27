import os
import re

def fix_nav_links_in_file(file_path):
    """Fix navigation links in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Count replacements
        replacements = 0
        
        # Fix main navigation links - remove .html from common nav links
        nav_links_to_fix = {
            'href="/"': 'href="/"',  # Keep home as is
            'href="/index.html"': 'href="/"',
            'href="/services.html"': 'href="/services"',
            'href="/service-area.html"': 'href="/service-area"',
            'href="/about.html"': 'href="/about"',
            'href="/referrals.html"': 'href="/referrals"',
            'href="/contact.html"': 'href="/contact"',
        }
        
        for old_link, new_link in nav_links_to_fix.items():
            if old_link in content:
                content = content.replace(old_link, new_link)
                replacements += 1
        
        # Also fix any other .html links in navigation (catch-all pattern)
        # This catches any href="/pagename.html" in the navigation
        html_link_pattern = r'href="/([^"]+)\.html"'
        
        def replace_html_links(match):
            page_name = match.group(1)
            # Don't remove .html from service pages themselves
            if page_name.startswith('services/'):
                return match.group(0)  # Keep service pages as .html
            return f'href="/{page_name}"'
        
        content = re.sub(html_link_pattern, replace_html_links, content)
        
        # Write the updated content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True, replacements
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False, 0

def main():
    print("Fixing Navigation Links in Service Pages")
    print("=" * 60)
    
    services_dir = "services"
    updated_count = 0
    error_count = 0
    total_replacements = 0
    
    # Get all HTML files in services directory
    service_files = [f for f in os.listdir(services_dir) if f.endswith('.html') and not f.endswith('.backup')]
    
    print(f"Found {len(service_files)} service pages to process")
    print("-" * 60)
    
    for filename in service_files:
        file_path = os.path.join(services_dir, filename)
        success, replacements = fix_nav_links_in_file(file_path)
        
        if success:
            if replacements > 0:
                print(f"UPDATED: {filename} - {replacements} links fixed")
                updated_count += 1
                total_replacements += replacements
            else:
                print(f"NO CHANGES: {filename} - links already correct")
        else:
            print(f"ERROR: {filename} - failed to process")
            error_count += 1
    
    print("-" * 60)
    print("RESULTS:")
    print(f"  Successfully updated: {updated_count} files")
    print(f"  Total link fixes: {total_replacements}")
    print(f"  Errors: {error_count} files")
    print(f"  Total processed: {len(service_files)} files")
    
    if updated_count > 0:
        print(f"\nSUCCESS: Fixed navigation links in {updated_count} service pages!")
        print("Navigation now points to pretty URLs instead of .html files")
    else:
        print("\nNo updates needed - all navigation links are already correct")

if __name__ == "__main__":
    main()