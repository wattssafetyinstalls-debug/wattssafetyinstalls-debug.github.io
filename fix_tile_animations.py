import os
import re

def add_tile_animations_to_html(file_path):
    """Add tile animation CSS and JS to an HTML file"""
    
    # The animation CSS to insert
    animation_css = """
    <!-- TILE ANIMATION STYLES -->
    <style>
    /* DESKTOP HOVER EFFECTS */
    .service-tile, .hero-tile, .promo-tile, .town-tile, .service-card {
        position: relative;
        overflow: hidden;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .service-tile::before, .hero-tile::before, .promo-tile::before, .town-tile::before, .service-card::before {
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
    
    .service-tile:hover::before, .hero-tile:hover::before, .promo-tile:hover::before, .town-tile:hover::before, .service-card:hover::before {
        left: 0;
    }
    
    .service-tile > *, .hero-tile > *, .promo-tile > *, .town-tile > *, .service-card > * {
        position: relative;
        z-index: 2;
    }
    
    .service-tile:hover, .hero-tile:hover, .promo-tile:hover, .town-tile:hover, .service-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* SATIN GLOSS SWIPE EFFECT */
    .service-tile::after, .hero-tile::after, .promo-tile::after, .town-tile::after, .service-card::after {
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
    
    .service-tile:hover::after, .hero-tile:hover::after, .promo-tile:hover::after, .town-tile:hover::after, .service-card:hover::after {
        left: 100%;
    }
    
    /* MOBILE AUTO-ANIMATION EFFECTS */
    @media (max-width: 768px) {
        .mobile-animated {
            animation: mobileTileGlow 3s ease-in-out 1;
        }
        
        @keyframes mobileTileGlow {
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
    
    # The animation JavaScript to insert
    animation_js = """
    <!-- TILE ANIMATION SCRIPT -->
    <script>
    // Mobile auto-animation for tiles
    function initTileAnimations() {
        const tiles = document.querySelectorAll('.service-tile, .hero-tile, .promo-tile, .town-tile, .service-card');
        
        // Add touch support for mobile
        tiles.forEach(tile => {
            // Remove any existing mobile-animated class
            tile.classList.remove('mobile-animated');
            
            // Add touch event listeners for mobile
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
            tiles.forEach(tile => {
                setTimeout(() => {
                    tile.classList.add('mobile-animated');
                    // Remove after animation completes
                    setTimeout(() => {
                        tile.classList.remove('mobile-animated');
                    }, 3000);
                }, delay);
                delay += 500; // Stagger animations
            });
            
            // Re-animate when coming back to the page
            document.addEventListener('visibilitychange', function() {
                if (!document.hidden) {
                    setTimeout(() => {
                        let newDelay = 0;
                        tiles.forEach(tile => {
                            setTimeout(() => {
                                tile.classList.add('mobile-animated');
                                setTimeout(() => {
                                    tile.classList.remove('mobile-animated');
                                }, 3000);
                            }, newDelay);
                            newDelay += 500;
                        });
                    }, 1000);
                }
            });
        }
        
        // Debug logging
        console.log('Tile animations initialized for', tiles.length, 'tiles');
    }
    
    // Initialize when DOM is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTileAnimations);
    } else {
        initTileAnimations();
    }
    
    // Re-initialize on page show (for back/forward cache)
    window.addEventListener('pageshow', initTileAnimations);
    </script>
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if animations are already added
        if 'TILE ANIMATION STYLES' in content and 'TILE ANIMATION SCRIPT' in content:
            print("Animations already present in " + os.path.basename(file_path))
            return False
        
        modified = False
        
        # Insert CSS before closing </head> tag
        if '</head>' in content and 'TILE ANIMATION STYLES' not in content:
            content = content.replace('</head>', animation_css + '\n</head>')
            modified = True
        
        # Insert JS before closing </body> tag
        if '</body>' in content and 'TILE ANIMATION SCRIPT' not in content:
            content = content.replace('</body>', animation_js + '\n</body>')
            modified = True
        
        if modified:
            # Write the modified content back
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print("Added tile animations to " + os.path.basename(file_path))
            return True
        else:
            print("No changes needed for " + os.path.basename(file_path))
            return False
        
    except Exception as e:
        print("Error processing " + file_path + ": " + str(e))
        return False

def find_html_files(directory):
    """Find all HTML files in the directory and subdirectories"""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Skip _site directory and backup directories
        dirs[:] = [d for d in dirs if not d.startswith('_site') and 'backup' not in d.lower()]
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def backup_file(file_path):
    """Create a backup of the file"""
    backup_path = file_path + '.backup'
    try:
        with open(file_path, 'r', encoding='utf-8') as original:
            content = original.read()
        with open(backup_path, 'w', encoding='utf-8') as backup:
            backup.write(content)
        return True
    except Exception as e:
        print("Failed to backup " + file_path + ": " + str(e))
        return False

def main():
    print("Tile Animation Fix Script")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    print("Working directory: " + current_dir)
    
    # Find all HTML files
    html_files = find_html_files(current_dir)
    print("Found " + str(len(html_files)) + " HTML files")
    
    if not html_files:
        print("No HTML files found in current directory!")
        return
    
    # Process each HTML file
    successful_files = 0
    for file_path in html_files:
        # Create backup first
        if backup_file(file_path):
            if add_tile_animations_to_html(file_path):
                successful_files += 1
    
    print("=" * 50)
    print("Successfully updated " + str(successful_files) + " out of " + str(len(html_files)) + " files")
    print("")
    print("Next steps:")
    print("1. Run this script: python fix_tile_animations.py")
    print("2. Open your browser in Incognito mode (Ctrl+Shift+N)")
    print("3. Visit http://localhost:8000 to see the animations")
    print("4. Hover over tiles to see navy-to-teal gradient + satin gloss swipe")
    print("5. On mobile/responsive view, tiles will auto-animate every 3 seconds")

if __name__ == "__main__":
    main()