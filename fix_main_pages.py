import os

pages = ['referrals.html', 'about.html', 'contact.html', 'service-area.html']

for page in pages:
    if not os.path.exists(page):
        print("Missing:", page)
        continue
    
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add CSS if missing
    if "MOBILE AUTO-ANIMATION EFFECTS" not in content:
        css_to_add = """
        /* MOBILE AUTO-ANIMATION EFFECTS + DESKTOP HOVER */
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
        .service-tile:hover::before, .promo-tile:hover::before, .tile:hover::before,
        .service-tile.mobile-animated::before, .promo-tile.mobile-animated::before, .tile.mobile-animated::before {
            opacity: 1;
        }
        .service-tile:hover, .promo-tile:hover, .tile:hover,
        .service-tile.mobile-animated, .promo-tile.mobile-animated, .tile.mobile-animated {
            transform: translateY(-12px) scale(1.03);
            box-shadow: 0 35px 90px rgba(10,29,55,0.38);
            color: white !important;
        }
        .service-tile.mobile-animated h2, .service-tile.mobile-animated p,
        .promo-tile.mobile-animated h2, .promo-tile.mobile-animated p { 
            color: white !important; 
        }
        """
        content = content.replace('</style>', css_to_add + '\n    </style>')
    
    # Add JS if missing
    if "Mobile auto-animation after 3 seconds" not in content:
        js_to_add = """
        <script>
        // Mobile auto-animation after 3 seconds (same as service pages)
        document.addEventListener('DOMContentLoaded', function() {
            if (window.innerWidth <= 768) {
                setTimeout(function() {
                    document.querySelectorAll('.service-tile, .promo-tile, .tile').forEach(tile => {
                        tile.classList.add('mobile-animated');
                    });
                }, 3000);
            }
        });
        </script>
        """
        content = content.replace('</body>', js_to_add + '\n</body>')
    
    with open(page, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed ->", page)

print("\nAll 4 pages now have identical desktop hover + mobile animation!")