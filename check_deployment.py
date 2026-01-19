#!/usr/bin/env python3
"""
Check Deployment Status
Verify if the accessibility page fix is deployed
"""

import requests
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_deployment():
    """Check if the accessibility page is properly deployed"""
    
    urls_to_check = [
        "https://wattsatpcontractor.com/services/accessibility-safety-solutions/",
        "https://wattsatpcontractor.com/services/accessibility-safety-solutions/index.html"
    ]
    
    for url in urls_to_check:
        try:
            logger.info(f"Checking: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # Check if page has body content
                if "<body>" in content and "</body>" in content:
                    logger.info(f"✅ {url} - Page has body content")
                    
                    # Check for specific elements
                    if "Accessibility Safety Solutions" in content:
                        logger.info(f"✅ {url} - Has correct title")
                    else:
                        logger.warning(f"⚠️ {url} - Missing title")
                        
                    if "WATTS" in content:
                        logger.info(f"✅ {url} - Has navigation")
                    else:
                        logger.warning(f"⚠️ {url} - Missing navigation")
                        
                else:
                    logger.error(f"❌ {url} - Missing body content")
                    
            else:
                logger.error(f"❌ {url} - HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error checking {url}: {e}")

if __name__ == "__main__":
    check_deployment()
