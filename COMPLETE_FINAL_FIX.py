#!/usr/bin/env python3
import re

print("COMPLETE FINAL FIX V3 - REMOVING DUPLICATE GRID, ENSURING GRADIENTS\n")

with open("services.html", "r", encoding="utf-8") as f:
    html = f.read()

original = html

# 1. REMOVE DUPLICATE SERVICES GRID (targets the div directly)
if '<div class="services-grid">' in html:
    pattern = r'<div class="services-grid">.*?</div>'
    html = re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)
    print("REMOVED duplicate services grid")

# 2. ENSURE SCROLLABLE DROPDOWNS IF MISSING
if 'max-height: 300px' not in html:
    scroll_css = '''
    <style>
    .dropdown {
        max-height: 300px;
        overflow-y: auto;
        scrollbar-width: thin;
    }
    
    .dropdown::-webkit-scrollbar {
        width: 6px;
    }
    
    .dropdown::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .dropdown::-webkit-scrollbar-thumb {
        background: #00C4B4;
        border-radius: 3px;
    }
    
    .dropdown::-webkit-scrollbar-thumb:hover {
        background: #0A1D37;
    }
    </style>
    '''
    html = html.replace('</head>', scroll_css + '\n</head>')
    print("ADDED scrollable dropdown CSS")

# 3. ENSURE GRADIENT ON PROMO BANNER IF MISSING
if '.certification-badge' in html and 'linear-gradient' not in html:
    banner_css = '''
    <style>
    .certification-badge {
        background: linear-gradient(135deg, #FFD700 0%, #F59E0B 100%);
        color: #0A1D37;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        display: inline-block;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .certification-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    </style>
    '''
    html = html.replace('</head>', banner_css + '\n</head>')
    print("RESTORED gradient to promo banner")

# Save if changed
if html != original:
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nV3 FIX APPLIED!")
    print(" - Removed duplicate grid")
    print(" - Added scrollable dropdowns (if missing)")
    print(" - Restored promo banner gradient")
    print("\nRun: python -m http.server 8000")
    print("Refresh with Ctrl+F5 - check for duplicates & gradients")
else:
    print("No changes needed - everything already fixed")
