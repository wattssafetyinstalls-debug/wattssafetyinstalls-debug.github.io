# create_professional_pages_fixed.py
import os

# Professional service data with proper images and all visual elements
professional_services = [
    {
        "slug": "accessibility-safety-solutions",
        "title": "Accessibility & Safety Solutions",
        "description": "Complete ADA-compliant accessibility modifications and safety installations for homes and businesses throughout Norfolk NE. ATP Approved Contractor specializing in mobility solutions.",
        "header_image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
        "services_included": [
            "ADA-Compliant Bathroom Modifications",
            "Zero-Step Shower Installations", 
            "Commercial-Grade Grab Bar Installation (500+ lb capacity)",
            "Wheelchair Ramp Construction & Installation",
            "Stairlift & Residential Elevator Installation",
            "Non-Slip Flooring Solutions",
            "Handrail & Safety Rail Systems",
            "Doorway Widening & Accessibility Modifications",
            "Senior Safety Modifications",
            "Mobility Equipment Installation"
        ],
        "key_benefits": [
            "Full ADA Compliance Certification",
            "Increased Property Value & Safety",
            "Professional Assessment & Planning",
            "Licensed & Insured Installations",
            "Lifetime Workmanship Warranty"
        ]
    },
    {
        "slug": "home-remodeling-renovation",
        "title": "Home Remodeling & Renovation",
        "description": "Complete home transformation services from kitchen and bathroom remodels to room additions and whole-house renovations. Licensed Nebraska contractor serving Norfolk and surrounding areas.",
        "header_image": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
        "services_included": [
            "Kitchen Remodeling & Complete Renovations",
            "Bathroom Remodels & Tub-to-Shower Conversions",
            "Room Additions & Sunroom Construction",
            "Flooring Installation (Hardwood, Laminate, Tile, Vinyl)",
            "Painting Services (Interior & Exterior)",
            "Drywall Installation & Repair",
            "Deck Construction & Repair",
            "Siding Replacement & Installation",
            "Basement Finishing & Waterproofing",
            "Whole-House Renovation Projects"
        ],
        "key_benefits": [
            "Nebraska Licensed Contractor #54690-25",
            "Project Management Included",
            "Quality Materials & Workmanship",
            "Timely Project Completion",
            "Building Permit Assistance"
        ]
    },
    {
        "slug": "tv-home-theater-installation",
        "title": "TV & Home Theater Installation",
        "description": "Professional TV mounting, home theater setup, and audio visual installation services for residential and commercial clients in Norfolk NE. Expert installation with cable management.",
        "header_image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
        "services_included": [
            "TV Wall Mounting (All sizes up to 85\")",
            "Home Theater System Installation",
            "Surround Sound Speaker Setup (5.1 & 7.1 Systems)",
            "Sound Bar & Wireless Speaker Installation",
            "Projector Mounting & Screen Installation",
            "Cable Management & Concealment",
            "Streaming Device Setup & Integration",
            "Whole-House Audio Systems",
            "Commercial Display Installation",
            "Smart Home Audio Integration"
        ],
        "key_benefits": [
            "Secure Stud Mounting Guarantee",
            "Professional Cable Management",
            "Optimal Viewing Angle Setup",
            "Equipment Integration & Setup",
            "Clean, Professional Installation"
        ]
    },
    {
        "slug": "property-maintenance-services",
        "title": "Property Maintenance & Care Services",
        "description": "Comprehensive property maintenance, lawn care, snow removal, and handyman services to keep your Norfolk NE property in optimal condition year-round.",
        "header_image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2058&q=80",
        "services_included": [
            "Lawn Maintenance & Regular Care Services",
            "Seasonal Lawn Fertilization & Weed Control",
            "Pressure Washing (Driveways, Siding, Decks)",
            "Gutter Cleaning & Repair Services",
            "Snow Removal & De-icing Services",
            "Emergency Snow Removal (On-Call)",
            "Fence Repair & Installation",
            "Tree Trimming & Landscaping Services",
            "Seasonal Property Clean-up",
            "General Handyman & Repair Services"
        ],
        "key_benefits": [
            "Regular Maintenance Scheduling Available",
            "Emergency Service Response",
            "Seasonal Service Packages",
            "Licensed & Insured Professionals",
            "Commercial & Residential Services"
        ]
    },
    {
        "slug": "handyman-repair-services",
        "title": "Handyman & Repair Services",
        "description": "Comprehensive handyman services for home repairs, installations, and maintenance tasks. Your one-call solution for home upkeep in Norfolk NE.",
        "header_image": "https://images.unsplash.com/photo-1581094794329-cdc0c0ba3b0d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
        "services_included": [
            "Drywall Repair & Patching",
            "Painting Touch-ups & Complete Jobs",
            "Door & Window Repair",
            "Furniture Assembly & Installation",
            "Shelf & Storage Installation",
            "Minor Plumbing Repairs",
            "Electrical Fixture Installation",
            "Appliance Installation",
            "General Home Maintenance",
            "Emergency Repair Services"
        ],
        "key_benefits": [
            "One-Call Solution for Multiple Tasks",
            "Quick Response Times",
            "Affordable Pricing",
            "Quality Workmanship Guaranteed",
            "No Job Too Small"
        ]
    }
]

# Read styling from index.html
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

# Generate professional service pages with all visual elements
for service in professional_services:
    page_path = f'services/{service["slug"]}.html'
    
    # Build services included list
    services_list = ""
    for srv in service["services_included"]:
        services_list += f'<li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-check-circle" style="color: var(--teal); margin-right: 10px;"></i>{srv}</li>\n'
    
    # Build benefits list
    benefits_list = ""
    for benefit in service["key_benefits"]:
        benefits_list += f'<li style="margin-bottom: 0.8rem;"><i class="fas fa-star" style="color: var(--gold); margin-right: 10px;"></i>{benefit}</li>\n'
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script>if(window.location.pathname==="/index"){{window.history.replaceState({{}},"","/");}}</script>
<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{service["title"]} | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="{service["description"]} ATP Approved Contractor. Nebraska Licensed #54690-25. Call (405) 410-6402">
  
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
    <meta property="og:title" content="{service["title"]} | Watts Safety Installs">
    <meta property="og:description" content="{service["description"]}">
    <meta property="og:image" content="{service["header_image"]}">
    <meta property="og:url" content="https://wattsatpcontractor.com/services/{service["slug"]}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{service["title"]}">
    <meta name="twitter:description" content="{service["description"]}">
    <meta name="twitter:image" content="{service["header_image"]}">
    <meta name="keywords" content="{service["title"]} Norfolk NE, professional installation services, ATP Approved Contractor">
    <meta name="author" content="Watts Safety Installs">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://wattsatpcontractor.com/services/{service["slug"]}">
    <meta http-equiv="Cache-Control" content="max-age=31536000, public">
 
    <!-- Fonts and Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
    {styles}
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KCPM8VZ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    {header}

    <!-- Service Hero Section with Header Image -->
    <section class="hero" style="height: 60vh; min-height: 500px; background: linear-gradient(135deg, rgba(10,29,55,0.85) 0%, rgba(245,158,11,0.2) 100%), url('{service["header_image"]}') center/cover no-repeat;">
        <h1>{service["title"]}</h1>
        <p class="certification-badge">ATP Approved Contractor • Nebraska Licensed #54690-25 • Serving All Nebraska</p>
        <p style="font-size: 1.3rem; max-width: 800px; margin: 0 auto;">{service["description"]}</p>
        <div class="promo-banner">
            <p style="font-size:1.4rem; margin:0"><strong>15% OFF First 3 Snow Visits 2025</strong> • <strong>LAWN2026 – 20% OFF Season</strong></p>
        </div>
        <a href="tel:+14054106402" class="cta-button">Call (405) 410-6402 – Free Quote</a>
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

    <!-- Service Details Section -->
    <section class="services" style="padding: 80px 20px;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            <h2 class="section-title">Our {service["title"]}</h2>
            <p class="section-subtitle">Comprehensive professional services tailored to your needs in Norfolk NE and surrounding areas</p>
            
            <div class="services-grid" style="grid-template-columns: 1fr 1fr; gap: 40px; margin: 3rem 0;">
                <div class="service-card" style="background: var(--white); border-radius: 20px; padding: 2rem; box-shadow: var(--teal-glow);">
                    <h3 style="color: var(--navy); margin-bottom: 1.5rem; border-bottom: 3px solid var(--teal); padding-bottom: 0.5rem;">Services Included</h3>
                    <ul style="list-style: none; padding: 0; color: var(--gray);">
                        {services_list}
                    </ul>
                </div>
                
                <div class="service-card" style="background: linear-gradient(135deg, var(--teal), var(--navy)); color: white; border-radius: 20px; padding: 2rem; box-shadow: var(--navy-glow);">
                    <h3 style="margin-bottom: 1.5rem; border-bottom: 3px solid var(--gold); padding-bottom: 0.5rem;">Key Benefits</h3>
                    <ul style="list-style: none; padding: 0;">
                        {benefits_list}
                    </ul>
                </div>
            </div>

            <!-- Professional CTA Section -->
            <div style="background: linear-gradient(135deg, var(--navy), #1e3a5f); color: white; padding: 3rem; border-radius: 20px; text-align: center; margin: 3rem 0;">
                <h2 style="margin-bottom: 1rem;">Ready to Get Started?</h2>
                <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
                    Contact us today for a professional consultation and free estimate on {service["title"].lower()} services.
                </p>
                <div>
                    <a href="tel:+14054106402" class="cta-button" style="background: var(--teal); margin: 0 10px;">Call (405) 410-6402</a>
                    <a href="/contact" class="cta-button" style="background: var(--gold); color: var(--navy); margin: 0 10px;">Schedule Consultation</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Final CTA Section -->
    <section class="cta-section">
        <h2>Professional {service["title"]} Services</h2>
        <p>Contact us today for a free consultation and estimate. We serve Norfolk NE and surrounding areas.</p>
        <a href="tel:+14054106402" class="cta-button">Call Now: (405) 410-6402</a>
    </section>

    {footer}

    {scripts}
</body>
</html>'''
    
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Created: " + page_path)

print("All professional service pages created with full visual appeal!")
print("Pages include:")
print("- Header images")
print("- Trust banners") 
print("- Gradient service cards")
print("- Professional styling")
print("- All the eye appeal from before")