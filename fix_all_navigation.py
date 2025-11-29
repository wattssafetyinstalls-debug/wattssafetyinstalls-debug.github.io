import os
import re

def update_navigation_links(file_path):
    """Update navigation links to use pretty URLs"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix navigation links - remove .html and use pretty URLs
    nav_updates = {
        'href="services.html"': 'href="/services"',
        'href="service-area.html"': 'href="/service-area"', 
        'href="about.html"': 'href="/about"',
        'href="referrals.html"': 'href="/referrals"',
        'href="contact.html"': 'href="/contact"',
        'href="index.html"': 'href="/"',
        'href="/index.html"': 'href="/"'
    }
    
    for old_link, new_link in nav_updates.items():
        content = content.replace(old_link, new_link)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_service_pages_mobile_animation(file_path):
    """Add mobile auto-animation to service pages"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add ID to main service tile for mobile targeting
    content = content.replace('class="service-tile"', 'class="service-tile" id="mainServiceTile"')
    
    # Add mobile animation CSS if not present
    if 'mobile-animated' not in content:
        mobile_css = """
        /* MOBILE AUTO-ANIMATION EFFECTS */
        @media (max-width: 768px) {
            .service-tile.mobile-animated {
                transform: translateY(-12px) scale(1.03);
                box-shadow: 0 35px 90px rgba(10,29,55,0.38);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-tile.mobile-animated::before {
                opacity: 1;
                animation: gloss 1.3s ease-out forwards;
            }
            .service-tile.mobile-animated::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.7);
                box-shadow: 0 0 35px rgba(0,196,180,0.6);
            }
            .service-tile.mobile-animated h2, 
            .service-tile.mobile-animated p, 
            .service-tile.mobile-animated .trust-text {
                color: white !important;
            }
            .service-tile.mobile-animated .trust-bar {
                background: rgba(255,255,255,0.12);
            }
            .service-tile.mobile-animated .trust-icon {
                transform: scale(1.5) translateY(-8px);
                color: var(--gold) !important;
            }
            
            .service-category.mobile-animated {
                transform: translateY(-6px) scale(1.01);
                box-shadow: 0 20px 45px rgba(10,29,55,0.25);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-category.mobile-animated::before {
                opacity: 1;
                animation: gloss 1.3s ease-out forwards;
            }
            .service-category.mobile-animated::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.7);
                box-shadow: 0 0 25px rgba(0,196,180,0.6);
            }
            .service-category.mobile-animated .category-title,
            .service-category.mobile-animated .category-services {
                color: white !important;
            }
            .service-category.mobile-animated .category-icon {
                transform: scale(1.3) translateY(-5px);
                color: var(--gold) !important;
            }
        }
        """
        
        # Insert mobile CSS before existing mobile media queries
        if '@media (max-width: 768px)' in content:
            content = content.replace('@media (max-width: 768px)', mobile_css + '\n        @media (max-width: 768px)')
    
    # Add mobile animation JavaScript if not present
    mobile_js = """
        // Mobile auto-animation after 3 seconds
        if (window.innerWidth <= 768) {
            setTimeout(function() {
                const mainTile = document.getElementById('mainServiceTile');
                const categories = document.querySelectorAll('.service-category');
                
                if (mainTile) mainTile.classList.add('mobile-animated');
                categories.forEach(category => {
                    category.classList.add('mobile-animated');
                });
            }, 3000);
        }
        """
    
    # Add to existing script tag
    if '</script>' in content and 'mobile-animated' not in content:
        content = content.replace('</script>', mobile_js + '\n    </script>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_all_files():
    """Process all HTML files in the website"""
    
    files_updated = 0
    
    # Main pages
    main_pages = ['index.html', 'about.html', 'services.html', 'service-area.html', 
                  'contact.html', 'referrals.html', 'privacy-policy.html', 'sitemap.html']
    
    for page in main_pages:
        if os.path.exists(page):
            update_navigation_links(page)
            print(f"Updated navigation: {page}")
            files_updated += 1
    
    # Service pages
    if os.path.exists('services'):
        for service_file in os.listdir('services'):
            if service_file.endswith('.html'):
                file_path = os.path.join('services', service_file)
                update_navigation_links(file_path)
                update_service_pages_mobile_animation(file_path)
                print(f"Updated service page: {service_file}")
                files_updated += 1
    
    print(f"Total files updated: {files_updated}")

if __name__ == "__main__":
    process_all_files()