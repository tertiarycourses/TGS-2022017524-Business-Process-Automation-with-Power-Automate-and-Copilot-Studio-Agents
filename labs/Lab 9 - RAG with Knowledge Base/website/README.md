# Cook & Bake Academy — course assistant website (Copilot Studio edition)


The page, styling and the course cards are unchanged. Only the integration
layer differs — and one deliberate behavioural change, below.

---

## Running it

```bash
cd website
python3 -m http.server 8033
```

Open <http://localhost:8033/index.html>.

> Serve it over HTTP. Opening `index.html` straight off the filesystem gives it
> an opaque `null` origin, which the browser will not let you POST from.

---

## Wiring it to your flow

1. In Copilot Studio, open the flow and click the
   **When a HTTP request is received** trigger.
2. Copy the **HTTP POST URL** from the bottom of the panel.
3. Paste it into **Lab configuration** on the web page.

The URL is remembered in `localStorage`, so learners paste it once per browser.

---

## What the page expects back

`script.js` accepts **either** shape, because the two are easy to confuse when
building the Response node:

**JSON** (what the build sheet asks for) — the first key found from
`reply`, `output`, `text`, `answer`, `response`, `message`:

```json
{ "reply": "BAK-101 Artisan Sourdough Bread Baking is S$680 for 4 weeks." }
```

**Plain text** — the bare agent output, with no wrapper. Also fine.

The widget reads the body as text first and only parses JSON when it starts with
`{` or `[`. Without that, a bare-text response throws
`Unexpected token 'A', "The Artisan"... is not valid JSON` and looks like a
network failure when the flow actually worked.

---

## The publish trap

The HTTP endpoint serves the **published** version of the flow. Saving is not
enough. After any edit you must click **Publish**.

Confirm with **⋯ → Version history** — if `LIVE` and `CURRENT DRAFT` are
different version numbers, you have an unpublished draft.

---

## CORS

Power Automate's HTTP trigger sends no `Access-Control-Allow-Origin` header,
and there is no setting for one.

**In practice it did not bite.** This page POSTs from `localhost:8033` to
`*.environment.api.powerplatform.com` and gets a normal response — verified
2026-08-02, same as Module 4.

If it ever does: the widget showing *"The request to your flow failed"* while the
flow's **Monitor** tab shows a **successful** run is the signature. Serve the page
from the SharePoint site rather than `localhost`.

> **Do not "fix" it by disabling browser security.** Launching Chrome with
> `--disable-web-security` removes protection for every site in that browser, not
> just this one. A parse error is far more likely than a real CORS block — read
> the actual message before reaching for a flag.

---

## Status as of 2026-08-02 — working end to end

Against the **NUS Copilot (Developer)** environment, flow **Lab 3 - RAG**
(trigger → HTTP to Pinecone → Compose → Agent → Response):

| Step | Evidence |
|---|---|
| Pinecone index populated | 20 vectors, `cookbake-brochures`, default namespace |
| Retrieval quality | "How much is the sourdough course?" → BAK-101 @ 0.53 |
| Grounded answer | Quotes BAK-101, SGD $680, 4 weeks, the real intakes and contact |
| Hallucination probe (TC7) | "Vietnamese pho" → refuses, offers CUL-202 and CUL-208 |
| Round trip | HTTP 200 in ~15s |
| CORS | **Not blocked** from `localhost:8033` against `*.environment.api.powerplatform.com` |

### The two bugs that cost the most time

Both failed **silently** — green node, successful run, no answer:

1. **The Compose reference in the Agent's Instructions.** Pasted as text, it was
   stored as plain characters and resolved to nothing. The agent received no
   question and no brochures, and said so — in its Run Details, where nobody
   looks. **Fix: insert it with the ⚡ picker, never paste.**
2. **The Response node read the wrong field.** The Agent's output is called
   **`Agent Response`**, not `text`. Reading `body/text` yields an empty string
   with no error.

### One widget change these caused

`callWebhook()` now reads the body as **text first** and only parses JSON when it
starts with `{` or `[`. A Response node that returns the bare agent output rather
than `{"reply": …}` therefore still works, instead of throwing
`Unexpected token 'W'`. Both shapes are accepted.

---

## Note on the Agent node vs the Copilot Studio agent

The README's headline setting — **Use general knowledge: Off** — does **not
exist** on the workflow *Agent node*. That toggle belongs to a Copilot Studio
*agent*, not to a flow.

Grounding here is enforced by the instruction text alone
(*"Answer only from the course brochures above"*), which is weaker than a
platform switch that makes ungrounded answers impossible.

That difference is worth raising in the debrief: the same product gives you a
hard control in one surface and only a soft one in the other, and you cannot
tell from the outside which you are relying on.
