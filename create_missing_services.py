# create_missing_services.py
import os

def create_missing_services():
    print("CREATING MISSING SERVICE PAGES...")
    
    # Service pages that are linked but don't exist
    missing_services = [
        "driveway-installation", "concrete-pouring", "hardwood-flooring", "garden-maintenance",
        "seasonal-cleanup", "landscape-design", "seasonal-prep", "painting-services",
        "drywall-repair", "fence-installation", "window-doors", "audio-visual",
        "tv-mounting-residential", "home-audio", "fertilization", "snow-removal",
        "emergency-repairs", "tree-trimming", "emergency-snow", "custom-cabinets",
        "cabinet-refacing", "onyx-countertops", "kitchen-cabinetry", "custom-storage",
        "countertop-repair", "concrete-repair", "floor-refinishing", "patio-construction",
        "basement-finishing", "siding-replacement", "deck-construction", "home-remodeling",
        "grab-bars", "custom-ramps", "senior-safety", "bathroom-accessibility"
    ]
    
    # Template for professional service pages
    service_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="{description}">
    <style>
        :root {{
            --teal: #00C4B4;
            --navy: #0A1D37;
            --light: #F8FAFC;
            --gray: #64748B;
            --gold: #FFD700;
            --white: #FFFFFF;
        }}
        body {{ font-family: 'Inter', sans-serif; background: var(--light); margin: 0; padding: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .service-hero {{ background: linear-gradient(135deg, var(--navy), #1e3a5f); color: white; padding: 80px 20px; text-align: center; }}
        .service-hero h1 {{ font-family: 'Playfair Display', serif; font-size: 3rem; margin-bottom: 20px; }}
        .service-content {{ background: white; padding: 40px; border-radius: 15px; margin-top: -50px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .return-link {{ display: inline-block; margin: 20px 0; padding: 12px 25px; background: var(--teal); color: white; text-decoration: none; border-radius: 25px; }}
    </style>
</head>
<body>
    <div class="service-hero">
        <div class="container">
            <h1>{title}</h1>
            <p>Professional {service_name} services in Norfolk NE and surrounding areas</p>
        </div>
    </div>
    
    <div class="container">
        <div class="service-content">
            <a href="../services.html" class="return-link">← Return to All Services</a>
            
            <h2>About Our {service_name} Services</h2>
            <p>{description}</p>
            
            <h3>Service Details</h3>
            <p>We provide comprehensive {service_name} solutions with attention to detail and quality craftsmanship. Contact us for a free estimate!</p>
            
            <div style="text-align: center; margin: 40px 0;">
                <a href="tel:+14054106402" style="background: var(--teal); color: white; padding: 15px 30px; border-radius: 25px; text-decoration: none; font-weight: bold;">
                    Call (405) 410-6402 for Free Estimate
                </a>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # Service descriptions
    service_descriptions = {
        "driveway-installation": "Professional driveway installation and concrete work for durable, beautiful driveways that enhance your property's curb appeal.",
        "concrete-pouring": "Expert concrete pouring and finishing services for driveways, patios, sidewalks, and other concrete surfaces.",
        "hardwood-flooring": "Beautiful hardwood floor installation and refinishing services to transform your space with timeless elegance.",
        # Add more descriptions as needed
    }
    
    created_count = 0
    for service in missing_services:
        file_path = f"services/{service}.html"
        if not os.path.exists(file_path):
            # Create title and description
            title = service.replace('-', ' ').title()
            description = service_descriptions.get(service, f"Professional {service.replace('-', ' ')} services with quality craftsmanship and attention to detail.")
            
            # Generate the page
            content = service_template.format(
                title=title,
                service_name=service.replace('-', ' '),
                description=description
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created: {file_path}")
            created_count += 1
        else:
            print(f"✅ Already exists: {file_path}")
    
    print(f"\n🎉 Created {created_count} missing service pages!")

create_missing_services()