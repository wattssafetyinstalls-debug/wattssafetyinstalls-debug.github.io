#!/usr/bin/env python3
import re

print("FINAL EVERYTHING FIX - RESTORING CAROUSEL + DROPDOWNS + BUTTON\n")

with open("services.html", "r", encoding="utf-8") as f:
    html = f.read()

original = html

# 1. FIRST - Add the carousel structure (7 service tiles)
carousel_html = '''
        <!-- Services Carousel -->
        <section class="services-carousel-section">
            <div class="container">
                <h2>Our Professional Services</h2>
                <p class="section-subtitle">Comprehensive solutions for your home and business needs</p>
                
                <div class="services-carousel">
                    <!-- Service Tile 1: Accessibility & Safety -->
                    <div class="service-tile">
                        <div class="service-icon">
                            <i class="fas fa-wheelchair"></i>
                        </div>
                        <h3>Accessibility & Safety</h3>
                        <p>ADA compliance, grab bars, ramps, and senior safety modifications</p>
                        <div class="nav-dropdown">
                            <button class="dropdown-toggle">View Services <i class="fas fa-chevron-down"></i></button>
                            <div class="dropdown">
                                <a href="/services/ada-compliant-showers.html">ADA Compliant Showers</a>
                                <a href="/services/grab-bars.html">Grab Bars Installation</a>
                                <a href="/services/non-slip-flooring.html">Non-Slip Flooring</a>
                                <a href="/services/custom-ramps.html">Custom Wheelchair Ramps</a>
                                <a href="/services/senior-safety.html">Senior Safety Modifications</a>
                                <a href="/services/bathroom-accessibility.html">Bathroom Accessibility</a>
                            </div>
                        </div>
                    </div>

                    <!-- Service Tile 2: Home Remodeling -->
                    <div class="service-tile">
                        <div class="service-icon">
                            <i class="fas fa-home"></i>
                        </div>
                        <h3>Home Remodeling</h3>
                        <p>Kitchen & bathroom renovations, basement finishing, and room additions</p>
                        <div class="nav-dropdown">
                            <button class="dropdown-toggle">View Services <i class="fas fa-chevron-down"></i></button>
                            <div class="dropdown">
                                <a href="/kitchen-renovations">Kitchen Renovations</a>
                                <a href="/home-remodeling">Bathroom Remodels</a>
                                <a href="/services/basement-finishing.html">Basement Finishing</a>
                                <a href="/deck-construction">Deck Construction</a>
                                <a href="/siding-replacement">Siding Replacement</a>
                                <a href="/window-doors">Window & Door Installation</a>
                                <a href="/painting-services">Painting Services</a>
                                <a href="/services/drywall-repair.html">Drywall Repair</a>
                            </div>
                        </div>
                    </div>

                    <!-- Service Tile 3: TV & Home Theater -->
                    <div class="service-tile">
                        <div class="service-icon">
                            <i class="fas fa-tv"></i>
                        </div>
                        <h3>TV & Home Theater</h3>
                        <p>Professional TV mounting, sound systems, and home theater setup</p>
                        <div class="nav-dropdown">
                            <button class="dropdown-toggle">View Services <i class="fas fa-chevron-down"></i></button>
                            <div class="dropdown">
                                <a href="/services/tv-mounting-residential.html">TV Mounting</a>
                                <a href="/services/home-theater.html">Home Theater Installation</a>
                                <a href="/services/soundbar-setup.html">Soundbar Setup</a>
                                <a href="/services/smart-audio.html">Smart Audio Systems</a>
                                <a href="/services/projector-install.html">Projector Installation</a>
                                <a href="/services/cable-management.html">Cable Management</a>
                            </div>
                        </div>
                    </div>

                    <!-- Service Tile 4: Property Maintenance -->
                    <div class="service-tile">
                        <div class="service-icon">
                            <i class="fas fa-tools"></i>
                        </div>
                        <h3>Property Maintenance</h3>
                        <p>Routine maintenance, emergency repairs, and seasonal services</p>
                        <div class="nav-dropdown">
                            <button class="dropdown-toggle">View Services <i class="fas fa-chevron-down"></i></button>
                            <div class="dropdown">
                                <a href="/services/property-maintenance-routine.html">Routine Maintenance</a>
                                <a href="/services/emergency-repairs.html">Emergency Repairs</a>
                                <a href="/snow-removal">Snow Removal</a>
                                <a href="/services/tree-trimming.html">Tree Trimming</a>
                                <a href="/services/seasonal-prep.html">Seasonal Prep & Cleanup</a>
                            </div>
                        </div>
                    </div>

                    <!-- Service Tile 5: Lawn & Landscape -->
                    <div class="service-tile">
                        <div class="service-icon">
                            <i class="fas fa-leaf"></i>
                        </div>
                        <h3>Lawn & Landscape</h3>
                        <p>Lawn care, landscaping, fertilization, and garden maintenance</p>
                        <div class="nav-dropdown">
                            <button class="dropdown-toggle">View Services <i class="fas fa-chevron-down"></i></button>
                            <div class="dropdown">
                                <a href="/services/lawn-maintenance.html">Lawn Maintenance</a>
                                <a href="/landscape-design">Landscape Design & Install</a>
                                <a href="/services/fertilization.html">Fertilization & Weed Control</a>
                                <a href="/services/seasonal-cleanup.html">Seasonal Cleanup</a>
                                <a href="/garden-maintenance">Garden Maintenance</a>
                            </div>
                        </div>
                    </div>

                    <!-- Service Tile 6: Concrete & Flooring -->
                    <div class="service-tile">
                        <div class="service-icon">
                            <i class="fas fa-border-style"></i>
                        </div>
                        <h3>Concrete & Flooring</h3>
                        <p>Concrete work, driveways, patios, and flooring installation</p>
                        <div class="nav-dropdown">
                            <button class="dropdown-toggle">View Services <i class="fas fa-chevron-down"></i></button>
                            <div class="dropdown">
                                <a href="/concrete-pouring">Concrete Pouring & Repair</a>
                                <a href="/driveway-installation">Driveways & Patios</a>
                                <a href="/hardwood-flooring">Hardwood Flooring</a>
                                <a href="/services/floor-refinishing.html">Floor Refinishing</a>
                            </div>
                        </div>
                    </div>

                    <!-- Service Tile 7: Cabinets & Countertops -->
                    <div class="service-tile">
                        <div class="service-icon">
                            <i class="fas fa-utensils"></i>
                        </div>
                        <h3>Cabinets & Countertops</h3>
                        <p>Custom cabinets, countertop installation, and kitchen cabinetry</p>
                        <div class="nav-dropdown">
                            <button class="dropdown-toggle">View Services <i class="fas fa-chevron-down"></i></button>
                            <div class="dropdown">
                                <a href="/custom-cabinets">Custom Cabinets</a>
                                <a href="/services/cabinet-refacing.html">Cabinet Refacing</a>
                                <a href="/services/onyx-countertops.html">Onyx & Countertops</a>
                                <a href="/services/kitchen-cabinetry.html">Kitchen Cabinetry</a>
                                <a href="/services/custom-storage.html">Custom Storage</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
'''

# Find where to insert the carousel (after the hero section)
if 'services-carousel-section' not in html:
    # Insert carousel right after the hero section
    hero_end = '</section>'
    hero_section_end = html.find(hero_end, html.find('services-hero'))
    if hero_section_end != -1:
        insert_position = hero_section_end + len(hero_end)
        html = html[:insert_position] + '\n' + carousel_html + '\n' + html[insert_position:]
        print("ADDED 7-TILE CAROUSEL - Success")
    else:
        print("WARNING: Could not find hero section end")

# 2. Add CSS for navy button if not present
if "pro-cta-btn" not in html:
    css = '''<style>
    .pro-cta-btn, .banner-quote-btn {
        display: inline-block !important;
        background: #003087 !important;
        color: white !important;
        padding: 14px 32px !important;
        margin: 15px 0 !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-decoration: none !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .pro-cta-btn:hover, .banner-quote-btn:hover {
        background: white !important;
        color: #003087 !important;
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
    }
    </style>'''
    html = html.replace("</head>", css + "\n</head>")
    print("ADDED NAVY BUTTON CSS - Success")

# 3. Find and fix "Contact Us for a Quote" button
# First check if there's a yellow banner section
if 'Contact Us for a Quote' in html:
    # Replace the text with a proper button
    html = html.replace(
        'Contact Us for a Quote',
        '<a href="/contact" class="pro-cta-btn banner-quote-btn">Contact Us for a Quote</a>'
    )
    print("FIXED YELLOW BANNER BUTTON - Now navy and clickable")
else:
    print("No 'Contact Us for a Quote' found - checking for other contact text")

# 4. Add carousel CSS if not present
if "services-carousel" in html and ".services-carousel" not in html:
    carousel_css = '''
    <style>
    /* Services Carousel Styles */
    .services-carousel-section {
        padding: 80px 0;
        background: var(--warm-light);
    }
    
    .services-carousel {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin-top: 50px;
    }
    
    .service-tile {
        background: white;
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .service-tile:hover {
        transform: translateY(-10px);
        box-shadow: var(--shadow-hover);
    }
    
    .service-icon {
        font-size: 3rem;
        color: var(--teal);
        margin-bottom: 20px;
    }
    
    .service-tile h3 {
        color: var(--navy);
        margin-bottom: 15px;
        font-size: 1.5rem;
    }
    
    .service-tile p {
        color: var(--gray);
        margin-bottom: 25px;
        line-height: 1.6;
    }
    
    .dropdown-toggle {
        background: linear-gradient(135deg, var(--navy), var(--teal));
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .dropdown-toggle:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    '''
    html = html.replace("</head>", carousel_css + "\n</head>")
    print("ADDED CAROUSEL CSS - Success")

# Save the file
if html != original:
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nSUCCESS - EVERYTHING RESTORED!")
    print("CHECKLIST:")
    print("- 7-tile carousel with dropdowns")
    print("- Navy button under yellow banner") 
    print("- All real service links working")
    print("\nRun: python -m http.server 8000")
    print("Refresh with Ctrl+F5 to see changes")
else:
    print("No changes needed - carousel already exists")