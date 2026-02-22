#!/usr/bin/env node
/**
 * Performance Optimizer — Injects preconnect hints, lazy loading, and
 * resource hints into all HTML pages for Core Web Vitals improvement.
 * Run once or after adding new pages.
 */

var fs = require('fs');
var path = require('path');

var ROOT = path.resolve(__dirname, '..');

// Preconnect hints — establish early connections to external resources
var PRECONNECT_TAGS = [
  '<link rel="preconnect" href="https://fonts.googleapis.com">',
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
  '<link rel="preconnect" href="https://cdnjs.cloudflare.com">',
  '<link rel="dns-prefetch" href="https://www.googletagmanager.com">',
  '<link rel="dns-prefetch" href="https://www.google-analytics.com">',
].join('\n');

function processFile(filePath) {
  var html = fs.readFileSync(filePath, 'utf8');
  var modified = false;
  var changes = [];

  // 1. Add preconnect hints (if not already present)
  if (html.indexOf('preconnect') === -1 && html.indexOf('fonts.googleapis.com') !== -1) {
    // Insert preconnect before the first <link to fonts
    html = html.replace(
      /<link[^>]*href="https:\/\/fonts\.googleapis\.com/,
      PRECONNECT_TAGS + '\n<link href="https://fonts.googleapis.com'
    );
    modified = true;
    changes.push('preconnect');
  }

  // 2. Add loading="lazy" to images that don't have it (skip first image for LCP)
  var imgCount = 0;
  html = html.replace(/<img\b([^>]*)>/gi, function(match, attrs) {
    imgCount++;
    if (attrs.indexOf('loading=') !== -1) return match;
    if (imgCount <= 1) return match; // Don't lazy-load first image (LCP)
    modified = true;
    if (!changes.includes('lazy-load')) changes.push('lazy-load');
    return '<img loading="lazy"' + attrs + '>';
  });

  // 3. Add fetchpriority="high" to first image (LCP optimization)
  var firstImgDone = false;
  html = html.replace(/<img\b([^>]*)>/i, function(match, attrs) {
    if (firstImgDone || attrs.indexOf('fetchpriority') !== -1) return match;
    firstImgDone = true;
    modified = true;
    changes.push('fetchpriority');
    return '<img fetchpriority="high"' + attrs + '>';
  });

  // 4. Add width/height to images that are missing them (CLS prevention)
  // Skip this for now — too risky without knowing actual dimensions

  if (modified) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log('  ✅ ' + path.basename(filePath) + ' (' + changes.join(', ') + ')');
    return true;
  } else {
    console.log('  ⏭️  ' + path.basename(filePath) + ' (no changes needed)');
    return false;
  }
}

function main() {
  console.log('⚡ Performance Optimizer');
  console.log('======================\n');

  var count = 0;

  // Process all HTML files in root
  var rootFiles = fs.readdirSync(ROOT).filter(function(f) { return f.endsWith('.html'); });
  console.log('ATP pages:');
  rootFiles.forEach(function(f) {
    if (processFile(path.join(ROOT, f))) count++;
  });

  // Process safety-installs
  var siDir = path.join(ROOT, 'safety-installs');
  if (fs.existsSync(siDir)) {
    var siFiles = fs.readdirSync(siDir).filter(function(f) { return f.endsWith('.html'); });
    console.log('\nSafety Installs pages:');
    siFiles.forEach(function(f) {
      if (processFile(path.join(siDir, f))) count++;
    });
  }

  console.log('\n✅ Done! Optimized ' + count + ' pages.');
}

main();
