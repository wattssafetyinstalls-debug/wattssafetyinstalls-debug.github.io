#!/usr/bin/env python3
"""
Update service pages with custom Q&A from user-provided data
Handles replacements in carousel and schema
"""

import re
import os

# User-provided Q&A data
qa_updates = {
    'services/custom-ramps.html': [
        {
            'question': 'custom wheelchair ramp builder near Norfolk NE',
            'answer': "We're Norfolk's go-to custom ramp builders because every ramp we create is measured, designed, and built specifically for your home, your porch height, and your exact needs. Choose pressure-treated wood that we can stain or paint to match your house perfectly, or go with maintenance-free aluminum—either way you get gentle 1:12 slope, wide platforms for turns, double handrails, concrete footings, and a non-slip surface that handles Nebraska ice and snow like a champ.",
            'icon': 'fa-wheelchair'
        },
        {
            'question': 'custom wood wheelchair ramp Norfolk Nebraska',
            'answer': "There's something warm and welcoming about a beautifully crafted wood ramp. We use premium pressure-treated lumber, dig proper concrete footings, add sturdy handrails on both sides, texture the walking surface for traction, and finish it with deck stain or exterior paint so it looks like it grew right out of your house. Norfolk families love that it feels permanent and blends right in.",
            'icon': 'fa-hammer'
        },
        {
            'question': 'custom porch ramp installation near me Norfolk',
            'answer': "Your porch deserves a ramp that looks intentional, not tacked-on. We design custom layouts with landings, gentle turns when space is tight, keyed railings that match your existing ones, and textured decking so it's safe in rain, snow, or sun. Most Norfolk porch ramps we build become a seamless extension families actually enjoy using.",
            'icon': 'fa-home'
        },
        {
            'question': 'permanent wheelchair ramp for home Norfolk NE',
            'answer': "A permanent ramp should last decades with zero headaches. We pour concrete footings below frost line, use treated lumber or aluminum, add double 1.5-inch handrails at the correct height, and finish with commercial-grade non-slip surfacing. Once it's in, you'll forget it's even an \"accessibility feature\"—it just feels like part of the home.",
            'icon': 'fa-check-circle'
        },
        {
            'question': 'custom accessibility ramp contractor Norfolk Nebraska',
            'answer': "From the first on-site measurement to the final handshake, we handle every detail—permits if needed, precise rise-and-run calculations, material choices that match your budget and style, and rock-solid construction. Norfolk homeowners trust us because we've been building safe, beautiful custom ramps for our neighbors for years.",
            'icon': 'fa-clipboard-check'
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
