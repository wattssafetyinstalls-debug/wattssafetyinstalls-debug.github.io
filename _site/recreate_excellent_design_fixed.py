# recreate_excellent_design_fixed.py
import os

# Individual service data with the elegant gradient card design
individual_services = [
    {
        "slug": "ada-compliant-showers-bathrooms",
        "title": "ADA-Compliant Showers & Bathrooms",
        "description": "Professional ADA-compliant bathroom modifications with zero-step showers, grab bars, and wheelchair-accessible layouts. Full compliance with Americans with Disabilities Act standards.",
        "services_included": [
            "Zero-step shower installations",
            "Roll-in shower with fold-down seat",
            "ADA-compliant toilet installation", 
            "Accessible vanity and sink modifications",
            "Handheld showerhead installation",
            "Anti-scald valve installation",
            "Grab bar placement and installation",
            "Bathroom layout redesign for accessibility"
        ]
    },
    {
        "slug": "grab-bar-installation",
        "title": "Grab Bar Installation",
        "description": "Commercial-grade grab bar installation rated for 500+ lbs weight capacity. Strategic placement in bathrooms, hallways, and stairways for maximum safety.",
        "services_included": [
            "Commercial-grade grab bars (500+ lb capacity)",
            "Reinforced stud mounting",
            "Bathroom safety bar installation",
            "Shower and tub grab bars",
            "Toilet safety rails",
            "Hallway safety rails",
            "Stairway handrail installation",
            "Custom height and placement"
        ]
    },
    {
        "slug": "wheelchair-ramp-installation",
        "title": "Wheelchair Ramp Installation",
        "description": "Custom wheelchair ramp installation meeting ADA slope requirements for safe home access. Permanent and modular ramp solutions.",
        "services_included": [
            "Custom ramp design and construction",
            "ADA-compliant 1:12 slope ratio",
            "Aluminum and wood ramp options",
            "Handrail installation",
            "Non-slip surface application",
            "Landing platform construction",
            "Weather-resistant materials",
            "Building permit assistance"
        ]
    },
    {
        "slug": "stairlift-elevator-installation",
        "title": "Stairlift & Elevator Installation",
        "description": "Professional stairlift and residential elevator installation for multi-story homes. We provide quality equipment with full service.",
        "services_included": [
            "Straight stairlift installation",
            "Curved stairlift solutions",
            "Residential elevator installation",
            "Platform lift installation",
            "Safety feature implementation",
            "Remote control setup",
            "Maintenance and repair services",
            "Equipment financing assistance"
        ]
    },
    {
        "slug": "non-slip-flooring-solutions",
        "title": "Non-Slip Flooring Solutions",
        "description": "Slip-resistant flooring installation for bathrooms, kitchens, and entryways. Prevent falls with professional non-slip solutions.",
        "services_included": [
            "Non-slip ceramic tile installation",
            "Textured vinyl flooring",
            "Epoxy coating applications",
            "Rubber flooring installation",
            "Bathroom safety flooring",
            "Kitchen non-slip solutions",
            "Entryway traction flooring",
            "ADA-compliant surface installation"
        ]
    },
    {
        "slug": "kitchen-renovations",
        "title": "Kitchen Renovations",
        "description": "Complete kitchen remodeling services including cabinet installation, countertop replacement, and appliance setup. Transform your kitchen with professional craftsmanship.",
        "services_included": [
            "Custom cabinet installation",
            "Quartz and granite countertops",
            "Tile backsplash installation",
            "Flooring installation and repair",
            "Lighting fixture upgrades",
            "Appliance installation",
            "Plumbing and electrical updates",
            "Complete kitchen redesign"
        ]
    },
    {
        "slug": "bathroom-remodels",
        "title": "Bathroom Remodels",
        "description": "Bathroom renovation services including tub-to-shower conversions, vanity installation, and complete bathroom transformations.",
        "services_included": [
            "Tub-to-shower conversions",
            "Vanity and sink installation",
            "Toilet upgrades and installation",
            "Tile flooring and walls",
            "Lighting fixture installation",
            "Ventilation system updates",
            "Plumbing fixture replacement",
            "Complete bathroom makeovers"
        ]
    },
    {
        "slug": "room-additions",
        "title": "Room Additions",
        "description": "Professional room addition construction for growing families. We handle everything from foundation to finishing.",
        "services_included": [
            "Room addition design and planning",
            "Foundation work and construction",
            "Framing and structural work",
            "Roofing and weatherproofing",
            "Electrical and plumbing rough-in",
            "Insulation and drywall",
            "Interior finishing work",
            "Permit acquisition assistance"
        ]
    },
    {
        "slug": "flooring-installation",
        "title": "Flooring Installation",
        "description": "Professional flooring installation including hardwood, laminate, vinyl, tile, and carpet. Quality installation for every room.",
        "services_included": [
            "Hardwood floor installation",
            "Laminate flooring installation",
            "Luxury vinyl plank installation",
            "Ceramic and porcelain tile",
            "Carpet installation",
            "Subfloor preparation and repair",
            "Floor finishing and sealing",
            "Transition strip installation"
        ]
    },
    {
        "slug": "painting-drywall",
        "title": "Painting & Drywall",
        "description": "Interior and exterior painting services with drywall repair and installation. Premium paints and professional finishes.",
        "services_included": [
            "Interior painting services",
            "Exterior painting and staining",
            "Drywall installation and repair",
            "Taping and mudding",
            "Texture matching services",
            "Popcorn ceiling removal",
            "Wall repair and patching",
            "Color consultation available"
        ]
    },
    {
        "slug": "tv-mounting",
        "title": "TV Mounting",
        "description": "Professional TV wall mounting service for flat screens up to 85 inches. Secure installation with optimal viewing angles.",
        "services_included": [
            "TV wall mounting (all sizes)",
            "Full-motion mount installation",
            "Tilting mount installation",
            "Fixed position mounting",
            "Cable concealment systems",
            "Power management setup",
            "Device connectivity assistance",
            "Optimal height placement"
        ]
    },
    {
        "slug": "home-theater-installation",
        "title": "Home Theater Installation",
        "description": "Complete home theater installation including surround sound, projection systems, and media center setup.",
        "services_included": [
            "5.1 and 7.1 surround sound",
            "4K projector installation",
            "Motorized screen setup",
            "Media console installation",
            "Streaming device setup",
            "Audio calibration services",
            "Acoustic room optimization",
            "Universal remote programming"
        ]
    },
    {
        "slug": "sound-system-setup",
        "title": "Sound System Setup",
        "description": "Sound bar and wireless speaker installation with optimal placement for superior audio quality throughout your home.",
        "services_included": [
            "Sound bar mounting and setup",
            "Wireless speaker placement",
            "Subwoofer positioning",
            "Multi-room audio systems",
            "Audio synchronization",
            "Streaming service integration",
            "Voice control setup",
            "Whole-house audio solutions"
        ]
    },
    {
        "slug": "cable-management",
        "title": "Cable Management",
        "description": "Professional cable management and concealment for clean, organized entertainment centers and workspaces.",
        "services_included": [
            "In-wall cable running",
            "Cord concealment systems",
            "Power management solutions",
            "Surge protection installation",
            "Entertainment center organization",
            "Desk cable management",
            "Wall plate installation",
            "Clean setup maintenance"
        ]
    },
    {
        "slug": "lawn-maintenance",
        "title": "Lawn Maintenance",
        "description": "Comprehensive lawn care services including mowing, edging, fertilization, and seasonal maintenance programs.",
        "services_included": [
            "Weekly lawn mowing services",
            "String trimming and edging",
            "Lawn fertilization programs",
            "Weed control applications",
            "Aeration services",
            "Overseeding and lawn repair",
            "Seasonal clean-up services",
            "Lawn health monitoring"
        ]
    },
    {
        "slug": "pressure-washing",
        "title": "Pressure Washing",
        "description": "Professional pressure washing for driveways, siding, decks, and patios. Restore your property's exterior beauty.",
        "services_included": [
            "Driveway and sidewalk cleaning",
            "House siding washing",
            "Deck and patio restoration",
            "Fence cleaning services",
            "Roof stain removal",
            "Gutter exterior cleaning",
            "Eco-friendly cleaning solutions",
            "Surface protection applications"
        ]
    },
    {
        "slug": "gutter-cleaning",
        "title": "Gutter Cleaning",
        "description": "Gutter cleaning, repair, and guard installation to protect your home from water damage and foundation issues.",
        "services_included": [
            "Gutter cleaning services",
            "Downspout clearing and repair",
            "Gutter leak repairs",
            "Gutter realignment",
            "Gutter guard installation",
            "Seasonal maintenance plans",
            "Emergency clog removal",
            "Gutter system inspection"
        ]
    },
    {
        "slug": "fence-repair",
        "title": "Fence Repair",
        "description": "Fence installation and repair services for wood, vinyl, and chain-link fences. Enhance privacy and security.",
        "services_included": [
            "Wood fence construction",
            "Vinyl fence installation",
            "Chain-link fencing",
            "Gate installation and repair",
            "Post replacement services",
            "Fence staining and sealing",
            "Privacy fence installation",
            "Fence maintenance services"
        ]
    },
    {
        "slug": "handyman-services",
        "title": "Handyman Services",
        "description": "Comprehensive handyman services for home repairs, installations, and maintenance tasks. Your one-call solution.",
        "services_included": [
            "Drywall repair and patching",
            "Painting touch-ups and jobs",
            "Door and window repair",
            "Furniture assembly",
            "Shelf and storage installation",
            "Minor plumbing repairs",
            "Electrical fixture installation",
            "General home maintenance"
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

# Create individual service pages with the excellent gradient card design
for service in individual_services:
    page_path = f'services/{service["slug"]}.html'
    
    # Build services included list
    services_list = ""
    for srv in service["services_included"]:
        services_list += f'<li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-check" style="color: var(--teal); margin-right: 10px;"></i>{srv}</li>\n'
    
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
    <meta property="og:url" content="https://wattsatpcontractor.com/services/{service["slug"]}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{service["title"]}">
    <meta name="twitter:description" content="{service["description"]}">
    <meta name="keywords" content="{service["title"]} Norfolk NE, professional installation services">
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

    <!-- Service Hero Section - Using homepage header styling -->
    <section class="hero">
        <h1>{service["title"]}</h1>
        <p class="certification-badge">ATP Approved Contractor • Nebraska Licensed #54690-25 • Serving All Nebraska</p>
        <p>Professional {service["title"].lower()} services in Norfolk NE and surrounding areas</p>
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

    <!-- Service Details with Gradient Cards -->
    <section class="services" style="padding: 80px 20px;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            
            <!-- Big Gradient Service Card -->
            <div class="service-card" style="max-width: 100%; margin: 0 auto 3rem auto; background: linear-gradient(135deg, var(--teal), var(--navy)); color: white; border-radius: 20px; overflow: hidden; box-shadow: var(--teal-glow); transition: all 0.4s ease;">
                <div class="service-content" style="padding: 3rem;">
                    <h2 class="service-title" style="color: white; font-size: 2.5rem; margin-bottom: 1.5rem; text-align: center;">Service Overview</h2>
                    <p class="service-description" style="color: white; font-size: 1.3rem; line-height: 1.7; text-align: center; margin-bottom: 2rem; opacity: 0.95;">
                        {service["description"]}
                    </p>
                    
                    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);">
                        <h3 style="color: white; margin-bottom: 1.5rem; text-align: center; border-bottom: 2px solid var(--gold); padding-bottom: 0.5rem; display: inline-block;">Services Included</h3>
                        <div style="columns: 2; gap: 2rem;">
                            <ul style="list-style: none; padding: 0; color: white;">
                                {services_list}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Additional Info Cards -->
            <div class="services-grid" style="grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px;">
                <!-- Why Choose Us Card -->
                <div class="service-card" style="background: var(--white); border-radius: 20px; padding: 2rem; box-shadow: var(--shadow); transition: all 0.3s ease;">
                    <h3 style="color: var(--navy); margin-bottom: 1rem; border-bottom: 3px solid var(--teal); padding-bottom: 0.5rem;">Why Choose Us</h3>
                    <ul style="list-style: none; padding: 0; color: var(--gray);">
                        <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-shield-alt" style="color: var(--teal); margin-right: 10px;"></i>ATP Approved Contractor</li>
                        <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-id-card" style="color: var(--teal); margin-right: 10px;"></i>Nebraska Licensed #54690-25</li>
                        <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-tools" style="color: var(--teal); margin-right: 10px;"></i>Professional Workmanship</li>
                        <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-dollar-sign" style="color: var(--teal); margin-right: 10px;"></i>Competitive Pricing</li>
                        <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-clock" style="color: var(--teal); margin-right: 10px;"></i>Timely Project Completion</li>
                    </ul>
                </div>

                <!-- Get Started Card -->
                <div class="service-card" style="background: linear-gradient(135deg, var(--gold), var(--warm-accent)); color: var(--navy); border-radius: 20px; padding: 2rem; box-shadow: var(--gold-glow); transition: all 0.3s ease;">
                    <h3 style="margin-bottom: 1rem; border-bottom: 3px solid var(--navy); padding-bottom: 0.5rem;">Get Started Today</h3>
                    <p style="margin-bottom: 1.5rem; font-size: 1.1rem;">Ready to transform your space with professional {service["title"].lower()} services?</p>
                    <div style="text-align: center;">
                        <a href="tel:+14054106402" class="cta-button" style="background: var(--navy); color: white; display: block; margin-bottom: 1rem;">Call (405) 410-6402</a>
                        <a href="/contact" class="cta-button" style="background: var(--teal); color: white; display: block;">Get Free Estimate</a>
                    </div>
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

print("Created 19 individual service pages with the excellent gradient card design!")
print("Features restored:")
print("- Big blueish-teal gradient cards")
print("- Color change on hover effects")
print("- Homepage header image styling")
print("- Professional elegance and uniformity")
print("- Full page descriptive service lists")
print("- That beautiful design you loved")