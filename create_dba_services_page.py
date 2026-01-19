import os

# Read the ATP services.html as template
with open('services.html', 'r', encoding='utf-8') as f:
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
content = content.replace('All Services | Watts ATP Contractor', 'Complete Home Services | Watts Safety Installs')
content = content.replace('Complete list of professional services: ADA ramps, grab bars, TV mounting, snow removal, lawn care, remodeling in Norfolk, NE. ATP Approved Contractor.', 'Professional home services including remodeling, TV mounting, property maintenance, and general contracting in Norfolk, NE. Sister company of Watts ATP Contractor.')

# Update hero section
content = content.replace('<h1>All Professional Services</h1>', '<h1>Complete Home Services</h1>')
content = content.replace('ATP Approved Contractor • Nebraska Regd #54690-25 • Serving All Nebraska', 'Sister Company of Watts ATP Contractor • Nebraska Regd #54690-25 • Serving All Nebraska')
content = content.replace('From ADA ramps to TV mounting, snow removal to full remodels — we do it all.', 'From home remodeling to TV mounting, property maintenance to general contracting — we handle it all.')

# Update navigation to point to DBA pages
content = content.replace('href="/"', 'href="/safety-installs/"')
content = content.replace('href="/services.html"', 'href="/safety-installs/services.html"')
content = content.replace('href="/service-area.html"', 'href="/safety-installs/service-area.html"')
content = content.replace('href="/about.html"', 'href="/safety-installs/about.html"')
content = content.replace('href="/referrals.html"', 'href="/safety-installs/referrals.html"')
content = content.replace('href="/contact.html"', 'href="/safety-installs/contact.html"')

# Update service card links to point to DBA service pages
content = content.replace('href="/services/', 'href="/safety-installs/services/')

# Remove Accessibility & Safety card (ATP only)
import re
accessibility_card = re.search(r'<!-- Service Card 1 - Accessibility & Safety -->.*?(?=<!-- Service Card 2)', content, re.DOTALL)
if accessibility_card:
    content = content.replace(accessibility_card.group(0), '')

# Update service cards header
content = content.replace('<h2 class="section-title">Our Comprehensive Services</h2>', '<h2 class="section-title">Complete Home Services</h2>')
content = content.replace('Professional contractor services designed to meet all your home improvement and maintenance needs with precision and care', 'Professional home services for remodeling, property maintenance, and general contracting throughout Norfolk, NE')

# Write to DBA location
os.makedirs('safety-installs', exist_ok=True)
with open('safety-installs/services.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Created DBA services.html with proper formatting and DBA branding")
print("📁 Location: safety-installs/services.html")
