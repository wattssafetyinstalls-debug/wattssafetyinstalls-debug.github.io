# analyze_current_redirects_ascii.py
import os
import re

def analyze_redirects():
    print("ANALYZING CURRENT REDIRECT PATTERNS...")
    
    html_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find window.location redirects
        location_matches = re.findall(r'window\.location\.(pathname|href)\s*=[^=]?===\s*["\']([^"\']+)["\']', content)
        # Find history.replaceState redirects
        history_matches = re.findall(r'window\.history\.replaceState\([^)]*["\']([^"\']+)["\']', content)
        # Find meta refresh redirects
        meta_matches = re.findall(r'meta http-equiv=["\']refresh["\'][^>]*url=([^"\'>]+)', content, re.IGNORECASE)
        
        if location_matches or history_matches or meta_matches:
            print(f"FILE: {file_path}")
            if location_matches:
                print(f"   Location redirects: {location_matches}")
            if history_matches:
                print(f"   History redirects: {history_matches}")
            if meta_matches:
                print(f"   Meta redirects: {meta_matches}")

analyze_redirects()