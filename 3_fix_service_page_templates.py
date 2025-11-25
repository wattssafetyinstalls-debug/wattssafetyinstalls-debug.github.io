# 3_fix_service_page_templates.py
import os

def fix_service_page_template(service_slug, service_title):
    """Fix a single service page to use consistent template"""
    
    filename = f"services/{service_slug}.html"
    if not os.path.exists(filename):
        print(f"SKIPPING: {filename} does not exist")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if page already has correct structure
    if '<!-- Service Page Template -->' in content:
        print(f"SKIPPING: {service_slug} already has correct template")
        return True
    
    # Basic template check - look for key elements
    has_correct_elements = all([
        '<h1 class="service-title">' in content,
        '<p class="service-description">' in content,
        'href="../services.html"' in content
    ])
    
    if has_correct_elements:
        print(f"SKIPPING: {service_slug} has correct structure")
        return True
    
    print(f"FIXING: {service_slug} page structure")
    
    # For now, just mark it as needing manual fix
    # We'll create a comprehensive fix script for this later
    return False

def fix_all_service_templates():
    print("STEP 3: CHECKING SERVICE PAGE TEMPLATES...")
    
    services = [
        'driveway-installation',
        'concrete-pouring',
        'hardwood-flooring', 
        'garden-maintenance',
        'landscape-design',
        'painting-services',
        'snow-removal',
        'custom-cabinets',
        'deck-construction',
        'home-remodeling'
    ]
    
    fixed_count = 0
    needs_fix = []
    
    for service_slug in services:
        if not fix_service_page_template(service_slug, service_slug.replace('-', ' ').title()):
            needs_fix.append(service_slug)
        else:
            fixed_count += 1
    
    print(f"\nSUMMARY:")
    print(f"Properly structured: {fixed_count}")
    print(f"Need manual fixing: {len(needs_fix)}")
    
    if needs_fix:
        print("\nServices needing template fixes:")
        for service in needs_fix:
            print(f"  - {service}")

if __name__ == "__main__":
    fix_all_service_templates()