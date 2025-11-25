# fix_hover_effects.py
import os

# Service pages to fix
service_pages = [
    "ada-compliant-showers-bathrooms",
    "grab-bar-installation", 
    "wheelchair-ramp-installation",
    "stairlift-elevator-installation",
    "non-slip-flooring-solutions",
    "kitchen-renovations",
    "bathroom-remodels",
    "room-additions",
    "flooring-installation",
    "painting-drywall",
    "tv-mounting",
    "home-theater-installation",
    "sound-system-setup",
    "cable-management",
    "lawn-maintenance",
    "pressure-washing",
    "gutter-cleaning",
    "fence-repair",
    "handyman-services"
]

# Add the exact hover effect CSS
hover_css = '''
    <style>
        .service-card-main {{
            background: var(--white);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--teal-glow);
            transition: all 0.4s ease;
            border: 1px solid rgba(255, 255, 255, 0.8);
        }}
        
        .service-card-main:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--teal-glow), var(--navy-glow);
            background: linear-gradient(135deg, var(--teal) 0%, var(--navy) 100%);
            color: var(--white);
        }}
        
        .service-card-main:hover .service-title,
        .service-card-main:hover .service-description,
        .service-card-main:hover h3,
        .service-card-main:hover h4,
        .service-card-main:hover p,
        .service-card-main:hover li {{
            color: var(--white) !important;
        }}
        
        .service-card-main:hover .service-features ul li i {{
            color: var(--gold) !important;
        }}
        
        .service-card-main:hover .service-cta a {{
            background: var(--gold) !important;
            color: var(--navy) !important;
        }}
    </style>
'''

for slug in service_pages:
    page_path = f'services/{slug}.html'
    
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Add the hover CSS to the page
        if '<style>' in content and '.service-card-main' not in content:
            # Insert the hover CSS right after the existing styles
            style_end = content.find('</style>') + 8
            content = content[:style_end] + hover_css + content[style_end:]
        
        # 2. Update the main service card to use the hover class
        if 'style="max-width: 100%; margin: 0;' in content:
            content = content.replace(
                'style="max-width: 100%; margin: 0;',
                'class="service-card-main" style="max-width: 100%; margin: 0;'
            )
        
        # 3. Ensure all text elements have the right classes for hover effects
        content = content.replace('<h3 class="service-title">', '<h3 class="service-title" style="color: var(--navy);">')
        content = content.replace('<p class="service-description"', '<p class="service-description" style="color: var(--gray);"')
        
        # 4. Fix the service features section
        if 'class="service-features"' in content:
            # Update service features to work with hover
            content = content.replace(
                'class="service-features"',
                'class="service-features" style="color: var(--gray);"'
            )
        
        # 5. Fix CTA buttons to work with hover
        content = content.replace(
            'style="display: inline-block; margin: 0 10px; padding: 12px 25px; font-size: 1.1rem;"',
            'style="display: inline-block; margin: 0 10px; padding: 12px 25px; font-size: 1.1rem; transition: all 0.3s ease;"'
        )
        
        # Write the fixed content back
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed hover effects: {page_path}")

print("All service pages now have the proper gradient hover effect!")