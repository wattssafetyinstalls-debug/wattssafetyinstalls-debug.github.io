import os

def fix_all_tile_layouts_and_animations(file_path):
    """Fix tile layouts and add consistent gradient animations to all pages"""
    
    # Comprehensive CSS for all tile layouts and animations
    comprehensive_css = """
    <!-- COMPREHENSIVE TILE LAYOUTS & ANIMATIONS -->
    <style>
    /* 4-GRID LAYOUT FOR ALL MULTI-TILE SECTIONS */
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
        margin: 40px 0;
        justify-content: center;
        max-width: 1300px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* 3-GRID LAYOUT FOR SECTIONS WITH 3 TILES */
    .benefits-grid.three-column {
        grid-template-columns: repeat(3, 1fr);
        max-width: 1000px;
    }
    
    /* TRUST BAR - 4 ITEMS IN A ROW */
    .trust-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
        max-width: 1300px;
        margin: 0 auto;
        justify-content: center;
    }
    
    /* SERVICE CATEGORIES GRID */
    .service-categories {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
        margin: 40px 0;
        justify-content: center;
        max-width: 1300px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* PROMO GRID - 3 COLUMNS */
    .promo-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        max-width: 1300px;
        margin: 0 auto;
        justify-content: center;
    }
    
    /* RESPONSIVE BREAKPOINTS */
    @media (max-width: 1200px) {
        .benefits-grid,
        .trust-container,
        .service-categories {
            grid-template-columns: repeat(2, 1fr);
            max-width: 800px;
        }
        
        .promo-grid {
            grid-template-columns: repeat(2, 1fr);
            max-width: 800px;
        }
        
        .benefits-grid.three-column {
            grid-template-columns: repeat(2, 1fr);
            max-width: 800px;
        }
    }
    
    @media (max-width: 768px) {
        .benefits-grid,
        .trust-container,
        .service-categories,
        .promo-grid,
        .benefits-grid.three-column {
            grid-template-columns: 1fr;
            max-width: 500px;
        }
    }
    
    /* CONSISTENT GRADIENT ANIMATIONS FOR ALL TILES */
    .benefit-card, 
    .value-tile, 
    .service-tile, 
    .trust-item,
    .service-card,
    .promo-card,
    .category-card,
    .contact-tile,
    .area-tile {
        position: relative;
        overflow: hidden;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .benefit-card::before, 
    .value-tile::before, 
    .service-tile::before, 
    .trust-item::before,
    .service-card::before,
    .promo-card::before,
    .category-card::before,
    .contact-tile::before,
    .area-tile::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #0A1D37, #00C4B4);
        transition: left 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        z-index: 1;
    }
    
    .benefit-card:hover::before, 
    .value-tile:hover::before, 
    .service-tile:hover::before, 
    .trust-item:hover::before,
    .service-card:hover::before,
    .promo-card:hover::before,
    .category-card:hover::before,
    .contact-tile:hover::before,
    .area-tile:hover::before {
        left: 0;
    }
    
    .benefit-card > *, 
    .value-tile > *, 
    .service-tile > *, 
    .trust-item > *,
    .service-card > *,
    .promo-card > *,
    .category-card > *,
    .contact-tile > *,
    .area-tile > * {
        position: relative;
        z-index: 2;
    }
    
    .benefit-card:hover, 
    .value-tile:hover, 
    .service-tile:hover, 
    .trust-item:hover,
    .service-card:hover,
    .promo-card:hover,
    .category-card:hover,
    .contact-tile:hover,
    .area-tile:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* SATIN GLOSS SWIPE EFFECT */
    .benefit-card::after, 
    .value-tile::after, 
    .service-tile::after, 
    .trust-item::after,
    .service-card::after,
    .promo-card::after,
    .category-card::after,
    .contact-tile::after,
    .area-tile::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 50%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
        );
        transition: left 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        z-index: 3;
    }
    
    .benefit-card:hover::after, 
    .value-tile:hover::after, 
    .service-tile:hover::after, 
    .trust-item:hover::after,
    .service-card:hover::after,
    .promo-card:hover::after,
    .category-card:hover::after,
    .contact-tile:hover::after,
    .area-tile:hover::after {
        left: 100%;
    }
    
    /* TEXT COLOR OPTIMIZATION */
    .benefit-card:hover *, 
    .value-tile:hover *, 
    .service-tile:hover *, 
    .trust-item:hover *,
    .service-card:hover *,
    .promo-card:hover *,
    .category-card:hover *,
    .contact-tile:hover *,
    .area-tile:hover * {
        color: white !important;
    }
    
    /* MOBILE AUTO-ANIMATIONS */
    @media (max-width: 768px) {
        .mobile-animated {
            animation: tileMobileGlow 3s ease-in-out 1;
        }
        
        @keyframes tileMobileGlow {
            0% {
                box-shadow: 0 0 0 rgba(0, 196, 180, 0);
                transform: translateY(0);
            }
            50% {
                box-shadow: 0 8px 25px rgba(0, 196, 180, 0.3);
                transform: translateY(-5px);
            }
            100% {
                box-shadow: 0 0 0 rgba(0, 196, 180, 0);
                transform: translateY(0);
            }
        }
    }
    </style>
    """
    
    # JavaScript for all tile animations
    comprehensive_js = """
    <!-- COMPREHENSIVE TILE ANIMATION SCRIPT -->
    <script>
    // Mobile auto-animation for all tiles
    function initAllTileAnimations() {
        const allTiles = document.querySelectorAll(
            '.benefit-card, .value-tile, .service-tile, .trust-item, ' +
            '.service-card, .promo-card, .category-card, .contact-tile, .area-tile'
        );
        
        console.log('Animating ' + allTiles.length + ' tiles across all pages');
        
        // Add touch support for mobile
        allTiles.forEach(tile => {
            tile.classList.remove('mobile-animated');
            
            // Touch events for mobile
            tile.addEventListener('touchstart', function() {
                this.style.transform = 'translateY(-5px)';
            });
            
            tile.addEventListener('touchend', function() {
                this.style.transform = '';
            });
        });
        
        // Auto-animate tiles on mobile
        if (window.matchMedia("(max-width: 768px)").matches) {
            let delay = 0;
            allTiles.forEach(tile => {
                setTimeout(() => {
                    tile.classList.add('mobile-animated');
                    setTimeout(() => {
                        tile.classList.remove('mobile-animated');
                    }, 3000);
                }, delay);
                delay += 300;
            });
        }
    }
    
    // Initialize when DOM loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAllTileAnimations);
    } else {
        initAllTileAnimations();
    }
    
    // Re-initialize on page show
    window.addEventListener('pageshow', initAllTileAnimations);
    
    // Animate when tiles come into view
    function animateTilesOnScroll() {
        const allTiles = document.querySelectorAll(
            '.benefit-card, .value-tile, .service-tile, .trust-item, ' +
            '.service-card, .promo-card, .category-card, .contact-tile, .area-tile'
        );
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && window.matchMedia("(max-width: 768px)").matches) {
                    entry.target.classList.add('mobile-animated');
                    setTimeout(() => {
                        entry.target.classList.remove('mobile-animated');
                    }, 3000);
                }
            });
        }, { threshold: 0.3 });
        
        allTiles.forEach(tile => {
            observer.observe(tile);
        });
    }
    
    // Start scroll animation observer
    if (window.matchMedia("(max-width: 768px)").matches) {
        document.addEventListener('DOMContentLoaded', animateTilesOnScroll);
    }
    </script>
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove any previous versions to avoid duplication
        if 'COMPREHENSIVE TILE LAYOUTS & ANIMATIONS' in content:
            # Remove old CSS
            start = content.find('<!-- COMPREHENSIVE TILE LAYOUTS & ANIMATIONS -->')
            end = content.find('</style>', start) + 8
            content = content[:start] + content[end:]
        
        if 'COMPREHENSIVE TILE ANIMATION SCRIPT' in content:
            # Remove old JS
            start = content.find('<!-- COMPREHENSIVE TILE ANIMATION SCRIPT -->')
            end = content.find('</script>', start) + 9
            content = content[:start] + content[end:]
        
        modified = False
        new_content = content
        
        # Insert CSS before closing </head> tag
        if '</head>' in new_content:
            new_content = new_content.replace('</head>', comprehensive_css + '\n</head>')
            modified = True
        
        # Insert JS before closing </body> tag
        if '</body>' in new_content:
            new_content = new_content.replace('</body>', comprehensive_js + '\n</body>')
            modified = True
        
        if modified:
            # Write the modified content back
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print("Applied comprehensive tile layouts and animations to " + os.path.basename(file_path))
            return True
        else:
            print("No changes needed for " + os.path.basename(file_path))
            return False
        
    except Exception as e:
        print("Error processing " + file_path + ": " + str(e))
        return False

def main():
    print("Comprehensive Tile Layouts & Animations")
    print("=" * 60)
    
    # Get current directory
    current_dir = os.getcwd()
    print("Working directory: " + current_dir)
    
    # Target all main pages that need tile fixes
    target_files = [
        'referrals.html', 
        'about.html', 
        'service-area.html', 
        'contact.html',
        'index.html',
        'services.html'
    ]
    
    html_files = []
    
    for file in target_files:
        if os.path.exists(file):
            html_files.append(file)
        else:
            print("File not found: " + file)
    
    print("Found " + str(len(html_files)) + " target files")
    
    if not html_files:
        print("No target files found!")
        return
    
    # Process each file
    successful_files = 0
    for file_path in html_files:
        if fix_all_tile_layouts_and_animations(file_path):
            successful_files += 1
    
    print("=" * 60)
    print("Successfully updated " + str(successful_files) + " out of " + str(len(html_files)) + " files")
    
    # Local testing instructions
    print("\n" + "=" * 60)
    print("TESTING INSTRUCTIONS:")
    print("1. Restart server: python redirect_pretty_url_server.py")
    print("2. Check referrals.html: 3 benefit cards centered, 4 benefit cards in 4-column grid")
    print("3. Check about.html: ALL tiles have gradient animations")
    print("4. Check service-area.html: ALL tiles have gradient animations") 
    print("5. Check contact.html: ALL tiles have gradient animations")
    print("6. Verify all grids are properly centered and responsive")

if __name__ == "__main__":
    main()