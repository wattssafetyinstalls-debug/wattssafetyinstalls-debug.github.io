#!/usr/bin/env python3
import re

print("NUKE THE OLD GRID - KEEP ONLY THE PREMIUM CAROUSEL\n")

with open("services.html", "r", encoding="utf-8") as f:
    html = f.read()

original = html

# 1. COMPLETELY REMOVE THE OLD STATIC GRID (everything from the CSS rule to the closing div)
# This pattern matches from the .services-grid CSS rule all the way to the actual <div class="services-grid"> closing tag
pattern = r'\.services-grid\s*\{.*?<div class="services-grid">.*?</div>'
html = re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)
print("REMOVED old static services-grid (CSS + HTML)")

# 2. Remove any leftover empty sections or wrappers that might remain
html = re.sub(r'<section\s*>\s*</section>', '', html)                    # empty sections
html = re.sub(r'<div\s*class="services-container">\s*</div>', '', html) # empty containers
print("Cleaned up any empty wrappers")

# 3. Make sure scrollable dropdowns exist (just in case)
if 'max-height' not in html:
    scroll_css = '''
    <style>
    .dropdown { max-height: 320px; overflow-y: auto; scrollbar-width: thin; }
    .dropdown::-webkit-scrollbar { width: 6px; }
    .dropdown::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 3px; }
    .dropdown::-webkit-scrollbar-thumb { background: #00C4B4; border-radius: 3px; }
    .dropdown::-webkit-scrollbar-thumb:hover { background: #0A1D37; }
    </style>
    '''
    html = html.replace('</head>', scroll_css + '\n</head>')
    print("Added scrollable dropdowns")

# Save
if html != original:
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nOLD GRID NUKED - ONLY PREMIUM CAROUSEL REMAINS")
    print("Run: python -m http.server 8000")
    print("Refresh with Ctrl+F5 - you should now see ONLY the beautiful carousel")
else:
    print("No old grid found - you're already clean!")
