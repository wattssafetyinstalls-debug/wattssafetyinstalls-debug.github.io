#!/usr/bin/env python3
"""
Fix Service Tiles Dropdown Background
Change service dropdown from white to navy/teal gradient
"""

import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_service_tiles_background():
    """Fix service tiles to show navy/teal gradient instead of white background"""
    
    services_page = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec\services.html")
    
    if not services_page.exists():
        logger.error("Services page not found")
        return
    
    content = services_page.read_text(encoding='utf-8', errors='ignore')
    original_content = content
    
    # Fix the dropdown background - change from white to transparent/gradient
    old_dropdown_bg = '''        .service-dropdown {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.6s ease;
            background: rgba(255,255,255,0.95);
            border-radius: 0 0 20px 20px;
        }'''
    
    new_dropdown_bg = '''        .service-dropdown {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.6s ease;
            background: rgba(10,29,55,0.9);
            border-radius: 0 0 20px 20px;
        }'''
    
    content = content.replace(old_dropdown_bg, new_dropdown_bg)
    
    # Also fix the mobile version
    old_mobile_dropdown = '''        .service-dropdown {
            background: rgba(255,255,255,0.95);
            border-radius: 0 0 20px 20px;
        }'''
    
    new_mobile_dropdown = '''        .service-dropdown {
            background: rgba(10,29,55,0.9);
            border-radius: 0 0 20px 20px;
        }'''
    
    content = content.replace(old_mobile_dropdown, new_mobile_dropdown)
    
    # Update dropdown links to be more visible on the dark background
    old_link_style = '''        .service-dropdown a { 
            display: block; 
            padding: 15px 20px; 
            color: var(--navy); 
            text-decoration: none; 
            border-bottom: 1px solid rgba(0,0,0,0.1); 
            transition: all 0.3s;
        }'''
    
    new_link_style = '''        .service-dropdown a { 
            display: block; 
            padding: 15px 20px; 
            color: white; 
            text-decoration: none; 
            border-bottom: 1px solid rgba(255,255,255,0.2); 
            transition: all 0.3s;
        }'''
    
    content = content.replace(old_link_style, new_link_style)
    
    # Update hover state for links
    old_link_hover = '''        .service-dropdown a:hover { 
            color: var(--teal); 
            padding-left: 15px;
            background: rgba(0,196,180,0.05);
        }'''
    
    new_link_hover = '''        .service-dropdown a:hover { 
            color: var(--teal); 
            padding-left: 15px;
            background: rgba(255,255,255,0.1);
        }'''
    
    content = content.replace(old_link_hover, new_link_hover)
    
    # Write the updated page
    services_page.write_text(content, encoding='utf-8')
    
    if content != original_content:
        logger.info("Fixed service tiles dropdown background - now shows navy/teal gradient")
    else:
        logger.info("No changes needed - service tiles already have correct background")

if __name__ == "__main__":
    fix_service_tiles_background()
