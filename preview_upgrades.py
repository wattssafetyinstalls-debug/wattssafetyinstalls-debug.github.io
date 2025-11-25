import webbrowser

files_to_preview = ['index.html', 'services.html']  # Add files

for file in files_to_preview:
    webbrowser.open('file://' + os.path.realpath(file))
print("Previewing files.")