#!/usr/bin/env python3
"""
Fix Q&A carousel colors to match brand schemes
- DBA pages: black/red/cream
- ATP pages: navy/teal/gold
"""

import os
import re
from pathlib import Path

def fix_qa_carousel_dba(filepath):
    """Fix Q&A carousel colors for DBA pages"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if this has Q&A carousel
        if 'qa-section' not in content and 'qa-carousel' not in content:
            return False
            
        # Fix Q&A specific color references
        qa_replacements = {
            # Active card gradient
            'linear-gradient(135deg, var(--navy), var(--teal))': 'linear-gradient(135deg, var(--black), var(--red))',
            'linear-gradient(135deg, var(--black), var(--red))': 'linear-gradient(135deg, var(--black), var(--red))',
            
            # Q&A specific color fixes
            '.qa-section h2 {\n            font-family: \'Playfair Display\', serif;\n            font-size: 3rem;\n            color: var(--navy);':
            '.qa-section h2 {\n            font-family: \'Playfair Display\', serif;\n            font-size: 3rem;\n            color: var(--black);',
            
            '.qa-question { \n            font-family: \'Playfair Display\', serif; \n            font-size: 2rem; \n            color: var(--navy);':
            '.qa-question { \n            font-family: \'Playfair Display\', serif; \n            font-size: 2rem; \n            color: var(--black);',
            
            '.qa-icon { \n            font-size: 3rem; \n            color: var(--teal);':
            '.qa-icon { \n            font-size: 3rem; \n            color: var(--red);',
            
            '.consultation-note { \n            font-style: italic; \n            font-weight: 600; \n            color: var(--teal);':
            '.consultation-note { \n            font-style: italic; \n            font-weight: 600; \n            color: var(--red);',
            
            '.qa-card.active .qa-icon { \n            color: var(--gold) !important;':
            '.qa-card.active .qa-icon { \n            color: var(--cream) !important;',
            
            # Dot colors
            'background: var(--teal);': 'background: var(--red);',
            'background: var(--navy);': 'background: var(--black);',
        }
        
        for old_text, new_text in qa_replacements.items():
            content = content.replace(old_text, new_text)
        
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
    dba_services_dir = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec\safety-installs\services")
    
    # ATP services directory  
    atp_services_dir = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec\services")
    
    fixed_files = []
    
    # Fix DBA service pages
    if dba_services_dir.exists():
        for html_file in dba_services_dir.glob("*.html"):
            if fix_qa_carousel_dba(html_file):
                fixed_files.append(f"DBA: {html_file.name}")
                print(f"✓ Fixed Q&A carousel in DBA: {html_file.name}")
        
        # Also process index.html files in subdirectories
        for subdir in dba_services_dir.iterdir():
            if subdir.is_dir():
                index_file = subdir / "index.html"
                if index_file.exists():
                    if fix_qa_carousel_dba(index_file):
                        fixed_files.append(f"DBA: {subdir.name}/index.html")
                        print(f"✓ Fixed Q&A carousel in DBA: {subdir.name}/index.html")
    
    # Check ATP pages to ensure they keep navy/teal/gold
    if atp_services_dir.exists():
        for html_file in atp_services_dir.glob("*.html"):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'qa-section' in content or 'qa-carousel' in content:
                # These should keep navy/teal/gold colors
                print(f"✓ ATP page has Q&A (keeping navy/teal/gold): {html_file.name}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Q&A Carousel Color Fix Summary:")
    print(f"{'='*50}")
    print(f"Files fixed: {len(fixed_files)}")
    
    if fixed_files:
        print(f"\nFixed files:")
        for f in sorted(fixed_files):
            print(f"  - {f}")

if __name__ == "__main__":
    main()
