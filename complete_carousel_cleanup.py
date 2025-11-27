#!/usr/bin/env python3
"""
COMPLETE CAROUSEL CLEANUP & FRESH START - No duplicates, proper layout
"""

import re

def complete_carousel_fix():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # COMPLETE CLEANUP - Remove ALL carousel-related code we've added
    # Remove carousel HTML sections
    content = re.sub(r'<!-- Auto-Rotating Premium Carousel -->.*?<!-- Promo Section -->', 
                    '<!-- Promo Section -->', content, flags=re.DOTALL)
    
    content = re.sub(r'<!-- Premium Service Carousel -->.*?<!-- Promo Section -->', 
                    '<!-- Promo Section -->', content, flags=re.DOTALL)
    
    content = re.sub(r'<!-- Services Carousel -->.*?<!-- Promo Section -->', 
                    '<!-- Promo Section -->', content, flags=re.DOTALL)
    
    content = re.sub(r'<!-- Simple Service Carousel -->.*?<!-- Promo Section -->', 
                    '<!-- Promo Section -->', content, flags=re.DOTALL)
    
    # Remove carousel CSS
    content = re.sub(r'/\* === AUTO-ROTATING CAROUSEL - PREMIUM DESIGN === \*/.*?@media \(max-width: 480px\)\s*\{.*?\}\s*\}', 
                    '', content, flags=re.DOTALL)
    
    content = re.sub(r'/\* === FIXED SERVICES CAROUSEL - Cross Browser Compatible === \*/.*?@media \(max-width: 480px\)\s*\{.*?\}\s*\}', 
                    '', content, flags=re.DOTALL)
    
    content = re.sub(r'/\* === CLEAN SERVICE CAROUSEL - Cross Browser Compatible === \*/.*?@media \(max-width: 480px\)\s*\{.*?\}\s*\}', 
                    '', content, flags=re.DOTALL)
    
    # Remove carousel JavaScript
    content = re.sub(r'<script>\s*// Auto-Rotating Premium Carousel.*?// Initialize.*?startAutoRotate\(\);\s*</script>', 
                    '', content, flags=re.DOTALL)
    
    content = re.sub(r'<script>\s*// Clean Service Carousel - Only 2 Working Buttons.*?startAutoRotate\(\);\s*</script>', 
                    '', content, flags=re.DOTALL)
    
    # Find the ORIGINAL services-grid section (the one that was there before we started)
    # Look for the services-grid that contains the 7 service cards
    services_grid_pattern = r'(<div class="services-grid">)(.*?)(</div>\s*</div>\s*<!-- Promo Section -->)'
    
    match = re.search(services_grid_pattern, content, re.DOTALL)
    
    if match:
        # Extract the service cards from the original grid
        service_cards_content = match.group(2)
        
        # Find all individual service cards within the grid
        service_cards = re.findall(r'<div class="service-card"[^>]*>.*?</div>\s*</div>\s*</div>', 
                                 service_cards_content, re.DOTALL)
        
        if service_cards and len(service_cards) > 0:
            # Create ONE clean carousel to replace the grid
            carousel_slides = []
            for i, card in enumerate(service_cards):
                slide = f'''
                        <div class="service-slide {'active' if i == 0 else ''}" data-index="{i}">
                            {card}
                        </div>'''
                carousel_slides.append(slide)
            
            # Create the replacement carousel HTML
            replacement_carousel = f'''
            <!-- Service Carousel Replacement -->
            <div class="services-carousel-wrapper">
                <div class="services-carousel">
                    <div class="carousel-inner">
                        {''.join(carousel_slides)}
                    </div>
                    
                    <div class="carousel-controls">
                        <button class="carousel-arrow prev" aria-label="Previous service">
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        
                        <div class="carousel-indicators">
                            {''.join([f'<span class="indicator {'active' if i == 0 else ''}" data-index="{i}"></span>' for i in range(len(service_cards))])}
                        </div>
                        
                        <button class="carousel-arrow next" aria-label="Next service">
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
            </div>  <!-- Close the services-container div -->
            <!-- Promo Section -->'''
            
            # Replace the entire services-grid section with the carousel
            content = content.replace(match.group(0), replacement_carousel)
            
            # Add clean, minimal CSS
            clean_css = '''
            /* === SERVICES CAROUSEL - CLEAN IMPLEMENTATION === */
            .services-carousel-wrapper {
                width: 100%;
                margin: 40px 0;
            }
            
            .services-carousel {
                max-width: 500px;
                margin: 0 auto;
                position: relative;
            }
            
            .carousel-inner {
                position: relative;
                min-height: 500px;
            }
            
            .service-slide {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                opacity: 0;
                transform: scale(0.95);
                transition: all 0.5s ease;
                pointer-events: none;
            }
            
            .service-slide.active {
                opacity: 1;
                transform: scale(1);
                pointer-events: all;
                position: relative;
            }
            
            .service-slide .service-card {
                margin: 0 auto;
                max-width: 450px;
            }
            
            .carousel-controls {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
            }
            
            .carousel-arrow {
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border: none;
                width: 45px;
                height: 45px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0,196,180,0.3);
            }
            
            .carousel-arrow:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(0,196,180,0.4);
            }
            
            .carousel-indicators {
                display: flex;
                gap: 8px;
            }
            
            .indicator {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: var(--gray);
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .indicator.active {
                background: var(--teal);
                transform: scale(1.2);
            }
            
            .indicator:hover {
                background: var(--teal);
            }
            
            @media (max-width: 768px) {
                .services-carousel {
                    max-width: 400px;
                }
                
                .carousel-inner {
                    min-height: 450px;
                }
            }
            
            @media (max-width: 480px) {
                .services-carousel {
                    max-width: 350px;
                }
                
                .carousel-inner {
                    min-height: 420px;
                }
                
                .carousel-arrow {
                    width: 40px;
                    height: 40px;
                }
            }'''
            
            # Add reliable JavaScript
            clean_js = '''
            // Simple Carousel Functionality
            document.addEventListener('DOMContentLoaded', function() {
                const carousel = document.querySelector('.services-carousel');
                if (!carousel) return;
                
                const slides = document.querySelectorAll('.service-slide');
                const indicators = document.querySelectorAll('.indicator');
                const prevBtn = document.querySelector('.carousel-arrow.prev');
                const nextBtn = document.querySelector('.carousel-arrow.next');
                
                if (slides.length === 0) return;
                
                let currentIndex = 0;
                let autoSlide;
                
                function showSlide(index) {
                    // Hide all slides
                    slides.forEach(slide => slide.classList.remove('active'));
                    indicators.forEach(indicator => indicator.classList.remove('active'));
                    
                    // Show current slide
                    slides[index].classList.add('active');
                    indicators[index].classList.add('active');
                    
                    currentIndex = index;
                }
                
                function nextSlide() {
                    let next = currentIndex + 1;
                    if (next >= slides.length) next = 0;
                    showSlide(next);
                }
                
                function prevSlide() {
                    let prev = currentIndex - 1;
                    if (prev < 0) prev = slides.length - 1;
                    showSlide(prev);
                }
                
                function startAutoSlide() {
                    autoSlide = setInterval(nextSlide, 5000);
                }
                
                function stopAutoSlide() {
                    clearInterval(autoSlide);
                }
                
                // Event listeners
                if (nextBtn) nextBtn.addEventListener('click', function() {
                    stopAutoSlide();
                    nextSlide();
                    startAutoSlide();
                });
                
                if (prevBtn) prevBtn.addEventListener('click', function() {
                    stopAutoSlide();
                    prevSlide();
                    startAutoSlide();
                });
                
                indicators.forEach((indicator, index) => {
                    indicator.addEventListener('click', function() {
                        stopAutoSlide();
                        showSlide(index);
                        startAutoSlide();
                    });
                });
                
                // Pause on hover
                carousel.addEventListener('mouseenter', stopAutoSlide);
                carousel.addEventListener('mouseleave', startAutoSlide);
                
                // Initialize
                showSlide(0);
                startAutoSlide();
            });'''
            
            # Add CSS to style tag
            if '.services-carousel-wrapper' not in content:
                content = content.replace('</style>', clean_css + '\n    </style>')
            
            # Add JavaScript
            if '// Simple Carousel Functionality' not in content:
                content = content.replace('</body>', '<script>' + clean_js + '</script>\n</body>')
            
            with open("services.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("SUCCESS: Completely cleaned up and created ONE proper carousel")
            print("The original services grid has been replaced with a single carousel")
        else:
            print("ERROR: Could not find service cards in the grid")
    else:
        print("ERROR: Could not find the original services-grid section")
        print("The file structure may have been changed")

if __name__ == "__main__":
    complete_carousel_fix()