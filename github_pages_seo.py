#!/usr/bin/env python3
"""
GitHub Pages SEO Optimization Script
Adjusts SEO fixes for GitHub Pages compatibility
"""

import os
import re
from pathlib import Path
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GitHubPagesSEO:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.changes_log = []
        
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

    def add_github_pages_security_headers(self, content: str, file_path: Path) -> str:
        """Add security headers using meta tags for GitHub Pages"""
        # Check if security headers are already present
        security_headers = [
            'http-equiv="Content-Security-Policy"',
            'http-equiv="X-Content-Type-Options"',
            'http-equiv="X-Frame-Options"',
            'http-equiv="Referrer-Policy"'
        ]
        
        has_headers = any(header in content for header in security_headers)
        
        if not has_headers:
            # Add security headers as meta tags
            head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
            if head_match:
                insert_pos = head_match.end()
                security_meta = '''
<!-- GitHub Pages Security Headers -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self' https:; img-src 'self' data: https:; script-src 'self' 'unsafe-inline' https:; style-src 'self' 'unsafe-inline' https:; font-src 'self' https:;">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
'''
                content = content[:insert_pos] + security_meta + content[insert_pos:]
                self.changes_log.append(f"Added GitHub Pages security headers to {file_path.name}")
        
        return content

    def fix_github_pages_canonicals(self, content: str, file_path: Path) -> str:
        """Fix canonical URLs for GitHub Pages"""
        # Update canonical URLs to use the correct domain
        canonical_pattern = r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\'][^>]*>'
        
        def update_canonical(match):
            current_url = match.group(1)
            # Ensure it uses the correct domain
            if not current_url.startswith('https://wattsatpcontractor.com'):
                if current_url.startswith('/'):
                    new_url = f'https://wattsatpcontractor.com{current_url}'
                else:
                    new_url = f'https://wattsatpcontractor.com/{current_url}'
                
                new_tag = match.group(0).replace(current_url, new_url)
                self.changes_log.append(f"Updated canonical URL in {file_path.name}: {current_url} -> {new_url}")
                return new_tag
            return match.group(0)
        
        content = re.sub(canonical_pattern, update_canonical, content, flags=re.IGNORECASE)
        return content

    def add_github_pages_optimization(self, content: str, file_path: Path) -> str:
        """Add GitHub Pages specific optimizations"""
        # Add GitHub Pages specific meta tags
        head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
        if head_match:
            insert_pos = head_match.end()
            
            # Check if GitHub Pages optimization is already present
            if 'github-pages' not in content.lower():
                github_meta = '''
<!-- GitHub Pages Optimization -->
<meta name="generator" content="GitHub Pages">
<meta name="theme-color" content="#3498db">
<link rel="dns-prefetch" href="//fonts.googleapis.com">
<link rel="dns-prefetch" href="//cdnjs.cloudflare.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
'''
                content = content[:insert_pos] + github_meta + content[insert_pos:]
                self.changes_log.append(f"Added GitHub Pages optimization to {file_path.name}")
        
        return content

    def update_jekyll_config(self) -> None:
        """Update Jekyll config for GitHub Pages"""
        config_path = self.base_dir / "_config.yml"
        content = self.read_file(config_path)
        
        if content:
            # Add GitHub Pages specific settings
            if 'plugins:' not in content:
                jekyll_config = '''

# GitHub Pages plugins
plugins:
  - jekyll-sitemap
  - jekyll-feed

# GitHub Pages settings
markdown: kramdown
highlighter: rouge
kramdown:
  input: GFM
  syntax_highlighter: rouge

# SEO settings
twitter:
  username: wattsatpcontractor
  card: summary

social:
  name: Watts Safety Installs
  links:
    - https://wattsatpcontractor.com

# GitHub Pages specific
github: [metadata]
'''
                content += jekyll_config
                self.write_file(config_path, content)
                self.changes_log.append("Updated _config.yml for GitHub Pages")

    def create_github_pages_workflow(self) -> None:
        """Create GitHub Actions workflow for SEO validation"""
        workflows_dir = self.base_dir / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = '''name: SEO Validation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  seo-validation:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install requests beautifulsoup4 lxml
    
    - name: Run SEO validation
      run: |
        python -c "
import requests
from bs4 import BeautifulSoup
import os

def validate_seo():
    print('Running SEO validation for GitHub Pages...')
    
    # Check critical files
    critical_files = ['index.html', 'about.html', 'contact.html']
    for file in critical_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Check for title
                title = soup.find('title')
                if title:
                    print(f'✓ {file}: Title found - {title.get_text()[:50]}...')
                else:
                    print(f'✗ {file}: Missing title')
                
                # Check for meta description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    print(f'✓ {file}: Meta description found')
                else:
                    print(f'✗ {file}: Missing meta description')
                
                # Check for canonical
                canonical = soup.find('link', attrs={'rel': 'canonical'})
                if canonical:
                    print(f'✓ {file}: Canonical found - {canonical.get(\"href\", \"\")[:50]}...')
                else:
                    print(f'✗ {file}: Missing canonical')
    
    validate_seo()
"
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: .
'''
        
        workflow_path = workflows_dir / "seo-validation.yml"
        self.write_file(workflow_path, workflow_content)
        self.changes_log.append("Created GitHub Actions workflow for SEO validation")

    def process_html_file(self, file_path: Path) -> None:
        """Process a single HTML file for GitHub Pages optimization"""
        logger.info(f"Processing: {file_path}")
        
        content = self.read_file(file_path)
        if not content:
            return
        
        # Apply GitHub Pages specific fixes
        content = self.add_github_pages_security_headers(content, file_path)
        content = self.fix_github_pages_canonicals(content, file_path)
        content = self.add_github_pages_optimization(content, file_path)
        
        # Write updated content
        self.write_file(file_path, content)

    def run(self) -> None:
        """Run the GitHub Pages SEO optimization"""
        logger.info("Starting GitHub Pages SEO optimization...")
        
        # Find all HTML files
        html_files = list(self.base_dir.glob("*.html"))
        
        # Process each HTML file
        for html_file in html_files:
            if html_file.is_file() and html_file.name not in ['404.html']:
                try:
                    self.process_html_file(html_file)
                except Exception as e:
                    logger.error(f"Error processing {html_file}: {e}")
        
        # Update Jekyll config
        self.update_jekyll_config()
        
        # Create GitHub Actions workflow
        self.create_github_pages_workflow()
        
        # Generate report
        self.generate_report()
        
        logger.info("GitHub Pages SEO optimization completed!")

    def generate_report(self) -> None:
        """Generate a report of all changes made"""
        report_path = self.base_dir / "github_pages_seo_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# GitHub Pages SEO Optimization Report\n\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Changes Made for GitHub Pages\n\n")
            for change in self.changes_log:
                f.write(f"- {change}\n")
            
            f.write("\n## GitHub Pages Specific Optimizations\n\n")
            f.write("- Added security headers as meta tags (GitHub Pages compatible)\n")
            f.write("- Updated canonical URLs for correct domain\n")
            f.write("- Added performance optimizations (DNS prefetch, preconnect)\n")
            f.write("- Updated Jekyll configuration for GitHub Pages\n")
            f.write("- Created GitHub Actions workflow for SEO validation\n")
            
            f.write("\n## Next Steps\n\n")
            f.write("1. Commit and push changes to GitHub\n")
            f.write("2. Enable GitHub Pages in repository settings\n")
            f.write("3. Monitor GitHub Actions workflow for SEO validation\n")
            f.write("4. Test the live site for proper SEO implementation\n")
        
        logger.info(f"Report generated: {report_path}")

if __name__ == "__main__":
    import datetime
    
    # Run the GitHub Pages SEO optimization
    base_dir = r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec"
    optimizer = GitHubPagesSEO(base_dir)
    optimizer.run()
