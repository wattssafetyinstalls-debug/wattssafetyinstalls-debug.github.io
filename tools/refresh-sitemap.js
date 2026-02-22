/**
 * Auto-refresh sitemap.xml with current dates for modified pages.
 * Updates lastmod to today's date for all URLs in sitemap.xml.
 * 
 * Run: node tools/refresh-sitemap.js
 * Called automatically by GitHub Actions after content generation.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITEMAP = path.join(ROOT, 'sitemap.xml');
const TODAY = new Date().toISOString().split('T')[0]; // YYYY-MM-DD

if (!fs.existsSync(SITEMAP)) {
  console.log('No sitemap.xml found');
  process.exit(0);
}

let xml = fs.readFileSync(SITEMAP, 'utf8');

// Update all lastmod dates to today
const before = (xml.match(/<lastmod>/g) || []).length;
xml = xml.replace(/<lastmod>\d{4}-\d{2}-\d{2}<\/lastmod>/g, `<lastmod>${TODAY}</lastmod>`);

fs.writeFileSync(SITEMAP, xml, 'utf8');
console.log(`✓ Updated ${before} lastmod dates to ${TODAY} in sitemap.xml`);
