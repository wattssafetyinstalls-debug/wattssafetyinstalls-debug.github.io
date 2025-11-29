import os

def center_benefit_tiles_and_fix_about(file_path):
    """Center the 3 benefit tiles in referrals.html and ensure about.html has gradient effects"""
    
    # CSS to center the 3 benefit tiles and apply gradients to about.html
    fix_css = """
    <!-- CENTER 3 BENEFIT TILES & ABOUT PAGE GRADIENTS -->
    <style>
    /* CENTER THE 3 BENEFIT TILES IN REFERRALS.HTML */
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin: 40px 0;
        justify-content: center;
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }
    
    @media (max-width: 1024px) {
        .benefits-grid {
            grid-template-columns: repeat(2, 1fr);
            max-width: 800px;
        }
    }
    
    @media (max-width: 768px) {
        .benefits-grid {
            grid-template-columns: 1fr;
            max-width: 500px;
        }
    }
    
    /* GRADIENT ANIMATIONS FOR ALL TILES IN ABOUT.HTML */
    .benefit-card, 
    .value-tile, 
    .service-tile, 
    .trust-item,
    .service-card,
    .promo-card {
        position: relative;
        overflow: hidden;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .benefit-card::before, 
    .value-tile::before, 
    .service-tile::before, 
    .trust-item::before,
    .service-card::before,
    .promo-card::before {
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
    .promo-card:hover::before {
        left: 0;
    }
    
    .benefit-card > *, 
    .value-tile > *, 
    .service-tile > *, 
    .trust-item > *,
    .service-card > *,
    .promo-card > * {
        position: relative;
        z-index: 2;
    }
    
    .benefit-card:hover, 
    .value-tile:hover, 
    .service-tile:hover, 
    .trust-item:hover,
    .service-card:hover,
    .promo-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* SATIN GLOSS SWIPE EFFECT */
    .benefit-card::after, 
    .value-tile::after, 
    .service-tile::after, 
    .trust-item::after,
    .service-card::after,
    .promo-card::after {
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
    .promo-card:hover::after {
        left: 100%;
    }
    
    /* TEXT COLOR OPTIMIZATION */
    .benefit-card:hover *, 
    .value-tile:hover *, 
    .service-tile:hover *, 
    .trust-item:hover *,
    .service-card:hover *,
    .promo-card:hover * {
        color: white !important;
    }
    
    /* MOBILE AUTO-ANIMATIONS */
    @media (max-width: 768px) {
        .benefit-card.mobile-animated,
        .value-tile.mobile-animated,
        .service-tile.mobile-animated,
        .trust-item.mobile-animated,
        .service-card.mobile-animated,
        .promo-card.mobile-animated {
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
    
    # JavaScript for tile animations
    tile_js = """
    <!-- TILE ANIMATION SCRIPT -->
    <script>
    // Mobile auto-animation for all tiles
    function initTileAnimations() {
        const allTiles = document.querySelectorAll('.benefit-card, .value-tile, .service-tile, .trust-item, .service-card, .promo-card');
        
        console.log('Animating ' + allTiles.length + ' tiles');
        
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
        document.addEventListener('DOMContentLoaded', initTileAnimations);
    } else {
        initTileAnimations();
    }
    
    // Re-initialize on page show
    window.addEventListener('pageshow', initTileAnimations);
    
    // Animate when tiles come into view
    function animateTilesOnScroll() {
        const allTiles = document.querySelectorAll('.benefit-card, .value-tile, .service-tile, .trust-item, .service-card, .promo-card');
        
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
        
        # Check if fixes are already added
        if 'CENTER 3 BENEFIT TILES & ABOUT PAGE GRADIENTS' in content and 'TILE ANIMATION SCRIPT' in content:
            print("Centering and animations already present in " + os.path.basename(file_path))
            return False
        
        modified = False
        new_content = content
        
        # Insert CSS before closing </head> tag
        if '</head>' in new_content and 'CENTER 3 BENEFIT TILES & ABOUT PAGE GRADIENTS' not in new_content:
            new_content = new_content.replace('</head>', fix_css + '\n</head>')
            modified = True
        
        # Insert JS before closing </body> tag
        if '</body>' in new_content and 'TILE ANIMATION SCRIPT' not in new_content:
            new_content = new_content.replace('</body>', tile_js + '\n</body>')
            modified = True
        
        if modified:
            # Write the modified content back
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print("Applied centering and gradient animations to " + os.path.basename(file_path))
            return True
        else:
            print("No changes needed for " + os.path.basename(file_path))
            return False
        
    except Exception as e:
        print("Error processing " + file_path + ": " + str(e))
        return False

def main():
    print("Center 3 Benefit Tiles & Fix About Page")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    print("Working directory: " + current_dir)
    
    # Target only these two files
    target_files = ['referrals.html', 'about.html']
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
        if center_benefit_tiles_and_fix_about(file_path):
            successful_files += 1
    
    print("=" * 50)
    print("Successfully updated " + str(successful_files) + " out of " + str(len(html_files)) + " files")
    
    # Local testing instructions
    print("\n" + "=" * 50)
    print("TESTING INSTRUCTIONS:")
    print("1. Restart server: python redirect_pretty_url_server.py")
    print("2. Check referrals.html: http://localhost:8000/referrals")
    print("   - The 3 'Why Choose Watts Safety Installs' tiles should be centered")
    print("   - They should have navy-to-teal gradient on hover")
    print("3. Check about.html: http://localhost:8000/about") 
    print("   - ALL tiles should have navy-to-teal gradient animations")
    print("4. Test mobile view for both pages")

if __name__ == "__main__":
    main()