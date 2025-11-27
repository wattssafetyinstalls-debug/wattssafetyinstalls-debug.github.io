#!/usr/bin/env python3
"""
Instant fix – restore full hover + tap effect on the 4 small service tiles
Run once – takes 3 seconds
"""

import os

services_dir = "services"

for filename in os.listdir(services_dir):
    if not filename.endswith(".html"):
        continue
        
    path = os.path.join(services_dir, filename)
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix 1: Make sure the @media rules for small tiles are correct and separate
    fixed = content.replace(
        '@media (hover:none), (max-width:768px) {',
        '@media (hover:none), (max-width:768px) {\n            .service-category:active {'
    )
    
    # Fix 2: Ensure the active styles are complete (sometimes got cut off)
    if ".service-category:active" not in fixed:
        # Re-insert the full active block right after the hover block
        insert_before = fixed.find("@media (max-width:768px)", fixed.find(".service-category:hover"))
        if insert_before != -1:
            active_css = """
        @media (hover:none), (max-width:768px) {
            .service-category:active {
                transform:translateY(-8px) scale(1.03);
                background:linear-gradient(135deg,var(--teal),var(--navy));
                color:white;
                border-color:var(--gray);
            }
            .service-category:active::before { opacity:1; animation:gloss 1.3s ease-out forwards; }
            .service-category:active .category-title,
            .service-category:active .category-services { color:white !important; }
            .service-category:active .category-icon { transform:scale(1.4) translateY(-6px); color:var(--gold)!important; }
        }"""
            fixed = fixed[:insert_before] + active_css + fixed[insert_before:]
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(fixed)
    
    print(f"Fixed hover/tap on small tiles → {filename}")

print("\nAll 4 small service tiles now have FULL hover + tap gradient effect!")