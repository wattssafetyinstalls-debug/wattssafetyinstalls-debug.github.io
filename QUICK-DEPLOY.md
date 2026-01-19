# Quick Deploy Guide

## Step 1: Install Dependencies
```bash
bundle install
```

## Step 2: Commit Everything
```bash
git add .
git commit -m "Complete SEO fixes: carousels, gradients, security, redirects"
git push origin main
```

## Step 3: Fix Security Headers (CRITICAL)

GitHub Pages **DOES NOT** support security headers natively.

### Fastest Solution: Cloudflare (5 minutes)

1. **Sign up**: Go to https://cloudflare.com (FREE)
2. **Add site**: Enter `wattsatpcontractor.com`
3. **Update nameservers** at your domain registrar (GoDaddy/Namecheap/etc)
4. **Add headers** in Cloudflare:
   - Go to Rules → Transform Rules → Modify Response Header
   - Add all 6 headers (see DEPLOYMENT-INSTRUCTIONS.md)

**This fixes 70 security warnings instantly!**

---

## Alternative: Move to Netlify

If you prefer, deploy to Netlify instead:

```bash
# Netlify reads _headers file automatically
netlify deploy --prod
```

---

## What's Fixed:

✅ 2 pages with missing carousels (smart-audio, wheelchair-ramp-installation)
✅ All gradient animations standardized
✅ Redirects for 404 errors
✅ Meta descriptions optimized
✅ Canonical tags cleaned
✅ External links secured

⚠️ Security headers require Cloudflare (GitHub Pages limitation)

---

## Test After Deploy:

```bash
# Test headers
curl -I https://wattsatpcontractor.com

# Test redirects
curl -I https://wattsatpcontractor.com/wheelchair-ramps
```

Expected: Should show security headers and 301 redirect!