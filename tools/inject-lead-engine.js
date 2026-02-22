/**
 * Inject Lead Generation Engine script into all HTML pages.
 * Adds <script src="/js/watts-lead-engine.js" defer></script> before </body>.
 * 
 * Run: node tools/inject-lead-engine.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const MARKER = 'watts-lead-engine.js';
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
  if (html.includes(MARKER)) { skipped++; continue; }
  if (!html.includes('</body>')) continue;

  const rel = path.relative(path.dirname(file), ROOT).replace(/\\/g, '/');
  const scriptPath = rel ? `${rel}/js/watts-lead-engine.js` : 'js/watts-lead-engine.js';
  const tag = `<script src="${scriptPath}" defer></script>`;
  
  // Insert before watts-push.js if it exists, otherwise before </body>
  if (html.includes('watts-push.js')) {
    html = html.replace(/(<script[^>]*watts-push\.js[^>]*><\/script>)/, `${tag}\n$1`);
  } else {
    html = html.replace('</body>', `${tag}\n</body>`);
  }
  
  fs.writeFileSync(file, html, 'utf8');
  injected++;
  console.log(`✓ ${path.relative(ROOT, file)}`);
}

console.log(`\nDone: ${injected} injected, ${skipped} already had it.`);
