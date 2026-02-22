/**
 * Watts AI Public Tools v2 — Professional Embedded Widgets
 * 1. Project Estimator — multi-step: service → scope → location → details → AI estimate
 * 2. Service Advisor — guided diagnostic with detailed, structured AI recommendation
 * Both use Gemini 2.5 Flash via Cloudflare Worker proxy.
 */
(function () {
  'use strict';

  var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  var MODEL = 'gemini-2.5-flash';
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

      var prompt = 'You are the lead estimator for ' + B.name + ', a licensed contractor (NE Reg #54690-25) based in Norfolk, Nebraska serving a 100-mile radius.\n\n' +
        'A potential customer has requested a project estimate:\n' +
        '• SERVICE: ' + svcLabel + '\n' +
        '• SCOPE: ' + state.scope + '\n' +
        '• LOCATION: ' + loc + '\n' +
        (state.details ? '• PROJECT DETAILS: ' + state.details + '\n' : '') +
        '\nProvide a professional estimate response with this EXACT structure:\n' +
        '1. First line: A realistic price RANGE using Nebraska market rates (format: **$X,XXX – $X,XXX**)\n' +
        '2. Second line: Brief explanation of what drives the cost (materials, labor, complexity)\n' +
        '3. Third line: What\'s typically INCLUDED at this price point (2-3 items)\n' +
        '4. Fourth line: One factor that could adjust the price up or down\n' +
        '5. Final line: "Schedule your free on-site estimate to get an exact quote — call (405) 410-6402"\n\n' +
        'RULES:\n' +
        '- Use realistic Nebraska contractor pricing, not national averages\n' +
        '- Be specific to the scope they selected, not generic\n' +
        '- Sound like a knowledgeable, trustworthy contractor — not a chatbot\n' +
        '- Keep total response under 120 words\n' +
        '- Format price range in bold with **\n' +
        '- Do NOT use bullet points or numbered lists — use flowing sentences';

      callProxy(prompt, 400).then(function(text) {
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
        var result = document.getElementById('wq-result');
        if (result) {
          result.innerHTML = '<h4>We\'d Love to Help</h4>' +
            '<p>Every project is unique, and we want to give you an accurate number — not a guess. ' +
            'Call us for a <strong>free, no-obligation on-site estimate</strong> tailored to your specific needs.</p>' +
            '<a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> (405) 410-6402 — Free Estimate</a>';
          result.classList.add('show');
        }
        var spinner = el.querySelector('.fa-cog');
        if (spinner) spinner.closest('div[style]').style.display = 'none';
      });
    }

    renderStep();
  }

  // ── SERVICE ADVISOR (guided diagnostic) ──
  function buildRecommender() {
    var el = document.getElementById('watts-recommender');
    if (!el) return;

    var questions = isSI ? [
      { q: 'What area of your home needs attention?', icon: 'fa-house',
        opts: [
          {label:'Kitchen',icon:'fa-kitchen-set',desc:'Cabinets, counters, layout'},
          {label:'Bathroom',icon:'fa-bath',desc:'Fixtures, tile, vanity'},
          {label:'Exterior',icon:'fa-tree',desc:'Siding, gutters, deck'},
          {label:'Living Areas',icon:'fa-couch',desc:'Walls, floors, fixtures'},
          {label:'Multiple Rooms',icon:'fa-layer-group',desc:'Whole-home project'},
          {label:'Electronics / AV',icon:'fa-tv',desc:'TV, sound, smart home'}
        ]},
      { q: 'What\'s the primary goal for this project?', icon: 'fa-bullseye',
        opts: [
          {label:'Complete renovation',desc:'Tear out and start fresh'},
          {label:'Cosmetic refresh',desc:'Update look without major work'},
          {label:'Repair something broken',desc:'Fix a specific problem'},
          {label:'New installation',desc:'Add something that isn\'t there'},
          {label:'Maintenance',desc:'Preventive upkeep'},
          {label:'Not sure yet',desc:'Need professional guidance'}
        ]},
      { q: 'What\'s your timeline?', icon: 'fa-calendar',
        opts: [
          {label:'Urgent — ASAP',desc:'Need it done this week'},
          {label:'Within 2 weeks',desc:'Soon but not emergency'},
          {label:'Within 1–2 months',desc:'Planning ahead'},
          {label:'Just exploring',desc:'Gathering info & pricing'}
        ]},
      { q: 'Do you have a budget range in mind?', icon: 'fa-wallet',
        opts: [
          {label:'Under $500',desc:'Small project'},
          {label:'$500 – $2,000',desc:'Mid-range project'},
          {label:'$2,000 – $5,000',desc:'Significant project'},
          {label:'$5,000+',desc:'Major renovation'},
          {label:'Not sure yet',desc:'Need help estimating'}
        ]}
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
        ]}
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
        el.querySelectorAll('[data-ans]').forEach(function(btn) {
          btn.addEventListener('click', function() {
            answers[step] = btn.dataset.ans;
            step++;
            if (step < questions.length) { render(); }
            else { render(); getRecommendation(); }
          });
        });
        var back = el.querySelector('.wai-back');
        if (back) back.addEventListener('click', function() { step--; render(); });
      }
    }

    function getRecommendation() {
      var svcList = B.services.map(function(s) { return s.label; }).join(', ');
      var prompt = 'You are a senior service advisor for ' + B.name + ', a licensed contractor (NE Reg #54690-25) in Norfolk, Nebraska.\n\n' +
        'Available services: ' + svcList + '.\n\n' +
        'A potential customer completed our needs assessment:\n';
      questions.forEach(function(q, i) {
        prompt += '• ' + q.q + ' → ' + (answers[i] || 'Not answered') + '\n';
      });
      prompt += '\nProvide a professional recommendation with this EXACT structure:\n' +
        '1. Start with "Based on your needs..." and name the #1 recommended service (bold with **)\n' +
        '2. Explain in 2 sentences WHY this service is the best fit for their specific situation\n' +
        '3. If a second service would complement it, mention it briefly\n' +
        '4. Include one specific detail about how ' + B.name + ' handles this type of project\n' +
        '5. End with: "Call (405) 410-6402 to schedule your free consultation"\n\n' +
        'RULES:\n' +
        '- Sound like an experienced, caring contractor — not a chatbot\n' +
        '- Reference their specific answers, don\'t be generic\n' +
        '- Keep total response under 100 words\n' +
        '- Format service names in bold with **\n' +
        '- Do NOT use bullet points or numbered lists';

      callProxy(prompt, 350).then(function(text) {
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
        var result = document.getElementById('wr-result');
        if (result) {
          result.innerHTML = '<h4>Let\'s Talk About Your Project</h4>' +
            '<p>Your situation is unique, and we want to make sure we recommend exactly the right solution. ' +
            'Call us for a <strong>free, no-obligation consultation</strong> — we\'ll assess your needs in person and provide a clear plan.</p>' +
            '<a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> (405) 410-6402 — Free Consultation</a>';
          result.classList.add('show');
        }
        var spinner = el.querySelector('.fa-magnifying-glass-chart');
        if (spinner) spinner.closest('div[style]').style.display = 'none';
      });
    }

    render();
  }

  // ── PROXY CALL ──
  function callProxy(prompt, maxTokens) {
    var body = {
      system_instruction: { parts: [{ text: 'You are a senior professional at ' + B.name + ', a licensed Nebraska contractor. You speak with authority, warmth, and expertise. You never sound like a generic chatbot. You give specific, actionable advice. You always reference the customer\'s specific situation. Price ranges must reflect real Nebraska contractor rates. Always end with the phone number (405) 410-6402.' }] },
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.7, maxOutputTokens: maxTokens || 300, topP: 0.9 },
      safetySettings: [
        { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' }
      ]
    };
    return fetch(PROXY + '?model=' + MODEL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }).then(function(r) {
      if (!r.ok) throw new Error('API error');
      return r.json();
    }).then(function(d) {
      var t = d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts && d.candidates[0].content.parts[0] && d.candidates[0].content.parts[0].text;
      if (!t) throw new Error('No response');
      return t;
    });
  }

  // ── INIT ──
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { buildQuoteCalc(); buildRecommender(); });
  } else {
    buildQuoteCalc(); buildRecommender();
  }
})();
