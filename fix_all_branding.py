#!/usr/bin/env python3
"""
Comprehensive script to fix all branding issues:
1. Change "DBA" to more casual language
2. Ensure license numbers are consistent
3. Fix service area links
"""

import os
import re
from pathlib import Path

def fix_dba_branding(content):
    """Replace formal DBA language with casual brother company language"""
    replacements = {
        'DBA of Watts ATP Contractor': 'Sister company of Watts ATP Contractor',
        'Watts ATP Contractor DBA': 'Sister company of Watts ATP Contractor',
        'alternateName": "Watts ATP Contractor DBA"': 'alternateName": "Sister company of Watts ATP Contractor"',
        'As a DBA of Watts ATP Contractor': 'As the sister company of Watts ATP Contractor',
        'Operating as DBA of': 'Operating as the sister company of',
        'DBA relationship': 'sister company relationship',
        'our DBA': 'our sister company',
        'the DBA': 'our sister company',
        'Visit our home services division': 'Visit our sister company for home services',
        'home services division': 'sister company',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    return content

def fix_service_area_links(content):
    """Fix service area links to point to DBA service area page"""
    # Fix navigation links
    content = re.sub(
        r'<a href="/service-area">Service Area</a>',
        '<a href="/safety-installs/service-area">Service Area</a>',
        content
    )
    
    return content

def ensure_license_info(content):
    """Ensure Nebraska license info is present"""
    # Make sure license number appears
    if 'Nebraska Reg #54690-25' not in content and 'Watts Safety Installs' in content:
        # Add to footer if missing
        content = re.sub(
            r'(<p>.*?Watts Safety Installs.*?</p>)',
            r'\1\n<p>Nebraska Reg #54690-25 • Fully Insured $1M</p>',
            content,
            count=1
        )
    
    return content

def process_file(filepath):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_dba_branding(content)
        content = fix_service_area_links(content)
        content = ensure_license_info(content)
        
        # Only write if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent
    dba_dir = base_dir / 'safety-installs'
    
    print("🔧 Fixing branding issues...")
    
    files_updated = 0
    
    # Fix DBA homepage
    if process_file(dba_dir / 'index.html'):
        print(f"✅ Updated: safety-installs/index.html")
        files_updated += 1
    
    # Fix all DBA service pages
    services_dir = dba_dir / 'services'
    if services_dir.exists():
        for service_dir in services_dir.iterdir():
            if service_dir.is_dir():
                index_file = service_dir / 'index.html'
                if index_file.exists():
                    if process_file(index_file):
                        print(f"✅ Updated: {service_dir.name}")
                        files_updated += 1
    
    # Fix main site references to DBA
    main_files = ['index.html', 'services.html', 'about.html']
    for filename in main_files:
        filepath = base_dir / filename
        if filepath.exists():
            if process_file(filepath):
                print(f"✅ Updated: {filename}")
                files_updated += 1
    
    print(f"\n✨ Complete! Updated {files_updated} files")
    print("   - Changed 'DBA' to 'sister company'")
    print("   - Ensured license numbers present")
    print("   - Fixed service area links")

if __name__ == '__main__':
    main()
