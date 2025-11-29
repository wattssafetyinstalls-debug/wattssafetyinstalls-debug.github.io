import os

def fix_seasonal_promo_animations(file_path):
    """Add specific animations to seasonal promo cards only"""
    
    # CSS specifically for seasonal promo cards
    promo_css = """
    <!-- SEASONAL PROMO ANIMATIONS -->
    <style>
    /* Seasonal promo card animations */
    .promo-card {
        position: relative;
        overflow: hidden;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
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
    
    .promo-card:hover::before {
        left: 0;
    }
    
    .promo-card > * {
        position: relative;
        z-index: 2;
    }
    
    .promo-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Satin gloss swipe for promo cards */
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
    
    .promo-card:hover::after {
        left: 100%;
    }
    
    /* Text color optimization for promo cards on hover */
    .promo-card:hover .promo-title,
    .promo-card:hover .promo-description {
        color: white !important;
    }
    
    .promo-card:hover .promo-code {
        background: var(--gold) !important;
        color: var(--navy) !important;
    }
    
    .promo-card:hover .promo-cta {
        background: white !important;
        color: var(--teal) !important;
    }
    
    /* Mobile auto-animation for promo cards */
    @media (max-width: 768px) {
        .promo-card.mobile-animated {
            animation: promoMobileGlow 3s ease-in-out 1;
        }
        
        @keyframes promoMobileGlow {
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
    
    # JavaScript specifically for seasonal promo cards
    promo_js = """
    <!-- SEASONAL PROMO ANIMATION SCRIPT -->
    <script>
    // Mobile auto-animation for seasonal promo cards
    function initPromoAnimations() {
        const promoCards = document.querySelectorAll('.promo-card');
        
        console.log('Found ' + promoCards.length + ' seasonal promo cards');
        
        // Add touch support for mobile
        promoCards.forEach(card => {
            card.classList.remove('mobile-animated');
            
            // Touch events for mobile
            card.addEventListener('touchstart', function() {
                this.style.transform = 'translateY(-5px)';
            });
            
            card.addEventListener('touchend', function() {
                this.style.transform = '';
            });
        });
        
        // Auto-animate promo cards on mobile
        if (window.matchMedia("(max-width: 768px)").matches) {
            let delay = 0;
            promoCards.forEach(card => {
                setTimeout(() => {
                    card.classList.add('mobile-animated');
                    setTimeout(() => {
                        card.classList.remove('mobile-animated');
                    }, 3000);
                }, delay);
                delay += 500;
            });
            
            // Re-animate when page becomes visible again
            document.addEventListener('visibilitychange', function() {
                if (!document.hidden) {
                    setTimeout(() => {
                        let newDelay = 0;
                        promoCards.forEach(card => {
                            setTimeout(() => {
                                card.classList.add('mobile-animated');
                                setTimeout(() => {
                                    card.classList.remove('mobile-animated');
                                }, 3000);
                            }, newDelay);
                            newDelay += 500;
                        });
                    }, 1000);
                }
            });
        }
    }
    
    // Initialize when DOM loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPromoAnimations);
    } else {
        initPromoAnimations();
    }
    
    // Re-initialize on page show
    window.addEventListener('pageshow', initPromoAnimations);
    
    // Also animate when promo cards come into view
    function animatePromoOnScroll() {
        const promoCards = document.querySelectorAll('.promo-card');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && window.matchMedia("(max-width: 768px)").matches) {
                    entry.target.classList.add('mobile-animated');
                    setTimeout(() => {
                        entry.target.classList.remove('mobile-animated');
                    }, 3000);
                }
            });
        }, { threshold: 0.5 });
        
        promoCards.forEach(card => {
            observer.observe(card);
        });
    }
    
    // Start scroll animation observer
    if (window.matchMedia("(max-width: 768px)").matches) {
        document.addEventListener('DOMContentLoaded', animatePromoOnScroll);
    }
    </script>
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if seasonal promo animations are already added
        if 'SEASONAL PROMO ANIMATIONS' in content and 'SEASONAL PROMO ANIMATION SCRIPT' in content:
            print("Seasonal promo animations already present in " + os.path.basename(file_path))
            return False
        
        modified = False
        new_content = content
        
        # Insert CSS before closing </head> tag
        if '</head>' in new_content and 'SEASONAL PROMO ANIMATIONS' not in new_content:
            new_content = new_content.replace('</head>', promo_css + '\n</head>')
            modified = True
        
        # Insert JS before closing </body> tag
        if '</body>' in new_content and 'SEASONAL PROMO ANIMATION SCRIPT' not in new_content:
            new_content = new_content.replace('</body>', promo_js + '\n</body>')
            modified = True
        
        if modified:
            # Write the modified content back
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print("Added seasonal promo animations to " + os.path.basename(file_path))
            return True
        else:
            print("No changes needed for " + os.path.basename(file_path))
            return False
        
    except Exception as e:
        print("Error processing " + file_path + ": " + str(e))
        return False

def find_services_html_files(directory):
    """Find services.html and other main pages that might have seasonal promos"""
    target_files = []
    for root, dirs, files in os.walk(directory):
        # Skip _site and backup directories
        dirs[:] = [d for d in dirs if not d.startswith('_site') and 'backup' not in d.lower()]
        
        for file in files:
            if file in ['services.html', 'index.html', 'service-area.html'] and not file.startswith('test_'):
                target_files.append(os.path.join(root, file))
    return target_files

def main():
    print("Seasonal Promo Animation Fix")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    print("Working directory: " + current_dir)
    
    # Find target HTML files
    html_files = find_services_html_files(current_dir)
    print("Found " + str(len(html_files)) + " target files")
    
    if not html_files:
        print("No target files found!")
        return
    
    # Process each file
    successful_files = 0
    for file_path in html_files:
        if fix_seasonal_promo_animations(file_path):
            successful_files += 1
    
    print("=" * 50)
    print("Successfully updated " + str(successful_files) + " out of " + str(len(html_files)) + " files")
    print("")
    print("Testing instructions:")
    print("1. Start server: python redirect_pretty_url_server.py")
    print("2. Open http://localhost:8000/services.html in Incognito (Ctrl+Shift+N)")
    print("3. Scroll to bottom to seasonal promo cards (Winter Snow Removal, Lawn Care, Fall Cleanup)")
    print("4. Hover over them - should see navy-to-teal gradient + satin gloss")
    print("5. Text should turn white on hover for better contrast")
    print("6. Test mobile view (F12 > Ctrl+Shift+M) - cards should auto-animate when scrolling into view")

if __name__ == "__main__":
    main()