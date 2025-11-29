import os

def fix_carousel_dropdown_readability(file_path):
    """Fix dropdown text readability and last tile mobile optimization"""
    
    fix_css = """
    <!-- CAROUSEL DROPDOWN READABILITY FIX -->
    <style>
    /* FIX DROPDOWN TEXT READABILITY FOR ALL TILES */
    .service-card:hover .service-dropdown,
    .service-card.touch-active .service-dropdown {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .service-card:hover .service-dropdown a,
    .service-card.touch-active .service-dropdown a {
        color: var(--navy) !important;
        text-shadow: none !important;
        font-weight: 600 !important;
        border-bottom: 1px solid rgba(10, 29, 55, 0.1) !important;
    }
    
    .service-card:hover .service-dropdown a:hover,
    .service-card.touch-active .service-dropdown a:hover {
        color: var(--teal) !important;
        background: rgba(0, 196, 180, 0.05) !important;
    }
    
    /* MOBILE LAST TILE OPTIMIZATION */
    @media (max-width: 768px) {
        .service-card:last-child.touch-active .service-dropdown {
            max-height: 800px !important;
            transition: max-height 1.2s ease !important;
            padding: 30px 25px !important;
        }
        
        .service-card:last-child.touch-active .service-title,
        .service-card:last-child.touch-active .service-description {
            color: white !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9) !important;
        }
    }
    </style>
    """
    
    fix_js = """
    <!-- CAROUSEL DROPDOWN FIX SCRIPT -->
    <script>
    // Fix dropdown readability and last tile optimization
    document.addEventListener('DOMContentLoaded', function() {
        const serviceCards = document.querySelectorAll('.service-card');
        const lastCard = serviceCards[serviceCards.length - 1];
        
        // Add touch support for all cards
        serviceCards.forEach(card => {
            let touchTimer;
            
            card.addEventListener('touchstart', function() {
                clearTimeout(touchTimer);
                
                // Different timing for last card
                const delay = card === lastCard ? 400 : 300;
                
                touchTimer = setTimeout(() => {
                    // Close other cards
                    serviceCards.forEach(otherCard => {
                        if (otherCard !== this && otherCard.classList.contains('touch-active')) {
                            otherCard.classList.remove('touch-active');
                        }
                    });
                    
                    // Toggle this card
                    this.classList.toggle('touch-active');
                }, delay);
            });
            
            card.addEventListener('touchend', function() {
                clearTimeout(touchTimer);
            });
        });
        
        // Close dropdown when tapping outside
        document.addEventListener('touchstart', function(e) {
            if (!e.target.closest('.service-card')) {
                serviceCards.forEach(card => {
                    card.classList.remove('touch-active');
                });
            }
        });
        
        console.log('Carousel dropdown readability and last tile optimization applied');
    });
    </script>
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove any existing fixes to avoid duplication
        if 'CAROUSEL DROPDOWN READABILITY FIX' in content:
            start = content.find('<!-- CAROUSEL DROPDOWN READABILITY FIX -->')
            end = content.find('</style>', start) + 8
            content = content[:start] + content[end:]
        
        if 'CAROUSEL DROPDOWN FIX SCRIPT' in content:
            start = content.find('<!-- CAROUSEL DROPDOWN FIX SCRIPT -->')
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
            print(f"SUCCESS: Fixed dropdown readability in {os.path.basename(file_path)}")
            return True
        else:
            print(f"NO CHANGES: {os.path.basename(file_path)}")
            return False
        
    except Exception as e:
        print(f"ERROR: {file_path}: {str(e)}")
        return False

def main():
    print("Fixing Carousel Dropdown Readability & Last Tile")
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
        fix_carousel_dropdown_readability(file_path)
    
    print("\nFIXES APPLIED:")
    print("1. Dropdown menus now have white background with blur effect")
    print("2. Dropdown text is navy color (readable)")
    print("3. Last tile has longer touch delay (400ms)")
    print("4. Last tile has larger dropdown space (800px)")
    print("5. All dropdown links are now clearly visible")
    print("\nReady to push live!")

if __name__ == "__main__":
    main()