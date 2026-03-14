/**
 * Contract Delivery System — BidGen Integration
 * Generates secure one-time e-sign links, sends via email,
 * tracks status (sent → viewed → signed), and syncs to Firebase.
 */
(function() {
    'use strict';

    var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';

    // ================================================================
    // SEND CONTRACT — Creates KV link + opens email compose
    // ================================================================
    // ================================================================
    // INLINE INPUT MODAL — replaces window.prompt() to avoid Chrome suppression
    // ================================================================
    function showInputModal(title, fields, onSubmit) {
        var existing = document.getElementById('cdInputModal');
        if (existing) existing.remove();

        var modal = document.createElement('div');
        modal.id = 'cdInputModal';
        modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px;';

        var fieldsHTML = '';
        for (var i = 0; i < fields.length; i++) {
            var f = fields[i];
            if (f.type === 'select') {
                var opts = '';
                for (var j = 0; j < f.options.length; j++) {
                    var o = f.options[j];
                    var sel = o.value === f.value ? ' selected' : '';
                    opts += '<option value="' + o.value + '"' + sel + '>' + o.label + '</option>';
                }
                fieldsHTML += '<div style="margin-bottom:12px"><label style="font-size:11px;color:#7f8c8d;text-transform:uppercase;font-weight:700;display:block;margin-bottom:4px">' + f.label + '</label><select id="cdInput_' + i + '" style="width:100%;background:#0f1a33;border:1px solid #2a3a5c;color:#ecf0f1;padding:10px 12px;border-radius:6px;font-size:14px;font-family:inherit">' + opts + '</select></div>';
            } else {
                fieldsHTML += '<div style="margin-bottom:12px"><label style="font-size:11px;color:#7f8c8d;text-transform:uppercase;font-weight:700;display:block;margin-bottom:4px">' + f.label + '</label><input type="' + (f.type || 'text') + '" id="cdInput_' + i + '" value="' + (f.value || '') + '" placeholder="' + (f.placeholder || '') + '" style="width:100%;background:#0f1a33;border:1px solid #2a3a5c;color:#ecf0f1;padding:10px 12px;border-radius:6px;font-size:14px;font-family:inherit;box-sizing:border-box" /></div>';
            }
        }

        modal.innerHTML = '<div style="background:#16213e;border:1px solid #2a3a5c;border-radius:16px;max-width:420px;width:100%;padding:24px">'
            + '<h3 style="color:#ecf0f1;font-size:16px;margin:0 0 16px">' + title + '</h3>'
            + fieldsHTML
            + '<div style="display:flex;gap:8px;margin-top:16px">'
            + '<button id="cdInputSubmit" style="flex:1;background:#3498db;color:white;border:none;padding:12px;border-radius:8px;font-weight:700;font-size:13px;cursor:pointer">Continue</button>'
            + '<button id="cdInputCancel" style="flex:1;background:#2a3a5c;color:#bdc3c7;border:none;padding:12px;border-radius:8px;font-weight:700;font-size:13px;cursor:pointer">Cancel</button>'
            + '</div></div>';

        document.body.appendChild(modal);

        // Focus first input
        var firstInput = modal.querySelector('input, select');
        if (firstInput) setTimeout(function() { firstInput.focus(); }, 50);

        document.getElementById('cdInputCancel').onclick = function() { modal.remove(); };
        modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });

        document.getElementById('cdInputSubmit').onclick = function() {
            var values = [];
            for (var k = 0; k < fields.length; k++) {
                values.push(document.getElementById('cdInput_' + k).value.trim());
            }
            modal.remove();
            onSubmit(values);
        };

        // Enter key submits
        modal.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') document.getElementById('cdInputSubmit').click();
        });
    }

    window.sendContractToClient = async function(invoiceId) {
        // Find the invoice across all statuses
        var invoice = null;
        for (var status in invoiceData) {
            if (invoiceData[status][invoiceId]) {
                invoice = invoiceData[status][invoiceId];
                break;
            }
        }
        if (!invoice) {
            showNotification('Invoice not found: ' + invoiceId, 'error');
            return;
        }

        // Show inline modal for client email instead of prompt()
        showInputModal('📧 Send Contract to Client', [
            { label: 'Client Email Address', type: 'email', value: invoice.clientEmail || '', placeholder: 'client@example.com' }
        ], async function(values) {
            var clientEmail = values[0];
            if (!clientEmail) return;

            // Validate email format
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clientEmail)) {
                showNotification('Invalid email address', 'error');
                return;
            }

            // Store email on invoice for future use
            invoice.clientEmail = clientEmail;

            showNotification('⏳ Generating secure contract link...', 'info');

            try {
                var res = await fetch(PROXY + '/contract/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        invoiceId: invoiceId,
                        contractData: invoice,
                        clientEmail: clientEmail,
                        clientName: invoice.clientName,
                        ownerPin: hashPIN(userPIN)
                    })
                });

                var data = await res.json();

                if (!res.ok) {
                    throw new Error(data.error || 'Failed to create contract link');
                }

                // Store contract link info on the invoice
                invoice.contractLink = {
                    token: data.token,
                    signature: data.signature,
                    url: data.url,
                    sentAt: new Date().toISOString(),
                    status: 'sent'
                };

                // Save updated invoice to Firebase
                saveInvoiceToFirebase(invoice);

                // Show success and open email compose
                showNotification('✅ Secure contract link created!', 'success');
                openEmailCompose(invoice, data.url, clientEmail);

                // Refresh the detail view if it's open
                invViewDetails(invoiceId);

            } catch (err) {
                showNotification('❌ Error: ' + err.message, 'error');
                console.error('Contract creation failed:', err);
            }
        });
    };

    // ================================================================
    // EMAIL COMPOSE — Opens mailto or shows copy-paste modal
    // ================================================================
    function openEmailCompose(invoice, contractUrl, clientEmail) {
        var companyName = invoice.companyInfo ? invoice.companyInfo.companyName || 'Watts Safety Installs' : 'Watts Safety Installs';
        var subject = encodeURIComponent('Contract & Estimate from ' + companyName + ' — ' + invoice.id);

        var body = [
            'Hi ' + invoice.clientName + ',',
            '',
            'Thank you for choosing ' + companyName + '.',
            '',
            'Please review and sign your contract/estimate using the secure link below:',
            '',
            contractUrl,
            '',
            'This link is secure, one-time-use for signing, and will lock once signed. Both parties will retain read-only access for records.',
            '',
            'Contract Details:',
            '  • Invoice: ' + invoice.id,
            '  • Estimate Date: ' + (invoice.estimateDate || 'N/A'),
            '  • Total: $' + (invoice.amount || 0).toFixed(2),
            '',
            'If you have any questions, please don\'t hesitate to reach out.',
            '',
            'Best regards,',
            'Justin Watts',
            companyName,
            'Nebraska Licensed Contractor #54690-25',
            '(405) 410-6402',
            'Justin.Watts@WattsATPContractor.com'
        ].join('\n');

        var encodedBody = encodeURIComponent(body);

        // Check if mailto URL isn't too long (some email clients have limits)
        var mailtoUrl = 'mailto:' + clientEmail + '?subject=' + subject + '&body=' + encodedBody;

        if (mailtoUrl.length < 2000) {
            // Open default email client
            window.open(mailtoUrl, '_blank');
        }

        // Always show the copy-paste modal as backup
        showContractModal(invoice, contractUrl, clientEmail, body);
    }

    // ================================================================
    // CONTRACT SEND MODAL — Copy link, email body, status
    // ================================================================
    function showContractModal(invoice, contractUrl, clientEmail, emailBody) {
        // Remove existing modal if any
        var existing = document.getElementById('contractSendModal');
        if (existing) existing.remove();

        var modal = document.createElement('div');
        modal.id = 'contractSendModal';
        modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px;';
        modal.innerHTML = '\
            <div style="background:#0f1a33;border:1px solid #2a3a5c;border-radius:16px;max-width:600px;width:100%;max-height:85vh;overflow-y:auto;padding:30px;">\
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">\
                    <h3 style="color:#ecf0f1;font-size:18px;margin:0">📧 Send Contract to Client</h3>\
                    <button onclick="document.getElementById(\'contractSendModal\').remove()" style="background:none;border:none;color:#7f8c8d;font-size:20px;cursor:pointer">&times;</button>\
                </div>\
                \
                <div style="background:#16213e;border:1px solid #2a3a5c;border-radius:8px;padding:16px;margin-bottom:16px">\
                    <div style="font-size:11px;color:#7f8c8d;text-transform:uppercase;margin-bottom:6px;font-weight:700">Secure Contract Link</div>\
                    <div style="display:flex;gap:8px">\
                        <input type="text" value="' + escAttr(contractUrl) + '" readonly style="flex:1;background:#0f1a33;border:1px solid #2a3a5c;color:#3498db;padding:8px 12px;border-radius:6px;font-size:12px;font-family:monospace" id="contractUrlField"/>\
                        <button onclick="copyContractUrl()" style="background:#3498db;color:white;border:none;padding:8px 16px;border-radius:6px;font-weight:600;font-size:12px;cursor:pointer;white-space:nowrap" id="copyUrlBtn">📋 Copy</button>\
                    </div>\
                </div>\
                \
                <div style="background:#16213e;border:1px solid #2a3a5c;border-radius:8px;padding:16px;margin-bottom:16px">\
                    <div style="font-size:11px;color:#7f8c8d;text-transform:uppercase;margin-bottom:6px;font-weight:700">Client Email</div>\
                    <div style="color:#ecf0f1;font-size:14px">' + esc(clientEmail) + '</div>\
                </div>\
                \
                <div style="background:#16213e;border:1px solid #2a3a5c;border-radius:8px;padding:16px;margin-bottom:16px">\
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">\
                        <div style="font-size:11px;color:#7f8c8d;text-transform:uppercase;font-weight:700">Email Body (Copy & Paste)</div>\
                        <button onclick="copyEmailBody()" style="background:#27ae60;color:white;border:none;padding:4px 12px;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer" id="copyBodyBtn">📋 Copy Email</button>\
                    </div>\
                    <textarea readonly style="width:100%;height:200px;background:#0f1a33;border:1px solid #2a3a5c;color:#bdc3c7;padding:12px;border-radius:6px;font-size:12px;resize:none;line-height:1.6" id="emailBodyField">' + esc(emailBody) + '</textarea>\
                </div>\
                \
                <div style="display:flex;gap:8px;flex-wrap:wrap">\
                    <a href="mailto:' + encodeURIComponent(clientEmail) + '?subject=' + encodeURIComponent('Contract & Estimate — ' + invoice.id) + '&body=' + encodeURIComponent(emailBody) + '" style="flex:1;text-align:center;background:#3498db;color:white;padding:12px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px">📧 Open Email Client</a>\
                    <button onclick="document.getElementById(\'contractSendModal\').remove()" style="flex:1;background:#2a3a5c;color:#bdc3c7;border:none;padding:12px;border-radius:8px;font-weight:700;font-size:13px;cursor:pointer">✅ Done</button>\
                </div>\
                \
                <div style="margin-top:16px;padding:12px;background:rgba(39,174,96,0.1);border:1px solid rgba(39,174,96,0.3);border-radius:8px">\
                    <div style="font-size:12px;color:#27ae60;font-weight:600">✅ Contract link created successfully</div>\
                    <div style="font-size:11px;color:#7f8c8d;margin-top:4px">Status will update automatically when the client views or signs the contract.</div>\
                </div>\
            </div>';

        document.body.appendChild(modal);

        // Close on backdrop click
        modal.addEventListener('click', function(e) {
            if (e.target === modal) modal.remove();
        });
    }

    window.copyContractUrl = function() {
        var field = document.getElementById('contractUrlField');
        field.select();
        navigator.clipboard.writeText(field.value).then(function() {
            var btn = document.getElementById('copyUrlBtn');
            btn.textContent = '✅ Copied!';
            setTimeout(function() { btn.textContent = '📋 Copy'; }, 2000);
        });
    };

    window.copyEmailBody = function() {
        var field = document.getElementById('emailBodyField');
        navigator.clipboard.writeText(field.value).then(function() {
            var btn = document.getElementById('copyBodyBtn');
            btn.textContent = '✅ Copied!';
            setTimeout(function() { btn.textContent = '📋 Copy Email'; }, 2000);
        });
    };

    // ================================================================
    // TEXT CONTRACT LINK — Redirects through Client Portal system
    // Publishes full invoice data to portal and opens share modal
    // with SMS/Email/WhatsApp options containing full breakdown.
    // ================================================================
    window.textContractLink = async function(invoiceId) {
        if (typeof publishToPortal === 'function') {
            publishToPortal(invoiceId);
        } else {
            showNotification('Portal system is still loading. Try again in a moment.', 'error');
        }
    };

    // ================================================================
    // CHECK CONTRACT STATUS — Poll KV for sent/viewed/signed
    // ================================================================
    window.checkContractStatus = async function(invoiceId) {
        if (!userPIN) return;

        try {
            var pin = hashPIN(userPIN);
            var res = await fetch(PROXY + '/contract/status?invoiceId=' + encodeURIComponent(invoiceId) + '&pin=' + encodeURIComponent(pin));
            var data = await res.json();

            if (!res.ok) {
                console.log('Contract status check:', data.error);
                return null;
            }

            // Update local invoice with latest status
            var invoice = findInvoice(invoiceId);
            if (invoice && invoice.contractLink) {
                invoice.contractLink.status = data.status;
                if (data.viewedAt) invoice.contractLink.viewedAt = data.viewedAt;
                if (data.signedAt) {
                    invoice.contractLink.signedAt = data.signedAt;
                    invoice.contractLink.signerName = data.signerName;
                    invoice.contractLink.signatureData = data.signatureData;
                    invoice.contractLink.signatureType = data.signatureType;
                }
            }

            return data;
        } catch (err) {
            console.error('Contract status check failed:', err);
            return null;
        }
    };

    // ================================================================
    // CONTRACT STATUS BADGE — Renders inline status for invoice detail
    // ================================================================
    window.getContractStatusHTML = function(invoice) {
        if (!invoice.contractLink) {
            return '<button class="invoice-btn view" onclick="sendContractToClient(\'' + invoice.id + '\')" style="background:#8e44ad;color:white">📧 Send to Client</button>';
        }

        var link = invoice.contractLink;
        var statusColor = { sent: '#3498db', viewed: '#f39c12', signed: '#27ae60' };
        var statusIcon = { sent: '📤', viewed: '👁️', signed: '✅' };
        var statusLabel = { sent: 'Sent', viewed: 'Viewed', signed: 'Signed' };
        var s = link.status || 'sent';

        var html = '<div style="background:#16213e;border:1px solid #2a3a5c;border-radius:8px;padding:12px;margin-bottom:16px">';
        html += '<div style="font-size:10px;color:#7f8c8d;text-transform:uppercase;margin-bottom:8px;font-weight:700">Contract Delivery Status</div>';
        html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">';
        html += '<span style="font-size:18px">' + (statusIcon[s] || '📤') + '</span>';
        html += '<span style="color:' + (statusColor[s] || '#3498db') + ';font-weight:700;font-size:14px">' + (statusLabel[s] || 'Sent') + '</span>';

        // Timeline dots
        html += '<div style="display:flex;gap:4px;margin-left:auto;align-items:center">';
        html += '<div style="width:10px;height:10px;border-radius:50%;background:#3498db" title="Sent"></div>';
        html += '<div style="width:20px;height:2px;background:' + (s === 'viewed' || s === 'signed' ? '#f39c12' : '#2a3a5c') + '"></div>';
        html += '<div style="width:10px;height:10px;border-radius:50%;background:' + (s === 'viewed' || s === 'signed' ? '#f39c12' : '#2a3a5c') + '" title="Viewed"></div>';
        html += '<div style="width:20px;height:2px;background:' + (s === 'signed' ? '#27ae60' : '#2a3a5c') + '"></div>';
        html += '<div style="width:10px;height:10px;border-radius:50%;background:' + (s === 'signed' ? '#27ae60' : '#2a3a5c') + '" title="Signed"></div>';
        html += '</div></div>';

        // Timestamps
        if (link.sentAt) html += '<div style="font-size:11px;color:#7f8c8d">Sent: ' + new Date(link.sentAt).toLocaleString() + '</div>';
        if (link.viewedAt) html += '<div style="font-size:11px;color:#f39c12">Viewed: ' + new Date(link.viewedAt).toLocaleString() + '</div>';
        if (link.signedAt) html += '<div style="font-size:11px;color:#27ae60">Signed: ' + new Date(link.signedAt).toLocaleString() + (link.signerName ? ' by ' + esc(link.signerName) : '') + '</div>';

        // Action buttons
        html += '<div style="display:flex;gap:6px;margin-top:10px;flex-wrap:wrap">';
        if (s !== 'signed') {
            html += '<button onclick="checkContractStatus(\'' + invoice.id + '\').then(function(){invViewDetails(\'' + invoice.id + '\')})" style="background:#2a3a5c;color:#bdc3c7;border:none;padding:6px 12px;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer">🔄 Refresh Status</button>';
            html += '<button onclick="sendContractToClient(\'' + invoice.id + '\')" style="background:#8e44ad;color:white;border:none;padding:6px 12px;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer">📧 Resend</button>';
        }
        if (link.url) {
            html += '<button onclick="navigator.clipboard.writeText(\'' + escAttr(link.url) + '\');showNotification(\'Link copied!\',\'success\')" style="background:#3498db;color:white;border:none;padding:6px 12px;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer">📋 Copy Link</button>';
        }
        if (s === 'signed' && link.signatureData) {
            html += '<button onclick="viewSignedContract(\'' + invoice.id + '\')" style="background:#27ae60;color:white;border:none;padding:6px 12px;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer">📄 View Signed</button>';
        }
        html += '</div></div>';

        return html;
    };

    // ================================================================
    // VIEW SIGNED CONTRACT — Shows signature in a modal
    // ================================================================
    window.viewSignedContract = function(invoiceId) {
        var invoice = findInvoice(invoiceId);
        if (!invoice || !invoice.contractLink) return;

        var link = invoice.contractLink;
        var existing = document.getElementById('signedViewModal');
        if (existing) existing.remove();

        var sigContent = '';
        if (link.signatureType === 'draw' && link.signatureData) {
            sigContent = '<img src="' + link.signatureData + '" style="max-width:100%;max-height:150px;border:1px solid #2a3a5c;border-radius:6px;padding:8px;background:white"/>';
        } else if (link.signatureData) {
            sigContent = '<div style="font-family:\'Brush Script MT\',\'Segoe Script\',cursive;font-size:2.5rem;color:#ecf0f1;text-align:center;padding:20px">' + esc(link.signatureData) + '</div>';
        }

        var modal = document.createElement('div');
        modal.id = 'signedViewModal';
        modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px';
        modal.innerHTML = '\
            <div style="background:#0f1a33;border:1px solid #2a3a5c;border-radius:16px;max-width:500px;width:100%;padding:30px">\
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">\
                    <h3 style="color:#27ae60;font-size:16px;margin:0">✅ Signed Contract Record</h3>\
                    <button onclick="document.getElementById(\'signedViewModal\').remove()" style="background:none;border:none;color:#7f8c8d;font-size:20px;cursor:pointer">&times;</button>\
                </div>\
                <div style="background:#16213e;border:1px solid #2a3a5c;border-radius:8px;padding:16px;margin-bottom:12px">\
                    <div style="font-size:10px;color:#7f8c8d;text-transform:uppercase;margin-bottom:6px;font-weight:700">Client Signature</div>\
                    ' + sigContent + '\
                </div>\
                <div style="font-size:12px;color:#7f8c8d;line-height:1.8">\
                    <div><strong style="color:#ecf0f1">Invoice:</strong> ' + esc(invoice.id) + '</div>\
                    <div><strong style="color:#ecf0f1">Client:</strong> ' + esc(invoice.clientName) + '</div>\
                    <div><strong style="color:#ecf0f1">Signed by:</strong> ' + esc(link.signerName || 'N/A') + '</div>\
                    <div><strong style="color:#ecf0f1">Signed at:</strong> ' + (link.signedAt ? new Date(link.signedAt).toLocaleString() : 'N/A') + '</div>\
                    <div><strong style="color:#ecf0f1">Status:</strong> <span style="color:#27ae60;font-weight:700">LOCKED — Read Only</span></div>\
                </div>\
                <div style="margin-top:16px;text-align:center">\
                    <button onclick="document.getElementById(\'signedViewModal\').remove()" style="background:#2a3a5c;color:#bdc3c7;border:none;padding:10px 24px;border-radius:6px;font-weight:600;cursor:pointer">Close</button>\
                </div>\
            </div>';

        document.body.appendChild(modal);
        modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });
    };

    // ================================================================
    // AUTO-POLL — Check contract statuses periodically
    // ================================================================
    function pollContractStatuses() {
        for (var status in invoiceData) {
            Object.values(invoiceData[status]).forEach(function(inv) {
                if (inv.contractLink && inv.contractLink.status !== 'signed') {
                    checkContractStatus(inv.id);
                }
            });
        }
    }

    // Poll every 2 minutes for status updates
    setInterval(pollContractStatuses, 120000);

    // ================================================================
    // HELPERS
    // ================================================================
    function findInvoice(invoiceId) {
        for (var status in invoiceData) {
            if (invoiceData[status][invoiceId]) return invoiceData[status][invoiceId];
        }
        return null;
    }

    function esc(s) {
        if (!s) return '';
        var d = document.createElement('div');
        d.textContent = s;
        return d.innerHTML;
    }

    function escAttr(s) {
        return (s || '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
    }

})();
