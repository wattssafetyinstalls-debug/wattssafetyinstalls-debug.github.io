/**
 * Replace placeholder GA4 ID with real measurement ID across all HTML files.
 * Run: node tools/fix-ga4-id.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OLD_ID = 'G-XXXXXXXXXX';
const NEW_ID = 'G-R7FNGWQVQG';
const SKIP_DIRS = new Set(['node_modules', '.git', '.github', 'web-stories']);

function findHtmlFiles(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) findHtmlFiles(full, files);
    } else if (entry.name.endsWith('.html')) {
      files.push(full);
    }
  }
  return files;
}

let fixed = 0;
for (const file of findHtmlFiles(ROOT)) {
  let html = fs.readFileSync(file, 'utf8');
  if (!html.includes(OLD_ID)) continue;
  html = html.split(OLD_ID).join(NEW_ID);
  fs.writeFileSync(file, html, 'utf8');
  fixed++;
  console.log('✓ ' + path.relative(ROOT, file));
}
console.log('\nDone: ' + fixed + ' files updated from ' + OLD_ID + ' to ' + NEW_ID);
