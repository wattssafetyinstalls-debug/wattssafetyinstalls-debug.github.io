# fix_service_pages.py

import os

# Simple service data with working generic images and fixed styling
services_fixed = [
    {
        "id": "accessibility-safety",
        "title": "Accessibility & Safety Solutions",
        "sub_services": [
            {
                "name": "ADA-compliant showers & bathrooms",
                "slug": "ada-compliant-showers",
                "image": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Professional ADA-compliant bathroom modifications with zero-step showers, grab bars, and wheelchair-accessible layouts in Norfolk NE."
            },
            {
                "name": "Grab bar installation", 
                "slug": "grab-bar-installation",
                "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Commercial-grade grab bar installation rated for 500+ lbs weight capacity for bathrooms and hallways in Norfolk NE homes."
            },
            {
                "name": "Wheelchair ramp installation",
                "slug": "wheelchair-ramp-installation", 
                "image": "https://images.unsplash.com/photo-1572021335466-1e8b5a0c8aab?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Custom wheelchair ramp installation meeting ADA requirements for safe home access in Norfolk NE."
            },
            {
                "name": "Stairlift & elevator installation",
                "slug": "stairlift-elevator-installation",
                "image": "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Professional stairlift and residential elevator installation for multi-story homes in Norfolk NE."
            },
            {
                "name": "Non-slip flooring solutions",
                "slug": "non-slip-flooring",
                "image": "https://images.unsplash.com/photo-1560449752-3ed683137d93?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
                "description": "Slip-resistant flooring installation for bathrooms and entryways to prevent falls in Norfolk NE homes."
            }
        ]
    },
    {
        "id": "home-remodeling",
        "title": "Home Remodeling & Renovation", 
        "sub_services": [
            {
                "name": "Kitchen renovations",
                "slug": "kitchen-renovations",
                "image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Complete kitchen remodeling including cabinets, countertops, and appliances in Norfolk NE."
            },
            {
                "name": "Bathroom remodels",
                "slug": "bathroom-remodels",
                "image": "https://images.unsplash.com/photo-1584622744904-801a3d2d73a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Bathroom renovation services including tub-to-shower conversions and vanity installation in Norfolk NE."
            },
            {
                "name": "Room additions",
                "slug": "room-additions",
                "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Professional room addition construction for growing families in Norfolk NE."
            },
            {
                "name": "Flooring installation", 
                "slug": "flooring-installation",
                "image": "https://images.unsplash.com/photo-1560449752-3ed683137d93?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Professional flooring installation including hardwood, laminate, and tile in Norfolk NE."
            },
            {
                "name": "Painting & drywall",
                "slug": "painting-drywall", 
                "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Interior and exterior painting services with drywall repair in Norfolk NE."
            }
        ]
    },
    {
        "id": "tv-mounting", 
        "title": "TV & Home Theater Setup",
        "sub_services": [
            {
                "name": "TV mounting on walls",
                "slug": "tv-mounting",
                "image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Professional TV wall mounting service for flat screens up to 85 inches in Norfolk NE."
            },
            {
                "name": "Home theater system installation",
                "slug": "home-theater-installation", 
                "image": "https://images.unsplash.com/photo-1563297007-0686b7003af7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Complete home theater installation including surround sound and projection systems in Norfolk NE."
            },
            {
                "name": "Sound bar & speaker setup",
                "slug": "sound-system-setup",
                "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Sound bar and wireless speaker installation with optimal placement in Norfolk NE."
            },
            {
                "name": "Cable management solutions",
                "slug": "cable-management",
                "image": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
                "description": "Professional cable management and concealment for clean entertainment centers in Norfolk NE."
            }
        ]
    },
    {
        "id": "property-maintenance",
        "title": "Property Maintenance & Lawn Care",
        "sub_services": [
            {
                "name": "Lawn maintenance & care", 
                "slug": "lawn-maintenance",
                "image": "https://images.unsplash.com/photo-1578309850417-0c6c5c7c3a0e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Comprehensive lawn care services including mowing, edging, and fertilization in Norfolk NE."
            },
            {
                "name": "Pressure washing services",
                "slug": "pressure-washing",
                "image": "https://images.unsplash.com/photo-1578301978068-9c4c2b9d7c6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Professional pressure washing for driveways, siding, and decks in Norfolk NE."
            },
            {
                "name": "Gutter cleaning & repair",
                "slug": "gutter-cleaning",
                "image": "https://images.unsplash.com/photo-1578632749014-ca77efd052eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Gutter cleaning, repair, and guard installation to protect your Norfolk NE home from water damage."
            },
            {
                "name": "Fence repair & installation",
                "slug": "fence-repair",
                "image": "https://images.unsplash.com/photo-1578632749014-ca77efd052eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
                "description": "Fence installation and repair services for wood, vinyl, and chain-link fences in Norfolk NE."
            },
            {
                "name": "General handyman services",
                "slug": "handyman-services",
                "image": "https://images.unsplash.com/photo-1581094794329-cdc0c0ba3b0d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                "description": "Comprehensive handyman services for home repairs and maintenance tasks in Norfolk NE."
            }
        ]
    }
]

# Read index.html for styling
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    header_start = index_content.find('<header>')
    header_end = index_content.find('</header>') + 9
    header = index_content[header_start:header_end]
    
    footer_start = index_content.find('<footer>')
    footer_end = index_content.find('</footer>') + 9
    footer = index_content[footer_start:footer_end]
    
    style_start = index_content.find('<style>')
    style_end = index_content.find('</style>') + 8
    styles = index_content[style_start:style_end]
    
    script_start = index_content.find('<script>')
    script_end = index_content.find('</script>') + 9
    scripts = index_content[script_start:script_end]
    
except FileNotFoundError:
    print("Error: Could not read index.html")
    exit()

# Generate fixed service pages
for service in services_fixed:
    for sub in service["sub_services"]:
        page_path = f'services/{sub["slug"]}.html'
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script>if(window.location.pathname==="/index"){{window.history.replaceState({{}},"","/");}}</script>
<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sub["name"]} | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="{sub["description"]} ATP Approved Contractor. Call (405) 410-6402">
  
    <!-- Favicon and meta tags -->
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">
  
    <!-- SEO Meta Tags -->
    <meta name="google-site-verification" content="9uPoUkPF9bV3aKmaJyxbcnlzzXjxYLkUPb-YXyvOabU" />
    <meta property="og:title" content="{sub["name"]} | Watts Safety Installs">
    <meta property="og:description" content="{sub["description"]}">
    <meta property="og:image" content="{sub["image"]}">
    <meta property="og:url" content="https://wattsatpcontractor.com/services/{sub["slug"]}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{sub["name"]} Services">
    <meta name="twitter:description" content="{sub["description"]}">
    <meta name="twitter:image" content="{sub["image"]}">
    <meta name="keywords" content="{sub["name"]} Norfolk NE, professional installation services">
    <meta name="author" content="Watts Safety Installs">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://wattsatpcontractor.com/services/{sub["slug"]}">
    <meta http-equiv="Cache-Control" content="max-age=31536000, public">
 
    <!-- Fonts and Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
    {styles}
    
    <!-- Fix for text visibility on service pages -->
    <style>
        .service-detail-content h2, 
        .service-detail-content h3,
        .service-detail-content h4,
        .service-detail-content p,
        .service-detail-content li {{
            color: #1E293B !important;
        }}
        
        .service-card .service-title {{
            color: var(--navy) !important;
        }}
        
        .service-card .service-description {{
            color: var(--gray) !important;
        }}
        
        .service-features ul li {{
            color: #1E293B !important;
        }}
    </style>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KCPM8VZ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    {header}

    <!-- Service Hero Section -->
    <section class="hero" style="height: 50vh; min-height: 400px;">
        <h1>{sub["name"]}</h1>
        <p class="certification-badge">ATP Approved Contractor • Nebraska Licensed #54690-25 • Serving All Nebraska</p>
        <p>Professional {sub["name"]} Services</p>
        <div class="promo-banner">
            <p style="font-size:1.4rem; margin:0"><strong>15% OFF First 3 Snow Visits 2025</strong> • <strong>LAWN2026 – 20% OFF Season</strong></p>
        </div>
        <a href="tel:+14054106402" class="cta-button">Call (405) 410-6402 – Free Quote</a>
    </section>

    <!-- Service Details Section -->
    <section class="services" style="padding: 80px 20px;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            <div class="service-detail-content">
                <h2 class="section-title" style="text-align: left; margin-bottom: 30px; color: #1E293B;">{sub["name"]}</h2>
                
                <div class="service-card" style="max-width: 100%; margin: 0; background: white;">
                    <img loading="lazy" src="{sub["image"]}" alt="{sub["name"]} - Watts Safety Installs Norfolk NE" class="service-image" style="height: 400px; object-fit: cover; width: 100%;">
                    <div class="service-content" style="padding: 2rem;">
                        <h3 class="service-title" style="color: #1E293B;">Service Overview</h3>
                        <p class="service-description" style="color: #64748B; font-size: 1.1rem; line-height: 1.7; margin-bottom: 2rem;">
                            {sub["description"]} We provide professional installation and repair services throughout Norfolk NE and surrounding areas.
                        </p>
                        
                        <div style="background: #f8fafc; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
                            <h4 style="color: #1E293B; margin-bottom: 1rem;">What We Offer</h4>
                            <ul style="color: #64748B; line-height: 1.6;">
                                <li>Professional installation and setup</li>
                                <li>Quality materials and workmanship</li>
                                <li>Safety-compliant solutions</li>
                                <li>Competitive pricing with free estimates</li>
                                <li>Licensed and insured professionals</li>
                            </ul>
                        </div>

                        <div style="background: linear-gradient(135deg, var(--teal), var(--navy)); color: white; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
                            <h3 style="margin-bottom: 1rem; color: white;">Why Choose Watts Safety Installs?</h3>
                            <ul style="color: white;">
                                <li>ATP Approved Contractor</li>
                                <li>Nebraska Licensed #54690-25</li>
                                <li>Professional Workmanship Guaranteed</li>
                                <li>Timely Project Completion</li>
                                <li>Serving Norfolk NE and Surrounding Areas</li>
                            </ul>
                        </div>

                        <div class="service-cta" style="margin-top: 2rem; text-align: center;">
                            <a href="tel:+14054106402" class="cta-button" style="display: inline-block; margin: 0 10px; padding: 15px 30px;">Call Now: (405) 410-6402</a>
                            <a href="/contact" class="cta-button" style="display: inline-block; margin: 0 10px; padding: 15px 30px; background: var(--navy);">Get Free Estimate</a>
                        </div>
                    </div>
                </div>

                <div class="back-to-services" style="text-align: center; margin-top: 3rem;">
                    <a href="/services" style="color: var(--teal); text-decoration: none; font-weight: 600; font-size: 1.1rem; padding: 10px 20px; border: 2px solid var(--teal); border-radius: 5px;">
                        <i class="fas fa-arrow-left"></i> Back to All Services
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Trust Bar -->
    <section class="trust-bar">
        <div class="trust-container">
            <div class="trust-item"><div class="trust-icon">✓</div><div class="trust-text">Licensed & Insured</div></div>
            <div class="trust-item"><div class="trust-icon">★</div><div class="trust-text">5.0/5 Customer Rating</div></div>
            <div class="trust-item"><div class="trust-icon">⚡</div><div class="trust-text">Same-Day Service Available</div></div>
            <div class="trust-item"><div class="trust-icon">🏆</div><div class="trust-text">ATP Approved Contractor</div></div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <h2>Ready for Professional {sub["name"]}?</h2>
        <p>Contact us today for a free consultation and estimate. We serve Norfolk NE and surrounding areas.</p>
        <a href="tel:+14054106402" class="cta-button">Call Now: (405) 410-6402</a>
    </section>

    {footer}

    {scripts}
</body>
</html>'''
        
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Fixed: {page_path}")

print("All service pages fixed!")
print("Fixed text visibility - all text now readable")
print("Fixed images - using reliable generic images")
print("Simplified content - clear, concise descriptions")