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

    # Create the 7 service tiles structure
    service_tiles = '''
    <!-- Service Carousel with 7 Tiles -->
    <section class="services-carousel-section">
        <div class="carousel-container">
            <div class="services-carousel">
                <div class="carousel-track">
                    <!-- Tile 1: Accessibility & Safety -->
                    <div class="carousel-slide active">
                        <div class="service-card">
                            <img src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Accessibility & Safety" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Accessibility & Safety Solutions</h3>
                                <p class="service-description">Professional ADA-compliant solutions for seniors and mobility challenges.</p>
                                <div class="service-hamburger">
                                    <i class="fas fa-bars hamburger-icon"></i>
                                    <div class="service-dropdown">
                                        <a href="/services/ada-compliant-showers.html">ADA Showers</a>
                                        <a href="/services/grab-bars.html">Grab Bars</a>
                                        <a href="/services/wheelchair-ramps.html">Wheelchair Ramps</a>
                                    </div>
                                </div>
                                <div class="service-cta">
                                    <a href="contact">Get Free Assessment</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tile 2: Home Remodeling -->
                    <div class="carousel-slide">
                        <div class="service-card">
                            <img src="https://images.unsplash.com/photo-1541888946425-d81bb19240f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Home Remodeling" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Home Remodeling & Improvements</h3>
                                <p class="service-description">Transform your living space with comprehensive remodeling services.</p>
                                <div class="service-hamburger">
                                    <i class="fas fa-bars hamburger-icon"></i>
                                    <div class="service-dropdown">
                                        <a href="/services/kitchen-renovations.html">Kitchen Renovations</a>
                                        <a href="/services/bathroom-remodels.html">Bathroom Remodels</a>
                                        <a href="/services/basement-finishing.html">Basement Finishing</a>
                                    </div>
                                </div>
                                <div class="service-cta">
                                    <a href="contact">Start Your Project</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tile 3: Concrete & Flooring -->
                    <div class="carousel-slide">
                        <div class="service-card">
                            <img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2058&q=80" alt="Concrete & Flooring" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Concrete & Floor Services</h3>
                                <p class="service-description">Professional concrete work and floor services for durable surfaces.</p>
                                <div class="service-hamburger">
                                    <i class="fas fa-bars hamburger-icon"></i>
                                    <div class="service-dropdown">
                                        <a href="/services/driveway-installation.html">Driveway Installation</a>
                                        <a href="/services/patio-construction.html">Patio Construction</a>
                                        <a href="/services/hardwood-flooring.html">Hardwood Flooring</a>
                                    </div>
                                </div>
                                <div class="service-cta">
                                    <a href="contact">Get Floor Quote</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tile 4: Cabinets & Countertops -->
                    <div class="carousel-slide">
                        <div class="service-card">
                            <img src="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Cabinets & Countertops" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Cabinets & Countertops</h3>
                                <p class="service-description">Custom cabinetry and beautiful countertop installations.</p>
                                <div class="service-hamburger">
                                    <i class="fas fa-bars hamburger-icon"></i>
                                    <div class="service-dropdown">
                                        <a href="/services/custom-cabinets.html">Custom Cabinets</a>
                                        <a href="/services/cabinet-refacing.html">Cabinet Refacing</a>
                                        <a href="/services/onyx-countertops.html">Onyx Countertops</a>
                                    </div>
                                </div>
                                <div class="service-cta">
                                    <a href="contact">Design Consultation</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tile 5: Property Maintenance -->
                    <div class="carousel-slide">
                        <div class="service-card">
                            <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Property Maintenance" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Property Maintenance</h3>
                                <p class="service-description">Comprehensive property maintenance services year-round.</p>
                                <div class="service-hamburger">
                                    <i class="fas fa-bars hamburger-icon"></i>
                                    <div class="service-dropdown">
                                        <a href="/services/snow-removal.html">Snow Removal</a>
                                        <a href="/services/emergency-repairs.html">Emergency Repairs</a>
                                        <a href="/services/gutter-cleaning.html">Gutter Cleaning</a>
                                    </div>
                                </div>
                                <div class="service-cta">
                                    <a href="contact">Schedule Service</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tile 6: Lawn & Landscape -->
                    <div class="carousel-slide">
                        <div class="service-card">
                            <img src="https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Lawn & Landscape" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Lawn & Landscape Care</h3>
                                <p class="service-description">Professional lawn care and landscaping for beautiful yards.</p>
                                <div class="service-hamburger">
                                    <i class="fas fa-bars hamburger-icon"></i>
                                    <div class="service-dropdown">
                                        <a href="/services/lawn-maintenance.html">Lawn Maintenance</a>
                                        <a href="/services/fertilization.html">Fertilization</a>
                                        <a href="/services/landscape-design.html">Landscape Design</a>
                                    </div>
                                </div>
                                <div class="service-cta">
                                    <a href="contact">Get Lawn Quote</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tile 7: Additional Services -->
                    <div class="carousel-slide">
                        <div class="service-card">
                            <img src="https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Additional Services" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Additional Services</h3>
                                <p class="service-description">Complete home solutions from a trusted general contractor.</p>
                                <div class="service-hamburger">
                                    <i class="fas fa-bars hamburger-icon"></i>
                                    <div class="service-dropdown">
                                        <a href="/services/tv-mounting.html">TV Mounting</a>
                                        <a href="/services/home-theater.html">Home Theater</a>
                                        <a href="/services/painting-services.html">Painting Services</a>
                                    </div>
                                </div>
                                <div class="service-cta">
                                    <a href="contact">Discuss Your Project</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Carousel Navigation -->
                <div class="carousel-navigation">
                    <button class="carousel-arrow prev-arrow">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <div class="carousel-dots">
                        <span class="dot active" data-index="0"></span>
                        <span class="dot" data-index="1"></span>
                        <span class="dot" data-index="2"></span>
                        <span class="dot" data-index="3"></span>
                        <span class="dot" data-index="4"></span>
                        <span class="dot" data-index="5"></span>
                        <span class="dot" data-index="6"></span>
                    </div>
                    <button class="carousel-arrow next-arrow">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        </div>
    </section>'''

    # Try to replace the existing carousel section
    import re
    
    # Pattern to find the current carousel section
    carousel_pattern = r'<section class="[^"]*carousel[^"]*">.*?</section>'
    
    if re.search(carousel_pattern, content, re.DOTALL):
        # Replace existing carousel
        new_content = re.sub(carousel_pattern, service_tiles, content, flags=re.DOTALL)
        print("Replaced existing carousel section")
    else:
        # Insert after services-hero section
        hero_pattern = r'(<section class="services-hero">.*?</section>)'
        new_content = re.sub(hero_pattern, r'\1' + service_tiles, content, flags=re.DOTALL)
        print("Inserted carousel after hero section")
    
    # Write the updated content
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("Step 1 completed: Added 7 service tiles with dropdown menus")

if __name__ == "__main__":
    restore_basic_structure()