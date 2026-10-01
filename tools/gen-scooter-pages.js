// Generates the 3 scooter catalog pages for the AmeriGlide dealer section.
// Run: node tools/gen-scooter-pages.js  (writes into repo root)
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');

// [name, classTag, blurb, ameriglideItemPath]
const TRAVEL = [
  ['Pride Go-Go Elite Traveller 3-Wheel', 'Travel · 3-Wheel', 'The classic portable scooter — disassembles in seconds for trunk storage and everyday errands.', 'Pride-Go-Go-Elite-Traveller---3-Wheel-Travel-Scooter.html'],
  ['Pride Go-Go Ultra X 3-Wheel', 'Travel · 3-Wheel', 'Lightweight travel scooter with easy frame split — the budget-friendly go-anywhere option.', 'Pride-Go-Go-Ultra-X---3-Wheel-Travel-Scooter.html'],
  ['Pride Go-Go Sport 3-Wheel', 'Travel · 3-Wheel', 'Sportier travel scooter with longer range and higher weight capacity than entry models.', 'Pride-Go-Go-Sport---3-Wheel-Travel-Scooter.html'],
  ['Pride Go-Go Sport 4-Wheel w/ EZ Turn', 'Travel · 4-Wheel', 'Four-wheel stability plus EZ Turn for tighter handling — the best of both.', 'prgosport-4wheel.html'],
  ['Pride Go-Go Ultra X GEN 3 4-Wheel', 'Travel · 4-Wheel', 'Latest-generation Ultra X — upgraded design in the proven ultra-portable format.', 'Pride-Go-Go-Ultra-X-GEN-3---4-Wheel-Travel-Scooter.html'],
  ['Pride Go-Go Elite Traveller Gen 3 4-Wheel', 'Travel · 4-Wheel', 'Gen 3 update to the best-seller — four-wheel stability in a take-apart package.', 'Pride-Go-Go-Elite-Traveller-Gen-3---4-Wheel-Travel-Scooter.html'],
  ['Pride Go-Go Elite Traveller Gen 3 Platinum 4-Wheel', 'Travel · 4-Wheel', 'The Platinum trim — premium touches on the Gen 3 travel platform.', 'Pride-Go-Go-Elite-Traveller-Gen-3-Platinum---4-Wheel-Travel-Scooter.html'],
  ['Pride Go-Go Endurance Li', 'Travel · Lithium', 'Lithium-ion powered Go-Go — lighter weight, faster charging, airline-friendly battery.', 'Pride-Go-Go-Endurance-Li.html'],
  ['Pride Go-Go Endurance AL+', 'Travel · Aluminum', 'Aluminum-frame endurance model — rustproof, light, and built to travel.', 'Pride-Go-Go-Endurance-AL%2B.html'],
  ['Pride Go Go Carbon', 'Travel · Carbon Fiber', 'Carbon-fiber frame travel scooter — ultralight folding design for serious portability.', 'Pride-Go-Go-Carbon-Scooter.html'],
  ['Pride Go Go Super Portable', 'Travel · Folding', 'Folds flat for storage and travel — the easiest-loading scooter in the lineup.', 'Pride-Go-Go-Super-Portable.html'],
  ['Golden Buzzaround LT 3-Wheel', 'Travel · 3-Wheel', 'Golden\'s compact Buzzaround — nimble indoor manners with outdoor capability.', 'Golden-Buzzaround-LT---3-Wheel-Travel-Scooter.html'],
  ['Golden Buzzaround LT 4-Wheel', 'Travel · 4-Wheel', 'The LT with an extra wheel — steadier footing without losing portability.', 'Golden-Buzzaround-LT---4-Wheel-Travel-Scooter.html'],
  ['Golden Buzzaround LX 3-Wheel', 'Travel · 3-Wheel', 'Step-up Buzzaround with upgraded comfort and lighting package.', 'Golden-Buzzaround-LX---3-Wheel-Travel-Scooter.html'],
  ['Golden Buzzaround LX 4-Wheel', 'Travel · 4-Wheel', 'Top-trim Buzzaround — four wheels, comfort seating, full lighting.', 'Golden-Buzzaround-LX---4-Wheel-Travel-Scooter.html'],
  ['Golden Buzzaround XL 4-Wheel', 'Travel · 4-Wheel', 'Bigger deck and battery in a still-portable frame.', 'Golden-Buzzaround-XL---4-Wheel-Travel-Scooter.html'],
  ['Golden Buzzaround XL+ 4-Wheel', 'Travel · 4-Wheel', 'The XL with more — extended range and comfort upgrades.', 'Golden-Buzzaround-XL%2B-4-Wheel-Scooter.html'],
  ['Golden Buzzaround XLS-HD 3-Wheel', 'Travel · HD', 'Heavy-duty Buzzaround — higher capacity in the travel format.', 'Golden-Buzzaround-XLS-HD-3-Wheel-Mobility-Scooter.html'],
  ['Golden Buzzaround CarryOn', 'Travel · Folding', 'Folds to luggage size and rolls like a suitcase — the travel specialist.', 'Golden-Buzzaround-CarryOn.html'],
  ['Golden LiteRider 3-Wheel', 'Travel · 3-Wheel', 'Golden\'s lightweight disassembling scooter — simple, reliable daily driver.', 'Golden-LiteRider---3-Wheel-Travel-Scooter.html'],
  ['Golden LiteRider 4-Wheel', 'Travel · 4-Wheel', 'LiteRider with four-wheel stability for uneven sidewalks and lots.', 'Golden-LiteRider---4-Wheel-Travel-Scooter.html'],
];

const FULLSIZE = [
  ['Pride Victory 10 3-Wheel', 'Full-Size · 3-Wheel', 'Full-size comfort and range for daily use — Pride\'s proven midsize-to-full platform.', 'Pride-Victory-10---3-Wheel-Scooter.html'],
  ['Pride Victory 10 4-Wheel', 'Full-Size · 4-Wheel', 'The 4-wheel Victory — more stability for outdoor routes and longer days out.', 'Pride-Victory-10---4-Wheel-Scooter.html'],
  ['Pride Victory LX Sport 4-Wheel CTS', 'Full-Size · 4-Wheel', 'CTS suspension for a genuinely smooth ride — the comfort flagship of the Victory line.', 'Pride-Victory-LX-Sport-4-Wheel-with-CTS-Suspension.html'],
  ['Pride Victory Platinum 4-Wheel', 'Full-Size · 4-Wheel', 'Platinum-trim Victory — premium finishes on the full-size frame.', 'Pride-Victory-Platinum---4-Wheel-Scooter.html'],
  ['Pride Revo 2.0 3-Wheel', 'Midsize · 3-Wheel', 'Midsize Revo — easy take-apart design with real everyday range.', 'Pride-Revo-2-0-3-Wheel-Scooter.html'],
  ['Pride Revo 2.0 4-Wheel', 'Midsize · 4-Wheel', 'Four-wheel Revo 2.0 — the versatile middle ground between travel and HD.', 'Pride-Revo-2-0-4-Wheel-Scooter.html'],
  ['Golden Companion Midsize 3-Wheel', 'Midsize · 3-Wheel', 'Golden\'s midsize Companion — comfort seating and solid range.', 'Golden-Companion---Midsize-3-Wheel-Scooter.html'],
  ['Golden Companion Full Size 3-Wheel', 'Full-Size · 3-Wheel', 'Full-size Companion — roomier ride for all-day use.', 'Golden-Companion---Full-Size-3-Wheel-Scooter.html'],
  ['Golden Companion Full Size 4-Wheel', 'Full-Size · 4-Wheel', 'The Companion with four-wheel poise for outdoor confidence.', 'Golden-Companion---Full-Size-4-Wheel-Scooter.html'],
  ['Golden Buzzaround EX 3-Wheel', 'Midsize · 3-Wheel', 'Extended-range Buzzaround — goes farther between charges.', 'Golden-Buzzaround-EX-3-Wheel-Mobility-Scooter.html'],
  ['Golden Buzzaround EX 4-Wheel', 'Midsize · 4-Wheel', 'EX range plus four-wheel stability — the road-trip Buzzaround.', 'Golden-Buzzaround-EX-4-Wheel-Mobility-Scooter.html'],
];

const HEAVYDUTY = [
  ['Pride Maxima 3-Wheel HD', 'Heavy-Duty · 3-Wheel', 'Heavy-duty classic — high capacity with Pride\'s proven Maxima drivetrain.', 'Pride-Maxima---3-Wheel-HD-Scooter.html'],
  ['Pride Maxima 4-Wheel HD', 'Heavy-Duty · 4-Wheel', 'The 4-wheel Maxima — maximum stability at maximum capacity.', 'Pride-Maxima---4-Wheel-HD-Scooter.html'],
  ['Golden Avenger 4-Wheel HD', 'Heavy-Duty · 4-Wheel', 'Golden\'s heavy hitter — rugged HD scooter for bigger riders and rougher routes.', 'Golden-Avenger---4-Wheel-HD-Scooter.html'],
  ['Pride Pursuit 2 4-Wheel PMV', 'Heavy-Duty · 4-Wheel', 'Premium heavy-duty PMV — suspension, power, and road presence.', 'Pride-Pursuit-2---4-Wheel-PMV.html'],
  ['Golden Eagle GR-595 4-Wheel', 'Heavy-Duty · 4-Wheel', 'Eagle-series power — built for distance and durability.', 'Golden-Eagle-GR-595-4-Wheel-Scooter.html'],
  ['Golden Eagle GR-596 All Terrain 4-Wheel', 'All-Terrain · 4-Wheel', 'The all-terrain flagship — real ground clearance and suspension for Nebraska outdoors.', 'Golden-Eagle-GR-596-All-Terrain-4-Wheel-Scooter.html'],
];

const EXTRA = [
  ['Pride Baja Wrangler 2 4-Wheel', 'All-Terrain · 4-Wheel', 'Off-road beast — trails, gravel, and rural property are its home turf.', 'Pride-Baja-Wrangler-2---4-Wheel-Scooter.html'],
  ['Pride PX4 4-Wheel', 'Heavy-Duty · 4-Wheel', 'Pride\'s premium HD platform — top-tier capacity and range.', 'Pride-PX4-4-Wheel-Scooter.html'],
  ['Golden Companion HD Full Size 3-Wheel', 'Heavy-Duty · 3-Wheel', 'HD Companion — heavy capacity with the Companion\'s comfort focus.', 'Golden-Companion-HD---Full-Size-3-Wheel-Scooter.html'],
];

function card([name, tag, blurb, itemPath]) {
  return `<div class="product-card">
<div class="product-card-img"><i class="fas fa-wheelchair"></i></div>
<div class="product-card-body">
<span class="product-tag">${tag}</span>
<h3>${name}</h3>
<p>${blurb}</p>
<div class="product-card-links">
<a class="buy" href="/contact.html?service=mobility-scooter&amp;product=${encodeURIComponent(name)}">Get Dealer Pricing</a>
<a class="specs" href="https://www.ameriglide.com/item/${itemPath}" target="_blank" rel="noopener">Full specs on ameriglide.com <i class="fas fa-external-link-alt"></i></a>
</div>
</div>
</div>`;
}

function itemListSchema(items, listName) {
  return `{"@context":"https://schema.org","@type":"ItemList","name":"${listName}","itemListElement":[${items.map((it, i) =>
    `{"@type":"ListItem","position":${i + 1},"item":{"@type":"Product","name":"${it[0]}","sameAs":"https://www.ameriglide.com/item/${it[3]}"}}`).join(',')}]}`;
}

function page({file, title, desc, canon, kw, h1, lead, sections, count, catLink, catLinkText}) {
  const body = sections.map(s => `
<h2 class="section-title" style="text-align:left;margin-top:50px;">${s.heading}</h2>
<div class="product-grid" style="margin-top:25px;">
${s.items.map(card).join('\n')}
</div>`).join('\n');
  const allItems = sections.flatMap(s => s.items);
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>${title}</title>
<meta content="${desc}" name="description"/>
<link href="${canon}" rel="canonical"/>
<meta content="${kw}" name="keywords"/>
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48"/>
<link rel="manifest" href="/manifest.json"/>
<meta name="theme-color" content="#0A1D37"/>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-KCPM8VZ');</script>
<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-R7FNGWQVQG"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-R7FNGWQVQG');</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&amp;family=Inter:wght@300;500;700&amp;display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet" media="print" onload="this.media='all'"/><noscript><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet"/></noscript>
<link rel="stylesheet" href="/css/ameriglide-catalog.css"/>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"Home","item":"https://wattsatpcontractor.com/"},
{"@type":"ListItem","position":2,"name":"Stair Lifts & Mobility","item":"https://wattsatpcontractor.com/stair-lift-installation"},
{"@type":"ListItem","position":3,"name":"${h1}","item":"${canon}"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"Mobility Scooter Sales & Delivery","name":"${h1} | Watts ATP Contractor | Norfolk NE","url":"${canon}","provider":{"@type":"HomeAndConstructionBusiness","@id":"https://wattsatpcontractor.com/#organization","name":"Watts ATP Contractor","telephone":"+14054106402"},"brand":{"@type":"Brand","name":"AmeriGlide","sameAs":"https://www.ameriglide.com"},"areaServed":{"@type":"GeoCircle","geoMidpoint":{"@type":"GeoCoordinates","latitude":42.032,"longitude":-97.418},"geoRadius":"241402"},"description":"${desc.replace(/&amp;/g,'&')}"}
</script>
<meta content="${title}" property="og:title"/>
<meta content="${desc}" property="og:description"/>
<meta content="website" property="og:type"/>
<meta content="${canon}" property="og:url"/>
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
<span class="here">${h1}</span>
</nav>

<section class="hero">
<h1>${h1}</h1>
<span class="dealer-badge"><i class="fas fa-certificate"></i> Certified AmeriGlide Dealer</span>
<p class="lead">${lead}</p>
<div class="hero-ctas">
<a class="cta-button" href="tel:+14054106402"><i class="fas fa-phone"></i> Call (405) 410-6402</a>
<a class="cta-button gold" href="/contact.html?service=mobility-scooter">Get Dealer Pricing</a>
</div>
</section>

<section class="section">
<h2 class="section-title">${count} Models Available</h2>
<p class="section-subtitle">Every scooter below ships through our AmeriGlide dealer account at dealer pricing. We handle ordering, delivery, setup, and a full walkthrough &mdash; no site assessment needed.</p>${body}
<p style="text-align:center;margin-top:35px;color:var(--gray);">Browse the full catalog at <a href="${catLink}" target="_blank" rel="noopener" style="color:var(--teal);font-weight:600;">${catLinkText} <i class="fas fa-external-link-alt"></i></a> &mdash; if it's on their site, we can order it for you.</p>
</section>

<section class="section" style="text-align:center;">
<h2 class="section-title">More AmeriGlide Equipment</h2>
<div class="related-links">
<a href="/straight-stair-lifts.html">Straight Stair Lifts</a>
<a href="/curved-stair-lifts.html">Curved Stair Lifts</a>
<a href="/vertical-platform-lifts.html">Platform Lifts (VPLs)</a>
<a class="teal" href="/stair-lift-installation.html">All AmeriGlide Products</a>
</div>
</section>

<div class="disclaimer-band">
<div class="disc-inner">
<strong>Independent Dealer Disclosure:</strong> AmeriGlide&reg;, Pride Mobility&reg;, and Golden Technologies&reg; product names are trademarks of their respective owners. Watts ATP Contractor is an independent, certified AmeriGlide dealer &mdash; not owned by or operated by AmeriGlide, Pride, or Golden. Manufacturer warranties are provided by the manufacturer; delivery, setup, and service are billed by Watts ATP Contractor. All pricing by custom quote.
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
<script type="application/ld+json">
${itemListSchema(allItems, h1 + ' Sold by Watts ATP Contractor')}
</script>
<script src="/js/watts-ai-chat.js" defer></script>
<script src="/js/watts-lead-engine.js" defer></script>
</body>
</html>`;
}

// All-scooters master = travel + fullsize + HD + extra (dedup not needed — mirrors AmeriGlide's groupings)
const ALL_SECTIONS = [
  { heading: 'Travel & Portable Scooters', items: TRAVEL },
  { heading: 'Midsize & Full-Size Scooters', items: FULLSIZE },
  { heading: 'Heavy-Duty & All-Terrain Scooters', items: HEAVYDUTY.concat(EXTRA) },
];

fs.writeFileSync(path.join(ROOT, 'mobility-scooters.html'), page({
  file: 'mobility-scooters.html',
  title: 'Mobility Scooters Norfolk NE | AmeriGlide Dealer | Watts ATP',
  desc: 'Mobility scooters at dealer pricing in Norfolk NE — Pride &amp; Golden travel, midsize &amp; heavy-duty scooters through certified AmeriGlide dealer Watts ATP. Order, delivery &amp; setup — (405) 410-6402.',
  canon: 'https://wattsatpcontractor.com/mobility-scooters',
  kw: 'mobility scooters Norfolk NE, Pride scooter dealer, Golden Technologies scooter, AmeriGlide scooter dealer Nebraska, heavy duty scooter, travel scooter',
  h1: 'Mobility Scooters',
  lead: 'The complete mobility scooter lineup — travel scooters that fold into your trunk, full-size daily drivers, and all-terrain heavy-duty machines. Every one ordered through our certified AmeriGlide dealer account and delivered with a full setup and walkthrough.',
  sections: ALL_SECTIONS,
  count: TRAVEL.length + FULLSIZE.length + HEAVYDUTY.length + EXTRA.length,
  catLink: 'https://www.ameriglide.com/AmeriGlide-Mobility-Scooters.htm',
  catLinkText: 'ameriglide.com/mobility-scooters',
}));

fs.writeFileSync(path.join(ROOT, 'travel-scooters.html'), page({
  file: 'travel-scooters.html',
  title: 'Travel Scooters Norfolk NE | Portable Mobility | Watts ATP',
  desc: 'Portable travel scooters at dealer pricing in Norfolk NE — Go-Go, Buzzaround &amp; LiteRider models that disassemble or fold for your trunk. Certified AmeriGlide dealer — (405) 410-6402.',
  canon: 'https://wattsatpcontractor.com/travel-scooters',
  kw: 'travel scooter Norfolk NE, portable mobility scooter, Go-Go scooter dealer, Buzzaround scooter Nebraska, folding mobility scooter',
  h1: 'Travel Scooters',
  lead: 'Lightweight scooters that come apart or fold for the trunk — doctor\'s appointments, road trips, grandkids\' games. We order at dealer pricing, deliver, and set you up right.',
  sections: [{ heading: 'Travel & Portable Models', items: TRAVEL }],
  count: TRAVEL.length,
  catLink: 'https://www.ameriglide.com/Travel-Scooters.htm',
  catLinkText: 'ameriglide.com/travel-scooters',
}));

fs.writeFileSync(path.join(ROOT, 'heavy-duty-scooters.html'), page({
  file: 'heavy-duty-scooters.html',
  title: 'Heavy-Duty Scooters Norfolk NE | All-Terrain | Watts ATP',
  desc: 'Heavy-duty &amp; all-terrain mobility scooters at dealer pricing in Norfolk NE — Maxima, Avenger, Eagle &amp; Pursuit models for higher capacity and real terrain. Dealer pricing — (405) 410-6402.',
  canon: 'https://wattsatpcontractor.com/heavy-duty-scooters',
  kw: 'heavy duty mobility scooter Norfolk NE, all terrain scooter Nebraska, Pride Maxima dealer, Golden Avenger, 500 lb scooter',
  h1: 'Heavy-Duty Scooters',
  lead: 'Higher weight capacity, real suspension, and ground clearance for Nebraska outdoors — acreages, gravel, county fairs, and everything else life throws at you.',
  sections: [{ heading: 'Heavy-Duty & All-Terrain Models', items: HEAVYDUTY.concat(EXTRA) }],
  count: HEAVYDUTY.length + EXTRA.length,
  catLink: 'https://www.ameriglide.com/Heavy-Duty-Scooters.htm',
  catLinkText: 'ameriglide.com/heavy-duty-scooters',
}));

console.log('Wrote mobility-scooters.html, travel-scooters.html, heavy-duty-scooters.html');
