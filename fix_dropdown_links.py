#!/usr/bin/env python3
"""
Update dropdown links to use direct file paths instead of pretty URLs
"""

import os

# Read the current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace pretty URLs with direct file paths
replacements = [
    ('href="/ada-compliant-showers"', 'href="/services/ada-compliant-showers.html"'),
    ('href="/grab-bars"', 'href="/services/grab-bars.html"'),
    ('href="/non-slip-flooring"', 'href="/services/non-slip-flooring.html"'),
    ('href="/custom-ramps"', 'href="/services/custom-ramps.html"'),
    ('href="/senior-safety"', 'href="/services/senior-safety.html"'),
    ('href="/kitchen-renovations"', 'href="/services/kitchen-renovations.html"'),
    ('href="/bathroom-remodels"', 'href="/services/bathroom-remodels.html"'),
    ('href="/deck-construction"', 'href="/services/deck-construction.html"'),
    ('href="/siding-replacement"', 'href="/services/siding-replacement.html"'),
    ('href="/home-remodeling"', 'href="/services/home-remodeling.html"'),
    ('href="/tv-mounting"', 'href="/services/tv-mounting.html"'),
    ('href="/home-theater"', 'href="/services/home-theater-installation.html"'),
    ('href="/snow-removal"', 'href="/services/snow-removal.html"'),
    ('href="/lawn-maintenance"', 'href="/services/lawn-maintenance.html"'),
    # Add more as needed
]

for old, new in replacements:
    content = content.replace(old, new)

# Write the updated content back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated dropdown links to use direct file paths")