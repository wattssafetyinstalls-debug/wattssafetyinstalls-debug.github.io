/**
 * BidGen Template Engine — Searchable dropdown, AI Smart Fill, predictive suggestions
 * Requires templates.js to be loaded first for JOB_TEMPLATES.
 */
(function() {
    'use strict';

    var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
    var _selectedTemplateKey = '';

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
            '<h3 style="margin:0 0 8px;color:#3498db;font-size:18px;">🤖 AI Smart Fill — Gemini 2.5 Pro</h3>' +
            '<p style="color:#a0a0a0;font-size:12px;margin:0 0 16px;">Describe the job in plain English. AI will generate a complete template with labor, materials, scope, notes, and disclaimer.</p>' +
            '<textarea id="aiSmartFillInput" rows="4" style="width:100%;background:#0d1b2a;color:white;border:1px solid #2a3a5c;border-radius:8px;padding:12px;font-size:14px;resize:vertical;box-sizing:border-box;" placeholder="e.g. Install 3 grab bars in a bathroom with tile walls, one 18 inch vertical by toilet, one 36 inch horizontal in shower, one 24 inch by tub entry...">' + (desc || '') + '</textarea>' +
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

    window.runAiSmartFill = function() {
        var input = document.getElementById('aiSmartFillInput');
        var status = document.getElementById('aiSmartFillStatus');
        if (!input || !input.value.trim()) { alert('Please describe the job.'); return; }

        var jobDesc = input.value.trim();
        status.style.display = 'block';
        status.innerHTML = '<div style="text-align:center;color:#3498db;font-size:13px;"><div style="margin-bottom:8px;">⏳ Gemini 2.5 Pro is generating your template...</div><div style="width:100%;height:3px;background:#0d1b2a;border-radius:2px;overflow:hidden;"><div style="width:60%;height:100%;background:linear-gradient(90deg,#8e44ad,#3498db);animation:pulse 1.5s ease infinite;border-radius:2px;"></div></div></div>';

        var prompt = 'You are BidGen Template Generator for a Nebraska general contractor. Generate a complete job template from this description.\n\n' +
            'JOB DESCRIPTION: ' + jobDesc + '\n\n' +
            'Return ONLY a valid JSON object (no markdown, no code fences) with this EXACT structure:\n' +
            '{\n' +
            '  "trade": "general|plumbing|electrical|flooring|painting|roofing|carpet_tile",\n' +
            '  "areaDesc": "short area description",\n' +
            '  "sqft": number,\n' +
            '  "markup": number (15-25),\n' +
            '  "scopeTitle": "scope heading for the bid",\n' +
            '  "scope": ["scope item 1", "scope item 2", ...],\n' +
            '  "notes": ["note 1", "note 2", ...],\n' +
            '  "labor": [{"desc": "task", "basis": "per unit|per sq ft|1 lot|per run|per lin ft", "price": number}, ...],\n' +
            '  "materials": [{"desc": "material name", "qty": "quantity string", "price": number}, ...],\n' +
            '  "disclaimer": "unforeseen conditions clause text"\n' +
            '}\n\n' +
            'IMPORTANT RULES:\n' +
            '- Use realistic Nebraska 2025 pricing\n' +
            '- Include ALL labor steps (demo, prep, install, cleanup)\n' +
            '- Include ALL materials needed\n' +
            '- Scope items should be professional bid language\n' +
            '- Disclaimer should cover hidden conditions\n' +
            '- Be thorough — a real contractor needs this to be complete\n' +
            '- ONLY return the JSON object, nothing else';

        var contents = [
            { role: 'user', parts: [{ text: prompt }] }
        ];

        fetch(PROXY + '?model=gemini-2.5-pro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: contents,
                generationConfig: {
                    temperature: 0.4,
                    maxOutputTokens: 8192,
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

        if (typeof showNotification === 'function') {
            showNotification('🤖 AI template generated and applied! Review and adjust as needed.', 'success');
        }
    }

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
