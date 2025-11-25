# enhance_service_pages.py

import os

# Detailed service data with specific descriptions and relevant images
services_enhanced = [
    {
        "id": "accessibility-safety",
        "title": "Accessibility & Safety Solutions",
        "hero_image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
        "sub_services": [
            {
                "name": "ADA-compliant showers & bathrooms",
                "slug": "ada-compliant-showers",
                "image": "https://images.unsplash.com/photo-1584622744904-801a3d2d73a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Professional ADA-compliant bathroom modifications including zero-step showers, grab bars, accessible sinks, and wheelchair-friendly layouts. We ensure complete compliance with Americans with Disabilities Act standards for both residential and commercial properties in Norfolk NE.",
                "details": "Our ADA bathroom renovations include roll-in showers with fold-down seats, handheld showerheads, anti-scald valves, raised toilet seats, and vanity modifications for wheelchair access. We handle everything from design to installation with certified ADA compliance.",
                "benefits": [
                    "Enhanced safety and independence",
                    "Full ADA compliance certification",
                    "Increased property value",
                    "Professional installation with lifetime warranty"
                ]
            },
            {
                "name": "Grab bar installation",
                "slug": "grab-bar-installation", 
                "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Commercial-grade grab bar installation rated for 500+ lbs weight capacity. Strategic placement in bathrooms, hallways, and stairways for maximum safety and fall prevention throughout your Norfolk NE home.",
                "details": "We install stainless steel and chrome grab bars with reinforced mounting into wall studs. Professional placement in showers, beside toilets, along hallways, and on staircases for comprehensive fall protection.",
                "benefits": [
                    "500+ lb weight capacity",
                    "Reinforced stud mounting",
                    "Rust-resistant materials", 
                    "Professional placement consultation"
                ]
            },
            {
                "name": "Wheelchair ramp installation",
                "slug": "wheelchair-ramp-installation",
                "image": "https://images.unsplash.com/photo-1572021335466-1e8b5a0c8aab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Custom wheelchair ramp installation meeting ADA slope requirements for safe, accessible home entry. Permanent and modular ramp solutions for Norfolk NE homes and businesses.",
                "details": "We build aluminum, wood, and concrete ramps with proper 1:12 slope ratios, handrails, and non-slip surfaces. Includes landing platforms and weather-resistant construction.",
                "benefits": [
                    "ADA-compliant 1:12 slope",
                    "Multiple material options",
                    "Weather-resistant construction",
                    "Building permit assistance"
                ]
            },
            {
                "name": "Stairlift & elevator installation",
                "slug": "stairlift-elevator-installation",
                "image": "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80", 
                "description": "Professional stairlift and residential elevator installation for multi-story homes. We provide Acorn, Bruno, and Harmar stairlifts with full service and maintenance.",
                "details": "Straight and curved stairlift installation, residential elevator setup, and platform lift solutions. Includes safety features, remote controls, and ongoing maintenance services.",
                "benefits": [
                    "Brand-name equipment (Acorn, Bruno, Harmar)",
                    "Professional installation and training",
                    "Maintenance and repair services", 
                    "Financing options available"
                ]
            },
            {
                "name": "Non-slip flooring solutions",
                "slug": "non-slip-flooring",
                "image": "https://images.unsplash.com/photo-1560449752-3ed683137d93?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Slip-resistant flooring installation for bathrooms, kitchens, and entryways. We use textured tiles, non-slip vinyl, and epoxy coatings to prevent falls in Norfolk NE homes.",
                "details": "Non-slip ceramic tile, textured vinyl flooring, epoxy coatings, and rubber flooring installations. Perfect for bathrooms, kitchens, laundry rooms, and entryways.",
                "benefits": [
                    "Wet-area slip resistance",
                    "Easy to clean and maintain",
                    "ADA-compliant surfaces",
                    "Multiple style options"
                ]
            }
        ]
    },
    {
        "id": "home-remodeling", 
        "title": "Home Remodeling & Renovation",
        "hero_image": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
        "sub_services": [
            {
                "name": "Kitchen renovations",
                "slug": "kitchen-renovations",
                "image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Complete kitchen remodeling services in Norfolk NE including cabinet installation, countertop replacement, flooring, and appliance setup. We create functional, beautiful kitchens that fit your lifestyle.",
                "details": "Cabinet refacing or replacement, quartz and granite countertops, tile backsplashes, flooring installation, lighting upgrades, and appliance installation with full plumbing and electrical.",
                "benefits": [
                    "Increased home value",
                    "Energy-efficient appliance options", 
                    "Custom cabinet design",
                    "Project management included"
                ]
            },
            {
                "name": "Bathroom remodels",
                "slug": "bathroom-remodels",
                "image": "https://images.unsplash.com/photo-1584622744904-801a3d2d73a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Bathroom renovation services including tub-to-shower conversions, vanity installation, tile work, and lighting upgrades. We create spa-like retreats in your Norfolk NE home.",
                "details": "Shower and tub replacements, vanity installation, toilet upgrades, tile flooring and walls, lighting fixtures, ventilation systems, and plumbing updates.",
                "benefits": [
                    "Modern fixture upgrades",
                    "Water-efficient installations",
                    "Mold-resistant materials",
                    "Increased functionality"
                ]
            },
            {
                "name": "Room additions",
                "slug": "room-additions", 
                "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Professional room addition construction for growing families in Norfolk NE. We handle everything from foundation to finishing for sunrooms, bedrooms, and office spaces.",
                "details": "Foundation work, framing, roofing, electrical, plumbing, insulation, drywall, and finishing. We obtain all necessary permits and ensure code compliance.",
                "benefits": [
                    "Increased living space",
                    "Professional design consultation",
                    "Permit and code compliance",
                    "Seamless integration with existing structure"
                ]
            },
            {
                "name": "Flooring installation",
                "slug": "flooring-installation",
                "image": "https://images.unsplash.com/photo-1560449752-3ed683137d93?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Professional flooring installation including hardwood, laminate, vinyl, tile, and carpet. We provide flooring solutions for every room in your Norfolk NE home.",
                "details": "Hardwood floor installation and refinishing, laminate flooring, luxury vinyl plank, ceramic and porcelain tile, and carpet installation with proper subfloor preparation.",
                "benefits": [
                    "Wide material selection",
                    "Professional subfloor preparation",
                    "Warranty on materials and labor", 
                    "Quick installation timeline"
                ]
            },
            {
                "name": "Painting & drywall",
                "slug": "painting-drywall",
                "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Interior and exterior painting services with drywall repair and installation. We use premium paints and proper surface preparation for lasting results in Norfolk NE homes.",
                "details": "Interior painting, exterior painting, drywall installation, taping, mudding, texture matching, popcorn ceiling removal, and wall repair services.",
                "benefits": [
                    "Premium paint brands (Sherwin-Williams, Benjamin Moore)",
                    "Proper surface preparation",
                    "Clean, professional finish",
                    "Drywall texture matching"
                ]
            }
        ]
    },
    {
        "id": "tv-mounting",
        "title": "TV & Home Theater Setup", 
        "hero_image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
        "sub_services": [
            {
                "name": "TV mounting on walls",
                "slug": "tv-mounting",
                "image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Professional TV wall mounting service for flat screens up to 85 inches. We ensure secure installation at optimal viewing height with complete cable management in Norfolk NE homes.",
                "details": "Full-motion, tilting, and fixed TV mounts installed into studs with proper weight capacity. Includes cable concealment, power management, and device connectivity.",
                "benefits": [
                    "Stud-mounted security",
                    "Optimal viewing height placement",
                    "Complete cable management",
                    "Device connectivity setup"
                ]
            },
            {
                "name": "Home theater system installation",
                "slug": "home-theater-installation",
                "image": "https://images.unsplash.com/photo-1563297007-0686b7003af7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80", 
                "description": "Complete home theater installation including surround sound, projection systems, and media center setup. We create immersive entertainment experiences for Norfolk NE homeowners.",
                "details": "5.1 and 7.1 surround sound systems, 4K projectors, motorized screens, media consoles, streaming device setup, and acoustic optimization.",
                "benefits": [
                    "Professional audio calibration",
                    "Seamless device integration",
                    "Acoustic room optimization",
                    "Universal remote programming"
                ]
            },
            {
                "name": "Sound bar & speaker setup",
                "slug": "sound-system-setup",
                "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Sound bar and wireless speaker installation with optimal placement for superior audio quality. We integrate with your existing TV and streaming systems in Norfolk NE.",
                "details": "Sound bar mounting and calibration, wireless speaker placement, subwoofer positioning, and audio synchronization with TV and streaming devices.",
                "benefits": [
                    "Optimal speaker placement",
                    "Wireless system integration", 
                    "Audio synchronization",
                    "Easy-to-use controls"
                ]
            },
            {
                "name": "Cable management solutions",
                "slug": "cable-management",
                "image": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Professional cable management and concealment for clean, organized entertainment centers. We eliminate cord clutter for safety and aesthetics in Norfolk NE homes.",
                "details": "In-wall cable running, cord concealment systems, power management, surge protection installation, and organized media center setup.",
                "benefits": [
                    "Clean, professional appearance",
                    "Reduced tripping hazards",
                    "Surge protection installation",
                    "Easy future upgrades"
                ]
            }
        ]
    },
    {
        "id": "property-maintenance",
        "title": "Property Maintenance, Snow Removal & Lawn Care", 
        "hero_image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2058&q=80",
        "sub_services": [
            {
                "name": "Lawn maintenance & care",
                "slug": "lawn-maintenance",
                "image": "https://images.unsplash.com/photo-1578309851877-65a2e0db4152?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Comprehensive lawn care services including mowing, edging, fertilization, and weed control. We keep your Norfolk NE property looking beautiful year-round.",
                "details": "Weekly/bi-weekly mowing, string trimming, edging, fertilization programs, weed control, aeration, overseeding, and lawn health monitoring.",
                "benefits": [
                    "Consistent, professional cut",
                    "Customized fertilization plans",
                    "Weed and pest control",
                    "Seasonal lawn care programs"
                ]
            },
            {
                "name": "Pressure washing services",
                "slug": "pressure-washing",
                "image": "https://images.unsplash.com/photo-1578301978892-1df48dfc5d9e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Professional pressure washing for driveways, siding, decks, and patios. We restore your Norfolk NE property's exterior to like-new condition.",
                "details": "Driveway and sidewalk cleaning, house siding washing, deck and patio restoration, fence cleaning, and roof stain removal with eco-friendly cleaning solutions.",
                "benefits": [
                    "Restores curb appeal",
                    "Prevents mold and mildew",
                    "Eco-friendly cleaning solutions", 
                    "Extends surface life"
                ]
            },
            {
                "name": "Gutter cleaning & repair",
                "slug": "gutter-cleaning",
                "image": "https://images.unsplash.com/photo-1578632749014-ca77efd052eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Gutter cleaning, repair, and guard installation to protect your Norfolk NE home from water damage. We ensure proper drainage and prevent foundation issues.",
                "details": "Gutter cleaning, downspout clearing, leak repairs, gutter realignment, guard installation, and seasonal maintenance plans.",
                "benefits": [
                    "Prevents water damage",
                    "Protects foundation",
                    "Extends gutter life",
                    "Seasonal maintenance plans"
                ]
            },
            {
                "name": "Fence repair & installation",
                "slug": "fence-repair", 
                "image": "https://images.unsplash.com/photo-1578632749014-ca77efd052eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Fence installation and repair services for wood, vinyl, and chain-link fences. We enhance privacy and security for Norfolk NE properties.",
                "details": "Wood fence construction and repair, vinyl fence installation, chain-link fencing, gate installation and repair, and post replacement services.",
                "benefits": [
                    "Increased privacy and security",
                    "Professional gate installation",
                    "Durable materials and construction",
                    "Property value enhancement"
                ]
            },
            {
                "name": "General handyman services",
                "slug": "handyman-services",
                "image": "https://images.unsplash.com/photo-1581094794329-cdc0c0ba3b0d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
                "description": "Comprehensive handyman services for home repairs, installations, and maintenance tasks. We're your one-call solution for Norfolk NE home upkeep.",
                "details": "Drywall repair, painting touch-ups, door and window repair, shelf installation, furniture assembly, minor plumbing and electrical fixes, and general home maintenance.",
                "benefits": [
                    "One-call solution for multiple tasks",
                    "Quick response times",
                    "Quality workmanship",
                    "Affordable pricing"
                ]
            }
        ]
    }
]

# Read your index.html to get the styling and structure
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Extract header, footer, styles, and scripts
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

# Generate enhanced service pages
for service in services_enhanced:
    for sub in service["sub_services"]:
        page_path = f'services/{sub["slug"]}.html'
        
        # Build benefits list HTML
        benefits_html = ""
        for benefit in sub["benefits"]:
            benefits_html += f'<li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-check-circle" style="color: var(--teal); margin-right: 10px;"></i>{benefit}</li>\n'
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script>if(window.location.pathname==="/index"){{window.history.replaceState({{}},"","/");}}</script>
<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sub["name"]} Services | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="{sub["description"]} 15% OFF First 3 Snow Visits 2025. LAWN2026 - 20% OFF Season. Call (405) 410-6402">
  
    <!-- Favicon and meta tags from index.html -->
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
    <meta property="og:title" content="{sub["name"]} Services | Watts Safety Installs">
    <meta property="og:description" content="{sub["description"]}">
    <meta property="og:image" content="{sub["image"]}">
    <meta property="og:url" content="https://wattsatpcontractor.com/services/{sub["slug"]}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{sub["name"]} Services">
    <meta name="twitter:description" content="{sub["description"]}">
    <meta name="twitter:image" content="{sub["image"]}">
    <meta name="keywords" content="{sub["name"]} Norfolk NE, {service['title']} near me, professional installation services">
    <meta name="author" content="Watts Safety Installs">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://wattsatpcontractor.com/services/{sub["slug"]}">
    <meta http-equiv="Cache-Control" content="max-age=31536000, public">
 
    <!-- Fonts and Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
    <!-- Structured Data -->
    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{sub["name"]}",
  "description": "{sub["description"]}",
  "provider": {{
    "@type": "HomeAndConstructionBusiness",
    "name": "Watts Safety Installs",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "500 Block Omaha Ave",
      "addressLocality": "Norfolk",
      "addressRegion": "NE",
      "postalCode": "68701"
    }},
    "telephone": "+14054106402",
    "areaServed": "Nebraska"
  }},
  "areaServed": "Nebraska"
}}
</script>
 
    {styles}
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KCPM8VZ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    {header}

    <!-- Service Hero Section -->
    <section class="hero" style="height: 50vh; min-height: 400px;">
        <h1>{sub["name"]}</h1>
        <p class="certification-badge">ATP Approved Contractor • Nebraska Licensed #54690-25 • Serving All Nebraska</p>
        <p>Professional {sub["name"]} Services in Norfolk NE</p>
        <div class="promo-banner">
            <p style="font-size:1.4rem; margin:0"><strong>15% OFF First 3 Snow Visits 2025</strong> • <strong>LAWN2026 – 20% OFF Season</strong></p>
        </div>
        <a href="tel:+14054106402" class="cta-button">Call (405) 410-6402 – Free Quote</a>
    </section>

    <!-- Service Details Section -->
    <section class="services" style="padding: 80px 20px;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            <div class="service-detail-content">
                <h2 class="section-title" style="text-align: left; margin-bottom: 30px;">Professional {sub["name"]}</h2>
                
                <div class="service-card" style="max-width: 100%; margin: 0;">
                    <img loading="lazy" src="{sub["image"]}" alt="{sub["name"]} - Watts Safety Installs Norfolk NE" class="service-image" style="height: 400px; object-fit: cover;">
                    <div class="service-content">
                        <h3 class="service-title">{sub["name"]} Services</h3>
                        <p class="service-description" style="max-height: none; overflow: visible; font-size: 1.1rem; line-height: 1.7;">
                            {sub["description"]}
                        </p>
                        
                        <div style="background: #f8fafc; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
                            <h4 style="color: var(--navy); margin-bottom: 1rem;">Service Details</h4>
                            <p style="line-height: 1.6;">{sub["details"]}</p>
                        </div>

                        <div class="service-features" style="margin: 2rem 0;">
                            <h3 style="color: var(--navy); margin-bottom: 1rem; border-bottom: 2px solid var(--teal); padding-bottom: 0.5rem;">Key Benefits</h3>
                            <ul style="columns: 2; list-style: none; padding: 0;">
                                {benefits_html}
                            </ul>
                        </div>

                        <div style="background: linear-gradient(135deg, var(--teal), var(--navy)); color: white; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
                            <h3 style="margin-bottom: 1rem;">Why Choose Watts Safety Installs?</h3>
                            <ul style="list-style: none; padding: 0;">
                                <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-shield-alt" style="margin-right: 10px;"></i>ATP Approved Contractor</li>
                                <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-id-card" style="margin-right: 10px;"></i>Nebraska Licensed #54690-25</li>
                                <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-tools" style="margin-right: 10px;"></i>Professional Workmanship</li>
                                <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-dollar-sign" style="margin-right: 10px;"></i>Competitive Pricing</li>
                                <li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-clock" style="margin-right: 10px;"></i>Timely Project Completion</li>
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
        print(f"Enhanced: {page_path}")

print("All service pages enhanced with detailed content and relevant images!")
print("Service pages now feature:")
print("✅ Specific, relevant images for each service")
print("✅ Detailed SEO-rich descriptions") 
print("✅ Comprehensive service details and benefits")
print("✅ Professional content structure")
print("✅ Enhanced trust elements and CTAs")