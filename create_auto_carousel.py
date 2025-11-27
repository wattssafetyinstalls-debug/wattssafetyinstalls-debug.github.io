#!/usr/bin/env python3
"""
AUTO-ROTATING PREMIUM CAROUSEL - Matches website design, cycles every 5 seconds
"""

import re

def create_auto_carousel():
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
            <div class="carousel-slide {'active' if i == 0 else ''}" data-index="{i}">
                <div class="slide-wrapper">
                    {card}
                </div>
            </div>'''
            carousel_slides.append(slide)
        
        carousel_html = f'''
        <!-- Auto-Rotating Premium Carousel -->
        <div class="auto-carousel-section">
            <div class="auto-carousel-container">
                <div class="carousel-track">
                    {''.join(carousel_slides)}
                </div>
                
                <!-- Minimal Navigation -->
                <div class="carousel-minimal-nav">
                    <button class="nav-arrow prev-arrow" aria-label="Previous service">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    
                    <div class="slide-indicators">
                        {''.join([f'<div class="slide-dot {"active" if i == 0 else ""}" data-index="{i}"></div>' for i in range(len(service_cards))])}
                    </div>
                    
                    <button class="nav-arrow next-arrow" aria-label="Next service">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        </div>'''
        
        # Replace the entire services-grid section with the auto carousel
        services_grid_pattern = r'<div class="services-grid">.*?</div>\s*</div>\s*<!-- Promo Section -->'
        replacement = f'{carousel_html}\n\n            <!-- Promo Section -->'
        
        content = re.sub(services_grid_pattern, replacement, content, flags=re.DOTALL)
        
        # Add auto-carousel CSS that perfectly matches your website
        auto_carousel_css = '''
        /* === AUTO-ROTATING CAROUSEL - PREMIUM DESIGN === */
        .auto-carousel-section {
            background: transparent;
            padding: 40px 0 60px;
            position: relative;
        }
        
        .auto-carousel-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 20px;
            position: relative;
        }
        
        .carousel-track {
            position: relative;
            height: 600px;
            overflow: hidden;
            border-radius: 20px;
        }
        
        .carousel-slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            transform: scale(0.95);
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            display: flex;
            justify-content: center;
            align-items: center;
            pointer-events: none;
        }
        
        .carousel-slide.active {
            opacity: 1;
            transform: scale(1);
            pointer-events: all;
            z-index: 2;
        }
        
        .slide-wrapper {
            width: 100%;
            display: flex;
            justify-content: center;
            padding: 20px;
        }
        
        .slide-wrapper .service-card {
            max-width: 450px;
            width: 100%;
            margin: 0;
            transform: translateY(0);
            transition: transform 0.3s ease;
        }
        
        .slide-wrapper .service-card:hover {
            transform: translateY(-5px);
        }
        
        /* Minimal Navigation */
        .carousel-minimal-nav {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 30px;
            margin-top: 40px;
        }
        
        .nav-arrow {
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
            box-shadow: 0 4px 15px rgba(0, 196, 180, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .nav-arrow::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .nav-arrow:hover::before {
            left: 100%;
        }
        
        .nav-arrow:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 196, 180, 0.4);
        }
        
        .nav-arrow:active {
            transform: translateY(0);
        }
        
        .slide-indicators {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .slide-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--gray);
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .slide-dot::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--teal), var(--navy));
            border-radius: 50%;
            transform: scale(0);
            transition: transform 0.3s ease;
        }
        
        .slide-dot.active::before {
            transform: scale(1);
        }
        
        .slide-dot.active {
            transform: scale(1.2);
        }
        
        .slide-dot:hover {
            transform: scale(1.1);
        }
        
        /* Progress bar for auto-rotation */
        .slide-dot::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0%;
            height: 2px;
            background: var(--teal);
            transition: width 5s linear;
        }
        
        .slide-dot.active::after {
            width: 100%;
            animation: progress 5s linear;
        }
        
        @keyframes progress {
            0% { width: 0%; }
            100% { width: 100%; }
        }
        
        /* Mobile adjustments */
        @media (max-width: 768px) {
            .carousel-track {
                height: 550px;
            }
            
            .slide-wrapper {
                padding: 15px;
            }
            
            .slide-wrapper .service-card {
                max-width: 400px;
            }
            
            .nav-arrow {
                width: 44px;
                height: 44px;
            }
            
            .carousel-minimal-nav {
                gap: 20px;
                margin-top: 30px;
            }
        }
        
        @media (max-width: 480px) {
            .carousel-track {
                height: 500px;
            }
            
            .slide-wrapper {
                padding: 10px;
            }
            
            .nav-arrow {
                width: 40px;
                height: 40px;
            }
            
            .slide-indicators {
                gap: 8px;
            }
            
            .slide-dot {
                width: 8px;
                height: 8px;
            }
        }'''
        
        # Add auto-carousel JavaScript
        auto_carousel_js = '''
        // Auto-Rotating Premium Carousel
        document.addEventListener('DOMContentLoaded', function() {
            const carousel = document.querySelector('.auto-carousel-section');
            if (!carousel) return;
            
            const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
            const dots = Array.from(carousel.querySelectorAll('.slide-dot'));
            const prevBtn = carousel.querySelector('.prev-arrow');
            const nextBtn = carousel.querySelector('.next-arrow');
            
            let currentIndex = 0;
            let autoRotateInterval;
            const rotationSpeed = 5000; // 5 seconds
            
            function showSlide(index) {
                // Remove active class from all slides and dots
                slides.forEach(slide => slide.classList.remove('active'));
                dots.forEach(dot => dot.classList.remove('active'));
                
                // Add active class to current slide and dot
                slides[index].classList.add('active');
                dots[index].classList.add('active');
                
                currentIndex = index;
            }
            
            function nextSlide() {
                const nextIndex = (currentIndex + 1) % slides.length;
                showSlide(nextIndex);
            }
            
            function prevSlide() {
                const prevIndex = (currentIndex - 1 + slides.length) % slides.length;
                showSlide(prevIndex);
            }
            
            function startAutoRotate() {
                autoRotateInterval = setInterval(nextSlide, rotationSpeed);
            }
            
            function stopAutoRotate() {
                clearInterval(autoRotateInterval);
            }
            
            // Event listeners for navigation
            nextBtn.addEventListener('click', function() {
                stopAutoRotate();
                nextSlide();
                startAutoRotate();
            });
            
            prevBtn.addEventListener('click', function() {
                stopAutoRotate();
                prevSlide();
                startAutoRotate();
            });
            
            // Dot navigation
            dots.forEach((dot, index) => {
                dot.addEventListener('click', function() {
                    stopAutoRotate();
                    showSlide(index);
                    startAutoRotate();
                });
            });
            
            // Pause auto-rotation on hover
            carousel.addEventListener('mouseenter', stopAutoRotate);
            carousel.addEventListener('mouseleave', startAutoRotate);
            
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
            
            // Touch swipe support
            let touchStartX = 0;
            let touchEndX = 0;
            
            carousel.addEventListener('touchstart', function(e) {
                touchStartX = e.changedTouches[0].screenX;
                stopAutoRotate();
            }, { passive: true });
            
            carousel.addEventListener('touchend', function(e) {
                touchEndX = e.changedTouches[0].screenX;
                handleSwipe();
                startAutoRotate();
            }, { passive: true });
            
            function handleSwipe() {
                const swipeThreshold = 50;
                const diff = touchStartX - touchEndX;
                
                if (Math.abs(diff) > swipeThreshold) {
                    if (diff > 0) {
                        nextSlide();
                    } else {
                        prevSlide();
                    }
                }
            }
            
            // Initialize
            showSlide(0);
            startAutoRotate();
        });'''
        
        # Add CSS to style tag
        if '.auto-carousel-section' not in content:
            # Find the style tag and insert before it closes
            style_pattern = r'(</style>)'
            content = re.sub(style_pattern, auto_carousel_css + '\\1', content)
        
        # Add JS before closing body tag
        if '// Auto-Rotating Premium Carousel' not in content:
            content = content.replace('</body>', '<script>' + auto_carousel_js + '</script>\n</body>')
        
        with open("services.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Created auto-rotating premium carousel that cycles every 5 seconds")
    else:
        print("ERROR: Could not find service cards to create carousel")

if __name__ == "__main__":
    create_auto_carousel()