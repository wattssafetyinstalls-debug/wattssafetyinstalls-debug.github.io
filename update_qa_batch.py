#!/usr/bin/env python3
"""
Update service pages with custom Q&A from user-provided data
Handles replacements in carousel and schema
"""

import re
import os

# User-provided Q&A data
qa_updates = {
    'services/room-additions.html': [
        {
            'question': 'room addition contractor near me Norfolk',
            'answer': "We've been adding beautiful, seamless rooms to Norfolk homes for years—master suites, sunrooms, in-law apartments, bigger kitchens, or that family room you've outgrown. New foundation, matching roof lines, siding that blends perfectly, and all the permits handled so it looks and feels like your house was born this way.",
            'icon': 'fa-home'
        },
        {
            'question': 'home addition builder Norfolk Nebraska',
            'answer': "From the first sketch to the final paint touch-up, we're your one-team builder. Concrete foundation poured below frost line, stick-framed or panelized walls, trusses or stick-built roof tied into the existing house, energy-efficient windows, and insulation that keeps your new space comfy year-round in Nebraska weather.",
            'icon': 'fa-hammer'
        },
        {
            'question': 'sunroom addition Norfolk NE',
            'answer': "Imagine coffee with sunrise every morning. Our Norfolk sunrooms come three-season (screened or windows) or four-season with heat, AC, and low-E glass. Cathedral ceilings, knee walls, tile or hardwood floors, and so much natural light your plants will thank you.",
            'icon': 'fa-lightbulb'
        },
        {
            'question': 'family room addition near me Norfolk',
            'answer': "Outgrowing the living room? We build spacious family room additions with vaulted ceilings, big windows, built-in entertainment centers, and luxury vinyl plank or carpet that stands up to kids and pets. Finally a place for everyone to spread out and still be together.",
            'icon': 'fa-users'
        },
        {
            'question': 'second story addition Norfolk Nebraska',
            'answer': "Double your living space without eating your yard. We reinforce the existing structure, add a full second story—new bedrooms, bathrooms, laundry upstairs, or that huge master suite you've dreamed about—and tie the roof perfectly so nobody can tell it wasn't original.",
            'icon': 'fa-arrow-up'
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
