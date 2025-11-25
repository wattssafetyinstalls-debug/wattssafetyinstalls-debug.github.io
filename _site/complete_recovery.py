# complete_recovery.py
import os
import subprocess

def complete_recovery():
    print("🚨 COMPLETE SITE RECOVERY...")
    
    # Restore all HTML files from BEFORE the corruption
    print("🔄 Restoring HTML files from commit before redirect mess...")
    subprocess.run(['git', 'checkout', 'e864d0a~1', '--', '*.html'], check=True)
    
    # Verify file sizes
    html_files = ["index.html", "services.html", "contact.html", "service-area.html", "referrals.html"]
    
    print("\n📊 VERIFYING RESTORED FILES:")
    for file in html_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            status = "✅ GOOD" if size > 10000 else "❌ STILL CORRUPTED"
            print(f"{status}: {file} - {size} bytes")
        else:
            print(f"❌ MISSING: {file}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Test locally: python -m http.server 8000")
    print("2. Visit: http://localhost:8000")
    print("3. If working: git add . && git commit -m 'RESTORE: Working HTML files'")
    print("4. git push origin main")

complete_recovery()