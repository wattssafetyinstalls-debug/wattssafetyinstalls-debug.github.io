# Watts AI Proxy + Contract Delivery — Cloudflare Worker

Securely proxies Gemini API requests and powers the contract e-sign delivery system.

## Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/` | Gemini AI proxy (existing) |
| POST | `/contract/create` | Create a one-time contract e-sign link |
| GET | `/contract/fetch` | Client fetches contract to view/sign |
| POST | `/contract/sign` | Client submits e-signature (locks contract) |
| GET | `/contract/status` | BidGen polls for contract status |

## Setup

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

### 4. Create KV namespace for contracts
```bash
cd tools/ai-proxy
wrangler kv namespace create CONTRACTS
```
Copy the `id` from the output and paste it into `wrangler.toml` replacing `PLACEHOLDER_REPLACE_AFTER_KV_CREATE`.

### 5. Deploy the worker
```bash
wrangler deploy
```

### 6. Set secrets
```bash
wrangler secret put GEMINI_API_KEY
```
Paste your paid Gemini API key when prompted.

```bash
wrangler secret put CONTRACT_HMAC_SECRET
```
Generate a strong random string (e.g. `openssl rand -hex 32`) and paste it. This signs contract tokens so they can't be forged.

### 7. Note your worker URL
After deploy, you'll see:
```
https://watts-ai-proxy.wattssafetyinstalls.workers.dev
```

## Security Features
- **CORS locked** to wattsatpcontractor.com, GitHub Pages, and localhost only
- **Rate limited** to 10 requests/minute per IP
- **Request validation** — rejects malformed payloads
- **API key hidden** — stored as Cloudflare encrypted secret
- **HMAC-signed tokens** — contract links are cryptographically verified
- **One-time signing** — contracts lock permanently after e-signature
- **90-day TTL** — contract data auto-expires from KV after 90 days

## Contract E-Sign Flow
1. BidGen calls `POST /contract/create` with invoice data → gets a signed URL
2. Client opens the URL → `GET /contract/fetch` returns contract, marks as "viewed"
3. Client signs → `POST /contract/sign` locks the contract permanently
4. BidGen polls `GET /contract/status` to track sent → viewed → signed

## Free Tier Limits
Cloudflare Workers free tier: **100,000 requests/day**, KV: **100,000 reads/day**, **1,000 writes/day** — more than enough.
