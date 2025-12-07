#!/usr/bin/env python3
"""
Update service pages with custom Q&A from user-provided data
Handles replacements in carousel and schema
"""

import re
import os

# User-provided Q&A data
qa_updates = {
    'services/ada-compliant-showers-bathrooms.html': [
        {
            'question': 'ADA compliant shower installation near me Norfolk NE',
            'answer': "Hey Norfolk neighbor! We build real ADA-compliant showers that are safe, beautiful, and actually get used every day. That means a true zero-threshold curbless entry, 60-inch turning radius, reinforced grab bars at the perfect 33–36 inch height, fold-down teak bench, adjustable handheld sprayer on a slide bar, anti-scald valve, and gorgeous large-format tile with built-in slip resistance. Families tell us it gives their loved one independence again and gives everyone else peace of mind — that's why we love what we do.",
            'icon': 'fa-wheelchair'
        },
        {
            'question': 'walk-in shower remodel Norfolk Nebraska',
            'answer': "Replacing that old tub with a spacious walk-in shower is the smartest, most popular upgrade we do in Norfolk. We remove the tub, create a true zero-step entry (sometimes lowering the floor slightly), install a sleek linear drain, add luxury tile that feels warm underfoot, include built-in or fold-down seating, multiple grab bars, and bright LED lighting. It's safer, easier to clean, and makes your whole bathroom feel brand new.",
            'icon': 'fa-bath'
        },
        {
            'question': 'roll-in shower installation near me Norfolk NE',
            'answer': "A properly built roll-in shower changes everything for wheelchair users. We create a gentle beveled entry with no curb at all, reinforce the walls with marine-grade blocking, install heavy-duty 1.5-inch stainless grab bars (500+ lb rating), add a waterproof fold-down seat, place controls and the handheld sprayer at seated height, and finish with a trench drain and stunning tile. It's pure freedom — and it still looks like a high-end spa.",
            'icon': 'fa-hand-holding-heart'
        },
        {
            'question': 'accessible bathroom remodeling Norfolk Nebraska',
            'answer': "We turn regular bathrooms into safe, luxurious, future-proof spaces you'll love for decades. Comfort-height toilets, roll-under vanities with pretty quartz tops, lever-handles everywhere, bright warm LED lighting with motion sensors, non-slip porcelain that looks like wood or marble, and blocking hidden in every wall ready for grab bars whenever you need them. Everything is placed so the room works perfectly whether you're standing or seated.",
            'icon': 'fa-hammer'
        },
        {
            'question': 'senior safe bathroom remodel Norfolk Nebraska',
            'answer': "Our senior-safe bathroom remodels focus on removing danger and adding confidence. We replace slippery tubs with zero-entry walk-in showers, install rock-solid grab bars and seating, upgrade to textured non-slip flooring, add bright task + night lighting, and make sure every control is easy to reach from a seated position. Norfolk seniors tell us they finally feel safe and spoiled in their own bathroom again.",
            'icon': 'fa-shield-alt'
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
