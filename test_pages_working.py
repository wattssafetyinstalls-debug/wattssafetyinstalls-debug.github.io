# test_pages_working.py
import webbrowser
import os
import time

print("Testing professional service pages...")

pages_to_test = [
    'services/accessibility-safety-solutions.html',
    'services/home-remodeling-renovation.html',
    'services/tv-home-theater-installation.html'
]

print("Checking pages:")
for page in pages_to_test:
    if os.path.exists(page):
        print("FOUND: " + page)
    else:
        print("MISSING: " + page)

print("Opening pages in browser...")
for page in pages_to_test:
    if os.path.exists(page):
        full_path = os.path.abspath(page)
        print("OPENING: " + page)
        webbrowser.open('file:///' + full_path)
        time.sleep(2)

print("Please check your browser - pages should have:")
print("- Header images")
print("- Trust banners")
print("- Gradient cards")
print("- Professional design")