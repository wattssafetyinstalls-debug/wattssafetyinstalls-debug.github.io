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
            'answer': "We're the Norfolk team families call when they want their home to stay safe and livable for decades. Wheelchair ramps, zero-step entries, wider doorways, stairlifts, grab bars, senior-friendly bathrooms; whatever you need to keep loving the house you're in, we make it happen with zero stress and a whole lot of care.",
            'icon': 'fa-home'
        },
        {
            'question': 'home safety upgrades for seniors Norfolk Nebraska',
            'answer': "Simple upgrades make the biggest difference: brighter motion-sensor lighting everywhere, removal of throw rugs and clutter, secure handrails on both sides of every step, non-slip flooring, bathroom grab bars, and lever door handles. Norfolk seniors tell us they finally feel steady and confident again in their own home.",
            'icon': 'fa-lightbulb'
        },
        {
            'question': 'aging in place remodeling contractor Norfolk NE',
            'answer': "Aging in place isn't about giving things up; it's about smart changes that let you keep everything you love. We widen doorways for walkers and wheelchairs, lower countertops when needed, install easy-grip faucets and handles, add beautiful ramps that match your house, and turn bathrooms into safe retreats. Stay home, stay happy, stay you.",
            'icon': 'fa-hammer'
        },
        {
            'question': 'ADA compliant home modifications Norfolk Nebraska',
            'answer': "Even though private homes aren't required to be fully commercial ADA, we follow the guidelines that actually matter: proper reach ranges, 32-inch clear doorways, 60-inch shower turning spaces, grab-bar blocking, and light switches at 42–48 inches. It's real-world accessibility that looks and feels like home.",
            'icon': 'fa-check-circle'
        },
        {
            'question': 'senior home safety assessment Norfolk NE',
            'answer': "Let us walk through your home with you—no cost, no pressure. We'll spot loose rugs, dark hallways, steep steps, slippery bathrooms, and anything else that could cause a fall, then give you a simple prioritized list of fixes from \"do this today\" to \"nice to have later.\" Most Norfolk families say it's the best hour they ever spent.",
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
