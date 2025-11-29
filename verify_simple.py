import os

def verify_css_injection_simple(file_path):
    """Verify that our CSS and JS were properly injected - simple version"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        has_css = 'COMPREHENSIVE TILE LAYOUTS & ANIMATIONS' in content
        has_js = 'COMPREHENSIVE TILE ANIMATION SCRIPT' in content
        
        status_css = "YES" if has_css else "NO"
        status_js = "YES" if has_js else "NO"
        print(f"{os.path.basename(file_path)} - CSS: {status_css}, JS: {status_js}")
        
        return has_css and has_js
        
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return False

def main():
    print("Verifying CSS/JS Injection")
    print("=" * 40)
    
    target_files = ['referrals.html', 'about.html', 'service-area.html', 'contact.html']
    
    all_good = True
    for file in target_files:
        if os.path.exists(file):
            if not verify_css_injection_simple(file):
                all_good = False
        else:
            print(f"{file} - File not found")
            all_good = False
    
    print("=" * 40)
    if all_good:
        print("SUCCESS: All files have CSS/JS injected")
        print("")
        print("If you still don't see changes, try:")
        print("1. Hard refresh: Ctrl+Shift+R")
        print("2. Incognito mode: Ctrl+Shift+N")
        print("3. Check browser console for errors (F12 > Console)")
    else:
        print("FAILED: Some files are missing CSS/JS - we need to fix this!")

if __name__ == "__main__":
    main()