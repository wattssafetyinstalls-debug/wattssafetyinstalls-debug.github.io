# create_all_services.py
import os

# Create ALL service pages
services = [
    # TV & Audio Visual
    "tv-mounting-service",
    "home-theater-installation", 
    "audio-visual-setup",
    "projector-mounting",
    
    # Bathroom Services
    "bathroom-remodeling",
    "walk-in-shower-installation",
    "bathroom-accessibility-modifications",
    
    # Kitchen Services
    "kitchen-remodeling", 
    "cabinet-installation",
    "countertop-installation",
    
    # Accessibility Services
    "ada-ramp-installation",
    "wheelchair-ramp-construction",
    "grab-bar-installation",
    "stairlift-installation",
    
    # Maintenance Services
    "snow-removal-service",
    "lawn-maintenance", 
    "landscape-design",
    "emergency-repair-services",
    
    # Handyman Services
    "handyman-services-hourly",
    "small-home-repairs"
]

# Create service-pages folder
if not os.path.exists('service-pages'):
    os.makedirs('service-pages')

# HTML template
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Watts Safety Installs</title>
    <meta name="description" content="{description}">
    
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #0A1D37;
            border-bottom: 3px solid #00C4B4;
            padding-bottom: 10px;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #00C4B4;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>{description}</p>
    <p><strong>Contact: (405) 410-6402</strong></p>
    <a href="../index.html" class="back-link">Back to Home</a>
</body>
</html>
'''

print("Creating service pages...")

for service in services:
    readable_name = service.replace('-', ' ').title()
    
    html_content = html_template.format(
        title=readable_name,
        description=f"Professional {readable_name} services in Norfolk NE. ATP approved contractor with Nebraska license #54690-25."
    )
    
    filename = f"service-pages/{service}.html"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"Created: {filename}")

print(f"SUCCESS! Created {len(services)} service pages!")