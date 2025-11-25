# fix_all_directory_paths_ascii.py
import os
import re

def fix_directory_paths():
    # Files to update
    files_to_update = [
        "index.html",
        "services.html", 
        "service-area.html",
        "referrals.html", 
        "contact.html",
        "sitemap.html"
    ]
    
    # Add all service pages
    service_dir = "services"
    if os.path.exists(service_dir):
        for file in os.listdir(service_dir):
            if file.endswith(".html"):
                files_to_update.append(f"{service_dir}/{file}")
    
    print(f"Updating {len(files_to_update)} files...")
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            old_content = content
            
            # Fix service page paths
            content = content.replace('href="/service-pages/', 'href="/services/')
            content = content.replace('href="service-pages/', 'href="services/')
            content = content.replace("href='/service-pages/", "href='/services/")
            
            # Fix case sensitivity in paths
            content = re.sub(r'href="([^"]*\.html)"', lambda m: m.group(0).lower(), content)
            content = re.sub(r"href='([^']*\.html)'", lambda m: m.group(0).lower(), content)
            
            # Ensure all service links are correct
            content = content.replace('href="services/services/', 'href="services/')
            
            if old_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[OK] Fixed paths: {file_path}")
            else:
                print(f"[NO CHANGE] No changes: {file_path}")
        else:
            print(f"[ERROR] Missing: {file_path}")

fix_directory_paths()