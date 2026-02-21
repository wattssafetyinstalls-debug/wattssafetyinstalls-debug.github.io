#!/usr/bin/env node
/**
 * Town Page Generator — Watts ATP Contractor & Watts Safety Installs
 * Generates service × town landing pages as static HTML for GitHub Pages.
 * Run: node tools/generate-town-pages.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA = JSON.parse(fs.readFileSync(path.join(ROOT, '_data', 'service-areas.json'), 'utf8'));

// ── SERVICE DEFINITIONS ──
const ATP_SERVICES = [
  { slug: 'wheelchair-ramp-installation', name: 'Wheelchair Ramp Installation', short: 'wheelchair ramps',
    desc: 'ADA-compliant wheelchair ramp installation', icon: 'fa-wheelchair-move',
    bullets: ['ADA-compliant design & slope','Pressure-treated lumber or aluminum','Permits & inspections handled','Handrails & non-slip surfaces','Custom sizing for your home'] },
  { slug: 'grab-bar-installation', name: 'Grab Bar Installation', short: 'grab bars',
    desc: 'Professional grab bar installation for bathrooms & showers', icon: 'fa-hand-holding-medical',
    bullets: ['ADA-height placement','Stainless steel & chrome options','Shower, tub & toilet areas','Wall-reinforced mounting','Senior safety focused'] },
  { slug: 'non-slip-flooring-solutions', name: 'Non-Slip Flooring Solutions', short: 'non-slip flooring',
    desc: 'Non-slip flooring installation for safer homes', icon: 'fa-shoe-prints',
    bullets: ['Slip-resistant tile & vinyl','Bathroom & kitchen flooring','Entryway & ramp surfaces','ADA-compliant materials','Professional installation'] },
  { slug: 'bathroom-accessibility', name: 'Bathroom Accessibility Modifications', short: 'bathroom accessibility',
    desc: 'Complete bathroom accessibility modifications', icon: 'fa-bath',
    bullets: ['Walk-in shower conversions','Roll-under vanities','Raised toilet seats','Wider doorways','Full ADA bathroom remodels'] },
  { slug: 'accessibility-safety-solutions', name: 'Accessibility & Safety Solutions', short: 'accessibility solutions',
    desc: 'Complete home accessibility and safety modifications', icon: 'fa-shield-halved',
    bullets: ['Home safety assessments','Stair lifts & ramps','Threshold modifications','Lighting improvements','Full accessibility planning'] },
];

const SI_SERVICES = [
  { slug: 'kitchen-bath-remodeling', name: 'Kitchen & Bath Remodeling', short: 'kitchen & bath remodeling',
    desc: 'Professional kitchen and bathroom remodeling', icon: 'fa-kitchen-set',
    bullets: ['Custom cabinetry & countertops','Tile & flooring installation','Plumbing fixture upgrades','Full kitchen renovations','Bathroom makeovers'] },
  { slug: 'painting', name: 'Interior & Exterior Painting', short: 'painting services',
    desc: 'Professional interior and exterior painting', icon: 'fa-paint-roller',
    bullets: ['Interior wall & ceiling painting','Exterior house painting','Cabinet refinishing','Deck & fence staining','Color consultation'] },
  { slug: 'gutters', name: 'Gutter Installation & Repair', short: 'gutter services',
    desc: 'Gutter installation, repair, and cleaning', icon: 'fa-droplet',
    bullets: ['Seamless gutter installation','Gutter guard systems','Downspout routing','Gutter cleaning & repair','Ice dam prevention'] },
  { slug: 'handyman-services', name: 'Handyman Services', short: 'handyman services',
    desc: 'Reliable handyman services for any home project', icon: 'fa-screwdriver-wrench',
    bullets: ['Drywall repair & patching','Door & window repairs','Shelving & storage','Minor plumbing & electrical','Furniture assembly'] },
  { slug: 'electronics-tv-mounting', name: 'Electronics & TV Mounting', short: 'TV mounting & electronics',
    desc: 'Professional TV mounting and electronics installation', icon: 'fa-tv',
    bullets: ['TV wall mounting','Cable concealment','Surround sound setup','Smart home installation','Network & Wi-Fi setup'] },
];

// ── TOP TOWNS (focus on biggest populations for max SEO impact) ──
function getTopTowns() {
  const allTowns = [];
  for (const county of DATA.serviceArea.nebraska.counties) {
    for (const town of county.towns) {
      allTowns.push({ town, county: county.name, state: 'NE' });
    }
  }
  for (const county of DATA.serviceArea.iowa.counties) {
    for (const town of county.towns) {
      allTowns.push({ town, county: county.name, state: 'IA' });
    }
  }
  // Prioritize larger towns first (hardcoded top ~30 by population)
  const priority = ['Norfolk','Columbus','Fremont','South Sioux City','Sioux City','Wayne','West Point',
    'Albion','O\'Neill','Neligh','Hartington','Creighton','Pierce','Plainview','Schuyler','David City',
    'Wahoo','Blair','Le Mars','Tekamah','Stanton','Madison','Central City','Pender','Ponca',
    'Bloomfield','Tilden','Wisner','Oakland','Crofton'];
  allTowns.sort((a, b) => {
    const ai = priority.indexOf(a.town), bi = priority.indexOf(b.town);
    if (ai !== -1 && bi !== -1) return ai - bi;
    if (ai !== -1) return -1;
    if (bi !== -1) return 1;
    return a.town.localeCompare(b.town);
  });
  return allTowns;
}

function slugify(str) {
  return str.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

// ── ATP PAGE TEMPLATE ──
function atpPage(svc, town) {
  const townSlug = slugify(town.town);
  const stFull = town.state === 'NE' ? 'Nebraska' : 'Iowa';
  const canonical = `https://wattsatpcontractor.com/services/${svc.slug}-${townSlug}-${town.state.toLowerCase()}`;
  const title = `${svc.name} in ${town.town}, ${town.state} | Watts ATP Contractor`;
  const metaDesc = `${svc.name} in ${town.town}, ${stFull}. ADA-compliant, licensed & insured. 5-star rated contractor serving ${town.county}. Free estimates — call (405) 410-6402.`;

  const bullets = svc.bullets.map(b => `<li><i class="fas fa-check" style="color:var(--teal);margin-right:8px"></i>${b}</li>`).join('\n              ');

  const faq = [
    { q: `How much does ${svc.short} cost in ${town.town}?`, a: `Every project is unique. We offer free, no-obligation estimates for ${svc.short} in ${town.town} and all of ${town.county}. Call (405) 410-6402 to schedule yours.` },
    { q: `Do you serve ${town.town}, ${town.state}?`, a: `Yes! ${town.town} is within our 100-mile service radius from Norfolk, NE. We proudly serve all of ${town.county} and surrounding areas.` },
    { q: `Are you licensed and insured?`, a: `Absolutely. Watts ATP Contractor is Nebraska Licensed #54690-25, fully insured, and ATP-approved for accessibility modifications.` },
  ];
  const faqHtml = faq.map(f => `
            <div style="background:#fff;border-radius:12px;padding:20px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,.05)">
              <h3 style="font-size:1rem;color:var(--navy);margin-bottom:8px">${f.q}</h3>
              <p style="color:var(--gray);font-size:.95rem">${f.a}</p>
            </div>`).join('');
  const faqSchema = faq.map(f => `{"@type":"Question","name":"${f.q.replace(/"/g,'\\"')}","acceptedAnswer":{"@type":"Answer","text":"${f.a.replace(/"/g,'\\"')}"}}`).join(',');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>${title}</title>
<meta content="${metaDesc}" name="description"/>
<link href="${canonical}" rel="canonical"/>
<meta content="${title}" property="og:title"/>
<meta content="${metaDesc}" property="og:description"/>
<meta content="${canonical}" property="og:url"/>
<meta content="website" property="og:type"/>
<meta content="index, follow" name="robots"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet"/>
<style>
:root{--teal:#00C4B4;--navy:#0A1D37;--light:#F8FAFC;--gray:#64748B;--gold:#FFD700;--white:#fff;--warm-light:#FEF7ED}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:var(--warm-light);color:#1E293B;line-height:1.7}
header{background:var(--navy);padding:16px 0;position:sticky;top:0;z-index:1000}
.nav-c{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;padding:0 20px}
.logo{font-family:'Playfair Display',serif;font-size:1.6rem;color:var(--teal);text-decoration:none;font-weight:700}
.nav-l{display:flex;gap:20px;align-items:center}
.nav-l a{color:rgba(255,255,255,.85);text-decoration:none;font-size:.9rem;font-weight:500;transition:color .2s}
.nav-l a:hover{color:var(--gold)}
.hero{background:linear-gradient(135deg,var(--navy),#16213e);padding:60px 20px;text-align:center;color:#fff}
.hero h1{font-family:'Playfair Display',serif;font-size:2.2rem;margin-bottom:12px}
.hero p{font-size:1.1rem;color:rgba(255,255,255,.85);max-width:600px;margin:0 auto 24px}
.btn{display:inline-block;background:var(--teal);color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:600;font-size:1rem;transition:all .2s}
.btn:hover{background:#009e91;transform:translateY(-1px)}
.content{max-width:900px;margin:0 auto;padding:40px 20px}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:24px;box-shadow:0 4px 16px rgba(0,0,0,.06)}
.card h2{font-size:1.4rem;color:var(--navy);margin-bottom:16px}
.card ul{list-style:none;padding:0}
.card li{padding:8px 0;font-size:.95rem;color:#444}
.faq{margin-top:24px}
.cta-box{background:linear-gradient(135deg,var(--teal),#009e91);border-radius:16px;padding:40px;text-align:center;color:#fff;margin:32px 0}
.cta-box h2{font-size:1.6rem;margin-bottom:12px}
.cta-box a{color:#fff;text-decoration:none;font-size:1.3rem;font-weight:700}
footer{background:var(--navy);color:rgba(255,255,255,.7);text-align:center;padding:24px;font-size:.85rem;margin-top:auto}
footer a{color:var(--gold);text-decoration:none}
@media(max-width:600px){.hero h1{font-size:1.6rem}.nav-l{display:none}}
</style>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","name":"${svc.name} in ${town.town}, ${town.state}","provider":{"@type":"LocalBusiness","name":"Watts ATP Contractor","telephone":"(405) 410-6402","address":{"@type":"PostalAddress","streetAddress":"507 West Omaha Ave Suite B","addressLocality":"Norfolk","addressRegion":"NE","postalCode":"68701"},"areaServed":{"@type":"City","name":"${town.town}","containedInPlace":{"@type":"AdministrativeArea","name":"${town.county}, ${stFull}"}},"aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"12"}},"description":"${metaDesc}"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[${faqSchema}]}
</script>
</head>
<body>
<header>
  <div class="nav-c">
    <a class="logo" href="/">Watts ATP</a>
    <nav class="nav-l">
      <a href="/services">Services</a>
      <a href="/service-area">Service Area</a>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
    </nav>
  </div>
</header>

<section class="hero">
  <h1>${svc.name} in ${town.town}, ${town.state}</h1>
  <p>Licensed, insured & ATP-approved. Serving ${town.town} and all of ${town.county} with professional ${svc.short}. 5-star rated.</p>
  <a class="btn" href="tel:+14054106402"><i class="fas fa-phone" style="margin-right:8px"></i>Get Your Free Estimate</a>
</section>

<div class="content">
  <div class="card">
    <h2><i class="fas ${svc.icon}" style="color:var(--teal);margin-right:10px"></i>What We Offer in ${town.town}</h2>
    <p style="margin-bottom:16px;color:var(--gray)">Watts ATP Contractor provides professional ${svc.short} to homeowners in ${town.town}, ${stFull} and throughout ${town.county}. As a licensed Nebraska contractor (#54690-25), we deliver quality workmanship backed by our 5-star reputation.</p>
    <ul>
      ${bullets}
    </ul>
  </div>

  <div class="card">
    <h2>Why Choose Watts ATP Contractor?</h2>
    <ul>
      <li><i class="fas fa-star" style="color:var(--gold);margin-right:8px"></i><strong>5.0-Star Rating</strong> — 12 verified reviews</li>
      <li><i class="fas fa-id-card" style="color:var(--teal);margin-right:8px"></i><strong>Nebraska Licensed #54690-25</strong> — Fully insured</li>
      <li><i class="fas fa-map-marker-alt" style="color:var(--teal);margin-right:8px"></i><strong>100-Mile Service Radius</strong> — ${town.town} is in our coverage area</li>
      <li><i class="fas fa-clipboard-check" style="color:var(--teal);margin-right:8px"></i><strong>ATP Approved</strong> — Certified accessibility contractor</li>
      <li><i class="fas fa-dollar-sign" style="color:var(--teal);margin-right:8px"></i><strong>Free Estimates</strong> — No obligation, no pressure</li>
    </ul>
  </div>

  <div class="faq">
    <h2 style="font-size:1.4rem;color:var(--navy);margin-bottom:16px">Frequently Asked Questions</h2>
    ${faqHtml}
  </div>

  <div class="cta-box">
    <h2>Ready for ${svc.name} in ${town.town}?</h2>
    <p style="margin-bottom:16px;opacity:.9">Call today for a free, no-obligation estimate. Justin will personally handle your project.</p>
    <a href="tel:+14054106402"><i class="fas fa-phone"></i> (405) 410-6402</a>
  </div>
</div>

<footer>
  <p>&copy; ${new Date().getFullYear()} Watts ATP Contractor — ATP Approved Contractor — Nebraska Licensed #54690-25</p>
  <p style="margin-top:6px"><a href="/">Home</a> · <a href="/services">Services</a> · <a href="/contact">Contact</a></p>
</footer>
<script src="/js/watts-ai-chat.js" defer></script>
</body>
</html>`;
}

// ── SAFETY INSTALLS PAGE TEMPLATE ──
function siPage(svc, town) {
  const townSlug = slugify(town.town);
  const stFull = town.state === 'NE' ? 'Nebraska' : 'Iowa';
  const canonical = `https://wattsatpcontractor.com/safety-installs/services/${svc.slug}-${townSlug}-${town.state.toLowerCase()}`;
  const title = `${svc.name} in ${town.town}, ${town.state} | Watts Safety Installs`;
  const metaDesc = `${svc.name} in ${town.town}, ${stFull}. Professional home services, licensed & insured. Serving ${town.county}. Free estimates — call (405) 410-6402.`;

  const bullets = svc.bullets.map(b => `<li><i class="fas fa-check" style="color:var(--red);margin-right:8px"></i>${b}</li>`).join('\n              ');

  const faq = [
    { q: `How much does ${svc.short} cost in ${town.town}?`, a: `Every project is unique. We offer free, no-obligation estimates for ${svc.short} in ${town.town} and all of ${town.county}. Call (405) 410-6402 to schedule yours.` },
    { q: `Do you serve ${town.town}, ${town.state}?`, a: `Yes! ${town.town} is within our 100-mile service radius from Norfolk, NE. We proudly serve all of ${town.county} and surrounding areas.` },
    { q: `Are you licensed and insured?`, a: `Absolutely. Watts Safety Installs is Nebraska Licensed #54690-25, fully insured, and committed to quality home services.` },
  ];
  const faqHtml = faq.map(f => `
            <div style="background:#fff;border-radius:12px;padding:20px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,.05)">
              <h3 style="font-size:1rem;color:var(--black);margin-bottom:8px">${f.q}</h3>
              <p style="color:var(--gray);font-size:.95rem">${f.a}</p>
            </div>`).join('');
  const faqSchema = faq.map(f => `{"@type":"Question","name":"${f.q.replace(/"/g,'\\"')}","acceptedAnswer":{"@type":"Answer","text":"${f.a.replace(/"/g,'\\"')}"}}`).join(',');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>${title}</title>
<meta content="${metaDesc}" name="description"/>
<link href="${canonical}" rel="canonical"/>
<meta content="${title}" property="og:title"/>
<meta content="${metaDesc}" property="og:description"/>
<meta content="${canonical}" property="og:url"/>
<meta content="website" property="og:type"/>
<meta content="index, follow" name="robots"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet"/>
<style>
:root{--red:#dc2626;--black:#1a1a1a;--light:#F8FAFC;--gray:#64748B;--cream:#f5f5dc;--white:#fff;--warm-light:#FEF7ED}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:var(--warm-light);color:#1E293B;line-height:1.7}
header{background:var(--black);padding:16px 0;position:sticky;top:0;z-index:1000}
.nav-c{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;padding:0 20px}
.logo{font-family:'Playfair Display',serif;font-size:1.6rem;color:var(--red);text-decoration:none;font-weight:700}
.nav-l{display:flex;gap:20px;align-items:center}
.nav-l a{color:rgba(255,255,255,.85);text-decoration:none;font-size:.9rem;font-weight:500;transition:color .2s}
.nav-l a:hover{color:var(--cream)}
.hero{background:linear-gradient(135deg,var(--black),#2d2d2d);padding:60px 20px;text-align:center;color:#fff}
.hero h1{font-family:'Playfair Display',serif;font-size:2.2rem;margin-bottom:12px;color:var(--cream)}
.hero p{font-size:1.1rem;color:rgba(255,255,255,.85);max-width:600px;margin:0 auto 24px}
.btn{display:inline-block;background:var(--red);color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:600;font-size:1rem;transition:all .2s}
.btn:hover{background:#b91c1c;transform:translateY(-1px)}
.content{max-width:900px;margin:0 auto;padding:40px 20px}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:24px;box-shadow:0 4px 16px rgba(0,0,0,.06)}
.card h2{font-size:1.4rem;color:var(--black);margin-bottom:16px}
.card ul{list-style:none;padding:0}
.card li{padding:8px 0;font-size:.95rem;color:#444}
.faq{margin-top:24px}
.cta-box{background:linear-gradient(135deg,var(--red),#b91c1c);border-radius:16px;padding:40px;text-align:center;color:#fff;margin:32px 0}
.cta-box h2{font-size:1.6rem;margin-bottom:12px}
.cta-box a{color:#fff;text-decoration:none;font-size:1.3rem;font-weight:700}
footer{background:var(--black);color:rgba(255,255,255,.7);text-align:center;padding:24px;font-size:.85rem;margin-top:auto}
footer a{color:var(--cream);text-decoration:none}
@media(max-width:600px){.hero h1{font-size:1.6rem}.nav-l{display:none}}
</style>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","name":"${svc.name} in ${town.town}, ${town.state}","provider":{"@type":"LocalBusiness","name":"Watts Safety Installs","telephone":"(405) 410-6402","address":{"@type":"PostalAddress","streetAddress":"507 West Omaha Ave Suite B","addressLocality":"Norfolk","addressRegion":"NE","postalCode":"68701"},"areaServed":{"@type":"City","name":"${town.town}","containedInPlace":{"@type":"AdministrativeArea","name":"${town.county}, ${stFull}"}}}},"description":"${metaDesc}"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[${faqSchema}]}
</script>
</head>
<body>
<header>
  <div class="nav-c">
    <a class="logo" href="/safety-installs/">Safety Installs</a>
    <nav class="nav-l">
      <a href="/safety-installs/services">Services</a>
      <a href="/safety-installs/service-area">Service Area</a>
      <a href="/safety-installs/about">About</a>
      <a href="/safety-installs/contact">Contact</a>
    </nav>
  </div>
</header>

<section class="hero">
  <h1>${svc.name} in ${town.town}, ${town.state}</h1>
  <p>Professional home services, licensed & insured. Serving ${town.town} and all of ${town.county}.</p>
  <a class="btn" href="tel:+14054106402"><i class="fas fa-phone" style="margin-right:8px"></i>Get Your Free Estimate</a>
</section>

<div class="content">
  <div class="card">
    <h2><i class="fas ${svc.icon}" style="color:var(--red);margin-right:10px"></i>What We Offer in ${town.town}</h2>
    <p style="margin-bottom:16px;color:var(--gray)">Watts Safety Installs provides professional ${svc.short} to homeowners in ${town.town}, ${stFull} and throughout ${town.county}. As a licensed Nebraska contractor (#54690-25), we deliver quality workmanship you can trust.</p>
    <ul>
      ${bullets}
    </ul>
  </div>

  <div class="card">
    <h2>Why Choose Watts Safety Installs?</h2>
    <ul>
      <li><i class="fas fa-id-card" style="color:var(--red);margin-right:8px"></i><strong>Nebraska Licensed #54690-25</strong> — Fully insured</li>
      <li><i class="fas fa-map-marker-alt" style="color:var(--red);margin-right:8px"></i><strong>100-Mile Service Radius</strong> — ${town.town} is in our coverage area</li>
      <li><i class="fas fa-home" style="color:var(--red);margin-right:8px"></i><strong>Professional Home Services</strong> — Quality you can count on</li>
      <li><i class="fas fa-dollar-sign" style="color:var(--red);margin-right:8px"></i><strong>Free Estimates</strong> — No obligation, no pressure</li>
    </ul>
  </div>

  <div class="faq">
    <h2 style="font-size:1.4rem;color:var(--black);margin-bottom:16px">Frequently Asked Questions</h2>
    ${faqHtml}
  </div>

  <div class="cta-box">
    <h2>Ready for ${svc.name} in ${town.town}?</h2>
    <p style="margin-bottom:16px;opacity:.9">Call today for a free, no-obligation estimate. Justin will personally handle your project.</p>
    <a href="tel:+14054106402"><i class="fas fa-phone"></i> (405) 410-6402</a>
  </div>
</div>

<footer>
  <p>&copy; ${new Date().getFullYear()} Watts Safety Installs — Professional Home Services — Nebraska Licensed #54690-25</p>
  <p style="margin-top:6px"><a href="/safety-installs/">Home</a> · <a href="/safety-installs/services">Services</a> · <a href="/safety-installs/contact">Contact</a></p>
</footer>
<script src="/js/watts-ai-chat.js" defer></script>
</body>
</html>`;
}

// ── GENERATE ──
function run() {
  const towns = getTopTowns();
  // Generate for top 25 towns to keep it manageable (= 250 ATP pages + 125 SI pages)
  const topTowns = towns.slice(0, 25);
  let atpCount = 0, siCount = 0;
  const sitemapEntries = [];

  // ATP service pages
  const atpDir = path.join(ROOT, 'services');
  if (!fs.existsSync(atpDir)) fs.mkdirSync(atpDir, { recursive: true });

  for (const svc of ATP_SERVICES) {
    for (const town of topTowns) {
      const slug = `${svc.slug}-${slugify(town.town)}-${town.state.toLowerCase()}`;
      const file = path.join(atpDir, `${slug}.html`);
      fs.writeFileSync(file, atpPage(svc, town), 'utf8');
      sitemapEntries.push(`https://wattsatpcontractor.com/services/${slug}`);
      atpCount++;
    }
  }

  // SI service pages
  const siDir = path.join(ROOT, 'safety-installs', 'services');
  if (!fs.existsSync(siDir)) fs.mkdirSync(siDir, { recursive: true });

  for (const svc of SI_SERVICES) {
    for (const town of topTowns) {
      const slug = `${svc.slug}-${slugify(town.town)}-${town.state.toLowerCase()}`;
      const file = path.join(siDir, `${slug}.html`);
      fs.writeFileSync(file, siPage(svc, town), 'utf8');
      sitemapEntries.push(`https://wattsatpcontractor.com/safety-installs/services/${slug}`);
      siCount++;
    }
  }

  // Generate index pages for /services/ and /safety-installs/services/
  generateAtpIndex(atpDir, topTowns);
  generateSiIndex(siDir, topTowns);

  // Append to sitemap.xml
  appendSitemap(sitemapEntries);

  console.log(`\n✅ Generated ${atpCount} ATP town pages in /services/`);
  console.log(`✅ Generated ${siCount} Safety Installs town pages in /safety-installs/services/`);
  console.log(`✅ Updated sitemap.xml with ${sitemapEntries.length} new URLs`);
  console.log(`\nTotal: ${atpCount + siCount} landing pages created!`);
}

function generateAtpIndex(dir, towns) {
  const links = [];
  for (const svc of ATP_SERVICES) {
    links.push(`<h3 style="margin:24px 0 12px;color:var(--navy)">${svc.name}</h3>`);
    for (const t of towns) {
      const slug = `${svc.slug}-${slugify(t.town)}-${t.state.toLowerCase()}`;
      links.push(`<a href="/services/${slug}" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid #e5e5e5;border-radius:8px;text-decoration:none;color:#333;font-size:.9rem">${t.town}, ${t.state}</a>`);
    }
  }
  const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>All Service Areas | Watts ATP Contractor</title>
<meta content="Browse all Watts ATP Contractor service areas across Nebraska and Iowa. Wheelchair ramps, grab bars, accessibility solutions in your town." name="description"/>
<link href="https://wattsatpcontractor.com/services/" rel="canonical"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet"/>
<style>:root{--teal:#00C4B4;--navy:#0A1D37;--gold:#FFD700;--warm-light:#FEF7ED}*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter',sans-serif;background:var(--warm-light);color:#1E293B;line-height:1.7}header{background:var(--navy);padding:16px 0}.nav-c{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;padding:0 20px}.logo{font-family:'Playfair Display',serif;font-size:1.6rem;color:var(--teal);text-decoration:none;font-weight:700}.content{max-width:1000px;margin:0 auto;padding:40px 20px}footer{background:var(--navy);color:rgba(255,255,255,.7);text-align:center;padding:24px;font-size:.85rem}footer a{color:var(--gold);text-decoration:none}</style>
</head><body>
<header><div class="nav-c"><a class="logo" href="/">Watts ATP</a></div></header>
<div class="content">
<h1 style="font-family:'Playfair Display',serif;font-size:2rem;margin-bottom:8px">Service Areas</h1>
<p style="color:#64748B;margin-bottom:24px">We serve 25+ towns across Nebraska and Iowa. Find your town below.</p>
${links.join('\n')}
</div>
<footer><p>&copy; ${new Date().getFullYear()} Watts ATP Contractor — Nebraska Licensed #54690-25</p></footer>
<script src="/js/watts-ai-chat.js" defer></script>
</body></html>`;
  fs.writeFileSync(path.join(dir, 'index.html'), html, 'utf8');
}

function generateSiIndex(dir, towns) {
  const links = [];
  for (const svc of SI_SERVICES) {
    links.push(`<h3 style="margin:24px 0 12px;color:var(--black)">${svc.name}</h3>`);
    for (const t of towns) {
      const slug = `${svc.slug}-${slugify(t.town)}-${t.state.toLowerCase()}`;
      links.push(`<a href="/safety-installs/services/${slug}" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid #e5e5e5;border-radius:8px;text-decoration:none;color:#333;font-size:.9rem">${t.town}, ${t.state}</a>`);
    }
  }
  const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>All Service Areas | Watts Safety Installs</title>
<meta content="Browse all Watts Safety Installs service areas across Nebraska and Iowa. Remodeling, painting, handyman, gutters and more in your town." name="description"/>
<link href="https://wattsatpcontractor.com/safety-installs/services/" rel="canonical"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet"/>
<style>:root{--red:#dc2626;--black:#1a1a1a;--cream:#f5f5dc;--warm-light:#FEF7ED}*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter',sans-serif;background:var(--warm-light);color:#1E293B;line-height:1.7}header{background:var(--black);padding:16px 0}.nav-c{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;padding:0 20px}.logo{font-family:'Playfair Display',serif;font-size:1.6rem;color:var(--red);text-decoration:none;font-weight:700}.content{max-width:1000px;margin:0 auto;padding:40px 20px}footer{background:var(--black);color:rgba(255,255,255,.7);text-align:center;padding:24px;font-size:.85rem}footer a{color:var(--cream);text-decoration:none}</style>
</head><body>
<header><div class="nav-c"><a class="logo" href="/safety-installs/">Safety Installs</a></div></header>
<div class="content">
<h1 style="font-family:'Playfair Display',serif;font-size:2rem;margin-bottom:8px">Service Areas</h1>
<p style="color:#64748B;margin-bottom:24px">We serve 25+ towns across Nebraska and Iowa. Find your town below.</p>
${links.join('\n')}
</div>
<footer><p>&copy; ${new Date().getFullYear()} Watts Safety Installs — Professional Home Services — Nebraska Licensed #54690-25</p></footer>
<script src="/js/watts-ai-chat.js" defer></script>
</body></html>`;
  fs.writeFileSync(path.join(dir, 'index.html'), html, 'utf8');
}

function appendSitemap(entries) {
  const smPath = path.join(ROOT, 'sitemap.xml');
  if (!fs.existsSync(smPath)) return;
  let sm = fs.readFileSync(smPath, 'utf8');
  const today = new Date().toISOString().split('T')[0];
  const newEntries = entries.map(url => `  <url>\n    <loc>${url}</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>`).join('\n');
  sm = sm.replace('</urlset>', newEntries + '\n</urlset>');
  fs.writeFileSync(smPath, sm, 'utf8');
}

run();
