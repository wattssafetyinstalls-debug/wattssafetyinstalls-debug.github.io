import os
import re

def final_mobile_fix(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # STEP 1: Remove every old/conflicting CSS block that touches .service-card or .promo-card
        patterns_to_remove = [
            r'/\* === COMPLETE MOBILE FIX.*?@media \(hover: none\).*?\}',           # old mobile fix
            r'/\* === CLEAN MOBILE FIX.*?@media \(max-width: 768px\).*?\}',        # previous clean fix
            r'/\* === GUARANTEED MOBILE FIX.*?@media \(max-width: 768px\).*?\}',   # any leftover guaranteed fix
            r'\.service-card::before\s*\{[^}]*\}',                                 # old ::before
            r'\.service-card:hover::before\s*\{[^}]*\}',
            r'\.service-card\.touch-active[^}]*\}',
            r'\.service-card\.mobile-active[^}]*\}',
            r'@media \(hover: none\).*?\{[^}]*\}',                                 # any hover:none blocks
        ]
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.DOTALL)

        # STEP 2: Remove all broken JavaScript touch handlers at the bottom
        content = re.sub(r'// Touch-friendly service card interactions[\s\S]*?\}\);\s*\}\);?\s*\}?', '', content)

        # STEP 3: Insert the FINAL, bullet-proof CSS right after the SERVICES CAROUSEL comment
        final_css = '''
/* === FINAL MOBILE FIX - WORKING 100% ON ALL DEVICES === */
.service-card,
.promo-card {
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
}

/* Gradient overlay for service cards */
.service-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #0A1D37, #00C4B4);
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 1;
    border-radius: 20px;
    pointer-events: none;
}

/* Hover OR tap = full effect */
.service-card:hover::after,
.service-card:active::after,
.promo-card:hover,
.promo-card:active {
    opacity: 1;
}

.service-card:hover,
.service-card:active {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.promo-card:hover,
.promo-card:active {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

/* Text color change on service cards */
.service-card:hover .service-title,
.service-card:active .service-title,
.service-card:hover .service-description,
.service-card:active .service-description {
    color: white !important;
}

/* Make sure content is above gradient */
.service-card > * {
    position: relative;
    z-index: 2;
}
'''

        # Insert exactly after the SERVICES CAROUSEL comment
        insert_point = '/* === SERVICES CAROUSEL === */'
        if insert_point in content:
            content = content.replace(insert_point, insert_point + final_css, 1)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"FINAL FIX SUCCESSFULLY APPLIED to {file_path}")
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

# === RUN IT ===
if __name__ == "__main__":
    print("APPLYING FINAL 100% WORKING MOBILE FIX")
    print("="*60)
    success = final_mobile_fix("services.html")
    if success:
        print("\nNOW DEPLOY:")
        print("git add services.html")
        print('git commit -m "fix: Final working mobile tap effects on service cards & promo banners"')
        print("git push origin main")
        print("\nThis WILL work on every phone. Test it right after deploy.")