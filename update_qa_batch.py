#!/usr/bin/env python3
"""
Update service pages with custom Q&A from user-provided data
Handles replacements in carousel and schema
"""

import re
import os

# User-provided Q&A data
qa_updates = {
    'services/grab-bar-installation.html': [
        {
            'question': 'grab bar installation near me Norfolk Nebraska',
            'answer': "We install grab bars the right way—never just into drywall. Every bar gets mounted into studs or solid blocking, supports 500+ lbs, and is sealed perfectly around tile so water can't sneak behind. Norfolk families trust us because their parents actually feel secure, and the bars look like they belong—not tacked on as an afterthought.",
            'icon': 'fa-grip-horizontal'
        },
        {
            'question': 'bathroom grab bar installation Norfolk NE',
            'answer': "Safety + style is our thing. We place bathroom grab bars exactly where they're needed: 33–36 inches high, beside the toilet, vertical at the shower entry, horizontal and angled on the control wall, and always with 1.5-inch clearance from the wall. You pick brushed nickel, chrome, matte black, or oil-rubbed bronze—we make them disappear into your décor while keeping you safe.",
            'icon': 'fa-hammer'
        },
        {
            'question': 'professional grab bar installer near me Norfolk',
            'answer': "DIY grab bars scare us (and should scare you too). We bring stud finders, moisture meters, marine-grade blocking when needed, and years of experience knowing exactly where weight is actually transferred. One customer told us, 'My mom now showers without fear for the first time in years.' That's why we're so careful on every single install.",
            'icon': 'fa-wrench'
        },
        {
            'question': 'ADA grab bars for seniors Norfolk Nebraska',
            'answer': "True ADA-spec grab bars are 1.25–1.5 inches in diameter (perfect grip size), knurled or textured for wet hands, mounted 33–36 inches off the floor, and spaced 1.5 inches from the wall. We carry heavy-duty stainless models that look elegant and hold real weight—because your safety deserves the best, not the cheapest option at the big-box store.",
            'icon': 'fa-shield-alt'
        },
        {
            'question': 'shower grab bar placement Norfolk NE',
            'answer': "Perfect shower grab bar layout we use in nearly every Norfolk home: a 24-inch vertical bar right at the entry (helps stepping in), an 18–24 inch horizontal bar on the back wall at seat height, and a 16–24 inch angled bar on the control wall so you can steady yourself while adjusting temperature. It's the combo seniors and physical therapists love most.",
            'icon': 'fa-bath'
        }
    ]
}

def select_icon(question, answer):
    """Select Font Awesome icon based on question/answer content"""
    text = (question + ' ' + answer).lower()
    
    icon_map = {
        'cost|price|free|budget|afford|money': 'fa-dollar-sign',
        'timeline|how long|week|month|quickly|rush': 'fa-clock',
        'install|build|repair|replace|remodel': 'fa-hammer',
        'wheelchair|roll|mobility|disabled': 'fa-wheelchair',
        'grab bar|handrail|railing|rail': 'fa-grip-horizontal',
        'shower|bath|bathroom|tub|water': 'fa-bath',
        'elderly|senior|aging|old': 'fa-users',
        'safe|safety|prevent|danger': 'fa-shield-alt',
        'fall|injury|risk|protect': 'fa-first-aid',
        'lighting|bright|light|dark': 'fa-lightbulb',
        'floor|slip|non-slip|slippery': 'fa-shoe-prints',
        'access|entry|door|ramp': 'fa-hand-holding-heart',
    }
    
    for keywords, icon in icon_map.items():
        if any(word in text for word in keywords.split('|')):
            return icon
    
    return 'fa-check-circle'

def build_qa_carousel_html(questions):
    """Build Q&A carousel HTML from question list"""
    cards = []
    for item in questions:
        question = item['question']
        answer = item['answer']
        icon = item.get('icon') or select_icon(question, answer)
        
        card = f'''                    <div class="qa-card">
                        <i class="fas {icon} qa-icon"></i>
                        <h3 class="qa-question">{question}</h3>
                        <p class="qa-answer">{answer}</p>
                        <p class="consultation-note">Free consultation</p>
                    </div>'''
        cards.append(card)
    
    carousel = f'''            <div class="qa-carousel-container">
                <div class="qa-track" id="qaTrack">
{chr(10).join(cards)}
                </div>
                <div class="qa-controls">
                    <div id="qaIndicators" class="qa-indicators"></div>
                    <div class="qa-progress"><div id="qaProgress" class="qa-progress-bar"></div></div>
                </div>
            </div>'''
    return carousel

def build_schema_faq(questions):
    """Build FAQPage JSON-LD schema"""
    entities = []
    for item in questions:
        entity = {
            "@type": "Question",
            "name": item['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item['answer']
            }
        }
        entities.append(entity)
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    
    import json
    return json.dumps(schema, indent=2)

def update_page(file_path, questions):
    """Update a service page with Q&A carousel and schema"""
    if not os.path.exists(file_path):
        return f"[FAIL] File not found: {file_path}"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build new carousel
    new_carousel = build_qa_carousel_html(questions)
    carousel_pattern = r'<div class="qa-carousel-container">.*?</div>\s*</div>'
    content = re.sub(carousel_pattern, new_carousel + '</div>', content, flags=re.DOTALL)
    
    # Build and inject new schema - use raw string for replacement to avoid escape issues
    new_schema = build_schema_faq(questions)
    schema_pattern = r'<script type="application/ld\+json">.*?</script>'
    new_schema_tag = r'<script type="application/ld+json">' + '\n' + new_schema + '\n' + r'</script>'
    content = re.sub(schema_pattern, lambda m: new_schema_tag, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return f"[OK] Updated: {file_path} with {len(questions)} Q&A items"

# Main execution
if __name__ == '__main__':
    updated_count = 0
    for page_path, questions in qa_updates.items():
        result = update_page(page_path, questions)
        print(result)
        if '[OK]' in result:
            updated_count += 1
    
    print(f"[OK] Complete - Updated {updated_count} service page(s) with custom Q&A")
