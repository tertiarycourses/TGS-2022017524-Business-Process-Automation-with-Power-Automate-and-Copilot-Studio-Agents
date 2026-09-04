# Meridian Asset Management — client portal (Copilot Studio edition)


The site, the styling and the eight trainer demo cases are unchanged. Only the
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

1. In Copilot Studio, open `Lab 14 - HTTP and Human Review` and click the
   **When a HTTP request is received** trigger.
2. Copy the **HTTP POST URL** from the bottom of the panel.
3. Paste it into **Lab configuration → Copilot Studio workflow URL** on the page.

The URL is remembered in `localStorage`, so learners paste it once per browser.
No file is ever edited.

The status line under the box validates the URL as you type:

| Message | Meaning |
|---|---|
| No workflow URL set — the chat cannot send | Field is empty |
| Workflow URL detected. The workflow must be Published | Looks like a Power Platform trigger URL |
| This does not look like a Copilot Studio HTTP trigger URL | Copy it again from the trigger node |

⚠️ **Published, not just saved.** The endpoint serves the *published* version.
Check **⋯ → Version history**: `LIVE` and `CURRENT DRAFT` must match.

---

## What it posts

```json
{
  "clientName":  "Rachel Ong",
  "clientEmail": "you@example.com",
  "accountRef":  "MAM-77401",
  "portfolio":   "Global Growth",
  "message":     "My portfolio is down 14% this quarter…",
  "channel":     "Website chat"
}
```

Six fields, matching the trigger's Request Body JSON Schema. There is no
`sessionId` and no `history` — this is not a conversation. A client raises one
concern and a human answers it.

## What it expects back

```json
{
  "status":    "received",
  "ticketId":  "MAM-20260802-a607f8",
  "urgency":   "Medium",
  "escalated": true,
  "message":   "Thank you. Your message has reached the…"
}
```

Five fields, and **the draft is not one of them.** Neither is `emotionalTone`
nor `complianceFlags`. Those are internal assessments about a person; the
browser is not where they belong.

⚠️ `escalated` must be an unquoted **boolean** in the Response node. Quoted, it
arrives as the string `"false"` — and `Boolean("false")` is `true`, so every
calm client would be told a manager is calling them.

---

## The trainer demo dropdown

Eight cases, one per compliance path — see
[`../sample-queries.csv`](../sample-queries.csv). Selecting one fills the chat
form and opens the widget.

**It deliberately clears the email field.** The approved reply is a real email
sent to whatever address is typed there. Always use your own.

---

## Files

| File | Purpose |
|---|---|
| `index.html` | Hero, portfolios, the "how we respond" explainer, lab config panel, chat widget |
| `style.css` | White-theme asset-management styling |
| `script.js` | Widget behaviour, validation, the POST, and the acknowledgement receipt |

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `Failed to fetch`, but Activity shows a **successful** run | CORS. Copilot Studio's HTTP trigger has no allowed-origins setting. Serve the page from SharePoint rather than `localhost`. |
| `Failed to fetch`, and no run at all | The workflow is saved but not **Published**, or the URL is wrong. |
| The chat shows `[object Object]` | The Response body is not the five-field JSON above. |
| Every client is told "a manager will call you" | `escalated` is quoted in the Response node. Remove the quotes. |
| The receipt shows the whole enquiry object as the reference | `ticketId` is returning all of `Normalise_Enquiry`. It needs `outputs('Normalise_Enquiry')?['ticketId']`. |
| Nothing happens and the browser console is silent | The lab config panel is empty. Paste the HTTP POST URL. |
