// =====================================================================
// BIDGEN PRO — 15 Professional Optimizations
// Loads AFTER all other BidGen scripts. Zero modifications to existing files.
// =====================================================================
(function() {
'use strict';

// Wait for DOM + all other scripts
var _ready = false;
function onReady(fn) {
    if (_ready) return fn();
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() { _ready = true; fn(); });
    } else { _ready = true; fn(); }
}

onReady(function() {
    // Small delay to let deferred scripts initialize
    setTimeout(initBidGenPro, 800);
});

function initBidGenPro() {
    console.log('[BidGen Pro] Initializing 15 optimizations...');

    // ═════════════════════════════════════════════════════════════════
    // 1. BOOT VALIDATOR — verify all scripts, containers, connections
    // ═════════════════════════════════════════════════════════════════
    var bootReport = { scripts: [], dom: [], functions: [], errors: [] };

    // Check required scripts loaded
    var requiredScripts = [
        { name: 'templates.js', check: function() { return typeof JOB_TEMPLATES !== 'undefined'; } },
        { name: 'template-engine.js', check: function() { return typeof window.BidGenTemplates !== 'undefined'; } },
        { name: 'bidgen-ai.js', check: function() { return !!document.getElementById('bgai-panel'); } },
        { name: 'contract-delivery.js', check: function() { return typeof sendContractToClient === 'function'; } },
        { name: 'field-calc.js', check: function() { return !!document.getElementById('fieldCalcPanel'); } },
        { name: 'widget-dock.js', check: function() { return !!document.getElementById('wd-dock'); } }
    ];
    requiredScripts.forEach(function(s) {
        var ok = false;
        try { ok = s.check(); } catch(e) {}
        bootReport.scripts.push({ name: s.name, loaded: ok });
        if (!ok) bootReport.errors.push('Script not loaded: ' + s.name);
    });

    // Check critical DOM elements
    var requiredDOM = [
        'clientName', 'complexName', 'unitNum', 'jobCity', 'sqft', 'linft',
        'areaDesc', 'estimateDate', 'tradeType', 'scopeTitle', 'materialsMarkup',
        'laborItemsContainer', 'matItemsContainer', 'scopeItemsContainer',
        'notesItemsContainer', 'liveCalcPanel', 'savedJobsSelect'
    ];
    requiredDOM.forEach(function(id) {
        var el = document.getElementById(id);
        bootReport.dom.push({ id: id, exists: !!el });
        if (!el) bootReport.errors.push('Missing DOM element: #' + id);
    });

    // Check critical functions exist
    var requiredFns = [
        'addLaborRow', 'addMatRow', 'addScopeRow', 'addNoteRow', 'liveCalc',
        'getLaborItems', 'getMatItems', 'getScope', 'getNotes', 'autoSaveInvoice',
        'generateLabor', 'generateMaterials', 'generateChangeOrder', 'hashPIN'
    ];
    requiredFns.forEach(function(fn) {
        var ok = typeof window[fn] === 'function';
        bootReport.functions.push({ name: fn, exists: ok });
        if (!ok) bootReport.errors.push('Missing function: ' + fn + '()');
    });

    // Store globally for health dashboard
    window._bidgenBootReport = bootReport;

    if (bootReport.errors.length > 0) {
        console.warn('[BidGen Pro] Boot issues:', bootReport.errors);
    } else {
        console.log('[BidGen Pro] ✅ All systems verified — ' +
            bootReport.scripts.length + ' scripts, ' +
            bootReport.dom.length + ' DOM elements, ' +
            bootReport.functions.length + ' functions OK');
    }

    // ═════════════════════════════════════════════════════════════════
    // 2. CROSS-WIDGET EVENT BUS
    // ═════════════════════════════════════════════════════════════════
    var _listeners = {};
    window.BidGen = window.BidGen || {};
    window.BidGen.on = function(event, fn) {
        if (!_listeners[event]) _listeners[event] = [];
        _listeners[event].push(fn);
    };
    window.BidGen.off = function(event, fn) {
        if (!_listeners[event]) return;
        _listeners[event] = _listeners[event].filter(function(f) { return f !== fn; });
    };
    window.BidGen.emit = function(event, data) {
        console.log('[BidGen Bus]', event, data ? '→' : '', data || '');
        (_listeners[event] || []).forEach(function(fn) {
            try { fn(data); } catch(e) { console.error('[BidGen Bus] Error in', event, 'handler:', e); }
        });
    };

    // Wire existing actions into the bus
    var _origGenLabor = window.generateLabor;
    window.generateLabor = function() {
        BidGen.emit('doc:generating', { type: 'labor' });
        _origGenLabor.apply(this, arguments);
        BidGen.emit('doc:generated', { type: 'labor', invoiceId: window._lastInvoiceId });
    };
    var _origGenMats = window.generateMaterials;
    window.generateMaterials = function() {
        BidGen.emit('doc:generating', { type: 'materials' });
        _origGenMats.apply(this, arguments);
        BidGen.emit('doc:generated', { type: 'materials', invoiceId: window._lastInvoiceId });
    };
    var _origGenCO = window.generateChangeOrder;
    window.generateChangeOrder = function() {
        BidGen.emit('doc:generating', { type: 'change_order' });
        _origGenCO.apply(this, arguments);
        BidGen.emit('doc:generated', { type: 'change_order', invoiceId: window._lastInvoiceId });
    };
    var _origSaveJob = window.saveJob;
    window.saveJob = function() {
        _origSaveJob.apply(this, arguments);
        BidGen.emit('job:saved', { name: document.getElementById('savedJobsSelect').value });
    };

    // ═════════════════════════════════════════════════════════════════
    // 3. SMART DIRTY-TRACKING AUTO-SAVE
    // ═════════════════════════════════════════════════════════════════
    var _formSnapshot = '';
    var _dirtyTimer = null;
    var _isDirty = false;

    function getFormFingerprint() {
        var fields = ['clientName','complexName','unitNum','jobCity','sqft','linft',
                      'areaDesc','estimateDate','tradeType','scopeTitle','materialsMarkup',
                      'supplierNote','disclaimer'];
        var parts = fields.map(function(id) {
            var el = document.getElementById(id);
            return el ? el.value : '';
        });
        // Include row counts
        parts.push(document.querySelectorAll('#laborItemsContainer .li-row').length + '');
        parts.push(document.querySelectorAll('#matItemsContainer .mi-row').length + '');
        parts.push(document.querySelectorAll('#scopeItemsContainer .scope-row').length + '');
        parts.push(document.querySelectorAll('#notesItemsContainer .note-row').length + '');
        return parts.join('|');
    }

    function checkDirty() {
        var current = getFormFingerprint();
        if (current !== _formSnapshot) {
            _isDirty = true;
            _formSnapshot = current;
            showDirtyIndicator(true);
            // Debounced auto-save: 8 seconds after last change
            clearTimeout(_dirtyTimer);
            _dirtyTimer = setTimeout(function() {
                if (_isDirty && typeof autoSaveInvoice === 'function' && window.userPIN) {
                    try {
                        var id = autoSaveInvoice('temporary');
                        if (id) {
                            _isDirty = false;
                            showDirtyIndicator(false);
                            BidGen.emit('form:autosaved', { invoiceId: id });
                        }
                    } catch(e) { console.warn('[BidGen Pro] Auto-save failed:', e); }
                }
            }, 8000);
        }
    }

    function showDirtyIndicator(dirty) {
        var el = document.getElementById('bgp-dirty');
        if (!el) {
            el = document.createElement('div');
            el.id = 'bgp-dirty';
            el.style.cssText = 'position:fixed;top:8px;right:120px;z-index:99998;font-size:10px;font-weight:600;padding:3px 10px;border-radius:12px;font-family:"Inter",sans-serif;transition:all 0.3s;pointer-events:none;';
            document.body.appendChild(el);
        }
        if (dirty) {
            el.textContent = '● Unsaved changes';
            el.style.background = 'rgba(239,68,68,0.15)';
            el.style.color = '#f87171';
            el.style.opacity = '1';
        } else {
            el.textContent = '✓ Saved';
            el.style.background = 'rgba(34,197,94,0.15)';
            el.style.color = '#4ade80';
            setTimeout(function() { el.style.opacity = '0'; }, 2000);
        }
    }

    // Listen for form changes
    var formContainer = document.querySelector('.container');
    if (formContainer) {
        formContainer.addEventListener('input', function() { checkDirty(); });
        formContainer.addEventListener('change', function() { checkDirty(); });
    }
    // Take initial snapshot after a beat
    setTimeout(function() { _formSnapshot = getFormFingerprint(); }, 2000);

    // ═════════════════════════════════════════════════════════════════
    // 4. ONE-CLICK CHANGE ORDER FROM ANY SAVED INVOICE
    // ═════════════════════════════════════════════════════════════════
    window.createCOFromInvoice = function(invoiceId) {
        // Find the invoice in invoiceData
        var inv = null;
        var statuses = ['temporary', 'permanent', 'lost'];
        if (typeof invoiceData !== 'undefined') {
            for (var s = 0; s < statuses.length; s++) {
                var bucket = invoiceData[statuses[s]];
                if (bucket && bucket[invoiceId]) { inv = bucket[invoiceId]; break; }
            }
        }
        if (!inv) {
            showNotification('Invoice ' + invoiceId + ' not found in library.', 'error');
            return;
        }
        // Load into form
        if (typeof window._aiLoadIntoBidGen === 'function') {
            window._aiLoadIntoBidGen(inv);
        } else {
            // Fallback manual load
            if (inv.clientName) document.getElementById('clientName').value = inv.clientName;
            if (inv.complexName) document.getElementById('complexName').value = inv.complexName;
            if (inv.unitNum) document.getElementById('unitNum').value = inv.unitNum;
            if (inv.jobCity) document.getElementById('jobCity').value = inv.jobCity;
            if (inv.sqft) document.getElementById('sqft').value = inv.sqft;
            if (typeof liveCalc === 'function') liveCalc();
        }
        showNotification('📥 Loaded ' + invoiceId + ' into form. Modify and click "Open Change Order".', 'success');
        window.scrollTo({ top: 0, behavior: 'smooth' });
        BidGen.emit('invoice:loadedForCO', { invoiceId: invoiceId });
    };

    // ═════════════════════════════════════════════════════════════════
    // 5. INVOICE STATUS BADGE ON FORM
    // ═════════════════════════════════════════════════════════════════
    function updateStatusBadge() {
        var badge = document.getElementById('bgp-status-badge');
        if (!badge) {
            badge = document.createElement('div');
            badge.id = 'bgp-status-badge';
            badge.style.cssText = 'display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:12px;font-size:10px;font-weight:600;font-family:"Inter",sans-serif;cursor:pointer;transition:all 0.2s;';
            badge.title = 'Current document status';
            // Insert after the h1 subtitle
            var subtitle = document.querySelector('.subtitle');
            if (subtitle) subtitle.appendChild(badge);
        }
        var invId = window._lastInvoiceId;
        if (!invId || typeof invoiceData === 'undefined') {
            badge.style.display = 'none';
            return;
        }
        badge.style.display = 'inline-flex';
        var status = 'draft';
        if (invoiceData.permanent && invoiceData.permanent[invId]) status = 'awarded';
        else if (invoiceData.lost && invoiceData.lost[invId]) status = 'lost';
        else if (invoiceData.temporary && invoiceData.temporary[invId]) status = 'pending';

        var colors = {
            draft: { bg: 'rgba(113,113,122,0.15)', fg: '#a1a1aa', icon: '○' },
            pending: { bg: 'rgba(251,191,36,0.15)', fg: '#fbbf24', icon: '◔' },
            awarded: { bg: 'rgba(34,197,94,0.15)', fg: '#22c55e', icon: '●' },
            lost: { bg: 'rgba(239,68,68,0.15)', fg: '#ef4444', icon: '✕' }
        };
        var c = colors[status];
        badge.style.background = c.bg;
        badge.style.color = c.fg;
        badge.innerHTML = c.icon + ' ' + status.toUpperCase() + ' <span style="opacity:0.6;font-weight:400">' + (invId || '') + '</span>';
    }

    // Update badge when docs are generated or saved
    BidGen.on('doc:generated', updateStatusBadge);
    BidGen.on('form:autosaved', updateStatusBadge);
    setTimeout(updateStatusBadge, 2500);

    // ═════════════════════════════════════════════════════════════════
    // 6. TOAST NOTIFICATION UPGRADE — stacking, auto-dismiss, no dupes
    // ═════════════════════════════════════════════════════════════════
    var _toasts = [];
    var _toastDupeCache = {};

    // Override showNotification with the upgraded version
    var _origNotify = window.showNotification;
    window.showNotification = function(message, type) {
        // Deduplicate — skip if same message shown in last 3 seconds
        var now = Date.now();
        if (_toastDupeCache[message] && (now - _toastDupeCache[message]) < 3000) return;
        _toastDupeCache[message] = now;

        var toast = document.createElement('div');
        toast.className = 'bgp-toast';
        var bg = type === 'success' ? 'rgba(34,197,94,0.95)' : type === 'error' ? 'rgba(239,68,68,0.95)' : 'rgba(59,130,246,0.95)';
        toast.style.cssText = 'position:fixed;right:16px;z-index:100000;padding:10px 18px;border-radius:10px;font-size:13px;font-weight:500;color:white;font-family:"Inter",sans-serif;box-shadow:0 8px 24px rgba(0,0,0,0.3);backdrop-filter:blur(12px);transition:all 0.3s ease;transform:translateX(120%);max-width:380px;line-height:1.4;cursor:pointer;background:' + bg;

        toast.textContent = message;
        toast.onclick = function() { removeToast(toast); };
        document.body.appendChild(toast);
        _toasts.push(toast);
        repositionToasts();
        // Animate in
        requestAnimationFrame(function() {
            requestAnimationFrame(function() { toast.style.transform = 'translateX(0)'; });
        });
        // Auto-dismiss
        var duration = type === 'error' ? 6000 : 3500;
        setTimeout(function() { removeToast(toast); }, duration);
    };

    function removeToast(toast) {
        toast.style.transform = 'translateX(120%)';
        toast.style.opacity = '0';
        setTimeout(function() {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
            _toasts = _toasts.filter(function(t) { return t !== toast; });
            repositionToasts();
        }, 300);
    }

    function repositionToasts() {
        var bottom = 16;
        for (var i = _toasts.length - 1; i >= 0; i--) {
            _toasts[i].style.top = 'auto';
            _toasts[i].style.bottom = bottom + 'px';
            bottom += _toasts[i].offsetHeight + 8;
        }
    }

    // ═════════════════════════════════════════════════════════════════
    // 7. FORM VALIDATION GATE — catch missing fields before doc gen
    // ═════════════════════════════════════════════════════════════════
    function validateForm(docType) {
        var errors = [];
        var clientName = (document.getElementById('clientName').value || '').trim();
        var sqft = parseFloat(document.getElementById('sqft').value) || 0;
        var laborCount = document.querySelectorAll('#laborItemsContainer .li-row').length;
        var matCount = document.querySelectorAll('#matItemsContainer .mi-row').length;

        if (!clientName) errors.push('Client name is empty');
        if (sqft <= 0) errors.push('Square footage is 0');

        if (docType === 'labor' || docType === 'change_order') {
            if (laborCount === 0) errors.push('No labor items');
        }
        if (docType === 'materials') {
            if (matCount === 0) errors.push('No material items');
        }

        if (errors.length > 0) {
            var proceed = confirm('⚠️ Missing fields:\n\n• ' + errors.join('\n• ') + '\n\nGenerate document anyway?');
            if (!proceed) return false;
        }
        return true;
    }

    // Wrap the generate functions with validation
    var _validatedGenLabor = window.generateLabor;
    window.generateLabor = function() {
        if (!validateForm('labor')) return;
        _validatedGenLabor.apply(this, arguments);
    };
    var _validatedGenMats = window.generateMaterials;
    window.generateMaterials = function() {
        if (!validateForm('materials')) return;
        _validatedGenMats.apply(this, arguments);
    };
    var _validatedGenCO = window.generateChangeOrder;
    window.generateChangeOrder = function() {
        if (!validateForm('change_order')) return;
        _validatedGenCO.apply(this, arguments);
    };

    // ═════════════════════════════════════════════════════════════════
    // 8. KEYBOARD SHORTCUTS
    // ═════════════════════════════════════════════════════════════════
    document.addEventListener('keydown', function(e) {
        // Don't intercept when typing in inputs/textareas
        var tag = (e.target.tagName || '').toLowerCase();
        var isInput = tag === 'input' || tag === 'textarea' || tag === 'select' || e.target.isContentEditable;

        // Ctrl+K — Command Palette (always works)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            openCommandPalette();
            return;
        }

        if (isInput && !e.ctrlKey && !e.metaKey) return;

        // Ctrl+S — Save job
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            if (typeof saveJob === 'function') saveJob();
            return;
        }

        // Ctrl+Enter — Generate labor estimate
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (typeof generateLabor === 'function') generateLabor();
            return;
        }

        // Ctrl+Shift+A — Toggle AI panel
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'a' || e.key === 'A')) {
            e.preventDefault();
            var toggle = document.getElementById('bgai-toggle');
            if (toggle) toggle.click();
            else {
                var wdBtn = document.getElementById('wd-ai');
                if (wdBtn) wdBtn.click();
            }
            return;
        }

        // Ctrl+D — Duplicate
        if ((e.ctrlKey || e.metaKey) && (e.key === 'd' || e.key === 'D')) {
            e.preventDefault();
            if (typeof duplicateCurrentBid === 'function') duplicateCurrentBid();
            return;
        }
    });

    // Inject shortcut hints into button row
    var btnRow = document.querySelector('.btn-row');
    if (btnRow) {
        var hint = document.createElement('div');
        hint.style.cssText = 'width:100%;font-size:10px;color:#52525b;margin-top:4px;font-family:"Inter",sans-serif;';
        hint.innerHTML = '<kbd style="background:rgba(255,255,255,0.06);padding:1px 5px;border-radius:3px;font-size:9px;border:1px solid rgba(255,255,255,0.1)">Ctrl+S</kbd> Save &nbsp; <kbd style="background:rgba(255,255,255,0.06);padding:1px 5px;border-radius:3px;font-size:9px;border:1px solid rgba(255,255,255,0.1)">Ctrl+Enter</kbd> Generate &nbsp; <kbd style="background:rgba(255,255,255,0.06);padding:1px 5px;border-radius:3px;font-size:9px;border:1px solid rgba(255,255,255,0.1)">Ctrl+K</kbd> Commands &nbsp; <kbd style="background:rgba(255,255,255,0.06);padding:1px 5px;border-radius:3px;font-size:9px;border:1px solid rgba(255,255,255,0.1)">Ctrl+Shift+A</kbd> AI';
        btnRow.appendChild(hint);
    }

    // ═════════════════════════════════════════════════════════════════
    // 9. AI PRE-FLIGHT CONTEXT CHECK
    // ═════════════════════════════════════════════════════════════════
    BidGen.on('doc:generating', function(data) {
        var laborCount = document.querySelectorAll('#laborItemsContainer .li-row').length;
        var matCount = document.querySelectorAll('#matItemsContainer .mi-row').length;
        if (laborCount === 0 && matCount === 0) {
            console.warn('[BidGen Pro] Generating doc with no line items');
        }
    });

    // Patch AI send to warn if form is empty
    var _origAiSend = window.aiSendMessage;
    if (typeof _origAiSend === 'function') {
        window.aiSendMessage = function() {
            var input = document.getElementById('aiChatInput');
            var msg = input ? input.value.trim() : '';
            var laborCount = document.querySelectorAll('#laborItemsContainer .li-row').length;
            var clientName = (document.getElementById('clientName').value || '').trim();

            // If the user is asking for a document but form is empty, add a gentle note
            if (msg && /generat|change order|quote|bid|estimate|scope/i.test(msg) && !clientName && laborCount === 0) {
                // Prepend context note
                input.value = msg + '\n\n[Note: The BidGen form is currently empty — please ask me for the details you need to generate this document.]';
            }
            _origAiSend.apply(this, arguments);
        };
    }

    // ═════════════════════════════════════════════════════════════════
    // 10. QUICK DUPLICATE
    // ═════════════════════════════════════════════════════════════════
    window.duplicateCurrentBid = function() {
        // Reset invoice ID so it gets a new one
        window._lastInvoiceId = null;

        // Clear the client name to force review
        var cn = document.getElementById('clientName');
        var origName = cn.value;
        cn.value = origName ? origName + ' (Copy)' : '';

        // Reset date to today
        document.getElementById('estimateDate').value = new Date().toISOString().split('T')[0];

        // Recalculate
        if (typeof liveCalc === 'function') liveCalc();

        showNotification('📋 Bid duplicated. Update client info and generate.', 'success');
        window.scrollTo({ top: 0, behavior: 'smooth' });
        cn.focus();
        cn.select();
        BidGen.emit('form:duplicated', { originalClient: origName });
    };

    // Add duplicate button to button row
    if (btnRow) {
        var dupBtn = document.createElement('button');
        dupBtn.className = 'btn btn-save';
        dupBtn.innerHTML = '📋 Duplicate';
        dupBtn.title = 'Clone this bid to a new invoice (Ctrl+D)';
        dupBtn.onclick = duplicateCurrentBid;
        btnRow.appendChild(dupBtn);
    }

    // ═════════════════════════════════════════════════════════════════
    // 11. RECENT DOCS QUICK-ACCESS
    // ═════════════════════════════════════════════════════════════════
    var _recentDocs = [];
    try {
        _recentDocs = JSON.parse(localStorage.getItem('bgp_recent_docs') || '[]');
    } catch(e) {}

    BidGen.on('doc:generated', function(data) {
        if (!data.invoiceId) return;
        // Remove if already in list
        _recentDocs = _recentDocs.filter(function(d) { return d.id !== data.invoiceId; });
        _recentDocs.unshift({
            id: data.invoiceId,
            type: data.type,
            client: (document.getElementById('clientName').value || '').trim() || 'Unknown',
            time: Date.now()
        });
        // Keep only last 8
        _recentDocs = _recentDocs.slice(0, 8);
        try { localStorage.setItem('bgp_recent_docs', JSON.stringify(_recentDocs)); } catch(e) {}
        renderRecentBar();
    });

    function renderRecentBar() {
        var bar = document.getElementById('bgp-recent');
        if (!bar) {
            bar = document.createElement('div');
            bar.id = 'bgp-recent';
            bar.style.cssText = 'margin-bottom:12px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;';
            // Insert before button row
            var btnR = document.querySelector('.btn-row');
            if (btnR && btnR.parentNode) btnR.parentNode.insertBefore(bar, btnR);
        }
        if (_recentDocs.length === 0) { bar.style.display = 'none'; return; }
        bar.style.display = 'flex';
        var icons = { labor: '📄', materials: '📦', change_order: '🔴', quote: '💰', temporary: '📝' };
        bar.innerHTML = '<span style="font-size:10px;color:#52525b;font-weight:500;margin-right:4px">Recent:</span>';
        _recentDocs.slice(0, 5).forEach(function(doc) {
            var elapsed = timeAgo(doc.time);
            var chip = document.createElement('button');
            chip.style.cssText = 'background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:6px;padding:3px 8px;font-size:10px;color:#a1a1aa;cursor:pointer;font-family:"Inter",sans-serif;transition:all 0.15s;display:flex;align-items:center;gap:3px;';
            chip.innerHTML = (icons[doc.type] || '📄') + ' <strong style="color:#d4d4d8">' + escH(doc.client.substring(0,15)) + '</strong> <span style="opacity:0.5">' + escH(doc.id) + '</span> <span style="opacity:0.3">' + elapsed + '</span>';
            chip.title = doc.id + ' — Click to reopen';
            chip.onmouseover = function() { this.style.background = 'rgba(255,255,255,0.08)'; };
            chip.onmouseout = function() { this.style.background = 'rgba(255,255,255,0.04)'; };
            chip.onclick = function() {
                if (typeof reopenDoc === 'function') reopenDoc(doc.id);
            };
            bar.appendChild(chip);
        });
    }
    renderRecentBar();

    // ═════════════════════════════════════════════════════════════════
    // 12. CONNECTION HEALTH MONITOR
    // ═════════════════════════════════════════════════════════════════
    window.BidGen.checkHealth = function() {
        var results = {
            firebase: false,
            proxy: false,
            scripts: bootReport.scripts.filter(function(s) { return s.loaded; }).length + '/' + bootReport.scripts.length,
            dom: bootReport.dom.filter(function(d) { return d.exists; }).length + '/' + bootReport.dom.length,
            functions: bootReport.functions.filter(function(f) { return f.exists; }).length + '/' + bootReport.functions.length
        };

        // Test Firebase
        try {
            if (typeof db !== 'undefined' && db) {
                db.ref('.info/connected').once('value').then(function(snap) {
                    results.firebase = snap.val() === true;
                    renderHealthBadge(results);
                }).catch(function() { renderHealthBadge(results); });
            }
        } catch(e) {}

        // Test proxy
        fetch('https://watts-ai-proxy.wattssafetyinstalls.workers.dev/', { method: 'GET', mode: 'cors' })
            .then(function() { results.proxy = true; renderHealthBadge(results); })
            .catch(function() { renderHealthBadge(results); });

        return results;
    };

    function renderHealthBadge(results) {
        var badge = document.getElementById('bgp-health');
        if (!badge) return;
        var allGood = results.firebase && results.proxy &&
            results.scripts === bootReport.scripts.length + '/' + bootReport.scripts.length;
        badge.style.background = allGood ? 'rgba(34,197,94,0.12)' : 'rgba(251,191,36,0.12)';
        badge.style.color = allGood ? '#4ade80' : '#fbbf24';
        badge.innerHTML = (allGood ? '●' : '◔') + ' System ' + (allGood ? 'OK' : 'Issue');
        badge.title = 'Firebase: ' + (results.firebase ? '✓' : '✗') +
            ' | Proxy: ' + (results.proxy ? '✓' : '✗') +
            ' | Scripts: ' + results.scripts +
            ' | DOM: ' + results.dom +
            ' | Functions: ' + results.functions;
    }

    // Add health indicator to header area
    var syncDevice = document.getElementById('syncDevice');
    if (syncDevice) {
        var healthBadge = document.createElement('span');
        healthBadge.id = 'bgp-health';
        healthBadge.style.cssText = 'display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:8px;font-size:9px;font-weight:600;cursor:pointer;margin-left:8px;transition:all 0.2s;';
        healthBadge.onclick = function() { BidGen.checkHealth(); showNotification('Running health check...', 'info'); };
        syncDevice.parentNode.insertBefore(healthBadge, syncDevice.nextSibling);
    }

    // Auto health check on boot and every 5 minutes
    setTimeout(function() { BidGen.checkHealth(); }, 3000);
    setInterval(function() { BidGen.checkHealth(); }, 300000);

    // ═════════════════════════════════════════════════════════════════
    // 13. BATCH INVOICE OPS — expose via event bus
    // ═════════════════════════════════════════════════════════════════
    window.BidGen.batchUpdateStatus = function(invoiceIds, newStatus) {
        if (!invoiceIds || !invoiceIds.length) return;
        if (!window.userPIN || typeof invoiceData === 'undefined') {
            showNotification('Not logged in or invoice data not loaded.', 'error');
            return;
        }
        var moved = 0;
        var hashedPIN = hashPIN(window.userPIN);
        invoiceIds.forEach(function(id) {
            var inv = null;
            var fromStatus = null;
            ['temporary', 'permanent', 'lost'].forEach(function(s) {
                if (invoiceData[s] && invoiceData[s][id]) {
                    inv = invoiceData[s][id];
                    fromStatus = s;
                }
            });
            if (!inv || fromStatus === newStatus) return;

            // Move
            inv.status = newStatus;
            inv.statusChangedAt = Date.now();
            if (newStatus === 'permanent') inv.awardedDate = new Date().toISOString();
            if (newStatus === 'lost') inv.lostDate = new Date().toISOString();

            invoiceData[newStatus][id] = inv;
            delete invoiceData[fromStatus][id];

            if (typeof db !== 'undefined' && db) {
                db.ref('invoices/' + hashedPIN + '/' + fromStatus + '/' + id).remove();
                db.ref('invoices/' + hashedPIN + '/' + newStatus + '/' + id).set(inv);
            }
            moved++;
        });
        if (moved > 0) {
            showNotification('✅ Moved ' + moved + ' invoice(s) to ' + newStatus, 'success');
            if (typeof invRenderList === 'function') invRenderList();
            if (typeof updateInvoiceStats === 'function') updateInvoiceStats();
            BidGen.emit('invoices:batchUpdated', { count: moved, newStatus: newStatus });
        }
    };

    // ═════════════════════════════════════════════════════════════════
    // 14. SMART DEFAULTS — remember preferences across sessions
    // ═════════════════════════════════════════════════════════════════
    var DEFAULTS_KEY = 'bgp_smart_defaults';

    function saveDefaults() {
        var defaults = {
            tradeType: gvSafe('tradeType'),
            brandSelect: gvSafe('brandSelect'),
            jobCity: gvSafe('jobCity'),
            materialsMarkup: gvSafe('materialsMarkup'),
            companyName: gvSafe('companyName'),
            licenseNum: gvSafe('licenseNum'),
            phone: gvSafe('phone'),
            email: gvSafe('email')
        };
        try { localStorage.setItem(DEFAULTS_KEY, JSON.stringify(defaults)); } catch(e) {}
    }

    function loadDefaults() {
        try {
            var saved = JSON.parse(localStorage.getItem(DEFAULTS_KEY) || '{}');
            if (!saved || typeof saved !== 'object') return;
            // Only fill empty fields
            Object.keys(saved).forEach(function(key) {
                if (!saved[key]) return;
                var el = document.getElementById(key);
                if (el && !el.value) el.value = saved[key];
            });
        } catch(e) {}
    }

    // Save defaults when docs are generated
    BidGen.on('doc:generated', saveDefaults);
    BidGen.on('job:saved', saveDefaults);

    // Load defaults on boot (after login)
    setTimeout(loadDefaults, 1500);

    // ═════════════════════════════════════════════════════════════════
    // 15. COMMAND PALETTE — Ctrl+K spotlight for any action
    // ═════════════════════════════════════════════════════════════════
    var _paletteOpen = false;

    function getCommands() {
        return [
            { id: 'gen-labor', label: 'Generate Labor Estimate', desc: 'Open Estimate A', icon: '📄', action: function() { generateLabor(); } },
            { id: 'gen-materials', label: 'Generate Materials Estimate', desc: 'Open Estimate B', icon: '📦', action: function() { generateMaterials(); } },
            { id: 'gen-co', label: 'Generate Change Order', desc: 'Create scope amendment', icon: '🔴', action: function() { generateChangeOrder(); } },
            { id: 'save-job', label: 'Save Current Job', desc: 'Save to Firebase (Ctrl+S)', icon: '💾', action: function() { saveJob(); } },
            { id: 'clear-form', label: 'Clear Form', desc: 'Reset all fields', icon: '🗑️', action: function() { clearForm(); } },
            { id: 'duplicate', label: 'Duplicate Bid', desc: 'Clone to new invoice (Ctrl+D)', icon: '📋', action: function() { duplicateCurrentBid(); } },
            { id: 'open-ai', label: 'Open AI Assistant', desc: 'Floating AI panel (Ctrl+Shift+A)', icon: '🤖', action: function() {
                var t = document.getElementById('bgai-toggle'); if (t) t.click();
                else { var w = document.getElementById('wd-ai'); if (w) w.click(); }
            }},
            { id: 'open-fieldcalc', label: 'Open Field Calculator', desc: 'Material calculator + room scanner', icon: '📐', action: function() {
                var t = document.getElementById('fieldCalcToggle'); if (t) t.click();
                else { var w = document.getElementById('wd-fieldcalc'); if (w) w.click(); }
            }},
            { id: 'open-templates', label: 'Open Template Manager', desc: 'Pre-built job templates', icon: '📑', action: function() { if (typeof openTemplateManager === 'function') openTemplateManager(); } },
            { id: 'open-scanner', label: 'Open Document Scanner', desc: 'Scan invoices with AI', icon: '📸', action: function() { if (typeof openScanner === 'function') openScanner(); } },
            { id: 'open-clients', label: 'Client Insights', desc: 'Job history & patterns', icon: '👥', action: function() { if (typeof openClientInsights === 'function') openClientInsights(); } },
            { id: 'health-check', label: 'System Health Check', desc: 'Test Firebase, proxy, scripts', icon: '🏥', action: function() { BidGen.checkHealth(); } },
            { id: 'trade-flooring', label: 'Switch to Flooring', desc: 'Load flooring presets', icon: '🪵', action: function() { document.getElementById('tradeType').value = 'flooring'; onTradeChange(); } },
            { id: 'trade-painting', label: 'Switch to Painting', desc: 'Load painting presets', icon: '🎨', action: function() { document.getElementById('tradeType').value = 'painting'; onTradeChange(); } },
            { id: 'trade-plumbing', label: 'Switch to Plumbing', desc: 'Load plumbing presets', icon: '🔧', action: function() { document.getElementById('tradeType').value = 'plumbing'; onTradeChange(); } },
            { id: 'trade-electrical', label: 'Switch to Electrical', desc: 'Load electrical presets', icon: '⚡', action: function() { document.getElementById('tradeType').value = 'electrical'; onTradeChange(); } },
            { id: 'trade-general', label: 'Switch to General', desc: 'Load general presets', icon: '🔨', action: function() { document.getElementById('tradeType').value = 'general'; onTradeChange(); } }
        ];
    }

    function openCommandPalette() {
        if (_paletteOpen) { closeCommandPalette(); return; }
        _paletteOpen = true;

        var overlay = document.createElement('div');
        overlay.id = 'bgp-cmd-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;z-index:100001;background:rgba(0,0,0,0.6);backdrop-filter:blur(4px);display:flex;align-items:flex-start;justify-content:center;padding-top:min(20vh,160px);';
        overlay.onclick = function(e) { if (e.target === overlay) closeCommandPalette(); };

        var palette = document.createElement('div');
        palette.id = 'bgp-cmd-palette';
        palette.style.cssText = 'background:rgba(15,15,20,0.98);border:1px solid rgba(255,255,255,0.1);border-radius:14px;width:min(520px,90vw);max-height:420px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.5),0 0 0 1px rgba(255,255,255,0.04);font-family:"Inter",sans-serif;display:flex;flex-direction:column;';

        var input = document.createElement('input');
        input.id = 'bgp-cmd-input';
        input.type = 'text';
        input.placeholder = 'Type a command...';
        input.style.cssText = 'background:transparent;border:none;border-bottom:1px solid rgba(255,255,255,0.08);padding:16px 20px;color:#e4e4e7;font-size:15px;font-family:"Inter",sans-serif;outline:none;width:100%;';

        var list = document.createElement('div');
        list.id = 'bgp-cmd-list';
        list.style.cssText = 'overflow-y:auto;max-height:340px;padding:6px;';

        palette.appendChild(input);
        palette.appendChild(list);
        overlay.appendChild(palette);
        document.body.appendChild(overlay);

        var commands = getCommands();
        var selectedIdx = 0;

        function renderList(filter) {
            var filtered = commands;
            if (filter) {
                var q = filter.toLowerCase();
                filtered = commands.filter(function(c) {
                    return c.label.toLowerCase().includes(q) || c.desc.toLowerCase().includes(q);
                });
            }
            selectedIdx = 0;
            list.innerHTML = '';
            filtered.forEach(function(cmd, i) {
                var item = document.createElement('div');
                item.style.cssText = 'display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:8px;cursor:pointer;transition:background 0.1s;';
                if (i === selectedIdx) item.style.background = 'rgba(59,130,246,0.12)';
                item.setAttribute('data-idx', i);
                item.innerHTML = '<span style="font-size:18px;width:28px;text-align:center;flex-shrink:0">' + cmd.icon + '</span>'
                    + '<div style="flex:1;min-width:0"><div style="color:#e4e4e7;font-size:13px;font-weight:500">' + escH(cmd.label) + '</div>'
                    + '<div style="color:#71717a;font-size:11px">' + escH(cmd.desc) + '</div></div>';
                item.onmouseover = function() {
                    list.querySelectorAll('div[data-idx]').forEach(function(d) { d.style.background = 'transparent'; });
                    this.style.background = 'rgba(59,130,246,0.12)';
                    selectedIdx = i;
                };
                item.onclick = function() {
                    closeCommandPalette();
                    cmd.action();
                };
                list.appendChild(item);
            });
        }

        renderList('');
        input.focus();

        input.oninput = function() { renderList(input.value); };
        input.onkeydown = function(e) {
            var items = list.querySelectorAll('div[data-idx]');
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedIdx = Math.min(selectedIdx + 1, items.length - 1);
                items.forEach(function(d, i) { d.style.background = i === selectedIdx ? 'rgba(59,130,246,0.12)' : 'transparent'; });
                if (items[selectedIdx]) items[selectedIdx].scrollIntoView({ block: 'nearest' });
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedIdx = Math.max(selectedIdx - 1, 0);
                items.forEach(function(d, i) { d.style.background = i === selectedIdx ? 'rgba(59,130,246,0.12)' : 'transparent'; });
                if (items[selectedIdx]) items[selectedIdx].scrollIntoView({ block: 'nearest' });
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (items[selectedIdx]) items[selectedIdx].click();
            } else if (e.key === 'Escape') {
                closeCommandPalette();
            }
        };
    }

    function closeCommandPalette() {
        _paletteOpen = false;
        var overlay = document.getElementById('bgp-cmd-overlay');
        if (overlay) overlay.remove();
    }

    window.openCommandPalette = openCommandPalette;

    // ═════════════════════════════════════════════════════════════════
    // UTILITY
    // ═════════════════════════════════════════════════════════════════
    function gvSafe(id) {
        var el = document.getElementById(id);
        return el ? el.value : '';
    }

    function escH(s) {
        return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function timeAgo(ts) {
        var diff = Date.now() - ts;
        var mins = Math.floor(diff / 60000);
        if (mins < 1) return 'now';
        if (mins < 60) return mins + 'm';
        var hrs = Math.floor(mins / 60);
        if (hrs < 24) return hrs + 'h';
        var days = Math.floor(hrs / 24);
        return days + 'd';
    }

    // ═════════════════════════════════════════════════════════════════
    // REGISTER WITH WIDGET DOCK
    // ═════════════════════════════════════════════════════════════════
    if (typeof window.widgetDockRegister === 'function') {
        window.widgetDockRegister({
            id: 'cmd',
            label: 'Commands (Ctrl+K)',
            icon: '⌘',
            toggle: openCommandPalette,
            isOpen: function() { return _paletteOpen; }
        });
    }

    // ═════════════════════════════════════════════════════════════════
    // DONE
    // ═════════════════════════════════════════════════════════════════
    console.log('[BidGen Pro] ✅ All 15 optimizations active');
    BidGen.emit('pro:ready', { version: '1.0', optimizations: 15 });
}

})();
