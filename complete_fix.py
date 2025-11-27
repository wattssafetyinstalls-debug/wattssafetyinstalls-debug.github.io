#!/usr/bin/env python3
"""
Complete fix for all service pages - handles all file naming patterns
"""

import os
import shutil

# Your template (same as before)
NEW_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{service_name} | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="Professional {service_name} in Norfolk NE. ATP Approved Contractor. Call (405) 410-6402 for free estimate.">
    
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-KCPM8VZ');</script>
    
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        /* Your full CSS from template */
        :root {{
            --teal: #00C4B4;
            --navy: #0A1D37;
            --light: #F8FAFC;
            --gray: #64748B;
            --gold: #FFD700;
            --white: #FFFFFF;
            --warm-light: #FEF7ED;
            --shadow: 0 10px 30px rgba(0,0,0,0.08);
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
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        /* ... include all your CSS from the template ... */
    </style>
</head>
<body>
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KCPM8VZ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <header>
        <div class="nav-container">
            <a href="../index.html" class="logo">WATTS</a>
            <button class="mobile-menu-btn" id="mobileMenuBtn"><i class="fas fa-bars"></i></button>
            <nav class="nav-links" id="navLinks">
                <a href="../services.html">Services</a>
                <a href="../service-area.html">Service Area</a>
                <a href="../about.html">About</a>
                <a href="../referrals.html">Referrals</a>
                <a href="../contact.html">Contact</a>
            </nav>
        </div>
    </header>

    <section class="hero">
        <h1>{service_name}</h1>
        <p class="certification-badge">ATP Approved Contractor • Nebraska Licensed #54690-25</p>
        <p>Professional {service_name} in Norfolk NE & Surrounding Areas</p>
        <a href="tel:+14054106402" class="cta-button">Call (405) 410-6402</a>
    </section>

    <div class="service-tile">
        <h2>{service_name}</h2>
        <p class="service-description">{service_description}</p>

        <div class="trust-bar">
            <div class="trust-item"><div class="trust-icon"><i class="fas fa-check-circle"></i></div><div class="trust-text">Licensed & Insured</div></div>
            <div class="trust-item"><div class="trust-icon"><i class="fas fa-star"></i></div><div class="trust-text">5.0/5 Rating</div></div>
            <div class="trust-item"><div class="trust-icon"><i class="fas fa-bolt"></i></div><div class="trust-text">Same-Day Available</div></div>
            <div class="trust-item"><div class="trust-icon"><i class="fas fa-trophy"></i></div><div class="trust-text">ATP Approved</div></div>
        </div>

        <div class="service-showcase">
            <h3>Comprehensive Service Solutions</h3>
            <div class="service-categories">
                <div class="service-category">
                    <div class="category-icon"><i class="fas fa-universal-access"></i></div>
                    <div class="category-title">Accessibility & Safety</div>
                    <div class="category-services">ADA Ramps, Grab Bars, Senior Safety</div>
                </div>
                <div class="service-category">
                    <div class="category-icon"><i class="fas fa-home"></i></div>
                    <div class="category-title">Home Improvements</div>
                    <div class="category-services">Remodeling, Decks, Siding & Windows</div>
                </div>
                <div class="service-category">
                    <div class="category-icon"><i class="fas fa-tv"></i></div>
                    <div class="category-title">Audio Visual</div>
                    <div class="category-services">TV Mounting, Home Theater, Smart Audio</div>
                </div>
                <div class="service-category">
                    <div class="category-icon"><i class="fas fa-snowflake"></i></div>
                    <div class="category-title">Property Maintenance</div>
                    <div class="category-services">Snow Removal, Lawn Care, Seasonal</div>
                </div>
            </div>
        </div>

        <a href="tel:+14054106402" class="contact-btn">Contact Us Now</a>
    </div>

    <a href="../services.html" class="return-btn">Return to All Services</a>

    <footer>
        <p><strong>Watts Safety Installs</strong> • Norfolk, NE • 
            <span class="footer-contact">
                <a href="tel:+14054106402">(405) 410-6402</a> • 
                <a href="mailto:wattssafetyinstalls@gmail.com">wattssafetyinstalls@gmail.com</a>
            </span>
        </p>
        <div class="footer-links">
            <a href="../sitemap.html">Sitemap</a> • <a href="../privacy-policy.html">Privacy Policy</a>
        </div>
        <p style="margin-top:20px; font-size:0.9rem; color:#aaa;">© 2025 Watts Safety Installs. Nebraska License #54690-25</p>
    </footer>

    <script>
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {{
            document.getElementById('navLinks').classList.toggle('active');
        }});
    </script>
</body>
</html>'''

def get_service_info(filename):
    """Generate service name and description based on filename"""
    base_name = filename.replace('.html', '').replace('-', ' ').title()
    
    # Custom descriptions for better SEO
    descriptions = {
        'accessibility-safety-solutions': 'Professional accessibility and safety solutions in Norfolk NE. We specialize in ADA compliance, grab bar installations, wheelchair ramps, and senior safety modifications to create secure, accessible environments.',
        'ada-compliant-showers': 'ADA compliant shower installations and bathroom modifications in Norfolk NE. Create accessible, safe bathrooms with zero-step entries, grab bars, and slip-resistant flooring.',
        'tv-mounting': 'Professional TV mounting services in Norfolk NE. Secure wall mounting, optimal viewing angles, cable management for residential and commercial installations.',
        'snow-removal': 'Reliable snow removal and de-icing services in Norfolk NE. Emergency snow removal available with 15% OFF first 3 visits in 2025.',
        'lawn-maintenance': 'Comprehensive lawn maintenance and care services in Norfolk NE. Regular mowing, fertilization, weed control with LAWN2026 20% OFF season special.',
        'kitchen-renovations': 'Professional kitchen renovations and remodeling in Norfolk NE. Transform your kitchen with custom cabinets, countertops, and modern appliances.',
        'bathroom-remodels': 'Complete bathroom remodeling services in Norfolk NE. Create beautiful, functional bathrooms with accessibility features and modern designs.',
        # Add more specific descriptions as needed
    }
    
    # Find matching description or use generic
    for key, desc in descriptions.items():
        if key in filename.lower():
            return base_name, desc
    
    # Generic description
    generic_desc = f'Professional {base_name} services in Norfolk NE. ATP Approved Contractor serving all of Nebraska with licensed, insured, and same-day service availability. Call (405) 410-6402 for free estimate.'
    
    return base_name, generic_desc

def update_all_service_pages():
    """Update ALL service pages regardless of filename"""
    
    services_dir = './services'
    updated_count = 0
    
    for filename in os.listdir(services_dir):
        if filename.endswith('.html') and not filename.endswith('.backup'):
            filepath = os.path.join(services_dir, filename)
            
            # Get service info based on filename
            service_name, service_description = get_service_info(filename)
            
            # Generate new content
            new_content = NEW_TEMPLATE.format(
                service_name=service_name,
                service_description=service_description
            )
            
            # Backup original file
            backup_path = filepath + '.backup2'
            shutil.copy2(filepath, backup_path)
            
            # Write new content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            updated_count += 1
            print(f"Updated: {filename}")
    
    print(f"Successfully updated {updated_count} service pages!")
    print("Original files backed up with .backup2 extension")

if __name__ == "__main__":
    update_all_service_pages()