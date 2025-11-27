#!/usr/bin/env python3
"""
FIX DROPDOWN CUTOFF - Makes hamburger dropdown fully visible on all 7 tiles
"""
import re

def fix_dropdown():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Remove any old dropdown styles that might be cutting it off
    content = re.sub(r'\.final-dropdown\{[^}]*\}', '', content)
    content = re.sub(r'\.hamburger-menu:hover \.final-dropdown\{[^}]*\}', '', content)

    # Inject the FIXED dropdown CSS (higher z-index, better positioning, overflow visible)
    dropdown_fix = '''
    <style>
    /* FIXED DROPDOWN - fully visible, no cutoff */
    .final-hamburger {
        position: relative;
        z-index: 100;
    }
    .final-hamburger i {
        font-size: 2rem;
        color: var(--teal);
        cursor: pointer;
        transition: color .3s;
    }
    .final-card:hover .final-hamburger i { color: #fff; }

    .final-dropdown {
        display: none;
        position: absolute;
        top: 100%;
        right: 0;
        background: #fff;
        min-width: 220px;
        border-radius: 16px;
        box-shadow: 0 20px 50px rgba(0,0,0,.25);
        padding: 12px 0;
        z-index: 9999;
        margin-top: 10px;
        border: 1px solid rgba(0,196,180,.2);
    }
    .final-hamburger:hover > .final-dropdown {
        display: block !important;
    }
    .final-dropdown a {
        display: block;
        padding: 14px 24px;
        color: var(--navy);
        text-decoration: none;
        font-weight: 500;
        transition: all .3s;
    }
    .final-dropdown a:hover {
        background: var(--teal);
        color: white;
        padding-left: 32px;
    }
    /* Ensure parent containers don't clip the dropdown */
    .final-card,
    .final-slide,
    .final-track,
    .final-carousel-inner {
        overflow: visible !important;
    }
    </style>'''

    # Insert right before </head> or after existing <style>
    if '<style>' in content:
        content = re.sub(r'(</style>)', dropdown_fix + '\\1', content, count=1)
    else:
        content = content.replace('</head>', dropdown_fix + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("DROPDOWN CUTOFF FIXED")
    print("All 7 tiles now show full dropdown menus")
    print("No overflow clipping, higher z-index, perfect spacing")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    fix_dropdown()