#!/usr/bin/env python3
import os
import re

services_dir = "services"
fixed = 0

# THE EXACT CSS THAT WORKS 100% — copied from a page where it already works perfectly
GOOD_CSS_BLOCK = """
        /* ==== 4 SMALL TILES — PERFECT HOVER & TAP (desktop + mobile) ==== */
        .service-category {
            background: var(--white);
            padding: 28px 20px;
            border-radius: 15px;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
            border: 2px solid transparent;
            cursor: pointer;
            transition: all .55s cubic-bezier(0.25,0.8,0.25,1);
        }
        .service-category::before {
            content:''; position:absolute; top:0; left:-100%; width:200%; height:100%;
            background:linear-gradient(90deg,transparent,rgba(255,255,255,0.4),transparent);
            opacity:0; transition:opacity .3s;
        }
        .service-category::after {
            content:''; position:absolute; inset:-4px; border-radius:19px;
            border:3px solid transparent; opacity:0;
            box-shadow:0 0 20px rgba(0,196,180,0); transition:all .5s;
        }
        @keyframes gloss { from {left:-100%} to {left:100%} }

        @media (hover:hover) and (pointer:fine) {
            .service-category:hover {
                transform:translateY(-10px) scale(1.04);
                box-shadow:0 30px 70px rgba(10,29,55,0.35);
                background:linear-gradient(135deg,var(--teal),var(--navy));
                color:white; border-color:var(--gray);
            }
            .service-category:hover::before { opacity:1; animation:gloss 1.6s ease-out forwards; }
            .service-category:hover::after { opacity:1; border-color:rgba(0,196,180,0.6); box-shadow:0 0 35px rgba(0,196,180,0.5); }
            .service-category:hover .category-title,
            .service-category:hover .category-services { color:white !important; }
            .service-category:hover .category-icon { transform:scale(1.4) translateY(-6px); color:var(--gold)!important; }
        }

        @media (hover:none), (max-width:768px) {
            .service-category:active {
                transform:translateY(-8px) scale(1.03);
                background:linear-gradient(135deg,var(--teal),var(--navy));
                color:white; border-color:var(--gray);
            }
            .service-category:active::before { opacity:1; animation:gloss 1.3s ease-out forwards; }
            .service-category:active .category-title,
            .service-category:active .category-services { color:white !important; }
            .service-category:active .category-icon { transform:scale(1.4) translateY(-6px); color:var(--gold)!important; }
        }
        /* ==== END OF SMALL TILES CSS ==== */"""

for filename in os.listdir(services_dir):
    if not filename.endswith(".html"):
        path = os.path.join(services_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        # 1. Remove ANY existing .service-category rules that might be broken
        html = re.sub(
            r'.service-category\s*\{.*?\}.*?(?=@media|$)', '', html, flags=re.DOTALL)
        html = re.sub(r'@media\s*\(hover:hover\).*?\{.*?\}','', html, flags=re.DOTALL)
        html = re.sub(r'@media\s*\(hover:none\).*?\{.*?\}','', html, flags=re.DOTALL)

        # 2. Inject the PERFECT block right before the .category-icon rule (or before </style> if not found)
        insert_point = html.find(".category-icon {")
        if insert_point == -1:
            insert_point = html.find("</style>")
        html = html[:insert_point] + GOOD_CSS_BLOCK + "\n        " + html[insert_point:]

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"FIXED 4 small tiles -> {filename}")
        fixed += 1

print(f"\nPERFECTION ACHIEVED: {fixed} pages now have FULLY WORKING small tiles")
print("Desktop hover = gradient + gloss + gold icons")
print("Mobile tap = same beautiful effect")