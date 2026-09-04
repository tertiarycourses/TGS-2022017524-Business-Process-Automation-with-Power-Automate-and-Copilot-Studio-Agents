/* =====================================================================
   Cook & Bake Academy — landing page + RAG chatbot widget (Copilot Studio)
   ---------------------------------------------------------------------
   The chatbot calls your Copilot Studio flow. You set the URL in the "Lab
   configuration" panel on the page, so you never have to edit this file.

     Paste the HTTP POST URL from the flow's "When a HTTP request is received"
     trigger into the Lab configuration panel. It looks like:
       https://<env>.environment.api.powerplatform.com/powerautomate/
         automations/direct/.../triggers/manual/paths/invoke?...&sig=...

   THERE IS NO OFFLINE FALLBACK. Every chatbot answer comes from your Copilot
   Studio flow or the widget shows an error. This is deliberate: a page that
   silently answers from a local keyword list makes a completely dead RAG
   pipeline look alive, which is the most expensive failure mode in this lab.
   (The COURSES array below renders the course cards on the page. It is never
   used to answer a chat message.)
   ===================================================================== */

const CONFIG = {
  STORAGE_KEY: "cookbake.webhookUrl",
  DEFAULT_WEBHOOK_URL: "",
  // Copilot Studio's Response node returns { reply: "..." };
  // n8n's Respond to Webhook node returns { output: "..." }.
  RESPONSE_KEYS: ["reply", "output", "text", "answer", "response", "message"],
};

/* ---------------------------------------------------------------------
   Lab configuration panel — the webhook URL lives here, not in this file
   --------------------------------------------------------------------- */
const WebhookConfig = (() => {
  const input = document.getElementById("webhookUrl");
  const status = document.getElementById("webhookStatus");

  const get = () => (input ? input.value.trim() : "");

  function render() {
    if (!input || !status) return;
    input.classList.remove("invalid");
    const url = get();

    if (!url) {
      status.textContent =
        "No flow URL set — paste your Copilot Studio HTTP POST URL below.";
      status.className = "config-status is-warn";
    } else if (!url.startsWith("https://")) {
      status.textContent = "The URL must start with https://";
      status.className = "config-status is-warn";
      input.classList.add("invalid");
    } else if (!url.includes("triggers/manual/paths/invoke")) {
      status.textContent = "This does not look like a Power Platform HTTP trigger URL.";
      status.className = "config-status is-warn";
    } else if (!url.includes("sig=")) {
      status.textContent = "URL is missing its sig= signature — it was truncated on copy.";
      status.className = "config-status is-warn";
      input.classList.add("invalid");
    } else {
      status.textContent = "HTTP POST URL detected. The flow must be Published.";
      status.className = "config-status is-ok";
    }
  }

  if (input) {
    input.value = localStorage.getItem(CONFIG.STORAGE_KEY) || CONFIG.DEFAULT_WEBHOOK_URL;
    input.addEventListener("input", () => {
      const url = get();
      if (url) localStorage.setItem(CONFIG.STORAGE_KEY, url);
      else localStorage.removeItem(CONFIG.STORAGE_KEY);
      render();
    });
    render();
  }

  return { get };
})();



const COURSES = [
  { code:"BAK-101", title:"Artisan Sourdough Bread Baking", cat:"Bakery", level:"Beginner", weeks:4, fee:680, campus:"Bakehouse", img:"1589367920969-ab8e050bbb04" },
  { code:"BAK-102", title:"French Pastry & Viennoiserie", cat:"Bakery", level:"Intermediate", weeks:8, fee:1480, campus:"Bakehouse", img:"1509440159596-0249088772ff" },
  { code:"BAK-103", title:"Wedding Cake Design & Decoration", cat:"Bakery", level:"Advanced", weeks:6, fee:1280, campus:"Bakehouse", img:"1535141192574-5d4897c12636" },
  { code:"BAK-104", title:"Macaron Masterclass", cat:"Bakery", level:"Intermediate", weeks:2, fee:420, campus:"Bakehouse", img:"1558326567-98ae2405596b" },
  { code:"BAK-105", title:"Chocolate & Confectionery Making", cat:"Bakery", level:"Intermediate", weeks:4, fee:760, campus:"Bakehouse", img:"1511381939415-e44015466834" },
  { code:"BAK-106", title:"Cupcake & Cake Pops Workshop", cat:"Bakery", level:"Beginner", weeks:1, fee:220, campus:"Bakehouse", img:"1486427944299-d1955d23e34d" },
  { code:"BAK-107", title:"Bread Making Fundamentals", cat:"Bakery", level:"Beginner", weeks:3, fee:480, campus:"Bakehouse", img:"1549931319-a545dcf3bc73" },
  { code:"BAK-108", title:"Cookie & Biscuit Baking", cat:"Bakery", level:"Beginner", weeks:1, fee:180, campus:"Bakehouse", img:"1499636136210-6f4ee915583e" },
  { code:"BAK-109", title:"Pie & Tart Specialist", cat:"Bakery", level:"Intermediate", weeks:3, fee:560, campus:"Bakehouse", img:"1535920527002-b35e96722eb9" },
  { code:"BAK-110", title:"Korean & Asian Bakery", cat:"Bakery", level:"Intermediate", weeks:4, fee:720, campus:"Bakehouse", img:"1558961363-fa8fdf82db35" },
  { code:"CUL-201", title:"Italian Cuisine Mastery", cat:"Cooking", level:"Intermediate", weeks:6, fee:1180, campus:"Culinary", img:"1551183053-bf91a1d81141" },
  { code:"CUL-202", title:"Thai Street Food Cooking", cat:"Cooking", level:"Beginner", weeks:3, fee:540, campus:"Culinary", img:"1559314809-0d155014e29e" },
  { code:"CUL-203", title:"Japanese Sushi & Sashimi", cat:"Cooking", level:"Intermediate", weeks:4, fee:980, campus:"Culinary", img:"1579871494447-9811cf80d66c" },
  { code:"CUL-204", title:"French Culinary Foundations", cat:"Cooking", level:"Beginner", weeks:8, fee:1580, campus:"Culinary", img:"1414235077428-338989a2e8c0" },
  { code:"CUL-205", title:"Chinese Wok Cooking", cat:"Cooking", level:"Beginner", weeks:3, fee:520, campus:"Culinary", img:"1525755662778-989d0524087e" },
  { code:"CUL-206", title:"Indian Curry & Spices", cat:"Cooking", level:"Beginner", weeks:3, fee:500, campus:"Culinary", img:"1505253758473-96b7015fcd40" },
  { code:"CUL-207", title:"Healthy Meal Prep & Nutrition", cat:"Cooking", level:"Beginner", weeks:2, fee:360, campus:"Culinary", img:"1490645935967-10de6ba17061" },
  { code:"CUL-208", title:"Vegetarian & Vegan Cuisine", cat:"Cooking", level:"Beginner", weeks:3, fee:540, campus:"Culinary", img:"1512621776951-a57141f2eefd" },
  { code:"CUL-209", title:"Grilling & BBQ Mastery", cat:"Cooking", level:"Intermediate", weeks:2, fee:460, campus:"Culinary", img:"1555939594-58d7cb561ad1" },
  { code:"CUL-210", title:"Knife Skills & Kitchen Essentials", cat:"Cooking", level:"Beginner", weeks:1, fee:160, campus:"Culinary", img:"1556909212-d5b604d0c90d" },
];

const CAMPUSES = {
  Bakehouse: "Sweet Heights Bakery Campus, 123 Orchard Road, #04-12, Singapore 238888",
  Culinary:  "Flavour Lab Culinary Campus, 88 Bukit Timah Road, #02-05, Singapore 229841",
};

const imgUrl = (id) => `https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=700&q=70`;

/* ---------------------------------------------------------------------
   Render course cards + filters
   --------------------------------------------------------------------- */
function renderCourses(filter = "all") {
  const grid = document.getElementById("course-grid");
  const list = COURSES.filter((c) => filter === "all" || c.cat === filter);
  grid.innerHTML = list.map((c) => `
    <article class="card">
      <div class="card__img" style="background-image:url('${imgUrl(c.img)}')">
        <span class="card__tag">${c.cat === "Bakery" ? "🧁 Bakery" : "🍳 Cooking"}</span>
        <span class="card__lvl">${c.level}</span>
      </div>
      <div class="card__body">
        <h3>${c.title}</h3>
        <div class="card__meta">
          <span>🕒 ${c.weeks} week${c.weeks > 1 ? "s" : ""}</span>
          <span>📍 ${c.campus === "Bakehouse" ? "Orchard Rd" : "Bukit Timah"}</span>
        </div>
        <div class="card__foot">
          <span class="card__price">S$${c.fee}</span>
          <button class="card__ask" onclick="window.CookBakeChat.ask('Tell me about the ${c.title.replace(/'/g,"")} course')">Ask &amp; enrol →</button>
        </div>
      </div>
    </article>`).join("");
}

document.getElementById("filters").addEventListener("click", (e) => {
  const btn = e.target.closest(".chip");
  if (!btn) return;
  document.querySelectorAll(".chip").forEach((c) => c.classList.remove("is-active"));
  btn.classList.add("is-active");
  renderCourses(btn.dataset.filter);
});
renderCourses();

/* =====================================================================
   Chatbot widget
   ===================================================================== */
const CookBakeChat = (() => {
  const panel  = document.getElementById("chat");
  const fab    = document.getElementById("chat-fab");
  const body   = document.getElementById("chat-body");
  const form   = document.getElementById("chat-form");
  const input  = document.getElementById("chat-text");
  const suggest= document.getElementById("chat-suggest");
  let greeted = false;

  function open() {
    panel.classList.add("is-open");
    panel.setAttribute("aria-hidden", "false");
    fab.style.display = "none";
    if (!greeted) { greet(); greeted = true; }
    setTimeout(() => input.focus(), 250);
  }
  function close() {
    panel.classList.remove("is-open");
    panel.setAttribute("aria-hidden", "true");
    fab.style.display = "grid";
  }
  function toggle() { panel.classList.contains("is-open") ? close() : open(); }

  function greet() {
    addMsg("bot",
      "👋 Hi! I'm the **Cook & Bake Academy** course assistant.\n\n" +
      "Ask me anything about our cooking & bakery courses — duration, course fees, locations, schedules or what you'll learn!");
  }

  function addMsg(who, text, extraClass) {
    const el = document.createElement("div");
    el.className = `msg msg--${who}${extraClass ? " " + extraClass : ""}`;
    el.innerHTML = formatText(text);
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  }

  function formatText(t) {
    return t
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");
  }

  function showTyping() {
    const el = document.createElement("div");
    el.className = "msg msg--bot";
    el.innerHTML = '<span class="typing"><span></span><span></span><span></span></span>';
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  }

  async function send(text) {
    text = (text || "").trim();
    if (!text) return;
    addMsg("user", text);
    input.value = "";
    suggest.style.display = "none";
    const typing = showTyping();

    const url = WebhookConfig.get();

    // There is deliberately NO local fallback. Every answer on this page comes
    // from the Copilot Studio flow or it does not come at all — a chatbot that
    // silently answers from a local keyword list makes a dead RAG pipeline look
    // alive, which is the single most expensive failure mode in this lab.
    if (!url) {
      typing.remove();
      addMsg("bot",
        "⚠️ **No flow URL set.**\n" +
        "Paste your Copilot Studio HTTP POST URL into the Lab configuration panel.",
        "msg--offline");
      return;
    }

    try {
      const reply = await callWebhook(url, text);
      typing.remove();
      if (!reply || !reply.trim()) {
        addMsg("bot",
          "⚠️ **The flow replied, but the answer was empty.**\n" +
          "The run succeeded and returned no text. Check the Agent node's output " +
          "in the flow's Monitor tab.",
          "msg--offline");
        return;
      }
      addMsg("bot", reply);
    } catch (err) {
      typing.remove();
      addMsg("bot",
        "⚠️ **The request to your flow failed.**\n" + err.message + "\n\n" +
        "If the flow's Monitor tab shows a successful run, this is CORS — the " +
        "browser blocked the reply. Serve this page from SharePoint rather than localhost.",
        "msg--offline");
    }
  }

  async function callWebhook(url, text) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chatInput: text, message: text, sessionId: getSession() }),
    });
    if (!res.ok) throw new Error(`The agent returned HTTP ${res.status}.`);

    // The flow may answer as JSON ({"reply": "..."}) or as plain text, depending
    // on whether the Response node wraps the agent's output. Accept both — read
    // the body as text first, then parse it as JSON only if it looks like JSON.
    const raw = (await res.text()).trim();
    if (!raw) return "";
    if (raw.startsWith("{") || raw.startsWith("[")) {
      try {
        const data = JSON.parse(raw);
        for (const k of CONFIG.RESPONSE_KEYS) {
          if (data && typeof data[k] === "string") return data[k];
        }
        return typeof data === "string" ? data : JSON.stringify(data);
      } catch {
        return raw; // looked like JSON but was not — show it rather than throw
      }
    }
    return raw;
  }

  function getSession() {
    let s = sessionStorage.getItem("cb_session");
    if (!s) { s = "web-" + Math.random().toString(36).slice(2); sessionStorage.setItem("cb_session", s); }
    return s;
  }

  // wire events
  form.addEventListener("submit", (e) => { e.preventDefault(); send(input.value); });
  suggest.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (b) { open(); send(b.textContent); }
  });

  return { open, close, toggle, ask: (q) => { open(); setTimeout(() => send(q), 300); } };
})();

window.CookBakeChat = CookBakeChat;
