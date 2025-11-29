import os

def fix_mobile_carousel_and_benefit_cards(file_path):
    """Fix mobile carousel dropdown and add animations to benefit cards"""
    
    # CSS to fix mobile carousel and add benefit card animations
    fix_css = """
    <!-- MOBILE CAROUSEL FIX & BENEFIT CARD ANIMATIONS -->
    <style>
    /* FIX: Mobile carousel dropdown background */
    @media (max-width: 768px) {
        .service-card.touch-active .service-dropdown {
            background: linear-gradient(135deg, #0A1D37, #00C4B4) !important;
            color: white !important;
        }
        
        .service-card.touch-active .service-dropdown a {
            color: white !important;
            border-bottom: 1px solid rgba(255,255,255,0.2) !important;
        }
        
        .service-card.touch-active .service-dropdown a:hover {
            background: rgba(255,255,255,0.1) !important;
            color: var(--gold) !important;
        }
    }

    /* BENEFIT CARD ANIMATIONS - Same as service tiles */
    .benefit-card {
        position: relative;
        overflow: hidden;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .benefit-card::before {
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
    
    .benefit-card:hover::before {
        left: 0;
    }
    
    .benefit-card > * {
        position: relative;
        z-index: 2;
    }
    
    .benefit-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* SATIN GLOSS SWIPE FOR BENEFIT CARDS */
    .benefit-card::after {
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
    
    .benefit-card:hover::after {
        left: 100%;
    }
    
    /* TEXT COLOR OPTIMIZATION FOR BENEFIT CARDS */
    .benefit-card:hover .benefit-icon,
    .benefit-card:hover h3,
    .benefit-card:hover p {
        color: white !important;
    }
    
    /* MOBILE AUTO-ANIMATION FOR BENEFIT CARDS */
    @media (max-width: 768px) {
        .benefit-card.mobile-animated {
            animation: benefitMobileGlow 3s ease-in-out 1;
        }
        
        @keyframes benefitMobileGlow {
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
    
    # JavaScript for benefit card animations
    benefit_js = """
    <!-- BENEFIT CARD ANIMATION SCRIPT -->
    <script>
    // Mobile auto-animation for benefit cards
    function initBenefitAnimations() {
        const benefitCards = document.querySelectorAll('.benefit-card');
        
        console.log('Found ' + benefitCards.length + ' benefit cards');
        
        // Add touch support for mobile
        benefitCards.forEach(card => {
            card.classList.remove('mobile-animated');
            
            // Touch events for mobile
            card.addEventListener('touchstart', function() {
                this.style.transform = 'translateY(-5px)';
            });
            
            card.addEventListener('touchend', function() {
                this.style.transform = '';
            });
        });
        
        // Auto-animate benefit cards on mobile
        if (window.matchMedia("(max-width: 768px)").matches) {
            let delay = 0;
            benefitCards.forEach(card => {
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
                        benefitCards.forEach(card => {
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
        document.addEventListener('DOMContentLoaded', initBenefitAnimations);
    } else {
        initBenefitAnimations();
    }
    
    // Re-initialize on page show
    window.addEventListener('pageshow', initBenefitAnimations);
    
    // Also animate when benefit cards come into view
    function animateBenefitOnScroll() {
        const benefitCards = document.querySelectorAll('.benefit-card');
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
        
        benefitCards.forEach(card => {
            observer.observe(card);
        });
    }
    
    // Start scroll animation observer
    if (window.matchMedia("(max-width: 768px)").matches) {
        document.addEventListener('DOMContentLoaded', animateBenefitOnScroll);
    }
    </script>
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if fixes are already added
        if 'MOBILE CAROUSEL FIX & BENEFIT CARD ANIMATIONS' in content and 'BENEFIT CARD ANIMATION SCRIPT' in content:
            print("Mobile carousel fix and benefit animations already present in " + os.path.basename(file_path))
            return False
        
        modified = False
        new_content = content
        
        # Insert CSS before closing </head> tag
        if '</head>' in new_content and 'MOBILE CAROUSEL FIX & BENEFIT CARD ANIMATIONS' not in new_content:
            new_content = new_content.replace('</head>', fix_css + '\n</head>')
            modified = True
        
        # Insert JS before closing </body> tag
        if '</body>' in new_content and 'BENEFIT CARD ANIMATION SCRIPT' not in new_content:
            new_content = new_content.replace('</body>', benefit_js + '\n</body>')
            modified = True
        
        if modified:
            # Write the modified content back
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print("Added mobile carousel fix and benefit animations to " + os.path.basename(file_path))
            return True
        else:
            print("No changes needed for " + os.path.basename(file_path))
            return False
        
    except Exception as e:
        print("Error processing " + file_path + ": " + str(e))
        return False

def find_all_html_files(directory):
    """Find all HTML files that need fixes"""
    target_files = []
    for root, dirs, files in os.walk(directory):
        # Skip _site and backup directories
        dirs[:] = [d for d in dirs if not d.startswith('_site') and 'backup' not in d.lower()]
        
        for file in files:
            if file.endswith('.html') and not file.startswith('test_'):
                target_files.append(os.path.join(root, file))
    return target_files

def main():
    print("Mobile Carousel Fix & Benefit Card Animations")
    print("=" * 60)
    
    # Get current directory
    current_dir = os.getcwd()
    print("Working directory: " + current_dir)
    
    # Find all HTML files
    html_files = find_all_html_files(current_dir)
    print("Found " + str(len(html_files)) + " HTML files")
    
    if not html_files:
        print("No HTML files found!")
        return
    
    # Process each file
    successful_files = 0
    for file_path in html_files:
        if fix_mobile_carousel_and_benefit_cards(file_path):
            successful_files += 1
    
    print("=" * 60)
    print("Successfully updated " + str(successful_files) + " out of " + str(len(html_files)) + " files")
    
    # Git commands to push live
    print("\n" + "=" * 60)
    print("TO PUSH UPDATES LIVE, RUN THESE COMMANDS:")
    print("git add .")
    print("git commit -m \"Fix mobile carousel dropdown and add benefit card animations\"")
    print("git push origin main")
    print("\nThen check your live site in 1-2 minutes!")

if __name__ == "__main__":
    main()