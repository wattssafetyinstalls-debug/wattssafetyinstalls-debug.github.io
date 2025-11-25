# fix_return_links.py
import os

# CSS for the return link with proper hover effects
return_link_css = """
    /* Return to Services Link Styling - Professional with Hover Effects */
    .return-to-services {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        margin: 30px 0;
        padding: 15px 30px;
        background: linear-gradient(135deg, var(--teal), #00a396);
        color: var(--white);
        text-decoration: none;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,196,180,0.3);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .return-to-services::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--navy), #09182e);
        transition: left 0.3s ease;
        z-index: -1;
    }
    
    .return-to-services:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,196,180,0.4);
        color: var(--white);
        border-color: var(--teal);
    }
    
    .return-to-services:hover::before {
        left: 0;
    }
    
    .return-to-services i {
        transition: transform 0.3s ease;
    }
    
    .return-to-services:hover i {
        transform: translateX(-3px);
    }
"""

# HTML for the return link
return_link_html = """
<div style="text-align: center; margin: 40px 0;">
    <a href="../services.html" class="return-to-services">
        <i class="fas fa-arrow-left"></i> Return to All Services
    </a>
</div>
"""

def fix_service_pages():
    # List all service pages
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
    
    for slug in service_pages:
        page_path = f'services/{slug}.html'
        
        if os.path.exists(page_path):
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add CSS if not already present
            if '.return-to-services' not in content:
                # Insert CSS before closing </style> tag
                if '</style>' in content:
                    content = content.replace('</style>', f'{return_link_css}\n</style>')
            
            # Add return link HTML if not already present
            if 'Return to All Services' not in content:
                # Find a good place to insert - usually after the main content but before footer
                if '<footer>' in content:
                    content = content.replace('<footer>', f'{return_link_html}\n<footer>')
                elif '</main>' in content:
                    content = content.replace('</main>', f'{return_link_html}\n</main>')
                else:
                    # Insert before footer as fallback
                    content = content.replace('</section>', f'</section>\n{return_link_html}')
            
            # Write updated content back
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"OK - Fixed return link: {page_path}")
        else:
            print(f"FAIL - File not found: {page_path}")

# Run the fix
fix_service_pages()
print("All service pages updated with proper return links!")