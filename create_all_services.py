import os
import re
from datetime import datetime

# Simple slugify function without external dependencies
def simple_slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

# Your services data - updated to match your homepage structure exactly
services = [
    {
        "id": "accessibility-safety",
        "title": "Accessibility & Safety Solutions", 
        "description": "Professional installation of ADA-compliant accessibility features and safety modifications for homes and businesses.",
        "hero_image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        "sub_services": [
            {"name": "ADA-compliant showers & bathrooms", "slug": "ada-compliant-showers"},
            {"name": "Grab bar installation", "slug": "grab-bar-installation"},
            {"name": "Wheelchair ramp installation", "slug": "wheelchair-ramp-installation"},
            {"name": "Stairlift & elevator installation", "slug": "stairlift-elevator-installation"},
            {"name": "Non-slip flooring solutions", "slug": "non-slip-flooring"}
        ]
    },
    {
        "id": "home-remodeling",
        "title": "Home Remodeling & Renovation",
        "description": "Complete home transformation services including kitchens, bathrooms, and whole-house renovations.",
        "hero_image": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        "sub_services": [
            {"name": "Kitchen renovations", "slug": "kitchen-renovations"},
            {"name": "Bathroom remodels", "slug": "bathroom-remodels"},
            {"name": "Room additions", "slug": "room-additions"},
            {"name": "Flooring installation", "slug": "flooring-installation"},
            {"name": "Painting & drywall", "slug": "painting-drywall"}
        ]
    },
    {
        "id": "tv-mounting",
        "title": "TV & Home Theater Setup",
        "description": "Professional TV mounting, home theater installation, and entertainment system setup.",
        "hero_image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        "sub_services": [
            {"name": "TV mounting on walls", "slug": "tv-mounting"},
            {"name": "Home theater system installation", "slug": "home-theater-installation"},
            {"name": "Sound bar & speaker setup", "slug": "sound-system-setup"},
            {"name": "Cable management solutions", "slug": "cable-management"}
        ]
    },
    {
        "id": "property-maintenance", 
        "title": "Property Maintenance, Snow Removal & Lawn Care",
        "description": "Keep your property in top condition year-round with our comprehensive maintenance services.",
        "hero_image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2058&q=80",
        "sub_services": [
            {"name": "Lawn maintenance & care", "slug": "lawn-maintenance"},
            {"name": "Pressure washing services", "slug": "pressure-washing"},
            {"name": "Gutter cleaning & repair", "slug": "gutter-cleaning"},
            {"name": "Fence repair & installation", "slug": "fence-repair"},
            {"name": "General handyman services", "slug": "handyman-services"}
        ]
    }
]

# Create services directory
os.makedirs('services', exist_ok=True)

# Read your actual index.html to copy the exact styling and structure
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Extract header from index.html
    header_start = index_content.find('<header>')
    header_end = index_content.find('</header>') + 9
    header = index_content[header_start:header_end]
    
    # Extract footer from index.html
    footer_start = index_content.find('<footer>')
    footer_end = index_content.find('</footer>') + 9
    footer = index_content[footer_start:footer_end]
    
    # Extract CSS styles from index.html
    style_start = index_content.find('<style>')
    style_end = index_content.find('</style>') + 8
    styles = index_content[style_start:style_end]
    
    # Extract scripts from index.html
    script_start = index_content.find('<script>')
    script_end = index_content.find('</script>') + 9
    scripts = index_content[script_start:script_end]
    
except FileNotFoundError:
    print("Warning: index.html not found. Using fallback templates.")
    header = '''
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
                <a href="/service-area">Service Area</a>
                <a href="/about">About</a>
                <a href="/referrals">Referrals</a>
                <a href="/contact">Contact</a>
            </nav>
            <a href="tel:+14054106402" class="phone-link">
                <i class="fas fa-phone"></i> (405) 410-6402
            </a>
        </div>
    </header>
    '''
    footer = '''
    <footer>
        <div class="footer-container">
            <div class="footer-about">
                <div class="footer-logo">WATTS SAFETY INSTALLS</div>
                <p>Nebraska's premier ATP Approved Contractor specializing in accessibility modifications, safety installations, TV mounting, and comprehensive home services near you.</p>
                <p>Nebraska License #54690-25 • ATP Approved Contractor</p>
                <p><a href="/sitemap">Sitemap</a> | <a href="/privacy-policy">Privacy Policy</a> | <a href="/referrals">Referral Program</a></p>
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
            <p>© 2024 Watts Safety Installs. All rights reserved. | Nebraska License #54690-25 • ATP Approved Contractor</p>
        </div>
    </footer>
    '''
    styles = '''
    <style>
        /* Your full CSS from index.html would go here */
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
    </style>
    '''
    scripts = '''
    <script>
        // Mobile menu toggle
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {
            document.getElementById('navLinks').classList.toggle('active');
        });
    </script>
    '''

# Generate HTML pages for each sub-service with EXACT same styling as homepage
for service in services:
    for sub in service["sub_services"]:
        page_path = f'services/{sub["slug"]}.html'
        
        # Create detailed content that matches your index.html styling exactly
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script>if(window.location.pathname==="/index"){{window.history.replaceState({{}},"","/");}}</script>
<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sub["name"]} | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="Professional {sub["name"]} services in Norfolk NE. {service['description']} 15% OFF First 3 Snow Visits 2025. LAWN2026 - 20% OFF Season.">
  
    <!-- Favicon -->
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
  
    <!-- Search Engine & Social Media Meta Tags -->
    <meta name="google-site-verification" content="9uPo