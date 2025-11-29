import os

def fix_last_carousel_tile_mobile(file_path):
    """Fix only the last service tile in mobile carousel"""
    
    fix_css = """
    <!-- MOBILE LAST CAROUSEL TILE FIX -->
    <style>
    @media (max-width: 768px) {
        /* ONLY target the last service card in carousel on mobile */
        .service-card:last-child.touch-active .service-dropdown {
            max-height: 800px !important;
            transition: max-height 1.2s ease !important;
            padding: 30px 25px !important;
        }
        
        /* Keep text readable for last tile only */
        .service-card:last-child.touch-active .service-title,
        .service-card:last-child.touch-active .service-description {
            color: white !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9) !important;
        }
        
        /* Make dropdown links more visible in last tile */
        .service-card:last-child.touch-active .service-dropdown a {
            color: white !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8) !important;
            font-weight: 600 !important;
            padding: 14px 0 !important;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3) !important;
        }
    }
    </style>
    """
    
    fix_js = """
    <!-- MOBILE LAST TILE FIX SCRIPT -->
    <script>
    // Only fix the last carousel tile on mobile
    if (window.matchMedia("(max-width: 768px)").matches) {
        document.addEventListener('DOMContentLoaded', function() {
            const serviceCards = document.querySelectorAll('.service-card');
            const lastCard = serviceCards[serviceCards.length - 1];
            
            if (lastCard) {
                let lastCardTouchTimer;
                
                lastCard.addEventListener('touchstart', function() {
                    clearTimeout(lastCardTouchTimer);
                    lastCardTouchTimer = setTimeout(() => {
                        // Close other cards
                        serviceCards.forEach(otherCard => {
                            if (otherCard !== this && otherCard.classList.contains('touch-active')) {
                                otherCard.classList.remove('touch-active');
                            }
                        });
                        
                        // Toggle this card with longer delay
                        this.classList.toggle('touch-active');
                    }, 400); // Longer delay for last card only
                });
                
                lastCard.addEventListener('touchend', function() {
                    clearTimeout(lastCardTouchTimer);
                });
            }
            
            console.log('Last carousel tile mobile optimization applied');
        });
    }
    </script>
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove any existing fixes to avoid duplication
        if 'MOBILE LAST CAROUSEL TILE FIX' in content:
            start = content.find('<!-- MOBILE LAST CAROUSEL TILE FIX -->')
            end = content.find('</style>', start) + 8
            content = content[:start] + content[end:]
        
        if 'MOBILE LAST TILE FIX SCRIPT' in content:
            start = content.find('<!-- MOBILE LAST TILE FIX SCRIPT -->')
            end = content.find('</script>', start) + 9
            content = content[:start] + content[end:]
        
        modified = False
        new_content = content
        
        # Insert CSS before closing </head> tag
        if '</head>' in new_content:
            new_content = new_content.replace('</head>', fix_css + '\n</head>')
            modified = True
        
        # Insert JS before closing </body> tag
        if '</body>' in new_content:
            new_content = new_content.replace('</body>', fix_js + '\n</body>')
            modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Fixed last carousel tile in {os.path.basename(file_path)}")
            return True
        else:
            print(f"No changes needed for {os.path.basename(file_path)}")
            return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def main():
    print("Fixing Last Carousel Tile - Mobile Only")
    print("=" * 50)
    
    # Target the services page specifically
    target_files = ['services.html', 'services/index.html']
    
    html_files = []
    for file in target_files:
        if os.path.exists(file):
            html_files.append(file)
    
    if not html_files:
        print("Services page not found!")
        return
    
    for file_path in html_files:
        if fix_last_carousel_tile_mobile(file_path):
            print(f"✓ Successfully updated last tile in {os.path.basename(file_path)}")
    
    print("\nChanges made to LAST TILE ONLY:")
    print("1. Longer touch delay (400ms vs 300ms)")
    print("2. Larger dropdown max-height (800px)")
    print("3. Smoother transition (1.2s)")
    print("4. Better text readability with shadows")
    print("5. More visible dropdown links")
    print("\nAll other tiles remain unchanged!")

if __name__ == "__main__":
    main()