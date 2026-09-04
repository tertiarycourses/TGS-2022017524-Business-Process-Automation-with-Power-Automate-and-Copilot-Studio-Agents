# Meridian Asset Management — advisory website (Copilot Studio edition)


The site, the styling and the ten trainer demo questions are unchanged. Only the
integration layer differs.

---

## Running it

```bash
cd website
python3 -m http.server 8000
```

Open <http://localhost:8000/index.html>.

> Serve it over HTTP. Opening `index.html` straight off the filesystem gives it
> an opaque `null` origin, which the browser will not let you POST from.

---

## Wiring it to your workflow

1. In Copilot Studio, open `Lab 13 - HTTP and Chatbot` and click the
   **When a HTTP request is received** trigger.
2. Copy the **HTTP POST URL** from the bottom of the panel.
3. Paste it into **Lab configuration** on the page.

The URL is remembered in `localStorage`, so learners paste it once per browser.

⚠️ **Published, not just saved.** The endpoint serves the *published* version.

---

## What it posts

```json
{
  "message":   "Is the initial consultation free?",
  "name":      "Rachel Ong",
  "phone":     "+65 9123 4567",
  "email":     "you@example.com",
  "history":   "visitor: … | agent: …",
  "sessionId": "web-1a2b3c",
  "source":    "Website chat"
}
```

Seven fields, only `message` required.

## What it expects back

```json
{ "reply": "Yes — the initial consultation is free…" }
```

If the shape is wrong the chat bubble shows `[object Object]`.

---

## Where the memory lives

A Copilot Studio workflow is **stateless** — every HTTP request is independent,
and there is no memory node to add. So the transcript lives in the browser:
`script.js` keeps a `transcript` array and posts the last six messages as a
`history` string with every request.

| | In this build |
|---|---|
| Who remembers | The browser |
| Window size | `HISTORY_TURNS` in `script.js` |
| Survives a page refresh | **No** |

That last row is worth demonstrating in class. Refresh mid-conversation and the
agent has forgotten the visitor's name — so the contact gate closes again.

---

## Files

| File | Purpose |
|---|---|
| `index.html` | Hero, services, the lab config panel, and the floating chat widget |
| `style.css` | White-theme advisory styling |
| `script.js` | Widget behaviour, the contact gate, transcript history, and the POST |

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `Failed to fetch`, but the run succeeded | CORS. Serve the page from SharePoint, not `localhost`. |
| `Failed to fetch`, and no run at all | The workflow is saved but not **Published**, or the URL is wrong. |
| The chat replies `[object Object]` | The Response body is not `{ "reply": "..." }`. |
| The agent answers before collecting details | The contact gate was weakened, or `chatStep` in `script.js` was edited. |
| The agent forgets after a refresh | Expected. The transcript is in the page, not the server. |
| The suggestion chips never appear | They stay hidden until name, phone and email are all given. |
