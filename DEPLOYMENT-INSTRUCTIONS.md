# GitHub Pages Deployment Instructions

## Security Headers Issue ⚠️

**GitHub Pages does NOT support custom HTTP headers** (like HSTS, CSP, X-Frame-Options).

### Solutions:

#### Option 1: Use Cloudflare (FREE - RECOMMENDED)
1. Go to [Cloudflare.com](https://cloudflare.com) and create free account
2. Add your domain `wattsatpcontractor.com`
3. Update nameservers at your domain registrar
4. In Cloudflare dashboard → Rules → Transform Rules → HTTP Response Headers:
   - Add these headers:
   ```
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   X-Content-Type-Options: nosniff
   X-Frame-Options: SAMEORIGIN
   Referrer-Policy: strict-origin-when-cross-origin
   Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://www.google-analytics.com https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https: http:; connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com; frame-src 'self' https://www.google.com https://www.googletagmanager.com
   Permissions-Policy: geolocation=(), microphone=(), camera=()
   ```

#### Option 2: Move to Netlify (FREE)
1. Sign up at [Netlify.com](https://netlify.com)
2. Connect your GitHub repo
3. Netlify automatically reads `_headers` file (already created)
4. Deploy happens automatically on git push

#### Option 3: Add Meta Tags (Partial Solution)
Add to each page's `<head>`:
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'">
```
**Note:** This is NOT as secure as HTTP headers

---

## Redirects Setup

### Step 1: Install Jekyll Plugins
```bash
bundle install
```

### Step 2: Add Front Matter to Create Redirects

For 404 pages, add redirect front matter:

**Example:** Create `wheelchair-ramps.html`:
```yaml
---
redirect_to: /services/wheelchair-ramp-installation/
---
```

---

## Deploy to GitHub Pages

### 1. Commit and Push
```bash
git add .
git commit -m "Complete SEO fixes: carousels, gradients, redirects, meta optimization"
git push origin main
```

### 2. Enable GitHub Pages
1. Go to repo Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/ (root)`
4. Save

### 3. Wait 1-3 minutes for deployment

---

## Post-Deployment Checklist

### Test Security Headers:
```bash
curl -I https://wattsatpcontractor.com
```

If you see headers like `Strict-Transport-Security`, you're good!

If NOT → Use Cloudflare (Option 1 above)

### Test Redirects:
- Visit https://wattsatpcontractor.com/wheelchair-ramps
- Should redirect to https://wattsatpcontractor.com/services/wheelchair-ramp-installation/

### Run SEO Audit Again:
Use Screaming Frog or similar tool to verify:
- ✅ Canonicals fixed
- ✅ Meta descriptions optimized
- ✅ Redirects working
- ✅ No 404 errors

---

## What's Been Fixed:

✅ **Q&A Carousels** - All 65 service pages
✅ **Gradient Animations** - Standardized across all pages  
✅ **Redirects** - `_redirects` file created (works on Netlify)
✅ **Meta Descriptions** - Optimized lengths
✅ **Canonicals** - Single canonical per page
✅ **External Links** - Added `rel="noopener"`

⚠️ **Security Headers** - Requires Cloudflare/Netlify (see above)

---

## Recommended: Use Cloudflare

**Why Cloudflare?**
- FREE forever
- Instant security headers
- CDN speeds up your site
- DDoS protection
- Works with GitHub Pages
- 5-minute setup

This solves ALL 70 security header warnings instantly!