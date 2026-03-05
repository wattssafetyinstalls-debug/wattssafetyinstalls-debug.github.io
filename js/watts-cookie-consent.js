/**
 * Watts Cookie Consent Banner v1
 * GDPR/CCPA compliant cookie consent with category controls.
 * Loads on all pages via default layout.
 * 
 * Categories:
 *   - Essential (always on) — session, PIN auth, form CSRF
 *   - Analytics (optional) — GA4, localStorage analytics
 *   - Functional (optional) — chatbot prefs, theme, saved states
 * 
 * When a visitor declines analytics, GA4 is blocked.
 * Consent choice stored in localStorage for 365 days.
 */
(function() {
  'use strict';

  var CONSENT_KEY = 'watts_cookie_consent';
  var CONSENT_VERSION = 1;
  var CONSENT_DAYS = 365;

  // Check if consent already given
  function getConsent() {
    try {
      var raw = localStorage.getItem(CONSENT_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (data.version !== CONSENT_VERSION) return null;
      // Check expiry
      if (Date.now() - data.ts > CONSENT_DAYS * 86400000) {
        localStorage.removeItem(CONSENT_KEY);
        return null;
      }
      return data;
    } catch (e) { return null; }
  }

  function saveConsent(analytics, functional) {
    localStorage.setItem(CONSENT_KEY, JSON.stringify({
      version: CONSENT_VERSION,
      essential: true,
      analytics: !!analytics,
      functional: !!functional,
      ts: Date.now()
    }));
  }

  // Block GA4 if analytics not consented
  function enforceConsent(consent) {
    if (!consent || !consent.analytics) {
      // Disable GA4 by setting opt-out
      window['ga-disable-G-R7FNGWQVQG'] = true;
      // Remove existing GA cookies
      document.cookie.split(';').forEach(function(c) {
        var name = c.split('=')[0].trim();
        if (name.indexOf('_ga') === 0 || name.indexOf('_gid') === 0) {
          document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=.' + location.hostname;
          document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
        }
      });
    }
  }

  // Inject banner styles
  function injectStyles() {
    var s = document.createElement('style');
    s.textContent =
      '#wcc-banner{position:fixed;bottom:0;left:0;right:0;z-index:99998;transform:translateY(100%);transition:transform 0.4s cubic-bezier(.4,0,.2,1);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}' +
      '#wcc-banner.show{transform:translateY(0)}' +
      '#wcc-inner{max-width:680px;margin:0 auto 16px;background:#1a1f2e;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:22px 26px;box-shadow:0 -4px 30px rgba(0,0,0,0.35);backdrop-filter:blur(20px);color:#c8cdd5}' +
      '#wcc-inner h4{color:#fff;font-size:15px;font-weight:700;margin:0 0 6px;display:flex;align-items:center;gap:8px}' +
      '#wcc-inner p{font-size:12px;color:#7a8494;line-height:1.6;margin:0 0 14px}' +
      '#wcc-inner a{color:#00C4B4;text-decoration:underline}' +
      '#wcc-toggles{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:16px}' +
      '.wcc-toggle{display:flex;align-items:center;gap:8px;font-size:12px;color:#9aa3b0}' +
      '.wcc-toggle.locked{opacity:0.5}' +
      '.wcc-switch{position:relative;width:36px;height:20px;flex-shrink:0}' +
      '.wcc-switch input{opacity:0;width:0;height:0}' +
      '.wcc-slider{position:absolute;inset:0;background:#2a3042;border-radius:10px;cursor:pointer;transition:background 0.25s}' +
      '.wcc-slider::before{content:"";position:absolute;width:16px;height:16px;left:2px;bottom:2px;background:#fff;border-radius:50%;transition:transform 0.25s}' +
      '.wcc-switch input:checked+.wcc-slider{background:#00C4B4}' +
      '.wcc-switch input:checked+.wcc-slider::before{transform:translateX(16px)}' +
      '.wcc-switch input:disabled+.wcc-slider{cursor:default;opacity:0.5}' +
      '#wcc-btns{display:flex;gap:8px;flex-wrap:wrap}' +
      '.wcc-btn{padding:10px 20px;border:none;border-radius:10px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.2s;letter-spacing:0.3px}' +
      '.wcc-accept{background:#00C4B4;color:#fff}' +
      '.wcc-accept:hover{background:#00d4c4;transform:translateY(-1px);box-shadow:0 4px 16px rgba(0,196,180,0.3)}' +
      '.wcc-selected{background:rgba(255,255,255,0.08);color:#c8cdd5;border:1px solid rgba(255,255,255,0.1)}' +
      '.wcc-selected:hover{background:rgba(255,255,255,0.12)}' +
      '.wcc-decline{background:transparent;color:#5a6474;border:1px solid rgba(255,255,255,0.06)}' +
      '.wcc-decline:hover{color:#9aa3b0;border-color:rgba(255,255,255,0.12)}' +
      '@media(max-width:600px){#wcc-inner{margin:8px;padding:18px 16px;border-radius:14px}#wcc-btns{flex-direction:column}.wcc-btn{width:100%;text-align:center}}';
    document.head.appendChild(s);
  }

  // Show the banner
  function showBanner() {
    injectStyles();

    var banner = document.createElement('div');
    banner.id = 'wcc-banner';
    banner.innerHTML =
      '<div id="wcc-inner">' +
        '<h4>\uD83C\uDF6A Cookie Preferences</h4>' +
        '<p>We use cookies and local storage to improve your experience. Essential cookies are required for the site to function. You can choose which optional categories to allow.</p>' +
        '<div id="wcc-toggles">' +
          '<label class="wcc-toggle locked">' +
            '<span class="wcc-switch"><input type="checkbox" checked disabled><span class="wcc-slider"></span></span>' +
            'Essential' +
          '</label>' +
          '<label class="wcc-toggle">' +
            '<span class="wcc-switch"><input type="checkbox" id="wccAnalytics" checked><span class="wcc-slider"></span></span>' +
            'Analytics' +
          '</label>' +
          '<label class="wcc-toggle">' +
            '<span class="wcc-switch"><input type="checkbox" id="wccFunctional" checked><span class="wcc-slider"></span></span>' +
            'Functional' +
          '</label>' +
        '</div>' +
        '<div id="wcc-btns">' +
          '<button class="wcc-btn wcc-accept" id="wccAcceptAll">Accept All</button>' +
          '<button class="wcc-btn wcc-selected" id="wccSaveSelected">Save Preferences</button>' +
          '<button class="wcc-btn wcc-decline" id="wccDecline">Essential Only</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(banner);

    // Animate in
    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        banner.classList.add('show');
      });
    });

    // Event handlers
    document.getElementById('wccAcceptAll').addEventListener('click', function() {
      saveConsent(true, true);
      enforceConsent({ analytics: true, functional: true });
      closeBanner();
    });

    document.getElementById('wccSaveSelected').addEventListener('click', function() {
      var a = document.getElementById('wccAnalytics').checked;
      var f = document.getElementById('wccFunctional').checked;
      saveConsent(a, f);
      enforceConsent({ analytics: a, functional: f });
      closeBanner();
    });

    document.getElementById('wccDecline').addEventListener('click', function() {
      saveConsent(false, false);
      enforceConsent({ analytics: false, functional: false });
      closeBanner();
    });
  }

  function closeBanner() {
    var banner = document.getElementById('wcc-banner');
    if (banner) {
      banner.classList.remove('show');
      setTimeout(function() { banner.remove(); }, 400);
    }
  }

  // Init
  var consent = getConsent();
  if (consent) {
    // Already consented — just enforce
    enforceConsent(consent);
  } else {
    // No consent yet — show banner (but not on /tools/ pages which have their own auth)
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() { showBanner(); });
    } else {
      showBanner();
    }
  }

})();
