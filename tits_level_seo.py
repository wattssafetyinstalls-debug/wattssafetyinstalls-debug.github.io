#!/usr/bin/env python3
"""
TITS-LEVEL SEO Descriptions - 400+ word premium content optimized for voice search and organic dominance
"""

import os

# TITS-LEVEL 400+ word SEO descriptions
PREMIUM_SEO_CONTENT = {
    'flooring-installation.html': {
        'meta_description': 'Professional flooring installation in Norfolk NE. Hardwood, laminate, vinyl, tile flooring installation services. Quality craftsmanship, free estimates. Call (405) 410-6402.',
        'visible_content': """
            <div class="service-tile">
                <h1>Premium Flooring Installation Services in Norfolk Nebraska</h1>
                <p class="service-description">
                    Transform your Norfolk NE home or business with professional flooring installation services from Watts Safety Installs. As Northeast Nebraska's premier flooring specialists, we provide comprehensive flooring solutions including hardwood floor installation, luxury vinyl plank flooring, durable laminate flooring, ceramic and porcelain tile installation, and commercial-grade carpeting. Our certified flooring installers serve homeowners and businesses throughout Norfolk, Madison, Stanton, Pierce, and surrounding communities with precision craftsmanship and attention to detail that exceeds industry standards.

                    When you choose Watts Safety Installs for your flooring project in Norfolk Nebraska, you're selecting a team that understands the importance of proper subfloor preparation, moisture barrier installation, and expansion gap planning specific to our region's climate conditions. We work with premium materials from trusted manufacturers including Mohawk, Shaw, Bruce, and Armstrong, ensuring your new floors withstand daily wear while enhancing your property's aesthetic appeal and resale value. Our installation process begins with thorough site evaluation and moisture testing, progresses through precise measurement and pattern planning, and culminates with flawless installation and protective finishing.

                    For Norfolk NE homeowners seeking hardwood flooring, we offer both solid wood and engineered wood options with various stain colors and protective coatings that resist scratches and moisture damage. Our laminate flooring installations feature advanced click-lock systems with attached padding for noise reduction and comfort underfoot. Luxury vinyl plank and tile installations provide waterproof durability perfect for bathrooms, kitchens, and basements while mimicking the authentic look of natural wood and stone. Ceramic and porcelain tile installations include proper substrate preparation, precise pattern layout, and commercial-grade grouting for lasting beauty.

                    Beyond residential flooring, we provide commercial flooring solutions for Norfolk NE businesses including durable sheet vinyl for medical facilities, commercial carpet tiles for office spaces, and slip-resistant flooring for retail environments. Our accessibility flooring services include non-slip surfaces for senior safety and ADA-compliant transitions for wheelchair accessibility. Each project includes detailed cost estimates, material selection guidance, precise installation timelines, and comprehensive post-installation cleanup.

                    Voice search optimized: "Hey Google, find flooring installation experts near me in Norfolk Nebraska for hardwood floor installation and vinyl plank flooring services with free estimates and professional installation." Watts Safety Installs answers this search with immediate response and scheduled consultations. Contact our Norfolk NE flooring specialists today at (405) 410-6402 for complimentary flooring assessments and discover how our premium flooring installation services can transform your space with quality, durability, and exceptional craftsmanship that stands the test of time.
                </p>
            </div>
        """
    }
}

def generate_analytics_code():
    """Generate complete analytics tracking code"""
    return """
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-KCPM8VZ');</script>
    <!-- End Google Tag Manager -->

    <!-- Google Search Console Verification -->
    <meta name="google-site-verification" content="9uPoUkPF9bV3aKmaJyxbcnlzzXjxYLkUPb-YXyvOabU" />

    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R7FNGWQVQG"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-R7FNGWQVQG');
      gtag('config', 'G-4BXXKZJZTZ');
      gtag('config', 'G-8TF95LBYRV');
      gtag('config', 'G-B8SKQ9HHPZ');
      gtag('config', 'G-E21ZQ9L9QC');
      gtag('config', 'G-JL3RR3JH55');
      gtag('config', 'G-P2MRLK93YK');
      gtag('config', 'G-PG3KZVYPV0');
      gtag('config', 'G-X6LMX9VR0Y');
    </script>

    <!-- Google Ads -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-586671676"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'AW-586671676');
    </script>
"""

def update_service_page_premium(filepath, service_key):
    """Update service page with TITS-level SEO content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if service_key in PREMIUM_SEO_CONTENT:
        # Update meta description
        if '<meta name="description"' in content:
            start = content.find('<meta name="description"')
            end = content.find('>', start) + 1
            new_meta = f'<meta name="description" content="{PREMIUM_SEO_CONTENT[service_key]["meta_description"]}">'
            content = content[:start] + new_meta + content[end:]
        
        # Replace the entire service tile content
        if '<div class="service-tile">' in content:
            start = content.find('<div class="service-tile">')
            end = content.find('</div><!-- end service-tile -->', start)
            if end == -1:
                end = content.find('</section>', start)
            if end == -1:
                end = content.find('</body>', start)
            
            if end != -1:
                new_content = content[:start] + PREMIUM_SEO_CONTENT[service_key]["visible_content"] + content[end:]
                content = new_content
        
        # Add analytics if not present
        if 'Google Tag Manager' not in content and '<head>' in content:
            head_end = content.find('</head>')
            analytics_code = generate_analytics_code()
            content = content[:head_end] + analytics_code + content[head_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"TITS-LEVEL SEO Updated: {service_key}")
        return True
    
    return False

def update_all_premium_seo():
    """Update all service pages with premium SEO content"""
    services_dir = './services'
    updated_count = 0
    
    for filename in os.listdir(services_dir):
        if filename.endswith('.html') and not filename.endswith('.backup'):
            filepath = os.path.join(services_dir, filename)
            if update_service_page_premium(filepath, filename):
                updated_count += 1
    
    print(f"TITS-LEVEL SEO COMPLETE!")
    print(f"Updated {updated_count} service pages with:")
    print("400+ word premium content")
    print("Voice search optimization") 
    print("Local keyword saturation")
    print("Professional expertise positioning")
    print("Complete analytics integration")
    print("Conversion-focused language")
    print("Your service pages now DOMINATE search results!")

if __name__ == "__main__":
    update_all_premium_seo()