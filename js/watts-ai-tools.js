/**
 * Watts AI Public Tools v2 — Professional Embedded Widgets
 * 1. Project Estimator — multi-step: service → scope → location → details → AI estimate
 * 2. Service Advisor — guided diagnostic with detailed, structured AI recommendation
 * Both use Gemini 2.5 Flash via Cloudflare Worker proxy.
 */
(function () {
  'use strict';

  var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  var MODEL = 'gemini-2.5-pro';
  var isSI = window.location.pathname.startsWith('/safety-installs');

  var TOWNS = ['Norfolk','Columbus','Fremont','Wayne','South Sioux City','West Point','Schuyler',
    'O\'Neill','Madison','Stanton','Pierce','Neligh','Albion','Humphrey','Wisner','Pender',
    'Tekamah','Oakland','Plainview','Tilden','Battle Creek','Sioux City, IA','Le Mars, IA','Onawa, IA','Other'];

  var B = isSI
    ? { name:'Watts Safety Installs', c:'#dc2626', cd:'#b91c1c', cl:'#fef2f2', bg:'#1a1a1a', tx:'#f5f5dc',
        accent:'#991b1b', badge:'Licensed & Insured · NE Reg #54690-25',
        services:[
          {id:'remodel',label:'Kitchen & Bath Remodeling',icon:'fa-kitchen-set',
           scopes:['Full kitchen remodel','Partial kitchen update','Full bathroom remodel','Tub-to-shower conversion','Countertop & cabinet replacement','Tile work only']},
          {id:'paint',label:'Interior & Exterior Painting',icon:'fa-paint-roller',
           scopes:['Single room interior','Whole house interior','Exterior siding & trim','Deck / fence staining','Cabinet painting','Touch-up & repair']},
          {id:'gutter',label:'Gutter Install & Repair',icon:'fa-droplet',
           scopes:['Full gutter replacement','Partial repair / patching','Gutter guard installation','Downspout rerouting','Cleaning & maintenance','Soffit & fascia repair']},
          {id:'handy',label:'Handyman Services',icon:'fa-screwdriver-wrench',
           scopes:['Door / window repair','Drywall patching','Shelving & storage install','Fixture replacement','Weather stripping','General repairs (describe below)']},
          {id:'tv',label:'Electronics & TV Mounting',icon:'fa-tv',
           scopes:['Single TV wall mount','Multi-room TV setup','Soundbar / surround install','Cable concealment','Smart home device setup','Outdoor TV installation']}
        ]}
    : { name:'Watts ATP Contractor', c:'#00C4B4', cd:'#009e91', cl:'#E0F7FA', bg:'#0A1D37', tx:'#FFD700',
        accent:'#007a6e', badge:'ATP Approved · NE Reg #54690-25 · Insured $1M',
        services:[
          {id:'ramp',label:'Wheelchair Ramp Installation',icon:'fa-wheelchair-move',
           scopes:['Wooden ramp (new build)','Aluminum modular ramp','Concrete ramp','Threshold ramp only','Ramp with landing / turn','Ramp removal & replacement']},
          {id:'grab',label:'Grab Bar Installation',icon:'fa-hand-holding-medical',
           scopes:['Single grab bar','Bathroom grab bar set (3–5 bars)','Shower / tub grab bars','Toilet area bars','Stairway grab rails','Whole-home grab bar package']},
          {id:'floor',label:'Non-Slip Flooring',icon:'fa-shoe-prints',
           scopes:['Single bathroom floor','Multiple bathroom floors','Hallway / entryway','Full home flooring','Non-slip coating application','Transition strip installation']},
          {id:'bath',label:'Bathroom Accessibility',icon:'fa-bath',
           scopes:['Walk-in shower conversion','Roll-in shower build','Raised toilet installation','Accessible vanity / sink','Full ADA bathroom remodel','Shower seat & accessories']},
          {id:'safety',label:'Accessibility & Safety Solutions',icon:'fa-shield-halved',
           scopes:['Home safety assessment','Stair lift installation','Door widening','Lighting upgrades','Lever handle conversion','Multi-room accessibility package']}
        ]};

  // ── SYSTEM INSTRUCTIONS (brand-specific — must be before callProxy) ──
  var SYS_INSTRUCTION = isSI
    ? 'You are Justin Watts, owner and lead contractor at Watts Safety Installs — a licensed, insured home services company (NE Reg #54690-25) based in Norfolk, Nebraska. You personally handle every project. You serve a 100-mile radius covering Norfolk, Columbus, Fremont, Wayne, South Sioux City, West Point, and surrounding towns.\n\n' +
      'YOUR SERVICES & EXPERTISE:\n' +
      '• Kitchen & Bath Remodeling — full gut remodels, cabinet replacement, tile, countertops, tub-to-shower conversions. You source materials from local suppliers and big-box stores depending on budget. Typical kitchen remodel: $15K–$50K. Partial kitchen update: $5K–$15K. Typical bathroom: $8K–$25K. Tub-to-shower conversion: $5K–$12K.\n' +
      '• Interior & Exterior Painting — prep work is 70% of a good paint job. You scrape, sand, prime, caulk. Sherwin-Williams and Benjamin Moore products. Single room: $400–$1,200. Whole house interior: $4K–$12K. Exterior: $5K–$15K.\n' +
      '• Gutter Install & Repair — 5" and 6" seamless aluminum. You carry a gutter machine on your truck. Full replacement: $1,800–$5,000. Guards: $1,200–$3,500. You also do soffit/fascia.\n' +
      '• Handyman Services — doors, windows, drywall, shelving, fixtures, weather stripping, odd jobs. Hourly rate around $75–$95/hr or flat-rate per job. Most jobs $200–$1,500.\n' +
      '• Electronics & TV Mounting — wall mounts, cable concealment, surround sound, smart home setup. Single TV mount: $200–$450. Multi-room setup: $500–$2,000.\n\n' +
      'YOUR PERSONALITY: You\'re down-to-earth, honest, and you explain things in plain English. You don\'t upsell. You tell people what they actually need. You\'ve been doing this work for years and you\'ve seen it all. You\'re proud of your work and you stand behind it.\n\n' +
      'RULES: Always sound like a real contractor talking to a homeowner, not a chatbot. Use specific details — material names, timeframes, process steps. Never be vague or generic. Always end with an invitation to call (405) 410-6402 for a free estimate or consultation. Prices should reflect Nebraska market rates.'
    : 'You are Justin Watts, owner and lead contractor at Watts ATP Contractor — an ATP-approved, licensed, insured accessibility contractor (NE Reg #54690-25) based in Norfolk, Nebraska. You specialize in home accessibility and safety modifications. You serve a 100-mile radius.\n\n' +
      'YOUR SERVICES & EXPERTISE:\n' +
      '• Wheelchair Ramp Installation — wood, aluminum modular, concrete. ADA-compliant slopes (1:12 ratio). You handle permits. Wood ramps: $2,500–$7,000. Aluminum modular: $4,000–$12,000. Concrete: $3,500–$10,000. You\'ve built hundreds.\n' +
      '• Grab Bar Installation — stainless, chrome, designer finishes. You locate studs, use proper blocking. Single bar: $200–$400 installed. Full bathroom set (3-5 bars): $600–$1,500. Whole-home package: $1,200–$3,000.\n' +
      '• Non-Slip Flooring — vinyl plank, textured tile, non-slip coatings. Single bathroom: $1,200–$3,500. Multiple rooms: $3,000–$8,000. You remove old flooring, prep subfloor, install.\n' +
      '• Bathroom Accessibility — walk-in showers, roll-in showers, comfort-height toilets, accessible vanities. Tub-to-shower conversion: $6,000–$15,000. Full ADA bathroom: $12,000–$30,000.\n' +
      '• Accessibility & Safety Solutions — stair lifts ($3,000–$8,000), door widening ($800–$2,500 per door), lever handles, lighting upgrades, home safety assessments. You do free assessments.\n\n' +
      'YOUR PERSONALITY: You genuinely care about helping people stay safe in their homes. Many of your clients are elderly or recently discharged from the hospital. You\'re patient, kind, and you explain everything clearly. You work with ATP (Assistive Technology Partnership) and insurance when applicable.\n\n' +
      'RULES: Sound like a real contractor who cares, not a chatbot. Use specific details. Never be vague. Always invite them to call (405) 410-6402. Use Nebraska pricing.';

  // ── PROXY CALL WITH RETRY (robust — handles thinking model, long timeouts, logging) ──
  function callProxy(prompt, maxTokens, attempt) {
    attempt = attempt || 0;
    var MAX_RETRIES = 3;
    var TIMEOUT_MS = 45000; // 45 seconds — Gemini 2.5 Flash thinks before responding
    var body = {
      system_instruction: { parts: [{ text: SYS_INSTRUCTION }] },
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.7, maxOutputTokens: maxTokens || 2048, topP: 0.9 },
      safetySettings: [
        { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' }
      ]
    };

    var controller = new AbortController();
    var timer = setTimeout(function(){ controller.abort(); }, TIMEOUT_MS);

    // Show "taking longer" message after 10 seconds
    var slowTimer = setTimeout(function() {
      var spinners = document.querySelectorAll('.fa-cog.fa-spin, .fa-magnifying-glass-chart.fa-pulse');
      spinners.forEach(function(s) {
        var parent = s.closest('div[style]');
        if (parent) {
          var note = parent.querySelector('.wai-slow-note');
          if (!note) {
            var el = document.createElement('p');
            el.className = 'wai-slow-note';
            el.style.cssText = 'color:#94a3b8;font-size:.8rem;margin-top:8px';
            el.textContent = 'Still working — Gemini is thinking through your project details...';
            parent.appendChild(el);
          }
        }
      });
    }, 10000);

    console.log('[Watts AI] callProxy attempt ' + (attempt + 1) + '/' + (MAX_RETRIES + 1));

    return fetch(PROXY + '?model=' + MODEL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: controller.signal
    }).then(function(r) {
      clearTimeout(timer);
      clearTimeout(slowTimer);
      console.log('[Watts AI] HTTP status: ' + r.status);
      if (r.status === 429) throw new Error('RATE_LIMIT');
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function(d) {
      console.log('[Watts AI] Response received, parsing...');
      var candidate = d.candidates && d.candidates[0];
      if (!candidate) { console.error('[Watts AI] No candidates in response', d); throw new Error('No candidates'); }
      if (candidate.finishReason === 'SAFETY') { console.warn('[Watts AI] Safety filter triggered'); throw new Error('Safety filter'); }

      // Handle Gemini 2.5 Flash thinking model — it may return multiple parts
      // The actual response text is in a part WITHOUT a "thought" property
      var parts = candidate.content && candidate.content.parts;
      if (!parts || parts.length === 0) { console.error('[Watts AI] No parts in response', candidate); throw new Error('Empty parts'); }

      var text = '';
      for (var i = 0; i < parts.length; i++) {
        // Skip thinking/thought parts — only grab the actual response
        if (parts[i].thought) continue;
        if (parts[i].text) { text = parts[i].text; break; }
      }

      // Fallback: if no non-thought text found, grab any text
      if (!text) {
        for (var j = 0; j < parts.length; j++) {
          if (parts[j].text) { text = parts[j].text; break; }
        }
      }

      if (!text || text.trim().length < 20) {
        console.error('[Watts AI] Response too short: "' + (text || '') + '"');
        throw new Error('Empty response');
      }

      console.log('[Watts AI] Success — got ' + text.length + ' chars');
      return text;
    }).catch(function(err) {
      clearTimeout(timer);
      clearTimeout(slowTimer);
      console.warn('[Watts AI] Attempt ' + (attempt + 1) + ' failed: ' + err.message);

      // Don't retry rate limits — just wait and fail gracefully
      if (err.message === 'RATE_LIMIT') {
        console.error('[Watts AI] Rate limited — not retrying');
        throw err;
      }

      if (attempt < MAX_RETRIES) {
        var delay = (attempt + 1) * 2000; // 2s, 4s, 6s backoff
        console.log('[Watts AI] Retrying in ' + delay + 'ms...');
        return new Promise(function(resolve) {
          setTimeout(function() { resolve(callProxy(prompt, maxTokens, attempt + 1)); }, delay);
        });
      }
      console.error('[Watts AI] All retries exhausted');
      throw err;
    });
  }

  // ── STYLES ──
  var css = document.createElement('style');
  css.textContent = '\
.wai-section{max-width:960px;margin:48px auto 32px;padding:0 20px}\
.wai-section-title{text-align:center;margin-bottom:32px}\
.wai-section-title h2{font-family:"Playfair Display",serif;font-size:2rem;color:' + B.bg + ';margin-bottom:8px}\
.wai-section-title p{color:#64748B;font-size:1rem;max-width:560px;margin:0 auto}\
.wai-row{display:grid;grid-template-columns:1fr 1fr;gap:24px}\
.wai-card{background:#fff;border-radius:16px;padding:32px 28px;box-shadow:0 2px 24px rgba(0,0,0,.07);position:relative;overflow:hidden}\
.wai-card::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,' + B.c + ',' + B.cd + ')}\
.wai-card-header{display:flex;align-items:center;gap:14px;margin-bottom:6px}\
.wai-card-icon{width:48px;height:48px;border-radius:12px;background:' + B.cl + ';display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:' + B.c + ';flex-shrink:0}\
.wai-card-header h3{font-family:"Playfair Display",serif;font-size:1.35rem;color:' + B.bg + ';margin:0}\
.wai-card .sub{color:#64748B;font-size:.88rem;margin-bottom:20px;line-height:1.5}\
.wai-badge{display:inline-block;background:' + B.cl + ';color:' + B.accent + ';font-size:.75rem;font-weight:600;padding:4px 12px;border-radius:20px;margin-bottom:16px}\
.wai-step-label{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:' + B.c + ';margin-bottom:8px}\
.wai-field-label{font-weight:600;font-size:.9rem;color:' + B.bg + ';margin-bottom:10px;display:block}\
.wai-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-bottom:16px}\
.wai-grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:16px}\
.wai-opt{background:#f8f9fa;border:2px solid #e9ecef;border-radius:10px;padding:12px 10px;text-align:center;\
cursor:pointer;transition:all .2s;font-size:.82rem;font-weight:500;color:#555;line-height:1.3}\
.wai-opt:hover{border-color:' + B.c + ';color:' + B.c + ';background:' + B.cl + '}\
.wai-opt.on{border-color:' + B.c + ';background:' + B.cl + ';color:' + B.cd + ';font-weight:600}\
.wai-opt i{display:block;font-size:1.3rem;margin-bottom:5px;color:' + B.c + '}\
.wai-opt-sm{padding:10px 8px;font-size:.78rem}\
.wai-input{width:100%;padding:11px 14px;border:1.5px solid #e0e0e0;border-radius:8px;font-size:.9rem;\
outline:none;transition:border-color .2s;margin-bottom:10px;font-family:inherit;background:#fafafa}\
.wai-input:focus{border-color:' + B.c + ';background:#fff}\
.wai-select{width:100%;padding:11px 14px;border:1.5px solid #e0e0e0;border-radius:8px;font-size:.9rem;\
outline:none;background:#fafafa;font-family:inherit;margin-bottom:10px;cursor:pointer;appearance:auto}\
.wai-select:focus{border-color:' + B.c + ';background:#fff}\
.wai-btn{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,' + B.c + ',' + B.cd + ');\
color:#fff;border:none;padding:13px 32px;border-radius:10px;font-size:.95rem;font-weight:600;cursor:pointer;\
transition:all .25s;box-shadow:0 2px 8px ' + B.c + '40}\
.wai-btn:hover{transform:translateY(-2px);box-shadow:0 4px 16px ' + B.c + '50}\
.wai-btn:disabled{opacity:.45;cursor:default;transform:none;box-shadow:none}\
.wai-btn i{font-size:.85rem}\
.wai-btn-outline{background:transparent;color:' + B.c + ';border:2px solid ' + B.c + ';box-shadow:none;padding:10px 20px;font-size:.85rem}\
.wai-btn-outline:hover{background:' + B.cl + ';transform:none;box-shadow:none}\
.wai-result{margin-top:20px;padding:24px;background:linear-gradient(135deg,' + B.cl + ',#fff);border-radius:12px;\
border-left:4px solid ' + B.c + ';font-size:.92rem;line-height:1.7;color:#333;display:none}\
.wai-result.show{display:block;animation:waiIn .4s ease}\
.wai-result h4{color:' + B.bg + ';font-size:1rem;margin:0 0 8px;font-family:"Playfair Display",serif}\
.wai-result strong{color:' + B.bg + '}\
.wai-result .est-range{font-size:1.6rem;font-weight:700;color:' + B.c + ';margin:8px 0 4px;font-family:"Playfair Display",serif}\
.wai-result .est-note{font-size:.8rem;color:#94a3b8;margin-bottom:12px}\
.wai-result .cta{display:inline-flex;align-items:center;gap:8px;margin-top:16px;background:linear-gradient(135deg,' + B.c + ',' + B.cd + ');\
color:#fff;padding:12px 28px;border-radius:10px;text-decoration:none;font-weight:600;font-size:.9rem;\
box-shadow:0 2px 8px ' + B.c + '40;transition:all .25s}\
.wai-result .cta:hover{transform:translateY(-1px);box-shadow:0 4px 12px ' + B.c + '50}\
.wai-divider{height:1px;background:#e9ecef;margin:16px 0}\
.wai-steps{display:flex;gap:6px;margin-bottom:20px}\
.wai-step-dot{width:100%;height:4px;border-radius:2px;background:#e9ecef;transition:background .3s}\
.wai-step-dot.done{background:' + B.c + '}\
.wai-step-dot.active{background:' + B.cd + '}\
.wai-progress{height:4px;background:#e9ecef;border-radius:2px;margin-bottom:20px;overflow:hidden}\
.wai-progress-bar{height:100%;background:linear-gradient(90deg,' + B.c + ',' + B.cd + ');border-radius:2px;transition:width .4s ease}\
.wai-rec-card{background:#fff;border:1.5px solid #e9ecef;border-radius:12px;padding:16px;margin-bottom:10px;transition:all .2s}\
.wai-rec-card:hover{border-color:' + B.c + '}\
.wai-rec-card h5{color:' + B.bg + ';font-size:.95rem;margin:0 0 4px}\
.wai-rec-card p{color:#64748B;font-size:.82rem;margin:0;line-height:1.5}\
.wai-rec-match{display:inline-block;background:' + B.cl + ';color:' + B.accent + ';font-size:.7rem;font-weight:700;padding:2px 8px;border-radius:10px;margin-bottom:6px}\
.wai-slider-wrap{padding:8px 0 16px}\
.wai-slider-track{position:relative;width:100%;height:6px;background:#e9ecef;border-radius:3px;margin:20px 0 12px}\
.wai-slider-fill{position:absolute;left:0;top:0;height:100%;background:linear-gradient(90deg,' + B.c + ',' + B.cd + ');border-radius:3px;transition:width .15s}\
.wai-range-input{-webkit-appearance:none;appearance:none;width:100%;height:6px;background:transparent;position:absolute;top:0;left:0;margin:0;cursor:pointer;z-index:2}\
.wai-range-input::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;border-radius:50%;background:' + B.c + ';border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.2);cursor:grab}\
.wai-range-input::-moz-range-thumb{width:24px;height:24px;border-radius:50%;background:' + B.c + ';border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.2);cursor:grab}\
.wai-budget-display{text-align:center;font-size:1.5rem;font-weight:700;color:' + B.c + ';font-family:"Playfair Display",serif;margin-bottom:4px}\
.wai-budget-labels{display:flex;justify-content:space-between;font-size:.72rem;color:#94a3b8;margin-top:2px}\
.wai-budget-hint{text-align:center;color:#94a3b8;font-size:.8rem;margin-bottom:16px}\
@keyframes waiIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}\
@media(max-width:768px){.wai-row{grid-template-columns:1fr}.wai-grid{grid-template-columns:repeat(2,1fr)}\
.wai-grid-3{grid-template-columns:repeat(2,1fr)}.wai-card{padding:24px 18px}\
.wai-section-title h2{font-size:1.5rem}.wai-result .est-range{font-size:1.3rem}}\
';
  document.head.appendChild(css);

  // ── QUOTE ESTIMATOR (multi-step) ──
  function buildQuoteCalc() {
    var el = document.getElementById('watts-quote-calc');
    if (!el) return;

    var state = { service: null, scope: null, town: '', details: '', step: 0 };

    function renderStep() {
      var s = state.step;
      var dots = '';
      for (var d = 0; d < 4; d++) {
        dots += '<div class="wai-step-dot ' + (d < s ? 'done' : '') + (d === s ? ' active' : '') + '"></div>';
      }

      var html = '<div class="wai-card">\
<div class="wai-card-header"><div class="wai-card-icon"><i class="fas fa-file-invoice-dollar"></i></div>\
<div><h3>Project Estimator</h3></div></div>\
<p class="sub">Get a detailed, AI-powered estimate tailored to your project — completely free, no obligation.</p>\
<span class="wai-badge"><i class="fas fa-shield-halved"></i> ' + B.badge + '</span>\
<div class="wai-steps">' + dots + '</div>';

      if (s === 0) {
        html += '<div class="wai-step-label">Step 1 of 4 — Select Your Service</div>';
        html += '<div class="wai-grid">';
        B.services.forEach(function(svc) {
          html += '<div class="wai-opt' + (state.service === svc.id ? ' on' : '') + '" data-svc="' + svc.id + '">\
<i class="fas ' + svc.icon + '"></i>' + svc.label + '</div>';
        });
        html += '</div>';
      } else if (s === 1) {
        var svc = null;
        B.services.forEach(function(sv) { if (sv.id === state.service) svc = sv; });
        html += '<div class="wai-step-label">Step 2 of 4 — Scope of Work</div>';
        html += '<span class="wai-field-label">What best describes your ' + svc.label.toLowerCase() + ' project?</span>';
        html += '<div class="wai-grid">';
        svc.scopes.forEach(function(sc) {
          html += '<div class="wai-opt wai-opt-sm' + (state.scope === sc ? ' on' : '') + '" data-scope="' + sc + '">' + sc + '</div>';
        });
        html += '</div>';
        html += '<button class="wai-btn-outline wai-back" style="margin-top:4px"><i class="fas fa-arrow-left"></i> Back</button>';
      } else if (s === 2) {
        html += '<div class="wai-step-label">Step 3 of 4 — Location & Details</div>';
        html += '<span class="wai-field-label">Where is the project located?</span>';
        html += '<select class="wai-select" id="wq-town"><option value="">Select your city / town...</option>';
        TOWNS.forEach(function(t) {
          html += '<option value="' + t + '"' + (state.town === t ? ' selected' : '') + '>' + t + '</option>';
        });
        html += '</select>';
        html += '<span class="wai-field-label" style="margin-top:6px">Describe your project</span>';
        html += '<textarea class="wai-input" id="wq-details" rows="3" placeholder="Help us understand your project: approximate dimensions, current condition, any accessibility needs, timeline preferences, budget range if you have one...">' + state.details + '</textarea>';
        html += '<div style="display:flex;gap:10px;align-items:center">';
        html += '<button class="wai-btn-outline wai-back"><i class="fas fa-arrow-left"></i> Back</button>';
        html += '<button class="wai-btn" id="wq-go"><i class="fas fa-calculator"></i> Generate My Estimate</button>';
        html += '</div>';
      } else if (s === 3) {
        html += '<div style="text-align:center;padding:24px 0">\
<div style="width:48px;height:48px;border-radius:50%;background:' + B.cl + ';display:inline-flex;align-items:center;justify-content:center;margin-bottom:12px">\
<i class="fas fa-cog fa-spin" style="font-size:1.2rem;color:' + B.c + '"></i></div>\
<p style="font-weight:600;color:' + B.bg + ';margin-bottom:4px">Analyzing your project...</p>\
<p style="color:#94a3b8;font-size:.85rem">Reviewing scope, materials, and local pricing data</p></div>';
      }

      html += '<div class="wai-result" id="wq-result"></div></div>';
      el.innerHTML = html;
      bindStepEvents();
    }

    function bindStepEvents() {
      var s = state.step;
      if (s === 0) {
        el.querySelectorAll('[data-svc]').forEach(function(btn) {
          btn.addEventListener('click', function() {
            state.service = btn.dataset.svc;
            state.scope = null;
            state.step = 1;
            renderStep();
          });
        });
      } else if (s === 1) {
        el.querySelectorAll('[data-scope]').forEach(function(btn) {
          btn.addEventListener('click', function() {
            state.scope = btn.dataset.scope;
            state.step = 2;
            renderStep();
          });
        });
        var back = el.querySelector('.wai-back');
        if (back) back.addEventListener('click', function() { state.step = 0; renderStep(); });
      } else if (s === 2) {
        var goBtn = document.getElementById('wq-go');
        var townSel = document.getElementById('wq-town');
        var detailsEl = document.getElementById('wq-details');
        var back = el.querySelector('.wai-back');
        if (back) back.addEventListener('click', function() {
          state.town = townSel.value;
          state.details = detailsEl.value;
          state.step = 1;
          renderStep();
        });
        if (goBtn) goBtn.addEventListener('click', function() {
          state.town = townSel.value;
          state.details = detailsEl.value;
          state.step = 3;
          renderStep();
          generateEstimate();
        });
      }
    }

    function generateEstimate() {
      var svcLabel = '';
      B.services.forEach(function(sv) { if (sv.id === state.service) svcLabel = sv.label; });
      var loc = state.town || 'Northeast Nebraska';

      var prompt = 'A potential customer wants an estimate for a project:\n' +
        '• SERVICE: ' + svcLabel + '\n' +
        '• SCOPE: ' + state.scope + '\n' +
        '• LOCATION: ' + loc + '\n' +
        (state.details ? '• THEIR DESCRIPTION: ' + state.details + '\n' : '') +
        '\nAs Justin, give them a detailed, professional estimate. Write in natural paragraphs — like you\'re talking to them in their kitchen.\n\n' +
        'Your response MUST include ALL of these:\n\n' +
        '1. A realistic PRICE RANGE for this specific scope using Nebraska contractor rates (bold with **: **$X,XXX – $X,XXX**). Be specific to what they selected.\n\n' +
        '2. EXPLAIN what drives the cost — materials, labor hours, complexity. Name specific materials you\'d likely use (e.g., "5/4 pressure-treated decking" or "Sherwin-Williams Duration exterior").\n\n' +
        '3. Tell them what\'s INCLUDED at this price — prep work, materials, labor, cleanup, warranty. Be specific, not generic.\n\n' +
        '4. Mention ONE thing that could push the price up or down (e.g., "If your subfloor needs replacing, add another $500–$1,000").\n\n' +
        '5. Describe the PROCESS briefly — "I\'d come out, take measurements, give you a written quote same day..."\n\n' +
        '6. End with: invite them to call (405) 410-6402 for a free on-site estimate.\n\n' +
        'RULES:\n' +
        '- Write 150–200 words. This is a REAL estimate breakdown, not a one-liner.\n' +
        '- Use Nebraska contractor pricing, not national averages\n' +
        '- Be specific to the exact scope they selected\n' +
        '- Sound like a contractor who\'s done this work a thousand times\n' +
        '- NO bullet points, NO numbered lists — flowing paragraphs\n' +
        '- Format price ranges and service names in bold with **';

      callProxy(prompt, 2048).then(function(text) {
        var formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
        var rangeMatch = text.match(/\$[\d,]+\s*[–—-]\s*\$[\d,]+/);
        var rangeStr = rangeMatch ? rangeMatch[0] : '';

        var resultHtml = '<h4><i class="fas fa-clipboard-check" style="color:' + B.c + ';margin-right:8px"></i>Your Project Estimate</h4>';
        if (rangeStr) {
          resultHtml += '<div class="est-range">' + rangeStr + '</div>';
          resultHtml += '<div class="est-note">Estimated range for ' + state.scope + ' in ' + loc + '</div>';
          resultHtml += '<div class="wai-divider"></div>';
        }
        resultHtml += '<div>' + formatted + '</div>';
        resultHtml += '<a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> Schedule Free On-Site Estimate</a>';
        resultHtml += '<div style="margin-top:12px"><button class="wai-btn-outline" id="wq-restart"><i class="fas fa-redo"></i> Start New Estimate</button></div>';

        var result = document.getElementById('wq-result');
        if (result) { result.innerHTML = resultHtml; result.classList.add('show'); }
        var spinner = el.querySelector('.fa-cog');
        if (spinner) spinner.closest('div[style]').style.display = 'none';
        var restart = document.getElementById('wq-restart');
        if (restart) restart.addEventListener('click', function() {
          state = { service: null, scope: null, town: '', details: '', step: 0 };
          renderStep();
        });
      }).catch(function() {
        // Contextual fallback with real info instead of generic dead-end
        var svcLabel2 = '';
        B.services.forEach(function(sv) { if (sv.id === state.service) svcLabel2 = sv.label; });
        var result = document.getElementById('wq-result');
        if (result) {
          result.innerHTML = '<h4><i class="fas fa-clipboard-check" style="color:' + B.c + ';margin-right:8px"></i>Estimate for ' + svcLabel2 + '</h4>' +
            '<p><strong>' + state.scope + '</strong> in <strong>' + (state.town || 'your area') + '</strong></p>' +
            '<p>I want to give you an accurate number for this — not a ballpark guess. Every ' + svcLabel2.toLowerCase() + ' project has unique variables like materials, site conditions, and scope that affect the final price.</p>' +
            '<p>Here\'s what I can tell you: I\'ll come out, take measurements, assess the situation, and give you a detailed written estimate — <strong>100% free, zero obligation</strong>. Most estimates take about 15–20 minutes and I can usually get out there within a day or two.</p>' +
            '<a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> (405) 410-6402 — Schedule Free Estimate</a>' +
            '<div style="margin-top:12px"><button class="wai-btn-outline" id="wq-restart"><i class="fas fa-redo"></i> Try Again</button></div>';
          result.classList.add('show');
        }
        var spinner = el.querySelector('.fa-cog');
        if (spinner) spinner.closest('div[style]').style.display = 'none';
        var restart = document.getElementById('wq-restart');
        if (restart) restart.addEventListener('click', function() {
          state = { service: null, scope: null, town: '', details: '', step: 0 };
          renderStep();
        });
      });
    }

    renderStep();
  }

  // ── SERVICE ADVISOR (guided diagnostic) ──
  function buildRecommender() {
    var el = document.getElementById('watts-recommender');
    if (!el) return;

    var questions = isSI ? [
      { q: 'What type of project are you looking at?', icon: 'fa-house',
        opts: [
          {label:'Kitchen remodel',icon:'fa-kitchen-set',desc:'Cabinets, counters, tile, layout'},
          {label:'Bathroom remodel',icon:'fa-bath',desc:'Fixtures, tile, vanity, shower'},
          {label:'Painting',icon:'fa-paint-roller',desc:'Interior or exterior'},
          {label:'Gutters',icon:'fa-droplet',desc:'Install, repair, guards'},
          {label:'Handyman / repairs',icon:'fa-screwdriver-wrench',desc:'Doors, drywall, fixtures'},
          {label:'TV / electronics',icon:'fa-tv',desc:'Mounting, wiring, smart home'}
        ]},
      { q: 'Tell me more about what you need done:', icon: 'fa-bullseye',
        opts: [
          {label:'Full tear-out & rebuild',desc:'Start from scratch, new everything'},
          {label:'Update the look',desc:'Keep the bones, freshen it up'},
          {label:'Fix something specific',desc:'Leak, crack, broken fixture'},
          {label:'Install something new',desc:'Add what\'s not there yet'},
          {label:'Maintenance / prevent issues',desc:'Upkeep before problems start'},
          {label:'Not sure — need advice',desc:'I want a pro to tell me what\'s best'}
        ]},
      { q: 'What\'s your timeline looking like?', icon: 'fa-calendar',
        opts: [
          {label:'ASAP — this week',desc:'Urgent, need it handled now'},
          {label:'Next couple weeks',desc:'Soon but flexible'},
          {label:'1–2 months out',desc:'Planning ahead, no rush'},
          {label:'Just pricing it out',desc:'Gathering info before deciding'}
        ]},
      { q: 'What budget range are you working with?', icon: 'fa-wallet',
        type: 'slider', min: 0, max: 50000, step: 500, defaultVal: 5000,
        format: function(v) { return v >= 50000 ? '$50,000+' : '$' + v.toLocaleString(); },
        hint: 'Drag the slider — don\'t worry about being exact, this just helps me tailor my recommendation.' }
    ] : [
      { q: 'Who will benefit from these modifications?', icon: 'fa-users',
        opts: [
          {label:'Aging parent',icon:'fa-person-cane',desc:'Help them stay home safely'},
          {label:'Myself',icon:'fa-user',desc:'Planning for my own needs'},
          {label:'Spouse or partner',icon:'fa-heart',desc:'Supporting their mobility'},
          {label:'Family member',icon:'fa-people-roof',desc:'Child or relative'},
          {label:'Planning ahead',icon:'fa-calendar-check',desc:'Proactive modifications'},
          {label:'Rental / facility',icon:'fa-building',desc:'ADA compliance needs'}
        ]},
      { q: 'Which area of the home needs modification?', icon: 'fa-house',
        opts: [
          {label:'Bathroom',icon:'fa-bath',desc:'Shower, tub, toilet area'},
          {label:'Entrance / doorway',icon:'fa-door-open',desc:'Getting in and out'},
          {label:'Stairs / levels',icon:'fa-stairs',desc:'Between floors'},
          {label:'Flooring',icon:'fa-shoe-prints',desc:'Slip hazards'},
          {label:'Multiple areas',icon:'fa-layer-group',desc:'Whole-home assessment'},
          {label:'Outdoor access',icon:'fa-tree',desc:'Yard, porch, driveway'}
        ]},
      { q: 'What is the primary concern?', icon: 'fa-shield-halved',
        opts: [
          {label:'Fall prevention',desc:'Reduce slip & trip risks'},
          {label:'Wheelchair access',desc:'Ramps, widened doors'},
          {label:'General mobility',desc:'Easier movement around home'},
          {label:'ADA compliance',desc:'Meet legal requirements'},
          {label:'Post-surgery prep',desc:'Temporary or permanent needs'},
          {label:'Not sure yet',desc:'Need a professional assessment'}
        ]},
      { q: 'How soon do you need this completed?', icon: 'fa-clock',
        opts: [
          {label:'Urgent — within days',desc:'Medical need or discharge'},
          {label:'Within 2 weeks',desc:'Soon but not emergency'},
          {label:'Within 1–2 months',desc:'Planning ahead'},
          {label:'Just researching',desc:'Gathering info & pricing'}
        ]},
      { q: 'What budget range are you working with?', icon: 'fa-wallet',
        type: 'slider', min: 0, max: 50000, step: 500, defaultVal: 5000,
        format: function(v) { return v >= 50000 ? '$50,000+' : '$' + v.toLocaleString(); },
        hint: 'Drag the slider — this helps me recommend the right scope for your budget.' }
    ];

    var answers = [];
    var step = 0;

    function render() {
      var pct = Math.round((step / questions.length) * 100);
      var html = '<div class="wai-card">\
<div class="wai-card-header"><div class="wai-card-icon"><i class="fas fa-stethoscope"></i></div>\
<div><h3>Service Advisor</h3></div></div>\
<p class="sub">Tell us about your situation and we\'ll recommend the right service — personalized to your needs, powered by AI.</p>\
<span class="wai-badge"><i class="fas fa-robot"></i> AI-Powered Recommendation</span>\
<div class="wai-progress"><div class="wai-progress-bar" style="width:' + pct + '%"></div></div>';

      if (step < questions.length) {
        var q = questions[step];
        html += '<div class="wai-step-label">Question ' + (step + 1) + ' of ' + questions.length + '</div>';
        html += '<span class="wai-field-label"><i class="fas ' + q.icon + '" style="color:' + B.c + ';margin-right:6px"></i>' + q.q + '</span>';
        if (q.type === 'slider') {
          var curVal = answers[step] ? parseInt(answers[step].replace(/[^0-9]/g,'')) : q.defaultVal;
          html += '<div class="wai-slider-wrap">';
          html += '<div class="wai-budget-display" id="wr-budget-val">' + q.format(curVal) + '</div>';
          if (q.hint) html += '<p class="wai-budget-hint">' + q.hint + '</p>';
          html += '<div class="wai-slider-track"><div class="wai-slider-fill" id="wr-slider-fill" style="width:' + ((curVal / q.max) * 100) + '%"></div>';
          html += '<input type="range" class="wai-range-input" id="wr-slider" min="' + q.min + '" max="' + q.max + '" step="' + q.step + '" value="' + curVal + '"></div>';
          html += '<div class="wai-budget-labels"><span>$0</span><span>$10K</span><span>$25K</span><span>$50K+</span></div>';
          html += '</div>';
          html += '<div style="display:flex;gap:10px;align-items:center;margin-top:8px">';
          if (step > 0) html += '<button class="wai-btn-outline wai-back"><i class="fas fa-arrow-left"></i> Back</button>';
          html += '<button class="wai-btn" id="wr-slider-next"><i class="fas fa-arrow-right"></i> Continue</button>';
          html += '</div>';
        } else {
          html += '<div class="wai-grid">';
          q.opts.forEach(function(o) {
            html += '<div class="wai-opt wai-opt-sm" data-ans="' + o.label + '">';
            if (o.icon) html += '<i class="fas ' + o.icon + '"></i>';
            html += '<strong>' + o.label + '</strong>';
            if (o.desc) html += '<br><span style="font-size:.72rem;color:#94a3b8;font-weight:400">' + o.desc + '</span>';
            html += '</div>';
          });
          html += '</div>';
          if (step > 0) html += '<button class="wai-btn-outline wai-back"><i class="fas fa-arrow-left"></i> Back</button>';
        }
      } else {
        html += '<div style="text-align:center;padding:24px 0">\
<div style="width:48px;height:48px;border-radius:50%;background:' + B.cl + ';display:inline-flex;align-items:center;justify-content:center;margin-bottom:12px">\
<i class="fas fa-magnifying-glass-chart fa-pulse" style="font-size:1.2rem;color:' + B.c + '"></i></div>\
<p style="font-weight:600;color:' + B.bg + ';margin-bottom:4px">Analyzing your needs...</p>\
<p style="color:#94a3b8;font-size:.85rem">Matching your situation to our services</p></div>';
      }

      html += '<div class="wai-result" id="wr-result"></div></div>';
      el.innerHTML = html;

      if (step < questions.length) {
        var q = questions[step];
        if (q.type === 'slider') {
          var slider = document.getElementById('wr-slider');
          var fill = document.getElementById('wr-slider-fill');
          var display = document.getElementById('wr-budget-val');
          if (slider) {
            slider.addEventListener('input', function() {
              var v = parseInt(slider.value);
              display.textContent = q.format(v);
              fill.style.width = ((v / q.max) * 100) + '%';
            });
          }
          var nextBtn = document.getElementById('wr-slider-next');
          if (nextBtn) nextBtn.addEventListener('click', function() {
            var v = parseInt(slider.value);
            answers[step] = q.format(v);
            step++;
            if (step < questions.length) { render(); }
            else { render(); getRecommendation(); }
          });
        } else {
          el.querySelectorAll('[data-ans]').forEach(function(btn) {
            btn.addEventListener('click', function() {
              answers[step] = btn.dataset.ans;
              step++;
              if (step < questions.length) { render(); }
              else { render(); getRecommendation(); }
            });
          });
        }
        var back = el.querySelector('.wai-back');
        if (back) back.addEventListener('click', function() { step--; render(); });
      }
    }

    function getRecommendation() {
      var svcList = B.services.map(function(s) { return s.label; }).join(', ');
      var prompt = 'A potential customer just completed our needs assessment on the website. Here are their answers:\n\n';
      questions.forEach(function(q, i) {
        prompt += '• ' + q.q + ' → ' + (answers[i] || 'Not answered') + '\n';
      });
      prompt += '\nAs Justin, give this person a detailed, personalized recommendation. Write it like you\'re talking directly to them — warm, knowledgeable, and specific.\n\n' +
        'Your response MUST include ALL of these (in flowing paragraphs, NOT bullet points):\n\n' +
        '1. LEAD with your top service recommendation (bold the service name with **). Tell them specifically WHY this is the right fit based on their exact answers — don\'t be generic.\n\n' +
        '2. EXPLAIN what the process looks like — what happens when you show up, how long it typically takes, what materials you\'d likely use. Give them a mental picture of the project from start to finish.\n\n' +
        '3. Give a REALISTIC PRICE RANGE for their specific scope using Nebraska rates. Be specific — "For a project like yours, you\'re typically looking at $X,XXX to $X,XXX depending on..."\n\n' +
        '4. If a SECOND service would complement the first one, mention it naturally — "While I\'m there, a lot of my customers also..."\n\n' +
        '5. Based on their timeline answer, address urgency appropriately — if urgent, emphasize your quick turnaround. If they\'re just exploring, reassure them there\'s no pressure.\n\n' +
        '6. END with a clear next step: invite them to call (405) 410-6402 for a free, no-obligation consultation or estimate.\n\n' +
        'RULES:\n' +
        '- Write 150–250 words. This is a DETAILED recommendation, not a one-liner.\n' +
        '- Sound like a real contractor who\'s done this a thousand times\n' +
        '- Reference their SPECIFIC answers, not generic filler\n' +
        '- Use real material names, timeframes, and Nebraska pricing\n' +
        '- NO bullet points, NO numbered lists — write in natural paragraphs\n' +
        '- Format service names and price ranges in bold with **';

      callProxy(prompt, 2048).then(function(text) {
        var formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
        var resultHtml = '<h4><i class="fas fa-check-circle" style="color:' + B.c + ';margin-right:8px"></i>Our Recommendation</h4>';
        resultHtml += '<div>' + formatted + '</div>';
        resultHtml += '<a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> Schedule Free Consultation</a>';
        resultHtml += '<div style="margin-top:12px"><button class="wai-btn-outline" id="wr-restart"><i class="fas fa-redo"></i> Start Over</button></div>';

        var result = document.getElementById('wr-result');
        if (result) { result.innerHTML = resultHtml; result.classList.add('show'); }
        var spinner = el.querySelector('.fa-magnifying-glass-chart');
        if (spinner) spinner.closest('div[style]').style.display = 'none';
        var restart = document.getElementById('wr-restart');
        if (restart) restart.addEventListener('click', function() { answers = []; step = 0; render(); });
      }).catch(function() {
        // Smart fallback — build a real recommendation from answers using service knowledge
        var answerSummary = [];
        questions.forEach(function(q, i) { if (answers[i]) answerSummary.push(answers[i]); });
        var combined = answerSummary.join(' ').toLowerCase();
        var bestGuess = '', fallbackDetail = '';

        // Service-specific matching with real details
        if (isSI) {
          if (combined.indexOf('kitchen') !== -1) {
            bestGuess = 'Kitchen & Bath Remodeling';
            fallbackDetail = 'For a kitchen project, I\'d typically start with an on-site visit to measure the space, look at your existing cabinets, plumbing, and electrical, and talk through what you want. A partial update (new countertops, backsplash, paint) usually runs <strong>$5,000–$15,000</strong>. A full gut remodel with new cabinets and layout changes is more like <strong>$15,000–$50,000</strong> depending on materials. I source from both local suppliers and big-box stores depending on your budget.';
          } else if (combined.indexOf('bathroom') !== -1) {
            bestGuess = 'Kitchen & Bath Remodeling';
            fallbackDetail = 'Bathroom remodels are one of my most common projects. A cosmetic refresh — new vanity, fixtures, paint, maybe some tile — typically runs <strong>$5,000–$12,000</strong>. A full remodel with tub-to-shower conversion, new tile, and layout changes is more like <strong>$8,000–$25,000</strong>. I handle all the plumbing, tile work, and finishing myself.';
          } else if (combined.indexOf('paint') !== -1) {
            bestGuess = 'Interior & Exterior Painting';
            fallbackDetail = 'Prep work is 70% of a good paint job — I scrape, sand, prime, and caulk before any paint goes on. A single room runs <strong>$400–$1,200</strong>, whole house interior <strong>$4,000–$12,000</strong>, exterior <strong>$5,000–$15,000</strong>. I use Sherwin-Williams and Benjamin Moore products exclusively.';
          } else if (combined.indexOf('gutter') !== -1) {
            bestGuess = 'Gutter Install & Repair';
            fallbackDetail = 'I carry a seamless gutter machine on my truck — 5" and 6" aluminum in your choice of colors. Full gutter replacement runs <strong>$1,800–$5,000</strong> for most homes. Gutter guards are <strong>$1,200–$3,500</strong>. I also handle soffit and fascia repair if needed.';
          } else if (combined.indexOf('tv') !== -1 || combined.indexOf('electronic') !== -1) {
            bestGuess = 'Electronics & TV Mounting';
            fallbackDetail = 'A single TV wall mount with cable concealment runs <strong>$200–$450</strong>. Multi-room setups, surround sound, and smart home integration depend on scope — usually <strong>$500–$2,000</strong>. I handle the mounting, wiring, and setup so everything looks clean.';
          } else {
            bestGuess = 'Handyman Services';
            fallbackDetail = 'I handle all kinds of home repairs and small projects — doors, windows, drywall, shelving, fixtures, weather stripping. I charge around <strong>$75–$95/hour</strong> or flat-rate for bigger jobs. Most handyman projects run <strong>$200–$1,500</strong> depending on scope.';
          }
        } else {
          if (combined.indexOf('bathroom') !== -1) { bestGuess = 'Bathroom Accessibility'; fallbackDetail = 'Walk-in shower conversions run <strong>$6,000–$15,000</strong>, and a full ADA bathroom remodel is typically <strong>$12,000–$30,000</strong>. I handle everything — demolition, plumbing, tile, fixtures, grab bars, and cleanup.'; }
          else if (combined.indexOf('entrance') !== -1 || combined.indexOf('wheelchair') !== -1) { bestGuess = 'Wheelchair Ramp Installation'; fallbackDetail = 'Wood ramps typically run <strong>$2,500–$7,000</strong> and aluminum modular ramps <strong>$4,000–$12,000</strong>. I build to ADA specs (1:12 slope ratio) and handle all permits.'; }
          else if (combined.indexOf('floor') !== -1 || combined.indexOf('slip') !== -1) { bestGuess = 'Non-Slip Flooring'; fallbackDetail = 'A single bathroom floor runs <strong>$1,200–$3,500</strong>. Multiple rooms: <strong>$3,000–$8,000</strong>. I remove the old flooring, prep the subfloor, and install slip-resistant vinyl plank or textured tile.'; }
          else if (combined.indexOf('stair') !== -1) { bestGuess = 'Accessibility & Safety Solutions'; fallbackDetail = 'Stair lifts run <strong>$3,000–$8,000</strong> installed, plus grab rails and other stairway safety modifications. I do a free home safety assessment to figure out exactly what you need.'; }
          else { bestGuess = 'Grab Bar Installation'; fallbackDetail = 'A single grab bar runs <strong>$200–$400</strong> installed, a full bathroom set (3-5 bars) is <strong>$600–$1,500</strong>, or a whole-home package is <strong>$1,200–$3,000</strong>. I locate studs and use proper blocking for maximum hold strength.'; }
        }

        var result = document.getElementById('wr-result');
        if (result) {
          result.innerHTML = '<h4><i class="fas fa-check-circle" style="color:' + B.c + ';margin-right:8px"></i>Our Recommendation</h4>' +
            '<p>Based on what you\'ve told me — <strong>' + answerSummary.join('</strong>, <strong>') + '</strong> — I\'d recommend our <strong>' + bestGuess + '</strong> service.</p>' +
            '<p>' + fallbackDetail + '</p>' +
            '<p>I\'m Justin, and I personally handle every project start to finish. I\'d love to come take a look at your situation — <strong>completely free, no pressure</strong>. I can usually get out there within a day or two.</p>' +
            '<a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> (405) 410-6402 — Free Consultation</a>' +
            '<div style="margin-top:12px"><button class="wai-btn-outline" id="wr-restart"><i class="fas fa-redo"></i> Try Again</button></div>';
          result.classList.add('show');
        }
        var spinner = el.querySelector('.fa-magnifying-glass-chart');
        if (spinner) spinner.closest('div[style]').style.display = 'none';
        var restart = document.getElementById('wr-restart');
        if (restart) restart.addEventListener('click', function() { answers = []; step = 0; render(); });
      });
    }

    render();
  }

  // callProxy is now defined above styles section

  // ── INIT ──
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { buildQuoteCalc(); buildRecommender(); });
  } else {
    buildQuoteCalc(); buildRecommender();
  }
})();
