#!/usr/bin/env node
/**
 * Breadcrumb Schema Injector — Adds BreadcrumbList JSON-LD to all pages
 * Also adds Speakable schema to service pages for voice search.
 * Run once or after adding new pages.
 */

var fs = require('fs');
var path = require('path');

var ROOT = path.resolve(__dirname, '..');
var BASE = 'https://wattsatpcontractor.com';

// ── BREADCRUMB MAP ──
// Define the breadcrumb hierarchy for each page
var ATP_CRUMBS = {
  'index.html':                        [{ name: 'Home', url: '/' }],
  'services.html':                     [{ name: 'Home', url: '/' }, { name: 'Services', url: '/services' }],
  'about.html':                        [{ name: 'Home', url: '/' }, { name: 'About', url: '/about' }],
  'contact.html':                      [{ name: 'Home', url: '/' }, { name: 'Contact', url: '/contact' }],
  'service-area.html':                 [{ name: 'Home', url: '/' }, { name: 'Service Area', url: '/service-area' }],
  'referrals.html':                    [{ name: 'Home', url: '/' }, { name: 'Referrals', url: '/referrals' }],
  'sitemap.html':                      [{ name: 'Home', url: '/' }, { name: 'Sitemap', url: '/sitemap' }],
  'privacy-policy.html':              [{ name: 'Home', url: '/' }, { name: 'Privacy Policy', url: '/privacy-policy' }],
  'grab-bar-installation.html':       [{ name: 'Home', url: '/' }, { name: 'Services', url: '/services' }, { name: 'Grab Bar Installation', url: '/grab-bar-installation' }],
  'wheelchair-ramp-installation.html': [{ name: 'Home', url: '/' }, { name: 'Services', url: '/services' }, { name: 'Wheelchair Ramp Installation', url: '/wheelchair-ramp-installation' }],
  'bathroom-accessibility.html':      [{ name: 'Home', url: '/' }, { name: 'Services', url: '/services' }, { name: 'Bathroom Accessibility', url: '/bathroom-accessibility' }],
  'non-slip-flooring-solutions.html': [{ name: 'Home', url: '/' }, { name: 'Services', url: '/services' }, { name: 'Non-Slip Flooring', url: '/non-slip-flooring-solutions' }],
  'accessibility-safety-solutions.html': [{ name: 'Home', url: '/' }, { name: 'Services', url: '/services' }, { name: 'Accessibility & Safety Solutions', url: '/accessibility-safety-solutions' }],
};

var SI_CRUMBS = {
  'index.html':        [{ name: 'Home', url: '/' }, { name: 'Watts Safety Installs', url: '/safety-installs/' }],
  'services.html':     [{ name: 'Home', url: '/' }, { name: 'Watts Safety Installs', url: '/safety-installs/' }, { name: 'Services', url: '/safety-installs/services' }],
  'about.html':        [{ name: 'Home', url: '/' }, { name: 'Watts Safety Installs', url: '/safety-installs/' }, { name: 'About', url: '/safety-installs/about' }],
  'contact.html':      [{ name: 'Home', url: '/' }, { name: 'Watts Safety Installs', url: '/safety-installs/' }, { name: 'Contact', url: '/safety-installs/contact' }],
  'service-area.html': [{ name: 'Home', url: '/' }, { name: 'Watts Safety Installs', url: '/safety-installs/' }, { name: 'Service Area', url: '/safety-installs/service-area' }],
  'referrals.html':    [{ name: 'Home', url: '/' }, { name: 'Watts Safety Installs', url: '/safety-installs/' }, { name: 'Referrals', url: '/safety-installs/referrals' }],
  'sitemap.html':      [{ name: 'Home', url: '/' }, { name: 'Watts Safety Installs', url: '/safety-installs/' }, { name: 'Sitemap', url: '/safety-installs/sitemap' }],
  'privacy-policy.html': [{ name: 'Home', url: '/' }, { name: 'Watts Safety Installs', url: '/safety-installs/' }, { name: 'Privacy Policy', url: '/safety-installs/privacy-policy' }],
};

// Pages that should get Speakable schema (service pages)
var SPEAKABLE_PAGES = [
  'grab-bar-installation.html',
  'wheelchair-ramp-installation.html',
  'bathroom-accessibility.html',
  'non-slip-flooring-solutions.html',
  'accessibility-safety-solutions.html',
  'services.html',
];

function buildBreadcrumbJSON(crumbs) {
  var items = crumbs.map(function(c, i) {
    return {
      '@type': 'ListItem',
      'position': i + 1,
      'name': c.name,
      'item': BASE + c.url
    };
  });
  return JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': items
  }, null, 2);
}

function buildSpeakableJSON(pageUrl) {
  return JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    'url': BASE + pageUrl,
    'speakable': {
      '@type': 'SpeakableSpecification',
      'cssSelector': ['h1', 'h2', '.qa-answer', 'article p']
    }
  }, null, 2);
}

function injectSchema(filePath, crumbs, filename) {
  var html = fs.readFileSync(filePath, 'utf8');

  // Skip if breadcrumb already injected
  if (html.indexOf('BreadcrumbList') !== -1) {
    console.log('  ⏭️  ' + filePath + ' (already has breadcrumbs)');
    return false;
  }

  var breadcrumbScript = '<script type="application/ld+json">\n' + buildBreadcrumbJSON(crumbs) + '\n</script>';

  // Also add speakable if it's a service page
  var speakableScript = '';
  if (SPEAKABLE_PAGES.indexOf(filename) !== -1) {
    var pageUrl = crumbs[crumbs.length - 1].url;
    speakableScript = '\n<script type="application/ld+json">\n' + buildSpeakableJSON(pageUrl) + '\n</script>';
  }

  // Inject before closing </head> or before first <style> in <head>
  var injection = breadcrumbScript + speakableScript + '\n';

  if (html.indexOf('</head>') !== -1) {
    html = html.replace('</head>', injection + '</head>');
  } else {
    // Fallback: inject before </body>
    html = html.replace('</body>', injection + '</body>');
  }

  fs.writeFileSync(filePath, html, 'utf8');
  console.log('  ✅ ' + filePath);
  return true;
}

function main() {
  console.log('🧭 Breadcrumb + Speakable Schema Injector');
  console.log('==========================================\n');

  var count = 0;

  // ATP pages
  console.log('ATP Contractor pages:');
  Object.keys(ATP_CRUMBS).forEach(function(file) {
    var filePath = path.join(ROOT, file);
    if (fs.existsSync(filePath)) {
      if (injectSchema(filePath, ATP_CRUMBS[file], file)) count++;
    } else {
      console.log('  ⚠️  ' + filePath + ' not found');
    }
  });

  // Safety Installs pages
  console.log('\nSafety Installs pages:');
  Object.keys(SI_CRUMBS).forEach(function(file) {
    var filePath = path.join(ROOT, 'safety-installs', file);
    if (fs.existsSync(filePath)) {
      if (injectSchema(filePath, SI_CRUMBS[file], file)) count++;
    } else {
      console.log('  ⚠️  ' + filePath + ' not found');
    }
  });

  console.log('\n✅ Done! Injected schema into ' + count + ' pages.');
}

main();
