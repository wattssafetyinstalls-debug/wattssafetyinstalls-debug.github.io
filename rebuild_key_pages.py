# rebuild_key_pages.py
from create_service_template import create_service_page

def rebuild_key_pages():
    print("REBUILDING KEY PAGES WITH PROPER TEMPLATES...")
    
    # Define core services
    core_services = [
        {
            'slug': 'driveway-installation',
            'title': 'Driveway Installation',
            'description': 'Professional driveway installation services in Norfolk, NE. We specialize in creating durable, beautiful driveways that enhance your home\'s curb appeal and functionality. Our experienced team uses high-quality materials and proven techniques to ensure your driveway stands the test of time.',
            'services': ['Asphalt Driveway Installation', 'Concrete Driveway Installation', 'Gravel Driveway Installation', 'Driveway Repair', 'Driveway Resurfacing']
        },
        {
            'slug': 'concrete-pouring',
            'title': 'Concrete Pouring',
            'description': 'Expert concrete pouring and finishing services for residential and commercial projects in Norfolk, NE. We deliver precise, durable concrete work that meets your specific needs and exceeds quality standards.',
            'services': ['Concrete Slabs', 'Concrete Patios', 'Concrete Walkways', 'Concrete Foundations', 'Decorative Concrete']
        },
        {
            'slug': 'hardwood-flooring',
            'title': 'Hardwood Flooring',
            'description': 'Premium hardwood floor installation and refinishing services in Norfolk, NE. Transform your space with beautiful, durable hardwood floors that add value and elegance to your home.',
            'services': ['Hardwood Floor Installation', 'Floor Sanding and Refinishing', 'Hardwood Floor Repair', 'Custom Staining', 'Floor Maintenance']
        }
    ]
    
    # Rebuild core service pages
    for service in core_services:
        page_content = create_service_page(
            service['slug'],
            service['title'], 
            service['description'],
            service['services']
        )
        
        with open(f"services/{service['slug']}.html", 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"Rebuilt: services/{service['slug']}.html")
    
    print("DONE: Core service pages rebuilt with proper templates")

if __name__ == "__main__":
    rebuild_key_pages()