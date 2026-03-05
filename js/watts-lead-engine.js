/**
 * Watts Lead Generation Engine
 * ============================
 * 1. Sticky mobile CTA bar (call button always visible)
 * 2. Click-to-call tracking (gtag events)
 * 3. Exit-intent lead capture popup
 * 4. Callback request widget
 * 5. Scroll-depth engagement tracking
 * 6. Time-on-page tracking
 * 
 * Created: 2026-02-22
 */
(function() {
  'use strict';

  var PHONE = '(405) 410-6402';
  var PHONE_LINK = 'tel:+14054106402';
  var BUSINESS = 'Watts ATP Contractor';

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
      '</a>' +
      '<button id="sticky-callback-btn" style="background:#FFD700;color:#0A1D37;border:none;padding:14px 20px;font-weight:700;font-size:0.9rem;cursor:pointer;white-space:nowrap;">Request Callback</button>';

    bar.style.cssText = 'position:fixed;bottom:0;left:0;right:0;z-index:9999;display:flex;background:#00C4B4;box-shadow:0 -4px 20px rgba(0,0,0,0.2);';
    
    // Add padding to body so content isn't hidden behind bar
    document.body.style.paddingBottom = '56px';
    document.body.appendChild(bar);

    // Callback button opens the widget
    document.getElementById('sticky-callback-btn').addEventListener('click', function() {
      openCallbackWidget();
    });
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
  // 3. EXIT-INTENT LEAD CAPTURE
  // Catches visitors about to leave
  // ══════════════════════════════════════
  var exitShown = false;

  function createExitIntent() {
    // Only on desktop (mobile uses sticky bar)
    if (window.innerWidth <= 768) return;
    // Don't show if already submitted or dismissed recently
    if (sessionStorage.getItem('watts_exit_dismissed')) return;

    document.addEventListener('mouseout', function(e) {
      if (exitShown) return;
      if (e.clientY > 50) return; // Only trigger when mouse moves to top of page (leaving)
      
      exitShown = true;
      showExitPopup();
    });
  }

  function showExitPopup() {
    var overlay = document.createElement('div');
    overlay.id = 'watts-exit-overlay';
    overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.7);z-index:99999;display:flex;align-items:center;justify-content:center;animation:fadeIn 0.3s ease;';

    overlay.innerHTML = 
      '<div style="background:#fff;border-radius:16px;max-width:480px;width:90%;padding:40px;text-align:center;position:relative;box-shadow:0 25px 60px rgba(0,0,0,0.3);animation:slideUp 0.4s ease;">' +
        '<button id="exit-close" style="position:absolute;top:12px;right:16px;background:none;border:none;font-size:1.8rem;cursor:pointer;color:#999;line-height:1;">&times;</button>' +
        '<div style="font-size:3rem;margin-bottom:15px;">🏠</div>' +
        '<h2 style="font-family:Playfair Display,serif;font-size:1.8rem;color:#0A1D37;margin-bottom:10px;">Wait! Get Your Free Estimate</h2>' +
        '<p style="color:#64748B;margin-bottom:25px;font-size:1.05rem;">Before you go — we offer <strong>free in-home safety assessments</strong> for grab bars, ramps, and accessibility modifications across Northeast Nebraska.</p>' +
        '<form id="exit-form" style="text-align:left;">' +
          '<input type="text" name="name" placeholder="Your Name" required style="width:100%;padding:14px;border:2px solid #e2e8f0;border-radius:8px;margin-bottom:12px;font-size:1rem;font-family:Inter,sans-serif;"/>' +
          '<input type="tel" name="phone" placeholder="Phone Number" required style="width:100%;padding:14px;border:2px solid #e2e8f0;border-radius:8px;margin-bottom:12px;font-size:1rem;font-family:Inter,sans-serif;"/>' +
          '<select name="service" style="width:100%;padding:14px;border:2px solid #e2e8f0;border-radius:8px;margin-bottom:16px;font-size:1rem;font-family:Inter,sans-serif;color:#64748B;">' +
            '<option value="">What do you need help with?</option>' +
            '<option value="grab-bars">Grab Bar Installation</option>' +
            '<option value="wheelchair-ramp">Wheelchair Ramp</option>' +
            '<option value="bathroom">Bathroom Accessibility</option>' +
            '<option value="non-slip">Non-Slip Flooring</option>' +
            '<option value="other">Other Safety Modification</option>' +
          '</select>' +
          '<button type="submit" style="width:100%;padding:16px;background:#00C4B4;color:#fff;border:none;border-radius:50px;font-size:1.15rem;font-weight:700;cursor:pointer;font-family:Inter,sans-serif;transition:all 0.3s;">Get My Free Estimate →</button>' +
        '</form>' +
        '<p style="margin-top:15px;font-size:0.85rem;color:#94a3b8;">Or call directly: <a href="' + PHONE_LINK + '" style="color:#00C4B4;font-weight:700;text-decoration:none;">' + PHONE + '</a></p>' +
      '</div>';

    // Add animation styles
    var style = document.createElement('style');
    style.textContent = '@keyframes fadeIn{from{opacity:0}to{opacity:1}}@keyframes slideUp{from{transform:translateY(30px);opacity:0}to{transform:translateY(0);opacity:1}}';
    document.head.appendChild(style);

    document.body.appendChild(overlay);

    // Close button
    document.getElementById('exit-close').addEventListener('click', function() {
      overlay.remove();
      sessionStorage.setItem('watts_exit_dismissed', '1');
    });

    // Click outside to close
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) {
        overlay.remove();
        sessionStorage.setItem('watts_exit_dismissed', '1');
      }
    });

    // Form submission
    document.getElementById('exit-form').addEventListener('submit', function(e) {
      e.preventDefault();
      var formData = new FormData(e.target);
      var data = {
        name: formData.get('name'),
        phone: formData.get('phone'),
        service: formData.get('service'),
        source: 'exit_intent',
        page: window.location.pathname,
        timestamp: new Date().toISOString()
      };

      // Track conversion
      if (typeof gtag === 'function') {
        gtag('event', 'lead_form_submit', {
          event_category: 'Lead',
          event_label: 'exit_intent',
          value: 1
        });
      }
      if (window.dataLayer) {
        window.dataLayer.push({ event: 'lead_form_submit', formType: 'exit_intent', service: data.service });
      }

      // Store lead locally (also sends to any connected backend)
      storeLead(data);

      // Show thank you
      overlay.querySelector('div').innerHTML = 
        '<div style="font-size:3rem;margin-bottom:15px;">✅</div>' +
        '<h2 style="font-family:Playfair Display,serif;font-size:1.8rem;color:#0A1D37;margin-bottom:10px;">Thank You!</h2>' +
        '<p style="color:#64748B;margin-bottom:20px;">Justin will call you back within 1 business day to schedule your free assessment.</p>' +
        '<a href="' + PHONE_LINK + '" style="display:inline-block;padding:14px 30px;background:#00C4B4;color:#fff;border-radius:50px;text-decoration:none;font-weight:700;">Or Call Now: ' + PHONE + '</a>';

      sessionStorage.setItem('watts_exit_dismissed', '1');
    });
  }

  // ══════════════════════════════════════
  // 4. CALLBACK REQUEST WIDGET
  // Floating button + slide-in form
  // ══════════════════════════════════════
  var callbackOpen = false;

  function createCallbackWidget() {
    // Don't create on mobile (sticky bar handles it)
    if (window.innerWidth <= 768) return;

    var widget = document.createElement('div');
    widget.id = 'watts-callback-widget';
    widget.innerHTML = 
      '<button id="callback-trigger" style="width:60px;height:60px;border-radius:50%;background:#00C4B4;border:none;cursor:pointer;box-shadow:0 4px 20px rgba(0,196,180,0.4);display:flex;align-items:center;justify-content:center;transition:all 0.3s;position:relative;" title="Request a Callback">' +
        '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>' +
        '<span style="position:absolute;top:-2px;right:-2px;width:16px;height:16px;background:#FFD700;border-radius:50%;border:2px solid #fff;"></span>' +
      '</button>' +
      '<div id="callback-panel" style="display:none;position:absolute;bottom:70px;right:0;width:320px;background:#fff;border-radius:16px;box-shadow:0 15px 50px rgba(0,0,0,0.15);overflow:hidden;">' +
        '<div style="background:#0A1D37;padding:20px;color:#fff;">' +
          '<h3 style="font-family:Playfair Display,serif;font-size:1.3rem;margin:0 0 5px;">Request a Callback</h3>' +
          '<p style="font-size:0.85rem;opacity:0.8;margin:0;">Justin will call you back within 1 business day</p>' +
        '</div>' +
        '<form id="callback-form" style="padding:20px;">' +
          '<input type="text" name="name" placeholder="Your Name" required style="width:100%;padding:12px;border:2px solid #e2e8f0;border-radius:8px;margin-bottom:10px;font-size:0.95rem;font-family:Inter,sans-serif;"/>' +
          '<input type="tel" name="phone" placeholder="Phone Number" required style="width:100%;padding:12px;border:2px solid #e2e8f0;border-radius:8px;margin-bottom:10px;font-size:0.95rem;font-family:Inter,sans-serif;"/>' +
          '<input type="text" name="city" placeholder="Your City (optional)" style="width:100%;padding:12px;border:2px solid #e2e8f0;border-radius:8px;margin-bottom:12px;font-size:0.95rem;font-family:Inter,sans-serif;"/>' +
          '<button type="submit" style="width:100%;padding:14px;background:#00C4B4;color:#fff;border:none;border-radius:50px;font-size:1rem;font-weight:700;cursor:pointer;font-family:Inter,sans-serif;">Call Me Back →</button>' +
        '</form>' +
      '</div>';

    widget.style.cssText = 'position:fixed;bottom:100px;right:24px;z-index:9998;';
    document.body.appendChild(widget);

    // Toggle panel
    document.getElementById('callback-trigger').addEventListener('click', function() {
      var panel = document.getElementById('callback-panel');
      callbackOpen = !callbackOpen;
      panel.style.display = callbackOpen ? 'block' : 'none';
    });

    // Form submission
    document.getElementById('callback-form').addEventListener('submit', function(e) {
      e.preventDefault();
      var formData = new FormData(e.target);
      var data = {
        name: formData.get('name'),
        phone: formData.get('phone'),
        city: formData.get('city'),
        source: 'callback_widget',
        page: window.location.pathname,
        timestamp: new Date().toISOString()
      };

      if (typeof gtag === 'function') {
        gtag('event', 'lead_form_submit', {
          event_category: 'Lead',
          event_label: 'callback_widget',
          value: 1
        });
      }
      if (window.dataLayer) {
        window.dataLayer.push({ event: 'lead_form_submit', formType: 'callback_widget' });
      }

      storeLead(data);

      document.getElementById('callback-panel').innerHTML = 
        '<div style="padding:30px;text-align:center;">' +
          '<div style="font-size:2.5rem;margin-bottom:10px;">✅</div>' +
          '<h3 style="font-family:Playfair Display,serif;color:#0A1D37;margin-bottom:8px;">Got it!</h3>' +
          '<p style="color:#64748B;font-size:0.95rem;">Justin will call you back soon.</p>' +
          '<a href="' + PHONE_LINK + '" style="display:inline-block;margin-top:12px;color:#00C4B4;font-weight:700;text-decoration:none;">Or call now: ' + PHONE + '</a>' +
        '</div>';
    });
  }

  // Open callback widget from sticky bar
  function openCallbackWidget() {
    // On mobile, show a simple inline form
    if (window.innerWidth <= 768) {
      showMobileCallbackForm();
      return;
    }
    var panel = document.getElementById('callback-panel');
    if (panel) {
      callbackOpen = true;
      panel.style.display = 'block';
    }
  }

  function showMobileCallbackForm() {
    if (document.getElementById('watts-mobile-callback')) return;

    var overlay = document.createElement('div');
    overlay.id = 'watts-mobile-callback';
    overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.7);z-index:99999;display:flex;align-items:flex-end;justify-content:center;';

    overlay.innerHTML = 
      '<div style="background:#fff;border-radius:16px 16px 0 0;width:100%;max-width:500px;padding:30px 20px 40px;animation:slideUp 0.3s ease;">' +
        '<button id="mobile-cb-close" style="position:absolute;top:12px;right:16px;background:none;border:none;font-size:1.8rem;cursor:pointer;color:#999;">&times;</button>' +
        '<h3 style="font-family:Playfair Display,serif;font-size:1.5rem;color:#0A1D37;margin-bottom:5px;">Request a Callback</h3>' +
        '<p style="color:#64748B;margin-bottom:20px;font-size:0.95rem;">Justin will call you back within 1 business day</p>' +
        '<form id="mobile-callback-form">' +
          '<input type="text" name="name" placeholder="Your Name" required style="width:100%;padding:14px;border:2px solid #e2e8f0;border-radius:8px;margin-bottom:10px;font-size:1rem;font-family:Inter,sans-serif;"/>' +
          '<input type="tel" name="phone" placeholder="Phone Number" required style="width:100%;padding:14px;border:2px solid #e2e8f0;border-radius:8px;margin-bottom:12px;font-size:1rem;font-family:Inter,sans-serif;"/>' +
          '<button type="submit" style="width:100%;padding:16px;background:#00C4B4;color:#fff;border:none;border-radius:50px;font-size:1.1rem;font-weight:700;cursor:pointer;font-family:Inter,sans-serif;">Call Me Back →</button>' +
        '</form>' +
      '</div>';

    document.body.appendChild(overlay);

    document.getElementById('mobile-cb-close').addEventListener('click', function() { overlay.remove(); });
    overlay.addEventListener('click', function(e) { if (e.target === overlay) overlay.remove(); });

    document.getElementById('mobile-callback-form').addEventListener('submit', function(e) {
      e.preventDefault();
      var formData = new FormData(e.target);
      var data = {
        name: formData.get('name'),
        phone: formData.get('phone'),
        source: 'mobile_callback',
        page: window.location.pathname,
        timestamp: new Date().toISOString()
      };

      if (typeof gtag === 'function') {
        gtag('event', 'lead_form_submit', { event_category: 'Lead', event_label: 'mobile_callback', value: 1 });
      }
      if (window.dataLayer) {
        window.dataLayer.push({ event: 'lead_form_submit', formType: 'mobile_callback' });
      }

      storeLead(data);

      overlay.querySelector('div').innerHTML = 
        '<div style="text-align:center;padding:20px 0;">' +
          '<div style="font-size:3rem;margin-bottom:10px;">✅</div>' +
          '<h3 style="font-family:Playfair Display,serif;color:#0A1D37;margin-bottom:8px;">Got it!</h3>' +
          '<p style="color:#64748B;">Justin will call you back soon.</p>' +
        '</div>';
      setTimeout(function() { overlay.remove(); }, 3000);
    });
  }

  // ══════════════════════════════════════
  // 5. SCROLL DEPTH & ENGAGEMENT TRACKING
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
  // 6. CONTACT FORM HANDLER
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
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
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
          '<div style="font-size:4rem;margin-bottom:20px;">✅</div>' +
          '<h2 style="font-family:Playfair Display,serif;color:var(--navy,#0A1D37);margin-bottom:12px;">Message Sent!</h2>' +
          '<p style="color:var(--gray,#64748B);font-size:1.1rem;margin-bottom:20px;">Thank you, ' + (data.name.split(' ')[0] || '') + '! Justin will personally review your request and get back to you within 2 hours during business hours.</p>' +
          '<p style="color:var(--gray,#64748B);font-size:0.95rem;margin-bottom:24px;">If this is urgent, call directly:</p>' +
          '<a href="' + PHONE_LINK + '" style="display:inline-block;padding:16px 32px;background:var(--teal,#00C4B4);color:#fff;border-radius:50px;text-decoration:none;font-weight:700;font-size:1.15rem;box-shadow:0 4px 15px rgba(0,196,180,0.3);">Call Now: ' + PHONE + '</a>' +
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
    var isWSI = window.location.pathname.indexOf('/safety-installs') === 0;
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
  // INIT
  // ══════════════════════════════════════
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', boot);
    } else {
      boot();
    }
  }

  // ══════════════════════════════════════
  // 7. SERVICE WORKER REGISTRATION
  // Faster repeat visits + offline fallback
  // ══════════════════════════════════════
  function registerSW() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(function() {});
    }
  }

  // ══════════════════════════════════════
  // 8. SOCIAL PROOF BANNER
  // Shows recent activity to build urgency
  // ══════════════════════════════════════
  function createSocialProof() {
    // Don't show on contact page (they're already converting)
    if (window.location.pathname.includes('contact')) return;
    // Only show once per session
    if (sessionStorage.getItem('watts_proof_shown')) return;

    var messages = [
      '🏠 Someone in Norfolk just requested a free estimate',
      '⭐ 5-star rated — 12 reviews on Google',
      '📞 3 people called this week about grab bars',
      '🔧 Justin completed a ramp install in Wayne yesterday',
      '✅ Free in-home safety assessments — no obligation',
      '📍 Serving 25+ cities across Northeast Nebraska'
    ];

    var delay = 15000 + Math.random() * 15000; // 15-30 seconds

    setTimeout(function() {
      var msg = messages[Math.floor(Math.random() * messages.length)];
      var toast = document.createElement('div');
      toast.id = 'watts-social-proof';
      toast.style.cssText = 'position:fixed;bottom:' + (window.innerWidth <= 768 ? '70px' : '24px') + ';left:24px;background:#fff;border-radius:12px;padding:16px 20px;box-shadow:0 8px 30px rgba(0,0,0,0.15);z-index:9997;max-width:340px;font-family:Inter,sans-serif;font-size:0.95rem;color:#1E293B;transform:translateX(-120%);transition:transform 0.5s cubic-bezier(0.4,0,0.2,1);border-left:4px solid #00C4B4;';
      toast.textContent = msg;
      document.body.appendChild(toast);

      // Slide in
      requestAnimationFrame(function() {
        requestAnimationFrame(function() {
          toast.style.transform = 'translateX(0)';
        });
      });

      // Slide out after 6 seconds
      setTimeout(function() {
        toast.style.transform = 'translateX(-120%)';
        setTimeout(function() { toast.remove(); }, 600);
      }, 6000);

      sessionStorage.setItem('watts_proof_shown', '1');

      if (typeof gtag === 'function') {
        gtag('event', 'social_proof_shown', { event_category: 'Engagement', event_label: msg });
      }
    }, delay);
  }

  function boot() {
    createStickyCTA();
    trackPhoneCalls();
    createExitIntent();
    createCallbackWidget();
    trackEngagement();
    handleContactForm();
    registerSW();
    createSocialProof();
  }

  init();
})();
