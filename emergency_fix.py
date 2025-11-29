import os

def emergency_fix_tiles(file_path):
    """Emergency fix - add CSS directly with !important flags"""
    
    emergency_css = """
    <!-- EMERGENCY TILE FIX -->
    <style>
    /* FORCE GRADIENT ANIMATIONS WITH !IMPORTANT */
    .benefit-card, .value-tile, .service-tile, .trust-item,
    .service-card, .promo-card, .category-card, .contact-tile, .area-tile {
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    }
    
    .benefit-card::before, .value-tile::before, .service-tile::before, 
    .trust-item::before, .service-card::before, .promo-card::before,
    .category-card::before, .contact-tile::before, .area-tile::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(135deg, #0A1D37, #00C4B4) !important;
        transition: left 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        z-index: 1 !important;
    }
    
    .benefit-card:hover::before, .value-tile:hover::before, 
    .service-tile:hover::before, .trust-item:hover::before,
    .service-card:hover::before, .promo-card:hover::before,
    .category-card:hover::before, .contact-tile:hover::before,
    .area-tile:hover::before {
        left: 0 !important;
    }
    
    .benefit-card > *, .value-tile > *, .service-tile > *, 
    .trust-item > *, .service-card > *, .promo-card > *,
    .category-card > *, .contact-tile > *, .area-tile > * {
        position: relative !important;
        z-index: 2 !important;
    }
    
    .benefit-card:hover, .value-tile:hover, .service-tile:hover, 
    .trust-item:hover, .service-card:hover, .promo-card:hover,
    .category-card:hover, .contact-tile:hover, .area-tile:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* FORCE TEXT COLOR CHANGE */
    .benefit-card:hover *, .value-tile:hover *, .service-tile:hover *, 
    .trust-item:hover *, .service-card:hover *, .promo-card:hover *,
    .category-card:hover *, .contact-tile:hover *, .area-tile:hover * {
        color: white !important;
    }
    </style>
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove any existing emergency fix
        if 'EMERGENCY TILE FIX' in content:
            start = content.find('<!-- EMERGENCY TILE FIX -->')
            end = content.find('</style>', start) + 8
            content = content[:start] + content[end:]
        
        # Insert at the VERY beginning of head to override everything
        if '<head>' in content:
            content = content.replace('<head>', '<head>' + emergency_css)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"✓ Emergency fix applied to {os.path.basename(file_path)}")
            return True
        else:
            print(f"✗ No <head> tag found in {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"Error with {file_path}: {str(e)}")
        return False

def main():
    print("EMERGENCY TILE FIX")
    print("=" * 30)
    
    files = ['referrals.html', 'about.html', 'service-area.html', 'contact.html']
    
    for file in files:
        if os.path.exists(file):
            emergency_fix_tiles(file)
        else:
            print(f"✗ {file} not found")

if __name__ == "__main__":
    main()