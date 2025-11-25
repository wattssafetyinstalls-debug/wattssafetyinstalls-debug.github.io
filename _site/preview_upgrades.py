import os
import webbrowser

files_to_preview = ['index.html', 'services.html']  # Add more files as needed

for file in files_to_preview:
    if os.path.exists(file):
        webbrowser.open('file://' + os.path.realpath(file))
        print(f"Opened: {file}")
    else:
        print(f"File not found: {file}")

print("Preview completed.")