#!/usr/bin/env python3
"""
Quick Fix for Remaining Issues
Fixes the tel link format and any remaining minor issues
"""

import os
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_tel_links(base_dir: str) -> None:
    """Fix tel link format to be more standard"""
    base_path = Path(base_dir)
    
    # Fix tel links - remove the + for better compatibility
    html_files = list(base_path.rglob("*.html"))
    
    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content
            
            # Fix tel links - remove the + for better compatibility
            content = re.sub(r'href="tel:\+14054106402"', 'href="tel:14054106402"', content)
            
            if content != original_content:
                html_file.write_text(content, encoding='utf-8')
                logger.info(f"Fixed tel links in: {html_file.name}")
                
        except Exception as e:
            logger.error(f"Error fixing {html_file}: {e}")

def fix_about_page(base_dir: str) -> None:
    """Ensure about page is optimized"""
    base_path = Path(base_dir)
    about_page = base_path / "about.html"
    
    if about_page.exists():
        content = about_page.read_text(encoding='utf-8', errors='ignore')
        
        # Check if optimizations are present
        if 'viewport' not in content.lower() or 'gradientShift' not in content:
            logger.info("Optimizing about page...")
            
            # Add viewport if missing
            if 'viewport' not in content.lower():
                head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
                if head_match:
                    insert_pos = head_match.end()
                    viewport_tag = '\n<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                    content = content[:insert_pos] + viewport_tag + content[insert_pos:]
            
            # Add gradient animations if missing
            if 'gradientShift' not in content:
                style_match = re.search(r'<style[^>]*>', content, re.IGNORECASE)
                if style_match:
                    insert_pos = style_match.end()
                    gradient_css = '''
/* Gradient Animations */
.service-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    animation: gradientShift 8s ease-in-out infinite;
    transition: all 0.3s ease;
}

@keyframes gradientShift {
    0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    25% { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    50% { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    75% { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
}
'''
                    content = content[:insert_pos] + gradient_css + content[insert_pos:]
            
            about_page.write_text(content, encoding='utf-8')
            logger.info("About page optimized")

if __name__ == "__main__":
    base_dir = r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec"
    
    logger.info("Applying final fixes...")
    fix_tel_links(base_dir)
    fix_about_page(base_dir)
    
    logger.info("Final fixes completed!")
