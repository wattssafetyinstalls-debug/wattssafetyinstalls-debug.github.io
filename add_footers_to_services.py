#!/usr/bin/env python3
import os
import re

SERVICES_DIR = "services"
FOOTER_HTML = """    <footer>
        <div class="footer-contact">
            <p><strong>Watts Safety Installs</strong></p>
            <p>Phone: <a href="tel:+14054106402">(405) 410-6402</a></p>
            <p>Service Areas: Norfolk, Battle Creek, Pierce, Madison County & Antelope County NE</p>
        </div>
        <div class="footer-links">
            <a href="/services">All Services</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/privacy-policy">Privacy Policy</a>
        </div>
        <p>&copy; 2024 Watts Safety Installs. All rights reserved.</p>
    </footer>
"""

def has_footer(content):
    """Check if page already has footer element"""
    return '<footer>' in content or '<footer ' in content

def add_footer_to_file(filepath):
    """Add footer to service page before closing body tag"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if has_footer(content):
        return False
    
    # Find closing body tag and insert footer before it
    new_content = content.replace('</body>', FOOTER_HTML + '\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

# Process all HTML files in services directory
added_count = 0
total_count = 0

for filename in sorted(os.listdir(SERVICES_DIR)):
    if filename.endswith('.html') and not filename.endswith('.backup2'):
        filepath = os.path.join(SERVICES_DIR, filename)
        total_count += 1
        
        if add_footer_to_file(filepath):
            added_count += 1
            print(f'✅ Added footer: {filename}')
        else:
            print(f'⏭️  Already has footer: {filename}')

print(f'\n✅ Complete - Added footers to {added_count} of {total_count} files')
