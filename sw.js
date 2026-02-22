/**
 * Watts Service Worker — PWA Lite
 * Caches key assets for instant repeat visits and offline fallback.
 * Created: 2026-02-22
 */
var CACHE_NAME = 'watts-v1';
var PRECACHE = [
  '/',
  '/services.html',
  '/contact.html',
  '/about.html',
  '/service-area.html',
  '/grab-bar-installation.html',
  '/wheelchair-ramp-installation.html',
  '/bathroom-accessibility.html',
  '/non-slip-flooring-solutions.html',
  '/404.html',
  '/js/watts-lead-engine.js',
  '/js/watts-push.js',
  '/favicon-96x96.png'
];

// Install: precache core pages
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(PRECACHE);
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

// Activate: clean old caches
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.filter(function(n) { return n !== CACHE_NAME; })
             .map(function(n) { return caches.delete(n); })
      );
    }).then(function() {
      return self.clients.claim();
    })
  );
});

// Fetch: network-first for HTML, cache-first for assets
self.addEventListener('fetch', function(e) {
  var url = new URL(e.request.url);

  // Only handle same-origin GET requests
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;

  // HTML pages: network-first (always get fresh content, fallback to cache)
  if (e.request.headers.get('accept') && e.request.headers.get('accept').includes('text/html')) {
    e.respondWith(
      fetch(e.request).then(function(response) {
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) { cache.put(e.request, clone); });
        return response;
      }).catch(function() {
        return caches.match(e.request).then(function(cached) {
          return cached || caches.match('/404.html');
        });
      })
    );
    return;
  }

  // JS/CSS/images: cache-first (fast loads)
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      if (cached) return cached;
      return fetch(e.request).then(function(response) {
        // Cache successful responses
        if (response.ok) {
          var clone = response.clone();
          caches.open(CACHE_NAME).then(function(cache) { cache.put(e.request, clone); });
        }
        return response;
      });
    })
  );
});
