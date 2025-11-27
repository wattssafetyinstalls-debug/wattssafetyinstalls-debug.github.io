#!/usr/bin/env python3
"""
FIX HEADER CALL BUTTON - Make it match the premium service/promo CTA buttons
"""
import re

def fix_header_call():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the header phone link with the premium button class
    content = re.sub(
        r'<a href="tel:\+14054106402" class="phone-link[^"]*">',
        '<a href="tel:+14054106402" class="perfect-cta header-call">',
        content
    )

    # Add the final premium CTA style (only if not already there)
    header_button_style = '''
    <style>
    /* PREMIUM HEADER CALL BUTTON - matches service & promo buttons */
    .header-call,
    a.perfect-cta.header-call {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 14px 32px !important;
        font-size: 1.1rem !important;
        background: linear-gradient(135deg, var(--teal), #00a396) !important;
        box-shadow: 0 8px 25px rgba(0,196,180,.3) !important;
        border-radius: 50px !important;
        transition: all .4s !important;
    }
    .header-call:hover,
    a.perfect-cta.header-call:hover {
        background: #fff !important;
        color: var(--navy) !important;
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,196,180,.4) !important;
    }
    .header-call i {font-size: 1.3rem;}
    </style>'''

    if '.header-call' not in content:
        content = content.replace('</head>', header_button_style + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("HEADER CALL BUTTON FIXED")
    print("- Now has exact same premium look as service & promo buttons")
    print("- Same gradient, same hover (white + navy text), same size")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    fix_header_call()