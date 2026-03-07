/**
 * Field Measurement Calculator — BidGen Trade Tool
 * Smart material calculator for flooring, drywall, trim, and more.
 * Powered by Gemini 2.5 Pro for cut optimization and install planning.
 * 
 * Features:
 *   - Sheet vinyl/carpet/padding cut optimizer with roll widths
 *   - Cove base calculator (perimeter minus doors)
 *   - Transition strip calculator (door count × width)
 *   - Drywall sheet/screw/mud/tape calculator
 *   - LVP/tile box calculator with waste %
 *   - Solo vs team install time estimates
 *   - Gemini AI for optimal seam placement and layout analysis
 */
(function() {
    'use strict';

    var PROXY = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';

    // ================================================================
    // STANDARD ROLL/SHEET SIZES
    // ================================================================
    var ROLL_WIDTHS = {
        'sheet_vinyl': [6, 12, 13.17],   // feet
        'carpet':      [12, 13.17, 15],
        'padding':     [6, 12],
        'cove_base':   [4]                // 4" standard, sold in 120ft coils or boxes of 16x4ft
    };

    var DRYWALL_SIZES = [
        { label: "4' × 8'",  w: 4, h: 8,  sqft: 32 },
        { label: "4' × 10'", w: 4, h: 10, sqft: 40 },
        { label: "4' × 12'", w: 4, h: 12, sqft: 48 }
    ];

    // ================================================================
    // INJECT TOGGLE BUTTON + PANEL
    // ================================================================
    function injectUI() {
        // Toggle button — fixed position
        var btn = document.createElement('button');
        btn.id = 'fieldCalcToggle';
        btn.title = 'Field Measurement Calculator';
        btn.innerHTML = '📐';
        var isMob = window.innerWidth <= 768;
        btn.style.cssText = 'position:fixed;' + (isMob ? 'bottom:56px;right:12px;width:40px;height:40px;font-size:18px;' : 'bottom:90px;right:24px;width:44px;height:44px;font-size:20px;') + 'border-radius:12px;background:rgba(255,255,255,0.06);color:#a1a1aa;border:1px solid rgba(255,255,255,0.08);cursor:pointer;z-index:9998;box-shadow:0 4px 16px rgba(0,0,0,0.3);transition:all 0.2s;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(8px);';
        btn.onmouseenter = function() { btn.style.transform = 'scale(1.1)'; };
        btn.onmouseleave = function() { btn.style.transform = 'scale(1)'; };
        btn.onclick = togglePanel;
        document.body.appendChild(btn);

        // Main panel
        var panel = document.createElement('div');
        panel.id = 'fieldCalcPanel';
        var isMobile = window.innerWidth <= 768;
        panel.style.cssText = 'display:none;position:fixed;' + (isMobile ? 'top:0;left:0;right:0;bottom:0;width:100%;max-height:100vh;border-radius:0;' : 'bottom:145px;right:24px;width:480px;max-height:72vh;border-radius:14px;') + 'background:rgba(9,9,11,0.96);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.06);box-shadow:0 20px 60px rgba(0,0,0,0.5);z-index:9997;overflow:hidden;font-family:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#e4e4e7;font-size:13px;-webkit-font-smoothing:antialiased;';
        panel.innerHTML = buildPanelHTML();
        document.body.appendChild(panel);
    }

    function togglePanel() {
        var p = document.getElementById('fieldCalcPanel');
        p.style.display = p.style.display === 'none' ? 'flex' : 'none';
        if (p.style.display !== 'none') p.style.flexDirection = 'column';
    }

    // ================================================================
    // PANEL HTML
    // ================================================================
    function buildPanelHTML() {
        return '\
<div style="background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.06);padding:10px 14px;display:flex;justify-content:space-between;align-items:center">\
    <div>\
        <div style="font-size:14px;font-weight:600;color:#fafafa;letter-spacing:-0.2px">📐 Field Calculator</div>\
        <div style="font-size:9px;color:#52525b;margin-top:1px">Material & cut planning • Gemini AI</div>\
    </div>\
    <div style="display:flex;gap:6px">\
        <button onclick="fcGenerateBid()" style="background:rgba(34,197,94,0.15);color:#4ade80;border:1px solid rgba(34,197,94,0.3);padding:4px 10px;border-radius:6px;font-size:10px;cursor:pointer;font-weight:600;transition:all 0.15s" title="Send all field calc data to Gemini AI and auto-populate a new bid">⚡ Build Bid</button>\
        <button onclick="fieldCalcClearAll()" style="background:rgba(255,255,255,0.06);color:#a1a1aa;border:1px solid rgba(255,255,255,0.08);padding:4px 10px;border-radius:6px;font-size:10px;cursor:pointer;font-weight:500;transition:all 0.15s">Clear</button>\
        <button onclick="document.getElementById(\'fieldCalcPanel\').style.display=\'none\'" style="background:rgba(255,255,255,0.06);color:#71717a;border:1px solid rgba(255,255,255,0.08);width:24px;height:24px;border-radius:6px;font-size:13px;cursor:pointer;font-weight:500;display:flex;align-items:center;justify-content:center">×</button>\
    </div>\
</div>\
\
<div style="display:flex;border-bottom:1px solid rgba(255,255,255,0.06);background:rgba(255,255,255,0.02)" id="fcTabs">\
    <button class="fc-tab active" onclick="fcSwitchTab(\'flooring\')">🏠 Flooring</button>\
    <button class="fc-tab" onclick="fcSwitchTab(\'drywall\')">🧱 Drywall</button>\
    <button class="fc-tab" onclick="fcSwitchTab(\'trim\')">📏 Trim & Base</button>\
    <button class="fc-tab" onclick="fcSwitchTab(\'ai\')">🧠 AI Planner</button>\
</div>\
\
<div style="flex:1;overflow-y:auto;padding:12px" id="fcContent">\
    ' + buildFlooringTab() + '\
    ' + buildDrywallTab() + '\
    ' + buildTrimTab() + '\
    ' + buildAITab() + '\
</div>\
\
<style>\
    .fc-tab{flex:1;background:none;border:none;color:#52525b;padding:8px 6px;font-size:11px;font-weight:500;cursor:pointer;border-bottom:2px solid transparent;transition:all 0.15s;white-space:nowrap;font-family:inherit}\
    .fc-tab.active{color:#e4e4e7;border-bottom-color:#e4e4e7}\
    .fc-tab:hover{color:#a1a1aa}\
    .fc-section{display:none}\
    .fc-section.active{display:block}\
    .fc-label{font-size:10px;color:#52525b;text-transform:uppercase;letter-spacing:0.8px;font-weight:500;margin-bottom:4px}\
    .fc-input{width:100%;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#e4e4e7;padding:8px 10px;border-radius:8px;font-size:13px;outline:none;font-family:inherit;transition:all 0.15s}\
    .fc-input:focus{border-color:rgba(59,130,246,0.5);box-shadow:0 0 0 3px rgba(59,130,246,0.08)}\
    .fc-select{width:100%;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#e4e4e7;padding:8px 10px;border-radius:8px;font-size:13px;outline:none;cursor:pointer;font-family:inherit}\
    .fc-select option{background:#18181b;color:#e4e4e7}\
    .fc-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}\
    .fc-row3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:10px}\
    .fc-group{margin-bottom:10px}\
    .fc-btn{width:100%;background:#fafafa;color:#09090b;border:none;padding:9px;border-radius:8px;font-weight:600;font-size:13px;cursor:pointer;transition:all 0.15s;margin-top:6px;font-family:inherit}\
    .fc-btn:hover{background:#e4e4e7;transform:translateY(-1px)}\
    .fc-btn-secondary{background:rgba(255,255,255,0.06);color:#a1a1aa;border:1px solid rgba(255,255,255,0.08)}\
    .fc-btn-secondary:hover{background:rgba(255,255,255,0.1);color:#e4e4e7;transform:none}\
    .fc-result{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:12px;margin-top:10px}\
    .fc-result-title{font-size:10px;color:#a1a1aa;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}\
    .fc-result-row{display:flex;justify-content:space-between;padding:4px 0;font-size:12px;border-bottom:1px solid rgba(255,255,255,0.04)}\
    .fc-result-row:last-child{border-bottom:none}\
    .fc-result-label{color:#71717a}\
    .fc-result-value{color:#e4e4e7;font-weight:600;font-variant-numeric:tabular-nums}\
    .fc-result-value.highlight{color:#4ade80;font-size:14px}\
    .fc-divider{border:none;border-top:1px solid rgba(255,255,255,0.06);margin:14px 0}\
    .fc-note{font-size:11px;color:#71717a;line-height:1.5;margin-top:8px;padding:8px 10px;background:rgba(255,255,255,0.02);border-radius:8px;border-left:2px solid rgba(255,255,255,0.1)}\
    .fc-room-entry{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:10px;margin-bottom:8px}\
    .fc-room-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}\
    .fc-remove{background:rgba(239,68,68,0.12);color:#f87171;border:1px solid rgba(239,68,68,0.2);width:22px;height:22px;border-radius:6px;font-size:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.15s}\
    .fc-remove:hover{background:rgba(239,68,68,0.25)}\
    .fc-send-btn{background:rgba(34,197,94,0.1);color:#4ade80;border:1px solid rgba(34,197,94,0.2);padding:7px 14px;border-radius:8px;font-weight:600;font-size:11px;cursor:pointer;margin-top:6px;width:100%;transition:all 0.15s;font-family:inherit}\
    .fc-send-btn:hover{background:rgba(34,197,94,0.2)}\
    @media(max-width:768px){\
        .fc-row{grid-template-columns:1fr !important}\
        .fc-row3{grid-template-columns:1fr 1fr !important}\
        .fc-tab{font-size:10px;padding:7px 4px}\
        #fieldCalcPanel{font-size:12px}\
        .fc-input,.fc-select{padding:8px 10px;font-size:13px}\
        .fc-btn{padding:9px;font-size:12px}\
        .fc-btn-secondary{padding:7px 6px;font-size:11px}\
        .fc-remove{width:22px;height:22px;font-size:11px}\
        .fc-group{margin-bottom:8px}\
        .fc-result{padding:10px}\
        .fc-result-title{font-size:9px;margin-bottom:6px}\
        .fc-result-row{font-size:11px;padding:3px 0}\
        .fc-note{font-size:10px;padding:6px 8px;margin-top:6px}\
        .fc-room-entry{padding:8px;margin-bottom:6px}\
        .fc-label{font-size:9px;margin-bottom:3px}\
    }\
</style>';
    }

    // ================================================================
    // FLOORING TAB
    // ================================================================
    function buildFlooringTab() {
        return '\
<div class="fc-section active" id="fcFlooring">\
    <div class="fc-group">\
        <div class="fc-label">Material Type</div>\
        <select class="fc-select" id="fcFloorType" onchange="fcUpdateFloorOptions()">\
            <option value="sheet_vinyl">Sheet Vinyl</option>\
            <option value="carpet">Carpet</option>\
            <option value="padding">Carpet Padding</option>\
            <option value="lvp">LVP / Laminate (box calc)</option>\
            <option value="tile">Ceramic / Porcelain Tile (box calc)</option>\
        </select>\
    </div>\
    \
    <div id="fcRollSection">\
        <div class="fc-row">\
            <div class="fc-group">\
                <div class="fc-label">Roll Width (ft)</div>\
                <select class="fc-select" id="fcRollWidth">\
                    <option value="12">12\'</option>\
                    <option value="13.17">13\' 2" (13.17\')</option>\
                    <option value="6">6\'</option>\
                    <option value="15">15\'</option>\
                </select>\
            </div>\
            <div class="fc-group">\
                <div class="fc-label">Install Crew</div>\
                <select class="fc-select" id="fcCrew">\
                    <option value="solo">Solo Install</option>\
                    <option value="team">Team (2+ people)</option>\
                </select>\
            </div>\
        </div>\
    </div>\
    \
    <div id="fcBoxSection" style="display:none">\
        <div class="fc-row">\
            <div class="fc-group">\
                <div class="fc-label">Box Coverage (sq ft)</div>\
                <input type="number" class="fc-input" id="fcBoxCoverage" placeholder="23.64" step="0.01"/>\
            </div>\
            <div class="fc-group">\
                <div class="fc-label">Waste Factor %</div>\
                <input type="number" class="fc-input" id="fcWaste" value="10" step="1"/>\
            </div>\
        </div>\
    </div>\
    \
    <hr class="fc-divider"/>\
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">\
        <div class="fc-label" style="margin-bottom:0">Room Measurements</div>\
        <button onclick="fcAddRoom()" style="background:#27ae60;color:white;border:none;padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer;font-weight:600">+ Add Room</button>\
    </div>\
    <div id="fcRooms"></div>\
    \
    <button class="fc-btn" onclick="fcCalculateFlooring()">📐 Calculate Material Needed</button>\
    <div id="fcFloorResult"></div>\
</div>';
    }

    // ================================================================
    // DRYWALL TAB
    // ================================================================
    function buildDrywallTab() {
        return '\
<div class="fc-section" id="fcDrywall">\
    <div class="fc-group">\
        <div class="fc-label">Drywall Sheet Size</div>\
        <select class="fc-select" id="fcDwSize">\
            <option value="0">4\' × 8\' (32 sq ft)</option>\
            <option value="1">4\' × 10\' (40 sq ft)</option>\
            <option value="2">4\' × 12\' (48 sq ft)</option>\
        </select>\
    </div>\
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Drywall Thickness</div>\
            <select class="fc-select" id="fcDwThick">\
                <option value="0.5">1/2" (Standard)</option>\
                <option value="0.625">5/8" (Fire-Rated / Ceiling)</option>\
                <option value="0.375">3/8" (Re-cover)</option>\
            </select>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">Install Type</div>\
            <select class="fc-select" id="fcDwType">\
                <option value="walls">Walls Only</option>\
                <option value="ceiling">Ceiling Only</option>\
                <option value="both">Walls + Ceiling</option>\
            </select>\
        </div>\
    </div>\
    \
    <hr class="fc-divider"/>\
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">\
        <div class="fc-label" style="margin-bottom:0">Wall / Ceiling Measurements</div>\
        <button onclick="fcAddDwWall()" style="background:#27ae60;color:white;border:none;padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer;font-weight:600">+ Add Wall</button>\
    </div>\
    <div id="fcDwWalls"></div>\
    \
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Ceiling Length (ft) — if applicable</div>\
            <input type="number" class="fc-input" id="fcDwCeilL" placeholder="0" step="0.1"/>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">Ceiling Width (ft)</div>\
            <input type="number" class="fc-input" id="fcDwCeilW" placeholder="0" step="0.1"/>\
        </div>\
    </div>\
    \
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Windows to Deduct (#)</div>\
            <input type="number" class="fc-input" id="fcDwWindows" value="0" step="1"/>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">Doors to Deduct (#)</div>\
            <input type="number" class="fc-input" id="fcDwDoors" value="0" step="1"/>\
        </div>\
    </div>\
    \
    <button class="fc-btn" onclick="fcCalculateDrywall()">🧱 Calculate Drywall & Supplies</button>\
    <div id="fcDwResult"></div>\
</div>';
    }

    // ================================================================
    // TRIM & BASE TAB
    // ================================================================
    function buildTrimTab() {
        return '\
<div class="fc-section" id="fcTrim">\
    <div class="fc-group">\
        <div class="fc-label">Cove Base / Baseboard Type</div>\
        <select class="fc-select" id="fcBaseType">\
            <option value="cove_vinyl">Vinyl Cove Base (4" — 120ft coil or 48" sticks)</option>\
            <option value="cove_rubber">Rubber Cove Base (4" or 6")</option>\
            <option value="baseboard_mdf">MDF Baseboard (8ft or 16ft lengths)</option>\
            <option value="baseboard_wood">Wood Baseboard (8ft or 16ft lengths)</option>\
        </select>\
    </div>\
    \
    <hr class="fc-divider"/>\
    <div class="fc-label">Room Perimeter Measurements</div>\
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Total Wall Length (linear ft)</div>\
            <input type="number" class="fc-input" id="fcTrimPerimeter" placeholder="e.g. 52" step="0.1"/>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">OR enter each wall and I\'ll add them</div>\
            <input type="text" class="fc-input" id="fcTrimWalls" placeholder="e.g. 12, 14, 12, 14"/>\
        </div>\
    </div>\
    \
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Number of Doors</div>\
            <input type="number" class="fc-input" id="fcTrimDoors" value="1" step="1"/>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">Avg Door Width (ft)</div>\
            <input type="number" class="fc-input" id="fcTrimDoorWidth" value="3" step="0.1"/>\
        </div>\
    </div>\
    \
    <div class="fc-group">\
        <div class="fc-label">Waste Factor %</div>\
        <input type="number" class="fc-input" id="fcTrimWaste" value="10" step="1"/>\
    </div>\
    \
    <button class="fc-btn" onclick="fcCalculateTrim()">📏 Calculate Trim & Transitions</button>\
    \
    <hr class="fc-divider"/>\
    <div class="fc-label">Transition Strips</div>\
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Number of Transitions</div>\
            <input type="number" class="fc-input" id="fcTransCount" value="1" step="1"/>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">Doorway Width (ft)</div>\
            <input type="number" class="fc-input" id="fcTransWidth" value="3" step="0.1"/>\
        </div>\
    </div>\
    <div class="fc-group">\
        <div class="fc-label">Transition Type</div>\
        <select class="fc-select" id="fcTransType">\
            <option value="t_mold">T-Molding (same height)</option>\
            <option value="reducer">Reducer (different heights)</option>\
            <option value="threshold">Threshold / End Cap</option>\
            <option value="stair_nose">Stair Nose</option>\
        </select>\
    </div>\
    \
    <button class="fc-btn fc-btn-secondary" onclick="fcCalculateTransitions()" style="margin-top:4px">📏 Calculate Transitions</button>\
    <div id="fcTrimResult"></div>\
</div>';
    }

    // ================================================================
    // AI PLANNER TAB — Camera + Upload + Vision Analysis
    // ================================================================
    function buildAITab() {
        return '\
<div class="fc-section" id="fcAI">\
    <div class="fc-note" style="margin-top:0;margin-bottom:12px">\
        <strong>📸 Snap a photo</strong> of the room or upload one, and Gemini Vision will analyze seam placement, cut sizes for solo install, material direction, and give you a full plan. You can also type measurements below.\
    </div>\
    \
    <div class="fc-group">\
        <div class="fc-label">📷 Room Photo (camera or upload)</div>\
        <div style="display:flex;gap:6px;margin-bottom:8px;flex-wrap:wrap">\
            <button class="fc-btn fc-btn-secondary" onclick="fcOpenCamera()" style="flex:1;min-width:80px;font-size:11px;padding:10px 6px">📷 Photo</button>\
            <button class="fc-btn fc-btn-secondary" onclick="document.getElementById(\'fcFileInput\').click()" style="flex:1;min-width:80px;font-size:11px;padding:10px 6px">📁 Upload</button>\
            <button class="fc-btn fc-btn-secondary" onclick="fcOpenRoomScanner()" style="flex:1;min-width:80px;font-size:11px;padding:10px 6px;border-color:#8e44ad;color:#bb86fc">📐 Room Scanner</button>\
        </div>\
        <div style="font-size:10px;color:#7f8c8d;margin-bottom:8px">🥽 Room Scanner works with <strong style="color:#bb86fc">Meta Quest 3</strong> AR passthrough, phone camera, or 2D floorplan mode</div>\
        <input type="file" id="fcFileInput" accept="image/*" style="display:none" onchange="fcHandleFile(event)">\
        <div id="fcCameraContainer" style="display:none;margin-bottom:8px;border-radius:8px;overflow:hidden;position:relative">\
            <video id="fcCameraVideo" autoplay playsinline style="width:100%;border-radius:8px;background:#000"></video>\
            <div style="position:absolute;bottom:8px;left:0;right:0;text-align:center">\
                <button class="fc-btn" onclick="fcCapturePhoto()" style="display:inline-block;width:auto;padding:10px 24px;font-size:12px;border-radius:20px">📸 Capture</button>\
                <button class="fc-btn fc-btn-secondary" onclick="fcCloseCamera()" style="display:inline-block;width:auto;padding:10px 16px;font-size:12px;border-radius:20px;margin-left:6px">✕ Close</button>\
            </div>\
        </div>\
        <canvas id="fcCameraCanvas" style="display:none"></canvas>\
        <div id="fcPhotoPreview" style="display:none;margin-bottom:8px;position:relative">\
            <img id="fcPhotoImg" style="width:100%;border-radius:8px;border:2px solid #27ae60">\
            <button onclick="fcRemovePhoto()" style="position:absolute;top:4px;right:4px;background:#e74c3c;color:white;border:none;width:24px;height:24px;border-radius:50%;font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center">✕</button>\
            <div style="position:absolute;bottom:6px;left:6px;background:rgba(39,174,96,0.9);color:white;padding:3px 10px;border-radius:4px;font-size:10px;font-weight:600">✓ Photo attached — AI will analyze this</div>\
        </div>\
    </div>\
    \
    <div class="fc-group">\
        <div class="fc-label">Material Type</div>\
        <select class="fc-select" id="fcAIType">\
            <option value="sheet_vinyl">Sheet Vinyl</option>\
            <option value="carpet">Carpet</option>\
            <option value="lvp">LVP / Laminate</option>\
            <option value="tile">Tile</option>\
            <option value="drywall">Drywall</option>\
            <option value="other">Other (describe below)</option>\
        </select>\
    </div>\
    <div class="fc-group">\
        <div class="fc-label">Room Details & Measurements <span style="font-weight:400;color:#7f8c8d">(optional if photo provided)</span></div>\
        <textarea class="fc-input" id="fcAIInput" rows="5" style="resize:vertical;min-height:80px" placeholder="Example:\nLiving room: 14\'3\" × 18\'6\"\nHallway: 3\'8\" × 22\'\nRoll width: 12ft\nDoors: 3 standard\nLayout: L-shaped\n\nOr just snap a photo above!"></textarea>\
    </div>\
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Install Crew</div>\
            <select class="fc-select" id="fcAICrew">\
                <option value="solo">Solo (one man)</option>\
                <option value="team2">Team of 2</option>\
                <option value="team3">Team of 3+</option>\
            </select>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">Experience Level</div>\
            <select class="fc-select" id="fcAIExp">\
                <option value="experienced">Experienced</option>\
                <option value="intermediate">Intermediate</option>\
                <option value="newer">Newer to this material</option>\
            </select>\
        </div>\
    </div>\
    <button class="fc-btn" onclick="fcAIAnalyze()">🧠 AI Vision — Seam & Cut Planner</button>\
    <div id="fcAIResult" style="margin-top:12px"></div>\
</div>';
    }

    // ================================================================
    // TAB SWITCHING
    // ================================================================
    window.fcSwitchTab = function(tab) {
        document.querySelectorAll('.fc-tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.fc-section').forEach(function(s) { s.classList.remove('active'); });

        var tabMap = { flooring: 0, drywall: 1, trim: 2, ai: 3 };
        var sectionMap = { flooring: 'fcFlooring', drywall: 'fcDrywall', trim: 'fcTrim', ai: 'fcAI' };
        document.querySelectorAll('.fc-tab')[tabMap[tab]].classList.add('active');
        document.getElementById(sectionMap[tab]).classList.add('active');
    };

    // ================================================================
    // FLOOR TYPE CHANGE — show roll or box options
    // ================================================================
    window.fcUpdateFloorOptions = function() {
        var type = document.getElementById('fcFloorType').value;
        var rollSection = document.getElementById('fcRollSection');
        var boxSection = document.getElementById('fcBoxSection');
        var rollSelect = document.getElementById('fcRollWidth');

        if (type === 'lvp' || type === 'tile') {
            rollSection.style.display = 'none';
            boxSection.style.display = 'block';
            document.getElementById('fcBoxCoverage').placeholder = type === 'lvp' ? '23.64' : '10';
        } else {
            rollSection.style.display = 'block';
            boxSection.style.display = 'none';
            // Update roll width options
            var widths = ROLL_WIDTHS[type] || [12];
            rollSelect.innerHTML = widths.map(function(w) {
                var label = w === 13.17 ? "13' 2\" (13.17')" : w + "'";
                return '<option value="' + w + '">' + label + '</option>';
            }).join('');
        }
    };

    // ================================================================
    // ROOM MANAGEMENT (Flooring)
    // ================================================================
    var _fcRooms = [{ name: 'Room 1', length: '', width: '' }];

    window.fcAddRoom = function() {
        _fcRooms.push({ name: 'Room ' + (_fcRooms.length + 1), length: '', width: '' });
        fcRenderRooms();
    };

    window.fcRemoveRoom = function(i) {
        _fcRooms.splice(i, 1);
        fcRenderRooms();
    };

    function fcRenderRooms() {
        var el = document.getElementById('fcRooms');
        if (!el) return;
        el.innerHTML = _fcRooms.map(function(r, i) {
            return '\
<div class="fc-room-entry">\
    <div class="fc-room-header">\
        <input type="text" value="' + esc(r.name) + '" class="fc-input" style="width:120px;font-weight:600" onchange="_fcRooms[' + i + '].name=this.value"/>\
        ' + (_fcRooms.length > 1 ? '<button class="fc-remove" onclick="fcRemoveRoom(' + i + ')">×</button>' : '') + '\
    </div>\
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Length (ft)</div>\
            <input type="number" class="fc-input" value="' + (r.length||'') + '" placeholder="e.g. 14.5" step="0.01" onchange="_fcRooms[' + i + '].length=parseFloat(this.value)||0"/>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">Width (ft)</div>\
            <input type="number" class="fc-input" value="' + (r.width||'') + '" placeholder="e.g. 12" step="0.01" onchange="_fcRooms[' + i + '].width=parseFloat(this.value)||0"/>\
        </div>\
    </div>\
</div>';
        }).join('');
    }

    // Make _fcRooms accessible globally for inline handlers
    window._fcRooms = _fcRooms;

    // ================================================================
    // DRYWALL WALL MANAGEMENT
    // ================================================================
    var _fcDwWalls = [{ name: 'Wall 1', length: '', height: '' }];
    window._fcDwWalls = _fcDwWalls;

    window.fcAddDwWall = function() {
        _fcDwWalls.push({ name: 'Wall ' + (_fcDwWalls.length + 1), length: '', height: '' });
        fcRenderDwWalls();
    };

    window.fcRemoveDwWall = function(i) {
        _fcDwWalls.splice(i, 1);
        fcRenderDwWalls();
    };

    function fcRenderDwWalls() {
        var el = document.getElementById('fcDwWalls');
        if (!el) return;
        el.innerHTML = _fcDwWalls.map(function(w, i) {
            return '\
<div class="fc-room-entry">\
    <div class="fc-room-header">\
        <input type="text" value="' + esc(w.name) + '" class="fc-input" style="width:120px;font-weight:600" onchange="_fcDwWalls[' + i + '].name=this.value"/>\
        ' + (_fcDwWalls.length > 1 ? '<button class="fc-remove" onclick="fcRemoveDwWall(' + i + ')">×</button>' : '') + '\
    </div>\
    <div class="fc-row">\
        <div class="fc-group">\
            <div class="fc-label">Length (ft)</div>\
            <input type="number" class="fc-input" value="' + (w.length||'') + '" placeholder="e.g. 14" step="0.1" onchange="_fcDwWalls[' + i + '].length=parseFloat(this.value)||0"/>\
        </div>\
        <div class="fc-group">\
            <div class="fc-label">Height (ft)</div>\
            <input type="number" class="fc-input" value="' + (w.height||'') + '" placeholder="e.g. 8" step="0.1" onchange="_fcDwWalls[' + i + '].height=parseFloat(this.value)||0"/>\
        </div>\
    </div>\
</div>';
        }).join('');
    }

    // ================================================================
    // CALCULATE: FLOORING
    // ================================================================
    window.fcCalculateFlooring = function() {
        var type = document.getElementById('fcFloorType').value;
        var crew = document.getElementById('fcCrew') ? document.getElementById('fcCrew').value : 'solo';
        var rooms = _fcRooms.filter(function(r) { return r.length > 0 && r.width > 0; });

        if (rooms.length === 0) {
            notify('Enter at least one room with length and width');
            return;
        }

        var totalSqft = 0;
        rooms.forEach(function(r) { totalSqft += r.length * r.width; });

        var html = '';

        if (type === 'lvp' || type === 'tile') {
            // Box-based calculation
            var boxCoverage = parseFloat(document.getElementById('fcBoxCoverage').value) || (type === 'lvp' ? 23.64 : 10);
            var wastePct = parseFloat(document.getElementById('fcWaste').value) || 10;
            var totalWithWaste = totalSqft * (1 + wastePct / 100);
            var boxes = Math.ceil(totalWithWaste / boxCoverage);
            var actualCoverage = boxes * boxCoverage;
            var leftover = actualCoverage - totalSqft;

            html = '<div class="fc-result"><div class="fc-result-title">' + (type === 'lvp' ? 'LVP / Laminate' : 'Tile') + ' — Box Calculation</div>';
            rooms.forEach(function(r) {
                html += '<div class="fc-result-row"><span class="fc-result-label">' + esc(r.name) + ' (' + r.length + '\' × ' + r.width + '\')</span><span class="fc-result-value">' + (r.length * r.width).toFixed(1) + ' sq ft</span></div>';
            });
            html += '<div class="fc-result-row"><span class="fc-result-label">Total Area</span><span class="fc-result-value">' + totalSqft.toFixed(1) + ' sq ft</span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label">+ ' + wastePct + '% waste</span><span class="fc-result-value">' + totalWithWaste.toFixed(1) + ' sq ft</span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label">Box coverage</span><span class="fc-result-value">' + boxCoverage + ' sq ft/box</span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label"><strong>Boxes to Order</strong></span><span class="fc-result-value highlight"><strong>' + boxes + ' boxes</strong></span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label">Total coverage purchased</span><span class="fc-result-value">' + actualCoverage.toFixed(1) + ' sq ft</span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label">Leftover material</span><span class="fc-result-value">' + leftover.toFixed(1) + ' sq ft</span></div>';
            html += '<button class="fc-send-btn" onclick="fcSendToBidGen(\'material\',[{desc:\'' + esc(type === 'lvp' ? 'LVP / Laminate Flooring' : 'Porcelain / Ceramic Tile') + ' (' + boxes + ' boxes)\',qty:' + boxes + ',unit:\'box\',price:\'\'}])">📥 Add to BidGen Materials</button>';
            html += '</div>';

        } else {
            // Roll-based calculation
            var rollWidth = parseFloat(document.getElementById('fcRollWidth').value) || 12;
            var totalLinFt = 0;

            html = '<div class="fc-result"><div class="fc-result-title">' + capitalize(type.replace('_', ' ')) + ' — Roll Calculation (' + rollWidth + '\' wide)</div>';

            rooms.forEach(function(r) {
                // Determine optimal cut direction
                var sqft = r.length * r.width;
                var runA = r.length;  // roll runs along length
                var runB = r.width;   // roll runs along width

                var cutsA, linftA, cutsB, linftB;

                // Option A: roll runs along room length
                cutsA = Math.ceil(r.width / rollWidth);
                linftA = cutsA * r.length;

                // Option B: roll runs along room width
                cutsB = Math.ceil(r.length / rollWidth);
                linftB = cutsB * r.width;

                // Pick the one that uses less material
                var bestDir, bestCuts, bestLinft, seamCount;
                if (linftA <= linftB) {
                    bestDir = 'Roll runs ' + r.length + '\' (along length)';
                    bestCuts = cutsA;
                    bestLinft = linftA;
                } else {
                    bestDir = 'Roll runs ' + r.width + '\' (along width)';
                    bestCuts = cutsB;
                    bestLinft = linftB;
                }
                seamCount = bestCuts > 1 ? bestCuts - 1 : 0;
                totalLinFt += bestLinft;

                html += '<div style="background:#0f1a33;border:1px solid #1a2744;border-radius:6px;padding:10px;margin-bottom:8px">';
                html += '<div style="font-weight:700;color:#ecf0f1;margin-bottom:6px">' + esc(r.name) + ' — ' + r.length + '\' × ' + r.width + '\' (' + sqft.toFixed(1) + ' sq ft)</div>';
                html += '<div class="fc-result-row"><span class="fc-result-label">Best direction</span><span class="fc-result-value">' + bestDir + '</span></div>';
                html += '<div class="fc-result-row"><span class="fc-result-label">Cuts from roll</span><span class="fc-result-value">' + bestCuts + ' piece(s)</span></div>';
                html += '<div class="fc-result-row"><span class="fc-result-label">Seams</span><span class="fc-result-value">' + seamCount + '</span></div>';
                html += '<div class="fc-result-row"><span class="fc-result-label">Linear feet of roll</span><span class="fc-result-value highlight">' + bestLinft.toFixed(1) + ' lf</span></div>';
                html += '</div>';
            });

            var wasteFt = totalLinFt * 0.10;
            var orderLinFt = Math.ceil(totalLinFt + wasteFt);
            var orderSqYd = (orderLinFt * rollWidth / 9).toFixed(1);

            html += '<div class="fc-result-row"><span class="fc-result-label">Total linear feet</span><span class="fc-result-value">' + totalLinFt.toFixed(1) + ' lf</span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label">+ 10% waste</span><span class="fc-result-value">' + wasteFt.toFixed(1) + ' lf</span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label"><strong>Order Amount</strong></span><span class="fc-result-value highlight"><strong>' + orderLinFt + ' lf (' + orderSqYd + ' sq yd)</strong></span></div>';
            var matName = capitalize(type.replace('_', ' '));
            html += '<button class="fc-send-btn" onclick="fcSendToBidGen(\'material\',[{desc:\'' + esc(matName) + ' (' + rollWidth + "\\' wide, " + orderLinFt + ' lf)\',qty:' + orderSqYd + ',unit:\'sq yd\',price:\'\'}])">📥 Add to BidGen Materials</button>';
            html += '</div>';
        }

        // Install time estimate
        var hoursPerSqft = { sheet_vinyl: 0.04, carpet: 0.03, padding: 0.015, lvp: 0.035, tile: 0.06 };
        var baseHours = totalSqft * (hoursPerSqft[type] || 0.04);
        var soloHours = Math.ceil(baseHours * 10) / 10;
        var teamHours = Math.ceil((baseHours * 0.6) * 10) / 10;

        html += '<div class="fc-result" style="margin-top:8px"><div class="fc-result-title">⏱️ Install Time Estimate</div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Solo install</span><span class="fc-result-value">' + soloHours + ' hrs (~' + Math.ceil(soloHours / 8) + ' day' + (Math.ceil(soloHours / 8) > 1 ? 's' : '') + ')</span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Team of 2</span><span class="fc-result-value">' + teamHours + ' hrs (~' + Math.ceil(teamHours / 8) + ' day' + (Math.ceil(teamHours / 8) > 1 ? 's' : '') + ')</span></div>';
        html += '<div class="fc-note">Times include prep, layout, install. Add extra for demo, leveling, or complex cuts. ' + (crew === 'solo' ? '<strong>Solo tip:</strong> For sheet goods, pre-cut in staging area and carry to install location. Use knee kicker and carpet tape for seams.' : '<strong>Team tip:</strong> One person holds/feeds, one seams and trims. Much faster and cleaner.') + '</div>';
        html += '</div>';

        document.getElementById('fcFloorResult').innerHTML = html;
    };

    // ================================================================
    // CALCULATE: DRYWALL
    // ================================================================
    window.fcCalculateDrywall = function() {
        var sizeIdx = parseInt(document.getElementById('fcDwSize').value);
        var sheet = DRYWALL_SIZES[sizeIdx];
        var installType = document.getElementById('fcDwType').value;
        var walls = _fcDwWalls.filter(function(w) { return w.length > 0 && w.height > 0; });
        var windowCount = parseInt(document.getElementById('fcDwWindows').value) || 0;
        var doorCount = parseInt(document.getElementById('fcDwDoors').value) || 0;
        var ceilL = parseFloat(document.getElementById('fcDwCeilL').value) || 0;
        var ceilW = parseFloat(document.getElementById('fcDwCeilW').value) || 0;

        if (walls.length === 0 && installType !== 'ceiling') {
            notify('Enter at least one wall measurement');
            return;
        }

        var wallSqft = 0;
        walls.forEach(function(w) { wallSqft += w.length * w.height; });

        // Deductions: avg window ~15 sqft, avg door ~21 sqft
        var deductSqft = (windowCount * 15) + (doorCount * 21);
        var netWallSqft = Math.max(0, wallSqft - deductSqft);

        var ceilSqft = ceilL * ceilW;
        var totalSqft = 0;
        if (installType === 'walls') totalSqft = netWallSqft;
        else if (installType === 'ceiling') totalSqft = ceilSqft;
        else totalSqft = netWallSqft + ceilSqft;

        // Add 10% waste
        var totalWithWaste = totalSqft * 1.10;
        var sheets = Math.ceil(totalWithWaste / sheet.sqft);

        // Supplies calculation
        var screws = Math.ceil(totalSqft * 1.5);              // ~1.5 screws per sq ft (32 screws per sheet on 16" OC)
        var screwBoxes = Math.ceil(screws / 150);              // typical box = 150 screws
        var mudBuckets = Math.ceil(totalSqft / 475);           // 1 bucket all-purpose per ~475 sqft
        var tapeRolls = Math.ceil(totalSqft / 370);            // 1 roll (500ft) per ~370 sqft
        var cornerBead = 0;
        walls.forEach(function(w) { cornerBead += w.height; });// rough estimate: 1 piece per wall height for outside corners
        // More realistic: user would specify corners, but we estimate

        var html = '<div class="fc-result"><div class="fc-result-title">🧱 Drywall Calculation — ' + sheet.label + '</div>';

        if (installType !== 'ceiling') {
            walls.forEach(function(w) {
                html += '<div class="fc-result-row"><span class="fc-result-label">' + esc(w.name) + ' (' + w.length + '\' × ' + w.height + '\')</span><span class="fc-result-value">' + (w.length * w.height).toFixed(0) + ' sq ft</span></div>';
            });
            html += '<div class="fc-result-row"><span class="fc-result-label">Gross wall area</span><span class="fc-result-value">' + wallSqft.toFixed(0) + ' sq ft</span></div>';
            if (deductSqft > 0) {
                html += '<div class="fc-result-row"><span class="fc-result-label">Deductions (' + windowCount + ' windows, ' + doorCount + ' doors)</span><span class="fc-result-value">-' + deductSqft.toFixed(0) + ' sq ft</span></div>';
            }
            html += '<div class="fc-result-row"><span class="fc-result-label">Net wall area</span><span class="fc-result-value">' + netWallSqft.toFixed(0) + ' sq ft</span></div>';
        }
        if (installType !== 'walls' && ceilSqft > 0) {
            html += '<div class="fc-result-row"><span class="fc-result-label">Ceiling area</span><span class="fc-result-value">' + ceilSqft.toFixed(0) + ' sq ft</span></div>';
        }
        html += '<div class="fc-result-row"><span class="fc-result-label">Total + 10% waste</span><span class="fc-result-value">' + totalWithWaste.toFixed(0) + ' sq ft</span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label"><strong>Sheets to Order</strong></span><span class="fc-result-value highlight"><strong>' + sheets + ' sheets (' + sheet.label + ')</strong></span></div>';
        html += '</div>';

        // Supplies
        html += '<div class="fc-result" style="margin-top:8px"><div class="fc-result-title">📦 Supplies Needed</div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Drywall screws</span><span class="fc-result-value">~' + screws + ' screws (' + screwBoxes + ' box' + (screwBoxes > 1 ? 'es' : '') + ' of 150)</span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Joint compound (all-purpose)</span><span class="fc-result-value">' + mudBuckets + ' bucket' + (mudBuckets > 1 ? 's' : '') + ' (4.5 gal)</span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Paper tape</span><span class="fc-result-value">' + tapeRolls + ' roll' + (tapeRolls > 1 ? 's' : '') + ' (500ft)</span></div>';
        html += '<div class="fc-note"><strong>Also bring:</strong> Drywall knife set (6", 10", 12"), T-square, utility knife, screw gun, drywall rasp, mud pan, sanding block. For ceilings: drywall lift or at least a deadman brace.</div>';
        html += '<button class="fc-send-btn" onclick="fcSendToBidGen(\'material\',[{desc:\'Drywall Sheets (' + sheet.label + ')\',qty:' + sheets + ',unit:\'sheet\',price:\'\'},{desc:\'Drywall Screws (box of 150)\',qty:' + screwBoxes + ',unit:\'box\',price:\'\'},{desc:\'Joint Compound (4.5 gal)\',qty:' + mudBuckets + ',unit:\'bucket\',price:\'\'},{desc:\'Paper Tape (500ft roll)\',qty:' + tapeRolls + ',unit:\'roll\',price:\'\'}])">📥 Add All to BidGen Materials</button>';
        html += '</div>';

        document.getElementById('fcDwResult').innerHTML = html;
    };

    // ================================================================
    // CALCULATE: TRIM / COVE BASE
    // ================================================================
    window.fcCalculateTrim = function() {
        var baseType = document.getElementById('fcBaseType').value;
        var perimeterInput = parseFloat(document.getElementById('fcTrimPerimeter').value) || 0;
        var wallsInput = document.getElementById('fcTrimWalls').value.trim();
        var doorCount = parseInt(document.getElementById('fcTrimDoors').value) || 0;
        var doorWidth = parseFloat(document.getElementById('fcTrimDoorWidth').value) || 3;
        var wastePct = parseFloat(document.getElementById('fcTrimWaste').value) || 10;

        // Calculate perimeter from individual walls if provided
        var perimeter = perimeterInput;
        if (!perimeter && wallsInput) {
            var wallLengths = wallsInput.split(/[,;\s]+/).map(function(v) { return parseFloat(v) || 0; });
            perimeter = wallLengths.reduce(function(a, b) { return a + b; }, 0);
        }

        if (perimeter <= 0) {
            notify('Enter a total perimeter or individual wall lengths');
            return;
        }

        var doorDeduction = doorCount * doorWidth;
        var netPerimeter = perimeter - doorDeduction;
        var withWaste = netPerimeter * (1 + wastePct / 100);

        // Material-specific calculations
        var html = '<div class="fc-result"><div class="fc-result-title">📏 ' + formatBaseType(baseType) + ' Calculation</div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Total perimeter</span><span class="fc-result-value">' + perimeter.toFixed(1) + ' lf</span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Door deductions (' + doorCount + ' × ' + doorWidth + '\')</span><span class="fc-result-value">-' + doorDeduction.toFixed(1) + ' lf</span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Net baseboard needed</span><span class="fc-result-value">' + netPerimeter.toFixed(1) + ' lf</span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">+ ' + wastePct + '% waste</span><span class="fc-result-value">' + withWaste.toFixed(1) + ' lf</span></div>';

        if (baseType.startsWith('cove')) {
            // Vinyl/rubber cove base — sold in 120ft coils or boxes of 16 sticks (48" = 4ft each = 64 lf)
            var coils = Math.ceil(withWaste / 120);
            var sticks = Math.ceil(withWaste / 4);
            var boxes = Math.ceil(sticks / 16);
            html += '<div class="fc-result-row"><span class="fc-result-label"><strong>Order (coils)</strong></span><span class="fc-result-value highlight"><strong>' + coils + ' coil' + (coils > 1 ? 's' : '') + ' (120 lf each)</strong></span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label"><strong>OR sticks</strong></span><span class="fc-result-value highlight"><strong>' + sticks + ' sticks (' + boxes + ' box' + (boxes > 1 ? 'es' : '') + ' of 16)</strong></span></div>';
            // Adhesive
            var adhesiveTubes = Math.ceil(withWaste / 50); // ~50 lf per tube of cove base adhesive
            html += '<div class="fc-result-row"><span class="fc-result-label">Cove base adhesive</span><span class="fc-result-value">' + adhesiveTubes + ' tube' + (adhesiveTubes > 1 ? 's' : '') + '</span></div>';
            html += '<button class="fc-send-btn" onclick="fcSendToBidGen(\'material\',[{desc:\'' + esc(formatBaseType(baseType)) + ' (' + Math.ceil(withWaste) + ' lf)\',qty:' + coils + ',unit:\'coil\',price:\'\'},{desc:\'Cove Base Adhesive\',qty:' + adhesiveTubes + ',unit:\'tube\',price:\'\'}])">📥 Add to BidGen Materials</button>';
        } else {
            // MDF/Wood baseboard — sold in 8ft or 16ft lengths
            var pieces8 = Math.ceil(withWaste / 8);
            var pieces16 = Math.ceil(withWaste / 16);
            html += '<div class="fc-result-row"><span class="fc-result-label"><strong>Order (8ft pieces)</strong></span><span class="fc-result-value highlight"><strong>' + pieces8 + ' pieces</strong></span></div>';
            html += '<div class="fc-result-row"><span class="fc-result-label"><strong>OR (16ft pieces)</strong></span><span class="fc-result-value highlight"><strong>' + pieces16 + ' pieces</strong></span></div>';
            // Nails
            html += '<div class="fc-result-row"><span class="fc-result-label">Finish nails (18ga × 2")</span><span class="fc-result-value">~' + Math.ceil(withWaste * 2) + ' nails</span></div>';
            html += '<button class="fc-send-btn" onclick="fcSendToBidGen(\'material\',[{desc:\'' + esc(formatBaseType(baseType)) + ' (8ft pieces)\',qty:' + pieces8 + ',unit:\'pc\',price:\'\'}])">📥 Add to BidGen Materials</button>';
        }

        // Inside/outside corners
        html += '<div class="fc-note"><strong>Don\'t forget corners:</strong> Count your inside corners (standard rooms) and outside corners (columns, bump-outs). You\'ll need pre-formed corners or miter cuts. Add 1 tube of caulk per ~50 lf for top-edge finish.</div>';
        html += '</div>';

        document.getElementById('fcTrimResult').innerHTML = html;
    };

    // ================================================================
    // CALCULATE: TRANSITIONS
    // ================================================================
    window.fcCalculateTransitions = function() {
        var count = parseInt(document.getElementById('fcTransCount').value) || 0;
        var width = parseFloat(document.getElementById('fcTransWidth').value) || 3;
        var type = document.getElementById('fcTransType').value;

        var typeNames = { t_mold: 'T-Molding', reducer: 'Reducer', threshold: 'Threshold / End Cap', stair_nose: 'Stair Nose' };
        var totalLf = count * width;
        // Transitions typically sold in 36" (3ft) or 72" (6ft) lengths
        var pieces36 = Math.ceil(totalLf / 3);
        var pieces72 = Math.ceil(totalLf / 6);

        var el = document.getElementById('fcTrimResult');
        var html = el.innerHTML;
        html += '<div class="fc-result" style="margin-top:8px"><div class="fc-result-title">🚪 Transition Strips — ' + typeNames[type] + '</div>';
        html += '<div class="fc-result-row"><span class="fc-result-label">Doorways</span><span class="fc-result-value">' + count + ' × ' + width + '\' = ' + totalLf.toFixed(1) + ' lf</span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label"><strong>Order (36" pieces)</strong></span><span class="fc-result-value highlight"><strong>' + pieces36 + ' piece' + (pieces36 > 1 ? 's' : '') + '</strong></span></div>';
        html += '<div class="fc-result-row"><span class="fc-result-label"><strong>OR (72" pieces)</strong></span><span class="fc-result-value highlight"><strong>' + pieces72 + ' piece' + (pieces72 > 1 ? 's' : '') + '</strong></span></div>';
        html += '<div class="fc-note"><strong>Track system:</strong> Most transitions need a metal track fastened to the subfloor. ' + (type === 'stair_nose' ? 'Stair nosing is glued + nailed — no track.' : 'Buy matching track if not included.') + '</div>';
        html += '</div>';

        el.innerHTML = html;
    };

    // ================================================================
    // CAMERA / PHOTO UPLOAD — capture or upload room photos
    // ================================================================
    var _fcPhotoBase64 = null; // stored photo as base64 data URL
    var _fcCameraStream = null;

    // ── Room Scanner launcher + data receiver ──
    window.fcOpenRoomScanner = function() {
        window.open('room-scanner.html', 'roomScanner', 'width=900,height=700');
    };

    // Listen for data coming back from Room Scanner
    window.addEventListener('message', function(e) {
        if (!e.data || e.data.type !== 'roomScannerData') return;
        // Fill in measurements textarea
        var input = document.getElementById('fcAIInput');
        if (input && e.data.measurements) {
            input.value = (input.value ? input.value + '\n\n' : '') + e.data.measurements;
        }
        // Attach photo if scanner sent one
        if (e.data.photo) {
            _fcPhotoBase64 = e.data.photo;
            fcShowPhotoPreview(e.data.photo);
        }
        notify('Room Scanner data received!');
        // Switch to AI tab
        if (typeof fcSwitchTab === 'function') fcSwitchTab('ai');
    });

    // Also check sessionStorage/localStorage on load (if scanner redirected here)
    (function checkScannerData() {
        var raw = null;
        try { raw = sessionStorage.getItem('roomScannerData'); sessionStorage.removeItem('roomScannerData'); } catch(e) {}
        if (!raw) try { raw = localStorage.getItem('roomScannerData'); localStorage.removeItem('roomScannerData'); } catch(e) {}
        if (!raw) return;
        try {
            var data = JSON.parse(raw);
            var input = document.getElementById('fcAIInput');
            if (input && data.measurements) {
                input.value = (input.value ? input.value + '\n\n' : '') + data.measurements;
            }
            if (data.photo) {
                _fcPhotoBase64 = data.photo;
                fcShowPhotoPreview(data.photo);
            }
            notify('Room Scanner data loaded!');
        } catch(e) {}
    })();

    window.fcOpenCamera = function() {
        var container = document.getElementById('fcCameraContainer');
        var video = document.getElementById('fcCameraVideo');

        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            notify('Camera not available — use the upload button instead');
            return;
        }

        container.style.display = 'block';
        navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } }
        })
        .then(function(stream) {
            _fcCameraStream = stream;
            video.srcObject = stream;
        })
        .catch(function(err) {
            container.style.display = 'none';
            notify('Camera access denied — use the upload button');
        });
    };

    window.fcCloseCamera = function() {
        var container = document.getElementById('fcCameraContainer');
        var video = document.getElementById('fcCameraVideo');
        container.style.display = 'none';
        if (_fcCameraStream) {
            _fcCameraStream.getTracks().forEach(function(t) { t.stop(); });
            _fcCameraStream = null;
        }
        video.srcObject = null;
    };

    window.fcCapturePhoto = function() {
        var video = document.getElementById('fcCameraVideo');
        var canvas = document.getElementById('fcCameraCanvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        // Compress to JPEG, max ~1MB for Gemini
        var quality = 0.8;
        var dataUrl = canvas.toDataURL('image/jpeg', quality);
        // If too large, reduce quality
        while (dataUrl.length > 1400000 && quality > 0.3) {
            quality -= 0.1;
            dataUrl = canvas.toDataURL('image/jpeg', quality);
        }

        _fcPhotoBase64 = dataUrl;
        fcShowPhotoPreview(dataUrl);
        fcCloseCamera();
        notify('Photo captured — hit the AI button to analyze');
    };

    window.fcHandleFile = function(e) {
        var file = e.target.files && e.target.files[0];
        if (!file) return;

        var reader = new FileReader();
        reader.onload = function(ev) {
            // Resize if needed to keep under ~1.5MB for Gemini
            var img = new Image();
            img.onload = function() {
                var canvas = document.getElementById('fcCameraCanvas');
                var maxDim = 1920;
                var w = img.width, h = img.height;
                if (w > maxDim || h > maxDim) {
                    if (w > h) { h = Math.round(h * maxDim / w); w = maxDim; }
                    else { w = Math.round(w * maxDim / h); h = maxDim; }
                }
                canvas.width = w;
                canvas.height = h;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, w, h);
                var quality = 0.8;
                var dataUrl = canvas.toDataURL('image/jpeg', quality);
                while (dataUrl.length > 1400000 && quality > 0.3) {
                    quality -= 0.1;
                    dataUrl = canvas.toDataURL('image/jpeg', quality);
                }
                _fcPhotoBase64 = dataUrl;
                fcShowPhotoPreview(dataUrl);
                notify('Photo loaded — hit the AI button to analyze');
            };
            img.src = ev.target.result;
        };
        reader.readAsDataURL(file);
        // Reset input so same file can be re-selected
        e.target.value = '';
    };

    function fcShowPhotoPreview(dataUrl) {
        var preview = document.getElementById('fcPhotoPreview');
        var img = document.getElementById('fcPhotoImg');
        img.src = dataUrl;
        preview.style.display = 'block';
    }

    window.fcRemovePhoto = function() {
        _fcPhotoBase64 = null;
        document.getElementById('fcPhotoPreview').style.display = 'none';
        document.getElementById('fcPhotoImg').src = '';
    };

    // ================================================================
    // AI VISION CUT & INSTALL PLANNER (Gemini 2.5 Pro Vision)
    // ================================================================
    window.fcAIAnalyze = function() {
        var matType = document.getElementById('fcAIType').value;
        var input = document.getElementById('fcAIInput').value.trim();
        var crew = document.getElementById('fcAICrew').value;
        var exp = document.getElementById('fcAIExp').value;
        var hasPhoto = !!_fcPhotoBase64;

        if (!input && !hasPhoto) {
            notify('Take a photo or enter room measurements');
            return;
        }

        var resultEl = document.getElementById('fcAIResult');
        var loadMsg = hasPhoto ? 'Analyzing room photo + measurements with Gemini Vision...' : 'Analyzing measurements with Gemini AI...';
        resultEl.innerHTML = '<div style="text-align:center;padding:20px;color:#7f8c8d"><div class="spinner" style="width:32px;height:32px;border:3px solid #2a3a5c;border-top-color:#e67e22;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 10px"></div>' + loadMsg + '</div><style>@keyframes spin{to{transform:rotate(360deg)}}</style>';

        var isSolo = crew === 'solo';
        var soloSection = isSolo ? [
            '',
            '## CRITICAL — SOLO (ONE MAN) INSTALL REQUIREMENTS:',
            'This is a ONE-PERSON install. Every recommendation must account for:',
            '- **Maximum manageable piece size** for one person to carry, position, and lay flat without wrinkles or misalignment',
            '- For sheet vinyl/carpet: maximum piece a solo installer can handle is typically 12ft × 10-12ft. Larger pieces MUST be cut down or you need a different strategy.',
            '- **Reduce cut sizes** so one person can fold, carry, and position each piece alone',
            '- **Seam placement** should allow pieces small enough for solo handling — even if it means one extra seam',
            '- **Install sequence** must be step-by-step for one person — what to dry-fit first, where to start adhesive, how to avoid trapping yourself',
            '- **Weight and bulk** considerations — a full 12ft wide × 20ft carpet piece weighs 60-80 lbs and is nearly impossible solo',
            '- Recommend folding techniques, kick methods, and solo tricks for each step',
            ''
        ].join('\n') : '';

        var photoSection = hasPhoto ? [
            '',
            '## ROOM PHOTO ATTACHED',
            'I have attached a photo of the room. Analyze the photo carefully:',
            '- **Estimate room dimensions** from visual cues (doorways are ~6\'8\" tall × 2\'8\"-3\'0\" wide, outlets are 12\" from floor, etc.)',
            '- **Identify the room shape** — is it rectangular, L-shaped, has alcoves, closets, bump-outs?',
            '- **Count doorways and transitions** visible in the photo',
            '- **Assess the subfloor** if visible (concrete, plywood, existing flooring)',
            '- **Note any obstacles** — cabinets, islands, pipes, odd angles, fixtures',
            '- **Recommend optimal seam location** based on the actual room layout you see',
            '- **Recommend best direction** to run the material based on light sources, room shape, traffic flow',
            ''
        ].join('\n') : '';

        var prompt = [
            'You are a master flooring and trades installation expert with 30 years of field experience. You are advising a real installer on a real job.',
            hasPhoto ? 'A photo of the room has been provided — analyze it carefully along with any measurements.' : '',
            '',
            '## Material: ' + matType.replace('_', ' ').toUpperCase(),
            '## Crew: ' + crew + (isSolo ? ' (ONE MAN — size ALL cuts for solo handling)' : ''),
            '## Experience: ' + exp,
            photoSection,
            soloSection,
            input ? '## Field Measurements & Room Details:\n' + input : '## No written measurements provided — estimate from the photo.',
            '',
            '## REQUIRED OUTPUT:',
            '1. **Room Assessment** — shape, dimensions (estimated if from photo), total sq ft, obstacles',
            '2. **Best Seam Placement** — EXACTLY where the seam(s) should go, why that spot minimizes visibility, and how it aligns with traffic patterns and light. If no seam needed, say so.',
            '3. **Material Direction** — which way to run the material and why (lengthwise vs widthwise, with or against light)',
            '4. **Total Material Order** — exact quantity with ' + (matType === 'carpet' || matType === 'sheet_vinyl' ? '10-15% waste' : '10% waste'),
            '5. **Cut List** — every piece with exact dimensions' + (isSolo ? ', sized so one person can handle each piece' : '') + '. Use a table.',
            '6. **Step-by-Step Install Sequence** — numbered steps' + (isSolo ? ' written for a solo installer' : '') + ', including dry-fit, trim, adhesive/tape, seaming, rolling',
            '7. **Time Estimate** — realistic hours for ' + crew + ' at ' + exp + ' level',
            '8. **Watch-Outs** — specific areas where mistakes happen on THIS job',
            '9. **Tools Needed** — every tool required',
            '',
            'Be thorough. Use tables for the cut list. Bold all measurements. This is a REAL job — accuracy matters. Think step by step.'
        ].join('\n');

        // Build the request parts — text + optional image
        var parts = [{ text: prompt }];
        if (hasPhoto) {
            // Extract base64 data and mime type from data URL
            var match = _fcPhotoBase64.match(/^data:(image\/\w+);base64,(.+)$/);
            if (match) {
                parts.unshift({
                    inlineData: {
                        mimeType: match[1],
                        data: match[2]
                    }
                });
            }
        }

        var body = {
            contents: [{ role: 'user', parts: parts }],
            generationConfig: {
                maxOutputTokens: 32768,
                temperature: 0.3
            }
        };

        fetch(PROXY + '?model=gemini-2.5-pro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        })
        .then(function(res) { return res.json(); })
        .then(function(data) {
            var text = '';
            try { text = data.candidates[0].content.parts[0].text; } catch(e) { text = 'Error parsing AI response. Raw: ' + JSON.stringify(data).substring(0, 300); }
            resultEl.innerHTML = '<div class="fc-result" style="max-height:500px;overflow-y:auto"><div class="fc-result-title">' + (hasPhoto ? '📸🧠' : '🧠') + ' AI Vision — Seam & Cut Plan</div><div style="font-size:12px;line-height:1.7;color:#bdc3c7">' + renderMarkdown(text) + '</div></div>';
        })
        .catch(function(err) {
            resultEl.innerHTML = '<div class="fc-result" style="border-color:#e74c3c"><div style="color:#e74c3c;font-weight:600">❌ Error: ' + err.message + '</div></div>';
        });
    };

    // ================================================================
    // SIMPLE MARKDOWN RENDERER
    // ================================================================
    function renderMarkdown(text) {
        return text
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/^### (.+)$/gm, '<h4 style="color:#e67e22;margin:12px 0 6px;font-size:13px">$1</h4>')
            .replace(/^## (.+)$/gm, '<h3 style="color:#ecf0f1;margin:14px 0 6px;font-size:14px;border-bottom:1px solid #2a3a5c;padding-bottom:4px">$1</h3>')
            .replace(/\*\*(.+?)\*\*/g, '<strong style="color:#ecf0f1">$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code style="background:#16213e;padding:1px 4px;border-radius:3px;font-size:11px;color:#e67e22">$1</code>')
            .replace(/^\|(.+)\|$/gm, function(match) {
                var cells = match.split('|').filter(function(c) { return c.trim(); });
                var isHeader = cells.every(function(c) { return /^[\s-:]+$/.test(c); });
                if (isHeader) return '';
                var tag = 'td';
                return '<tr>' + cells.map(function(c) { return '<' + tag + ' style="padding:4px 8px;border:1px solid #2a3a5c;font-size:11px">' + c.trim() + '</' + tag + '>'; }).join('') + '</tr>';
            })
            .replace(/(<tr>.*<\/tr>\n?)+/g, '<table style="width:100%;border-collapse:collapse;margin:8px 0;background:#0f1a33">$&</table>')
            .replace(/^- (.+)$/gm, '<div style="padding-left:12px;margin:2px 0">• $1</div>')
            .replace(/^\d+\. (.+)$/gm, function(m, p1, off, str) { return '<div style="padding-left:12px;margin:2px 0">' + m.match(/^\d+/)[0] + '. ' + p1 + '</div>'; })
            .replace(/\n\n/g, '<br/><br/>')
            .replace(/\n/g, '<br/>');
    }

    // ================================================================
    // CLEAR ALL
    // ================================================================
    window.fieldCalcClearAll = function() {
        _fcRooms.length = 0;
        _fcRooms.push({ name: 'Room 1', length: '', width: '' });
        _fcDwWalls.length = 0;
        _fcDwWalls.push({ name: 'Wall 1', length: '', height: '' });
        fcRenderRooms();
        fcRenderDwWalls();
        document.getElementById('fcFloorResult').innerHTML = '';
        document.getElementById('fcDwResult').innerHTML = '';
        document.getElementById('fcTrimResult').innerHTML = '';
        document.getElementById('fcAIResult').innerHTML = '';
        // Clear photo
        _fcPhotoBase64 = null;
        var preview = document.getElementById('fcPhotoPreview');
        if (preview) preview.style.display = 'none';
        var photoImg = document.getElementById('fcPhotoImg');
        if (photoImg) photoImg.src = '';
        // Reset inputs
        var inputs = document.querySelectorAll('#fieldCalcPanel input[type="number"]');
        inputs.forEach(function(inp) { if (!inp.value || inp.id === 'fcTrimDoors' || inp.id === 'fcTransCount') return; });
    };

    // ================================================================
    // SEND TO BIDGEN — push calculated materials into main form
    // ================================================================
    window.fcSendToBidGen = function(type, items) {
        // type: 'labor' or 'material'
        // items: array of { desc, qty, unit, price }
        if (!items || !items.length) return;

        items.forEach(function(item) {
            if (type === 'material' && typeof addMatRow === 'function') {
                addMatRow(item.desc || '', item.qty || '', item.price || '');
            } else if (type === 'labor' && typeof addLaborRow === 'function') {
                addLaborRow(item.desc || '', item.qty || '', item.price || '');
            }
        });

        // Recalculate live totals
        if (typeof liveCalc === 'function') liveCalc();
        notify('Added ' + items.length + ' item' + (items.length > 1 ? 's' : '') + ' to BidGen form');
    };

    // ================================================================
    // HELPERS
    // ================================================================
    function esc(s) { var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
    function capitalize(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''; }
    function formatBaseType(t) {
        var map = { cove_vinyl: 'Vinyl Cove Base', cove_rubber: 'Rubber Cove Base', baseboard_mdf: 'MDF Baseboard', baseboard_wood: 'Wood Baseboard' };
        return map[t] || t;
    }
    function notify(msg) {
        if (typeof showNotification === 'function') { showNotification(msg, 'success'); return; }
        // Fallback toast
        var toast = document.createElement('div');
        toast.textContent = msg;
        toast.style.cssText = 'position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:#27ae60;color:white;padding:10px 20px;border-radius:8px;font-size:13px;font-weight:600;z-index:99999;box-shadow:0 4px 12px rgba(0,0,0,0.3);transition:opacity 0.3s';
        document.body.appendChild(toast);
        setTimeout(function() { toast.style.opacity = '0'; setTimeout(function() { toast.remove(); }, 300); }, 2500);
    }

    // ================================================================
    // GENERATE FULL BID — Collects all field calc data, sends to
    // Gemini for structured bid JSON, auto-populates BidGen form
    // ================================================================
    window.fcGenerateBid = async function() {
        // 1. Collect ALL field calc data
        var floorType = document.getElementById('fcFloorType') ? document.getElementById('fcFloorType').value : '';
        var rooms = (_fcRooms || []).filter(function(r) { return r.length > 0 && r.width > 0; });
        var dwWalls = (_fcDwWalls || []).filter(function(w) { return w.length > 0 && w.height > 0; });
        var trimPerim = parseFloat((document.getElementById('fcTrimPerimeter') || {}).value) || 0;
        var trimWallsStr = (document.getElementById('fcTrimWalls') || {}).value || '';
        var trimDoors = parseInt((document.getElementById('fcTrimDoors') || {}).value) || 0;
        var transCount = parseInt((document.getElementById('fcTransCount') || {}).value) || 0;
        var transType = (document.getElementById('fcTransType') || {}).value || '';

        if (rooms.length === 0 && dwWalls.length === 0 && trimPerim <= 0 && !trimWallsStr) {
            notify('Enter at least one room or wall measurement first');
            return;
        }

        // Compute totals for context
        var totalSqft = 0;
        rooms.forEach(function(r) { totalSqft += r.length * r.width; });
        var totalWallSqft = 0;
        dwWalls.forEach(function(w) { totalWallSqft += w.length * w.height; });

        // Get the current trade type from BidGen if available
        var tradeEl = document.getElementById('tradeType');
        var currentTrade = tradeEl ? tradeEl.value : 'flooring';
        var jobCity = (document.getElementById('jobCity') || {}).value || 'Norfolk, NE';

        // 2. Build the Gemini prompt
        var roomsDesc = rooms.map(function(r) {
            return '  - ' + r.name + ': ' + r.length + '\' × ' + r.width + '\' (' + (r.length * r.width).toFixed(1) + ' sq ft)';
        }).join('\n');

        var dwDesc = dwWalls.map(function(w) {
            return '  - ' + w.name + ': ' + w.length + '\' × ' + w.height + '\' (' + (w.length * w.height).toFixed(0) + ' sq ft)';
        }).join('\n');

        var prompt = [
            'You are a senior general contracting estimator for Nebraska. You are generating a REAL bid — every number must be defensible.',
            '',
            '## ABSOLUTE RULES — NO EXCEPTIONS:',
            '1. **NEVER hallucinate.** Do NOT invent measurements, prices, or quantities that were not provided or cannot be calculated from the provided data.',
            '2. **Use ONLY the measurements provided below.** Do not add rooms, change dimensions, or assume additional work not listed.',
            '3. **Prices must reflect Nebraska 2025-2026 market rates** for the ' + jobCity + ' area. If you are uncertain about a specific price, output the field as 0 and add a note saying "VERIFY: [reason]".',
            '4. **Show your math** in the notes. Every quantity must trace back to the input measurements.',
            '5. **Itemize labor PER ROOM** — each room is a separate labor line item for installation.',
            '6. **Materials must match the calculated quantities** from the field measurements — do not round up excessively or add items not needed for this specific job.',
            '',
            '## FIELD CALCULATOR DATA:',
            'Trade: ' + currentTrade,
            'Material type: ' + (floorType || currentTrade),
            'Job location: ' + jobCity,
            ''
        ];

        if (rooms.length > 0) {
            prompt.push('### Flooring Rooms (' + totalSqft.toFixed(1) + ' total sq ft):');
            prompt.push(roomsDesc);
            prompt.push('');
        }
        if (dwWalls.length > 0) {
            prompt.push('### Drywall Walls (' + totalWallSqft.toFixed(0) + ' total sq ft):');
            prompt.push(dwDesc);
            prompt.push('');
        }
        if (trimPerim > 0 || trimWallsStr) {
            prompt.push('### Trim/Base:');
            prompt.push('  Perimeter: ' + (trimPerim || trimWallsStr) + ' lf, ' + trimDoors + ' doors');
            if (transCount > 0) prompt.push('  Transitions: ' + transCount + ' × ' + transType);
            prompt.push('');
        }

        prompt.push('## REQUIRED OUTPUT FORMAT:');
        prompt.push('Return ONLY valid JSON — no markdown, no backticks, no explanation. The JSON must match this exact schema:');
        prompt.push('{');
        prompt.push('  "scopeTitle": "string — e.g. Flooring Installation",');
        prompt.push('  "areaDesc": "string — e.g. Living Room, Hallway, Kitchen",');
        prompt.push('  "scope": ["string array — each item is one scope of work bullet"],');
        prompt.push('  "labor": [');
        prompt.push('    {');
        prompt.push('      "desc": "string — description, include room name for install items",');
        prompt.push('      "basis": "string — one of: per sq ft, per lin ft, per unit, per hour, per fixture, 1 lot, fixed",');
        prompt.push('      "qty": "number — quantity (sq ft, units, hours, etc.)",');
        prompt.push('      "price": "number — rate per unit in dollars (Nebraska market rate, 0 if unsure)"');
        prompt.push('    }');
        prompt.push('  ],');
        prompt.push('  "materials": [');
        prompt.push('    {');
        prompt.push('      "desc": "string — product name with size/spec",');
        prompt.push('      "qty": "string — e.g. 3 box, 1 bag, 24 sq yd",');
        prompt.push('      "price": "number — unit price in dollars (Nebraska retail, 0 if unsure)"');
        prompt.push('    }');
        prompt.push('  ],');
        prompt.push('  "notes": ["string array — include math verification, assumptions, VERIFY flags"],');
        prompt.push('  "supplierNote": "string — note about who supplies the main material",');
        prompt.push('  "disclaimer": "string — standard concealed-conditions disclaimer"');
        prompt.push('}');
        prompt.push('');
        prompt.push('CRITICAL: Output raw JSON only. No markdown code fences. No text before or after the JSON.');

        // 3. Show loading state
        notify('⚡ AI is building your bid from field measurements...');
        var loadingOverlay = document.createElement('div');
        loadingOverlay.id = 'fcBidLoading';
        loadingOverlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:99999;display:flex;align-items:center;justify-content:center;';
        loadingOverlay.innerHTML = '<div style="background:#16213e;border:1px solid #2a3a5c;border-radius:16px;padding:30px 40px;text-align:center"><div style="width:40px;height:40px;border:3px solid #2a3a5c;border-top-color:#4ade80;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 16px"></div><div style="color:#e4e4e7;font-size:14px;font-weight:600">Building bid from field data...</div><div style="color:#71717a;font-size:12px;margin-top:6px">Gemini is itemizing rooms, calculating materials, and setting labor rates</div></div><style>@keyframes spin{to{transform:rotate(360deg)}}</style>';
        document.body.appendChild(loadingOverlay);

        try {
            var res = await fetch(PROXY + '?model=gemini-2.5-pro', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ role: 'user', parts: [{ text: prompt.join('\n') }] }],
                    generationConfig: { temperature: 0.2, maxOutputTokens: 8192 }
                })
            });

            var data = await res.json();
            // Extract text — skip thought parts for Gemini 2.5 Pro
            var parts = (data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts) || [];
            var rawText = '';
            for (var pi = 0; pi < parts.length; pi++) {
                if (parts[pi].thought) continue;
                if (parts[pi].text) { rawText = parts[pi].text; break; }
            }
            if (!rawText) throw new Error('No response from AI');

            // Clean any markdown fences the AI might add despite instructions
            rawText = rawText.replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/\s*```$/i, '').trim();

            var bid;
            try {
                bid = JSON.parse(rawText);
            } catch(parseErr) {
                // Try to extract JSON from the response
                var jsonMatch = rawText.match(/\{[\s\S]*\}/);
                if (jsonMatch) {
                    bid = JSON.parse(jsonMatch[0]);
                } else {
                    throw new Error('AI returned invalid JSON. Raw: ' + rawText.substring(0, 200));
                }
            }

            // 4. Auto-populate the BidGen form
            // Set area description
            var adEl = document.getElementById('areaDesc');
            if (adEl && bid.areaDesc) adEl.value = bid.areaDesc;

            // Set scope title
            var stEl = document.getElementById('scopeTitle');
            if (stEl && bid.scopeTitle) stEl.value = bid.scopeTitle;

            // Set sq ft from our known total
            var sfEl = document.getElementById('sqft');
            if (sfEl && totalSqft > 0) sfEl.value = Math.round(totalSqft);

            // Populate scope items
            if (bid.scope && bid.scope.length) {
                document.getElementById('scopeItemsContainer').innerHTML = '';
                bid.scope.forEach(function(s) { if (typeof addScopeRow === 'function') addScopeRow(s); });
            }

            // Populate labor items — clear existing and add new
            if (bid.labor && bid.labor.length) {
                document.getElementById('laborItemsContainer').innerHTML = '';
                bid.labor.forEach(function(li) {
                    if (typeof addLaborRow === 'function') {
                        addLaborRow(li.desc || '', li.basis || 'per sq ft', li.price || 0, li.qty || '');
                    }
                });
            }

            // Populate material items — clear existing and add new
            if (bid.materials && bid.materials.length) {
                document.getElementById('matItemsContainer').innerHTML = '';
                bid.materials.forEach(function(mi) {
                    if (typeof addMatRow === 'function') {
                        addMatRow(mi.desc || '', mi.qty || '1', mi.price || 0);
                    }
                });
            }

            // Populate notes
            if (bid.notes && bid.notes.length) {
                document.getElementById('notesItemsContainer').innerHTML = '';
                bid.notes.forEach(function(n) { if (typeof addNoteRow === 'function') addNoteRow(n); });
            }

            // Set supplier note and disclaimer
            if (bid.supplierNote) {
                var snEl = document.getElementById('supplierNote');
                if (snEl) snEl.value = bid.supplierNote;
            }
            if (bid.disclaimer) {
                var dcEl = document.getElementById('disclaimer');
                if (dcEl) dcEl.value = bid.disclaimer;
            }

            // Recalculate totals
            if (typeof liveCalc === 'function') liveCalc();

            // Close the field calc panel
            var fcPanel = document.getElementById('fieldCalcPanel');
            if (fcPanel) fcPanel.style.display = 'none';

            notify('⚡ Bid populated! Review all prices — items marked VERIFY need your input.');

        } catch (err) {
            notify('❌ Bid generation failed: ' + err.message);
            console.error('fcGenerateBid error:', err);
        } finally {
            var overlay = document.getElementById('fcBidLoading');
            if (overlay) overlay.remove();
        }
    };

    // ================================================================
    // INIT
    // ================================================================
    function init() {
        injectUI();
        // Initial render of room/wall entries
        setTimeout(function() {
            fcRenderRooms();
            fcRenderDwWalls();
        }, 100);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
