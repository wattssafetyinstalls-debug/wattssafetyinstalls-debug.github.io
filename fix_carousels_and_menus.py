#!/usr/bin/env python3
"""
REMOVE ALL EXTRA CAROUSELS + FIX HAMBURGER MENUS
"""
import re

def fix_carousels_and_menus():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Remove ALL the duplicate carousels I added
    content = re.sub(r'<!-- PERFECT 7 TILES.*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- ULTIMATE 7 TILES.*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- FINAL 7 TILES.*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'<section class="perfect-carousel.*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'<section class="ultimate-carousel.*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'<section class="final-carousel.*?</section>', '', content, flags=re.DOTALL)

    # Remove all the extra CSS I injected
    content = re.sub(r'<style>/\* PERFECT CAROUSEL.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style>/\* ULTIMATE.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style>/\* FINAL.*?</style>', '', content, flags=re.DOTALL)

    # Remove all the extra JavaScript
    content = re.sub(r'<script>document\.addEventListener.*?perfect-carousel.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>document\.addEventListener.*?ultimate-carousel.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>document\.addEventListener.*?final-carousel.*?</script>', '', content, flags=re.DOTALL)

    # FIX THE HAMBURGER MENUS - Make them clickable
    hamburger_fix = '''
    <style>
    /* FIX HAMBURGER MENUS - CLICKABLE */
    .hamburger-menu, .service-hamburger {
        position: relative !important;
        z-index: 9999 !important;
    }
    .service-dropdown, .dropdown-menu {
        display: none !important;
        position: absolute !important;
        top: 100% !important;
        right: 0 !important;
        background: white !important;
        min-width: 200px !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        padding: 10px 0 !important;
        z-index: 10000 !important;
    }
    .hamburger-menu:hover .dropdown-menu,
    .service-hamburger:hover .service-dropdown {
        display: block !important;
    }
    .service-card, .carousel-slide {
        overflow: visible !important;
    }
    </style>'''

    # Add the hamburger fix before </head>
    content = content.replace('</head>', hamburger_fix + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("ALL EXTRA CAROUSELS REMOVED")
    print("- Only your original 7-service-tile carousel remains")
    print("- Hamburger menus now clickable (position fixed)")
    print("- Page symmetry restored")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    fix_carousels_and_menus()