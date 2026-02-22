/**
 * Inject AggregateRating into all service pages that have LocalBusiness/Service schema
 * but are missing AggregateRating.
 * 
 * Run: node tools/inject-aggregate-rating.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const RATING = { ratingValue: '5.0', reviewCount: '12', bestRating: '5', worstRating: '1' };

const SKIP_DIRS = new Set(['node_modules', '.git', '.github', 'web-stories', 'tools', 'blog']);

function findHtmlFiles(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) findHtmlFiles(full, files);
    } else if (entry.name.endsWith('.html') && entry.name !== 'sitemap.html' && entry.name !== '404.html') {
      files.push(full);
    }
  }
  return files;
}

let updated = 0, skipped = 0, alreadyHas = 0;

for (const file of findHtmlFiles(ROOT)) {
  let html = fs.readFileSync(file, 'utf8');

  // Only process files with schema markup
  if (!html.includes('schema.org')) { skipped++; continue; }
  // Skip if already has aggregateRating
  if (html.includes('aggregateRating') || html.includes('AggregateRating')) { alreadyHas++; continue; }

  // Find the last occurrence of "priceRange" or "areaServed" closing bracket to inject after
  // We need to add aggregateRating to the LocalBusiness/Service schema
  const patterns = [
    // After priceRange line
    /"priceRange"\s*:\s*"[^"]*"/,
    // After openingHours line  
    /"openingHours"\s*:\s*"[^"]*"/,
    // After telephone line
    /"telephone"\s*:\s*"[^"]*"/
  ];

  let injected = false;
  for (const pattern of patterns) {
    const match = html.match(pattern);
    if (match) {
      const insertPoint = match.index + match[0].length;
      const ratingJson = `,\n      "aggregateRating": {"@type": "AggregateRating", "ratingValue": "${RATING.ratingValue}", "reviewCount": "${RATING.reviewCount}", "bestRating": "${RATING.bestRating}", "worstRating": "${RATING.worstRating}"}`;
      html = html.slice(0, insertPoint) + ratingJson + html.slice(insertPoint);
      injected = true;
      break;
    }
  }

  if (injected) {
    fs.writeFileSync(file, html, 'utf8');
    updated++;
    console.log(`✓ ${path.relative(ROOT, file)}`);
  } else {
    skipped++;
  }
}

console.log(`\nDone: ${updated} updated, ${alreadyHas} already had rating, ${skipped} skipped (no schema or no insertion point).`);
