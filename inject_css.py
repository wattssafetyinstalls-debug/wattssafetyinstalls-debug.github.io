#!/usr/bin/env python3
"""
Inject the full CSS and template structure into broken service pages
"""

import os

# Your full CSS from your working template
FULL_CSS = """
        :root {
            --teal: #00C4B4;
            --navy: #0A1D37;
            --light: #F8FAFC;
            --gray: #64748B;
            --gold: #FFD700;
            --white: #FFFFFF;
            --warm-light: #FEF7ED;
            --shadow: 0 10px 30px rgba(0,0,0,0.08);
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--warm-light);
            color: #1E293B;
            line-height: 1.7;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        /* Navigation */
        header {
            background: var(--navy);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .logo {
            font-family: 'Playfair Display', serif;
            font-size: 2.8rem;
            color: var(--teal);
            text-decoration: none;
            font-weight: 700;
        }
        .nav-links {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        .nav-links a {
            color: var(--white);
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s;
            position: relative;
            padding: 10px 0;
        }
        .nav-links a:hover {
            color: var(--teal);
        }
        .nav-links a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 3px;
            bottom: 0;
            left: 0;
            background-color: var(--teal);
            transition: width 0.3s;
        }
        .nav-links a:hover::after {
            width: 100%;
        }
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--white);
            font-size: 1.8rem;
            cursor: pointer;
        }
        
        .hero {
            height: 85vh;
            min-height: 600px;
            background: linear-gradient(135deg, rgba(10,29,55,0.9), rgba(245,158,11,0.25)),
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80') center/cover;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
        }
        .hero h1 {
            font-family: 'Playfair Display', serif;
            font-size: 4.5rem;
            margin-bottom: 15px;
        }
        .certification-badge {
            background: var(--gold);
            color: var(--navy);
            padding: 10px 28px;
            border-radius: 50px;
            font-weight: 700;
        }
        .cta-button {
            background: var(--teal);
            color: white;
            padding: 20px 60px;
            border-radius: 50px;
            font-size: 1.4rem;
            font-weight: 700;
            text-decoration: none;
            margin-top: 30px;
            box-shadow: 0 12px 30px rgba(0,196,180,0.4);
            transition: all .3s;
        }
        .cta-button:hover, .cta-button:active {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,196,180,0.6);
        }

        /* PREMIUM SERVICE TILE */
        .service-tile {
            max-width: 1200px;
            margin: 70px auto;
            padding: 60px 50px;
            background: white;
            border-radius: 32px;
            box-shadow: var(--shadow);
            text-align: center;
            position: relative;
            overflow: hidden;
            border: 3px solid transparent;
            cursor: pointer;
            transition: all 0.55s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .service-tile::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }
        .service-tile::after {
            content: '';
            position: absolute;
            inset: -8px;
            border-radius: 38px;
            border: 4px solid transparent;
            opacity: 0;
            box-shadow: 0 0 30px rgba(0,196,180,0);
            transition: all 0.5s ease;
            pointer-events: none;
        }
        @media (hover:hover) and (pointer:fine) {
            .service-tile:hover {
                transform: translateY(-14px) scale(1.035);
                box-shadow: 0 40px 100px rgba(10,29,55,0.4);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-tile:hover::before {
                opacity: 1;
                animation: gloss 1.6s ease-out forwards;
            }
            .service-tile:hover::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.6);
                box-shadow: 0 0 40px rgba(0,196,180,0.5);
            }
            .service-tile:hover h2, .service-tile:hover p, .service-tile:hover .trust-text {
                color: white !important;
            }
            .service-tile:hover .trust-bar {
                background: rgba(255,255,255,0.12);
            }
            .service-tile:hover .trust-icon {
                transform: scale(1.5) translateY(-8px);
                color: var(--gold) !important;
            }
        }
        @media (hover:none), (max-width:768px) {
            .service-tile:active {
                transform: translateY(-12px) scale(1.03);
                box-shadow: 0 35px 90px rgba(10,29,55,0.38);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-tile:active::before {
                opacity: 1;
                animation: gloss 1.3s ease-out forwards;
            }
            .service-tile:active::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.7);
                box-shadow: 0 0 35px rgba(0,196,180,0.6);
            }
            .service-tile:active h2, .service-tile:active p, .service-tile:active .trust-text {
                color: white !important;
            }
            .service-tile:active .trust-bar {
                background: rgba(255,255,255,0.12);
            }
            .service-tile:active .trust-icon {
                transform: scale(1.5) translateY(-8px);
                color: var(--gold) !important;
            }
        }
        @keyframes gloss {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .service-tile h2 {
            font-family: 'Playfair Display', serif;
            font-size: 3.2rem;
            color: var(--navy);
            margin-bottom: 25px;
            transition: color 0.4s;
        }
        .service-description {
            font-size: 1.25rem;
            color: #444;
            margin-bottom: 45px;
            line-height: 1.8;
            transition: color 0.4s;
        }
        
        /* SMALLER TRUST BAR - Reduced size for better SEO space */
        .trust-bar {
            background: var(--light);
            padding: 30px 35px; /* Reduced padding */
            border-radius: 20px; /* Slightly smaller radius */
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px; /* Reduced gap */
            transition: all 0.5s;
            margin-bottom: 35px; /* Reduced margin */
        }
        .trust-item {
            text-align: center;
            flex: 1;
            min-width: 140px; /* Slightly smaller minimum width */
        }
        .trust-icon {
            font-size: 2.5rem; /* Smaller icons */
            color: var(--teal);
            margin-bottom: 8px; /* Reduced margin */
            transition: all 0.4s ease;
        }
        .trust-text {
            font-weight: 600;
            color: var(--navy);
            font-size: 0.95rem; /* Slightly smaller text */
            transition: color 0.4s;
        }

        /* Professional Service Showcase */
        .service-showcase {
            margin-top: 50px;
            padding: 40px;
            background: var(--light);
            border-radius: 20px;
            text-align: center;
        }
        .service-showcase h3 {
            font-size: 1.8rem;
            color: var(--navy);
            margin-bottom: 30px;
            font-family: 'Playfair Display', serif;
        }
        
        /* FIXED: Service Categories 4-Grid Layout */
        .service-categories {
            display: grid;
            grid-template-columns: repeat(4, 1fr); /* Fixed 4-column grid */
            gap: 25px;
            margin-top: 30px;
        }
        
        /* Service Category Tiles */
        .service-category {
            background: var(--white);
            padding: 25px;
            border-radius: 15px;
            box-shadow: var(--shadow);
            transition: all 0.55s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
            border: 2px solid transparent;
            cursor: pointer;
        }
        .service-category::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }
        .service-category::after {
            content: '';
            position: absolute;
            inset: -4px;
            border-radius: 19px;
            border: 2px solid transparent;
            opacity: 0;
            box-shadow: 0 0 20px rgba(0,196,180,0);
            transition: all 0.5s ease;
            pointer-events: none;
        }
        
        /* Hover effects for service category tiles */
        @media (hover:hover) and (pointer:fine) {
            .service-category:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 25px 60px rgba(10,29,55,0.3);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-category:hover::before {
                opacity: 1;
                animation: gloss 1.6s ease-out forwards;
            }
            .service-category:hover::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.6);
                box-shadow: 0 0 30px rgba(0,196,180,0.5);
            }
            .service-category:hover .category-title,
            .service-category:hover .category-services {
                color: white !important;
            }
            .service-category:hover .category-icon {
                transform: scale(1.3) translateY(-5px);
                color: var(--gold) !important;
            }
        }
        @media (hover:none), (max-width:768px) {
            .service-category:active {
                transform: translateY(-6px) scale(1.01);
                box-shadow: 0 20px 45px rgba(10,29,55,0.25);
                background: linear-gradient(135deg, var(--teal), var(--navy));
                color: white;
                border-color: var(--gray);
            }
            .service-category:active::before {
                opacity: 1;
                animation: gloss 1.3s ease-out forwards;
            }
            .service-category:active::after {
                opacity: 1;
                border-color: rgba(0,196,180,0.7);
                box-shadow: 0 0 25px rgba(0,196,180,0.6);
            }
            .service-category:active .category-title,
            .service-category:active .category-services {
                color: white !important;
            }
            .service-category:active .category-icon {
                transform: scale(1.3) translateY(-5px);
                color: var(--gold) !important;
            }
        }

        .category-icon {
            font-size: 2.5rem;
            color: var(--teal);
            margin-bottom: 15px;
            transition: all 0.4s ease;
        }
        .category-title {
            font-weight: 700;
            color: var(--navy);
            margin-bottom: 10px;
            font-size: 1.2rem;
            transition: color 0.4s;
        }
        .category-services {
            color: var(--gray);
            font-size: 0.95rem;
            line-height: 1.5;
            transition: color 0.4s;
        }

        .contact-btn {
            background: var(--teal);
            color: white;
            padding: 16px 48px;
            border-radius: 50px;
            font-weight: 700;
            text-decoration: none;
            box-shadow: 0 8px 25px rgba(0,196,180,0.4);
            transition: all .35s;
        }
        .contact-btn:hover, .contact-btn:active {
            transform: translateY(-5px) scale(1.06);
            box-shadow: 0 15px 35px rgba(0,196,180,0.6);
        }
        .return-btn {
            display: inline-block;
            background: var(--gray);
            color: white;
            padding: 12px 32px;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            margin: 40px auto 0;
            transition: all .35s;
        }
        .return-btn:hover, .return-btn:active {
            background: var(--teal);
            transform: translateY(-4px);
        }
        footer {
            background: var(--navy);
            color: white;
            padding: 80px 20px 30px;
            margin-top: auto;
            text-align: center;
        }
        .footer-contact a {
            color: var(--teal);
            text-decoration: none;
            transition: color .3s;
        }
        .footer-contact a:hover {
            color: var(--gold);
        }
        .footer-links a {
            color: var(--teal);
            margin: 0 15px;
            text-decoration: none;
        }
        .footer-links a:hover {
            color: var(--gold);
        }

        /* Mobile Responsive */
        @media (max-width: 1024px) {
            .service-categories {
                grid-template-columns: repeat(2, 1fr); /* 2 columns on tablets */
            }
        }

        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            .service-tile {
                margin: 40px 15px;
                padding: 40px 25px;
            }
            .trust-bar {
                flex-direction: column;
                padding: 25px 20px; /* Even smaller on mobile */
                gap: 15px;
            }
            .trust-item {
                min-width: 100%;
            }
            .service-categories {
                grid-template-columns: 1fr; /* 1 column on mobile */
            }
            .nav-links {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                width: 100%;
                background: var(--navy);
                flex-direction: column;
                padding: 30px 20px;
                gap: 20px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .nav-links.active {
                display: flex;
            }
            .nav-links a {
                padding: 15px 0;
                font-size: 1.2rem;
                text-align: center;
                width: 100%;
                display: block;
            }
            .mobile-menu-btn {
                display: block;
            }
        }
"""

def inject_full_css():
    """Inject the full CSS into all service pages"""
    services_dir = './services'
    fixed_count = 0
    
    for filename in os.listdir(services_dir):
        if filename.endswith('.html') and not filename.endswith('.backup'):
            filepath = os.path.join(services_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the broken CSS with full CSS
            if '<style>' in content and '</style>' in content:
                # Find the style section and replace it
                start = content.find('<style>')
                end = content.find('</style>') + 8
                new_content = content[:start] + '<style>' + FULL_CSS + '</style>' + content[end:]
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                fixed_count += 1
                print(f"Injected full CSS: {filename}")
    
    print(f"Injected full CSS into {fixed_count} service pages")

if __name__ == "__main__":
    inject_full_css()