/**
 * BidGen Quick Templates — 42 pre-built job templates
 * Searchable, categorized, with scope/notes/scopeTitle for full auto-fill.
 * AI Smart Fill uses Gemini 2.5 Pro for custom job descriptions.
 */

const JOB_TEMPLATES = {
    // ── ACCESSIBILITY / ATP ──────────────────────────────────────────
    grab_bar_install: {
        label: 'Grab Bar Installation', cat: 'Accessibility / ATP', tags: ['grab bar','ada','bathroom','safety','atp','accessibility'],
        trade: 'general', areaDesc: 'Bathroom', sqft: 48, markup: 20,
        scopeTitle: 'ADA Grab Bar Installation',
        scope: ['Install ADA-compliant grab bars at specified locations','Locate wall studs and install wood blocking where needed','Patch and finish any drywall disturbance','Final inspection and function test per ADA standards'],
        notes: ['All grab bars rated for 250 lb static load per ADA','Mounting into solid wood backing or steel plate behind drywall'],
        labor: [
            { desc: 'Wall stud location & blocking', basis: '1 lot', price: 45 },
            { desc: 'Grab bar mounting (per bar)', basis: 'per unit', price: 35 },
            { desc: 'Drywall patching (if needed)', basis: '1 lot', price: 30 },
            { desc: 'Cleanup & inspection', basis: '1 lot', price: 20 }
        ],
        materials: [
            { desc: 'Stainless Steel Grab Bar 18"', qty: '2', price: 28 },
            { desc: 'Stainless Steel Grab Bar 36"', qty: '1', price: 42 },
            { desc: 'Wood Blocking / Backing Board', qty: '1 lot', price: 12 },
            { desc: 'Stainless Mounting Hardware', qty: '1 lot', price: 15 },
            { desc: 'Drywall Patch Kit', qty: '1', price: 12 }
        ],
        disclaimer: 'Wall conditions behind tile or drywall cannot be assessed until access is gained. If studs are not present at required locations, additional blocking or reinforcement may be needed. Contractor shall provide written notice and a Change Order before proceeding.'
    },
    grab_bar_shower: {
        label: 'Grab Bars — Shower/Tub Combo', cat: 'Accessibility / ATP', tags: ['grab bar','shower','tub','ada','tile','atp','bathroom'],
        trade: 'general', areaDesc: 'Bathroom — Shower/Tub', sqft: 48, markup: 20,
        scopeTitle: 'Shower/Tub Grab Bar Installation',
        scope: ['Install grab bars inside tub/shower surround','Drill through tile and mount into blocking','Seal all penetrations with silicone','Test load rating and verify ADA placement'],
        notes: ['Tile penetration requires diamond-tip bit','Silicone sealant at every screw to prevent water intrusion'],
        labor: [
            { desc: 'Tile drilling & stud/blocking location', basis: '1 lot', price: 55 },
            { desc: 'Grab bar mounting through tile (per bar)', basis: 'per unit', price: 45 },
            { desc: 'Silicone sealing all penetrations', basis: '1 lot', price: 20 },
            { desc: 'Cleanup & load test', basis: '1 lot', price: 20 }
        ],
        materials: [
            { desc: 'ADA Grab Bar 16" (vertical)', qty: '1', price: 28 },
            { desc: 'ADA Grab Bar 24" (horizontal)', qty: '1', price: 35 },
            { desc: 'ADA Grab Bar 36" (angled/L-shape)', qty: '1', price: 55 },
            { desc: 'Diamond Drill Bit Set', qty: '1', price: 18 },
            { desc: 'Silicone Sealant (clear)', qty: '1', price: 8 },
            { desc: 'Stainless Mounting Hardware', qty: '1 lot', price: 15 }
        ],
        disclaimer: 'Tile and wall conditions behind shower surround cannot be assessed until drilling begins. Cracked tile, missing backing, water damage, or mold behind walls may be discovered.'
    },
    ada_ramp: {
        label: 'ADA Wheelchair Ramp', cat: 'Accessibility / ATP', tags: ['ramp','wheelchair','ada','exterior','entry','atp','accessibility','entrance'],
        trade: 'general', areaDesc: 'Exterior Entry', sqft: 120, markup: 20,
        scopeTitle: 'ADA Wheelchair Ramp Construction',
        scope: ['Construct ADA-compliant wheelchair ramp (1:12 slope max)','Install 60x60 landing platforms at top and bottom','Install continuous handrails both sides per ADA','Non-slip surface treatment on all walking surfaces'],
        notes: ['Ramp width minimum 36" clear between handrails','Handrails 34-38" height, continuous, with extensions'],
        labor: [
            { desc: 'Site prep & layout', basis: '1 lot', price: 150 },
            { desc: 'Foundation / post setting', basis: '1 lot', price: 200 },
            { desc: 'Ramp framing & decking', basis: 'per sq ft', price: 8 },
            { desc: 'Handrail installation', basis: '1 lot', price: 175 },
            { desc: 'Landing platform', basis: '1 lot', price: 125 },
            { desc: 'Final inspection & cleanup', basis: '1 lot', price: 50 }
        ],
        materials: [
            { desc: 'Pressure-Treated Lumber (framing)', qty: '1 lot', price: 280 },
            { desc: 'Composite Decking Boards', qty: '1 lot', price: 350 },
            { desc: 'Aluminum Handrails', qty: '2', price: 120 },
            { desc: 'Concrete / Post Anchors', qty: '1 lot', price: 65 },
            { desc: 'Hardware / Fasteners', qty: '1 lot', price: 45 },
            { desc: 'Non-Slip Surface Strips', qty: '1 lot', price: 30 }
        ],
        disclaimer: 'Ground conditions, slope grade, and soil composition cannot be fully assessed until excavation begins. Frost depth, drainage issues, or underground utilities may require design modifications. All work per ADA guidelines and local building code.'
    },
    portable_ramp: {
        label: 'Portable/Modular Ramp Install', cat: 'Accessibility / ATP', tags: ['ramp','portable','modular','aluminum','ada','atp','threshold'],
        trade: 'general', areaDesc: 'Exterior Entry', sqft: 60, markup: 15,
        scopeTitle: 'Portable Aluminum Ramp Installation',
        scope: ['Install pre-fabricated modular aluminum ramp system','Level and secure ramp to entry threshold','Adjust handrails and verify ADA slope compliance'],
        notes: ['Modular ramp can be relocated if client moves','No permanent modification to structure required'],
        labor: [
            { desc: 'Site assessment & measurements', basis: '1 lot', price: 60 },
            { desc: 'Ramp assembly & installation', basis: '1 lot', price: 150 },
            { desc: 'Leveling & anchoring', basis: '1 lot', price: 75 },
            { desc: 'Threshold transition plate', basis: '1 lot', price: 35 },
            { desc: 'Final inspection', basis: '1 lot', price: 25 }
        ],
        materials: [
            { desc: 'Modular Aluminum Ramp Kit', qty: '1', price: 800 },
            { desc: 'Threshold Plate', qty: '1', price: 45 },
            { desc: 'Ground Anchors / Stakes', qty: '4', price: 8 },
            { desc: 'Leveling Shims', qty: '1 lot', price: 15 }
        ],
        disclaimer: 'Ground surface must be level and stable. Soft soil, drainage issues, or uneven concrete may require additional site preparation.'
    },
    walk_in_shower: {
        label: 'Walk-In Shower Conversion', cat: 'Accessibility / ATP', tags: ['shower','tub','conversion','ada','bathroom','walk-in','barrier free','atp','plumbing'],
        trade: 'plumbing', areaDesc: 'Bathroom', sqft: 48, markup: 20,
        scopeTitle: 'Tub-to-Walk-In Shower Conversion',
        scope: ['Demolish existing tub/shower assembly','Reroute plumbing for barrier-free shower pan','Install walk-in shower pan (zero/low threshold)','Install shower surround or tile','Install ADA fixtures: handheld showerhead, grab bars, fold-down seat'],
        notes: ['Barrier-free design for wheelchair/walker access','Handheld showerhead on adjustable slide bar','Fold-down shower seat rated for 250 lbs'],
        labor: [
            { desc: 'Demolition of existing tub/shower', basis: '1 lot', price: 250 },
            { desc: 'Plumbing rough-in / reroute', basis: '1 lot', price: 300 },
            { desc: 'Shower pan installation', basis: '1 lot', price: 200 },
            { desc: 'Tile / surround installation', basis: '1 lot', price: 400 },
            { desc: 'Fixture installation', basis: '1 lot', price: 150 },
            { desc: 'Grab bar installation', basis: '1 lot', price: 75 },
            { desc: 'Cleanup & haul-away', basis: '1 lot', price: 100 }
        ],
        materials: [
            { desc: 'Walk-In Shower Pan (barrier-free)', qty: '1', price: 350 },
            { desc: 'Shower Surround / Tile', qty: '1 lot', price: 280 },
            { desc: 'Shower Valve & Trim Kit', qty: '1', price: 120 },
            { desc: 'Handheld Shower Head w/ Slide Bar', qty: '1', price: 65 },
            { desc: 'ADA Grab Bars', qty: '2', price: 35 },
            { desc: 'Fold-Down Shower Seat', qty: '1', price: 85 },
            { desc: 'Waterproofing Membrane', qty: '1 lot', price: 45 },
            { desc: 'PEX / Fittings', qty: '1 lot', price: 40 },
            { desc: 'Drain Assembly', qty: '1', price: 30 }
        ],
        disclaimer: 'Plumbing and structural conditions behind walls and under floors cannot be assessed until demolition. Corroded pipes, water damage, or inadequate subfloor may be discovered.'
    },
    stairlift: {
        label: 'Stairlift Installation (Straight)', cat: 'Accessibility / ATP', tags: ['stairlift','chair lift','stairs','ada','atp','mobility'],
        trade: 'general', areaDesc: 'Stairway', sqft: 30, markup: 15,
        scopeTitle: 'Straight Stairlift Installation',
        scope: ['Install straight-rail stairlift on existing stairway','Mount rail to stair treads (not wall)','Wire dedicated 20A outlet','Program limits and safety sensors','Client training on operation'],
        notes: ['Rail mounts to treads — no structural modification','Stairway must be minimum 28" wide','Battery backup provides 3-5 trips during power outage'],
        labor: [
            { desc: 'Site assessment & rail measurement', basis: '1 lot', price: 75 },
            { desc: 'Rail mounting to stair treads', basis: '1 lot', price: 200 },
            { desc: 'Chair/carriage assembly & mounting', basis: '1 lot', price: 150 },
            { desc: 'Electrical — dedicated outlet install', basis: '1 lot', price: 120 },
            { desc: 'Programming, testing, safety check', basis: '1 lot', price: 75 },
            { desc: 'Client training & cleanup', basis: '1 lot', price: 40 }
        ],
        materials: [
            { desc: 'Stairlift Unit (straight rail)', qty: '1', price: 2800 },
            { desc: '20A Outlet + Wiring', qty: '1 lot', price: 45 },
            { desc: 'Mounting Hardware / Rail Brackets', qty: '1 lot', price: 35 }
        ],
        disclaimer: 'Stairway dimensions, wall clearance, and structural condition of treads cannot be fully confirmed until installation begins. Non-standard stairways may require a curved-rail unit at additional cost.'
    },
    stairlift_curved: {
        label: 'Stairlift Installation (Curved)', cat: 'Accessibility / ATP', tags: ['stairlift','curved','custom','stairs','ada','atp','mobility'],
        trade: 'general', areaDesc: 'Stairway (Curved)', sqft: 30, markup: 15,
        scopeTitle: 'Curved Stairlift Installation',
        scope: ['Custom-measure stairway for curved rail fabrication','Install curved stairlift rail system','Mount chair/carriage and program travel path','Wire dedicated outlet','Client training'],
        notes: ['Curved rail is custom-fabricated — 2-4 week lead time','Chair folds flat when not in use for stair access'],
        labor: [
            { desc: 'Detailed stairway measurement & template', basis: '1 lot', price: 150 },
            { desc: 'Curved rail installation', basis: '1 lot', price: 350 },
            { desc: 'Chair assembly & mounting', basis: '1 lot', price: 200 },
            { desc: 'Electrical — dedicated outlet', basis: '1 lot', price: 120 },
            { desc: 'Programming & safety testing', basis: '1 lot', price: 100 },
            { desc: 'Client training & cleanup', basis: '1 lot', price: 50 }
        ],
        materials: [
            { desc: 'Curved Stairlift Unit (custom rail)', qty: '1', price: 6500 },
            { desc: '20A Outlet + Wiring', qty: '1 lot', price: 45 },
            { desc: 'Custom Mounting Hardware', qty: '1 lot', price: 50 }
        ],
        disclaimer: 'Stairway geometry must be precisely measured for custom rail fabrication. Changes after ordering will incur re-fabrication costs. Lead time typically 2-4 weeks.'
    },
    door_widening: {
        label: 'Doorway Widening (ADA 36")', cat: 'Accessibility / ATP', tags: ['door','widening','ada','wheelchair','36 inch','atp','entrance'],
        trade: 'general', areaDesc: 'Room Interior', sqft: 30, markup: 20,
        scopeTitle: 'ADA Doorway Widening — 36" Clear',
        scope: ['Remove existing door, frame, and trim','Widen rough opening for 36" door','Install new header if load-bearing wall','Install 36" pre-hung door with lever handle','Patch and finish surrounding drywall'],
        notes: ['ADA requires 32" min clear (36" preferred)','Lever handle required (no round knobs per ADA)'],
        labor: [
            { desc: 'Remove existing door, frame & trim', basis: '1 lot', price: 45 },
            { desc: 'Widen rough opening', basis: '1 lot', price: 120 },
            { desc: 'Header installation (if load-bearing)', basis: '1 lot', price: 85 },
            { desc: 'Install 36" pre-hung door', basis: '1 lot', price: 75 },
            { desc: 'Trim, casing & drywall patching', basis: '1 lot', price: 65 },
            { desc: 'Install lever hardware', basis: '1 lot', price: 25 }
        ],
        materials: [
            { desc: '36" Pre-Hung Door', qty: '1', price: 125 },
            { desc: 'Lever Handle Set (ADA)', qty: '1', price: 35 },
            { desc: 'Header Lumber (if needed)', qty: '1 lot', price: 25 },
            { desc: 'Drywall / Patch Material', qty: '1 lot', price: 20 },
            { desc: 'Trim / Casing', qty: '1 lot', price: 30 },
            { desc: 'Paint / Finish', qty: '1 lot', price: 18 }
        ],
        disclaimer: 'Wall structure cannot be assessed until opened. Load-bearing walls require a properly sized header. Electrical, plumbing, or HVAC within the wall may need rerouting.'
    },
    threshold_ramp: {
        label: 'Threshold Ramp / Transition', cat: 'Accessibility / ATP', tags: ['threshold','ramp','transition','ada','door','trip hazard','atp'],
        trade: 'general', areaDesc: 'Doorway / Entry', sqft: 10, markup: 20,
        scopeTitle: 'ADA Threshold Ramp Installation',
        scope: ['Install beveled threshold ramp at doorway(s)','Secure to floor with adhesive or screws','Verify smooth wheelchair/walker transition'],
        notes: ['Thresholds > 1/2" require a ramp per ADA','Rubber, aluminum, or wood options available'],
        labor: [
            { desc: 'Measure threshold differential', basis: '1 lot', price: 25 },
            { desc: 'Install threshold ramp (per location)', basis: 'per unit', price: 35 },
            { desc: 'Secure & test transition', basis: '1 lot', price: 15 }
        ],
        materials: [
            { desc: 'Threshold Ramp (rubber/aluminum)', qty: '2', price: 35 },
            { desc: 'Construction Adhesive', qty: '1', price: 8 },
            { desc: 'Screws / Fasteners', qty: '1 lot', price: 5 }
        ],
        disclaimer: 'Threshold height and floor conditions may vary. Custom sizing may be required for non-standard thresholds.'
    },
    raised_toilet_seat: {
        label: 'Raised Toilet Seat / Safety Rails', cat: 'Accessibility / ATP', tags: ['toilet','raised seat','safety rails','ada','bathroom','atp','comfort height'],
        trade: 'plumbing', areaDesc: 'Bathroom', sqft: 48, markup: 20,
        scopeTitle: 'Raised Toilet Seat & Safety Rail Installation',
        scope: ['Install raised toilet seat or comfort-height toilet','Install toilet safety frame/rails','Verify stability and load rating'],
        notes: ['ADA toilet seat height: 17-19 inches','Safety rails bolt to toilet or floor — no wall mounting needed'],
        labor: [
            { desc: 'Install raised seat / safety frame', basis: '1 lot', price: 40 },
            { desc: 'Stability test & adjustment', basis: '1 lot', price: 15 },
            { desc: 'Cleanup', basis: '1 lot', price: 10 }
        ],
        materials: [
            { desc: 'Raised Toilet Seat (4" rise)', qty: '1', price: 45 },
            { desc: 'Toilet Safety Frame w/ Rails', qty: '1', price: 55 },
            { desc: 'Mounting Hardware', qty: '1 lot', price: 8 }
        ],
        disclaimer: 'Existing toilet condition and floor stability cannot be fully assessed until work begins. Loose bolts, damaged flanges, or unstable flooring may require additional repair.'
    },
    non_slip_flooring: {
        label: 'Non-Slip Surface Treatment', cat: 'Accessibility / ATP', tags: ['non-slip','flooring','safety','ada','atp','slip resistant','bathroom'],
        trade: 'flooring', areaDesc: 'Bathroom / Entry', sqft: 48, markup: 20,
        scopeTitle: 'Non-Slip Surface Treatment',
        scope: ['Apply non-slip coating or install non-slip flooring','Treat tub/shower floor with anti-slip coating','Install non-slip adhesive strips'],
        notes: ['ADA requires slip-resistant surfaces in wet areas','Anti-slip coating is invisible, does not change appearance'],
        labor: [
            { desc: 'Surface cleaning & preparation', basis: '1 lot', price: 35 },
            { desc: 'Anti-slip coating application', basis: 'per sq ft', price: 2.50 },
            { desc: 'Adhesive strip installation', basis: '1 lot', price: 25 },
            { desc: 'Dry time & verification', basis: '1 lot', price: 15 }
        ],
        materials: [
            { desc: 'Anti-Slip Floor Coating', qty: '1', price: 45 },
            { desc: 'Non-Slip Adhesive Strips', qty: '10', price: 3 },
            { desc: 'Surface Cleaner / Prep', qty: '1', price: 12 }
        ],
        disclaimer: 'Surface porosity and condition affect coating adhesion. Some surfaces may require mechanical etching.'
    },
    handheld_showerhead: {
        label: 'Handheld Showerhead w/ Slide Bar', cat: 'Accessibility / ATP', tags: ['showerhead','handheld','slide bar','ada','bathroom','atp','shower'],
        trade: 'plumbing', areaDesc: 'Bathroom', sqft: 48, markup: 20,
        scopeTitle: 'ADA Handheld Showerhead Installation',
        scope: ['Remove existing showerhead','Install adjustable slide bar','Mount handheld showerhead','Test water flow and connections'],
        notes: ['Slide bar allows seated or standing use','Hose length 60-72" for wheelchair access'],
        labor: [
            { desc: 'Remove existing showerhead', basis: '1 lot', price: 15 },
            { desc: 'Install slide bar & mount', basis: '1 lot', price: 40 },
            { desc: 'Connect handheld unit & test', basis: '1 lot', price: 20 }
        ],
        materials: [
            { desc: 'Handheld Showerhead w/ 60" Hose', qty: '1', price: 45 },
            { desc: 'Adjustable Slide Bar (24-30")', qty: '1', price: 35 },
            { desc: 'Teflon Tape / Thread Sealant', qty: '1', price: 4 }
        ],
        disclaimer: 'Existing shower plumbing connections may be corroded or non-standard. If shower arm or valve needs replacement, additional work will be required.'
    },
    stair_rail: {
        label: 'Stair Rail / Handrail Install', cat: 'Accessibility / ATP', tags: ['stair','rail','handrail','safety','ada','atp','stairway'],
        trade: 'general', areaDesc: 'Stairway', sqft: 30, markup: 20,
        scopeTitle: 'Stair Handrail Installation',
        scope: ['Install continuous handrail on stairway','Mount brackets into wall studs','Verify height (34-38") per code','Install returns at top and bottom'],
        notes: ['Handrail 1-1/4" to 1-1/2" diameter','Must extend 12" past top and bottom risers per code'],
        labor: [
            { desc: 'Measurement & layout', basis: '1 lot', price: 40 },
            { desc: 'Bracket / post mounting', basis: '1 lot', price: 75 },
            { desc: 'Rail installation & leveling', basis: '1 lot', price: 60 },
            { desc: 'Cleanup', basis: '1 lot', price: 20 }
        ],
        materials: [
            { desc: 'Handrail (wood or metal)', qty: '1', price: 55 },
            { desc: 'Wall Brackets', qty: '4', price: 8 },
            { desc: 'End Caps / Returns', qty: '2', price: 12 },
            { desc: 'Mounting Hardware', qty: '1 lot', price: 10 }
        ],
        disclaimer: 'Wall composition and stud placement cannot be confirmed until installation begins. Additional blocking may be required.'
    },
    exterior_handrail: {
        label: 'Exterior Step/Porch Handrail', cat: 'Accessibility / ATP', tags: ['handrail','exterior','porch','steps','safety','atp','outdoor'],
        trade: 'general', areaDesc: 'Exterior Steps / Porch', sqft: 20, markup: 20,
        scopeTitle: 'Exterior Handrail Installation',
        scope: ['Install weather-rated handrail at exterior steps','Mount posts into concrete or wood','Verify code-compliant height and graspability'],
        notes: ['Aluminum or galvanized steel recommended for exterior','Must withstand 200 lb concentrated load'],
        labor: [
            { desc: 'Post anchoring (concrete or wood)', basis: '1 lot', price: 65 },
            { desc: 'Rail mounting & leveling', basis: '1 lot', price: 55 },
            { desc: 'Weather seal / finish', basis: '1 lot', price: 25 },
            { desc: 'Cleanup', basis: '1 lot', price: 15 }
        ],
        materials: [
            { desc: 'Exterior Handrail (aluminum or steel)', qty: '1', price: 75 },
            { desc: 'Post Bases / Concrete Anchors', qty: '2', price: 18 },
            { desc: 'Mounting Hardware (stainless)', qty: '1 lot', price: 15 },
            { desc: 'Concrete Repair / Epoxy', qty: '1 lot', price: 12 }
        ],
        disclaimer: 'Concrete conditions at mounting points cannot be assessed until drilling begins. Crumbling concrete or rebar conflicts may require alternative anchoring.'
    },

    // ── PLUMBING ─────────────────────────────────────────────────────
    toilet_replace: {
        label: 'Toilet Replacement', cat: 'Plumbing', tags: ['toilet','replace','bathroom','plumbing','ada','comfort height'],
        trade: 'plumbing', areaDesc: 'Bathroom', sqft: 48, markup: 20,
        scopeTitle: 'Toilet Replacement',
        scope: ['Remove and dispose of existing toilet','Inspect flange and drain','Install new comfort-height toilet','Connect water supply and test'],
        notes: ['ADA comfort height: 17-19"','Wax ring replaced every install'],
        labor: [
            { desc: 'Remove existing toilet', basis: '1 lot', price: 45 },
            { desc: 'Inspect flange & drain', basis: '1 lot', price: 30 },
            { desc: 'Install new toilet', basis: '1 lot', price: 75 },
            { desc: 'Connect supply & test', basis: '1 lot', price: 25 },
            { desc: 'Cleanup & haul-away', basis: '1 lot', price: 25 }
        ],
        materials: [
            { desc: 'Toilet (elongated, ADA height)', qty: '1', price: 189 },
            { desc: 'Wax Ring / Gasket', qty: '1', price: 5 },
            { desc: 'Supply Line (braided)', qty: '1', price: 8 },
            { desc: 'Shut-Off Valve', qty: '1', price: 12 },
            { desc: 'Toilet Seat', qty: '1', price: 25 },
            { desc: 'Caulk', qty: '1', price: 6 }
        ],
        disclaimer: 'Plumbing conditions beneath the toilet cannot be assessed until removal. Corroded flanges or damaged subfloor may require additional work.'
    },
    faucet_replace: {
        label: 'Faucet Replacement', cat: 'Plumbing', tags: ['faucet','replace','kitchen','bathroom','plumbing','sink'],
        trade: 'plumbing', areaDesc: 'Kitchen / Bathroom', sqft: 48, markup: 20,
        scopeTitle: 'Faucet Replacement',
        scope: ['Remove existing faucet','Install new faucet and connect supply lines','Test for leaks'],
        notes: ['Shut-off valves tested before starting'],
        labor: [
            { desc: 'Remove existing faucet', basis: '1 lot', price: 35 },
            { desc: 'Install new faucet', basis: '1 lot', price: 55 },
            { desc: 'Connect supply lines & test', basis: '1 lot', price: 25 },
            { desc: 'Cleanup', basis: '1 lot', price: 15 }
        ],
        materials: [
            { desc: 'Faucet (single-handle)', qty: '1', price: 85 },
            { desc: 'Supply Lines (braided)', qty: '2', price: 8 },
            { desc: 'Plumber\'s Putty / Teflon', qty: '1 lot', price: 6 }
        ],
        disclaimer: 'Supply line connections and valve conditions cannot be assessed until the existing faucet is removed.'
    },
    water_heater: {
        label: 'Water Heater Install', cat: 'Plumbing', tags: ['water heater','replace','install','plumbing','gas','electric'],
        trade: 'plumbing', areaDesc: 'Utility / Basement', sqft: 48, markup: 20,
        scopeTitle: 'Water Heater Replacement',
        scope: ['Disconnect, drain, and remove existing unit','Install new 50-gallon water heater','Connect plumbing, gas/electric, and venting','Test operation and temperature'],
        notes: ['Expansion tank required by code in closed systems','Permits may be required'],
        labor: [
            { desc: 'Disconnect & drain existing unit', basis: '1 lot', price: 75 },
            { desc: 'Remove & haul away old unit', basis: '1 lot', price: 60 },
            { desc: 'Install new water heater', basis: '1 lot', price: 200 },
            { desc: 'Connect plumbing & gas/electric', basis: '1 lot', price: 100 },
            { desc: 'Test & verify operation', basis: '1 lot', price: 40 }
        ],
        materials: [
            { desc: 'Water Heater (50 gal)', qty: '1', price: 450 },
            { desc: 'Expansion Tank', qty: '1', price: 35 },
            { desc: 'Flex Connectors', qty: '2', price: 15 },
            { desc: 'T&P Valve / Discharge Pipe', qty: '1 lot', price: 20 },
            { desc: 'Gas Flex / Fittings (if gas)', qty: '1 lot', price: 25 }
        ],
        disclaimer: 'Existing plumbing, gas, and electrical connections may not meet current code. Venting or circuit upgrades may be required.'
    },
    drain_repair: {
        label: 'Drain Repair / Clearing', cat: 'Plumbing', tags: ['drain','repair','clog','snake','plumbing','pipe'],
        trade: 'plumbing', areaDesc: 'Bathroom / Kitchen', sqft: 48, markup: 20,
        scopeTitle: 'Drain Repair & Clearing',
        scope: ['Diagnose drain blockage or damage','Clear blockage with snake or hydro-jet','Repair or replace damaged pipe section','Test flow'],
        notes: ['Camera inspection available for $75 additional'],
        labor: [
            { desc: 'Diagnose drain issue', basis: '1 lot', price: 60 },
            { desc: 'Access / open drain line', basis: '1 lot', price: 45 },
            { desc: 'Snake / clear blockage', basis: '1 lot', price: 75 },
            { desc: 'Repair / replace damaged section', basis: '1 lot', price: 100 },
            { desc: 'Test & verify flow', basis: '1 lot', price: 25 }
        ],
        materials: [
            { desc: 'PVC / ABS Pipe & Fittings', qty: '1 lot', price: 25 },
            { desc: 'Drain Cleaner / Treatment', qty: '1', price: 12 },
            { desc: 'Pipe Cement / Primer', qty: '1 lot', price: 10 }
        ],
        disclaimer: 'Drain conditions within walls, floors, and underground cannot be assessed until access is gained.'
    },
    sink_install: {
        label: 'Sink Installation', cat: 'Plumbing', tags: ['sink','install','kitchen','bathroom','plumbing','vanity'],
        trade: 'plumbing', areaDesc: 'Kitchen / Bathroom', sqft: 48, markup: 20,
        scopeTitle: 'Sink Installation',
        scope: ['Remove existing sink','Install new sink and faucet','Connect drain, supply, and disposal (if applicable)','Test for leaks'],
        notes: ['Counter modifications for undermount may add cost'],
        labor: [
            { desc: 'Remove existing sink', basis: '1 lot', price: 40 },
            { desc: 'Install new sink', basis: '1 lot', price: 65 },
            { desc: 'Connect faucet & supply lines', basis: '1 lot', price: 35 },
            { desc: 'Connect drain / P-trap', basis: '1 lot', price: 30 },
            { desc: 'Test & cleanup', basis: '1 lot', price: 20 }
        ],
        materials: [
            { desc: 'Sink (stainless or porcelain)', qty: '1', price: 120 },
            { desc: 'Faucet', qty: '1', price: 85 },
            { desc: 'P-Trap Assembly', qty: '1', price: 12 },
            { desc: 'Supply Lines', qty: '2', price: 8 },
            { desc: 'Plumber\'s Putty / Silicone', qty: '1 lot', price: 8 }
        ],
        disclaimer: 'Existing plumbing connections and counter condition cannot be fully assessed until the old sink is removed.'
    },

    // ── ELECTRICAL ───────────────────────────────────────────────────
    outlet_install: {
        label: 'Outlet / Switch Install', cat: 'Electrical', tags: ['outlet','switch','receptacle','electrical','wiring'],
        trade: 'electrical', areaDesc: 'Room Interior', sqft: 120, markup: 20,
        scopeTitle: 'Electrical Outlet / Switch Installation',
        scope: ['Install new outlet(s) or switch(es)','Run new wiring from panel or circuit','Test all circuits with meter'],
        notes: ['GFCI required in wet locations','AFCI required in bedrooms per current code'],
        labor: [
            { desc: 'Circuit identification', basis: '1 lot', price: 40 },
            { desc: 'Cut-in box installation', basis: 'per unit', price: 35 },
            { desc: 'Wire run (new or extension)', basis: 'per run', price: 85 },
            { desc: 'Device installation & wiring', basis: 'per unit', price: 30 },
            { desc: 'Testing & verification', basis: '1 lot', price: 25 }
        ],
        materials: [
            { desc: 'Outlet / Receptacle', qty: '2', price: 4 },
            { desc: 'Old-Work Electrical Box', qty: '2', price: 5 },
            { desc: 'Romex Wire (12/2 or 14/2)', qty: '1 lot', price: 25 },
            { desc: 'Cover Plates', qty: '2', price: 3 },
            { desc: 'Wire Nuts / Connectors', qty: '1 lot', price: 5 }
        ],
        disclaimer: 'Electrical systems concealed within walls cannot be fully assessed until access is gained. All work per NEC and local code.'
    },
    light_fixture: {
        label: 'Light Fixture Install', cat: 'Electrical', tags: ['light','fixture','install','electrical','LED','ceiling'],
        trade: 'electrical', areaDesc: 'Room Interior', sqft: 120, markup: 20,
        scopeTitle: 'Light Fixture Installation',
        scope: ['Remove existing fixture','Install new fixture with proper wiring','Verify operation and switch function'],
        notes: ['Heavy fixtures may require fan-rated box'],
        labor: [
            { desc: 'Remove existing fixture', basis: 'per unit', price: 25 },
            { desc: 'Install new fixture', basis: 'per unit', price: 45 },
            { desc: 'Wiring connection & testing', basis: 'per unit', price: 20 },
            { desc: 'Cleanup', basis: '1 lot', price: 15 }
        ],
        materials: [
            { desc: 'Light Fixture', qty: '1', price: 65 },
            { desc: 'Wire Nuts / Electrical Tape', qty: '1 lot', price: 5 },
            { desc: 'Mounting Hardware', qty: '1 lot', price: 8 }
        ],
        disclaimer: 'Electrical box condition and wiring cannot be assessed until the existing fixture is removed.'
    },
    ceiling_fan: {
        label: 'Ceiling Fan Install', cat: 'Electrical', tags: ['ceiling fan','fan','install','electrical','bedroom'],
        trade: 'electrical', areaDesc: 'Bedroom / Living Room', sqft: 150, markup: 20,
        scopeTitle: 'Ceiling Fan Installation',
        scope: ['Remove existing fixture','Install fan-rated box','Assemble and mount ceiling fan','Wire, test, verify'],
        notes: ['Fan-rated box required by NEC','8ft minimum ceiling height recommended'],
        labor: [
            { desc: 'Remove existing fixture', basis: '1 lot', price: 30 },
            { desc: 'Install fan-rated box (if needed)', basis: '1 lot', price: 55 },
            { desc: 'Assemble & mount ceiling fan', basis: '1 lot', price: 75 },
            { desc: 'Wiring & testing', basis: '1 lot', price: 30 }
        ],
        materials: [
            { desc: 'Ceiling Fan w/ Light Kit', qty: '1', price: 120 },
            { desc: 'Fan-Rated Ceiling Box', qty: '1', price: 15 },
            { desc: 'Mounting Hardware', qty: '1 lot', price: 8 }
        ],
        disclaimer: 'Ceiling structure and existing electrical box rating cannot be confirmed until the old fixture is removed. A fan-rated box is required by code.'
    },
    gfci_upgrade: {
        label: 'GFCI Outlet Upgrade', cat: 'Electrical', tags: ['gfci','outlet','upgrade','electrical','safety','bathroom','kitchen'],
        trade: 'electrical', areaDesc: 'Kitchen / Bathroom / Garage', sqft: 48, markup: 20,
        scopeTitle: 'GFCI Outlet Upgrade',
        scope: ['Replace standard outlets with GFCI protection','Test trip/reset function','Verify downstream protection'],
        notes: ['GFCI required within 6ft of water per NEC','One GFCI can protect downstream outlets on same circuit'],
        labor: [
            { desc: 'Circuit identification & testing', basis: '1 lot', price: 40 },
            { desc: 'Remove existing outlet', basis: 'per unit', price: 10 },
            { desc: 'Install GFCI outlet', basis: 'per unit', price: 30 },
            { desc: 'Test trip/reset function', basis: '1 lot', price: 15 }
        ],
        materials: [
            { desc: 'GFCI Outlet (20A)', qty: '3', price: 18 },
            { desc: 'GFCI Cover Plates', qty: '3', price: 4 },
            { desc: 'Wire Nuts / Tape', qty: '1 lot', price: 5 }
        ],
        disclaimer: 'Wiring behind existing outlets cannot be assessed until removal. Aluminum wiring or missing grounds may require additional work per NEC.'
    },
    panel_upgrade: {
        label: 'Electrical Panel Upgrade (200A)', cat: 'Electrical', tags: ['panel','breaker','upgrade','electrical','200 amp','service'],
        trade: 'electrical', areaDesc: 'Utility / Garage', sqft: 48, markup: 20,
        scopeTitle: 'Electrical Panel Upgrade — 200A',
        scope: ['Replace existing panel with 200A service','Transfer all circuits to new panel','Label all circuits','Coordinate with utility for disconnect'],
        notes: ['Permit and inspection required','Utility disconnect scheduled 2-3 days ahead'],
        labor: [
            { desc: 'Disconnect coordination with utility', basis: '1 lot', price: 50 },
            { desc: 'Remove old panel', basis: '1 lot', price: 120 },
            { desc: 'Install new 200A panel', basis: '1 lot', price: 350 },
            { desc: 'Transfer & terminate circuits', basis: '1 lot', price: 250 },
            { desc: 'Grounding & bonding', basis: '1 lot', price: 75 },
            { desc: 'Labeling, testing & inspection', basis: '1 lot', price: 60 }
        ],
        materials: [
            { desc: '200A Main Breaker Panel', qty: '1', price: 180 },
            { desc: 'Circuit Breakers (various)', qty: '1 lot', price: 120 },
            { desc: 'Grounding Rod / Wire', qty: '1 lot', price: 35 },
            { desc: 'Conduit / Wire', qty: '1 lot', price: 60 },
            { desc: 'Connectors / Lugs', qty: '1 lot', price: 25 }
        ],
        disclaimer: 'Existing wiring condition cannot be fully assessed until the old panel is removed. Undersized wiring or code violations may be discovered. Permit and inspection required.'
    },

    // ── GENERAL / REMODEL ────────────────────────────────────────────
    drywall_patch: {
        label: 'Drywall Patch & Repair', cat: 'General / Remodel', tags: ['drywall','patch','repair','hole','wall','general'],
        trade: 'general', areaDesc: 'Room Interior', sqft: 120, markup: 20,
        scopeTitle: 'Drywall Patch & Repair',
        scope: ['Cut out damaged section','Install backing and patch','Tape, mud, sand (3 coats)','Prime and paint to match'],
        notes: ['Allow 24 hrs between mud coats'],
        labor: [
            { desc: 'Cut out damaged area', basis: '1 lot', price: 30 },
            { desc: 'Install backing & patch', basis: 'per patch', price: 35 },
            { desc: 'Tape, mud & sand (3 coats)', basis: 'per patch', price: 55 },
            { desc: 'Prime & paint to match', basis: '1 lot', price: 45 },
            { desc: 'Cleanup', basis: '1 lot', price: 15 }
        ],
        materials: [
            { desc: 'Drywall Patch / Sheet', qty: '1', price: 12 },
            { desc: 'Joint Compound', qty: '1', price: 10 },
            { desc: 'Mesh Tape', qty: '1', price: 6 },
            { desc: 'Sandpaper (various grit)', qty: '1 lot', price: 8 },
            { desc: 'Primer', qty: '1 qt', price: 12 },
            { desc: 'Paint (matched)', qty: '1 qt', price: 18 }
        ],
        disclaimer: 'Conditions behind drywall cannot be assessed until the damaged area is opened. Water damage, mold, or structural issues may be discovered.'
    },
    door_install: {
        label: 'Interior Door Install', cat: 'General / Remodel', tags: ['door','install','interior','general','pre-hung'],
        trade: 'general', areaDesc: 'Room Interior', sqft: 120, markup: 20,
        scopeTitle: 'Interior Door Installation',
        scope: ['Remove existing door and hardware','Prep opening and shim frame','Hang new pre-hung door','Install hardware, trim, casing'],
        notes: ['Verify rough opening before ordering'],
        labor: [
            { desc: 'Remove existing door & hardware', basis: '1 lot', price: 30 },
            { desc: 'Prep opening / shim frame', basis: '1 lot', price: 45 },
            { desc: 'Hang new door', basis: '1 lot', price: 65 },
            { desc: 'Install hardware (knob, hinges)', basis: '1 lot', price: 30 },
            { desc: 'Trim & casing adjustment', basis: '1 lot', price: 40 }
        ],
        materials: [
            { desc: 'Pre-Hung Interior Door', qty: '1', price: 95 },
            { desc: 'Door Knob / Lever Set', qty: '1', price: 25 },
            { desc: 'Hinges (3-pack)', qty: '1', price: 10 },
            { desc: 'Shims / Screws', qty: '1 lot', price: 8 },
            { desc: 'Caulk / Wood Filler', qty: '1', price: 6 }
        ],
        disclaimer: 'Door frame and wall conditions cannot be assessed until the existing door is removed. Out-of-square frames or non-standard sizing may require additional work.'
    },
    exterior_door: {
        label: 'Exterior Door Replacement', cat: 'General / Remodel', tags: ['door','exterior','entry','replace','front door','security'],
        trade: 'general', areaDesc: 'Entry', sqft: 30, markup: 20,
        scopeTitle: 'Exterior Door Replacement',
        scope: ['Remove existing exterior door and frame','Install new pre-hung exterior door','Install deadbolt and handle set','Seal, caulk, and insulate around frame'],
        notes: ['Steel or fiberglass recommended','Verify rough opening before ordering'],
        labor: [
            { desc: 'Remove existing door & frame', basis: '1 lot', price: 55 },
            { desc: 'Prep rough opening', basis: '1 lot', price: 45 },
            { desc: 'Install pre-hung exterior door', basis: '1 lot', price: 120 },
            { desc: 'Install hardware (deadbolt, handle)', basis: '1 lot', price: 35 },
            { desc: 'Insulation, caulk & weatherseal', basis: '1 lot', price: 40 },
            { desc: 'Trim & finish', basis: '1 lot', price: 45 }
        ],
        materials: [
            { desc: 'Pre-Hung Exterior Door', qty: '1', price: 275 },
            { desc: 'Deadbolt & Handle Set', qty: '1', price: 65 },
            { desc: 'Weatherstripping / Threshold', qty: '1 lot', price: 25 },
            { desc: 'Low-Expansion Foam', qty: '1', price: 8 },
            { desc: 'Exterior Caulk', qty: '1', price: 8 },
            { desc: 'Exterior Trim / Brick Mold', qty: '1 lot', price: 30 }
        ],
        disclaimer: 'Exterior framing and flashing conditions cannot be assessed until the old door is removed. Rot or water damage may require additional repair.'
    },
    window_replace: {
        label: 'Window Replacement', cat: 'General / Remodel', tags: ['window','replace','vinyl','double pane','energy'],
        trade: 'general', areaDesc: 'Room Interior', sqft: 120, markup: 20,
        scopeTitle: 'Window Replacement',
        scope: ['Remove existing window and trim','Install new vinyl double-pane window','Insulate, flash, and seal','Reinstall interior trim'],
        notes: ['Low-E glass recommended for energy efficiency','Flashing tape on exterior prevents water intrusion'],
        labor: [
            { desc: 'Remove existing window & trim', basis: 'per unit', price: 45 },
            { desc: 'Install new window', basis: 'per unit', price: 85 },
            { desc: 'Insulate & flash perimeter', basis: 'per unit', price: 30 },
            { desc: 'Interior trim & caulk', basis: 'per unit', price: 35 },
            { desc: 'Cleanup', basis: '1 lot', price: 20 }
        ],
        materials: [
            { desc: 'Vinyl Double-Pane Window', qty: '1', price: 225 },
            { desc: 'Flashing Tape', qty: '1 roll', price: 15 },
            { desc: 'Low-Expansion Foam', qty: '1', price: 8 },
            { desc: 'Interior Trim / Casing', qty: '1 lot', price: 25 },
            { desc: 'Caulk (interior & exterior)', qty: '2', price: 6 }
        ],
        disclaimer: 'Framing and sheathing around windows cannot be assessed until the old window is removed. Rot, mold, or structural damage may be discovered.'
    },
    deck_repair: {
        label: 'Deck Repair / Board Replacement', cat: 'General / Remodel', tags: ['deck','repair','boards','exterior','wood','composite'],
        trade: 'general', areaDesc: 'Exterior Deck', sqft: 100, markup: 20,
        scopeTitle: 'Deck Repair & Board Replacement',
        scope: ['Remove damaged/rotted deck boards','Inspect joists and framing','Replace boards with matching material','Re-fasten and seal all connections'],
        notes: ['Match existing material (wood vs composite)','Inspect ledger board and flashing while accessible'],
        labor: [
            { desc: 'Remove damaged boards', basis: '1 lot', price: 45 },
            { desc: 'Inspect & repair joists (if needed)', basis: '1 lot', price: 75 },
            { desc: 'Install replacement boards', basis: 'per sq ft', price: 3.50 },
            { desc: 'Fastening & finishing', basis: '1 lot', price: 40 },
            { desc: 'Cleanup', basis: '1 lot', price: 20 }
        ],
        materials: [
            { desc: 'Deck Boards (PT or composite)', qty: '1 lot', price: 3.00 },
            { desc: 'Deck Screws (stainless)', qty: '1 lb', price: 12 },
            { desc: 'Joist Material (if needed)', qty: '1 lot', price: 25 },
            { desc: 'Wood Sealer / Stain', qty: '1 gal', price: 30 }
        ],
        disclaimer: 'Joist and framing conditions cannot be assessed until deck boards are removed. Rot, insect damage, or code deficiencies may be discovered.'
    },

    // ── FLOORING ─────────────────────────────────────────────────────
    flooring_vinyl: {
        label: 'Vinyl Flooring Install (LVP)', cat: 'Flooring', tags: ['vinyl','lvp','flooring','luxury vinyl plank','click lock'],
        trade: 'flooring', areaDesc: 'Room Interior', sqft: 120, markup: 20,
        scopeTitle: 'Luxury Vinyl Plank (LVP) Installation',
        scope: ['Remove existing flooring','Prep subfloor — level, patch, clean','Install LVP with expansion gaps','Install transitions, quarter round, shoe molding'],
        notes: ['10% waste factor included','Acclimate 48 hrs before install'],
        labor: [
            { desc: 'Remove existing flooring', basis: 'per sq ft', price: 1.50 },
            { desc: 'Subfloor prep & leveling', basis: 'per sq ft', price: 0.75 },
            { desc: 'Vinyl plank installation', basis: 'per sq ft', price: 2.50 },
            { desc: 'Transition strips & trim', basis: '1 lot', price: 45 },
            { desc: 'Cleanup & haul-away', basis: '1 lot', price: 40 }
        ],
        materials: [
            { desc: 'Luxury Vinyl Plank (LVP)', qty: '1 lot', price: 2.50 },
            { desc: 'Underlayment', qty: '1 lot', price: 0.50 },
            { desc: 'Transition Strips', qty: '3', price: 12 },
            { desc: 'Quarter Round / Shoe Molding', qty: '1 lot', price: 25 },
            { desc: 'Adhesive / Spacers', qty: '1 lot', price: 15 }
        ],
        disclaimer: 'Subfloor conditions cannot be assessed until existing flooring is removed. Water damage, uneven surfaces, or asbestos may be discovered.'
    },
    flooring_tile: {
        label: 'Ceramic / Porcelain Tile', cat: 'Flooring', tags: ['tile','ceramic','porcelain','flooring','bathroom','kitchen','grout'],
        trade: 'flooring', areaDesc: 'Bathroom / Kitchen', sqft: 80, markup: 20,
        scopeTitle: 'Ceramic/Porcelain Tile Installation',
        scope: ['Remove existing flooring','Install backer board','Set tile with thinset','Grout, seal, and install transitions'],
        notes: ['Backer board required over wood in wet areas','Large format tile requires 95% mortar coverage'],
        labor: [
            { desc: 'Remove existing flooring', basis: 'per sq ft', price: 2.00 },
            { desc: 'Backer board installation', basis: 'per sq ft', price: 1.50 },
            { desc: 'Tile setting (thinset)', basis: 'per sq ft', price: 5.00 },
            { desc: 'Grouting & sealing', basis: 'per sq ft', price: 1.50 },
            { desc: 'Transitions & cleanup', basis: '1 lot', price: 50 }
        ],
        materials: [
            { desc: 'Porcelain Tile', qty: '1 lot', price: 4.00 },
            { desc: 'Thinset Mortar', qty: '2 bags', price: 18 },
            { desc: 'Backer Board (3x5)', qty: '4', price: 14 },
            { desc: 'Grout (sanded)', qty: '1 bag', price: 15 },
            { desc: 'Grout Sealer', qty: '1', price: 12 },
            { desc: 'Tile Spacers', qty: '1 bag', price: 5 }
        ],
        disclaimer: 'Subfloor condition cannot be assessed until existing flooring is removed. Water damage or asbestos in old mastic may be discovered.'
    },
    carpet_tile: {
        label: 'Carpet Tile (Commercial)', cat: 'Flooring', tags: ['carpet','tile','commercial','flooring','office','glue down'],
        trade: 'carpet_tile', areaDesc: 'Commercial Space', sqft: 200, markup: 20,
        scopeTitle: 'Commercial Carpet Tile Installation',
        scope: ['Remove existing flooring','Prep concrete/subfloor surface','Install carpet tile in pattern','Install base/trim at perimeter'],
        notes: ['Individual tiles replaceable if damaged','Monolithic, quarter-turn, ashlar, or brick patterns'],
        labor: [
            { desc: 'Remove existing flooring', basis: 'per sq ft', price: 1.00 },
            { desc: 'Floor prep & cleaning', basis: 'per sq ft', price: 0.50 },
            { desc: 'Carpet tile installation', basis: 'per sq ft', price: 1.75 },
            { desc: 'Base trim installation', basis: '1 lot', price: 50 },
            { desc: 'Cleanup', basis: '1 lot', price: 30 }
        ],
        materials: [
            { desc: 'Carpet Tile (24x24)', qty: '1 lot', price: 2.25 },
            { desc: 'Carpet Tile Adhesive', qty: '1 lot', price: 0.30 },
            { desc: 'Rubber Wall Base', qty: '1 lot', price: 0.75 },
            { desc: 'Base Adhesive', qty: '1 lot', price: 10 }
        ],
        disclaimer: 'Concrete moisture levels cannot be assessed until existing flooring is removed. High moisture (>75% RH) may require mitigation.'
    },

    // ── PAINTING ─────────────────────────────────────────────────────
    paint_room: {
        label: 'Room Paint (Interior)', cat: 'Painting', tags: ['paint','interior','room','walls','ceiling','painting'],
        trade: 'painting', areaDesc: 'Room Interior', sqft: 150, markup: 20,
        scopeTitle: 'Interior Room Painting',
        scope: ['Prep surfaces — fill holes, sand, tape','Prime walls and ceiling','Apply 2 coats walls','Paint ceiling','Trim and detail work'],
        notes: ['Wall area typically 3x floor area','Low-VOC paint recommended for occupied spaces'],
        labor: [
            { desc: 'Surface prep (fill, sand, tape)', basis: 'per sq ft', price: 0.50 },
            { desc: 'Prime walls & ceiling', basis: 'per sq ft', price: 0.40 },
            { desc: 'Paint — 2 coats walls', basis: 'per sq ft', price: 0.80 },
            { desc: 'Paint — ceiling', basis: 'per sq ft', price: 0.50 },
            { desc: 'Trim & detail work', basis: '1 lot', price: 75 },
            { desc: 'Cleanup & touch-up', basis: '1 lot', price: 30 }
        ],
        materials: [
            { desc: 'Interior Paint (walls)', qty: '2 gal', price: 35 },
            { desc: 'Ceiling Paint', qty: '1 gal', price: 28 },
            { desc: 'Primer', qty: '1 gal', price: 22 },
            { desc: 'Painter\'s Tape', qty: '2 rolls', price: 7 },
            { desc: 'Drop Cloths', qty: '2', price: 8 },
            { desc: 'Rollers / Brushes / Tray', qty: '1 lot', price: 18 },
            { desc: 'Spackle / Caulk', qty: '1 lot', price: 10 }
        ],
        disclaimer: 'Wall and ceiling conditions may reveal water stains, mold, or lead paint (pre-1978) once preparation begins.'
    },
    paint_exterior: {
        label: 'Exterior Painting', cat: 'Painting', tags: ['paint','exterior','siding','house','scrape','prime'],
        trade: 'painting', areaDesc: 'Exterior', sqft: 200, markup: 20,
        scopeTitle: 'Exterior House Painting',
        scope: ['Power wash all surfaces','Scrape and sand loose paint','Caulk gaps and joints','Prime bare areas','Apply 2 coats exterior paint','Paint trim, fascia, soffits'],
        notes: ['Temperature must be 50F+ and dry 24 hrs','Lead testing required pre-1978 homes'],
        labor: [
            { desc: 'Power washing', basis: 'per sq ft', price: 0.25 },
            { desc: 'Scraping & sanding', basis: 'per sq ft', price: 0.75 },
            { desc: 'Caulking & patching', basis: '1 lot', price: 100 },
            { desc: 'Priming', basis: 'per sq ft', price: 0.50 },
            { desc: 'Paint — 2 coats', basis: 'per sq ft', price: 1.25 },
            { desc: 'Trim, fascia & soffits', basis: '1 lot', price: 200 },
            { desc: 'Cleanup', basis: '1 lot', price: 50 }
        ],
        materials: [
            { desc: 'Exterior Paint', qty: '5 gal', price: 42 },
            { desc: 'Exterior Primer', qty: '2 gal', price: 30 },
            { desc: 'Caulk (exterior)', qty: '6', price: 6 },
            { desc: 'Painter\'s Tape', qty: '3 rolls', price: 7 },
            { desc: 'Drop Cloths / Plastic', qty: '1 lot', price: 20 },
            { desc: 'Rollers / Brushes / Sprayer Tips', qty: '1 lot', price: 35 }
        ],
        disclaimer: 'Siding, trim, and substrate conditions cannot be fully assessed until scraping begins. Rot, mold, or lead paint may be discovered.'
    },
    cabinet_paint: {
        label: 'Cabinet Painting / Refinish', cat: 'Painting', tags: ['cabinet','paint','refinish','kitchen','painting'],
        trade: 'painting', areaDesc: 'Kitchen', sqft: 120, markup: 20,
        scopeTitle: 'Kitchen Cabinet Painting',
        scope: ['Remove all doors, drawers, and hardware','Clean, sand, and degloss all surfaces','Apply bonding primer','Apply 2 coats cabinet-grade paint','Reinstall doors, drawers, and new hardware'],
        notes: ['Allow 2 weeks for full cure before heavy use','Spray application recommended for smoothest finish'],
        labor: [
            { desc: 'Remove doors, drawers & hardware', basis: '1 lot', price: 80 },
            { desc: 'Clean, sand & degloss', basis: '1 lot', price: 120 },
            { desc: 'Prime all surfaces', basis: '1 lot', price: 100 },
            { desc: 'Paint — 2 coats (spray or brush)', basis: '1 lot', price: 250 },
            { desc: 'Reinstall doors, drawers, hardware', basis: '1 lot', price: 80 },
            { desc: 'Touch-up & cleanup', basis: '1 lot', price: 40 }
        ],
        materials: [
            { desc: 'Cabinet Paint (Benjamin Moore Advance or equiv)', qty: '2 gal', price: 55 },
            { desc: 'Bonding Primer', qty: '1 gal', price: 35 },
            { desc: 'Sandpaper / Sanding Sponges', qty: '1 lot', price: 15 },
            { desc: 'Tack Cloth / Degreaser', qty: '1 lot', price: 10 },
            { desc: 'New Cabinet Hardware (knobs/pulls)', qty: '20', price: 5 },
            { desc: 'Painter\'s Tape / Plastic', qty: '1 lot', price: 15 }
        ],
        disclaimer: 'Cabinet substrate (wood, MDF, laminate, thermofoil) affects adhesion. Laminate or thermofoil cabinets may not accept paint long-term. Contractor will assess and advise.'
    },

    // ── ROOFING / EXTERIOR ───────────────────────────────────────────
    roof_repair: {
        label: 'Roof Repair (Shingle Patch)', cat: 'Roofing / Exterior', tags: ['roof','repair','shingle','leak','patch','exterior'],
        trade: 'general', areaDesc: 'Roof', sqft: 100, markup: 20,
        scopeTitle: 'Roof Shingle Repair',
        scope: ['Locate and assess leak/damage area','Remove damaged shingles','Inspect underlayment and decking','Install new shingles to match','Seal all penetrations and flashings'],
        notes: ['Color match may not be exact on aged roofs','Work only in dry conditions above 40F'],
        labor: [
            { desc: 'Roof access & safety setup', basis: '1 lot', price: 50 },
            { desc: 'Remove damaged shingles', basis: '1 lot', price: 45 },
            { desc: 'Inspect & repair decking (if needed)', basis: '1 lot', price: 60 },
            { desc: 'Install replacement shingles', basis: '1 lot', price: 85 },
            { desc: 'Flash & seal', basis: '1 lot', price: 40 },
            { desc: 'Cleanup', basis: '1 lot', price: 25 }
        ],
        materials: [
            { desc: 'Shingle Bundle (matching)', qty: '1', price: 35 },
            { desc: 'Roofing Nails', qty: '1 lb', price: 8 },
            { desc: 'Roofing Cement / Sealant', qty: '1', price: 12 },
            { desc: 'Underlayment (if needed)', qty: '1 roll', price: 25 },
            { desc: 'Flashing (if needed)', qty: '1 lot', price: 15 }
        ],
        disclaimer: 'Roof decking and underlayment conditions cannot be assessed until damaged shingles are removed. Rot, mold, or structural damage may be discovered.'
    },
    gutter_install: {
        label: 'Gutter Install / Replacement', cat: 'Roofing / Exterior', tags: ['gutter','install','replace','downspout','exterior','rain'],
        trade: 'general', areaDesc: 'Exterior', sqft: 100, markup: 20,
        scopeTitle: 'Gutter Installation',
        scope: ['Remove existing gutters (if applicable)','Install new seamless aluminum gutters','Install downspouts with splash blocks','Verify slope and drainage flow'],
        notes: ['Minimum 1/4" slope per 10ft of gutter','Downspouts every 30-40ft of gutter run'],
        labor: [
            { desc: 'Remove existing gutters', basis: '1 lot', price: 45 },
            { desc: 'Install new gutters', basis: 'per lin ft', price: 6 },
            { desc: 'Install downspouts', basis: 'per unit', price: 35 },
            { desc: 'Splash blocks / extensions', basis: 'per unit', price: 15 },
            { desc: 'Cleanup', basis: '1 lot', price: 20 }
        ],
        materials: [
            { desc: 'Aluminum Gutter (5")', qty: '1 lot', price: 3.50 },
            { desc: 'Downspouts', qty: '2', price: 18 },
            { desc: 'Gutter Hangers / Brackets', qty: '1 lot', price: 1.50 },
            { desc: 'End Caps / Corners', qty: '1 lot', price: 12 },
            { desc: 'Splash Blocks', qty: '2', price: 10 },
            { desc: 'Sealant', qty: '1', price: 8 }
        ],
        disclaimer: 'Fascia board condition cannot be assessed until old gutters are removed. Rot or structural issues may require fascia repair before gutter mounting.'
    }
};
