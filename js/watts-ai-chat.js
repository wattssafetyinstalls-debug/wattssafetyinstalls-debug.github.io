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

  // Brand detection with unique colors for each
  const isSafetyInstalls = window.location.pathname.startsWith('/safety-installs');
  const BRAND = isSafetyInstalls
    ? {
        name: 'Watts Safety Installs',
        tagline: 'Bringing Peace of Mind to Your Doorstep',
        services: 'kitchen & bath remodeling, painting, gutters, handyman services, electronics & TV mounting, property maintenance, snow removal, and lawn care',
        color: '#00C4B4', // Teal
        colorDark: '#009e91',
        colorLight: '#E0F7F6',
        gradient: 'linear-gradient(135deg, #00C4B4, #009e91)',
      }
    : {
        name: 'Watts ATP Contractor',
        tagline: 'ATP Approved Contractor',
        services: 'wheelchair ramp installation, grab bar installation, non-slip flooring, bathroom accessibility modifications, and ADA-compliant safety solutions',
        color: '#FFD700', // Gold for ATP
        colorDark: '#F4C430',
        colorLight: '#FFF9E6',
        gradient: 'linear-gradient(135deg, #FFD700, #F4C430)',
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
  // STYLES — Professional & Polished Design
  // ═══════════════════════════════════════════
  const style = document.createElement('style');
  style.textContent = `
    #watts-chat-widget * { margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI',system-ui,-apple-system,sans-serif; }
    
    /* Chat Bubble — More Professional */
    #watts-chat-bubble {
      position:fixed; bottom:24px; right:24px; z-index:99999;
      width:68px; height:68px; border-radius:50%;
      background:${BRAND.gradient}; color:#fff;
      border:3px solid #fff; cursor:pointer;
      box-shadow:0 6px 24px rgba(0,0,0,0.15), 0 0 0 1px rgba(0,0,0,0.05);
      display:flex; align-items:center; justify-content:center;
      transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      animation:watts-float 3s ease-in-out infinite;
    }
    #watts-chat-bubble:hover { 
      transform:scale(1.05) translateY(-2px); 
      box-shadow:0 8px 32px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.05);
    }
    #watts-chat-bubble:active { transform:scale(0.95); }
    #watts-chat-bubble svg { width:32px; height:32px; transition:transform 0.3s; }
    #watts-chat-bubble:hover svg { transform:scale(1.1); }
    #watts-chat-bubble .close-icon { display:none; }
    #watts-chat-bubble.open .chat-icon { display:none; }
    #watts-chat-bubble.open .close-icon { display:block; }
    @keyframes watts-float {
      0%,100% { transform:translateY(0); }
      50% { transform:translateY(-5px); }
    }

    /* Notification Badge */
    #watts-chat-badge {
      position:absolute; top:-2px; right:-2px;
      background:#e74c3c; color:#fff; font-size:10px; font-weight:700;
      width:24px; height:24px; border-radius:50%;
      display:flex; align-items:center; justify-content:center;
      border:3px solid #fff;
      animation:watts-badgePulse 2s infinite;
    }
    @keyframes watts-badgePulse {
      0%,100% { transform:scale(1); }
      50% { transform:scale(1.1); }
    }

    /* Chat Window — Premium Design */
    #watts-chat-window {
      position:fixed; bottom:100px; right:24px; z-index:99998;
      width:400px; max-width:calc(100vw - 32px);
      height:560px; max-height:calc(100vh - 140px);
      background:#fff; border-radius:20px;
      overflow:hidden; display:none; flex-direction:column;
      box-shadow:0 20px 60px rgba(0,0,0,0.15), 0 0 0 1px rgba(0,0,0,0.05);
      animation:watts-windowOpen 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    #watts-chat-window.open { display:flex; }
    @keyframes watts-windowOpen {
      from { opacity:0; transform:translateY(20px) scale(0.95); }
      to { opacity:1; transform:translateY(0) scale(1); }
    }

    /* Header — Professional */
    #watts-chat-header {
      background:${BRAND.gradient}; padding:20px; position:relative;
      display:flex; align-items:center; gap:14px;
    }
    #watts-chat-header::before {
      content:''; position:absolute; bottom:0; left:0; right:0;
      height:1px; background:linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }
    #watts-chat-header .avatar {
      width:48px; height:48px; border-radius:50%;
      background:rgba(255,255,255,0.2); backdrop-filter:blur(10px);
      display:flex; align-items:center; justify-content:center;
      font-size:20px; font-weight:700; color:#fff; flex-shrink:0;
      border:2px solid rgba(255,255,255,0.3);
    }
    #watts-chat-header .info h3 { 
      color:#fff; font-size:16px; font-weight:600; 
      text-shadow:0 1px 2px rgba(0,0,0,0.1);
    }
    #watts-chat-header .info p { 
      color:rgba(255,255,255,0.9); font-size:12px; margin-top:2px;
      display:flex; align-items:center; gap:6px;
    }
    #watts-chat-header .status { 
      width:10px; height:10px; border-radius:50%; 
      background:#2ecc71; margin-left:auto; flex-shrink:0;
      box-shadow:0 0 10px rgba(46,204,113,0.5);
      animation:watts-statusGlow 2s infinite;
    }
    @keyframes watts-statusGlow {
      0%,100% { box-shadow:0 0 10px rgba(46,204,113,0.5); }
      50% { box-shadow:0 0 20px rgba(46,204,113,0.8); }
    }

    /* Messages Area */
    #watts-chat-messages {
      flex:1; overflow-y:auto; padding:20px;
      display:flex; flex-direction:column; gap:14px;
      background:#f8f9fa;
      scrollbar-width:thin; scrollbar-color:rgba(0,0,0,0.1) transparent;
    }
    #watts-chat-messages::-webkit-scrollbar { width:6px; }
    #watts-chat-messages::-webkit-scrollbar-track { background:transparent; }
    #watts-chat-messages::-webkit-scrollbar-thumb { 
      background:rgba(0,0,0,0.1); border-radius:3px;
    }
    #watts-chat-messages::-webkit-scrollbar-thumb:hover { background:rgba(0,0,0,0.2); }

    /* Message Bubbles — Modern Design */
    .watts-msg {
      max-width:80%; padding:12px 16px; border-radius:18px;
      font-size:14px; line-height:1.5; word-wrap:break-word;
      animation:watts-msgIn 0.3s ease;
    }
    @keyframes watts-msgIn {
      from { opacity:0; transform:translateY(10px); }
      to { opacity:1; transform:translateY(0); }
    }
    .watts-msg.bot {
      background:#fff; color:#333; align-self:flex-start;
      border-bottom-left-radius:6px;
      box-shadow:0 2px 8px rgba(0,0,0,0.08);
    }
    .watts-msg.user {
      background:${BRAND.gradient}; color:#fff; align-self:flex-end;
      border-bottom-right-radius:6px;
      box-shadow:0 2px 8px rgba(0,0,0,0.15);
    }
    .watts-msg.bot a { 
      color:${BRAND.color}; text-decoration:none; font-weight:500;
      border-bottom:1px solid transparent; transition:border-color 0.2s;
    }
    .watts-msg.bot a:hover { border-bottom-color:${BRAND.color}; }

    /* Typing Indicator — Refined */
    .watts-typing { 
      align-self:flex-start; display:flex; gap:4px; 
      padding:14px 18px; background:#fff; border-radius:18px;
      border-bottom-left-radius:6px; box-shadow:0 2px 8px rgba(0,0,0,0.08);
    }
    .watts-typing span {
      width:8px; height:8px; border-radius:50%; background:${BRAND.color};
      animation:watts-typingDot 1.2s infinite;
    }
    .watts-typing span:nth-child(2) { animation-delay:0.15s; }
    .watts-typing span:nth-child(3) { animation-delay:0.3s; }
    @keyframes watts-typingDot {
      0%,60%,100% { transform:translateY(0); opacity:0.4; }
      30% { transform:translateY(-8px); opacity:1; }
    }

    /* Quick Actions — Professional Pills */
    .watts-quick-actions {
      display:flex; flex-wrap:wrap; gap:8px; padding:0 20px 12px;
      background:#f8f9fa;
    }
    .watts-quick-btn {
      background:#fff; border:1px solid #e0e0e0; color:#666;
      padding:8px 16px; border-radius:20px; font-size:13px;
      cursor:pointer; transition:all 0.2s; font-weight:500;
      box-shadow:0 2px 4px rgba(0,0,0,0.04);
    }
    .watts-quick-btn:hover { 
      background:${BRAND.colorLight}; border-color:${BRAND.color}; 
      color:${BRAND.colorDark}; transform:translateY(-1px);
      box-shadow:0 4px 8px rgba(0,0,0,0.1);
    }

    /* Input Area — Clean Design */
    #watts-chat-input-area {
      padding:16px 20px; border-top:1px solid #e0e0e0;
      display:flex; gap:12px; align-items:center; background:#fff;
    }
    #watts-chat-input {
      flex:1; background:#f8f9fa; border:1px solid #e0e0e0;
      border-radius:24px; padding:12px 18px; color:#333;
      font-size:14px; outline:none; resize:none;
      max-height:80px; line-height:1.4; transition:all 0.2s;
    }
    #watts-chat-input::placeholder { color:#999; }
    #watts-chat-input:focus { 
      background:#fff; border-color:${BRAND.color}; 
      box-shadow:0 0 0 3px ${BRAND.colorLight};
    }
    #watts-chat-send {
      width:44px; height:44px; border-radius:50%;
      background:${BRAND.gradient}; border:none; cursor:pointer;
      display:flex; align-items:center; justify-content:center;
      transition:all 0.2s; flex-shrink:0; box-shadow:0 2px 8px rgba(0,0,0,0.15);
    }
    #watts-chat-send:hover { 
      transform:scale(1.05); box-shadow:0 4px 12px rgba(0,0,0,0.2);
    }
    #watts-chat-send:active { transform:scale(0.95); }
    #watts-chat-send:disabled { opacity:0.5; cursor:not-allowed; transform:none; }
    #watts-chat-send svg { width:20px; height:20px; fill:#fff; }

    /* CTA Banner — Elegant */
    .watts-cta-banner {
      background:${BRAND.gradient}; padding:12px 20px; text-align:center;
      font-size:13px; color:#fff; font-weight:600;
      cursor:pointer; transition:all 0.2s;
      position:relative; overflow:hidden;
    }
    .watts-cta-banner::before {
      content:''; position:absolute; top:0; left:-100%;
      width:100%; height:100%; background:rgba(255,255,255,0.2);
      transition:left 0.3s;
    }
    .watts-cta-banner:hover::before { left:100%; }
    .watts-cta-banner:hover { filter:brightness(1.05); }

    /* Mobile Optimizations */
    @media(max-width:480px) {
      #watts-chat-window { bottom:0; right:0; width:100%; height:100vh; max-height:100vh; border-radius:0; }
      #watts-chat-bubble { bottom:20px; right:20px; width:60px; height:60px; }
      #watts-chat-bubble svg { width:28px; height:28px; }
      #watts-chat-messages { padding:16px; }
      #watts-chat-header { padding:16px; }
      #watts-chat-input-area { padding:12px 16px; }
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
        <button class="watts-quick-btn" data-msg="I need a free estimate">💬 Get Free Estimate</button>
        <button class="watts-quick-btn" data-msg="What services do you offer?">🔧 Our Services</button>
        <button class="watts-quick-btn" data-msg="What areas do you serve?">📍 Service Area</button>
        <button class="watts-quick-btn" data-msg="I'd like to schedule a consultation">📅 Schedule Visit</button>
      </div>
      <div class="watts-cta-banner" onclick="window.location.href='tel:+14054106402'">
        Call Now: (405) 410-6402 &mdash; Free Estimates
      </div>
      <div id="watts-chat-input-area">
        <input id="watts-chat-input" type="text" placeholder="Ask me anything about our services..." autocomplete="off" />
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
      ? `Hello! 👋 Welcome to Watts Safety Installs. I'm your personal assistant here to help with any questions about our home services. Whether you're considering a remodel, need repairs, or want to prepare your home for the seasons — I'm here to help! Would you like a **free estimate** on any project?`
      : `Hi there! 👋 Welcome to Watts ATP Contractor. I'm here to help make your home safer and more accessible. From wheelchair ramps and grab bars to complete bathroom modifications, we're here to serve your family. Can I help you with a **free estimate** or answer any questions?`;

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
