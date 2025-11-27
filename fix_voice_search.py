#!/usr/bin/env python3
"""
FIX VOICE SEARCH TEXT - Embed naturally without breaking design
"""

import os
import re

def fix_voice_search_text():
    services_dir = "services"
    fixed_count = 0
    
    # Voice search replacements - natural embedding
    voice_search_fixes = {
        r'Voice search optimized: "Hey Google, who does the best TV mounting near me in Norfolk Nebraska\?" – Watts Safety Installs appears first because': 
        'Homeowners searching for TV mounting experts in Norfolk Nebraska choose Watts Safety Installs because',
        
        r'Voice search ready: "Hey Siri, find snow removal near me in Norfolk Nebraska that comes automatically" – Watts Safety Installs has you covered':
        'When Norfolk residents need reliable snow removal that arrives automatically after heavy snowfall, they trust Watts Safety Installs to',
        
        r'Voice search optimized: "Hey Google, who installs hardwood floors near me in Norfolk Nebraska with free estimates\?" – Watts Safety Installs delivers':
        'For hardwood floor installation in Norfolk Nebraska with complimentary estimates, homeowners select Watts Safety Installs for',
        
        r'Voice search friendly: "Find TV mounting service in Norfolk Nebraska" - Watts Safety Installs provides':
        'When searching for professional TV mounting in Norfolk Nebraska, customers choose Watts Safety Installs for',
        
        r'Voice search ready: "Find snow shoveling service in Norfolk NE" - Watts Safety Installs offers':
        'For dependable snow shoveling service throughout Norfolk NE, residents rely on Watts Safety Installs to',
        
        r'Voice search friendly: "Find flooring installation in Norfolk Nebraska" - Watts Safety Installs delivers':
        'Homeowners looking for quality flooring installation in Norfolk Nebraska trust Watts Safety Installs for',
        
        r'Voice search optimized: "Find lawn fertilization services near me in Norfolk Nebraska" - Watts Safety Installs delivers':
        'When Norfolk homeowners search for professional lawn fertilization services nearby, they choose Watts Safety Installs for',
        
        r'Voice search optimized: "Hey Google, who installs ADA compliant showers near me in Norfolk Nebraska\?" - Watts Safety Installs creates':
        'For ADA compliant shower installation in Norfolk Nebraska, families trust Watts Safety Installs to create',
        
        r'Voice search optimized: "Hey Google, find kitchen remodeling contractors near me in Norfolk Nebraska" - Watts Safety Installs delivers':
        'Homeowners searching for kitchen remodeling contractors in Norfolk Nebraska select Watts Safety Installs for',
        
        r'Voice search optimized: "Hey Google, who does bathroom remodeling near me in Norfolk Nebraska\?" - Watts Safety Installs transforms':
        'When Norfolk residents need bathroom remodeling services, they choose Watts Safety Installs to transform',
        
        r'Voice search optimized: "Hey Google, find deck builders near me in Norfolk Nebraska" - Watts Safety Installs creates':
        'For custom deck building in Norfolk Nebraska, homeowners trust Watts Safety Installs to create',
        
        r'Voice search optimized: "Hey Google, find a reliable handyman near me in Norfolk Nebraska" - Watts Safety Installs is':
        'When searching for reliable handyman services in Norfolk Nebraska, residents choose Watts Safety Installs as',
        
        r'Voice search optimized: "Hey Google, find professional painters near me in Norfolk Nebraska" - Watts Safety Installs delivers':
        'Homeowners looking for professional painting services in Norfolk Nebraska select Watts Safety Installs for',
        
        r'Voice search optimized: "Hey Google, who installs grab bars near me in Norfolk Nebraska\?" - Watts Safety Installs creates':
        'For secure grab bar installation in Norfolk Nebraska, families trust Watts Safety Installs to create',
        
        r'Voice search optimized: "Hey Google, find wheelchair ramp builders near me in Norfolk Nebraska" - Watts Safety Installs creates':
        'When Norfolk residents need wheelchair ramp construction, they choose Watts Safety Installs to build',
        
        r'Voice search optimized: "Hey Google, who installs home theater systems near me in Norfolk Nebraska\?" - Watts Safety Installs creates':
        'For professional home theater installation in Norfolk Nebraska, homeowners trust Watts Safety Installs to create'
    }
    
    for filename in os.listdir(services_dir):
        if not filename.endswith(".html") or filename.endswith(".backup"):
            continue
            
        filepath = os.path.join(services_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Fix voice search text
        for voice_pattern, replacement in voice_search_fixes.items():
            content = re.sub(voice_pattern, replacement, content)
        
        # Also fix any remaining generic voice search patterns
        content = re.sub(
            r'Voice search (?:optimized|ready|friendly): "[^"]*" - Watts Safety Installs',
            'Watts Safety Installs',
            content
        )
        
        # Fix any awkward transitions from the replacements
        content = re.sub(r'because\s+we deliver', 'because we deliver', content)
        content = re.sub(r'for\s+we provide', 'for our professional', content)
        content = re.sub(r'to\s+we create', 'to create', content)
        
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"FIXED VOICE SEARCH -> {filename}")
            fixed_count += 1
        else:
            print(f"ALREADY GOOD -> {filename}")
    
    print(f"COMPLETE - Fixed voice search text in {fixed_count} pages")
    print("Voice search keywords are now naturally embedded in the content")

if __name__ == "__main__":
    fix_voice_search_text()