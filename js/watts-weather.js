/**
 * Watts Weather Widget v1
 * Shows current Norfolk NE weather + job-planning alerts.
 * Requires OpenWeatherMap API key set in data-weather-key attribute on script tag,
 * or falls back to a free endpoint.
 *
 * Usage: <script src="/js/watts-weather.js" data-weather-key="YOUR_KEY" defer></script>
 * Widget auto-injects into element with id="watts-weather" if present,
 * otherwise appends a floating badge to the page.
 */
(function () {
  'use strict';

  var NORFOLK_LAT = 42.032;
  var NORFOLK_LON = -97.418;
  var scriptTag = document.currentScript || document.querySelector('script[data-weather-key]');
  var API_KEY = scriptTag && scriptTag.getAttribute('data-weather-key');

  if (!API_KEY) return; // No key, no widget

  var ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather?lat=' + NORFOLK_LAT + '&lon=' + NORFOLK_LON + '&units=imperial&appid=' + API_KEY;

  // Cache for 30 minutes
  var CACHE_KEY = 'watts-weather-cache';
  var CACHE_TTL = 30 * 60 * 1000;

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

  function getJobAlert(data) {
    var temp = data.main.temp;
    var wind = data.wind.speed;
    var weather = data.weather[0].main.toLowerCase();
    var alerts = [];

    if (weather.indexOf('rain') !== -1 || weather.indexOf('drizzle') !== -1) {
      alerts.push({ icon: '🌧️', text: 'Rain today — outdoor ramp/concrete work not recommended', level: 'warn' });
    }
    if (weather.indexOf('snow') !== -1) {
      alerts.push({ icon: '❄️', text: 'Snow conditions — snow removal services available', level: 'info' });
    }
    if (weather.indexOf('thunder') !== -1) {
      alerts.push({ icon: '⛈️', text: 'Thunderstorms — all outdoor work postponed for safety', level: 'warn' });
    }
    if (temp < 20) {
      alerts.push({ icon: '🥶', text: 'Extreme cold (' + Math.round(temp) + '°F) — limited outdoor work today', level: 'warn' });
    } else if (temp < 35) {
      alerts.push({ icon: '🧊', text: 'Cold conditions — concrete/adhesive work may be affected', level: 'info' });
    }
    if (temp > 95) {
      alerts.push({ icon: '🔥', text: 'Extreme heat (' + Math.round(temp) + '°F) — extra hydration breaks scheduled', level: 'warn' });
    }
    if (wind > 25) {
      alerts.push({ icon: '💨', text: 'High winds (' + Math.round(wind) + ' mph) — elevated work postponed', level: 'warn' });
    }
    if (alerts.length === 0) {
      alerts.push({ icon: '✅', text: 'Great conditions for all job types today', level: 'good' });
    }
    return alerts;
  }

  function getWeatherIcon(code) {
    if (code >= 200 && code < 300) return '⛈️';
    if (code >= 300 && code < 400) return '🌦️';
    if (code >= 500 && code < 600) return '🌧️';
    if (code >= 600 && code < 700) return '❄️';
    if (code >= 700 && code < 800) return '🌫️';
    if (code === 800) return '☀️';
    if (code > 800) return '⛅';
    return '🌡️';
  }

  function render(data) {
    var temp = Math.round(data.main.temp);
    var desc = data.weather[0].description;
    var icon = getWeatherIcon(data.weather[0].id);
    var alerts = getJobAlert(data);
    var wind = Math.round(data.wind.speed);
    var humidity = data.main.humidity;

    var target = document.getElementById('watts-weather');
    if (!target) {
      // Create floating badge
      target = document.createElement('div');
      target.id = 'watts-weather';
      target.style.cssText = 'position:fixed;top:16px;left:16px;z-index:9998;';
      document.body.appendChild(target);
    }

    var alertHTML = alerts.map(function (a) {
      var bg = a.level === 'warn' ? 'rgba(251,191,36,0.15)' : a.level === 'good' ? 'rgba(34,197,94,0.15)' : 'rgba(59,130,246,0.15)';
      var color = a.level === 'warn' ? '#f59e0b' : a.level === 'good' ? '#22c55e' : '#3b82f6';
      return '<div style="background:' + bg + ';color:' + color + ';padding:6px 10px;border-radius:8px;font-size:12px;display:flex;align-items:center;gap:6px;">' +
        '<span>' + a.icon + '</span><span>' + a.text + '</span></div>';
    }).join('');

    target.innerHTML = '<div style="background:#111827;border:1px solid #1e2d4a;border-radius:14px;padding:16px 18px;min-width:260px;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;box-shadow:0 4px 20px rgba(0,0,0,0.3);">' +
      '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">' +
        '<div style="display:flex;align-items:center;gap:8px;">' +
          '<span style="font-size:28px;">' + icon + '</span>' +
          '<div><div style="font-size:22px;font-weight:700;color:#fff;">' + temp + '°F</div>' +
          '<div style="font-size:11px;color:#8899aa;text-transform:capitalize;">' + desc + '</div></div>' +
        '</div>' +
        '<div style="text-align:right;">' +
          '<div style="font-size:11px;color:#6b7280;">Norfolk, NE</div>' +
          '<div style="font-size:11px;color:#6b7280;">💨 ' + wind + ' mph · 💧 ' + humidity + '%</div>' +
        '</div>' +
      '</div>' +
      '<div style="display:flex;flex-direction:column;gap:4px;">' + alertHTML + '</div>' +
      '<div style="text-align:right;margin-top:8px;font-size:10px;color:#3a4a5c;">Updated ' + new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}) + '</div>' +
    '</div>';
  }

  function fetchWeather() {
    var cached = getCached();
    if (cached) { render(cached); return; }

    fetch(ENDPOINT)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.main) {
          setCache(data);
          render(data);
        }
      })
      .catch(function () {});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fetchWeather);
  } else {
    fetchWeather();
  }

  // Refresh every 30 min
  setInterval(fetchWeather, CACHE_TTL);
})();
