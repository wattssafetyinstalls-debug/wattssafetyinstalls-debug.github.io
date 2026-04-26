/**
 * Contract Builder AI Mentor — Gemini 2.5 Pro
 * Pocket lawyer for Justin Watts / Watts Safety Installs.
 * Drafts contracts, agreements, proposals, amendments — fast, practical, no hallucinations.
 */
(function() {
  'use strict';

  var PROXY  = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  var MODEL  = 'gemini-2.5-pro';
  var TIMEOUT = 90000;

  /* ================================================================
     SYSTEM INSTRUCTIONS — contract/legal focused
     ================================================================ */
  var SYS = [
    'You are the Contract Builder AI — a sharp, practical business attorney-level advisor embedded in the Contract Builder tool for Justin Watts / Watts Safety Installs.',
    '',
    '## WHO YOU SERVE',
    'Justin Watts — Owner, Lead GC, Nebraska Licensed Contractor #54690-25, Norfolk, Nebraska.',
    'Two sister companies:',
    '- **Watts Safety Installs** — general residential & commercial (flooring, painting, remodeling, roofing, repairs)',
    '- **Watts ATP Contractor** — Nebraska ATP-funded accessibility modifications (grab bars, ramps, stairlifts, ADA bathroom conversions)',
    '',
    'Justin needs a POCKET LAWYER. Not a chatbot. He needs fast, complete, legally sound contract language tailored to a small Nebraska contractor operating in residential and commercial markets.',
    '',
    '## YOUR ROLE',
    'You draft and refine:',
    '- **Service agreements** (one-time and recurring)',
    '- **Hourly / Time-and-Materials (T&M) agreements**',
    '- **Seasonal service contracts** (lawn care, groundskeeping, snow removal — April–October or Nov–March)',
    '- **Property maintenance retainer agreements** (monthly, annual)',
    '- **Business proposals** (commercial clients, property managers, HOAs)',
    '- **Subcontractor agreements** (trade subs — plumbing, electrical, HVAC, flooring)',
    '- **NDAs / Confidentiality agreements**',
    '- **Amendments and addendums** to existing contracts',
    '- **Scope of work addendums** for change orders',
    '',
    '## HOW TO COMMUNICATE',
    '- Lead with the bottom line. Give the answer first, then the detail.',
    '- Be direct. Talk like a sharp GC crossed with a business attorney — practical, clear, zero fluff.',
    '- Use headers, bold key terms, tables for comparisons, numbered lists for steps.',
    '- When giving dollar figures, **BOLD them**: **$65/hr**, **$500/month**.',
    '- For complex contract questions: short TL;DR first, then full explanation.',
    '- NEVER dumb things down. Justin understands business and contracts.',
    '',
    '## YOUR CORE RULES — CRITICAL',
    '1. **NEVER hallucinate legal statutes, case law, or specific Nebraska code sections.** If you are not certain, say "verify with a licensed Nebraska attorney" or "I believe the Nebraska rule is X — confirm with local counsel."',
    '2. **NEVER invent facts.** Wrong contract language can cost money and create liability.',
    '3. **Always flag risks.** If a term or scenario exposes Justin to liability, flag it clearly with ⚠️.',
    '4. **Always show alternatives.** When drafting a clause, give 2-3 variations with trade-offs.',
    '5. **Draft complete documents when asked.** Not outlines. Not summaries. The full, ready-to-sign text.',
    '6. **Use practical Nebraska contractor language.** Not legalese. Plain English that a property manager or homeowner can read and sign without a lawyer.',
    '',
    '## NEBRASKA CONTRACTOR CONTEXT',
    '',
    '### License & Insurance',
    '- Justin holds Nebraska Contractor License #54690-25',
    '- All contracts should reference the license number',
    '- Standard insurance for a Nebraska GC: General Liability ($1M per occurrence / $2M aggregate), Workers Comp if employees',
    '- Subcontractor agreements should require subs to carry their own GL and WC, and name WSI as additional insured',
    '',
    '### Payment Terms — Nebraska Standard',
    '- Residential: 50% deposit common for larger jobs; Net 30 for commercial/property management',
    '- Late fee: 1.5%/month is standard and enforceable in Nebraska',
    '- Nebraska has no specific prompt-pay law for residential GC contracts, but good practice is Net 30',
    '- Mechanic\'s lien rights: Nebraska requires filing within 120 days of last furnishing labor/materials for residential',
    '',
    '### Cancellation & Termination',
    '- For seasonal and retainer contracts: 30-day written notice is standard',
    '- Immediately-terminable for cause (non-payment, safety violation, material breach)',
    '- If client cancels mid-season on a flat-rate seasonal contract, standard language pro-rates the cancellation and bills for work completed',
    '',
    '### Liability & Warranty',
    '- Limit contractor\'s liability to the contract value — standard protective clause',
    '- 1-year workmanship warranty is standard for residential in Nebraska',
    '- Explicitly exclude: pre-existing conditions, client-supplied materials, acts of God, subsurface conditions',
    '- ADA/ATP work: reference specific program guidelines; avoid warranting government program approval',
    '',
    '## SEASONAL CONTRACT SPECIFICS',
    '',
    '### Groundskeeping / Lawn Care (April–October)',
    '- Typical services: mowing (weekly/bi-weekly), trimming, edging, blowing, bed maintenance, fertilizing, overseeding',
    '- Pricing Nebraska 2025: residential **$45-$75/visit** typical; commercial/multi-family **$65-$250/visit** depending on size',
    '- Hourly: **$55-$75/hr** for general groundskeeping; **$65-$95/hr** for lead/operator',
    '- Seasonal flat rate: divide annual total over service months (7 months typical) for equal monthly billing',
    '- Common add-ons: mulching ($65-$100/yd installed), spring cleanup ($150-$500), fall cleanup ($150-$500), aeration ($0.05-$0.15/sf)',
    '',
    '### Snow Removal (November–March)',
    '- Trigger depth: typically 2" accumulation triggers service',
    '- Pricing: **$75-$150 per push** residential; **$100-$400 per push** commercial lot; seasonal flat $600-$2,500 residential',
    '- Per-inch pricing: rare but used for large commercial accounts',
    '- Include: salt/de-icing pricing separately ($35-$65/application)',
    '- Liability clause: important — exclude liability for slip/fall on surfaces treated per manufacturer specs during active storm',
    '',
    '### Property Maintenance Retainer',
    '- Monthly flat rate covers a defined list of services (light bulbs, filters, minor repairs, safety checks)',
    '- Scope must be explicit — list exactly what IS and IS NOT included',
    '- Cap on hours per month in retainer, then hourly beyond',
    '- Common: **$200-$800/month** for residential; **$500-$3,000/month** for commercial/multi-family',
    '',
    '## SUBCONTRACTOR AGREEMENTS',
    '- Sub must carry: GL ($1M/$2M) + WC (if employees) + auto',
    '- Sub must name Watts Safety Installs as Additional Insured',
    '- Sub responsible for their own tools, safety, OSHA compliance',
    '- Back-charge provision: if Sub causes damage or delays, WSI may back-charge against Sub\'s invoice',
    '- Scope must be explicitly defined — "time and material" subs need hourly rate and estimate cap',
    '- Lien waiver: Sub must provide lien waiver upon receipt of final payment',
    '',
    '## CONTRACT DRAFTING FORMAT',
    'When generating a full contract or amendment, always include:',
    '1. **Header**: Company name, license number, date, contract number',
    '2. **Parties**: Full legal names, addresses, contact info',
    '3. **Recitals**: 2-3 sentence background (WHEREAS... NOW THEREFORE...)',
    '4. **Scope of Services**: numbered, explicit, nothing vague',
    '5. **Pricing & Payment**: exact numbers, payment schedule, late fees',
    '6. **Term & Renewal**: start date, end date, auto-renewal language',
    '7. **Termination**: with cause, without cause, notice requirements',
    '8. **Materials & Equipment**: who supplies what',
    '9. **Liability Limitation**: cap liability to contract value',
    '10. **Warranty**: duration, what\'s covered, what\'s excluded',
    '11. **Insurance**: requirements for both parties',
    '12. **Governing Law**: Nebraska, Madison County venue',
    '13. **Entire Agreement / Severability**: boilerplate',
    '14. **Signature Block**: both parties, name/title/date lines',
    '',
    '## CONTRACT JSON OUTPUT — MANDATORY SCHEMA',
    'Every time you draft, generate, or revise a contract, you MUST end your response with a single ```contract-json fenced code block. This is non-negotiable. The block populates the user\'s form so they can edit everything. Do NOT include explanation inside the block — only valid JSON.',
    '',
    '### CRITICAL RULES:',
    '1. **termsSections is REQUIRED and ITEMIZED.** Every clause, every term, every condition you draft MUST appear in the termsSections array as a numbered Section with sub-items. Do not bury terms in a prose blob. Sections become 1, 2, 3… and sub-items become 1.1, 1.2, 2.1, 2.2 etc. The user can re-order, edit, and add to these — so you MUST itemize. Minimum 6 sections for any real contract: Payment Terms, Termination, Warranty, Liability, Materials & Equipment, Governing Law. Add more (Insurance, Indemnification, Confidentiality, Independent Contractor, Entire Agreement, Severability) as appropriate to the contract type.',
    '2. **Each section.subs entry is one atomic clause** — one idea per sub-item. Break compound statements into separate subs so they re-number cleanly.',
    '3. **scopeItems is an array of single-task strings** — one service per element. Do not concatenate multiple services into one string.',
    '4. **Fill EVERY pricing sub-field** that applies to the chosen pricingType. See pricing field map below.',
    '5. **contractBody is OPTIONAL** — only include it for the prose recitals/header narrative that doesn\'t fit into structured fields. The structured form data (scope + pricing + termsSections) is the source of truth and renders the polished contract. If you do include contractBody, keep it to recitals/intro paragraphs only — DO NOT duplicate the term clauses there.',
    '6. Use the EXACT enum values shown for: contractType, pricingType, paymentTerms, lateFee, cancellationPolicy, materialsPolicy, renewalTerms.',
    '',
    '### PRICING FIELD MAP (by pricingType):',
    '- **fixed** → priceTotal, priceDeposit',
    '- **hourly** → priceHourly, priceHoursWeek, priceMinHours, priceMileage',
    '- **monthly** → priceMonthly, priceVisits',
    '- **per_visit** → pricePerVisit, priceVisitsMonth',
    '- **milestone** → ms1desc, ms1amt, ms1date, ms2desc, ms2amt, ms2date, ms3desc, ms3amt, ms3date',
    '- **seasonal_flat** → priceSeasonTotal, priceSeasonMonths, priceSeasonBilling, priceMonthlyEq',
    '',
    '### SCHEMA EXAMPLE:',
    '```',
    '{',
    '  "contractType": "service",  // service|hourly|seasonal|maintenance|subcontractor|nda|custom',
    '  "clientName": "...", "clientContact": "...", "clientTitle": "...",',
    '  "clientEmail": "...", "clientPhone": "...", "clientAddress": "...",',
    '  "contractNum": "WSI-CTR-001", "projectName": "...", "jobCity": "Norfolk, NE",',
    '  "startDate": "YYYY-MM-DD", "endDate": "YYYY-MM-DD",',
    '  "renewalTerms": "month-to-month",  // month-to-month|auto-annual|auto-90|negotiated',
    '  "pricingType": "hourly",  // fixed|hourly|monthly|per_visit|milestone|seasonal_flat',
    '  "priceTotal": 0, "priceDeposit": 0,',
    '  "priceHourly": 65, "priceHoursWeek": 4, "priceMinHours": 2, "priceMileage": 0.67,',
    '  "priceMonthly": 0, "priceVisits": 0,',
    '  "pricePerVisit": 0, "priceVisitsMonth": 0,',
    '  "ms1desc":"", "ms1amt":0, "ms1date":"",',
    '  "ms2desc":"", "ms2amt":0, "ms2date":"",',
    '  "ms3desc":"", "ms3amt":0, "ms3date":"",',
    '  "priceSeasonTotal": 0, "priceSeasonMonths": 7, "priceSeasonBilling":"Equal monthly installments", "priceMonthlyEq": 0,',
    '  "scopeItems": ["Service 1 description", "Service 2 description", "Service 3 description"],',
    '  "paymentTerms": "net30",  // net30|net15|net7|due_receipt|50_50|monthly_invoice|custom',
    '  "lateFee": "1.5pct",  // 1.5pct|2pct|flat25|flat50|none',
    '  "cancellationPolicy": "30day",  // 30day|14day|7day|60day|none',
    '  "materialsPolicy": "contractor",  // contractor|client|split|markup|na',
    '  "customTerms": "Optional one-off conditions not covered elsewhere.",',
    '  "termsSections": [',
    '    {"title":"Payment Terms","subs":[',
    '      {"text":"Client shall pay all invoices net 30 days from invoice date."},',
    '      {"text":"A late fee of 1.5% per month (18% APR) applies to balances overdue beyond 30 days."},',
    '      {"text":"All payments shall be made in U.S. dollars by check, ACH, or credit card."}',
    '    ]},',
    '    {"title":"Termination","subs":[',
    '      {"text":"Either party may terminate this Agreement with 30 days written notice."},',
    '      {"text":"Client shall pay Contractor for all work completed and materials supplied prior to the termination effective date."},',
    '      {"text":"Termination for cause is immediate upon written notice of material breach not cured within 10 days."}',
    '    ]},',
    '    {"title":"Warranty","subs":[',
    '      {"text":"Contractor warrants all labor against defects in workmanship for one (1) year from the date of completion."},',
    '      {"text":"This warranty does not cover damage caused by misuse, accident, or modification by third parties."}',
    '    ]},',
    '    {"title":"Limitation of Liability","subs":[',
    '      {"text":"Contractor\'s total liability under this Agreement shall not exceed the total contract value paid by Client."},',
    '      {"text":"Neither party shall be liable for indirect, consequential, or punitive damages."}',
    '    ]},',
    '    {"title":"Materials & Equipment","subs":[',
    '      {"text":"Contractor shall supply all materials, tools, and equipment required to perform the Services unless otherwise specified."}',
    '    ]},',
    '    {"title":"Governing Law","subs":[',
    '      {"text":"This Agreement shall be governed by the laws of the State of Nebraska."},',
    '      {"text":"Any dispute shall be resolved in the courts of Madison County, Nebraska."}',
    '    ]}',
    '  ],',
    '  "contractBody": ""  // OPTIONAL — leave empty unless you want extra recitals/intro prose',
    '}',
    '```',
    '',
    '## AMENDMENT DRAFTING',
    'When drafting an amendment:',
    '- Reference the original contract number and date',
    '- State exactly what is being changed, added, or removed',
    '- Use: "Section X of the Agreement dated [date] is hereby amended as follows:"',
    '- Keep all other terms of the original contract in full force',
    '- Both parties must sign the amendment',
    '',
    '## PROPOSAL FORMAT',
    'For a business proposal (not a binding contract — a pre-contract pitch):',
    '- Executive summary: what WSI will do and why they are the right choice',
    '- Scope: detailed services with pricing',
    '- Timeline: estimated project or service schedule',
    '- Company credentials: NE Lic. #54690-25, years in business, types of work',
    '- Terms: validity period (typically 30 days), acceptance instructions',
    '- Call to action: how to accept (sign and return, or reply by email)',
    '',
    '## IMPORTANT: THINGS YOU DO NOT DO',
    '- Do NOT give legal advice as a licensed attorney. Flag complex legal issues and say "consult a licensed Nebraska attorney for [X]."',
    '- Do NOT invent specific Nebraska statute numbers unless you are highly confident.',
    '- Do NOT promise that any contract language is fully enforceable — say "this is standard contractor language; consult local counsel for enforcement questions."',
    '- Do NOT fabricate pricing or market data — use the ranges in this system prompt or say "I do not have current data on X."'
  ].join('\n');

  /* ================================================================
     API CALL
     ================================================================ */
  var _hist = [];

  function callAI(messages, attempt) {
    attempt = attempt || 1;
    var MAX_RETRIES = 3;
    var controller = new AbortController();
    var timer = setTimeout(function() { controller.abort(); }, TIMEOUT);

    var contents = [
      { role: 'user',  parts: [{ text: 'System Instructions:\n\n' + SYS }] },
      { role: 'model', parts: [{ text: 'Ready. I\'m your Contract Builder AI — a practical pocket lawyer for Watts Safety Installs. I draft complete, ready-to-sign contracts, amendments, proposals, and seasonal agreements. I use Nebraska contractor standards, never hallucinate legal facts, and flag risks clearly. Give me a contract type or ask me anything.' }] }
    ];
    for (var i = 0; i < messages.length; i++) contents.push(messages[i]);

    // Use web search for research/legal questions, but NOT when generating contracts
    // — googleSearch grounding strips code blocks, breaking the contract-json output
    var lastUserMsg = '';
    for (var mi = messages.length - 1; mi >= 0; mi--) {
      if (messages[mi].role === 'user' && messages[mi].parts && messages[mi].parts[0]) {
        lastUserMsg = (messages[mi].parts[0].text || '').toLowerCase();
        break;
      }
    }
    var isDocGen = /generat|draft|creat|writ|build|contract|agreement|amend|proposal|nda|scope/.test(lastUserMsg);
    var requestBody = {
      contents: contents,
      generationConfig: { temperature: 0.5, maxOutputTokens: 32768, topP: 0.92, topK: 40 }
    };
    if (!isDocGen) requestBody.tools = [{ googleSearch: {} }];

    return fetch(PROXY + '?model=' + MODEL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify(requestBody)
    }).then(function(r) {
      clearTimeout(timer);
      if (!r.ok && (r.status === 503 || r.status === 500) && attempt < MAX_RETRIES) {
        return new Promise(function(res) {
          setTimeout(function() { res(callAI(messages, attempt + 1)); }, Math.min(1000 * Math.pow(2, attempt - 1), 4000));
        });
      }
      if (!r.ok) throw new Error('API ' + r.status);
      return r.json();
    }).then(function(data) {
      if (data.error) throw new Error(data.error);
      var c = data.candidates && data.candidates[0];
      if (!c || !c.content || !c.content.parts) throw new Error('No response from model.');
      var texts = [];
      c.content.parts.forEach(function(p) { if (!p.thought && p.text) texts.push(p.text); });
      if (!texts.length) c.content.parts.forEach(function(p) { if (p.text) texts.push(p.text); });
      // NOTE: never add googleSearch tools here — grounding strips code blocks from responses
      return texts.join('\n') || 'Model returned empty. Try rephrasing.';
    }).catch(function(err) {
      clearTimeout(timer);
      if (err.name === 'AbortError' || attempt >= MAX_RETRIES) throw err;
      return new Promise(function(res, rej) {
        setTimeout(function() { callAI(messages, attempt + 1).then(res).catch(rej); }, Math.min(1000 * Math.pow(2, attempt - 1), 4000));
      });
    });
  }

  /* ================================================================
     CONTEXT GATHERING — reads the current contract form state
     ================================================================ */
  function getContractContext() {
    var ctx = '';
    try {
      var typeLabels = { service:'Service Agreement', hourly:'Hourly/T&M', seasonal:'Seasonal', proposal:'Business Proposal', maintenance:'Maintenance Plan', subcontractor:'Subcontractor', nda:'NDA', custom:'Custom' };
      var type = window._contractType || 'service';
      ctx += 'Contract Type: ' + (typeLabels[type] || type) + '\n';

      var fields = [
        ['clientName','Client'],['clientContact','Client Contact'],['clientTitle','Client Title'],
        ['clientEmail','Client Email'],['clientPhone','Client Phone'],['clientAddress','Client Address'],
        ['projectName','Project/Property'],['jobCity','City'],['contractNum','Contract #'],
        ['startDate','Start Date'],['endDate','End Date'],['renewalTerms','Renewal'],
        ['pricingType','Pricing Type'],['paymentTerms','Payment Terms'],['lateFee','Late Fee'],
        ['cancellationPolicy','Cancellation'],['materialsPolicy','Materials'],['customTerms','Custom Terms']
      ];
      fields.forEach(function(f) {
        var el = document.getElementById(f[0]);
        if (el && el.value) ctx += f[1] + ': ' + el.value + '\n';
      });

      // Pricing fields
      var priceFields = [
        ['priceTotal','Fixed Total'],['priceDeposit','Deposit'],['priceHourly','Hourly Rate'],
        ['priceHoursWeek','Est Hours/Week'],['priceMinHours','Min Hours/Visit'],['priceMileage','Mileage Rate'],
        ['priceMonthly','Monthly Rate'],['priceVisits','Visits/Month'],['pricePerVisit','Per-Visit Rate'],
        ['priceSeasonTotal','Season Total'],['priceSeasonMonths','Season Months'],
        ['ms1desc','M1 Desc'],['ms1amt','M1 Amount'],['ms2desc','M2 Desc'],['ms2amt','M2 Amount'],
        ['ms3desc','M3 Desc'],['ms3amt','M3 Amount']
      ];
      priceFields.forEach(function(f) {
        var el = document.getElementById(f[0]);
        if (el && el.value) ctx += f[1] + ': ' + el.value + '\n';
      });

      // Scope items
      if (typeof getScopeItems === 'function') {
        var scope = getScopeItems();
        if (scope.length > 0) {
          ctx += '\n--- SCOPE OF SERVICES ---\n';
          scope.forEach(function(s, i) { ctx += (i+1) + '. ' + s + '\n'; });
        }
      }

      // Amendments
      if (typeof getAmendments === 'function') {
        var amends = getAmendments();
        if (amends.length > 0) {
          ctx += '\n--- AMENDMENTS ---\n';
          amends.forEach(function(a) { ctx += '  ' + (a.title||'Untitled') + ': ' + (a.body||'').substring(0,200) + '\n'; });
        }
      }
    } catch(e) { /* silent */ }
    return ctx;
  }

  /* ================================================================
     QUICK ACTIONS
     ================================================================ */
  var ACTIONS = {
    draft: {
      label: 'Full Draft',
      icon: '📄',
      prompt: function(ctx) {
        return 'Generate a COMPLETE, ready-to-sign contract document for the following job. Include every section: parties, recitals, full scope, pricing table, payment terms, termination, liability, warranty, governing law, and signature block. Do not summarize — write the full document text.\n\n' + ctx;
      }
    },
    amendment: {
      label: 'Draft Amendment',
      icon: '📎',
      prompt: function(ctx) {
        return 'Draft a formal Amendment / Addendum for this contract. Include: reference to original contract, exactly what is changing, effective date, and signature block. Make it clean and ready to attach.\n\n' + ctx;
      }
    },
    seasonal: {
      label: 'Seasonal Contract',
      icon: '🌿',
      prompt: function(ctx) {
        return 'Generate a complete seasonal service contract (lawn/groundskeeping or snow removal based on context). Include: season dates, exact services per visit, frequency, pricing structure, cancellation pro-rate language, trigger conditions (if snow), and all standard terms. Use Nebraska market rates if pricing is missing.\n\n' + ctx;
      }
    },
    proposal: {
      label: 'Business Proposal',
      icon: '💼',
      prompt: function(ctx) {
        return 'Write a polished business proposal for the services described. Include: executive summary, why Watts Safety Installs, detailed scope and pricing, timeline, credentials (NE Lic. #54690-25), and a clear call-to-action. This should be persuasive AND professional — something a property manager or business owner would take seriously.\n\n' + ctx;
      }
    },
    risks: {
      label: 'Risk Analysis',
      icon: '⚠️',
      prompt: function(ctx) {
        return 'Analyze this contract for risks. For each risk:\n1. What is the risk\n2. Likelihood and severity\n3. Exact protective clause language to add\n\nBe specific. Flag anything that could expose Justin to unpaid work, unlimited liability, or legal disputes.\n\n' + ctx;
      }
    },
    clauses: {
      label: 'Clause Library',
      icon: '📚',
      prompt: function(ctx) {
        var type = window._contractType || 'service';
        return 'Give me a clause library for a ' + type + ' contract. For each important clause, provide:\n1. The clause name\n2. 2-3 versions (standard / contractor-friendly / client-friendly)\n3. When to use each version\n\nInclude: payment, termination, liability cap, warranty, change orders, lien waiver, materials, force majeure, and dispute resolution.\n\n' + ctx;
      }
    },
    pricing: {
      label: 'Price It For Me',
      icon: '💰',
      prompt: function(ctx) {
        var type = window._contractType || 'service';
        return 'Based on the services described, give me realistic Nebraska 2025 pricing for this ' + type + ' contract. Show:\n1. Per-visit / per-hour / per-month breakdown\n2. Annual value\n3. Low / mid / premium tiers\n4. What competitors in Norfolk NE area would charge\n5. My recommended pricing with reasoning\n\nBold all numbers. Show all math.\n\n' + ctx;
      }
    },
    terms: {
      label: 'Explain Terms',
      icon: '🎓',
      prompt: function(ctx) {
        return 'Explain the key terms in this contract in plain English — what they mean for Justin as the contractor, what could go wrong, and what to watch out for. Focus on any terms that are unusual, risky, or worth negotiating.\n\n' + ctx;
      }
    }
  };

  /* ================================================================
     MARKDOWN RENDERER
     ================================================================ */
  function renderMd(text) {
    var h = text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    h = h.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="cai-pre"><code>$2</code></pre>');
    h = h.replace(/((?:^\|.+\|$\n?)+)/gm, function(tbl) {
      var rows = tbl.trim().split('\n');
      var out = '<table class="cai-tbl">'; var isHdr = true;
      rows.forEach(function(row) {
        if (row.match(/^\|[\s\-:]+\|$/)) { isHdr = false; return; }
        var cells = row.split('|').filter(function(c) { return c.trim() !== ''; });
        var tag = isHdr ? 'th' : 'td';
        out += '<tr>' + cells.map(function(c) { return '<' + tag + '>' + c.trim() + '</' + tag + '>'; }).join('') + '</tr>';
        if (isHdr) isHdr = false;
      });
      return out + '</table>';
    });
    h = h.replace(/^#### (.+)$/gm,'<h4 class="cai-h">$1</h4>');
    h = h.replace(/^### (.+)$/gm,'<h3 class="cai-h">$1</h3>');
    h = h.replace(/^## (.+)$/gm,'<h2 class="cai-h">$1</h2>');
    h = h.replace(/^# (.+)$/gm,'<h1 class="cai-h">$1</h1>');
    h = h.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
    h = h.replace(/\*(.+?)\*/g,'<em>$1</em>');
    h = h.replace(/`([^`]+)`/g,'<code class="cai-ic">$1</code>');
    h = h.replace(/^- \[x\] (.+)$/gm,'<div class="cai-cb done">☑ $1</div>');
    h = h.replace(/^- \[ \] (.+)$/gm,'<div class="cai-cb">☐ $1</div>');
    h = h.replace(/^(\d+)\. (.+)$/gm,'<div class="cai-oli"><span class="cai-oln">$1.</span> $2</div>');
    h = h.replace(/^[-•] (.+)$/gm,'<div class="cai-li">• $1</div>');
    h = h.replace(/^⚠️ (.+)$/gm,'<div class="cai-warn">⚠️ $1</div>');
    h = h.replace(/^---$/gm,'<hr class="cai-hr">');
    h = h.replace(/\n\n/g,'<div class="cai-gap"></div>');
    h = h.replace(/\n/g,'<br>');
    return h;
  }

  /* ================================================================
     STYLES
     ================================================================ */
  function injectStyles() {
    var css = document.createElement('style');
    css.textContent =
      /* Toggle btn */
      '#cai-toggle{position:fixed;bottom:24px;right:20px;width:58px;height:58px;border-radius:16px;border:none;cursor:pointer;z-index:9990;display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 4px 24px rgba(139,92,246,0.5);background:linear-gradient(135deg,#6d28d9,#8b5cf6);color:#fff;transition:all 0.3s}' +
      '#cai-toggle:hover{transform:scale(1.08);box-shadow:0 8px 32px rgba(139,92,246,0.6)}' +

      /* Panel */
      '#cai-panel{position:fixed;bottom:94px;right:20px;width:560px;height:660px;background:#080e1a;border:1px solid #1a2540;border-radius:18px;z-index:9991;display:none;flex-direction:column;box-shadow:0 16px 60px rgba(0,0,0,0.7);overflow:hidden;font-family:"Segoe UI",system-ui,sans-serif;transition:all 0.3s ease}' +
      '#cai-panel.open{display:flex}' +
      '#cai-panel.expanded{top:10px;left:10px;right:10px;bottom:10px;width:auto;height:auto;border-radius:14px}' +

      /* Header */
      '#cai-hdr{padding:12px 16px;background:linear-gradient(135deg,#150d2e,#1e0f40);border-bottom:1px solid #2d1b69;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}' +
      '#cai-hdr h4{color:#fff;font-size:15px;font-weight:700;margin:0;display:flex;align-items:center;gap:8px}' +
      '#cai-hdr h4 span{background:linear-gradient(135deg,#a78bfa,#c4b5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}' +
      '.cai-model{font-size:9px;color:#6d28d9;font-weight:700;background:#150d2e;padding:3px 8px;border-radius:6px;border:1px solid #2d1b69}' +
      '#cai-hdr-btns{display:flex;gap:4px}' +
      '.cai-hbtn{background:none;border:1px solid #2d1b69;color:#6d28d9;width:30px;height:30px;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;transition:all 0.2s}' +
      '.cai-hbtn:hover{border-color:#8b5cf6;color:#a78bfa}' +

      /* Actions */
      '#cai-acts{padding:8px 10px;display:flex;gap:6px;overflow-x:auto;border-bottom:1px solid #1a2540;background:#050a14;flex-shrink:0;scrollbar-width:none}' +
      '#cai-acts::-webkit-scrollbar{display:none}' +
      '.cai-act{background:#0d1929;border:1px solid #1a2540;color:#6b7a8d;padding:7px 11px;border-radius:10px;font-size:11px;font-weight:600;cursor:pointer;transition:all 0.2s;white-space:nowrap;flex-shrink:0}' +
      '.cai-act:hover{border-color:#8b5cf6;color:#a78bfa;background:#130d26}' +

      /* Messages */
      '#cai-msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:14px;scroll-behavior:smooth}' +
      '#cai-msgs::-webkit-scrollbar{width:5px}' +
      '#cai-msgs::-webkit-scrollbar-thumb{background:#1a2540;border-radius:3px}' +

      /* User msg */
      '.cai-msg.user{background:linear-gradient(135deg,#5b21b6,#7c3aed);color:#fff;align-self:flex-end;max-width:82%;padding:11px 15px;border-radius:16px 16px 4px 16px;font-size:13px;line-height:1.6;word-wrap:break-word}' +

      /* Bot msg */
      '.cai-msg.bot{background:#0c1726;color:#c8d4e0;align-self:flex-start;max-width:96%;padding:18px 22px;border-radius:16px 16px 16px 4px;font-size:13.5px;line-height:1.8;word-wrap:break-word;border:1px solid #1a2540}' +
      '.cai-msg.bot .cai-h{margin:12px 0 6px;line-height:1.3}' +
      '.cai-msg.bot h1{font-size:17px;color:#e2e8f0}' +
      '.cai-msg.bot h2{font-size:15px;color:#a78bfa}' +
      '.cai-msg.bot h3{font-size:14px;color:#c4b5fd}' +
      '.cai-msg.bot h4{font-size:13px;color:#34d399}' +
      '.cai-msg.bot strong{color:#c4b5fd}' +
      '.cai-msg.bot em{color:#a78bfa}' +
      '.cai-msg.bot .cai-ic{background:#150d2e;color:#fbbf24;padding:1px 5px;border-radius:4px;font-size:12px;font-family:monospace}' +
      '.cai-msg.bot .cai-pre{background:#0a1222;border:1px solid #1a2540;border-radius:8px;padding:12px;overflow-x:auto;margin:8px 0}' +
      '.cai-msg.bot .cai-pre code{background:none;padding:0;color:#a5b4fc;font-family:monospace;font-size:12px}' +
      '.cai-msg.bot .cai-li,.cai-msg.bot .cai-oli{padding:2px 0 2px 4px}' +
      '.cai-msg.bot .cai-oln{color:#a78bfa;font-weight:700;margin-right:4px}' +
      '.cai-msg.bot .cai-cb{padding:2px 0}' +
      '.cai-msg.bot .cai-cb.done{color:#34d399}' +
      '.cai-msg.bot .cai-warn{background:rgba(245,158,11,0.08);border-left:3px solid #f59e0b;padding:6px 10px;margin:4px 0;border-radius:0 6px 6px 0;color:#fcd34d}' +
      '.cai-msg.bot .cai-hr{border:none;border-top:1px solid #1a2540;margin:10px 0}' +
      '.cai-msg.bot .cai-gap{height:10px}' +
      '.cai-msg.bot .cai-tbl{width:100%;border-collapse:collapse;margin:8px 0;font-size:12px}' +
      '.cai-msg.bot .cai-tbl th{background:#150d2e;color:#a78bfa;text-align:left;padding:6px 10px;border:1px solid #2d1b69;font-weight:700}' +
      '.cai-msg.bot .cai-tbl td{padding:5px 10px;border:1px solid #1a2540}' +

      /* Typing */
      '.cai-typing{display:flex;gap:5px;padding:12px 16px;align-self:flex-start}' +
      '.cai-typing span{width:7px;height:7px;background:#8b5cf6;border-radius:50%;animation:caiDot 1.2s infinite}' +
      '.cai-typing span:nth-child(2){animation-delay:0.2s}' +
      '.cai-typing span:nth-child(3){animation-delay:0.4s}' +
      '@keyframes caiDot{0%,80%,100%{opacity:.3;transform:scale(.8)}40%{opacity:1;transform:scale(1.2)}}' +
      '.cai-timer{font-size:10px;color:#4a5568;text-align:center;padding:4px}' +

      /* Input */
      '#cai-irow{padding:10px 14px;border-top:1px solid #1a2540;display:flex;gap:8px;background:#050a14;flex-shrink:0;align-items:flex-end}' +
      '#cai-in{flex:1;background:#0d1929;border:1px solid #1a2540;border-radius:12px;padding:12px 16px;color:#eee;font-size:13px;font-family:inherit;outline:none;resize:none;min-height:44px;max-height:160px;line-height:1.5}' +
      '#cai-in:focus{border-color:#8b5cf6;box-shadow:0 0 0 2px rgba(139,92,246,0.15)}' +
      '#cai-in::placeholder{color:#3a4558}' +
      '#cai-send{background:linear-gradient(135deg,#6d28d9,#8b5cf6);border:none;color:#fff;width:44px;height:44px;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;transition:all 0.2s;flex-shrink:0}' +
      '#cai-send:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(139,92,246,0.4)}' +
      '#cai-send:disabled{opacity:0.4;cursor:default;transform:none;box-shadow:none}' +
      '#cai-attach{background:#0d1929;border:1px solid #1a2540;color:#6b7a8d;width:44px;height:44px;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;transition:all 0.2s;flex-shrink:0}' +
      '#cai-attach:hover{border-color:#8b5cf6;color:#a78bfa}' +
      '#cai-attach.has-doc{border-color:#6d28d9;color:#a78bfa;background:#130d26}' +
      '#cai-doc-preview{padding:6px 14px 0;background:#050a14;display:none;gap:6px;flex-shrink:0;overflow-x:auto;flex-wrap:nowrap;scrollbar-width:thin;scrollbar-color:#1a2540 transparent}' +
      '#cai-doc-preview::-webkit-scrollbar{height:4px}' +
      '#cai-doc-preview::-webkit-scrollbar-thumb{background:#1a2540;border-radius:2px}' +
      '.cai-doc-chip{position:relative;flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:3px;cursor:default}' +
      '.cai-doc-chip img{height:52px;width:52px;border-radius:6px;border:1px solid #2d1b69;object-fit:cover}' +
      '.cai-doc-chip .chip-name{font-size:9px;color:#a78bfa;max-width:56px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:center}' +
      '.cai-doc-chip .chip-rm{position:absolute;top:-4px;right:-4px;background:#1a0533;border:1px solid #2d1b69;color:#6b7a8d;width:16px;height:16px;border-radius:50%;cursor:pointer;font-size:9px;display:flex;align-items:center;justify-content:center;line-height:1}' +
      '.cai-doc-chip .chip-rm:hover{background:#7f1d1d;color:#fca5a5;border-color:#991b1b}' +

      /* Mobile */
      '@media(max-width:600px){#cai-panel{right:6px;left:6px;width:auto;bottom:88px;height:75vh}#cai-panel.expanded{top:0;left:0;right:0;bottom:0;border-radius:0}}';
    document.head.appendChild(css);
  }

  /* ================================================================
     HTML INJECTION
     ================================================================ */
  var _open = false;
  var _expanded = false;

  function injectHTML() {
    var btn = document.createElement('button');
    btn.id = 'cai-toggle';
    btn.innerHTML = '⚖️';
    btn.title = 'Contract AI Mentor';
    btn.addEventListener('click', togglePanel);
    document.body.appendChild(btn);

    var panel = document.createElement('div');
    panel.id = 'cai-panel';

    var actBtns = '';
    Object.keys(ACTIONS).forEach(function(key) {
      var a = ACTIONS[key];
      actBtns += '<button class="cai-act" data-act="' + key + '">' + a.icon + ' ' + a.label + '</button>';
    });

    panel.innerHTML =
      '<div id="cai-hdr">' +
        '<h4>⚖️ <span>Contract</span> AI <span class="cai-model">Pro</span></h4>' +
        '<div id="cai-hdr-btns">' +
          '<button class="cai-hbtn" id="cai-expand" title="Expand">⛶</button>' +
          '<button class="cai-hbtn" id="cai-clear" title="Clear chat">🗑</button>' +
          '<button class="cai-hbtn" id="cai-close" title="Close">✕</button>' +
        '</div>' +
      '</div>' +
      '<div id="cai-acts">' + actBtns + '</div>' +
      '<div id="cai-msgs"></div>' +
      '<div id="cai-doc-preview"></div>' +
      '<div id="cai-irow">' +
        '<button id="cai-attach" title="Attach documents (PDF or image, multiple OK)">📎</button>' +
        '<input type="file" id="cai-file-in" accept="image/*,.pdf" multiple style="display:none">' +
        '<textarea id="cai-in" placeholder="Ask me anything — or attach contracts/documents to review..." rows="1"></textarea>' +
        '<button id="cai-send">➤</button>' +
      '</div>';
    document.body.appendChild(panel);

    document.getElementById('cai-close').addEventListener('click', togglePanel);
    document.getElementById('cai-attach').addEventListener('click', function() {
      document.getElementById('cai-file-in').click();
    });
    document.getElementById('cai-file-in').addEventListener('change', function(e) {
      if (e.target.files && e.target.files.length) {
        Array.from(e.target.files).forEach(attachDocument);
      }
      e.target.value = '';
    });
    document.getElementById('cai-expand').addEventListener('click', function() {
      _expanded = !_expanded;
      document.getElementById('cai-panel').classList.toggle('expanded', _expanded);
      this.textContent = _expanded ? '✦' : '⛶';
    });
    document.getElementById('cai-clear').addEventListener('click', function() {
      if (!confirm('Clear conversation?')) return;
      _hist = [];
      document.getElementById('cai-msgs').innerHTML = '';
      addBotMsg('Conversation cleared. What contract do you need?');
    });
    document.getElementById('cai-send').addEventListener('click', function() {
      var inp = document.getElementById('cai-in');
      var text = inp.value.trim();
      var defaultMsg = _attachedDocs.length > 0 ? 'Please read these ' + (_attachedDocs.length > 1 ? _attachedDocs.length + ' documents' : 'document') + ' and summarize what each is, flag any risks or weak clauses, and tell me how I should handle them.' : '';
      if (text || _attachedDocs.length > 0) { sendMessage(text || defaultMsg); inp.value = ''; autoSize(inp); }
    });
    document.getElementById('cai-in').addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); document.getElementById('cai-send').click(); }
    });
    document.getElementById('cai-in').addEventListener('input', function() { autoSize(this); });

    document.querySelectorAll('.cai-act').forEach(function(b) {
      b.addEventListener('click', function() {
        var key = this.getAttribute('data-act');
        var action = ACTIONS[key];
        if (!action) return;
        var ctx = getContractContext();
        var prompt = action.prompt(ctx);
        sendMessage(prompt, true, action.icon + ' ' + action.label);
      });
    });

    // Drag-and-drop onto the panel
    panel.addEventListener('dragover', function(e) { e.preventDefault(); panel.style.outline = '2px dashed #8b5cf6'; });
    panel.addEventListener('dragleave', function() { panel.style.outline = ''; });
    panel.addEventListener('drop', function(e) {
      e.preventDefault(); panel.style.outline = '';
      var files = e.dataTransfer.files;
      if (files && files.length) {
        if (!_open) togglePanel();
        Array.from(files).forEach(function(f) {
          if (f.type.startsWith('image/') || f.type === 'application/pdf') attachDocument(f);
        });
      }
    });

    addBotMsg('**Hey Justin.** I\'m your Contract AI — your pocket lawyer.\n\nI draft complete, ready-to-sign contracts for:\n• Seasonal groundskeeping & snow removal\n• Hourly / T&M service agreements\n• Monthly maintenance retainers\n• Business proposals\n• Subcontractor agreements\n• Amendments & addendums\n\nHit a quick action above, or just tell me what you need. I\'ll draft the full document — not a template, not an outline. **The real thing.**\n\n📎 *You can also attach an existing contract, quote, or document — I\'ll read it and help you rewrite, review, or match it.*\n\n⚖️ *I give contractor-grade legal guidance. For court-level enforcement questions, consult a licensed Nebraska attorney.*');
  }

  /* ================================================================
     DOCUMENT ATTACH — supports multiple files
     ================================================================ */
  var _attachedDocs = []; // [{ dataUrl, mime, name, pages? }]

  function renderDocStrip() {
    var preview = document.getElementById('cai-doc-preview');
    var attachBtn = document.getElementById('cai-attach');
    preview.innerHTML = '';
    if (_attachedDocs.length === 0) {
      preview.style.display = 'none';
      attachBtn.classList.remove('has-doc');
      return;
    }
    preview.style.display = 'flex';
    attachBtn.classList.add('has-doc');
    _attachedDocs.forEach(function(doc, idx) {
      var chip = document.createElement('div');
      chip.className = 'cai-doc-chip';
      var img = document.createElement('img');
      img.src = doc.dataUrl;
      img.alt = doc.name;
      var rm = document.createElement('button');
      rm.className = 'chip-rm';
      rm.title = 'Remove';
      rm.textContent = '✕';
      rm.onclick = function() { _attachedDocs.splice(idx, 1); renderDocStrip(); };
      var label = document.createElement('div');
      label.className = 'chip-name';
      label.textContent = doc.name;
      chip.appendChild(img);
      chip.appendChild(rm);
      chip.appendChild(label);
      preview.appendChild(chip);
    });
  }

  function attachDocument(file) {
    if (file.type === 'application/pdf') {
      var reader = new FileReader();
      reader.onload = function(e) {
        var buf = e.target.result;
        var loadPdfJs = (typeof pdfjsLib !== 'undefined')
          ? Promise.resolve()
          : new Promise(function(res) {
              var s = document.createElement('script');
              s.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
              s.onload = function() {
                pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
                res();
              };
              document.head.appendChild(s);
            });
        loadPdfJs.then(function() {
          pdfjsLib.getDocument({ data: buf }).promise.then(function(pdf) {
            pdf.getPage(1).then(function(page) {
              var vp = page.getViewport({ scale: 2 });
              var canvas = document.createElement('canvas');
              canvas.width = vp.width;
              canvas.height = vp.height;
              page.render({ canvasContext: canvas.getContext('2d'), viewport: vp }).promise.then(function() {
                var dataUrl = canvas.toDataURL('image/png');
                _attachedDocs.push({ dataUrl: dataUrl, mime: 'image/png', name: file.name, pages: pdf.numPages });
                renderDocStrip();
              });
            });
          });
        });
      };
      reader.readAsArrayBuffer(file);
    } else {
      var reader2 = new FileReader();
      reader2.onload = function(e) {
        _attachedDocs.push({ dataUrl: e.target.result, mime: file.type || 'image/jpeg', name: file.name });
        renderDocStrip();
      };
      reader2.readAsDataURL(file);
    }
  }

  function clearAllAttachments() {
    _attachedDocs = [];
    renderDocStrip();
  }

  /* ================================================================
     CHAT FUNCTIONS
     ================================================================ */
  function autoSize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  }

  function togglePanel() {
    _open = !_open;
    document.getElementById('cai-panel').classList.toggle('open', _open);
    if (_open) document.getElementById('cai-in').focus();
  }

  function addUserMsg(text, docs) {
    var msgs = document.getElementById('cai-msgs');
    var div = document.createElement('div');
    div.className = 'cai-msg user';
    if (docs && docs.length > 0) {
      var strip = document.createElement('div');
      strip.style.cssText = 'display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px';
      docs.forEach(function(doc) {
        var wrap = document.createElement('div');
        wrap.style.cssText = 'display:flex;flex-direction:column;align-items:center;gap:2px';
        var img = document.createElement('img');
        img.src = doc.dataUrl;
        img.style.cssText = 'height:56px;width:56px;border-radius:6px;border:1px solid rgba(255,255,255,0.15);object-fit:cover';
        var lbl = document.createElement('div');
        lbl.style.cssText = 'font-size:9px;opacity:0.65;max-width:60px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:center';
        lbl.textContent = doc.name;
        wrap.appendChild(img);
        wrap.appendChild(lbl);
        strip.appendChild(wrap);
      });
      div.appendChild(strip);
    }
    var t = document.createElement('span');
    t.textContent = text;
    div.appendChild(t);
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function addBotMsg(text) {
    var msgs = document.getElementById('cai-msgs');
    var typing = msgs.querySelector('.cai-typing');
    if (typing) typing.remove();
    var timerEl = msgs.querySelector('.cai-timer');
    if (timerEl) timerEl.remove();

    var div = document.createElement('div');
    div.className = 'cai-msg bot';
    div.innerHTML = renderMd(text);

    if (text.length > 200) {
      var acts = document.createElement('div');
      acts.style.cssText = 'margin-top:10px;padding-top:8px;border-top:1px solid #1a2540;display:flex;gap:6px;flex-wrap:wrap';

      // Load into form — parse contract-json block (prefer contract-json tag over generic json)
      var jsonData = null;
      var strictMatch = text.match(/```contract-json\s*\n([\s\S]*?)```/);
      if (strictMatch) {
        try { jsonData = JSON.parse(strictMatch[1].trim()); } catch(e) {}
      }
      if (!jsonData) {
        // Fallback: last ```json block in response (not an example, the real data)
        var allJsonBlocks = [];
        var jre = /```json\s*\n([\s\S]*?)```/g;
        var jm;
        while ((jm = jre.exec(text)) !== null) allJsonBlocks.push(jm[1]);
        var lastBlock = allJsonBlocks[allJsonBlocks.length - 1];
        if (lastBlock) try { jsonData = JSON.parse(lastBlock.trim()); } catch(e) {}
      }
      if (jsonData && typeof applyAIJson === 'function') {
        var loadBtn = document.createElement('button');
        loadBtn.style.cssText = 'background:linear-gradient(135deg,#6d28d9,#8b5cf6);border:none;color:#fff;padding:5px 12px;border-radius:6px;font-size:11px;cursor:pointer;font-weight:700';
        loadBtn.textContent = '📥 Load & Regenerate';
        loadBtn.onclick = function() {
          applyAIJson(jsonData);
          if (typeof generateContract === 'function') generateContract();
          loadBtn.textContent = '✅ Applied!';
          loadBtn.style.background = '#27ae60';
          // Re-enable after 2s so user can reload if they keep refining
          setTimeout(function() {
            loadBtn.textContent = '📥 Load & Regenerate';
            loadBtn.style.background = 'linear-gradient(135deg,#6d28d9,#8b5cf6)';
          }, 2000);
        };
        acts.appendChild(loadBtn);
      }

      // Copy
      var copyBtn = document.createElement('button');
      copyBtn.style.cssText = 'background:#0d1929;border:1px solid #1a2540;color:#6b7a8d;padding:5px 10px;border-radius:6px;font-size:11px;cursor:pointer';
      copyBtn.textContent = '📋 Copy';
      copyBtn.onclick = function() {
        navigator.clipboard.writeText(text).then(function() {
          copyBtn.textContent = '✅ Copied!';
          setTimeout(function() { copyBtn.textContent = '📋 Copy'; }, 2000);
        });
      };
      acts.appendChild(copyBtn);

      // Email
      var emailBtn = document.createElement('button');
      emailBtn.style.cssText = 'background:#0d1929;border:1px solid #1a2540;color:#6b7a8d;padding:5px 10px;border-radius:6px;font-size:11px;cursor:pointer';
      emailBtn.textContent = '✉️ Email';
      emailBtn.onclick = function() {
        var sub = 'Watts Safety Installs — Contract';
        var body = text.replace(/\*\*/g,'').replace(/#{1,4}\s/g,'');
        window.open('mailto:?subject=' + encodeURIComponent(sub) + '&body=' + encodeURIComponent(body));
      };
      acts.appendChild(emailBtn);

      div.appendChild(acts);
    }

    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function showTyping() {
    var msgs = document.getElementById('cai-msgs');
    var d = document.createElement('div');
    d.className = 'cai-typing';
    d.innerHTML = '<span></span><span></span><span></span>';
    msgs.appendChild(d);

    var timerDiv = document.createElement('div');
    timerDiv.className = 'cai-timer';
    timerDiv.textContent = 'Thinking...';
    msgs.appendChild(timerDiv);
    var start = Date.now();
    timerDiv._interval = setInterval(function() {
      var secs = Math.round((Date.now() - start) / 1000);
      timerDiv.textContent = 'Drafting... ' + secs + 's';
    }, 1000);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function clearTimer() {
    var msgs = document.getElementById('cai-msgs');
    var el = msgs.querySelector('.cai-timer');
    if (el && el._interval) clearInterval(el._interval);
  }

  /* ================================================================
     SEND MESSAGE
     ================================================================ */
  var _busy = false;

  function sendMessage(text, isAction, actionLabel) {
    if (_busy) return;
    _busy = true;
    document.getElementById('cai-send').disabled = true;
    if (!_open) togglePanel();

    // Snapshot attached docs before clearing
    var docsSnap = _attachedDocs.slice();
    if (isAction && actionLabel) {
      addUserMsg(actionLabel, []);
    } else {
      addUserMsg(text, docsSnap);
    }
    showTyping();

    var fullMsg = text;
    if (!isAction) {
      var ctx = getContractContext();
      if (ctx) fullMsg = text + '\n\n[Current Contract Form Data]\n' + ctx;
    }

    // If a contract has already been generated, append its plain-text so AI can revise it
    var docWrapper = document.querySelector('#docOut .doc-wrapper');
    if (docWrapper) {
      var docText = docWrapper.innerText || '';
      if (docText && docText.length > 100) {
        fullMsg += '\n\n[Currently Generated Contract — Plain Text]\n' + docText.substring(0, 6000);
      }
    }

    // Build parts array — text first, then all attached images
    var parts = [{ text: fullMsg }];
    docsSnap.forEach(function(doc) {
      var b64 = doc.dataUrl.replace(/^data:[^;]+;base64,/, '');
      parts.push({ inline_data: { mime_type: doc.mime, data: b64 } });
    });
    if (docsSnap.length > 0) clearAllAttachments();

    _hist.push({ role: 'user', parts: parts });
    if (_hist.length > 40) _hist = _hist.slice(0, 2).concat(_hist.slice(-38));

    callAI(_hist).then(function(reply) {
      clearTimer();
      addBotMsg(reply);
      _hist.push({ role: 'model', parts: [{ text: reply }] });
    }).catch(function(err) {
      clearTimer();
      addBotMsg('**Connection issue.** ' + (err.name === 'AbortError' ? 'Request timed out. Try a shorter question or check your internet.' : 'Error: ' + err.message + '. Try again.'));
    }).finally(function() {
      _busy = false;
      document.getElementById('cai-send').disabled = false;
    });
  }

  /* ================================================================
     INIT
     ================================================================ */
  function init() {
    injectStyles();
    injectHTML();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
