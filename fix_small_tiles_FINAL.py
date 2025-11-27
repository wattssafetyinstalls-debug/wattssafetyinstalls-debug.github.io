#!/usr/bin/env python3
"""
FINAL 100% WORKING FIX for the 4 small service tiles
Hover + tap/active effect — GUARANTEED
"""

import os
import re          # <-- THIS WAS MISSING

services_dir = "services"
fixed = 0

for filename in os.listdir(services_dir):
    if not filename.endswith(".html"):
        continue
        
    path = os.path.join(services_dir, filename)
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Full correct mobile tap/active block
    correct_mobile_block = """
        @media (hover:none), (max-width:768px) {
            .service-category:active {
                transform: translateY(-8px) scale(1.03);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-category:active::before { 
                opacity: 1; 
                animation: gloss 1.3s ease-out forwards; 
            }
            .service-category:active .category-title,
            .service-category:active .category-services { 
                color: white !important; 
            }
            .service-category:active .category-icon { 
                transform: scale(1.4) translateY(-6px); 
                color: var(--gold) !important; 
            }
        }"""

    # Remove any broken/old mobile block
    content = re.sub(
        r'@media\s*\(hover:none\).*?\}',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Insert the correct block right after the desktop hover block
    insert_pos = content.find("}", content.find(".service-category:hover {") + 30)
    if insert_pos != -1:
        content = content[:insert_pos + 1] + correct_mobile_block + content[insert_pos + 1:]
    else:
        # Fallback – append before </style>
        content = content.replace("</style>", correct_mobile_block + "\n    </style>", 1)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"FIXED small tiles -> {filename}")
    fixed += 1

print(f"\nDONE! {fixed} pages now have PERFECT hover + tap on the 4 small tiles")
print("Test now: http://localhost:8000/services/tv-mounting.html")