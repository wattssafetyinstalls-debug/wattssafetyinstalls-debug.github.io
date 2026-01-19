#!/usr/bin/env python3
"""
Final Website Verification
Verifies all fixes are properly applied and website is optimized
"""

import os
import re
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalVerification:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.issues_found = []
        self.fixes_verified = []
        
    def verify_service_pages(self) -> Dict:
        """Verify service page structure and optimizations"""
        logger.info("Verifying service pages...")
        
        services_dir = self.base_dir / "services"
        service_pages = list(services_dir.rglob("*.html"))
        
        verification_results = {
            'total_pages': len(service_pages),
            'pages_with_viewport': 0,
            'pages_with_carousel': 0,
            'pages_with_animations': 0,
            'pages_mobile_optimized': 0,
            'broken_links_found': 0
        }
        
        for page in service_pages:
            try:
                content = page.read_text(encoding='utf-8', errors='ignore')
                
                # Check viewport meta tag
                if 'viewport' in content.lower():
                    verification_results['pages_with_viewport'] += 1
                else:
                    self.issues_found.append(f"Missing viewport: {page.name}")
                
                # Check carousel implementation
                if 'carousel' in content.lower() or 'qa-carousel' in content.lower():
                    verification_results['pages_with_carousel'] += 1
                else:
                    self.issues_found.append(f"Missing carousel: {page.name}")
                
                # Check gradient animations
                if 'gradientShift' in content or 'animation' in content.lower():
                    verification_results['pages_with_animations'] += 1
                else:
                    self.issues_found.append(f"Missing animations: {page.name}")
                
                # Check mobile optimization
                if ('@media' in content and '768px' in content) or 'touchstart' in content.lower():
                    verification_results['pages_mobile_optimized'] += 1
                else:
                    self.issues_found.append(f"Not mobile optimized: {page.name}")
                
                # Check for broken links
                broken_links = re.findall(r'href=["\']([^"\']+)["\']', content)
                for link in broken_links:
                    if link.startswith('tel:+') or link.startswith('mailto:'):
                        if '+' in link and link.startswith('tel:+'):
                            verification_results['broken_links_found'] += 1
                            self.issues_found.append(f"Malformed tel link in {page.name}: {link}")
                
            except Exception as e:
                self.issues_found.append(f"Error reading {page.name}: {e}")
        
        return verification_results
    
    def verify_main_pages(self) -> Dict:
        """Verify main website pages"""
        logger.info("Verifying main pages...")
        
        main_pages = ['index.html', 'about.html', 'contact.html', 'services.html']
        verification_results = {
            'pages_checked': 0,
            'pages_optimized': 0
        }
        
        for page_name in main_pages:
            page_path = self.base_dir / page_name
            if page_path.exists():
                verification_results['pages_checked'] += 1
                content = page_path.read_text(encoding='utf-8', errors='ignore')
                
                # Check for optimizations
                if ('viewport' in content.lower() and 
                    'gradientShift' in content and 
                    'carousel' in content.lower()):
                    verification_results['pages_optimized'] += 1
                    self.fixes_verified.append(f"Optimized: {page_name}")
                else:
                    self.issues_found.append(f"Main page not optimized: {page_name}")
        
        return verification_results
    
    def verify_redirects(self) -> Dict:
        """Verify redirects are properly configured"""
        logger.info("Verifying redirects...")
        
        netlify_config = self.base_dir / "netlify.toml"
        redirect_file = self.base_dir / "service_redirects.txt"
        
        verification_results = {
            'netlify_config_exists': netlify_config.exists(),
            'redirect_file_exists': redirect_file.exists(),
            'broken_redirects': 0
        }
        
        if netlify_config.exists():
            content = netlify_config.read_text(encoding='utf-8')
            # Check for broken redirects
            if 'testimonials.html' in content or 'test_mobile_fix.html' in content:
                verification_results['broken_redirects'] += 1
                self.issues_found.append("Broken redirects still exist in netlify.toml")
            else:
                self.fixes_verified.append("Redirects cleaned up in netlify.toml")
        
        if redirect_file.exists():
            self.fixes_verified.append("Service redirects file created")
        
        return verification_results
    
    def verify_css_js_consistency(self) -> Dict:
        """Verify CSS and JS consistency"""
        logger.info("Verifying CSS/JS consistency...")
        
        html_files = list(self.base_dir.rglob("*.html"))
        font_awesome_versions = set()
        
        for html_file in html_files:
            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                # Find Font Awesome versions
                fa_matches = re.findall(r'font-awesome/([^/]+)/', content)
                font_awesome_versions.update(fa_matches)
            except:
                continue
        
        verification_results = {
            'unique_font_awesome_versions': len(font_awesome_versions),
            'versions_found': list(font_awesome_versions)
        }
        
        if len(font_awesome_versions) <= 1:
            self.fixes_verified.append("Font Awesome versions consistent")
        else:
            self.issues_found.append(f"Inconsistent Font Awesome versions: {font_awesome_versions}")
        
        return verification_results
    
    def generate_final_report(self) -> None:
        """Generate final verification report"""
        logger.info("Generating final verification report...")
        
        # Run all verifications
        service_results = self.verify_service_pages()
        main_results = self.verify_main_pages()
        redirect_results = self.verify_redirects()
        css_js_results = self.verify_css_js_consistency()
        
        # Generate report
        report_path = self.base_dir / "final_verification_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Final Website Verification Report\n\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## ✅ VERIFICATION RESULTS\n\n")
            
            f.write("### Service Pages Optimization\n")
            f.write(f"- Total Service Pages: {service_results['total_pages']}\n")
            f.write(f"- Pages with Viewport Meta: {service_results['pages_with_viewport']}/{service_results['total_pages']}\n")
            f.write(f"- Pages with Carousels: {service_results['pages_with_carousel']}/{service_results['total_pages']}\n")
            f.write(f"- Pages with Animations: {service_results['pages_with_animations']}/{service_results['total_pages']}\n")
            f.write(f"- Mobile Optimized Pages: {service_results['pages_mobile_optimized']}/{service_results['total_pages']}\n")
            f.write(f"- Broken Links Found: {service_results['broken_links_found']}\n\n")
            
            f.write("### Main Pages Optimization\n")
            f.write(f"- Pages Checked: {main_results['pages_checked']}\n")
            f.write(f"- Pages Optimized: {main_results['pages_optimized']}/{main_results['pages_checked']}\n\n")
            
            f.write("### Redirects Configuration\n")
            f.write(f"- Netlify Config Exists: {redirect_results['netlify_config_exists']}\n")
            f.write(f"- Redirect File Exists: {redirect_results['redirect_file_exists']}\n")
            f.write(f"- Broken Redirects: {redirect_results['broken_redirects']}\n\n")
            
            f.write("### CSS/JS Consistency\n")
            f.write(f"- Font Awesome Versions: {css_js_results['unique_font_awesome_versions']}\n")
            f.write(f"- Versions Found: {', '.join(css_js_results['versions_found'])}\n\n")
            
            if self.fixes_verified:
                f.write("## ✅ FIXES VERIFIED\n\n")
                for fix in self.fixes_verified:
                    f.write(f"- {fix}\n")
                f.write("\n")
            
            if self.issues_found:
                f.write("## ⚠️ REMAINING ISSUES\n\n")
                for issue in self.issues_found[:20]:  # Limit to first 20 issues
                    f.write(f"- {issue}\n")
                if len(self.issues_found) > 20:
                    f.write(f"- ... and {len(self.issues_found) - 20} more issues\n")
                f.write("\n")
            
            f.write("## 📊 OVERALL STATUS\n\n")
            
            total_issues = len(self.issues_found)
            total_fixes = len(self.fixes_verified)
            
            if total_issues == 0:
                f.write("🎉 **EXCELLENT** - All issues resolved!\n")
            elif total_issues < 10:
                f.write("✅ **GOOD** - Minor issues remaining\n")
            elif total_issues < 50:
                f.write("⚠️ **FAIR** - Some issues need attention\n")
            else:
                f.write("❌ **NEEDS WORK** - Many issues remaining\n")
            
            f.write(f"\n- Issues Resolved: {total_fixes}\n")
            f.write(f"- Issues Remaining: {total_issues}\n")
            f.write(f"- Success Rate: {((total_fixes / (total_fixes + total_issues)) * 100):.1f}%\n")
            
            f.write("\n## 🚀 READY FOR DEPLOYMENT?\n\n")
            if total_issues == 0:
                f.write("✅ **YES** - Website is fully optimized and ready!\n")
            elif total_issues < 10:
                f.write("🟡 **MOSTLY** - Minor tweaks recommended before deployment\n")
            else:
                f.write("🔴 **NOT YET** - Additional work needed before deployment\n")
        
        logger.info(f"Final verification report generated: {report_path}")
        
        return {
            'total_issues': len(self.issues_found),
            'total_fixes': len(self.fixes_verified),
            'ready_for_deployment': len(self.issues_found) < 10
        }

if __name__ == "__main__":
    import datetime
    
    base_dir = r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec"
    verifier = FinalVerification(base_dir)
    results = verifier.generate_final_report()
    
    logger.info(f"Verification complete: {results['total_issues']} issues, {results['total_fixes']} fixes verified")
    logger.info(f"Ready for deployment: {'YES' if results['ready_for_deployment'] else 'NO'}")
