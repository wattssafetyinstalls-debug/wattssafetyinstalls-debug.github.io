/**
 * Watts Photo Upload Widget v1
 * Allows customers to upload photos of their project for quick quotes.
 * Uses Cloudinary unsigned upload preset.
 *
 * Setup: Create a free Cloudinary account at cloudinary.com
 * 1. Get your Cloud Name from Dashboard
 * 2. Create an unsigned upload preset: Settings → Upload → Add upload preset → Signing Mode: Unsigned
 * 3. Set data-cloud-name and data-upload-preset on the script tag
 *
 * Usage: <script src="/js/watts-photo-upload.js" data-cloud-name="YOUR_CLOUD" data-upload-preset="YOUR_PRESET" defer></script>
 * Place <div id="watts-photo-upload"></div> where you want the widget.
 */
(function () {
  'use strict';

  var scriptTag = document.currentScript || document.querySelector('script[data-cloud-name]');
  var CLOUD_NAME = scriptTag && scriptTag.getAttribute('data-cloud-name');
  var UPLOAD_PRESET = scriptTag && scriptTag.getAttribute('data-upload-preset');

  if (!CLOUD_NAME || !UPLOAD_PRESET) return;

  var UPLOAD_URL = 'https://api.cloudinary.com/v1_1/' + CLOUD_NAME + '/image/upload';
  var uploads = [];

  function init() {
    var target = document.getElementById('watts-photo-upload');
    if (!target) return;

    target.innerHTML = '<div id="wpu-box" style="border:2px dashed #cbd5e1;border-radius:12px;padding:30px;text-align:center;cursor:pointer;transition:all 0.2s;background:#fafafa;">' +
      '<div style="font-size:36px;margin-bottom:8px;">📸</div>' +
      '<div style="font-size:15px;font-weight:600;color:#333;margin-bottom:4px;">Upload Photos of Your Project</div>' +
      '<div style="font-size:13px;color:#64748b;">Snap a photo of the area you want modified — helps us give you a faster, more accurate estimate</div>' +
      '<div style="font-size:12px;color:#94a3b8;margin-top:8px;">Click or drag photos here (max 5 photos, 10MB each)</div>' +
      '<input type="file" id="wpu-input" accept="image/*" multiple style="display:none"/>' +
      '</div>' +
      '<div id="wpu-preview" style="display:flex;flex-wrap:wrap;gap:10px;margin-top:12px;"></div>' +
      '<div id="wpu-status" style="font-size:13px;color:#64748b;margin-top:8px;text-align:center;"></div>';

    var box = document.getElementById('wpu-box');
    var input = document.getElementById('wpu-input');

    box.addEventListener('click', function () { input.click(); });
    box.addEventListener('dragover', function (e) { e.preventDefault(); box.style.borderColor = '#00C4B4'; box.style.background = '#f0fdf4'; });
    box.addEventListener('dragleave', function () { box.style.borderColor = '#cbd5e1'; box.style.background = '#fafafa'; });
    box.addEventListener('drop', function (e) {
      e.preventDefault();
      box.style.borderColor = '#cbd5e1';
      box.style.background = '#fafafa';
      handleFiles(e.dataTransfer.files);
    });
    input.addEventListener('change', function () { handleFiles(this.files); this.value = ''; });
  }

  function handleFiles(files) {
    if (uploads.length + files.length > 5) {
      document.getElementById('wpu-status').textContent = 'Maximum 5 photos allowed.';
      return;
    }
    for (var i = 0; i < files.length; i++) {
      if (files[i].size > 10 * 1024 * 1024) {
        document.getElementById('wpu-status').textContent = files[i].name + ' is too large (max 10MB).';
        continue;
      }
      uploadFile(files[i]);
    }
  }

  function uploadFile(file) {
    var preview = document.getElementById('wpu-preview');
    var status = document.getElementById('wpu-status');

    // Show preview immediately
    var thumb = document.createElement('div');
    thumb.style.cssText = 'width:80px;height:80px;border-radius:8px;overflow:hidden;position:relative;background:#e2e8f0;';
    thumb.innerHTML = '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:12px;color:#64748b;">Uploading...</div>';
    preview.appendChild(thumb);

    var reader = new FileReader();
    reader.onload = function (e) {
      thumb.innerHTML = '<img src="' + e.target.result + '" style="width:100%;height:100%;object-fit:cover;"/>' +
        '<div style="position:absolute;inset:0;background:rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;" id="wpu-overlay-' + uploads.length + '">' +
        '<div style="width:20px;height:20px;border:2px solid #fff;border-top-color:transparent;border-radius:50%;animation:wpu-spin 0.6s linear infinite;"></div></div>';
    };
    reader.readAsDataURL(file);

    // Add spinner animation if not already added
    if (!document.getElementById('wpu-style')) {
      var style = document.createElement('style');
      style.id = 'wpu-style';
      style.textContent = '@keyframes wpu-spin{to{transform:rotate(360deg)}}';
      document.head.appendChild(style);
    }

    var idx = uploads.length;
    var formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', UPLOAD_PRESET);
    formData.append('folder', 'watts-customer-photos');

    status.textContent = 'Uploading ' + file.name + '...';

    fetch(UPLOAD_URL, { method: 'POST', body: formData })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.secure_url) {
          uploads.push(data.secure_url);
          var overlay = document.getElementById('wpu-overlay-' + idx);
          if (overlay) {
            overlay.innerHTML = '<div style="color:#22c55e;font-size:18px;">✓</div>';
            setTimeout(function () { overlay.style.display = 'none'; }, 1000);
          }
          status.textContent = uploads.length + ' photo(s) uploaded successfully.';

          // Store URLs for form submission
          window.wattsPhotoUrls = uploads;

          // Fire custom event
          document.dispatchEvent(new CustomEvent('watts-photo-uploaded', { detail: { urls: uploads } }));
        } else {
          status.textContent = 'Upload failed — try again.';
          thumb.remove();
        }
      })
      .catch(function () {
        status.textContent = 'Upload failed — check your connection.';
        thumb.remove();
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
