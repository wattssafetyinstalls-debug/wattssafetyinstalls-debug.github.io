#!/usr/bin/env python3
"""
FIX CAROUSEL LAYOUT & NAVIGATION - Clean implementation above promo section
"""

import re

def fix_carousel_completely():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # Remove any existing carousel implementations to start fresh
    content = re.sub(r'<!-- Auto-Rotating Premium Carousel -->.*?<!-- Promo Section -->', 
                    '<!-- Promo Section -->', content, flags=re.DOTALL)
    
    content = re.sub(r'<!-- Premium Service Carousel -->.*?<!-- Promo Section -->', 
                    '<!-- Promo Section -->', content, flags=re.DOTALL)
    
    content = re.sub(r'<!-- Services Carousel -->.*?<!-- Promo Section -->', 
                    '<!-- Promo Section -->', content, flags=re.DOTALL)
    
    # Remove any carousel CSS and JS we added
    content = re.sub(r'/\* === AUTO-ROTATING CAROUSEL - PREMIUM DESIGN === \*/.*?/\* Mobile adjustments \*/\s*\}', 
                    '', content, flags=re.DOTALL)
    
    content = re.sub(r'/\* === FIXED SERVICES CAROUSEL - Cross Browser Compatible === \*/.*?/\* Mobile adjustments \*/\s*\}', 
                    '', content, flags=re.DOTALL)
    
    content = re.sub(r'// Auto-Rotating Premium Carousel.*?// Initialize.*?startAutoRotate\(\);', 
                    '', content, flags=re.DOTALL)
    
    # Find all service cards
    service_card_pattern = r'<div class="service-card"[^>]*>.*?</div>\s*</div>\s*</div>'
    service_cards = re.findall(service_card_pattern, content, re.DOTALL)
    
    if service_cards and len(service_cards) > 0:
        # Create clean carousel slides
        carousel_slides = []
        for i, card in enumerate(service_cards):
            slide = f'''
                    <div class="service-carousel-slide {'active' if i == 0 else ''}" data-index="{i}">
                        {card}
                    </div>'''
            carousel_slides.append(slide)
        
        # Create simple, clean carousel HTML
        carousel_html = f'''
        <!-- Simple Service Carousel -->
        <section class="service-carousel-section">
            <div class="service-carousel-container">
                <div class="service-carousel">
                    <div class="service-carousel-track">
                        {''.join(carousel_slides)}
                    </div>
                    
                    <div class="service-carousel-nav">
                        <button class="service-carousel-prev" aria-label="Previous service">
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        
                        <div class="service-carousel-dots">
                            {''.join([f'<button class="service-carousel-dot {'active' if i == 0 else ''}" data-index="{i}"></button>' for i in range(len(service_cards))])}
                        </div>
                        
                        <button class="service-carousel-next" aria-label="Next service">
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        </section>'''
        
        # Insert the carousel right before the promo section
        promo_pattern = r'<!-- Promo Section -->'
        if re.search(promo_pattern, content):
            content = re.sub(promo_pattern, carousel_html + '\n\n            <!-- Promo Section -->', content)
            
            # Add clean, cross-browser compatible CSS
            clean_carousel_css = '''
            /* === CLEAN SERVICE CAROUSEL - Cross Browser Compatible === */
            .service-carousel-section {
                padding: 60px 0 40px;
                background: var(--warm-light);
                position: relative;
            }
            
            .service-carousel-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }
            
            .service-carousel {
                position: relative;
                margin: 0 auto;
                max-width: 1000px;
            }
            
            .service-carousel-track {
                display: flex;
                transition: transform 0.5s ease;
                margin-bottom: 40px;
            }
            
            .service-carousel-slide {
                min-width: 100%;
                display: none;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.5s ease;
            }
            
            .service-carousel-slide.active {
                display: flex;
                opacity: 1;
            }
            
            .service-carousel-slide .service-card {
                max-width: 450px;
                width: 100%;
                margin: 0;
            }
            
            .service-carousel-nav {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 30px;
            }
            
            .service-carousel-prev,
            .service-carousel-next {
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border: none;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,196,180,0.3);
                font-size: 1.1rem;
            }
            
            .service-carousel-prev:hover,
            .service-carousel-next:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,196,180,0.4);
            }
            
            .service-carousel-prev:active,
            .service-carousel-next:active {
                transform: translateY(0);
            }
            
            .service-carousel-dots {
                display: flex;
                gap: 12px;
                align-items: center;
            }
            
            .service-carousel-dot {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: var(--gray);
                border: none;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .service-carousel-dot.active {
                background: var(--teal);
                transform: scale(1.2);
            }
            
            .service-carousel-dot:hover {
                background: var(--teal);
                transform: scale(1.1);
            }
            
            /* Mobile adjustments */
            @media (max-width: 768px) {
                .service-carousel-section {
                    padding: 40px 0 30px;
                }
                
                .service-carousel-slide .service-card {
                    max-width: 400px;
                }
                
                .service-carousel-prev,
                .service-carousel-next {
                    width: 44px;
                    height: 44px;
                }
                
                .service-carousel-nav {
                    gap: 20px;
                }
            }
            
            @media (max-width: 480px) {
                .service-carousel-slide .service-card {
                    max-width: 350px;
                }
                
                .service-carousel-prev,
                .service-carousel-next {
                    width: 40px;
                    height: 40px;
                    font-size: 1rem;
                }
                
                .service-carousel-dots {
                    gap: 8px;
                }
                
                .service-carousel-dot {
                    width: 10px;
                    height: 10px;
                }
            }'''
            
            # Add clean, reliable JavaScript
            clean_carousel_js = '''
            // Clean Service Carousel - Only 2 Working Buttons + Dots
            document.addEventListener('DOMContentLoaded', function() {
                const carouselSection = document.querySelector('.service-carousel-section');
                if (!carouselSection) return;
                
                const slides = document.querySelectorAll('.service-carousel-slide');
                const dots = document.querySelectorAll('.service-carousel-dot');
                const prevBtn = document.querySelector('.service-carousel-prev');
                const nextBtn = document.querySelector('.service-carousel-next');
                
                if (slides.length === 0) return;
                
                let currentIndex = 0;
                let autoRotate;
                
                function showSlide(index) {
                    // Hide all slides
                    slides.forEach(slide => {
                        slide.classList.remove('active');
                    });
                    
                    // Remove active from all dots
                    dots.forEach(dot => {
                        dot.classList.remove('active');
                    });
                    
                    // Show current slide and dot
                    slides[index].classList.add('active');
                    dots[index].classList.add('active');
                    
                    currentIndex = index;
                }
                
                function nextSlide() {
                    let nextIndex = currentIndex + 1;
                    if (nextIndex >= slides.length) {
                        nextIndex = 0;
                    }
                    showSlide(nextIndex);
                }
                
                function prevSlide() {
                    let prevIndex = currentIndex - 1;
                    if (prevIndex < 0) {
                        prevIndex = slides.length - 1;
                    }
                    showSlide(prevIndex);
                }
                
                function startAutoRotate() {
                    autoRotate = setInterval(nextSlide, 5000);
                }
                
                function stopAutoRotate() {
                    clearInterval(autoRotate);
                }
                
                // Event listeners for navigation
                if (nextBtn) {
                    nextBtn.addEventListener('click', function() {
                        stopAutoRotate();
                        nextSlide();
                        startAutoRotate();
                    });
                }
                
                if (prevBtn) {
                    prevBtn.addEventListener('click', function() {
                        stopAutoRotate();
                        prevSlide();
                        startAutoRotate();
                    });
                }
                
                // Dot navigation
                dots.forEach((dot, index) => {
                    dot.addEventListener('click', function() {
                        stopAutoRotate();
                        showSlide(index);
                        startAutoRotate();
                    });
                });
                
                // Pause on hover
                if (carouselSection) {
                    carouselSection.addEventListener('mouseenter', stopAutoRotate);
                    carouselSection.addEventListener('mouseleave', startAutoRotate);
                }
                
                // Keyboard navigation
                document.addEventListener('keydown', function(e) {
                    if (e.key === 'ArrowLeft') {
                        stopAutoRotate();
                        prevSlide();
                        startAutoRotate();
                    } else if (e.key === 'ArrowRight') {
                        stopAutoRotate();
                        nextSlide();
                        startAutoRotate();
                    }
                });
                
                // Initialize
                showSlide(0);
                startAutoRotate();
            });'''
            
            # Add CSS to the existing style tag
            if '.service-carousel-section' not in content:
                # Find the closing style tag and insert before it
                style_end_pattern = r'(\s*</style>)'
                content = re.sub(style_end_pattern, clean_carousel_css + '\\1', content)
            
            # Add JavaScript before closing body tag
            if '// Clean Service Carousel' not in content:
                content = content.replace('</body>', '<script>' + clean_carousel_js + '</script>\n</body>')
            
            with open("services.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("SUCCESS: Created clean, properly positioned carousel with working navigation")
        else:
            print("ERROR: Could not find Promo Section to insert carousel before")
    else:
        print("ERROR: Could not find service cards")

if __name__ == "__main__":
    fix_carousel_completely()