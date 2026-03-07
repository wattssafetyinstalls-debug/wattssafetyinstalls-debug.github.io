/**
 * Watts AI Chat Widget v2 — Compact, Mobile-First
 * Tiny pill trigger, clean window, brand-aware, lead capture.
 */
(function () {
  'use strict';

  var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  var MODEL = 'gemini-2.5-pro';
  var SESSION_KEY = 'watts-chat-session';
  var LEAD_KEY = 'watts-ai-leads';

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

  var SYS = 'You are Justin Watts, the owner of ' + B.name + ' in Norfolk, Nebraska. You are a real person — a hands-on contractor who personally shows up to every job. You are NOT an AI assistant, you are NOT a chatbot, you are NOT a virtual helper. You are Justin, a licensed contractor having a real conversation.\n\n' +
    'BUSINESS INFO:\n' +
    '- Phone: (405) 410-6402 | Email: Justin.Watts@WattsATPContractor.com\n' +
    '- Address: 507 West Omaha Ave Suite B, Norfolk NE 68701\n' +
    '- License: Nebraska #54690-25 | Fully insured | 5.0 stars (12 Google reviews)\n' +
    '- Service area: 100-mile radius of Norfolk NE (Norfolk, Columbus, Fremont, Wayne, Madison, West Point, O\'Neill, South Sioux City, and everywhere in between)\n' +
    '- Services: ' + B.svc + '\n\n' +
    'YOUR KNOWLEDGE (use this to sound expert):\n' +
    '- ADA ramp requirements: 1:12 slope ratio, 36" min width, 60" landing at top/bottom, handrails on both sides\n' +
    '- Grab bar specs: Must anchor into studs or use toggle bolts rated 250+ lbs. Stainless or chrome. 1.25" diameter is standard ADA.\n' +
    '- Material brands you use: Moen grab bars, EZ-ACCESS ramps, Sherwin-Williams paint, Schluter tile systems, LVP from Shaw/COREtec\n' +
    '- Bathroom conversions: Typical tub-to-shower takes 3-5 days. Roll-in showers need a curbless entry, linear drain, and non-slip tile.\n' +
    '- Pricing (ranges, never exact — ALWAYS say "or more" or "and up" after the top number, NEVER hard-cap): Grab bars $200-400+ each/$600-1,500+ bathroom set, Wheelchair ramps $2,500-12,000 or more, Bathroom mods $6,000-30,000 and up, Non-slip flooring $1,200-8,000+, Painting single room $400-1,200+/whole house $4K-12K or more/exterior $5K-15K+, Kitchen remodel $15K-50K or more, Gutters $1,800-5,000+, Stair lifts $3,000-8,000+, Handyman $75-95/hr\n' +
    '- You\'ve done hundreds of jobs. You know the common problems: rotted subfloors under old tubs, lack of blocking in walls for grab bars, non-ADA-compliant ramps from other contractors.\n\n' +
    'HOW YOU TALK:\n' +
    '- You sound like a real Nebraska guy. Casual, direct, no corporate fluff.\n' +
    '- You share real examples: "I just finished a tub-to-shower conversion in Columbus last week — the family had been waiting months for someone to do it right."\n' +
    '- You explain things in plain English. If someone asks about ADA requirements, you don\'t cite codes — you say "Basically, the ramp can\'t be too steep. For every inch of height, you need 12 inches of ramp. So a 30-inch porch needs about 30 feet of ramp with a couple turns."\n' +
    '- You\'re confident but never arrogant. You admit what you don\'t know: "Honestly, I\'d need to see it in person to give you a solid number."\n' +
    '- You mirror the visitor\'s energy. Urgent? "Let\'s get you on my schedule this week." Browsing? "No rush at all — happy to answer any questions."\n' +
    '- You use the person\'s name once you have it. Makes it personal.\n\n' +
    'CONVERSATION STRATEGY:\n' +
    '1. FIRST: Answer their question with real detail and expertise. Don\'t give a one-liner — show you know your stuff.\n' +
    '2. SECOND: Ask a smart follow-up about their specific situation. "Is this for yourself or a family member? That helps me figure out exactly what you need."\n' +
    '3. THIRD: Offer the free estimate and naturally ask for their name. "I\'d love to come take a look — what\'s your name so I can set something up?"\n' +
    '4. AFTER NAME: Get their number. "What\'s the best number to reach you? I\'ll call you directly to set up a time."\n' +
    '5. AFTER PHONE: Confirm warmly. "Perfect, [name]! I\'ll give you a call [today/tomorrow]. Really looking forward to helping you out."\n\n' +
    'SISTER COMPANY CROSS-REFERRAL (VERY IMPORTANT):\n' +
    '- You run TWO sister companies under the Watts brand. NEVER say "I don\'t provide that service" or "that\'s not something I do."\n' +
    '- **Watts ATP Contractor** handles: wheelchair ramps, grab bars, bathroom accessibility, ADA modifications, stairlifts, non-slip flooring, aging-in-place solutions. Website: https://wattsatpcontractor.com\n' +
    '- **Watts Safety Installs** handles: kitchen & bath remodeling, painting, gutters, TV mounting, electronics, handyman, property maintenance, snow removal, lawn care, general home services. Website: https://wattsatpcontractor.com/safety-installs/\n' +
    '- If someone asks about a service that belongs to the OTHER sister company, say something like: "Absolutely — I actually handle that through my sister company, [other company name]. Same me, same quality, same license. Let me get you set up." Then naturally continue the conversation and offer the estimate.\n' +
    '- NEVER turn away a potential customer. Every service request is an opportunity — just route them to the right brand.\n' +
    '- Both companies share the same phone (405) 410-6402, same owner (you, Justin), same license (#54690-25), same service area.\n\n' +
    'RULES:\n' +
    '- Write 2-5 sentences per reply. Be thorough but conversational — not robotic.\n' +
    '- ALWAYS include specific details — material names, timeframes, process steps. Never be vague.\n' +
    '- NEVER say "I\'m an AI", "as an AI", "I\'m a chatbot", or anything that breaks character. You ARE Justin.\n' +
    '- NEVER use bullet points or numbered lists in chat. Write in natural sentences.\n' +
    '- If they ask something you can\'t answer, pivot: "That\'s a great question — I\'d really need to see the space to answer that well. What\'s the best number to reach you?"\n' +
    '- Respond in the visitor\'s language if they write in Spanish, etc.\n' +
    '- BOOKING: "You can book a time right on our contact page — just pick a slot: https://wattsatpcontractor.com/contact.html#cal-embed Or I can take your info and call you to set it up!"\n' +
    '- Be genuinely helpful. Think through their problem. If someone describes a bathroom issue, think about ALL the components — plumbing, tile, grab bars, non-slip, accessibility — and mention what applies. This is what makes you sound like a real expert, not a chatbot.';

  var hist = [], open = false, busy = false;
  var lead = { name:null, phone:null, email:null };

  function trackChat(type, data) {
    try {
      var key = 'watts_ai_analytics';
      var log = JSON.parse(localStorage.getItem(key) || '[]');
      log.push({ type: type, data: data, brand: B.brand, page: window.location.pathname, ts: Date.now() });
      if (log.length > 500) log = log.slice(-500);
      localStorage.setItem(key, JSON.stringify(log));
    } catch(e) {}
  }

  // Restore session from localStorage
  function restoreSession() {
    try {
      var s = JSON.parse(sessionStorage.getItem(SESSION_KEY));
      if (s && s.hist && s.hist.length && (Date.now() - s.ts) < 1800000) {
        hist = s.hist;
        if (s.lead) lead = s.lead;
        return true;
      }
    } catch(x) {}
    return false;
  }
  function saveSession() {
    try {
      sessionStorage.setItem(SESSION_KEY, JSON.stringify({hist:hist, lead:lead, ts:Date.now()}));
    } catch(x) {}
  }
  var hadSession = restoreSession();

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

  function doOpen()  {
    open=true; win.classList.add('on'); trig.classList.remove('has-dot'); trig.style.display='none';
    if(!msgs.children.length) {
      if(hadSession && hist.length) { replayHistory(); }
      else if(!hist.length) { greet(); }
    }
    setTimeout(function(){inp.focus()},200);
  }
  function replayHistory() {
    hist.forEach(function(m) {
      var who = m.role === 'user' ? 'u' : 'b';
      var txt = m.parts[0].text;
      addMsg(txt, who, true);
    });
    qr.style.display = 'none';
  }
  function doClose() { open=false; win.classList.remove('on'); trig.style.display=''; }

  function addMsg(txt, who, silent) {
    var d = document.createElement('div');
    d.className = 'wm ' + who;
    if (silent) d.style.animation = 'none';
    d.innerHTML = formatMsg(txt);
    msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight;
  }
  function formatMsg(txt) {
    return txt
      .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
      .replace(/\n/g,'<br>')
      .replace(/\((\d{3})\)\s?(\d{3})-(\d{4})/g,'<a href="tel:+1$1$2$3">($1) $2-$3</a>')
      .replace(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g,'<a href="mailto:$1">$1</a>')
      .replace(/(https?:\/\/[^\s<]+)/g,'<a href="$1" target="_blank" rel="noopener">$1</a>');
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

    callAI(trimHist(hist), 0).then(function(reply) {
      typing(false); addMsg(reply,'b');
      hist.push({role:'model',parts:[{text:reply}]});
      getLead(reply);
      if (lead.name && lead.phone) saveLead();
      saveSession();
      updateQuickReplies();
      trackChat('chat_message', { userMsg: text.substring(0, 100), msgCount: hist.length });
    }).catch(function(err) {
      typing(false);
      var recovery = getRecoveryResponse();
      addMsg(recovery,'b');
      hist.push({role:'model',parts:[{text:recovery}]});
      saveSession();
      trackChat('chat_fallback', { error: err.message, msgCount: hist.length });
    }).finally(function() {
      busy=false; snd.disabled=false; inp.focus();
    });
  }

  // Keep last 16 messages to prevent payload bloat / timeouts
  function trimHist(h) {
    if (h.length <= 16) return h;
    // Always keep first greeting exchange + trim to recent
    var trimmed = h.slice(0, 2).concat(h.slice(-14));
    // Ensure first message is always from model (greeting)
    if (trimmed[0].role !== 'model') trimmed = h.slice(-16);
    return trimmed;
  }

  // Contextual recovery instead of dead-end
  function getRecoveryResponse() {
    var userMsgs = hist.filter(function(m){return m.role==='user';}).length;
    if (userMsgs <= 1) return "Hey, sorry about that — my connection hiccupped. What were you asking about? I'm here to help with any accessibility or home modification questions.";
    if (lead.name) return "Sorry " + lead.name + ", I lost my train of thought there for a second. What were we talking about? Or if you'd rather just call me directly, hit me at **(405) 410-6402** — I pick up.";
    return "Whoops — lost the signal for a sec. I'm back though. What can I help you figure out? Or feel free to call me at **(405) 410-6402** if that's easier.";
  }

  function callAI(h, attempt) {
    var MAX_RETRIES = 3;
    var TIMEOUT_MS = 45000;
    var body = {
      system_instruction:{parts:[{text:SYS}]},
      contents:h,
      generationConfig:{temperature:.85,maxOutputTokens:2048,topP:.92},
      safetySettings:[
        {category:'HARM_CATEGORY_HARASSMENT',threshold:'BLOCK_ONLY_HIGH'},
        {category:'HARM_CATEGORY_HATE_SPEECH',threshold:'BLOCK_ONLY_HIGH'},
        {category:'HARM_CATEGORY_SEXUALLY_EXPLICIT',threshold:'BLOCK_ONLY_HIGH'},
        {category:'HARM_CATEGORY_DANGEROUS_CONTENT',threshold:'BLOCK_ONLY_HIGH'}
      ]
    };

    var controller = new AbortController();
    var timer = setTimeout(function(){ controller.abort(); }, TIMEOUT_MS);
    console.log('[Watts Chat] callAI attempt '+(attempt+1)+'/'+(MAX_RETRIES+1));

    return fetch(PROXY+'?model='+MODEL,{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(body),
      signal:controller.signal
    }).then(function(r) {
      clearTimeout(timer);
      console.log('[Watts Chat] HTTP status: '+r.status);
      if (r.status===429) throw new Error('RATE_LIMIT');
      if (!r.ok) throw new Error('HTTP '+r.status);
      return r.json();
    }).then(function(d) {
      var candidate = d.candidates && d.candidates[0];
      if (!candidate) { console.error('[Watts Chat] No candidates',d); throw new Error('No candidates'); }
      if (candidate.finishReason === 'SAFETY') {
        return "I appreciate you sharing that. I want to make sure I give you the best answer — can you tell me a bit more about your project? Or just call me at **(405) 410-6402** and we'll figure it out together.";
      }
      // Handle Gemini 2.5 Pro thinking model — skip thought parts
      var parts = candidate.content && candidate.content.parts;
      if (!parts || parts.length===0) { console.error('[Watts Chat] No parts',candidate); throw new Error('Empty parts'); }
      var text = '';
      for (var i=0;i<parts.length;i++) {
        if (parts[i].thought) continue;
        if (parts[i].text) { text=parts[i].text; break; }
      }
      if (!text) {
        for (var j=0;j<parts.length;j++) {
          if (parts[j].text) { text=parts[j].text; break; }
        }
      }
      if (!text || text.trim().length<5) { console.error('[Watts Chat] Response too short: "'+(text||'')+'"'); throw new Error('Empty response'); }
      console.log('[Watts Chat] Success — '+text.length+' chars');
      return text;
    }).catch(function(err) {
      clearTimeout(timer);
      console.warn('[Watts Chat] Attempt '+(attempt+1)+' failed: '+err.message);
      if (err.message==='RATE_LIMIT') throw err;
      if (attempt < MAX_RETRIES) {
        var delay = (attempt+1)*2000;
        return new Promise(function(resolve) {
          setTimeout(function() { resolve(callAI(h,attempt+1)); },delay);
        });
      }
      throw err;
    });
  }

  function getLead(t) {
    var ph = t.match(/(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})/);
    if (ph) lead.phone=ph[1];
    var nm = t.match(/(?:my name is|i'm|i am|this is|name:?|call me|it's|hey i'm|hey im|^\s*)([A-Z][a-z]{1,15}(?:\s[A-Z][a-z]{1,15})?)/i);
    if (nm && nm[1].length > 1 && !/^(?:I|A|The|My|It|We|He|She|So|Ok|Hi|Hey|Yes|No|Do|Is|Im)$/i.test(nm[1])) lead.name=nm[1];
    var em = t.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/);
    if (em) lead.email=em[0];
  }

  function saveLead() {
    try {
      var ls = JSON.parse(localStorage.getItem(LEAD_KEY)||'[]');
      var e = {name:lead.name,phone:lead.phone,email:lead.email||null,brand:B.name,page:location.pathname,ts:new Date().toISOString(),msgs:hist.length};
      var dup = false;
      for (var i=0;i<ls.length;i++) { if(ls[i].phone===e.phone&&ls[i].name===e.name){dup=true;break;} }
      if (!dup) {
        ls.push(e);
        localStorage.setItem(LEAD_KEY,JSON.stringify(ls));
        sendLeadNotification(e);
      }
    } catch(x) {}
  }
  function sendLeadNotification(e) {
    // Fire-and-forget to Formspree for email notification
    try {
      fetch('https://formspree.io/f/mjkjgrlb', {
        method:'POST',
        headers:{'Content-Type':'application/json','Accept':'application/json'},
        body:JSON.stringify({
          _subject:'AI Chat Lead: '+(e.name||'Unknown'),
          name:e.name||'Not captured',
          phone:e.phone||'Not captured',
          email:e.email||'Not captured',
          brand:e.brand,
          page:'https://wattsatpcontractor.com'+e.page,
          source:'AI Chat Widget',
          messages:e.msgs+' messages exchanged'
        })
      });
    } catch(x) {}
  }

  // ── EVENTS ──
  trig.addEventListener('click', function(){ open ? doClose() : doOpen(); });
  document.getElementById('wc-x').addEventListener('click', doClose);
  snd.addEventListener('click', function(){ send(inp.value); });
  inp.addEventListener('keydown', function(e){ if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send(inp.value);} });
  qr.addEventListener('click', function(e){
    var b=e.target.closest('.qr'); if(!b) return;
    var m=b.dataset.m;
    if(m.slice(-1)===' ') { inp.value=m; inp.focus(); } else { send(m); }
  });

  // Smart quick replies that adapt
  function updateQuickReplies() {
    if (hist.length < 4) return;
    var has = function(k){ return hist.some(function(m){return m.parts[0].text.toLowerCase().indexOf(k)!==-1;}); };
    var btns = [];
    if (!lead.name) btns.push({m:'My name is ',l:'Share My Name'});
    if (!lead.phone && lead.name) btns.push({m:'My number is ',l:'Share My Number'});
    if (!has('estimate') && !has('schedule')) btns.push({m:'I\'d like a free estimate',l:'Get Estimate'});
    if (!has('cost') && !has('price') && !has('much')) btns.push({m:'How much does this cost?',l:'Pricing'});
    if (btns.length > 0) {
      qr.innerHTML = btns.map(function(b){return '<button class="qr" data-m="'+b.m+'">'+b.l+'</button>';}).join('');
      qr.style.display = 'flex';
    }
  }

  // Nudge after 6s
  setTimeout(function(){ if(!open&&!hist.length&&!hadSession) trig.classList.add('has-dot'); }, 6000);

  // Save session on unload
  window.addEventListener('beforeunload', function(){
    saveSession();
    if(hist.length>1) {
      try {
        var ss=JSON.parse(localStorage.getItem('watts-ai-sessions')||'[]');
        ss.push({brand:B.name,page:location.pathname,ts:new Date().toISOString(),msgs:hist.length,lead:lead});
        localStorage.setItem('watts-ai-sessions',JSON.stringify(ss));
      } catch(x) {}
    }
  });
})();
