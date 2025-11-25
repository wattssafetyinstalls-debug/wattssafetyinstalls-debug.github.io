# final_deploy.py
import os
import subprocess

def final_deployment():
    print("🚀 FINAL DEPLOYMENT - FIXING ALL URLS...")
    
    # Run all fixes
    scripts_to_run = [
        "analyze_current_redirects.py",
        "fix_all_redirects.py", 
        "fix_all_python_scripts.py",
        "create_all_redirect_files.py"
    ]
    
    for script in scripts_to_run:
        if os.path.exists(script):
            print(f"\n▶️ RUNNING: {script}")
            result = subprocess.run(['python', script], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"STDERR: {result.stderr}")
        else:
            print(f"❌ SCRIPT NOT FOUND: {script}")
    
    # Git deployment
    print("\n📦 DEPLOYING TO GITHUB...")
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ git add .")
        
        subprocess.run(['git', 'commit', '-m', 'COMPLETE: Fix all redirect URLs and navigation'], check=True)
        print("✅ git commit")
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ git push")
        
        print("\n🎉 DEPLOYMENT COMPLETE!")
        print("⏰ Wait 1-2 minutes for GitHub Pages to update")
        print("🌐 Your fixed URLs will be live at: https://wattsatpcontractor.com")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        print("\n💡 Manual deployment:")
        print("git add .")
        print("git commit -m 'COMPLETE: Fix all redirect URLs and navigation'")
        print("git push origin main")

# Run final deployment
final_deployment()