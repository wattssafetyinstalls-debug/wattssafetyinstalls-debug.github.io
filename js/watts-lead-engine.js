/**
 * Watts Lead Generation Engine (Slimmed — 2026-09-30)
 * ===================================================
 * 1. Sticky mobile CTA bar (call button always visible)
 * 2. Click-to-call tracking (gtag events)
 * 3. Contact form handler -> Cloudflare Worker + Formspree fallback
 * 4. Scroll-depth & time-on-page engagement tracking
 * 5. Service worker registration
 *
 * Removed: exit-intent popup, callback widget, mobile callback overlay,
 * fake social-proof toasts (reduced floating clutter + professionalism).
 */
(function() {
  'use strict';

  var PHONE = '(405) 410-6402';
  var PHONE_LINK = 'tel:+14054106402';

  // Brand detection — DBA pages get Watts Safety Installs colors
  var isWSI = window.location.pathname.indexOf('/safety-installs') === 0;
  var BRAND = isWSI
    ? { name: 'Watts Safety Installs', primary: '#dc2626', dark: '#1a1a1a', accent: '#f5f5dc', accentText: '#1a1a1a', shadow: 'rgba(220,38,38,0.3)' }
    : { name: 'Watts ATP Contractor', primary: '#00C4B4', dark: '#0A1D37', accent: '#FFD700', accentText: '#0A1D37', shadow: 'rgba(0,196,180,0.3)' };
  var BUSINESS = BRAND.name;

  // ══════════════════════════════════════
  // 1. STICKY MOBILE CTA BAR
  // Always-visible call button on mobile
  // ══════════════════════════════════════
  function createStickyCTA() {
    if (window.innerWidth > 768) return;

    var bar = document.createElement('div');
    bar.id = 'watts-sticky-cta';
    bar.innerHTML =
      '<a href="' + PHONE_LINK + '" id="sticky-call-btn" style="flex:1;text-align:center;text-decoration:none;color:#fff;font-weight:700;font-size:1rem;padding:14px 0;display:flex;align-items:center;justify-content:center;gap:8px;">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>' +
        'Call Now — Free Estimate' +
      '</a>';

    bar.style.cssText = 'position:fixed;bottom:0;left:0;right:0;z-index:9999;display:flex;background:' + BRAND.primary + ';box-shadow:0 -4px 20px rgba(0,0,0,0.2);';

    // Add padding to body so content isn't hidden behind bar
    document.body.style.paddingBottom = '56px';
    document.body.appendChild(bar);
  }

  // ══════════════════════════════════════
  // 2. CLICK-TO-CALL TRACKING
  // Track every phone tap as a conversion
  // ══════════════════════════════════════
  function trackPhoneCalls() {
    document.addEventListener('click', function(e) {
      var link = e.target.closest('a[href^="tel:"]');
      if (!link) return;

      // Google Analytics event
      if (typeof gtag === 'function') {
        gtag('event', 'phone_call', {
          event_category: 'Lead',
          event_label: link.href,
          value: 1
        });
        // Also fire as a conversion
        gtag('event', 'conversion', {
          send_to: 'AW-CONVERSION_ID/LABEL', // Replace when Google Ads is set up
          event_category: 'Lead',
          event_label: 'phone_call'
        });
      }

      // Google Tag Manager dataLayer
      if (window.dataLayer) {
        window.dataLayer.push({
          event: 'phone_call',
          eventCategory: 'Lead',
          eventAction: 'click_to_call',
          eventLabel: link.href
        });
      }
    });
  }

  // ══════════════════════════════════════
  // 3. SCROLL DEPTH & ENGAGEMENT TRACKING
  // Know which pages keep visitors engaged
  // ══════════════════════════════════════
  function trackEngagement() {
    var scrollMarks = [25, 50, 75, 90];
    var fired = {};

    window.addEventListener('scroll', function() {
      var scrollPct = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);

      scrollMarks.forEach(function(mark) {
        if (scrollPct >= mark && !fired[mark]) {
          fired[mark] = true;
          if (typeof gtag === 'function') {
            gtag('event', 'scroll_depth', { event_category: 'Engagement', event_label: mark + '%', value: mark });
          }
          if (window.dataLayer) {
            window.dataLayer.push({ event: 'scroll_depth', scrollDepth: mark });
          }
        }
      });
    });

    // Time on page tracking (30s, 60s, 120s, 300s)
    var timeMarks = [30, 60, 120, 300];
    timeMarks.forEach(function(seconds) {
      setTimeout(function() {
        if (typeof gtag === 'function') {
          gtag('event', 'time_on_page', { event_category: 'Engagement', event_label: seconds + 's', value: seconds });
        }
      }, seconds * 1000);
    });
  }

  // ══════════════════════════════════════
  // 4. CONTACT FORM HANDLER
  // Captures main contact form + sends to automation
  // ══════════════════════════════════════
  function handleContactForm() {
    var form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
      e.preventDefault();

      var btn = form.querySelector('button[type="submit"]');
      var origText = btn ? btn.innerHTML : '';
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = 'Sending...';
      }

      var data = {
        name: (form.querySelector('#name') || {}).value || '',
        phone: (form.querySelector('#phone') || {}).value || '',
        email: (form.querySelector('#email') || {}).value || '',
        service: (form.querySelector('#service') || {}).value || '',
        timeline: (form.querySelector('#timeline') || {}).value || '',
        message: (form.querySelector('#message') || {}).value || '',
        source: 'contact_form',
        page: window.location.pathname,
        timestamp: new Date().toISOString()
      };

      // GA tracking
      if (typeof gtag === 'function') {
        gtag('event', 'contact_form_submit', {
          event_category: 'Lead',
          event_label: 'contact_page_form',
          value: 1
        });
      }
      if (window.dataLayer) {
        window.dataLayer.push({ event: 'contact_form_submit', formType: 'contact_page', service: data.service });
      }

      storeLead(data);

      // Show thank-you state
      var container = form.parentElement;
      container.innerHTML =
        '<div style="text-align:center;padding:40px 20px;">' +
          '<h2 style="font-family:Playfair Display,serif;color:var(--navy,' + BRAND.dark + ');margin-bottom:12px;">Message Sent!</h2>' +
          '<p style="color:var(--gray,#64748B);font-size:1.1rem;margin-bottom:20px;">Thank you, ' + (data.name.split(' ')[0] || '') + '! Justin will personally review your request and get back to you within 2 hours during business hours.</p>' +
          '<p style="color:var(--gray,#64748B);font-size:0.95rem;margin-bottom:24px;">If this is urgent, call directly:</p>' +
          '<a href="' + PHONE_LINK + '" style="display:inline-block;padding:16px 32px;background:' + BRAND.primary + ';color:#fff;border-radius:50px;text-decoration:none;font-weight:700;font-size:1.15rem;box-shadow:0 4px 15px ' + BRAND.shadow + ';">Call Now: ' + PHONE + '</a>' +
        '</div>';
    });
  }

  // ══════════════════════════════════════
  // LEAD STORAGE
  // Sends to Cloudflare Worker for scoring, SMS, CRM, email
  // Falls back to Formspree if worker is unreachable
  // ══════════════════════════════════════
  var WORKER_URL = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';

  function storeLead(data) {
    // Store in localStorage as backup
    var leads = JSON.parse(localStorage.getItem('watts_leads') || '[]');
    leads.push(data);
    localStorage.setItem('watts_leads', JSON.stringify(leads));

    // Detect brand from URL
    data.brand = isWSI ? 'wsi' : 'atp';
    data.referrer = document.referrer || '';

    // Send to Cloudflare Worker (lead scoring + SMS + CRM + email)
    fetch(WORKER_URL + '/lead/incoming', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(function(res) { return res.json(); })
    .then(function(result) {
      console.log('[Watts Lead Engine] Lead processed:', result);
    })
    .catch(function(err) {
      console.warn('[Watts Lead Engine] Worker unreachable, falling back to Formspree');
      // Fallback to Formspree
      fetch('https://formspree.io/f/mjkjgrlb', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: data.name,
          phone: data.phone,
          service: data.service || 'Callback Request',
          city: data.city || '',
          source: data.source,
          page: data.page,
          _subject: 'New Lead from ' + BUSINESS + ' Website (' + data.source + ')'
        })
      }).catch(function() {});
    });
  }

  // ══════════════════════════════════════
  // 5. SERVICE WORKER REGISTRATION
  // Faster repeat visits + offline fallback
  // ══════════════════════════════════════
  function registerSW() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(function() {});
    }
  }

  // ══════════════════════════════════════
  // INIT
  // ══════════════════════════════════════
  function boot() {
    createStickyCTA();
    trackPhoneCalls();
    trackEngagement();
    handleContactForm();
    registerSW();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
