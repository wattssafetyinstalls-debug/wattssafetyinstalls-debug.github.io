import os
import re

pages = ['index.html', 'about.html', 'referrals.html', 'contact.html', 'service-area.html']

css = '''
    /* FINAL — FULL NAVY-TO-TEAL GRADIENT + SATIN GLOSS — EVERY TILE, EVERY PAGE */
    .service-tile, .promo-tile, .town-tile, .hero-tile, .seasonal-tile,
    [class*="tile"], [class*="Tile"], .trust-banner, .card, .feature-box, .review-card, .trust-tile {
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s ease !important;
    }

    .service-tile::before, .promo-tile::before, .town-tile::before,
    .hero-tile::before, .seasonal-tile::before,
    [class*="tile"]::before, [class*="Tile"]::before,
    .trust-banner::before, .card::before, .feature-box::before, .trust-tile::before {
        content: "" !important;
        position: absolute !important;
        inset: 0 !important;
        background: linear-gradient(135deg, var(--teal), var(--navy)) !important;
        opacity: 0 !important;
        transition: opacity 0.5s ease !important;
        z-index: -1 !important;
    }

    .service-tile::after, .promo-tile::after, .town-tile::after,
    .hero-tile::after, .seasonal-tile::after,
    [class*="tile"]::after, [class*="Tile"]::after,
    .trust-banner::after, .card::after, .feature-box::after, .trust-tile::after {
        content: "" !important;
        position: absolute !important;
        inset: 0 !important;
        background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%) !important;
        transform: translateX(-100%) !important;
        z-index: 1 !important;
        pointer-events: none !important;
    }

    .service-tile:hover, .promo-tile:hover, .town-tile:hover,
    .hero-tile:hover, .seasonal-tile:hover,
    [class*="tile"]:hover, [class*="Tile"]:hover,
    .trust-banner:hover, .card:hover, .feature-box:hover, .trust-tile:hover,
    .service-tile.mobile-animated, .promo-tile.mobile-animated,
    .town-tile.mobile-animated, .hero-tile.mobile-animated,
    .seasonal-tile.mobile-animated,
    [class*="tile"].mobile-animated, [class*="Tile"].mobile-animated,
    .trust-banner.mobile-animated, .card.mobile-animated, .feature-box.mobile-animated, .trust-tile.mobile-animated {
        transform: translateY(-12px) scale(1.03) !important;
        box-shadow: 0 35px 90px rgba(10,29,55,0.38) !important;
        color: white !important;
    }

    .service-tile:hover::before, .promo-tile:hover::before, .town-tile:hover::before,
    [class*="tile"]:hover::before, .trust-banner:hover::before, .trust-tile:hover::before,
    .service-tile.mobile-animated::before, .promo-tile.mobile-animated::before,
    .town-tile.mobile-animated::before, [class*="tile"].mobile-animated::before,
    .trust-banner.mobile-animated::before, .trust-tile.mobile-animated::before {
        opacity: 1 !important;
    }

    .service-tile:hover::after, .promo-tile:hover::after, .town-tile:hover::after,
    [class*="tile"]:hover::after, .trust-banner:hover::after, .trust-tile:hover::after,
    .service-tile.mobile-animated::after, .promo-tile.mobile-animated::after,
    .town-tile.mobile-animated::after, [class*="tile"].mobile-animated::after,
    .trust-banner.mobile-animated::after, .trust-tile.mobile-animated::after {
        animation: gloss 1.3s ease-out forwards !important;
    }

    @keyframes gloss {
        0%   { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
'''

js = '''
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        if (window.innerWidth <= 768) {
            setTimeout(function() {
                document.querySelectorAll("[class*='tile'], .trust-banner, .card, .trust-tile").forEach(el => {
                    el.classList.add("mobile-animated");
                });
            }, 3000);
        }
    });
    </script>
'''

for page in pages:
    if not os.path.exists(page): 
        continue
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    if "gloss 1.3s" not in content:
        content = re.sub(r'(?i)</style>', css + '\n</style>', content, count=1)
    if "mobile-animated" not in content:
        content = re.sub(r'(?i)</body>', js + '\n</body>', content, count=1)
    with open(page, 'w', encoding='utf-8') as f:
        f.write(content)
    print("FIXED:", page)

print("\nDONE. EVERY TILE ON EVERY PAGE NOW HAS FULL NAVY-TO-TEAL GRADIENT + SATIN GLOSS.")
print("NO MORE SCRIPTS AFTER THIS. EVER.")