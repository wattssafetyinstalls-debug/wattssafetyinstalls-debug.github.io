/**
 * Watts AI Proxy — Cloudflare Worker
 * Securely proxies requests to Google Gemini API
 * 
 * DEPLOYMENT:
 * 1. Install Wrangler: npm install -g wrangler
 * 2. Login: wrangler login
 * 3. Deploy: wrangler deploy
 * 4. Set API key: wrangler secret put GEMINI_API_KEY
 *    (paste your Gemini paid API key when prompted)
 * 
 * Your worker URL will be: https://watts-ai-proxy.<your-subdomain>.workers.dev
 * Update PROXY_URL in watts-ai-chat.js and ai-dashboard after deploying.
 */

const ALLOWED_ORIGINS = [
  'https://wattsatpcontractor.com',
  'https://www.wattsatpcontractor.com',
  'https://wattssafetyinstalls-debug.github.io',
  'http://localhost:4000',
  'http://127.0.0.1:4000'
];

const RATE_LIMIT = new Map(); // IP -> { count, resetTime }
const MAX_REQUESTS_PER_MINUTE = 10;

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
  if (entry.count > MAX_REQUESTS_PER_MINUTE) return true;
  return false;
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const isAllowed = ALLOWED_ORIGINS.some(o => origin.startsWith(o));
    
    const corsHeaders = {
      'Access-Control-Allow-Origin': isAllowed ? origin : ALLOWED_ORIGINS[0],
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    };

    // Handle preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    // Only POST allowed
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Rate limiting
    const clientIP = getRateLimitKey(request);
    if (isRateLimited(clientIP)) {
      return new Response(JSON.stringify({ error: 'Rate limit exceeded. Please wait a moment.' }), {
        status: 429,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    try {
      const body = await request.json();
      const url = new URL(request.url);
      const model = url.searchParams.get('model') || 'gemini-2.5-flash';

      // Validate request structure
      if (!body.contents || !Array.isArray(body.contents)) {
        return new Response(JSON.stringify({ error: 'Invalid request format' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      // Call Gemini API
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
        return new Response(JSON.stringify({ error: data.error?.message || 'Gemini API error' }), {
          status: geminiResponse.status,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      return new Response(JSON.stringify(data), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });

    } catch (error) {
      return new Response(JSON.stringify({ error: 'Internal proxy error' }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }
  },
};
