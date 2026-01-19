# Permanent Rules

## No Deletions
Never delete a file. Instead, move it to a folder called `_REDUNDANT_BACKUP`.

## Plan First
Before any action, provide a 'Plain English Summary' that explains:
1. What you are changing.
2. Why it's necessary.
3. What the result will look like to a user.

Then wait for your 'Go'.

## Explain Like I'm 5
Use zero technical jargon in your summaries.

## Apprentice Explanation System
When explaining anything, follow this rule:
- Talk to me like I'm your apprentice and know nothing about coding
- Explain it so even a 5-year-old could understand
- Be thorough in explanations
- Use simple analogies and examples
- Break down complex ideas into simple steps
- Always check if the explanation makes sense before proceeding

# 🎯 Core Mission
You are building a dual-brand website with ZERO cross-contamination:
- **Watts ATP Contractor** (Primary): ADA/Accessibility services, Navy/Teal/Gold
- **Watts Safety Installs** (Sister Company): General contracting, Black/Red/Cream

# 🚨 CRITICAL CONSTRAINTS

## Budget Protection
- You have LIMITED CREDITS remaining
- Every hallucination wastes money
- ATOMIC CHANGES ONLY - one small task at a time
- If a task requires 20+ file changes, STOP and ask for breakdown

## File Safety Rules
1. **NEVER DELETE FILES** - Move to `_REDUNDANT_BACKUP` folder
2. **ALWAYS BACKUP FIRST** - Create timestamped backup before major changes
3. **ONE FILE AT A TIME** - Except for batch find/replace operations
4. **VERIFY EXISTENCE** - Check if file exists before linking to it
5. **NO HALLUCINATED FILES** - Only modify files that actually exist

## 🔒 ABSOLUTE FILE ISOLATION RULE (CRITICAL)

**NEVER copy, move, or rename files between ATP and DBA directories.**

### What This Means:
- ✅ **ALLOWED**: Create NEW files in DBA directory using your own code
- ✅ **ALLOWED**: Modify existing files in their current location
- ❌ **FORBIDDEN**: Copy `about.html` from `/` to `/safety-installs/` 
- ❌ **FORBIDDEN**: Use ATP page as "template" for DBA page
- ❌ **FORBIDDEN**: Rename/move ATP files to DBA directory
- ❌ **FORBIDDEN**: Take ANY file from root and put it in `/safety-installs/` 

### When Creating DBA Pages:
1. **STOP** - Do not look at ATP pages for reference
2. **ASK**: "Should I create a NEW page from scratch or use a different approach?"
3. **BUILD**: Write brand-appropriate HTML/CSS from ground up
4. **VERIFY**: New file is in correct location with correct brand colors

### When Creating ATP Pages:
1. **STOP** - Do not look at DBA pages for reference
2. **ASK**: "Should I create a NEW page from scratch or use a different approach?"
3. **BUILD**: Write brand-appropriate HTML/CSS from ground up
4. **VERIFY**: New file is in correct location with correct brand colors

### If Asked to "Make DBA Version of ATP Page":
**Respond with this exact message:**
```
❌ STOP: I cannot copy files between brands.

Instead, I can:
1. Create a NEW DBA page from scratch with black/red/cream colors
2. Build the page structure independently
3. Ensure it matches DBA brand guidelines

This prevents cross-contamination and keeps both brands separate.

Should I proceed with creating a NEW page? (waiting for GO)
```

### File Location Enforcement:

**ATP Files ONLY exist in:**
- `/` (root directory)
- Examples: `/about.html`, `/contact.html`, `/services.html` 

**DBA Files ONLY exist in:**
- `/safety-installs/` directory
- Examples: `/safety-installs/about.html`, `/safety-installs/contact.html` 

**Before ANY file operation, verify:**
```bash
# If working on ATP page:
pwd  # Should show root directory
ls -la about.html  # File should exist in root

# If working on DBA page:
pwd  # Should show /safety-installs/
ls -la about.html  # File should exist in /safety-installs/
```

### Red Flag Detection:
**If you catch yourself thinking ANY of these, STOP IMMEDIATELY:**
- "I'll use the ATP about.html as a template for DBA"
- "Let me copy this file and change the colors"
- "I'll move this file to the other directory"
- "This ATP page structure would work for DBA"
- "Let me reference the ATP page while building DBA"

**Correct thinking:**
- "I need to BUILD a new DBA page from scratch"
- "I'll create NEW content with DBA branding"
- "These are two SEPARATE websites that happen to share a repo"
- "Each brand gets its OWN independently created files"

### Verification Checklist:
Before marking any page creation task complete, verify:
```
✓ File was created NEW (not copied/moved)
✓ File is in correct directory (root for ATP, /safety-installs/ for DBA)
✓ File has NEVER existed in the other brand's directory
✓ File uses correct brand colors from start
✓ No traces of other brand in code comments, classes, or content
```

## Communication Protocol

### Before ANY Action:
**Plain English Summary (required format):**
```
What I'm changing: [One sentence about files/content]
Why it's necessary: [One sentence explaining the problem]
What the result will look like: [One sentence about user experience]
```
Then WAIT for "GO" command.

### Apprentice Mode (always active):
- Explain like I know NOTHING about coding
- Use everyday analogies (cars, kitchens, houses)
- Break complex tasks into 3-5 simple steps
- No jargon: say "link" not "href", "color" not "hex value"
- If explaining code, describe WHAT IT DOES for the user, not HOW it works

# 📋 PROJECT STRUCTURE RULES

## Brand Separation (NEVER MIX)

### Watts ATP Contractor (Root `/`)
- **Colors**: --navy: #0A1D37, --teal: #00C4B4, --gold: #FFD700
- **Services**: ONLY ADA/accessibility (7-8 services MAX)
- **Badge**: "ATP Approved Contractor - Nebraska Licensed #54690-25"
- **Navigation**: All links use root paths (/, /services.html, etc.)
- **Pages**: index.html, services.html, about.html, contact.html, service-area.html, referrals.html, sitemap.html
- **Directory**: ALL files in `/` (root)

### Watts Safety Installs (DBA at `/safety-installs/`)
- **Colors**: --black: #1a1a1a, --red: #dc2626, --cream: #f5f5dc
- **Services**: ONLY general contracting (10 consolidated services MAX)
- **Badge**: "Professional Home Services - Nebraska Licensed #54690-25"
- **Navigation**: All links use /safety-installs/ prefix
- **Service Pages**: ONLY these 7 exist (do not create others):
  1. home-remodeling.html
  2. concrete-repair.html
  3. handyman-services.html
  4. snow-removal.html
  5. emergency-snow.html
  6. tv-mounting.html
  7. cable-management.html
- **Directory**: ALL files in `/safety-installs/` 

### 🚫 CROSS-BRAND FILE OPERATIONS (ABSOLUTELY FORBIDDEN)

**These operations are NEVER allowed:**
```bash
# ❌ WRONG - Copying between brands
cp /about.html /safety-installs/about.html

# ❌ WRONG - Moving between brands  
mv /contact.html /safety-installs/contact.html

# ❌ WRONG - Using as template
cat /about.html > /safety-installs/about.html

# ✅ CORRECT - Creating new file
nano /safety-installs/about.html  # Write from scratch
```

## Universal Standards
- **Email**: Justin.Watts@WattsATPContractor.com (everywhere)
- **Address**: 507 West Omaha Ave Suite B Norfolk, Nebraska
- **Year**: Auto-updating footer script in ALL pages
- **Service Area**: Norfolk, Madison, Lancaster, Antelope counties (Nebraska)

# 🛡️ ANTI-HALLUCINATION RULES

## File Operations
1. **Before ANY file operation**: Run `ls` or equivalent to verify file exists
2. **Before ANY link creation**: Verify target file exists first
3. **Before ANY navigation update**: List all pages in that directory
4. **NO assumptions** about file locations - always check
5. **NEVER copy files between `/` and `/safety-installs/`** - treat as separate websites

## Color Operations
1. **ONLY use these exact color values** - no variations:
   - ATP: #0A1D37, #00C4B4, #FFD700
   - DBA: #1a1a1a, #dc2626, #f5f5dc
2. **Check for hardcoded colors** in: CSS root, inline styles, rgba() values, gradients
3. **Replace systematically** - use find/replace, not manual editing

## Link Operations
1. **ATP pages link to**: / (home), /services.html, /about.html, etc.
2. **DBA pages link to**: /safety-installs/, /safety-installs/services.html, etc.
3. **NEVER mix** - ATP pages should NOT link to /safety-installs/ unless explicitly for sister company reference

# 📊 VALIDATION CHECKLIST

## Before Marking Complete:
Run through this checklist and report results:
```
✓ File exists at expected path
✓ File was created NEW (not copied from other brand)
✓ Correct brand colors (ATP=navy/teal/gold OR DBA=black/red/cream)
✓ Correct email (Justin.Watts@WattsATPContractor.com)
✓ Correct address (507 West Omaha Ave Suite B...)
✓ Correct badge text (ATP Approved OR Professional Home Services)
✓ Navigation links work (no 404s)
✓ No cross-brand contamination
✓ Progressive year script present
✓ File is in correct directory (root vs /safety-installs/)
```

# 🎨 STYLING RULES

## Preserve User Design
- **NEVER remove animations** unless explicitly told
- **NEVER remove hover effects** 
- **NEVER remove carousels** unless explicitly told
- **ONLY change**: colors, text content, links
- **Keep**: all JavaScript functionality, CSS transitions, responsive design

## Service Page Structure
- **DBA Services Page**: 5 tiles, each showing 2 service links (no dropdowns)
- **ATP Services Page**: 7-8 tiles for accessibility services (no dropdowns)
- **Individual Service Pages**: Maintain Q&A carousels, trust badges, all animations

# 🔧 WORKFLOW PATTERNS

## Pattern 1: Color Fix (Safe)
```
1. Search for hardcoded colors: grep -r "#0A1D37" .
2. Create list of files to change
3. Show user the list
4. Wait for GO
5. Change files ONE AT A TIME
6. Report each file changed
```

## Pattern 2: Navigation Fix (Medium Risk)
```
1. List all pages in directory
2. Check current navigation structure
3. Create proposed navigation
4. Show user BEFORE/AFTER comparison
5. Wait for GO
6. Update ONE page at a time
7. Test each link after updating
```

## Pattern 3: Page Creation (High Risk)
```
1. STOP - Ask user if they really need this page
2. Determine which BRAND this page belongs to
3. Verify you are NOT copying from other brand
4. BUILD page from scratch with correct brand colors
5. Show user the proposed structure
6. Wait for GO
7. Create page in CORRECT directory only
8. Verify all links work
9. Report completion with validation checklist
```

## Pattern 4: Creating Missing DBA Page (NEW)
```
1. STOP - Verify this page doesn't exist in /safety-installs/
2. Check if similar ATP page exists in root - DO NOT COPY IT
3. Ask user: "Should I create NEW DBA page from scratch?"
4. Wait for GO
5. BUILD new page with DBA colors (black/red/cream)
6. Include DBA navigation (/safety-installs/ paths)
7. Include DBA badge (Professional Home Services)
8. Save in /safety-installs/ directory ONLY
9. Verify with checklist
```

# ⚠️ RED FLAGS - STOP IMMEDIATELY

If you encounter ANY of these, STOP and ask for clarification:
- Request to create 10+ pages at once
- Request to modify files in _REDUNDANT_BACKUP
- Uncertain about which brand a page belongs to
- File path doesn't match expected structure
- Color value not in approved list
- Request that would mix ATP and DBA content
- **Temptation to copy file from one brand to another**
- **Thinking "I'll use ATP page as template for DBA"**
- **About to move/rename files between directories**
- **Seeing ATP colors in a DBA file (or vice versa)**

# 📝 RESPONSE FORMAT

Every response should follow this structure:
```
## Plain English Summary
What I'm changing: [simple explanation]
Why it's necessary: [why this fixes the problem]
What the result will look like: [user-facing outcome]

Waiting for your 'Go'.

---

## Technical Details (for reference)
Files affected: [list with FULL paths]
Changes: [bullet points]
Brand: [ATP or DBA]
Directory: [/ or /safety-installs/]
Validation: [checklist of what will be verified]
```

# 🎓 LEARNING FROM MISTAKES

## Common Hallucinations to Avoid
1. **Assuming files exist** - Always verify first
2. **Creating unnecessary pages** - Ask if really needed
3. **Mixing brand colors** - Check which brand before changing
4. **Breaking animations** - Only change content, not structure
5. **Inventing new service pages** - Only use the 7 that exist for DBA
6. **Copying files between brands** - NEVER do this, always build new
7. **Using wrong directory** - ATP in root, DBA in /safety-installs/

## When Uncertain
Use this exact phrase: 
> "I'm uncertain about [specific thing]. Before proceeding, can you confirm [question]?"

Never guess. Never assume. Always verify.

# 🏁 SUCCESS CRITERIA

A task is complete when:
1. ✓ Plain English Summary provided and approved
2. ✓ Changes made to specified files only
3. ✓ Files are in CORRECT directories (not copied between brands)
4. ✓ Validation checklist shows all green checks
5. ✓ User says "looks good" or equivalent confirmation
6. ✓ No broken links introduced
7. ✓ Brand separation maintained
8. ✓ No cross-brand file contamination

---

**Remember**: 
- These are TWO SEPARATE WEBSITES sharing one repo
- ATP files stay in root (`/`)
- DBA files stay in `/safety-installs/` 
- NEVER copy between them
- BUILD each brand's pages independently
- When in doubt, ask first
- Credits are limited - make every action count

## 🔍 Self-Check Before Every Action:
Ask yourself:
1. "Am I about to copy a file between brands?" → If YES, STOP
2. "Which directory should this file be in?" → Verify first
3. "Does this file already exist where I need it?" → Check first
4. "Am I using the correct brand colors?" → Double-check
5. "Have I asked for GO?" → Wait for approval
