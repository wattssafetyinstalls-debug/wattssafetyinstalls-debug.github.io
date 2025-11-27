#!/usr/bin/env python3
"""
STEP 1: RESTORE BASIC STRUCTURE - Fix missing tiles and dropdowns
"""

def restore_basic_structure():
    print("STEP 1: Restoring basic structure with all 7 service tiles...")
    
    try:
        with open("services.html", "r", encoding="utf-8") as f:
            content = f.read()
        print("Found existing services.html")
    except:
        print("Error reading services.html")
        return

    # Simple replacement - find the carousel section and replace with proper structure
    # Look for the carousel section
    if '<section class="carousel-section">' in content:
        print("Found carousel section to replace")
        # We'll replace just the carousel content
        new_carousel = '''
        <!-- Service Carousel with 7 Tiles -->
        <section class="services-carousel-section">
            <div class="carousel-container">
                <div class="services-carousel">
                    <div class="carousel-track">'''
        
        # Add the 7 service tiles here...
        service_tiles = []
        services = [
            ("Accessibility & Safety", "accessibility-safety", "Get Free Assessment"),
            ("Home Remodeling", "home-remodeling", "Start Your Project"), 
            ("Concrete & Flooring", "concrete-flooring", "Get Floor Quote"),
            ("Cabinets & Countertops", "cabinets-countertops", "Design Consultation"),
            ("Property Maintenance", "property-maintenance", "Schedule Service"),
            ("Lawn & Landscape", "lawn-care", "Get Lawn Quote"),
            ("Additional Services", "additional-services", "Discuss Project")
        ]
        
        for i, (title, id, cta) in enumerate(services):
            tile = f'''
                        <div class="carousel-slide {'active' if i == 0 else ''}">
                            <div class="service-card" id="{id}">
                                <img src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="{title}" class="service-image">
                                <div class="service-content">
                                    <h3 class="service-title">{title}</h3>
                                    <p class="service-description">Professional {title.lower()} services for your home.</p>
                                    <div class="service-hamburger">
                                        <i class="fas fa-bars hamburger-icon"></i>
                                        <div class="service-dropdown">
                                            <a href="/services/service1.html">Service 1</a>
                                            <a href="/services/service2.html">Service 2</a>
                                            <a href="/services/service3.html">Service 3</a>
                                        </div>
                                    </div>
                                    <div class="service-cta">
                                        <a href="contact">{cta}</a>
                                    </div>
                                </div>
                            </div>
                        </div>'''
            service_tiles.append(tile)
        
        new_carousel += ''.join(service_tiles)
        new_carousel += '''
                    </div>
                    <div class="carousel-navigation">
                        <button class="carousel-arrow prev-arrow">
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        <div class="carousel-dots">'''
        
        # Add dots for 7 slides
        for i in range(7):
            new_carousel += f'<span class="dot {"active" if i == 0 else ""}" data-index="{i}"></span>'
        
        new_carousel += '''
                        </div>
                        <button class="carousel-arrow next-arrow">
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        </section>'''
        
        # Replace the carousel section
        old_carousel_pattern = r'<section class="carousel-section">.*?</section>'
        import re
        content = re.sub(old_carousel_pattern, new_carousel, content, flags=re.DOTALL)
        
        with open("services.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Successfully updated carousel with 7 service tiles and dropdowns")
    else:
        print("Could not find carousel section - structure may be different")

if __name__ == "__main__":
    restore_basic_structure()