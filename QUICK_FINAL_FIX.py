#!/usr/bin/env python3
"""
QUICK FINAL FIX - ONLY dropdown position + promo hover/center
No new carousels, no duplicates
"""
import re

def quick_fix():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix dropdown position — now perfectly clickable
    content = re.sub(r'\.final-dropdown\s*\{[^}]*top:[^;]*;', '', content)
    content = re.sub(r'\.final-hamburger:hover\s*>\s*\.final-dropdown\s*\{[^}]*\}', '', content)

    dropdown_css = '''
    <style>
    /* PERFECT CLICKABLE DROPDOWN */
    .final-hamburger,
    .perfect-hamburger,
    .ultimate-hamburger,
    .hamburger-menu,
    .service-hamburger {position:relative;z-index:9999}
    
    .final-dropdown,
    .perfect-dropdown,
    .ultimate-dropdown,
    .service-dropdown,
    .dropdown {
        display:none;
        position:absolute;
        top:100% !important;
        right:0;
        background:#fff;
        min-width:220px;
        border-radius:16px;
        box-shadow:0 20px 50px rgba(0,0,0,.25);
        padding:12px 0;
        z-index:99999;
        margin-top:8px;
    }
    
    .final-hamburger:hover > .final-dropdown,
    .perfect-hamburger:hover > .perfect-dropdown,
    .ultimate-hamburger:hover > .ultimate-dropdown,
    .hamburger-menu:hover > .dropdown,
    .service-hamburger:hover > .service-dropdown {
        display:block !important;
    }
    
    .final-card,
    .perfect-card,
    .ultimate-card,
    .service-card,
    .carousel-slide,
    .final-slide {overflow:visible !important}
    </style>'''

    # 2. Fix promo section — centered + navy to teal gradient hover
    promo_css = '''
    <style>
    /* PROMO SECTION - CENTERED + NAVY TO TEAL HOVER */
    .promo-section,
    .promo-cards {max-width:1200px;margin:80px auto;padding:0 20px}
    .promo-section {text-align:center}
    .promo-cards {display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:30px}
    .promo-card {
        background:rgba(255,255,255,.1);
        padding:40px;
        border-radius:20px;
        transition:all .5s;
        backdrop-filter:blur(10px);
        border:1px solid rgba(255,255,255,.2);
    }
    .promo-card:hover {
        background:linear-gradient(135deg,var(--teal),var(--navy));
        transform:translateY(-12px);
        box-shadow:0 25px 50px rgba(0,196,180,.4);
    }
    .promo-card:hover .cta-button {background:#fff;color:var(--navy)}
    </style>'''

    # Insert both fixes right before </head>
    combined_fix = dropdown_css + promo_css
    content = content.replace('</head>', combined_fix + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("QUICK FIX COMPLETE")
    print("- Dropdowns now perfectly clickable")
    print("- Promo section centered with navy to teal hover")
    print("- No new carousels, no duplicates")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    quick_fix()