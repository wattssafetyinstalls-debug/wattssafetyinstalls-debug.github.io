#!/usr/bin/env python3
"""
FIX PROMO CARDS - Give them the same premium CTA button as service tiles
"""
import re

def fix_promo_buttons():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace all promo CTA links with the premium button style
    content = re.sub(
        r'<a href="contact" class="cta-button">[^<]*</a>',
        '<a href="contact" class="perfect-cta">Claim Offer</a>',
        content
    )

    # Make sure the perfect-cta style exists (same as service tiles)
    promo_button_style = '''
    <style>
    /* PREMIUM CTA BUTTON FOR PROMO CARDS */
    .perfect-cta,
    .promo-card a.perfect-cta {
        display: inline-block;
        margin-top: 20px;
        padding: 14px 32px;
        background: linear-gradient(135deg, var(--teal), #00a396);
        color: white;
        border-radius: 50px;
        font-weight: 700;
        text-decoration: none;
        transition: all .4s;
        box-shadow: 0 8px 25px rgba(0,196,180,.3);
    }
    .perfect-cta:hover,
    .promo-card:hover .perfect-cta {
        background: #fff !important;
        color: var(--navy) !important;
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,196,180,.4);
    }
    </style>'''

    # Insert style if not already there
    if '.perfect-cta' not in content:
        content = content.replace('</head>', promo_button_style + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("PROMO BUTTONS FIXED")
    print("- All 3 seasonal cards now have premium 'Claim Offer' button")
    print("- Same style/hover as service tiles")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    fix_promo_buttons()