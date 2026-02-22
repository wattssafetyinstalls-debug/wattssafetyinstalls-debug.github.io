#!/usr/bin/env node
/**
 * Google Indexing API — Force Google to crawl/index URLs immediately
 * Uses a Google Cloud service account for authentication.
 * Free tier: 200 URL submissions per day.
 *
 * Setup:
 * 1. In Google Cloud Console (same project as GBP OAuth):
 *    - Enable "Web Search Indexing API"
 *    - Create a Service Account → download JSON key
 * 2. In Google Search Console:
 *    - Add the service account email as an Owner
 * 3. Add the JSON key as GitHub secret: GOOGLE_INDEXING_KEY
 *
 * Usage: node tools/google-indexing-api.js [url1] [url2] ...
 * Env: GOOGLE_INDEXING_KEY (base64-encoded service account JSON)
 */

const https = require('https');
const crypto = require('crypto');

var KEY_JSON_B64 = process.env.GOOGLE_INDEXING_KEY || '';

function base64url(buf) {
  return buf.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function createJWT(email, privateKey) {
  var now = Math.floor(Date.now() / 1000);
  var header = { alg: 'RS256', typ: 'JWT' };
  var payload = {
    iss: email,
    scope: 'https://www.googleapis.com/auth/indexing',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600
  };

  var segments = [
    base64url(Buffer.from(JSON.stringify(header))),
    base64url(Buffer.from(JSON.stringify(payload)))
  ];
  var signingInput = segments.join('.');
  var sign = crypto.createSign('RSA-SHA256');
  sign.update(signingInput);
  var signature = sign.sign(privateKey);
  segments.push(base64url(signature));
  return segments.join('.');
}

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

async function getAccessToken(email, privateKey) {
  var jwt = createJWT(email, privateKey);
  var body = 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=' + jwt;
  var res = await httpsRequest({
    hostname: 'oauth2.googleapis.com',
    path: '/token',
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': Buffer.byteLength(body) }
  }, body);

  if (res.status !== 200) throw new Error('Token error: ' + res.data);
  return JSON.parse(res.data).access_token;
}

async function submitUrl(accessToken, url, type) {
  type = type || 'URL_UPDATED';
  var body = JSON.stringify({ url: url, type: type });
  var res = await httpsRequest({
    hostname: 'indexing.googleapis.com',
    path: '/v3/urlNotifications:publish',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + accessToken,
      'Content-Length': Buffer.byteLength(body)
    }
  }, body);

  return { status: res.status, data: JSON.parse(res.data) };
}

async function main() {
  console.log('🔍 Google Indexing API');
  console.log('====================\n');

  if (!KEY_JSON_B64) {
    console.log('⚠️  GOOGLE_INDEXING_KEY not set. Skipping Google Indexing API.');
    console.log('   To enable: add base64-encoded service account JSON as a GitHub secret.');
    process.exit(0);
  }

  var keyData;
  try {
    keyData = JSON.parse(Buffer.from(KEY_JSON_B64, 'base64').toString('utf8'));
  } catch (e) {
    console.error('ERROR: Invalid GOOGLE_INDEXING_KEY format. Must be base64-encoded JSON.');
    process.exit(1);
  }

  var urls = process.argv.slice(2).filter(function(u) { return u.startsWith('http'); });
  if (urls.length === 0) {
    console.log('No URLs provided. Usage: node google-indexing-api.js [url1] [url2] ...');
    process.exit(0);
  }

  console.log('Authenticating as: ' + keyData.client_email);
  var token = await getAccessToken(keyData.client_email, keyData.private_key);
  console.log('✅ Authenticated\n');

  console.log('Submitting ' + urls.length + ' URL(s) to Google...');
  var success = 0;
  var failed = 0;

  for (var i = 0; i < urls.length && i < 200; i++) {
    try {
      var result = await submitUrl(token, urls[i]);
      if (result.status === 200) {
        console.log('  ✅ ' + urls[i]);
        success++;
      } else {
        console.log('  ⚠️ ' + urls[i] + ' — ' + (result.data.error ? result.data.error.message : 'HTTP ' + result.status));
        failed++;
      }
    } catch (e) {
      console.log('  ❌ ' + urls[i] + ' — ' + e.message);
      failed++;
    }
    // Small delay to respect rate limits
    if (i < urls.length - 1) await new Promise(function(r) { setTimeout(r, 200); });
  }

  console.log('\n📊 Results: ' + success + ' submitted, ' + failed + ' failed');
  if (urls.length > 200) console.log('⚠️ Only first 200 URLs submitted (daily quota)');
}

main().catch(function(e) { console.error('ERROR:', e.message); process.exit(1); });
