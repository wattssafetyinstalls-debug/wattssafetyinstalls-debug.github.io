/**
 * Watts AI Proxy + Contract Delivery + Lead Automation — Cloudflare Worker
 * 
 * ROUTES:
 *   POST /                  — Gemini AI proxy (existing)
 *   POST /contract/create   — Create a one-time contract link (stores in KV)
 *   GET  /contract/fetch    — Client fetches contract to view/sign
 *   POST /contract/sign     — Client submits e-signature (locks contract)
 *   GET  /contract/status   — BidGen polls for contract status
 *   POST /lead/incoming     — Receive new lead from website forms
 *   GET  /lead/list         — List all leads (pin-protected)
 *   POST /lead/update       — Update lead status (pin-protected)
 *   GET  /lead/stats        — Dashboard stats (pin-protected)
 *   GET  /notifications     — Pull notification queue (pin-protected)
 * 
 * SECRETS (set via wrangler secret put):
 *   GEMINI_API_KEY          — Google Gemini API key
 *   CONTRACT_HMAC_SECRET    — HMAC key for signing tokens
 *   OWNER_PIN               — PIN for dashboard access
 * 
 * KV NAMESPACE:
 *   CONTRACTS               — KV store for contract data + leads
 *   Create: wrangler kv namespace create CONTRACTS
 * 
 * CRON TRIGGER (wrangler.toml):
 *   [triggers]
 *   crons = ["0 15 * * *"]   — Runs daily at 9 AM CST (15:00 UTC)
 * 
 * DEPLOYMENT:
 *   wrangler deploy          (from tools/ai-proxy/)
 */

const ALLOWED_ORIGINS = [
  'https://wattsatpcontractor.com',
  'https://www.wattsatpcontractor.com',
  'https://wattssafetyinstalls-debug.github.io',
  'http://localhost:4000',
  'http://127.0.0.1:4000'
];

const RATE_LIMIT = new Map();
const MAX_REQUESTS_PER_MINUTE = 10;
const CONTRACT_TTL = 90 * 24 * 60 * 60; // 90 days in seconds
const LEAD_TTL = 365 * 24 * 60 * 60; // 1 year in seconds

// Lead scoring rules
const LEAD_SCORES = {
  service: {
    'wheelchair-ramp': 10, 'grab-bars': 8, 'bathroom-accessibility': 9,
    'non-slip-flooring': 7, 'accessibility-safety': 10,
    'snow-removal': 6, 'handyman': 5, 'painting': 5, 'remodeling': 7,
    'other': 3, '': 1
  },
  urgency: {
    'immediately': 10, '1-2 weeks': 7, '1 month': 4, 'flexible': 2, '': 1
  }
};

function getRateLimitKey(request) {
  return request.headers.get('CF-Connecting-IP') || 'unknown';
}

function isRateLimited(key) {
  const now = Date.now();
  const entry = RATE_LIMIT.get(key);
  if (!entry || now > entry.resetTime) {
    RATE_LIMIT.set(key, { count: 1, resetTime: now + 60000 });
    return false;
  }
  entry.count++;
  return entry.count > MAX_REQUESTS_PER_MINUTE;
}

function getCorsHeaders(origin) {
  const isAllowed = ALLOWED_ORIGINS.some(o => origin.startsWith(o));
  return {
    'Access-Control-Allow-Origin': isAllowed ? origin : ALLOWED_ORIGINS[0],
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Contract-Auth',
    'Access-Control-Max-Age': '86400',
  };
}

function jsonResponse(data, status, corsHeaders) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });
}

// Generate a cryptographically secure token
async function generateToken() {
  const bytes = new Uint8Array(32);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
}

// HMAC-SHA256 sign a token so only our worker could have created it
async function hmacSign(token, secret) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(token));
  return Array.from(new Uint8Array(sig), b => b.toString(16).padStart(2, '0')).join('');
}

async function hmacVerify(token, signature, secret) {
  const expected = await hmacSign(token, secret);
  return expected === signature;
}

// =====================================================================
// ROUTE: AI PROXY (existing functionality)
// =====================================================================
async function handleAIProxy(request, env, corsHeaders) {
  if (request.method !== 'POST') {
    return jsonResponse({ error: 'Method not allowed' }, 405, corsHeaders);
  }

  const clientIP = getRateLimitKey(request);
  if (isRateLimited(clientIP)) {
    return jsonResponse({ error: 'Rate limit exceeded. Please wait a moment.' }, 429, corsHeaders);
  }

  try {
    const body = await request.json();
    const url = new URL(request.url);
    const model = url.searchParams.get('model') || 'gemini-2.5-pro';

    if (!body.contents || !Array.isArray(body.contents)) {
      return jsonResponse({ error: 'Invalid request format' }, 400, corsHeaders);
    }

    const geminiResponse = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      }
    );

    const data = await geminiResponse.json();

    if (!geminiResponse.ok) {
      return jsonResponse({ error: data.error?.message || 'Gemini API error' }, geminiResponse.status, corsHeaders);
    }

    return jsonResponse(data, 200, corsHeaders);
  } catch (error) {
    return jsonResponse({ error: 'Internal proxy error' }, 500, corsHeaders);
  }
}

// =====================================================================
// ROUTE: POST /contract/create
// Creates a one-time contract link, stores in KV
// Body: { invoiceId, contractData, clientEmail, clientName, ownerPin }
// Returns: { token, signature, url }
// =====================================================================
async function handleContractCreate(request, env, corsHeaders) {
  if (request.method !== 'POST') {
    return jsonResponse({ error: 'Method not allowed' }, 405, corsHeaders);
  }

  try {
    const body = await request.json();
    const { invoiceId, contractData, clientEmail, clientName, ownerPin } = body;

    if (!invoiceId || !contractData || !clientName || !ownerPin) {
      return jsonResponse({ error: 'Missing required fields: invoiceId, contractData, clientName, ownerPin' }, 400, corsHeaders);
    }

    const token = await generateToken();
    const signature = await hmacSign(token, env.CONTRACT_HMAC_SECRET);

    const record = {
      invoiceId,
      clientName,
      clientEmail: clientEmail || null,
      contractData,
      ownerPin,
      status: 'sent',           // sent → viewed → signed
      createdAt: new Date().toISOString(),
      viewedAt: null,
      signedAt: null,
      signatureData: null,      // base64 signature image or typed name
      signatureType: null,      // 'draw' or 'type'
      signerName: null,
      signerIP: null,
      lockedAt: null,
    };

    // Store in KV with 90-day TTL
    await env.CONTRACTS.put(`contract:${token}`, JSON.stringify(record), {
      expirationTtl: CONTRACT_TTL,
    });

    // Also store a lookup by invoiceId for status polling
    await env.CONTRACTS.put(`lookup:${ownerPin}:${invoiceId}`, token, {
      expirationTtl: CONTRACT_TTL,
    });

    const contractUrl = `https://wattsatpcontractor.com/contract/?t=${token}&s=${signature}`;

    return jsonResponse({
      success: true,
      token,
      signature,
      url: contractUrl,
    }, 200, corsHeaders);
  } catch (error) {
    return jsonResponse({ error: 'Failed to create contract: ' + error.message }, 500, corsHeaders);
  }
}

// =====================================================================
// ROUTE: GET /contract/fetch?t=TOKEN&s=SIGNATURE
// Client-facing: returns contract data for viewing/signing
// Marks status as 'viewed' on first access
// =====================================================================
async function handleContractFetch(request, env, corsHeaders) {
  const url = new URL(request.url);
  const token = url.searchParams.get('t');
  const signature = url.searchParams.get('s');

  if (!token || !signature) {
    return jsonResponse({ error: 'Missing token or signature' }, 400, corsHeaders);
  }

  // Verify HMAC
  const valid = await hmacVerify(token, signature, env.CONTRACT_HMAC_SECRET);
  if (!valid) {
    return jsonResponse({ error: 'Invalid or tampered link' }, 403, corsHeaders);
  }

  const raw = await env.CONTRACTS.get(`contract:${token}`);
  if (!raw) {
    return jsonResponse({ error: 'Contract not found or expired' }, 404, corsHeaders);
  }

  const record = JSON.parse(raw);

  // Mark as viewed on first access
  if (record.status === 'sent') {
    record.status = 'viewed';
    record.viewedAt = new Date().toISOString();
    await env.CONTRACTS.put(`contract:${token}`, JSON.stringify(record), {
      expirationTtl: CONTRACT_TTL,
    });
  }

  // Return contract data (hide internal fields)
  return jsonResponse({
    invoiceId: record.invoiceId,
    clientName: record.clientName,
    contractData: record.contractData,
    status: record.status,
    createdAt: record.createdAt,
    signedAt: record.signedAt,
    signerName: record.signerName,
    // If signed, include signature for read-only record view
    signatureData: record.status === 'signed' ? record.signatureData : null,
    signatureType: record.status === 'signed' ? record.signatureType : null,
  }, 200, corsHeaders);
}

// =====================================================================
// ROUTE: POST /contract/sign
// Client submits their e-signature — locks the contract permanently
// Body: { token, signature (HMAC), signerName, signatureData, signatureType }
// =====================================================================
async function handleContractSign(request, env, corsHeaders) {
  if (request.method !== 'POST') {
    return jsonResponse({ error: 'Method not allowed' }, 405, corsHeaders);
  }

  try {
    const body = await request.json();
    const { token, signature, signerName, signatureData, signatureType } = body;

    if (!token || !signature || !signerName || !signatureData) {
      return jsonResponse({ error: 'Missing required fields' }, 400, corsHeaders);
    }

    // Verify HMAC
    const valid = await hmacVerify(token, signature, env.CONTRACT_HMAC_SECRET);
    if (!valid) {
      return jsonResponse({ error: 'Invalid or tampered link' }, 403, corsHeaders);
    }

    const raw = await env.CONTRACTS.get(`contract:${token}`);
    if (!raw) {
      return jsonResponse({ error: 'Contract not found or expired' }, 404, corsHeaders);
    }

    const record = JSON.parse(raw);

    // Check if already signed — cannot sign twice
    if (record.status === 'signed') {
      return jsonResponse({
        error: 'This contract has already been signed',
        signedAt: record.signedAt,
        signerName: record.signerName,
      }, 409, corsHeaders);
    }

    // Lock the contract
    const signerIP = request.headers.get('CF-Connecting-IP') || 'unknown';
    record.status = 'signed';
    record.signedAt = new Date().toISOString();
    record.signatureData = signatureData;
    record.signatureType = signatureType || 'type';
    record.signerName = signerName;
    record.signerIP = signerIP;
    record.lockedAt = new Date().toISOString();

    // Save back to KV (keep the same TTL)
    await env.CONTRACTS.put(`contract:${token}`, JSON.stringify(record), {
      expirationTtl: CONTRACT_TTL,
    });

    return jsonResponse({
      success: true,
      message: 'Contract signed and locked successfully',
      signedAt: record.signedAt,
      signerName: record.signerName,
    }, 200, corsHeaders);
  } catch (error) {
    return jsonResponse({ error: 'Failed to process signature: ' + error.message }, 500, corsHeaders);
  }
}

// =====================================================================
// ROUTE: GET /contract/status?invoiceId=XXX&pin=YYY
// BidGen polls this to check contract status (sent/viewed/signed)
// =====================================================================
async function handleContractStatus(request, env, corsHeaders) {
  const url = new URL(request.url);
  const invoiceId = url.searchParams.get('invoiceId');
  const pin = url.searchParams.get('pin');

  if (!invoiceId || !pin) {
    return jsonResponse({ error: 'Missing invoiceId or pin' }, 400, corsHeaders);
  }

  // Lookup token by invoiceId
  const token = await env.CONTRACTS.get(`lookup:${pin}:${invoiceId}`);
  if (!token) {
    return jsonResponse({ error: 'No contract link found for this invoice' }, 404, corsHeaders);
  }

  const raw = await env.CONTRACTS.get(`contract:${token}`);
  if (!raw) {
    return jsonResponse({ error: 'Contract data expired' }, 404, corsHeaders);
  }

  const record = JSON.parse(raw);

  return jsonResponse({
    invoiceId: record.invoiceId,
    status: record.status,
    createdAt: record.createdAt,
    viewedAt: record.viewedAt,
    signedAt: record.signedAt,
    signerName: record.signerName,
    // Return signature data only when signed (for owner's records)
    signatureData: record.status === 'signed' ? record.signatureData : null,
    signatureType: record.status === 'signed' ? record.signatureType : null,
  }, 200, corsHeaders);
}

// =====================================================================
// LEAD SCORING
// =====================================================================
function scoreLead(data) {
  let score = 0;
  // Service type
  score += LEAD_SCORES.service[data.service] || LEAD_SCORES.service[''] || 1;
  // Urgency / timeline
  score += LEAD_SCORES.urgency[data.timeline] || LEAD_SCORES.urgency[''] || 1;
  // Phone provided = high intent
  if (data.phone && data.phone.replace(/\D/g, '').length >= 7) score += 5;
  // Email provided
  if (data.email && data.email.includes('@')) score += 2;
  // Message length (effort = intent)
  if (data.message && data.message.length > 50) score += 3;
  if (data.message && data.message.length > 150) score += 2;
  // Source bonus
  if (data.source === 'contact_form') score += 3;
  if (data.source === 'callback_widget' || data.source === 'mobile_callback') score += 4;
  if (data.source === 'exit_intent') score += 1;

  return score;
}

function getLeadPriority(score) {
  if (score >= 20) return 'hot';
  if (score >= 12) return 'warm';
  return 'cool';
}

// =====================================================================
// NOTIFICATION SYSTEM — No third-party APIs needed
// 1. SMS via AT&T email-to-SMS gateway (MailChannels, free on CF Workers)
// 2. Email via Formspree (already connected)
// 3. KV queue for dashboard pull-notifications
// =====================================================================

// AT&T email-to-SMS gateway — sends a real text to Justin's phone
const SMS_GATEWAY = '4054106402@txt.att.net';
const FROM_EMAIL = 'alerts@wattsatpcontractor.com';
const FROM_NAME = 'Watts Leads';

async function sendSMSviaEmail(message) {
  try {
    // MailChannels Send API — free for Cloudflare Workers (no API key needed)
    const res = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [{
          to: [{ email: SMS_GATEWAY }],
        }],
        from: { email: FROM_EMAIL, name: FROM_NAME },
        subject: 'Lead Alert',
        content: [{
          type: 'text/plain',
          // SMS gateway strips subject, only sends body. Keep under 160 chars.
          value: message.substring(0, 300),
        }],
      }),
    });
    const ok = res.status >= 200 && res.status < 300;
    if (!ok) console.log('[SMS] MailChannels status:', res.status, await res.text().catch(() => ''));
    return ok;
  } catch (err) {
    console.log('[SMS] MailChannels failed:', err.message);
    return false;
  }
}

async function sendNotification(env, message, priority) {
  const results = { sms: false, email: false, queued: false };

  // 1. Send real SMS via AT&T email-to-SMS gateway (MailChannels)
  results.sms = await sendSMSviaEmail(message);

  // 2. Send email notification via Formspree
  try {
    const priorityEmoji = priority === 'hot' ? '🔥' : priority === 'warm' ? '🟡' : '🔵';
    await fetch('https://formspree.io/f/mjkjgrlb', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        _subject: `${priorityEmoji} Watts Lead Alert: ${message.substring(0, 60)}`,
        message: message,
        priority: priority || 'normal',
        timestamp: new Date().toISOString(),
        _replyto: 'noreply@wattsatpcontractor.com',
      }),
    });
    results.email = true;
  } catch (err) {
    console.log('[Notify] Formspree failed:', err.message);
  }

  // 3. Queue in KV for dashboard pull-notifications
  try {
    const queueRaw = await env.CONTRACTS.get('notification_queue');
    const queue = queueRaw ? JSON.parse(queueRaw) : [];
    queue.unshift({
      message,
      priority: priority || 'normal',
      timestamp: new Date().toISOString(),
      read: false,
    });
    if (queue.length > 50) queue.length = 50;
    await env.CONTRACTS.put('notification_queue', JSON.stringify(queue), {
      expirationTtl: LEAD_TTL,
    });
    results.queued = true;
  } catch (err) {
    console.log('[Notify] Queue failed:', err.message);
  }

  return { success: results.sms || results.email || results.queued, ...results };
}

// =====================================================================
// LEAD EMAIL — sends lead details to Justin via Formspree
// =====================================================================
async function sendLeadEmail(env, lead) {
  try {
    const priorityEmoji = lead.priority === 'hot' ? '🔥' : lead.priority === 'warm' ? '🟡' : '🔵';
    await fetch('https://formspree.io/f/mjkjgrlb', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: lead.name,
        phone: lead.phone || '',
        email: lead.email || '',
        service: lead.service || 'General Inquiry',
        message: lead.message || '',
        _replyto: lead.email || '',
        _subject: `${priorityEmoji} New ${lead.priority?.toUpperCase() || ''} Lead (Score: ${lead.score}): ${lead.name} — ${lead.service || 'General'}`,
        source: lead.source,
        score: lead.score,
        priority: lead.priority,
        timeline: lead.timeline || '',
        page: lead.page,
        timestamp: lead.createdAt,
      }),
    });
    return { success: true };
  } catch (err) {
    return { success: false, reason: err.message };
  }
}

// =====================================================================
// ROUTE: GET /notifications?pin=XXXX — pull notification queue
// =====================================================================
async function handleNotifications(request, env, corsHeaders) {
  const url = new URL(request.url);
  const pin = url.searchParams.get('pin');

  if (!pin || pin !== env.OWNER_PIN) {
    return jsonResponse({ error: 'Unauthorized' }, 401, corsHeaders);
  }

  const queueRaw = await env.CONTRACTS.get('notification_queue');
  const queue = queueRaw ? JSON.parse(queueRaw) : [];

  // Mark as read if requested
  if (url.searchParams.get('markRead') === '1') {
    queue.forEach(n => n.read = true);
    await env.CONTRACTS.put('notification_queue', JSON.stringify(queue), {
      expirationTtl: LEAD_TTL,
    });
  }

  return jsonResponse({
    unread: queue.filter(n => !n.read).length,
    notifications: queue,
  }, 200, corsHeaders);
}

// =====================================================================
// ROUTE: POST /lead/incoming — Receive new lead from website
// =====================================================================
async function handleLeadIncoming(request, env, corsHeaders) {
  if (request.method !== 'POST') {
    return jsonResponse({ error: 'Method not allowed' }, 405, corsHeaders);
  }

  try {
    const data = await request.json();

    if (!data.name) {
      return jsonResponse({ error: 'Name is required' }, 400, corsHeaders);
    }

    // Score the lead
    const score = scoreLead(data);
    const priority = getLeadPriority(score);

    // Build lead record
    const leadId = `lead:${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    const lead = {
      id: leadId,
      name: data.name,
      phone: data.phone || '',
      email: data.email || '',
      service: data.service || '',
      timeline: data.timeline || '',
      message: data.message || '',
      source: data.source || 'unknown',
      page: data.page || '',
      referrer: data.referrer || '',
      score,
      priority,
      status: 'new',          // new → contacted → quoted → won → lost
      createdAt: new Date().toISOString(),
      contactedAt: null,
      followUps: [],           // track follow-up attempts
      notes: '',
      ip: request.headers.get('CF-Connecting-IP') || '',
      brand: data.brand || 'atp',  // atp or wsi
    };

    // Store in KV
    await env.CONTRACTS.put(leadId, JSON.stringify(lead), { expirationTtl: LEAD_TTL });

    // Add to the lead index (list of all lead IDs for dashboard)
    const indexRaw = await env.CONTRACTS.get('lead_index');
    const index = indexRaw ? JSON.parse(indexRaw) : [];
    index.unshift({ id: leadId, name: lead.name, score, priority, status: 'new', createdAt: lead.createdAt, service: lead.service });
    // Keep last 500 leads in index
    if (index.length > 500) index.length = 500;
    await env.CONTRACTS.put('lead_index', JSON.stringify(index), { expirationTtl: LEAD_TTL });

    // === AUTOMATION: Email lead details to Justin via Formspree ===
    const emailResult = await sendLeadEmail(env, lead);

    // === AUTOMATION: Queue notification for dashboard ===
    const notifyMsg = `NEW LEAD: ${lead.name} — ${lead.service || 'General'} — ${lead.phone || 'No phone'} — Score: ${score}`;
    const notifyResult = await sendNotification(env, notifyMsg, priority);

    return jsonResponse({
      success: true,
      leadId,
      score,
      priority,
      email: emailResult.success ? 'sent' : 'skipped',
      notified: notifyResult.success ? 'sent' : 'skipped',
    }, 200, corsHeaders);
  } catch (error) {
    return jsonResponse({ error: 'Failed to process lead: ' + error.message }, 500, corsHeaders);
  }
}

// =====================================================================
// ROUTE: GET /lead/list?pin=XXXX&status=new&limit=50
// =====================================================================
async function handleLeadList(request, env, corsHeaders) {
  const url = new URL(request.url);
  const pin = url.searchParams.get('pin');

  if (!pin || pin !== env.OWNER_PIN) {
    return jsonResponse({ error: 'Unauthorized' }, 401, corsHeaders);
  }

  const statusFilter = url.searchParams.get('status') || '';
  const limit = Math.min(parseInt(url.searchParams.get('limit') || '50'), 200);

  const indexRaw = await env.CONTRACTS.get('lead_index');
  let index = indexRaw ? JSON.parse(indexRaw) : [];

  if (statusFilter) {
    index = index.filter(l => l.status === statusFilter);
  }

  // Return summary list (not full lead data — fetch individually for detail)
  return jsonResponse({
    total: index.length,
    leads: index.slice(0, limit),
  }, 200, corsHeaders);
}

// =====================================================================
// ROUTE: GET /lead/detail?pin=XXXX&id=lead:XXXXX
// =====================================================================
async function handleLeadDetail(request, env, corsHeaders) {
  const url = new URL(request.url);
  const pin = url.searchParams.get('pin');
  const id = url.searchParams.get('id');

  if (!pin || pin !== env.OWNER_PIN) {
    return jsonResponse({ error: 'Unauthorized' }, 401, corsHeaders);
  }
  if (!id) {
    return jsonResponse({ error: 'Missing lead id' }, 400, corsHeaders);
  }

  const raw = await env.CONTRACTS.get(id);
  if (!raw) {
    return jsonResponse({ error: 'Lead not found' }, 404, corsHeaders);
  }

  return jsonResponse(JSON.parse(raw), 200, corsHeaders);
}

// =====================================================================
// ROUTE: POST /lead/update — Update lead status/notes
// Body: { pin, id, status?, notes?, contactedAt? }
// =====================================================================
async function handleLeadUpdate(request, env, corsHeaders) {
  if (request.method !== 'POST') {
    return jsonResponse({ error: 'Method not allowed' }, 405, corsHeaders);
  }

  try {
    const body = await request.json();
    const { pin, id, status, notes, contactedAt } = body;

    if (!pin || pin !== env.OWNER_PIN) {
      return jsonResponse({ error: 'Unauthorized' }, 401, corsHeaders);
    }
    if (!id) {
      return jsonResponse({ error: 'Missing lead id' }, 400, corsHeaders);
    }

    const raw = await env.CONTRACTS.get(id);
    if (!raw) {
      return jsonResponse({ error: 'Lead not found' }, 404, corsHeaders);
    }

    const lead = JSON.parse(raw);

    if (status) lead.status = status;
    if (notes !== undefined) lead.notes = notes;
    if (contactedAt) lead.contactedAt = contactedAt;

    await env.CONTRACTS.put(id, JSON.stringify(lead), { expirationTtl: LEAD_TTL });

    // Also update the index
    const indexRaw = await env.CONTRACTS.get('lead_index');
    if (indexRaw) {
      const index = JSON.parse(indexRaw);
      const entry = index.find(l => l.id === id);
      if (entry && status) entry.status = status;
      await env.CONTRACTS.put('lead_index', JSON.stringify(index), { expirationTtl: LEAD_TTL });
    }

    return jsonResponse({ success: true, lead }, 200, corsHeaders);
  } catch (error) {
    return jsonResponse({ error: 'Failed to update lead: ' + error.message }, 500, corsHeaders);
  }
}

// =====================================================================
// ROUTE: GET /lead/stats?pin=XXXX — Dashboard stats
// =====================================================================
async function handleLeadStats(request, env, corsHeaders) {
  const url = new URL(request.url);
  const pin = url.searchParams.get('pin');

  if (!pin || pin !== env.OWNER_PIN) {
    return jsonResponse({ error: 'Unauthorized' }, 401, corsHeaders);
  }

  const indexRaw = await env.CONTRACTS.get('lead_index');
  const index = indexRaw ? JSON.parse(indexRaw) : [];

  const now = new Date();
  const today = now.toISOString().split('T')[0];
  const weekAgo = new Date(now - 7 * 86400000).toISOString();
  const monthAgo = new Date(now - 30 * 86400000).toISOString();

  const stats = {
    total: index.length,
    today: index.filter(l => l.createdAt?.startsWith(today)).length,
    thisWeek: index.filter(l => l.createdAt >= weekAgo).length,
    thisMonth: index.filter(l => l.createdAt >= monthAgo).length,
    byStatus: {},
    byPriority: { hot: 0, warm: 0, cool: 0 },
    byService: {},
    avgScore: 0,
    needsFollowUp: 0,
  };

  let totalScore = 0;
  index.forEach(l => {
    stats.byStatus[l.status] = (stats.byStatus[l.status] || 0) + 1;
    stats.byPriority[l.priority] = (stats.byPriority[l.priority] || 0) + 1;
    if (l.service) stats.byService[l.service] = (stats.byService[l.service] || 0) + 1;
    totalScore += l.score || 0;
    // Needs follow-up: new leads older than 2 hours
    if (l.status === 'new' && l.createdAt < new Date(now - 2 * 3600000).toISOString()) {
      stats.needsFollowUp++;
    }
  });
  stats.avgScore = index.length > 0 ? Math.round(totalScore / index.length * 10) / 10 : 0;

  return jsonResponse(stats, 200, corsHeaders);
}

// =====================================================================
// CRON: Daily follow-up check (runs at 9 AM CST via Cloudflare Cron)
// =====================================================================
async function handleScheduled(env) {
  const indexRaw = await env.CONTRACTS.get('lead_index');
  if (!indexRaw) return;

  const index = JSON.parse(indexRaw);
  const now = new Date();
  let followUpCount = 0;

  for (const entry of index) {
    if (entry.status !== 'new') continue;

    const raw = await env.CONTRACTS.get(entry.id);
    if (!raw) continue;

    const lead = JSON.parse(raw);
    const ageMs = now - new Date(lead.createdAt);
    const ageDays = Math.floor(ageMs / 86400000);

    // Follow-up at 1 day, 3 days, 7 days
    const followUpDays = [1, 3, 7];
    const dueFollowUp = followUpDays.find(d => ageDays >= d && !lead.followUps.includes(d));

    if (dueFollowUp && lead.phone) {
      const msgs = {
        1: `⏰ FOLLOW UP (Day 1): ${lead.name} — ${lead.service || 'General'} — ${lead.phone}. Lead from ${lead.source}. No response yet.`,
        3: `📋 FOLLOW UP (Day 3): ${lead.name} still hasn't been contacted. Phone: ${lead.phone}. Service: ${lead.service || 'General'}. Consider calling today.`,
        7: `🚨 FINAL FOLLOW UP (Day 7): ${lead.name} — ${lead.phone}. This lead will go cold soon. Last chance to convert.`,
      };

      await sendNotification(env, msgs[dueFollowUp], lead.priority);

      lead.followUps.push(dueFollowUp);
      await env.CONTRACTS.put(entry.id, JSON.stringify(lead), { expirationTtl: LEAD_TTL });
      followUpCount++;
    }

    // Auto-mark as cold after 14 days with no contact
    if (ageDays >= 14 && lead.status === 'new') {
      lead.status = 'cold';
      entry.status = 'cold';
      await env.CONTRACTS.put(entry.id, JSON.stringify(lead), { expirationTtl: LEAD_TTL });
    }
  }

  // Save updated index
  await env.CONTRACTS.put('lead_index', JSON.stringify(index), { expirationTtl: LEAD_TTL });

  // Send daily summary if there are new leads
  const newLeads = index.filter(l => l.status === 'new').length;
  const hotLeads = index.filter(l => l.priority === 'hot' && l.status === 'new').length;
  if (newLeads > 0) {
    await sendNotification(env,
      `📊 Daily Lead Summary: ${newLeads} open leads (${hotLeads} hot). ${followUpCount} follow-up reminders sent today.`, 'normal');
  }
}

// =====================================================================
// MAIN ROUTER
// =====================================================================
export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const corsHeaders = getCorsHeaders(origin);
    const url = new URL(request.url);
    const path = url.pathname;

    // Handle preflight for all routes
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    // Contract routes
    if (path === '/contract/create') {
      return handleContractCreate(request, env, corsHeaders);
    }
    if (path === '/contract/fetch') {
      return handleContractFetch(request, env, corsHeaders);
    }
    if (path === '/contract/sign') {
      return handleContractSign(request, env, corsHeaders);
    }
    if (path === '/contract/status') {
      return handleContractStatus(request, env, corsHeaders);
    }

    // Lead automation routes
    if (path === '/lead/incoming') {
      return handleLeadIncoming(request, env, corsHeaders);
    }
    if (path === '/lead/list') {
      return handleLeadList(request, env, corsHeaders);
    }
    if (path === '/lead/detail') {
      return handleLeadDetail(request, env, corsHeaders);
    }
    if (path === '/lead/update') {
      return handleLeadUpdate(request, env, corsHeaders);
    }
    if (path === '/lead/stats') {
      return handleLeadStats(request, env, corsHeaders);
    }
    if (path === '/notifications') {
      return handleNotifications(request, env, corsHeaders);
    }

    // Default: AI proxy (existing behavior)
    return handleAIProxy(request, env, corsHeaders);
  },

  // Cron trigger handler — daily follow-up checks
  async scheduled(event, env, ctx) {
    ctx.waitUntil(handleScheduled(env));
  },
};
