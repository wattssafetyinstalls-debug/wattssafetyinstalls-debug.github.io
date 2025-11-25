# fix_all_redirects.py
import os
import re

def fix_all_html_redirects():
    print("🛠️ FIXING ALL HTML REDIRECTS...")
    
    # Standardize all redirects to this format
    standard_redirect_script = """<script>
// Pretty URL Standardization
(function() {
    const path = window.location.pathname;
    const redirects = {
        // Main pages
        '/index': '/',
        '/services': '/services.html',
        '/service-area': '/service-area.html', 
        '/about': '/about.html',
        '/referrals': '/referrals.html',
        '/contact': '/contact.html',
        '/sitemap': '/sitemap.html',
        
        // Service pages - pretty URLs to actual files
        '/ada-compliant-showers': '/services/ada-compliant-showers-bathrooms.html',
        '/grab-bar-installation': '/services/grab-bar-installation.html',
        '/wheelchair-ramps': '/services/wheelchair-ramp-installation.html',
        '/stairlift-installation': '/services/stairlift-elevator-installation.html',
        '/non-slip-flooring': '/services/non-slip-flooring-solutions.html',
        '/kitchen-renovations': '/services/kitchen-renovations.html',
        '/bathroom-remodels': '/services/bathroom-remodels.html',
        '/room-additions': '/services/room-additions.html',
        '/flooring-installation': '/services/flooring-installation.html',
        '/painting-services': '/services/painting-drywall.html',
        '/tv-mounting': '/services/tv-mounting.html',
        '/home-theater-installation': '/services/home-theater-installation.html',
        '/sound-system-setup': '/services/sound-system-setup.html',
        '/cable-management': '/services/cable-management.html',
        '/lawn-maintenance': '/services/lawn-maintenance.html',
        '/pressure-washing': '/services/pressure-washing.html',
        '/gutter-cleaning': '/services/gutter-cleaning.html',
        '/fence-repair': '/services/fence-repair.html',
        '/handyman-services': '/services/handyman-services.html'
    };
    
    // Handle redirects
    if (redirects[path]) {
        window.history.replaceState({}, "", redirects[path]);
    }
    
    // Special case for home page
    if (path === '/index') {
        window.history.replaceState({}, "", "/");
    }
})();
</script>"""

    html_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        old_content = content
        
        # Remove all existing redirect scripts to avoid conflicts
        content = re.sub(r'<script>\s*//\s*Pretty URL[^<]*</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'<script>\s*\(function\(\)[^<]*}</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'window\.location\.pathname\s*===\s*[^;]+;', '', content)
        content = re.sub(r'window\.history\.replaceState\([^;]+;', '', content)
        
        # Add standard redirect script before closing head tag
        if '</head>' in content:
            content = content.replace('</head>', f'{standard_redirect_script}\n</head>')
        elif '<body>' in content:
            content = content.replace('<body>', f'{standard_redirect_script}\n<body>')
        else:
            content = standard_redirect_script + content
        
        if old_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ FIXED: {file_path}")
        else:
            print(f"✅ ALREADY OK: {file_path}")

fix_all_html_redirects()