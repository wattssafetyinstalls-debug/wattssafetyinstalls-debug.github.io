import os
import re

def clean_and_add_js(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove all instances of the mobile JS code, including fragments and duplicates
    patterns = [
        r'(?s)<script>\s*// Mobile auto-animation after 3 seconds.*?console\.log\(\'Mobile animation completed\'\);\s*\}\);\s*</script>',
        r'(?s)// Mobile auto-animation after 3 seconds.*?console\.log\(\'Mobile animation completed\'\);\s*\}\);',
        r',3000\);\s*\}\);\s*',  # Specific fragment cleanup
        r'setTimeout\(function\(\)\s*\{.*?mobile-animated.*?\}\s*,\s*3000\);',  # Broader match for any setTimeout blocks
        r'\}\);\s*'  # Trailing fragments like }};)
    ]
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)
    
    # Reinsert single wrapped JS before </body>
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
            if clean_and_add_js(file_path):
                count += 1
                print(f"Cleaned and updated JS in: {service_file}")
    print(f"Total service pages cleaned: {count}")