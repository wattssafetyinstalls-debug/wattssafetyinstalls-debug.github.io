import os
import re

def update_state_references():
    """Update all state references from Massachusetts to Nebraska/Norfolk"""
    
    print("UPDATING STATE REFERENCES: Massachusetts to Nebraska/Norfolk")
    print("=" * 60)
    
    # Files to check and update
    target_files = [
        'index.html', 'about.html', 'services.html', 'contact.html',
        'service-area.html', 'referrals.html', 'privacy-policy.html', 'sitemap.html'
    ]
    
    # Add all service pages
    services_dir = 'services'
    if os.path.exists(services_dir):
        for filename in os.listdir(services_dir):
            if filename.endswith('.html'):
                target_files.append(os.path.join(services_dir, filename))
    
    updated_files = 0
    total_updates = 0
    
    for file_path in target_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # Replace Massachusetts with Nebraska
            content = content.replace('Massachusetts', 'Nebraska')
            content = content.replace('massachusetts', 'nebraska')
            content = content.replace('MA', 'NE')
            
            # Update specific location references
            content = content.replace('Norfolk NE', 'Norfolk, NE')
            content = content.replace('Nebraska area', 'Norfolk, NE area')
            content = content.replace('Nebraska homes', 'Nebraska homes')
            
            # Update service area descriptions
            content = content.replace('throughout Massachusetts', 'throughout Northeast Nebraska')
            content = content.replace('across Massachusetts', 'across Nebraska')
            content = content.replace('Massachusetts properties', 'Nebraska properties')
            content = content.replace('Massachusetts residents', 'Nebraska residents')
            
            # Update meta descriptions and titles
            content = content.replace('Massachusetts\'s', 'Nebraska\'s')
            content = content.replace('Massachusetts’s', 'Nebraska\'s')
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                changes = len(re.findall(r'Nebraska|NE|Norfolk', content)) - len(re.findall(r'Nebraska|NE|Norfolk', original_content))
                total_updates += changes
                updated_files += 1
                print(f"UPDATED: {os.path.basename(file_path)} - {changes} changes")
        
        except Exception as e:
            print(f"ERROR: {file_path}: {str(e)}")
    
    print("=" * 60)
    print(f"SUCCESS: Updated {updated_files} files with {total_updates} state references")
    print("\nCHANGES MADE:")
    print("- Massachusetts to Nebraska")
    print("- MA to NE") 
    print("- Added proper Norfolk, NE references")
    print("- Updated service area descriptions")
    print("- Fixed meta descriptions and titles")

def main():
    update_state_references()
    
    print("\n" + "=" * 60)
    print("READY TO PUSH STATE CORRECTIONS:")
    print("git add .")
    print('git commit -m "Critical: Update all state references from Massachusetts to Nebraska/Norfolk"')
    print("git push origin main")

if __name__ == "__main__":
    main()