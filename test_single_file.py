# test_single_file.py
import os

def test_single_file():
    # Test on services.html first
    test_file = "services.html"
    
    if os.path.exists(test_file):
        print("Testing on: " + test_file)
        
        # Backup the file
        with open(test_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Check if already has animations
        if 'TILE ANIMATION STYLES' in original_content:
            print("File already has animations")
            return True
        
        # Add the CSS before </head>
        if '</head>' in original_content:
            css_to_add = """
    <!-- TILE ANIMATION STYLES -->
    <style>
    .service-tile, .service-card {
        position: relative;
        overflow: hidden;
    }
    .service-tile::before, .service-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #0A1D37, #00C4B4);
        transition: left 0.6s ease;
        z-index: 1;
    }
    .service-tile:hover::before, .service-card:hover::before {
        left: 0;
    }
    .service-tile > *, .service-card > * {
        position: relative;
        z-index: 2;
    }
    </style>
"""
            new_content = original_content.replace('</head>', css_to_add + '\n</head>')
            
            # Write the test file
            with open('test_' + test_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("Created test file: test_" + test_file)
            print("Open this file in browser to check if animations work")
            return True
    else:
        print("Test file not found: " + test_file)
        return False

if __name__ == "__main__":
    test_single_file()