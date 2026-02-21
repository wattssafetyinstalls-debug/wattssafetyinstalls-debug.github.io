/**
 * Watts AI Public Tools — Embedded on service pages
 * 1. Instant Quote Calculator — visitors pick service + details → ballpark range + CTA
 * 2. Service Recommender — "Not sure what you need?" guided quiz
 * Both use Gemini via Cloudflare Worker proxy for smart responses.
 */
(function () {
  'use strict';

  var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  var MODEL = 'gemini-2.5-flash';
  var isSI = window.location.pathname.startsWith('/safety-installs');

  var B = isSI
    ? { name:'Watts Safety Installs', c:'#dc2626', cd:'#b91c1c', cl:'#fef2f2', bg:'#1a1a1a', tx:'#f5f5dc',
        services:[
          {id:'remodel',label:'Kitchen & Bath Remodeling',icon:'fa-kitchen-set'},
          {id:'paint',label:'Interior & Exterior Painting',icon:'fa-paint-roller'},
          {id:'gutter',label:'Gutter Install & Repair',icon:'fa-droplet'},
          {id:'handy',label:'Handyman Services',icon:'fa-screwdriver-wrench'},
          {id:'tv',label:'Electronics & TV Mounting',icon:'fa-tv'}
        ]}
    : { name:'Watts ATP Contractor', c:'#00C4B4', cd:'#009e91', cl:'#E0F7FA', bg:'#0A1D37', tx:'#FFD700',
        services:[
          {id:'ramp',label:'Wheelchair Ramp Installation',icon:'fa-wheelchair-move'},
          {id:'grab',label:'Grab Bar Installation',icon:'fa-hand-holding-medical'},
          {id:'floor',label:'Non-Slip Flooring',icon:'fa-shoe-prints'},
          {id:'bath',label:'Bathroom Accessibility',icon:'fa-bath'},
          {id:'safety',label:'Accessibility & Safety Solutions',icon:'fa-shield-halved'}
        ]};

  // ── STYLES ──
  var css = document.createElement('style');
  css.textContent = '\
.wai-section{max-width:900px;margin:32px auto;padding:0 20px}\
.wai-card{background:#fff;border-radius:16px;padding:28px 24px;box-shadow:0 4px 20px rgba(0,0,0,.06);margin-bottom:24px}\
.wai-card h2{font-family:"Playfair Display",serif;font-size:1.5rem;color:' + B.bg + ';margin-bottom:6px}\
.wai-card .sub{color:#64748B;font-size:.9rem;margin-bottom:20px}\
.wai-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin-bottom:16px}\
.wai-opt{background:#f8f9fa;border:2px solid #e5e5e5;border-radius:12px;padding:14px 12px;text-align:center;\
cursor:pointer;transition:all .2s;font-size:.85rem;font-weight:500;color:#444}\
.wai-opt:hover{border-color:' + B.c + ';color:' + B.c + ';background:' + B.cl + '}\
.wai-opt.on{border-color:' + B.c + ';background:' + B.cl + ';color:' + B.cd + '}\
.wai-opt i{display:block;font-size:1.4rem;margin-bottom:6px;color:' + B.c + '}\
.wai-input{width:100%;padding:12px 16px;border:1px solid #e5e5e5;border-radius:10px;font-size:.95rem;\
outline:none;transition:border-color .2s;margin-bottom:12px;font-family:inherit}\
.wai-input:focus{border-color:' + B.c + '}\
.wai-btn{display:inline-flex;align-items:center;gap:8px;background:' + B.c + ';color:#fff;border:none;padding:12px 28px;\
border-radius:10px;font-size:.95rem;font-weight:600;cursor:pointer;transition:all .2s}\
.wai-btn:hover{background:' + B.cd + ';transform:translateY(-1px)}\
.wai-btn:disabled{opacity:.5;cursor:default;transform:none}\
.wai-btn i{font-size:.85rem}\
.wai-result{margin-top:16px;padding:20px;background:' + B.cl + ';border-radius:12px;border-left:4px solid ' + B.c + ';\
font-size:.95rem;line-height:1.6;color:#333;display:none}\
.wai-result.show{display:block;animation:waiIn .3s ease}\
.wai-result strong{color:' + B.bg + '}\
.wai-result .cta{display:inline-block;margin-top:12px;background:' + B.c + ';color:#fff;padding:10px 24px;\
border-radius:8px;text-decoration:none;font-weight:600;font-size:.9rem}\
.wai-result .cta:hover{background:' + B.cd + '}\
@keyframes waiIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}\
.wai-quiz-step{display:none}\
.wai-quiz-step.active{display:block}\
.wai-progress{height:4px;background:#e5e5e5;border-radius:2px;margin-bottom:16px;overflow:hidden}\
.wai-progress-bar{height:100%;background:' + B.c + ';border-radius:2px;transition:width .3s ease}\
@media(max-width:600px){.wai-grid{grid-template-columns:repeat(2,1fr)}.wai-card{padding:20px 16px}}\
';
  document.head.appendChild(css);

  // ── QUOTE CALCULATOR ──
  function buildQuoteCalc() {
    var el = document.getElementById('watts-quote-calc');
    if (!el) return;

    var svcBtns = B.services.map(function(s) {
      return '<div class="wai-opt" data-svc="' + s.id + '"><i class="fas ' + s.icon + '"></i>' + s.label + '</div>';
    }).join('');

    el.innerHTML = '\
<div class="wai-card">\
<h2><i class="fas fa-calculator" style="color:' + B.c + ';margin-right:10px"></i>Instant Estimate Calculator</h2>\
<p class="sub">Get a ballpark range in seconds — no commitment, no pressure.</p>\
<div class="wai-grid" id="wq-svcs">' + svcBtns + '</div>\
<textarea class="wai-input" id="wq-details" rows="3" placeholder="Tell us a bit about your project (e.g., size of room, what needs done, any special requirements)..."></textarea>\
<button class="wai-btn" id="wq-go" disabled><i class="fas fa-bolt"></i>Get My Estimate</button>\
<div class="wai-result" id="wq-result"></div>\
</div>';

    var selected = null;
    var svcs = el.querySelectorAll('.wai-opt');
    var goBtn = document.getElementById('wq-go');
    var details = document.getElementById('wq-details');
    var result = document.getElementById('wq-result');

    svcs.forEach(function(btn) {
      btn.addEventListener('click', function() {
        svcs.forEach(function(b) { b.classList.remove('on'); });
        btn.classList.add('on');
        selected = btn.dataset.svc;
        goBtn.disabled = false;
      });
    });

    goBtn.addEventListener('click', function() {
      if (!selected) return;
      var svcLabel = '';
      B.services.forEach(function(s) { if (s.id === selected) svcLabel = s.label; });
      var desc = details.value.trim();
      var prompt = 'You are a helpful estimator for ' + B.name + ' in Norfolk, Nebraska. ' +
        'A visitor wants a ballpark estimate for: ' + svcLabel + '. ' +
        (desc ? 'Project details: ' + desc + '. ' : '') +
        'Give a realistic price RANGE (e.g., "$800 - $2,500") based on typical Nebraska pricing. ' +
        'Keep it to 3-4 sentences. Mention that exact pricing requires a free on-site estimate. ' +
        'End with encouraging them to call (405) 410-6402 for their free estimate. ' +
        'Format the price range in bold. Be warm and helpful.';

      goBtn.disabled = true;
      goBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>Calculating...';
      result.classList.remove('show');

      callProxy(prompt).then(function(text) {
        result.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>') +
          '<br><a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> Call for Free Estimate</a>';
        result.classList.add('show');
      }).catch(function() {
        result.innerHTML = 'Every project is unique! Call us at <strong>(405) 410-6402</strong> for a free, no-obligation estimate.' +
          '<br><a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> Call Now</a>';
        result.classList.add('show');
      }).finally(function() {
        goBtn.disabled = false;
        goBtn.innerHTML = '<i class="fas fa-bolt"></i>Get My Estimate';
      });
    });
  }

  // ── SERVICE RECOMMENDER ──
  function buildRecommender() {
    var el = document.getElementById('watts-recommender');
    if (!el) return;

    var questions = isSI ? [
      { q: 'What area of your home needs work?', opts: ['Kitchen','Bathroom','Exterior','Living areas','Multiple rooms'] },
      { q: 'What kind of work are you looking for?', opts: ['Full remodel','Cosmetic update','Repair / fix','New installation','Not sure yet'] },
      { q: 'How soon do you need this done?', opts: ['ASAP','Within a month','Within 3 months','Just planning ahead'] }
    ] : [
      { q: 'Who is this modification for?', opts: ['Aging parent','Myself','Spouse / partner','Family member','Planning ahead'] },
      { q: 'What area needs modification?', opts: ['Bathroom','Entrance / doorway','Stairs','Flooring','Multiple areas'] },
      { q: 'What is the main concern?', opts: ['Fall prevention','Wheelchair access','General mobility','ADA compliance','Not sure yet'] }
    ];

    var answers = [];
    var step = 0;

    function render() {
      var pct = Math.round(((step) / questions.length) * 100);
      var html = '<div class="wai-card">\
<h2><i class="fas fa-compass" style="color:' + B.c + ';margin-right:10px"></i>Not Sure What You Need?</h2>\
<p class="sub">Answer 3 quick questions and we\'ll recommend the right service for you.</p>\
<div class="wai-progress"><div class="wai-progress-bar" style="width:' + pct + '%"></div></div>';

      if (step < questions.length) {
        var q = questions[step];
        html += '<p style="font-weight:600;margin-bottom:12px;color:' + B.bg + '">' + q.q + '</p>\
<div class="wai-grid" id="wr-opts">';
        q.opts.forEach(function(o) {
          html += '<div class="wai-opt" data-ans="' + o + '">' + o + '</div>';
        });
        html += '</div>';
      } else {
        html += '<div style="text-align:center;padding:16px 0">\
<i class="fas fa-spinner fa-spin" style="font-size:1.5rem;color:' + B.c + '"></i>\
<p style="margin-top:8px;color:#64748B">Finding your perfect service...</p></div>';
      }

      html += '<div class="wai-result" id="wr-result"></div></div>';
      el.innerHTML = html;

      if (step < questions.length) {
        el.querySelectorAll('.wai-opt').forEach(function(btn) {
          btn.addEventListener('click', function() {
            answers.push(btn.dataset.ans);
            step++;
            if (step < questions.length) {
              render();
            } else {
              render();
              getRecommendation();
            }
          });
        });
      }
    }

    function getRecommendation() {
      var svcList = B.services.map(function(s) { return s.label; }).join(', ');
      var prompt = 'You are a service recommender for ' + B.name + ' in Norfolk, Nebraska. ' +
        'Available services: ' + svcList + '. ' +
        'A visitor answered these questions: ';
      questions.forEach(function(q, i) {
        prompt += q.q + ' → ' + answers[i] + '. ';
      });
      prompt += 'Recommend the 1-2 best services for them. Keep it to 3-4 sentences. ' +
        'Be warm and specific about why those services fit. ' +
        'End with encouraging them to call (405) 410-6402 for a free consultation. Format service names in bold.';

      callProxy(prompt).then(function(text) {
        var result = document.getElementById('wr-result');
        if (result) {
          result.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>') +
            '<br><a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> Get Free Consultation</a>';
          result.classList.add('show');
        }
        // Remove spinner
        var spinner = el.querySelector('.fa-spinner');
        if (spinner) spinner.parentElement.parentElement.style.display = 'none';
      }).catch(function() {
        var result = document.getElementById('wr-result');
        if (result) {
          result.innerHTML = 'Based on your answers, we\'d love to discuss the best options for you! Call <strong>(405) 410-6402</strong> for a free consultation.' +
            '<br><a class="cta" href="tel:+14054106402"><i class="fas fa-phone"></i> Call Now</a>';
          result.classList.add('show');
        }
      });
    }

    render();
  }

  // ── PROXY CALL ──
  function callProxy(prompt) {
    var body = {
      system_instruction: { parts: [{ text: 'You are a helpful assistant for ' + B.name + '. Keep responses concise (3-4 sentences). Be warm and professional. Never give exact prices, only ranges. Always mention free estimates and the phone number (405) 410-6402.' }] },
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.7, maxOutputTokens: 200, topP: 0.9 },
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
