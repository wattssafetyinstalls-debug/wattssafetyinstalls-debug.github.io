#!/usr/bin/env python3
"""
Remove all stairlift-elevator references from active files
"""

import re
from pathlib import Path

def remove_stairlift_from_file(filepath):
    """Remove stairlift references from a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Remove stairlift links and list items
        content = re.sub(
            r'<li><a href="[^"]*stairlift[^"]*">.*?</a></li>\s*',
            '',
            content,
            flags=re.IGNORECASE
        )
        
        # Remove stairlift mentions in text
        content = re.sub(
            r'[,\s]*stairlifts?[,\s]*',
            ' ',
            content,
            flags=re.IGNORECASE
        )
        
        content = re.sub(
            r'[,\s]*elevator installation[,\s]*',
            ' ',
            content,
            flags=re.IGNORECASE
        )
        
        # Clean up double spaces and commas
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r',\s*,', ',', content)
        content = re.sub(r',\s*</li>', '</li>', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    base_dir = Path('.')
    
    # Only process active files, not backups
    files_to_process = [
        'index.html',
        'services.html',
        'about.html',
        'contact.html',
        'service-area.html',
        'safety-installs/index.html',
        'safety-installs/services.html',
        'safety-installs/about.html',
        'safety-installs/contact.html',
        'safety-installs/service-area.html',
    ]
    
    # Also process ATP service pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        for service_dir in services_dir.iterdir():
            if service_dir.is_dir() and service_dir.name != 'stairlift-elevator-installation':
                index_file = service_dir / 'index.html'
                if index_file.exists():
                    files_to_process.append(str(index_file.relative_to(base_dir)))
    
    print("🗑️  Removing stairlift-elevator references...")
    
    updated = 0
    for filepath in files_to_process:
        full_path = base_dir / filepath
        if full_path.exists():
            if remove_stairlift_from_file(full_path):
                print(f"✅ Updated: {filepath}")
                updated += 1
    
    print(f"\n✨ Complete! Updated {updated} files")

if __name__ == '__main__':
    main()
