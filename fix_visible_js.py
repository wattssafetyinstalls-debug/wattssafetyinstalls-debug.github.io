import os
import re

def fix_javascript_wrapping(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove any visible (unwrapped) JS code
    pattern = r'(?s)// Mobile auto-animation after 3 seconds.*?console\.log$$   \'Mobile animation completed\'   $$;\s*\}\);\s*'
    content = re.sub(pattern, '', content)
    
    # Reinsert properly wrapped JS before </body>
    mobile_js = '''
<script>
    // Mobile auto-animation after 3 seconds
    document.addEventListener('DOMContentLoaded', function() {
        if (window.innerWidth <= 768) {
            setTimeout(function() {
                const mainTile = document.getElementById('mainServiceTile');
                const categories = document.querySelectorAll('.service-category');
                
                if (mainTile) {
                    mainTile.classList.add('mobile-animated');
                    console.log('Mobile animation applied to main tile');
                }
                categories.forEach(category => {
                    category.classList.add('mobile-animated');
                });
                console.log('Mobile animation completed');
            }, 3000);
        }
    });
</script>
'''
    
    if '</body>' in content:
        content = content.replace('</body>', mobile_js + '\n</body>')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Apply to all service pages
if os.path.exists('services'):
    count = 0
    for service_file in os.listdir('services'):
        if service_file.endswith('.html') and not service_file.endswith('.backup'):
            file_path = os.path.join('services', service_file)
            if fix_javascript_wrapping(file_path):
                count += 1
                print(f"Fixed JavaScript in: {service_file}")
    print(f"Total service pages fixed: {count}")