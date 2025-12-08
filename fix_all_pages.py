import os
import re
from pathlib import Path

def fix_all_pages():
    base_url = "https://wattsatpcontractor.com"
    
    # Walk through all HTML files
    for file_path in Path('.').rglob('*.html'):
        # Skip 404.html and backup directories
        if '404.html' in str(file_path) or 'backup' in str(file_path):
            continue
            
        print(f"Processing: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Fix canonical URL
        if file_path.name == 'index.html':
            # Directory index
            folder = str(file_path.parent).replace('\\', '/')
            if folder == '.':
                correct_url = f"{base_url}/"
            else:
                correct_url = f"{base_url}/{folder}"
        else:
            # Regular file
            folder = str(file_path.parent).replace('\\', '/')
            file_stem = file_path.stem
            if folder == '.':
                correct_url = f"{base_url}/{file_stem}"
            else:
                correct_url = f"{base_url}/{folder}/{file_stem}"
        
        # Clean up URL
        correct_url = re.sub(r'(?<!:)/+', '/', correct_url)
        correct_url = correct_url.rstrip('/')
        
        # Update or add canonical tag
        canonical_pattern = r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>'
        canonical_tag = f'<link rel="canonical" href="{correct_url}" />'
        
        if re.search(canonical_pattern, content):
            content = re.sub(canonical_pattern, canonical_tag, content)
        else:
            # Insert before </head>
            if '</head>' in content:
                content = content.replace('</head>', f'{canonical_tag}\n</head>')
        
        # 2. Fix internal links to services
        # Pattern to find service links
        service_patterns = [
            (r'href="/services/([^"/]+)\.html"', r'href="/services/\1"'),
            (r'href="/services/([^"/]+)/"', r'href="/services/\1"'),
            (r'href="/service-pages/([^"/]+)\.html"', r'href="/services/\1"'),
            (r'href="/([^"/]+)\.html"', r'href="/\1"')
        ]
        
        for pattern, replacement in service_patterns:
            content = re.sub(pattern, replacement, content)
        
        # 3. Ensure consistent formatting
        # Remove multiple newlines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Update file if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated: {file_path}")

def generate_sitemap():
    """Generate sitemap.xml for all pages"""
    base_url = "https://wattsatpcontractor.com"
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    # Add homepage
    sitemap_content += f'''  <url>
    <loc>{base_url}/</loc>
    <priority>1.0</priority>
    <changefreq>weekly</changefreq>
  </url>
'''
    
    # Add service pages
    services_dir = Path('./services')
    if services_dir.exists():
        for service in services_dir.iterdir():
            if service.is_dir():
                service_url = f"{base_url}/services/{service.name}"
                sitemap_content += f'''  <url>
    <loc>{service_url}</loc>
    <priority>0.8</priority>
    <changefreq>monthly</changefreq>
  </url>
'''
    
    sitemap_content += '</urlset>'
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("Generated sitemap.xml")

if __name__ == "__main__":
    print("Starting comprehensive fix for 60+ pages...")
    fix_all_pages()
    generate_sitemap()
    print("Fix complete!")