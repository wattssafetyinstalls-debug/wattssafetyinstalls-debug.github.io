#!/usr/bin/env python3
"""
Premium SEO + Analytics Implementation
- 150 character meta descriptions
- SEO-rich visible content
- All GA4 tracking codes
- Google Search Console verification
"""

import os

# Your Analytics Tracking Codes
ANALYTICS_CODES = {
    'google_site_verification': '9uPoUkPF9bV3aKmaJyxbcnlzzXjxYLkUPb-YXyvOabU',
    'ga4_main': 'G-R7FNGWQVQG',
    'ga4_tags': [
        'G-4BXXKZJZTZ',
        'G-8TF95LBYRV', 
        'G-B8SKQ9HHPZ',
        'G-E21ZQ9L9QC',
        'G-JL3RR3JH55',
        'G-P2MRLK93YK',
        'G-PG3KZVYPV0',
        'G-X6LMX9VR0Y'
    ],
    'aw_tag': 'AW-586671676'
}

# Premium 150-character Meta Descriptions
META_DESCRIPTIONS = {
    'tv-mounting.html': 'Professional TV mounting in Norfolk NE. Secure installations, optimal viewing angles, hidden cables. Same-day service. Call (405) 410-6402 for free estimate.',
    'snow-removal.html': 'Snow removal services in Norfolk NE. Residential & commercial plowing, de-icing, emergency response. Reliable winter maintenance. Call (405) 410-6402.',
    'ada-compliant-showers.html': 'ADA compliant shower installation in Norfolk NE. Barrier-free showers, grab bars, senior safety features. Licensed contractors. Free consultation.',
    'kitchen-renovations.html': 'Kitchen remodeling in Norfolk NE. Cabinet refacing, countertops, appliance installation. Transform your cooking space. Free design consultation.',
    'wheelchair-ramp-installation.html': 'Wheelchair ramp installation in Norfolk NE. ADA compliant, custom designs, permanent & portable solutions. Mobility access specialists.',
    'bathroom-remodels.html': 'Bathroom remodeling services in Norfolk NE. Luxury upgrades, accessibility features, complete renovations. Quality craftsmanship guaranteed.',
    'home-theater-installation.html': 'Home theater installation in Norfolk NE. TV mounting, surround sound, smart home integration. Cinema experience at home. Expert technicians.',
    'lawn-maintenance.html': 'Lawn care services in Norfolk NE. Mowing, fertilization, weed control, seasonal cleanups. Pristine lawns guaranteed. Free estimate.',
    'deck-construction.html': 'Deck building services in Norfolk NE. Custom wood & composite decks, pergolas, outdoor living spaces. Quality construction, durable materials.',
    'painting-services.html': 'Professional painting services in Norfolk NE. Interior & exterior painting, drywall repair, texture matching. Quality finishes, free estimates.'
}

# SEO-Rich Service Descriptions (Visible Content)
SEO_CONTENT = {
    'tv-mounting.html': {
        'title': 'Professional TV Mounting Services Norfolk NE | Secure Installation',
        'heading': 'Expert TV Mounting Services in Norfolk Nebraska',
        'description': 'Professional TV mounting services in Norfolk NE and throughout Northeast Nebraska. Our certified technicians provide secure wall mounting for all television sizes with optimal viewing angles and complete cable concealment. We serve Norfolk, Madison, Stanton, Pierce and surrounding communities with same-day installation available.'
    },
    'snow-removal.html': {
        'title': 'Snow Removal Services Norfolk NE | Emergency Plowing',
        'heading': 'Reliable Snow Removal & Ice Management Norfolk Nebraska',
        'description': 'Professional snow removal services in Norfolk NE providing 24/7 emergency response for residential and commercial properties. Our fleet serves Norfolk, Madison, Stanton, Pierce counties with commercial-grade plowing, de-icing, and winter maintenance solutions.'
    }
}

def generate_analytics_code():
    """Generate complete analytics tracking code"""
    return f"""
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-KCPM8VZ');</script>
    <!-- End Google Tag Manager -->

    <!-- Google Search Console Verification -->
    <meta name="google-site-verification" content="{ANALYTICS_CODES['google_site_verification']}" />

    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ANALYTICS_CODES['ga4_main']}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ANALYTICS_CODES['ga4_main']}');
      {''.join([f"gtag('config', '{tag}');" for tag in ANALYTICS_CODES['ga4_tags']])}
    </script>

    <!-- Google Ads -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ANALYTICS_CODES['aw_tag']}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ANALYTICS_CODES['aw_tag']}');
    </script>
"""

def update_service_page_seo(filepath, service_key):
    """Update a service page with premium SEO and analytics"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update meta description
    if service_key in META_DESCRIPTIONS:
        if '<meta name="description"' in content:
            start = content.find('<meta name="description"')
            end = content.find('>', start) + 1
            new_meta = f'<meta name="description" content="{META_DESCRIPTIONS[service_key]}">'
            content = content[:start] + new_meta + content[end:]
    
    # Update page title
    if service_key in SEO_CONTENT:
        if '<title>' in content:
            start = content.find('<title>')
            end = content.find('</title>', start) + 8
            new_title = f'<title>{SEO_CONTENT[service_key]["title"]}</title>'
            content = content[:start] + new_title + content[end:]
        
        # Update H1 heading
        if '<h1>' in content:
            start = content.find('<h1>')
            end = content.find('</h1>', start) + 5
            new_heading = f'<h1>{SEO_CONTENT[service_key]["heading"]}</h1>'
            content = content[:start] + new_heading + content[end:]
        
        # Update service description
        if 'service-description' in content:
            start = content.find('service-description')
            # Find the paragraph after service-description class
            p_start = content.find('<p>', start)
            p_end = content.find('</p>', p_start) + 4
            new_desc = f'<p class="service-description">{SEO_CONTENT[service_key]["description"]}</p>'
            content = content[:p_start] + new_desc + content[p_end:]
    
    # Add analytics to head section
    if '<head>' in content and 'Google Tag Manager' not in content:
        head_end = content.find('</head>')
        analytics_code = generate_analytics_code()
        content = content[:head_end] + analytics_code + content[head_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {service_key}")

def update_all_pages():
    """Update all service pages with premium SEO and analytics"""
    services_dir = './services'
    
    for filename in os.listdir(services_dir):
        if filename.endswith('.html') and not filename.endswith('.backup'):
            filepath = os.path.join(services_dir, filename)
            update_service_page_seo(filepath, filename)
    
    # Also update main pages
    main_pages = ['index.html', 'services.html', 'contact.html', 'about.html', 'service-area.html']
    for page in main_pages:
        if os.path.exists(page):
            update_service_page_seo(page, page)

def create_analytics_folder():
    """Create folder with analytics codes for your dashboard"""
    os.makedirs('analytics-codes', exist_ok=True)
    
    # Create tracking codes file
    with open('analytics-codes/tracking-codes.txt', 'w') as f:
        f.write("WATTS SAFETY INSTALLS - ANALYTICS TRACKING CODES\n")
        f.write("=" * 50 + "\n\n")
        f.write("GOOGLE SITE VERIFICATION:\n")
        f.write(f"{ANALYTICS_CODES['google_site_verification']}\n\n")
        f.write("GA4 MAIN TAG:\n")
        f.write(f"{ANALYTICS_CODES['ga4_main']}\n\n")
        f.write("GA4 ADDITIONAL TAGS:\n")
        for tag in ANALYTICS_CODES['ga4_tags']:
            f.write(f"{tag}\n")
        f.write(f"\nGOOGLE ADS TAG:\n{ANALYTICS_CODES['aw_tag']}\n")
    
    # Create HTML snippet file
    with open('analytics-codes/analytics-snippet.html', 'w') as f:
        f.write("<!-- COPY THIS CODE TO ALL PAGES -->\n")
        f.write(generate_analytics_code())
    
    print("Analytics codes saved to 'analytics-codes' folder")

if __name__ == "__main__":
    print("Updating all pages with premium SEO and analytics...")
    update_all_pages()
    create_analytics_folder()
    print("Complete! All pages updated with:")
    print("✅ 150-character meta descriptions")
    print("✅ SEO-rich visible content") 
    print("✅ All GA4 tracking codes")
    print("✅ Google Search Console verification")
    print("✅ Analytics codes saved to 'analytics-codes' folder")