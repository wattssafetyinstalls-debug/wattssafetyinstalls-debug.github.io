// =====================================================================
// FINAL INVOICE AI MENTOR - Smart invoice generation with JSON output
// Mirrors BidGen AI Mentor capabilities for final invoice workflow
// =====================================================================
(function() {
'use strict';

// Configuration
var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
var MODEL = 'gemini-2.5-pro';
var TIMEOUT = 120000; // 2 minutes

// System instructions for Final Invoice AI
var SYS = [
  'You are the Final Invoice AI Mentor for Watts Safety Installs. Your job is to generate professional final invoices with COMPLETE, VALID JSON data.',
  '',
  'CRITICAL: EVERY RESPONSE MUST INCLUDE VALID JSON',
  '- You MUST ALWAYS include a complete ```final-invoice-json block',
  '- The JSON MUST be valid and loadable into the Final Invoice Builder',
  '- NEVER give text-only responses - ALWAYS provide JSON',
  '- Use the provided invoice/project data to fill ALL fields',
  '',
  'REQUIRED JSON STRUCTURE:',
  '```final-invoice-json',
  '{',
  '  "invoiceNumber": "WSI-2026-0001",',
  '  "invoiceDate": "2026-04-07",',
  '  "dueDate": "2026-04-21",',
  '  "status": "sent",',
  '  "clientName": "Client Name from data",',
  '  "clientAddress": "Full client address",',
  '  "clientPhone": "402-xxx-xxxx",',
  '  "clientEmail": "client@email.com",',
  '  "projectName": "Project name from data",',
  '  "projectAddress": "Project address",',
  '  "lineItems": [',
  '    {',
  '      "description": "Labor/Item description",',
  '      "quantity": 1,',
  '      "unit": "ea",',
  '      "price": 150.00,',
  '      "total": 150.00',
  '    }',
  '  ],',
  '  "subtotal": 150.00,',
  '  "tax": 10.50,',
  '  "total": 160.50,',
  '  "paymentTerms": "Due within 14 days. Late payments subject to 1.5% monthly fee.",',
  '  "notes": "Project notes and warranty information",',
  '  "warranty": "1-year workmanship warranty",',
  '  "changeOrders": []',
  '}',
  '```',
  '',
  'DATA SOURCES TO USE:',
  '- Current invoice data (if available)',
  '- Project context from BidGen',
  '- Client information from database',
  '- Invoice numbers you provide',
  '- Any specific details you mention',
  '',
  'RULES:',
  '1. Extract ALL available data from the context',
  '2. Fill EVERY field in the JSON structure',
  '3. Calculate totals (subtotal + 7% tax = total)',
  '4. Use real data, never placeholders like "Client Name"',
  '5. If data is missing, ask for it or use reasonable defaults',
  '6. ALWAYS include the complete JSON block',
  '',
  'I will NEVER give incomplete responses. Every response includes the full JSON block ready to load.'
].join('\n');

// Chat history
var _hist = [];

// =====================================================================
// API CALL with retry logic
// =====================================================================
function callAI(messages, attempt) {
  attempt = attempt || 1;
  var MAX_RETRIES = 3;
  var controller = new AbortController();
  var timer = setTimeout(function() { controller.abort(); }, TIMEOUT);

  var contents = [];
  contents.push({ role: 'user', parts: [{ text: 'System Instructions:\n\n' + SYS }] });
  contents.push({ role: 'model', parts: [{ text: 'Ready. I\\'m your Final Invoice AI Mentor — I generate complete, professional final invoices with full JSON data ready to load into the Final Invoice Builder. I will NEVER give incomplete responses.' }] });
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
    // Retry on 503 or 500 errors
    if (!r.ok && (r.status === 503 || r.status === 500) && attempt < MAX_RETRIES) {
      var delay = Math.min(1000 * Math.pow(2, attempt - 1), 4000);
      console.log('[Final Invoice AI] Retry ' + attempt + '/' + MAX_RETRIES + ' after ' + delay + 'ms (status ' + r.status + ')');
      return new Promise(function(resolve) {
        setTimeout(function() {
          resolve(callAI(messages, attempt + 1));
        }, delay);
      });
    }
    if (!r.ok) throw new Error('API ' + r.status);
    return r.json();
  }).then(function(data) {
    if (data.error) throw new Error(data.error);
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
    // Don't retry on abort (timeout) or if we've exhausted retries
    if (err.name === 'AbortError' || attempt >= MAX_RETRIES) {
      throw err;
    }
    // Retry on network errors
    var delay = Math.min(1000 * Math.pow(2, attempt - 1), 4000);
    console.log('[Final Invoice AI] Retry ' + attempt + '/' + MAX_RETRIES + ' after error: ' + err.message);
    return new Promise(function(resolve, reject) {
      setTimeout(function() {
        callAI(messages, attempt + 1).then(resolve).catch(reject);
      }, delay);
    });
  });
}

// =====================================================================
// CONTEXT GATHERING - reads Final Invoice state and Firebase data
// =====================================================================
function getFinalInvoiceContext() {
  return new Promise(function(resolve) {
    var ctx = '';
    
    // Get current invoice data if available
    if (typeof getCurrentInvoice === 'function') {
      var invoice = getCurrentInvoice();
      if (invoice) {
        ctx += '\n## CURRENT FINAL INVOICE DATA\n';
        ctx += 'Invoice #: ' + (invoice.invoiceNumber || 'Not set') + '\n';
        ctx += 'Client: ' + (invoice.clientName || 'Not set') + '\n';
        ctx += 'Date: ' + (invoice.invoiceDate || 'Not set') + '\n';
        ctx += 'Due Date: ' + (invoice.dueDate || 'Not set') + '\n';
        ctx += 'Status: ' + (invoice.status || 'Draft') + '\n';
        
        if (invoice.lineItems && invoice.lineItems.length > 0) {
          ctx += '\nLine Items:\n';
          invoice.lineItems.forEach(function(item, i) {
            ctx += (i + 1) + '. ' + item.description + ' - ' + item.quantity + ' ' + item.unit + ' x $' + item.price + ' = $' + item.total + '\n';
          });
        }
        
        ctx += 'Subtotal: $' + (invoice.subtotal || '0') + '\n';
        ctx += 'Tax: $' + (invoice.tax || '0') + '\n';
        ctx += 'Total: $' + (invoice.total || '0') + '\n';
      }
    }

    // Get project context from BidGen if available
    if (typeof getProjectContext === 'function') {
      var projCtx = getProjectContext();
      if (projCtx) {
        ctx += '\n## PROJECT CONTEXT\n' + projCtx;
      }
    }

    // Get client information
    if (typeof getClientInfo === 'function') {
      var client = getClientInfo();
      if (client) {
        ctx += '\n## CLIENT INFORMATION\n';
        ctx += 'Name: ' + (client.name || '') + '\n';
        ctx += 'Address: ' + (client.address || '') + '\n';
        ctx += 'Phone: ' + (client.phone || '') + '\n';
        ctx += 'Email: ' + (client.email || '') + '\n';
      }
    }

    // Get change orders if any
    if (typeof getChangeOrders === 'function') {
      var cos = getChangeOrders();
      if (cos && cos.length > 0) {
        ctx += '\n## CHANGE ORDERS\n';
        cos.forEach(function(co, i) {
          ctx += 'CO' + (i + 1) + ': ' + co.description + ' - $' + co.amount + '\n';
        });
      }
    }

    // Add localStorage project data if available
    var projectData = localStorage.getItem('bidgen_project_context');
    if (projectData) {
      try {
        var proj = JSON.parse(projectData);
        ctx += '\n## LOCAL PROJECT DATA\n';
        if (proj.clientName) ctx += 'Client: ' + proj.clientName + '\n';
        if (proj.complexName) ctx += 'Complex: ' + proj.complexName + '\n';
        if (proj.unitNum) ctx += 'Unit: ' + proj.unitNum + '\n';
        if (proj.jobCity) ctx += 'City: ' + proj.jobCity + '\n';
        if (proj.sqft) ctx += 'SQFT: ' + proj.sqft + '\n';
        if (proj.scopeTitle) ctx += 'Scope: ' + proj.scopeTitle + '\n';
        if (proj.laborItems && proj.laborItems.length > 0) {
          ctx += 'Labor Items (' + proj.laborItems.length + '):\n';
          proj.laborItems.forEach(function(item, i) {
            ctx += '  ' + (i+1) + '. ' + item.desc + ' - ' + item.qty + ' ' + item.basis + ' x $' + item.price + '\n';
          });
        }
        if (proj.matItems && proj.matItems.length > 0) {
          ctx += 'Material Items (' + proj.matItems.length + '):\n';
          proj.matItems.forEach(function(item, i) {
            ctx += '  ' + (i+1) + '. ' + item.desc + ' - ' + item.qty + ' ' + item.unit + ' x $' + item.price + '\n';
          });
        }
      } catch(e) {
        console.error('Failed to parse local project data:', e);
      }
    }

    // NEW: Fetch invoice data from Firebase if invoice numbers are mentioned in chat
    var chatText = _hist.map(function(m) { return m.parts[0].text; }).join(' ').toLowerCase();
    var invoiceMatches = chatText.match(/wsi-\d{4}-\d{4,}/gi) || chatText.match(/invoice\s+#?\s*\w+/gi);
    
    if (invoiceMatches && typeof db !== 'undefined' && typeof userPIN !== 'undefined') {
      ctx += '\n## FETCHING INVOICE DATA FROM FIREBASE\n';
      ctx += 'Found invoice references: ' + invoiceMatches.join(', ') + '\n';
      
      // Hash the PIN for Firebase path
      var hashedPIN = (typeof hashPIN === 'function') ? hashPIN(userPIN) : '';
      
      // Create array of promises for all Firebase fetches
      var fetchPromises = [];
      
      invoiceMatches.forEach(function(invNum) {
        // Clean up invoice number
        var cleanInv = invNum.replace(/[^a-z0-9-]/gi, '').toUpperCase();
        ctx += '\n--- Invoice: ' + cleanInv + ' ---\n';
        ctx += 'Invoice ID: ' + cleanInv + '\n';
        
        // Try to fetch from different Firebase paths
        var paths = [
          'invoices/' + hashedPIN + '/awarded/' + cleanInv,
          'invoices/' + hashedPIN + '/permanent/' + cleanInv,
          'invoices/' + hashedPIN + '/sent/' + cleanInv,
          'invoices/' + hashedPIN + '/' + cleanInv
        ];
        
        paths.forEach(function(path) {
          var promise = db.ref(path).once('value').then(function(snap) {
            if (snap.exists()) {
              var data = snap.val();
              var invCtx = '\nFound at path: ' + path + '\n';
              if (data.clientName) invCtx += 'Client: ' + data.clientName + '\n';
              if (data.projectName) invCtx += 'Project: ' + data.projectName + '\n';
              if (data.projectAddress) invCtx += 'Address: ' + data.projectAddress + '\n';
              if (data.estimateDate) invCtx += 'Date: ' + data.estimateDate + '\n';
              if (data.totalCost) invCtx += 'Total: $' + data.totalCost + '\n';
              if (data.laborTotal) invCtx += 'Labor: $' + data.laborTotal + '\n';
              if (data.materialTotal) invCtx += 'Materials: $' + data.materialTotal + '\n';
              if (data.scopeTitle) invCtx += 'Scope: ' + data.scopeTitle + '\n';
              
              // Add line items
              if (data.laborItems && data.laborItems.length > 0) {
                invCtx += 'Labor Items:\n';
                data.laborItems.forEach(function(item, i) {
                  invCtx += '  ' + (i+1) + '. ' + item.desc + ' - ' + item.qty + ' ' + item.basis + ' x $' + item.price + '\n';
                });
              }
              if (data.matItems && data.matItems.length > 0) {
                invCtx += 'Material Items:\n';
                data.matItems.forEach(function(item, i) {
                  invCtx += '  ' + (i+1) + '. ' + item.desc + ' - ' + item.qty + ' ' + item.unit + ' x $' + item.price + '\n';
                });
              }
              return invCtx;
            }
            return '';
          }).catch(function(err) {
            console.error('Failed to fetch from ' + path + ':', err);
            return '';
          });
          fetchPromises.push(promise);
        });
      });
      
      // Wait for all Firebase fetches to complete
      Promise.all(fetchPromises).then(function(results) {
        // Append all fetched data to context
        results.forEach(function(result) {
          if (result) ctx += result;
        });
        console.log('[Final Invoice AI] Firebase data fetched, context length:', ctx.length);
        resolve(ctx);
      }).catch(function(err) {
        console.error('[Final Invoice AI] Error fetching Firebase data:', err);
        resolve(ctx);
      });
    } else {
      // No Firebase fetches needed, resolve immediately
      resolve(ctx);
    }
  });
}

// =====================================================================
// QUICK ACTIONS - smart, context-aware prompts
// =====================================================================
var ACTIONS = {
  generate: {
    label: 'Generate Final Invoice',
    icon: '📝',
    prompt: function(ctx) {
      return 'Generate a complete final invoice with VALID JSON. Use all available data from context.\n\n' +
        'CRITICAL: You MUST include a complete ```final-invoice-json block with ALL fields filled:\n' +
        '- invoiceNumber (use WSI-2026-XXXX format)\n' +
        '- invoiceDate (today: ' + new Date().toISOString().split('T')[0] + ')\n' +
        '- dueDate (14 days from today)\n' +
        '- clientName, clientAddress, clientPhone, clientEmail\n' +
        '- projectName, projectAddress\n' +
        '- lineItems array with description, quantity, unit, price, total\n' +
        '- subtotal, tax (7%), total calculations\n' +
        '- paymentTerms, notes, warranty\n\n' +
        'USE REAL DATA from the context. NO PLACEHOLDERS.\n\n' +
        'Context data:\n' + ctx + '\n\n' +
        'REQUIREMENT: End your response with the complete JSON block.';
    }
  },
  convert: {
    label: 'Convert Estimate to Invoice',
    icon: '�',
    prompt: function(ctx) {
      return 'Convert the estimate/bid data to a final invoice with VALID JSON.\n\n' +
        'STEPS:\n' +
        '1. Change estimate language to invoice language\n' +
        '2. Add actual dates (today: ' + new Date().toISOString().split('T')[0] + ')\n' +
        '3. Generate sequential invoice number\n' +
        '4. Include all labor and material items\n' +
        '5. Calculate totals with 7% tax\n' +
        '6. Add payment terms (Net 14)\n' +
        '7. Include warranty info\n\n' +
        'CRITICAL: MUST include complete ```final-invoice-json block.\n\n' +
        'Context:\n' + ctx;
    }
  },
  addChangeOrder: {
    label: 'Add Change Order',
    icon: '📝',
    prompt: function(ctx) {
      return 'Add a change order to the final invoice and generate UPDATED JSON.\n\n' +
        'Ask me for:\n' +
        '1. Change order description\n' +
        '2. Additional labor/materials with costs\n' +
        '3. Reason for change\n\n' +
        'Then generate the complete final invoice JSON including:\n' +
        '- Updated line items with change order\n' +
        '- Recalculated totals\n' +
        '- Change order in the changeOrders array\n\n' +
        'CRITICAL: MUST include complete ```final-invoice-json block.\n\n' +
        'Current context:\n' + ctx;
    }
  },
  payment: {
    label: 'Payment Schedule',
    icon: '�',
    prompt: function(ctx) {
      return 'Create a payment schedule for the final invoice with VALID JSON.\n\n' +
        'Include:\n' +
        '- Total project cost from context\n' +
        '- Payment milestones (e.g., 50% deposit, 50% completion)\n' +
        '  * Payment 1: 50% due on ' + new Date().toISOString().split('T')[0] + '\n' +
        '  * Payment 2: 50% due on completion\n' +
        '- Late payment fee (1.5% monthly)\n' +
        '- Accepted payment methods\n\n' +
        'Generate complete final invoice JSON with payment schedule in paymentTerms field.\n\n' +
        'CRITICAL: MUST include complete ```final-invoice-json block.\n\n' +
        'Context:\n' + ctx;
    }
  },
  review: {
    label: 'Invoice Review',
    icon: '🔍',
    prompt: function(ctx) {
      return 'Review and fix the final invoice, then provide CORRECTED JSON.\n\n' +
        'CHECKLIST:\n' +
        '✓ All required fields filled\n' +
        '✓ Calculations are correct (subtotal + 7% tax = total)\n' +
        '✓ Professional language\n' +
        '✓ Payment terms are clear\n' +
        '✓ Warranty information included\n' +
        '✓ No placeholder text\n\n' +
        'If issues found, provide corrected invoice with complete JSON.\n\n' +
        'CRITICAL: MUST include complete ```final-invoice-json block.\n\n' +
        'Current data:\n' + ctx;
    }
  },
  customize: {
    label: 'Custom Invoice',
    icon: '🎨',
    prompt: function(ctx) {
      return 'Create a custom final invoice based on your specific needs.\n\n' +
        'I can create:\n' +
        '- Progress invoices\n' +
        '- Partial completion invoices\n' +
        '- Final completion invoices\n' +
        '- Time and materials invoices\n' +
        '- Fixed price invoices\n\n' +
        'Tell me what you need and I\'ll generate the complete JSON.\n\n' +
        'CRITICAL: MUST include complete ```final-invoice-json block.\n\n' +
        'Available context:\n' + ctx;
    }
  }
};

// =====================================================================
// MARKDOWN RENDERER - rich formatting for AI responses
// =====================================================================
function renderMd(text) {
  // Escape HTML first
  var h = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // Code blocks
  h = h.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="fai-pre"><code>$2</code></pre>');

  // Tables
  h = h.replace(/((?:^\|.+\|$\n?)+)/gm, function(tableBlock) {
    var rows = tableBlock.trim().split('\n');
    var html = '<table class="fai-tbl">';
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
  h = h.replace(/^#### (.+)$/gm, '<h4 class="fai-h">$1</h4>');
  h = h.replace(/^### (.+)$/gm, '<h3 class="fai-h">$1</h3>');
  h = h.replace(/^## (.+)$/gm, '<h2 class="fai-h">$1</h2>');
  h = h.replace(/^# (.+)$/gm, '<h1 class="fai-h">$1</h1>');

  // Bold & italic
  h = h.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  h = h.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Inline code
  h = h.replace(/`([^`]+)`/g, '<code class="fai-ic">$1</code>');

  // Checkboxes
  h = h.replace(/^- \[x\] (.+)$/gm, '<div class="fai-cb done">☑ $1</div>');
  h = h.replace(/^- \[ \] (.+)$/gm, '<div class="fai-cb">☐ $1</div>');

  // Numbered lists
  h = h.replace(/^(\d+)\. (.+)$/gm, '<div class="fai-oli"><span class="fai-oln">$1.</span> $2</div>');

  // Bullet lists
  h = h.replace(/^[-\u2022] (.+)$/gm, '<div class="fai-li">• $1</div>');

  // Horizontal rules
  h = h.replace(/^---$/gm, '<hr class="fai-hr">');

  // Paragraphs
  h = h.replace(/\n\n/g, '<div class="fai-gap"></div>');
  h = h.replace(/\n/g, '<br>');

  return h;
}

// =====================================================================
// CHAT UI - matches BidGen AI style
// =====================================================================
function injectStyles() {
  var css = document.createElement('style');
  css.textContent =
    /* Toggle button */
    '#fai-toggle{position:fixed;bottom:80px;right:20px;width:60px;height:60px;border-radius:16px;border:none;cursor:pointer;z-index:9990;display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 4px 24px rgba(239,68,68,0.5);background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;transition:all 0.3s}' +
    '#fai-toggle:hover{transform:scale(1.08);box-shadow:0 8px 32px rgba(239,68,68,0.6)}' +

    /* Panel */
    '#fai-panel{position:fixed;bottom:80px;right:20px;width:540px;height:640px;background:#1a1a1a;border:1px solid #333;border-radius:18px;z-index:9991;display:none;flex-direction:column;box-shadow:0 16px 60px rgba(0,0,0,0.6);overflow:hidden;font-family:"Segoe UI",system-ui,sans-serif;transition:all 0.3s ease}' +
    '#fai-panel.open{display:flex}' +
    '#fai-panel.expanded{top:10px;left:10px;right:10px;bottom:10px;width:auto;height:auto;border-radius:14px}' +

    /* Header */
    '#fai-hdr{padding:12px 16px;background:linear-gradient(135deg,#dc2626,#991b1b);border-bottom:1px solid #333;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}' +
    '#fai-hdr h4{color:#fff;font-size:15px;font-weight:700;margin:0;display:flex;align-items:center;gap:8px}' +
    '#fai-hdr h4 span{background:linear-gradient(135deg,#ef4444,#f87171);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}' +
    '.fai-model{font-size:9px;color:#999;font-weight:600;background:#0d0d0d;padding:3px 8px;border-radius:6px;border:1px solid #333}' +
    '#fai-hdr-btns{display:flex;gap:4px}' +
    '.fai-hbtn{background:none;border:1px solid #333;color:#999;width:30px;height:30px;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;transition:all 0.2s}' +
    '.fai-hbtn:hover{border-color:#ef4444;color:#ef4444}' +

    /* Actions bar */
    '#fai-acts{padding:8px 12px;display:flex;gap:6px;overflow-x:auto;border-bottom:1px solid #333;background:#0d0d0d;flex-shrink:0;scrollbar-width:none;-ms-overflow-style:none}' +
    '#fai-acts::-webkit-scrollbar{display:none}' +
    '.fai-act{background:#1a1a1a;border:1px solid #333;color:#999;padding:7px 12px;border-radius:10px;font-size:11px;font-weight:600;cursor:pointer;transition:all 0.2s;white-space:nowrap;flex-shrink:0}' +
    '.fai-act:hover{border-color:#ef4444;color:#ef4444;background:#2a1a1a}' +

    /* Messages */
    '#fai-msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:14px;scroll-behavior:smooth}' +
    '#fai-msgs::-webkit-scrollbar{width:6px}' +
    '#fai-msgs::-webkit-scrollbar-thumb{background:#333;border-radius:4px}' +

    /* User msg */
    '.fai-msg.user{background:linear-gradient(135deg,#dc2626,#ef4444);color:#fff;align-self:flex-end;max-width:80%;padding:12px 16px;border-radius:16px 16px 4px 16px;font-size:13px;line-height:1.6;white-space:pre-wrap;word-wrap:break-word}' +

    /* Bot msg */
    '.fai-msg.bot{background:#1a1a1a;color:#e5e5e5;align-self:flex-start;max-width:95%;padding:18px 22px;border-radius:16px 16px 16px 4px;font-size:13.5px;line-height:1.8;word-wrap:break-word;border:1px solid #333}' +
    '.fai-msg.bot .fai-h{margin:12px 0 6px;line-height:1.3}' +
    '.fai-msg.bot h1{font-size:17px;color:#f87171}' +
    '.fai-msg.bot h2{font-size:15px;color:#ef4444}' +
    '.fai-msg.bot h3{font-size:14px;color:#fbbf24}' +
    '.fai-msg.bot h4{font-size:13px;color:#34d399}' +
    '.fai-msg.bot strong{color:#ef4444}' +
    '.fai-msg.bot em{color:#fbbf24}' +
    '.fai-msg.bot .fai-ic{background:#2a1a1a;color:#fbbf24;padding:1px 5px;border-radius:4px;font-size:12px;font-family:monospace}' +
    '.fai-msg.bot .fai-pre{background:#0d0d0d;border:1px solid #333;border-radius:8px;padding:12px;overflow-x:auto;margin:8px 0}' +
    '.fai-msg.bot .fai-pre code{background:none;padding:0;color:#f87171;font-family:monospace;font-size:12px}' +
    '.fai-msg.bot .fai-li,.fai-msg.bot .fai-oli{padding:2px 0 2px 4px}' +
    '.fai-msg.bot .fai-oln{color:#ef4444;font-weight:700;margin-right:4px}' +
    '.fai-msg.bot .fai-cb{padding:2px 0}' +
    '.fai-msg.bot .fai-cb.done{color:#34d399}' +
    '.fai-msg.bot .fai-hr{border:none;border-top:1px solid #333;margin:10px 0}' +
    '.fai-msg.bot .fai-gap{height:10px}' +
    '.fai-msg.bot .fai-tbl{width:100%;border-collapse:collapse;margin:8px 0;font-size:12px}' +
    '.fai-msg.bot .fai-tbl th{background:#2a1a1a;color:#ef4444;text-align:left;padding:6px 10px;border:1px solid #333;font-weight:700}' +
    '.fai-msg.bot .fai-tbl td{padding:5px 10px;border:1px solid #333}' +

    /* Typing indicator */
    '.fai-typing{display:flex;gap:5px;padding:12px 16px;align-self:flex-start}' +
    '.fai-typing span{width:7px;height:7px;background:#ef4444;border-radius:50%;animation:faiDot 1.2s infinite}' +
    '.fai-typing span:nth-child(2){animation-delay:0.2s}' +
    '.fai-typing span:nth-child(3){animation-delay:0.4s}' +
    '@keyframes faiDot{0%,80%,100%{opacity:.3;transform:scale(.8)}40%{opacity:1;transform:scale(1.2)}}' +

    /* Timer */
    '.fai-timer{font-size:10px;color:#666;text-align:center;padding:4px}' +

    /* Input area */
    '#fai-irow{padding:10px 14px;border-top:1px solid #333;display:flex;gap:8px;background:#0d0d0d;flex-shrink:0;align-items:flex-end}' +
    '#fai-in{flex:1;background:#1a1a1a;border:1px solid #333;border-radius:12px;padding:12px 16px;color:#e5e5e5;font-size:13px;font-family:inherit;outline:none;resize:none;min-height:44px;max-height:160px;line-height:1.5}' +
    '#fai-in:focus{border-color:#ef4444;box-shadow:0 0 0 2px rgba(239,68,68,0.15)}' +
    '#fai-in::placeholder{color:#666}' +
    '#fai-send{background:linear-gradient(135deg,#ef4444,#dc2626);border:none;color:#fff;width:44px;height:44px;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;transition:all 0.2s;flex-shrink:0}' +
    '#fai-send:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(239,68,68,0.3)}' +
    '#fai-send:disabled{opacity:0.4;cursor:default;transform:none;box-shadow:none}' +

    /* Mobile */
    '@media(max-width:600px){#fai-panel{right:6px;left:6px;width:auto;bottom:80px;height:75vh}#fai-panel.expanded{top:0;left:0;right:0;bottom:0;border-radius:0}}';
  document.head.appendChild(css);
}

// =====================================================================
// UI INJECTION
// =====================================================================
var _open = false;
var _expanded = false;

function injectHTML() {
  // Toggle button
  var btn = document.createElement('button');
  btn.id = 'fai-toggle';
  btn.innerHTML = '🧾';
  btn.title = 'Final Invoice AI Mentor';
  btn.addEventListener('click', togglePanel);
  document.body.appendChild(btn);

  // Panel
  var panel = document.createElement('div');
  panel.id = 'fai-panel';

  var actBtns = '';
  Object.keys(ACTIONS).forEach(function(key) {
    var a = ACTIONS[key];
    actBtns += '<button class="fai-act" data-act="' + key + '">' + a.icon + ' ' + a.label + '</button>';
  });

  panel.innerHTML =
    '<div id="fai-hdr">' +
      '<h4>🧾 <span>Final Invoice</span> AI Mentor <span class="fai-model">Gemini 2.5 Pro</span></h4>' +
      '<div id="fai-hdr-btns">' +
        '<button class="fai-hbtn" id="fai-expand" title="Expand">⛶</button>' +
        '<button class="fai-hbtn" id="fai-clear" title="Clear chat">🗑</button>' +
        '<button class="fai-hbtn" id="fai-close" title="Close">✕</button>' +
      '</div>' +
    '</div>' +
    '<div id="fai-acts">' + actBtns + '</div>' +
    '<div id="fai-msgs"></div>' +
    '<div id="fai-irow">' +
      '<textarea id="fai-in" placeholder="Describe the final invoice you need... I\\'ll generate the complete JSON to load into the Final Invoice Builder" rows="1"></textarea>' +
      '<button id="fai-send">➤</button>' +
    '</div>';
  document.body.appendChild(panel);

  // Events
  document.getElementById('fai-close').addEventListener('click', togglePanel);
  document.getElementById('fai-expand').addEventListener('click', function() {
    _expanded = !_expanded;
    document.getElementById('fai-panel').classList.toggle('expanded', _expanded);
    this.textContent = _expanded ? '◱' : '⛶';
  });
  document.getElementById('fai-clear').addEventListener('click', function() {
    if (!confirm('Clear conversation history?')) return;
    _hist = [];
    var msgs = document.getElementById('fai-msgs');
    msgs.innerHTML = '';
    addBotMsg('Conversation cleared. What final invoice would you like to generate?');
  });

  document.getElementById('fai-send').addEventListener('click', function() {
    var inp = document.getElementById('fai-in');
    var text = inp.value.trim();
    if (text) { sendMessage(text); inp.value = ''; autoSize(inp); }
  });
  document.getElementById('fai-in').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      document.getElementById('fai-send').click();
    }
  });
  document.getElementById('fai-in').addEventListener('input', function() { autoSize(this); });

  // Quick action buttons
  document.querySelectorAll('.fai-act').forEach(function(b) {
    b.addEventListener('click', function() {
      var key = this.getAttribute('data-act');
      var action = ACTIONS[key];
      if (!action) return;
      
      // Get context asynchronously
      getFinalInvoiceContext().then(function(ctx) {
        var prompt = action.prompt(ctx);
        sendMessage(prompt, true, action.icon + ' ' + action.label);
      });
    });
  });

  // Welcome
  addBotMsg('**Welcome to Final Invoice AI Mentor.** I generate complete, professional final invoices with full JSON data ready to load into the Final Invoice Builder.\n\n✨ **What I can do:**\n• Generate complete final invoices from project data\n• Convert estimates/bids to final invoices\n• Add change orders and additional work\n• Create payment schedules and terms\n• Include warranty and maintenance info\n• Generate valid JSON for instant upload\n\n📋 **Every response includes** a complete ```final-invoice-json block that you can click to load directly into the Final Invoice Builder.\n\n**No incomplete responses** - every invoice is complete and ready to send.');
}

function autoSize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}

function togglePanel() {
  _open = !_open;
  document.getElementById('fai-panel').classList.toggle('open', _open);
  if (_open) document.getElementById('fai-in').focus();
}

function addUserMsg(text) {
  var msgs = document.getElementById('fai-msgs');
  var div = document.createElement('div');
  div.className = 'fai-msg user';
  div.textContent = text;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function addBotMsg(text) {
  var msgs = document.getElementById('fai-msgs');
  var typing = msgs.querySelector('.fai-typing');
  if (typing) typing.remove();
  var timerEl = msgs.querySelector('.fai-timer');
  if (timerEl) timerEl.remove();

  var div = document.createElement('div');
  div.className = 'fai-msg bot';
  div.innerHTML = renderMd(text);

  // Action buttons on all responses
  var acts = document.createElement('div');
  acts.style.cssText = 'margin-top:10px;padding-top:8px;border-top:1px solid #333;display:flex;gap:6px;flex-wrap:wrap';

  // Load into Final Invoice Builder — parse final-invoice-json block
  var jsonData = null;
  var jm = text.match(/```(?:final-invoice-json|final-invoice|json)\s*\n([\s\S]*?)```/);
  if (jm) { 
    try { 
      jsonData = JSON.parse(jm[1].trim()); 
      console.log('[Final Invoice AI] Successfully parsed JSON:', jsonData);
    } catch(e) { 
      console.error('[Final Invoice AI] JSON parse error:', e);
      console.log('[Final Invoice AI] Raw JSON text:', jm[1]);
    }
  }
  if (jsonData && typeof loadFinalInvoice === 'function') {
    var loadBtn = document.createElement('button');
    loadBtn.style.cssText = 'background:linear-gradient(135deg,#dc2626,#ef4444);border:none;color:#fff;padding:5px 12px;border-radius:6px;font-size:11px;cursor:pointer;font-weight:700';
    loadBtn.textContent = '\ud83d\udce5 Load into Final Invoice Builder';
    loadBtn.onclick = function() {
      try {
        var success = loadFinalInvoice(jsonData);
        if (success) { 
          loadBtn.textContent = '\u2705 Loaded Successfully'; 
          loadBtn.disabled = true; 
          loadBtn.style.background = '#22c55e'; 
        } else {
          loadBtn.textContent = '\u274c Load Failed';
          loadBtn.style.background = '#dc2626';
        }
      } catch(err) {
        loadBtn.textContent = '\u274c Load Failed';
        loadBtn.style.background = '#dc2626';
        console.error('[Final Invoice AI] Load error:', err);
      }
    };
    acts.appendChild(loadBtn);
  }

  // Copy
  var copyBtn = document.createElement('button');
  copyBtn.style.cssText = 'background:#1a1a1a;border:1px solid #333;color:#999;padding:5px 10px;border-radius:6px;font-size:11px;cursor:pointer';
  copyBtn.textContent = '\ud83d\udccb Copy';
  copyBtn.onclick = function() {
    navigator.clipboard.writeText(text).then(function() {
      copyBtn.textContent = '\u2705 Copied!';
      setTimeout(function() { copyBtn.textContent = '\ud83d\udccb Copy'; }, 2000);
    });
  };
  acts.appendChild(copyBtn);

  // Save as Draft
  var saveBtn = document.createElement('button');
  saveBtn.style.cssText = 'background:#1a1a1a;border:1px solid #333;color:#999;padding:5px 10px;border-radius:6px;font-size:11px;cursor:pointer';
  saveBtn.textContent = '\ud83d\udcbe Save as Draft';
  saveBtn.onclick = function() {
    if (typeof saveInvoiceDraft === 'function') {
      var draftId = saveInvoiceDraft(text, jsonData);
      if (draftId) {
        saveBtn.textContent = '\u2705 Saved ' + draftId;
        saveBtn.disabled = true;
        saveBtn.style.background = '#22c55e';
      }
    }
  };
  acts.appendChild(saveBtn);

    div.appendChild(acts);

  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
  var msgs = document.getElementById('fai-msgs');
  var div = document.createElement('div');
  div.className = 'fai-typing';
  div.innerHTML = '<span></span><span></span><span></span>';
  msgs.appendChild(div);

  // Show elapsed time
  var timerDiv = document.createElement('div');
  timerDiv.className = 'fai-timer';
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
  var msgs = document.getElementById('fai-msgs');
  var timerEl = msgs.querySelector('.fai-timer');
  if (timerEl && timerEl._interval) clearInterval(timerEl._interval);
}

// =====================================================================
// SEND MESSAGE
// =====================================================================
var _busy = false;

function sendMessage(text, isAction, actionLabel) {
  if (_busy) return;
  _busy = true;
  document.getElementById('fai-send').disabled = true;

  if (!_open) togglePanel();

  // Show user message
  if (isAction && actionLabel) {
    addUserMsg(actionLabel);
  } else {
    addUserMsg(text);
  }

  showTyping();

  // Build message with context for non-action messages - now async
  var fullMsg = text;
  var contextPromise = !isAction ? getFinalInvoiceContext() : Promise.resolve('');
  
  contextPromise.then(function(ctx) {
    if (ctx) fullMsg = text + '\n\n[Current Final Invoice Data]\n' + ctx;

    // Add to history
    _hist.push({ role: 'user', parts: [{ text: fullMsg }] });

    // Keep history manageable
    if (_hist.length > 40) {
      _hist = _hist.slice(0, 2).concat(_hist.slice(-38));
    }

    callAI(_hist).then(function(reply) {
      clearTimer();
      addBotMsg(reply);
      _hist.push({ role: 'model', parts: [{ text: reply }] });
    }).catch(function(err) {
      clearTimer();
      addBotMsg('**Connection issue.** ' + (err.name === 'AbortError' ? 'Request timed out (2 min limit). Try a simpler question or check your internet.' : 'Error: ' + err.message + '. Try again in a moment.'));
    }).finally(function() {
      _busy = false;
      document.getElementById('fai-send').disabled = false;
    });
  });
}

// =====================================================================
// INIT
// =====================================================================
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
