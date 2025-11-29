# test_pages.py
import os
import webbrowser
import time

pages_to_test = [
    'index.html',
    'about.html', 
    'contact.html',
    'referrals.html',
    'service-area.html'
]

print("Testing all pages exist...")
for page in pages_to_test:
    if os.path.exists(page):
        print(f"OK - {page} - EXISTS")
    else:
        print(f"MISSING - {page} - NOT FOUND")

print("\nAll pages checked!")