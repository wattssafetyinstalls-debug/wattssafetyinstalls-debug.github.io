#!/usr/bin/env python3
"""
Fix homepage structure:
1. Update service dropdown redirects to match new ATP/DBA split
2. Remove stairlift-elevator references
3. Update service cards to ATP-only with DBA redirect
"""

import re

def fix_homepage():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove stairlift-elevator references
    content = re.sub(
        r'<li><a href="/stairlift-installation">.*?</a></li>\n?',
        '',
        content
    )
    content = re.sub(
        r'<li><a href="/services/stairlift-elevator-installation">.*?</a></li>\n?',
        '',
        content
    )
    
    # Update service dropdown links - DBA services should go to /safety-installs/services/
    dba_services = [
        'kitchen-renovations', 'deck-construction', 'siding-replacement', 
        'home-remodeling', 'basement-finishing', 'room-additions',
        'fence-installation', 'window-doors', 'painting-services',
        'tv-mounting', 'home-theater-installation', 'soundbar-setup',
        'cable-management', 'smart-audio', 'projector-install',
        'snow-removal', 'lawn-maintenance', 'landscape-design',
        'garden-maintenance', 'tree-trimming', 'emergency-repairs',
        'seasonal-cleanup', 'gutter-cleaning', 'pressure-washing'
    ]
    
    for service in dba_services:
        # Update links to point to DBA
        content = re.sub(
            f'href="/services/{service}"',
            f'href="/safety-installs/services/{service}/"',
            content
        )
    
    # Update the "Home Remodeling" service card to redirect to DBA
    old_remodeling_card = re.search(
        r'<div class="service-card" id="home-remodeling">.*?</div>\s*</div>\s*</div>',
        content,
        re.DOTALL
    )
    
    if old_remodeling_card:
        new_remodeling_card = '''<div class="service-card" id="home-remodeling" style="background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); border: 3px solid #fef3c7;">
<img alt="Watts Safety Installs - Home Services" class="service-image" loading="lazy" src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80"/>
<div class="service-content">
<h3 class="service-title" style="color: #fef3c7;">Other Home Services</h3>
<p class="service-description" style="color: #fff;">Looking for home remodeling, TV mounting, snow removal, or lawn care? Visit our sister company: <strong>Watts Safety Installs</strong></p>
<i class="fas fa-bars hamburger"></i>
<div class="service-dropdown" style="background: linear-gradient(135deg, #0a0a0a, #1a1a1a) !important;">
<ul>
<li><a href="/safety-installs/services/tv-mounting/" style="color: #fef3c7 !important;"><i class="fas fa-check-circle"></i> TV Mounting & Home Theater</a></li>
<li><a href="/safety-installs/services/home-remodeling/" style="color: #fef3c7 !important;"><i class="fas fa-check-circle"></i> Kitchen & Bathroom Remodeling</a></li>
<li><a href="/safety-installs/services/snow-removal/" style="color: #fef3c7 !important;"><i class="fas fa-check-circle"></i> Snow Removal & Winter Services</a></li>
<li><a href="/safety-installs/services/lawn-maintenance/" style="color: #fef3c7 !important;"><i class="fas fa-check-circle"></i> Lawn Care & Landscaping</a></li>
<li><a href="/safety-installs/services/handyman-services/" style="color: #fef3c7 !important;"><i class="fas fa-check-circle"></i> Handyman Services</a></li>
<li><a href="/safety-installs/services.html" style="color: #dc2626 !important; font-weight: 700;"><i class="fas fa-arrow-right"></i> View All Services</a></li>
</ul>
</div>
<div class="service-cta">
<a href="/safety-installs/" style="background: #fef3c7; color: #dc2626;">Visit Watts Safety Installs →</a>
</div>
</div>
</div>'''
        content = content.replace(old_remodeling_card.group(0), new_remodeling_card)
    
    # Update TV mounting card to redirect to DBA
    old_tv_card = re.search(
        r'<div class="service-card" id="tv-mounting">.*?</div>\s*</div>\s*</div>',
        content,
        re.DOTALL
    )
    
    if old_tv_card:
        # Remove this card since it's now in the "Other Home Services" card
        content = content.replace(old_tv_card.group(0), '')
    
    # Update property maintenance card to redirect to DBA
    old_property_card = re.search(
        r'<div class="service-card" id="property-maintenance">.*?</div>\s*</div>\s*</div>',
        content,
        re.DOTALL
    )
    
    if old_property_card:
        # Remove this card since it's now in the "Other Home Services" card
        content = content.replace(old_property_card.group(0), '')
    
    # Update footer service links
    content = re.sub(
        r'<li><a href="/services/home-remodeling">Complete Home Remodeling</a></li>',
        '',
        content
    )
    content = re.sub(
        r'<li><a href="/services/tv-mounting">TV Mounting &amp; AV</a></li>',
        '',
        content
    )
    content = re.sub(
        r'<li><a href="/services/snow-removal">Property Maintenance</a></li>',
        '',
        content
    )
    
    # Write updated content
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Homepage updated successfully!")
    print("   - Removed stairlift-elevator references")
    print("   - Updated service dropdowns for ATP/DBA split")
    print("   - Updated service cards to ATP-only + DBA redirect")

if __name__ == '__main__':
    fix_homepage()
