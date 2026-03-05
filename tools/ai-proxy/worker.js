/**
 * Watts AI Proxy + Contract Delivery — Cloudflare Worker
 * 
 * ROUTES:
 *   POST /                  — Gemini AI proxy (existing)
 *   POST /contract/create   — Create a one-time contract link (stores in KV)
 *   GET  /contract/fetch    — Client fetches contract to view/sign
 *   POST /contract/sign     — Client submits e-signature (locks contract)
 *   GET  /contract/status   — BidGen polls for contract status
 * 
 * SECRETS (set via wrangler secret put):
 *   GEMINI_API_KEY          — Google Gemini API key
 *   CONTRACT_HMAC_SECRET    — HMAC key for signing tokens
 * 
 * KV NAMESPACE:
 *   CONTRACTS               — KV store for contract data
 *   Create: wrangler kv namespace create CONTRACTS
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

    // Default: AI proxy (existing behavior)
    return handleAIProxy(request, env, corsHeaders);
  },
};
