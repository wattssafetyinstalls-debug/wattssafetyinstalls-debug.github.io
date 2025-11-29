# create_favicons.py
import os

# Create minimal favicon files to prevent 404 errors
icon_files = [
    'favicon.ico',
    'favicon-16x16.png', 
    'favicon-32x32.png',
    'favicon-96x96.png',
    'android-chrome-192x192.png'
]

# Create minimal content for each file
for file in icon_files:
    with open(file, 'wb') as f:
        f.write(b'')  # Empty file but exists
    print(f"Created: {file}")

# Create a basic manifest.json
manifest_content = '''{
    "name": "My Website",
    "short_name": "Website",
    "start_url": ".",
    "display": "standalone"
}'''

with open('manifest.json', 'w') as f:
    f.write(manifest_content)
print("Created: manifest.json")

print("All favicon files created to prevent 404 errors")