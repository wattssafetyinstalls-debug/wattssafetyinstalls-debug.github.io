#!/usr/bin/env node
/**
 * RSS Feed Generator — Watts ATP Contractor & Watts Safety Installs
 * Scans blog directories and generates feed.xml for each brand.
 * Called after blog posts are generated.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

function generateFeed(brandConfig, blogDir) {
  var fullDir = path.join(ROOT, blogDir, 'blog');
  if (!fs.existsSync(fullDir)) {
    console.log('  No blog dir: ' + fullDir);
    return [];
  }

  var files = fs.readdirSync(fullDir)
    .filter(function(f) { return f.endsWith('.html'); })
    .sort()
    .reverse()
    .slice(0, 20); // Latest 20 posts

  if (files.length === 0) {
    console.log('  No blog posts in ' + fullDir);
    return [];
  }

  var items = '';
  var urls = [];
  files.forEach(function(file) {
    var content = fs.readFileSync(path.join(fullDir, file), 'utf8');
    var titleMatch = content.match(/<title>([^<]+)<\/title>/);
    var descMatch = content.match(/<meta[^>]*name="description"[^>]*content="([^"]+)"/);
    var dateMatch = file.match(/^(\d{4}-\d{2}-\d{2})/);
    var slug = file.replace('.html', '').replace(/^\d{4}-\d{2}-\d{2}-/, '');

    var title = titleMatch ? titleMatch[1].replace(/ \|.*$/, '') : slug;
    var desc = descMatch ? descMatch[1] : title;
    var date = dateMatch ? dateMatch[1] + 'T10:00:00-06:00' : new Date().toISOString();
    var url = brandConfig.baseUrl + '/blog/' + slug;
    urls.push(url);

    items += '    <item>\n' +
      '      <title>' + escXml(title) + '</title>\n' +
      '      <link>' + url + '</link>\n' +
      '      <description>' + escXml(desc) + '</description>\n' +
      '      <pubDate>' + new Date(date).toUTCString() + '</pubDate>\n' +
      '      <guid isPermaLink="true">' + url + '</guid>\n' +
      '    </item>\n';
  });

  var rss = '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n' +
    '  <channel>\n' +
    '    <title>' + escXml(brandConfig.name) + ' Blog</title>\n' +
    '    <link>' + brandConfig.baseUrl + '</link>\n' +
    '    <description>Home improvement tips, accessibility guides, and contractor insights from ' + brandConfig.name + ' in Norfolk, NE.</description>\n' +
    '    <language>en-us</language>\n' +
    '    <lastBuildDate>' + new Date().toUTCString() + '</lastBuildDate>\n' +
    '    <atom:link href="' + brandConfig.baseUrl + '/feed.xml" rel="self" type="application/rss+xml"/>\n' +
    '    <managingEditor>Justin.Watts@WattsATPContractor.com (Justin Watts)</managingEditor>\n' +
    '    <webMaster>Justin.Watts@WattsATPContractor.com (Justin Watts)</webMaster>\n' +
    items +
    '  </channel>\n' +
    '</rss>\n';

  var feedPath = path.join(ROOT, blogDir, 'feed.xml');
  if (blogDir === '.') feedPath = path.join(ROOT, 'feed.xml');
  fs.writeFileSync(feedPath, rss, 'utf8');
  console.log('  ✅ ' + feedPath + ' (' + files.length + ' items)');
  return urls;
}

function escXml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function main() {
  console.log('📰 RSS Feed Generator');
  console.log('====================\n');

  var atpUrls = generateFeed({
    name: 'Watts ATP Contractor',
    baseUrl: 'https://wattsatpcontractor.com'
  }, '.');

  var siUrls = generateFeed({
    name: 'Watts Safety Installs',
    baseUrl: 'https://wattsatpcontractor.com/safety-installs'
  }, 'safety-installs');

  console.log('\n✅ RSS feeds generated. Total URLs: ' + (atpUrls.length + siUrls.length));
  return atpUrls.concat(siUrls);
}

// Export for use by other scripts
if (require.main === module) {
  main();
} else {
  module.exports = { generateFeeds: main };
}
