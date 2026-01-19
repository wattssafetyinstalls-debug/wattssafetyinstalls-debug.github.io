# WATTS ATP CONTRACTOR → WATTS SAFETY INSTALLS DBA RESTRUCTURE

## OBJECTIVE
Create a complete, fully functional embedded DBA website at `/safety-installs/` that mirrors the main Watts ATP Contractor site structure but serves non-safety services with distinct black/red/cream branding.

---

## SERVICE CATEGORIZATION

### ATP Services (Keep on Main Site - Safety/Accessibility Only)
**Path: `/services/[service-name]/`**

1. accessibility-safety-solutions
2. ada-compliant-showers
3. ada-compliant-showers-bathrooms
4. bathroom-accessibility
5. custom-ramps
6. grab-bar-installation
7. grab-bars
8. non-slip-flooring
9. non-slip-flooring-solutions
10. senior-safety
11. stairlift-installation
12. walk-in-tubs
13. wheelchair-ramps

### DBA Services (Move to `/safety-installs/services/[service-name]/`)
**All non-safety services - 31+ services:**

1. audio-visual
2. basement-finishing
3. bathroom-remodels
4. cabinet-refacing
5. cable-management
6. concrete-pouring
7. concrete-repair
8. countertop-repair
9. custom-cabinets
10. custom-storage
11. deck-construction
12. driveway-installation
13. drywall-repair
14. emergency-repairs
15. emergency-snow
16. fence-installation
17. fence-repair
18. fertilization
19. floor-refinishing
20. flooring-installation
21. garden-maintenance
22. gutter-cleaning
23. handyman-repair-services
24. handyman-services
25. hardwood-flooring
26. home-audio
27. home-remodeling
28. home-remodeling-renovation
29. home-theater-installation
30. kitchen-cabinetry
31. kitchen-renovations
32. landscape-design
33. lawn-maintenance
34. onyx-countertops
35. painting-services
36. patio-construction
37. pressure-washing
38. projector-install
39. room-additions
40. seasonal-cleanup
41. siding-replacement
42. smart-audio
43. snow-removal
44. soundbar-setup
45. tile-installation
46. tree-trimming
47. tv-mounting
48. window-doors

---

## PHASE-BY-PHASE IMPLEMENTATION

### PHASE 1: Update Main Site `/services.html`

**Goal:** Remove all DBA service tiles, keep only ATP services

**Actions:**
1. Read `/services.html` completely
2. Identify all service tile sections
3. Remove tiles for all DBA services listed above
4. Keep only ATP service tiles (13 services)
5. Add prominent banner at top: "Looking for TV mounting, snow removal, lawn care, or home remodeling? Visit our home services division: [Watts Safety Installs](/safety-installs/)"
6. Update page title/description to focus on ATP services only
7. Ensure all remaining tiles link to `/services/[atp-service]/`

### PHASE 2: Create DBA Homepage `/safety-installs/index.html`

**Goal:** Complete homepage matching main site structure with DBA branding

**Structure to Match:** `/index.html`

**Required Sections:**
1. **Header/Navigation**
   - Logo: "WATTS SAFETY INSTALLS"
   - Nav links: Home | Services | About | Contact | [Link to ATP Contractor]
   - Phone CTA button
   - Black/red/cream color scheme

2. **Hero Section**
   - Headline: "Watts Safety Installs - Your Complete Home Services Partner"
   - Subheadline: "Professional TV mounting, snow removal, lawn care, home remodeling, and property maintenance in Norfolk, NE"
   - Background image (home services themed)
   - CTA: "Explore Our Services" → `/safety-installs/services.html`

3. **Trust Bar**
   - DBA of Watts ATP Contractor
   - Nebraska Reg #54690-25
   - Fully Insured $1M
   - 75-Mile Service Area

4. **Services Preview** (4-6 featured services)
   - TV Mounting & Home Theater
   - Snow Removal & Winter Services
   - Lawn Care & Landscaping
   - Home Remodeling & Improvements
   - Each with image, description, "Learn More" CTA

5. **About Preview**
   - Brief about DBA relationship
   - "Learn More About Us" → `/safety-installs/about.html`

6. **Service Area Section**
   - Map showing Norfolk, NE coverage
   - 75-mile radius information

7. **CTA Section**
   - "Ready to Transform Your Home?"
   - Phone: (405) 410-6402
   - Email: Justin.Watts@WattsATPContractor.com

8. **Footer**
   - Company info with DBA status
   - Quick links to services
   - Contact information
   - Link back to Watts ATP Contractor
   - Compliance: Nebraska Reg #54690-25 • Fully Insured $1M

**Color Scheme:**
```css
:root {
    --primary: #dc2626;      /* Red */
    --secondary: #fef3c7;    /* Cream */
    --dark: #0a0a0a;         /* Black */
    --medium: #1a1a1a;       /* Dark gray */
    --light: #f5f5f5;        /* Off-white */
    --text: #d1d5db;         /* Light gray text */
}
```

### PHASE 3: Create DBA Services Page `/safety-installs/services.html`

**Goal:** Full services directory with service tiles grid

**Structure to Match:** `/services.html` (but with DBA services only)

**Required Elements:**
1. **Hero Section**
   - "Our Home Services"
   - Description of comprehensive offerings

2. **Service Tiles Grid** (31+ services)
   - Each tile includes:
     - Service image
     - Service title
     - Brief description
     - Dropdown with sub-services (if applicable)
     - "Get Free Quote" CTA
     - Links to `/safety-installs/services/[service-name]/`

3. **Service Categories:**
   - **Entertainment & Technology**
     - TV Mounting
     - Home Theater Installation
     - Audio/Visual Systems
     - Cable Management
   
   - **Outdoor Services**
     - Snow Removal
     - Lawn Maintenance
     - Landscape Design
     - Garden Maintenance
     - Tree Trimming
   
   - **Home Improvement**
     - Kitchen Renovations
     - Bathroom Remodels
     - Basement Finishing
     - Room Additions
   
   - **Property Maintenance**
     - Handyman Services
     - Emergency Repairs
     - Gutter Cleaning
     - Pressure Washing

4. **Same carousel/animation functionality** as main site
5. **Black/red/cream color scheme** throughout
6. **Mobile responsive** with touch-optimized tiles

### PHASE 4: Create DBA About Page `/safety-installs/about.html`

**Goal:** Complete about page matching ATP structure

**Structure to Match:** `/about.html`

**Required Sections:**
1. **Hero**
   - "About Watts Safety Installs"
   - DBA relationship explanation

2. **Company Story**
   - Operating as DBA of Watts ATP Contractor
   - Same owner, same quality standards
   - Comprehensive home services focus

3. **Services Overview**
   - What makes DBA different from ATP division
   - Full range of non-safety services

4. **Credentials**
   - Nebraska Reg #54690-25
   - Fully Insured $1M
   - Licensed & bonded

5. **Service Area**
   - Map with 75-mile radius
   - Cities/areas served

6. **Why Choose Us**
   - Free estimates
   - Licensed & insured
   - Senior & veteran discounts
   - Emergency services available

### PHASE 5: Create DBA Contact Page `/safety-installs/contact.html`

**Goal:** Functional contact page with DBA branding

**Structure to Match:** `/contact.html`

**Required Elements:**
1. Contact form (same functionality)
2. Contact information
3. Business hours
4. Embedded map
5. FAQ section (DBA-specific)
6. Black/red/cream styling

### PHASE 6: Rebrand All DBA Service Detail Pages

**Goal:** Copy and rebrand 31+ service pages from `/services/` to `/safety-installs/services/`

**For EACH DBA service:**

1. **Copy Structure** from `/services/[service-name]/index.html`
2. **Apply DBA Branding:**
   - Update all color variables to black/red/cream
   - Change "Watts ATP Contractor" → "Watts Safety Installs"
   - Add "DBA of Watts ATP Contractor" in footer
   - Update logo and header
   
3. **Update Navigation:**
   - Header nav links to DBA pages
   - Breadcrumbs: Home > Services > [Service Name]
   - All paths use `/safety-installs/` prefix

4. **Update Content:**
   - Keep service descriptions
   - Update branding references
   - Update contact CTAs to DBA contact

5. **Update SEO:**
   - Title: "[Service] | Watts Safety Installs | Norfolk, NE"
   - Meta description with DBA branding
   - Canonical URL: `https://wattsatpcontractor.com/safety-installs/services/[service-name]/`
   - Structured data for DBA entity

6. **Update Related Services:**
   - Link to other DBA services
   - Remove ATP service links

### PHASE 7: Update Redirect System

**Goal:** Seamless redirects from old paths to new DBA paths

**Files to Update:**

1. **`pretty_urls.json`**
   ```json
   {
     "/services/tv-mounting": "/safety-installs/services/tv-mounting/",
     "/services/snow-removal": "/safety-installs/services/snow-removal/",
     "/services/lawn-maintenance": "/safety-installs/services/lawn-maintenance/",
     [... all 31+ DBA services ...]
   }
   ```

2. **`_includes/redirect-handler.html`**
   - Add redirect logic for DBA service paths
   - Handle clean URLs for DBA services
   - Preserve query parameters

3. **`404.html`**
   - Add DBA service redirect logic
   - Suggest DBA services if ATP service not found

### PHASE 8: Cross-Site Navigation

**Goal:** Clear navigation between both entities

**Main Site Updates:**
1. Add "Watts Safety Installs" to main navigation
2. Add DBA link in footer
3. Service tiles for DBA services redirect to `/safety-installs/services/`
4. Banner on services page directing to DBA

**DBA Site Updates:**
1. Add "Watts ATP Contractor" to DBA navigation
2. Add ATP link in footer
3. Banner: "Looking for accessibility services? Visit Watts ATP Contractor"

### PHASE 9: SEO & Meta Updates

**For ALL DBA pages:**

1. **Page Titles:**
   - Format: "[Page/Service] | Watts Safety Installs | Norfolk, NE"

2. **Meta Descriptions:**
   - Include "Watts Safety Installs"
   - Mention DBA relationship
   - Include service area

3. **Structured Data (JSON-LD):**
   ```json
   {
     "@context": "https://schema.org",
     "@type": "HomeAndConstructionBusiness",
     "name": "Watts Safety Installs",
     "alternateName": "Watts ATP Contractor DBA",
     "url": "https://wattsatpcontractor.com/safety-installs/",
     "telephone": "+14054106402",
     "email": "Justin.Watts@WattsATPContractor.com",
     "address": {
       "@type": "PostalAddress",
       "streetAddress": "507 W Omaha Ave Suite B",
       "addressLocality": "Norfolk",
       "addressRegion": "NE",
       "postalCode": "68701"
     }
   }
   ```

4. **Canonical URLs:**
   - All DBA pages: `https://wattsatpcontractor.com/safety-installs/[path]`

5. **Open Graph Tags:**
   - Update for DBA branding
   - Proper social sharing

### PHASE 10: Quality Assurance

**Testing Checklist:**

- [ ] All ATP service tiles on main site link correctly
- [ ] All DBA service tiles redirect to `/safety-installs/services/`
- [ ] DBA homepage loads with proper styling
- [ ] DBA services page shows all 31+ services
- [ ] DBA about page matches structure
- [ ] DBA contact form works
- [ ] All 31+ DBA service detail pages load
- [ ] Black/red/cream colors applied consistently
- [ ] Navigation works between both sites
- [ ] Mobile responsiveness on both sites
- [ ] All redirects work (test old URLs)
- [ ] No broken links
- [ ] SEO meta tags correct
- [ ] Structured data validates
- [ ] Forms submit correctly
- [ ] Phone/email links work

---

## CRITICAL REQUIREMENTS

1. **NO NEW FILES** - Only modify existing structure
2. **IDENTICAL FUNCTIONALITY** - DBA site must work exactly like ATP site
3. **COMPLETE SEPARATION** - Two distinct visual identities
4. **SEAMLESS NAVIGATION** - Easy movement between both sites
5. **MAINTAIN SEO** - Proper redirects and canonical URLs
6. **MOBILE FIRST** - Both sites must be fully responsive
7. **BRAND CONSISTENCY** - Each site maintains its own branding throughout

---

## SUCCESS CRITERIA

✅ Main site `/services.html` shows only ATP services (13 services)
✅ DBA site has complete homepage with hero, services preview, about preview
✅ DBA site has full services page with 31+ service tiles
✅ DBA site has complete about page
✅ DBA site has functional contact page
✅ All 31+ DBA service detail pages are rebranded
✅ All redirects work properly
✅ Both sites feel like completely separate entities
✅ Identical functionality maintained
✅ Clear navigation between both sites
✅ Mobile responsiveness perfect on both
✅ SEO value preserved

---

## EXECUTION NOTES

- Work systematically through each phase
- Test after each major change
- Keep backups of modified files
- Document any issues encountered
- Verify color schemes are correct throughout
- Ensure all links are updated
- Check mobile responsiveness frequently

---

**This document provides complete instructions for restructuring the Watts ATP Contractor website to properly separate ATP services from DBA services under Watts Safety Installs.**
