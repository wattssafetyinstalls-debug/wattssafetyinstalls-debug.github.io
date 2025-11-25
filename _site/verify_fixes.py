# verify_fixes.py
import os

def verify_fixes():
    print("VERIFYING ALL FIXES...\n")
    
    # Check main files exist
    main_files = ["index.html", "services.html", "service_area.html", "referrals.html", "contact.html", "sitemap.html"]
    for file in main_files:
        if os.path.exists(file):
            print(f"OK - {file} exists")
        else:
            print(f"FAIL - {file} missing")
    
    # Check countertop wording in index.html
    if os.path.exists("index.html"):
        with open("index.html", 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "custom countertops" in content.lower():
            print("OK - Custom countertops wording found in index.html")
        else:
            print("FAIL - Custom countertops wording missing in index.html")
    
    # Check return links in service pages
    service_pages = ["services/kitchen-renovations.html", "services/bathroom-remodels.html"]
    for page in service_pages:
        if os.path.exists(page):
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "Return to All Services" in content:
                print(f"OK - Return link found in {page}")
            else:
                print(f"FAIL - Return link missing in {page}")
    
    print("\nQUICK FIXES TO RUN:")
    print("1. Run: python fix_return_links.py")
    print("2. Run: python update_all_main_files.py") 
    print("3. Run: python fix_services_navigation.py")
    print("4. Run: python verify_fixes.py (to confirm)")

verify_fixes()