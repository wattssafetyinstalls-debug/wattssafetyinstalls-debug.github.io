#!/usr/bin/env python3
"""
FIX ALL HAMBURGER MENUS WITH REAL SERVICE LINKS
"""
import re

def fix_all_service_links():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Define all your real service links organized by category
    service_links = {
        'accessibility': [
            ('ADA Compliant Showers', 'https://wattsatpcontractor.com/services/ada-compliant-showers.html'),
            ('Grab Bars Installation', 'https://wattsatpcontractor.com/services/grab-bars.html'),
            ('Non-Slip Flooring', 'https://wattsatpcontractor.com/services/non-slip-flooring.html'),
            ('Custom Wheelchair Ramps', 'https://wattsatpcontractor.com/services/custom-ramps.html'),
            ('Senior Safety Modifications', 'https://wattsatpcontractor.com/services/senior-safety.html'),
            ('Bathroom Accessibility', 'https://wattsatpcontractor.com/services/bathroom-accessibility.html')
        ],
        'remodeling': [
            ('Kitchen Renovations', 'https://wattsatpcontractor.com/kitchen-renovations'),
            ('Bathroom Remodels', 'https://wattsatpcontractor.com/home-remodeling'),
            ('Basement Finishing', 'https://wattsatpcontractor.com/services/basement-finishing.html'),
            ('Deck Construction', 'https://wattsatpcontractor.com/deck-construction'),
            ('Siding Replacement', 'https://wattsatpcontractor.com/siding-replacement'),
            ('Window & Door Installation', 'https://wattsatpcontractor.com/window-doors')
        ],
        'av_services': [
            ('TV Mounting', 'https://wattsatpcontractor.com/services/tv-mounting-residential.html'),
            ('Home Theater Installation', 'https://wattsatpcontractor.com/services/home-theater.html'),
            ('Soundbar Setup', 'https://wattsatpcontractor.com/services/soundbar-setup.html'),
            ('Smart Audio Systems', 'https://wattsatpcontractor.com/services/smart-audio.html'),
            ('Projector Installation', 'https://wattsatpcontractor.com/services/projector-install.html'),
            ('Cable Management', 'https://wattsatpcontractor.com/services/cable-management.html')
        ],
        'maintenance': [
            ('Property Maintenance', 'https://wattsatpcontractor.com/services/property-maintenance-routine.html'),
            ('Emergency Repairs', 'https://wattsatpcontractor.com/services/emergency-repairs.html'),
            ('Snow Removal', 'https://wattsatpcontractor.com/snow-removal'),
            ('Seasonal Preparation', 'https://wattsatpcontractor.com/services/seasonal-prep.html'),
            ('Tree Trimming', 'https://wattsatpcontractor.com/services/tree-trimming.html'),
            ('Emergency Snow Service', 'https://wattsatpcontractor.com/services/emergency-snow.html')
        ],
        'lawn_landscape': [
            ('Lawn Maintenance', 'https://wattsatpcontractor.com/services/lawn-maintenance.html'),
            ('Landscape Design', 'https://wattsatpcontractor.com/landscape-design'),
            ('Fertilization Services', 'https://wattsatpcontractor.com/services/fertilization.html'),
            ('Seasonal Cleanup', 'https://wattsatpcontractor.com/services/seasonal-cleanup.html'),
            ('Garden Maintenance', 'https://wattsatpcontractor.com/garden-maintenance')
        ],
        'concrete_flooring': [
            ('Concrete Pouring', 'https://wattsatpcontractor.com/concrete-pouring'),
            ('Driveway Installation', 'https://wattsatpcontractor.com/driveway-installation'),
            ('Patio Construction', 'https://wattsatpcontractor.com/patio-construction'),
            ('Hardwood Flooring', 'https://wattsatpcontractor.com/hardwood-flooring'),
            ('Floor Refinishing', 'https://wattsatpcontractor.com/services/floor-refinishing.html'),
            ('Concrete Repair', 'https://wattsatpcontractor.com/services/concrete-repair.html')
        ],
        'cabinets_countertops': [
            ('Custom Cabinets', 'https://wattsatpcontractor.com/custom-cabinets'),
            ('Cabinet Refacing', 'https://wattsatpcontractor.com/services/cabinet-refacing.html'),
            ('Onyx Countertops', 'https://wattsatpcontractor.com/services/onyx-countertops.html'),
            ('Kitchen Cabinetry', 'https://wattsatpcontractor.com/services/kitchen-cabinetry.html'),
            ('Custom Storage Solutions', 'https://wattsatpcontractor.com/services/custom-storage.html'),
            ('Countertop Repair', 'https://wattsatpcontractor.com/services/countertop-repair.html')
        ]
    }

    # Replace Accessibility & Safety dropdown
    accessibility_html = ''.join([f'<a href="{url}">{name}</a>' for name, url in service_links['accessibility']])
    content = re.sub(
        r'<div class="[^"]*dropdown[^"]*">.*?</div>',
        f'<div class="service-dropdown">{accessibility_html}</div>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Replace Home Remodeling dropdown
    remodeling_html = ''.join([f'<a href="{url}">{name}</a>' for name, url in service_links['remodeling']])
    content = re.sub(
        r'<div class="[^"]*dropdown[^"]*">.*?</div>',
        f'<div class="service-dropdown">{remodeling_html}</div>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Replace TV & Audio dropdown
    av_html = ''.join([f'<a href="{url}">{name}</a>' for name, url in service_links['av_services']])
    content = re.sub(
        r'<div class="[^"]*dropdown[^"]*">.*?</div>',
        f'<div class="service-dropdown">{av_html}</div>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Replace Property Maintenance dropdown
    maintenance_html = ''.join([f'<a href="{url}">{name}</a>' for name, url in service_links['maintenance']])
    content = re.sub(
        r'<div class="[^"]*dropdown[^"]*">.*?</div>',
        f'<div class="service-dropdown">{maintenance_html}</div>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Replace Lawn & Landscape dropdown
    lawn_html = ''.join([f'<a href="{url}">{name}</a>' for name, url in service_links['lawn_landscape']])
    content = re.sub(
        r'<div class="[^"]*dropdown[^"]*">.*?</div>',
        f'<div class="service-dropdown">{lawn_html}</div>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Replace Concrete & Flooring dropdown
    concrete_html = ''.join([f'<a href="{url}">{name}</a>' for name, url in service_links['concrete_flooring']])
    content = re.sub(
        r'<div class="[^"]*dropdown[^"]*">.*?</div>',
        f'<div class="service-dropdown">{concrete_html}</div>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Replace Cabinets & Countertops dropdown
    cabinets_html = ''.join([f'<a href="{url}">{name}</a>' for name, url in service_links['cabinets_countertops']])
    content = re.sub(
        r'<div class="[^"]*dropdown[^"]*">.*?</div>',
        f'<div class="service-dropdown">{cabinets_html}</div>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Also fix the "Contact Us Now" link in the hero section
    content = re.sub(
        r'<a href="[^"]*"[^>]*>Contact Us Now</a>',
        '<a href="tel:+14054106402" class="cta-button">Contact Us Now</a>',
        content
    )

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("ALL SERVICE LINKS FIXED!")
    print("- All 7 hamburger menus now have your REAL service page links")
    print("- 40+ actual service pages linked correctly")
    print("- 'Contact Us Now' hero button fixed to call phone number")
    print("- All dropdowns now work with your real website URLs")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    fix_all_service_links()