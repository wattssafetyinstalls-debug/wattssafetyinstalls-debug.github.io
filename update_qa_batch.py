#!/usr/bin/env python3
"""
Update service pages with custom Q&A from user-provided data
Handles replacements in carousel and schema
"""

import re
import os

# User-provided Q&A data
qa_updates = {
    'services/wheelchair-ramp-installation.html': [
        {
            'question': 'wheelchair ramp installation near me Norfolk NE',
            'answer': "We install both modular aluminum and site-built ramps all across Norfolk and the surrounding towns. Same-day or next-day service on most modular installs, full 1:12 slope, 36-inch minimum width, handrails on both sides when the rise is over 6 inches, and a grippy surface that stays safe even when it's wet or icy. Your independence starts the day we roll up.",
            'icon': 'fa-wheelchair'
        },
        {
            'question': 'aluminum wheelchair ramp installation Norfolk Nebraska',
            'answer': "Norfolk loves aluminum ramps for good reason: zero painting ever, rust-proof, lightweight yet rated for 1,000 lbs, and they can be taken apart and moved if life changes. We stock multiple styles and can usually have your new ramp installed in just a few hours—perfect for coming home from the hospital or making Grandma's visit worry-free.",
            'icon': 'fa-hammer'
        },
        {
            'question': 'modular wheelchair ramp near me Norfolk',
            'answer': "Modular ramps are our fastest solution—most installs take less than a day. No concrete, no permits in most cases, just a perfectly level, rock-solid ramp with handrails, platforms, and non-slip mesh or solid surface. When you're ready, we can remove it just as easily or reconfigure it for a different door.",
            'icon': 'fa-boxes'
        },
        {
            'question': 'temporary wheelchair ramp rental Norfolk NE',
            'answer': "Hospital discharge tomorrow? Call us today. We deliver and install rental aluminum ramps the same or next day anywhere in the Norfolk area. Weekends and evenings too. Short-term or month-to-month, you get exactly what you need with zero long-term commitment—most families have it ready before the paperwork is even signed.",
            'icon': 'fa-clock'
        },
        {
            'question': 'home wheelchair ramp requirements Norfolk Nebraska',
            'answer': "Every ramp we install meets or exceeds residential code: maximum 1:12 slope (1 inch of rise per 12 inches of run), minimum 36-inch clear width, handrails between 34–38 inches high when rise is over 6 inches, 5-foot landings at top and bottom, and non-slip walking surface. We handle the details so you can just roll safely and confidently.",
            'icon': 'fa-check-circle'
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
