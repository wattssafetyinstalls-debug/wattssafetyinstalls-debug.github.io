/**
 * Web Push Notifications — Watts ATP Contractor & Watts Safety Installs
 * Uses OneSignal free tier (up to 10,000 subscribers).
 * Auto-prompts visitors to subscribe after 30 seconds on site.
 * 
 * Setup: Create free account at https://onesignal.com
 * Then set your App ID below.
 */
(function() {
  // ── CONFIGURATION ──
  // Replace with your OneSignal App ID after signup
  var APP_ID = window.ONESIGNAL_APP_ID || '';
  
  if (!APP_ID) return; // Skip if no App ID configured yet

  // Load OneSignal SDK
  window.OneSignalDeferred = window.OneSignalDeferred || [];

  var script = document.createElement('script');
  script.src = 'https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js';
  script.defer = true;
  document.head.appendChild(script);

  OneSignalDeferred.push(function(OneSignal) {
    OneSignal.init({
      appId: APP_ID,
      allowLocalhostAsSecureOrigin: false,
      promptOptions: {
        slidedown: {
          prompts: [{
            type: 'push',
            autoPrompt: true,
            text: {
              actionMessage: 'Get home improvement tips & special offers from Justin at Watts ATP Contractor!',
              acceptButton: 'Allow',
              cancelButton: 'Maybe Later'
            },
            delay: {
              pageViews: 2,
              timeDelay: 30
            }
          }]
        }
      },
      welcomeNotification: {
        title: 'Welcome!',
        message: "Thanks for subscribing! You'll get helpful tips from Justin at Watts ATP Contractor."
      },
      notifyButton: {
        enable: false // We use the chat widget instead
      }
    });
  });
})();
