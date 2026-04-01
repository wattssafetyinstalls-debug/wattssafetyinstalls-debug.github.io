// =====================================================================
// CLIENT PORTAL — BidGen Integration Module
// Publishes invoices to portal, tracks engagement, shows dashboard,
// sends notifications when clients view/sign/message.
// =====================================================================
(function() {
'use strict';

console.log('[Client Portal] Script loaded — waiting for BidGen login...');

var PORTAL_BASE = '';  // auto-detected below
var FINAL_INVOICE_BASE = '';  // for final invoice portal links
var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';

// Detect portal base URL from current location
(function() {
    var loc = window.location;
    var base = (loc.hostname === 'localhost' || loc.hostname === '127.0.0.1')
        ? loc.protocol + '//' + loc.host + '/tools/bidgen/'
        : loc.protocol + '//' + loc.hostname + '/tools/bidgen/';
    PORTAL_BASE = base + 'portal.html';
    FINAL_INVOICE_BASE = base + 'final-invoice.html';
})();

function waitForBidGen(fn) {
    var attempts = 0;
    var iv = setInterval(function() {
        attempts++;
        // userPIN is a let, not on window — check via the sync device label which shows PIN after login
        var loggedIn = false;
        try {
            var syncEl = document.getElementById('syncDevice');
            loggedIn = syncEl && syncEl.textContent && syncEl.textContent.indexOf('PIN:') !== -1;
        } catch(e) {}
        var hasHash = typeof window.hashPIN === 'function';
        if (hasHash && loggedIn) {
            clearInterval(iv);
            console.log('[Client Portal] BidGen ready — login detected');
            fn();
        }
        if (attempts > 120) {
            clearInterval(iv);
            console.warn('[Client Portal] Timed out. hashPIN:', hasHash, '| loggedIn:', loggedIn);
        }
    }, 500);
}

waitForBidGen(function() {
    console.log('[Client Portal] Initializing...');
    initPortalSystem();
});

function initPortalSystem() {
    var db = firebase.database();
    var _pin = window._bidgenUserPIN ? window._bidgenUserPIN() : sessionStorage.getItem('bid_pin');
    if (!_pin) { console.warn('[Client Portal] No PIN found'); return; }
    var hashedPIN = hashPIN(_pin);

    // ================================================================
    // 1. PUBLISH INVOICE TO PORTAL
    // ================================================================
    window.publishToPortal = async function(invoiceId) {
        var invoice = findInvoiceGlobal(invoiceId);
        if (!invoice) {
            showNotification('Invoice not found: ' + invoiceId, 'error');
            return;
        }

        // Detect document type and change order context
        var docType = invoice.type || invoice.documentType || 'quote';
        var isChangeOrder = docType === 'change_order' || (invoice.id && invoice.id.indexOf('CO-') === 0);
        var originalAmount = 0;

        if (isChangeOrder) {
            // 1. Try in-memory lookup via explicit originalInvoiceId (most reliable)
            if (invoice.originalInvoiceId) {
                var origInv = findInvoiceGlobal(invoice.originalInvoiceId);
                if (origInv && origInv.amount !== invoice.amount) {
                    originalAmount = origInv.amount || 0;
                }
            }
            // 2. Try stored originalAmount — but ONLY if it differs from the CO amount (self-match guard)
            if (!originalAmount && invoice.originalAmount && invoice.originalAmount !== invoice.amount) {
                originalAmount = invoice.originalAmount;
            }
            // NOTE: Removed aggressive Firebase name-matching fallback.
            // It was fabricating original amounts by matching wrong invoices or self-matching.
            // Original contract amount should only come from explicit links, never guesses.
        }

        var materialsMarkup = invoice.materialsMarkup || (invoice.jobDetails || {}).materialsMarkup || 0;

        // Build portal-safe data (strip any sensitive internal fields)
        var portalData = {
            invoice: {
                id: invoice.id,
                clientName: invoice.clientName,
                estimateDate: invoice.estimateDate,
                expiresDate: invoice.expiresDate,
                amount: invoice.amount,
                laborTotal: invoice.laborTotal,
                materialsTotal: invoice.materialsTotal,
                status: invoice.status,
                documentType: isChangeOrder ? 'change_order' : docType,
                brand: invoice.brand || invoice.brandSelect || gv('brandSelect') || 'wsi',
                // Change order context
                originalInvoiceId: isChangeOrder ? (invoice.originalInvoiceId || '') : '',
                originalAmount: isChangeOrder ? originalAmount : 0,
                revisedTotal: isChangeOrder ? (originalAmount + (invoice.amount || 0)) : 0,
                materialsMarkup: materialsMarkup,
                jobDetails: {
                    complexName: (invoice.jobDetails || {}).complexName || '',
                    unitNum: (invoice.jobDetails || {}).unitNum || '',
                    jobCity: (invoice.jobDetails || {}).jobCity || '',
                    sqft: (invoice.jobDetails || {}).sqft || 0,
                    areaDesc: (invoice.jobDetails || {}).areaDesc || '',
                    tradeType: (invoice.jobDetails || {}).tradeType || '',
                    laborItems: invoice.laborItems || (invoice.jobDetails || {}).laborItems || [],
                    matItems: invoice.materialItems || (invoice.jobDetails || {}).matItems || [],
                    scopeItems: invoice.scope || (invoice.jobDetails || {}).scopeItems || [],
                    noteItems: invoice.notes || (invoice.jobDetails || {}).noteItems || [],
                    disclaimer: invoice.disclaimer || (invoice.jobDetails || {}).disclaimer || ''
                },
                companyInfo: invoice.companyInfo || {
                    companyName: gv('companyName') || 'Watts Safety Installs',
                    licenseNum: gv('licenseNum') || '#54690-25',
                    phone: gv('phone') || '(405) 410-6402',
                    email: gv('email') || 'Justin.Watts@WattsATPContractor.com'
                }
            },
            publishedAt: new Date().toISOString(),
            publishedBy: 'contractor',
            viewCount: 0
        };

        // Write to portal path in Firebase
        db.ref('portal/' + hashedPIN + '/' + invoiceId).set(portalData).then(function() {
            var portalUrl = buildPortalUrl(invoiceId);

            // Store portal link on the invoice
            invoice.portalLink = {
                url: portalUrl,
                publishedAt: portalData.publishedAt,
                viewCount: 0
            };
            saveInvoiceToFirebase(invoice);

            // Show share modal with originalAmount on invoice for SMS text
            invoice.originalAmount = originalAmount;
            invoice.revisedTotal = originalAmount + (invoice.amount || 0);
            showPortalShareModal(invoice, portalUrl);

            showNotification('🌐 Portal link created! Share with your client.', 'success');

            if (typeof BidGen !== 'undefined' && BidGen.emit) {
                BidGen.emit('portal:published', { invoiceId: invoiceId, url: portalUrl });
            }
        }).catch(function(err) {
            showNotification('Failed to publish: ' + err.message, 'error');
        });
    };

    function buildPortalUrl(invoiceId, isFinalInvoice) {
        var base = isFinalInvoice ? FINAL_INVOICE_BASE : PORTAL_BASE;
        return base + '?id=' + encodeURIComponent(invoiceId) + '&pin=' + encodeURIComponent(hashedPIN);
    }

    // ================================================================
    // 2. SHARE MODAL — Copy link, text, email
    // ================================================================
    function showPortalShareModal(invoice, portalUrl) {
        var existing = document.getElementById('portalShareModal');
        if (existing) existing.remove();

        var brandName = (invoice.companyInfo && invoice.companyInfo.companyName) || 'Watts Safety Installs';
        var clientName = invoice.clientName || 'Client';
        var total = (invoice.amount || 0).toFixed(2);
        var docType = invoice.type || invoice.documentType || 'quote';
        var isCO = docType === 'change_order' || (invoice.id && invoice.id.indexOf('CO-') === 0);
        var laborAmt = (invoice.laborTotal || 0).toFixed(2);
        var matAmt = (invoice.materialsTotal || 0).toFixed(2);
        var origAmt = invoice.originalAmount || 0;
        var revisedAmt = origAmt > 0 ? (origAmt + (invoice.amount || 0)).toFixed(2) : '';

        var smsBody, emailSubject, emailBody;
        if (isCO) {
            smsBody = brandName + ': Hi ' + clientName + ', a change order (#' + invoice.id + ') has been issued for your project. Additional work: $' + total + ' (Labor: $' + laborAmt + ' / Materials: $' + matAmt + ').' + (revisedAmt ? ' Revised project total: $' + revisedAmt + '.' : '') + ' Review & approve: ' + portalUrl + ' — Justin Watts (405) 410-6402';
            emailSubject = encodeURIComponent('Change Order from ' + brandName + ' — #' + invoice.id);
            emailBody = encodeURIComponent('Hi ' + clientName + ',\n\nA change order has been issued for your project. Please review and approve online:\n\n' + portalUrl + '\n\nChange Order Details:\n  CO #: ' + invoice.id + (invoice.originalInvoiceId ? '\n  Original Estimate: #' + invoice.originalInvoiceId : '') + '\n  Labor: $' + laborAmt + '\n  Materials & Consumables: $' + matAmt + '\n  Change Order Total: $' + total + (origAmt > 0 ? '\n\n  Original Contract: $' + origAmt.toFixed(2) + '\n  This Change Order: + $' + total + '\n  Revised Project Total: $' + revisedAmt : '') + '\n\nIMPORTANT: Materials & consumables ($' + matAmt + ') are required up front upon due notice before work begins. Labor balances are due upon completion.\n\nYou can review the full scope, ask questions, and approve with a digital signature — all from your phone or computer.\n\nBest regards,\nJustin Watts\n' + brandName + '\nNebraska Licensed Contractor #54690-25\n(405) 410-6402');
        } else {
            smsBody = brandName + ': Hi ' + clientName + ', your estimate #' + invoice.id + ' ($' + total + ') is ready for review. View, approve & sign online: ' + portalUrl + ' — Justin Watts (405) 410-6402';
            emailSubject = encodeURIComponent('Your Estimate from ' + brandName + ' — #' + invoice.id);
            emailBody = encodeURIComponent('Hi ' + clientName + ',\n\nYour estimate is ready to review, approve, and sign online:\n\n' + portalUrl + '\n\nEstimate Details:\n  Invoice: ' + invoice.id + '\n  Labor: $' + laborAmt + '\n  Materials: $' + matAmt + '\n  Total: $' + total + '\n\nYou can review the full scope of work, ask questions, and accept with a digital signature — all from your phone or computer.\n\nIf you have any questions, just reply to this email or call me.\n\nBest regards,\nJustin Watts\n' + brandName + '\nNebraska Licensed Contractor #54690-25\n(405) 410-6402');
        }

        var modal = document.createElement('div');
        modal.id = 'portalShareModal';
        modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px;';
        modal.innerHTML = '\
<div style="background:#0f172a;border:1px solid rgba(59,130,246,0.3);border-radius:20px;max-width:520px;width:100%;padding:28px;box-shadow:0 25px 60px rgba(0,0,0,0.5)">\
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">\
        <div style="display:flex;align-items:center;gap:10px">\
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:16px">🌐</div>\
            <div><div style="font-size:16px;font-weight:700;color:white">Client Portal Link</div>\
            <div style="font-size:11px;color:#64748b">Share this link with your client</div></div>\
        </div>\
        <button onclick="document.getElementById(\'portalShareModal\').remove()" style="background:none;border:none;color:#64748b;font-size:22px;cursor:pointer;padding:4px">&times;</button>\
    </div>\
    \
    <div style="background:#1e293b;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:14px;margin-bottom:16px">\
        <div style="font-size:10px;color:#64748b;text-transform:uppercase;font-weight:700;letter-spacing:0.5px;margin-bottom:6px">Portal URL</div>\
        <div style="display:flex;gap:8px">\
            <input type="text" value="' + portalUrl.replace(/"/g, '&quot;') + '" readonly id="portalUrlCopy" style="flex:1;background:#0f172a;border:1px solid rgba(255,255,255,0.1);color:#3b82f6;padding:10px 12px;border-radius:8px;font-size:11px;font-family:monospace;outline:none" />\
            <button onclick="cpPortalUrl()" id="cpUrlBtn" style="background:#3b82f6;color:white;border:none;padding:10px 18px;border-radius:8px;font-weight:700;font-size:12px;cursor:pointer;white-space:nowrap">📋 Copy</button>\
        </div>\
    </div>\
    \
    <div style="font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Quick Share</div>\
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:16px">\
        <a href="sms:?body=' + encodeURIComponent(smsBody) + '" style="display:flex;flex-direction:column;align-items:center;gap:6px;background:#1e293b;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:14px 8px;text-decoration:none;transition:all 0.15s;cursor:pointer" onmouseover="this.style.borderColor=\'rgba(34,197,94,0.3)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.06)\'">\
            <span style="font-size:22px">💬</span>\
            <span style="font-size:11px;font-weight:600;color:#22c55e">Text</span>\
        </a>\
        <a href="mailto:?subject=' + emailSubject + '&body=' + emailBody + '" style="display:flex;flex-direction:column;align-items:center;gap:6px;background:#1e293b;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:14px 8px;text-decoration:none;transition:all 0.15s;cursor:pointer" onmouseover="this.style.borderColor=\'rgba(59,130,246,0.3)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.06)\'">\
            <span style="font-size:22px">📧</span>\
            <span style="font-size:11px;font-weight:600;color:#3b82f6">Email</span>\
        </a>\
        <button onclick="cpPortalUrl();window.open(\'https://wa.me/?text=' + encodeURIComponent(smsBody) + '\',\'_blank\')" style="display:flex;flex-direction:column;align-items:center;gap:6px;background:#1e293b;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:14px 8px;cursor:pointer;transition:all 0.15s" onmouseover="this.style.borderColor=\'rgba(37,211,102,0.3)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.06)\'">\
            <span style="font-size:22px">📱</span>\
            <span style="font-size:11px;font-weight:600;color:#25d366">WhatsApp</span>\
        </button>\
    </div>\
    \
    <div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.15);border-radius:10px;padding:14px;margin-bottom:16px">\
        <div style="font-size:12px;color:#93c5fd;font-weight:600;margin-bottom:6px">✨ What your client will see:</div>\
        <ul style="font-size:11px;color:#94a3b8;line-height:1.8;padding-left:16px;margin:0">\
            <li>Professional branded estimate with full scope of work</li>\
            <li>One-click accept with digital signature pad</li>\
            <li>Built-in Q&A — they can ask questions without calling</li>\
            <li>Auto-updates your BidGen dashboard when they interact</li>\
        </ul>\
    </div>\
    \
    <div style="display:flex;gap:8px">\
        <button onclick="document.getElementById(\'portalShareModal\').remove()" style="flex:1;background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:12px;border-radius:10px;font-weight:700;font-size:13px;cursor:pointer;font-family:inherit">Done</button>\
    </div>\
</div>';

        document.body.appendChild(modal);
        modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });
    }

    window.cpPortalUrl = function() {
        var field = document.getElementById('portalUrlCopy');
        if (field) {
            navigator.clipboard.writeText(field.value).then(function() {
                var btn = document.getElementById('cpUrlBtn');
                if (btn) { btn.textContent = '✅ Copied!'; setTimeout(function() { btn.textContent = '📋 Copy'; }, 2000); }
            });
        }
    };

    // ================================================================
    // 3. PORTAL DASHBOARD WIDGET — engagement metrics
    // ================================================================
    function createPortalDashboard() {
        // Add portal tab to invoice detail view
        var style = document.createElement('style');
        style.textContent = '\
.portal-dash{background:#0f172a;border:1px solid rgba(59,130,246,0.2);border-radius:12px;padding:16px;margin-bottom:16px}\
.portal-dash-title{font-size:10px;color:#3b82f6;text-transform:uppercase;font-weight:700;letter-spacing:0.8px;margin-bottom:12px;display:flex;align-items:center;gap:6px}\
.portal-metric{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04)}\
.portal-metric:last-child{border-bottom:none}\
.portal-metric-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px}\
.portal-metric-label{font-size:11px;color:#64748b;font-weight:500}\
.portal-metric-value{font-size:14px;color:#e2e8f0;font-weight:700}\
.portal-metric-right{margin-left:auto;text-align:right}\
.portal-msg-alert{background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);border-radius:10px;padding:12px;margin-top:12px;display:flex;align-items:center;gap:10px;cursor:pointer;transition:all 0.15s}\
.portal-msg-alert:hover{background:rgba(59,130,246,0.15)}\
.portal-timeline{display:flex;align-items:center;gap:4px;margin:12px 0}\
.portal-dot{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border:2px solid}\
.portal-line{flex:1;height:2px}\
';
        document.head.appendChild(style);
    }
    createPortalDashboard();

    // Generate portal status HTML for invoice detail view
    window.getPortalStatusHTML = function(invoice) {
        if (!invoice.portalLink) {
            return '<div style="margin-bottom:16px">\
                <button onclick="publishToPortal(\'' + invoice.id + '\')" style="width:100%;background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:white;border:none;padding:14px;border-radius:12px;font-weight:700;font-size:13px;cursor:pointer;font-family:inherit;display:flex;align-items:center;justify-content:center;gap:8px;transition:all 0.15s">🌐 Create Client Portal Link</button>\
            </div>';
        }

        var h = '<div class="portal-dash">';
        h += '<div class="portal-dash-title">🌐 Client Portal</div>';

        // Status timeline: Published → Viewed → Signed
        var portalData = null;
        var status = 'published';
        
        // We'll load live data async, but show cached state first
        h += '<div id="portalLiveStatus_' + invoice.id + '">';
        h += buildPortalMetrics(invoice, null);
        h += '</div>';

        // Action buttons
        h += '<div style="display:flex;gap:6px;margin-top:12px;flex-wrap:wrap">';
        h += '<button onclick="cpQuickPortal(\'' + invoice.portalLink.url + '\')" style="background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:8px 14px;border-radius:8px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit">📋 Copy Link</button>';
        h += '<button onclick="publishToPortal(\'' + invoice.id + '\')" style="background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:8px 14px;border-radius:8px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit">🔄 Republish</button>';
        h += '<button onclick="openPortalMessages(\'' + invoice.id + '\')" style="background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:8px 14px;border-radius:8px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit">💬 Messages</button>';
        h += '<a href="' + invoice.portalLink.url + '" target="_blank" style="background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:8px 14px;border-radius:8px;font-size:11px;font-weight:600;cursor:pointer;text-decoration:none;font-family:inherit">🔗 Preview</a>';
        h += '</div>';

        h += '</div>';

        // Load live metrics from Firebase
        loadPortalLiveData(invoice.id);

        return h;
    };

    function buildPortalMetrics(invoice, liveData) {
        var vc = liveData ? (liveData.viewCount || 0) : 0;
        var lastView = liveData ? liveData.lastViewedAt : null;
        var isSigned = liveData ? !!liveData.signedAt : false;
        var isDeclined = liveData ? !!liveData.declinedAt : false;
        var unread = liveData ? (liveData.unreadClient || 0) : 0;
        var lastMsg = liveData ? liveData.lastClientMsg : null;

        var h = '';

        // Timeline
        h += '<div class="portal-timeline">';
        h += portalDot('📤', true, '#3b82f6', 'Published');
        h += '<div class="portal-line" style="background:' + (vc > 0 ? '#f59e0b' : 'rgba(255,255,255,0.06)') + '"></div>';
        h += portalDot('👁', vc > 0, '#f59e0b', 'Viewed');
        h += '<div class="portal-line" style="background:' + (isSigned ? '#22c55e' : isDeclined ? '#ef4444' : 'rgba(255,255,255,0.06)') + '"></div>';
        h += portalDot(isSigned ? '✓' : isDeclined ? '✕' : '✍', isSigned || isDeclined, isSigned ? '#22c55e' : isDeclined ? '#ef4444' : '#64748b', isSigned ? 'Signed' : isDeclined ? 'Declined' : 'Awaiting');
        h += '</div>';

        // Metrics row
        h += '<div class="portal-metric">';
        h += '<div class="portal-metric-icon" style="background:rgba(59,130,246,0.1)">👁</div>';
        h += '<div><div class="portal-metric-value">' + vc + ' view' + (vc !== 1 ? 's' : '') + '</div>';
        h += '<div class="portal-metric-label">' + (lastView ? 'Last: ' + timeAgo(lastView) : 'Not yet viewed') + '</div></div>';
        h += '</div>';

        if (isSigned) {
            h += '<div class="portal-metric">';
            h += '<div class="portal-metric-icon" style="background:rgba(34,197,94,0.1)">✅</div>';
            h += '<div><div class="portal-metric-value" style="color:#22c55e">Accepted & Signed</div>';
            h += '<div class="portal-metric-label">by ' + esc(liveData.signerName || 'Client') + ' · ' + timeAgo(liveData.signedAt) + '</div></div>';
            h += '</div>';
        }
        if (isDeclined) {
            h += '<div class="portal-metric">';
            h += '<div class="portal-metric-icon" style="background:rgba(239,68,68,0.1)">❌</div>';
            h += '<div><div class="portal-metric-value" style="color:#ef4444">Declined</div>';
            h += '<div class="portal-metric-label">' + (liveData.declineReason ? 'Reason: ' + esc(liveData.declineReason) : 'No reason given') + ' · ' + timeAgo(liveData.declinedAt) + '</div></div>';
            h += '</div>';
        }

        // Unread messages alert
        if (unread > 0 && lastMsg) {
            h += '<div class="portal-msg-alert" onclick="openPortalMessages(\'' + invoice.id + '\')">';
            h += '<div style="width:28px;height:28px;border-radius:50%;background:#3b82f6;color:white;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800">' + unread + '</div>';
            h += '<div><div style="font-size:12px;color:#e2e8f0;font-weight:600">New message from client</div>';
            h += '<div style="font-size:11px;color:#64748b">"' + esc((lastMsg.text || '').substring(0, 60)) + '"</div></div>';
            h += '</div>';
        }

        // Engagement data
        if (liveData && liveData.engagement) {
            var engagements = Object.values(liveData.engagement);
            if (engagements.length > 0) {
                var totalTime = 0;
                var maxScroll = 0;
                engagements.forEach(function(e) {
                    totalTime += e.duration || 0;
                    if ((e.scrollDepth || 0) > maxScroll) maxScroll = e.scrollDepth;
                });
                h += '<div class="portal-metric">';
                h += '<div class="portal-metric-icon" style="background:rgba(168,85,247,0.1)">⏱</div>';
                h += '<div><div class="portal-metric-value">' + formatDuration(totalTime) + ' total time</div>';
                h += '<div class="portal-metric-label">Scrolled ' + maxScroll + '% of estimate</div></div>';
                h += '</div>';
            }
        }

        return h;
    }

    function portalDot(icon, active, color, label) {
        var bg = active ? color + '20' : 'transparent';
        var bc = active ? color : 'rgba(255,255,255,0.1)';
        var fc = active ? color : '#64748b';
        return '<div style="display:flex;flex-direction:column;align-items:center;gap:4px"><div class="portal-dot" style="background:' + bg + ';border-color:' + bc + ';color:' + fc + '">' + icon + '</div><div style="font-size:9px;color:' + fc + ';font-weight:600">' + label + '</div></div>';
    }

    function loadPortalLiveData(invoiceId) {
        db.ref('portal/' + hashedPIN + '/' + invoiceId).once('value').then(function(snap) {
            var data = snap.val();
            if (!data) return;
            var container = document.getElementById('portalLiveStatus_' + invoiceId);
            if (container) {
                var inv = findInvoiceGlobal(invoiceId);
                if (inv) container.innerHTML = buildPortalMetrics(inv, data);
            }
        });
    }

    window.cpQuickPortal = function(url) {
        navigator.clipboard.writeText(url).then(function() {
            showNotification('📋 Portal link copied!', 'success');
        });
    };

    // ================================================================
    // 4. PORTAL MESSAGES — Contractor side
    // ================================================================
    window.openPortalMessages = function(invoiceId) {
        var existing = document.getElementById('portalMsgModal');
        if (existing) existing.remove();

        var modal = document.createElement('div');
        modal.id = 'portalMsgModal';
        modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px';
        modal.innerHTML = '\
<div style="background:#0f172a;border:1px solid rgba(59,130,246,0.2);border-radius:20px;max-width:500px;width:100%;height:70vh;display:flex;flex-direction:column;overflow:hidden">\
    <div style="padding:16px 20px;border-bottom:1px solid rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:space-between">\
        <div style="font-size:15px;font-weight:700;color:white">💬 Client Messages — ' + invoiceId + '</div>\
        <button onclick="document.getElementById(\'portalMsgModal\').remove()" style="background:none;border:none;color:#64748b;font-size:20px;cursor:pointer">&times;</button>\
    </div>\
    <div id="portalMsgThread" style="flex:1;overflow-y:auto;padding:16px 20px;display:flex;flex-direction:column;gap:10px"></div>\
    <div style="padding:12px 16px;border-top:1px solid rgba(255,255,255,0.06);display:flex;gap:8px">\
        <textarea id="portalMsgInput" rows="1" placeholder="Reply to client..." style="flex:1;background:#1e293b;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:10px 14px;color:white;font-size:13px;font-family:inherit;resize:none;outline:none"></textarea>\
        <button onclick="sendPortalReply(\'' + invoiceId + '\')" style="background:#3b82f6;color:white;border:none;padding:0 18px;border-radius:10px;font-weight:700;font-size:12px;cursor:pointer;font-family:inherit">Send</button>\
    </div>\
</div>';

        document.body.appendChild(modal);
        modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });

        // Load messages
        var thread = document.getElementById('portalMsgThread');
        var msgRef = db.ref('portal/' + hashedPIN + '/' + invoiceId + '/messages');
        msgRef.orderByChild('at').on('child_added', function(snap) {
            var msg = snap.val();
            var div = document.createElement('div');
            var isClient = msg.from === 'client';
            div.style.cssText = 'max-width:85%;padding:10px 14px;border-radius:14px;font-size:13px;line-height:1.5;' +
                (isClient
                    ? 'align-self:flex-start;background:#1e293b;border:1px solid rgba(255,255,255,0.06);color:#e2e8f0;border-bottom-left-radius:4px'
                    : 'align-self:flex-end;background:#3b82f6;color:white;border-bottom-right-radius:4px');
            div.innerHTML = esc(msg.text) + '<div style="font-size:10px;margin-top:4px;opacity:0.6">' + (isClient ? esc(msg.fromName || 'Client') : 'You') + ' · ' + timeAgo(msg.at) + '</div>';
            thread.appendChild(div);
            thread.scrollTop = thread.scrollHeight;
        });

        // Clear unread count
        db.ref('portal/' + hashedPIN + '/' + invoiceId + '/unreadClient').set(0);

        // Enter key sends
        document.getElementById('portalMsgInput').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendPortalReply(invoiceId); }
        });
    };

    window.sendPortalReply = function(invoiceId) {
        var input = document.getElementById('portalMsgInput');
        var text = (input.value || '').trim();
        if (!text) return;

        db.ref('portal/' + hashedPIN + '/' + invoiceId + '/messages').push({
            from: 'contractor',
            fromName: 'Justin Watts',
            text: text,
            at: new Date().toISOString()
        });
        input.value = '';
    };

    // ================================================================
    // 5. LIVE NOTIFICATIONS — Watch for client actions
    // ================================================================
    function watchPortalActivity() {
        db.ref('portal/' + hashedPIN).on('child_changed', function(snap) {
            var data = snap.val();
            var invoiceId = snap.key;
            if (!data) return;

            // Check for new signature
            if (data.signedAt && !_notifiedSigned[invoiceId]) {
                _notifiedSigned[invoiceId] = true;
                showNotification('✅ ' + (data.invoice ? data.invoice.clientName : invoiceId) + ' ACCEPTED & SIGNED your estimate!', 'success');
                if (typeof BidGen !== 'undefined' && BidGen.emit) {
                    BidGen.emit('portal:signed', { invoiceId: invoiceId, signerName: data.signerName });
                }
                // Auto-move to awarded
                var inv = findInvoiceGlobal(invoiceId);
                if (inv && inv.status === 'temporary') {
                    inv.status = 'permanent';
                    inv.awardedDate = data.signedAt;
                    try { var _id = window._bidgenInvoiceData(); if(_id) { _id.permanent[invoiceId] = inv; delete _id.temporary[invoiceId]; } } catch(e) {}
                    db.ref('invoices/' + hashedPIN + '/temporary/' + invoiceId).remove();
                    saveInvoiceToFirebase(inv);
                    if (typeof invRenderList === 'function') invRenderList();
                    if (typeof updateInvoiceStats === 'function') updateInvoiceStats();
                }
            }

            // Check for new decline
            if (data.declinedAt && !_notifiedDeclined[invoiceId]) {
                _notifiedDeclined[invoiceId] = true;
                showNotification('❌ ' + (data.invoice ? data.invoice.clientName : invoiceId) + ' declined your estimate.', 'error');
                if (typeof BidGen !== 'undefined' && BidGen.emit) {
                    BidGen.emit('portal:declined', { invoiceId: invoiceId });
                }
            }

            // Check for new client messages
            if (data.unreadClient > 0 && !_lastUnread[invoiceId]) {
                _lastUnread[invoiceId] = data.unreadClient;
                var clientName = data.invoice ? data.invoice.clientName : invoiceId;
                var msgPreview = data.lastClientMsg ? data.lastClientMsg.text : '';
                showNotification('💬 New message from ' + clientName + ': "' + msgPreview.substring(0, 50) + '"', 'info');
                if (typeof BidGen !== 'undefined' && BidGen.emit) {
                    BidGen.emit('portal:message', { invoiceId: invoiceId, text: msgPreview });
                }
            } else if (data.unreadClient > (_lastUnread[invoiceId] || 0)) {
                _lastUnread[invoiceId] = data.unreadClient;
                var cn2 = data.invoice ? data.invoice.clientName : invoiceId;
                var mp2 = data.lastClientMsg ? data.lastClientMsg.text : '';
                showNotification('💬 ' + cn2 + ': "' + mp2.substring(0, 50) + '"', 'info');
            }

            // New view notification (only first view)
            if (data.viewCount === 1 && !_notifiedFirstView[invoiceId]) {
                _notifiedFirstView[invoiceId] = true;
                var cn3 = data.invoice ? data.invoice.clientName : invoiceId;
                showNotification('👁 ' + cn3 + ' just opened your estimate!', 'info');
                if (typeof BidGen !== 'undefined' && BidGen.emit) {
                    BidGen.emit('portal:viewed', { invoiceId: invoiceId });
                }
            }
        });
    }

    var _notifiedSigned = {};
    var _notifiedDeclined = {};
    var _notifiedFirstView = {};
    var _lastUnread = {};

    // Pre-populate notification caches so we don't re-fire old events
    db.ref('portal/' + hashedPIN).once('value').then(function(snap) {
        var all = snap.val() || {};
        Object.keys(all).forEach(function(id) {
            var d = all[id];
            if (d.signedAt) _notifiedSigned[id] = true;
            if (d.declinedAt) _notifiedDeclined[id] = true;
            if (d.viewCount > 0) _notifiedFirstView[id] = true;
            if (d.unreadClient) _lastUnread[id] = d.unreadClient;
        });
        // Start watching after cache is loaded
        watchPortalActivity();
    });

    // ================================================================
    // 6. PORTAL OVERVIEW DASHBOARD — all portals at a glance
    // ================================================================
    window.openPortalDashboard = function() {
        var existing = document.getElementById('portalDashModal');
        if (existing) existing.remove();

        var modal = document.createElement('div');
        modal.id = 'portalDashModal';
        modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:99999;display:flex;flex-direction:column;overflow:hidden';
        modal.innerHTML = '\
<div style="background:#0b1121;border-bottom:1px solid rgba(59,130,246,0.2);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0">\
    <div style="display:flex;align-items:center;gap:12px">\
        <div style="width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:18px">🌐</div>\
        <div><div style="font-size:18px;font-weight:800;color:white;letter-spacing:-0.3px">Portal Dashboard</div>\
        <div style="font-size:11px;color:#64748b">All published estimates — real-time status</div></div>\
    </div>\
    <button onclick="document.getElementById(\'portalDashModal\').remove()" style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);color:#94a3b8;font-size:18px;cursor:pointer;padding:6px 12px;border-radius:8px;font-weight:700">&times;</button>\
</div>\
<div style="padding:16px 24px;display:flex;gap:12px;align-items:center;flex-shrink:0;border-bottom:1px solid rgba(255,255,255,0.04)">\
    <div id="pdStatSigned" style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.2);border-radius:10px;padding:10px 16px;text-align:center;flex:1">\
        <div style="font-size:22px;font-weight:800;color:#22c55e">—</div>\
        <div style="font-size:10px;color:#22c55e;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">Signed</div>\
    </div>\
    <div id="pdStatViewed" style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.2);border-radius:10px;padding:10px 16px;text-align:center;flex:1">\
        <div style="font-size:22px;font-weight:800;color:#f59e0b">—</div>\
        <div style="font-size:10px;color:#f59e0b;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">Viewed</div>\
    </div>\
    <div id="pdStatPending" style="background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);border-radius:10px;padding:10px 16px;text-align:center;flex:1">\
        <div style="font-size:22px;font-weight:800;color:#3b82f6">—</div>\
        <div style="font-size:10px;color:#3b82f6;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">Pending</div>\
    </div>\
    <div id="pdStatDeclined" style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:10px;padding:10px 16px;text-align:center;flex:1">\
        <div style="font-size:22px;font-weight:800;color:#ef4444">—</div>\
        <div style="font-size:10px;color:#ef4444;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">Declined</div>\
    </div>\
</div>\
<div id="pdList" style="flex:1;overflow-y:auto;padding:16px 24px">\
    <div style="text-align:center;padding:40px 0;color:#64748b;font-size:13px">Loading portal data...</div>\
</div>';

        document.body.appendChild(modal);
        modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });

        // Load all portal data
        db.ref('portal/' + hashedPIN).once('value').then(function(snap) {
            var allData = snap.val() || {};
            var items = [];
            var stats = { signed: 0, viewed: 0, pending: 0, declined: 0 };

            Object.keys(allData).forEach(function(id) {
                var d = allData[id];
                if (!d || !d.invoice) return;
                var status = 'pending';
                if (d.signedAt) { status = 'signed'; stats.signed++; }
                else if (d.declinedAt) { status = 'declined'; stats.declined++; }
                else if (d.viewCount > 0) { status = 'viewed'; stats.viewed++; }
                else { stats.pending++; }
                items.push({
                    id: id,
                    data: d,
                    invoice: d.invoice,
                    status: status,
                    lastActivity: d.signedAt || d.declinedAt || d.lastViewedAt || d.publishedAt || ''
                });
            });

            // Sort by last activity (newest first)
            items.sort(function(a, b) { return (b.lastActivity || '').localeCompare(a.lastActivity || ''); });

            // Update stat cards
            _pdUpdateStat('pdStatSigned', stats.signed);
            _pdUpdateStat('pdStatViewed', stats.viewed);
            _pdUpdateStat('pdStatPending', stats.pending);
            _pdUpdateStat('pdStatDeclined', stats.declined);

            // Render list
            var list = document.getElementById('pdList');
            if (!list) return;
            if (items.length === 0) {
                list.innerHTML = '<div style="text-align:center;padding:60px 0;color:#64748b"><div style="font-size:40px;margin-bottom:12px">🌐</div><div style="font-size:15px;font-weight:600;color:#94a3b8;margin-bottom:6px">No portals published yet</div><div style="font-size:13px">Publish an estimate to see it here</div></div>';
                return;
            }

            var h = '';
            items.forEach(function(item) {
                var d = item.data;
                var inv = item.invoice;
                var vc = d.viewCount || 0;
                var isFI = inv.documentType === 'final_invoice' || inv.type === 'final_invoice';
                var url = buildPortalUrl(item.id, isFI);

                // Status badge
                var badge = '';
                if (item.status === 'signed') badge = '<span style="background:rgba(34,197,94,0.15);color:#22c55e;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700">✓ SIGNED</span>';
                else if (item.status === 'declined') badge = '<span style="background:rgba(239,68,68,0.15);color:#ef4444;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700">✕ DECLINED</span>';
                else if (item.status === 'viewed') badge = '<span style="background:rgba(245,158,11,0.15);color:#f59e0b;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700">👁 VIEWED</span>';
                else badge = '<span style="background:rgba(59,130,246,0.15);color:#3b82f6;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700">● SENT</span>';

                h += '<div style="background:#0f172a;border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:16px;margin-bottom:10px;transition:border-color 0.15s" onmouseover="this.style.borderColor=\'rgba(59,130,246,0.3)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.06)\'">';

                // Top row: client name, amount, status badge
                h += '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-wrap:wrap;gap:6px">';
                h += '<div style="display:flex;align-items:center;gap:10px;min-width:0">';
                if (isFI) h += '<span style="background:rgba(34,197,94,0.15);color:#22c55e;padding:2px 8px;border-radius:6px;font-size:9px;font-weight:700;letter-spacing:0.3px">FINAL INVOICE</span>';
                h += '<div style="font-size:15px;font-weight:700;color:#e2e8f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + esc(inv.clientName || 'Client') + '</div>';
                h += '<div style="font-size:13px;font-weight:800;color:#3b82f6">$' + (parseFloat(isFI ? inv.amountDue : inv.amount) || 0).toFixed(2) + '</div>';
                h += '</div>';
                h += badge;
                h += '</div>';

                // Middle row: invoice #, date, views, time spent
                h += '<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px;font-size:11px;color:#64748b">';
                h += '<span>#' + esc(item.id) + '</span>';
                if (d.publishedAt) h += '<span>Published ' + timeAgo(d.publishedAt) + '</span>';
                h += '<span>' + vc + ' view' + (vc !== 1 ? 's' : '') + '</span>';
                if (d.lastViewedAt) h += '<span>Last: ' + timeAgo(d.lastViewedAt) + '</span>';
                if (d.unreadClient > 0) h += '<span style="color:#3b82f6;font-weight:700">💬 ' + d.unreadClient + ' unread</span>';
                h += '</div>';

                // Signed info
                if (d.signedAt) {
                    h += '<div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.12);border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:11px;color:#86efac">';
                    h += 'Signed by <strong>' + esc(d.signerName || 'Client') + '</strong> on ' + new Date(d.signedAt).toLocaleDateString('en-US',{year:'numeric',month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});
                    h += '</div>';
                }
                if (d.declinedAt) {
                    h += '<div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.12);border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:11px;color:#fca5a5">';
                    h += 'Declined ' + timeAgo(d.declinedAt);
                    if (d.declineReason) h += ' — "' + esc(d.declineReason) + '"';
                    h += '</div>';
                }

                // Action buttons
                h += '<div style="display:flex;gap:6px;flex-wrap:wrap">';
                h += '<button onclick="cpQuickPortal(\'' + url.replace(/'/g, "\\'") + '\')" style="background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:6px 12px;border-radius:8px;font-size:10px;font-weight:600;cursor:pointer;font-family:inherit">📋 Copy Link</button>';
                h += '<button onclick="openPortalMessages(\'' + esc(item.id) + '\')" style="background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:6px 12px;border-radius:8px;font-size:10px;font-weight:600;cursor:pointer;font-family:inherit">💬 Messages</button>';
                h += '<a href="' + url + '" target="_blank" style="background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:6px 12px;border-radius:8px;font-size:10px;font-weight:600;cursor:pointer;text-decoration:none;font-family:inherit">🔗 Open Portal</a>';
                h += '<button onclick="publishToPortal(\'' + esc(item.id) + '\')" style="background:#1e293b;color:#94a3b8;border:1px solid rgba(255,255,255,0.06);padding:6px 12px;border-radius:8px;font-size:10px;font-weight:600;cursor:pointer;font-family:inherit">🔄 Republish</button>';
                h += '</div>';

                h += '</div>';
            });

            list.innerHTML = h;
        }).catch(function(err) {
            var list = document.getElementById('pdList');
            if (list) list.innerHTML = '<div style="text-align:center;padding:40px 0;color:#ef4444">Error loading portal data: ' + esc(err.message) + '</div>';
        });
    };

    function _pdUpdateStat(id, val) {
        var el = document.getElementById(id);
        if (!el) return;
        var numEl = el.querySelector('div');
        if (numEl) numEl.textContent = val;
    }

    // ================================================================
    // 7. INJECT "SHARE PORTAL" BUTTONS INTO EXISTING UI
    // ================================================================
    function injectPortalButtons() {
        // Patch invViewDetails to include portal section
        var _origViewDetails = window.invViewDetails;
        if (typeof _origViewDetails === 'function') {
            window.invViewDetails = function(invoiceId) {
                _origViewDetails(invoiceId);
                // After original renders, inject portal section
                setTimeout(function() {
                    var panel = document.getElementById('quoteDetailPanel');
                    if (!panel) return;
                    var inner = panel.querySelector('div[style*="background:#0f1a33"]');
                    if (!inner) return;

                    var invoice = findInvoiceGlobal(invoiceId);
                    if (!invoice) return;

                    // Find the contract status section and add portal section after it
                    var portalDiv = document.createElement('div');
                    portalDiv.id = 'portalSection_' + invoiceId;
                    portalDiv.innerHTML = getPortalStatusHTML(invoice);

                    // Insert before the action buttons row
                    var actionBtns = inner.querySelector('div[style*="display:flex"][style*="gap:8px"][style*="flex-wrap:wrap"]');
                    if (actionBtns) {
                        inner.insertBefore(portalDiv, actionBtns);
                    } else {
                        inner.appendChild(portalDiv);
                    }
                }, 100);
            };
        }

        // Add "Share Portal" to invoice list item actions
        var _origRenderItem = window.renderInvoiceItem;
        if (typeof _origRenderItem === 'function') {
            window.renderInvoiceItem = function(invoice) {
                var html = _origRenderItem(invoice);
                // Inject portal button into the actions row
                var portalBtn = '<button class="invoice-btn view" onclick="event.stopPropagation();publishToPortal(\'' + invoice.id + '\')" style="background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:white" title="Create client portal link">🌐 Portal</button>';
                html = html.replace('</div>\n            </div>\n        </div>', portalBtn + '</div>\n            </div>\n        </div>');
                return html;
            };
        }
    }
    injectPortalButtons();

    // ================================================================
    // 7. INTEGRATE WITH EVENT BUS
    // ================================================================
    if (typeof BidGen !== 'undefined') {
        // Auto-publish to portal when a doc is generated (if setting enabled)
        BidGen.on('doc:generated', function(data) {
            var autoPublish = localStorage.getItem('bgp_autoPortal');
            if (autoPublish === 'true' && data.invoiceId) {
                setTimeout(function() { publishToPortal(data.invoiceId); }, 1000);
            }
        });

        // Register portal in command palette if available
        BidGen.on('pro:ready', function() {
            if (window._bgpCommands) {
                window._bgpCommands.push(
                    { label: 'Portal Dashboard', desc: 'View all published estimates — status, views, signatures, messages', action: function() {
                        openPortalDashboard();
                    }},
                    { label: 'Publish to Client Portal', desc: 'Create a shareable portal link for the current invoice', action: function() {
                        var id = window._lastInvoiceId;
                        if (id) publishToPortal(id);
                        else showNotification('Generate an invoice first.', 'error');
                    }},
                    { label: 'Open Portal Messages', desc: 'View client Q&A for the current invoice', action: function() {
                        var id = window._lastInvoiceId;
                        if (id) openPortalMessages(id);
                        else showNotification('No active invoice.', 'error');
                    }},
                    { label: 'Toggle Auto-Publish to Portal', desc: 'Automatically create portal links when generating docs', action: function() {
                        var current = localStorage.getItem('bgp_autoPortal') === 'true';
                        localStorage.setItem('bgp_autoPortal', !current ? 'true' : 'false');
                        showNotification('Auto-publish to portal: ' + (!current ? 'ON' : 'OFF'), 'success');
                    }}
                );
            }
        });
    }

    // ================================================================
    // 8. REGISTER WITH WIDGET DOCK
    // ================================================================
    if (typeof window.widgetDockRegister === 'function') {
        // Create a small portal activity indicator
        var portalIndicator = document.createElement('div');
        portalIndicator.id = 'portalActivityDot';
        portalIndicator.style.cssText = 'display:none;position:absolute;top:-2px;right:-2px;width:8px;height:8px;border-radius:50%;background:#3b82f6;animation:portalPulse 2s infinite';
        var pulseStyle = document.createElement('style');
        pulseStyle.textContent = '@keyframes portalPulse{0%,100%{opacity:1}50%{opacity:0.3}}';
        document.head.appendChild(pulseStyle);
    }

    // ================================================================
    // HELPERS
    // ================================================================
    function findInvoiceGlobal(invoiceId) {
        var iData = window._bidgenInvoiceData ? window._bidgenInvoiceData() : null;
        if (!iData) return null;
        var statuses = ['temporary', 'permanent', 'lost'];
        for (var i = 0; i < statuses.length; i++) {
            if (iData[statuses[i]] && iData[statuses[i]][invoiceId]) {
                return iData[statuses[i]][invoiceId];
            }
        }
        return null;
    }

    function gv(id) {
        var el = document.getElementById(id);
        return el ? el.value : '';
    }

    function esc(s) {
        if (!s) return '';
        var d = document.createElement('div');
        d.textContent = s;
        return d.innerHTML;
    }

    function timeAgo(iso) {
        if (!iso) return '';
        var ms = Date.now() - new Date(iso).getTime();
        var m = Math.floor(ms / 60000);
        if (m < 1) return 'just now';
        if (m < 60) return m + 'm ago';
        var h = Math.floor(m / 60);
        if (h < 24) return h + 'h ago';
        return Math.floor(h / 24) + 'd ago';
    }

    function formatDuration(seconds) {
        if (seconds < 60) return seconds + 's';
        var m = Math.floor(seconds / 60);
        var s = seconds % 60;
        if (m < 60) return m + 'm ' + s + 's';
        var h = Math.floor(m / 60);
        return h + 'h ' + (m % 60) + 'm';
    }

    console.log('[Client Portal] ✅ Portal system active — publish, track, and message clients in real-time');
}

})();
