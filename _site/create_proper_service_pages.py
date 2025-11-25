# create_proper_service_pages.py
import os

# Proper service page template with all fixes
service_template = '''<!DOCTYPE html>
<html lang="en">
<head>
<script>if(window.location.pathname==="/index"){{window.history.replaceState({{}},"","/");}}</script>
<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="{description} ATP Approved Contractor. Nebraska Licensed #54690-25. Call (405) 410-6402">
  
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
    <meta name="mservice-lication-TileColor" content="#ffffff">
    <meta name="mservice-lication-TileImage" content="/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">
  
    <!-- SEO Meta Tags -->
    <meta name="google-site-verification" content="9uPoUkPF9bV3aKmaJyxbcnlzzXjxYLkUPb-YXyvOabU" />
    <meta property="og:title" content="{title} | Watts Safety Installs">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="https://wattsatpcontractor.com/services/{slug}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="keywords" content="{title} Norfolk NE, professional installation services">
    <meta name="author" content="Watts Safety Installs">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://wattsatpcontractor.com/services/{slug}">
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

    <!-- Service Hero Section -->
    <section class="hero" style="height: 50vh; min-height: 400px;">
        <h1>{title}</h1>
        <p class="certification-badge">ATP Approved Contractor • Nebraska Licensed #54690-25 • Serving All Nebraska</p>
        <p>Professional {title} Services in Norfolk NE</p>
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
            <div class="service-detail-content">
                <h2 class="section-title" style="text-align: left; margin-bottom: 30px;">Professional {title}</h2>
                
                <!-- Single Service Card with Hover Effects -->
                <div class="service-card" style="max-width: 100%; margin: 0; background: var(--white); border-radius: 20px; overflow: hidden; box-shadow: var(--teal-glow); transition: all 0.4s ease;">
                    <div class="service-content" style="padding: 3rem;">
                        <h3 class="service-title" style="color: var(--navy); font-size: 2rem; margin-bottom: 1.5rem; text-align: center; border-bottom: 3px solid var(--teal); padding-bottom: 1rem;">Service Overview</h3>
                        <p class="service-description" style="color: var(--gray); font-size: 1.2rem; line-height: 1.7; text-align: center; margin-bottom: 2rem;">
                            {description}
                        </p>
                        
                        <div style="background: #f8fafc; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
                            <h4 style="color: var(--navy); margin-bottom: 1rem; border-bottom: 2px solid var(--teal); padding-bottom: 0.5rem;">Service Details</h4>
                            <p style="line-height: 1.6; color: var(--gray);">{details}</p>
                        </div>

                        <div class="service-features" style="margin: 2rem 0;">
                            <h3 style="color: var(--navy); margin-bottom: 1rem; border-bottom: 2px solid var(--teal); padding-bottom: 0.5rem;">Key Benefits</h3>
                            <ul style="columns: 2; list-style: none; padding: 0; gap: 2rem;">
                                {benefits_html}
                            </ul>
                        </div>

                        <div style="background: linear-gradient(135deg, var(--teal), var(--navy)); color: white; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
                            <h3 style="margin-bottom: 1rem; text-align: center;">Why Choose Watts Safety Installs?</h3>
                            <ul style="list-style: none; padding: 0; text-align: center;">
                                <li style="margin-bottom: 0.8rem; display: inline-block; margin-right: 2rem;"><i class="fas fa-shield-alt" style="margin-right: 10px;"></i>ATP Approved Contractor</li>
                                <li style="margin-bottom: 0.8rem; display: inline-block; margin-right: 2rem;"><i class="fas fa-id-card" style="margin-right: 10px;"></i>Nebraska Licensed</li>
                                <li style="margin-bottom: 0.8rem; display: inline-block;"><i class="fas fa-tools" style="margin-right: 10px;"></i>Professional Workmanship</li>
                            </ul>
                        </div>

                        <!-- Clean, Professional Buttons -->
                        <div class="service-cta" style="margin-top: 2rem; text-align: center;">
                            <a href="tel:+14054106402" class="cta-button" style="display: inline-block; margin: 0 10px; padding: 12px 25px; font-size: 1.1rem;">Call Now: (405) 410-6402</a>
                            <a href="/contact" class="cta-button" style="display: inline-block; margin: 0 10px; padding: 12px 25px; font-size: 1.1rem; background: var(--navy);">Get Free Estimate</a>
                        </div>
                    </div>
                </div>

                <!-- Working Back Button -->
                <div class="back-to-services" style="text-align: center; margin-top: 3rem;">
                    <a href="/services.html" style="color: var(--teal); text-decoration: none; font-weight: 600; font-size: 1.1rem; padding: 10px 20px; border: 2px solid var(--teal); border-radius: 5px; transition: all 0.3s ease;">
                        <i class="fas fa-arrow-left"></i> Back to All Services
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Final CTA Section -->
    <section class="cta-section">
        <h2>Ready for Professional {title}?</h2>
        <p>Contact us today for a free consultation and estimate. We serve Norfolk NE and surrounding areas.</p>
        <a href="tel:+14054106402" class="cta-button">Call Now: (405) 410-6402</a>
    </section>

    {footer}

    {scripts}
</body>
</html>'''

# Service data
service_data = {
    "ada-compliant-showers-bathrooms": {
        "title": "ADA-Compliant Showers & Bathrooms",
        "description": "Professional ADA-compliant bathroom modifications with zero-step showers, grab bars, and wheelchair-accessible layouts. Full compliance with Americans with Disabilities Act standards.",
        "details": "Our ADA bathroom renovations include roll-in showers with fold-down seats, handheld showerheads, anti-scald valves, raised toilet seats, and vanity modifications for wheelchair access.",
        "benefits": [
            "Enhanced safety and independence",
            "Full ADA compliance certification", 
            "Increased property value",
            "Professional installation with lifetime warranty"
        ]
    },
    "kitchen-renovations": {
        "title": "Kitchen Renovations",
        "description": "Complete kitchen remodeling services in Norfolk NE including cabinet installation, countertop replacement, and appliance setup. We create functional, beautiful kitchens.",
        "details": "Cabinet refacing or replacement, quartz and granite countertops, tile backsplashes, flooring installation, lighting upgrades, and appliance installation with full plumbing and electrical.",
        "benefits": [
            "Increased home value",
            "Energy-efficient appliance options",
            "Custom cabinet design",
            "Project management included"
        ]
    },
    "tv-mounting": {
        "title": "TV Mounting",
        "description": "Professional TV wall mounting service for flat screens up to 85 inches. Secure installation with optimal viewing height and complete cable management.",
        "details": "Full-motion, tilting, and fixed TV mounts installed into studs with proper weight capacity. Includes cable concealment, power management, and device connectivity.",
        "benefits": [
            "Stud-mounted security",
            "Optimal viewing height placement",
            "Complete cable management",
            "Device connectivity setup"
        ]
    }
}

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

# Create proper service pages
for slug, service in service_data.items():
    page_path = f'services/{slug}.html'
    
    # Build benefits HTML
    benefits_html = ""
    for benefit in service["benefits"]:
        benefits_html += f'<li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-check-circle" style="color: var(--teal); margin-right: 10px;"></i>{benefit}</li>\n'
    
    # Create the page
    html_content = service_template.format(
        title=service["title"],
        description=service["description"],
        details=service["details"],
        benefits_html=benefits_html,
        slug=slug,
        styles=styles,
        header=header,
        footer=footer,
        scripts=scripts
    )
    
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created proper: {page_path}")

print("Created properly structured service pages with all fixes!")