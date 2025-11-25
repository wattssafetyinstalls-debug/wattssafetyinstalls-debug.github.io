import os
import re

def apply_upgrades(html_files):
    for file in html_files:
        with open(file, 'r+') as f:
            content = f.read()
            # Example upgrade: Add or update schema
            if '<script type="application/ld+json">' not in content:
                schema = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Watts Safety Installs",
  "url": "https://wattsatpcontractor.com"
}
</script>
'''
                content = content.replace('</head>', schema + '</head>')
            # Other upgrades, e.g., fix descriptions
            content = re.sub(r'<p class="service-description">(.*?)</p>', r'<p class="service-description">\1</p>', content, flags=re.DOTALL)
            f.seek(0)
            f.write(content)
            f.truncate()
    print("Upgrades applied to HTML files.")

# Usage example
html_files = ['index.html', 'services.html']  # Add your files
apply_upgrades(html_files)