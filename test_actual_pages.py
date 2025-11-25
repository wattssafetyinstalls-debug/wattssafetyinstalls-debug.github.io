# test_actual_pages.py
import webbrowser
import os
import time

print("=== TESTING SERVICE PAGES ===")

# Test the pages that should exist
test_pages = [
    'services/ada-compliant-showers.html',
    'services/kitchen-renovations.html', 
    'services/tv-mounting.html',
    'services/lawn-maintenance.html'
]

print("Checking if service pages exist:")
for page in test_pages:
    if os.path.exists(page):
        file_size = os.path.getsize(page)
        print(f"✓ {page} - EXISTS ({file_size} bytes)")
    else:
        print(f"✗ {page} - MISSING")

print("\nOpening pages in your browser...")
for i, page in enumerate(test_pages):
    if os.path.exists(page):
        full_path = os.path.abspath(page)
        print(f"Opening {i+1}. {page}")
        webbrowser.open('file:///' + full_path)
        time.sleep(2)  # Wait 2 seconds between opens

print("\n" + "="*50)
print("Please check your browser and answer:")
print("1. Do the pages open?")
print("2. Is the text readable (black on white)?") 
print("3. Any error messages?")
print("4. Can you see the service content?")