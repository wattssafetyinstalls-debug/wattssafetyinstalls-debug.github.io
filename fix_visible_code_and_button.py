#!/usr/bin/env python3
"""
REMOVE VISIBLE CODE + FIX HEADER CALL BUTTON
"""
import re

def fix_visible_code_and_button():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove the visible JavaScript code at the bottom
    content = re.sub(
        r"document\.addEventListener\('DOMContentLoaded',.*?setInterval\(c,5000\)\)\}\);",
        "",
        content,
        flags=re.DOTALL
    )

    # 2. Fix the header call button under the yellow ATP banner
    # Look for the phone link in the header and add proper button styling
    header_button_fix = '''
    <style>
    /* HEADER CALL BUTTON STYLING */
    .header-phone-btn {
        display: inline-block;
        background: linear-gradient(135deg, var(--teal), #00a396);
        color: white !important;
        padding: 12px 30px;
        border-radius: 50px;
        font-weight: 700;
        text-decoration: none;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0,196,180,0.3);
        transition: all 0.3s ease;
        margin-left: 20px;
    }
    .header-phone-btn:hover {
        background: white !important;
        color: var(--navy) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,196,180,0.4);
    }
    </style>'''

    # Add the phone button class to the header call link
    content = re.sub(
        r'(<a href="tel:\+14054106402"[^>]*)(>Call Now for Quote</a>)',
        r'\1 class="header-phone-btn"\2',
        content
    )

    # Add the CSS to the head
    if '.header-phone-btn' not in content:
        content = content.replace('</head>', header_button_fix + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("FIXED BOTH ISSUES:")
    print("- Removed visible JavaScript code from bottom of page")
    print("- Added beautiful button styling to 'Call Now for Quote' in header")
    print("- Button now has gradient, hover effects, and proper spacing")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    fix_visible_code_and_button()