/**
 * BidGen AI Assistant v2 — Gemini 2.5 Pro (Full Reasoning)
 * Complete contractor mentor: pricing, materials, scope, codes, warranty,
 * manufacturer specs, step-by-step job guidance, estimate review.
 * Max output (65536 tokens), full reasoning chain, expandable UI.
 */
(function() {
  'use strict';

  var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  var MODEL = 'gemini-2.5-pro';
  var TIMEOUT = 120000;

  /* ================================================================
     SYSTEM INSTRUCTIONS — deep contractor mentor
     ================================================================ */
  var SYS = [
    'You are the BidGen AI Mentor — a senior-level general contracting advisor embedded inside the Bid Document Generator for Watts Safety Installs and Watts ATP Contractor.',
    '',
    '## WHO YOU SERVE',
    'Justin Watts — Owner, Lead GC, Nebraska Licensed Contractor #54690-25, based in Norfolk, Nebraska.',
    'He runs two sister companies:',
    '- **Watts ATP Contractor** — accessibility modifications (grab bars, ramps, stairlifts, bathroom ADA conversions) funded by Nebraska ATP program',
    '- **Watts Safety Installs** — general residential & commercial work (flooring, painting, remodeling, repairs, roofing)',
    'He has solid hands-on trade knowledge but is newer to the bidding/quoting side. He needs a real mentor — not a chatbot.',
    '',
    '## HOW TO COMMUNICATE',
    '- Justin is a sharp, capable contractor who understands complex technical material. NEVER dumb things down or skip the hard details. If a topic needs a deep dive, DO the deep dive — all the way to the studs.',
    '- Structure for engagement, not simplicity. Use short paragraphs, headers, bold key numbers, bullet points, and tables so the information is scannable and easy to lock onto — but NEVER reduce the depth or complexity of the actual content.',
    '- Lead with the bottom line first ("Here is what you need to know..."), then unpack the full reasoning and technical detail underneath.',
    '- Use real-world analogies to make abstract concepts click faster, not to replace the real explanation. Give the analogy AND the technical truth. Example: "Think of self-leveler like pancake batter — too thick it won\'t flow, too thin it won\'t hold. Technically, you want ~19-20 oz water per 50lb bag for ARDEX K 15 — that gets you the right viscosity for a self-healing pour."',
    '- When giving numbers, BOLD them: **$3.50/sf**, **10% waste factor**. Numbers should jump off the screen.',
    '- Use checklists and checkboxes where they help organize action items.',
    '- Use tables for any side-by-side comparisons — products, pricing tiers, pros/cons.',
    '- For complex answers: TL;DR summary at the TOP, then the FULL technical detail below. The detail section should hold nothing back — specs, math, reasoning, code references, manufacturer data, all of it.',
    '- Talk like a veteran GC on a jobsite — direct, practical, no corporate fluff — but with the depth of an engineer when the question calls for it.',
    '',
    '## YOUR CORE RULES',
    '1. **NEVER hallucinate.** If you are not 100% certain about a specific fact (price, code, spec), say "verify this" or "I believe" rather than stating it as gospel. Wrong information costs money on a jobsite.',
    '2. **NEVER cut yourself short.** If the answer needs 2000 words to be thorough, write 2000 words. Justin asked because he needs the full picture.',
    '3. **ALWAYS show your math.** When pricing, break down every number. Show quantity x unit price = line total. Show subtotals, markup, overhead, profit.',
    '4. **ALWAYS analyze the actual bid data** when it is provided in context. Do NOT give generic advice when you have specific numbers to work with.',
    '5. **Think step by step.** Use reasoning chains. If something in a bid looks off, explain WHY it looks off and what the correct number should be.',
    '6. **Be direct.** No corporate-speak. Talk like a GC on a jobsite — practical, clear, actionable.',
    '7. **Use markdown formatting** — headers (##), bold (**text**), tables, numbered lists, bullet points.',
    '',
    '## PRICING KNOWLEDGE (Nebraska 2025-2026)',
    '',
    '### Labor Rates (installed)',
    '| Task | Budget | Mid-Range | Premium | Notes |',
    '|------|--------|-----------|---------|-------|',
    '| LVP/Laminate install | $2.00/sf | $3.25/sf | $5.00+/sf | Click-lock vs glue-down |',
    '| Ceramic/Porcelain tile | $4.00/sf | $7.00/sf | $12.00+/sf | Large format costs more |',
    '| Carpet install | $0.75/sf | $1.50/sf | $3.00+/sf | Stretch-in vs glue |',
    '| Demo (flooring) | $1.50/sf | $3.50/sf | $6.00+/sf | Multiple layers = more |',
    '| Self-leveling pour | $2.00/sf | $3.50/sf | $5.00+/sf | Depth-dependent |',
    '| Interior painting | $1.25/sf | $2.50/sf | $4.50+/sf | Wall area not floor |',
    '| Exterior painting | $2.00/sf | $3.50/sf | $6.00+/sf | Height/access factor |',
    '| Drywall hang+finish | $1.50/sf | $2.75/sf | $4.50+/sf | Level 4-5 finish |',
    '| Grab bar install | $175/ea | $275/ea | $450+/ea | Blocking+tile = more |',
    '| Wheelchair ramp | $80/lf | $150/lf | $250+/lf | Wood vs aluminum |',
    '| Stairlift | $2,500 | $4,000 | $8,000+ | Straight vs curved |',
    '| Tub-to-shower | $3,500 | $6,000 | $12,000+ | Full gut vs insert |',
    '| Toilet R&R | $100 | $150 | $225+ | Wax ring included |',
    '| General labor | $45/hr | $65/hr | $95+/hr | Helper vs lead |',
    '| Plumbing | $75/hr | $110/hr | $175+/hr | Licensed |',
    '| Electrical | $75/hr | $120/hr | $185+/hr | Licensed |',
    '',
    '### Markup & Overhead',
    '- Material markup: **20-25%** sweet spot (range 15-30%)',
    '- Overhead: **10-20%** of direct costs (truck, insurance, tools, fuel)',
    '- Profit margin: **10-20%** on top. Net **8-15%** is healthy.',
    '- Travel: $1-2/mile or flat $50-150/trip',
    '- Dumpster: $350-$600 for 10-15 yd roll-off',
    '- Permits: typically $50-$200 residential',
    '',
    '### Room-Level Benchmarks',
    '- Bathroom remodel: **$25-$75+/sf** total (labor+materials)',
    '- Kitchen remodel: **$30-$100+/sf** total',
    '- Full flooring (LVP): **$5-$10/sf** total installed',
    '- Interior paint job: **$2.50-$5.00/sf** of wall area',
    '',
    '## MATERIAL INTELLIGENCE',
    'When asked about ANY product, provide ALL of these if known:',
    '- Manufacturer, product line, what it does in plain English',
    '- Coverage rate at specific thicknesses (e.g. "50 sf/bag at 1/8 inch")',
    '- Working time, cure/dry time at 70F and at lower temps',
    '- Min/max temperature for application',
    '- Shelf life and storage requirements',
    '- Warranty terms, price range (retail + contractor), where to buy',
    '- Prep requirements, common mistakes, pro tips, alternatives',
    '',
    '### Key Products You Should Know',
    '- **ARDEX K 15**: Self-leveling underlayment, 50lb covers ~50sf at 1/8". 15-20 min working time. Primer (P 51) required.',
    '- **ARDEX FEATHER FINISH**: Cement skim coat, ~90sf/10lb at 1/16". Dries 15-20 min.',
    '- **ARDEX P 51**: Primer for SLU. 1 qt ~ 200sf. Dry 1-3 hrs before pour.',
    '- **Sherwin-Williams Duration**: Interior/exterior. 350-400 sf/gal. Lifetime limited warranty.',
    '- **Benjamin Moore Regal Select**: Premium interior. 350-400 sf/gal. Excellent hide.',
    '- **HardieBacker / Durock**: Backer board 3x5 sheets, $12-$18/sheet. Required behind tile in wet areas.',
    '- **LVP (general)**: $2-$6/sf material. Waterproof, click-lock.',
    '- **Ceramic tile (general)**: $1-$8/sf material. Mortar + grout additional.',
    '',
    '## BUILDING CODES & ADA',
    '- Nebraska follows IRC for residential',
    '- ADA grab bars: 1-1/4" to 1-1/2" OD, 1-1/2" clearance from wall, support 250 lbs',
    '- ADA ramp: max 1:12 slope, 60"x60" landings top and bottom',
    '- ADA doorway: 32" clear min, 36" preferred',
    '- ADA toilet: 17-19" seat height (comfort height)',
    '- GFCI required: bathrooms, kitchens, garages, outdoors, basements, within 6ft of water',
    '- When uncertain about a specific code, say so and recommend checking with local AHJ',
    '',
    '## SCOPE & CHANGE ORDER ANALYSIS',
    'Always check for missing: demolition, waste hauling, surface protection, permits, travel/mobilization, contingency.',
    'Common change order triggers: hidden water damage, rot, mold, non-level subfloors, lead paint (pre-1978), asbestos in old mastic, plumbing not to code once exposed.',
    '',
    '## STEP-BY-STEP GUIDANCE FORMAT',
    'When walking through any job:',
    '1. Pre-job: site visit checklist, measurements, photos, client questions',
    '2. Materials list: exact products, quantities with 10% waste, where to buy',
    '3. Tools needed: specific tools, rental vs buy',
    '4. Step-by-step: numbered steps, time estimates, crew size',
    '5. Inspection points: what to verify before covering work',
    '6. Cleanup & protection',
    '7. Common problems and how to handle them'
  ].join('\n');

  /* ================================================================
     API CALL — full reasoning, max output
     ================================================================ */
  var _hist = [];

  function callAI(messages) {
    var controller = new AbortController();
    var timer = setTimeout(function() { controller.abort(); }, TIMEOUT);

    var contents = [];
    contents.push({ role: 'user', parts: [{ text: 'System Instructions:\n\n' + SYS }] });
    contents.push({ role: 'model', parts: [{ text: 'Ready. I\'m your BidGen AI Mentor — think of me as a 90-year-old master tradesman who types fast. I can see your current bid data and I\'ll give you thorough, fact-checked, no-BS answers. Ask me anything.' }] });
    for (var i = 0; i < messages.length; i++) {
      contents.push(messages[i]);
    }

    return fetch(PROXY + '?model=' + MODEL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify({
        contents: contents,
        tools: [{ googleSearch: {} }],
        generationConfig: {
          temperature: 0.8,
          maxOutputTokens: 65536,
          topP: 0.95,
          topK: 64
        }
      })
    }).then(function(r) {
      clearTimeout(timer);
      if (!r.ok) throw new Error('API ' + r.status);
      return r.json();
    }).then(function(data) {
      var c = data.candidates && data.candidates[0];
      if (!c || !c.content || !c.content.parts) throw new Error('No response from model.');
      var texts = [];
      for (var i = 0; i < c.content.parts.length; i++) {
        if (c.content.parts[i].thought) continue;
        if (c.content.parts[i].text) texts.push(c.content.parts[i].text);
      }
      if (texts.length === 0) {
        for (var j = 0; j < c.content.parts.length; j++) {
          if (c.content.parts[j].text) texts.push(c.content.parts[j].text);
        }
      }
      return texts.join('\n\n') || 'Model returned empty. Try rephrasing.';
    }).catch(function(err) {
      clearTimeout(timer);
      throw err;
    });
  }

  /* ================================================================
     CONTEXT GATHERING — reads ALL BidGen state
     ================================================================ */
  function getBidContext() {
    var ctx = '';
    try {
      var fields = [
        ['tradeType', 'Trade Type'],
        ['clientName', 'Client'],
        ['complexName', 'Property/Complex'],
        ['unitNum', 'Unit'],
        ['jobCity', 'City'],
        ['sqft', 'Square Footage'],
        ['linft', 'Linear Footage'],
        ['areaDesc', 'Area Description'],
        ['materialsMarkup', 'Material Markup %'],
        ['supplierNote', 'Supplier Note'],
        ['disclaimer', 'Disclaimer']
      ];
      fields.forEach(function(f) {
        var el = document.getElementById(f[0]);
        if (el && el.value) ctx += f[1] + ': ' + el.value + '\n';
      });

      // Scope
      if (typeof getScope === 'function') {
        var scope = getScope();
        if (scope.length > 0) {
          ctx += '\n--- SCOPE OF WORK ---\n';
          scope.forEach(function(s, i) { ctx += (i + 1) + '. ' + s + '\n'; });
        }
      }

      // Notes
      if (typeof getNotes === 'function') {
        var notes = getNotes();
        if (notes.length > 0) {
          ctx += '\n--- NOTES/DISCLAIMERS ---\n';
          notes.forEach(function(n) { ctx += '- ' + n + '\n'; });
        }
      }

      var sqftEl = document.getElementById('sqft');
      var sqftVal = sqftEl ? parseFloat(sqftEl.value) : 0;
      var markupEl = document.getElementById('materialsMarkup');
      var mkVal = markupEl ? (parseFloat(markupEl.value) || 0) : 0;

      // Labor
      if (typeof getLaborItems === 'function') {
        var labor = getLaborItems();
        if (labor.length > 0) {
          ctx += '\n--- LABOR ITEMS ---\n';
          var laborTotal = 0;
          labor.forEach(function(li) {
            var lt = li.qty * li.price;
            laborTotal += lt;
            ctx += '  ' + li.desc + '  |  ' + li.qty + ' ' + (li.basis || '') + ' x $' + li.price.toFixed(2) + ' = $' + lt.toFixed(2) + '\n';
          });
          ctx += 'LABOR TOTAL: $' + laborTotal.toFixed(2) + '\n';
          if (sqftVal > 0) ctx += 'Labor per SF: $' + (laborTotal / sqftVal).toFixed(2) + '/sf\n';
        }
      }

      // Materials
      if (typeof getMatItems === 'function') {
        var mats = getMatItems();
        if (mats.length > 0) {
          ctx += '\n--- MATERIAL ITEMS ---\n';
          var matTotal = 0;
          mats.forEach(function(mi) {
            var mt = mi.qtyNum * mi.price;
            matTotal += mt;
            ctx += '  ' + mi.desc + '  |  ' + mi.qty + ' x $' + mi.price.toFixed(2) + ' = $' + mt.toFixed(2) + '\n';
          });
          ctx += 'MATERIALS SUBTOTAL: $' + matTotal.toFixed(2) + '\n';
          if (mkVal > 0) {
            var mkAmt = matTotal * (mkVal / 100);
            ctx += 'MARKUP (' + mkVal + '%): $' + mkAmt.toFixed(2) + '\n';
            ctx += 'MATERIALS TOTAL: $' + (matTotal + mkAmt).toFixed(2) + '\n';
          }
        }
      }

      // Distributor Materials
      if (typeof getDistMatItems === 'function') {
        var dist = getDistMatItems();
        if (dist.length > 0) {
          ctx += '\n--- DISTRIBUTOR MATERIALS ---\n';
          var distTotal = 0;
          dist.forEach(function(di) {
            var dt = di.qtyNum * di.price;
            distTotal += dt;
            ctx += '  ' + di.desc + '  |  ' + di.qty + ' x $' + di.price.toFixed(2) + ' = $' + dt.toFixed(2) + '\n';
          });
          ctx += 'DISTRIBUTOR TOTAL: $' + distTotal.toFixed(2) + '\n';
        }
      }

      // Grand Total
      if (typeof calcLaborTotal === 'function' && typeof calcMatTotal === 'function') {
        var lt2 = calcLaborTotal();
        var ms2 = calcMatTotal();
        var mt2 = ms2 + (ms2 * mkVal / 100);
        var dt2 = (typeof calcDistMatTotal === 'function') ? calcDistMatTotal() : 0;
        var grand = lt2 + mt2 + dt2;
        ctx += '\n=== GRAND TOTAL: $' + grand.toFixed(2) + ' ===\n';
        if (sqftVal > 0) ctx += 'TOTAL PER SF: $' + (grand / sqftVal).toFixed(2) + '/sf\n';
      }

      // Catalog snapshot
      if (typeof _catalog !== 'undefined' && _catalog.materials) {
        var catKeys = Object.keys(_catalog.materials);
        if (catKeys.length > 0) {
          ctx += '\n--- YOUR MATERIAL CATALOG (' + catKeys.length + ' items) ---\n';
          catKeys.slice(0, 25).forEach(function(key) {
            var item = _catalog.materials[key];
            ctx += '  ' + key + ': $' + (item.lastPrice || '?') + '\n';
          });
          if (catKeys.length > 25) ctx += '  ... and ' + (catKeys.length - 25) + ' more\n';
        }
      }
    } catch (e) { /* silent */ }
    return ctx;
  }

  /* ================================================================
     QUICK ACTIONS — smart, context-aware prompts
     ================================================================ */
  var ACTIONS = {
    review: {
      label: 'Full Bid Review',
      icon: '\uD83D\uDCCA',
      prompt: function(ctx) {
        return 'Do a THOROUGH review of my current bid. Analyze:\n' +
          '1. **Pricing** — Is each line item priced right for Nebraska? Show me where I am too high or too low.\n' +
          '2. **Missing Items** — What labor or material items am I forgetting? Give product names and prices.\n' +
          '3. **Scope Gaps** — What scope items are missing?\n' +
          '4. **Change Order Risks** — What hidden conditions could bite me?\n' +
          '5. **Markup Check** — Is my material markup healthy?\n' +
          '6. **Recommendations** — What would YOU change if you were bidding this?\n\nGive me the FULL analysis.\n\n' + ctx;
      }
    },
    materials: {
      label: 'Materials Deep Dive',
      icon: '\uD83D\uDD27',
      prompt: function(ctx) {
        var trade = (document.getElementById('tradeType') || {}).value || 'general';
        return 'Based on my ' + trade + ' job, give me a COMPLETE materials analysis:\n' +
          '1. **Missing Materials** — specific products, sizes, quantities, prices I am missing\n' +
          '2. **Quantity Check** — are my quantities right for the square footage? Show math.\n' +
          '3. **Product Recs** — for each material listed, is it the right product? Better alternatives?\n' +
          '4. **Waste Factor** — am I accounting for 10-15% waste?\n' +
          '5. **Where to Buy** — Menards vs HD vs specialty for best pricing near Norfolk NE\n\n' + ctx;
      }
    },
    pricing: {
      label: 'Pricing Breakdown',
      icon: '\uD83D\uDCB0',
      prompt: function(ctx) {
        return 'Break down my pricing in DETAIL:\n' +
          '1. **Per-SF Analysis** — my cost/sf vs Nebraska market\n' +
          '2. **Labor Rate Check** — effective hourly rate, is it competitive?\n' +
          '3. **Material Cost Ratio** — materials vs labor %, is ratio healthy?\n' +
          '4. **Profit Margin** — after everything, what is my actual margin? Show math.\n' +
          '5. **Market Comparison** — where would my bid land among 3 competing GCs?\n' +
          '6. **Optimization** — where can I adjust without losing the bid?\n\n' + ctx;
      }
    },
    scope: {
      label: 'Scope & Legal Shield',
      icon: '\uD83D\uDCCB',
      prompt: function(ctx) {
        return 'Review my scope and protect me legally:\n' +
          '1. **Missing Scope** — what work will I end up doing that is NOT listed?\n' +
          '2. **Change Order Triggers** — hidden conditions that commonly cause COs\n' +
          '3. **Protective Language** — write me 3-4 disclaimer clauses to add\n' +
          '4. **Client Expectations** — what should I make clear BEFORE signing?\n' +
          '5. **Inspection Risks** — what could fail and how to prevent it?\n\n' + ctx;
      }
    },
    howto: {
      label: 'Walk Me Through It',
      icon: '\uD83C\uDF93',
      prompt: function(ctx) {
        var trade = (document.getElementById('tradeType') || {}).value || 'this';
        return 'Walk me through this ' + trade + ' job step by step like I have never done one before:\n' +
          '1. **Pre-Job Checklist** — what to verify/measure/photo\n' +
          '2. **Material Staging** — delivery order, acclimation needs\n' +
          '3. **Day-by-Day Plan** — break the job into days, crew size\n' +
          '4. **Critical Steps** — where mistakes are most expensive, walk through in detail\n' +
          '5. **Quality Checkpoints** — what to verify before moving on\n' +
          '6. **Cleanup & Punchlist** — close out professionally\n' +
          '7. **Time Estimate** — realistic man-days\n\n' + ctx;
      }
    },
    codes: {
      label: 'Codes & ADA',
      icon: '\uD83D\uDCD0',
      prompt: function(ctx) {
        return 'Check this job for code and ADA compliance:\n' +
          '1. **Applicable Codes** — what applies in Nebraska for this work?\n' +
          '2. **Permit Needed?** — what type?\n' +
          '3. **ADA Requirements** — dimensions, slopes, clearances, mounting heights\n' +
          '4. **Common Violations** — what fails inspection most often?\n' +
          '5. **Inspection Prep** — what will they check, how to pass first time?\n\n' + ctx;
      }
    },
    changeorder: {
      label: 'Draft Change Order',
      icon: '\uD83D\uDCDD',
      prompt: function(ctx) {
        return 'Help me draft a change order:\n' +
          '1. **Template** — professional language for the scope change\n' +
          '2. **Pricing** — labor + materials breakdown for additional work\n' +
          '3. **Impact** — timeline and cost impact statement\n' +
          '4. **Protection** — clauses to protect me if client disputes\n' +
          'If you do not know the specific change, suggest common ones for this job type.\n\n' + ctx;
      }
    },
    compare: {
      label: 'Compare Options',
      icon: '\u2696\uFE0F',
      prompt: function(ctx) {
        return 'Compare material options for this job:\n' +
          '1. For each material category, show 2-3 options (budget, mid, premium)\n' +
          '2. Compare: price, quality, warranty, install difficulty, availability near Norfolk NE\n' +
          '3. Your recommendation with reasoning\n' +
          '4. Total cost difference between budget and premium for the whole job\n\n' + ctx;
      }
    }
  };

  /* ================================================================
     MATERIAL LOOKUP
     ================================================================ */
  function lookupMaterial(name) {
    var catalogInfo = '';
    try {
      if (typeof _catalog !== 'undefined' && _catalog.materials) {
        Object.keys(_catalog.materials).forEach(function(key) {
          if (key.toLowerCase().indexOf(name.toLowerCase()) !== -1) {
            var item = _catalog.materials[key];
            catalogInfo += '\nFROM YOUR CATALOG:\n  Name: ' + key + '\n  Last Price: $' + (item.lastPrice || '?') + '\n  Last Job: ' + (item.lastJob || 'n/a') + '\n';
            if (item.priceHistory) catalogInfo += '  Price History: ' + JSON.stringify(item.priceHistory) + '\n';
          }
        });
      }
    } catch (e) { /* silent */ }
    var msg = 'Give me the COMPLETE product profile for **' + name + '**:\n' +
      'Manufacturer, what it is, coverage rates, working/cure times, temp requirements, warranty, price (retail + contractor), where to buy, prep, common mistakes, pro tips, alternatives, storage/shelf life.\n' +
      'If unsure on any spec, say so.\n\n' + catalogInfo;
    sendMessage(msg, true);
  }

  /* ================================================================
     ANALYTICS
     ================================================================ */
  function trackEvent(type, data) {
    try {
      var key = 'watts_ai_analytics';
      var log = JSON.parse(localStorage.getItem(key) || '[]');
      log.push({ type: type, data: data, brand: 'BidGen', page: '/tools/bidgen/', ts: Date.now() });
      if (log.length > 500) log = log.slice(-500);
      localStorage.setItem(key, JSON.stringify(log));
    } catch (e) { /* full */ }
  }

  /* ================================================================
     MARKDOWN RENDERER — rich formatting for AI responses
     ================================================================ */
  function renderMd(text) {
    // Escape HTML first
    var h = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Code blocks
    h = h.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="bgai-pre"><code>$2</code></pre>');

    // Tables — detect table blocks and wrap them
    h = h.replace(/((?:^\|.+\|$\n?)+)/gm, function(tableBlock) {
      var rows = tableBlock.trim().split('\n');
      var html = '<table class="bgai-tbl">';
      var isHeader = true;
      rows.forEach(function(row) {
        if (row.match(/^\|[\s\-:]+\|$/)) { isHeader = false; return; }
        var cells = row.split('|').filter(function(c) { return c.trim() !== ''; });
        var tag = isHeader ? 'th' : 'td';
        html += '<tr>' + cells.map(function(c) { return '<' + tag + '>' + c.trim() + '</' + tag + '>'; }).join('') + '</tr>';
        if (isHeader) { isHeader = false; }
      });
      return html + '</table>';
    });

    // Headers
    h = h.replace(/^#### (.+)$/gm, '<h4 class="bgai-h">$1</h4>');
    h = h.replace(/^### (.+)$/gm, '<h3 class="bgai-h">$1</h3>');
    h = h.replace(/^## (.+)$/gm, '<h2 class="bgai-h">$1</h2>');
    h = h.replace(/^# (.+)$/gm, '<h1 class="bgai-h">$1</h1>');

    // Bold & italic
    h = h.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    h = h.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Inline code
    h = h.replace(/`([^`]+)`/g, '<code class="bgai-ic">$1</code>');

    // Checkboxes
    h = h.replace(/^- \[x\] (.+)$/gm, '<div class="bgai-cb done">\u2611 $1</div>');
    h = h.replace(/^- \[ \] (.+)$/gm, '<div class="bgai-cb">\u2610 $1</div>');

    // Numbered lists
    h = h.replace(/^(\d+)\. (.+)$/gm, '<div class="bgai-oli"><span class="bgai-oln">$1.</span> $2</div>');

    // Bullet lists
    h = h.replace(/^[-\u2022] (.+)$/gm, '<div class="bgai-li">\u2022 $1</div>');

    // Horizontal rules
    h = h.replace(/^---$/gm, '<hr class="bgai-hr">');

    // Paragraphs
    h = h.replace(/\n\n/g, '<div class="bgai-gap"></div>');
    h = h.replace(/\n/g, '<br>');

    return h;
  }

  /* ================================================================
     CHAT UI — large panel, expandable to full-screen
     ================================================================ */
  function injectStyles() {
    var css = document.createElement('style');
    css.textContent =
      /* Toggle button */
      '#bgai-toggle{position:fixed;bottom:80px;right:20px;width:60px;height:60px;border-radius:16px;border:none;cursor:pointer;z-index:9990;display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 4px 24px rgba(52,152,219,0.5);background:linear-gradient(135deg,#3498db,#8e44ad);color:#fff;transition:all 0.3s}' +
      '#bgai-toggle:hover{transform:scale(1.08);box-shadow:0 8px 32px rgba(52,152,219,0.6)}' +

      /* Panel */
      '#bgai-panel{position:fixed;bottom:80px;right:20px;width:540px;height:640px;background:#080e1a;border:1px solid #1a2540;border-radius:18px;z-index:9991;display:none;flex-direction:column;box-shadow:0 16px 60px rgba(0,0,0,0.6);overflow:hidden;font-family:"Segoe UI",system-ui,sans-serif;transition:all 0.3s ease}' +
      '#bgai-panel.open{display:flex}' +
      '#bgai-panel.expanded{top:10px;left:10px;right:10px;bottom:10px;width:auto;height:auto;border-radius:14px}' +

      /* Header */
      '#bgai-hdr{padding:12px 16px;background:linear-gradient(135deg,#0c1726,#14223d);border-bottom:1px solid #1a2540;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}' +
      '#bgai-hdr h4{color:#fff;font-size:15px;font-weight:700;margin:0;display:flex;align-items:center;gap:8px}' +
      '#bgai-hdr h4 span{background:linear-gradient(135deg,#3498db,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}' +
      '.bgai-model{font-size:9px;color:#4a5568;font-weight:600;background:#0d1929;padding:3px 8px;border-radius:6px;border:1px solid #1a2540}' +
      '#bgai-hdr-btns{display:flex;gap:4px}' +
      '.bgai-hbtn{background:none;border:1px solid #1a2540;color:#4a5568;width:30px;height:30px;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;transition:all 0.2s}' +
      '.bgai-hbtn:hover{border-color:#3498db;color:#3498db}' +

      /* Actions bar */
      '#bgai-acts{padding:8px 12px;display:flex;gap:6px;overflow-x:auto;border-bottom:1px solid #1a2540;background:#060c16;flex-shrink:0;scrollbar-width:none;-ms-overflow-style:none}' +
      '#bgai-acts::-webkit-scrollbar{display:none}' +
      '.bgai-act{background:#0d1929;border:1px solid #1a2540;color:#6b7a8d;padding:7px 12px;border-radius:10px;font-size:11px;font-weight:600;cursor:pointer;transition:all 0.2s;white-space:nowrap;flex-shrink:0}' +
      '.bgai-act:hover{border-color:#3498db;color:#3498db;background:#111d33}' +

      /* Messages */
      '#bgai-msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:14px;scroll-behavior:smooth}' +
      '#bgai-msgs::-webkit-scrollbar{width:6px}' +
      '#bgai-msgs::-webkit-scrollbar-thumb{background:#1a2540;border-radius:4px}' +

      /* User msg */
      '.bgai-msg.user{background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;align-self:flex-end;max-width:80%;padding:12px 16px;border-radius:16px 16px 4px 16px;font-size:13px;line-height:1.6;white-space:pre-wrap;word-wrap:break-word}' +

      /* Bot msg — rich content */
      '.bgai-msg.bot{background:#0c1726;color:#c8d4e0;align-self:flex-start;max-width:95%;padding:18px 22px;border-radius:16px 16px 16px 4px;font-size:13.5px;line-height:1.8;word-wrap:break-word;border:1px solid #152040}' +
      '.bgai-msg.bot .bgai-h{margin:12px 0 6px;line-height:1.3}' +
      '.bgai-msg.bot h1{font-size:17px;color:#e2e8f0}' +
      '.bgai-msg.bot h2{font-size:15px;color:#60a5fa}' +
      '.bgai-msg.bot h3{font-size:14px;color:#a78bfa}' +
      '.bgai-msg.bot h4{font-size:13px;color:#34d399}' +
      '.bgai-msg.bot strong{color:#60a5fa}' +
      '.bgai-msg.bot em{color:#c4b5fd}' +
      '.bgai-msg.bot .bgai-ic{background:#162544;color:#fbbf24;padding:1px 5px;border-radius:4px;font-size:12px;font-family:monospace}' +
      '.bgai-msg.bot .bgai-pre{background:#0a1222;border:1px solid #1a2540;border-radius:8px;padding:12px;overflow-x:auto;margin:8px 0}' +
      '.bgai-msg.bot .bgai-pre code{background:none;padding:0;color:#a5b4fc;font-family:monospace;font-size:12px}' +
      '.bgai-msg.bot .bgai-li,.bgai-msg.bot .bgai-oli{padding:2px 0 2px 4px}' +
      '.bgai-msg.bot .bgai-oln{color:#60a5fa;font-weight:700;margin-right:4px}' +
      '.bgai-msg.bot .bgai-cb{padding:2px 0}' +
      '.bgai-msg.bot .bgai-cb.done{color:#34d399}' +
      '.bgai-msg.bot .bgai-hr{border:none;border-top:1px solid #1a2540;margin:10px 0}' +
      '.bgai-msg.bot .bgai-gap{height:10px}' +
      '.bgai-msg.bot .bgai-tbl{width:100%;border-collapse:collapse;margin:8px 0;font-size:12px}' +
      '.bgai-msg.bot .bgai-tbl th{background:#14223d;color:#60a5fa;text-align:left;padding:6px 10px;border:1px solid #1a2540;font-weight:700}' +
      '.bgai-msg.bot .bgai-tbl td{padding:5px 10px;border:1px solid #1a2540}' +

      /* Typing indicator */
      '.bgai-typing{display:flex;gap:5px;padding:12px 16px;align-self:flex-start}' +
      '.bgai-typing span{width:7px;height:7px;background:#3498db;border-radius:50%;animation:bgaiDot 1.2s infinite}' +
      '.bgai-typing span:nth-child(2){animation-delay:0.2s}' +
      '.bgai-typing span:nth-child(3){animation-delay:0.4s}' +
      '@keyframes bgaiDot{0%,80%,100%{opacity:.3;transform:scale(.8)}40%{opacity:1;transform:scale(1.2)}}' +

      /* Timer */
      '.bgai-timer{font-size:10px;color:#4a5568;text-align:center;padding:4px}' +

      /* Input area */
      '#bgai-irow{padding:10px 14px;border-top:1px solid #1a2540;display:flex;gap:8px;background:#060c16;flex-shrink:0;align-items:flex-end}' +
      '#bgai-in{flex:1;background:#0d1929;border:1px solid #1a2540;border-radius:12px;padding:12px 16px;color:#eee;font-size:13px;font-family:inherit;outline:none;resize:none;min-height:44px;max-height:160px;line-height:1.5}' +
      '#bgai-in:focus{border-color:#3498db;box-shadow:0 0 0 2px rgba(52,152,219,0.15)}' +
      '#bgai-in::placeholder{color:#3a4558}' +
      '#bgai-send{background:linear-gradient(135deg,#3498db,#2563eb);border:none;color:#fff;width:44px;height:44px;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;transition:all 0.2s;flex-shrink:0}' +
      '#bgai-send:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(52,152,219,0.3)}' +
      '#bgai-send:disabled{opacity:0.4;cursor:default;transform:none;box-shadow:none}' +

      /* Mobile */
      '@media(max-width:600px){#bgai-panel{right:6px;left:6px;width:auto;bottom:80px;height:75vh}#bgai-panel.expanded{top:0;left:0;right:0;bottom:0;border-radius:0}}';
    document.head.appendChild(css);
  }

  /* ================================================================
     UI INJECTION
     ================================================================ */
  var _open = false;
  var _expanded = false;

  function injectHTML() {
    // Toggle button
    var btn = document.createElement('button');
    btn.id = 'bgai-toggle';
    btn.innerHTML = '\uD83E\uDDE0';
    btn.title = 'BidGen AI Mentor';
    btn.addEventListener('click', togglePanel);
    document.body.appendChild(btn);

    // Panel
    var panel = document.createElement('div');
    panel.id = 'bgai-panel';

    var actBtns = '';
    Object.keys(ACTIONS).forEach(function(key) {
      var a = ACTIONS[key];
      actBtns += '<button class="bgai-act" data-act="' + key + '">' + a.icon + ' ' + a.label + '</button>';
    });

    panel.innerHTML =
      '<div id="bgai-hdr">' +
        '<h4>\uD83E\uDDE0 <span>BidGen</span> AI Mentor <span class="bgai-model">Gemini 2.5 Pro</span></h4>' +
        '<div id="bgai-hdr-btns">' +
          '<button class="bgai-hbtn" id="bgai-expand" title="Expand">\u26F6</button>' +
          '<button class="bgai-hbtn" id="bgai-clear" title="Clear chat">\uD83D\uDDD1</button>' +
          '<button class="bgai-hbtn" id="bgai-close" title="Close">\u2715</button>' +
        '</div>' +
      '</div>' +
      '<div id="bgai-acts">' + actBtns + '</div>' +
      '<div id="bgai-msgs"></div>' +
      '<div id="bgai-irow">' +
        '<textarea id="bgai-in" placeholder="Ask me anything \u2014 pricing, materials, codes, step-by-step, scope review..." rows="1"></textarea>' +
        '<button id="bgai-send">\u27A4</button>' +
      '</div>';
    document.body.appendChild(panel);

    // Events
    document.getElementById('bgai-close').addEventListener('click', togglePanel);
    document.getElementById('bgai-expand').addEventListener('click', function() {
      _expanded = !_expanded;
      document.getElementById('bgai-panel').classList.toggle('expanded', _expanded);
      this.textContent = _expanded ? '\u2750' : '\u26F6';
    });
    document.getElementById('bgai-clear').addEventListener('click', function() {
      if (!confirm('Clear conversation history?')) return;
      _hist = [];
      var msgs = document.getElementById('bgai-msgs');
      msgs.innerHTML = '';
      addBotMsg('Conversation cleared. What would you like to work on?');
    });

    document.getElementById('bgai-send').addEventListener('click', function() {
      var inp = document.getElementById('bgai-in');
      var text = inp.value.trim();
      if (text) { sendMessage(text); inp.value = ''; autoSize(inp); }
    });
    document.getElementById('bgai-in').addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.getElementById('bgai-send').click();
      }
    });
    document.getElementById('bgai-in').addEventListener('input', function() { autoSize(this); });

    // Quick action buttons
    document.querySelectorAll('.bgai-act').forEach(function(b) {
      b.addEventListener('click', function() {
        var key = this.getAttribute('data-act');
        var action = ACTIONS[key];
        if (!action) return;
        var ctx = getBidContext();
        var prompt = action.prompt(ctx);
        sendMessage(prompt, true, action.icon + ' ' + action.label);
      });
    });

    // Welcome
    addBotMsg('**Hey Justin.** I\'m your BidGen AI Mentor \u2014 think of me as a 90-year-old master tradesman who types fast.\n\nI can see your current bid data in real time. Ask me anything:\n- \u2022 "Am I pricing this right?"\n- \u2022 "Walk me through a tub-to-shower conversion"\n- \u2022 "Tell me everything about ARDEX K 15"\n- \u2022 "What am I missing in this scope?"\n\nOr hit one of the quick actions above. **No question is too long or too detailed.** I will match your energy.');
  }

  function autoSize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  }

  function togglePanel() {
    _open = !_open;
    document.getElementById('bgai-panel').classList.toggle('open', _open);
    if (_open) document.getElementById('bgai-in').focus();
  }

  function addUserMsg(text) {
    var msgs = document.getElementById('bgai-msgs');
    var div = document.createElement('div');
    div.className = 'bgai-msg user';
    div.textContent = text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function addBotMsg(text) {
    var msgs = document.getElementById('bgai-msgs');
    var typing = msgs.querySelector('.bgai-typing');
    if (typing) typing.remove();
    var timerEl = msgs.querySelector('.bgai-timer');
    if (timerEl) timerEl.remove();

    var div = document.createElement('div');
    div.className = 'bgai-msg bot';
    div.innerHTML = renderMd(text);
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function showTyping() {
    var msgs = document.getElementById('bgai-msgs');
    var div = document.createElement('div');
    div.className = 'bgai-typing';
    div.innerHTML = '<span></span><span></span><span></span>';
    msgs.appendChild(div);

    // Show elapsed time
    var timerDiv = document.createElement('div');
    timerDiv.className = 'bgai-timer';
    timerDiv.textContent = 'Thinking...';
    msgs.appendChild(timerDiv);
    var start = Date.now();
    timerDiv._interval = setInterval(function() {
      var secs = Math.round((Date.now() - start) / 1000);
      timerDiv.textContent = 'Thinking... ' + secs + 's';
    }, 1000);

    msgs.scrollTop = msgs.scrollHeight;
  }

  function clearTimer() {
    var msgs = document.getElementById('bgai-msgs');
    var timerEl = msgs.querySelector('.bgai-timer');
    if (timerEl && timerEl._interval) clearInterval(timerEl._interval);
  }

  /* ================================================================
     SEND MESSAGE
     ================================================================ */
  var _busy = false;

  function sendMessage(text, isAction, actionLabel) {
    if (_busy) return;
    _busy = true;
    document.getElementById('bgai-send').disabled = true;

    if (!_open) togglePanel();

    // Show user message
    if (isAction && actionLabel) {
      addUserMsg(actionLabel);
    } else {
      addUserMsg(text);
    }

    showTyping();

    // Build message with context for non-action messages
    var fullMsg = text;
    if (!isAction) {
      var ctx = getBidContext();
      if (ctx) fullMsg = text + '\n\n[Current Bid Data]\n' + ctx;
    }

    _hist.push({ role: 'user', parts: [{ text: fullMsg }] });

    // Keep history — up to 40 messages (20 exchanges)
    if (_hist.length > 40) {
      _hist = _hist.slice(0, 2).concat(_hist.slice(-38));
    }

    callAI(_hist).then(function(reply) {
      clearTimer();
      addBotMsg(reply);
      _hist.push({ role: 'model', parts: [{ text: reply }] });
      trackEvent('bidgen_ai_chat', { q: text.substring(0, 120), msgs: _hist.length });
    }).catch(function(err) {
      clearTimer();
      addBotMsg('**Connection issue.** ' + (err.name === 'AbortError' ? 'Request timed out (2 min limit). Try a simpler question or check your internet.' : 'Error: ' + err.message + '. Try again in a moment.'));
      trackEvent('bidgen_ai_error', { error: err.message });
    }).finally(function() {
      _busy = false;
      document.getElementById('bgai-send').disabled = false;
    });
  }

  /* ================================================================
     BIDGEN INTEGRATIONS
     ================================================================ */
  function enhanceCatalog() {
    var searchRow = document.querySelector('.pl-search-row');
    if (!searchRow) return;
    var aiBtn = document.createElement('button');
    aiBtn.innerHTML = '\uD83E\uDDE0 AI Lookup';
    aiBtn.style.cssText = 'background:linear-gradient(135deg,#3498db,#8e44ad);color:white;border:none;padding:10px 16px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;white-space:nowrap';
    aiBtn.addEventListener('click', function() {
      var si = searchRow.querySelector('input');
      if (si && si.value.trim()) lookupMaterial(si.value.trim());
      else { togglePanel(); addBotMsg('Type a material name in the catalog search box first, then hit AI Lookup.'); }
    });
    searchRow.appendChild(aiBtn);
  }

  function enhanceButtons() {
    var btnRow = document.querySelector('.btn-row');
    if (!btnRow) return;
    var aiBtn = document.createElement('button');
    aiBtn.className = 'btn';
    aiBtn.innerHTML = '\uD83E\uDDE0 AI Review';
    aiBtn.style.cssText = 'background:linear-gradient(135deg,#3498db,#8e44ad);color:white';
    aiBtn.addEventListener('click', function() {
      var ctx = getBidContext();
      if (!ctx || ctx.length < 30) { togglePanel(); addBotMsg('Fill in some bid details first, then I can review your estimate.'); return; }
      sendMessage(ACTIONS.review.prompt(ctx), true, ACTIONS.review.icon + ' ' + ACTIONS.review.label);
    });
    btnRow.appendChild(aiBtn);
  }

  function trackUsage() {
    ['generateLaborEstimate', 'generateMaterialsEstimate', 'generateChangeOrder'].forEach(function(fn) {
      if (typeof window[fn] === 'function') {
        var orig = window[fn];
        window[fn] = function() {
          trackEvent('bidgen_generate', { type: fn, trade: (document.getElementById('tradeType') || {}).value });
          return orig.apply(this, arguments);
        };
      }
    });
    if (typeof window.saveJob === 'function') {
      var origSave = window.saveJob;
      window.saveJob = function() {
        trackEvent('bidgen_save', { trade: (document.getElementById('tradeType') || {}).value });
        return origSave.apply(this, arguments);
      };
    }
  }

  /* ================================================================
     INIT
     ================================================================ */
  function init() {
    injectStyles();
    injectHTML();
    setTimeout(function() {
      enhanceCatalog();
      enhanceButtons();
      trackUsage();
    }, 2000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
