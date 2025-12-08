import os
import re

def fix_canonicals():
    base_url = "https://wattsatpcontractor.com"
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                # Skip 404.html and backups
                if '404' in file or 'backup' in root:
                    continue
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Determine correct canonical URL
                if file == 'index.html':
                    # Directory index page
                    if root == '.':
                        canonical = f"{base_url}/"
                    else:
                        folder = root.replace('\\', '/').replace('./', '/')
                        canonical = f"{base_url}{folder}"
                else:
                    # Regular HTML file
                    folder = root.replace('\\', '/').replace('./', '/')
                    file_no_ext = file.replace('.html', '')
                    canonical = f"{base_url}{folder}/{file_no_ext}"
                
                # Remove double slashes and ensure no trailing slash
                canonical = re.sub(r'(?<!:)/+', '/', canonical)
                canonical = canonical.rstrip('/')
                
                # Update canonical tag
                new_content = re.sub(
                    r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>',
                    f'<link rel="canonical" href="{canonical}" />',
                    content
                )
                
                # If no canonical tag exists, add one before </head>
                if '<link rel="canonical"' not in new_content:
                    new_content = new_content.replace('</head>', f'<link rel="canonical" href="{canonical}" />\n</head>')
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed canonical in {filepath} -> {canonical}")

fix_canonicals()