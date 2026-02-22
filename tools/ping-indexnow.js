#!/usr/bin/env node
/**
 * IndexNow + Sitemap Ping — Instant search engine notification
 * Pings Bing, Yandex, Seznam, Naver (IndexNow) + Google & Bing sitemap ping
 * Called after any content change (blog posts, new pages, etc.)
 *
 * Usage: node tools/ping-indexnow.js [url1] [url2] ...
 * If no URLs provided, pings sitemap only.
 */

const https = require('https');

const SITE_HOST = 'wattsatpcontractor.com';
const INDEXNOW_KEY = 'a1b2c3d4e5f6g7h8';
const SITEMAP_URL = 'https://wattsatpcontractor.com/sitemap.xml';

// IndexNow endpoints
const INDEXNOW_ENGINES = [
  { name: 'Bing', host: 'www.bing.com' },
  { name: 'Yandex', host: 'yandex.com' },
  { name: 'Seznam', host: 'search.seznam.cz' },
  { name: 'Naver', host: 'searchadvisor.naver.com' },
];

function httpsGet(url) {
  return new Promise(function(resolve, reject) {
    https.get(url, function(res) {
      var data = '';
      res.on('data', function(c) { data += c; });
      res.on('end', function() { resolve({ status: res.statusCode, data: data }); });
    }).on('error', reject);
  });
}

function httpsPost(options, body) {
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

// ── INDEXNOW: Batch submit URLs to all engines ──
async function pingIndexNow(urls) {
  if (!urls || urls.length === 0) return;
  console.log('\n📡 IndexNow — submitting ' + urls.length + ' URL(s)...');

  var body = JSON.stringify({
    host: SITE_HOST,
    key: INDEXNOW_KEY,
    keyLocation: 'https://' + SITE_HOST + '/' + INDEXNOW_KEY + '.txt',
    urlList: urls
  });

  for (var i = 0; i < INDEXNOW_ENGINES.length; i++) {
    var engine = INDEXNOW_ENGINES[i];
    try {
      var res = await httpsPost({
        hostname: engine.host,
        path: '/indexnow',
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) }
      }, body);
      var ok = res.status >= 200 && res.status < 300;
      console.log('  ' + (ok ? '✅' : '⚠️') + ' ' + engine.name + ': HTTP ' + res.status);
    } catch (e) {
      console.log('  ❌ ' + engine.name + ': ' + e.message);
    }
  }
}

// ── SITEMAP PING: Notify Google & Bing of sitemap update ──
async function pingSitemap() {
  console.log('\n🗺️ Sitemap ping...');
  var targets = [
    { name: 'Google', url: 'https://www.google.com/ping?sitemap=' + encodeURIComponent(SITEMAP_URL) },
    { name: 'Bing', url: 'https://www.bing.com/ping?sitemap=' + encodeURIComponent(SITEMAP_URL) },
  ];

  for (var i = 0; i < targets.length; i++) {
    try {
      var res = await httpsGet(targets[i].url);
      var ok = res.status >= 200 && res.status < 300;
      console.log('  ' + (ok ? '✅' : '⚠️') + ' ' + targets[i].name + ': HTTP ' + res.status);
    } catch (e) {
      console.log('  ❌ ' + targets[i].name + ': ' + e.message);
    }
  }
}

async function main() {
  console.log('🚀 Search Engine Ping Utility');
  console.log('============================');

  // Collect URLs from CLI args
  var urls = process.argv.slice(2).filter(function(u) { return u.startsWith('http'); });

  if (urls.length > 0) {
    console.log('URLs to submit:');
    urls.forEach(function(u) { console.log('  • ' + u); });
    await pingIndexNow(urls);
  } else {
    console.log('No specific URLs provided — sitemap ping only.');
  }

  await pingSitemap();
  console.log('\n✅ Done!');
}

main().catch(function(e) { console.error('ERROR:', e.message); process.exit(1); });
