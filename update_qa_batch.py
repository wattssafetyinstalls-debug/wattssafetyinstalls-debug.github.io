#!/usr/bin/env python3
"""
Update service pages with custom Q&A from user-provided data
Handles replacements in carousel and schema
"""

import re
import os

# User-provided Q&A data
qa_updates = {
    'services/non-slip-flooring.html': [
        {
            'question': 'non-slip flooring installation near me Norfolk',
            'answer': "We bring real peace-of-mind flooring to Norfolk homes every week. Whether it's luxury vinyl plank with deep embossed texture, porcelain tile with a high DCOF rating (0.60+), or a commercial-grade epoxy-quartz broadcast system, we only install surfaces that stay grippy even when soaking wet—because one fall is one too many.",
            'icon': 'fa-shoe-prints'
        },
        {
            'question': 'non-slip bathroom floor coating Norfolk Nebraska',
            'answer': "Our clear non-slip bathroom floor coatings go right over your existing tile or concrete and create a permanent textured surface that's invisible until your feet thank you. No more worrying about kids, grandkids, or aging parents slipping—Norfolk families call it the best $800–$1,200 they've ever spent on safety.",
            'icon': 'fa-shield-alt'
        },
        {
            'question': 'anti-slip flooring for seniors Norfolk NE',
            'answer': "We've installed hundreds of senior-safe floors across Norfolk and know exactly what works: matte-finish LVP that looks like real wood but grips like sandpaper when wet, small mosaic shower floors with tons of grout lines for traction, and warm-to-the-touch vinyl that doesn't get slick with soap or shampoo. Safety never looked this good.",
            'icon': 'fa-users'
        },
        {
            'question': 'safe shower floor for elderly near me Norfolk',
            'answer': "The safest shower floors we install for Norfolk seniors are either tiny 1×1 or 2×2 mosaic porcelain (all those grout lines = instant traction), factory-textured luxury vinyl bases, or our rolled-on quartz epoxy system that feels like fine sandpaper underfoot. Pair it with a grab bar and a seat and showering becomes worry-free again.",
            'icon': 'fa-bath'
        },
        {
            'question': 'non-slip kitchen flooring Norfolk Nebraska',
            'answer': "Kitchens see spills constantly, so we steer Norfolk homeowners toward cork (naturally grippy + forgiving), commercial-grade textured LVP, rubber flooring that looks like hardwood, or matte porcelain with a high slip rating. You still get the gorgeous look you want—just without the ER visit when the spaghetti sauce hits the floor.",
            'icon': 'fa-home'
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
