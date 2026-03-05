/**
 * BidGen AI Assistant v1 — Gemini 2.5 Pro via Cloudflare Proxy
 * Adds: floating chat panel, material intelligence, estimate review,
 * pricing help, scope analysis, and analytics tracking.
 * Hooks into BidGen's existing global functions and data.
 */
(function() {
  'use strict';

  var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  var MODEL = 'gemini-2.5-pro';
  var TIMEOUT = 45000;

  // ══════════════════════════════════════════
  // SYSTEM INSTRUCTIONS
  // ══════════════════════════════════════════
  var SYS = 'You are the BidGen AI Assistant for Watts Safety Installs / Watts ATP Contractor, built into the Bid Document Generator used by Justin Watts — owner, lead contractor, and general contractor based in Norfolk, Nebraska (NE License #54690-25).\n\n' +
    'YOUR ROLE: You are Justin\'s on-the-go AI co-pilot for bidding, estimating, and material planning. You think like an experienced GC who has done hundreds of remodels, accessibility jobs, and repairs.\n\n' +
    'WHAT YOU CAN DO:\n' +
    '• PRICING HELP — Give realistic Nebraska contractor pricing for any task. Labor rates, material costs, markup guidance. Always give ranges, never hard caps. Say "or more" after the top number.\n' +
    '• MATERIAL INTELLIGENCE — When asked about a specific product (e.g. "ARDEX K 15"), give manufacturer, product specs, coverage rates, dry times, warranty info, best practices, and common mistakes.\n' +
    '• SCOPE REVIEW — Review a bid\'s scope of work and flag missing items, suggest additions, warn about potential change orders.\n' +
    '• ESTIMATE SANITY CHECK — Look at labor + material totals and tell if pricing is competitive, too low, or too high for Nebraska market.\n' +
    '• STEP-BY-STEP GUIDANCE — Walk through complex jobs step by step (e.g. "how to bid a tub-to-shower conversion").\n' +
    '• TRADE KNOWLEDGE — Deep knowledge of flooring, painting, plumbing, electrical, general contracting, accessibility/ADA, roofing, carpet/tile.\n' +
    '• CHANGE ORDER HELP — Help draft change order language when scope changes mid-project.\n\n' +
    'PRICING KNOWLEDGE (Nebraska 2025-2026 rates):\n' +
    '• Flooring install: $2.50-$4.50/sf or more depending on material\n' +
    '• Demolition: $3.00-$6.00/sf or more\n' +
    '• Self-leveling: $2.50-$4.00/sf or more\n' +
    '• Painting interior: $1.50-$3.50/sf or more\n' +
    '• Painting exterior: $2.00-$5.00/sf or more\n' +
    '• Grab bar install: $200-$400+ each\n' +
    '• Wheelchair ramp: $100-$200+/lin ft\n' +
    '• Toilet removal/reinstall: $120-$180+\n' +
    '• Plumbing rough-in: $75-$150+/hr\n' +
    '• Electrical rough-in: $80-$160+/hr\n' +
    '• General labor rate: $55-$95+/hr\n' +
    '• Material markup: 15-30% is standard\n' +
    '• Typical per-sq-ft total (labor+materials) for bathroom remodel: $25-$75+/sf\n' +
    '• Typical per-sq-ft total for kitchen remodel: $30-$100+/sf\n\n' +
    'MATERIAL KNOWLEDGE:\n' +
    '• ARDEX FEATHER FINISH — Cement-based, 1-2mm skim coat, ~90 sf/10lb bag at 1/16". Dry: 15-20 min. Mfg: ARDEX Americas. Warranty: limited.\n' +
    '• ARDEX K 15 — Self-leveling underlayment, 50 lb bag covers ~50 sf at 1/8". Pour time: 15-20 min working. Mfg: ARDEX Americas.\n' +
    '• ARDEX P 51 — Primer for self-leveling. 1 qt covers ~200 sf. Must dry 1-3 hrs before pour. Mfg: ARDEX Americas.\n' +
    '• ARDEX GPS — Patch and skim coat compound. 10 lb covers ~45 sf at 1/16". Mfg: ARDEX Americas.\n' +
    '• Sherwin-Williams Duration — Interior/exterior paint. 350-400 sf/gal. Lifetime limited warranty. Best for high-traffic.\n' +
    '• Benjamin Moore Regal Select — Premium interior. 350-400 sf/gal. Lifetime limited warranty. Excellent hide.\n' +
    '• Backer board (HardieBacker, Durock) — 3\'x5\' sheets, ~$12-$18/sheet. Required behind tile in wet areas.\n' +
    '• Wax ring with sleeve: $6-$12. Always replace when pulling a toilet.\n' +
    '• OSB 3/4" sheet: $35-$55. Subfloor repair/replacement.\n' +
    '• LVP (Luxury Vinyl Plank): $2-$6/sf material. Easy install, waterproof.\n' +
    '• Ceramic tile: $1-$8/sf material. Mortar + grout additional.\n\n' +
    'RULES:\n' +
    '• Sound like a real GC talking to himself — practical, direct, no fluff.\n' +
    '• When giving prices, always give ranges and say "or more" or "+" after the top.\n' +
    '• Reference specific products and brands when relevant.\n' +
    '• If you see bid data in the context, analyze it and give specific feedback.\n' +
    '• Be concise — this is a work tool, not a chatbot. Short, useful answers.\n' +
    '• Use bold (**) for key numbers and product names.\n' +
    '• If the user asks about a material in their catalog, reference the actual data provided.';

  // ══════════════════════════════════════════
  // API CALL
  // ══════════════════════════════════════════
  var _hist = [];

  function callAI(messages) {
    var controller = new AbortController();
    var timer = setTimeout(function() { controller.abort(); }, TIMEOUT);

    var contents = [];
    // Add system instruction as first user message
    contents.push({ role: 'user', parts: [{ text: 'System: ' + SYS }] });
    contents.push({ role: 'model', parts: [{ text: 'Understood. I\'m your BidGen AI assistant. How can I help with your bid?' }] });
    // Add conversation history
    for (var i = 0; i < messages.length; i++) {
      contents.push(messages[i]);
    }

    return fetch(PROXY + '?model=' + MODEL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify({
        contents: contents,
        generationConfig: { temperature: 0.7, maxOutputTokens: 2048, topP: 0.9 }
      })
    }).then(function(r) {
      clearTimeout(timer);
      if (!r.ok) throw new Error('API ' + r.status);
      return r.json();
    }).then(function(data) {
      var c = data.candidates && data.candidates[0];
      if (!c || !c.content || !c.content.parts) throw new Error('No response');
      var text = '';
      for (var i = 0; i < c.content.parts.length; i++) {
        if (c.content.parts[i].thought) continue;
        if (c.content.parts[i].text) { text = c.content.parts[i].text; break; }
      }
      if (!text) {
        for (var j = 0; j < c.content.parts.length; j++) {
          if (c.content.parts[j].text) { text = c.content.parts[j].text; break; }
        }
      }
      return text || 'No response generated.';
    }).catch(function(err) {
      clearTimeout(timer);
      throw err;
    });
  }

  // ══════════════════════════════════════════
  // CONTEXT GATHERING — reads BidGen state
  // ══════════════════════════════════════════
  function getBidContext() {
    var ctx = '';
    try {
      // Current trade type
      var trade = document.getElementById('tradeType');
      if (trade) ctx += 'Trade: ' + trade.value + '\n';

      // Client info
      var client = document.getElementById('clientName');
      if (client && client.value) ctx += 'Client: ' + client.value + '\n';

      // Square footage
      var sqft = document.getElementById('sqft');
      if (sqft && sqft.value) ctx += 'Sq Ft: ' + sqft.value + '\n';

      // Labor items
      if (typeof getLaborItems === 'function') {
        var labor = getLaborItems();
        if (labor.length > 0) {
          ctx += '\nLABOR ITEMS:\n';
          var laborTotal = 0;
          labor.forEach(function(li) {
            var lineTotal = li.qty * li.price;
            laborTotal += lineTotal;
            ctx += '- ' + li.desc + ': ' + li.qty + ' × $' + li.price.toFixed(2) + ' = $' + lineTotal.toFixed(2) + '\n';
          });
          ctx += 'Labor Total: $' + laborTotal.toFixed(2) + '\n';
        }
      }

      // Material items
      if (typeof getMatItems === 'function') {
        var mats = getMatItems();
        if (mats.length > 0) {
          ctx += '\nMATERIAL ITEMS:\n';
          var matTotal = 0;
          mats.forEach(function(mi) {
            var lineTotal = mi.qtyNum * mi.price;
            matTotal += lineTotal;
            ctx += '- ' + mi.desc + ': ' + mi.qty + ' × $' + mi.price.toFixed(2) + ' = $' + lineTotal.toFixed(2) + '\n';
          });
          ctx += 'Materials Subtotal: $' + matTotal.toFixed(2) + '\n';
        }
      }

      // Markup
      var markup = document.getElementById('materialsMarkup');
      if (markup && markup.value) ctx += 'Material Markup: ' + markup.value + '%\n';

      // Scope items
      if (typeof getScope === 'function') {
        var scope = getScope();
        if (scope.length > 0) {
          ctx += '\nSCOPE OF WORK:\n';
          scope.forEach(function(s) { ctx += '- ' + s + '\n'; });
        }
      }

      // Material catalog data
      if (typeof _catalog !== 'undefined' && _catalog.materials) {
        var catCount = Object.keys(_catalog.materials).length;
        if (catCount > 0) ctx += '\nCatalog: ' + catCount + ' materials tracked\n';
      }
    } catch (e) { /* silent */ }
    return ctx;
  }

  // ══════════════════════════════════════════
  // QUICK ACTIONS
  // ══════════════════════════════════════════
  function reviewEstimate() {
    var ctx = getBidContext();
    if (!ctx || ctx.length < 20) {
      addBotMsg('Fill in some bid details first — trade type, labor items, materials — then I can review your estimate.');
      return;
    }
    var msg = 'Review this bid and give me feedback. Is pricing competitive for Nebraska? Any missing items? Any red flags?\n\n' + ctx;
    sendMessage(msg, true);
  }

  function suggestMaterials() {
    var ctx = getBidContext();
    var trade = document.getElementById('tradeType');
    var tradeVal = trade ? trade.value : 'general';
    var msg = 'Based on this ' + tradeVal + ' job, what materials am I likely missing? Give specific products, quantities, and prices.\n\n' + ctx;
    sendMessage(msg, true);
  }

  function pricingHelp() {
    var ctx = getBidContext();
    var sqft = document.getElementById('sqft');
    var sf = sqft ? sqft.value : '';
    var msg = 'Am I pricing this right? Check my per-sq-ft rate and tell me if I\'m competitive, low, or high for Nebraska.\n\n' + ctx;
    sendMessage(msg, true);
  }

  // ══════════════════════════════════════════
  // MATERIAL INTELLIGENCE — lookup from catalog
  // ══════════════════════════════════════════
  function lookupMaterial(name) {
    var catalogInfo = '';
    try {
      if (typeof _catalog !== 'undefined' && _catalog.materials) {
        Object.keys(_catalog.materials).forEach(function(key) {
          if (key.toLowerCase().indexOf(name.toLowerCase()) !== -1) {
            var item = _catalog.materials[key];
            catalogInfo += 'FROM YOUR CATALOG:\n';
            catalogInfo += '- Name: ' + key + '\n';
            catalogInfo += '- Last Price: $' + (item.lastPrice || 'unknown') + '\n';
            catalogInfo += '- Last Used: ' + (item.lastJob || 'unknown') + '\n';
            if (item.priceHistory) {
              catalogInfo += '- Price History: ' + JSON.stringify(item.priceHistory) + '\n';
            }
          }
        });
      }
    } catch (e) { /* silent */ }

    var msg = 'Tell me everything about **' + name + '**: manufacturer, coverage rate, dry time, warranty, best practices, common mistakes, and current approximate price.\n\n' + catalogInfo;
    sendMessage(msg, true);
  }

  // ══════════════════════════════════════════
  // ANALYTICS TRACKING
  // ══════════════════════════════════════════
  function trackBidEvent(type, data) {
    try {
      var key = 'watts_ai_analytics';
      var log = JSON.parse(localStorage.getItem(key) || '[]');
      log.push({
        type: type,
        data: data,
        brand: 'BidGen',
        page: '/tools/bidgen/',
        ts: Date.now()
      });
      if (log.length > 500) log = log.slice(-500);
      localStorage.setItem(key, JSON.stringify(log));
    } catch (e) { /* full */ }
  }

  // ══════════════════════════════════════════
  // CHAT UI
  // ══════════════════════════════════════════
  function injectStyles() {
    var css = document.createElement('style');
    css.textContent = '' +
      '#bgai-toggle{position:fixed;bottom:80px;right:20px;width:56px;height:56px;border-radius:16px;border:none;cursor:pointer;z-index:9990;display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 4px 20px rgba(52,152,219,0.4);background:linear-gradient(135deg,#3498db,#8e44ad);color:#fff;transition:all 0.3s}' +
      '#bgai-toggle:hover{transform:scale(1.08);box-shadow:0 6px 28px rgba(52,152,219,0.5)}' +
      '#bgai-panel{position:fixed;bottom:148px;right:20px;width:380px;max-height:520px;background:#0d1b2a;border:1px solid #1e2d4a;border-radius:16px;z-index:9991;display:none;flex-direction:column;box-shadow:0 12px 40px rgba(0,0,0,0.5);overflow:hidden;font-family:"Segoe UI",system-ui,sans-serif}' +
      '#bgai-panel.open{display:flex}' +
      '#bgai-header{padding:14px 18px;background:linear-gradient(135deg,#16213e,#1a2744);border-bottom:1px solid #1e2d4a;display:flex;align-items:center;justify-content:space-between}' +
      '#bgai-header h4{color:#fff;font-size:14px;font-weight:700;margin:0;display:flex;align-items:center;gap:8px}' +
      '#bgai-header h4 span{color:#3498db}' +
      '#bgai-close{background:none;border:none;color:#555;font-size:20px;cursor:pointer;padding:0}' +
      '#bgai-close:hover{color:#e74c3c}' +
      '#bgai-actions{padding:8px 12px;display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid #1e2d4a;background:#0a1525}' +
      '.bgai-action{background:#16213e;border:1px solid #1e2d4a;color:#8899aa;padding:5px 10px;border-radius:8px;font-size:10px;font-weight:600;cursor:pointer;transition:all 0.2s;white-space:nowrap}' +
      '.bgai-action:hover{border-color:#3498db;color:#3498db;background:#1a2744}' +
      '#bgai-msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;min-height:200px;max-height:320px}' +
      '.bgai-msg{max-width:90%;padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.6;word-wrap:break-word}' +
      '.bgai-msg.user{background:#3498db;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}' +
      '.bgai-msg.bot{background:#16213e;color:#c8d0d8;align-self:flex-start;border-bottom-left-radius:4px;border:1px solid #1e2d4a}' +
      '.bgai-msg.bot strong{color:#3498db}' +
      '.bgai-typing{display:flex;gap:4px;padding:10px 14px;align-self:flex-start}' +
      '.bgai-typing span{width:6px;height:6px;background:#3498db;border-radius:50%;animation:bgaiDot 1.2s infinite}' +
      '.bgai-typing span:nth-child(2){animation-delay:0.2s}' +
      '.bgai-typing span:nth-child(3){animation-delay:0.4s}' +
      '@keyframes bgaiDot{0%,80%,100%{opacity:.3;transform:scale(.8)}40%{opacity:1;transform:scale(1.2)}}' +
      '#bgai-input-row{padding:10px 12px;border-top:1px solid #1e2d4a;display:flex;gap:8px;background:#0a1525}' +
      '#bgai-input{flex:1;background:#16213e;border:1px solid #1e2d4a;border-radius:10px;padding:10px 14px;color:#eee;font-size:13px;font-family:inherit;outline:none;resize:none;min-height:38px;max-height:80px}' +
      '#bgai-input:focus{border-color:#3498db}' +
      '#bgai-input::placeholder{color:#4a5568}' +
      '#bgai-send{background:#3498db;border:none;color:#fff;width:38px;height:38px;border-radius:10px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:all 0.2s;flex-shrink:0}' +
      '#bgai-send:hover{background:#2980b9}' +
      '#bgai-send:disabled{opacity:0.4;cursor:default}' +
      '@media(max-width:500px){#bgai-panel{right:8px;left:8px;width:auto;bottom:140px;max-height:60vh}}';
    document.head.appendChild(css);
  }

  function injectHTML() {
    // Toggle button
    var btn = document.createElement('button');
    btn.id = 'bgai-toggle';
    btn.innerHTML = '🤖';
    btn.title = 'BidGen AI Assistant';
    btn.addEventListener('click', togglePanel);
    document.body.appendChild(btn);

    // Panel
    var panel = document.createElement('div');
    panel.id = 'bgai-panel';
    panel.innerHTML =
      '<div id="bgai-header">' +
        '<h4>🤖 <span>BidGen</span> AI</h4>' +
        '<button id="bgai-close">&times;</button>' +
      '</div>' +
      '<div id="bgai-actions">' +
        '<button class="bgai-action" data-action="review">📊 Review Estimate</button>' +
        '<button class="bgai-action" data-action="materials">🔧 Suggest Materials</button>' +
        '<button class="bgai-action" data-action="pricing">💰 Check Pricing</button>' +
        '<button class="bgai-action" data-action="scope">📋 Scope Check</button>' +
      '</div>' +
      '<div id="bgai-msgs"></div>' +
      '<div id="bgai-input-row">' +
        '<textarea id="bgai-input" placeholder="Ask about pricing, materials, scope..." rows="1"></textarea>' +
        '<button id="bgai-send">→</button>' +
      '</div>';
    document.body.appendChild(panel);

    // Event listeners
    document.getElementById('bgai-close').addEventListener('click', togglePanel);
    document.getElementById('bgai-send').addEventListener('click', function() {
      var input = document.getElementById('bgai-input');
      var text = input.value.trim();
      if (text) { sendMessage(text); input.value = ''; autoResize(input); }
    });
    document.getElementById('bgai-input').addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.getElementById('bgai-send').click();
      }
    });
    document.getElementById('bgai-input').addEventListener('input', function() { autoResize(this); });

    // Quick action buttons
    document.querySelectorAll('.bgai-action').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var action = this.getAttribute('data-action');
        if (action === 'review') reviewEstimate();
        else if (action === 'materials') suggestMaterials();
        else if (action === 'pricing') pricingHelp();
        else if (action === 'scope') scopeCheck();
      });
    });

    // Add welcome message
    addBotMsg('Hey Justin — I\'m your AI bidding co-pilot. Ask me about pricing, materials, or hit one of the quick actions above. I can see your current bid data and give real feedback.');
  }

  function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 80) + 'px';
  }

  var _panelOpen = false;
  function togglePanel() {
    _panelOpen = !_panelOpen;
    document.getElementById('bgai-panel').classList.toggle('open', _panelOpen);
  }

  function addUserMsg(text) {
    var msgs = document.getElementById('bgai-msgs');
    var div = document.createElement('div');
    div.className = 'bgai-msg user';
    div.textContent = text.length > 200 ? text.substring(0, 200) + '...' : text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function addBotMsg(text) {
    var msgs = document.getElementById('bgai-msgs');
    // Remove typing indicator if present
    var typing = msgs.querySelector('.bgai-typing');
    if (typing) typing.remove();

    var div = document.createElement('div');
    div.className = 'bgai-msg bot';
    div.innerHTML = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function showTyping() {
    var msgs = document.getElementById('bgai-msgs');
    var div = document.createElement('div');
    div.className = 'bgai-typing';
    div.innerHTML = '<span></span><span></span><span></span>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  // ══════════════════════════════════════════
  // SEND MESSAGE
  // ══════════════════════════════════════════
  var _busy = false;

  function sendMessage(text, isAction) {
    if (_busy) return;
    _busy = true;
    document.getElementById('bgai-send').disabled = true;

    // Ensure panel is open
    if (!_panelOpen) togglePanel();

    // Show user message (shortened for actions)
    if (!isAction) {
      addUserMsg(text);
    } else {
      // Show a short label for the action
      var shortLabel = text.split('\n')[0];
      if (shortLabel.length > 80) shortLabel = shortLabel.substring(0, 80) + '...';
      addUserMsg(shortLabel);
    }

    showTyping();

    // Build context-aware message
    var fullMsg = text;
    if (!isAction) {
      // For regular messages, inject current bid context
      var ctx = getBidContext();
      if (ctx) {
        fullMsg = text + '\n\n[Current Bid Context]\n' + ctx;
      }
    }

    // Add to history
    _hist.push({ role: 'user', parts: [{ text: fullMsg }] });

    // Keep history manageable
    if (_hist.length > 16) {
      _hist = _hist.slice(0, 2).concat(_hist.slice(-14));
    }

    callAI(_hist).then(function(reply) {
      addBotMsg(reply);
      _hist.push({ role: 'model', parts: [{ text: reply }] });
      trackBidEvent('bidgen_ai_chat', { question: text.substring(0, 100), msgCount: _hist.length });
    }).catch(function(err) {
      addBotMsg('Connection issue — try again in a sec. If this keeps happening, check your internet or the Cloudflare proxy status.');
      trackBidEvent('bidgen_ai_error', { error: err.message });
    }).finally(function() {
      _busy = false;
      document.getElementById('bgai-send').disabled = false;
    });
  }

  function scopeCheck() {
    var ctx = getBidContext();
    if (!ctx || ctx.length < 20) {
      addBotMsg('Add some scope items and job details first, then I can check for missing items and potential change order risks.');
      return;
    }
    var msg = 'Review my scope of work. What am I missing? What could turn into a change order? What should I add to protect myself?\n\n' + ctx;
    sendMessage(msg, true);
  }

  // ══════════════════════════════════════════
  // MATERIAL LOOKUP INTEGRATION
  // ══════════════════════════════════════════
  // Add AI lookup button to material catalog search
  function enhanceCatalog() {
    var searchRow = document.querySelector('.pl-search-row');
    if (!searchRow) return;

    var aiBtn = document.createElement('button');
    aiBtn.innerHTML = '🤖 AI Lookup';
    aiBtn.style.cssText = 'background:linear-gradient(135deg,#3498db,#8e44ad);color:white;border:none;padding:10px 16px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;white-space:nowrap';
    aiBtn.addEventListener('click', function() {
      var searchInput = searchRow.querySelector('input');
      if (searchInput && searchInput.value.trim()) {
        lookupMaterial(searchInput.value.trim());
      } else {
        togglePanel();
        addBotMsg('Type a material name in the catalog search box first, then hit AI Lookup — I\'ll tell you everything about it.');
      }
    });
    searchRow.appendChild(aiBtn);
  }

  // ══════════════════════════════════════════
  // ESTIMATE REVIEW INTEGRATION
  // ══════════════════════════════════════════
  // Add AI review button to the generate buttons area
  function enhanceButtons() {
    var btnRow = document.querySelector('.btn-row');
    if (!btnRow) return;

    var aiReviewBtn = document.createElement('button');
    aiReviewBtn.className = 'btn';
    aiReviewBtn.innerHTML = '🤖 AI Review';
    aiReviewBtn.style.cssText = 'background:linear-gradient(135deg,#3498db,#8e44ad);color:white';
    aiReviewBtn.addEventListener('click', function() {
      reviewEstimate();
    });
    btnRow.appendChild(aiReviewBtn);
  }

  // ══════════════════════════════════════════
  // BID ANALYTICS TRACKING
  // ══════════════════════════════════════════
  function trackBidGenUsage() {
    // Track when bids are generated by monitoring the generate functions
    var origWindow = window;

    // Intercept generate calls if they exist
    ['generateLaborEstimate', 'generateMaterialsEstimate', 'generateChangeOrder'].forEach(function(fnName) {
      if (typeof origWindow[fnName] === 'function') {
        var orig = origWindow[fnName];
        origWindow[fnName] = function() {
          var ctx = getBidContext();
          var trade = document.getElementById('tradeType');
          trackBidEvent('bidgen_generate', {
            type: fnName.replace('generate', ''),
            trade: trade ? trade.value : 'unknown',
            bidSummary: ctx.substring(0, 200)
          });
          return orig.apply(this, arguments);
        };
      }
    });

    // Track job saves
    if (typeof origWindow.saveJob === 'function') {
      var origSave = origWindow.saveJob;
      origWindow.saveJob = function() {
        trackBidEvent('bidgen_save_job', { trade: (document.getElementById('tradeType') || {}).value });
        return origSave.apply(this, arguments);
      };
    }

    // Track template usage
    if (typeof origWindow.applyTemplate === 'function') {
      var origTpl = origWindow.applyTemplate;
      origWindow.applyTemplate = function() {
        var sel = document.getElementById('templateSelect');
        trackBidEvent('bidgen_template', { template: sel ? sel.value : 'unknown' });
        return origTpl.apply(this, arguments);
      };
    }
  }

  // ══════════════════════════════════════════
  // INIT
  // ══════════════════════════════════════════
  function init() {
    injectStyles();
    injectHTML();

    // Wait for BidGen to load, then enhance
    setTimeout(function() {
      enhanceCatalog();
      enhanceButtons();
      trackBidGenUsage();
    }, 2000);
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
