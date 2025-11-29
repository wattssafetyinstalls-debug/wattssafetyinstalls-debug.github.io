import os
import re

def fix_service_area_in_descriptions():
    """Fix service area from Massachusetts to Nebraska in meta descriptions"""
    
    services_dir = 'services'
    if not os.path.exists(services_dir):
        print("Services directory not found!")
        return
    
    service_files = [f for f in os.listdir(services_dir) if f.endswith('.html')]
    total_files = len(service_files)
    
    print(f"UPDATING SERVICE AREA IN {total_files} SERVICE PAGES")
    print("=" * 60)
    
    updated_count = 0
    
    for filename in service_files:
        file_path = os.path.join(services_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace Massachusetts with Nebraska in meta descriptions
            old_description_pattern = r'<meta name="description" content="[^"]*Massachusetts[^"]*"'
            matches = re.findall(old_description_pattern, content)
            
            if matches:
                for match in matches:
                    new_description = match.replace('Massachusetts', 'Nebraska')
                    content = content.replace(match, new_description)
                    updated_count += 1
                    print(f"UPDATED: {filename}")
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
        except Exception as e:
            print(f"ERROR: {filename}: {str(e)}")
    
    print("=" * 60)
    print(f"SUCCESS: Updated {updated_count} out of {total_files} service pages")
    print("All meta descriptions now mention Nebraska instead of Massachusetts.")

if __name__ == "__main__":
    fix_service_area_in_descriptions()