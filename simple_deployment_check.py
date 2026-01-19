#!/usr/bin/env python3
"""
Simple Deployment Check
Check if the accessibility page is properly deployed
"""

import urllib.request
import urllib.error
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_page_content():
    """Check if the page has the expected content"""
    
    url = "https://wattsatpcontractor.com/services/accessibility-safety-solutions/"
    
    try:
        logger.info(f"Checking: {url}")
        
        # Create request with user agent
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                content = response.read().decode('utf-8')
                
                logger.info(f"Response status: {response.status}")
                logger.info(f"Content length: {len(content)} characters")
                
                # Check for key indicators
                checks = {
                    "Has DOCTYPE": "<!DOCTYPE html>" in content,
                    "Has HTML tag": "<html" in content,
                    "Has HEAD": "<head>" in content,
                    "Has BODY": "<body>" in content,
                    "Has closing BODY": "</body>" in content,
                    "Has closing HTML": "</html>" in content,
                    "Has navigation": "WATTS" in content,
                    "Has title": "Accessibility Safety Solutions" in content,
                    "Has hero section": "hero" in content,
                    "Has footer": "footer" in content
                }
                
                logger.info("Content checks:")
                for check, result in checks.items():
                    status = "✅" if result else "❌"
                    logger.info(f"  {status} {check}")
                
                # Look for specific broken indicators
                if "</head></html>" in content:
                    logger.error("❌ PAGE ENDS WITH </head></html> - NO BODY CONTENT!")
                    return False
                elif not checks["Has BODY"]:
                    logger.error("❌ NO BODY TAG FOUND!")
                    return False
                elif not checks["Has navigation"]:
                    logger.error("❌ NO NAVIGATION FOUND!")
                    return False
                else:
                    logger.info("✅ PAGE APPEARS TO BE FIXED!")
                    return True
            else:
                logger.error(f"❌ HTTP {response.status}")
                return False
                
    except urllib.error.URLError as e:
        logger.error(f"❌ Network error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def check_local_file():
    """Verify the local file is correct"""
    
    local_file = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec\services\accessibility-safety-solutions\index.html")
    
    if local_file.exists():
        content = local_file.read_text(encoding='utf-8', errors='ignore')
        
        logger.info(f"Local file size: {len(content)} characters")
        
        if "</head></html>" in content:
            logger.error("❌ LOCAL FILE STILL BROKEN!")
            return False
        elif "<body>" in content and "</body>" in content:
            logger.info("✅ LOCAL FILE IS FIXED")
            return True
        else:
            logger.error("❌ LOCAL FILE HAS ISSUES")
            return False
    else:
        logger.error("❌ LOCAL FILE NOT FOUND")
        return False

if __name__ == "__main__":
    logger.info("=== DEPLOYMENT VERIFICATION ===")
    
    # Check local file first
    logger.info("Checking local file...")
    local_ok = check_local_file()
    
    # Check deployed page
    logger.info("\nChecking deployed page...")
    deployed_ok = check_page_content()
    
    logger.info("\n=== SUMMARY ===")
    logger.info(f"Local file: {'✅ FIXED' if local_ok else '❌ BROKEN'}")
    logger.info(f"Deployed page: {'✅ FIXED' if deployed_ok else '❌ BROKEN'}")
    
    if local_ok and not deployed_ok:
        logger.info("\n🔍 DIAGNOSIS: Local file is fixed but deployment hasn't updated yet")
        logger.info("💡 SOLUTION: Wait for GitHub Pages to deploy (5-30 minutes)")
    elif not local_ok:
        logger.info("\n🔍 DIAGNOSIS: Local file is still broken")
        logger.info("💡 SOLUTION: Fix the local file first")
    elif deployed_ok:
        logger.info("\n🎉 SUCCESS: Page is fixed and deployed!")
    else:
        logger.info("\n❌ UNKNOWN ISSUE: Both local and deployed have problems")
