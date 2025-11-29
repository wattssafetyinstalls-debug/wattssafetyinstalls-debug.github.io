import os

pages = ['referrals.html', 'about.html', 'contact.html', 'service-area.html']

for page in pages:
    if not os.path.exists(page):
        print("Missing:", page)
        continue
    
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # FULL exact CSS from your working service pages (gradient + satin gloss + glow)
    if "MOBILE AUTO-ANIMATION EFFECTS" not in content:
        full_css = """
        /* === EXACT SAME MOBILE AUTO-ANIMATION + DESKTOP HOVER FROM SERVICE PAGES === */
        .service-tile, .promo-tile, .tile {
            position: relative;
            overflow: hidden;
            transition: all 0.4s ease;
        }
        .service-tile::before, .promo-tile::before, .tile::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, var(--teal), var(--navy));
            opacity: 0;
            transition: opacity 0.5s ease;
            z-index: -1;
        }
        .service-tile::after, .promo-tile::after, .tile::after {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.15) 50%, transparent 70%);
            transform: translateX(-100%);
            transition: transform 1.3s ease-out;
            z-index: 1;
        }
        .service-tile:hover::before, .promo-tile:hover::before, .tile:hover::before,
        .service-tile.mobile-animated::before, .promo-tile.mobile-animated::before, .tile.mobile-animated::before {
            opacity: 1;
        }
        .service-tile:hover::after, .promo-tile:hover::after, .tile:hover::after,
        .service-tile.mobile-animated::after, .promo-tile.mobile-animated::after, .tile.mobile-animated::after {
            transform: translateX(100%);
            animation: gloss 1.3s ease-out forwards;
        }
        @keyframes gloss {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        .service-tile:hover, .promo-tile:hover, .tile:hover,
        .service-tile.mobile-animated, .promo-tile.mobile-animated, .tile.mobile-animated {
            transform: translateY(-12px) scale(1.03);
            box-shadow: 0 35px 90px rgba(10,29,55,0.38);
            background: linear-gradient(135deg, var(--teal), var(--navy));
            color: white !important;
            border-color: var(--gray);
        }
        .service-tile.mobile-animated .trust-icon,
        .promo-tile.mobile-animated .trust-icon,
        .tile.mobile-animated .trust-icon {
            transform: scale(1.5) translateY(-8px);
            color: var(--gold) !important;
        }
        """
        content = content.replace('</style>', full_css + '\n    </style>')
    
    # FULL exact JS from your working service pages
    if "Mobile auto-animation after 3 seconds" not in content:
        full_js = """
        <script>
        // Exact same mobile auto-animation your service pages use
        document.addEventListener('DOMContentLoaded', function() {
            if (window.innerWidth <= 768) {
                setTimeout(function() {
                    document.querySelectorAll('.service-tile, .promo-tile, .tile').forEach(tile => {
                        tile.classList.add('mobile-animated');
                        console.log('Mobile animation applied');
                    });
                }, 3000);
            }
        });
        </script>
        """
        content = content.replace('</body>', full_js + '\n</body>')
    
    with open(page, 'w', encoding='utf-8') as f:
        f.write(content)
    print("FULLY FIXED ->", page)

print("\nDone! referrals / about / contact / service-area now have the EXACT same navy-to-teal satin glow animation as your service pages.")