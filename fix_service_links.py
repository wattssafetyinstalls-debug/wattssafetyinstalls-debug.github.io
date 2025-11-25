# fix_service_links.py
import os
import re

def fix_service_links():
    print("FIXING BROKEN SERVICE LINKS...")
    
    files_to_fix = ["index.html", "services.html"]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"Checking: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count how many broken links we find
            broken_links = re.findall(r'href="/service-pages/[^"]*"', content)
            print(f"Found {len(broken_links)} broken service-pages links")
            
            # Fix service-pages to services
            old_content = content
            content = content.replace('href="/service-pages/', 'href="/services/')
            
            if old_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"FIXED: Updated {len(broken_links)} links in {file_path}")
            else:
                print("No broken links found")
        else:
            print(f"File not found: {file_path}")

fix_service_links()