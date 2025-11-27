#!/usr/bin/env python3
"""
CREATE SINGLE ITEM CAROUSEL - Show one service tile at a time
"""

import re

def create_single_item_carousel():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # Find all service cards in the services-grid
    service_card_pattern = r'<div class="service-card"[^>]*>.*?</div>\s*</div>\s*</div>'
    service_cards = re.findall(service_card_pattern, content, re.DOTALL)
    
    if service_cards and len(service_cards) > 0:
        # Create carousel slides with one card per slide
        carousel_slides = []
        for i, card in enumerate(service_cards):
            slide = f'''
            <div class="carousel-slide {'active' if i == 0 else ''}">
                {card}
            </div>'''
            carousel_slides.append(slide)
        
        carousel_html = f'''
        <!-- Single Item Service Carousel -->
        <div class="service-carousel-wrapper">
            <div class="service-carousel">
                <button class="carousel-btn carousel-prev">&#10094;</button>
                <button class="carousel-btn carousel-next">&#10095;</button>
                
                <div class="carousel-track-container">
                    <div class="carousel-track">
                        {''.join(carousel_slides)}
                    </div>
                </div>
                
                <div class="carousel-nav">
                    <div class="carousel-dots">
                        {''.join([f'<button class="carousel-dot {"active" if i == 0 else ""}" data-index="{i}"></button>' for i in range(len(service_cards))])}
                    </div>
                </div>
            </div>
        </div>'''
        
        # Replace the entire services-grid section with the carousel
        services_grid_pattern = r'<div class="services-grid">.*?</div>\s*</div>\s*<!-- Promo Section -->'
        replacement = f'{carousel_html}\n\n            <!-- Promo Section -->'
        
        content = re.sub(services_grid_pattern, replacement, content, flags=re.DOTALL)
        
        # Add single-item carousel CSS
        single_carousel_css = '''
        /* === SINGLE ITEM CAROUSEL === */
        .service-carousel-wrapper {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .service-carousel {
            position: relative;
            overflow: hidden;
            border-radius: 20px;
            background: var(--white);
            box-shadow: var(--shadow);
            padding: 40px 20px;
        }
        
        .carousel-track-container {
            overflow: hidden;
            padding: 20px 0;
        }
        
        .carousel-track {
            display: flex;
            transition: transform 0.5s ease-in-out;
        }
        
        .carousel-slide {
            min-width: 100%;
            padding: 0 20px;
            display: flex;
            justify-content: center;
        }
        
        .carousel-slide .service-card {
            max-width: 400px;
            margin: 0 auto;
        }
        
        .carousel-btn {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: var(--teal);
            color: white;
            border: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            font-size: 1.5rem;
            cursor: pointer;
            z-index: 10;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,196,180,0.3);
        }
        
        .carousel-btn:hover {
            background: var(--navy);
            transform: translateY(-50%) scale(1.1);
        }
        
        .carousel-prev {
            left: 10px;
        }
        
        .carousel-next {
            right: 10px;
        }
        
        .carousel-nav {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        
        .carousel-dots {
            display: flex;
            gap: 10px;
        }
        
        .carousel-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--gray);
            border: none;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .carousel-dot.active {
            background: var(--teal);
            transform: scale(1.2);
        }
        
        /* Mobile adjustments */
        @media (max-width: 768px) {
            .service-carousel {
                padding: 30px 10px;
            }
            
            .carousel-slide {
                padding: 0 10px;
            }
            
            .carousel-btn {
                width: 44px;
                height: 44px;
                font-size: 1.2rem;
            }
            
            .carousel-prev {
                left: 5px;
            }
            
            .carousel-next {
                right: 5px;
            }
        }'''
        
        # Add single-item carousel JavaScript
        single_carousel_js = '''
        // Single Item Service Carousel
        document.addEventListener('DOMContentLoaded', function() {
            const carousel = document.querySelector('.service-carousel');
            if (!carousel) return;
            
            const track = carousel.querySelector('.carousel-track');
            const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
            const prevBtn = carousel.querySelector('.carousel-prev');
            const nextBtn = carousel.querySelector('.carousel-next');
            const dots = Array.from(carousel.querySelectorAll('.carousel-dot'));
            
            let currentIndex = 0;
            const totalSlides = slides.length;
            
            function updateCarousel() {
                // Move track to show current slide
                track.style.transform = 'translateX(-' + (currentIndex * 100) + '%)';
                
                // Update active states
                slides.forEach((slide, index) => {
                    slide.classList.toggle('active', index === currentIndex);
                });
                
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === currentIndex);
                });
                
                // Update button states
                prevBtn.disabled = currentIndex === 0;
                nextBtn.disabled = currentIndex === totalSlides - 1;
            }
            
            function nextSlide() {
                if (currentIndex < totalSlides - 1) {
                    currentIndex++;
                    updateCarousel();
                }
            }
            
            function prevSlide() {
                if (currentIndex > 0) {
                    currentIndex--;
                    updateCarousel();
                }
            }
            
            // Event listeners
            nextBtn.addEventListener('click', nextSlide);
            prevBtn.addEventListener('click', prevSlide);
            
            // Dot navigation
            dots.forEach((dot, index) => {
                dot.addEventListener('click', () => {
                    currentIndex = index;
                    updateCarousel();
                });
            });
            
            // Keyboard navigation
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') prevSlide();
                if (e.key === 'ArrowRight') nextSlide();
            });
            
            // Touch/swipe support
            let startX = 0;
            let currentX = 0;
            
            track.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
            }, { passive: true });
            
            track.addEventListener('touchmove', (e) => {
                currentX = e.touches[0].clientX;
            }, { passive: true });
            
            track.addEventListener('touchend', () => {
                const diff = startX - currentX;
                const threshold = 50;
                
                if (Math.abs(diff) > threshold) {
                    if (diff > 0) nextSlide();
                    else prevSlide();
                }
            });
            
            // Auto-advance (optional)
            let autoAdvance = setInterval(nextSlide, 5000);
            
            carousel.addEventListener('mouseenter', () => {
                clearInterval(autoAdvance);
            });
            
            carousel.addEventListener('mouseleave', () => {
                autoAdvance = setInterval(nextSlide, 5000);
            });
            
            // Initialize
            updateCarousel();
        });'''
        
        # Add CSS to style tag
        if '.service-carousel-wrapper' not in content:
            content = content.replace('</style>', single_carousel_css + '\n    </style>')
        
        # Add JS before closing body tag
        if '// Single Item Service Carousel' not in content:
            content = content.replace('</body>', '<script>' + single_carousel_js + '</script>\n</body>')
        
        with open("services.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Created single-item carousel with one service tile at a time")
    else:
        print("ERROR: Could not find service cards to create carousel")

if __name__ == "__main__":
    create_single_item_carousel()