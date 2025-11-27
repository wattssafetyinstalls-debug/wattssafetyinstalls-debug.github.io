#!/usr/bin/env python3
"""
HEADER CALL BUTTON ONLY - Make it match your premium CTA buttons
"""
import re

def fix_header_button_only():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Change the header phone link to use the premium button class
    content = re.sub(
        r'class="phone-link[^"]*"',
        'class="perfect-cta header-call"',
        content
    )

    # Add the style only if not already there
    header_style = '''
    <style>
    /* HEADER CALL BUTTON - EXACTLY LIKE SERVICE & PROMO BUTTONS */
    .header-call, a.perfect-cta.header-call {
        display: inline-flex !important;
        align-items: center !important;
        gap: 10px !important;
        padding: 14px 32px !important;
        background: linear-gradient(135deg, var(--teal), #00a396) !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        box-shadow: 0 8px 25px rgba(0,196,180,.3) !important;
        transition: all .4s !important;
        font-size: 1.1rem !important;
    }
    .header-call:hover, a.perfect-cta.header-call:hover {
        background: white !important;
        color: var(--navy) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(0,196,180,.4) !important;
    }
    </style>'''

    if '.header-call' not in content:
        content = content.replace('</head>', header_style + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("HEADER CALL BUTTON FIXED ONLY")
    print("- Now has exact same premium button as service tiles & promo cards")
    print("- Nothing else changed")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    fix_header_button_only()