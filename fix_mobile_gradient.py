import os
import re

def fix_mobile_gradient_issue(file_path):
    """Fix the gradient transition issue on mobile devices"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find and replace the problematic gradient CSS
        # The issue is likely with the ::before pseudo-element and transform conflicts
        
        # OLD problematic CSS (replace this):
        old_css_pattern = r'''.service-card::before \{
\s*content: '';\s*
\s*position: absolute;\s*
\s*top: 0;\s*
\s*left: -100%;\s*
\s*width: 100%;\s*
\s*height: 100%;\s*
\s*background: linear-gradient\(135deg, var\(--navy\), var\(--teal\)\);\s*
\s*transition: left 0\.6s ease;\s*
\s*z-index: 1;\s*
\s*\}
        
        \.service-card:hover::before \{ left: 0; \}'''
        
        # NEW optimized CSS for mobile:
        new_css = '''.service-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--navy), var(--teal));
    transition: left 0.6s ease;
    z-index: 1;
    border-radius: 20px;
}

.service-card:hover::before,
.service-card.mobile-active::before { 
    left: 0; 
}'''
        
        # Also fix the mobile touch interactions
        mobile_fix_js = '''
        // Mobile touch optimization for service cards
        if (window.matchMedia("(hover: none)").matches) {
            const serviceCards = document.querySelectorAll('.service-card');
            
            serviceCards.forEach(card => {
                card.addEventListener('touchstart', function(e) {
                    // Remove active class from all other cards
                    serviceCards.forEach(otherCard => {
                        if (otherCard !== this) {
                            otherCard.classList.remove('mobile-active');
                        }
                    });
                    
                    // Toggle this card
                    this.classList.toggle('mobile-active');
                    
                    // Prevent default to avoid scrolling issues
                    e.preventDefault();
                });
                
                // Close card when tapping outside
                document.addEventListener('touchstart', function(e) {
                    if (!e.target.closest('.service-card')) {
                        serviceCards.forEach(card => {
                            card.classList.remove('mobile-active');
                        });
                    }
                });
            });
        }'''
        
        # Apply the CSS fix
        if '.service-card::before' in content:
            # Replace the specific problematic CSS
            content = re.sub(
                r'\.service-card::before\s*\{[^}]+\}',
                '.service-card::before {\n    content: \'\';\n    position: absolute;\n    top: 0;\n    left: -100%;\n    width: 100%;\n    height: 100%;\n    background: linear-gradient(135deg, var(--navy), var(--teal));\n    transition: left 0.6s ease;\n    z-index: 1;\n    border-radius: 20px;\n}',
                content
            )
            
            # Fix the hover state
            content = re.sub(
                r'\.service-card:hover::before\s*\{[^}]+\}',
                '.service-card:hover::before,\n.service-card.mobile-active::before { \n    left: 0; \n}',
                content
            )
            
            print(f"UPDATED: Fixed gradient CSS in {os.path.basename(file_path)}")
        
        # Add mobile JavaScript if not already present
        if 'window.matchMedia("(hover: none)").matches' not in content:
            # Find the closing </script> tag and insert before it
            script_pattern = r'(</script>)'
            content = re.sub(script_pattern, mobile_fix_js + r'\n\1', content, count=1)
            print(f"ADDED: Mobile touch JavaScript to {os.path.basename(file_path)}")
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True
        
    except Exception as e:
        print(f"ERROR processing {file_path}: {str(e)}")
        return False

def main():
    print("Fixing Mobile Gradient Transition Issues")
    print("=" * 60)
    
    # Files that likely have the service card CSS
    files_to_fix = [
        "services.html",
        "index.html"
    ]
    
    # Also check service pages that might have the same CSS
    services_dir = "services"
    service_files = [os.path.join(services_dir, f) for f in os.listdir(services_dir) 
                    if f.endswith('.html') and not f.endswith('.backup')]
    
    files_to_fix.extend(service_files[:5])  # Check first 5 service pages
    
    updated_count = 0
    error_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            success = fix_mobile_gradient_issue(file_path)
            if success:
                updated_count += 1
            else:
                error_count += 1
        else:
            print(f"SKIPPED: {file_path} not found")
    
    print("-" * 60)
    print("RESULTS:")
    print(f"  Successfully updated: {updated_count} files")
    print(f"  Errors: {error_count} files")
    
    if updated_count > 0:
        print(f"\nSUCCESS: Fixed mobile gradient issues!")
        print("The service cards should now work smoothly on mobile devices")
        print("\nTo deploy these fixes live, run:")
        print("git add -u")
        print('git commit -m "fix: Optimize service card gradient transitions for mobile"')
        print("git push origin main")
    else:
        print("\nNo files needed updates")

if __name__ == "__main__":
    main()