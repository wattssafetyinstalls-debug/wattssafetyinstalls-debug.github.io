#!/usr/bin/env python3
"""
Update service pages with custom Q&A from user-provided data
Handles replacements in carousel and schema
"""

import re
import os

# User-provided Q&A data
qa_updates = {
    'services/bathroom-accessibility.html': [
        {
            'question': 'accessible bathroom remodel near me Norfolk NE',
            'answer': "We turn everyday bathrooms into safe, beautiful, easy-to-use spaces that work for every body and every age. That means 30×48-inch clear floor spaces beside fixtures, reinforced walls ready for grab bars, roll-under vanities with pretty sinks, comfort-height toilets, lever faucets, bright motion-sensor lighting, and gorgeous non-slip tile throughout. Norfolk families love that it looks like a high-end remodel while being 100% future-proof.",
            'icon': 'fa-hammer'
        },
        {
            'question': 'handicap accessible bathroom remodeling Norfolk Nebraska',
            'answer': "Whether you use a wheelchair today or just want to plan ahead, we build bathrooms that give you room to move. Five-foot turning circles, zero-threshold showers with trench drains, lower mirrors and towel bars, roll-under sinks with knee space, heavy-duty grab bars exactly where they're needed, and anti-scald everything. It's accessibility done with style—no hospital vibes here.",
            'icon': 'fa-wheelchair'
        },
        {
            'question': 'senior friendly bathroom remodel Norfolk Nebraska',
            'answer': "Our senior-friendly remodels are all about making mornings easier and safer without sacrificing beauty. Higher \"comfort-height\" toilets (easier on hips and knees), spacious walk-in showers with built-in seats and handheld sprayers, grab bars that double as towel bars, bright warm lighting that comes on automatically, and slip-resistant floors that still look elegant. You'll feel independent and spoiled every single day.",
            'icon': 'fa-shield-alt'
        },
        {
            'question': 'bathroom modifications for disabled Norfolk NE',
            'answer': "We listen first, then customize everything to your exact needs—ceiling track lifts, permanent or removable transfer benches, bidet toilet seats, extra-wide doors, lowered light switches, contrasting toe-kicks so steps are visible, and reinforced walls ready for any equipment you might add later. Whatever makes your daily routine smoother and safer, we make it happen with care.",
            'icon': 'fa-hand-holding-heart'
        },
        {
            'question': 'wheelchair accessible shower remodel near me Norfolk',
            'answer': "Our wheelchair-accessible showers give you real room to roll in, turn around, and transfer comfortably. Full 5-foot turning radius, fold-down waterproof teak bench, multiple grab bar layouts (vertical at entry, L-shaped inside, horizontal on back wall), rainfall + handheld combo at the perfect height, trench drain, and large-format tile that's easy to clean and easy on bare feet. It's pure independence that still feels luxurious.",
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
