#!/usr/bin/env node
/**
 * Web Stories Generator — Watts ATP Contractor & Watts Safety Installs
 * Creates AMP Web Stories from blog posts for Google Discover traffic.
 * Each story is a full-screen, swipeable visual experience.
 *
 * Requires: GEMINI_API_KEY, PEXELS_API_KEY (optional) env vars
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = path.resolve(__dirname, '..');
const GEMINI_KEY = process.env.GEMINI_API_KEY;
const PEXELS_KEY = process.env.PEXELS_API_KEY || '';

function httpsRequest(options, body) {
  return new Promise(function(resolve, reject) {
    var req = https.request(options, function(res) {
      var data = '';
      res.on('data', function(c) { data += c; });
      res.on('end', function() { resolve({ status: res.statusCode, data: data }); });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function callGemini(prompt) {
  var url = new URL('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + GEMINI_KEY);
  var body = JSON.stringify({
    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    generationConfig: { temperature: 0.85, maxOutputTokens: 1200, topP: 0.9 }
  });
  var res = await httpsRequest({
    hostname: url.hostname, path: url.pathname + url.search, method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
  }, body);
  var json = JSON.parse(res.data);
  var text = json.candidates && json.candidates[0] && json.candidates[0].content &&
    json.candidates[0].content.parts && json.candidates[0].content.parts[0] &&
    json.candidates[0].content.parts[0].text;
  if (!text) throw new Error('Gemini error: ' + res.data.substring(0, 300));
  return text.trim();
}

async function fetchPhoto(query) {
  if (!PEXELS_KEY) return 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1080&h=1920&fit=crop';
  try {
    var q = encodeURIComponent(query);
    var res = await httpsRequest({
      hostname: 'api.pexels.com', path: '/v1/search?query=' + q + '&per_page=6&orientation=portrait',
      method: 'GET', headers: { 'Authorization': PEXELS_KEY }
    });
    var json = JSON.parse(res.data);
    if (json.photos && json.photos.length > 0) {
      return json.photos[Math.floor(Math.random() * Math.min(json.photos.length, 6))].src.large2x;
    }
  } catch (e) { /* fallback */ }
  return 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1080&h=1920&fit=crop';
}

// ── STORY TOPICS ──
const STORY_TOPICS = [
  { title: '5 Signs Your Nebraska Home Needs Grab Bars', cat: 'atp', images: ['grab bar bathroom', 'senior safety home', 'bathroom remodel accessible', 'family helping senior', 'contractor installing'] },
  { title: 'Wheelchair Ramp 101: Wood vs Aluminum', cat: 'atp', images: ['wheelchair ramp wood', 'aluminum ramp home', 'wheelchair accessibility', 'nebraska home winter', 'contractor building ramp'] },
  { title: 'Kitchen Remodel Ideas for Nebraska Homes', cat: 'si', images: ['modern kitchen remodel', 'kitchen countertop granite', 'kitchen cabinet white', 'kitchen island design', 'contractor kitchen work'] },
  { title: 'Fall Prevention Tips for Seniors', cat: 'atp', images: ['senior walking safely', 'non slip flooring', 'grab bar shower', 'well lit hallway', 'home safety senior'] },
  { title: 'TV Mounting: 5 Mistakes to Avoid', cat: 'si', images: ['tv mounted wall', 'tv mounting bracket', 'living room tv', 'cable management wall', 'smart home setup'] },
  { title: 'Winter Home Prep Checklist: Nebraska Edition', cat: 'both', images: ['winter home nebraska', 'gutter ice dam', 'insulation home', 'thermostat heating', 'snow removal driveway'] },
  { title: 'Bathroom Accessibility Upgrades That Look Great', cat: 'atp', images: ['modern accessible bathroom', 'walk in shower', 'bathroom vanity accessible', 'grab bar stylish', 'bathroom remodel'] },
  { title: 'Gutter Maintenance: Save Thousands', cat: 'si', images: ['gutter cleaning', 'gutter damage leaves', 'rain gutter repair', 'water damage foundation', 'professional gutter service'] },
  { title: 'How to Choose a Contractor in Nebraska', cat: 'both', images: ['contractor handshake', 'license certificate', 'home inspection', 'contractor tools', 'happy homeowner'] },
  { title: 'Aging in Place: Make Your Home Safe', cat: 'atp', images: ['senior happy home', 'accessible home entry', 'stair lift home', 'bathroom safety senior', 'family multigenerational'] },
];

function buildStoryHTML(title, slides, brandConfig, slug) {
  var canonical = brandConfig.baseUrl + '/stories/' + slug;
  var storyPages = '';

  // Cover page
  storyPages += '    <amp-story-page id="cover">\n' +
    '      <amp-story-grid-layer template="fill">\n' +
    '        <amp-img src="' + slides[0].image + '" width="720" height="1280" layout="responsive" alt="' + escAttr(title) + '"></amp-img>\n' +
    '      </amp-story-grid-layer>\n' +
    '      <amp-story-grid-layer template="vertical" class="bottom">\n' +
    '        <div class="overlay">\n' +
    '          <h1>' + escHtml(title) + '</h1>\n' +
    '          <p class="byline">By Justin Watts · ' + brandConfig.name + '</p>\n' +
    '        </div>\n' +
    '      </amp-story-grid-layer>\n' +
    '    </amp-story-page>\n';

  // Content pages
  for (var i = 0; i < slides.length; i++) {
    storyPages += '    <amp-story-page id="page-' + (i + 1) + '">\n' +
      '      <amp-story-grid-layer template="fill">\n' +
      '        <amp-img src="' + slides[i].image + '" width="720" height="1280" layout="responsive" alt="' + escAttr(slides[i].heading) + '"></amp-img>\n' +
      '      </amp-story-grid-layer>\n' +
      '      <amp-story-grid-layer template="vertical" class="bottom">\n' +
      '        <div class="overlay">\n' +
      '          <h2>' + escHtml(slides[i].heading) + '</h2>\n' +
      '          <p>' + escHtml(slides[i].text) + '</p>\n' +
      '        </div>\n' +
      '      </amp-story-grid-layer>\n' +
      '    </amp-story-page>\n';
  }

  // CTA page
  storyPages += '    <amp-story-page id="cta">\n' +
    '      <amp-story-grid-layer template="fill">\n' +
    '        <amp-img src="' + slides[0].image + '" width="720" height="1280" layout="responsive" alt="Contact us"></amp-img>\n' +
    '      </amp-story-grid-layer>\n' +
    '      <amp-story-grid-layer template="vertical" class="center">\n' +
    '        <div class="cta-overlay">\n' +
    '          <h2>Need Help?</h2>\n' +
    '          <p>Free estimates for Norfolk, NE &amp; surrounding areas</p>\n' +
    '          <p class="phone">(405) 410-6402</p>\n' +
    '        </div>\n' +
    '      </amp-story-grid-layer>\n' +
    '    </amp-story-page>\n';

  return '<!DOCTYPE html>\n' +
    '<html amp lang="en">\n' +
    '<head>\n' +
    '  <meta charset="utf-8">\n' +
    '  <script async src="https://cdn.ampproject.org/v0.js"></script>\n' +
    '  <script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>\n' +
    '  <title>' + escHtml(title) + ' | ' + brandConfig.name + '</title>\n' +
    '  <meta name="description" content="' + escAttr(title) + ' — Tips from ' + brandConfig.name + ' in Norfolk, NE.">\n' +
    '  <link rel="canonical" href="' + canonical + '">\n' +
    '  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">\n' +
    '  <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;animation:none}</style></noscript>\n' +
    '  <style amp-custom>\n' +
    '    amp-story { font-family: "Inter", sans-serif; }\n' +
    '    .overlay { background: linear-gradient(transparent, rgba(0,0,0,0.85)); padding: 32px 24px; color: #fff; }\n' +
    '    .cta-overlay { background: rgba(0,0,0,0.8); padding: 40px 24px; color: #fff; text-align: center; border-radius: 16px; margin: 0 16px; }\n' +
    '    h1 { font-size: 28px; font-weight: 700; line-height: 1.2; margin-bottom: 8px; }\n' +
    '    h2 { font-size: 22px; font-weight: 700; line-height: 1.3; margin-bottom: 8px; color: #fff; }\n' +
    '    p { font-size: 16px; line-height: 1.5; color: rgba(255,255,255,0.9); }\n' +
    '    .byline { font-size: 14px; color: rgba(255,255,255,0.7); }\n' +
    '    .phone { font-size: 28px; font-weight: 700; color: ' + brandConfig.accent + '; margin-top: 16px; }\n' +
    '    .bottom { justify-content: flex-end; }\n' +
    '    .center { justify-content: center; align-items: center; }\n' +
    '  </style>\n' +
    '  <script type="application/ld+json">\n' +
    '  {\n' +
    '    "@context": "https://schema.org",\n' +
    '    "@type": "WebPage",\n' +
    '    "name": "' + escAttr(title) + '",\n' +
    '    "url": "' + canonical + '",\n' +
    '    "publisher": {\n' +
    '      "@type": "Organization",\n' +
    '      "name": "' + brandConfig.name + '",\n' +
    '      "logo": { "@type": "ImageObject", "url": "https://wattsatpcontractor.com/favicon-96x96.png" }\n' +
    '    }\n' +
    '  }\n' +
    '  </script>\n' +
    '</head>\n' +
    '<body>\n' +
    '  <amp-story standalone\n' +
    '    title="' + escAttr(title) + '"\n' +
    '    publisher="' + brandConfig.name + '"\n' +
    '    publisher-logo-src="https://wattsatpcontractor.com/favicon-96x96.png"\n' +
    '    poster-portrait-src="' + slides[0].image + '">\n' +
    storyPages +
    '  </amp-story>\n' +
    '</body>\n' +
    '</html>\n';
}

function escHtml(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function escAttr(s) { return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }

async function generateStory(topic, brandConfig) {
  var prompt = 'Create a 5-slide Web Story (short-form visual content like Instagram Stories) about: "' + topic.title + '"\n\n' +
    'You are Justin Watts, owner of ' + brandConfig.name + ' in Norfolk, NE.\n\n' +
    'Return EXACTLY 5 slides in this JSON format (no markdown, no code fences):\n' +
    '[{"heading":"Short punchy headline","text":"1-2 sentences of helpful info"},{"heading":"...","text":"..."},...]\n\n' +
    'Rules:\n' +
    '- Each heading: max 6 words, attention-grabbing\n' +
    '- Each text: max 25 words, practical tip\n' +
    '- Write as Justin — warm, expert, helpful\n' +
    '- Mention Norfolk NE or Nebraska in 1-2 slides\n' +
    '- Last slide should be a soft CTA\n' +
    '- Return ONLY the JSON array, nothing else.';

  var raw = await callGemini(prompt);
  // Clean any markdown fences
  raw = raw.replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();
  var slides = JSON.parse(raw);
  if (!Array.isArray(slides) || slides.length < 3) throw new Error('Invalid slides: ' + raw.substring(0, 200));

  // Fetch images for each slide
  for (var i = 0; i < slides.length && i < topic.images.length; i++) {
    slides[i].image = await fetchPhoto(topic.images[i]);
  }
  // Fill remaining with first image
  for (var j = 0; j < slides.length; j++) {
    if (!slides[j].image) slides[j].image = slides[0].image;
  }

  return slides;
}

async function main() {
  console.log('📖 Web Stories Generator');
  console.log('======================\n');

  if (!GEMINI_KEY) { console.error('ERROR: GEMINI_API_KEY required'); process.exit(1); }

  var atpConfig = { name: 'Watts ATP Contractor', baseUrl: 'https://wattsatpcontractor.com', accent: '#00C4B4' };
  var siConfig = { name: 'Watts Safety Installs', baseUrl: 'https://wattsatpcontractor.com/safety-installs', accent: '#dc2626' };

  // Pick one story per brand based on week
  var weekNum = Math.floor((Date.now() - new Date('2025-01-01').getTime()) / (7 * 24 * 60 * 60 * 1000));
  var atpTopics = STORY_TOPICS.filter(function(t) { return t.cat === 'atp' || t.cat === 'both'; });
  var siTopics = STORY_TOPICS.filter(function(t) { return t.cat === 'si' || t.cat === 'both'; });
  var atpTopic = atpTopics[weekNum % atpTopics.length];
  var siTopic = siTopics[weekNum % siTopics.length];

  var allUrls = [];
  var date = new Date().toISOString().split('T')[0];

  try {
    // ATP Story
    console.log('Generating ATP story: ' + atpTopic.title);
    var atpSlides = await generateStory(atpTopic, atpConfig);
    var atpSlug = date + '-' + atpTopic.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 50);
    var atpHtml = buildStoryHTML(atpTopic.title, atpSlides, atpConfig, atpSlug);
    var atpDir = path.join(ROOT, 'stories');
    if (!fs.existsSync(atpDir)) fs.mkdirSync(atpDir, { recursive: true });
    fs.writeFileSync(path.join(atpDir, atpSlug + '.html'), atpHtml, 'utf8');
    allUrls.push(atpConfig.baseUrl + '/stories/' + atpSlug);
    console.log('  ✅ stories/' + atpSlug + '.html');

    // SI Story
    console.log('Generating SI story: ' + siTopic.title);
    var siSlides = await generateStory(siTopic, siConfig);
    var siSlug = date + '-' + siTopic.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 50);
    var siHtml = buildStoryHTML(siTopic.title, siSlides, siConfig, siSlug);
    var siDir = path.join(ROOT, 'safety-installs', 'stories');
    if (!fs.existsSync(siDir)) fs.mkdirSync(siDir, { recursive: true });
    fs.writeFileSync(path.join(siDir, siSlug + '.html'), siHtml, 'utf8');
    allUrls.push(siConfig.baseUrl + '/stories/' + siSlug);
    console.log('  ✅ safety-installs/stories/' + siSlug + '.html');

    // Update sitemap with story URLs
    var smPath = path.join(ROOT, 'sitemap.xml');
    if (fs.existsSync(smPath)) {
      var sm = fs.readFileSync(smPath, 'utf8');
      var today = new Date().toISOString().split('T')[0];
      var entries = '';
      allUrls.forEach(function(u) {
        entries += '  <url>\n    <loc>' + u + '</loc>\n    <lastmod>' + today + '</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.5</priority>\n  </url>\n';
      });
      sm = sm.replace('</urlset>', entries + '</urlset>');
      fs.writeFileSync(smPath, sm, 'utf8');
      console.log('\n✅ Sitemap updated with story URLs');
    }

    console.log('\n✅ Done! ' + allUrls.length + ' Web Stories generated.');
    // Output URLs for ping script
    allUrls.forEach(function(u) { console.log('URL:' + u); });

  } catch (err) {
    console.error('ERROR:', err.message);
    process.exit(1);
  }
}

main();
