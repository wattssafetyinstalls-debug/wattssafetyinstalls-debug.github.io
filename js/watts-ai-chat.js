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

  var SYS = 'You are the friendly AI assistant for ' + B.name + ' in Norfolk, Nebraska. ' +
    'Phone: (405) 410-6402 | Email: Justin.Watts@WattsATPContractor.com | 507 West Omaha Ave Suite B, Norfolk NE | License #54690-25 | Owner: Justin Watts | ' +
    'Service area: 100-mile radius of Norfolk NE | Rating: 5.0 stars (12 reviews) | Services: ' + B.svc + '. ' +
    'GOALS: 1) Capture name + phone + project. 2) Answer questions helpfully. 3) Push free estimates. 4) Build trust. ' +
    'RULES: Keep replies to 2-3 SHORT sentences. Be warm like a friendly receptionist. Never give exact pricing. Always try to collect contact info. Respond in the visitor\'s language.';

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
<button id="wc-trig" aria-label="Chat with us">\
<span id="wc-dot"></span>\
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>\
<span class="lb">Chat with us</span>\
</button>\
<div id="wc-win">\
<div id="wc-hdr">\
<div class="av">W</div>\
<div><div class="nm">' + B.short + '</div><div class="st">Online now</div></div>\
<button id="wc-x" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>\
</div>\
<div id="wc-msgs"></div>\
<div id="wc-qr">\
<button class="qr" data-m="I need a free estimate">Free Estimate</button>\
<button class="qr" data-m="What services do you offer?">Services</button>\
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
      var g = isSI
        ? 'Hey! How can I help you today? We offer remodeling, painting, handyman services and more across Northeast Nebraska. Want a **free estimate**?'
        : 'Hey! Need help making your home safer? We install wheelchair ramps, grab bars, and accessibility modifications across NE Nebraska. Want a **free estimate**?';
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
      generationConfig:{temperature:.7,maxOutputTokens:200,topP:.9},
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
    var nm = t.match(/(?:my name is|i'm|i am|this is|name:?)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)/i);
    if (nm) lead.name=nm[1];
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
