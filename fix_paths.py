#!/usr/bin/env python3
"""
Fix path references in service pages for correct CSS, navigation, and resource loading
"""

import os

def fix_service_paths():
    services_dir = './services'
    fixed_count = 0
    
    for filename in os.listdir(services_dir):
        if filename.endswith('.html') and not filename.endswith('.backup'):
            filepath = os.path.join(services_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix navigation links to go up one directory
            old_content = content
            
            # Fix header navigation links
            content = content.replace('href="services.html"', 'href="../services.html"')
            content = content.replace('href="service-area.html"', 'href="../service-area.html"')
            content = content.replace('href="about.html"', 'href="../about.html"')
            content = content.replace('href="referrals.html"', 'href="../referrals.html"')
            content = content.replace('href="contact.html"', 'href="../contact.html"')
            content = content.replace('href="index.html"', 'href="../index.html"')
            
            # Fix footer links
            content = content.replace('href="/sitemap.html"', 'href="../sitemap.html"')
            content = content.replace('href="/privacy-policy.html"', 'href="../privacy-policy.html"')
            content = content.replace('href="/terms.html"', 'href="../terms.html"')
            content = content.replace('href="/services.html"', 'href="../services.html"')
            
            # Fix return button
            content = content.replace('href="/services.html"', 'href="../services.html"')
            
            # Only write if changes were made
            if content != old_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"Fixed paths: {filename}")
    
    print(f"Fixed path references in {fixed_count} service pages")

if __name__ == "__main__":
    fix_service_paths()