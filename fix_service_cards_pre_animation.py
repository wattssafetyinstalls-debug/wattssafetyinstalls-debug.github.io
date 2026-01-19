#!/usr/bin/env python3
<arg_value>Fix Service Cards Pre-Animation Background
Remove white background from service cards initial state, show navy/teal gradient from start
"""

import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_service_cards_pre_animation():
    """Remove white background from service cards initial state"""
    
    services_page = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec\services.html")
    
    if not services_page.exists():
        logger.error("Services page not found")
        return
    
    content = services_page.read_text(encoding='utf-8', errors='ignore')
    original_content = content
    
    # Remove white background from service cards initial state
    old_service_card = '''        .service-card {
            min-width: 100%;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,196,180,0.1);
            display: flex;
            flex-direction: column;
        }'''
    
    new_service_card = '''        .service-card {
            min-width: 100%;
            background: linear-gradient(135deg, var(--navy), var(--teal));
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,196,180,0.1);
            display: flex;
            flex-direction: column;
        }'''
    
    content = content.replace(old_service_card, new_service_card)
    
    # Update text colors to work with dark gradient background
    old_title_color = '''        .service-title { 
            font-family: 'Playfair Display', serif; 
            font-size: 2rem; 
            color: var(--navy); 
            margin-bottom: 15px; 
            line-height: 1.2;
        }
        
        .service-card:hover .service-title { color: white; }'''
    
    new_title_color = '''        .service-title { 
            font-family: 'Playfair Display', serif; 
            font-size: 2rem; 
            color: white; 
            margin-bottom: 15px; 
            line-height: 1.2;
        }
        
        .service-card:hover .service-title { color: white; }'''
    
    content = content.replace(old_title_color, new_title_color)
    
    # Update description color
    old_description_color = '''        .service-description { 
            color: var(--gray); 
            margin-bottom: 25px; 
            font-size: 1.1rem; 
            line-height: 1.6;
            flex-grow: 1;
        }
        
        .service-card:hover .service-description { color: rgba(255,255,255,0.95); }'''
    
    new_description_color = '''        .service-description { 
            color: rgba(255,255,255,0.9); 
            margin-bottom: 25px; 
            font-size: 1.1rem; 
            line-height: 1.6;
            flex-grow: 1;
        }
        
        .service-card:hover .service-description { color: rgba(255,255,255,0.95); }'''
    
    content = content.replace(old_description_color, new_description_color)
    
    # Write the updated page
    services_page.write_text(content, encoding='utf-8')
    
    if content != original_content:
        logger.info("Removed white background from service cards pre-animation")
    else:
        logger.info("No changes needed - service cards already have correct background")

if __name__ == "__main__":
    fix_service_cards_pre_animation()
