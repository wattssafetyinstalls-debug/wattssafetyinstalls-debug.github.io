services = [
    {
        "id": "accessibility-safety",
        "title": "Accessibility & Safety Solutions",
        "description": "We specialize in creating safe, accessible environments for individuals with mobility challenges. Our comprehensive solutions include ADA-compliant showers with zero-step entries, commercial-grade grab bars rated for 500+ lbs, non-slip flooring options, and custom-built accessibility ramps that meet all regulatory requirements.",
        "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80",
        "alt": "Accessibility & Safety Solutions Near Me - ADA Ramps & Grab Bars",
        "sub_services": [
            {"name": "ADA-compliant showers & bathrooms", "link": "/service-pages/ada-compliant-showers.html"},
            {"name": "Commercial-grade grab bars & handrails", "link": "/service-pages/grab-bars.html"},
            {"name": "Non-slip flooring installations", "link": "/service-pages/non-slip-flooring.html"},
            {"name": "Custom accessibility ramps", "link": "/service-pages/custom-ramps.html"},
            {"name": "Senior safety modifications", "link": "/service-pages/senior-safety.html"}
        ]
    },
    # Add similar dictionaries for other services: home-remodeling, tv-mounting, property-maintenance (including lawn care subs)
]

os.makedirs('service-pages', exist_ok=True)

for service in services:
    with open(f'service-pages/{service["id"]}.html', 'w') as f:
        f.write(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{service["title"]} | Watts Safety Installs</title>
</head>
<body>
    <h1>{service["title"]}</h1>
    <p>{service["description"]}</p>
    <!-- Add more content -->
</body>
</html>
        ''')
print("Service pages created.")