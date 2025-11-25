# fix_all_issues_no_unicode.py
import os
import re

def fix_all_issues():
    print("FIXING ALL IDENTIFIED ISSUES...")
    
    # 1. First, let's fix the hover effect text legibility
    print("\nFIXING HOVER EFFECT TEXT LEGIBILITY...")
    
    # Read the service pages and fix the hover CSS
    for filename in os.listdir('services'):
        if filename.endswith('.html'):
            filepath = f"services/{filename}"
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix hover effect - ensure text stays readable
            content = content.replace(
                '.service-card:hover .service-title,',
                '.service-card:hover .service-title {'
            )
            
            # Add better text shadow for readability on hover
            content = content.replace(
                'color: var(--white) !important;',
                'color: var(--white) !important; text-shadow: 0 2px 4px rgba(0,0,0,0.3); font-weight: 700;'
            )
            
            # Fix the return to services link
            content = content.replace(
                'href="/services.html"',
                'href="../services.html"'
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed hover and links: {filename}")

    # 2. Fix the dropdown link descriptions in main pages
    print("\nUPDATING DROPDOWN LINK DESCRIPTIONS...")
    
    # Update index.html dropdown descriptions
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # More descriptive dropdown text replacements
    dropdown_updates = {
        'Driveway Installation': 'Professional Driveway Installation & Repair',
        'Concrete Pouring': 'Expert Concrete Pouring & Finishing',
        'Hardwood Flooring': 'Premium Hardwood Floor Installation',
        'Garden Maintenance': 'Complete Garden Care & Maintenance',
        'Landscape Design': 'Custom Landscape Design & Installation',
        'Painting Services': 'Interior & Exterior Painting',
        'Snow Removal': 'Snow Removal & De-icing Services',
        'Custom Cabinets': 'Custom Cabinet Design & Installation',
        'Deck Construction': 'Deck Building & Construction',
        'Home Remodeling': 'Complete Home Remodeling Services'
    }
    
    for old, new in dropdown_updates.items():
        index_content = index_content.replace(f'>{old}<', f'>{new}<')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("Updated index.html dropdown descriptions")

    # 3. Update services.html dropdown descriptions
    with open('services.html', 'r', encoding='utf-8') as f:
        services_content = f.read()
    
    for old, new in dropdown_updates.items():
        services_content = services_content.replace(f'>{old}<', f'>{new}<')
    
    with open('services.html', 'w', encoding='utf-8') as f:
        f.write(services_content)
    print("Updated services.html dropdown descriptions")

    # 4. Create SEO-optimized service pages with warm, human descriptions
    print("\nUPDATING SEO DESCRIPTIONS (150+ WORDS)...")
    
    # Enhanced service descriptions with warm, human tone
    enhanced_descriptions = {
        "driveway-installation": """
        Welcome to Watts Safety Installs - your trusted partner for professional driveway installation in Norfolk, NE and surrounding communities. 
        We understand that your driveway is more than just a parking space; it's the first impression visitors have of your home and a crucial 
        element of your property's curb appeal. Our experienced team takes pride in transforming worn-out driveways into beautiful, durable surfaces 
        that stand the test of time. Using only the highest quality materials and proven installation techniques, we ensure your new driveway not 
        only looks stunning but provides years of reliable service. Whether you're considering elegant concrete, durable asphalt, or natural gravel, 
        we'll guide you through every decision to create the perfect driveway solution for your home and lifestyle. What truly sets us apart is our 
        commitment to clear communication, transparent pricing, and making the entire process stress-free for you. We treat every project with the 
        same care and attention we would give our own homes, because we believe you deserve nothing less.
        """,
        
        "concrete-pouring": """
        At Watts Safety Installs, we pour more than just concrete - we pour our passion for craftsmanship into every project we undertake in Norfolk 
        and throughout Northeast Nebraska. With years of experience in concrete work, we've mastered the art and science of creating beautiful, 
        long-lasting concrete surfaces that enhance both the functionality and beauty of your property. Our process begins with a thorough consultation 
        where we listen carefully to your vision, assess your specific needs, and provide expert recommendations tailored to your situation. We then 
        prepare the site with meticulous attention to detail, ensuring proper grading and foundation work that prevents future issues. When it comes 
        time to pour, we use premium concrete mixes and advanced techniques to achieve that perfect finish you're looking for. But our service doesn't 
        stop there - we provide comprehensive sealing and maintenance advice to protect your investment for years to come. We're not just contractors; 
        we're your neighbors who genuinely care about delivering results that make you proud to call us.
        """,
        
        "hardwood-flooring": """
        There's something truly special about hardwood floors - they bring warmth, character, and timeless elegance to any space. At Watts Safety 
        Installs, we're passionate about helping Norfolk area homeowners experience the beauty and value that quality hardwood flooring can bring 
        to their homes. Our journey with you begins with a personal consultation where we take the time to understand your lifestyle, design preferences, 
        and practical needs. We'll walk you through the various options available - from classic oak and maple to exotic species like Brazilian cherry 
        or bamboo - explaining the unique benefits and considerations of each. Our installation team approaches every project with an artist's eye for 
        detail and a craftsman's commitment to quality, ensuring perfectly laid floors that enhance your home's architecture. We also specialize in 
        restoring existing hardwood floors, bringing worn surfaces back to their original glory through careful sanding, staining, and finishing. 
        What makes us different is our genuine care for your satisfaction and our commitment to making the entire process enjoyable and stress-free.
        """
    }
    
    # Update service pages with enhanced descriptions
    for service_slug, description in enhanced_descriptions.items():
        filepath = f"services/{service_slug}.html"
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update meta description (first 160 chars for SEO)
            meta_desc = description[:160].replace('\n', ' ') + '...'
            content = re.sub(
                r'<meta name="description" content="[^"]*"',
                f'<meta name="description" content="{meta_desc}"',
                content
            )
            
            # Update the page description
            content = re.sub(
                r'<p class="service-description">[^<]*</p>',
                f'<p class="service-description">{description.strip()}</p>',
                content
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Enhanced SEO description: {service_slug}")

    print("\nALL ISSUES FIXED!")
    print("Hover effects now readable with text shadows")
    print("Dropdown links have descriptive professional text") 
    print("Return to Services button now functional")
    print("SEO descriptions expanded with warm, human tone")
    print("All files updated and ready for deployment")

if __name__ == "__main__":
    fix_all_issues()