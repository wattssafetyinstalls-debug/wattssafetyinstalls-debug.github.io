import os
import re

def fix_all_mobile_interactions(file_path):
    """Complete fix for ALL mobile interactions on services page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # COMPLETE CSS FIX FOR ALL INTERACTIVE ELEMENTS
        complete_css_fix = '''
/* === COMPLETE MOBILE FIX - ALL INTERACTIVE ELEMENTS === */

/* Service Cards Fix */
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
}

.service-card:hover::after,
.service-card:active::after,
.service-card:focus::after {
    opacity: 1;
}

.service-card:hover,
.service-card:active,
.service-card:focus {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}

.service-card:hover .service-title,
.service-card:active .service-title,
.service-card:focus .service-title {
    color: white;
}

.service-card:hover .service-description,
.service-card:active .service-description,
.service-card:focus .service-description {
    color: rgba(255,255,255,0.9);
}

/* Seasonal Promo Cards Fix */
.promo-card {
    transition: all 0.3s ease;
}

.promo-card:hover,
.promo-card:active,
.promo-card:focus {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}

/* CTA Buttons Fix */
.cta-button, .promo-cta, .service-cta a {
    transition: all 0.3s ease;
}

.cta-button:hover,
.cta-button:active,
.cta-button:focus,
.promo-cta:hover,
.promo-cta:active,
.promo-cta:focus,
.service-cta a:hover,
.service-cta a:active,
.service-cta a:focus {
    transform: translateY(-2px);
}

/* Trust Items Fix */
.trust-item {
    transition: all 0.3s ease;
}

.trust-item:hover,
.trust-item:active,
.trust-item:focus {
    transform: translateY(-3px);
}

/* Mobile-specific improvements */
@media (hover: none) {
    .service-card,
    .promo-card,
    .cta-button,
    .promo-cta,
    .service-cta a,
    .trust-item {
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
    }
    
    .service-card:active,
    .promo-card:active {
        transform: translateY(-2px);
    }
    
    .cta-button:active,
    .promo-cta:active,
    .service-cta a:active {
        transform: translateY(-1px);
    }
}

/* Remove all JavaScript-based mobile interactions */
.service-card.mobile-active,
.promo-card.mobile-active {
    /* Reset any mobile-active classes */
    transform: none;
}
'''

        # REMOVE ALL PROBLEMATIC JAVASCRIPT
        # Remove service card JavaScript
        content = re.sub(r'/\* Mobile Touch Handler[^*]*\*/\s*[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'// Mobile touch[^}]*?\n\}', '', content, flags=re.DOTALL)
        content = re.sub(r'if \(window\.matchMedia[^}]*?\n\s*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'isTouchDevice[^}]*?\n\s*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'document\.addEventListener[^}]*?service-card[^}]*?\n\s*\}', '', content, flags=re.DOTALL)
        
        # Remove mobile-active classes from CSS
        content = re.sub(r'\.service-card\.mobile-active[^}]*\}', '', content)
        content = re.sub(r'\.promo-card\.mobile-active[^}]*\}', '', content)
        
        # Remove old gradient CSS
        content = re.sub(r'\.service-card::before\s*\{[^}]*\}', '', content)
        content = re.sub(r'\.service-card:hover::before\s*\{[^}]*\}', '', content)
        
        # Add the complete CSS fix
        css_insert_point = '/* === SERVICES CAROUSEL === */'
        if css_insert_point in content:
            content = content.replace(css_insert_point, css_insert_point + complete_css_fix)
        
        # Write the complete fix
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True
        
    except Exception as e:
        print(f"ERROR: {file_path} - {str(e)}")
        return False

def main():
    print("COMPLETE MOBILE FIX - ALL INTERACTIVE ELEMENTS")
    print("=" * 60)
    
    # Fix both main pages that have these elements
    files_to_fix = ["services.html", "index.html"]
    updated_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"Fixing: {file_path}")
            success = fix_all_mobile_interactions(file_path)
            if success:
                updated_count += 1
                print(f"SUCCESS: {file_path} completely fixed")
            else:
                print(f"FAILED: {file_path}")
        else:
            print(f"NOT FOUND: {file_path}")
    
    print("-" * 60)
    
    if updated_count > 0:
        print("COMPLETE FIX APPLIED! This covers:")
        print("- Service cards (gradient + lift)")
        print("- Seasonal promo cards") 
        print("- CTA buttons")
        print("- Trust items")
        print("- All mobile interactions")
        print("\nDeploy now:")
        print("git add services.html index.html")
        print('git commit -m "fix: Complete mobile interactions - all elements, no JavaScript"')
        print("git push origin main")
    else:
        print("No files updated")

if __name__ == "__main__":
    main()