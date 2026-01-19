# Script to generate all 5 ATP service pages using the proper template
import os

# Service data for each page
services = {
    'bathroom-accessibility.html': {
        'title': 'Bathroom Accessibility',
        'questions': [
            {
                'icon': 'fa-question-circle',
                'question': 'What makes a bathroom ADA compliant?',
                'answer': 'An ADA compliant bathroom includes specific features like grab bars, zero-step showers, appropriate toilet heights, adequate turning space, and accessible fixtures. We ensure all modifications meet ADA guidelines and local building codes for safety and accessibility.'
            },
            {
                'icon': 'fa-dollar-sign', 
                'question': 'How much does Bathroom Accessibility cost?',
                'answer': 'Costs vary based on project scope, materials, and complexity. Basic grab bar installation starts around $300, while complete bathroom renovations range from $5,000-15,000. We provide transparent, detailed quotes after a free on-site assessment.'
            },
            {
                'icon': 'fa-search-location',
                'question': 'Bathroom Accessibility near me',
                'answer': 'You\'ve found your local experts. Watts ATP Contractor provides professional Bathroom Accessibility throughout Northeast Nebraska, serving Norfolk, Battle Creek, Pierce, Madison County, Antelope County, and all surrounding communities.'
            },
            {
                'icon': 'fa-user-tie',
                'question': 'Why choose professional Bathroom Accessibility?',
                'answer': 'Professional installation ensures quality, safety, compliance with codes, and long-term durability. It protects your investment and prevents costly future problems. Our licensed, ATP-approved technicians guarantee proper workmanship.'
            },
            {
                'icon': 'fa-calendar-alt',
                'question': 'What is the process for Bathroom Accessibility?',
                'answer': 'Our process starts with a free consultation, followed by precise measurement/planning, professional execution with minimal disruption, thorough cleanup, and a final walkthrough to ensure your complete satisfaction.'
            }
        ]
    },
    'grab-bar-installation.html': {
        'title': 'Grab Bar Installation',
        'questions': [
            {
                'icon': 'fa-question-circle',
                'question': 'Where should grab bars be installed?',
                'answer': 'Grab bars should be installed in bathrooms near toilets and showers, along hallways, stairways, and any area where additional support is needed. We strategically place them based on your specific needs and ADA requirements.'
            },
            {
                'icon': 'fa-dollar-sign',
                'question': 'How much does grab bar installation cost?',
                'answer': 'Professional grab bar installation typically ranges from $150-500 per bar depending on location, wall type, and mounting requirements. Commercial-grade grab bars with proper structural anchoring ensure maximum safety and durability.'
            },
            {
                'icon': 'fa-search-location',
                'question': 'Grab bar installation near me',
                'answer': 'You\'ve found your local experts. Watts ATP Contractor provides professional grab bar installation throughout Northeast Nebraska, serving Norfolk, Battle Creek, Pierce, Madison County, Antelope County, and all surrounding communities.'
            },
            {
                'icon': 'fa-user-tie',
                'question': 'Why choose professional grab bar installation?',
                'answer': 'Professional installation ensures grab bars are properly anchored to wall studs or using appropriate mounting systems for maximum weight capacity. Incorrect installation can lead to serious injuries and property damage.'
            },
            {
                'icon': 'fa-calendar-alt',
                'question': 'What is the grab bar installation process?',
                'answer': 'Our process includes assessment of optimal placement, wall stud location, proper mounting hardware selection, secure installation, and weight testing to ensure all grab bars meet safety standards.'
            }
        ]
    },
    'wheelchair-ramp-installation.html': {
        'title': 'Wheelchair Ramp Installation',
        'questions': [
            {
                'icon': 'fa-question-circle',
                'question': 'What are ADA requirements for wheelchair ramps?',
                'answer': 'ADA requirements include 1:12 slope ratio, minimum 36-inch width, level landings, handrails on both sides, and slip-resistant surfaces. We ensure all ramps meet or exceed these standards for safety and compliance.'
            },
            {
                'icon': 'fa-dollar-sign',
                'question': 'How much does wheelchair ramp installation cost?',
                'answer': 'Wheelchair ramp costs range from $1,500-6,000 depending on length, materials, and complexity. Factors include site preparation, permits, handrails, and whether it\'s modular or custom construction.'
            },
            {
                'icon': 'fa-search-location',
                'question': 'Wheelchair ramp installation near me',
                'answer': 'You\'ve found your local experts. Watts ATP Contractor provides professional wheelchair ramp installation throughout Northeast Nebraska, serving Norfolk, Battle Creek, Pierce, Madison County, Antelope County, and all surrounding communities.'
            },
            {
                'icon': 'fa-user-tie',
                'question': 'Why choose professional ramp installation?',
                'answer': 'Professional installation ensures proper slope, structural integrity, weather resistance, and compliance with local building codes. Improper ramps can be dangerous and may require costly corrections.'
            },
            {
                'icon': 'fa-calendar-alt',
                'question': 'What is the ramp installation process?',
                'answer': 'Our process includes site evaluation, design consultation, permit acquisition, site preparation, foundation work, ramp construction, handrail installation, and final inspection to ensure safety and compliance.'
            }
        ]
    },
    'non-slip-flooring-solutions.html': {
        'title': 'Non-Slip Flooring Solutions',
        'questions': [
            {
                'icon': 'fa-question-circle',
                'question': 'What makes flooring non-slip?',
                'answer': 'Non-slip flooring features textured surfaces, specialized coatings, or materials with high COF (coefficient of friction) ratings. We offer solutions including anti-slip treatments, safety coatings, and slip-resistant flooring materials.'
            },
            {
                'icon': 'fa-dollar-sign',
                'question': 'How much do non-slip flooring solutions cost?',
                'answer': 'Costs range from $2-15 per square foot depending on the solution. Anti-slip treatments start around $2/sf, while complete flooring replacement ranges from $8-15/sf including materials and installation.'
            },
            {
                'icon': 'fa-search-location',
                'question': 'Non-slip flooring near me',
                'answer': 'You\'ve found your local experts. Watts ATP Contractor provides professional non-slip flooring solutions throughout Northeast Nebraska, serving Norfolk, Battle Creek, Pierce, Madison County, Antelope County, and all surrounding communities.'
            },
            {
                'icon': 'fa-user-tie',
                'question': 'Why choose professional non-slip flooring?',
                'answer': 'Professional application ensures proper surface preparation, correct product application, and lasting slip resistance. DIY solutions often wear quickly and may not provide adequate protection.'
            },
            {
                'icon': 'fa-calendar-alt',
                'question': 'What is the installation process?',
                'answer': 'Our process includes surface evaluation, cleaning and preparation, product selection based on usage needs, professional application, and curing time to ensure maximum effectiveness and durability.'
            }
        ]
    },
    'accessibility-safety-solutions.html': {
        'title': 'Home Accessibility Solutions',
        'questions': [
            {
                'icon': 'fa-question-circle',
                'question': 'What are home accessibility solutions?',
                'answer': 'Home accessibility solutions include door widening, ramp installation, bathroom modifications, kitchen adaptations, hallway improvements, and other modifications to make homes safe and accessible for people with mobility challenges.'
            },
            {
                'icon': 'fa-dollar-sign',
                'question': 'How much do home accessibility solutions cost?',
                'answer': 'Costs vary widely from $500 for minor modifications to $50,000+ for complete home renovations. We provide customized solutions based on your specific needs, budget, and home layout.'
            },
            {
                'icon': 'fa-search-location',
                'question': 'Home accessibility solutions near me',
                'answer': 'You\'ve found your local experts. Watts ATP Contractor provides professional home accessibility solutions throughout Northeast Nebraska, serving Norfolk, Battle Creek, Pierce, Madison County, Antelope County, and all surrounding communities.'
            },
            {
                'icon': 'fa-user-tie',
                'question': 'Why choose professional accessibility solutions?',
                'answer': 'Professional solutions ensure compliance with ADA standards, structural integrity, and long-term functionality. We consider current and future needs to create lasting accessibility improvements.'
            },
            {
                'icon': 'fa-calendar-alt',
                'question': 'What is the assessment process?',
                'answer': 'Our process includes comprehensive home assessment, needs evaluation, design consultation, cost estimation, planning, and phased implementation to minimize disruption while maximizing accessibility.'
            }
        ]
    }
}

# Read the template file
with open('bathroom-accessibility.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Generate each service page
for filename, service_data in services.items():
    if filename == 'bathroom-accessibility.html':
        continue  # Skip the template file itself
    
    # Create service-specific content
    content = template
    
    # Replace service-specific content
    content = content.replace('>Bathroom Accessibility<', f'>{service_data["title"]}<')
    content = content.replace('Bathroom Accessibility', service_data['title'])
    
    # Replace Q&A cards
    qa_cards_html = ""
    for i, question in enumerate(service_data['questions']):
        active_class = "active" if i == 0 else ""
        qa_cards_html += f'''<!-- Card {i+1} -->
<div class="qa-card {active_class}">
<i class="fas {question['icon']} qa-icon"></i>
<h3 class="qa-question">{question['question']}</h3>
<p class="qa-answer">{question['answer']}</p>
<p class="consultation-note">Free consultation for your {service_data['title']} project</p>
</div>
'''
    
    content = content.replace('<!-- Card 1 -->\n<div class="qa-card active">\n<i class="fas fa-question-circle qa-icon"></i>\n<h3 class="qa-question">What makes a bathroom ADA compliant?</h3>\n<p class="qa-answer">An ADA compliant bathroom includes specific features like grab bars, zero-step showers, appropriate toilet heights, adequate turning space, and accessible fixtures. We ensure all modifications meet ADA guidelines and local building codes for safety and accessibility.</p>\n<p class="consultation-note">Free consultation for your Bathroom Accessibility project</p>\n</div>\n<!-- Card 2 -->\n<div class="qa-card">\n<i class="fas fa-dollar-sign qa-icon"></i>\n<h3 class="qa-question">How much does Bathroom Accessibility cost?</h3>\n<p class="qa-answer">Costs vary based on project scope, materials, and complexity. Basic grab bar installation starts around $300, while complete bathroom renovations range from $5,000-15,000. We provide transparent, detailed quotes after a free on-site assessment.</p>\n<p class="consultation-note">Clear pricing with no hidden fees</p>\n</div>\n<!-- Card 3 -->\n<div class="qa-card">\n<i class="fas fa-search-location qa-icon"></i>\n<h3 class="qa-question">Bathroom Accessibility near me</h3>\n<p class="qa-answer">You\'ve found your local experts. Watts ATP Contractor provides professional Bathroom Accessibility throughout Northeast Nebraska, serving Norfolk, Battle Creek, Pierce, Madison County, Antelope County, and all surrounding communities.</p>\n<p class="consultation-note">Serving all of Northeast Nebraska</p>\n</div>\n<!-- Card 4 -->\n<div class="qa-card">\n<i class="fas fa-user-tie qa-icon"></i>\n<h3 class="qa-question">Why choose professional Bathroom Accessibility?</h3>\n<p class="qa-answer">Professional installation ensures quality, safety, compliance with codes, and long-term durability. It protects your investment and prevents costly future problems. Our licensed, ATP-approved technicians guarantee proper workmanship.</p>\n<p class="consultation-note">Expertise that adds value and prevents problems</p>\n</div>\n<!-- Card 5 -->\n<div class="qa-card">\n<i class="fas fa-calendar-alt qa-icon"></i>\n<h3 class="qa-question">What is the process for Bathroom Accessibility?</h3>\n<p class="qa-answer">Our process starts with a free consultation, followed by precise measurement/planning, professional execution with minimal disruption, thorough cleanup, and a final walkthrough to ensure your complete satisfaction.</p>\n<p class="consultation-note">A seamless process from start to finish</p>\n</div>', qa_cards_html)
    
    # Update title and meta
    content = content.replace('<title>Bathroom Accessibility | Watts ATP Contractor | Norfolk NE</title>', f'<title>{service_data["title"]} | Watts ATP Contractor | Norfolk NE</title>')
    
    # Write the new file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Generated {filename}")

print("All service pages generated successfully!")
