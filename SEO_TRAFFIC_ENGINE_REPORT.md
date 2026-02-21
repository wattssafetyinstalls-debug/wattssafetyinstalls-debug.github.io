# PHASE 1 — REPO ANALYSIS REPORT
**Generated:** Feb 20, 2026  
**Domain:** wattsatpcontractor.com  
**Hosting:** GitHub Pages  
**Brands:** Watts ATP Contractor (root) + Watts Safety Installs (/safety-installs/)

---

## A. INVENTORY — ALL PAGES

### ATP Site (root /) — 14 pages
| Page | File | Schema | Meta Desc | Canonical | FAQ Schema | Service Schema |
|------|------|--------|-----------|-----------|------------|----------------|
| Homepage | index.html | ✅ HomeAndConstructionBusiness + WebSite | ✅ | ✅ | ❌ | ❌ (only Offer) |
| About | about.html | ✅ HomeAndConstructionBusiness | ✅ | ✅ | ❌ | ❌ |
| Services | services.html | ✅ Service | ✅ | ✅ | ❌ | ✅ |
| Service Area | service-area.html | ✅ HomeAndConstructionBusiness + WebPage | ✅ | ✅ | ❌ | ❌ |
| Contact | contact.html | ✅ HomeAndConstructionBusiness | ✅ | ✅ | ❌ | ❌ |
| Referrals | referrals.html | ✅ HomeAndConstructionBusiness | ✅ | ✅ | ❌ | ❌ |
| Privacy | privacy-policy.html | ✅ HomeAndConstructionBusiness | ✅ | ✅ | ❌ | ❌ |
| Sitemap | sitemap.html | ✅ HomeAndConstructionBusiness | ✅ | ✅ | ❌ | ❌ |
| 404 | 404.html | ❌ | ✅ | ❌ | ❌ | ❌ |
| Accessibility Solutions | accessibility-safety-solutions.html | ✅ Service | ✅ | ✅ | ❌ | ✅ |
| Bathroom Accessibility | bathroom-accessibility.html | ✅ ? | ✅ | ✅ | ❌ | ? |
| Grab Bar Install | grab-bar-installation.html | ✅ Service | ✅ | ✅ | ❌ | ✅ |
| Non-Slip Flooring | non-slip-flooring-solutions.html | ✅ ? | ✅ | ✅ | ❌ | ? |
| Wheelchair Ramps | wheelchair-ramp-installation.html | ✅ ? | ✅ | ✅ | ❌ | ? |

### Safety Installs (/safety-installs/) — 13 pages
| Page | File | Schema | Meta Desc | Canonical | FAQ Schema | Service Schema |
|------|------|--------|-----------|-----------|------------|----------------|
| Homepage | index.html | ✅ | ✅ | ✅ | ❌ | ❌ |
| About | about.html | ✅ | ✅ | ✅ | ❌ | ❌ |
| Services | services.html | ✅ Service | ✅ | ✅ | ❌ | ✅ |
| Service Area | service-area.html | ✅ | ✅ | ✅ | ❌ | ❌ |
| Contact | contact.html | ✅ | ✅ | ✅ | ❌ | ❌ |
| Referrals | referrals.html | ✅ | ✅ | ✅ | ❌ | ❌ |
| Privacy | privacy-policy.html | ✅ | ✅ | ✅ | ❌ | ❌ |
| Sitemap | sitemap.html | ✅ | ✅ | ✅ | ❌ | ❌ |
| Electronics | services/electronics.html | ❌ MISSING | ✅ | ✅ | ❌ | ❌ |
| Handyman | services/handyman.html | ❌ MISSING | ✅ | ✅ | ❌ | ❌ |
| Kitchen/Bath | services/kitchen-bath-remodeling.html | ❌ MISSING | ✅ | ✅ | ❌ | ❌ |
| Painting/Gutters | services/painting-gutters.html | ❌ MISSING | ✅ | ✅ | ❌ | ❌ |
| Property Maint. | services/property-maintenance.html | ❌ MISSING | ✅ | ✅ | ❌ | ❌ |

**Total pages: 27** (14 ATP + 13 Safety Installs)

---

## B. CRITICAL SCHEMA GAPS

### B1. areaServed is GENERIC on ALL pages
- **Current:** `"areaServed": "Nebraska"` (one word, statewide)
- **Should be:** Array of ~24 NE counties + ~3 IA counties with all towns within 100-mile radius of Norfolk
- **Impact:** Google has no idea you serve specific towns. Zero local SEO signal for any town besides Norfolk.
- **Fix:** Replace with structured GeoCircle + county/town array on every page

### B2. ZERO FAQPage schema — entire site
- **0 out of 27 pages** have FAQPage schema
- **Impact:** No FAQ rich results in Google. Missing featured snippet opportunities for every service.
- **Fix:** Add 3-5 Q&A per service page as FAQPage JSON-LD

### B3. ZERO QAPage schema — entire site
- **Impact:** No Q&A rich results
- **Fix:** Add to service-area and service pages where relevant

### B4. ZERO Review/AggregateRating schema on service pages
- Homepage has `aggregateRating` (5.0, 1 review) but NO individual Review schema
- Service pages have ZERO review schema
- **Impact:** No star ratings in search results
- **Fix:** Add AggregateRating + individual Review schema to service pages

### B5. 5 Safety Installs service pages — ZERO schema of any kind
- `services/electronics.html` — no schema
- `services/handyman.html` — no schema
- `services/kitchen-bath-remodeling.html` — no schema
- `services/painting-gutters.html` — no schema
- `services/property-maintenance.html` — no schema
- **Impact:** Google treats these as thin pages with no structured data signal
- **Fix:** Add full Service + LocalBusiness + FAQ schema to each

---

## C. METADATA GAPS

### C1. Meta descriptions are generic / not town-targeted
- Most descriptions mention only "Norfolk NE"
- No descriptions target surrounding towns (Columbus, Wayne, Fremont, South Sioux City, etc.)
- **Fix:** Rewrite descriptions with "Norfolk NE & surrounding areas" + key nearby cities

### C2. Missing OG/Twitter tags on some pages
- Safety Installs service subpages may lack OG tags
- **Fix:** Add OG + Twitter meta to all pages

### C3. Sitemap lastmod dates are stale
- All entries show `2025-02-20` — nearly a year old
- **Fix:** Update to current date on every deploy

---

## D. INTERNAL LINKING GAPS

### D1. Service pages don't cross-link to each other
- `grab-bar-installation.html` doesn't link to `bathroom-accessibility.html`
- `wheelchair-ramp-installation.html` doesn't link to `accessibility-safety-solutions.html`
- No "Related Services" section on any service page
- **Impact:** Poor link equity distribution. Google can't understand page relationships.
- **Fix:** Add "Related Services" section to every service page

### D2. ATP site doesn't link to Safety Installs service pages
- No cross-brand linking between brother/sister companies
- **Fix:** Add contextual links where services overlap (e.g., remodeling, maintenance)

### D3. Service-area pages don't link to specific services
- The service-area page lists areas but doesn't link to relevant services
- **Fix:** Add service links per area or at minimum a "Services We Bring" section

### D4. No town-specific landing pages exist
- Zero pages targeting "grab bar installation Columbus NE" or "wheelchair ramp Wayne NE"
- **Impact:** Missing all long-tail local search traffic
- **Fix:** Phase 4 landing page generator

---

## E. CONTENT GAPS

### E1. No FAQ content on any page
- Not a single page has visible FAQ accordion or section
- **Impact:** Missing voice search, featured snippet, and People Also Ask opportunities
- **Fix:** Add 3-5 Q&A per service page (visible + schema)

### E2. No "100-mile radius" or "no job too far" messaging
- Service-area pages don't mention the 100-mile radius
- No travel/distance messaging anywhere
- **Fix:** Add to service-area pages, footers, schema, FAQ entries

### E3. No town-specific content
- No pages mention specific towns by name in body content
- **Fix:** Add county/town content blocks to service-area pages

### E4. No seasonal/urgency content
- No winter prep, spring accessibility, storm damage content
- **Fix:** Phase 4 predictive content engine

### E5. No testimonial/review content pages
- No dedicated testimonials page
- Only 1 review mentioned in schema (aggregateRating reviewCount: 1)
- **Fix:** Create testimonials section or page; add Review schema

---

## F. IMAGE & PERFORMANCE ISSUES

### F1. All OG images use Unsplash stock photos
- Every page uses the same Unsplash URL for og:image
- Not branded, not unique per page
- **Fix:** Create branded OG images or use service-specific images

### F2. Several favicon files are 0 bytes
- `android-chrome-192x192.png` — 0 bytes
- `favicon-16x16.png` — 0 bytes
- `favicon-32x32.png` — 0 bytes
- `favicon-96x96.png` — 0 bytes
- `favicon.ico` — 0 bytes
- **Impact:** Broken favicons in browsers and search results

### F3. Alt text audit needed
- Service pages use Unsplash URLs inline — alt text may be generic or missing
- **Fix:** Audit all `<img>` tags for descriptive, keyword-rich alt text

---

## G. AUTOMATION OPPORTUNITIES

### G1. Service Area Schema Automation
- Build a single JSON data file with all counties + towns
- Inject into every page's schema automatically
- One source of truth for the entire 100-mile radius

### G2. FAQ Generation & Injection
- Generate 3-5 Q&As per service using Gemini
- Inject as both visible HTML and JSON-LD FAQPage schema
- Template-based so new pages get FAQs automatically

### G3. Landing Page Generator
- Generate "service + town" pages (e.g., "Grab Bar Installation in Columbus NE")
- Template-based, auto-interlinked, auto-added to sitemap
- Could generate 100+ targeted pages from existing service × town matrix

### G4. Schema Automation Script
- Single script that injects/updates schema across all pages
- Reads from centralized data files
- Runs on deploy or manually

### G5. GBP Post Templates
- Auto-generate Google Business Profile posts from service pages + seasonal data
- Include service-area messaging in every post

---

## H. PRIORITY ACTION PLAN

### IMMEDIATE (Phase 2-3, this session):
1. ✅ Build comprehensive service-area data (counties + towns)
2. ✅ Update areaServed schema on ALL 27 pages
3. ✅ Add FAQPage schema to all service pages
4. ✅ Add Service schema to 5 Safety Installs service subpages
5. ✅ Add Review/AggregateRating to service pages
6. ✅ Add "100-mile radius / no job too far" messaging
7. ✅ Add internal cross-links between related services
8. ✅ Update sitemap.xml dates

### SHORT-TERM (Phase 4, next session):
1. Landing page generator script
2. GBP post automation templates
3. Competitor keyword integration
4. Social media content templates

### MEDIUM-TERM (Phase 5-7):
1. Background AI worker configuration
2. Predictive content engine
3. Cron scheduling system
4. Bid generator service-area enhancements

---

## I. TECHNICAL CONSTRAINTS

### GitHub Pages Limitations:
- **No server-side execution** — no cron jobs, no Node.js, no Python scripts running on the server
- **No database** — Firebase is client-side only
- **No dynamic routing** — all pages must be static HTML files
- **No server-side redirects** — must use meta refresh or JS redirects

### Automation Workarounds:
- **GitHub Actions** — can run scheduled workflows (cron) to generate/deploy content
- **Firebase Cloud Functions** — can run background tasks (GBP posts, content generation)
- **Cloudflare Workers** — can handle edge logic (redirects, A/B testing)
- **Local scripts** — can run locally or in CI/CD to generate static pages

---

*End of Phase 1 Report*
