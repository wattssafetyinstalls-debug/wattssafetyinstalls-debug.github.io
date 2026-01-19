#!/usr/bin/env python3
"""
Create complete DBA site pages matching ATP structure exactly
"""

import shutil
from pathlib import Path

def create_dba_services_page():
    """Create DBA services.html by copying and rebranding ATP services.html"""
    
    # Read ATP services page
    with open('services.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rebrand for DBA
    replacements = {
        'Watts ATP Contractor': 'Watts Safety Installs',
        'WATTS ATP CONTRACTOR': 'WATTS SAFETY INSTALLS',
        'ATP Approved Contractor': 'Sister company of Watts ATP Contractor',
        'Accessibility & Safety Services': 'Complete Home Services',
        'ATP Accessibility & Safety Services': 'Our Complete Home Services',
        'Professional ADA accessibility and aging-in-place services': 'Professional home services including TV mounting, remodeling, and property maintenance',
        'ADA accessibility and aging-in-place modifications for safer, more accessible living': 'Complete home services for all your TV mounting, remodeling, and maintenance needs',
        'Professional ADA compliance and aging-in-place solutions designed to create safer, more accessible living environments': 'Comprehensive home services designed to enhance your property and lifestyle',
        
        # Color scheme
        '--teal: #00C4B4': '--primary: #dc2626',
        '--navy: #0A1D37': '--dark: #0a0a0a',
        '--gold: #FFD700': '--secondary: #fef3c7',
        'var(--teal)': 'var(--primary)',
        'var(--navy)': 'var(--dark)',
        'var(--gold)': 'var(--secondary)',
        
        # URLs
        'href="/services/': 'href="/safety-installs/services/',
        'href="services/': 'href="/safety-installs/services/',
        '/services.html': '/safety-installs/services.html',
        'wattsatpcontractor.com/services': 'wattsatpcontractor.com/safety-installs/services',
        
        # Navigation
        '<a href="/services">Services</a>': '<a href="/safety-installs/services.html">Services</a>',
        '<a href="/">Home</a>': '<a href="/safety-installs/">Home</a>',
        '<a href="/about">About</a>': '<a href="/safety-installs/about.html">About</a>',
        '<a href="/contact">Contact</a>': '<a href="/safety-installs/contact.html">Contact</a>',
        '<a href="/service-area">Service Area</a>': '<a href="/safety-installs/service-area.html">Service Area</a>',
        
        # Theme color
        'name="theme-color" content="#ffffff"': 'name="theme-color" content="#000000"',
        
        # Canonical
        'canonical" href="https://wattsatpcontractor.com/services"': 'canonical" href="https://wattsatpcontractor.com/safety-installs/services"',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Remove the "Looking for Other Home Services" section since this IS the home services site
    # Replace with "Looking for Accessibility Services" pointing back to ATP
    content = content.replace(
        '<!-- DBA Services Redirect Section -->',
        '<!-- ATP Services Redirect Section -->'
    )
    content = content.replace(
        '<h2 class="seasonal-title">Looking for Other Home Services?</h2>',
        '<h2 class="seasonal-title">Looking for Accessibility Services?</h2>'
    )
    content = content.replace(
        '<p class="seasonal-subtitle">TV mounting, snow removal, lawn care, home remodeling, and more available through our home services division</p>',
        '<p class="seasonal-subtitle">ADA accessibility, grab bars, wheelchair ramps, and senior safety modifications available through our sister company</p>'
    )
    
    # Update promo cards to point back to ATP
    content = content.replace(
        '<div class="promo-icon">📺</div>\n<h3 class="promo-title">TV & Home Theater</h3>',
        '<div class="promo-icon">♿</div>\n<h3 class="promo-title">Accessibility & Safety</h3>'
    )
    content = content.replace(
        '<p class="promo-description">Professional TV mounting, home theater installation, soundbar setup, and complete audio/visual solutions.</p>',
        '<p class="promo-description">Professional ADA accessibility modifications, grab bars, wheelchair ramps, and senior safety solutions.</p>'
    )
    content = content.replace(
        '<a class="promo-cta" href="/safety-installs/services.html">View Services</a>',
        '<a class="promo-cta" href="/services.html">View Services</a>'
    )
    
    content = content.replace(
        '<div class="promo-icon">🏠</div>\n<h3 class="promo-title">Home Remodeling</h3>',
        '<div class="promo-icon">🛁</div>\n<h3 class="promo-title">Accessible Bathrooms</h3>'
    )
    content = content.replace(
        '<p class="promo-description">Kitchen renovations, bathroom remodels, basement finishing, deck construction, and complete home improvements.</p>',
        '<p class="promo-description">ADA-compliant showers, walk-in tubs, grab bars, non-slip flooring, and complete bathroom accessibility upgrades.</p>'
    )
    
    content = content.replace(
        '<div class="promo-icon">🌿</div>\n<h3 class="promo-title">Property Maintenance</h3>',
        '<div class="promo-icon">🚪</div>\n<h3 class="promo-title">Ramps & Mobility</h3>'
    )
    content = content.replace(
        '<p class="promo-description">Snow removal, lawn care, landscaping, gutter cleaning, pressure washing, and seasonal maintenance.</p>\n<div class="promo-code">SNOW2025 • LAWN2026</div>',
        '<p class="promo-description">Custom wheelchair ramps, stairlifts, elevator installation, and complete mobility solutions for safer living.</p>'
    )
    
    content = content.replace(
        '<a href="/safety-installs/" class="cta-button" style="background: #dc2626;">Visit Watts Safety Installs →</a>',
        '<a href="/" class="cta-button" style="background: #00C4B4;">Visit Watts ATP Contractor →</a>'
    )
    
    # Write DBA services page
    dba_dir = Path('safety-installs')
    dba_dir.mkdir(exist_ok=True)
    
    with open(dba_dir / 'services.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Created: safety-installs/services.html")

def create_dba_about_page():
    """Create DBA about page by copying and rebranding ATP about page"""
    
    if not Path('about.html').exists():
        print("⚠️  about.html not found, skipping")
        return
    
    with open('about.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rebrand for DBA
    replacements = {
        'Watts ATP Contractor': 'Watts Safety Installs',
        'WATTS ATP CONTRACTOR': 'WATTS SAFETY INSTALLS',
        'ATP Approved Contractor': 'Sister company of Watts ATP Contractor',
        
        # Color scheme
        '--teal: #00C4B4': '--primary: #dc2626',
        '--navy: #0A1D37': '--dark: #0a0a0a',
        '--gold: #FFD700': '--secondary: #fef3c7',
        'var(--teal)': 'var(--primary)',
        'var(--navy)': 'var(--dark)',
        'var(--gold)': 'var(--secondary)',
        
        # URLs and navigation
        'href="/services': 'href="/safety-installs/services',
        'href="/about"': 'href="/safety-installs/about.html"',
        'href="/contact"': 'href="/safety-installs/contact.html"',
        'href="/service-area"': 'href="/safety-installs/service-area.html"',
        'href="/"': 'href="/safety-installs/"',
        
        # Theme
        'name="theme-color" content="#ffffff"': 'name="theme-color" content="#000000"',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Write DBA about page
    with open('safety-installs/about.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Created: safety-installs/about.html")

def create_dba_contact_page():
    """Create DBA contact page by copying and rebranding ATP contact page"""
    
    if not Path('contact.html').exists():
        print("⚠️  contact.html not found, skipping")
        return
    
    with open('contact.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rebrand for DBA
    replacements = {
        'Watts ATP Contractor': 'Watts Safety Installs',
        'WATTS ATP CONTRACTOR': 'WATTS SAFETY INSTALLS',
        'ATP Approved Contractor': 'Sister company of Watts ATP Contractor',
        
        # Color scheme
        '--teal: #00C4B4': '--primary: #dc2626',
        '--navy: #0A1D37': '--dark: #0a0a0a',
        '--gold: #FFD700': '--secondary: #fef3c7',
        'var(--teal)': 'var(--primary)',
        'var(--navy)': 'var(--dark)',
        'var(--gold)': 'var(--secondary)',
        
        # URLs and navigation
        'href="/services': 'href="/safety-installs/services',
        'href="/about"': 'href="/safety-installs/about.html"',
        'href="/contact"': 'href="/safety-installs/contact.html"',
        'href="/service-area"': 'href="/safety-installs/service-area.html"',
        'href="/"': 'href="/safety-installs/"',
        
        # Theme
        'name="theme-color" content="#ffffff"': 'name="theme-color" content="#000000"',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Write DBA contact page
    with open('safety-installs/contact.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Created: safety-installs/contact.html")

def create_dba_service_area_page():
    """Create DBA service area page by copying and rebranding ATP service area page"""
    
    service_area_file = Path('service-area.html')
    if not service_area_file.exists():
        service_area_file = Path('service-area') / 'index.html'
    
    if not service_area_file.exists():
        print("⚠️  service-area page not found, skipping")
        return
    
    with open(service_area_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rebrand for DBA
    replacements = {
        'Watts ATP Contractor': 'Watts Safety Installs',
        'WATTS ATP CONTRACTOR': 'WATTS SAFETY INSTALLS',
        'ATP Approved Contractor': 'Sister company of Watts ATP Contractor',
        
        # Color scheme
        '--teal: #00C4B4': '--primary: #dc2626',
        '--navy: #0A1D37': '--dark: #0a0a0a',
        '--gold: #FFD700': '--secondary: #fef3c7',
        'var(--teal)': 'var(--primary)',
        'var(--navy)': 'var(--dark)',
        'var(--gold)': 'var(--secondary)',
        
        # URLs and navigation
        'href="/services': 'href="/safety-installs/services',
        'href="/about"': 'href="/safety-installs/about.html"',
        'href="/contact"': 'href="/safety-installs/contact.html"',
        'href="/service-area"': 'href="/safety-installs/service-area.html"',
        'href="/"': 'href="/safety-installs/"',
        
        # Theme
        'name="theme-color" content="#ffffff"': 'name="theme-color" content="#000000"',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Write DBA service area page
    with open('safety-installs/service-area.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Created: safety-installs/service-area.html")

def main():
    print("🚀 Creating complete DBA site structure...\n")
    
    create_dba_services_page()
    create_dba_about_page()
    create_dba_contact_page()
    create_dba_service_area_page()
    
    print("\n✨ DBA site structure complete!")
    print("   - All pages match ATP structure")
    print("   - Black/red/cream color scheme applied")
    print("   - Sister company branding throughout")

if __name__ == '__main__':
    main()
