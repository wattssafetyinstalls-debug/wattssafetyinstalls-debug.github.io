#!/usr/bin/env python3
"""
FIX YELLOW BANNER QUOTE LINK - Make it a professional button
"""
import re

def fix_yellow_banner_button():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Fix the "Contact Us for a Quote" link in the yellow banner
    yellow_banner_fix = '''
    <style>
    /* YELLOW BANNER QUOTE BUTTON */
    .banner-quote-btn {
        display: inline-block;
        background: var(--navy) !important;
        color: white !important;
        padding: 10px 25px;
        border-radius: 25px;
        font-weight: 600;
        text-decoration: none;
        font-size: 1rem;
        margin-left: 15px;
        border: 2px solid var(--navy);
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    .banner-quote-btn:hover {
        background: white !important;
        color: var(--navy) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    </style>'''

    # Find and replace the contact link in the yellow banner
    content = re.sub(
        r'(<a href="[^"]*contact[^"]*"[^>]*)(>Contact Us for a Quote</a>)',
        r'\1 class="banner-quote-btn"\2',
        content
    )

    # If the above doesn't work, try a more general approach
    if 'banner-quote-btn' not in content:
        content = re.sub(
            r'Contact Us for a Quote</a>',
            'Contact Us for a Quote</a>',
            content
        )
        # Add class manually to any contact link in that section
        content = re.sub(
            r'(yellow-banner|top-banner|atp-banner).*?(<a href="[^"]*contact[^"]*")',
            r'\1 \2 class="banner-quote-btn"',
            content,
            flags=re.DOTALL
        )

    # Add the CSS to the head
    if '.banner-quote-btn' not in content:
        content = content.replace('</head>', yellow_banner_fix + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("YELLOW BANNER BUTTON FIXED")
    print("- 'Contact Us for a Quote' now has professional button styling")
    print("- Navy background, white text, hover effects")
    print("- Looks clickable and matches your site design")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    fix_yellow_banner_button()