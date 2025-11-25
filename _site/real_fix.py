# real_fix.py
import os

# Let's use simple, reliable local images or basic colors instead of broken external images
service_data = [
    {
        "name": "ADA-compliant showers & bathrooms",
        "slug": "ada-compliant-showers",
        "description": "Professional ADA bathroom modifications with zero-step showers and grab bars."
    },
    {
        "name": "Grab bar installation", 
        "slug": "grab-bar-installation",
        "description": "Commercial-grade grab bar installation rated for 500+ lbs capacity."
    },
    {
        "name": "Wheelchair ramp installation",
        "slug": "wheelchair-ramp-installation", 
        "description": "Custom wheelchair ramp installation meeting ADA requirements."
    },
    {
        "name": "Kitchen renovations",
        "slug": "kitchen-renovations",
        "description": "Complete kitchen remodeling including cabinets and countertops."
    },
    {
        "name": "TV mounting on walls",
        "slug": "tv-mounting",
        "description": "Professional TV wall mounting service for flat screens."
    },
    {
        "name": "Lawn maintenance & care", 
        "slug": "lawn-maintenance",
        "description": "Comprehensive lawn care services including mowing and fertilization."
    }
]

# Simple HTML template that WILL work
simple_template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{name} | Watts Safety Installs</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #f8fafc;
            color: #1E293B;
        }}
        .header {{
            background: #0A1D37;
            color: white;
            padding: 1rem 2rem;
        }}
        .content {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .service-image {{
            background: linear-gradient(135deg, #00C4B4, #0A1D37);
            height: 200px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            margin-bottom: 2rem;
        }}
        .cta-button {{
            background: #00C4B4;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            font-size: 1.1rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Watts Safety Installs</h1>
        <p>ATP Approved Contractor • Nebraska Licensed #54690-25</p>
    </div>
    
    <div class="content">
        <div class="service-image">
            {name}
        </div>
        
        <h1>{name}</h1>
        <p style="font-size: 1.2rem; line-height: 1.6;">{description}</p>
        
        <h2>Service Details</h2>
        <p>Professional installation and repair services in Norfolk NE and surrounding areas.</p>
        
        <h2>Why Choose Us?</h2>
        <ul>
            <li>ATP Approved Contractor</li>
            <li>Nebraska Licensed #54690-25</li>
            <li>Professional Workmanship</li>
            <li>Free Estimates</li>
        </ul>
        
        <div style="margin-top: 2rem;">
            <a href="tel:+14054106402" class="cta-button">Call (405) 410-6402</a>
            <a href="/" class="cta-button" style="background: #0A1D37; margin-left: 1rem;">Back to Home</a>
        </div>
    </div>
</body>
</html>
'''

# Create simple, working pages
for service in service_data:
    page_path = f'services/{service["slug"]}.html'
    
    html_content = simple_template.format(
        name=service["name"],
        description=service["description"]
    )
    
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created: {page_path}")

print("Created simple, working service pages")
print("These WILL work - no broken images, readable text")