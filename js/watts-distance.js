/**
 * Watts Distance Calculator v1
 * Shows "X minutes from you" based on Google Maps Distance Matrix API.
 * Requires Google Maps API key with Distance Matrix API enabled.
 *
 * Usage: <script src="/js/watts-distance.js" data-maps-key="YOUR_KEY" defer></script>
 * Widget auto-injects into element with id="watts-distance" if present.
 */
(function () {
  'use strict';

  var scriptTag = document.currentScript || document.querySelector('script[data-maps-key]');
  var API_KEY = scriptTag && scriptTag.getAttribute('data-maps-key');
  
  if (!API_KEY) return; // No key, no widget

  // Norfolk, NE coordinates
  var NORFOLK_LAT = 42.032;
  var NORFOLK_LON = -97.418;

  // Cache for 1 hour
  var CACHE_KEY = 'watts-distance-cache';
  var CACHE_TTL = 60 * 60 * 1000;

  function getCached() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var obj = JSON.parse(raw);
      if (Date.now() - obj.ts > CACHE_TTL) return null;
      return obj.data;
    } catch (e) { return null; }
  }

  function setCache(data) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({ ts: Date.now(), data: data }));
    } catch (e) {}
  }

  function getUserLocation() {
    return new Promise(function(resolve) {
      if (!navigator.geolocation) {
        resolve(null);
        return;
      }

      navigator.geolocation.getCurrentPosition(
        function(pos) {
          resolve({
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
          });
        },
        function() {
          resolve(null);
        },
        { timeout: 5000, enableHighAccuracy: false }
      );
    });
  }

  function calculateDistance(origin, destination) {
    var url = 'https://maps.googleapis.com/maps/api/distancematrix/json' +
      '?origins=' + origin.lat + ',' + origin.lng +
      '&destinations=' + destination.lat + ',' + destination.lng +
      '&units=imperial' +
      '&key=' + API_KEY;

    return fetch(url)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.status === 'OK' && data.rows[0].elements[0].status === 'OK') {
          var element = data.rows[0].elements[0];
          return {
            distance: element.distance.text,
            duration: element.duration.text,
            durationValue: element.duration.value, // seconds
            distanceValue: element.distance.value // meters
          };
        }
        return null;
      });
  }

  function formatDistance(miles, minutes) {
    if (miles <= 1) {
      return 'Less than 1 mile away — ' + Math.round(minutes) + ' min drive';
    } else if (miles <= 5) {
      return Math.round(miles) + ' miles away — ' + Math.round(minutes) + ' min drive';
    } else {
      return Math.round(miles) + ' miles away — ' + Math.round(minutes) + ' min drive';
    }
  }

  function render(data, userLoc) {
    var target = document.getElementById('watts-distance');
    if (!target) return;

    var miles = data.distanceValue / 1609.34; // convert meters to miles
    var minutes = data.durationValue / 60;

    var message = formatDistance(miles, minutes);
    var statusColor = minutes <= 15 ? '#22c55e' : minutes <= 30 ? '#f59e0b' : '#ef4444';
    var statusText = minutes <= 15 ? 'Right in our service area!' : 
                    minutes <= 30 ? 'We service your area!' : 
                    'Still within our 100-mile service area!';

    target.innerHTML = '<div style="background:#111827;border:1px solid #1e2d4a;border-radius:14px;padding:16px 18px;min-width:260px;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;box-shadow:0 4px 20px rgba(0,0,0,0.3);">' +
      '<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">' +
        '<span style="font-size:24px;">📍</span>' +
        '<div style="font-size:15px;font-weight:600;color:#fff;">' + message + '</div>' +
      '</div>' +
      '<div style="display:flex;align-items:center;justify-content:space-between;">' +
        '<div style="font-size:12px;color:' + statusColor + ';font-weight:500;">' + statusText + '</div>' +
        '<div style="font-size:11px;color:#6b7280;">100-mile service radius</div>' +
      '</div>' +
      '<div style="margin-top:10px;padding-top:10px;border-top:1px solid #1e2d4a;">' +
        '<div style="font-size:11px;color:#8899aa;margin-bottom:4px;">Service Area Highlights:</div>' +
        '<div style="display:flex;flex-wrap:wrap;gap:4px;">' +
          '<span style="font-size:10px;background:rgba(34,197,94,0.15);color:#22c55e;padding:2px 6px;border-radius:4px;">Norfolk</span>' +
          '<span style="font-size:10px;background:rgba(59,130,246,0.15);color:#3b82f6;padding:2px 6px;border-radius:4px;">Columbus</span>' +
          '<span style="font-size:10px;background:rgba(59,130,246,0.15);color:#3b82f6;padding:2px 6px;border-radius:4px;">Fremont</span>' +
          '<span style="font-size:10px;background:rgba(59,130,246,0.15);color:#3b82f6;padding:2px 6px;border-radius:4px;">Madison</span>' +
          '<span style="font-size:10px;background:rgba(59,130,246,0.15);color:#3b82f6;padding:2px 6px;border-radius:4px;">+23 more towns</span>' +
        '</div>' +
      '</div>' +
      '<div style="text-align:right;margin-top:8px;font-size:10px;color:#3a4a5c;">Based on your location</div>' +
    '</div>';
  }

  function init() {
    var cached = getCached();
    if (cached) {
      render(cached.data, cached.userLoc);
      return;
    }

    getUserLocation().then(function(userLoc) {
      if (!userLoc) {
        // Fallback: show Norfolk distance (0 miles)
        render({
          distance: '0 miles',
          duration: '0 mins',
          distanceValue: 0,
          durationValue: 0
        }, { lat: NORFOLK_LAT, lng: NORFOLK_LON });
        return;
      }

      calculateDistance(userLoc, { lat: NORFOLK_LAT, lng: NORFOLK_LON })
        .then(function(data) {
          if (data) {
            setCache({ data: data, userLoc: userLoc });
            render(data, userLoc);
          }
        })
        .catch(function() {
          // Silently fail
        });
    });
  }

  // Auto-refresh every hour
  setInterval(init, CACHE_TTL);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
