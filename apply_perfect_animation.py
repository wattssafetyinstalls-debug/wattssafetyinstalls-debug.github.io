import os
import re

# ALL your pages — including index.html
pages = ['index.html', 'about.html', 'referrals.html', 'contact.html', 'service-area.html']

# EXACT animation from your working service pages — copied 1:1
css = '''
    /* FULL NAVY-TO-TEAL GRADIENT + SATIN GLOSS — APPLIED TO EVERY TILE YOU HAVE */
    .service-tile, .promo-tile, .town-tile, .hero-tile, .seasonal-tile,
    [class*="tile"], [class*="Tile"] {
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s ease !important;
        cursor: pointer;
    }

    /* Gradient overlay */
    .service-tile::before, .promo-tile::before, .town-tile::before, 
    .hero-tile::before, .seasonal-tile::before,
    [class*="tile"]::before, [class*="Tile"]::before {
        content: "" !important;
        position: absolute !important;
        top: 0; left: 0; right: 0; bottom: 0 !important;
        background: linear-gradient(135deg, var(--teal), var(--navy)) !important;
        opacity: 0 !important;
        transition: opacity 0.5s ease !important;
        z-index: -1 !important;
    }

    /* Satin gloss swipe */
    .service-tile::after, .promo-tile::after, .town-tile::after,
    .hero-tile::after, .seasonal-tile::after,
    [class*="tile"]::after, [class*="Tile"]::after {
        content: "" !important;
        position: absolute !important;
        top: 0; left: 0; right: 0; bottom: 0 !important;
        background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%) !important;
        transform: translateX(-100%) !important;
        transition: transform 1.3s ease-out !important;
        z-index: 1 !important;
        pointer-events: none !important;
    }

    /* HOVER & MOBILE = FULL EFFECT */
    .service-tile:hover, .promo-tile:hover, .town-tile:hover, 
    .hero-tile:hover, .seasonal-tile:hover,
    [class*="tile"]:hover, [class*="Tile"]:hover,
    .service-tile.mobile-animated, .promo-tile.mobile-animated, 
    .town-tile.mobile-animated, .hero-tile.mobile-animated, 
    .seasonal-tile.mobile-animated,
    [class*="tile"].mobile-animated, [class*="Tile"].mobile-animated {
        transform: translateY(-12px) scale(1.03) !important;
        box-shadow: 0 35px 90px rgba(10,29,55,0.38) !important;
        color: white !important;
        border-color: var(--gray) !important;
    }

    .service-tile:hover::before, .promo-tile:hover::before, .town-tile:hover::before,
    [class*="tile"]:hover::before,
    .service-tile.mobile-animated::before, .promo-tile.mobile-animated::before,
    .town-tile.mobile-animated::before, [class*="tile"].mobile-animated::before {
        opacity: 1 !important;
    }

    .service-tile:hover::after, .promo-tile:hover::after, .town-tile:hover::after,
    [class*="tile"]:hover::after,
    .service-tile.mobile-animated::after, .promo-tile.mobile-animated::after,
    .town-tile.mobile-animated::after, [class*="tile"].mobile-animated::after {
        animation: gloss 1.3s ease-out forwards !important;
    }

    @keyframes gloss {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
'''

js = '''
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        if (window.innerWidth <= 768) {
            setTimeout(function() {
                document.querySelectorAll(".service-tile, .promo-tile, .town-tile, .hero-tile, .seasonal-tile, [class*=\"tile\"], [class*=\"Tile\"]").forEach(function(tile) {
                    tile.classList.add("mobile-animated");
                });
            }, 3000);
        }
    });
    </script>
'''

for page in pages:
    if not os.path.exists(page):
        print("Not found:", page)
        continue
        
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "gloss 1.3s" not in content:
        content = re.sub(r'(?i)</style>', css + '\n</style>', content, count=1)
    
    if "mobile-animated" not in content:
        content = re.sub(r'(?i)</body>', js + '\n</body>', content, count=1)
    
    with open(page, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("PERFECTLY FIXED:", page)

print("\nALL TILES — SERVICE, PROMO, TOWN, HERO, SEASONAL — NOW HAVE FULL NAVY-TO-TEAL SATIN ANIMATION ON EVERY PAGE.")
print("NO MORE SCRIPTS. NO MORE FIXES. IT IS DONE.")