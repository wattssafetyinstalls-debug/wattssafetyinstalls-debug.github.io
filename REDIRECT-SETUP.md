# GitHub Pages Redirect & URL Structure Fix

## Problem Summary
GitHub Pages uses **nginx** (not Apache), so `.htaccess` files don't work. You had:
- Inconsistent canonical URLs (some with .html, some without, some with /index)
- Duplicate pages (both `/about.html` and `/about/index.html`)
- No proper redirect handling
- URL structure chaos

## Solution Implemented

### 1. Updated `_config.yml`
- Added comprehensive exclusion list for backup files, test files, and unnecessary content
- Set `permalink: none` for clean URLs
- Removed `.htaccess` from deployment

### 2. Created Client-Side Redirect System
Since GitHub Pages doesn't support server-side redirects (except through Jekyll plugins), we use JavaScript:

#### `_includes/redirect-handler.html`
Add this to all pages in the `<head>` section:
```html
{% include redirect-handler.html %}
```

This handles:
- `/index` → `/`
- `/about/index` → `/about.html`
- `/services/[slug]/index` → `/services/[slug]/`
- Cleans `.html` from URL bar display

#### Enhanced `404.html`
- Custom branded 404 page
- Includes redirect logic for common patterns
- Provides navigation options

### 3. Fixed Canonical URLs
Updated `_includes/seo-meta.html` to:
- Automatically remove `/index.html` and `/index` from canonical URLs
- Support manual override with `canonical` front matter
- Generate clean, consistent URLs

### 4. URL Structure Standards

#### Main Pages (use .html files)
```
✅ /about.html          → canonical: https://wattsatpcontractor.com/about.html
✅ /contact.html        → canonical: https://wattsatpcontractor.com/contact.html
✅ /services.html       → canonical: https://wattsatpcontractor.com/services.html
✅ /privacy-policy.html → canonical: https://wattsatpcontractor.com/privacy-policy.html
```

#### Service Pages (use folders with index.html)
```
✅ /services/accessibility-safety-solutions/index.html
   → canonical: https://wattsatpcontractor.com/services/accessibility-safety-solutions/
   
✅ /services/grab-bars/index.html
   → canonical: https://wattsatpcontractor.com/services/grab-bars/
```

## Action Items

### Immediate (Required)

1. **Delete Duplicate Folders**
   ```bash
   # Delete these duplicate page folders:
   rm -rf about/
   rm -rf contact/
   rm -rf privacy-policy/
   rm -rf service-area/
   rm -rf referrals/
   rm -rf sitemap/
   ```

2. **Add Redirect Handler to All Pages**
   Add to `<head>` section of:
   - `index.html`
   - `about.html`
   - `contact.html`
   - `services.html`
   - `testimonials.html`
   - `service-area.html`
   - `referrals.html`
   - `privacy-policy.html`
   - All service pages in `/services/*/index.html`

   ```html
   {% include redirect-handler.html %}
   ```

3. **Fix Canonical URLs**
   Replace hardcoded canonical tags with:
   ```html
   {% include seo-meta.html %}
   ```

4. **Update Service Page Canonicals**
   Each service page should have:
   ```html
   ---
   canonical: https://wattsatpcontractor.com/services/[slug]/
   ---
   ```

### Medium Priority

5. **Create Redirect Map File**
   Create `_redirects.yml` for documentation:
   ```yaml
   # Old URL → New URL
   /index: /
   /about/index: /about.html
   /services/index: /services.html
   # etc.
   ```

6. **Update Internal Links**
   Change all internal links to use clean URLs:
   ```html
   <!-- Before -->
   <a href="/about.html">About</a>
   
   <!-- After -->
   <a href="/about">About</a>
   ```

7. **Update Sitemap**
   Already done! The sitemap.xml now has correct URLs.

## How GitHub Pages Serves Files

### Default Behavior
```
Request: /about
GitHub serves: /about.html (if exists)

Request: /services/grab-bars/
GitHub serves: /services/grab-bars/index.html (if exists)

Request: /services/grab-bars
GitHub redirects: /services/grab-bars/ (301)
```

### Our Structure
```
Root pages:
  /about.html          → accessible as /about
  /contact.html        → accessible as /contact
  /services.html       → accessible as /services

Service pages:
  /services/grab-bars/index.html → accessible as /services/grab-bars/
```

## Testing Checklist

After deployment, test these URLs:

### Should Work (200 OK)
- [ ] https://wattsatpcontractor.com/
- [ ] https://wattsatpcontractor.com/about
- [ ] https://wattsatpcontractor.com/about.html
- [ ] https://wattsatpcontractor.com/contact
- [ ] https://wattsatpcontractor.com/services
- [ ] https://wattsatpcontractor.com/services/grab-bars/
- [ ] https://wattsatpcontractor.com/services/accessibility-safety-solutions/

### Should Redirect
- [ ] /index → /
- [ ] /about/index → /about.html
- [ ] /services/grab-bars/index → /services/grab-bars/

### Should 404
- [ ] /about/
- [ ] /contact/
- [ ] /nonexistent-page

## Canonical URL Patterns

### Homepage
```html
<link rel="canonical" href="https://wattsatpcontractor.com/">
```

### Main Pages
```html
<link rel="canonical" href="https://wattsatpcontractor.com/about.html">
<link rel="canonical" href="https://wattsatpcontractor.com/contact.html">
<link rel="canonical" href="https://wattsatpcontractor.com/services.html">
```

### Service Pages
```html
<link rel="canonical" href="https://wattsatpcontractor.com/services/grab-bars/">
<link rel="canonical" href="https://wattsatpcontractor.com/services/tv-mounting/">
```

## Common Issues & Solutions

### Issue: Duplicate Content
**Problem**: Both `/about.html` and `/about/index.html` exist
**Solution**: Delete folder versions, keep only .html files for main pages

### Issue: Wrong Canonical
**Problem**: Canonical points to `/about/index`
**Solution**: Use the seo-meta.html include which auto-fixes this

### Issue: 404 on Service Pages
**Problem**: Service page URLs not working
**Solution**: Ensure folder structure is `/services/[slug]/index.html`

### Issue: Redirect Loops
**Problem**: Page keeps redirecting
**Solution**: Check redirect-handler.html logic, ensure no circular redirects

## File Cleanup Commands

```bash
# Remove all backup files
find . -name "*.backup" -delete
find . -name "*.backup2" -delete
find . -name "*.bak" -delete

# Remove backup directories
rm -rf website-backup-*
rm -rf services-backup-*
rm -rf backup_before_faq_*

# Remove test files
rm -f test_*.html
rm -f test-*.html
rm -f html-test.html
rm -f index-backup.html
rm -f idex.html

# Remove duplicate folders
rm -rf about/
rm -rf contact/
rm -rf privacy-policy/
rm -rf service-area/
rm -rf referrals/
rm -rf sitemap/

# Remove .htaccess (doesn't work on GitHub Pages)
rm -f .htaccess
```

## Deployment Notes

1. **GitHub Pages automatically**:
   - Serves .html files without extension
   - Adds trailing slash to directories
   - Serves index.html from directories

2. **We handle**:
   - Redirecting old /index URLs
   - Cleaning up URL bar display
   - Consistent canonical URLs
   - 404 page with helpful redirects

3. **Users see**:
   - Clean URLs without .html
   - Consistent navigation
   - No broken links
   - Proper SEO signals

---

**Last Updated**: December 8, 2025
**Status**: Ready for implementation