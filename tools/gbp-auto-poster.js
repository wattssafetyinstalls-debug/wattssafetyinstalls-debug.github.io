#!/usr/bin/env node
/**
 * GBP Auto-Poster — Watts ATP Contractor & Watts Safety Installs
 * Automatically posts to Google Business Profile using OAuth2.
 * Called by GitHub Actions on a weekly schedule.
 * 
 * Requires: GBP_CLIENT_ID, GBP_CLIENT_SECRET, GBP_REFRESH_TOKEN environment variables
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = path.resolve(__dirname, '..');
const CLIENT_ID = process.env.GBP_CLIENT_ID;
const CLIENT_SECRET = process.env.GBP_CLIENT_SECRET;
const REFRESH_TOKEN = process.env.GBP_REFRESH_TOKEN;

if (!CLIENT_ID || !CLIENT_SECRET || !REFRESH_TOKEN) {
  console.error('ERROR: Missing GBP OAuth credentials');
  process.exit(1);
}

// ── POST TOPICS POOL ──
const POST_TOPICS = [
  'Seasonal home maintenance tips for Nebraska homeowners',
  'How to prepare your home for winter in Norfolk NE',
  'Spring cleaning checklist for Northeast Nebraska homes',
  'Energy efficiency upgrades that save money in Nebraska',
  'Kitchen remodeling trends for Norfolk homeowners',
  'Bathroom accessibility modifications for seniors',
  'Why professional grab bar installation matters',
  'Wheelchair ramp options for Nebraska weather',
  'Home safety checklist for aging in place',
  'TV mounting tips for the perfect viewing angle',
  'Gutter maintenance before Nebraska storms',
  'Handyman services that increase home value',
  'Paint color trends for Nebraska homes',
  'Fall home preparation checklist',
  'Summer home improvement projects',
  'ADA compliance for residential homes',
  'How to choose the right contractor in Norfolk',
  'Home accessibility for family members with mobility needs',
  'Property maintenance tips for rental owners',
  'Emergency home repairs: what to do first',
];

// ── CALL GEMINI ──
function callGemini(prompt) {
  return new Promise(function(resolve, reject) {
    var url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=AIzaSyB5Pipp05TkgemKGQkRGIYXKmF8s8qO4Ng';
    var body = JSON.stringify({
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.8, maxOutputTokens: 500, topP: 0.9 }
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
          else reject(new Error('No text in response'));
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ── GET ACCESS TOKEN ──
function getAccessToken() {
  return new Promise(function(resolve, reject) {
    var body = JSON.stringify({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      refresh_token: REFRESH_TOKEN,
      grant_type: 'refresh_token'
    });

    var options = {
      hostname: 'oauth2.googleapis.com',
      path: '/token',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
    };

    var req = https.request(options, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        try {
          var json = JSON.parse(data);
          if (json.access_token) resolve(json.access_token);
          else reject(new Error('No access token: ' + data));
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ── POST TO GBP ──
function postToGBP(accessToken, postData) {
  return new Promise(function(resolve, reject) {
    // First, we need to get the account/location ID
    // For now, we'll use a placeholder - in production, you'd fetch this from the API
    var locationId = '09996134269287007529';
    
    var body = JSON.stringify({
      topicType: 'STANDARD',
      summary: postData.title,
      callToAction: {
        actionType: 'CALL',
        url: 'tel:+14054106402'
      }
    });

    var options = {
      hostname: 'mybusinessbusinessinformation.googleapis.com',
      path: '/v1/locations/' + locationId + '/localPosts',
      method: 'POST',
      headers: { 
        'Authorization': 'Bearer ' + accessToken,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    };

    var req = https.request(options, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else {
          reject(new Error('GBP API error: ' + res.statusCode + ' - ' + data));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ── MAIN ──
async function main() {
  console.log('🤖 Watts GBP Auto-Poster');
  console.log('=======================\n');

  // Pick topic based on week
  var weekNum = Math.floor((Date.now() - new Date('2025-01-01').getTime()) / (7 * 24 * 60 * 60 * 1000));
  var topic = POST_TOPICS[weekNum % POST_TOPICS.length];

  // Generate post content
  var prompt = 'Write a short, engaging Google Business Profile post (max 150 words) about: ' + topic + '\n\n' +
    'Requirements:\n' +
    '- For Watts ATP Contractor & Watts Safety Installs in Norfolk, NE\n' +
    '- Include a helpful tip or insight\n' +
    '- End with a soft call-to-action to call (405) 410-6402\n' +
    '- Use 1-2 emojis maximum\n' +
    '- Write in a friendly, professional tone\n' +
    '- Mention Norfolk or Northeast Nebraska if natural\n\n' +
    'Return ONLY the post text, no title or formatting.';

  try {
    console.log('Generating post about: ' + topic);
    var postContent = await callGemini(prompt);
    
    // Get access token
    console.log('Getting access token...');
    var accessToken = await getAccessToken();
    
    // Post to GBP
    console.log('Posting to GBP...');
    var result = await postToGBP(accessToken, {
      title: postContent.substring(0, 58) + '...',
      content: postContent
    });
    
    console.log('✅ Post published successfully!');
    
    // Save result
    fs.writeFileSync(path.join(ROOT, 'gbp-result.txt'), 
      'GBP Post Published - ' + new Date().toISOString() + '\n\n' +
      'Content: ' + postContent + '\n\n' +
      'Response: ' + result,
      'utf8');
      
  } catch (err) {
    console.error('ERROR:', err.message);
    
    // Save error
    fs.writeFileSync(path.join(ROOT, 'gbp-result.txt'), 
      'GBP Post Failed - ' + new Date().toISOString() + '\n\n' +
      'Error: ' + err.message,
      'utf8');
    process.exit(1);
  }
}

main();
