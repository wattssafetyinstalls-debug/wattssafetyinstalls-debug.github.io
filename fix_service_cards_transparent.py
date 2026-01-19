#!/usr/bin/env python3
<arg_value>Fix Service Cards - Remove White Background, Keep Text Visible
Make service cards transparent with navy/teal gradient animation while keeping text visible
"""

import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_service_cards_transparent():
    """Remove white background from service cards but keep text visible with gradient animation"""
    
    services_page = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec\services.html")
    
    if not services_page.exists():
        logger.error("Services page not found")
        return
    
    content = services_page.read_text(encoding='utf-8', errors='ignore')
    original_content = content
    
    # Make service cards transparent but keep the gradient animation
    old_service_card = '''        .service-card {
            min-width: 100%;
            background: white;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            position: relative;
            transition: transform 0.5s ease-in-out;
        }'''
    
    new_service_card = '''        .service-card {
            min-width: 100%;
            background: transparent;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            position: relative;
            transition: transform 0.5s ease-in-out;
        }'''
    
    content = content.replace(old_service_card, new_service_card)
    
    # Keep text colors as they were (navy/gray) for visibility
    # The gradient animation will provide the background
    
    # Make sure the gradient animation is visible behind the text
    old_before_pseudo = '''        .service-card::before {
            content: ''; 
            position: absolute; 
            top: 0; 
            left: -100%; 
            width: 100%; 
            height: 100%;
            background: linear-gradient(135deg, var(--navy), var(--teal));
            transition: left 0.6s ease;
            z-index: 1;
        }'''
    
    new_before_pseudo = '''        .service-card::before {
            content: ''; 
            position: absolute; 
            top: 0; 
            left: -100%; 
            width: 100%; 
            height: 100%;
            background: linear-gradient(135deg, var(--navy), var(--teal));
            transition: left 0.6s ease;
            z-index: 1;
        }'''
    
    content = content.replace(old_before_pseudo, new_before_pseudo)
    
    # Make sure the text stays above the gradient
    old_after_pseudo = '''        .service-card > * { position: relative; z-index: 2; }'''
    
    new_after_pseudo = '''        .service-card > * { 
            position: relative; 
            z-index: 2; 
            background: rgba(255,255,255,0.85);
            padding: 5px;
            border-radius: 5px;
        }'''
    
    content = content.replace(old_after_pseudo, new_after_pseudo)
    
    # Write the updated page
    services_page.write_text(content, encoding='utf-8')
    
    if content != original_content:
        logger.info("Made service cards transparent with visible text and gradient animation")
    else:
        logger.info("No changes needed - service cards already have correct styling")

if __name__ == "__main__":
    fix_service_cards_transparent()
