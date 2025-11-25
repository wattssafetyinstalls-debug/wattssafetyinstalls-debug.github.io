# deploy_to_github_ascii.py
import os
import subprocess

def deploy_changes():
    print("Deploying to GitHub Pages...")
    
    try:
        # Add all files
        result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Files added to git")
        else:
            print(f"[ERROR] git add failed: {result.stderr}")
            return
        
        # Commit changes
        result = subprocess.run(['git', 'commit', '-m', 'Fix service pages, directory paths, and navigation'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Changes committed")
        else:
            print(f"[INFO] Commit: {result.stderr}")
        
        # Push to GitHub
        result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Changes pushed to GitHub!")
            print("GitHub Pages will automatically rebuild in 1-2 minutes")
            print("Your live site: https://wattsatpcontractor.com")
        else:
            print(f"[ERROR] git push failed: {result.stderr}")
            
    except Exception as e:
        print(f"[ERROR] Deployment error: {e}")
        print("\nManual deployment:")
        print("1. Open Git Bash or Terminal")
        print("2. Run: git add .")
        print("3. Run: git commit -m 'Fix service pages and navigation'")
        print("4. Run: git push origin main")

# Ask user if they want to deploy
response = input("Do you want to deploy these changes to your live site? (y/n): ")
if response.lower() == 'y':
    deploy_changes()
else:
    print("Changes are ready but not deployed. Run 'python deploy_to_github_ascii.py' when ready.")