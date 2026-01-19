import os
import re

# ATP (Safety-related) services - keep navy/teal
ATP_SERVICES = [
    'accessibility-safety-solutions',
    'ada-compliant-showers',
    'ada-compliant-showers-bathrooms',
    'bathroom-accessibility',
    'custom-ramps',
    'grab-bar-installation',
    'grab-bars',
    'non-slip-flooring',
    'non-slip-flooring-solutions',
    'senior-safety',
    'wheelchair-ramp-installation'
]

# DBA (Non-safety) services - rebrand to black/red/cream
DBA_SERVICES = [
    'audio-visual',
    'basement-finishing',
    'bathroom-remodels',
    'cabinet-refacing',
    'cable-management',
    'concrete-pouring',
    'concrete-repair',
    'countertop-repair',
    'custom-cabinets',
    'custom-storage',
    'deck-construction',
    'driveway-installation',
    'drywall-repair',
    'emergency-repairs',
    'emergency-snow',
    'fence-installation',
    'fence-repair',
    'fertilization',
    'floor-refinishing',
    'flooring-installation',
    'garden-maintenance',
    'gutter-cleaning',
    'handyman-repair-services',
    'handyman-services',
    'hardwood-flooring',
    'home-audio',
    'home-remodeling',
    'home-remodeling-renovation',
    'home-theater-installation',
    'kitchen-cabinetry',
    'kitchen-renovations',
    'landscape-design',
    'lawn-maintenance',
    'onyx-countertops',
    'painting-services',
    'patio-construction',
    'pressure-washing',
    'projector-install',
    'property-maintenance-services',
    'room-additions',
    'seasonal-cleanup',
    'seasonal-prep',
    'siding-replacement',
    'snow-removal',
    'sound-system-setup',
    'soundbar-setup',
    'tree-trimming',
    'tv-mounting',
    'window-doors'
]

def rebrand_dba_service(service_name):
    """Rebrand a single DBA service page"""
    source_path = f'services/{service_name}/index.html'
    dest_dir = f'safety-installs/services/{service_name}'
    dest_path = f'{dest_dir}/index.html'
    
    if not os.path.exists(source_path):
        print(f"⚠️  Source not found: {source_path}")
        return False
    
    # Read source file
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rebrand colors
    content = re.sub(r'--navy:\s*#0A1D37;', '--navy: #1a1a1a;', content)
    content = re.sub(r'--teal:\s*#00C4B4;', '--teal: #dc2626;', content)
    content = re.sub(r'--gold:\s*#FFD700;', '--gold: #f5f5dc;', content)
    
    # Rebrand company name
    content = content.replace('Watts ATP Contractor', 'Watts Safety Installs')
    content = content.replace('WATTS ATP CONTRACTOR', 'WATTS SAFETY INSTALLS')
    content = content.replace('ATP Approved Contractor', 'Professional Home Services')
    
    # Update navigation links to point to DBA pages
    content = re.sub(r'href="/services\.html"', 'href="/safety-installs/services.html"', content)
    content = re.sub(r'href="/about\.html"', 'href="/safety-installs/about.html"', content)
    content = re.sub(r'href="/contact\.html"', 'href="/safety-installs/contact.html"', content)
    content = re.sub(r'href="/service-area\.html"', 'href="/safety-installs/service-area.html"', content)
    
    # Create destination directory
    os.makedirs(dest_dir, exist_ok=True)
    
    # Write rebranded file
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Rebranded: {service_name}")
    return True

def main():
    print("🔧 Starting DBA service rebranding...\n")
    
    success_count = 0
    fail_count = 0
    
    for service in DBA_SERVICES:
        if rebrand_dba_service(service):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n✨ Rebranding complete!")
    print(f"   ✅ Success: {success_count}")
    print(f"   ⚠️  Failed: {fail_count}")
    print(f"\n📁 DBA services now in: safety-installs/services/")

if __name__ == '__main__':
    main()
