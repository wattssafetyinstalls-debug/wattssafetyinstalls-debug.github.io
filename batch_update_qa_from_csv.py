#!/usr/bin/env python3
"""
Batch Q&A updater - uses norfolk-qa.csv to customize Q&A carousels and schema for service pages
Processes 3 pages at a time to maintain quality and prevent breaking changes
"""

import csv
import os
import re
from pathlib import Path

# Read CSV to get Q&A data
def read_qa_csv(csv_file):
    qa_data = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            page_url = row['Page URL']
            if page_url not in qa_data:
                qa_data[page_url] = []
            qa_data[page_url].append({
                'question': row['Question'],
                'answer': row['Answer']
            })
    return qa_data

def get_icon_for_question(question_text):
    """Determine appropriate Font Awesome icon based on question content"""
    question_lower = question_text.lower()
    
    if any(word in question_lower for word in ['cost', 'price', 'affordable', 'budget']):
        return 'fa-dollar-sign'
    elif any(word in question_lower for word in ['how long', 'timeline', 'duration']):
        return 'fa-clock'
    elif any(word in question_lower for word in ['install', 'installation', 'build']):
        return 'fa-hammer'
    elif any(word in question_lower for word in ['difference', 'vs', 'vs.']):
        return 'fa-balance-scale'
    elif any(word in question_lower for word in ['maintenance', 'care', 'clean']):
        return 'fa-broom'
    elif any(word in question_lower for word in ['location', 'near', 'service']):
        return 'fa-map-marker-alt'
    elif any(word in question_lower for word in ['safety', 'safe', 'prevent']):
        return 'fa-shield-alt'
    elif any(word in question_lower for word in ['accessibility', 'wheelchair', 'ada']):
        return 'fa-wheelchair'
    elif any(word in question_lower for word in ['professional', 'contractor', 'expert']):
        return 'fa-user-tie'
    elif any(word in question_lower for word in ['material', 'type', 'option', 'options']):
        return 'fa-list'
    elif any(word in question_lower for word in ['design', 'style', 'custom']):
        return 'fa-palette'
    else:
        return 'fa-info-circle'

def build_qa_carousel_html(qa_list):
    """Build HTML carousel section from Q&A list (takes first 5)"""
    qa_items = qa_list[:5]  # Limit to 5 cards
    
    html = '            <div class="qa-carousel-container">\n'
    html += '                <div class="qa-track" id="qaTrack">\n'
    
    for idx, qa in enumerate(qa_items):
        is_active = 'active' if idx == 0 else ''
        icon = get_icon_for_question(qa['question'])
        
        html += '                    <!-- Card -->\n'
        html += f'                    <div class="qa-card {is_active}">\n'
        html += f'                        <i class="fas {icon} qa-icon"></i>\n'
        html += f'                        <h3 class="qa-question">{qa["question"]}</h3>\n'
        html += f'                        <p class="qa-answer">{qa["answer"]}</p>\n'
        html += f'                        <p class="consultation-note">Free consultation for your project</p>\n'
        html += '                    </div>\n'
    
    html += '                </div>\n'
    html += '            </div>'
    
    return html

def build_schema_faq(page_name, qa_list):
    """Build FAQPage schema from Q&A list"""
    qa_items = qa_list[:5]
    
    schema = '    <script type="application/ld+json">\n'
    schema += '{\n'
    schema += '  "@context": "https://schema.org",\n'
    schema += '  "@type": "FAQPage",\n'
    schema += '  "mainEntity": [\n'
    
    for idx, qa in enumerate(qa_items):
        # Escape quotes and special characters for JSON
        question = qa['question'].replace('"', '\\"')
        answer = qa['answer'].replace('"', '\\"')
        
        schema += '    {\n'
        schema += '      "@type": "Question",\n'
        schema += f'      "name": "{question}",\n'
        schema += '      "acceptedAnswer": {\n'
        schema += '        "@type": "Answer",\n'
        schema += f'        "text": "{answer}"\n'
        schema += '      }\n'
        schema += '    }'
        
        if idx < len(qa_items) - 1:
            schema += ','
        schema += '\n'
    
    schema += '  ]\n'
    schema += '}\n'
    schema += '</script>'
    
    return schema

def update_page_qa_and_schema(file_path, qa_data):
    """Update a single page with Q&A carousel and schema"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the Q&A carousel section
    carousel_pattern = r'<div class="qa-carousel-container">.*?</div>\s*<div class="carousel-dots"'
    new_carousel = build_qa_carousel_html(qa_data) + '\n\n            <div class="carousel-dots"'
    
    content = re.sub(carousel_pattern, new_carousel, content, flags=re.DOTALL)
    
    # Find and replace or add schema
    schema_pattern = r'<script type="application/ld\+json">\s*\{[\s\S]*?"FAQPage"[\s\S]*?</script>'
    new_schema = build_schema_faq(file_path, qa_data)
    
    if re.search(schema_pattern, content):
        content = re.sub(schema_pattern, new_schema, content, flags=re.DOTALL)
    else:
        # Add before closing body if no schema exists
        content = content.replace('</body>', new_schema + '\n\n</body>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    csv_file = 'norfolk-qa.csv'
    services_dir = 'services'
    
    qa_data = read_qa_csv(csv_file)
    
    updated_count = 0
    
    # Get unique pages from CSV and sort them
    pages_to_update = sorted(qa_data.keys())
    
    print(f'Found {len(pages_to_update)} pages with Q&A data\n')
    
    for page_url in pages_to_update:
        file_path = os.path.join(services_dir, os.path.basename(page_url))
        
        if os.path.exists(file_path):
            try:
                update_page_qa_and_schema(file_path, qa_data[page_url])
                updated_count += 1
                print(f'[OK] Updated: {os.path.basename(file_path)} ({len(qa_data[page_url])} Q&A items)')
            except Exception as e:
                print(f'[FAIL] Failed: {file_path} - {e}')
        else:
            print(f'[SKIP] Missing: {file_path}')
    
    print(f'\n[OK] Complete - Updated {updated_count} service pages with Q&A from CSV')

if __name__ == '__main__':
    main()
