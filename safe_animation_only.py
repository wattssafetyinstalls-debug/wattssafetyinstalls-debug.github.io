import os
import re

# Source of truth: your working service page
source = "services/siding-replacement.html"
with open(source, 'r', encoding='utf-8') as f:
    src = f.read()

css = re.search(r'(?s)(/\* MOBILE AUTO-ANIMATION EFFECTS.*?</style>)', src, re.DOTALL).group(1)
js  = re.search(r'(?s)(<script>.*mobile-animated.*?</script>)', src, re.DOTALL).group(1)

pages = ['index.html','about.html','referrals.html','contact.html','service-area.html']

for p in pages:
    if not os.path.exists(p): continue
    with open(p,'r',encoding='utf-8') as f: content = f.read()
    if "MOBILE AUTO-ANIMATION" not in content:
        content = re.sub(r'(?i)</style>', css + '\n</style>', content, count=1)
    if "mobile-animated" not in content:
        content = re.sub(r'(?i)</body>', '\n' + js + '\n</body>', content, count=1)
    with open(p,'w',encoding='utf-8') as f: f.write(content)
    print("Animation added to:", p)