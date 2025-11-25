# cleanup_js_redirects.py
import os
import re

def clean_js_redirects():
    print("CLEANING JAVASCRIPT REDIRECTS...")
    
    main_files = ["index.html", "services.html", "service-area.html", "referrals.html", "contact.html", "sitemap.html"]
    
    for file_path in main_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove the JavaScript redirect script that was causing loops
            old_content = content
            content = re.sub(r'<script>\s*//\s*Pretty URL Standardization.*?</script>', '', content, flags=re.DOTALL)
            
            if old_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"CLEANED: {file_path}")
            else:
                print(f"ALREADY CLEAN: {file_path}")
        else:
            print(f"MISSING: {file_path}")

clean_js_redirects()