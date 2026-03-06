/**
 * Widget Dock — BidGen Floating Tool Launcher
 * A single draggable pill that holds all tool widgets.
 * Drag anywhere on screen (touch + mouse), remembers position.
 * Tap icon to open/close that tool's panel.
 */
(function() {
  'use strict';

  var DOCK_KEY = 'bidgen-dock-pos';
  var SNAP_EDGE = true;

  // ================================================================
  // WIDGET REGISTRY — add new widgets here
  // ================================================================
  var widgets = [
    {
      id: 'bgai',
      icon: '🧠',
      label: 'AI Mentor',
      toggle: function() {
        var btn = document.getElementById('bgai-toggle');
        if (btn) btn.click();
      },
      isOpen: function() {
        var p = document.getElementById('bgai-panel');
        return p && p.classList.contains('open');
      }
    },
    {
      id: 'fieldcalc',
      icon: '📐',
      label: 'Field Calc',
      toggle: function() {
        var p = document.getElementById('fieldCalcPanel');
        if (p) {
          p.style.display = p.style.display === 'none' ? 'flex' : 'none';
          if (p.style.display !== 'none') p.style.flexDirection = 'column';
        }
      },
      isOpen: function() {
        var p = document.getElementById('fieldCalcPanel');
        return p && p.style.display !== 'none';
      }
    }
  ];

  // ================================================================
  // STYLES
  // ================================================================
  function injectStyles() {
    var css = document.createElement('style');
    css.textContent =
      '#wd-dock{position:fixed;z-index:99990;display:flex;align-items:center;gap:2px;' +
      'background:rgba(9,9,11,0.88);backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);' +
      'border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:4px;' +
      'box-shadow:0 8px 32px rgba(0,0,0,0.4),0 0 0 1px rgba(255,255,255,0.03);' +
      'cursor:grab;user-select:none;-webkit-user-select:none;touch-action:none;transition:box-shadow 0.2s}' +
      '#wd-dock.dragging{cursor:grabbing;box-shadow:0 12px 40px rgba(0,0,0,0.6),0 0 0 1px rgba(255,255,255,0.06);transform:scale(1.04)}' +
      '#wd-dock.snapping{transition:left 0.25s ease,top 0.25s ease,box-shadow 0.2s}' +

      '.wd-btn{width:40px;height:40px;border:none;border-radius:10px;background:transparent;' +
      'color:#71717a;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;' +
      'transition:all 0.15s;position:relative;flex-shrink:0}' +
      '.wd-btn:hover{background:rgba(255,255,255,0.06);color:#e4e4e7}' +
      '.wd-btn.active{background:rgba(59,130,246,0.12);color:#60a5fa}' +
      '.wd-btn.active::after{content:"";position:absolute;bottom:2px;left:50%;transform:translateX(-50%);' +
      'width:12px;height:2px;background:#60a5fa;border-radius:1px}' +

      '.wd-tip{position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);' +
      'background:rgba(9,9,11,0.95);color:#e4e4e7;font-size:11px;font-weight:500;padding:4px 10px;' +
      'border-radius:6px;white-space:nowrap;pointer-events:none;opacity:0;transition:opacity 0.15s;' +
      'border:1px solid rgba(255,255,255,0.06);font-family:"Inter",-apple-system,sans-serif}' +
      '.wd-btn:hover .wd-tip{opacity:1}' +

      '.wd-grip{width:6px;display:flex;flex-direction:column;gap:2px;padding:0 4px;align-items:center;opacity:0.25;flex-shrink:0}' +
      '.wd-grip span{width:3px;height:3px;border-radius:50%;background:#a1a1aa}' +
      '#wd-dock:hover .wd-grip{opacity:0.5}' +

      '@media(max-width:768px){' +
        '#wd-dock{padding:3px;border-radius:12px;gap:1px}' +
        '.wd-btn{width:38px;height:38px;font-size:17px;border-radius:9px}' +
        '.wd-tip{display:none}' +
      '}';
    document.head.appendChild(css);
  }

  // ================================================================
  // BUILD DOCK
  // ================================================================
  function buildDock() {
    var dock = document.createElement('div');
    dock.id = 'wd-dock';

    // Grip dots (drag handle visual indicator)
    var grip = document.createElement('div');
    grip.className = 'wd-grip';
    grip.innerHTML = '<span></span><span></span><span></span>';
    dock.appendChild(grip);

    // Widget buttons
    widgets.forEach(function(w) {
      var btn = document.createElement('button');
      btn.className = 'wd-btn';
      btn.id = 'wd-' + w.id;
      btn.setAttribute('data-wid', w.id);
      btn.innerHTML = w.icon + '<span class="wd-tip">' + w.label + '</span>';
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        // Only trigger if this wasn't a drag
        if (!_didDrag) {
          w.toggle();
          updateActive();
        }
      });
      dock.appendChild(btn);
    });

    document.body.appendChild(dock);

    // Position — restore or default
    var saved = loadPosition();
    if (saved) {
      dock.style.left = clamp(saved.x, 0, window.innerWidth - dock.offsetWidth) + 'px';
      dock.style.top = clamp(saved.y, 0, window.innerHeight - dock.offsetHeight) + 'px';
    } else {
      // Default: bottom-right above the live-calc bar
      dock.style.right = '16px';
      dock.style.bottom = '52px';
    }

    // Make draggable
    enableDrag(dock);

    // Periodically update active states
    setInterval(updateActive, 500);

    return dock;
  }

  // ================================================================
  // ACTIVE STATE SYNC
  // ================================================================
  function updateActive() {
    widgets.forEach(function(w) {
      var btn = document.getElementById('wd-' + w.id);
      if (!btn) return;
      try {
        var isOpen = w.isOpen();
        btn.classList.toggle('active', !!isOpen);
      } catch(e) {}
    });
  }

  // ================================================================
  // DRAGGING — mouse + touch
  // ================================================================
  var _dragging = false;
  var _didDrag = false;
  var _startX, _startY, _dockX, _dockY;

  function enableDrag(dock) {
    // Mouse
    dock.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', moveDrag);
    document.addEventListener('mouseup', endDrag);

    // Touch
    dock.addEventListener('touchstart', startDrag, { passive: false });
    document.addEventListener('touchmove', moveDrag, { passive: false });
    document.addEventListener('touchend', endDrag);
  }

  function getXY(e) {
    if (e.touches && e.touches.length > 0) return { x: e.touches[0].clientX, y: e.touches[0].clientY };
    return { x: e.clientX, y: e.clientY };
  }

  function startDrag(e) {
    // Don't drag if clicking a button (let click handler run)
    if (e.target.closest('.wd-btn')) {
      _didDrag = false;
      // Still track for drag detection
      var pos = getXY(e);
      _startX = pos.x;
      _startY = pos.y;
      return;
    }

    var dock = document.getElementById('wd-dock');
    var pos = getXY(e);
    var rect = dock.getBoundingClientRect();

    _dragging = true;
    _didDrag = false;
    _startX = pos.x;
    _startY = pos.y;
    _dockX = rect.left;
    _dockY = rect.top;

    dock.classList.add('dragging');
    dock.classList.remove('snapping');

    // Clear right/bottom positioning so left/top takes over
    dock.style.right = 'auto';
    dock.style.bottom = 'auto';
    dock.style.left = _dockX + 'px';
    dock.style.top = _dockY + 'px';

    if (e.cancelable) e.preventDefault();
  }

  function moveDrag(e) {
    if (!_dragging) {
      // Check if a button press turned into a drag
      if (e.target && _startX !== undefined) {
        var pos = getXY(e);
        var dist = Math.abs(pos.x - _startX) + Math.abs(pos.y - _startY);
        if (dist > 8) {
          // Convert to drag
          var dock = document.getElementById('wd-dock');
          var rect = dock.getBoundingClientRect();
          _dragging = true;
          _didDrag = true;
          _dockX = rect.left;
          _dockY = rect.top;
          dock.classList.add('dragging');
          dock.classList.remove('snapping');
          dock.style.right = 'auto';
          dock.style.bottom = 'auto';
          dock.style.left = _dockX + 'px';
          dock.style.top = _dockY + 'px';
        }
      }
      if (!_dragging) return;
    }

    var pos = getXY(e);
    var dx = pos.x - _startX;
    var dy = pos.y - _startY;

    if (Math.abs(dx) + Math.abs(dy) > 4) _didDrag = true;

    var dock = document.getElementById('wd-dock');
    var newX = _dockX + dx;
    var newY = _dockY + dy;

    // Clamp to viewport
    var dw = dock.offsetWidth;
    var dh = dock.offsetHeight;
    newX = clamp(newX, 0, window.innerWidth - dw);
    newY = clamp(newY, 0, window.innerHeight - dh);

    dock.style.left = newX + 'px';
    dock.style.top = newY + 'px';

    if (e.cancelable) e.preventDefault();
  }

  function endDrag(e) {
    if (!_dragging) return;
    _dragging = false;

    var dock = document.getElementById('wd-dock');
    dock.classList.remove('dragging');

    // Snap to nearest edge if enabled
    if (SNAP_EDGE) {
      var rect = dock.getBoundingClientRect();
      var midX = rect.left + rect.width / 2;
      var snapX;

      if (midX < window.innerWidth / 2) {
        snapX = 8; // snap left
      } else {
        snapX = window.innerWidth - rect.width - 8; // snap right
      }

      var snapY = clamp(rect.top, 8, window.innerHeight - rect.height - 8);

      dock.classList.add('snapping');
      dock.style.left = snapX + 'px';
      dock.style.top = snapY + 'px';

      setTimeout(function() { dock.classList.remove('snapping'); }, 300);

      savePosition(snapX, snapY);
    } else {
      savePosition(parseInt(dock.style.left), parseInt(dock.style.top));
    }
  }

  // ================================================================
  // PERSISTENCE
  // ================================================================
  function savePosition(x, y) {
    try { localStorage.setItem(DOCK_KEY, JSON.stringify({ x: x, y: y })); } catch(e) {}
  }

  function loadPosition() {
    try {
      var s = localStorage.getItem(DOCK_KEY);
      return s ? JSON.parse(s) : null;
    } catch(e) { return null; }
  }

  function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }

  // ================================================================
  // HIDE OLD TOGGLE BUTTONS
  // ================================================================
  function hideOldToggles() {
    // Hide BidGen AI toggle
    var bgaiToggle = document.getElementById('bgai-toggle');
    if (bgaiToggle) bgaiToggle.style.display = 'none';

    // Hide Field Calc toggle
    var fcToggle = document.getElementById('fieldCalcToggle');
    if (fcToggle) fcToggle.style.display = 'none';
  }

  // ================================================================
  // RESIZE HANDLER — keep dock in viewport
  // ================================================================
  function onResize() {
    var dock = document.getElementById('wd-dock');
    if (!dock) return;
    var rect = dock.getBoundingClientRect();
    var newX = clamp(rect.left, 0, window.innerWidth - dock.offsetWidth);
    var newY = clamp(rect.top, 0, window.innerHeight - dock.offsetHeight);
    dock.style.left = newX + 'px';
    dock.style.top = newY + 'px';
    dock.style.right = 'auto';
    dock.style.bottom = 'auto';
  }

  // ================================================================
  // INIT
  // ================================================================
  function init() {
    injectStyles();
    buildDock();
    // Wait for other scripts to inject their toggles, then hide them
    setTimeout(hideOldToggles, 1500);
    setTimeout(hideOldToggles, 3000);
    window.addEventListener('resize', onResize);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose for adding widgets dynamically
  window.widgetDockRegister = function(cfg) {
    widgets.push(cfg);
    // Rebuild if dock exists
    var dock = document.getElementById('wd-dock');
    if (dock) {
      var btn = document.createElement('button');
      btn.className = 'wd-btn';
      btn.id = 'wd-' + cfg.id;
      btn.setAttribute('data-wid', cfg.id);
      btn.innerHTML = cfg.icon + '<span class="wd-tip">' + cfg.label + '</span>';
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (!_didDrag) {
          cfg.toggle();
          updateActive();
        }
      });
      dock.appendChild(btn);
    }
  };
})();
