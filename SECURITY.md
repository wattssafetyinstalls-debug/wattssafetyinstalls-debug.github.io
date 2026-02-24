# SECURITY RULES — Watts ATP / Watts Safety Installs

## THIS IS A PUBLIC REPOSITORY

Everything committed here is **publicly visible on the internet**. GitHub Pages repos are public by nature.

---

## ABSOLUTE RULE: NO API KEYS IN CODE

**NEVER** put any of the following directly in HTML, JS, JSON, Python, or any source file:

- Google Maps API keys (`AIza...`)
- Firebase API keys
- OpenWeatherMap API keys
- Cloudinary API secrets
- OpenAI / Gemini API keys (`sk-...`)
- AWS credentials (`AKIA...`)
- Any token, secret, password, or credential of any kind

### What to do instead

| Scenario | Solution |
|----------|----------|
| **Server-side API calls** | Use GitHub Secrets + GitHub Actions |
| **Client-side API calls** | Route through the Cloudflare Worker proxy (`watts-ai-proxy.wattssafetyinstalls.workers.dev`) |
| **Firebase** | Use domain-restricted keys + Firebase Security Rules (keys are still visible but locked to your domain) |
| **Google Maps** | Restrict the key to your domains only in Google Cloud Console |
| **Weather / 3rd party widgets** | Route through the Cloudflare Worker proxy |

### Placeholder format

If a file needs a key value, use these placeholders:
```
YOUR_FIREBASE_API_KEY_HERE
YOUR_GOOGLE_MAPS_KEY_HERE
YOUR_OPENWEATHERMAP_KEY_HERE
YOUR_CLOUDINARY_CLOUD_NAME
YOUR_UPLOAD_PRESET
```

---

## Protection layers in place

1. **Pre-commit hook** (`.git/hooks/pre-commit`) — blocks commits containing key patterns locally
2. **GitHub Actions scanner** (`.github/workflows/secret-scanner.yml`) — fails the build if keys are detected
3. **`.gitignore`** — blocks `.env`, `secrets.json`, credential files from being staged
4. **GitHub's built-in secret scanning** — sends email alerts when known key patterns are pushed

---

## If a key is accidentally exposed

1. **Rotate the key immediately** — the old key is compromised forever once pushed
2. Remove it from the source files
3. Check billing dashboards for unauthorized usage
4. Consider running BFG Repo Cleaner to scrub git history

---

## Key rotation dashboard links

- **Google Cloud Console**: https://console.cloud.google.com/apis/credentials
- **Firebase Console**: https://console.firebase.google.com (Project Settings)
- **OpenWeatherMap**: https://home.openweathermap.org/api_keys
- **Cloudinary**: https://console.cloudinary.com
- **Cloudflare Workers**: https://dash.cloudflare.com (Workers & Pages > watts-ai-proxy > Settings > Variables)
