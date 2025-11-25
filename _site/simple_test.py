# simple_test.py
import webbrowser
import os
import time

print("TESTING SERVICE PAGES")

# Test pages
test_pages = [
    'services/ada-compliant-showers.html',
    'services/kitchen-renovations.html', 
    'services/tv-mounting.html'
]

print("Checking pages:")
for page in test_pages:
    if os.path.exists(page):
        print("FOUND: " + page)
    else:
        print("MISSING: " + page)

print("Opening pages in browser...")
for page in test_pages:
    if os.path.exists(page):
        full_path = os.path.abspath(page)
        print("OPENING: " + page)
        webbrowser.open('file:///' + full_path)
        time.sleep(1)

print("Please check your browser windows and tell me what you see!")