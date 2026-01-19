#!/usr/bin/env python3
"""
Script to copy and rebrand DBA service pages from /services/ to /safety-installs/services/
with black/red/cream color scheme and Watts Safety Installs branding.
"""

import os
import shutil
import re
from pathlib import Path

# DBA services to copy and rebrand
DBA_SERVICES = [
    'audio-visual', 'basement-finishing', 'bathroom-remodels', 'cabinet-refacing',
    'cable-management', 'concrete-pouring', 'concrete-repair', 'countertop-repair',
    'custom-cabinets', 'custom-storage', 'deck-construction', 'driveway-installation',
    'drywall-repair', 'emergency-repairs', 'emergency-snow', 'fence-installation',
    'fence-repair', 'fertilization', 'floor-refinishing', 'flooring-installation',
    'garden-maintenance', 'gutter-cleaning', 'handyman-repair-services', 'handyman-services',
    'hardwood-flooring', 'home-audio', 'home-remodeling', 'home-remodeling-renovation',
    'home-theater-installation', 'kitchen-cabinetry', 'kitchen-renovations',
    'landscape-design', 'lawn-maintenance', 'onyx-countertops', 'painting-services',
    'patio-construction', 'pressure-washing', 'projector-install', 'room-additions',
    'seasonal-cleanup', 'siding-replacement', 'smart-audio', 'snow-removal',
    'soundbar-setup', 'tile-installation', 'tree-trimming', 'tv-mounting', 'window-doors'
]

# Color scheme replacements
COLOR_REPLACEMENTS = {
    '--teal: #00C4B4': '--primary: #dc2626',
    '--navy: #0A1D37': '--dark: #0a0a0a',
    '--gold: #FFD700': '--secondary: #fef3c7',
    'var(--teal)': 'var(--primary)',
    'var(--navy)': 'var(--dark)',
    'var(--gold)': 'var(--secondary)',
}

# Branding replacements
BRANDING_REPLACEMENTS = {
    'Watts ATP Contractor': 'Watts Safety Installs',
    'WATTS ATP CONTRACTOR': 'WATTS SAFETY INSTALLS',
    'ATP Approved Contractor': 'DBA of Watts ATP Contractor',
    'wattsatpcontractor.com/services/': 'wattsatpcontractor.com/safety-installs/services/',
    'href="/services/': 'href="/safety-installs/services/',
    'href="services/': 'href="/safety-installs/services/',
    '/services.html': '/safety-installs/services.html',
    'All Services | Watts ATP': 'All Services | Watts Safety Installs',
}

def rebrand_content(content):
    """Apply color scheme and branding changes to content."""
    # Apply color replacements
    for old, new in COLOR_REPLACEMENTS.items():
        content = content.replace(old, new)
    
    # Apply branding replacements
    for old, new in BRANDING_REPLACEMENTS.items():
        content = content.replace(old, new)
    
    # Update canonical URLs
    content = re.sub(
        r'<link rel="canonical" href="https://wattsatpcontractor\.com/services/([^"]+)"',
        r'<link rel="canonical" href="https://wattsatpcontractor.com/safety-installs/services/\1"',
        content
    )
    
    # Update structured data URLs
    content = re.sub(
        r'"url":\s*"https://wattsatpcontractor\.com/services/([^"]+)"',
        r'"url": "https://wattsatpcontractor.com/safety-installs/services/\1"',
        content
    )
    
    return content

def copy_and_rebrand_service(service_name, source_dir, dest_dir):
    """Copy a service directory and rebrand its content."""
    source_path = source_dir / service_name
    dest_path = dest_dir / service_name
    
    if not source_path.exists():
        print(f"⚠️  Source not found: {source_path}")
        return False
    
    # Create destination directory
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Copy and rebrand index.html
    source_file = source_path / 'index.html'
    dest_file = dest_path / 'index.html'
    
    if source_file.exists():
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Rebrand content
        rebranded_content = rebrand_content(content)
        
        # Write to destination
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(rebranded_content)
        
        print(f"✅ Copied and rebranded: {service_name}")
        return True
    else:
        print(f"⚠️  No index.html found in: {source_path}")
        return False

def main():
    """Main execution function."""
    base_dir = Path(__file__).parent
    source_dir = base_dir / 'services'
    dest_dir = base_dir / 'safety-installs' / 'services'
    
    print("🚀 Starting DBA service rebranding...")
    print(f"📁 Source: {source_dir}")
    print(f"📁 Destination: {dest_dir}")
    print(f"📋 Services to process: {len(DBA_SERVICES)}\n")
    
    success_count = 0
    failed_count = 0
    
    for service in DBA_SERVICES:
        if copy_and_rebrand_service(service, source_dir, dest_dir):
            success_count += 1
        else:
            failed_count += 1
    
    print(f"\n✨ Rebranding complete!")
    print(f"✅ Successfully processed: {success_count}")
    print(f"❌ Failed: {failed_count}")

if __name__ == '__main__':
    main()
