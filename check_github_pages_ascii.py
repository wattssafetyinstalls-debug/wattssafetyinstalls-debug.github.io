# check_github_pages_ascii.py
import os

def check_github_setup():
    print("Checking GitHub Pages Setup...")
    
    # Check for required files
    required_files = ["index.html", "services.html", "service-area.html"]
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file} exists")
        else:
            print(f"[ERROR] {file} missing")
    
    # Check for CNAME file (if using custom domain)
    if os.path.exists("CNAME"):
        with open("CNAME", 'r') as f:
            cname_content = f.read().strip()
        print(f"[OK] CNAME file found: {cname_content}")
    else:
        print("[INFO] No CNAME file found (using github.io domain)")
    
    # Check for .nojekyll file (important for SPAs)
    if os.path.exists(".nojekyll"):
        print("[OK] .nojekyll file found")
    else:
        print("[INFO] Consider creating .nojekyll file for better GitHub Pages compatibility")
    
    print("\nTo deploy changes to live site:")
    print("1. git add .")
    print("2. git commit -m 'Fix service pages and paths'") 
    print("3. git push origin main")
    print("4. Wait 1-2 minutes for GitHub Pages to rebuild")

check_github_setup()