# update_to_old_style.py
import os

# Read the kitchen renovations page as our template
with open('services/kitchen-renovations.html', 'r', encoding='utf-8') as f:
    template_content = f.read()

# Our improved service data with detailed descriptions
service_data = {
    "ada-compliant-showers-bathrooms": {
        "title": "ADA-Compliant Showers & Bathrooms",
        "description": "Professional ADA-compliant bathroom modifications with zero-step showers, grab bars, and wheelchair-accessible layouts. Full compliance with Americans with Disabilities Act standards for both residential and commercial properties in Norfolk NE.",
        "details": "Our ADA bathroom renovations include roll-in showers with fold-down seats, handheld showerheads, anti-scald valves, raised toilet seats, and vanity modifications for wheelchair access. We handle everything from design to installation with certified ADA compliance.",
        "benefits": [
            "Enhanced safety and independence",
            "Full ADA compliance certification", 
            "Increased property value",
            "Professional installation with lifetime warranty"
        ]
    },
    "grab-bar-installation": {
        "title": "Grab Bar Installation",
        "description": "Commercial-grade grab bar installation rated for 500+ lbs weight capacity. Strategic placement in bathrooms, hallways, and stairways for maximum safety and fall prevention throughout your Norfolk NE home.",
        "details": "We install stainless steel and chrome grab bars with reinforced mounting into wall studs. Professional placement in showers, beside toilets, along hallways, and on staircases for comprehensive fall protection.",
        "benefits": [
            "500+ lb weight capacity",
            "Reinforced stud mounting",
            "Rust-resistant materials",
            "Professional placement consultation"
        ]
    },
    "wheelchair-ramp-installation": {
        "title": "Wheelchair Ramp Installation", 
        "description": "Custom wheelchair ramp installation meeting ADA slope requirements for safe home access. Permanent and modular ramp solutions for Norfolk NE homes and businesses.",
        "details": "We build aluminum, wood, and concrete ramps with proper 1:12 slope ratios, handrails, and non-slip surfaces. Includes landing platforms and weather-resistant construction.",
        "benefits": [
            "ADA-compliant 1:12 slope",
            "Multiple material options",
            "Weather-resistant construction", 
            "Building permit assistance"
        ]
    },
    "stairlift-elevator-installation": {
        "title": "Stairlift & Elevator Installation",
        "description": "Professional stairlift and residential elevator installation for multi-story homes. We provide Acorn, Bruno, and Harmar stairlifts with full service and maintenance.",
        "details": "Straight and curved stairlift installation, residential elevator setup, and platform lift solutions. Includes safety features, remote controls, and ongoing maintenance services.",
        "benefits": [
            "Brand-name equipment (Acorn, Bruno, Harmar)",
            "Professional installation and training",
            "Maintenance and repair services",
            "Financing options available"
        ]
    },
    "non-slip-flooring-solutions": {
        "title": "Non-Slip Flooring Solutions",
        "description": "Slip-resistant flooring installation for bathrooms, kitchens, and entryways. We use textured tiles, non-slip vinyl, and epoxy coatings to prevent falls in Norfolk NE homes.",
        "details": "Non-slip ceramic tile, textured vinyl flooring, epoxy coatings, and rubber flooring installations. Perfect for bathrooms, kitchens, laundry rooms, and entryways.",
        "benefits": [
            "Wet-area slip resistance",
            "Easy to clean and maintain",
            "ADA-compliant surfaces",
            "Multiple style options"
        ]
    },
    "kitchen-renovations": {
        "title": "Kitchen Renovations",
        "description": "Complete kitchen remodeling services in Norfolk NE including cabinet installation, countertop replacement, and appliance setup. We create functional, beautiful kitchens that fit your lifestyle.",
        "details": "Cabinet refacing or replacement, custom countertops, tile backsplashes, flooring installation, lighting upgrades, and appliance installation with full plumbing and electrical.",
        "benefits": [
            "Increased home value",
            "Energy-efficient appliance options",
            "Custom cabinet design",
            "Project management included"
        ]
    },
    "bathroom-remodels": {
        "title": "Bathroom Remodels",
        "description": "Bathroom renovation services including tub-to-shower conversions, vanity installation, and complete bathroom transformations in Norfolk NE.",
        "details": "Shower and tub replacements, vanity installation, toilet upgrades, tile flooring and walls, lighting fixtures, ventilation systems, and plumbing updates.",
        "benefits": [
            "Modern fixture upgrades",
            "Water-efficient installations",
            "Mold-resistant materials", 
            "Increased functionality"
        ]
    },
    "room-additions": {
        "title": "Room Additions",
        "description": "Professional room addition construction for growing families in Norfolk NE. We handle everything from foundation to finishing for sunrooms, bedrooms, and office spaces.",
        "details": "Foundation work, framing, roofing, electrical, plumbing, insulation, drywall, and finishing. We obtain all necessary permits and ensure code compliance.",
        "benefits": [
            "Increased living space",
            "Professional design consultation",
            "Permit and code compliance",
            "Seamless integration with existing structure"
        ]
    },
    "flooring-installation": {
        "title": "Flooring Installation",
        "description": "Professional flooring installation including hardwood, laminate, vinyl, tile, and carpet. We provide flooring solutions for every room in your Norfolk NE home.",
        "details": "Hardwood floor installation and refinishing, laminate flooring, luxury vinyl plank, ceramic and porcelain tile, and carpet installation with proper subfloor preparation.",
        "benefits": [
            "Wide material selection",
            "Professional subfloor preparation",
            "Warranty on materials and labor",
            "Quick installation timeline"
        ]
    },
    "painting-drywall": {
        "title": "Painting & Drywall",
        "description": "Interior and exterior painting services with drywall repair and installation. We use premium paints and proper surface preparation for lasting results in Norfolk NE homes.",
        "details": "Interior painting, exterior painting, drywall installation, taping, mudding, texture matching, popcorn ceiling removal, and wall repair services.",
        "benefits": [
            "Premium paint brands (Sherwin-Williams, Benjamin Moore)",
            "Proper surface preparation",
            "Clean, professional finish",
            "Drywall texture matching"
        ]
    },
    "tv-mounting": {
        "title": "TV Mounting",
        "description": "Professional TV wall mounting service for flat screens up to 85 inches. We ensure secure installation at optimal viewing height with complete cable management in Norfolk NE homes.",
        "details": "Full-motion, tilting, and fixed TV mounts installed into studs with proper weight capacity. Includes cable concealment, power management, and device connectivity.",
        "benefits": [
            "Stud-mounted security",
            "Optimal viewing height placement",
            "Complete cable management",
            "Device connectivity setup"
        ]
    },
    "home-theater-installation": {
        "title": "Home Theater Installation",
        "description": "Complete home theater installation including surround sound, projection systems, and media center setup. We create immersive entertainment experiences for Norfolk NE homeowners.",
        "details": "5.1 and 7.1 surround sound systems, 4K projectors, motorized screens, media consoles, streaming device setup, and acoustic optimization.",
        "benefits": [
            "Professional audio calibration",
            "Seamless device integration",
            "Acoustic room optimization", 
            "Universal remote programming"
        ]
    },
    "sound-system-setup": {
        "title": "Sound System Setup",
        "description": "Sound bar and wireless speaker installation with optimal placement for superior audio quality. We integrate with your existing TV and streaming systems in Norfolk NE.",
        "details": "Sound bar mounting and calibration, wireless speaker placement, subwoofer positioning, and audio synchronization with TV and streaming devices.",
        "benefits": [
            "Optimal speaker placement",
            "Wireless system integration",
            "Audio synchronization",
            "Easy-to-use controls"
        ]
    },
    "cable-management": {
        "title": "Cable Management",
        "description": "Professional cable management and concealment for clean, organized entertainment centers. We eliminate cord clutter for safety and aesthetics in Norfolk NE homes.",
        "details": "In-wall cable running, cord concealment systems, power management, surge protection installation, and organized media center setup.",
        "benefits": [
            "Clean, professional appearance",
            "Reduced tripping hazards",
            "Surge protection installation",
            "Easy future upgrades"
        ]
    },
    "lawn-maintenance": {
        "title": "Lawn Maintenance",
        "description": "Comprehensive lawn care services including mowing, edging, fertilization, and weed control. We keep your Norfolk NE property looking beautiful year-round.",
        "details": "Weekly/bi-weekly mowing, string trimming, edging, fertilization programs, weed control, aeration, overseeding, and lawn health monitoring.",
        "benefits": [
            "Consistent, professional cut",
            "Customized fertilization plans",
            "Weed and pest control",
            "Seasonal lawn care programs"
        ]
    },
    "pressure-washing": {
        "title": "Pressure Washing",
        "description": "Professional pressure washing for driveways, siding, decks, and patios. We restore your Norfolk NE property's exterior to like-new condition.",
        "details": "Driveway and sidewalk cleaning, house siding washing, deck and patio restoration, fence cleaning, and roof stain removal with eco-friendly cleaning solutions.",
        "benefits": [
            "Restores curb appeal",
            "Prevents mold and mildew",
            "Eco-friendly cleaning solutions",
            "Extends surface life"
        ]
    },
    "gutter-cleaning": {
        "title": "Gutter Cleaning",
        "description": "Gutter cleaning, repair, and guard installation to protect your Norfolk NE home from water damage. We ensure proper drainage and prevent foundation issues.",
        "details": "Gutter cleaning, downspout clearing, leak repairs, gutter realignment, guard installation, and seasonal maintenance plans.",
        "benefits": [
            "Prevents water damage",
            "Protects foundation", 
            "Extends gutter life",
            "Seasonal maintenance plans"
        ]
    },
    "fence-repair": {
        "title": "Fence Repair",
        "description": "Fence installation and repair services for wood, vinyl, and chain-link fences. We enhance privacy and security for Norfolk NE properties.",
        "details": "Wood fence construction and repair, vinyl fence installation, chain-link fencing, gate installation and repair, and post replacement services.",
        "benefits": [
            "Increased privacy and security",
            "Professional gate installation",
            "Durable materials and construction",
            "Property value enhancement"
        ]
    },
    "handyman-services": {
        "title": "Handyman Services",
        "description": "Comprehensive handyman services for home repairs, installations, and maintenance tasks. We're your one-call solution for Norfolk NE home upkeep.",
        "details": "Drywall repair, painting touch-ups, door and window repair, shelf installation, furniture assembly, minor plumbing and electrical fixes, and general home maintenance.",
        "benefits": [
            "One-call solution for multiple tasks",
            "Quick response times",
            "Quality workmanship",
            "Affordable pricing"
        ]
    }
}

# Update each service page
for slug, service in service_data.items():
    page_path = f'services/{slug}.html'
    
    if os.path.exists(page_path):
        # Read the current page
        with open(page_path, 'r', encoding='utf-8') as f:
            page_content = f.read()
        
        # Build benefits HTML
        benefits_html = ""
        for benefit in service["benefits"]:
            benefits_html += f'<li style="margin-bottom: 0.8rem; display: flex; align-items: center;"><i class="fas fa-check-circle" style="color: var(--teal); margin-right: 10px;"></i>{benefit}</li>\n'
        
        # Update the title in hero section
        page_content = page_content.replace('<h1>Kitchen renovations</h1>', f'<h1>{service["title"]}</h1>')
        page_content = page_content.replace('<p>Professional Kitchen renovations Services in Norfolk NE</p>', f'<p>Professional {service["title"]} Services in Norfolk NE</p>')
        
        # Update the main title in content section
        page_content = page_content.replace('<h2 class="section-title" style="text-align: left; margin-bottom: 30px;">Professional Kitchen renovations</h2>', f'<h2 class="section-title" style="text-align: left; margin-bottom: 30px;">Professional {service["title"]}</h2>')
        
        # Update service title
        page_content = page_content.replace('<h3 class="service-title">Kitchen renovations Services</h3>', f'<h3 class="service-title">{service["title"]} Services</h3>')
        
        # Update description
        page_content = page_content.replace('Complete kitchen remodeling services in Norfolk NE including cabinet installation, countertop replacement, flooring, and appliance setup. We create functional, beautiful kitchens that fit your lifestyle.', service["description"])
        
        # Update service details
        page_content = page_content.replace('Cabinet refacing or replacement, quartz and granite countertops, tile backsplashes, flooring installation, lighting upgrades, and appliance installation with full plumbing and electrical.', service["details"])
        
        # Update benefits
        old_benefits_start = page_content.find('<h3 style="color: var(--navy); margin-bottom: 1rem; border-bottom: 2px solid var(--teal); padding-bottom: 0.5rem;">Key Benefits</h3>')
        old_benefits_end = page_content.find('</ul>', old_benefits_start) + 5
        
        new_benefits_section = f'''<h3 style="color: var(--navy); margin-bottom: 1rem; border-bottom: 2px solid var(--teal); padding-bottom: 0.5rem;">Key Benefits</h3>
                            <ul style="columns: 2; list-style: none; padding: 0;">
                                {benefits_html}
                            </ul>'''
        
        page_content = page_content[:old_benefits_start] + new_benefits_section + page_content[old_benefits_end:]
        
        # Remove the broken image
        image_start = page_content.find('<img loading="lazy" src="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"')
        if image_start != -1:
            image_end = page_content.find('/>', image_start) + 2
            page_content = page_content[:image_start] + page_content[image_end:]
        
        # Update CTA section title
        page_content = page_content.replace('<h2>Ready for Professional Kitchen renovations?</h2>', f'<h2>Ready for Professional {service["title"]}?</h2>')
        
        # Write the updated page
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        
        print(f"Updated: {page_path}")

print("All service pages updated to match the old style with new descriptions!")
print("Features:")
print("- Same professional structure as kitchen renovations page")
print("- No broken images")
print("- Updated detailed descriptions")
print"- All the visual appeal you liked")