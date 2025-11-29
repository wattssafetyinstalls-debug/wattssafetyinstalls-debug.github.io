import os
import subprocess

def run_safe_update():
    print("SAFETY FIRST: Creating backup...")
    
    # Step 1: Backup
    subprocess.run(['python', 'backup_all_files.py'])
    
    print("Backup completed. Proceeding with updates...")
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    # Step 2: Update files
    print("Updating navigation and mobile animations...")
    subprocess.run(['python', 'fix_all_navigation.py'])
    
    print("Update completed!")
    print("Mobile auto-animation will trigger after 3 seconds on mobile devices")
    print("Navigation links now use pretty URLs")

if __name__ == "__main__":
    run_safe_update()