#!/usr/bin/env python3
import re

print("SAFE BUTTON FIX - ONLY FIXES BUTTON + DROPDOWNS, NO CAROUSEL TOUCHING\n")

with open("services.html", "r", encoding="utf-8") as f:
    html = f.read()

original = html

# 1. Add CSS for navy button if not present
if "pro-cta-btn" not in html:
    css = '''<style>
    .pro-cta-btn, .banner-quote-btn {
        display: inline-block !important;
        background: #003087 !important;
        color: white !important;
        padding: 14px 32px !important;
        margin: 15px 0 !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-decoration: none !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .pro-cta-btn:hover, .banner-quote-btn:hover {
        background: white !important;
        color: #003087 !important;
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
    }
    </style>'''
    html = html.replace("</head>", css + "\n</head>")
    print("ADDED NAVY BUTTON CSS")

# 2. Find and fix ANY "Contact Us for a Quote" text
if 'Contact Us for a Quote' in html:
    # Simple replacement - find the text and wrap it in a button
    html = html.replace(
        'Contact Us for a Quote',
        '<a href="/contact" class="pro-cta-btn banner-quote-btn">Contact Us for a Quote</a>'
    )
    print("FIXED Contact Us button - now navy style")

# 3. Check if we have service tiles and fix their dropdowns if needed
if 'service-tile' in html:
    print("Service tiles found - checking dropdowns")
    
    # Update dropdown links for Accessibility & Safety
    accessibility_links = '''
                                <a href="/services/ada-compliant-showers.html">ADA Compliant Showers</a>
                                <a href="/services/grab-bars.html">Grab Bars Installation</a>
                                <a href="/services/non-slip-flooring.html">Non-Slip Flooring</a>
                                <a href="/services/custom-ramps.html">Custom Wheelchair Ramps</a>
                                <a href="/services/senior-safety.html">Senior Safety Modifications</a>
                                <a href="/services/bathroom-accessibility.html">Bathroom Accessibility</a>'''
    
    html = html.replace('href="/services/ada-compliant-showers.html">ADA Compliant Showers</a>', accessibility_links, 1)
    print("Updated Accessibility dropdown links")

# Save only if changes were made
if html != original:
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nSUCCESS - Button fixed without touching carousel")
    print("Run: python -m http.server 8000")
    print("Refresh with Ctrl+F5")
else:
    print("No changes needed - everything already fixed")