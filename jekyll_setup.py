# jekyll_setup.py
import os
import shutil

def setup_jekyll():
    print("SETTING UP JEKYLL TEMPLATE SYSTEM...")
    
    # Create directories
    directories = ['_layouts', '_includes', '_data']
    for dir in directories:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"Created directory: {dir}")
    
    print("Jekyll structure created!")
    print("Now you need to:")
    print("1. Move your existing HTML files to use the layout")
    print("2. Update your service pages")
    print("3. The dropdown will be automatic and consistent across all pages!")

if __name__ == "__main__":
    setup_jekyll()