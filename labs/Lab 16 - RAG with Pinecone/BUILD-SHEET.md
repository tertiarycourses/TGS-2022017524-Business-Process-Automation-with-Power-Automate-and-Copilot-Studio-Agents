# Build sheet — Cook & Bake Course Assistant (RAG over 20 brochures)

Environment: the learner's **Training Class** Sandbox (for example **Training Class 1**)
Flow: **`Lab 16 - RAG with Pinecone`** — trigger → HTTP → Compose → Agent → Response

Terse reference. The teaching version is [`README.md`](README.md).

> **Verified working end to end on 2026-08-02.** Every value below was read off
> the live flow, not from documentation.

---

## Node 0 — Ingestion (run once, before the flow)

```bash
export PINECONE_API_KEY=pcsk_...
python3 ingest_brochures.py
```

The script does three things and prints the URL you need in Node 2:

**1. Create the index with an integrated embedding model**

```json
POST https://api.pinecone.io/indexes/create-for-model
{ "name": "lab16-course-brochures", "cloud": "aws", "region": "us-east-1",
  "embed": { "model": "llama-text-embed-v2", "field_map": { "text": "chunk_text" } } }
```

| | |
|---|---|
| Model | `llama-text-embed-v2` — Pinecone-hosted |
| Dimension | **1024** — a property of the model, not a choice |
| `field_map` | **the embedding config**: embed whatever is in `chunk_text` |

> Name the field anything other than `chunk_text` on upload and records are
> stored **with no vector and no error**.

**2. Upload the 20 brochures as TEXT** — NDJSON, one object per line, no array:

```
POST https://{HOST}/records/namespaces/__default__/upsert
Content-Type: application/x-ndjson

{"_id":"BAK-101","chunk_text":"…whole brochure…","source":"…","course_code":"BAK-101"}
```

One record per brochure, whole. ~685 tokens each, inside the model's 2048 limit.

**3. Verify** — 20 vectors, and "How much is the sourdough course?" → BAK-101 @ 0.53.

### No embeddings model in the flow

| | With integrated inference |
|---|---|
| Ingestion | Upload text — Pinecone embeds it |
| Query | Send text — same model, automatically |
| Model / dims | Pinecone's: llama-text-embed-v2, 1024 |
| passage vs query | Handled by the index |
| Can mismatch? | **Yes, silently** | No |

---

## Reference values

| Thing | Value |
|---|---|
| Index host | `lab16-course-brochures-XXXXXX.svc.aped-4627-b74a.pinecone.io` |
| Namespace | default — written **`__default__`** in the URL path |
| SharePoint | `…/sites/CookandBakeAcademy/Shared Documents/CourseBrochures` |

> Do not confuse this with `course-brochures` (3072 dims, Gemini) — that is the

---

## Node 1 — Trigger

**When a HTTP request is received**

- **Who can trigger:** *Anyone (no authentication)*
- **Relative path:** **blank** (a value breaks Publish)

```json
{
  "type": "object",
  "properties": {
    "message":   { "type": "string" },
    "history":   { "type": "string" },
    "sessionId": { "type": "string" },
    "source":    { "type": "string" }
  },
  "required": ["message"]
}
```

---

## Node 2 — HTTP (retrieval)

| Field | Value |
|---|---|
| Method | `POST` ← **separate dropdown, not part of the URI** |
| URI | `https://lab16-course-brochures-XXXXXX.svc.aped-4627-b74a.pinecone.io/records/namespaces/__default__/search` |

**Headers** (click *Show all* under Advanced parameters):

| Key | Value |
|---|---|
| `Api-Key` | the key itself, starting `pcsk_` |
| `Content-Type` | `application/json` |
| `X-Pinecone-Api-Version` | `2025-04` |

**Body:**

```json
{"query":{"inputs":{"text":"@{triggerBody()?['message']}"},"top_k":3},"fields":["course_code","chunk_text"]}
```

Insert the `message` token with the ⚡ picker.

> - The key goes in **Headers**, never in *Authentication*.
> - Paste the **key**, not `PINECONE_API_KEY` — Power Automate cannot read `.env`.
> - Header names truncate on screen; check `X-Pinecone-Api-Version` kept its `X`.
> - No embedding step: the index has a hosted model, so you send **text**.

---

## Node 3 — Compose (the prompt)

**Function → Data Operations → Compose.** Inputs, via the `</>` editor:

```
concat('Customer question: ', triggerBody()?['message'], '

Course brochures:
', string(body('HTTP')))
```

`string()` escapes the quotes and newlines inside the brochures. Without it the
prompt breaks.

Exists because **the Agent node has no input field** — and because its output is
visible in the run history, which is how you debug an empty answer.

---

## Node 4 — Agent

### Instructions — paste the prose

```
You are the customer care assistant for Cook & Bake Academy, a cooking and bakery school in Singapore.

Answer the customer's question using only the course brochures provided below. They are the only knowledge you have.

If the brochures do not answer the question, say "I don't have that in our course information" and offer the team on +65 6888 1234 or enrol@cookbakeacademy.sg.

Never invent a fee, a date, a duration, a course code, an instructor name or a discount. If a number is not in a brochure, you do not know it.

If we do not run a course, say so plainly, then list the two or three closest courses we do run.

Always give the course code (for example BAK-101) next to the course title. Quote fees in Singapore dollars exactly as written.

Be warm and brief — two to four short sentences. Never mention brochures, searching, or that you are reading documents.

COURSE BROCHURES AND CUSTOMER QUESTION:
```

### Then insert the reference with the ⚡ picker  ← *the step that breaks everything*

Cursor at the very end → **⚡** → **Compose** → **Outputs**. A blue chip appears.

> **Never paste `@{outputs('Compose')}` as text.** Instructions is a rich-text
> editor: it stores pasted expressions as plain characters, or escapes
> underscores in node names (`Normalise_Enquiry` → `Normalise\_Enquiry`).
>
> **A reference to nothing resolves to empty, not to an error.** Green node,
> successful run, no answer.
>
> Diagnose from **Agent → Run Details → Outputs**. If it says *"the course
> brochures weren't included in your message"*, the chip is missing.

### Settings

| Setting | Value |
|---|---|
| Web search | **Off** |
| Request human assistance | **Off** |
| Output | **Text response** |

> There is **no *Use general knowledge* toggle** and **no temperature** on a
> workflow Agent node — those belong to a Copilot Studio *agent*. Grounding here
> rests on instruction wording alone.

---

## Node 5 — Response

| Field | Value |
|---|---|
| Status Code | `200` |
| Body | `{ "reply": "` ⚡**Agent Response** `" }` |

> The output field is **`Agent Response`**, not `text`. Typing `body/text` yields
> an empty string and no error.

---

## Publish

**Publish**, not Save — the endpoint serves the published version.
**⋯ → Version history**: `LIVE` and `CURRENT DRAFT` must match.

Copy the **HTTP POST URL** from the trigger. It must end with `sig=…`.

---

## Test

```bash
curl -X POST "<HTTP POST URL>" \
  -H "Content-Type: application/json" \
  -d '{"message":"How much is the sourdough course?"}'
```

Expect ~15s and an answer naming **BAK-101** and **SGD $680**.

Then the website — **just double-click `website/index.html`.**

Verified against a live tenant: this gateway returns
`access-control-allow-origin: *` and passes CORS preflight even from
`Origin: null`, which is what `file://` sends. No local web server, no SharePoint
hosting, no browser flags.

```bash
# only if localStorage misbehaves on file:// and Lab configuration keeps forgetting the URL
cd website && python3 -m http.server 8033
```

Paste the URL into **Lab configuration**.

| # | Question | A good answer |
|---|---|---|
| TC1 | How much is the sourdough course? | BAK-101 + exact fee |
| TC2 | How long is the French Pastry course? | BAK-102 + duration |
| TC3 | Where are your campuses? | Both, with addresses |
| TC4 | Cooking courses for beginners? | Two or three, not twenty |
| TC5 | What is CUL-203 about? | Sushi & Sashimi + curriculum |
| TC6 | Cheaper — macarons or cookies? | Both fees + which |
| **TC7** | Vietnamese pho course? | **"We don't run that"** + closest |
| **TC8** | Who teaches the macaron class? | **"Not in our course information"** |
| **TC9** | The 40% alumni discount on sushi? | **Does not confirm it** |
| TC10 | Recommend a restaurant? | Declines, steers back |

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `{"reply": ""}`, run succeeds | Instructions chip missing or mangled. Check Agent → Run Details → Outputs. Re-insert with ⚡. |
| Empty reply, but Agent Outputs show a real answer | Response node reads the wrong field — must be **Agent Response**. |
| `Unauthorized` on HTTP | `Api-Key` holds a variable name or a truncated key. Must start `pcsk_`. |
| Sudden 401 after it worked | The index was deleted. `GET https://api.pinecone.io/indexes`. |
| Fee that is in no brochure | Check the Compose output in the run history — did retrieval return anything useful? |
| Website: *"request to your flow failed"* | Not Published, or the URL lost its `sig=`. |
| `Failed to fetch`, run succeeded | **Not CORS** — this gateway sends `access-control-allow-origin: *` and passes preflight from `file://`. Check the URL kept its `sig=`, and that the flow is Published. |
| ~15s per answer | Normal. It calls a model. |
| Edited a brochure, answer unchanged | Vectors are a copy made at ingestion. Re-ingest. |
