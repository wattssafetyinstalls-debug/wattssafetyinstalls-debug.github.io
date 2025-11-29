import os

def add_hamburger_js(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'hamburgerToggle' in content:  # Check if already added
        print(f"Hamburger JS already in {file_path}")
        return False
    
    hamburger_js = '''
<script>
// Hamburger menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');  // Adjust selector if needed
    const navMenu = document.querySelector('.nav-menu');    // Adjust to your nav class/ID
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            console.log('Hamburger menu toggled');
        });
        // Optional: Add touchstart for better mobile support
        hamburger.addEventListener('touchstart', () => {
            navMenu.classList.toggle('active');
            console.log('Hamburger menu toggled via touch');
        });
    }
});
</script>
'''
    
    if '</body>' in content:
        content = content.replace('</body>', hamburger_js + '\n</body>')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Apply to all pages (main and services)
count = 0
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') and not file.endswith('.backup'):
            file_path = os.path.join(root, file)
            if add_hamburger_js(file_path):
                count += 1
                print(f"Added hamburger JS to: {file_path}")

print(f"Total pages updated: {count}")