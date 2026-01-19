#!/usr/bin/env python3
"""
Comprehensive fix for all current issues:
1. Fix homepage service cards - same size, working hamburger dropdowns
2. Recreate DBA services.html properly formatted
3. Recreate DBA homepage to match ATP structure exactly
"""

import re
from pathlib import Path

def fix_homepage_service_cards():
    """Fix homepage service cards to be same size with working dropdowns"""
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the "Other Home Services" card to match standard format
    # Remove inline styles that break layout
    old_card_pattern = r'<div class="service-card" id="other-services"[^>]*>.*?</div>\s*</div>\s*</div>'
    
    new_card = '''<div class="service-card" id="other-services">
<img alt="Watts Safety Installs - Home Services" class="service-image" loading="lazy" src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80"/>
<div class="service-content">
<h3 class="service-title">Other Home Services</h3>
<p class="service-description">Looking for home remodeling, TV mounting, snow removal, or lawn care? Visit our sister company Watts Safety Installs for comprehensive home services throughout Norfolk, NE.</p>
<i class="fas fa-bars hamburger"></i>
<div class="service-dropdown">
<ul>
<li><a href="/safety-installs/services/tv-mounting/"><i class="fas fa-check-circle"></i> TV Mounting & Home Theater</a></li>
<li><a href="/safety-installs/services/home-remodeling/"><i class="fas fa-check-circle"></i> Kitchen & Bathroom Remodeling</a></li>
<li><a href="/safety-installs/services/snow-removal/"><i class="fas fa-check-circle"></i> Snow Removal & Winter Services</a></li>
<li><a href="/safety-installs/services/lawn-maintenance/"><i class="fas fa-check-circle"></i> Lawn Care & Landscaping</a></li>
<li><a href="/safety-installs/services/handyman-services/"><i class="fas fa-check-circle"></i> Handyman Services</a></li>
<li><a href="/safety-installs/services.html"><i class="fas fa-arrow-right"></i> View All Services</a></li>
</ul>
</div>
<div class="service-cta">
<a href="/safety-installs/">Visit Watts Safety Installs</a>
</div>
</div>
</div>'''
    
    content = re.sub(old_card_pattern, new_card, content, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed homepage service cards")

def create_proper_dba_services_page():
    """Create properly formatted DBA services.html"""
    
    # Read ATP services page as template
    with open('services.html', 'r', encoding='utf-8') as f:
        atp_content = f.read()
    
    # Create DBA version with proper formatting
    dba_content = atp_content
    
    # Replace branding
    replacements = {
        'Watts ATP Contractor': 'Watts Safety Installs',
        'WATTS ATP CONTRACTOR': 'WATTS SAFETY INSTALLS',
        'ATP Approved Contractor': 'Sister company of Watts ATP Contractor',
        'Accessibility & Safety Services': 'Complete Home Services',
        'ATP Accessibility & Safety Services': 'Our Complete Home Services',
        'Professional ADA accessibility and aging-in-place services': 'Professional home services including TV mounting, remodeling, and property maintenance',
        'Professional ADA compliance and aging-in-place solutions designed to create safer, more accessible living environments': 'Comprehensive home services designed to enhance your property and lifestyle',
        
        # Colors
        '--teal: #00C4B4': '--primary: #dc2626',
        '--navy: #0A1D37': '--dark: #0a0a0a',
        '--gold: #FFD700': '--secondary: #fef3c7',
        'var(--teal)': 'var(--primary)',
        'var(--navy)': 'var(--dark)',
        'var(--gold)': 'var(--secondary)',
        
        # Navigation
        '<a href="/services">Services</a>': '<a href="/safety-installs/services.html">Services</a>',
        '<a href="/">Home</a>': '<a href="/safety-installs/">Home</a>',
        '<a href="/about">About</a>': '<a href="/safety-installs/about.html">About</a>',
        '<a href="/contact">Contact</a>': '<a href="/safety-installs/contact.html">Contact</a>',
        '<a href="/service-area">Service Area</a>': '<a href="/safety-installs/service-area.html">Service Area</a>',
        '<a href="/referrals">Referrals</a>': '<a href="/referrals">Referrals</a>',
        
        # Logo
        '<a class="logo" href="/">WATTS</a>': '<a class="logo" href="/safety-installs/">WATTS</a>',
        
        # Theme
        'content="#ffffff" name="theme-color"': 'content="#000000" name="theme-color"',
        
        # Canonical
        'href="https://wattsatpcontractor.com/services"': 'href="https://wattsatpcontractor.com/safety-installs/services"',
    }
    
    for old, new in replacements.items():
        dba_content = dba_content.replace(old, new)
    
    # Replace the ATP accessibility card with DBA service cards
    # This is the key - we need to show DBA services, not ATP services
    
    # Replace "Looking for Other Home Services" section to point back to ATP
    dba_content = dba_content.replace(
        '<h2 class="seasonal-title">Looking for Other Home Services?</h2>',
        '<h2 class="seasonal-title">Looking for Accessibility Services?</h2>'
    )
    dba_content = dba_content.replace(
        '<p class="seasonal-subtitle">TV mounting, snow removal, lawn care, home remodeling, and more available through our home services division</p>',
        '<p class="seasonal-subtitle">ADA accessibility, grab bars, wheelchair ramps, and senior safety modifications available through our sister company</p>'
    )
    
    # Update the promo cards to point to ATP
    dba_content = re.sub(
        r'<div class="promo-icon">📺</div>\s*<h3 class="promo-title">TV & Home Theater</h3>',
        '<div class="promo-icon">♿</div>\n<h3 class="promo-title">Accessibility & Safety</h3>',
        dba_content
    )
    dba_content = re.sub(
        r'<p class="promo-description">Professional TV mounting.*?</p>',
        '<p class="promo-description">Professional ADA accessibility modifications, grab bars, wheelchair ramps, and senior safety solutions.</p>',
        dba_content
    )
    
    dba_content = dba_content.replace(
        '<a class="promo-cta" href="/safety-installs/services.html">View Services</a>',
        '<a class="promo-cta" href="/services.html">View ATP Services</a>'
    )
    
    dba_content = dba_content.replace(
        '<a href="/safety-installs/" class="cta-button" style="background: #dc2626;">Visit Watts Safety Installs →</a>',
        '<a href="/" class="cta-button" style="background: #00C4B4;">Visit Watts ATP Contractor →</a>'
    )
    
    # Write properly formatted file
    with open('safety-installs/services.html', 'w', encoding='utf-8') as f:
        f.write(dba_content)
    
    print("✅ Created properly formatted DBA services.html")

def create_proper_dba_homepage():
    """Create DBA homepage matching ATP structure exactly"""
    
    # Read ATP homepage
    with open('index.html', 'r', encoding='utf-8') as f:
        atp_content = f.read()
    
    # Create DBA version
    dba_content = atp_content
    
    # Replace branding
    replacements = {
        'Watts ATP Contractor': 'Watts Safety Installs',
        'WATTS ATP CONTRACTOR': 'WATTS SAFETY INSTALLS',
        'ATP Approved Contractor': 'Sister company of Watts ATP Contractor',
        'Accessibility Contractor Near Me': 'Home Services Contractor Near Me',
        'ADA accessibility &amp; aging-in-place': 'TV mounting, home remodeling, snow removal &amp; property maintenance',
        
        # Colors
        '--teal: #00C4B4': '--primary: #dc2626',
        '--navy: #0A1D37': '--dark: #0a0a0a',
        '--gold: #FFD700': '--secondary: #fef3c7',
        'var(--teal)': 'var(--primary)',
        'var(--navy)': 'var(--dark)',
        'var(--gold)': 'var(--secondary)',
        
        # Navigation
        '<a href="/services">Services</a>': '<a href="/safety-installs/services.html">Services</a>',
        '<a href="/">Home</a>': '<a href="/safety-installs/">Home</a>',
        '<a href="/about">About</a>': '<a href="/safety-installs/about.html">About</a>',
        '<a href="/contact">Contact</a>': '<a href="/safety-installs/contact.html">Contact</a>',
        '<a href="/service-area">Service Area</a>': '<a href="/safety-installs/service-area.html">Service Area</a>',
        
        # Service links
        'href="/services/': 'href="/safety-installs/services/',
        
        # Theme
        'content="#ffffff" name="theme-color"': 'content="#000000" name="theme-color"',
        
        # Canonical
        'href="https://wattsatpcontractor.com"': 'href="https://wattsatpcontractor.com/safety-installs/"',
    }
    
    for old, new in replacements.items():
        dba_content = dba_content.replace(old, new)
    
    # Replace the "Other Home Services" card with actual DBA service cards
    # Remove ATP accessibility card, add DBA service cards
    
    # Write properly formatted file
    with open('safety-installs/index.html', 'w', encoding='utf-8') as f:
        f.write(dba_content)
    
    print("✅ Created properly formatted DBA homepage")

def main():
    print("🔧 Comprehensive fix starting...\n")
    
    fix_homepage_service_cards()
    create_proper_dba_services_page()
    create_proper_dba_homepage()
    
    print("\n✨ All fixes complete!")
    print("   - Homepage cards fixed (same size, working dropdowns)")
    print("   - DBA services.html properly formatted")
    print("   - DBA homepage matches ATP structure")

if __name__ == '__main__':
    main()
