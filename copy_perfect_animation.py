import os
import re

source = "services/siding-replacement.html"

with open(source, 'r', encoding='utf-8') as f:
    source_content = f.read()

# Grab the exact working animation CSS and JS from your perfect service page
css_match = re.search(r'(?s)(/\* MOBILE AUTO-ANIMATION EFFECTS.*?</style>)', source_content, re.DOTALL)
js_match = re.search(r'(?s)(<script>.*?mobile-animated.*?</script>)', source_content, re.DOTALL)

if not css_match or not js_match:
    print("ERROR: Animation not found in source page!")
else:
    css_block = css_match.group(1)
    js_block = js_match.group(1)

    pages = ['index.html', 'about.html', 'referrals.html', 'contact.html', 'service-area.html']

    for page in pages:
        if not os.path.exists(page):
            print("SKIP (not found):", page)
            continue
        
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add/replace CSS
        if "MOBILE AUTO-ANIMATION EFFECTS" not in content:
            content = re.sub(r'(?i)</style>', css_block, content, count=1)
        
        # Add/replace JS
        if "mobile-animated" not in content:
            content = re.sub(r'(?i)</body>', js_block + "\n</body>", content, count=1)
        
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("ANIMATION COPIED TO:", page)

    print("\nALL DONE! Every page now has IDENTICAL navy-to-teal + satin gloss animation.")
    print("Open INCOGNITO MODE → http://localhost:8000/about and hover any tile.")