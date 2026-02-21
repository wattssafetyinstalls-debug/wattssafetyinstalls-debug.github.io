# Watts AI Proxy — Cloudflare Worker

Securely proxies Gemini API requests so your API key is never exposed in browser code.

## Setup (5 minutes)

### 1. Create free Cloudflare account
Go to https://dash.cloudflare.com/sign-up

### 2. Install Wrangler CLI
```bash
npm install -g wrangler
```

### 3. Login to Cloudflare
```bash
wrangler login
```

### 4. Deploy the worker
```bash
cd tools/ai-proxy
wrangler deploy
```

### 5. Set your Gemini API key as a secret
```bash
wrangler secret put GEMINI_API_KEY
```
Paste your paid Gemini API key when prompted. This is stored encrypted — never visible in code.

### 6. Note your worker URL
After deploy, you'll see something like:
```
https://watts-ai-proxy.YOUR_SUBDOMAIN.workers.dev
```

### 7. Update the chatbot and dashboard
Replace `PROXY_URL` in these files with your worker URL:
- `/js/watts-ai-chat.js` (line ~10)
- `/tools/ai-dashboard/index.html` (line ~15)

## Security Features
- **CORS locked** to wattsatpcontractor.com only
- **Rate limited** to 10 requests/minute per IP
- **Request validation** — rejects malformed payloads
- **API key hidden** — stored as Cloudflare encrypted secret

## Free Tier Limits
Cloudflare Workers free tier: **100,000 requests/day** — more than enough.
