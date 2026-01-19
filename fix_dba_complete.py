import os
import re
import shutil

def create_dba_page(source_file, dest_file, page_type):
    """Create a DBA page by copying and rebranding ATP page"""
    
    if not os.path.exists(source_file):
        print(f"⚠️  Source not found: {source_file}")
        return False
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rebrand colors - black/red/cream for DBA
    content = content.replace('--navy: #0A1D37;', '--navy: #1a1a1a;')
    content = content.replace('--teal: #00C4B4;', '--teal: #dc2626;')
    content = content.replace('--gold: #FFD700;', '--gold: #f5f5dc;')
    
    # Rebrand company name
    content = content.replace('Watts ATP Contractor', 'Watts Safety Installs')
    content = content.replace('WATTS ATP CONTRACTOR', 'WATTS SAFETY INSTALLS')
    content = content.replace('ATP Approved Contractor', 'Professional Home Services')
    content = content.replace('ATP Approved', 'Professional')
    
    # Update navigation to point to DBA pages
    content = re.sub(r'href="/"(?!>)', 'href="/safety-installs/"', content)
    content = content.replace('href="/services.html"', 'href="/safety-installs/services.html"')
    content = content.replace('href="/service-area.html"', 'href="/safety-installs/service-area.html"')
    content = content.replace('href="/about.html"', 'href="/safety-installs/about.html"')
    content = content.replace('href="/referrals.html"', 'href="/safety-installs/referrals.html"')
    content = content.replace('href="/contact.html"', 'href="/safety-installs/contact.html"')
    
    # Update canonical URL
    if page_type == 'about':
        content = re.sub(r'<link rel="canonical" href="https://wattsatpcontractor\.com/about"', '<link rel="canonical" href="https://wattsatpcontractor.com/safety-installs/about"', content)
    elif page_type == 'contact':
        content = re.sub(r'<link rel="canonical" href="https://wattsatpcontractor\.com/contact"', '<link rel="canonical" href="https://wattsatpcontractor.com/safety-installs/contact"', content)
    elif page_type == 'service-area':
        content = re.sub(r'<link rel="canonical" href="https://wattsatpcontractor\.com/service-area"', '<link rel="canonical" href="https://wattsatpcontractor.com/safety-installs/service-area"', content)
    elif page_type == 'referrals':
        content = re.sub(r'<link rel="canonical" href="https://wattsatpcontractor\.com/referrals"', '<link rel="canonical" href="https://wattsatpcontractor.com/safety-installs/referrals"', content)
    
    # Create destination directory
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    
    # Write rebranded file
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created DBA {page_type}.html")
    return True

def fix_dba_services_carousel():
    """Fix DBA services.html carousel styling and timing"""
    
    services_file = 'safety-installs/services.html'
    
    if not os.path.exists(services_file):
        print(f"⚠️  {services_file} not found")
        return False
    
    with open(services_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix carousel auto-rotate timing from ~11s to 25s
    content = re.sub(r'setInterval\([^,]+,\s*\d+\)', 'setInterval(autoRotate, 25000)', content)
    
    # Remove teal background from service card text on hover
    # Find and replace the hover effect that adds teal background
    content = re.sub(
        r'\.service-card:hover\s*{[^}]*background:\s*linear-gradient\([^)]*#00C4B4[^)]*\)[^}]*}',
        '.service-card:hover { transform: translateY(-8px) scale(1.02); box-shadow: 0 20px 60px rgba(220, 38, 38, 0.4), 0 0 40px rgba(220, 38, 38, 0.2); }',
        content,
        flags=re.DOTALL
    )
    
    # Update service card hover to use red instead of teal
    content = content.replace('background: linear-gradient(135deg, var(--teal) 0%, var(--navy) 100%);', 'background: linear-gradient(135deg, #dc2626 0%, #1a1a1a 100%);')
    
    with open(services_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed DBA services.html carousel timing and styling")
    return True

def fix_homepage_service_tiles():
    """Fix homepage service tiles to be uniform size"""
    
    index_file = 'index.html'
    
    if not os.path.exists(index_file):
        print(f"⚠️  {index_file} not found")
        return False
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure service cards have consistent sizing
    # Find the .service-card CSS and ensure it has fixed dimensions
    service_card_css = '''
        .service-card {
            background: var(--white);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            display: flex;
            flex-direction: column;
            min-height: 450px;
            max-height: 450px;
            text-align: center;
        }'''
    
    # Replace existing .service-card definition
    content = re.sub(
        r'\.service-card\s*{[^}]*}',
        service_card_css,
        content,
        count=1
    )
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed homepage service tile sizing")
    return True

def main():
    print("🔧 Starting comprehensive DBA fixes...\n")
    
    # 1. Create missing DBA pages
    print("📄 Creating DBA pages...")
    create_dba_page('about.html', 'safety-installs/about.html', 'about')
    create_dba_page('contact.html', 'safety-installs/contact.html', 'contact')
    create_dba_page('service-area.html', 'safety-installs/service-area.html', 'service-area')
    create_dba_page('referrals.html', 'safety-installs/referrals.html', 'referrals')
    
    # 2. Fix DBA services.html carousel
    print("\n🎠 Fixing DBA services carousel...")
    fix_dba_services_carousel()
    
    # 3. Fix homepage service tiles
    print("\n🏠 Fixing homepage service tiles...")
    fix_homepage_service_tiles()
    
    print("\n✨ All DBA fixes complete!")
    print("📁 DBA pages created in: safety-installs/")
    print("🔗 Test at: http://localhost:8000/safety-installs/")

if __name__ == '__main__':
    main()
