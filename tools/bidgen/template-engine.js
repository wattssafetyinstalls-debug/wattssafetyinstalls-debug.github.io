/**
 * BidGen Template Engine v2 — Searchable dropdown, AI Smart Fill w/ Google Search Grounding,
 * predictive suggestions, contractor jargon, local material pricing (Menards, HD, etc.),
 * and deep interlinks with AI Mentor widget + Field Calculator.
 * Requires templates.js to be loaded first for JOB_TEMPLATES.
 */
(function() {
    'use strict';

    var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
    var _selectedTemplateKey = '';
    var _lastAITemplate = null; // stores last AI-generated template for interlink use
    var _speechRecognition = null; // Web Speech API instance
    var _speechTarget = null; // which input element is receiving speech

    // ── VOICE INPUT (Web Speech API) ────────────────────────────────
    function hasSpeechSupport() {
        return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
    }

    function startVoiceInput(targetId, statusId) {
        if (!hasSpeechSupport()) {
            alert('Speech recognition not supported in this browser. Use Chrome or Edge.');
            return;
        }

        // Stop existing recognition
        if (_speechRecognition) {
            _speechRecognition.stop();
            _speechRecognition = null;
        }

        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        _speechRecognition = new SpeechRecognition();
        _speechRecognition.continuous = true;
        _speechRecognition.interimResults = true;
        _speechRecognition.lang = 'en-US';
        _speechTarget = document.getElementById(targetId);

        var micBtn = document.getElementById(statusId);
        var finalTranscript = _speechTarget ? _speechTarget.value : '';

        if (micBtn) {
            micBtn.style.background = '#e74c3c';
            micBtn.style.animation = 'pulse 1s ease infinite';
            micBtn.title = 'Listening... click to stop';
        }

        _speechRecognition.onresult = function(event) {
            var interim = '';
            for (var i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interim += event.results[i][0].transcript;
                }
            }
            if (_speechTarget) {
                _speechTarget.value = finalTranscript + interim;
            }
        };

        _speechRecognition.onerror = function(event) {
            if (event.error !== 'aborted') {
                if (typeof showNotification === 'function') {
                    showNotification('Mic error: ' + event.error + '. Try again.', 'error');
                }
            }
            stopVoiceInput(statusId);
        };

        _speechRecognition.onend = function() {
            stopVoiceInput(statusId);
        };

        _speechRecognition.start();
    }

    function stopVoiceInput(statusId) {
        if (_speechRecognition) {
            try { _speechRecognition.stop(); } catch(e) {}
            _speechRecognition = null;
        }
        var micBtn = document.getElementById(statusId);
        if (micBtn) {
            micBtn.style.background = '';
            micBtn.style.animation = '';
            micBtn.title = 'Voice input';
        }
    }

    function toggleVoiceInput(targetId, statusId) {
        if (_speechRecognition) {
            stopVoiceInput(statusId);
        } else {
            startVoiceInput(targetId, statusId);
        }
    }

    window.toggleTemplateVoice = function() {
        toggleVoiceInput('templateSearch', 'templateMicBtn');
    };

    window.toggleSmartFillVoice = function() {
        toggleVoiceInput('aiSmartFillInput', 'smartFillMicBtn');
    };

    // ── BUILD CATEGORY INDEX ─────────────────────────────────────────
    function getTemplateIndex() {
        var cats = {};
        var keys = Object.keys(JOB_TEMPLATES);
        for (var i = 0; i < keys.length; i++) {
            var k = keys[i];
            var t = JOB_TEMPLATES[k];
            var cat = t.cat || 'Other';
            if (!cats[cat]) cats[cat] = [];
            cats[cat].push({ key: k, label: t.label, tags: t.tags || [] });
        }
        return cats;
    }

    // ── SEARCHABLE TEMPLATE DROPDOWN ─────────────────────────────────
    window.filterTemplates = function() {
        var input = document.getElementById('templateSearch');
        var drop = document.getElementById('templateDrop');
        if (!input || !drop) return;

        var q = input.value.toLowerCase().trim();
        var cats = getTemplateIndex();
        var html = '';
        var count = 0;

        var catOrder = Object.keys(cats);
        for (var ci = 0; ci < catOrder.length; ci++) {
            var cat = catOrder[ci];
            var items = cats[cat];
            var matchedItems = [];

            for (var ii = 0; ii < items.length; ii++) {
                var item = items[ii];
                if (!q) {
                    matchedItems.push(item);
                } else {
                    var searchStr = (item.label + ' ' + item.tags.join(' ')).toLowerCase();
                    if (searchStr.indexOf(q) !== -1) {
                        matchedItems.push(item);
                    }
                }
            }

            if (matchedItems.length > 0) {
                html += '<div style="padding:6px 12px;font-size:10px;text-transform:uppercase;color:#7f8c8d;letter-spacing:0.5px;border-bottom:1px solid #1a2744;background:#0d1b2a;">' + cat + '</div>';
                for (var mi = 0; mi < matchedItems.length; mi++) {
                    var m = matchedItems[mi];
                    count++;
                    html += '<div class="tpl-opt" data-key="' + m.key + '" onclick="selectTemplate(\'' + m.key + '\')" style="padding:8px 14px;cursor:pointer;font-size:13px;color:#e0e0e0;border-bottom:1px solid rgba(42,58,92,0.4);transition:background 0.15s;"';
                    html += ' onmouseenter="this.style.background=\'#1a2744\'" onmouseleave="this.style.background=\'transparent\'">';
                    html += m.label;
                    html += '</div>';
                }
            }
        }

        if (count === 0 && q) {
            html += '<div style="padding:16px;text-align:center;color:#7f8c8d;font-size:12px;">';
            html += 'No templates match "<b>' + q + '</b>"<br><br>';
            html += '<span style="color:#3498db;cursor:pointer;" onclick="aiSmartFill()">Try AI Smart Fill instead →</span>';
            html += '</div>';
        }

        drop.innerHTML = html;
        drop.style.display = (html ? 'block' : 'none');
    };

    window.selectTemplate = function(key) {
        _selectedTemplateKey = key;
        var t = JOB_TEMPLATES[key];
        if (!t) return;
        document.getElementById('templateSearch').value = t.label;
        document.getElementById('templateSelect').value = key;
        document.getElementById('templateDrop').style.display = 'none';
    };

    window.applySelectedTemplate = function() {
        var key = _selectedTemplateKey || document.getElementById('templateSelect').value;
        if (!key || !JOB_TEMPLATES[key]) {
            alert('Search and select a template first, or use AI Fill to describe any job.');
            return;
        }
        applyTemplateByKey(key);
    };

    // ── APPLY TEMPLATE (enhanced — fills scope, notes, scopeTitle, markup) ──
    function applyTemplateByKey(key) {
        var t = JOB_TEMPLATES[key];
        if (!t) return;

        if (document.getElementById('clientName').value && !confirm('This will replace current labor & material items. Continue?')) return;

        // Trade & basics
        document.getElementById('tradeType').value = t.trade;
        if (typeof onTradeChange === 'function') onTradeChange();
        document.getElementById('areaDesc').value = t.areaDesc;
        document.getElementById('sqft').value = t.sqft;

        // Markup
        if (t.markup) {
            var mkEl = document.getElementById('materialsMarkup');
            if (mkEl) mkEl.value = t.markup;
        }

        // Scope title
        if (t.scopeTitle) {
            var stEl = document.getElementById('scopeTitle');
            if (stEl) stEl.value = t.scopeTitle;
        }

        // Scope items
        if (t.scope && t.scope.length > 0) {
            var scopeContainer = document.getElementById('scopeItemsContainer');
            if (scopeContainer) {
                scopeContainer.innerHTML = '';
                for (var si = 0; si < t.scope.length; si++) {
                    if (typeof addScopeRow === 'function') addScopeRow(t.scope[si]);
                }
            }
        }

        // Notes
        if (t.notes && t.notes.length > 0) {
            var notesContainer = document.getElementById('notesItemsContainer');
            if (notesContainer) {
                notesContainer.innerHTML = '';
                for (var ni = 0; ni < t.notes.length; ni++) {
                    if (typeof addNoteRow === 'function') addNoteRow(t.notes[ni]);
                }
            }
        }

        // Labor items
        document.getElementById('laborItemsContainer').innerHTML = '';
        for (var li = 0; li < t.labor.length; li++) {
            if (typeof addLaborRow === 'function') addLaborRow(t.labor[li].desc, t.labor[li].basis, t.labor[li].price);
        }

        // Material items
        document.getElementById('matItemsContainer').innerHTML = '';
        for (var mi = 0; mi < t.materials.length; mi++) {
            if (typeof addMatRow === 'function') addMatRow(t.materials[mi].desc, t.materials[mi].qty, t.materials[mi].price);
        }

        // Disclaimer
        document.getElementById('disclaimer').value = t.disclaimer;

        // Reset search
        document.getElementById('templateSearch').value = '';
        _selectedTemplateKey = '';

        // Recalc
        if (typeof liveCalc === 'function') liveCalc();

        if (typeof showNotification === 'function') {
            showNotification('⚡ Template "' + t.label + '" applied! Fill in client & job details.', 'success');
        }
    }

    // Keep old applyTemplate working for backwards compat
    window.applyTemplate = function() {
        var key = document.getElementById('templateSelect').value;
        if (!key) { alert('Select a template first.'); return; }
        applyTemplateByKey(key);
    };

    // ── AI SMART FILL — Gemini 2.5 Pro ──────────────────────────────
    window.aiSmartFill = function() {
        var searchInput = document.getElementById('templateSearch');
        var desc = searchInput ? searchInput.value.trim() : '';

        // Show modal for job description
        var existing = document.getElementById('aiSmartFillModal');
        if (existing) existing.remove();

        var modal = document.createElement('div');
        modal.id = 'aiSmartFillModal';
        modal.style.cssText = 'position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;padding:20px;';
        modal.innerHTML = '<div style="background:#16213e;border-radius:12px;padding:28px;max-width:520px;width:100%;box-shadow:0 12px 40px rgba(0,0,0,0.5);">' +
            '<h3 style="margin:0 0 8px;color:#3498db;font-size:18px;">🤖 AI Smart Fill — Gemini 2.5 Pro + Web Search</h3>' +
            '<p style="color:#a0a0a0;font-size:12px;margin:0 0 6px;">Describe the job in plain English. AI searches the web for <strong style="color:#4ade80">current material pricing</strong> (Menards, HD, Lowe\'s), uses <strong style="color:#f59e0b">real contractor jargon</strong>, and generates a complete bid-ready template.</p>' +
            '<p style="color:#71717a;font-size:10px;margin:0 0 12px;">Tip: Be specific — mention quantities, brands, sizes, room details, ADA requirements. The more detail, the better the template.</p>' +
            '<div style="position:relative;">' +
            '<textarea id="aiSmartFillInput" rows="5" style="width:100%;background:#0d1b2a;color:white;border:1px solid #2a3a5c;border-radius:8px;padding:12px;padding-right:44px;font-size:14px;resize:vertical;box-sizing:border-box;" placeholder="e.g. Install 3 ADA grab bars in a bathroom with tile walls — one 18in vertical by toilet, one 36in horizontal in shower, one 24in by tub entry...">' + (desc || '') + '</textarea>' +
            (hasSpeechSupport() ? '<button id="smartFillMicBtn" onclick="toggleSmartFillVoice()" style="position:absolute;right:8px;top:8px;width:32px;height:32px;border-radius:50%;border:1px solid #2a3a5c;background:#1a2744;color:#e74c3c;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;" title="Voice input">🎙</button>' : '') +
            '</div>' +
            '<div style="display:flex;gap:8px;margin-top:14px;">' +
            '<button onclick="runAiSmartFill()" style="flex:1;padding:10px;background:linear-gradient(135deg,#8e44ad,#3498db);color:white;border:none;border-radius:8px;font-weight:700;font-size:14px;cursor:pointer;">Generate Template</button>' +
            '<button onclick="document.getElementById(\'aiSmartFillModal\').remove()" style="padding:10px 20px;background:#2a3a5c;color:#ccc;border:none;border-radius:8px;cursor:pointer;">Cancel</button>' +
            '</div>' +
            '<div id="aiSmartFillStatus" style="margin-top:12px;display:none;"></div>' +
            '</div>';

        document.body.appendChild(modal);
        modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });
        setTimeout(function() { document.getElementById('aiSmartFillInput').focus(); }, 100);
    };

    // ── CONTEXT GATHERING — pull data from BidGen, Field Calc, Catalog ──
    function gatherBidContext() {
        var ctx = '';
        try {
            var fields = [
                ['tradeType','Trade'],['clientName','Client'],['complexName','Property'],
                ['unitNum','Unit'],['jobCity','City'],['sqft','SqFt'],['linft','LinFt'],
                ['areaDesc','Area'],['materialsMarkup','Markup%']
            ];
            fields.forEach(function(f) {
                var el = document.getElementById(f[0]);
                if (el && el.value) ctx += f[1] + ': ' + el.value + '\n';
            });
            if (typeof getLaborItems === 'function') {
                var li = getLaborItems();
                if (li.length) {
                    ctx += '\nExisting Labor Items:\n';
                    li.forEach(function(i) { ctx += '  - ' + i.desc + ' (' + i.qty + ' x $' + i.price + ')\n'; });
                }
            }
            if (typeof getMatItems === 'function') {
                var mi = getMatItems();
                if (mi.length) {
                    ctx += '\nExisting Material Items:\n';
                    mi.forEach(function(i) { ctx += '  - ' + i.desc + ' (' + i.qty + ' x $' + i.price + ')\n'; });
                }
            }
            if (typeof _catalog !== 'undefined' && _catalog && _catalog.materials) {
                var keys = Object.keys(_catalog.materials);
                if (keys.length) {
                    ctx += '\nMaterial Catalog (recent prices):\n';
                    keys.slice(0, 15).forEach(function(k) {
                        var item = _catalog.materials[k];
                        ctx += '  ' + k + ': $' + (item.lastPrice || '?') + '\n';
                    });
                }
            }
        } catch(e) {}
        return ctx;
    }

    window.runAiSmartFill = function() {
        var input = document.getElementById('aiSmartFillInput');
        var status = document.getElementById('aiSmartFillStatus');
        if (!input || !input.value.trim()) { alert('Please describe the job.'); return; }

        var jobDesc = input.value.trim();
        var existingContext = gatherBidContext();
        status.style.display = 'block';
        status.innerHTML = '<div style="text-align:center;color:#3498db;font-size:13px;"><div style="margin-bottom:8px;">⏳ Gemini 2.5 Pro is searching the web & generating your template...</div><div style="width:100%;height:3px;background:#0d1b2a;border-radius:2px;overflow:hidden;"><div style="width:60%;height:100%;background:linear-gradient(90deg,#8e44ad,#3498db);animation:pulse 1.5s ease infinite;border-radius:2px;"></div></div></div>';

        var prompt = [
            'You are BidGen Template Generator for Watts Safety Installs / Watts ATP Contractor — a Nebraska Licensed General Contractor (#54690-25) based in Norfolk, NE.',
            '',
            '## YOUR JOB',
            'Generate a COMPLETE, bid-ready job template from the description below. You have access to Google Search — USE IT to look up:',
            '- Current material prices at Menards, Home Depot, Lowe\'s, or specialty suppliers',
            '- Correct trade terminology and contractor/jobsite jargon for line item descriptions',
            '- ADA standards, building codes (Nebraska IRC), and manufacturer specs for products mentioned',
            '- Real product names, SKUs, and model numbers when possible',
            '',
            '## CONTRACTOR LANGUAGE RULES',
            'Write ALL line items in real contractor/tradesman language:',
            '- Use field terms: "rough-in" not "prepare plumbing", "R&R" for remove and replace, "LF" for linear feet, "EA" for each',
            '- Material descriptions should include size, type, brand when known: "3/4 PurePEX × 10ft stick" not just "PEX pipe"',
            '- Labor basis options: "per sq ft", "per lin ft", "per unit", "1 lot", "per hour", "per run", "EA"',
            '- Use abbreviations a contractor would: "GFI" or "GFCI", "WH" for water heater, "ADA" for accessibility, "PT" for pressure-treated, "LVP", "SLU" for self-leveling underlayment',
            '',
            '## PRICING RULES',
            '- Search the web for CURRENT material prices — Menards Norfolk NE or nearest store, Home Depot, or online',
            '- Labor rates must be Nebraska 2025-2026 market rates for a licensed GC',
            '- If you find a specific product price online, use it. Include the source in a note.',
            '- Material markup is separate (the user sets it in BidGen) — quote material at contractor/wholesale cost',
            '',
            '## JOB DESCRIPTION',
            jobDesc,
            '',
            existingContext ? ('## EXISTING BID CONTEXT (already in BidGen form)\n' + existingContext + '\n') : '',
            '## OUTPUT FORMAT',
            'Return ONLY a valid JSON object (no markdown, no code fences, no explanation) with this EXACT structure:',
            '{',
            '  "trade": "general|plumbing|electrical|flooring|painting|roofing|carpet_tile",',
            '  "areaDesc": "short area description",',
            '  "sqft": number,',
            '  "markup": number (15-25),',
            '  "scopeTitle": "professional scope heading for the bid document",',
            '  "scope": ["scope item 1 in professional bid language", ...],',
            '  "notes": ["note with real specs, product names, code references", ...],',
            '  "labor": [{"desc": "contractor-language task description", "basis": "per unit|per sq ft|1 lot|per lin ft|EA", "price": number}, ...],',
            '  "materials": [{"desc": "specific product name with size/brand", "qty": "quantity with unit", "price": number}, ...],',
            '  "disclaimer": "unforeseen conditions clause covering hidden conditions specific to THIS job type",',
            '  "webSources": ["brief notes on pricing sources found, e.g. Menards Norfolk NE $X.XX for product Y"]',
            '}',
            '',
            'CRITICAL: Include ALL labor steps (demo, prep, install, test, cleanup). Include ALL materials needed (fasteners, adhesives, consumables). Be thorough — a real contractor needs this to be COMPLETE and bid-ready.',
            'ONLY return the JSON object.'
        ].join('\n');

        var contents = [
            { role: 'user', parts: [{ text: prompt }] }
        ];

        fetch(PROXY + '?model=gemini-2.5-pro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: contents,
                tools: [{ googleSearch: {} }],
                generationConfig: {
                    temperature: 0.4,
                    maxOutputTokens: 16384,
                    topP: 0.9
                }
            })
        })
        .then(function(r) {
            if (!r.ok) throw new Error('API error: ' + r.status);
            return r.json();
        })
        .then(function(data) {
            var c = data.candidates && data.candidates[0];
            if (!c || !c.content || !c.content.parts) throw new Error('No response from model.');

            var text = '';
            for (var i = 0; i < c.content.parts.length; i++) {
                if (c.content.parts[i].text) text += c.content.parts[i].text;
            }

            // Strip markdown code fences if present
            text = text.replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();

            var template;
            try {
                template = JSON.parse(text);
            } catch (e) {
                // Try to extract JSON from response
                var match = text.match(/\{[\s\S]*\}/);
                if (match) {
                    template = JSON.parse(match[0]);
                } else {
                    throw new Error('Could not parse AI response as JSON.');
                }
            }

            // Validate required fields
            if (!template.labor || !template.materials || !template.trade) {
                throw new Error('AI response missing required fields (labor, materials, trade).');
            }

            // Store for interlink use
            _lastAITemplate = template;

            // Apply the AI-generated template
            applyAITemplate(template, jobDesc);

            // Close modal
            var modal = document.getElementById('aiSmartFillModal');
            if (modal) modal.remove();
        })
        .catch(function(err) {
            status.innerHTML = '<div style="color:#e74c3c;font-size:13px;padding:8px;background:#1a0a0a;border-radius:6px;">❌ ' + err.message + '<br><small style="color:#999;">Try rephrasing or use a pre-built template.</small></div>';
        });
    };

    function applyAITemplate(t, desc) {
        if (document.getElementById('clientName').value && !confirm('AI template will replace current items. Continue?')) return;

        // Trade
        var tradeEl = document.getElementById('tradeType');
        var validTrades = [];
        for (var i = 0; i < tradeEl.options.length; i++) validTrades.push(tradeEl.options[i].value);
        if (validTrades.indexOf(t.trade) !== -1) {
            tradeEl.value = t.trade;
        } else {
            tradeEl.value = 'general';
        }
        if (typeof onTradeChange === 'function') onTradeChange();

        // Basics
        if (t.areaDesc) document.getElementById('areaDesc').value = t.areaDesc;
        if (t.sqft) document.getElementById('sqft').value = t.sqft;
        if (t.markup) {
            var mkEl = document.getElementById('materialsMarkup');
            if (mkEl) mkEl.value = t.markup;
        }

        // Scope title
        if (t.scopeTitle) {
            var stEl = document.getElementById('scopeTitle');
            if (stEl) stEl.value = t.scopeTitle;
        }

        // Scope
        if (t.scope && t.scope.length > 0) {
            var scopeContainer = document.getElementById('scopeItemsContainer');
            if (scopeContainer) {
                scopeContainer.innerHTML = '';
                for (var si = 0; si < t.scope.length; si++) {
                    if (typeof addScopeRow === 'function') addScopeRow(t.scope[si]);
                }
            }
        }

        // Notes
        if (t.notes && t.notes.length > 0) {
            var notesContainer = document.getElementById('notesItemsContainer');
            if (notesContainer) {
                notesContainer.innerHTML = '';
                for (var ni = 0; ni < t.notes.length; ni++) {
                    if (typeof addNoteRow === 'function') addNoteRow(t.notes[ni]);
                }
            }
        }

        // Labor
        document.getElementById('laborItemsContainer').innerHTML = '';
        if (t.labor) {
            for (var li = 0; li < t.labor.length; li++) {
                if (typeof addLaborRow === 'function') addLaborRow(t.labor[li].desc, t.labor[li].basis, t.labor[li].price);
            }
        }

        // Materials
        document.getElementById('matItemsContainer').innerHTML = '';
        if (t.materials) {
            for (var mi = 0; mi < t.materials.length; mi++) {
                if (typeof addMatRow === 'function') addMatRow(t.materials[mi].desc, t.materials[mi].qty, t.materials[mi].price);
            }
        }

        // Disclaimer
        if (t.disclaimer) document.getElementById('disclaimer').value = t.disclaimer;

        // Recalc
        if (typeof liveCalc === 'function') liveCalc();

        // Show web sources if available
        var sourceNote = '';
        if (t.webSources && t.webSources.length) {
            sourceNote = ' | Sources: ' + t.webSources.slice(0, 3).join('; ');
        }

        if (typeof showNotification === 'function') {
            showNotification('🤖 AI template applied! Web-sourced pricing included.' + sourceNote, 'success');
        }

        // Show interlink action bar
        showPostApplyBar(desc);
    }

    // ── POST-APPLY INTERLINK BAR ────────────────────────────────────
    function showPostApplyBar(jobDesc) {
        var existing = document.getElementById('templateInterlinkBar');
        if (existing) existing.remove();

        var bar = document.createElement('div');
        bar.id = 'templateInterlinkBar';
        bar.style.cssText = 'background:linear-gradient(135deg,#0d1b2a,#16213e);border:1px solid #2a3a5c;border-radius:8px;padding:10px 14px;margin-bottom:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;';
        bar.innerHTML = '<span style="font-size:11px;color:#7f8c8d;text-transform:uppercase;letter-spacing:0.5px;">Template Applied</span>' +
            '<button onclick="templateReviewWithAI()" style="background:linear-gradient(135deg,#3498db,#8e44ad);color:white;border:none;padding:6px 14px;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;white-space:nowrap;" title="Have AI Mentor review the filled bid">🧠 Review with AI Mentor</button>' +
            '<button onclick="templateSendToFieldCalc()" style="background:linear-gradient(135deg,#e67e22,#f39c12);color:white;border:none;padding:6px 14px;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;white-space:nowrap;" title="Open Field Calc with this job\'s measurements">📐 Open Field Calc</button>' +
            '<button onclick="templatePriceLookup()" style="background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;border:none;padding:6px 14px;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;white-space:nowrap;" title="Search web for current material prices">🔍 Price Check</button>' +
            '<button onclick="this.parentElement.remove()" style="background:#2a3a5c;color:#999;border:none;padding:4px 8px;border-radius:4px;font-size:11px;cursor:pointer;margin-left:auto;">✕</button>';

        var templateBar = document.getElementById('templateBar');
        if (templateBar && templateBar.parentNode) {
            templateBar.parentNode.insertBefore(bar, templateBar.nextSibling);
        }
    }

    // ── INTERLINK: Review with AI Mentor ─────────────────────────────
    window.templateReviewWithAI = function() {
        // Open AI Mentor panel and send a review request with current bid context
        var toggle = document.getElementById('bgai-toggle');
        var panel = document.getElementById('bgai-panel');
        if (toggle && panel && !panel.classList.contains('open')) {
            toggle.click();
        }

        // Find the AI Mentor's input and send button
        setTimeout(function() {
            var aiInput = document.getElementById('bgai-in');
            var aiSend = document.getElementById('bgai-send');
            if (aiInput && aiSend) {
                var trade = (document.getElementById('tradeType') || {}).value || 'general';
                var sqft = (document.getElementById('sqft') || {}).value || '?';
                var area = (document.getElementById('areaDesc') || {}).value || '?';
                aiInput.value = 'I just applied a template for a ' + trade + ' job (' + sqft + ' sq ft, ' + area + '). Do a FULL BID REVIEW — check my pricing against Nebraska market rates, flag anything I\'m missing, check my scope for gaps, and tell me if my material quantities look right for the square footage. Use your web search to verify current material pricing at Menards or Home Depot near Norfolk NE.';
                aiSend.click();
            }
        }, 500);
    };

    // ── INTERLINK: Open Field Calc with job context ──────────────────
    window.templateSendToFieldCalc = function() {
        // Open Field Calc panel
        var fcToggle = document.getElementById('fieldCalcToggle');
        var fcPanel = document.getElementById('fieldCalcPanel');
        if (fcToggle && fcPanel && fcPanel.style.display === 'none') {
            fcToggle.click();
        }

        // Pre-fill Field Calc AI tab with job measurements context
        setTimeout(function() {
            // Switch to AI tab
            if (typeof fcSwitchTab === 'function') fcSwitchTab('ai');

            var aiInput = document.getElementById('fcAIInput');
            if (aiInput) {
                var sqft = (document.getElementById('sqft') || {}).value || '';
                var area = (document.getElementById('areaDesc') || {}).value || '';
                var trade = (document.getElementById('tradeType') || {}).value || '';
                var linft = (document.getElementById('linft') || {}).value || '';
                var msg = 'Job: ' + trade + ' — ' + area;
                if (sqft) msg += '\nTotal area: ' + sqft + ' sq ft';
                if (linft && linft !== '0') msg += '\nLinear feet: ' + linft + ' lf';

                // Add material info from the template
                if (_lastAITemplate && _lastAITemplate.materials) {
                    msg += '\n\nMaterials to calculate:';
                    _lastAITemplate.materials.forEach(function(m) {
                        msg += '\n  - ' + m.desc + ' (' + m.qty + ')';
                    });
                }
                aiInput.value = msg;
            }
        }, 300);

        if (typeof showNotification === 'function') {
            showNotification('📐 Field Calc opened with job context. Use AI Planner tab for cut optimization.', 'success');
        }
    };

    // ── INTERLINK: Web Price Check ───────────────────────────────────
    window.templatePriceLookup = function() {
        var matItems = [];
        try {
            if (typeof getMatItems === 'function') matItems = getMatItems();
        } catch(e) {}

        if (!matItems.length) {
            alert('No materials in the current bid to price check.');
            return;
        }

        // Build a list of materials to search
        var matList = matItems.map(function(m) { return m.desc; }).join(', ');

        // Open AI Mentor and ask for price verification
        var toggle = document.getElementById('bgai-toggle');
        var panel = document.getElementById('bgai-panel');
        if (toggle && panel && !panel.classList.contains('open')) {
            toggle.click();
        }

        setTimeout(function() {
            var aiInput = document.getElementById('bgai-in');
            var aiSend = document.getElementById('bgai-send');
            if (aiInput && aiSend) {
                aiInput.value = 'Search the web and verify current pricing for these materials near Norfolk, NE (check Menards, Home Depot, Lowe\'s, and online suppliers):\n\n' +
                    matItems.map(function(m) { return '- ' + m.desc + ' (currently listed at $' + m.price + ')'; }).join('\n') +
                    '\n\nFor each material, tell me: current retail price, contractor price if different, where to get the best deal, and if my listed price is reasonable. Use a comparison table.';
                aiSend.click();
            }
        }, 500);
    };

    // ── GLOBAL INTERLINK API — other widgets can call these ──────────
    window.BidGenTemplates = {
        getLastAITemplate: function() { return _lastAITemplate; },
        getTemplateList: function() {
            return Object.keys(JOB_TEMPLATES).map(function(k) {
                return { key: k, label: JOB_TEMPLATES[k].label, cat: JOB_TEMPLATES[k].cat };
            });
        },
        applyByKey: function(key) { applyTemplateByKey(key); },
        getCurrentFormData: gatherBidContext
    };

    // ── CLOSE DROPDOWN ON OUTSIDE CLICK ──────────────────────────────
    document.addEventListener('click', function(e) {
        var drop = document.getElementById('templateDrop');
        var search = document.getElementById('templateSearch');
        if (drop && search && !drop.contains(e.target) && e.target !== search) {
            drop.style.display = 'none';
        }
    });

    // ── KEYBOARD NAVIGATION ──────────────────────────────────────────
    document.addEventListener('keydown', function(e) {
        if (e.target.id !== 'templateSearch') return;

        var drop = document.getElementById('templateDrop');
        if (!drop || drop.style.display === 'none') return;

        var opts = drop.querySelectorAll('.tpl-opt');
        if (opts.length === 0) return;

        var current = drop.querySelector('.tpl-opt[data-active]');
        var idx = -1;
        if (current) {
            for (var i = 0; i < opts.length; i++) {
                if (opts[i] === current) { idx = i; break; }
            }
        }

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (current) current.removeAttribute('data-active');
            idx = (idx + 1) % opts.length;
            opts[idx].setAttribute('data-active', '1');
            opts[idx].style.background = '#1a2744';
            if (current && current !== opts[idx]) current.style.background = 'transparent';
            opts[idx].scrollIntoView({ block: 'nearest' });
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (current) current.removeAttribute('data-active');
            idx = idx <= 0 ? opts.length - 1 : idx - 1;
            opts[idx].setAttribute('data-active', '1');
            opts[idx].style.background = '#1a2744';
            if (current && current !== opts[idx]) current.style.background = 'transparent';
            opts[idx].scrollIntoView({ block: 'nearest' });
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (current) {
                var key = current.getAttribute('data-key');
                if (key) {
                    selectTemplate(key);
                    applyTemplateByKey(key);
                }
            }
        } else if (e.key === 'Escape') {
            drop.style.display = 'none';
        }
    });

})();
