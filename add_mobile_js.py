import os

def add_mobile_js(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the mobile JS code is already present
    if 'setTimeout' in content and 'mobile-animated' in content:
        print(f"Mobile JS already in {file_path}")
        return False
    
    # The mobile JS code we want to add
    mobile_js = """
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
    """
    
    # Try to insert before the closing </body> tag
    if '</body>' in content:
        content = content.replace('</body>', mobile_js + '\n</body>')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added mobile JS to {file_path}")
        return True
    else:
        print(f"Could not find </body> in {file_path}")
        return False

# Process all service pages
if os.path.exists('services'):
    count = 0
    for service_file in os.listdir('services'):
        if service_file.endswith('.html') and not service_file.endswith('.backup'):
            file_path = os.path.join('services', service_file)
            if add_mobile_js(file_path):
                count += 1
    
    print(f"Total service pages updated with mobile JS: {count}")