# Build sheet — Lab 9: RAG with a Knowledge base

The same chatbot as [Lab 10](../Lab 10 - RAG with Pinecone/README.md), with the entire retrieval half
deleted.

Flow: `Lab3a - RAG with Knowledge Base`

```
Lab 10:   Trigger →  HTTP  →  Compose  →  Agent  →  Response      5 nodes
Lab 9:   Trigger →                        Agent  →  Response      3 nodes
```

**In Copilot Studio, RAG is not a node.** There is no ingestion workflow, no
embedding model, no vector store, no chunk size and no `top_k`. Retrieval happens
inside the Agent node the moment you attach a knowledge source.

> That absence is the lesson. Lab 10 needed a Python ingestion script, a Pinecone
> index, an API key and two extra nodes before a single question could be asked.
> Here all of it is replaced by uploading files to SharePoint and pointing at the
> folder. What that convenience costs you is the debrief.

---

## Node 0 — SharePoint: the knowledge source

The flow is trivial; the grounding is the work. Follow **Task 0** in the
[README](README.md) — create a `Cook and Bake Academy` site, a `CourseBrochures`
folder, upload the 20 `.txt` files from [`brochures/`](brochures/).

Confirm the library shows **20 items**, and point at the **folder**, not the
library root — the root would pull in Module 4's banking documents and answer a
sourdough question out of a KYC policy.

### Then wait for indexing

SharePoint must crawl the files before the agent can retrieve anything. This is
minutes, not seconds, and there is no progress bar.

**A knowledge source that is still indexing returns nothing, and the agent looks
broken when it is merely empty.**

---

## Node 1 — Trigger

**When a HTTP request is received.**

| Field | Value |
|---|---|
| Who can trigger | **Anyone (no authentication)** |
| Relative path | **leave blank** — a value here breaks Publish |

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

## Node 2 — Agent

### 2a — Knowledge  ← the whole lab

**Knowledge → + → SharePoint**, and paste the folder URL:

```
https://YOURTENANT.sharepoint.com/sites/CookandBakeAcademy/Shared%20Documents/CourseBrochures
```

**There is no file upload in this picker** — only *Public websites* and
*SharePoint*. That is why the brochures had to go to SharePoint first; the upload
is not a convenience, it is the only route in.

> **Do not choose *Public websites*.** It grounds the assistant in whatever is
> live on the open web — a competitor's fee, quoted to your customer, in your
> academy's voice.

**What Copilot Studio just did silently:** chunked each brochure, chose an
embedding model, chose a dimension, indexed the vectors, and picked how many
results to return. You chose none of those. In Lab 10 you chose all of them.

### 2b — Instructions

Paste **Version B** from [`agent/instructions.md`](agent/instructions.md), then
insert the question with the ⚡ picker: cursor after `Customer question:` →
**⚡ → When a HTTP request is received → message**.

> ### ⚠️ The wording differs from Lab 10, and this is where the day goes
>
> 3b says *"using only the course brochures **provided below**"* — correct there,
> because Compose injects them. Lab 9 injects nothing; the agent must search.
> The line must read:
>
> ```
> Search your knowledge source for the Cook & Bake Academy course brochures
> and answer from what you find there.
> ```
>
> Leave 3b's wording in place and the agent is told its only permitted source is
> empty. It then produces **nothing at all** — not even the refusal sentence the
> instruction defines. The flow returns `{ "reply": "" }` in ~25s and looks
> broken for reasons that have nothing to do with SharePoint.

### 2c — If you built this by copying Lab 10

Duplicating the flow carries 3b's Instructions verbatim, including its final
chip:

```
COURSE BROCHURES AND CUSTOMER QUESTION:{outputs('builtinFunction-d20387b9-…')}
```

That `builtinFunction-…` is 3b's Compose node, which does not exist here. The
canvas shows `This input references action "builtinFunction-d2…", which is not on
the canvas` — **and the flow still runs green and returns an empty string.**

Clear the Instructions box completely before pasting Version B.

### 2d — Settings

| Setting | Value |
|---|---|
| Web search | **Off** |
| Request human assistance | **Off** |
| Output | **Text response** |

> No *Use general knowledge* toggle and no temperature — those belong to a
> Copilot Studio *agent*, not a workflow *Agent node*. Grounding rests entirely
> on instruction wording, which is strictly weaker than a platform switch.

### 2e — Citation markers

A Knowledge source appends grounding metadata the model did not write. Without an
explicit line, replies arrive **duplicated** — once with `[doc:turn1doc11]`
markers, again with `[1]`:

```
…priced at **SGD $680**, which includes ingredients…[doc:turn1doc11].
…priced at **SGD $680**, which includes ingredients…[1].
```

Version B carries the fix:

```
Never include citation markers, reference numbers or source tags in your reply.
```

The *"never mention brochures or searching"* line does **not** cover it — these
are added after generation. **Neither defect occurs in Lab 10**, where retrieved
text arrives as plain Compose output.

---

## Node 3 — Response

| Field | Value |
|---|---|
| Status Code | `200` |
| Headers | `Content-Type` : `application/json` |
| Body | `{ "reply": "` ⚡**Agent Response** `" }` |

Use the ⚡ picker for the output. Typing `body/text` yields an empty string and no
error — indistinguishable from the instruction fault above, which is why it costs
so much time.

---

## Publish and test

**Publish**, not Save. **⋯ → Version history**: `LIVE` and `CURRENT DRAFT` must
match.

```bash
curl -X POST "<HTTP POST URL>" \
  -H "Content-Type: application/json" \
  -d '{"message":"How much is the sourdough course?"}'
```

Expect ~25s — slower than 3b, because SharePoint retrieval plus generation is a
longer round trip than a Pinecone query.

Then the website: **double-click `website/index.html`.** This gateway sends
`access-control-allow-origin: *` and passes preflight from `file://`, so no local
server is needed.

Run all ten rows of [`sample-questions.csv`](sample-questions.csv). TC1–TC6 check
retrieval; **TC7–TC9 are the ones that matter** — each plants something false or
absent and invites the model to agree.

---

## The comparison worth running in class

Same brochures, same questions, same agent instructions apart from one line.

| | Lab 10 — Pinecone | Lab 9 — Knowledge base |
|---|---|---|
| Nodes | 5 | 3 |
| Ingestion | A Python script, run once | Upload to SharePoint |
| Embedding model | `llama-text-embed-v2`, visible in the script | Hidden |
| Dimension | 1024, printed by the script | Unknown |
| Chunking | One brochure = one record, **your decision** | Hidden |
| Results returned | `top_k: 3`, **your decision** | Hidden |
| Cost per question | A Pinecone query + a model call | A model call |
| Citation markers | None | Leak into the reply |
| Changing a fee | Edit + **re-ingest** | Edit + wait for re-crawl |
| What you can tune when it answers badly | All four levers above | The prompt |

**That last row is the debrief.** When Lab 9 retrieves the wrong brochure, there
is no chunk size to change, no `top_k` to raise, no embedding model to swap. You
can rewrite the instruction and hope. Lab 10 gives you four levers and four ways
to get it wrong.

Neither is the right answer. Which one is right depends on whether the person
maintaining it will ever need those levers — and that is a staffing question, not
a technical one.

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `{"reply": ""}`, run succeeds | **First suspect the Instructions wording**, not the knowledge source. If it still says "provided below" with nothing below, that is the cause. Then check for a stale `builtinFunction-…` reference. |
| Empty reply, but Agent Outputs show a real answer | Response node reads the wrong field — must be **Agent Response**. |
| Every answer is "I don't have that in our course information" | The knowledge source is still indexing, or the folder URL points somewhere with no brochures. |
| Replies appear twice, with `[1]` / `[doc:turnNdocN]` | Missing the citation-marker line. See 2e. |
| It answers about banking | The knowledge source points at a library shared with Module 4. |
| One course is always missing | The library has 19 items, not 20. |
| `Failed to fetch`, run succeeded | **Not CORS on this gateway.** Check the URL kept its `sig=`, and that the flow is Published. |
| ~25s per answer | Normal. Retrieval plus a model call. |
