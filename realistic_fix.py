#!/usr/bin/env python3
"""
FINAL PERFECT RESTORE - Realistic professional descriptions
Accurate for current business stage - no overpromising
"""

import os

# Your PERFECT working template (copy-pasted from above)
PERFECT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__SERVICENAME__ | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="Professional __SERVICENAME__ in Norfolk NE. Same-day service. Call (405) 410-6402.">
    
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-KCPM8VZ');</script>
    <!-- End Google Tag Manager -->

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXXXXX');
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <style>
        :root {
            --teal: #00C4B4;
            --navy: #0A1D37;
            --light: #F8FAFC;
            --gray: #64748B;
            --gold: #FFD700;
            --white: #FFFFFF;
            --warm-light: #FEF7ED;
            --shadow: 0 10px 30px rgba(0,0,0,0.08);
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--warm-light);
            color: #1E293B;
            line-height: 1.7;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        /* Navigation */
        header {
            background: var(--navy);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .logo {
            font-family: 'Playfair Display', serif;
            font-size: 2.8rem;
            color: var(--teal);
            text-decoration: none;
            font-weight: 700;
        }
        .nav-links {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        .nav-links a {
            color: var(--white);
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s;
            position: relative;
            padding: 10px 0;
        }
        .nav-links a:hover {
            color: var(--teal);
        }
        .nav-links a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 3px;
            bottom: 0;
            left: 0;
            background-color: var(--teal);
            transition: width 0.3s;
        }
        .nav-links a:hover::after {
            width: 100%;
        }
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--white);
            font-size: 1.8rem;
            cursor: pointer;
        }
        
        .hero {
            height: 85vh;
            min-height: 600px;
            background: linear-gradient(135deg, rgba(10,29,55,0.9), rgba(245,158,11,0.25)),
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80') center/cover;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
        }
        .hero h1 {
            font-family: 'Playfair Display', serif;
            font-size: 4.5rem;
            margin-bottom: 15px;
        }
        .certification-badge {
            background: var(--gold);
            color: var(--navy);
            padding: 10px 28px;
            border-radius: 50px;
            font-weight: 700;
        }
        .cta-button {
            background: var(--teal);
            color: white;
            padding: 20px 60px;
            border-radius: 50px;
            font-size: 1.4rem;
            font-weight: 700;
            text-decoration: none;
            margin-top: 30px;
            box-shadow: 0 12px 30px rgba(0,196,180,0.4);
            transition: all .3s;
        }
        .cta-button:hover, .cta-button:active {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,196,180,0.6);
        }

        /* PREMIUM SERVICE TILE */
        .service-tile {
            max-width: 1200px;
            margin: 70px auto;
            padding: 60px 50px;
            background: white;
            border-radius: 32px;
            box-shadow: var(--shadow);
            text-align: center;
            position: relative;
            overflow: hidden;
            border: 3px solid transparent;
            cursor: pointer;
            transition: all 0.55s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .service-tile::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }
        .service-tile::after {
            content: '';
            position: absolute;
            inset: -8px;
            border-radius: 38px;
            border: 4px solid transparent;
            opacity: 0;
            box-shadow: 0 0 30px rgba(0,196,180,0);
            transition: all 0.5s ease;
            pointer-events: none;
        }
        @media (hover:hover) and (pointer:fine) {
            .service-tile:hover {
                transform: translateY(-14px) scale(1.035);
                box-shadow: 0 40px 100px rgba(10,29,55,0.4);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-tile:hover::before {
                opacity: 1;
                animation: gloss 1.6s ease-out forwards;
            }
            .service-tile:hover::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.6);
                box-shadow: 0 0 40px rgba(0,196,180,0.5);
            }
            .service-tile:hover h2, .service-tile:hover p, .service-tile:hover .trust-text {
                color: white !important;
            }
            .service-tile:hover .trust-bar {
                background: rgba(255,255,255,0.12);
            }
            .service-tile:hover .trust-icon {
                transform: scale(1.5) translateY(-8px);
                color: var(--gold) !important;
            }
        }
        @media (hover:none), (max-width:768px) {
            .service-tile:active {
                transform: translateY(-12px) scale(1.03);
                box-shadow: 0 35px 90px rgba(10,29,55,0.38);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-tile:active::before {
                opacity: 1;
                animation: gloss 1.3s ease-out forwards;
            }
            .service-tile:active::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.7);
                box-shadow: 0 0 35px rgba(0,196,180,0.6);
            }
            .service-tile:active h2, .service-tile:active p, .service-tile:active .trust-text {
                color: white !important;
            }
            .service-tile:active .trust-bar {
                background: rgba(255,255,255,0.12);
            }
            .service-tile:active .trust-icon {
                transform: scale(1.5) translateY(-8px);
                color: var(--gold) !important;
            }
        }
        @keyframes gloss {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .service-tile h2 {
            font-family: 'Playfair Display', serif;
            font-size: 3.2rem;
            color: var(--navy);
            margin-bottom: 25px;
            transition: color 0.4s;
        }
        .service-description {
            font-size: 1.25rem;
            color: #444;
            margin-bottom: 45px;
            line-height: 1.8;
            transition: color 0.4s;
        }
        
        /* SMALLER TRUST BAR - Reduced size for better SEO space */
        .trust-bar {
            background: var(--light);
            padding: 30px 35px; /* Reduced padding */
            border-radius: 20px; /* Slightly smaller radius */
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px; /* Reduced gap */
            transition: all 0.5s;
            margin-bottom: 35px; /* Reduced margin */
        }
        .trust-item {
            text-align: center;
            flex: 1;
            min-width: 140px; /* Slightly smaller minimum width */
        }
        .trust-icon {
            font-size: 2.5rem; /* Smaller icons */
            color: var(--teal);
            margin-bottom: 8px; /* Reduced margin */
            transition: all 0.4s ease;
        }
        .trust-text {
            font-weight: 600;
            color: var(--navy);
            font-size: 0.95rem; /* Slightly smaller text */
            transition: color 0.4s;
        }

        /* Professional Service Showcase */
        .service-showcase {
            margin-top: 50px;
            padding: 40px;
            background: var(--light);
            border-radius: 20px;
            text-align: center;
        }
        .service-showcase h3 {
            font-size: 1.8rem;
            color: var(--navy);
            margin-bottom: 30px;
            font-family: 'Playfair Display', serif;
        }
        
        /* FIXED: Service Categories 4-Grid Layout */
        .service-categories {
            display: grid;
            grid-template-columns: repeat(4, 1fr); /* Fixed 4-column grid */
            gap: 25px;
            margin-top: 30px;
        }
        
        /* Service Category Tiles */
        .service-category {
            background: var(--white);
            padding: 25px;
            border-radius: 15px;
            box-shadow: var(--shadow);
            transition: all 0.55s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
            border: 2px solid transparent;
            cursor: pointer;
        }
        .service-category::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }
        .service-category::after {
            content: '';
            position: absolute;
            inset: -4px;
            border-radius: 19px;
            border: 2px solid transparent;
            opacity: 0;
            box-shadow: 0 0 20px rgba(0,196,180,0);
            transition: all 0.5s ease;
            pointer-events: none;
        }
        
        /* Hover effects for service category tiles */
        @media (hover:hover) and (pointer:fine) {
            .service-category:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 25px 60px rgba(10,29,55,0.3);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-category:hover::before {
                opacity: 1;
                animation: gloss 1.6s ease-out forwards;
            }
            .service-category:hover::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.6);
                box-shadow: 0 0 30px rgba(0,196,180,0.5);
            }
            .service-category:hover .category-title,
            .service-category:hover .category-services {
                color: white !important;
            }
            .service-category:hover .category-icon {
                transform: scale(1.3) translateY(-5px);
                color: var(--gold) !important;
            }
        }
        @media (hover:none), (max-width:768px) {
            .service-category:active {
                transform: translateY(-6px) scale(1.01);
                box-shadow: 0 20px 45px rgba(10,29,55,0.25);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-category:active::before {
                opacity: 1;
                animation: gloss 1.3s ease-out forwards;
            }
            .service-category:active::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.7);
                box-shadow: 0 0 25px rgba(0,196,180,0.6);
            }
            .service-category:active .category-title,
            .service-category:active .category-services {
                color: white !important;
            }
            .service-category:active .category-icon {
                transform: scale(1.3) translateY(-5px);
                color: var(--gold) !important;
            }
        }

        .category-icon {
            font-size: 2.5rem;
            color: var(--teal);
            margin-bottom: 15px;
            transition: all 0.4s ease;
        }
        .category-title {
            font-weight: 700;
            color: var(--navy);
            margin-bottom: 10px;
            font-size: 1.2rem;
            transition: color 0.4s;
        }
        .category-services {
            color: var(--gray);
            font-size: 0.95rem;
            line-height: 1.5;
            transition: color 0.4s;
        }

        .contact-btn {
            background: var(--teal);
            color: white;
            padding: 16px 48px;
            border-radius: 50px;
            font-weight: 700;
            text-decoration: none;
            box-shadow: 0 8px 25px rgba(0,196,180,0.4);
            transition: all .35s;
        }
        .contact-btn:hover, .contact-btn:active {
            transform: translateY(-5px) scale(1.06);
            box-shadow: 0 15px 35px rgba(0,196,180,0.6);
        }
        .return-btn {
            display: inline-block;
            background: var(--gray);
            color: white;
            padding: 12px 32px;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            margin: 40px auto 0;
            transition: all .35s;
        }
        .return-btn:hover, .return-btn:active {
            background: var(--teal);
            transform: translateY(-4px);
        }
        footer {
            background: var(--navy);
            color: white;
            padding: 80px 20px 30px;
            margin-top: auto;
            text-align: center;
        }
        .footer-contact a {
            color: var(--teal);
            text-decoration: none;
            transition: color .3s;
        }
        .footer-contact a:hover {
            color: var(--gold);
        }
        .footer-links a {
            color: var(--teal);
            margin: 0 15px;
            text-decoration: none;
        }
        .footer-links a:hover {
            color: var(--gold);
        }

        /* Mobile Responsive */
        @media (max-width: 1024px) {
            .service-categories {
                grid-template-columns: repeat(2, 1fr); /* 2 columns on tablets */
            }
        }

        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            .service-tile {
                margin: 40px 15px;
                padding: 40px 25px;
            }
            .trust-bar {
                flex-direction: column;
                padding: 25px 20px; /* Even smaller on mobile */
                gap: 15px;
            }
            .trust-item {
                min-width: 100%;
            }
            .service-categories {
                grid-template-columns: 1fr; /* 1 column on mobile */
            }
            .nav-links {
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
            }
            .nav-links.active {
                display: flex;
            }
            .nav-links a {
                padding: 15px 0;
                font-size: 1.2rem;
                text-align: center;
                width: 100%;
                display: block;
            }
            .mobile-menu-btn {
                display: block;
            }
        }
    </style>
</head>
<body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KCPM8VZ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <header>
        <div class="nav-container">
            <a href="index.html" class="logo">WATTS</a>
            
            <button class="mobile-menu-btn" id="mobileMenuBtn">
                <i class="fas fa-bars"></i>
            </button>
            
            <nav class="nav-links" id="navLinks">
                <a href="services.html">Services</a>
                <a href="service-area.html">Service Area</a>
                <a href="about.html">About</a>
                <a href="referrals.html">Referrals</a>
                <a href="contact.html">Contact</a>
            </nav>
        </div>
    </header>

    <section class="hero">
        <h1>__SERVICENAME__</h1>
        <p class="certification-badge">ATP Approved Contractor • Nebraska Licensed #54690-25</p>
        <p>Professional __SERVICENAME__ in Norfolk NE</p>
        <a href="tel:+14054106402" class="cta-button">Call (405) 410-6402</a>
    </section>

    <div class="service-tile">
        <h2>__SERVICENAME__</h2>
        <p class="service-description">__UNIQUE_DESCRIPTION__</p>

        <div class="trust-bar">
            <div class="trust-item"><div class="trust-icon"><i class="fas fa-check-circle"></i></div><div class="trust-text">Licensed & Insured</div></div>
            <div class="trust-item"><div class="trust-icon"><i class="fas fa-star"></i></div><div class="trust-text">5.0/5 Rating</div></div>
            <div class="trust-item"><div class="trust-icon"><i class="fas fa-bolt"></i></div><div class="trust-text">Same-Day Available</div></div>
            <div class="trust-item"><div class="trust-icon"><i class="fas fa-trophy"></i></div><div class="trust-text">ATP Approved</div></div>
        </div>

        <!-- Service Showcase with 4-Grid Layout -->
        <div class="service-showcase">
            <h3>Comprehensive Service Solutions</h3>
            
            <div class="service-categories">
                <div class="service-category">
                    <div class="category-icon"><i class="fas fa-universal-access"></i></div>
                    <div class="category-title">Accessibility & Safety</div>
                    <div class="category-services">ADA Ramps, Grab Bars, Senior Safety Modifications</div>
                </div>
                <div class="service-category">
                    <div class="category-icon"><i class="fas fa-home"></i></div>
                    <div class="category-title">Home Improvements</div>
                    <div class="category-services">Remodeling, Deck Construction, Siding & Windows</div>
                </div>
                <div class="service-category">
                    <div class="category-icon"><i class="fas fa-tv"></i></div>
                    <div class="category-title">Audio Visual</div>
                    <div class="category-services">TV Mounting, Home Theater, Smart Home Integration</div>
                </div>
                <div class="service-category">
                    <div class="category-icon"><i class="fas fa-snowflake"></i></div>
                    <div class="category-title">Property Maintenance</div>
                    <div class="category-services">Snow Removal, Lawn Care, Seasonal Services</div>
                </div>
            </div>
        </div>

        <a href="tel:+14054106402" class="contact-btn">Contact Us Now</a>
    </div>

    <a href="/services.html" class="return-btn">Return to All Services</a>

    <footer>
        <p><strong>Watts Safety Installs</strong> • Norfolk, NE • 
            <span class="footer-contact">
                <a href="tel:+14054106402">(405) 410-6402</a> • 
                <a href="mailto:wattssafetyinstalls@gmail.com">wattssafetyinstalls@gmail.com</a>
            </span>
        </p>
        <div class="footer-links">
            <a href="/sitemap.html">Sitemap</a> • <a href="/privacy-policy.html">Privacy Policy</a> • <a href="/terms.html">Terms of Service</a>
        </div>
        <p style="margin-top:20px; font-size:0.9rem; color:#aaa;">© 2025 Watts Safety Installs. All rights reserved.</p>
    </footer>

    <script>
        // Mobile menu toggle
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {
            document.getElementById('navLinks').classList.toggle('active');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            const navLinks = document.getElementById('navLinks');
            const mobileMenuBtn = document.getElementById('mobileMenuBtn');
            
            if (!navLinks.contains(event.target) && !mobileMenuBtn.contains(event.target)) {
                navLinks.classList.remove('active');
            }
        });

        // GA4 Event Tracking
        document.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function(e) {
                gtag('event', 'link_click', {
                    'event_category': 'Navigation',
                    'event_label': this.href,
                    'transport_type': 'beacon'
                });
            });
        });
    </script>
</body>
</html>"""

# REALISTIC PROFESSIONAL DESCRIPTIONS - No overpromising
PREMIUM_DESCRIPTIONS = {
    "tv-mounting.html": """Professional TV mounting services in Norfolk, NE and surrounding Northeast Nebraska areas. Watts Safety Installs provides reliable television wall mounting with proper viewing angles, cable management, and secure installations. I serve Norfolk, Madison, Stanton, Pierce, and nearby communities with flexible scheduling to meet your needs.

I mount various TV sizes and types on different surfaces including drywall, brick, and fireplace mantels. Each installation includes basic wire management and uses quality mounts that provide stability and safety. I can also help set up soundbars and basic home theater components to enhance your viewing experience.

Homeowners appreciate my attention to detail and clean installation work. I focus on making sure your TV is securely mounted at the right height and position for comfortable viewing. Voice search friendly: "Find TV mounting service in Norfolk Nebraska" - Watts Safety Installs provides dependable service you can trust.

Safety and quality workmanship are my priorities. As a licensed Nebraska contractor #54690-25, I ensure every installation meets proper safety standards. Call (405) 410-6402 today to discuss your TV mounting needs and get a straightforward quote.""",

    "snow-removal.html": """Reliable snow removal services in Norfolk, Nebraska and surrounding areas. Watts Safety Installs provides driveway clearing, sidewalk shoveling, and basic ice management for residential properties throughout Northeast Nebraska including Norfolk, Madison, Stanton, and Pierce communities.

When winter weather hits, I'm ready to help keep your property accessible and safe. Using dependable equipment and proper techniques, I focus on clearing driveways, walkways, and steps to prevent slips and falls. I use pet-safe ice melt and pay attention to details like mailbox access and proper drainage areas.

I offer flexible service options based on your needs and budget. Whether you need one-time clearing after a storm or occasional assistance throughout the winter, I provide honest pricing and reliable work. My goal is to make winter easier for homeowners who need help with snow removal.

As a local contractor who understands Nebraska winters, I provide practical snow removal solutions that work. Voice search ready: "Find snow shoveling service in Norfolk NE" - Watts Safety Installs offers the help you need during winter months.

Don't struggle with snow removal alone this winter. Call (405) 410-6402 to discuss your snow clearing needs and get a fair price for professional service.""",

    "flooring-installation.html": """Professional flooring installation services in Norfolk NE serving the local community. Watts Safety Installs handles various flooring types including laminate, luxury vinyl plank, and basic carpet installation for homes in Norfolk and surrounding areas.

I help homeowners transform their spaces with quality flooring installations using proper techniques and attention to detail. From subfloor preparation to final trim work, I focus on doing the job right. I work with you to select materials that fit your budget and lifestyle needs.

Whether you're updating one room or need flooring throughout your home, I provide honest assessments and clear pricing. I take the time to explain your options and help you choose flooring that will work well in Nebraska's climate conditions.

Voice search friendly: "Find flooring installation in Norfolk Nebraska" - Watts Safety Installs delivers quality work at fair prices.

Call (405) 410-6402 today to discuss your flooring project and get a straightforward estimate for professional installation work.""",
    
    # Default for all other pages - more realistic
    "default": """Professional home improvement and safety services in Norfolk, Nebraska. Watts Safety Installs serves Northeast Nebraska including Norfolk, Madison, Stanton, Pierce, and surrounding communities with reliable workmanship and honest service.

As your local licensed contractor (Nebraska License #54690-25), I specialize in practical home solutions including safety modifications, basic remodeling, property maintenance, and repair work. Every project receives careful attention and quality workmanship.

Homeowners trust me for grab bar installation, basic home repairs, TV mounting, minor remodeling projects, and seasonal maintenance. I believe in providing good value - quality work at fair prices with clear communication throughout the process.

I understand that every home and budget is different, which is why I offer flexible solutions that meet your specific needs. Voice search friendly: "Find handyman services in Norfolk Nebraska" - Watts Safety Installs provides the reliable help you need.

Experience the difference of working with a contractor who cares about doing the job right. Call (405) 410-6402 today to discuss your project needs."""
}

def restore_perfect_template():
    services_dir = "services"
    fixed_count = 0
    
    for filename in os.listdir(services_dir):
        if not filename.endswith(".html") or filename.endswith(".backup"):
            continue
            
        filepath = os.path.join(services_dir, filename)
        
        # Extract service name from filename
        service_name = filename.replace(".html", "").replace("-", " ").replace("_", " ").title()
        
        # Get premium description or use default
        description = PREMIUM_DESCRIPTIONS.get(filename, PREMIUM_DESCRIPTIONS["default"])
        
        # Build final HTML with perfect template
        final_html = PERFECT_TEMPLATE.replace("__SERVICENAME__", service_name)
        final_html = final_html.replace("__UNIQUE_DESCRIPTION__", description)
        
        # Write the file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_html)
        
        print(f"RESTORED REALISTIC TEMPLATE -> {filename}")
        fixed_count += 1
    
    print(f"\nSUCCESS! {fixed_count} service pages now have:")
    print("   - Perfect working template design")
    print("   - 4 small tiles with FULL hover + tap effects")
    print("   - Realistic professional descriptions")
    print("   - No overpromising - accurate business representation")
    print("   - Voice search optimization")
    print("\nTest it now: python -m http.server 8000")

if __name__ == "__main__":
    restore_perfect_template()