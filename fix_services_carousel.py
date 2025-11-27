#!/usr/bin/env python3
"""
FIX SERVICES PAGE CAROUSEL - Add proper carousel HTML structure
"""

import re

def fix_services_carousel():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # Find the services-grid section and wrap it with carousel
    services_grid_pattern = r'<div class="services-grid">(.*?)</div>\s*<!-- Promo Section -->'
    
    if re.search(services_grid_pattern, content, re.DOTALL):
        # Replace with carousel structure
        carousel_html = '''
            <!-- Service Tiles Carousel -->
            <div class="service-tiles-carousel">
                <button class="carousel-btn carousel-prev">&#10094;</button>
                <button class="carousel-btn carousel-next">&#10095;</button>
                <div class="carousel-container">
                    <div class="services-grid">\\1</div>
                </div>
                <div class="carousel-dots">
                    <button class="carousel-dot active" data-index="0"></button>
                    <button class="carousel-dot" data-index="1"></button>
                    <button class="carousel-dot" data-index="2"></button>
                    <button class="carousel-dot" data-index="3"></button>
                </div>
            </div>
            
            <!-- Promo Section -->'''
        
        content = re.sub(services_grid_pattern, carousel_html, content, flags=re.DOTALL)
        
        with open("services.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Added carousel structure to services.html")
    else:
        print("ALREADY FIXED: Carousel structure already exists in services.html")

if __name__ == "__main__":
    fix_services_carousel()