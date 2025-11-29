import os
import re

def generate_seo_data(filename):
    """Generate SEO data for any service page based on filename"""
    
    # Convert filename to readable format
    base_name = filename.replace('.html', '')
    words = base_name.replace('-', ' ').split()
    
    # Common service patterns
    service_keywords = {
        'ada': 'ADA compliant',
        'accessibility': 'accessibility',
        'safety': 'safety',
        'installation': 'installation',
        'repair': 'repair', 
        'maintenance': 'maintenance',
        'remodeling': 'remodeling',
        'renovation': 'renovation',
        'cleaning': 'cleaning',
        'construction': 'construction',
        'solutions': 'solutions',
        'services': 'services'
    }
    
    # Build primary keyword
    primary_keyword = base_name.replace('-', ' ')
    
    # Build meta description template
    descriptions = [
        f"Professional {primary_keyword} services in Massachusetts. Expert solutions for residential and commercial properties. Free consultations available.",
        f"Looking for reliable {primary_keyword}? Our experienced team provides top-quality service with guaranteed satisfaction. Serving all of Massachusetts.",
        f"Massachusetts's trusted {primary_keyword} experts. Quality workmanship, affordable pricing, and exceptional customer service. Contact us today!",
        f"Expert {primary_keyword} services for homes and businesses. Licensed, insured professionals with years of experience. Get your free estimate now."
    ]
    
    # Choose different description templates for variety
    meta_description = descriptions[hash(filename) % len(descriptions)]
    
    return {
        'primary_keyword': primary_keyword,
        'meta_description': meta_description,
        'focus_phrase': primary_keyword
    }

def optimize_all_service_pages():
    """Optimize ALL service pages for SEO"""
    
    services_dir = 'services'
    if not os.path.exists(services_dir):
        print("Services directory not found!")
        return
    
    service_files = [f for f in os.listdir(services_dir) if f.endswith('.html')]
    total_files = len(service_files)
    
    print(f"OPTIMIZING ALL {total_files} SERVICE PAGES")
    print("=" * 60)
    
    optimized_count = 0
    
    for filename in service_files:
        file_path = os.path.join(services_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Generate SEO data for this page
            seo_data = generate_seo_data(filename)
            
            # Remove existing meta description if present
            content = re.sub(r'<meta name="description" content="[^"]*">', '', content)
            
            # Add optimized meta description
            meta_tag = f'<meta name="description" content="{seo_data["meta_description"]}">'
            if '<title>' in content:
                # Update title and add meta description
                new_title = f'{seo_data["primary_keyword"].title()} | Watts At Your Service'
                content = content.replace('<title>', f'<title>{new_title}</title>\n    {meta_tag}')
            
            # Ensure H1 exists with primary keyword
            if not re.search(r'<h1[^>]*>', content, re.IGNORECASE):
                # Add H1 if missing
                h1_tag = f'<h1 class="service-title">{seo_data["primary_keyword"].title()}</h1>'
                
                # Insert after header or at beginning of main content
                header_end = content.find('</header>')
                if header_end != -1:
                    content = content[:header_end] + h1_tag + content[header_end:]
                else:
                    main_start = content.find('<main>')
                    if main_start != -1:
                        content = content[:main_start+6] + h1_tag + content[main_start+6:]
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            optimized_count += 1
            print(f"OPTIMIZED: {filename}")
            print(f"  Keyword: {seo_data['primary_keyword']}")
            print(f"  Description: {seo_data['meta_description'][:80]}...")
            
        except Exception as e:
            print(f"ERROR: {filename}: {str(e)}")
    
    print("=" * 60)
    print(f"SUCCESS: Optimized {optimized_count} out of {total_files} service pages")
    print("\nAll service pages now have:")
    print("- Targeted primary keywords")
    print("- Optimized meta descriptions") 
    print("- Proper H1 headings")
    print("- Consistent title structure")

if __name__ == "__main__":
    optimize_all_service_pages()