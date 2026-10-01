// Generates the 11 AmeriGlide lift product landing pages (Phase 2+3).
// Run: node tools/gen-lift-product-pages.js  (writes into repo root)
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');

const P = [
  // ---------------- STRAIGHT ----------------
  {
    file: 'stair-lift-rave-2.html', name: 'AmeriGlide Rave 2', cat: 'Straight Stair Lift',
    catPage: '/straight-stair-lifts.html', catName: 'Straight Stair Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/AmeriGlide---Rave-2.html',
    img: 'https://media.ameriglide.com/blobs/4b/4bba7b3bb51cb7987a704306e99e7e1f.jpg',
    imgAlt: 'AmeriGlide Rave 2 stair lift key features',
    tagline: 'The ultra-compact straight stair lift — 350 lb capacity, folds to just over 11 inches, and keeps running in a power outage.',
    specs: [
      ['Weight capacity', '350 lbs'],
      ['Folded width', 'Just over 11 inches — stairs stay usable'],
      ['Rail mounting', 'Mounts to the steps, not the wall'],
      ['Power', 'Battery (DC) — charges at top or bottom of track, works in outages'],
      ['Controls', 'Arm-mounted switch + call/send remotes'],
      ['Safety', 'Obstruction sensors, swivel seat for safe top exit'],
      ['Build', 'All-metal case construction, assembled in the USA'],
      ['Install', 'Single-bracket contact points — faster, cleaner install'],
    ],
    blurb: 'The Rave 2 is the pick for narrow staircases — the seat, arms, and footrest fold so slim that everyday stair traffic barely notices it. Battery power means a Nebraska ice storm can\'t leave you stranded, and the step-mounted rail keeps your walls untouched.',
  },
  {
    file: 'stair-lift-cardinal-indoor.html', name: 'Cardinal Indoor Straight Stair Lift', cat: 'Straight Stair Lift',
    catPage: '/straight-stair-lifts.html', catName: 'Straight Stair Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/Cardinal-Indoor-Straight-Stair-Lift.html',
    img: 'https://media.ameriglide.com/blobs/a4/a493e123b28172ec07998bfde5e0738a.jpg',
    imgAlt: 'Cardinal Indoor stair lift selling points',
    tagline: 'Simple, dependable straight lift — diagnostic display, retractable seatbelt, and key lockout for family-proof safety.',
    specs: [
      ['Weight capacity', '300 lbs'],
      ['Display', 'Digital diagnostic display with backlit status text'],
      ['Seat', 'Swivel seat (powered option available), removable washable covers'],
      ['Safety', 'Retractable seatbelt, stop sensors, key lockout'],
      ['Controls', 'Remote controls included as standard'],
      ['Footprint', 'Chair + footrest fold flat to keep stairs open'],
      ['Power', 'Battery (DC) operation'],
    ],
    blurb: 'The Cardinal keeps it simple without cutting corners — the backlit diagnostic display tells you the lift\'s status at a glance, and the two-key lockout stops curious grandkids from taking rides.',
  },
  // ---------------- CURVED ----------------
  {
    file: 'curved-stair-lift-infinity.html', name: 'AmeriGlide Infinity Curved Stair Lift', cat: 'Curved Stair Lift',
    catPage: '/curved-stair-lifts.html', catName: 'Curved Stair Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/AmeriGlide---Infinity-Curved-Stair-Lift.html',
    img: 'https://media.ameriglide.com/blobs/94/9481fc08feec04098d1081b75caae977.jpg',
    imgAlt: 'AmeriGlide Infinity curved stair lift selling points',
    tagline: 'AmeriGlide\'s flagship curved lift — a rail custom-engineered to your staircase\'s exact turns and landings.',
    specs: [
      ['Rail', 'Custom curved rail built to your staircase measurements'],
      ['Weight capacity', 'Up to ~300 lbs class'],
      ['Seat', 'Folding seat and footrest — maximizes staircase space'],
      ['Display', 'Digital diagnostic display with backlit status text'],
      ['Controls', 'Ergonomic lever controls + swivel seat'],
      ['Power', 'Battery (DC) with automatic charging'],
      ['Install', 'Factory-trained installer required — that\'s us'],
    ],
    blurb: 'Turns, landings, pie-shaped steps — the Infinity\'s rail is drawn for your staircase and your staircase only. That\'s why every curved job starts with our on-site measurement visit: the photos and measurements we take feed the CAD drawings the rail is bent from.',
  },
  {
    file: 'curved-stair-lift-rave-curved-hd.html', name: 'AmeriGlide Rave Curved HD Stair Lift', cat: 'Curved Stair Lift',
    catPage: '/curved-stair-lifts.html', catName: 'Curved Stair Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/AmeriGlide---Rave-Curved-HD-Stair-Lift.html',
    img: 'https://media.ameriglide.com/blobs/a4/a437b66ff86e99fb2ae988bc4af92504.jpg',
    imgAlt: 'AmeriGlide Rave Curved HD stair lift in use',
    tagline: 'The heavy-duty curved lift — 90°, 180°, spiral, and multi-story staircases, assembled in the USA with a True-Curve rail.',
    specs: [
      ['Weight capacity', '300+ lbs heavy-duty class'],
      ['Rail', 'True-Curve precision-bent steel — smoother turns'],
      ['Measuring', 'Calibrated camera-kit digital measurement'],
      ['Seat', 'Ergonomic swivel seat with flip-up arms'],
      ['Options', 'Custom colors and fabrics available'],
      ['Staircases', '90° turns, 180° turns, spirals, multi-story'],
      ['Build', 'Assembled in the USA; narrow profile, quiet ride'],
      ['Install', 'Simple-connect rails for faster professional install'],
    ],
    blurb: 'When a staircase does more than go straight — or you need the extra capacity — the Rave Curved HD is the heavy hitter. The rail is measured with a calibrated camera kit, bent in the factory, and arrives ready for a clean install.',
  },
  // ---------------- VPLs ----------------
  {
    file: 'vpl-nano-quick-ship.html', name: 'AmeriGlide Nano VPL (Quick Ship)', cat: 'Vertical Platform Lift',
    catPage: '/vertical-platform-lifts.html', catName: 'Vertical Platform Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/nano-qs_ag.html',
    img: 'https://media.ameriglide.com/blobs/f3/f33df9819e2e05f295d2931608cd30e7.jpg',
    imgAlt: 'Nano vertical platform lift installed under a shelter',
    tagline: 'The slimmest, best-looking VPL tower on the market — plug-and-play design, quick-ship availability.',
    specs: [
      ['Design', 'Market\'s slimmest tower — most attractive footprint'],
      ['Construction', 'Automotive-grade steel'],
      ['Install', 'Plug-n-play design; reversible left/right tower'],
      ['Listing', 'ASME / QAI listed'],
      ['Availability', 'Quick-Ship configuration'],
      ['Use', 'Residential porches, decks, trailers, garages'],
    ],
    blurb: 'The Nano is the answer when you want a porch lift that doesn\'t look like industrial equipment — the slim tower blends in, and the plug-and-play build makes it one of the fastest VPL installs we do.',
  },
  {
    file: 'vpl-hercules-mini.html', name: 'AmeriGlide Hercules Mini VPL', cat: 'Vertical Platform Lift',
    catPage: '/vertical-platform-lifts.html', catName: 'Vertical Platform Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/AmeriGlide---Hercules-Mini.html',
    img: 'https://media.ameriglide.com/blobs/89/892f97ed47cb2247877fcf7d3be935a0.jpg',
    imgAlt: 'Hercules Mini VPL installed in a garage',
    tagline: 'Compact 30-inch VPL with full 750 lb capacity — the garage and low-porch specialist.',
    specs: [
      ['Weight capacity', '750 lbs — lifts a large chair plus a second person'],
      ['Lift height', '30″ max (quick-ship); heights to 160″ available as upgrades'],
      ['Platform', '36″ × 54″ non-skid epoxy-coated floor'],
      ['Drive', 'Acme screw direct drive — smoothest, quietest on the market'],
      ['Weather', 'Galvanized steel panels — outdoor-rated in harsh conditions'],
      ['Safety', 'Under-platform obstruction detection, e-stop, alarm'],
      ['Options', 'Upper landing gate, interlocks, extra call/send stations'],
    ],
    blurb: 'Don\'t let "Mini" fool you — it carries 750 pounds. For low porches, garage entries, and decks under 30 inches of rise, the Hercules Mini is the no-ramp-needed answer.',
  },
  {
    file: 'vpl-hercules-750-residential.html', name: 'AmeriGlide Hercules 750 Residential VPL', cat: 'Vertical Platform Lift',
    catPage: '/vertical-platform-lifts.html', catName: 'Vertical Platform Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/AmeriGlide---Hercules-750-Residential.html',
    img: 'https://media.ameriglide.com/blobs/a4/a4037e9022d439d8bfdc91a6b420b88e.jpg',
    imgAlt: 'Hercules 750 residential VPL installed beside a house',
    tagline: 'The workhorse home VPL — 750 lb standard capacity (1,000 lb option), heights to 160 inches, works in power outages.',
    specs: [
      ['Weight capacity', '750 lbs standard · 1,000 lb option'],
      ['Lift heights', '64″ shown; 44″ to 160″ configurations available'],
      ['Drive', 'Acme screw direct drive — smooth and quiet'],
      ['Power', 'Battery (DC) — operates during power outages'],
      ['Ramp', 'Automatic self-lowering folding ramp (standard)'],
      ['Weather', 'Galvanized steel, non-skid epoxy floor — outdoor rated'],
      ['Safety', 'Under-platform obstruction detection, e-stop, alarm'],
      ['Options', 'Canopy, gates, interlocks, DC power upgrades'],
    ],
    blurb: 'Tall porch? Second-story deck? The Hercules 750 family goes up to 160 inches of lift — and being battery powered, it keeps working when the power doesn\'t.',
  },
  {
    file: 'vpl-hercules-750-portable.html', name: 'AmeriGlide Hercules 750 Portable VPL', cat: 'Vertical Platform Lift',
    catPage: '/vertical-platform-lifts.html', catName: 'Vertical Platform Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/AmeriGlide---Hercules-750-Portable.html',
    img: 'https://media.ameriglide.com/blobs/7c/7c13119cc5a79c02b56da331d7bbcf16.jpg',
    imgAlt: 'Hercules 750 portable VPL lifted outside a building',
    tagline: 'Heavy-duty lifting that moves with you — retractable casters let one lift serve multiple locations.',
    specs: [
      ['Weight capacity', '750 lbs'],
      ['Lift heights', '44″ and 64″'],
      ['Mobility', 'Retractable casters + adjustable stabilizing screws'],
      ['Drive', 'Acme screw direct drive — smooth, quiet'],
      ['Power', 'Battery (DC) with battery backup'],
      ['Use', 'Homes, events, stages, churches — anywhere access moves'],
      ['Safety', 'Under-platform obstruction detection, e-stop, alarm'],
    ],
    blurb: 'Need wheelchair access in more than one spot — or only sometimes? The Portable rolls where it\'s needed on retractable casters, stabilizes, and lifts 750 pounds like it never moved.',
  },
  {
    file: 'vpl-hercules-750-commercial.html', name: 'AmeriGlide Hercules 750 Commercial VPL (Quick Ship)', cat: 'Vertical Platform Lift',
    catPage: '/vertical-platform-lifts.html', catName: 'Vertical Platform Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/AmeriGlide-Hercules-750---Commercial---Quick-Ship.html',
    img: 'https://media.ameriglide.com/blobs/8f/8f7bec30028ac0cb3678761217f3a680.jpg',
    imgAlt: 'Hercules 750 commercial VPL installed at an office',
    tagline: 'Turnkey commercial access — platform and upper-landing gates plus call/send stations included, quick-ship ready.',
    specs: [
      ['Weight capacity', '750 lbs'],
      ['Lift heights', '64″ shown; 44″ to 130″ available'],
      ['Included', 'Platform gate, upper landing gate, call/send both levels'],
      ['Drive', 'Acme screw direct drive'],
      ['Power', 'Battery (DC) — works during outages'],
      ['Rated', 'Commercial applications — businesses, churches, municipal buildings'],
      ['Safety', 'Obstruction detection, e-stop, alarm, ASME/QAI listed'],
    ],
    blurb: 'For businesses, churches, and public buildings that need code-aware wheelchair access without an elevator — this ships as a turnkey package with gates and call stations included.',
  },
  {
    file: 'vpl-stratos-residential.html', name: 'Stratos VPL — Residential', cat: 'Vertical Platform Lift',
    catPage: '/vertical-platform-lifts.html', catName: 'Vertical Platform Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/Stratos-VPL---Residential.html',
    img: 'https://media.ameriglide.com/blobs/94/940edfb4debc53933e1e4eeaf2fed65e.jpg',
    imgAlt: 'Stratos residential vertical platform lift',
    tagline: 'The next-generation home VPL — Guardian diagnostic lights, SteadyDrive smoothness, and true battery backup.',
    specs: [
      ['Generation', 'Next-gen VPL — easier to use, service, and troubleshoot'],
      ['Diagnostics', 'Guardian System — 4 LED status lights report system health'],
      ['Drive', 'SteadyDrive — smooth, quiet, stable lift'],
      ['Backup', 'ReadyUPS battery backup option — 5+ cycles in a power outage'],
      ['Ratings', 'ETL listed; residential + light commercial rated'],
      ['Heights', 'Multiple lift-height configurations'],
    ],
    blurb: 'The Stratos is the "smart" VPL — its Guardian LED system tells you what the lift is doing before you ever have to guess, and the ReadyUPS backup keeps it cycling through outages.',
  },
  {
    file: 'vpl-stratos-commercial.html', name: 'Stratos VPL — Commercial', cat: 'Vertical Platform Lift',
    catPage: '/vertical-platform-lifts.html', catName: 'Vertical Platform Lifts',
    mfrUrl: 'https://www.ameriglide.com/item/Stratos-VPL---Commercial.html',
    img: 'https://media.ameriglide.com/blobs/5d/5da424521b3f9d12b13b5af99fef2228.jpg',
    imgAlt: 'Stratos commercial VPL, side view',
    tagline: 'Commercial-rated Stratos — ETL listed, ASME A18.1 compliant, built for public-access duty.',
    specs: [
      ['Certifications', 'ETL listed · CSA B44.1 / ASME A17.5 · ASME A18.1'],
      ['Rated', 'Commercial AND residential duty'],
      ['Diagnostics', 'Guardian System — 4 LED status indicators'],
      ['Drive', 'SteadyDrive — smooth, quiet, stable'],
      ['Backup', 'ReadyUPS true battery backup option'],
      ['Heights', 'Multiple configurations for commercial rises'],
    ],
    blurb: 'When a storefront, office, or facility needs real accessibility compliance, the commercial Stratos carries the certifications to back it up — ASME A18.1, ETL listing, and a battery backup that keeps the door open during outages.',
  },
];

function productPage(p) {
  const kw = p.name.toLowerCase().replace(/[^a-z0-9 ]/g,'').split(' ').join(', ') + ', Norfolk NE, AmeriGlide dealer, installed price';
  const rows = p.specs.map(([k,v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join('\n');
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>${p.name} | Installed by Watts ATP | Norfolk NE</title>
<meta content="${p.name} sold &amp; installed by certified AmeriGlide dealer Watts ATP Contractor — Norfolk NE. ${p.tagline.replace(/&/g,'&amp;').replace(/"/g,'&quot;').slice(0,120)} Dealer pricing quote — (405) 410-6402." name="description"/>
<link href="https://wattsatpcontractor.com/${p.file.replace('.html','')}" rel="canonical"/>
<meta content="${kw}" name="keywords"/>
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48"/>
<link rel="manifest" href="/manifest.json"/>
<meta name="theme-color" content="#0A1D37"/>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-KCPM8VZ');</script>
<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-R7FNGWQVQG"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-R7FNGWQVQG');</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://media.ameriglide.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&amp;family=Inter:wght@300;500;700&amp;display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet" media="print" onload="this.media='all'"/><noscript><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet"/></noscript>
<link rel="stylesheet" href="/css/ameriglide-catalog.css"/>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"Home","item":"https://wattsatpcontractor.com/"},
{"@type":"ListItem","position":2,"name":"Stair Lifts & Mobility","item":"https://wattsatpcontractor.com/stair-lift-installation"},
{"@type":"ListItem","position":3,"name":"${p.catName}","item":"https://wattsatpcontractor.com${p.catPage.replace('.html','')}"},
{"@type":"ListItem","position":4,"name":"${p.name}","item":"https://wattsatpcontractor.com/${p.file.replace('.html','')}"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Product","name":"${p.name}","category":"${p.cat}","image":"${p.img}","description":"${p.tagline.replace(/"/g,'\\"')} Sold and professionally installed by Watts ATP Contractor, a certified AmeriGlide dealer serving a 150-mile radius of Norfolk, Nebraska.","brand":{"@type":"Brand","name":"AmeriGlide","sameAs":"https://www.ameriglide.com"},"sameAs":"${p.mfrUrl}","url":"https://wattsatpcontractor.com/${p.file.replace('.html','')}"}
</script>
<meta content="${p.name} | Installed by Watts ATP | Norfolk NE" property="og:title"/>
<meta content="${p.tagline.replace(/&/g,'&amp;')} Dealer pricing from a certified AmeriGlide dealer." property="og:description"/>
<meta content="product" property="og:type"/>
<meta content="https://wattsatpcontractor.com/${p.file.replace('.html','')}" property="og:url"/>
<meta content="${p.img}" property="og:image"/>
</head>
<body>
<noscript><iframe height="0" src="https://www.googletagmanager.com/ns.html?id=GTM-KCPM8VZ" style="display:none;visibility:hidden" width="0"></iframe></noscript>
<header>
<div class="nav-container">
<a class="logo" href="/">WATTS</a>
<button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Open navigation menu" aria-expanded="false"><i class="fas fa-bars"></i></button>
<nav class="nav-links" id="navLinks">
<a href="/services.html">Services</a><a href="/service-area.html">Service Area</a><a href="/about.html">About</a><a href="/referrals.html">Referrals</a><a href="/contact.html">Contact</a>
</nav>
</div>
</header>
<nav class="breadcrumb">
<a href="/">Home</a><span class="sep"><i class="fas fa-chevron-right"></i></span>
<a href="/stair-lift-installation.html">Stair Lifts &amp; Mobility</a><span class="sep"><i class="fas fa-chevron-right"></i></span>
<a href="${p.catPage}">${p.catName}</a><span class="sep"><i class="fas fa-chevron-right"></i></span>
<span class="here">${p.name}</span>
</nav>

<section class="hero" style="padding:55px 20px 50px;">
<span class="dealer-badge"><i class="fas fa-certificate"></i> Certified AmeriGlide Dealer &amp; Installer</span>
<h1>${p.name}</h1>
<p class="lead">${p.tagline}</p>
<div class="hero-ctas">
<a class="cta-button" href="tel:+14054106402"><i class="fas fa-phone"></i> Call (405) 410-6402</a>
<a class="cta-button gold" href="/contact.html?service=stair-lift&amp;product=${encodeURIComponent(p.name)}">Get Dealer Pricing</a>
</div>
</section>

<div class="product-detail">
<div class="product-gallery">
<img src="${p.img}" alt="${p.imgAlt}" loading="lazy"/>
<p class="img-credit">Product image courtesy of AmeriGlide &mdash; <a href="${p.mfrUrl}" target="_blank" rel="noopener">view official product page <i class="fas fa-external-link-alt"></i></a></p>
</div>
<div class="product-info">
<h2>Key Specs &amp; Features</h2>
<p class="lead-in">${p.blurb}</p>
<table class="spec-table">
${rows}
</table>
<div class="quote-box">
<h3><i class="fas fa-tag"></i> Dealer-Direct Pricing</h3>
<p>Every lift is quoted after an on-site assessment — we measure and photograph your space so the equipment quote and install are exact. Pricing varies by model, configuration, and site conditions.</p>
<a class="cta-button" href="/contact.html?service=stair-lift&amp;product=${encodeURIComponent(p.name)}">Request a Quote</a>
</div>
<a class="mfr-link" href="${p.mfrUrl}" target="_blank" rel="noopener"><i class="fas fa-external-link-alt"></i> Full manufacturer specs &amp; documentation on ameriglide.com</a>
</div>
</div>

<section class="section process">
<h2 class="section-title">Getting One Installed</h2>
<div class="process-steps">
<div class="step"><div class="step-num">1</div><h4>Talk It Over</h4><p>Call or send the form — we'll confirm this model fits your situation.</p></div>
<div class="step"><div class="step-num">2</div><h4>On-Site Assessment</h4><p>We visit, measure, and photograph the site for CAD drawings and engineering. An assessment fee applies.</p></div>
<div class="step"><div class="step-num">3</div><h4>Written Quote</h4><p>Dealer-direct equipment pricing plus certified installation — in writing before you commit.</p></div>
<div class="step"><div class="step-num">4</div><h4>Install &amp; Warranty</h4><p>Justin installs, tests every safety feature, and registers your AmeriGlide warranty.</p></div>
</div>
</section>

<section class="section" style="text-align:center;">
<h2 class="section-title">Keep Browsing</h2>
<div class="related-links">
<a href="${p.catPage}">More ${p.catName}</a>
<a href="/stair-lift-installation.html">All AmeriGlide Products</a>
<a class="teal" href="/contact.html?service=stair-lift&amp;product=${encodeURIComponent(p.name)}">Get Dealer Pricing</a>
</div>
</section>

<div class="disclaimer-band">
<div class="disc-inner">
<strong>Independent Dealer Disclosure:</strong> AmeriGlide&reg; and ${p.name} are trademarks/products of AmeriGlide Distributing 2019 Inc. Watts ATP Contractor is an independent, certified AmeriGlide dealer and installer — not owned by or operated by AmeriGlide. Manufacturer warranty (2 years parts/drivetrain, 30 days batteries) is provided by AmeriGlide; installation labor and ongoing service are billed by Watts ATP Contractor. All pricing by custom quote.
</div>
</div>

<footer>
<div class="footer-inner">
<div class="footer-contact">
<p><strong>Watts ATP Contractor</strong> &mdash; Norfolk, NE &mdash; <a href="tel:+14054106402">(405) 410-6402</a></p>
<p><a href="mailto:Justin.Watts@WattsATPContractor.com">Justin.Watts@WattsATPContractor.com</a></p>
</div>
<div class="footer-links">
<a href="/">Home</a><a href="/services.html">Services</a><a href="/stair-lift-installation.html">AmeriGlide Products</a><a href="/about.html">About</a><a href="/contact.html">Contact</a>
</div>
<a class="dba-redirect" href="/safety-installs/">Watts Safety Installs &rarr;</a>
<p class="fine-print">Certified AmeriGlide dealer &amp; installer. AmeriGlide&reg; is a registered trademark of AmeriGlide Distributing 2019 Inc.</p>
<p>&copy; <span id="current-year"></span> Watts ATP Contractor. All rights reserved.</p>
</div>
</footer>
<script>document.getElementById('current-year').textContent = new Date().getFullYear();</script>
<script>document.getElementById('mobileMenuBtn').addEventListener('click',function(){var n=document.getElementById('navLinks');var open=n.classList.toggle('active');this.setAttribute('aria-expanded',open);});</script>
<script src="/js/watts-ai-chat.js" defer></script>
<script src="/js/watts-lead-engine.js" defer></script>
</body>
</html>`;
}

for (const p of P) {
  fs.writeFileSync(path.join(ROOT, p.file), productPage(p));
  console.log('wrote', p.file);
}
