# Script to update all service pages to ATP branding
import os
import re

# List of service pages to update
service_pages = [
    'bathroom-accessibility.html',
    'grab-bar-installation.html', 
    'wheelchair-ramp-installation.html',
    'non-slip-flooring-solutions.html',
    'accessibility-safety-solutions.html'
]

# Updates to apply
updates = [
    (r'--red: #dc2626', '--navy: #0A1D37'),
    (r'--black: #1a1a1a', '--teal: #00C4B4'),
    (r'--cream: #f5f5dc', '--gold: #FFD700'),
    (r'Watts Safety Installs', 'Watts ATP Contractor'),
    (r'color: var\(--red\)', 'color: var(--navy)'),
    (r'Safety Installs', 'ATP Contractor')
]

for page in service_pages:
    if os.path.exists(page):
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply all updates
        for pattern, replacement in updates:
            content = re.sub(pattern, replacement, content)
        
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {page}")
    else:
        print(f"File not found: {page}")

print("All service pages updated to ATP branding!")
