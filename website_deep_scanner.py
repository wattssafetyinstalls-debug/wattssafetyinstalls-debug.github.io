#!/usr/bin/env python3
"""
Comprehensive Website Deep Scanner
Analyzes service pages for consistency, duplicate files, and structural issues
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
import logging
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebsiteDeepScanner:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.issues = {
            'inconsistent_carousels': [],
            'missing_animations': [],
            'duplicate_files': [],
            'broken_links': [],
            'css_js_inconsistencies': [],
            'mobile_issues': [],
            'qa_carousel_issues': [],
            'structural_problems': [],
            'redirect_issues': []
        }
        self.service_pages = []
        self.file_hashes = {}
        self.page_analysis = {}

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate file hash for duplicate detection"""
        try:
            import hashlib
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""

    def find_duplicate_files(self) -> None:
        """Find duplicate files that might cause conflicts"""
        logger.info("Scanning for duplicate files...")
        
        all_files = list(self.base_dir.rglob("*"))
        file_groups = defaultdict(list)
        
        for file_path in all_files:
            if file_path.is_file() and file_path.suffix in ['.html', '.css', '.js']:
                # Group by filename first
                file_groups[file_path.name].append(file_path)
        
        # Check for duplicate filenames
        for filename, paths in file_groups.items():
            if len(paths) > 1:
                # Check if files are actually different
                hashes = {}
                for path in paths:
                    file_hash = self.get_file_hash(path)
                    if file_hash:
                        hashes[file_hash] = hashes.get(file_hash, []) + [path]
                
                # Report duplicates
                for hash_val, duplicate_paths in hashes.items():
                    if len(duplicate_paths) > 1:
                        self.issues['duplicate_files'].append({
                            'filename': filename,
                            'paths': [str(p) for p in duplicate_paths],
                            'hash': hash_val,
                            'type': 'identical_duplicates' if len(duplicate_paths) > 1 else 'same_name_different_content'
                        })

    def find_service_pages(self) -> None:
        """Identify all service pages"""
        logger.info("Finding service pages...")
        
        # Find service pages in various locations
        service_patterns = [
            self.base_dir.glob("services*.html"),
            self.base_dir.glob("services/*.html"),
            self.base_dir.glob("services/**/*.html"),
            self.base_dir.rglob("*services*.html"),
            self.base_dir.rglob("ada-*.html"),
            self.base_dir.rglob("*-installation.html"),
            self.base_dir.rglob("*-repair.html"),
            self.base_dir.rglob("*-maintenance.html")
        ]
        
        service_files = set()
        for pattern in service_patterns:
            for file_path in pattern:
                if file_path.is_file() and file_path.name not in ['404.html', 'sitemap.html']:
                    service_files.add(file_path)
        
        self.service_pages = list(service_files)
        logger.info(f"Found {len(self.service_pages)} service pages")

    def analyze_page_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze individual page structure"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except:
            return {}
        
        analysis = {
            'has_carousel': bool(re.search(r'carousel|slider|swiper', content, re.IGNORECASE)),
            'has_qa_section': bool(re.search(r'qa|question.*answer|faq', content, re.IGNORECASE)),
            'has_gradient_animation': bool(re.search(r'gradient|animation|transition', content, re.IGNORECASE)),
            'carousel_type': None,
            'qa_carousel_type': None,
            'css_files': re.findall(r'<link[^>]*href=["\']([^"\']*\.css)["\']', content, re.IGNORECASE),
            'js_files': re.findall(r'<script[^>]*src=["\']([^"\']*\.js)["\']', content, re.IGNORECASE),
            'inline_css': re.findall(r'<style[^>]*>([^<]+)</style>', content, re.DOTALL | re.IGNORECASE),
            'inline_js': re.findall(r'<script[^>]*>([^<]+)</script>', content, re.DOTALL | re.IGNORECASE),
            'has_mobile_optimization': bool(re.search(r'@media|mobile|responsive', content, re.IGNORECASE)),
            'has_touch_events': bool(re.search(r'touchstart|touchend|touchmove', content, re.IGNORECASE)),
            'gradient_classes': re.findall(r'class=["\'][^"\']*gradient[^"\']*["\']', content, re.IGNORECASE),
            'animation_classes': re.findall(r'class=["\'][^"\']*animate[^"\']*["\']', content, re.IGNORECASE),
            'carousel_elements': re.findall(r'class=["\'][^"\']*carousel[^"\']*["\']', content, re.IGNORECASE),
            'qa_elements': re.findall(r'class=["\'][^"\']*qa[^"\']*["\']', content, re.IGNORECASE)
        }
        
        # Determine carousel type
        if 'swiper' in content.lower():
            analysis['carousel_type'] = 'swiper'
        elif 'bootstrap' in content.lower():
            analysis['carousel_type'] = 'bootstrap'
        elif 'slick' in content.lower():
            analysis['carousel_type'] = 'slick'
        elif analysis['has_carousel']:
            analysis['carousel_type'] = 'custom'
        
        # Determine Q&A carousel type
        if 'swiper' in content.lower() and 'qa' in content.lower():
            analysis['qa_carousel_type'] = 'swiper'
        elif 'accordion' in content.lower():
            analysis['qa_carousel_type'] = 'accordion'
        elif analysis['has_qa_section']:
            analysis['qa_carousel_type'] = 'simple_list'
        
        return analysis

    def analyze_service_consistency(self) -> None:
        """Analyze consistency across service pages"""
        logger.info("Analyzing service page consistency...")
        
        # Analyze each service page
        for page_path in self.service_pages:
            analysis = self.analyze_page_structure(page_path)
            self.page_analysis[str(page_path)] = analysis
        
        # Find inconsistencies
        carousel_types = [a.get('carousel_type') for a in self.page_analysis.values() if a.get('carousel_type')]
        qa_types = [a.get('qa_carousel_type') for a in self.page_analysis.values() if a.get('qa_carousel_type')]
        
        # Check for inconsistent carousel implementations
        carousel_counter = Counter(carousel_types)
        if len(carousel_counter) > 1:
            self.issues['inconsistent_carousels'].append({
                'issue': 'Multiple carousel types found',
                'distribution': dict(carousel_counter),
                'pages_by_type': defaultdict(list)
            })
            
            for page_path, analysis in self.page_analysis.items():
                if analysis.get('carousel_type'):
                    self.issues['inconsistent_carousels'][0]['pages_by_type'][analysis['carousel_type']].append(page_path)
        
        # Check for inconsistent Q&A implementations
        qa_counter = Counter(qa_types)
        if len(qa_counter) > 1:
            self.issues['qa_carousel_issues'].append({
                'issue': 'Multiple Q&A types found',
                'distribution': dict(qa_counter),
                'pages_by_type': defaultdict(list)
            })
            
            for page_path, analysis in self.page_analysis.items():
                if analysis.get('qa_carousel_type'):
                    self.issues['qa_carousel_issues'][0]['pages_by_type'][analysis['qa_carousel_type']].append(page_path)
        
        # Check for missing animations
        for page_path, analysis in self.page_analysis.items():
            if not analysis.get('has_gradient_animation'):
                self.issues['missing_animations'].append({
                    'page': page_path,
                    'issue': 'Missing gradient animations'
                })
            
            if not analysis.get('has_carousel') and analysis.get('has_qa_section'):
                self.issues['qa_carousel_issues'].append({
                    'page': page_path,
                    'issue': 'Q&A section without carousel implementation'
                })

    def analyze_css_js_consistency(self) -> None:
        """Analyze CSS and JavaScript consistency"""
        logger.info("Analyzing CSS/JS consistency...")
        
        # Collect all CSS and JS files used
        css_files = Counter()
        js_files = Counter()
        
        for analysis in self.page_analysis.values():
            css_files.update(analysis.get('css_files', []))
            js_files.update(analysis.get('js_files', []))
        
        # Find inconsistencies
        common_css = [file for file, count in css_files.items() if count > len(self.service_pages) * 0.8]
        rare_css = [file for file, count in css_files.items() if count < len(self.service_pages) * 0.2]
        
        common_js = [file for file, count in js_files.items() if count > len(self.service_pages) * 0.8]
        rare_js = [file for file, count in js_files.items() if count < len(self.service_pages) * 0.2]
        
        if rare_css:
            self.issues['css_js_inconsistencies'].append({
                'type': 'inconsistent_css',
                'rare_files': rare_css,
                'common_files': common_css
            })
        
        if rare_js:
            self.issues['css_js_inconsistencies'].append({
                'type': 'inconsistent_js',
                'rare_files': rare_js,
                'common_files': common_js
            })

    def find_broken_links_and_redirects(self) -> None:
        """Find broken links and redirect issues"""
        logger.info("Scanning for broken links and redirect issues...")
        
        # Check netlify.toml for redirects
        netlify_config = self.base_dir / "netlify.toml"
        if netlify_config.exists():
            content = netlify_config.read_text(encoding='utf-8')
            redirects = re.findall(r'from = "([^"]+)"\s+to = "([^"]+)"', content)
            
            for from_url, to_url in redirects:
                # Check if target files exist
                target_file = self.base_dir / to_url.lstrip('/')
                if not target_file.exists() and not to_url.startswith('http'):
                    self.issues['redirect_issues'].append({
                        'type': 'broken_redirect',
                        'from': from_url,
                        'to': to_url,
                        'target_missing': str(target_file)
                    })
        
        # Check for common broken link patterns in HTML files
        for page_path in self.service_pages:
            try:
                content = page_path.read_text(encoding='utf-8', errors='ignore')
                
                # Find internal links
                internal_links = re.findall(r'href=["\']([^"\']+)["\']', content)
                
                for link in internal_links:
                    if link.startswith('/') or not link.startswith('http'):
                        # Convert to file path
                        if link.startswith('/'):
                            link_file = self.base_dir / link.lstrip('/')
                        else:
                            link_file = page_path.parent / link
                        
                        # Handle .html extensions
                        if not link_file.suffix:
                            link_file = link_file.with_suffix('.html')
                        
                        if not link_file.exists():
                            self.issues['broken_links'].append({
                                'source_page': str(page_path),
                                'broken_link': link,
                                'target_file': str(link_file)
                            })
                            
            except Exception as e:
                logger.error(f"Error analyzing {page_path}: {e}")

    def analyze_mobile_responsiveness(self) -> None:
        """Analyze mobile responsiveness issues"""
        logger.info("Analyzing mobile responsiveness...")
        
        for page_path in self.service_pages:
            analysis = self.page_analysis.get(str(page_path), {})
            
            issues = []
            
            if not analysis.get('has_mobile_optimization'):
                issues.append('Missing mobile media queries')
            
            if not analysis.get('has_touch_events'):
                issues.append('Missing touch event handlers')
            
            # Check for common mobile issues
            try:
                content = page_path.read_text(encoding='utf-8', errors='ignore')
                
                # Check for viewport meta tag
                if not re.search(r'viewport.*width=device-width', content, re.IGNORECASE):
                    issues.append('Missing viewport meta tag')
                
                # Check for fixed widths that break mobile
                if re.search(r'width:\s*\d+px', content):
                    issues.append('Fixed pixel widths detected (may break mobile)')
                
                # Check for large images without responsive sizing
                if re.search(r'<img[^>]*(?!width=.*%)(?!height=.*%)(width="\d+")[^>]*>', content):
                    issues.append('Images with fixed pixel widths')
                
            except Exception as e:
                logger.error(f"Error analyzing mobile for {page_path}: {e}")
            
            if issues:
                self.issues['mobile_issues'].append({
                    'page': str(page_path),
                    'issues': issues
                })

    def generate_comprehensive_report(self) -> None:
        """Generate comprehensive report of all findings"""
        logger.info("Generating comprehensive report...")
        
        report_path = self.base_dir / "website_deep_scan_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Website Deep Scan Report\n\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## Summary\n\n")
            f.write(f"- **Service Pages Analyzed:** {len(self.service_pages)}\n")
            f.write(f"- **Duplicate Files Found:** {len(self.issues['duplicate_files'])}\n")
            f.write(f"- **Inconsistent Carousels:** {len(self.issues['inconsistent_carousels'])}\n")
            f.write(f"- **Q&A Carousel Issues:** {len(self.issues['qa_carousel_issues'])}\n")
            f.write(f"- **Missing Animations:** {len(self.issues['missing_animations'])}\n")
            f.write(f"- **Broken Links:** {len(self.issues['broken_links'])}\n")
            f.write(f"- **Redirect Issues:** {len(self.issues['redirect_issues'])}\n")
            f.write(f"- **Mobile Issues:** {len(self.issues['mobile_issues'])}\n")
            f.write(f"- **CSS/JS Inconsistencies:** {len(self.issues['css_js_inconsistencies'])}\n\n")
            
            # Duplicate Files Section
            if self.issues['duplicate_files']:
                f.write("## 🚨 Duplicate Files (Potential Conflicts)\n\n")
                for duplicate in self.issues['duplicate_files']:
                    f.write(f"### {duplicate['filename']}\n")
                    f.write(f"**Type:** {duplicate['type']}\n")
                    f.write("**Locations:**\n")
                    for path in duplicate['paths']:
                        f.write(f"- `{path}`\n")
                    f.write("\n")
            
            # Inconsistent Carousels
            if self.issues['inconsistent_carousels']:
                f.write("## 🎠 Inconsistent Carousel Implementations\n\n")
                for issue in self.issues['inconsistent_carousels']:
                    f.write(f"### {issue['issue']}\n")
                    f.write("**Distribution:**\n")
                    for carousel_type, count in issue['distribution'].items():
                        f.write(f"- {carousel_type}: {count} pages\n")
                    f.write("\n**Pages by Type:**\n")
                    for carousel_type, pages in issue['pages_by_type'].items():
                        f.write(f"\n**{carousel_type}:**\n")
                        for page in pages:
                            f.write(f"- {page}\n")
                    f.write("\n")
            
            # Q&A Carousel Issues
            if self.issues['qa_carousel_issues']:
                f.write("## ❓ Q&A Carousel Issues\n\n")
                for issue in self.issues['qa_carousel_issues']:
                    if 'issue' in issue:
                        f.write(f"### {issue['page']}\n")
                        f.write(f"**Issue:** {issue['issue']}\n\n")
                    else:
                        f.write(f"### {issue['issue']}\n")
                        f.write("**Distribution:**\n")
                        for qa_type, count in issue['distribution'].items():
                            f.write(f"- {qa_type}: {count} pages\n")
                        f.write("\n**Pages by Type:**\n")
                        for qa_type, pages in issue['pages_by_type'].items():
                            f.write(f"\n**{qa_type}:**\n")
                            for page in pages:
                                f.write(f"- {page}\n")
                    f.write("\n")
            
            # Missing Animations
            if self.issues['missing_animations']:
                f.write("## 🎨 Missing Gradient Animations\n\n")
                for missing in self.issues['missing_animations']:
                    f.write(f"- **{missing['page']}:** {missing['issue']}\n")
                f.write("\n")
            
            # Broken Links
            if self.issues['broken_links']:
                f.write("## 🔗 Broken Internal Links\n\n")
                for link in self.issues['broken_links'][:20]:  # Limit to first 20
                    f.write(f"### {link['source_page']}\n")
                    f.write(f"**Broken Link:** `{link['broken_link']}`\n")
                    f.write(f"**Target:** `{link['target_file']}`\n\n")
                if len(self.issues['broken_links']) > 20:
                    f.write(f"... and {len(self.issues['broken_links']) - 20} more broken links\n\n")
            
            # Redirect Issues
            if self.issues['redirect_issues']:
                f.write("## 🔄 Redirect Issues\n\n")
                for redirect in self.issues['redirect_issues']:
                    f.write(f"### {redirect['from']} → {redirect['to']}\n")
                    f.write(f"**Issue:** {redirect['type']}\n")
                    f.write(f"**Missing Target:** `{redirect['target_missing']}`\n\n")
            
            # Mobile Issues
            if self.issues['mobile_issues']:
                f.write("## 📱 Mobile Responsiveness Issues\n\n")
                for mobile in self.issues['mobile_issues']:
                    f.write(f"### {mobile['page']}\n")
                    for issue in mobile['issues']:
                        f.write(f"- {issue}\n")
                    f.write("\n")
            
            # CSS/JS Inconsistencies
            if self.issues['css_js_inconsistencies']:
                f.write("## 🎭 CSS/JS Inconsistencies\n\n")
                for inconsistency in self.issues['css_js_inconsistencies']:
                    f.write(f"### {inconsistency['type'].replace('_', ' ').title()}\n")
                    if inconsistency.get('rare_files'):
                        f.write("**Rarely Used Files:**\n")
                        for file in inconsistency['rare_files']:
                            f.write(f"- `{file}` (used on few pages)\n")
                    if inconsistency.get('common_files'):
                        f.write("**Commonly Used Files:**\n")
                        for file in inconsistency['common_files']:
                            f.write(f"- `{file}`\n")
                    f.write("\n")
            
            # Recommendations
            f.write("## 🔧 Recommendations\n\n")
            f.write("### High Priority\n")
            f.write("1. **Fix duplicate files** - Remove or consolidate duplicates to prevent conflicts\n")
            f.write("2. **Standardize carousel implementation** - Choose one carousel type and apply consistently\n")
            f.write("3. **Fix Q&A carousel consistency** - Ensure all service pages have the same Q&A interaction\n")
            f.write("4. **Add missing gradient animations** - Implement consistent animations across all pages\n")
            f.write("5. **Fix broken links** - Update or remove broken internal links\n")
            
            f.write("\n### Medium Priority\n")
            f.write("1. **Improve mobile responsiveness** - Add touch events and proper media queries\n")
            f.write("2. **Standardize CSS/JS** - Use consistent stylesheets and scripts\n")
            f.write("3. **Fix redirect issues** - Ensure all redirects point to existing pages\n")
            
            f.write("\n### Low Priority\n")
            f.write("1. **Optimize image loading** - Add responsive images and proper dimensions\n")
            f.write("2. **Improve page load performance** - Minimize and bundle CSS/JS files\n")
        
        logger.info(f"Comprehensive report generated: {report_path}")
        return report_path

    def run(self) -> str:
        """Run the complete deep scan"""
        logger.info("Starting comprehensive website deep scan...")
        
        # Run all analyses
        self.find_duplicate_files()
        self.find_service_pages()
        self.analyze_service_consistency()
        self.analyze_css_js_consistency()
        self.find_broken_links_and_redirects()
        self.analyze_mobile_responsiveness()
        
        # Generate report
        report_path = self.generate_comprehensive_report()
        
        logger.info("Comprehensive deep scan completed!")
        return report_path

if __name__ == "__main__":
    import datetime
    from collections import defaultdict, Counter
    
    # Run the deep scan
    base_dir = r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec"
    scanner = WebsiteDeepScanner(base_dir)
    report_path = scanner.run()
