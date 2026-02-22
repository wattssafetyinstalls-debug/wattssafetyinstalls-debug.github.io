#!/usr/bin/env node
/**
 * GBP Auto-Poster v2 — Watts ATP Contractor & Watts Safety Installs
 * Automated Google Business Profile posting with AI content + stock photos.
 * Runs 3x/week via GitHub Actions (Mon/Wed/Fri).
 *
 * Requires env vars:
 *   GBP_CLIENT_ID, GBP_CLIENT_SECRET, GBP_REFRESH_TOKEN
 *   GEMINI_API_KEY
 *   PEXELS_API_KEY (optional — posts without image if missing)
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = path.resolve(__dirname, '..');
const CLIENT_ID     = process.env.GBP_CLIENT_ID;
const CLIENT_SECRET = process.env.GBP_CLIENT_SECRET;
const REFRESH_TOKEN = process.env.GBP_REFRESH_TOKEN;
const GEMINI_KEY    = process.env.GEMINI_API_KEY;
const PEXELS_KEY    = process.env.PEXELS_API_KEY || '';
const LOCATION_ID   = '09996134269287007529';

if (!CLIENT_ID || !CLIENT_SECRET || !REFRESH_TOKEN || !GEMINI_KEY) {
  console.error('ERROR: Missing required environment variables');
  console.error('Need: GBP_CLIENT_ID, GBP_CLIENT_SECRET, GBP_REFRESH_TOKEN, GEMINI_API_KEY');
  process.exit(1);
}

// ── SERVICE PAGE LINKS (for LEARN_MORE CTAs) ──
const SERVICE_LINKS = {
  atp: [
    { url: 'https://wattsatpcontractor.com/wheelchair-ramp-installation', label: 'Wheelchair Ramps' },
    { url: 'https://wattsatpcontractor.com/grab-bar-installation', label: 'Grab Bars' },
    { url: 'https://wattsatpcontractor.com/bathroom-accessibility', label: 'Bathroom Accessibility' },
    { url: 'https://wattsatpcontractor.com/non-slip-flooring-solutions', label: 'Non-Slip Flooring' },
    { url: 'https://wattsatpcontractor.com/accessibility-safety-solutions', label: 'Safety Solutions' },
  ],
  si: [
    { url: 'https://wattsatpcontractor.com/safety-installs/services/electronics', label: 'TV Mounting & Electronics' },
    { url: 'https://wattsatpcontractor.com/safety-installs/services', label: 'Home Services' },
    { url: 'https://wattsatpcontractor.com/safety-installs/contact', label: 'Get a Quote' },
  ]
};

// ── 45 TOPICS — rotated by day-of-year so content never repeats for months ──
const TOPICS = [
  // ATP — Accessibility & Safety
  { text: 'Why grab bars are the #1 fall prevention upgrade for Nebraska seniors', cat: 'atp', img: 'grab bar bathroom safety', cta: 'LEARN_MORE', link: 0 },
  { text: 'Wheelchair ramp materials: wood vs aluminum in Nebraska winters', cat: 'atp', img: 'wheelchair ramp home', cta: 'LEARN_MORE', link: 0 },
  { text: 'ADA bathroom modifications every Norfolk NE homeowner should know', cat: 'atp', img: 'accessible bathroom remodel', cta: 'LEARN_MORE', link: 2 },
  { text: 'How non-slip flooring prevents 80% of senior falls at home', cat: 'atp', img: 'non slip flooring home', cta: 'LEARN_MORE', link: 3 },
  { text: 'Planning home accessibility before winter hits Northeast Nebraska', cat: 'atp', img: 'home accessibility winter', cta: 'CALL', link: -1 },
  { text: 'Walk-in shower conversions: the most requested aging-in-place upgrade', cat: 'atp', img: 'walk in shower modern', cta: 'LEARN_MORE', link: 2 },
  { text: 'How to make your Nebraska home wheelchair accessible on a budget', cat: 'atp', img: 'wheelchair accessible home', cta: 'CALL', link: -1 },
  { text: 'Stair safety solutions for multi-level Norfolk NE homes', cat: 'atp', img: 'stair handrail safety', cta: 'LEARN_MORE', link: 4 },
  { text: 'Medicare and home accessibility: what Nebraska residents should know', cat: 'atp', img: 'senior home safety', cta: 'CALL', link: -1 },
  { text: 'Room-by-room fall prevention checklist for Nebraska seniors', cat: 'atp', img: 'senior safety home', cta: 'LEARN_MORE', link: 4 },
  { text: 'Why professional grab bar installation beats DIY every time', cat: 'atp', img: 'professional contractor installing', cta: 'LEARN_MORE', link: 1 },
  { text: 'Home accessibility assessment: what to expect from your contractor', cat: 'atp', img: 'home inspection contractor', cta: 'CALL', link: -1 },
  { text: 'Preparing your Norfolk home for a family member with mobility needs', cat: 'atp', img: 'family home accessibility', cta: 'LEARN_MORE', link: 4 },
  { text: 'How accessibility modifications increase your Nebraska home value', cat: 'atp', img: 'home value increase', cta: 'CALL', link: -1 },
  { text: 'The complete guide to threshold ramps for Nebraska doorways', cat: 'atp', img: 'threshold ramp doorway', cta: 'LEARN_MORE', link: 0 },

  // SI — Home Services
  { text: 'Kitchen remodeling trends Nebraska homeowners love right now', cat: 'si', img: 'modern kitchen remodel', cta: 'LEARN_MORE', link: 1 },
  { text: 'Interior paint colors that sell homes faster in Norfolk NE', cat: 'si', img: 'interior painting home', cta: 'LEARN_MORE', link: 1 },
  { text: 'Gutter maintenance before Nebraska storm season: a quick guide', cat: 'si', img: 'gutter cleaning maintenance', cta: 'CALL', link: -1 },
  { text: 'TV mounting tips: choosing the right wall height and bracket', cat: 'si', img: 'tv mounting living room', cta: 'LEARN_MORE', link: 0 },
  { text: 'Top 5 handyman projects that boost home value in Nebraska', cat: 'si', img: 'handyman home improvement', cta: 'LEARN_MORE', link: 1 },
  { text: 'Bathroom remodeling ideas for small Northeast Nebraska homes', cat: 'si', img: 'small bathroom remodel', cta: 'LEARN_MORE', link: 1 },
  { text: 'When to replace vs repair your gutters in Norfolk NE', cat: 'si', img: 'gutter repair replacement', cta: 'CALL', link: -1 },
  { text: 'Smart home upgrades every Norfolk homeowner should consider', cat: 'si', img: 'smart home technology', cta: 'LEARN_MORE', link: 0 },
  { text: 'Deck staining and maintenance for Northeast Nebraska weather', cat: 'si', img: 'deck staining outdoor', cta: 'CALL', link: -1 },
  { text: 'Cabinet refinishing vs replacement: cost comparison for Nebraska', cat: 'si', img: 'kitchen cabinet refinishing', cta: 'LEARN_MORE', link: 1 },
  { text: 'How to prevent ice dams on your Norfolk NE roof this winter', cat: 'si', img: 'ice dam roof winter', cta: 'CALL', link: -1 },
  { text: 'Outdoor TV mounting: weatherproofing tips for Nebraska patios', cat: 'si', img: 'outdoor tv patio', cta: 'LEARN_MORE', link: 0 },
  { text: 'Energy efficient home improvements for brutal Nebraska winters', cat: 'si', img: 'energy efficient home', cta: 'CALL', link: -1 },
  { text: 'Property maintenance checklist for Nebraska rental owners', cat: 'si', img: 'property maintenance checklist', cta: 'LEARN_MORE', link: 1 },
  { text: 'Snow removal tips to protect your Norfolk NE driveway and walkways', cat: 'si', img: 'snow removal driveway', cta: 'CALL', link: -1 },

  // Seasonal / Community (both brands)
  { text: 'Spring home maintenance checklist for Northeast Nebraska', cat: 'both', img: 'spring home maintenance', cta: 'CALL', link: -1 },
  { text: 'Summer home improvement projects worth tackling in Norfolk NE', cat: 'both', img: 'summer home improvement', cta: 'CALL', link: -1 },
  { text: 'Fall home preparation: get your Nebraska home ready before winter', cat: 'both', img: 'fall home preparation', cta: 'CALL', link: -1 },
  { text: 'Winter home safety tips every Norfolk NE family needs', cat: 'both', img: 'winter home safety', cta: 'CALL', link: -1 },
  { text: 'How to choose the right contractor in Norfolk Nebraska', cat: 'both', img: 'contractor handshake professional', cta: 'CALL', link: -1 },
  { text: 'Supporting aging parents in Nebraska: home modification guide', cat: 'both', img: 'senior parent home', cta: 'CALL', link: -1 },
  { text: 'Emergency home repairs: what to do first and who to call', cat: 'both', img: 'emergency home repair', cta: 'CALL', link: -1 },
  { text: 'Norfolk NE home improvement: projects that pay for themselves', cat: 'both', img: 'home improvement value', cta: 'CALL', link: -1 },
  { text: 'Hiring a licensed contractor in Nebraska: what to look for', cat: 'both', img: 'licensed contractor nebraska', cta: 'CALL', link: -1 },
  { text: 'Home safety for families with young children in Norfolk NE', cat: 'both', img: 'child safety home', cta: 'CALL', link: -1 },
  { text: 'Why local contractors beat national chains for Nebraska homeowners', cat: 'both', img: 'local business community', cta: 'CALL', link: -1 },
  { text: 'New year home goals: top upgrades for Norfolk NE homes', cat: 'both', img: 'new year home goals', cta: 'CALL', link: -1 },
  { text: 'Holiday home prep: getting your Nebraska house guest-ready', cat: 'both', img: 'holiday home decoration', cta: 'CALL', link: -1 },
  { text: 'Watts community spotlight: serving Northeast Nebraska families', cat: 'both', img: 'community norfolk nebraska', cta: 'CALL', link: -1 },
  { text: 'Customer story: how a simple grab bar changed everything', cat: 'atp', img: 'senior happy home safe', cta: 'LEARN_MORE', link: 1 },
];

// ── HTTPS REQUEST HELPER ──
function httpsRequest(options, body) {
  return new Promise(function(resolve, reject) {
    var req = https.request(options, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() { resolve({ status: res.statusCode, data: data }); });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

// ── CALL GEMINI ──
async function callGemini(prompt) {
  var url = new URL('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + GEMINI_KEY);
  var body = JSON.stringify({
    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    generationConfig: { temperature: 0.85, maxOutputTokens: 600, topP: 0.92 }
  });
  var res = await httpsRequest({
    hostname: url.hostname, path: url.pathname + url.search, method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
  }, body);
  var json = JSON.parse(res.data);
  var text = json.candidates && json.candidates[0] && json.candidates[0].content &&
    json.candidates[0].content.parts && json.candidates[0].content.parts[0] &&
    json.candidates[0].content.parts[0].text;
  if (!text) throw new Error('Gemini returned no text: ' + res.data.substring(0, 300));
  return text.trim();
}

// ── FETCH STOCK PHOTO FROM PEXELS ──
async function fetchPhoto(query) {
  if (!PEXELS_KEY) { console.log('  ⚠ No PEXELS_API_KEY — posting without image'); return null; }
  try {
    var q = encodeURIComponent(query);
    var res = await httpsRequest({
      hostname: 'api.pexels.com', path: '/v1/search?query=' + q + '&per_page=5&orientation=landscape',
      method: 'GET', headers: { 'Authorization': PEXELS_KEY }
    });
    var json = JSON.parse(res.data);
    if (json.photos && json.photos.length > 0) {
      // Pick a random photo from top 5 for variety
      var pick = json.photos[Math.floor(Math.random() * json.photos.length)];
      console.log('  📸 Photo: ' + pick.src.large2x.substring(0, 80) + '...');
      return pick.src.large2x; // High-res landscape
    }
    console.log('  ⚠ No Pexels results for "' + query + '" — posting without image');
    return null;
  } catch (e) {
    console.log('  ⚠ Pexels error: ' + e.message + ' — posting without image');
    return null;
  }
}

// ── GET OAUTH ACCESS TOKEN ──
async function getAccessToken() {
  var body = JSON.stringify({
    client_id: CLIENT_ID, client_secret: CLIENT_SECRET,
    refresh_token: REFRESH_TOKEN, grant_type: 'refresh_token'
  });
  var res = await httpsRequest({
    hostname: 'oauth2.googleapis.com', path: '/token', method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
  }, body);
  var json = JSON.parse(res.data);
  if (!json.access_token) throw new Error('OAuth failed: ' + res.data.substring(0, 300));
  return json.access_token;
}

// ── FIND GBP ACCOUNT ID ──
async function getAccountId(accessToken) {
  var res = await httpsRequest({
    hostname: 'mybusinessaccountmanagement.googleapis.com',
    path: '/v1/accounts', method: 'GET',
    headers: { 'Authorization': 'Bearer ' + accessToken }
  });
  var json = JSON.parse(res.data);
  if (json.accounts && json.accounts.length > 0) {
    // accounts[].name is like "accounts/123456789"
    var accountName = json.accounts[0].name;
    console.log('  Account: ' + accountName);
    return accountName;
  }
  throw new Error('No GBP accounts found: ' + res.data.substring(0, 300));
}

// ── POST TO GBP ──
async function postToGBP(accessToken, accountName, postBody) {
  var body = JSON.stringify(postBody);
  var apiPath = '/v4/' + accountName + '/locations/' + LOCATION_ID + '/localPosts';
  console.log('  API path: ' + apiPath);

  var res = await httpsRequest({
    hostname: 'mybusiness.googleapis.com', path: apiPath, method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + accessToken,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(body)
    }
  }, body);

  if (res.status >= 200 && res.status < 300) {
    return res.data;
  }
  throw new Error('GBP API ' + res.status + ': ' + res.data.substring(0, 500));
}

// ── BUILD POST BODY ──
function buildPostBody(content, topic, photoUrl) {
  var post = {
    languageCode: 'en-US',
    summary: content,
    topicType: 'STANDARD'
  };

  // Add image if available
  if (photoUrl) {
    post.media = [{ mediaFormat: 'PHOTO', sourceUrl: photoUrl }];
  }

  // Add CTA
  if (topic.cta === 'LEARN_MORE' && topic.link >= 0) {
    var links = SERVICE_LINKS[topic.cat] || SERVICE_LINKS.si;
    var linkObj = links[Math.min(topic.link, links.length - 1)];
    post.callToAction = { actionType: 'LEARN_MORE', url: linkObj.url };
  } else {
    post.callToAction = { actionType: 'CALL', url: 'tel:+14054106402' };
  }

  return post;
}

// ── GENERATE POST CONTENT ──
async function generateContent(topic) {
  var dayName = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][new Date().getDay()];
  var month = ['January','February','March','April','May','June','July','August','September','October','November','December'][new Date().getMonth()];

  var brandContext = '';
  if (topic.cat === 'atp') {
    brandContext = 'Watts ATP Contractor — Nebraska\'s premier ATP Approved Contractor for wheelchair ramps, grab bars, ADA bathroom modifications, non-slip flooring, and aging-in-place solutions.';
  } else if (topic.cat === 'si') {
    brandContext = 'Watts Safety Installs — Professional home services including kitchen & bath remodeling, painting, gutters, TV mounting, electronics, handyman, property maintenance, and seasonal services.';
  } else {
    brandContext = 'Watts ATP Contractor & Watts Safety Installs — Licensed Nebraska contractor (#54690-25) offering accessibility modifications, home remodeling, and professional home services.';
  }

  var prompt = 'You are Justin Watts, owner of ' + brandContext + ' Based in Norfolk, NE. Serving a 100-mile radius across Northeast Nebraska and Northwest Iowa.\n\n' +
    'Write a Google Business Profile post about: "' + topic.text + '"\n\n' +
    'CONTEXT: It is ' + dayName + ' in ' + month + '. You are writing as Justin — the actual owner, not a marketing team.\n\n' +
    'REQUIREMENTS:\n' +
    '- 100-150 words MAXIMUM. GBP posts must be concise.\n' +
    '- Write in first person as Justin. Warm, knowledgeable, hands-on tone.\n' +
    '- Open with a hook that stops the scroll — a question, surprising fact, or relatable scenario.\n' +
    '- Include ONE practical tip or insight the reader can use immediately.\n' +
    '- Mention Norfolk, NE or Northeast Nebraska naturally (not forced).\n' +
    '- Reference your license (#54690-25) or experience ONLY if it fits naturally.\n' +
    '- End with a clear call-to-action: call (405) 410-6402 for a free estimate.\n' +
    '- Use 1-2 emojis max. No hashtags. No bullet points.\n' +
    '- Do NOT start with "Hey" or "Hi there" — start with the hook.\n' +
    '- Sound like a real person, not a template. Vary your openings.\n' +
    '- If seasonal, reference current ' + month + ' conditions in Nebraska.\n\n' +
    'Return ONLY the post text. No title, no quotes, no formatting marks.';

  return await callGemini(prompt);
}

// ── PICK TODAY'S TOPIC ──
function pickTopic() {
  // Use day-of-year so each run gets a different topic
  var now = new Date();
  var start = new Date(now.getFullYear(), 0, 0);
  var dayOfYear = Math.floor((now - start) / (24 * 60 * 60 * 1000));
  return TOPICS[dayOfYear % TOPICS.length];
}

// ── MAIN ──
async function main() {
  console.log('🤖 Watts GBP Auto-Poster v2');
  console.log('===========================');
  console.log('Time: ' + new Date().toISOString() + '\n');

  var topic = pickTopic();
  console.log('📝 Topic: ' + topic.text);
  console.log('   Category: ' + topic.cat + ' | CTA: ' + topic.cta);

  try {
    // Step 1: Generate content
    console.log('\n1. Generating content...');
    var content = await generateContent(topic);
    console.log('   ✅ Content ready (' + content.length + ' chars)');
    console.log('   Preview: ' + content.substring(0, 100) + '...');

    // Step 2: Fetch stock photo
    console.log('\n2. Fetching photo...');
    var photoUrl = await fetchPhoto(topic.img);

    // Step 3: Get OAuth token
    console.log('\n3. Authenticating...');
    var accessToken = await getAccessToken();
    console.log('   ✅ Token acquired');

    // Step 4: Get account ID
    console.log('\n4. Finding GBP account...');
    var accountName = await getAccountId(accessToken);

    // Step 5: Build and publish post
    console.log('\n5. Publishing to GBP...');
    var postBody = buildPostBody(content, topic, photoUrl);
    var result = await postToGBP(accessToken, accountName, postBody);
    console.log('   ✅ Post published!');

    // Log result
    var logEntry = '═══ GBP POST PUBLISHED ═══\n' +
      'Date: ' + new Date().toISOString() + '\n' +
      'Topic: ' + topic.text + '\n' +
      'Category: ' + topic.cat + '\n' +
      'CTA: ' + topic.cta + '\n' +
      'Photo: ' + (photoUrl ? 'Yes' : 'No') + '\n' +
      '───────────────────────\n' +
      content + '\n' +
      '───────────────────────\n' +
      'API Response: ' + result.substring(0, 500) + '\n';

    // Append to log file
    var logPath = path.join(ROOT, 'tools', 'gbp-post-log.txt');
    var existing = fs.existsSync(logPath) ? fs.readFileSync(logPath, 'utf8') : '';
    fs.writeFileSync(logPath, logEntry + '\n' + existing, 'utf8');

    console.log('\n✅ Done! Post is live on Google Business Profile.');

  } catch (err) {
    console.error('\n❌ ERROR:', err.message);

    var errorLog = 'GBP Post FAILED - ' + new Date().toISOString() + '\n' +
      'Topic: ' + topic.text + '\nError: ' + err.message + '\n\n';
    var logPath = path.join(ROOT, 'tools', 'gbp-post-log.txt');
    var existing = fs.existsSync(logPath) ? fs.readFileSync(logPath, 'utf8') : '';
    fs.writeFileSync(logPath, errorLog + existing, 'utf8');

    process.exit(1);
  }
}

main();
