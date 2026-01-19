import os
import re

# Read ATP homepage as template
with open('index.html', 'r', encoding='utf-8') as f:
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

# Update page title and meta
content = content.replace('Accessibility Contractor Near Me | Watts ATP Contractor | Norfolk NE', 'Home Services Contractor Near Me | Watts Safety Installs | Norfolk NE')
content = content.replace('ATP Approved Contractor near me for ADA ramps, grab bars, wheelchair access, snow removal, lawn care, TV mounting &amp; audio visual services in Norfolk NE.', 'Sister company of Watts ATP Contractor for home remodeling, TV mounting, property maintenance, and general contracting services in Norfolk NE.')

# Update hero section
content = content.replace('Professional Accessibility, Safety &amp; Audio Visual Solutions Near You', 'Professional Home Services &amp; General Contracting Near You')
content = content.replace('Nebraska Licensed #54690-25', 'Sister Company of Watts ATP Contractor • Nebraska Licensed #54690-25')

# Update navigation to point to DBA pages
content = re.sub(r'<a class="logo" href="/">', '<a class="logo" href="/safety-installs/">', content)
content = re.sub(r'<a class="active" href="/">', '<a class="active" href="/safety-installs/">', content)
content = re.sub(r'<a href="/">', '<a href="/safety-installs/">', content)
content = content.replace('href="/services.html"', 'href="/safety-installs/services.html"')
content = content.replace('href="/service-area.html"', 'href="/safety-installs/service-area.html"')
content = content.replace('href="/about.html"', 'href="/safety-installs/about.html"')
content = content.replace('href="/referrals.html"', 'href="/safety-installs/referrals.html"')
content = content.replace('href="/contact.html"', 'href="/safety-installs/contact.html"')

# Update service dropdown links to point to DBA service pages
content = content.replace('href="/services/', 'href="/safety-installs/services/')

# Update about section
content = content.replace('for accessibility modifications, home safety solutions, and professional TV mounting services throughout Nebraska.', 'for home remodeling, property maintenance, TV mounting, and general contracting services throughout Nebraska.')
content = content.replace('We specialize in creating safe, accessible environments for seniors and individuals with mobility challenges, while also providing comprehensive contracting services for all your home improvement and audio visual needs.', 'We specialize in complete home services including remodeling, property maintenance, and general contracting for all your home improvement needs.')

# Update canonical URL
content = re.sub(r'<link rel="canonical" href="https://wattsatpcontractor\.com/"', '<link rel="canonical" href="https://wattsatpcontractor.com/safety-installs/"', content)

# Update service cards - change titles and descriptions for DBA focus
# Accessibility & Safety -> Home Remodeling & Improvements
content = re.sub(
    r'<h3 class="service-title">Accessibility &amp; Safety Solutions</h3>',
    '<h3 class="service-title">Home Remodeling &amp; Improvements</h3>',
    content
)
content = re.sub(
    r'We specialize in creating safe, accessible environments for individuals with mobility challenges\. Our comprehensive solutions include ADA-compliant showers with zero-step entries, commercial-grade grab bars rated for 500\+ lbs, non-slip flooring options, and custom-built accessibility ramps that meet all regulatory requirements\.',
    'Transform your living space with our comprehensive remodeling services. From kitchen and bathroom renovations to deck construction and complete home makeovers, we handle projects of all sizes with precision and care.',
    content
)

# Update section title
content = content.replace('Comprehensive accessibility, safety, and audio visual solutions', 'Complete home services including remodeling, property maintenance, and general contracting')

# Write to DBA location
os.makedirs('safety-installs', exist_ok=True)
with open('safety-installs/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Created DBA homepage with proper formatting and structure")
print("📁 Location: safety-installs/index.html")
print("🔗 Test at: http://localhost:8000/safety-installs/")
