# check_service_files_ascii.py
import os

def check_service_files():
    service_dir = "services"
    if os.path.exists(service_dir):
        print("Files in services directory:")
        for file in os.listdir(service_dir):
            if file.endswith(".html"):
                print(f"  [OK] {file}")
    else:
        print("[ERROR] services directory not found!")
    
    # Check if service-area.html exists
    if os.path.exists("service-area.html"):
        print("[OK] service-area.html exists")
    else:
        print("[ERROR] service-area.html missing - creating basic version...")
        create_service_area_file()

def create_service_area_file():
    basic_service_area = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Service Area | Watts Safety Installs | Norfolk NE</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Our Service Area</h1>
        <p>Watts Safety Installs serves Norfolk, NE and surrounding areas.</p>
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>"""
    
    with open("service-area.html", 'w', encoding='utf-8') as f:
        f.write(basic_service_area)
    print("[OK] Created basic service-area.html")

check_service_files()