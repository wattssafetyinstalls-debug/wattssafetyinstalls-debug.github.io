/**
 * Watts AI Chat Widget v2 — Compact, Mobile-First
 * Tiny pill trigger, clean window, brand-aware, lead capture.
 */
(function () {
  'use strict';

  var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  var MODEL = 'gemini-2.5-flash';

  var isSI = window.location.pathname.startsWith('/safety-installs');
  var B = isSI
    ? { name:'Watts Safety Installs', short:'Safety Installs',
        svc:'kitchen & bath remodeling, painting, gutters, handyman, electronics, property maintenance, snow removal, lawn care',
        c:'#dc2626', cd:'#b91c1c', cl:'#fef2f2',
        hdr:'linear-gradient(135deg,#1a1a1a,#2d2d2d)', ht:'#f5f5dc', mb:'#faf9f6' }
    : { name:'Watts ATP Contractor', short:'ATP Contractor',
        svc:'wheelchair ramp installation, grab bar installation, non-slip flooring, bathroom accessibility, ADA-compliant safety solutions',
        c:'#00C4B4', cd:'#009e91', cl:'#E0F7FA',
        hdr:'linear-gradient(135deg,#0A1D37,#16213e)', ht:'#FFD700', mb:'#f8f9fa' };

  var SYS = 'You are Justin Watts, the owner of ' + B.name + ' in Norfolk, Nebraska. You\'re a real person — a hands-on contractor who personally shows up to every job. You\'re friendly, confident, and genuinely care about helping people.\n\n' +
    'BUSINESS INFO:\n' +
    '- Phone: (405) 410-6402 | Email: Justin.Watts@WattsATPContractor.com\n' +
    '- Address: 507 West Omaha Ave Suite B, Norfolk NE 68701\n' +
    '- License: Nebraska #54690-25 | Fully insured\n' +
    '- Service area: 100-mile radius of Norfolk NE (Norfolk, Columbus, Fremont, Wayne, Madison, West Point, O\'Neill, South Sioux City, and everywhere in between)\n' +
    '- Rating: 5.0 stars (12 Google reviews)\n' +
    '- Services: ' + B.svc + '\n\n' +
    'YOUR PERSONALITY:\n' +
    '- Talk like a real Nebraska contractor, not a corporate chatbot. Use casual language.\n' +
    '- Share quick stories or examples: "Just finished a grab bar job in Columbus last week — the homeowner was thrilled."\n' +
    '- Show expertise by mentioning specifics: ADA slope requirements, material brands, common problems you solve.\n' +
    '- Use humor occasionally — you\'re approachable and down-to-earth.\n' +
    '- If someone seems hesitant, reassure them: "No pressure at all — the estimate is 100% free and I can usually get out there within a day or two."\n' +
    '- Mirror the visitor\'s energy — if they\'re urgent, be responsive. If they\'re browsing, be relaxed.\n\n' +
    'CONVERSATION STRATEGY:\n' +
    '1. FIRST MESSAGE: Answer their question helpfully. Build rapport.\n' +
    '2. SECOND MESSAGE: Naturally ask about their specific situation. "Is this for yourself or a family member?"\n' +
    '3. THIRD MESSAGE: Suggest a free estimate and ask for their name. "I\'d love to take a look — what\'s your name so I can get you on my schedule?"\n' +
    '4. AFTER NAME: Ask for phone number. "What\'s the best number to reach you at? I\'ll give you a call to set up a time."\n' +
    '5. AFTER PHONE: Confirm and close warm. "Perfect, [name]! I\'ll give you a call [today/tomorrow]. Looking forward to helping you out."\n\n' +
    'SMART RESPONSES:\n' +
    '- Pricing questions: "Every job is different, but I can tell you [service] typically runs between $X-$Y depending on the specifics. The best way to get an exact number is a free on-site estimate — takes about 15 minutes."\n' +
    '- Price ranges to reference (NEVER give exact quotes): Grab bars $150-400, Wheelchair ramps $1,500-8,000, Bathroom mods $2,000-15,000, Non-slip flooring $500-3,000\n' +
    '- Timeline questions: "Most jobs I can start within 1-2 weeks of the estimate. Smaller jobs like grab bars I can sometimes do same-week."\n' +
    '- Insurance/ATP questions: "Yes, I work directly with ATP (Assistive Technology Partnership) and can handle all the paperwork. I\'m one of the few approved contractors in the area."\n' +
    '- Competitor comparisons: Never badmouth competitors. Say "I can\'t speak for others, but here\'s what you get with me: licensed, insured, 5-star rated, and I personally do the work — no subcontractors."\n\n' +
    'RULES:\n' +
    '- Keep replies to 2-4 sentences. Be concise but warm.\n' +
    '- ALWAYS try to move toward capturing name + phone + project type.\n' +
    '- If they give a name, USE IT in your replies.\n' +
    '- Respond in the visitor\'s language (Spanish, etc).\n' +
    '- Never say "I\'m an AI" or "I\'m a chatbot." You ARE Justin.\n' +
    '- If asked something you don\'t know, say "That\'s a great question — let me look into that and get back to you. What\'s the best number to reach you?"\n' +
    '- BOOKING: If someone wants to schedule, say "You can book a time right on our website — just head to our contact page and pick a slot that works for you: https://wattsatpcontractor.com/contact.html#cal-embed Or I can take your info and call you to set it up!"';

  var hist = [], open = false, busy = false;
  var lead = { name:null, phone:null };

  // ── STYLES ──
  var s = document.createElement('style');
  s.textContent = '\
#wc *{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}\
#wc-trig{position:fixed;bottom:16px;right:16px;z-index:99999;display:flex;align-items:center;gap:8px;\
background:' + B.c + ';color:#fff;border:none;cursor:pointer;padding:10px 16px;border-radius:28px;\
font-size:13px;font-weight:600;box-shadow:0 2px 12px rgba(0,0,0,.18);transition:all .25s ease}\
#wc-trig:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(0,0,0,.22)}\
#wc-trig:active{transform:scale(.97)}\
#wc-trig svg{width:18px;height:18px;flex-shrink:0}\
#wc-trig .lb{white-space:nowrap}\
#wc-dot{position:absolute;top:-3px;right:-3px;width:14px;height:14px;border-radius:50%;background:#ef4444;border:2px solid #fff;display:none}\
#wc-trig.has-dot #wc-dot{display:block}\
#wc-win{position:fixed;bottom:64px;right:16px;z-index:99998;width:340px;max-width:calc(100vw - 24px);\
height:440px;max-height:calc(100vh - 80px);background:#fff;border-radius:16px;display:none;flex-direction:column;\
box-shadow:0 8px 40px rgba(0,0,0,.15);overflow:hidden;animation:wcUp .25s ease}\
#wc-win.on{display:flex}\
@keyframes wcUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}\
#wc-hdr{background:' + B.hdr + ';padding:14px 16px;display:flex;align-items:center;gap:10px}\
#wc-hdr .av{width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.15);display:flex;\
align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#fff;flex-shrink:0;\
border:1.5px solid rgba(255,255,255,.25)}\
#wc-hdr .nm{color:' + B.ht + ';font-size:14px;font-weight:600}\
#wc-hdr .st{color:rgba(255,255,255,.7);font-size:11px;display:flex;align-items:center;gap:4px}\
#wc-hdr .st::before{content:"";width:6px;height:6px;border-radius:50%;background:#22c55e;display:inline-block}\
#wc-x{margin-left:auto;background:none;border:none;cursor:pointer;color:rgba(255,255,255,.6);padding:4px;\
border-radius:6px;display:flex;align-items:center;justify-content:center;transition:color .2s}\
#wc-x:hover{color:#fff}\
#wc-x svg{width:16px;height:16px}\
#wc-msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;background:' + B.mb + '}\
#wc-msgs::-webkit-scrollbar{width:4px}\
#wc-msgs::-webkit-scrollbar-thumb{background:rgba(0,0,0,.1);border-radius:2px}\
.wm{max-width:82%;padding:10px 14px;border-radius:16px;font-size:13px;line-height:1.5;word-wrap:break-word;animation:wmI .2s ease}\
@keyframes wmI{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}\
.wm.b{background:#fff;color:#333;align-self:flex-start;border-bottom-left-radius:4px;box-shadow:0 1px 4px rgba(0,0,0,.06)}\
.wm.u{background:' + B.c + ';color:#fff;align-self:flex-end;border-bottom-right-radius:4px}\
.wm a{color:' + B.c + ';font-weight:500}\
.wm-t{align-self:flex-start;display:flex;gap:3px;padding:10px 14px;background:#fff;border-radius:16px;\
border-bottom-left-radius:4px;box-shadow:0 1px 4px rgba(0,0,0,.06)}\
.wm-t i{width:6px;height:6px;border-radius:50%;background:' + B.c + ';opacity:.4;animation:wd 1s infinite;font-style:normal}\
.wm-t i:nth-child(2){animation-delay:.15s}\
.wm-t i:nth-child(3){animation-delay:.3s}\
@keyframes wd{0%,80%{transform:translateY(0);opacity:.4}40%{transform:translateY(-5px);opacity:1}}\
#wc-qr{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 10px;background:' + B.mb + '}\
.qr{background:#fff;border:1px solid #e5e5e5;color:#555;padding:6px 12px;border-radius:16px;\
font-size:12px;cursor:pointer;transition:all .15s;font-weight:500}\
.qr:hover{border-color:' + B.c + ';color:' + B.c + ';background:' + B.cl + '}\
#wc-cta{background:' + B.c + ';padding:8px;text-align:center;font-size:12px;color:#fff;font-weight:600;\
cursor:pointer;transition:opacity .2s}\
#wc-cta:hover{opacity:.9}\
#wc-bar{padding:10px 12px;border-top:1px solid #eee;display:flex;gap:8px;align-items:center;background:#fff}\
#wc-inp{flex:1;background:#f5f5f5;border:1px solid #e5e5e5;border-radius:20px;padding:9px 14px;\
color:#333;font-size:14px;outline:none;transition:border-color .2s}\
#wc-inp:focus{border-color:' + B.c + ';background:#fff}\
#wc-inp::placeholder{color:#aaa}\
#wc-snd{width:34px;height:34px;border-radius:50%;background:' + B.c + ';border:none;cursor:pointer;\
display:flex;align-items:center;justify-content:center;transition:all .15s;flex-shrink:0}\
#wc-snd:hover{opacity:.9;transform:scale(1.05)}\
#wc-snd:disabled{opacity:.35;cursor:default;transform:none}\
#wc-snd svg{width:16px;height:16px;fill:#fff}\
@media(max-width:600px){\
#wc-win{width:100%;max-width:100%;right:0;bottom:0;height:80vh;max-height:80vh;border-radius:16px 16px 0 0}\
#wc-trig{bottom:12px;right:12px;padding:8px 14px;font-size:12px}\
#wc-inp{font-size:16px}\
}';
  document.head.appendChild(s);

  // ── DOM ──
  var w = document.createElement('div');
  w.id = 'wc';
  w.innerHTML = '\
<button id="wc-trig" aria-label="Chat with Justin">\
<span id="wc-dot"></span>\
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>\
<span class="lb">Chat with Justin</span>\
</button>\
<div id="wc-win">\
<div id="wc-hdr">\
<div class="av">J</div>\
<div><div class="nm">Justin</div><div class="st">Online now</div></div>\
<button id="wc-x" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>\
</div>\
<div id="wc-msgs"></div>\
<div id="wc-qr">\
<button class="qr" data-m="I need a free estimate">Free Estimate</button>\
<button class="qr" data-m="How much does this cost?">Pricing</button>\
<button class="qr" data-m="How soon can you start?">Timeline</button>\
<button class="qr" data-m="What areas do you serve?">Service Area</button>\
</div>\
<div id="wc-cta" onclick="window.location.href=\'tel:+14054106402\'">Call (405) 410-6402 — Free Estimate</div>\
<div id="wc-bar">\
<input id="wc-inp" type="text" placeholder="Type a message..." autocomplete="off"/>\
<button id="wc-snd" aria-label="Send"><svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg></button>\
</div>\
</div>';
  document.body.appendChild(w);

  var trig = document.getElementById('wc-trig');
  var win  = document.getElementById('wc-win');
  var msgs = document.getElementById('wc-msgs');
  var inp  = document.getElementById('wc-inp');
  var snd  = document.getElementById('wc-snd');
  var qr   = document.getElementById('wc-qr');

  function doOpen()  { open=true;  win.classList.add('on'); trig.classList.remove('has-dot'); trig.style.display='none'; if(!hist.length) greet(); setTimeout(function(){inp.focus()},200); }
  function doClose() { open=false; win.classList.remove('on'); trig.style.display=''; }

  function addMsg(txt, who) {
    var d = document.createElement('div');
    d.className = 'wm ' + who;
    d.innerHTML = txt.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/\n/g,'<br>').replace(/\((\d{3})\)\s?(\d{3})-(\d{4})/g,'<a href="tel:+1$1$2$3">($1) $2-$3</a>');
    msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight;
  }

  function typing(on) {
    var el = document.getElementById('wc-typ');
    if (!on && el) { el.remove(); return; }
    if (on && !el) {
      var d = document.createElement('div'); d.className='wm-t'; d.id='wc-typ';
      d.innerHTML='<i></i><i></i><i></i>'; msgs.appendChild(d); msgs.scrollTop=msgs.scrollHeight;
    }
  }

  function greet() {
    typing(true);
    setTimeout(function() {
      typing(false);
      var pg = window.location.pathname.toLowerCase();
      var g;
      if (pg.indexOf('grab-bar') !== -1) {
        g = 'Hey there! I\'m Justin — I\'ve installed hundreds of grab bars across NE Nebraska. Bathroom, shower, hallway — you name it. What are you looking to get done? I can give you a **free estimate** this week.';
      } else if (pg.indexOf('wheelchair-ramp') !== -1) {
        g = 'Hey! I\'m Justin — wheelchair ramps are one of my specialties. ADA-compliant, built to last, and I handle all the permits. What\'s the situation? I\'d love to come take a look for **free**.';
      } else if (pg.indexOf('bathroom') !== -1) {
        g = 'Hey! I\'m Justin — I do a lot of bathroom accessibility work. Walk-in showers, grab bars, raised toilets, the whole nine yards. What are you thinking about? **Free estimates** always.';
      } else if (pg.indexOf('non-slip') !== -1) {
        g = 'Hey! Justin here — non-slip flooring is a game-changer for safety. I\'ve done kitchens, bathrooms, entryways, you name it. What area are you looking at? I can come measure for **free**.';
      } else if (pg.indexOf('service-area') !== -1) {
        g = 'Hey! I\'m Justin — I cover a 100-mile radius from Norfolk. Columbus, Fremont, Wayne, South Sioux City, and everywhere in between. Where are you located? I\'ll let you know if I can get out there.';
      } else if (pg.indexOf('contact') !== -1) {
        g = 'Hey! I\'m Justin — glad you\'re reaching out. You can fill out the form or just tell me what you need right here and I\'ll get you taken care of. What\'s going on?';
      } else if (isSI) {
        g = 'Hey, I\'m Justin! I handle remodeling, painting, gutters, handyman work, and more across Northeast Nebraska. What can I help you with? **Free estimates** — always.';
      } else {
        g = 'Hey, I\'m Justin! I specialize in wheelchair ramps, grab bars, and accessibility modifications across NE Nebraska. What brings you here today? **Free estimates** — no pressure.';
      }
      addMsg(g,'b');
      hist.push({role:'model',parts:[{text:g}]});
    }, 600);
  }

  function send(text) {
    if (!text.trim()||busy) return;
    addMsg(text,'u'); qr.style.display='none'; inp.value='';
    busy=true; snd.disabled=true;
    hist.push({role:'user',parts:[{text:text}]});
    getLead(text);
    typing(true);

    callAI(hist).then(function(reply) {
      typing(false); addMsg(reply,'b');
      hist.push({role:'model',parts:[{text:reply}]});
      getLead(reply);
      if (lead.name && lead.phone) saveLead();
      busy=false; snd.disabled=false; inp.focus();
    }).catch(function() {
      typing(false);
      addMsg("I'm having trouble connecting. Call us at **(405) 410-6402** — happy to help!",'b');
      busy=false; snd.disabled=false; inp.focus();
    });
  }

  function callAI(h) {
    var body = {
      system_instruction:{parts:[{text:SYS}]},
      contents:h,
      generationConfig:{temperature:.8,maxOutputTokens:300,topP:.9},
      safetySettings:[
        {category:'HARM_CATEGORY_HARASSMENT',threshold:'BLOCK_ONLY_HIGH'},
        {category:'HARM_CATEGORY_HATE_SPEECH',threshold:'BLOCK_ONLY_HIGH'},
        {category:'HARM_CATEGORY_SEXUALLY_EXPLICIT',threshold:'BLOCK_ONLY_HIGH'},
        {category:'HARM_CATEGORY_DANGEROUS_CONTENT',threshold:'BLOCK_ONLY_HIGH'}
      ]
    };
    return fetch(PROXY+'?model='+MODEL,{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(body)
    }).then(function(r) {
      if (!r.ok) throw new Error('API error');
      return r.json();
    }).then(function(d) {
      var t = d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts && d.candidates[0].content.parts[0] && d.candidates[0].content.parts[0].text;
      return t || "I'd love to help — call us at **(405) 410-6402**!";
    });
  }

  function getLead(t) {
    var ph = t.match(/(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})/);
    if (ph) lead.phone=ph[1];
    var nm = t.match(/(?:my name is|i'm|i am|this is|name:?|call me|it's|hey i'm|hey im)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)/i);
    if (nm) lead.name=nm[1];
    var em = t.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/);
    if (em) lead.email=em[0];
  }

  function saveLead() {
    try {
      var ls = JSON.parse(localStorage.getItem('watts-ai-leads')||'[]');
      var e = {name:lead.name,phone:lead.phone,brand:B.name,page:location.pathname,ts:new Date().toISOString()};
      var dup = false;
      for (var i=0;i<ls.length;i++) { if(ls[i].phone===e.phone&&ls[i].name===e.name){dup=true;break;} }
      if (!dup) { ls.push(e); localStorage.setItem('watts-ai-leads',JSON.stringify(ls)); }
    } catch(x) {}
  }

  // ── EVENTS ──
  trig.addEventListener('click', function(){ open ? doClose() : doOpen(); });
  document.getElementById('wc-x').addEventListener('click', doClose);
  snd.addEventListener('click', function(){ send(inp.value); });
  inp.addEventListener('keydown', function(e){ if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send(inp.value);} });
  qr.addEventListener('click', function(e){ var b=e.target.closest('.qr'); if(b) send(b.dataset.m); });

  // Nudge after 8s
  setTimeout(function(){ if(!open&&!hist.length) trig.classList.add('has-dot'); }, 8000);

  // Save session on unload
  window.addEventListener('beforeunload', function(){
    if(hist.length>1) {
      try {
        var ss=JSON.parse(localStorage.getItem('watts-ai-sessions')||'[]');
        ss.push({brand:B.name,page:location.pathname,ts:new Date().toISOString(),msgs:hist.length,lead:lead});
        localStorage.setItem('watts-ai-sessions',JSON.stringify(ss));
      } catch(x) {}
    }
  });
})();
