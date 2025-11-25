# check_github_pages.py
import os

def check_github_setup():
    print("🔧 Checking GitHub Pages Setup...")
    
    # Check for required files
    required_files = ["index.html", "services.html", "service-area.html"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"❌ {file} missing")
    
    # Check for CNAME file (if using custom domain)
    if os.path.exists("CNAME"):
        with open("CNAME", 'r') as f:
            cname_content = f.read().strip()
        print(f"✓ CNAME file found: {cname_content}")
    else:
        print("ℹ️  No CNAME file found (using github.io domain)")
    
    # Check for .nojekyll file (important for SPAs)
    if os.path.exists(".nojekyll"):
        print("✓ .nojekyll file found")
    else:
        print("ℹ️  Consider creating .nojekyll file for better GitHub Pages compatibility")
    
    print("\n🚀 To deploy changes to live site:")
    print("1. git add .")
    print("2. git commit -m 'Fix service pages and paths'") 
    print("3. git push origin main")
    print("4. Wait 1-2 minutes for GitHub Pages to rebuild")

check_github_setup()