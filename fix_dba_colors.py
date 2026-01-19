#!/usr/bin/env python3
"""
Fix color schemes in DBA service pages
- Replace navy/teal/gold with black/red/cream
"""

import os
import re
from pathlib import Path

# Define color replacements
COLOR_REPLACEMENTS = {
    # CSS Variables
    '--teal: #00C4B4': '--red: #dc2626',
    '--navy: #0A1D37': '--black: #1a1a1a',
    '--gold: #FFD700': '--cream: #f5f5dc',
    
    # Variable references
    'var(--teal)': 'var(--red)',
    'var(--navy)': 'var(--black)',
    'var(--gold)': 'var(--cream)',
    
    # Direct hex colors
    '#00C4B4': '#dc2626',
    '#0A1D37': '#1a1a1a',
    '#FFD700': '#f5f5dc',
}

def fix_colors_in_file(filepath):
    """Fix color scheme in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old_color, new_color in COLOR_REPLACEMENTS.items():
            content = content.replace(old_color, new_color)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # DBA services directory
    services_dir = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec\safety-installs\services")
    
    if not services_dir.exists():
        print(f"Directory not found: {services_dir}")
        return
    
    fixed_files = []
    skipped_files = []
    
    # Process all HTML files in the services directory
    for html_file in services_dir.glob("*.html"):
        if fix_colors_in_file(html_file):
            fixed_files.append(html_file.name)
            print(f"✓ Fixed colors in: {html_file.name}")
        else:
            skipped_files.append(html_file.name)
    
    # Also process index.html files in subdirectories
    for subdir in services_dir.iterdir():
        if subdir.is_dir():
            index_file = subdir / "index.html"
            if index_file.exists():
                if fix_colors_in_file(index_file):
                    fixed_files.append(f"{subdir.name}/index.html")
                    print(f"✓ Fixed colors in: {subdir.name}/index.html")
                else:
                    skipped_files.append(f"{subdir.name}/index.html")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Color Scheme Fix Summary:")
    print(f"{'='*50}")
    print(f"Files fixed: {len(fixed_files)}")
    print(f"Files unchanged: {len(skipped_files)}")
    
    if fixed_files:
        print(f"\nFixed files:")
        for f in sorted(fixed_files):
            print(f"  - {f}")

if __name__ == "__main__":
    main()
