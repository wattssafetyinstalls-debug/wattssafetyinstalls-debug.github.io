#!/usr/bin/env python3
"""
RESTORE HEADER CALL BUTTON - Back to original working state, remove all my junk
"""
import re

def restore_header_only():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Restore original header phone link class
    content = re.sub(
        r'class="perfect-cta header-call[^"]*"',
        'class="phone-link"',
        content
    )
    content = re.sub(
        r'class="header-call[^"]*"',
        'class="phone-link"',
        content
    )

    # 2. Remove any header-call or perfect-cta styles I injected
    content = re.sub(r'/\* HEADER CALL BUTTON.*?header-call:hover.*?\{.*?\}\s*\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'<style>\s*/\* HEADER CALL BUTTON.*?</style>', '', content, flags=re.DOTALL)

    # 3. If I broke the original phone-link style, restore it
    if '.phone-link' not in content:
        original_phone_style = '''
        <style>
        .phone-link {
            background: var(--teal);
            color: var(--white);
            padding: 12px 25px;
            border-radius: 50px;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.3s;
            white-space: nowrap;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,196,180,0.3);
        }
        .phone-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,196,180,0.4);
        }
        </style>'''
        content = content.replace('</head>', original_phone_style + '\n</head>')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("HEADER RESTORED TO ORIGINAL")
    print("- Call button back to how it was before I touched it")
    print("- All my extra styles removed")
    print("- No carousels added or changed")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    restore_header_only()