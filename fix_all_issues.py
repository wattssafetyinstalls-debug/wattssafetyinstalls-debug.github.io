# fix_all_issues.py
import os

# First, let's check what pages actually exist and fix the structure
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

# Fix each service page
for slug in service_pages:
    page_path = f'services/{slug}.html'
    
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix 1: Add hover effects to the main service card
        if 'style="max-width: 100%; margin: 0;"' in content:
            # Add hover effect to the main service card
            content = content.replace(
                'style="max-width: 100%; margin: 0;"',
                'style="max-width: 100%; margin: 0; background: var(--white); border-radius: 20px; overflow: hidden; box-shadow: var(--teal-glow); transition: all 0.4s ease;"'
            )
        
        # Fix 2: Fix the clunky buttons - make them smaller and better styled
        content = content.replace(
            'style="display: inline-block; margin: 0 10px; padding: 15px 30px;"',
            'style="display: inline-block; margin: 0 10px; padding: 12px 25px; font-size: 1.1rem;"'
        )
        
        # Fix 3: Fix the broken "Back to Services" button
        content = content.replace(
            'href="/services"',
            'href="/services.html"'
        )
        
        # Fix 4: Remove any duplicate content by ensuring clean structure
        # Look for duplicate service-card divs and remove extras
        service_card_count = content.count('class="service-card"')
        if service_card_count > 1:
            # Keep only the first service-card (the main one)
            first_card_start = content.find('class="service-card"')
            second_card_start = content.find('class="service-card"', first_card_start + 1)
            
            if second_card_start != -1:
                # Find the end of the first service card section
                section_end = content.find('</section>', first_card_start)
                if section_end != -1:
                    # Remove everything between second card start and section end
                    content = content[:second_card_start] + content[section_end:]
        
        # Fix 5: Ensure proper hover effects are working
        if 'transition: all 0.4s ease' not in content:
            # Add hover effect to service card
            card_style_pos = content.find('style="max-width: 100%; margin: 0;')
            if card_style_pos != -1:
                content = content[:card_style_pos] + 'style="max-width: 100%; margin: 0; background: var(--white); border-radius: 20px; overflow: hidden; box-shadow: var(--teal-glow); transition: all 0.4s ease;"' + content[card_style_pos + len('style="max-width: 100%; margin: 0;"'):]
        
        # Write the fixed content back
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {page_path}")

print("Fixed all service pages!")
print("Fixed issues:")
print("- Added hover effects to service cards")
print("- Fixed clunky button styling")
print("- Fixed broken 'Back to Services' links")
print("- Removed duplicate content")
print("- Ensured proper page structure")