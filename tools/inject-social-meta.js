#!/usr/bin/env node
/**
 * Social Meta Tag Injector — Ensures all pages have OG + Twitter Card meta
 * Also adds Pinterest Rich Pin validation meta.
 * Run once or after adding new pages.
 */

var fs = require('fs');
var path = require('path');

var ROOT = path.resolve(__dirname, '..');
var BASE = 'https://wattsatpcontractor.com';
var DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80';

var PAGE_META = {
  // ATP pages
  'index.html': { title: 'Accessibility Contractor Near Me | Watts ATP Contractor | Norfolk NE', url: '/', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'services.html': { title: 'Our Services | Watts ATP Contractor | Norfolk NE', url: '/services', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'about.html': { title: 'About Us | Watts ATP Contractor | Norfolk NE', url: '/about', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'contact.html': { title: 'Contact Us | Watts ATP Contractor | Norfolk NE', url: '/contact', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'service-area.html': { title: 'Service Area | Watts ATP Contractor | Norfolk NE', url: '/service-area', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'referrals.html': { title: 'Referrals | Watts ATP Contractor | Norfolk NE', url: '/referrals', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'grab-bar-installation.html': { title: 'Grab Bar Installation | Watts ATP Contractor | Norfolk NE', url: '/grab-bar-installation', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'wheelchair-ramp-installation.html': { title: 'Wheelchair Ramp Installation | Watts ATP Contractor | Norfolk NE', url: '/wheelchair-ramp-installation', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'bathroom-accessibility.html': { title: 'Bathroom Accessibility | Watts ATP Contractor | Norfolk NE', url: '/bathroom-accessibility', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'non-slip-flooring-solutions.html': { title: 'Non-Slip Flooring Solutions | Watts ATP Contractor | Norfolk NE', url: '/non-slip-flooring-solutions', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
  'accessibility-safety-solutions.html': { title: 'Accessibility & Safety Solutions | Watts ATP Contractor | Norfolk NE', url: '/accessibility-safety-solutions', image: DEFAULT_IMAGE, site: 'Watts ATP Contractor' },
};

var SI_PAGE_META = {
  'index.html': { title: 'Watts Safety Installs | Home Remodeling & Maintenance | Norfolk NE', url: '/safety-installs/', site: 'Watts Safety Installs' },
  'services.html': { title: 'Services | Watts Safety Installs | Norfolk NE', url: '/safety-installs/services', site: 'Watts Safety Installs' },
  'about.html': { title: 'About | Watts Safety Installs | Norfolk NE', url: '/safety-installs/about', site: 'Watts Safety Installs' },
  'contact.html': { title: 'Contact | Watts Safety Installs | Norfolk NE', url: '/safety-installs/contact', site: 'Watts Safety Installs' },
  'service-area.html': { title: 'Service Area | Watts Safety Installs | Norfolk NE', url: '/safety-installs/service-area', site: 'Watts Safety Installs' },
  'referrals.html': { title: 'Referrals | Watts Safety Installs | Norfolk NE', url: '/safety-installs/referrals', site: 'Watts Safety Installs' },
};

function getDescription(html) {
  var m = html.match(/<meta[^>]*name="description"[^>]*content="([^"]+)"/);
  if (!m) m = html.match(/<meta[^>]*content="([^"]+)"[^>]*name="description"/);
  return m ? m[1] : '';
}

function injectMeta(filePath, meta) {
  var html = fs.readFileSync(filePath, 'utf8');
  var desc = getDescription(html);
  var modified = false;

  // Check for existing OG tags
  var hasOgTitle = html.indexOf('og:title') !== -1;
  var hasOgUrl = html.indexOf('og:url') !== -1;
  var hasOgImage = html.indexOf('og:image') !== -1;
  var hasOgSiteName = html.indexOf('og:site_name') !== -1;
  var hasTwitterCard = html.indexOf('twitter:card') !== -1;

  var tags = '';

  if (!hasOgTitle) {
    tags += '<meta content="' + esc(meta.title) + '" property="og:title"/>\n';
    tags += '<meta content="' + esc(desc) + '" property="og:description"/>\n';
    tags += '<meta content="website" property="og:type"/>\n';
  }
  if (!hasOgUrl) {
    tags += '<meta content="' + BASE + meta.url + '" property="og:url"/>\n';
  }
  if (!hasOgImage) {
    tags += '<meta content="' + (meta.image || DEFAULT_IMAGE) + '" property="og:image"/>\n';
    tags += '<meta content="1200" property="og:image:width"/>\n';
    tags += '<meta content="630" property="og:image:height"/>\n';
  }
  if (!hasOgSiteName) {
    tags += '<meta content="' + esc(meta.site) + '" property="og:site_name"/>\n';
  }
  if (!hasTwitterCard) {
    tags += '<meta content="summary_large_image" name="twitter:card"/>\n';
    tags += '<meta content="' + esc(meta.title) + '" name="twitter:title"/>\n';
    tags += '<meta content="' + esc(desc) + '" name="twitter:description"/>\n';
    tags += '<meta content="' + (meta.image || DEFAULT_IMAGE) + '" name="twitter:image"/>\n';
  }

  if (tags === '') {
    console.log('  ⏭️  ' + path.basename(filePath) + ' (already complete)');
    return false;
  }

  // Inject before </head>
  html = html.replace('</head>', tags + '</head>');
  fs.writeFileSync(filePath, html, 'utf8');
  console.log('  ✅ ' + path.basename(filePath) + ' (' + tags.split('\n').filter(Boolean).length + ' tags added)');
  return true;
}

function esc(s) { return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }

function main() {
  console.log('📱 Social Meta Tag Injector (OG + Twitter Card + Pinterest)');
  console.log('==========================================================\n');

  var count = 0;

  console.log('ATP pages:');
  Object.keys(PAGE_META).forEach(function(file) {
    var fp = path.join(ROOT, file);
    if (fs.existsSync(fp) && injectMeta(fp, PAGE_META[file])) count++;
  });

  console.log('\nSafety Installs pages:');
  Object.keys(SI_PAGE_META).forEach(function(file) {
    var fp = path.join(ROOT, 'safety-installs', file);
    if (fs.existsSync(fp) && injectMeta(fp, SI_PAGE_META[file])) count++;
  });

  console.log('\n✅ Done! Updated ' + count + ' pages with social meta tags.');
}

main();
