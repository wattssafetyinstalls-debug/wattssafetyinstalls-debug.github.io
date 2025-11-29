import os
import shutil
from datetime import datetime

def backup_website():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = f"website-backup-{timestamp}"
    
    # Files to backup
    files_to_backup = [
        'index.html', 'about.html', 'services.html', 'service-area.html', 
        'contact.html', 'referrals.html', 'privacy-policy.html', 'sitemap.html'
    ]
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    os.makedirs(os.path.join(backup_dir, 'services'), exist_ok=True)
    
    # Backup main files
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(backup_dir, file))
            print(f"Backed up: {file}")
    
    # Backup services directory
    if os.path.exists('services'):
        for service_file in os.listdir('services'):
            if service_file.endswith('.html'):
                shutil.copy2(
                    os.path.join('services', service_file), 
                    os.path.join(backup_dir, 'services', service_file)
                )
        print(f"Backed up services directory ({len(os.listdir('services'))} files)")
    
    print(f"Backup completed: {backup_dir}")

if __name__ == "__main__":
    backup_website()