# convert_to_jekyll.py
import os
import re
import yaml

def convert_existing_pages():
    print("CONVERTING EXISTING PAGES TO JEKYLL FORMAT...")
    
    # Files to convert
    pages_to_convert = ['index.html', 'services.html', 'about.html', 'contact.html', 'service-area.html']
    
    for page in pages_to_convert:
        if os.path.exists(page):
            print(f"Converting {page}...")
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1).replace(' - Watts Safety Installs', '') if title_match else page.replace('.html', '').title()
            
            # Extract main content between header and footer
            main_content_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
            if not main_content_match:
                main_content_match = re.search(r'<div class="main-content">(.*?)</div>', content, re.DOTALL)
            
            main_content = main_content_match.group(1) if main_content_match else content
            
            # Create Jekyll front matter and content
            jekyll_content = f'''---
layout: default
title: {title}
---

{main_content}'''
            
            # Write new file
            with open(page, 'w', encoding='utf-8') as f:
                f.write(jekyll_content)
            
            print(f"  Converted {page} to Jekyll format")
    
    print("Conversion complete! All main pages now use Jekyll layout.")

def update_service_pages():
    print("\nUPDATING SERVICE PAGES...")
    
    service_files = [f for f in os.listdir('services') if f.endswith('.html')]
    
    for service_file in service_files:
        service_path = f"services/{service_file}"
        service_slug = service_file.replace('.html', '')
        
        with open(service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract service title and description
        title_match = re.search(r'<h1 class="service-title">(.*?)</h1>', content)
        title = title_match.group(1) if title_match else service_slug.replace('-', ' ').title()
        
        desc_match = re.search(r'<p class="service-description">(.*?)</p>', content, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else f"Professional {title} services in Norfolk, NE."
        
        # Create Jekyll service page
        jekyll_content = f'''---
layout: default
title: {title}
description: {description}
---

<div class="service-header">
    <h1 class="service-title">{{ page.title }}</h1>
    <p class="service-subtitle">Professional Services in Norfolk, NE</p>
</div>

<a href="{{ "{{" }} "/services.html" | relative_url {{ "}}" }}" class="back-button">← Back to All Services</a>

<div class="service-description">
    <p>{{ page.description }}</p>
</div>

<div class="cta-section">
    <h2>Ready to Get Started?</h2>
    <p>Contact us today for a free consultation and estimate!</p>
    <a href="{{ "{{" }} "/contact.html" | relative_url {{ "}}" }}" class="cta-button">Get Free Estimate</a>
</div>'''
        
        with open(service_path, 'w', encoding='utf-8') as f:
            f.write(jekyll_content)
        
        print(f"  Updated {service_file}")

if __name__ == "__main__":
    convert_existing_pages()
    update_service_pages()
    print("\nJEKYLL CONVERSION COMPLETE!")
    print("All pages now use consistent layout and navigation")
    print("Dropdown automatically includes all services")
    print("Professional design applied across entire site")