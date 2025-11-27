import os
import re

def fix_all_mobile_conflicts(file_path):
    """COMPLETE FIX - Remove all conflicting CSS and JavaScript"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # COMPLETELY REMOVE ALL PROBLEMATIC CSS
        # Remove old gradient CSS
        content = re.sub(r'\.service-card::before\s*\{[^}]*\}', '', content)
        content = re.sub(r'\.service-card:hover::before\s*\{[^}]*\}', '', content)
        content = re.sub(r'\.service-card\.touch-active[^}]*\}', '', content)
        content = re.sub(r'\.service-card\.mobile-active[^}]*\}', '', content)
        
        # Remove the broken mobile fix CSS section
        content = re.sub(r'/\* === COMPLETE MOBILE FIX[^*]*\*/.*?@media \(hover: none\)[^}]*\}', '', content, flags=re.DOTALL)
        
        # Remove duplicate service-card styles
        content = re.sub(r'/\* Service Cards Fix \*/\s*\.service-card[^}]*\}', '', content, flags=re.DOTALL)
        
        # CLEAN CSS REPLACEMENT - SIMPLE AND WORKING
        clean_css = '''
/* === CLEAN MOBILE FIX - WORKING === */
.service-card {
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.service-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--navy), var(--teal));
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 1;
    border-radius: 20px;
    pointer-events: none;
}

.service-card:hover::after {
    opacity: 1;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}

.service-card:hover .service-title {
    color: white;
}

.service-card:hover .service-description {
    color: rgba(255,255,255,0.9);
}

/* Mobile active state */
.service-card:active::after {
    opacity: 1;
}

.service-card:active {
    transform: translateY(-2px);
}

.service-card:active .service-title {
    color: white;
}

.service-card:active .service-description {
    color: rgba(255,255,255,0.9);
}

/* Promo cards */
.promo-card {
    transition: all 0.3s ease;
}

.promo-card:hover,
.promo-card:active {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}

/* Mobile improvements */
@media (max-width: 768px) {
    .service-card,
    .promo-card {
        -webkit-tap-highlight-color: transparent;
        cursor: pointer;
    }
}
'''
        
        # Remove any existing clean CSS to avoid duplicates
        content = re.sub(r'/\* === CLEAN MOBILE FIX[^*]*\*/.*?@media \(max-width: 768px\)[^}]*\}', '', content, flags=re.DOTALL)
        
        # Insert clean CSS after services carousel comment
        css_insert_point = '/* === SERVICES CAROUSEL === */'
        if css_insert_point in content:
            content = content.replace(css_insert_point, css_insert_point + clean_css)
        
        # COMPLETELY REMOVE BROKEN JAVASCRIPT
        # Remove all touch interaction JavaScript
        content = re.sub(r'// Touch-friendly service card interactions.*?document\.addEventListener[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'if \(window\.matchMedia\("\(hover: none\)"\)\.matches\)[^}]*?\n\s*\}', '', content, flags=re.DOTALL)
        
        # Remove broken JavaScript fragments
        content = re.sub(r'// Close service cards when clicking outside[^}]*?\n\s*\}', '', content)
        content = re.sub(r'this\.classList\.toggle\(\'touch-active\'\);', '', content)
        content = re.sub(r'card\.classList\.remove\(\'touch-active\'\);', '', content)
        
        # Fix the broken JavaScript at the end of the file
        broken_js_pattern = r'// Touch-friendly service card interactions[\s\S]*?document\.addEventListener\(\s*\'click\'[^}]*?\}\);\s*\n\s*\}\);\s*\n\s*\}'
        content = re.sub(broken_js_pattern, '', content)
        
        # Remove the specific broken line
        content = re.sub(r'// Close service cards when clicking outside[^;]*\);', '', content)
        
        # Write the cleaned content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True
        
    except Exception as e:
        print(f"ERROR: {file_path} - {str(e)}")
        return False

def main():
    print("COMPLETE MOBILE FIX - REMOVING ALL CONFLICTS")
    print("=" * 60)
    
    files_to_fix = ["services.html"]
    updated_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"Fixing: {file_path}")
            success = fix_all_mobile_conflicts(file_path)
            if success:
                updated_count += 1
                print(f"SUCCESS: {file_path} completely cleaned")
            else:
                print(f"FAILED: {file_path}")
        else:
            print(f"NOT FOUND: {file_path}")
    
    print("-" * 60)
    
    if updated_count > 0:
        print("COMPLETE CLEANUP APPLIED!")
        print("All conflicting CSS and JavaScript has been removed.")
        print("Now using simple, working CSS transitions.")
        print("\nDeploy now:")
        print("git add services.html")
        print('git commit -m "fix: Complete mobile cleanup - remove all conflicts, use simple CSS"')
        print("git push origin main")
    else:
        print("No files updated")

if __name__ == "__main__":
    main()