#!/usr/bin/env node
/**
 * Auto Blog Generator — Watts ATP Contractor & Watts Safety Installs
 * Generates a weekly SEO blog post using Gemini AI.
 * Called by GitHub Actions on a weekly schedule.
 * 
 * Requires: GEMINI_API_KEY environment variable
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = path.resolve(__dirname, '..');
const API_KEY = process.env.GEMINI_API_KEY;
const MODEL = 'gemini-2.5-flash';

if (!API_KEY) {
  console.error('ERROR: GEMINI_API_KEY environment variable not set');
  process.exit(1);
}

// ── TOPIC POOLS ──
const ATP_TOPICS = [
  'Benefits of wheelchair ramps for aging in place in Nebraska',
  'How grab bars prevent falls: a guide for Nebraska seniors',
  'ADA bathroom modifications: what every Nebraska homeowner should know',
  'Non-slip flooring options for safer homes in Northeast Nebraska',
  'Planning home accessibility modifications before winter in Nebraska',
  'How to choose the right wheelchair ramp material for Nebraska weather',
  'Bathroom safety checklist for seniors living in Norfolk NE',
  'Understanding ADA compliance for residential homes in Nebraska',
  'Top 5 home modifications for aging in place safely',
  'Why professional grab bar installation matters: avoiding DIY mistakes',
  'Stair safety solutions for multi-level Nebraska homes',
  'How accessibility modifications increase home value in Nebraska',
  'Medicare and Medicaid coverage for home accessibility in Nebraska',
  'Preparing your Norfolk NE home for a family member with mobility needs',
  'Seasonal home safety tips for seniors in Northeast Nebraska',
  'The complete guide to walk-in shower conversions in Nebraska',
  'How to make your Nebraska home wheelchair accessible on a budget',
  'Fall prevention strategies for Nebraska seniors: room by room guide',
  'Choosing between wood and aluminum wheelchair ramps in Nebraska',
  'Home accessibility assessment: what to expect from Watts ATP Contractor',
];

const SI_TOPICS = [
  'Kitchen remodeling trends for Nebraska homes in 2025',
  'How to choose the right paint colors for your Norfolk NE home',
  'Gutter maintenance guide for Northeast Nebraska homeowners',
  'Top handyman projects that increase home value in Nebraska',
  'TV mounting tips: choosing the right wall and height',
  'Preparing your Norfolk NE home for winter: a complete checklist',
  'Bathroom remodeling ideas for small Nebraska homes',
  'When to replace vs repair your gutters in Northeast Nebraska',
  'Smart home upgrades every Norfolk NE homeowner should consider',
  'Spring home maintenance checklist for Nebraska homeowners',
  'How to budget for a kitchen remodel in Norfolk Nebraska',
  'Interior painting preparation: the steps most homeowners skip',
  'Gutter guard systems: are they worth it in Nebraska weather',
  'Handyman vs contractor: when to call which for your Nebraska home',
  'Outdoor TV mounting: weatherproofing tips for Nebraska',
  'Energy efficient home improvements for Nebraska winters',
  'Deck staining and maintenance for Northeast Nebraska homes',
  'Cabinet refinishing vs replacement: a cost comparison for Nebraska',
  'How to prevent ice dams on your Norfolk NE home',
  'Summer home improvement projects for Northeast Nebraska',
];

// ── PICK TOPIC ──
function pickTopic(topics) {
  // Use week number to rotate through topics so we don't repeat
  const weekNum = Math.floor((Date.now() - new Date('2025-01-01').getTime()) / (7 * 24 * 60 * 60 * 1000));
  return topics[weekNum % topics.length];
}

// ── CALL GEMINI ──
function callGemini(prompt) {
  return new Promise(function(resolve, reject) {
    var url = 'https://generativelanguage.googleapis.com/v1beta/models/' + MODEL + ':generateContent?key=' + API_KEY;
    var body = JSON.stringify({
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.8, maxOutputTokens: 2048, topP: 0.9 }
    });

    var parsed = new URL(url);
    var options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
    };

    var req = https.request(options, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        try {
          var json = JSON.parse(data);
          var text = json.candidates && json.candidates[0] && json.candidates[0].content && json.candidates[0].content.parts && json.candidates[0].content.parts[0] && json.candidates[0].content.parts[0].text;
          if (text) resolve(text);
          else reject(new Error('No text in response: ' + data.substring(0, 200)));
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ── GENERATE BLOG POST ──
async function generatePost(brand, topic, outDir, brandConfig) {
  var prompt = 'Write a 600-800 word SEO blog post for ' + brandConfig.name + ' in Norfolk, Nebraska.\n\n' +
    'TOPIC: ' + topic + '\n\n' +
    'REQUIREMENTS:\n' +
    '- Write for homeowners in Northeast Nebraska\n' +
    '- Include the city "Norfolk, NE" and "Northeast Nebraska" naturally 2-3 times\n' +
    '- Mention ' + brandConfig.name + ' by name once or twice\n' +
    '- Include a call-to-action to call (405) 410-6402 for a free estimate\n' +
    '- Use H2 subheadings (## format) to break up sections\n' +
    '- Be helpful, informative, and warm — not salesy\n' +
    '- Include practical tips homeowners can use\n' +
    '- Mention Nebraska License #54690-25 once\n' +
    '- End with a strong CTA paragraph\n\n' +
    'OUTPUT FORMAT: Return ONLY the blog content in markdown format. Start with a # title.';

  console.log('Generating: ' + topic);
  var content = await callGemini(prompt);

  // Extract title from markdown
  var titleMatch = content.match(/^#\s+(.+)/m);
  var title = titleMatch ? titleMatch[1].trim() : topic;
  var slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '').substring(0, 60);
  var date = new Date().toISOString().split('T')[0];
  var filename = date + '-' + slug + '.html';

  // Convert markdown to HTML
  var htmlContent = content
    .replace(/^# (.+)/gm, '<h1>$1</h1>')
    .replace(/^## (.+)/gm, '<h2>$1</h2>')
    .replace(/^### (.+)/gm, '<h3>$1</h3>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^- (.+)/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, ' ');
  htmlContent = '<p>' + htmlContent + '</p>';
  htmlContent = htmlContent.replace(/<p>\s*<h([123])>/g, '<h$1>').replace(/<\/h([123])>\s*<\/p>/g, '</h$1>');
  htmlContent = htmlContent.replace(/<p>\s*<ul>/g, '<ul>').replace(/<\/ul>\s*<\/p>/g, '</ul>');
  htmlContent = htmlContent.replace(/<p>\s*<\/p>/g, '');

  var canonical = brandConfig.baseUrl + '/blog/' + slug;
  var metaDesc = title + ' — Expert tips from ' + brandConfig.name + ' in Norfolk, NE. Licensed contractor serving Northeast Nebraska. Call (405) 410-6402.';
  if (metaDesc.length > 160) metaDesc = metaDesc.substring(0, 157) + '...';

  var html = '<!DOCTYPE html>\n<html lang="en">\n<head>\n' +
    '<meta charset="utf-8"/>\n<meta content="width=device-width, initial-scale=1.0" name="viewport"/>\n' +
    '<title>' + title + ' | ' + brandConfig.name + '</title>\n' +
    '<meta content="' + metaDesc + '" name="description"/>\n' +
    '<link href="' + canonical + '" rel="canonical"/>\n' +
    '<meta content="' + title + ' | ' + brandConfig.name + '" property="og:title"/>\n' +
    '<meta content="' + metaDesc + '" property="og:description"/>\n' +
    '<meta content="article" property="og:type"/>\n' +
    '<meta content="index, follow" name="robots"/>\n' +
    '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet"/>\n' +
    '<style>\n' + brandConfig.css + '\n' +
    'article{max-width:740px;margin:0 auto;padding:40px 20px}\n' +
    'article h1{font-family:"Playfair Display",serif;font-size:2rem;margin-bottom:8px;color:' + brandConfig.heading + '}\n' +
    'article h2{font-size:1.4rem;color:' + brandConfig.heading + ';margin:28px 0 12px}\n' +
    'article p{color:#444;font-size:1rem;line-height:1.8;margin-bottom:16px}\n' +
    'article ul{margin:12px 0 16px 20px;color:#444}\n' +
    'article li{margin-bottom:8px;line-height:1.6}\n' +
    'article strong{color:#222}\n' +
    '.blog-meta{color:#64748B;font-size:.9rem;margin-bottom:24px}\n' +
    '.blog-cta{background:' + brandConfig.ctaBg + ';border-radius:16px;padding:32px;text-align:center;color:#fff;margin:32px 0}\n' +
    '.blog-cta h2{color:#fff;margin:0 0 12px}\n' +
    '.blog-cta a{color:#fff;font-size:1.2rem;font-weight:700;text-decoration:none}\n' +
    'header{background:' + brandConfig.headerBg + ';padding:16px 0}\n' +
    '.nav-c{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;padding:0 20px}\n' +
    '.logo{font-family:"Playfair Display",serif;font-size:1.6rem;color:' + brandConfig.logoCl + ';text-decoration:none;font-weight:700}\n' +
    'footer{background:' + brandConfig.headerBg + ';color:rgba(255,255,255,.7);text-align:center;padding:24px;font-size:.85rem}\n' +
    'footer a{color:' + brandConfig.footerLink + ';text-decoration:none}\n' +
    '@media(max-width:600px){article h1{font-size:1.5rem}}\n' +
    '</style>\n' +
    '<script type="application/ld+json">\n' +
    '{"@context":"https://schema.org","@type":"BlogPosting","headline":"' + title.replace(/"/g, '\\"') + '","datePublished":"' + date + '","author":{"@type":"Organization","name":"' + brandConfig.name + '"},"publisher":{"@type":"Organization","name":"' + brandConfig.name + '"}}\n' +
    '</script>\n' +
    '</head>\n<body>\n' +
    '<header><div class="nav-c"><a class="logo" href="' + brandConfig.homeUrl + '">' + brandConfig.logoText + '</a></div></header>\n' +
    '<article>\n' +
    '<p class="blog-meta">Published ' + date + ' · ' + brandConfig.name + '</p>\n' +
    htmlContent + '\n' +
    '<div class="blog-cta">\n' +
    '<h2>Need Help? We\'re Here for You.</h2>\n' +
    '<p>Call today for a free, no-obligation estimate.</p>\n' +
    '<a href="tel:+14054106402">(405) 410-6402</a>\n' +
    '</div>\n' +
    '</article>\n' +
    '<footer><p>&copy; ' + new Date().getFullYear() + ' ' + brandConfig.name + ' — Nebraska Licensed #54690-25</p>' +
    '<p style="margin-top:6px"><a href="' + brandConfig.homeUrl + '">Home</a> · <a href="' + brandConfig.homeUrl + (brandConfig.homeUrl === '/' ? '' : '/') + 'services">Services</a> · <a href="' + brandConfig.homeUrl + (brandConfig.homeUrl === '/' ? '' : '/') + 'contact">Contact</a></p></footer>\n' +
    '<script src="/js/watts-ai-chat.js" defer></script>\n' +
    '</body>\n</html>';

  var blogDir = path.join(ROOT, outDir, 'blog');
  if (!fs.existsSync(blogDir)) fs.mkdirSync(blogDir, { recursive: true });
  fs.writeFileSync(path.join(blogDir, filename), html, 'utf8');
  console.log('  → ' + outDir + '/blog/' + filename);
  return { title: title, slug: slug, date: date, url: canonical };
}

// ── MAIN ──
async function main() {
  console.log('🤖 Watts Auto Blog Generator');
  console.log('============================\n');

  var atpTopic = pickTopic(ATP_TOPICS);
  var siTopic = pickTopic(SI_TOPICS);

  var atpConfig = {
    name: 'Watts ATP Contractor',
    baseUrl: 'https://wattsatpcontractor.com',
    homeUrl: '/',
    logoText: 'Watts ATP',
    logoCl: '#00C4B4',
    heading: '#0A1D37',
    headerBg: '#0A1D37',
    ctaBg: 'linear-gradient(135deg,#00C4B4,#009e91)',
    footerLink: '#FFD700',
    css: '*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Inter",sans-serif;background:#FEF7ED;color:#1E293B;line-height:1.7}'
  };

  var siConfig = {
    name: 'Watts Safety Installs',
    baseUrl: 'https://wattsatpcontractor.com/safety-installs',
    homeUrl: '/safety-installs/',
    logoText: 'Safety Installs',
    logoCl: '#dc2626',
    heading: '#1a1a1a',
    headerBg: '#1a1a1a',
    ctaBg: 'linear-gradient(135deg,#dc2626,#b91c1c)',
    footerLink: '#f5f5dc',
    css: '*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Inter",sans-serif;background:#FEF7ED;color:#1E293B;line-height:1.7}'
  };

  try {
    var atp = await generatePost('atp', atpTopic, '.', atpConfig);
    var si = await generatePost('si', siTopic, 'safety-installs', siConfig);

    // Update sitemap
    var smPath = path.join(ROOT, 'sitemap.xml');
    if (fs.existsSync(smPath)) {
      var sm = fs.readFileSync(smPath, 'utf8');
      var today = new Date().toISOString().split('T')[0];
      var entries = '';
      entries += '  <url>\n    <loc>' + atp.url + '</loc>\n    <lastmod>' + today + '</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n';
      entries += '  <url>\n    <loc>' + si.url + '</loc>\n    <lastmod>' + today + '</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n';
      sm = sm.replace('</urlset>', entries + '</urlset>');
      fs.writeFileSync(smPath, sm, 'utf8');
      console.log('\n✅ Sitemap updated');
    }

    console.log('\n✅ Done! 2 blog posts generated and ready to commit.');
  } catch (err) {
    console.error('ERROR:', err.message);
    process.exit(1);
  }
}

main();
