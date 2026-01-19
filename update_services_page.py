#!/usr/bin/env python3
"""
Script to update services.html to show only ATP services and redirect to DBA
"""

import re

# Read the original file
with open('services.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update title and meta description
content = re.sub(
    r'<title>All Services \| Watts ATP Contractor \| Norfolk, NE</title>',
    '<title>Accessibility & Safety Services | Watts ATP Contractor | Norfolk, NE</title>',
    content
)

content = re.sub(
    r'<meta content="Complete list of professional services: ADA ramps, grab bars, TV mounting, snow removal, lawn care, remodeling in Norfolk, NE\. ATP Approved Contractor\." name="description"/>',
    '<meta content="Professional ADA accessibility and aging-in-place services: ramps, grab bars, accessible showers, senior safety modifications in Norfolk, NE. ATP Approved Contractor." name="description"/>',
    content
)

# Update hero section
old_hero = '''<!-- Hero -->
<section class="hero">
<h1>All Professional Services</h1>
<p class="certification-badge">ATP Approved Contractor • Nebraska Regd #54690-25 • Serving All Nebraska</p>
<p>From ADA ramps to TV mounting, snow removal to full remodels — we do it all.</p>
<div class="promo-banner">
<p style="font-size:1.6rem; margin:0"><strong>15% OFF First 3 Snow Visits 2025</strong> • <strong>LAWN2026 – 20% OFF Season</strong></p>
</div>
<a class="cta-button" href="tel:+14054106402">Call (405) 410-6402 – Free Quote</a>
</section>'''

new_hero = '''<!-- Hero -->
<section class="hero">
<h1>Accessibility & Safety Services</h1>
<p class="certification-badge">ATP Approved Contractor • Nebraska Regd #54690-25 • Serving All Nebraska</p>
<p>Professional ADA accessibility and aging-in-place modifications for safer, more accessible living.</p>
<div class="promo-banner" style="background: rgba(220, 38, 38, 0.2); border: 2px solid #dc2626;">
<p style="font-size:1.4rem; margin:0"><strong>Looking for TV mounting, snow removal, lawn care, or home remodeling?</strong><br><a href="/safety-installs/" style="color: #FFD700; text-decoration: underline;">Visit Watts Safety Installs →</a></p>
</div>
<a class="cta-button" href="tel:+14054106402">Call (405) 410-6402 – Free Assessment</a>
</section>'''

content = content.replace(old_hero, new_hero)

# Update services header
content = re.sub(
    r'<h2 class="section-title">Our Comprehensive Services</h2>\s*<p class="section-subtitle">Professional contractor services designed to meet all your home improvement and maintenance needs with precision and care</p>',
    '<h2 class="section-title">ATP Accessibility & Safety Services</h2>\n<p class="section-subtitle">Professional ADA compliance and aging-in-place solutions designed to create safer, more accessible living environments</p>',
    content
)

# Remove all service cards except the first one (Accessibility)
# Find the carousel container section
carousel_start = content.find('<div class="carousel-container" id="carouselContainer">')
carousel_end = content.find('</div>\n<!-- REMOVED ARROW BUTTONS -->')

if carousel_start != -1 and carousel_end != -1:
    # Extract just the first service card
    first_card_start = content.find('<!-- Service Card 1 - Accessibility & Safety -->', carousel_start)
    first_card_end = content.find('</div>\n</div>\n<!-- Service Card 2', first_card_start)
    
    if first_card_start != -1 and first_card_end != -1:
        first_card = content[first_card_start:first_card_end + 12]  # +12 for </div></div>
        
        # Replace the entire carousel content with just the first card
        new_carousel = f'<div class="carousel-container" id="carouselContainer">\n{first_card}\n</div>'
        old_carousel = content[carousel_start:carousel_end]
        content = content.replace(old_carousel, new_carousel)

# Replace seasonal services section with DBA redirect
old_seasonal = '''<!-- Seasonal Services Section - 3 Column Grid -->
<section class="seasonal-services">
<h2 class="seasonal-title">Seasonal Services &amp; Contracts</h2>
<p class="seasonal-subtitle">Special offers and seasonal maintenance packages to keep your property looking great year-round</p>
<div class="promo-grid">
<!-- Snow Removal Promo -->
<div class="promo-card">
<div class="promo-icon">❄️</div>
<h3 class="promo-title">Winter Snow Removal</h3>
<p class="promo-description">Keep your property safe and accessible all winter long with our reliable snow removal services. Contracts available for residential and commercial properties.</p>
<div class="promo-code">SNOW2025</div>
<p class="promo-description"><strong>15% OFF</strong> First 3 Snow Visits</p>
<a class="promo-cta" href="/contact">Book Now</a>
</div>
<!-- Lawn Care Promo -->
<div class="promo-card">
<div class="promo-icon">🌿</div>
<h3 class="promo-title">Spring/Summer Lawn Care</h3>
<p class="promo-description">Professional lawn maintenance including mowing, trimming, edging, and fertilization. Keep your lawn lush and healthy all season long.</p>
<div class="promo-code">LAWN2026</div>
<p class="promo-description"><strong>20% OFF</strong> Seasonal Contracts</p>
<a class="promo-cta" href="/contact">Get Quote</a>
</div>
<!-- Fall Cleanup Promo -->
<div class="promo-card">
<div class="promo-icon">🍂</div>
<h3 class="promo-title">Fall Cleanup Services</h3>
<p class="promo-description">Prepare your property for winter with our comprehensive fall cleanup services. Leaf removal, gutter cleaning, and winter preparation.</p>
<div class="promo-code">FALL2025</div>
<p class="promo-description"><strong>10% OFF</strong> Full Property Cleanup</p>
<a class="promo-cta" href="/contact">Schedule Service</a>
</div>
</div>
</section>'''

new_seasonal = '''<!-- DBA Services Redirect Section -->
<section class="seasonal-services">
<h2 class="seasonal-title">Looking for Other Home Services?</h2>
<p class="seasonal-subtitle">TV mounting, snow removal, lawn care, home remodeling, and more available through our home services division</p>
<div class="promo-grid">
<div class="promo-card">
<div class="promo-icon">📺</div>
<h3 class="promo-title">TV & Home Theater</h3>
<p class="promo-description">Professional TV mounting, home theater installation, soundbar setup, and complete audio/visual solutions.</p>
<a class="promo-cta" href="/safety-installs/services.html">View Services</a>
</div>
<div class="promo-card">
<div class="promo-icon">🏠</div>
<h3 class="promo-title">Home Remodeling</h3>
<p class="promo-description">Kitchen renovations, bathroom remodels, basement finishing, deck construction, and complete home improvements.</p>
<a class="promo-cta" href="/safety-installs/services.html">View Services</a>
</div>
<div class="promo-card">
<div class="promo-icon">🌿</div>
<h3 class="promo-title">Property Maintenance</h3>
<p class="promo-description">Snow removal, lawn care, landscaping, gutter cleaning, pressure washing, and seasonal maintenance.</p>
<div class="promo-code">SNOW2025 • LAWN2026</div>
<a class="promo-cta" href="/safety-installs/services.html">View Services</a>
</div>
</div>
<div style="text-align: center; margin-top: 40px;">
<a href="/safety-installs/" class="cta-button" style="background: #dc2626;">Visit Watts Safety Installs →</a>
</div>
</section>'''

content = content.replace(old_seasonal, new_seasonal)

# Update footer
old_footer_desc = '<p>Nebraska\'s premier ATP Approved Contractor specializing in accessibility modifications, safety installations, TV mounting, and comprehensive home services near you.</p>'
new_footer_desc = '<p>Nebraska\'s premier ATP Approved Contractor specializing in ADA accessibility modifications, aging-in-place solutions, and senior safety installations.</p>'
content = content.replace(old_footer_desc, new_footer_desc)

# Write the updated file
with open('services.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ services.html updated successfully!")
print("   - Updated to ATP services only")
print("   - Added DBA redirect banner")
print("   - Updated footer")
