#!/usr/bin/env python3
"""
ADD CAROUSEL & DROPDOWN - Fully mobile optimized
Cross-platform compatible - No breaking changes
"""

import os
import re

def add_carousel_and_dropdown():
    target_files = ["index.html", "services.html"]
    
    for filename in target_files:
        if not os.path.exists(filename):
            print(f"SKIPPED -> {filename} (not found)")
            continue
            
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Mobile-optimized carousel CSS
        carousel_css = """
        /* === MOBILE-FIRST SERVICE TILES CAROUSEL === */
        .service-tiles-carousel {
            max-width: 1200px;
            margin: 50px auto;
            position: relative;
            overflow: hidden;
            border-radius: 20px;
            padding: 0 10px;
        }
        
        .carousel-container {
            display: flex;
            transition: transform 0.5s ease-in-out;
            gap: 20px;
            padding: 20px 10px;
            scroll-behavior: smooth;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            -webkit-overflow-scrolling: touch;
        }
        
        .carousel-container::-webkit-scrollbar {
            display: none;
        }
        
        .carousel-item {
            flex: 0 0 auto;
            scroll-snap-align: start;
            min-width: calc(100% - 20px);
        }
        
        .carousel-btn {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: var(--teal);
            color: white;
            border: none;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            font-size: 1.2rem;
            cursor: pointer;
            z-index: 10;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,196,180,0.3);
            display: none;
        }
        
        .carousel-btn:hover {
            background: var(--navy);
            transform: translateY(-50%) scale(1.1);
        }
        
        .carousel-prev {
            left: 5px;
        }
        
        .carousel-next {
            right: 5px;
        }
        
        .carousel-dots {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 20px;
            padding: 0 10px;
        }
        
        .carousel-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--gray);
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            flex-shrink: 0;
        }
        
        .carousel-dot.active {
            background: var(--teal);
            transform: scale(1.2);
        }
        
        /* === DROPDOWN MENUS - MOBILE FIRST === */
        .dropdown {
            position: relative;
        }
        
        .dropdown-content {
            display: none;
            position: absolute;
            background: white;
            min-width: 200px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            border-radius: 12px;
            z-index: 1000;
            top: 100%;
            left: 0;
            margin-top: 10px;
            overflow: hidden;
        }
        
        .dropdown-content a {
            color: var(--navy);
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            transition: all 0.3s;
            border-bottom: 1px solid var(--light);
            font-size: 0.95rem;
        }
        
        .dropdown-content a:hover {
            background: var(--teal);
            color: white;
        }
        
        .dropdown-content a:last-child {
            border-bottom: none;
        }
        
        .dropdown:hover .dropdown-content {
            display: block;
        }
        
        .dropdown-toggle::after {
            content: ' \\25BC';
            font-size: 0.7em;
            margin-left: 4px;
        }
        
        /* === TABLET STYLES (768px and up) === */
        @media (min-width: 768px) {
            .service-tiles-carousel {
                padding: 0 20px;
            }
            
            .carousel-container {
                gap: 25px;
                padding: 20px;
                overflow-x: visible;
            }
            
            .carousel-item {
                min-width: calc(50% - 13px);
            }
            
            .carousel-btn {
                display: block;
                width: 50px;
                height: 50px;
                font-size: 1.5rem;
            }
            
            .carousel-prev {
                left: 15px;
            }
            
            .carousel-next {
                right: 15px;
            }
            
            .dropdown-content a {
                padding: 15px 20px;
                font-size: 1rem;
            }
        }
        
        /* === DESKTOP STYLES (1024px and up) === */
        @media (min-width: 1024px) {
            .carousel-item {
                min-width: calc(25% - 19px);
            }
            
            .carousel-container {
                padding: 20px 40px;
            }
        }
        
        /* === TOUCH DEVICE OPTIMIZATIONS === */
        @media (hover: none) and (pointer: coarse) {
            .carousel-btn {
                width: 52px;
                height: 52px;
                font-size: 1.3rem;
            }
            
            .dropdown-content {
                min-width: 220px;
            }
            
            .dropdown-content a {
                padding: 14px 18px;
            }
        }
        
        /* === REDUCED MOTION SUPPORT === */
        @media (prefers-reduced-motion: reduce) {
            .carousel-container {
                transition: none;
                scroll-behavior: auto;
            }
        }"""
        
        # Cross-platform compatible JavaScript
        carousel_js = """
        // Service Tiles Carousel - Mobile Optimized
        document.addEventListener('DOMContentLoaded', function() {
            const carousels = document.querySelectorAll('.service-tiles-carousel');
            
            carousels.forEach(function(carousel) {
                const container = carousel.querySelector('.carousel-container');
                const items = carousel.querySelectorAll('.carousel-item');
                const prevBtn = carousel.querySelector('.carousel-prev');
                const nextBtn = carousel.querySelector('.carousel-next');
                const dots = carousel.querySelectorAll('.carousel-dot');
                
                if (!container || items.length === 0) return;
                
                let currentIndex = 0;
                let itemsPerView = 1;
                
                function calculateItemsPerView() {
                    const containerWidth = container.clientWidth;
                    const itemWidth = items[0].offsetWidth + 20; // including gap
                    
                    if (containerWidth >= 1024) {
                        return 4;
                    } else if (containerWidth >= 768) {
                        return 2;
                    } else {
                        return 1;
                    }
                }
                
                function updateCarousel() {
                    itemsPerView = calculateItemsPerView();
                    const maxIndex = Math.max(0, items.length - itemsPerView);
                    currentIndex = Math.min(currentIndex, maxIndex);
                    
                    const translateX = -currentIndex * (100 / itemsPerView);
                    container.style.transform = 'translateX(' + translateX + '%)';
                    
                    // Update dots
                    dots.forEach(function(dot, index) {
                        dot.classList.toggle('active', index === currentIndex);
                    });
                    
                    // Update button states
                    if (prevBtn) prevBtn.disabled = currentIndex === 0;
                    if (nextBtn) nextBtn.disabled = currentIndex >= maxIndex;
                }
                
                function nextSlide() {
                    itemsPerView = calculateItemsPerView();
                    const maxIndex = Math.max(0, items.length - itemsPerView);
                    if (currentIndex < maxIndex) {
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
                
                // Event listeners for buttons
                if (nextBtn) {
                    nextBtn.addEventListener('click', nextSlide);
                }
                
                if (prevBtn) {
                    prevBtn.addEventListener('click', prevSlide);
                }
                
                // Dot navigation
                dots.forEach(function(dot, index) {
                    dot.addEventListener('click', function() {
                        currentIndex = index;
                        updateCarousel();
                    });
                });
                
                // Touch/swipe support
                let startX = 0;
                let currentX = 0;
                
                container.addEventListener('touchstart', function(e) {
                    startX = e.touches[0].clientX;
                }, { passive: true });
                
                container.addEventListener('touchmove', function(e) {
                    currentX = e.touches[0].clientX;
                }, { passive: true });
                
                container.addEventListener('touchend', function() {
                    const diff = startX - currentX;
                    const threshold = 50;
                    
                    if (Math.abs(diff) > threshold) {
                        if (diff > 0) {
                            nextSlide();
                        } else {
                            prevSlide();
                        }
                    }
                });
                
                // Keyboard navigation
                container.setAttribute('tabindex', '0');
                container.addEventListener('keydown', function(e) {
                    if (e.key === 'ArrowLeft') {
                        prevSlide();
                    } else if (e.key === 'ArrowRight') {
                        nextSlide();
                    }
                });
                
                // Window resize handling
                let resizeTimer;
                window.addEventListener('resize', function() {
                    clearTimeout(resizeTimer);
                    resizeTimer = setTimeout(function() {
                        updateCarousel();
                    }, 250);
                });
                
                // Initialize
                updateCarousel();
                
                // Fallback for older browsers
                if (!('transform' in document.documentElement.style)) {
                    container.style.transform = 'none';
                    container.style.overflowX = 'auto';
                }
            });
        });"""
        
        # Insert CSS into style tag
        if '<style>' in content and carousel_css not in content:
            content = content.replace('<style>', '<style>' + carousel_css)
        
        # Insert JavaScript before closing body tag
        if '</body>' in content and carousel_js not in content:
            content = content.replace('</body>', '<script>' + carousel_js + '</script></body>')
        
        if content != original_content:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"ADDED CAROUSEL -> {filename}")
        else:
            print(f"ALREADY UPDATED -> {filename}")
    
    print("COMPLETE - Added mobile-optimized carousel to main pages")
    print("Features: Touch swipes, keyboard nav, reduced motion support, cross-browser compatible")

if __name__ == "__main__":
    add_carousel_and_dropdown()