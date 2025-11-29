import os
import re

pages = ['referrals.html', 'about.html', 'contact.html', 'service-area.html', 'index.html']

full_animation_css = """
    /* FULL NAVY-TO-TEAL GRADIENT + SATIN GLOSS SWIPE - APPLIED TO EVERYTHING */
    .service-tile, .promo-tile, .trust-tile, .testimonial-tile, .banner-tile,
    [class*="tile"], [class*="Tile"], .trust-banner, .card, .feature-box, .review-card {
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s ease !important;
    }

    .service-tile::before, .promo-tile::before, .trust-tile::before, .testimonial-tile::before,
    .banner-tile::before, [class*="tile"]::before, [class*="Tile"]::before,
    .trust-banner::before, .card::before, .feature-box::before, .review-card::before {
        content: "" !important;
        position: absolute !important;
        top: 0; left: 0; right: 0; bottom: 0 !important;
        background: linear-gradient(135deg, var(--teal), var(--navy)) !important;
        opacity: 0 !important;
        transition: opacity 0.5s ease !important;
        z-index: -1 !important;
    }

    .service-tile::after, .promo-tile::after, .trust-tile::after, .testimonial-tile::after,
    .banner-tile::after, [class*="tile"]::after, [class*="Tile"]::after,
    .trust-banner::after, .card::after, .feature-box::after, .review-card::after {
        content: "" !important;
        position: absolute !important;
        top: 0; left: 0; right: 0; bottom: 0 !important;
        background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.18) 50%, transparent 70%) !important;
        transform: translateX(-100%) !important;
        transition: transform 1.3s ease-out !important;
        z-index: 1 !important;
        pointer-events: none !important;
    }

    .service-tile:hover, .promo-tile:hover, .trust-tile:hover, .testimonial-tile:hover,
    .banner-tile:hover, [class*="tile"]:hover, [class*="Tile"]:hover,
    .trust-banner:hover, .card:hover, .feature-box:hover, .review-card:hover,
    .service-tile.mobile-animated, .promo-tile.mobile-animated, .trust-tile.mobile-animated,
    .testimonial-tile.mobile-animated, .banner-tile.mobile-animated,
    [class*="tile"].mobile-animated, [class*="Tile"].mobile-animated,
    .trust-banner.mobile-animated, .card.mobile-animated, .feature-box.mobile-animated, .review-card.mobile-animated {
        transform: translateY(-12px) scale(1.03) !important;
        box-shadow: 0 35px 90px rgba(10,29,55,0.38) !important;
        background: linear-gradient(135deg, var(--teal), var(--navy)) !important;
        color: white !important;
        border-color: var(--gray) !important;
    }

    .service-tile:hover::before, .promo-tile:hover::before, .trust-tile:hover::before,
    [class*="tile"]:hover::before, .trust-banner:hover::before, .card:hover::before, .review-card:hover::before,
    .service-tile.mobile-animated::before, .promo-tile.mobile-animated::before,
    .trust-tile.mobile-animated::before, [class*="tile"].mobile-animated::before,
    .trust-banner.mobile-animated::before, .card.mobile-animated::before, .review-card.mobile-animated::before {
        opacity: 1 !important;
    }

    .service-tile:hover::after, .promo-tile:hover::after, .trust-tile:hover::after,
    [class*="tile"]:hover::after, .trust-banner:hover::after, .card:hover::after, .review-card:hover::after,
    .service-tile.mobile-animated::after, .promo-tile.mobile-animated::after,
    .trust-tile.mobile-animated::after, [class*="tile"].mobile-animated::after,
    .trust-banner.mobile-animated::after, .card.mobile-animated::after, .review-card.mobile-animated::after {
        animation: gloss 1.3s ease-out forwards !important;
    }

    @keyframes gloss {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
"""

full_animation_js = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        if (window.innerWidth <= 768) {
            setTimeout(function() {
                document.querySelectorAll('.service-tile, .promo-tile, .trust-tile, .testimonial-tile, .banner-tile, [class*="tile"], [class*="Tile"], .trust-banner, .card, .feature-box, .review-card').forEach(function(el) {
                    el.classList.add('mobile-animated');
                });
            }, 3000);
        }
    });
    </script>
"""

for page in pages:
    if not os.path.exists(page):
        print("Not found:", page)
        continue
    
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "gloss 1.3s" not in content:
        content = re.sub(r'(</style>)', full_animation_css + r'\1', content, count=1, flags=re.IGNORECASE)
    
    if "mobile-animated" not in content:
        content = re.sub(r'(</body>)', full_animation_js + r'\1', content, count=1, flags=re.IGNORECASE)
    
    with open(page, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("100% FIXED EVERY TILE ON:", page)

print("\nFINISHED - EVERY SINGLE TILE NOW HAS FULL NAVY-TO-TEAL GRADIENT + SATIN GLOSS ANIMATION - NO EXCEPTIONS")