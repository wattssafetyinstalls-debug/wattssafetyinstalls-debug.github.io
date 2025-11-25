# create_all_missing_services.py
import os
import json

def create_missing_services():
    print("CREATING ALL MISSING SERVICE PAGES...")
    
    # All missing service pages from your dropdown menus
    missing_services = [
        "driveway-installation", "concrete-pouring", "hardwood-flooring", "garden-maintenance",
        "seasonal-cleanup", "landscape-design", "seasonal-prep", "painting-services",
        "drywall-repair", "fence-installation", "window-doors", "audio-visual",
        "tv-mounting-residential", "home-audio", "fertilization", "snow-removal",
        "emergency-repairs", "tree-trimming", "emergency-snow", "custom-cabinets",
        "cabinet-refacing", "onyx-countertops", "kitchen-cabinetry", "custom-storage",
        "countertop-repair", "concrete-repair", "floor-refinishing", "patio-construction",
        "basement-finishing", "siding-replacement", "deck-construction", "home-remodeling",
        "grab-bars", "custom-ramps", "senior-safety", "bathroom-accessibility"
    ]
    
    # Service details with proper descriptions
    service_details = {
        "driveway-installation": {
            "title": "Driveway Installation",
            "description": "Professional driveway installation and concrete work for durable, beautiful driveways that enhance your property's curb appeal.",
            "services_list": ["Asphalt driveway installation", "Concrete driveway pouring", "Gravel driveway construction", "Driveway repair and resurfacing", "Driveway sealing and maintenance"]
        },
        "concrete-pouring": {
            "title": "Concrete Pouring", 
            "description": "Expert concrete pouring and finishing services for driveways, patios, sidewalks, and other concrete surfaces.",
            "services_list": ["Concrete slab pouring", "Patio concrete work", "Sidewalk installation", "Concrete finishing", "Concrete sealing and curing"]
        },
        "hardwood-flooring": {
            "title": "Hardwood Flooring",
            "description": "Beautiful hardwood floor installation and refinishing services to transform your space with timeless elegance.",
            "services_list": ["Hardwood floor installation", "Floor sanding and refinishing", "Engineered wood flooring", "Floor staining options", "Floor protection coating"]
        },
        "garden-maintenance": {
            "title": "Garden Maintenance",
            "description": "Complete garden maintenance services including planting, weeding, pruning, and seasonal care for beautiful outdoor spaces.",
            "services_list": ["Garden bed maintenance", "Planting and transplanting", "Weeding and mulching", "Seasonal cleanup", "Irrigation system maintenance"]
        },
        "landscape-design": {
            "title": "Landscape Design",
            "description": "Custom landscape design and installation to create beautiful, functional outdoor spaces that enhance your property.",
            "services_list": ["Custom landscape design", "Plant selection and placement", "Hardscape installation", "Garden bed creation", "Lighting design"]
        },
        "painting-services": {
            "title": "Painting Services",
            "description": "Professional interior and exterior painting services with quality materials and expert application for lasting results.",
            "services_list": ["Interior painting", "Exterior painting", "Wall preparation", "Color consultation", "Trim and detail work"]
        },
        "snow-removal": {
            "title": "Snow Removal",
            "description": "Reliable snow removal and de-icing services to keep your property safe and accessible all winter long.",
            "services_list": ["Residential snow removal", "Commercial snow clearing", "Driveway and sidewalk clearing", "Ice melting application", "Emergency snow services"]
        },
        "custom-cabinets": {
            "title": "Custom Cabinets",
            "description": "Custom cabinet design and installation for kitchens, bathrooms, and storage solutions tailored to your space.",
            "services_list": ["Custom cabinet design", "Kitchen cabinetry", "Bathroom vanities", "Built-in storage solutions", "Cabinet installation"]
        },
        "deck-construction": {
            "title": "Deck Construction", 
            "description": "Professional deck construction and repair services for beautiful outdoor living spaces that last for years.",
            "services_list": ["Custom deck design", "Deck construction", "Deck repair and restoration", "Railings and safety features", "Deck sealing and staining"]
        },
        "home-remodeling": {
            "title": "Home Remodeling",
            "description": "Complete home remodeling services to transform your living space with quality craftsmanship and attention to detail.",
            "services_list": ["Room additions", "Kitchen remodeling", "Bathroom renovations", "Basement finishing", "Whole-house remodeling"]
        },
        "grab-bars": {
            "title": "Grab Bars Installation",
            "description": "Commercial-grade grab bar installation for enhanced bathroom safety and accessibility for all ages and abilities.",
            "services_list": ["Bathroom grab bars", "Shower safety bars", "Toilet safety frames", "Commercial-grade installation", "ADA compliant placement"]
        },
        "custom-ramps": {
            "title": "Custom Ramps",
            "description": "Custom accessibility ramp installation for wheelchair access and mobility assistance throughout your property.",
            "services_list": ["Wheelchair ramps", "Porch and entry ramps", "Modular ramp systems", "Permanent concrete ramps", "ADA compliant designs"]
        }
    }
    
    # Default service template for services not in the details dictionary
    default_service_details = {
        "title": "",
        "description": "",
        "services_list": []
    }
    
    # Base template following your professional design
    service_template = """<!DOCTYPE html>
<html lang="en">
<head>
<script>if(window.location.pathname==="/index"){{window.history.replaceState({{}},"","/");}}</script>
<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="{description} Professional services in Norfolk NE. ATP Approved Contractor. Nebraska Licensed #54690-25. Call (405) 410-6402">
  
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
    <meta property="og:title" content="{title} | Watts Safety Installs">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="https://wattsatpcontractor.com/services/{service_slug}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="keywords" content="{title} Norfolk NE, professional installation services, home improvement">
    <meta name="author" content="Watts Safety Installs">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://wattsatpcontractor.com/services/{service_slug}">
    <meta http-equiv="Cache-Control" content="max-age=31536000, public">
 
    <!-- Fonts and Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
    <!-- Structured Data -->
    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{title}",
  "description": "{description}",
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
  "areaServed": "Nebraska",
  "url": "https://wattsatpcontractor.com/services/{service_slug}"
}}
</script>
 
    <style>
        :root {{
            --teal: #00C4B4;
            --navy: #0A1D37;
            --light: #F8FAFC;
            --gray: #64748B;
            --gold: #FFD700;
            --white: #FFFFFF;
            --warm-light: #FEF7ED;
            --warm-accent: #F59E0B;
            --warm-dark: #E07C10;
            --shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            --shadow-hover: 0 20px 50px rgba(0, 0, 0, 0.15);
            --teal-glow: 0 15px 40px rgba(0, 196, 180, 0.15);
            --navy-glow: 0 15px 40px rgba(10, 29, 55, 0.12);
            --gold-glow: 0 15px 40px rgba(255, 215, 0, 0.1);
        }}
     
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
     
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--warm-light);
            color: #1E293B;
            line-height: 1.7;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }}
     
        /* Professional Navigation */
        header {{
            background: var(--navy);
            padding: 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            width: 100%;
        }}
        .header-container {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            height: 80px;
        }}
        .logo-container {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .logo {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            color: var(--teal);
            font-weight: 700;
            text-decoration: none;
            letter-spacing: -0.5px;
        }}
        .nav-links {{
            display: flex;
            gap: 40px;
            align-items: center;
        }}
        .nav-links a {{
            color: var(--white);
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s;
            position: relative;
            padding: 10px 0;
        }}
        .nav-links a:hover {{
            color: var(--teal);
        }}
        .nav-links a::after {{
            content: '';
            position: absolute;
            width: 0;
            height: 3px;
            bottom: 0;
            left: 0;
            background-color: var(--teal);
            transition: width 0.3s;
        }}
        .nav-links a:hover::after {{
            width: 100%;
        }}
        .nav-links a.active {{
            color: var(--teal);
        }}
        .nav-links a.active::after {{
            width: 100%;
        }}
        .phone-link {{
            background: var(--teal);
            color: var(--white);
            padding: 12px 25px;
            border-radius: 50px;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.3s;
            white-space: nowrap;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,196,180,0.3);
        }}
        .phone-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,196,180,0.4);
            background: #00b3a4;
        }}
        /* MOBILE OPTIMIZATION - Phone Button */
        @media (max-width: 768px) {{
            .phone-link {{
                padding: 8px 16px;
                font-size: 0.9rem;
                margin-left: 10px;
            }}
        }}
        @media (max-width: 480px) {{
            .phone-link {{
                padding: 6px 12px;
                font-size: 0.85rem;
                margin-left: 8px;
            }}
        }}
        /* Improved Mobile Menu Button */
        .mobile-menu-btn {{
            display: none;
            background: none;
            border: none;
            color: var(--white);
            font-size: 1.8rem;
            cursor: pointer;
            padding: 12px;
            margin: -12px;
        }}
     
        .hero {{
            position: relative;
            height: 50vh;
            min-height: 400px;
            background: linear-gradient(135deg, var(--navy), #1e3a5f);
            color: var(--white);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 0 20px;
            width: 100%;
        }}
     
        .hero h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
        }}
        .certification-badge {{
            background: var(--gold);
            color: var(--navy);
            padding: 10px 25px;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 15px 0;
            display: inline-block;
            text-align: center;
        }}
        .promo-banner {{
            background: rgba(255,255,255,0.15);
            padding: 20px 35px;
            border-radius: 12px;
            margin: 25px 0;
            backdrop-filter: blur(10px);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .cta-button {{
            background: var(--teal);
            color: var(--white);
            padding: 20px 55px;
            border-radius: 50px;
            font-size: 1.3rem;
            font-weight: 700;
            text-decoration: none;
            box-shadow: 0 12px 30px rgba(0,196,180,0.4);
            display: inline-block;
            margin-top: 20px;
            transition: all 0.3s;
            text-align: center;
            border: none;
            cursor: pointer;
        }}
        .cta-button:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,196,180,0.6);
            background: #00b3a4;
        }}
     
        .trust-bar {{
            background: var(--white);
            padding: 40px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            width: 100%;
        }}
        .trust-container {{
            max-width: 1300px;
            margin: 0 auto;
            display: flex;
            justify-content: space-around;
            align-items: center;
            flex-wrap: wrap;
            padding: 0 20px;
            gap: 30px;
        }}
        .trust-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }}
        .trust-icon {{
            font-size: 3rem;
            color: var(--teal);
            margin-bottom: 15px;
        }}
        .trust-text {{
            font-weight: 600;
            color: var(--navy);
            font-size: 1.1rem;
        }}
     
        .services {{
            padding: 80px 20px;
            background: var(--warm-light);
            position: relative;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
      
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
      
        .service-detail-content {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            margin-top: -50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
      
        .section-title {{
            text-align: left;
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            color: var(--navy);
            margin-bottom: 30px;
            position: relative;
            z-index: 1;
            width: 100%;
        }}
      
        .service-card {{
            background: var(--white);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--teal-glow);
            transition: all 0.4s ease;
            border: 1px solid rgba(255, 255, 255, 0.8);
        }}
      
        .service-image {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            transition: transform 0.4s ease;
        }}
      
        .service-content {{
            padding: 30px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            gap: 15px;
            position: relative;
        }}
      
        .service-title {{
            font-size: 1.8rem;
            color: var(--navy);
            margin-bottom: 15px;
            font-family: 'Playfair Display', serif;
            position: relative;
            padding-bottom: 15px;
        }}
      
        .service-title::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 3px;
            background: linear-gradient(135deg, var(--teal), var(--warm-accent));
            border-radius: 2px;
        }}
      
        .service-description {{
            color: var(--gray);
            margin-bottom: 20px;
            line-height: 1.7;
            font-size: 1.1rem;
        }}
      
        .service-features {{
            margin: 2rem 0;
        }}
      
        .service-cta {{
            margin-top: 2rem;
            text-align: center;
        }}
      
        .back-to-services {{
            text-align: center;
            margin-top: 3rem;
        }}
      
        .return-to-services {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin: 30px 0;
            padding: 15px 30px;
            background: linear-gradient(135deg, var(--teal), #00a396);
            color: var(--white);
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,196,180,0.3);
            border: 2px solid transparent;
        }}
      
        .return-to-services:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,196,180,0.4);
            background: linear-gradient(135deg, var(--navy), #09182e);
        }}
      
        /* CTA Section */
        .cta-section {{
            padding: 100px 20px;
            background: linear-gradient(135deg, var(--teal), #00b3a4);
            color: var(--white);
            text-align: center;
        }}
      
        .cta-section h2 {{
            font-family: 'Playfair Display', serif;
            font-size: 3.2rem;
            margin-bottom: 20px;
        }}
      
        .cta-section p {{
            font-size: 1.3rem;
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
      
        footer {{
            background: var(--navy);
            color: var(--white);
            padding: 80px 20px 30px;
            width: 100%;
            margin-top: auto;
        }}
      
        .footer-container {{
            max-width: 1300px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 60px;
            width: 100%;
        }}
      
        .footer-logo {{
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            color: var(--teal);
            margin-bottom: 25px;
        }}
      
        .footer-about p {{
            margin-bottom: 20px;
            color: #cbd5e1;
            line-height: 1.7;
        }}
      
        .footer-links h3, .footer-contact h3 {{
            font-size: 1.4rem;
            margin-bottom: 25px;
            color: var(--teal);
        }}
      
        .footer-links ul {{
            list-style: none;
        }}
      
        .footer-links li {{
            margin-bottom: 12px;
        }}
      
        .footer-links a, .footer-contact a {{
            color: #cbd5e1;
            text-decoration: none;
            transition: color 0.3s;
            font-size: 1.05rem;
        }}
      
        .footer-links a:hover, .footer-contact a:hover {{
            color: var(--teal);
        }}
      
        .copyright {{
            text-align: center;
            padding-top: 50px;
            margin-top: 50px;
            border-top: 1px solid #334155;
            color: #94a3b8;
            width: 100%;
            font-size: 1rem;
        }}
      
        /* Responsive Design */
        @media (max-width: 1024px) {{
            .hero h1 {{ font-size: 2.5rem; }}
            .footer-container {{ grid-template-columns: 1fr 1fr; gap: 40px; }}
            .nav-links {{ gap: 25px; }}
        }}
      
        @media (max-width: 768px) {{
            .header-container {{
                padding: 0 15px;
                height: 70px;
            }}
            .nav-links {{
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                width: 100%;
                background: var(--navy);
                flex-direction: column;
                padding: 30px 20px;
                gap: 20px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .nav-links.active {{
                display: flex;
            }}
          
            .nav-links a {{
                padding: 15px 0;
                font-size: 1.2rem;
                text-align: center;
                width: 100%;
                display: block;
            }}
          
            .mobile-menu-btn {{
                display: block;
            }}
            .logo {{
                font-size: 2rem;
            }}
            .hero {{
                height: auto;
                padding: 80px 20px;
            }}
            .hero h1 {{
                font-size: 2.2rem;
            }}
            .section-title {{
                font-size: 2rem;
            }}
            .footer-container {{
                grid-template-columns: 1fr;
                gap: 40px;
            }}
            .trust-container {{
                gap: 25px;
            }}
            .trust-item {{
                flex: 0 0 45%;
            }}
        }}
      
        @media (max-width: 480px) {{
            .nav-links {{
                padding: 25px 15px;
                gap: 15px;
            }}
            .nav-links a {{
                font-size: 1.1rem;
                padding: 12px 0;
            }}
            .mobile-menu-btn {{
                font-size: 1.6rem;
                padding: 10px;
            }}
          
            .hero h1 {{
                font-size: 1.8rem;
            }}
            .section-title {{
                font-size: 1.8rem;
            }}
            .trust-item {{
                flex: 0 0 100%;
            }}
            .cta-button {{
                padding: 18px 40px;
                font-size: 1.2rem;
            }}
        }}
    </style>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KCPM8VZ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <header>
        <div class="header-container">
            <div class="logo-container">
                <a href="/" class="logo">WATTS</a>
            </div>
          
            <button class="mobile-menu-btn" id="mobileMenuBtn">
                <i class="fas fa-bars"></i>
            </button>
          
            <nav class="nav-links" id="navLinks">
                <a href="/">Home</a>
                <a href="/services.html">Services</a>
                <a href="/service-area.html">Service Area</a>
                <a href="/about.html">About</a>
                <a href="/referrals.html">Referrals</a>
                <a href="/contact.html">Contact</a>
            </nav>
          
            <a href="tel:+14054106402" class="phone-link">
                <i class="fas fa-phone"></i> (405) 410-6402
            </a>
        </div>
    </header>
    <!-- Service Hero Section -->
    <section class="hero">
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
    <section class="services">
        <div class="container">
            <div class="service-detail-content">
                <h2 class="section-title">Professional {title}</h2>
                
                <div class="service-card">
                    <div class="service-content">
                        <h3 class="service-title">{title} Services</h3>
                        <p class="service-description">
                            {description}
                        </p>
                        
                        <div style="background: #f8fafc; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
                            <h4 style="color: var(--navy); margin-bottom: 1rem;">Service Details</h4>
                            <p style="line-height: 1.6;">We provide comprehensive {title} solutions with attention to detail and quality craftsmanship. Our team of experienced professionals ensures every project meets the highest standards of quality and safety.</p>
                        </div>
                        
                        <div class="service-features">
                            <h3 style="color: var(--navy); margin-bottom: 1rem; border-bottom: 2px solid var(--teal); padding-bottom: 0.5rem;">Services Included</h3>
                            <ul style="columns: 2; list-style: none; padding: 0;">
                                {services_list_items}
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
                        
                        <div class="service-cta">
                            <a href="tel:+14054106402" class="cta-button" style="display: inline-block; margin: 0 10px; padding: 15px 30px;">Call Now: (405) 410-6402</a>
                            <a href="/contact.html" class="cta-button" style="display: inline-block; margin: 0 10px; padding: 15px 30px; background: var(--navy);">Get Free Estimate</a>
                        </div>
                    </div>
                </div>
                
                <div class="back-to-services">
                    <a href="/services.html" class="return-to-services">
                        <i class="fas fa-arrow-left"></i> Return to All Services
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
    
    <footer>
        <div class="footer-container">
            <div class="footer-about">
                <div class="footer-logo">WATTS SAFETY INSTALLS</div>
                <p>Nebraska's premier ATP Approved Contractor specializing in accessibility modifications, safety installations, TV mounting, and comprehensive home services near you.</p>
                <p>Nebraska License #54690-25 • ATP Approved Contractor</p>
                <p><a href="/sitemap.html">Sitemap</a> | <a href="/privacy-policy.html">Privacy Policy</a> | <a href="/referrals.html">Referral Program</a></p>
            </div>
            <div class="footer-links">
                <h3>Our Services</h3>
                <ul>
                    <li><a href="/services.html#accessibility-safety">Accessibility & Safety</a></li>
                    <li><a href="/services.html#home-remodeling">Home Remodeling</a></li>
                    <li><a href="/services.html#tv-mounting">TV Mounting & AV</a></li>
                    <li><a href="/services.html#property-maintenance">Property Maintenance</a></li>
                </ul>
            </div>
            <div class="footer-contact">
                <h3>Contact Us</h3>
                <p><strong>Phone:</strong> <a href="tel:+14054106402">(405) 410-6402</a></p>
                <p><strong>Email:</strong> <a href="mailto:wattssafetyinstalls@gmail.com">wattssafetyinstalls@gmail.com</a></p>
                <p><strong>Address:</strong> 500 Block Omaha Ave, Norfolk, NE 68701</p>
                <p><strong>Hours:</strong> Mon-Fri 8:30 AM - 6:00 PM, Sat On Call</p>
            </div>
        </div>
        <div class="copyright">
            <p>© <span id="current-year"></span> Watts Safety Installs. All rights reserved. | Nebraska License #54690-25 • ATP Approved Contractor</p>
        </div>
    </footer>
    
    <script>
        // Mobile menu functionality
        document.addEventListener('DOMContentLoaded', function() {{
            const mobileMenuBtn = document.getElementById('mobileMenuBtn');
            const navLinks = document.getElementById('navLinks');
            
            if (mobileMenuBtn && navLinks) {{
                mobileMenuBtn.addEventListener('click', function() {{
                    navLinks.classList.toggle('active');
                }});
            }}
            
            // Set current year in copyright
            document.getElementById('current-year').textContent = new Date().getFullYear();
        }});
        
        // Pretty URL handling
        if(window.location.pathname==="/index"){{
            window.history.replaceState({{}},"","/");
        }}
    </script>
</body>
</html>"""
    
    created_count = 0
    for service in missing_services:
        file_path = f"services/{service}.html"
        if not os.path.exists(file_path):
            # Get service details or use defaults
            details = service_details.get(service)
            if not details:
                # Create default details for services not in our dictionary
                title = service.replace('-', ' ').title()
                description = f"Professional {service.replace('-', ' ')} services with quality craftsmanship and attention to detail."
                services_list = [
                    f"{title} consultation",
                    f"Professional {service.replace('-', ' ')} installation",
                    f"{title} maintenance",
                    f"{title} repair services",
                    f"Custom {service.replace('-', ' ')} solutions"
                ]
                details = {
                    "title": title,
                    "description": description,
                    "services_list": services_list
                }
            
            # Generate services list items
            services_list_items = ""
            for service_item in details["services_list"]:
                services_list_items += f'<li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-check-circle" style="color: var(--teal); margin-right: 10px;"></i>{service_item}</li>\n'
            
            # Generate the page content
            content = service_template.format(
                title=details["title"],
                description=details["description"],
                service_slug=service,
                services_list_items=services_list_items
            )
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"CREATED: {file_path}")
            created_count += 1
        else:
            print(f"EXISTS: {file_path}")
    
    print(f"SUCCESS: Created {created_count} missing service pages!")
    print("All dropdown links should now work properly!")

if __name__ == "__main__":
    create_missing_services()