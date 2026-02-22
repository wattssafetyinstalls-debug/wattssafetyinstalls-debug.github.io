/**
 * Inject OneSignal push notification script into all HTML pages.
 * Adds <script src="/js/watts-push.js" defer></script> before </body>.
 * For pages in subdirectories, adjusts the path accordingly.
 * 
 * Run: node tools/inject-push-script.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SCRIPT_TAG_MARKER = 'watts-push.js';

// Directories to skip
const SKIP_DIRS = new Set(['node_modules', '.git', '.github', 'web-stories', 'tools']);

function findHtmlFiles(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) findHtmlFiles(full, files);
    } else if (entry.name.endsWith('.html') && entry.name !== 'sitemap.html') {
      files.push(full);
    }
  }
  return files;
}

let injected = 0, skipped = 0;

for (const file of findHtmlFiles(ROOT)) {
  let html = fs.readFileSync(file, 'utf8');

  // Skip if already has the push script
  if (html.includes(SCRIPT_TAG_MARKER)) {
    skipped++;
    continue;
  }

  // Skip if no </body>
  if (!html.includes('</body>')) continue;

  // Calculate relative path from file to /js/watts-push.js
  const rel = path.relative(path.dirname(file), ROOT).replace(/\\/g, '/');
  const scriptPath = rel ? `${rel}/js/watts-push.js` : 'js/watts-push.js';

  const tag = `<script src="${scriptPath}" defer></script>`;
  html = html.replace('</body>', `${tag}\n</body>`);
  fs.writeFileSync(file, html, 'utf8');
  injected++;
  console.log(`✓ ${path.relative(ROOT, file)}`);
}

console.log(`\nDone: ${injected} injected, ${skipped} already had it.`);
