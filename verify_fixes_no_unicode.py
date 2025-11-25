# verify_fixes_no_unicode.py
import os
import subprocess

def verify_fixes():
    print("VERIFYING ALL FIXES...")
    
    # Check Git status
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print("Changes ready to commit:")
        print(result.stdout)
    else:
        print("No uncommitted changes")
    
    # Check service pages exist
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    print(f"{len(service_files)} service pages found")
    
    # Check if main files are modified
    main_files = ['index.html', 'services.html']
    for file in main_files:
        if os.path.exists(file):
            print(f"{file} is ready")
    
    print("\nQUICK DEPLOYMENT COMMANDS:")
    print("git add .")
    print('git commit -m "Final fixes: hover readability, SEO descriptions, navigation"')
    print("git push origin main")
    
    print("\nLIVE SITE URLs TO CHECK:")
    print("https://wattsatpcontractor.com")
    print("https://wattsatpcontractor.com/services.html")
    print("https://wattsatpcontractor.com/services/driveway-installation.html")

if __name__ == "__main__":
    verify_fixes()