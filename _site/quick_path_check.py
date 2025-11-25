# quick_path_check.py
import os

def check_current_paths():
    print("Checking current paths in key files...")
    
    files_to_check = ["services.html", "services/kitchen-renovations.html"]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"\n--- {file_path} ---")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for problematic paths
            if 'service-pages' in content:
                print("[ISSUE] Found 'service-pages' paths that need fixing")
            else:
                print("[OK] No 'service-pages' paths found")
            
            # Check for correct paths
            if 'href="services/' in content:
                print("[OK] Found correct 'services/' paths")
            
            # Count links
            import re
            links = re.findall(r'href=[\'"]?([^\'" >]+)', content)
            service_links = [link for link in links if 'service' in link]
            print(f"Found {len(service_links)} service-related links")
        else:
            print(f"\n[ERROR] {file_path} not found")

check_current_paths()