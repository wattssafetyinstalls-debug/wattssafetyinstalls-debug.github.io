/**
 * Watts AI Chat Widget
 * Floating chatbot powered by Google Gemini via Cloudflare Worker proxy.
 * Auto-detects ATP Contractor vs Safety Installs based on URL.
 * Captures leads, answers service questions, drives bookings.
 *
 * SETUP: Replace PROXY_URL below with your Cloudflare Worker URL.
 */

(function () {
  'use strict';

  // ═══════════════════════════════════════════
  // CONFIGURATION — UPDATE AFTER DEPLOYING PROXY
  // ═══════════════════════════════════════════
  const PROXY_URL = 'https://watts-ai-proxy.wattssafetyinstalls.workers.dev';
  const GEMINI_MODEL = 'gemini-2.0-flash';

  // Brand detection
  const isSafetyInstalls = window.location.pathname.startsWith('/safety-installs');
  const BRAND = isSafetyInstalls
    ? {
        name: 'Watts Safety Installs',
        tagline: 'Bringing Peace of Mind to Your Doorstep',
        services: 'kitchen & bath remodeling, painting, gutters, handyman services, electronics & TV mounting, property maintenance, snow removal, and lawn care',
        color: '#00C4B4',
        colorDark: '#009e91',
      }
    : {
        name: 'Watts ATP Contractor',
        tagline: 'ATP Approved Contractor',
        services: 'wheelchair ramp installation, grab bar installation, non-slip flooring, bathroom accessibility modifications, and ADA-compliant safety solutions',
        color: '#00C4B4',
        colorDark: '#009e91',
      };

  const SYSTEM_PROMPT = `You are the friendly, professional AI assistant for ${BRAND.name} based in Norfolk, Nebraska.

BUSINESS INFO:
- Company: ${BRAND.name}
- Phone: (405) 410-6402
- Email: Justin.Watts@WattsATPContractor.com
- Address: 507 West Omaha Ave Suite B, Norfolk, Nebraska
- Nebraska License: #54690-25
- Owner: Justin Watts
- Service Area: Norfolk NE and within 100 miles of Northeast Nebraska (Madison County, Stanton County, Pierce County, Wayne County, Antelope County, Knox County, Cedar County, Dixon County, Dakota County, Thurston County, Cuming County, Platte County, Colfax County, Boone County, Lancaster County, and surrounding areas)
- Rating: 5.0 stars (12 reviews)
- Services: ${BRAND.services}

YOUR GOALS (in priority order):
1. CAPTURE LEADS: Get the visitor's name, phone number, and project description. This is your #1 job.
2. ANSWER QUESTIONS: Be helpful about services, process, timelines, and general pricing ranges.
3. DRIVE BOOKINGS: Push toward scheduling a free estimate. "Can I get your name and number so Justin can call you with a free estimate?"
4. BUILD TRUST: Mention the 5-star rating, licensed & insured, 100-mile service area, and free estimates naturally.

RULES:
- Keep responses SHORT (2-3 sentences max). This is a chat widget, not an essay.
- Be warm and conversational, like a friendly receptionist.
- NEVER give exact pricing. Say "Every project is different — I'd love to get Justin on the phone for a free estimate. What's a good number to reach you?"
- If someone asks about a service you don't offer, say "That's not one of our specialties, but I can check with Justin. Want to leave your number?"
- Always try to collect: name, phone, and brief project description.
- When you have their contact info, confirm it and say "Justin will be in touch shortly!"
- If asked about competitors, stay professional: "I can't speak about other companies, but I can tell you about what makes us different."
- Respond in the same language the visitor uses.
- If the visitor seems frustrated or the question is complex, offer to connect them directly: "Let me get Justin on the line — call (405) 410-6402 anytime."

OPENING: Greet warmly and ask how you can help. Mention the free estimate offer.`;

  // Chat state
  let chatHistory = [];
  let isOpen = false;
  let isLoading = false;
  let leadCaptured = { name: null, phone: null, project: null };

  // ═══════════════════════════════════════════
  // STYLES
  // ═══════════════════════════════════════════
  const style = document.createElement('style');
  style.textContent = `
    #watts-chat-widget * { margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI',system-ui,-apple-system,sans-serif; }
    #watts-chat-bubble {
      position:fixed; bottom:24px; right:24px; z-index:99999;
      width:64px; height:64px; border-radius:50%;
      background:${BRAND.color}; color:#fff;
      border:none; cursor:pointer;
      box-shadow:0 4px 20px rgba(0,196,180,0.4);
      display:flex; align-items:center; justify-content:center;
      transition:transform 0.3s, box-shadow 0.3s;
      animation:watts-pulse 3s infinite;
    }
    #watts-chat-bubble:hover { transform:scale(1.1); box-shadow:0 6px 28px rgba(0,196,180,0.6); }
    #watts-chat-bubble svg { width:30px; height:30px; }
    #watts-chat-bubble .close-icon { display:none; }
    #watts-chat-bubble.open .chat-icon { display:none; }
    #watts-chat-bubble.open .close-icon { display:block; }
    @keyframes watts-pulse {
      0%,100% { box-shadow:0 4px 20px rgba(0,196,180,0.4); }
      50% { box-shadow:0 4px 30px rgba(0,196,180,0.7); }
    }

    #watts-chat-badge {
      position:absolute; top:-4px; right:-4px;
      background:#e74c3c; color:#fff; font-size:11px; font-weight:700;
      width:22px; height:22px; border-radius:50%;
      display:flex; align-items:center; justify-content:center;
      border:2px solid #0A1D37;
    }

    #watts-chat-window {
      position:fixed; bottom:100px; right:24px; z-index:99998;
      width:380px; max-width:calc(100vw - 32px);
      height:520px; max-height:calc(100vh - 140px);
      background:#0A1D37; border:1px solid #1a3a5c;
      border-radius:16px; overflow:hidden;
      display:none; flex-direction:column;
      box-shadow:0 12px 48px rgba(0,0,0,0.5);
      animation:watts-slideUp 0.3s ease;
    }
    #watts-chat-window.open { display:flex; }
    @keyframes watts-slideUp {
      from { opacity:0; transform:translateY(20px); }
      to { opacity:1; transform:translateY(0); }
    }

    #watts-chat-header {
      background:linear-gradient(135deg,#0A1D37,#16213e);
      padding:16px 20px; border-bottom:1px solid #1a3a5c;
      display:flex; align-items:center; gap:12px;
    }
    #watts-chat-header .avatar {
      width:40px; height:40px; border-radius:50%;
      background:${BRAND.color}; display:flex; align-items:center; justify-content:center;
      font-size:18px; font-weight:700; color:#fff; flex-shrink:0;
    }
    #watts-chat-header .info h3 { color:#fff; font-size:14px; font-weight:600; }
    #watts-chat-header .info p { color:#7f8c8d; font-size:11px; margin-top:2px; }
    #watts-chat-header .status { width:8px; height:8px; border-radius:50%; background:#2ecc71; margin-left:auto; flex-shrink:0; }

    #watts-chat-messages {
      flex:1; overflow-y:auto; padding:16px; display:flex; flex-direction:column; gap:12px;
      scrollbar-width:thin; scrollbar-color:#1a3a5c transparent;
    }
    #watts-chat-messages::-webkit-scrollbar { width:6px; }
    #watts-chat-messages::-webkit-scrollbar-track { background:transparent; }
    #watts-chat-messages::-webkit-scrollbar-thumb { background:#1a3a5c; border-radius:3px; }

    .watts-msg {
      max-width:85%; padding:10px 14px; border-radius:14px;
      font-size:13.5px; line-height:1.5; word-wrap:break-word;
    }
    .watts-msg.bot {
      background:#16213e; color:#ddd; align-self:flex-start;
      border-bottom-left-radius:4px;
    }
    .watts-msg.user {
      background:${BRAND.color}; color:#fff; align-self:flex-end;
      border-bottom-right-radius:4px;
    }
    .watts-msg.bot a { color:${BRAND.color}; text-decoration:underline; }

    .watts-typing { align-self:flex-start; display:flex; gap:4px; padding:12px 16px; }
    .watts-typing span {
      width:7px; height:7px; border-radius:50%; background:#3a5a7c;
      animation:watts-typingDot 1.4s infinite;
    }
    .watts-typing span:nth-child(2) { animation-delay:0.2s; }
    .watts-typing span:nth-child(3) { animation-delay:0.4s; }
    @keyframes watts-typingDot {
      0%,60%,100% { opacity:0.3; transform:translateY(0); }
      30% { opacity:1; transform:translateY(-4px); }
    }

    .watts-quick-actions {
      display:flex; flex-wrap:wrap; gap:6px; padding:0 16px 8px;
    }
    .watts-quick-btn {
      background:#16213e; border:1px solid #1a3a5c; color:#aaa;
      padding:6px 12px; border-radius:20px; font-size:12px;
      cursor:pointer; transition:all 0.2s;
    }
    .watts-quick-btn:hover { background:#1a3a5c; color:#fff; border-color:${BRAND.color}; }

    #watts-chat-input-area {
      padding:12px 16px; border-top:1px solid #1a3a5c;
      display:flex; gap:8px; align-items:center; background:#0d1829;
    }
    #watts-chat-input {
      flex:1; background:#16213e; border:1px solid #1a3a5c;
      border-radius:24px; padding:10px 16px; color:#eee;
      font-size:13.5px; outline:none; resize:none;
      max-height:80px; line-height:1.4;
    }
    #watts-chat-input::placeholder { color:#4a5a6c; }
    #watts-chat-input:focus { border-color:${BRAND.color}; }
    #watts-chat-send {
      width:38px; height:38px; border-radius:50%;
      background:${BRAND.color}; border:none; cursor:pointer;
      display:flex; align-items:center; justify-content:center;
      transition:background 0.2s; flex-shrink:0;
    }
    #watts-chat-send:hover { background:${BRAND.colorDark}; }
    #watts-chat-send:disabled { opacity:0.4; cursor:not-allowed; }
    #watts-chat-send svg { width:18px; height:18px; fill:#fff; }

    .watts-cta-banner {
      background:linear-gradient(90deg,${BRAND.color},${BRAND.colorDark});
      padding:8px 16px; text-align:center;
      font-size:12px; color:#fff; font-weight:600;
      cursor:pointer;
    }
    .watts-cta-banner:hover { filter:brightness(1.1); }

    @media(max-width:480px) {
      #watts-chat-window { bottom:0; right:0; width:100%; height:100vh; max-height:100vh; border-radius:0; }
      #watts-chat-bubble { bottom:16px; right:16px; width:56px; height:56px; }
      #watts-chat-bubble svg { width:26px; height:26px; }
    }
  `;
  document.head.appendChild(style);

  // ═══════════════════════════════════════════
  // BUILD DOM
  // ═══════════════════════════════════════════
  const widget = document.createElement('div');
  widget.id = 'watts-chat-widget';
  widget.innerHTML = `
    <button id="watts-chat-bubble" aria-label="Chat with us">
      <span id="watts-chat-badge">1</span>
      <svg class="chat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
      </svg>
      <svg class="close-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>
    <div id="watts-chat-window">
      <div id="watts-chat-header">
        <div class="avatar">W</div>
        <div class="info">
          <h3>${BRAND.name}</h3>
          <p>AI Assistant &bull; Typically replies instantly</p>
        </div>
        <div class="status"></div>
      </div>
      <div id="watts-chat-messages"></div>
      <div class="watts-quick-actions" id="watts-quick-actions">
        <button class="watts-quick-btn" data-msg="I need a free estimate">Free Estimate</button>
        <button class="watts-quick-btn" data-msg="What services do you offer?">Services</button>
        <button class="watts-quick-btn" data-msg="What areas do you serve?">Service Area</button>
        <button class="watts-quick-btn" data-msg="I'd like to schedule a consultation">Schedule</button>
      </div>
      <div class="watts-cta-banner" onclick="window.location.href='tel:+14054106402'">
        Call Now: (405) 410-6402 &mdash; Free Estimates
      </div>
      <div id="watts-chat-input-area">
        <input id="watts-chat-input" type="text" placeholder="Type your message..." autocomplete="off" />
        <button id="watts-chat-send" aria-label="Send message">
          <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>
    </div>
  `;
  document.body.appendChild(widget);

  // ═══════════════════════════════════════════
  // REFERENCES
  // ═══════════════════════════════════════════
  const bubble = document.getElementById('watts-chat-bubble');
  const badge = document.getElementById('watts-chat-badge');
  const chatWindow = document.getElementById('watts-chat-window');
  const messages = document.getElementById('watts-chat-messages');
  const input = document.getElementById('watts-chat-input');
  const sendBtn = document.getElementById('watts-chat-send');
  const quickActions = document.getElementById('watts-quick-actions');

  // ═══════════════════════════════════════════
  // CHAT LOGIC
  // ═══════════════════════════════════════════
  function toggleChat() {
    isOpen = !isOpen;
    chatWindow.classList.toggle('open', isOpen);
    bubble.classList.toggle('open', isOpen);
    badge.style.display = 'none';

    if (isOpen && chatHistory.length === 0) {
      sendInitialGreeting();
    }
    if (isOpen) {
      setTimeout(() => input.focus(), 300);
    }
  }

  function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `watts-msg ${sender}`;
    // Simple markdown-like formatting
    let html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>')
      .replace(/\((\d{3})\)\s?(\d{3})-(\d{4})/g, '<a href="tel:+1$1$2$3">($1) $2-$3</a>');
    div.innerHTML = html;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function showTyping() {
    const div = document.createElement('div');
    div.className = 'watts-typing';
    div.id = 'watts-typing-indicator';
    div.innerHTML = '<span></span><span></span><span></span>';
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function hideTyping() {
    const el = document.getElementById('watts-typing-indicator');
    if (el) el.remove();
  }

  function hideQuickActions() {
    quickActions.style.display = 'none';
  }

  async function sendInitialGreeting() {
    showTyping();
    await sleep(800);
    hideTyping();
    const greeting = isSafetyInstalls
      ? `Hey there! Welcome to Watts Safety Installs. I'm here to help with any questions about our home services — remodeling, painting, handyman work, snow removal, you name it. Looking for a **free estimate**? I can help with that!`
      : `Hi! Welcome to Watts ATP Contractor. I'm here to help with ADA accessibility questions — wheelchair ramps, grab bars, bathroom modifications, and more. We offer **free estimates** for all projects. How can I help you today?`;

    addMessage(greeting, 'bot');
    chatHistory.push({ role: 'model', parts: [{ text: greeting }] });
  }

  async function sendMessage(text) {
    if (!text.trim() || isLoading) return;

    addMessage(text, 'user');
    hideQuickActions();
    input.value = '';
    isLoading = true;
    sendBtn.disabled = true;

    // Add to history
    chatHistory.push({ role: 'user', parts: [{ text }] });

    // Check for lead info in message
    extractLeadInfo(text);

    showTyping();

    try {
      const response = await callGemini(chatHistory);
      hideTyping();
      addMessage(response, 'bot');
      chatHistory.push({ role: 'model', parts: [{ text: response }] });

      // Extract lead info from context
      extractLeadInfo(response);

      // If we have a complete lead, log it
      if (leadCaptured.name && leadCaptured.phone) {
        logLead();
      }
    } catch (err) {
      hideTyping();
      addMessage("I'm having a connection issue. Please call us directly at **(405) 410-6402** — we'd love to help!", 'bot');
    }

    isLoading = false;
    sendBtn.disabled = false;
    input.focus();
  }

  async function callGemini(history) {
    const payload = {
      system_instruction: {
        parts: [{ text: SYSTEM_PROMPT }]
      },
      contents: history,
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: 256,
        topP: 0.9,
      },
      safetySettings: [
        { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' },
      ],
    };

    const res = await fetch(`${PROXY_URL}?model=${GEMINI_MODEL}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'API error');
    }

    const data = await res.json();
    const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!text) throw new Error('No response');
    return text;
  }

  function extractLeadInfo(text) {
    // Phone pattern
    const phoneMatch = text.match(/(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})/);
    if (phoneMatch) leadCaptured.phone = phoneMatch[1];

    // Name pattern (simple heuristic: "my name is X" or "I'm X")
    const nameMatch = text.match(/(?:my name is|i'm|i am|this is|name:?)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)/i);
    if (nameMatch) leadCaptured.name = nameMatch[1];
  }

  function logLead() {
    // Store lead in localStorage for retrieval
    const leads = JSON.parse(localStorage.getItem('watts-ai-leads') || '[]');
    const newLead = {
      name: leadCaptured.name,
      phone: leadCaptured.phone,
      project: leadCaptured.project,
      brand: BRAND.name,
      page: window.location.pathname,
      timestamp: new Date().toISOString(),
      conversation: chatHistory.map(m => ({ role: m.role, text: m.parts[0].text })),
    };

    // Avoid duplicates
    const isDuplicate = leads.some(l => l.phone === newLead.phone && l.name === newLead.name);
    if (!isDuplicate) {
      leads.push(newLead);
      localStorage.setItem('watts-ai-leads', JSON.stringify(leads));
    }
  }

  function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
  }

  // ═══════════════════════════════════════════
  // EVENT LISTENERS
  // ═══════════════════════════════════════════
  bubble.addEventListener('click', toggleChat);

  sendBtn.addEventListener('click', () => sendMessage(input.value));

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input.value);
    }
  });

  quickActions.addEventListener('click', (e) => {
    const btn = e.target.closest('.watts-quick-btn');
    if (btn) sendMessage(btn.dataset.msg);
  });

  // Auto-open after 30 seconds if not interacted
  setTimeout(() => {
    if (!isOpen && chatHistory.length === 0) {
      badge.textContent = '1';
      badge.style.display = 'flex';
    }
  }, 5000);

  // Save leads before page unload
  window.addEventListener('beforeunload', () => {
    if (chatHistory.length > 1) {
      const sessionData = {
        brand: BRAND.name,
        page: window.location.pathname,
        timestamp: new Date().toISOString(),
        messages: chatHistory.length,
        lead: leadCaptured,
      };
      const sessions = JSON.parse(localStorage.getItem('watts-ai-sessions') || '[]');
      sessions.push(sessionData);
      localStorage.setItem('watts-ai-sessions', JSON.stringify(sessions));
    }
  });

})();
