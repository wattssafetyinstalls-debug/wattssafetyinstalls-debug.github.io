#!/usr/bin/env python3
"""
Replace service page CSS with the exact CSS from the working homepage
"""

import os

# Read the complete CSS from homepage
with open('homepage-css.txt', 'r', encoding='utf-8') as f:
    HOMEPAGE_CSS = f.read()

def replace_with_homepage_css():
    services_dir = './services'
    fixed_count = 0
    
    for filename in os.listdir(services_dir):
        if filename.endswith('.html') and not filename.endswith('.backup'):
            filepath = os.path.join(services_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the entire style section with homepage CSS
            if '<style>' in content and '</style>' in content:
                start = content.find('<style>')
                end = content.find('</style>') + 8
                new_content = content[:start] + HOMEPAGE_CSS + content[end:]
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                fixed_count += 1
                print(f"Replaced CSS with homepage CSS: {filename}")
    
    print(f"Replaced CSS in {fixed_count} service pages with homepage CSS")

if __name__ == "__main__":
    replace_with_homepage_css()