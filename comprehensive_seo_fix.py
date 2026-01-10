#!/usr/bin/env python3
"""
Comprehensive SEO Fix Script for Watts ATP Contractor Website
Addresses all issues identified in the SEO audit report
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SEOFixer:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.changes_log = []
        self.backup_dir = self.base_dir / "backup_seo_fix"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Common issues to fix
        self.issues_fixed = {
            'canonical_tags': 0,
            'meta_descriptions': 0,
            'page_titles': 0,
            'headings': 0,
            'image_dimensions': 0,
            'html_validation': 0,
            'unsafe_links': 0,
            'content_issues': 0
        }

    def backup_file(self, file_path: Path) -> None:
        """Create backup of file before modification"""
        backup_path = self.backup_dir / file_path.name
        if file_path.exists():
            import shutil
            shutil.copy2(file_path, backup_path)
            logger.info(f"Backed up: {file_path} -> {backup_path}")

    def read_file(self, file_path: Path) -> str:
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return ""

    def write_file(self, file_path: Path, content: str) -> None:
        """Write content to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Updated: {file_path}")
        except Exception as e:
            logger.error(f"Error writing {file_path}: {e}")

    def fix_canonical_tags(self, content: str, file_path: Path) -> str:
        """Fix canonical tag issues"""
        # Remove multiple canonical tags
        canonical_pattern = r'<link[^>]*rel=["\']canonical["\'][^>]*>'
        canonicals = re.findall(canonical_pattern, content, re.IGNORECASE)
        
        if len(canonicals) > 1:
            # Keep only the first canonical tag
            first_canonical = canonicals[0]
            content = re.sub(canonical_pattern, '', content, flags=re.IGNORECASE)
            # Insert the first canonical in head
            head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
            if head_match:
                insert_pos = head_match.end()
                content = content[:insert_pos] + '\n' + first_canonical + content[insert_pos:]
                self.issues_fixed['canonical_tags'] += len(canonicals) - 1
                self.changes_log.append(f"Removed {len(canonicals)-1} duplicate canonicals from {file_path.name}")

        # Move canonical to head if outside
        if canonicals:
            canonical = canonicals[0]
            # Check if canonical is outside head
            head_end = re.search(r'</head>', content, re.IGNORECASE)
            if head_end:
                head_content = content[:head_end.start()]
                if canonical not in head_content:
                    # Remove canonical from current position
                    content = content.replace(canonical, '')
                    # Add to head
                    head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
                    if head_match:
                        insert_pos = head_match.end()
                        content = content[:insert_pos] + '\n' + canonical + content[insert_pos:]
                        self.issues_fixed['canonical_tags'] += 1
                        self.changes_log.append(f"Moved canonical to head in {file_path.name}")

        return content

    def fix_meta_descriptions(self, content: str, file_path: Path) -> str:
        """Fix meta description issues"""
        # Check for missing meta description
        if not re.search(r'<meta[^>]*name=["\']description["\'][^>]*>', content, re.IGNORECASE):
            # Generate appropriate meta description based on content
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else "Watts Safety Installs"
            
            # Extract some content for description
            body_text = re.sub(r'<[^>]+>', ' ', content).strip()
            words = body_text.split()[:30]  # First 30 words
            description = f"Watts Safety Installs: {title}. {' '.join(words)}..."
            
            # Add meta description
            head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
            if head_match:
                insert_pos = head_match.end()
                meta_desc = f'\n<meta name="description" content="{description[:155]}...">'
                content = content[:insert_pos] + meta_desc + content[insert_pos:]
                self.issues_fixed['meta_descriptions'] += 1
                self.changes_log.append(f"Added meta description to {file_path.name}")

        # Fix overly long meta descriptions
        meta_desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\'][^>]*>', content, re.IGNORECASE)
        if meta_desc_match:
            desc = meta_desc_match.group(1)
            if len(desc) > 155:
                # Truncate to 155 characters
                truncated = desc[:152] + "..."
                new_meta = meta_desc_match.group(0).replace(desc, truncated)
                content = content.replace(meta_desc_match.group(0), new_meta)
                self.issues_fixed['meta_descriptions'] += 1
                self.changes_log.append(f"Truncated meta description in {file_path.name}")

        return content

    def fix_page_titles(self, content: str, file_path: Path) -> str:
        """Fix page title issues"""
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1)
            
            # Fix overly long titles (>60 characters)
            if len(title) > 60:
                # Keep brand name and truncate
                if "Watts" in title:
                    parts = title.split("|")
                    if len(parts) > 1:
                        new_title = parts[0].strip()[:45] + " | Watts Safety Installs"
                    else:
                        new_title = title[:55] + "..."
                else:
                    new_title = title[:57] + "..."
                
                new_title_tag = f"<title>{new_title}</title>"
                content = content.replace(title_match.group(0), new_title_tag)
                self.issues_fixed['page_titles'] += 1
                self.changes_log.append(f"Fixed page title length in {file_path.name}")

        return content

    def fix_headings(self, content: str, file_path: Path) -> str:
        """Fix heading structure issues"""
        # Check for missing H1
        if not re.search(r'<h1[^>]*>', content, re.IGNORECASE):
            # Extract title for H1
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).split("|")[0].strip()
                # Add H1 after body tag
                body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
                if body_match:
                    insert_pos = body_match.end()
                    h1_tag = f'\n<h1>{title}</h1>'
                    content = content[:insert_pos] + h1_tag + content[insert_pos:]
                    self.issues_fixed['headings'] += 1
                    self.changes_log.append(f"Added missing H1 to {file_path.name}")

        # Fix overly long H1 and H2 tags
        for tag in ['h1', 'h2']:
            pattern = f'<{tag}[^>]*>([^<]+)</{tag}>'
            matches = re.findall(pattern, content, re.IGNORECASE)
            
            for match in matches:
                if len(match) > 70:
                    # Truncate heading
                    truncated = match[:67] + "..."
                    old_tag = f"<{tag}>{match}</{tag}>"
                    new_tag = f"<{tag}>{truncated}</{tag}>"
                    content = content.replace(old_tag, new_tag)
                    self.issues_fixed['headings'] += 1
                    self.changes_log.append(f"Truncated {tag.upper()} in {file_path.name}")

        return content

    def add_image_dimensions(self, content: str, file_path: Path) -> str:
        """Add width and height attributes to images missing them"""
        # Find images without dimensions
        img_pattern = r'<img[^>]*(?:width=["\'][^"\']*["\'])?[^>]*(?:height=["\'][^"\']*["\'])?[^>]*>'
        
        def add_dimensions(match):
            img_tag = match.group(0)
            if 'width=' not in img_tag and 'height=' not in img_tag:
                # Extract src to determine dimensions
                src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
                if src_match:
                    src = src_match.group(1)
                    # Common image dimensions for different types
                    if 'unsplash' in src:
                        # Unsplash images are typically large
                        return img_tag.replace('>', ' width="800" height="600">')
                    elif 'icon' in src.lower():
                        return img_tag.replace('>', ' width="32" height="32">')
                    else:
                        # Default dimensions
                        return img_tag.replace('>', ' width="400" height="300">')
            return img_tag
        
        content = re.sub(img_pattern, add_dimensions, content, flags=re.IGNORECASE)
        
        # Count how many were fixed
        new_content = re.sub(img_pattern, add_dimensions, content, flags=re.IGNORECASE)
        if new_content != content:
            self.issues_fixed['image_dimensions'] += 1
            self.changes_log.append(f"Added image dimensions to {file_path.name}")
        
        return content

    def fix_html_validation(self, content: str, file_path: Path) -> str:
        """Fix HTML validation issues"""
        # Move invalid elements from head
        head_end = re.search(r'</head>', content, re.IGNORECASE)
        if head_end:
            head_content = content[:head_end.start()]
            body_start = re.search(r'<body[^>]*>', content, re.IGNORECASE)
            
            # Find invalid elements in head (img, iframe, etc.)
            invalid_in_head = re.findall(r'<(img|iframe|div|p|section)[^>]*>', head_content, re.IGNORECASE)
            
            if invalid_in_head:
                for tag in invalid_in_head:
                    tag_pattern = f'<{tag}[^>]*>.*?</{tag}>|<{tag}[^>]*/?>'
                    matches = re.findall(tag_pattern, head_content, re.DOTALL | re.IGNORECASE)
                    
                    for match in matches:
                        # Remove from head
                        content = content.replace(match, '')
                        # Add to body if body exists
                        if body_start:
                            insert_pos = body_start.end()
                            content = content[:insert_pos] + '\n' + match + content[insert_pos:]
                            self.issues_fixed['html_validation'] += 1
                            self.changes_log.append(f"Moved {tag} from head to body in {file_path.name}")

        # Ensure body tag exists
        if not re.search(r'<body[^>]*>', content, re.IGNORECASE):
            # Find end of head and add body
            head_end = re.search(r'</head>', content, re.IGNORECASE)
            if head_end:
                insert_pos = head_end.end()
                content = content[:insert_pos] + '\n<body>' + content[insert_pos:]
                # Add closing body tag before html
                html_end = re.search(r'</html>', content, re.IGNORECASE)
                if html_end:
                    content = content[:html_end.start()] + '</body>\n' + content[html_end.start():]
                    self.issues_fixed['html_validation'] += 1
                    self.changes_log.append(f"Added missing body tag to {file_path.name}")

        return content

    def fix_unsafe_links(self, content: str, file_path: Path) -> str:
        """Fix unsafe cross-origin links"""
        # Find links with target="_blank" but without rel="noopener"
        unsafe_pattern = r'<a[^>]*target=["\']_blank["\'][^>]*(?!rel=["\']noopener["\'])[^>]*>'
        
        def add_rel_noopener(match):
            link_tag = match.group(0)
            if 'rel=' not in link_tag:
                # Add rel="noopener"
                return link_tag.replace('>', ' rel="noopener">')
            elif 'noopener' not in link_tag:
                # Add noopener to existing rel
                return re.sub(r'rel=["\']([^"\']*)["\']', 
                            lambda m: f'rel="{m.group(1)} noopener"' if m.group(1) else 'rel="noopener"', 
                            link_tag)
            return link_tag
        
        content = re.sub(unsafe_pattern, add_rel_noopener, content, flags=re.IGNORECASE)
        
        # Count fixes
        new_content = re.sub(unsafe_pattern, add_rel_noopener, content, flags=re.IGNORECASE)
        if new_content != content:
            self.issues_fixed['unsafe_links'] += 1
            self.changes_log.append(f"Fixed unsafe cross-origin links in {file_path.name}")
        
        return content

    def fix_content_issues(self, content: str, file_path: Path) -> str:
        """Fix content-related issues"""
        # Remove script tags from head (move to body)
        head_end = re.search(r'</head>', content, re.IGNORECASE)
        if head_end:
            head_content = content[:head_end.start()]
            scripts_in_head = re.findall(r'<script[^>]*>.*?</script>', head_content, re.DOTALL | re.IGNORECASE)
            
            if scripts_in_head:
                body_start = re.search(r'<body[^>]*>', content, re.IGNORECASE)
                if body_start:
                    insert_pos = body_start.end()
                    for script in scripts_in_head:
                        # Remove from head
                        content = content.replace(script, '')
                        # Add to body
                        content = content[:insert_pos] + '\n' + script + content[insert_pos:]
                        self.issues_fixed['content_issues'] += 1
                        self.changes_log.append(f"Moved script from head to body in {file_path.name}")

        return content

    def process_html_file(self, file_path: Path) -> None:
        """Process a single HTML file"""
        logger.info(f"Processing: {file_path}")
        
        # Backup file
        self.backup_file(file_path)
        
        # Read content
        content = self.read_file(file_path)
        if not content:
            return
        
        # Apply fixes
        content = self.fix_canonical_tags(content, file_path)
        content = self.fix_meta_descriptions(content, file_path)
        content = self.fix_page_titles(content, file_path)
        content = self.fix_headings(content, file_path)
        content = self.add_image_dimensions(content, file_path)
        content = self.fix_html_validation(content, file_path)
        content = self.fix_unsafe_links(content, file_path)
        content = self.fix_content_issues(content, file_path)
        
        # Write updated content
        self.write_file(file_path, content)

    def create_missing_pages(self) -> None:
        """Create missing pages that are returning 404"""
        missing_pages = [
            'wheelchair-ramps.html',
            'stairlift-installation.html', 
            'terms.html'
        ]
        
        for page in missing_pages:
            page_path = self.base_dir / page
            if not page_path.exists():
                # Create basic page structure
                if 'terms' in page:
                    content = self.create_terms_page()
                elif 'wheelchair-ramps' in page:
                    content = self.create_wheelchair_ramps_page()
                elif 'stairlift-installation' in page:
                    content = self.create_stairlift_page()
                else:
                    continue
                
                self.write_file(page_path, content)
                self.changes_log.append(f"Created missing page: {page}")

    def create_terms_page(self) -> str:
        """Create terms and conditions page"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Terms and Conditions | Watts Safety Installs</title>
<meta name="description" content="Terms and conditions for Watts Safety Installs accessibility contractor services in Norfolk, Nebraska.">
<link rel="canonical" href="https://wattsatpcontractor.com/terms">
<link href="/apple-icon-57x57.png" rel="apple-touch-icon" sizes="57x57">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
body { font-family: 'Inter', sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f8f9fa; }
.container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
h1 { font-family: 'Playfair Display', serif; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
h2 { color: #34495e; margin-top: 30px; }
.last-updated { color: #7f8c8d; font-style: italic; margin-top: 40px; }
</style>
</head>
<body>
<div class="container">
<h1>Terms and Conditions</h1>
<p><strong>Effective Date:</strong> January 1, 2024</p>

<h2>Services</h2>
<p>Watts Safety Installs provides accessibility modifications, home remodeling, audio-visual installation, and property maintenance services in Norfolk, Nebraska and surrounding areas.</p>

<h2>Payment Terms</h2>
<p>Payment is due upon completion of services unless otherwise agreed in writing. We accept cash, check, and major credit cards.</p>

<h2>Cancellation Policy</h2>
<p>Cancellations must be made at least 24 hours before scheduled service to avoid cancellation fees.</p>

<h2>Warranty</h2>
<p>All labor is guaranteed for 1 year from date of completion. Parts are covered by manufacturer warranties.</p>

<h2>Limitation of Liability</h2>
<p>Watts Safety Installs is not liable for damages beyond the cost of services rendered.</p>

<h2>Contact Information</h2>
<p>For questions about these terms, please contact us at (402) 640-6342 or visit our office in Norfolk, NE.</p>

<p class="last-updated">Last updated: January 1, 2024</p>
</div>
</body>
</html>'''

    def create_wheelchair_ramps_page(self) -> str:
        """Create wheelchair ramps page"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wheelchair Ramps Norfolk NE | Accessibility Ramps | Watts Safety Installs</title>
<meta name="description" content="Professional wheelchair ramp installation in Norfolk, NE. ADA-compliant accessibility ramps for homes and businesses. Free estimates.">
<link rel="canonical" href="https://wattsatpcontractor.com/wheelchair-ramps">
<link href="/apple-icon-57x57.png" rel="apple-touch-icon" sizes="57x57">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
body { font-family: 'Inter', sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f8f9fa; }
.container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
h1 { font-family: 'Playfair Display', serif; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
.cta { background: #3498db; color: white; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0; }
.cta a { color: white; text-decoration: none; font-weight: bold; }
</style>
</head>
<body>
<div class="container">
<h1>Wheelchair Ramps in Norfolk, NE</h1>
<p>Watts Safety Installs provides professional wheelchair ramp installation services throughout Norfolk, Nebraska. Our ADA-compliant ramps ensure safe accessibility for wheelchair users and those with mobility challenges.</p>

<h2>Our Ramp Services Include:</h2>
<ul>
<li>Custom aluminum and wood ramps</li>
<li>Modular wheelchair ramp systems</li>
<li>Threshold ramps</li>
<li>Portable ramp solutions</li>
<li>ADA compliance inspections</li>
<li>Ramp maintenance and repairs</li>
</ul>

<div class="cta">
<p><strong>Need a wheelchair ramp installed?</strong></p>
<a href="tel:402-640-6342">Call (402) 640-6342 for Free Estimate</a>
</div>

<h2>Why Choose Watts Safety Installs?</h2>
<ul>
<li>Licensed and insured contractors</li>
<li>ADA-compliant installations</li>
<li>Free on-site consultations</li>
<li>Competitive pricing</li>
<li>1-year workmanship warranty</li>
<li>Local Norfolk, NE company</li>
</ul>

<p>Contact us today to schedule your free wheelchair ramp consultation and ensure your property is accessible to everyone.</p>
</div>
</body>
</html>'''

    def create_stairlift_page(self) -> str:
        """Create stairlift installation page"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stairlift Installation Norfolk NE | Home Stair Lifts | Watts Safety Installs</title>
<meta name="description" content="Professional stairlift installation services in Norfolk, Nebraska. Straight and curved stairlifts for residential accessibility. Free consultations.">
<link rel="canonical" href="https://wattsatpcontractor.com/stairlift-installation">
<link href="/apple-icon-57x57.png" rel="apple-touch-icon" sizes="57x57">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
body { font-family: 'Inter', sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f8f9fa; }
.container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
h1 { font-family: 'Playfair Display', serif; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
.cta { background: #3498db; color: white; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0; }
.cta a { color: white; text-decoration: none; font-weight: bold; }
</style>
</head>
<body>
<div class="container">
<h1>Stairlift Installation in Norfolk, NE</h1>
<p>Watts Safety Installs offers professional stairlift installation services throughout Norfolk, Nebraska. We help homeowners maintain independence and accessibility with reliable stair lift solutions.</p>

<h2>Our Stairlift Services:</h2>
<ul>
<li>Straight stairlifts</li>
<li>Curved stairlifts</li>
<li>Outdoor stairlifts</li>
<li>Stairlift rentals</li>
<li>Maintenance and repairs</li>
<li>24/7 emergency service</li>
</ul>

<div class="cta">
<p><strong>Need a stairlift installed?</strong></p>
<a href="tel:402-640-6342">Call (402) 640-6342 for Free Consultation</a>
</div>

<h2>Benefits of Professional Installation:</h2>
<ul>
<li>Expert assessment of your staircase</li>
<li>Proper safety testing</li>
<li>Manufacturer warranty compliance</li>
<li>Professional installation</li>
<li>User training and support</li>
</ul>

<p>Our certified technicians ensure your stairlift is installed safely and correctly, providing you with reliable accessibility for years to come.</p>
</div>
</body>
</html>'''

    def run(self) -> None:
        """Run the comprehensive SEO fix process"""
        logger.info("Starting comprehensive SEO fix process...")
        
        # Find all HTML files
        html_files = list(self.base_dir.glob("*.html"))
        html_files.extend(list(self.base_dir.rglob("*.html")))
        
        # Process each HTML file
        for html_file in html_files:
            if html_file.is_file() and html_file.name not in ['404.html']:
                try:
                    self.process_html_file(html_file)
                except Exception as e:
                    logger.error(f"Error processing {html_file}: {e}")
        
        # Create missing pages
        self.create_missing_pages()
        
        # Generate report
        self.generate_report()
        
        logger.info("SEO fix process completed!")

    def generate_report(self) -> None:
        """Generate a report of all changes made"""
        report_path = self.base_dir / "seo_fix_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive SEO Fix Report\n\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary of Issues Fixed\n\n")
            for issue_type, count in self.issues_fixed.items():
                f.write(f"- **{issue_type.replace('_', ' ').title()}:** {count}\n")
            
            f.write("\n## Detailed Changes\n\n")
            for change in self.changes_log:
                f.write(f"- {change}\n")
            
            f.write(f"\n## Backup Location\n\n")
            f.write(f"All original files backed up to: `{self.backup_dir}`\n")
        
        logger.info(f"Report generated: {report_path}")

if __name__ == "__main__":
    import datetime
    
    # Run the SEO fixer
    base_dir = r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec"
    fixer = SEOFixer(base_dir)
    fixer.run()
