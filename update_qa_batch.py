#!/usr/bin/env python3
"""
Update service pages with custom Q&A from user-provided data
Handles replacements in carousel and schema
"""

import re
import os

# User-provided Q&A data
qa_updates = {
    'services/accessibility-safety-solutions.html': [
        {
            'question': 'accessibility home modifications near me Norfolk NE',
            'answer': "If you're looking for accessibility home modifications in the Norfolk, Nebraska area, we specialize in thoughtful changes that make your home safer and more comfortable — everything from installing wheelchair ramps and stairlifts to widening doorways, adding grab bars, and converting bathrooms for easier access. We take the time to understand your exact needs so you or your loved one can stay independent at home for years to come.",
            'icon': 'fa-wheelchair'
        },
        {
            'question': 'home safety upgrades for seniors Norfolk Nebraska',
            'answer': "We love helping Norfolk-area seniors stay safe and confident in their own homes! Popular safety upgrades include brighter motion-sensor lighting, removing trip hazards, adding secure handrails on both sides of stairs, non-slip flooring throughout, and senior-friendly bathroom remodels with walk-in showers and grab bars. It's all about peace of mind for you and your family.",
            'icon': 'fa-shield-alt'
        },
        {
            'question': 'aging in place remodeling contractor Norfolk NE',
            'answer': "As a local aging-in-place remodeling contractor serving Norfolk and all of Northeast Nebraska, we focus on modifications that let you stay in the home you love as mobility needs change. Whether it's a zero-step entrance, lever door handles, or a fully accessible kitchen, we handle everything with care and respect for your lifestyle.",
            'icon': 'fa-home'
        },
        {
            'question': 'ADA compliant home modifications Norfolk Nebraska',
            'answer': "While private homes aren't required to meet full commercial ADA standards, we follow ADA guidelines whenever it makes sense — proper grab bar heights (33-36 inches), 60-inch turning radii in bathrooms, reachable light switches, and more. The goal is real-world usability, not just checking boxes.",
            'icon': 'fa-check-circle'
        },
        {
            'question': 'senior home safety assessment Norfolk NE',
            'answer': "We offer a complimentary senior home safety assessment where we walk through every room with you, looking at stairs, bathrooms, lighting, flooring, and entryways. We'll point out hidden risks and give you a clear, prioritized list of practical, affordable solutions — no pressure, just helpful advice from folks who truly care.",
            'icon': 'fa-clipboard-check'
        }
    ],
    'services/senior-safety.html': [
        {
            'question': 'senior home safety modifications near me Norfolk',
            'answer': "Nothing makes us happier than helping Norfolk families keep their parents or grandparents safe at home. Our most requested senior safety modifications include brighter LED lighting, lever-style door handles, contrast strips on steps, secure railings, and bathroom upgrades that prevent falls.",
            'icon': 'fa-lightbulb'
        },
        {
            'question': 'aging in place home modifications Norfolk Nebraska',
            'answer': "Aging in place is all about small, smart changes that add up to huge independence. We commonly install comfort-height toilets, roll-under sinks, rocker light switches, and easy-grip faucets — plus strategic lighting and flooring upgrades that make daily life simpler and safer.",
            'icon': 'fa-home'
        },
        {
            'question': 'fall prevention home assessment Norfolk NE',
            'answer': "Falls are the #1 reason seniors lose independence, but most are preventable! During our fall-prevention assessment, we check for loose rugs, poor lighting, cluttered walkways, steep stairs, and bathroom hazards, then give you a custom plan to fix the biggest risks first.",
            'icon': 'fa-exclamation-triangle'
        },
        {
            'question': 'safe home upgrades for elderly Norfolk NE',
            'answer': "Some of our favorite \"wow\" upgrades for elderly homeowners in Norfolk are automatic night lights that guide you to the bathroom, hands-free faucets, pull-down shelving in kitchens, and stairlifts that make second floors accessible again without moving.",
            'icon': 'fa-star'
        }
    ]
}

def build_qa_carousel_html(qa_list):
    """Build HTML carousel section from Q&A list"""
    html = '                        <div class="qa-carousel-container">\n'
    html += '                <div class="qa-track" id="qaTrack">\n'
    
    for idx, qa in enumerate(qa_list):
        is_active = 'active' if idx == 0 else ''
        icon = qa.get('icon', 'fa-info-circle')
        question = qa['question'].replace('"', '&quot;')
        answer = qa['answer'].replace('"', '&quot;')
        
        html += '                    <!-- Card -->\n'
        html += f'                    <div class="qa-card {is_active}">\n'
        html += f'                        <i class="fas {icon} qa-icon"></i>\n'
        html += f'                        <h3 class="qa-question">{question}</h3>\n'
        html += f'                        <p class="qa-answer">{answer}</p>\n'
        html += f'                        <p class="consultation-note">Free consultation for your project</p>\n'
        html += '                    </div>\n'
    
    html += '                </div>\n'
    html += '            </div>'
    
    return html

def build_schema_faq(qa_list):
    """Build FAQPage schema from Q&A list"""
    schema = '    <script type="application/ld+json">\n'
    schema += '{\n'
    schema += '  "@context": "https://schema.org",\n'
    schema += '  "@type": "FAQPage",\n'
    schema += '  "mainEntity": [\n'
    
    for idx, qa in enumerate(qa_list):
        question = qa['question'].replace('"', '\\"').replace('\n', ' ')
        answer = qa['answer'].replace('"', '\\"').replace('\n', ' ')
        
        schema += '    {\n'
        schema += '      "@type": "Question",\n'
        schema += f'      "name": "{question}",\n'
        schema += '      "acceptedAnswer": {\n'
        schema += '        "@type": "Answer",\n'
        schema += f'        "text": "{answer}"\n'
        schema += '      }\n'
        schema += '    }'
        
        if idx < len(qa_list) - 1:
            schema += ','
        schema += '\n'
    
    schema += '  ]\n'
    schema += '}\n'
    schema += '</script>'
    
    return schema

def update_page(file_path, qa_list):
    """Update a single page with new Q&A"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Q&A carousel
    new_carousel = build_qa_carousel_html(qa_list)
    carousel_pattern = r'<div class="qa-carousel-container">.*?</div>\s*<div class="carousel-dots"'
    new_carousel_full = new_carousel + '\n\n            <div class="carousel-dots"'
    content = re.sub(carousel_pattern, new_carousel_full, content, flags=re.DOTALL)
    
    # Replace schema
    new_schema = build_schema_faq(qa_list)
    schema_pattern = r'<script type="application/ld\+json">.*?FAQPage.*?</script>'
    content = re.sub(schema_pattern, new_schema, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Main execution
for file_path, qa_list in qa_updates.items():
    full_path = os.path.join('c:\\Users\\User\\my-website', file_path)
    if os.path.exists(full_path):
        try:
            update_page(full_path, qa_list)
            print(f'[OK] Updated: {file_path} with {len(qa_list)} Q&A items')
        except Exception as e:
            print(f'[FAIL] {file_path}: {e}')
    else:
        print(f'[SKIP] Not found: {full_path}')

print('[OK] Complete - Updated 2 service pages with custom Q&A')
