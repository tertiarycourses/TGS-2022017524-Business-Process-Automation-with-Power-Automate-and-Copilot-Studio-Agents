---
name: copilot-studio-flows
description: Hard-won facts about building Copilot Studio / Power Automate agent flows in the NEW designer (the dark-canvas one inside copilotstudio.microsoft.com), and about wiring them to Pinecone, SharePoint, Excel Online, Outlook, Microsoft Teams approvals and a static website. Use whenever building, debugging or documenting a Copilot Studio workflow, an Agent node, a Human review / human-in-the-loop gate, a Power Automate HTTP action, a SharePoint list lookup, an Outlook send step, or a RAG lab that grounds an agent in documents. Covers the Instructions rich-text editor that silently mangles pasted expressions, structured output vs Parse JSON, why the Outlook To field rejects typed expressions with a trailing-newline error, why moving a node wipes its configuration, and why approval requests must go to Teams rather than Outlook. Every entry here was verified against a live tenant — believe these over guesses about how the product "should" work.
---

# Copilot Studio flows — what is actually true

This skill exists because a single LU3 RAG lab burned hours on wrong assumptions.
Everything below was verified against a live tenant on 2026-08-02. When the UI
and this file disagree, trust the UI and update this file.

> A second night (LU2b, human-in-the-loop) added the **Human review**, **structured
> output** and **rich-text editor** sections. Same lesson, learned again: eight
> publish-test cycles were spent theorising about a reference path when one look at
> the upstream node's *Run Details → Outputs* would have settled it in one.
>
> A third night (LU1, retail banking onboarding) added the **Outlook To field**,
> **node ordering**, **Filter Query** and **moved-node** sections. Six consecutive
> wrong fixes were proposed for one email error before the trainer solved it by
> switching from a typed expression to the ⚡ picker. The signal was in the error
> text from the first attempt — `'"someone@example.com\n"'` — and was read as
> "the value has a newline" instead of "typing produces a newline".

## The cardinal rule

**Never assert how a Copilot Studio field behaves without seeing it.** This
product has at least three designers that look similar and behave differently
(classic Power Automate, the new Power Automate designer, and the Copilot Studio
workflow designer). Guidance written for one is routinely wrong for another.
Ask for a screenshot before giving field-level instructions.

---

## The Agent node

### There is NO user-message / input field

In the Copilot Studio workflow designer, the Agent node's Configure tab has,
top to bottom, and nothing else:

```
Connection · Agent (model picker) · Instructions · Microsoft IQ ·
Tools · Knowledge · Request human assistance · Web search · Output
```

**Output is the last field.** Older build sheets say to "scroll past Web search
to find the input box" — that box no longer exists. The only place to put
per-call data is **Instructions**.

### There is NO "Use general knowledge" toggle

That switch belongs to a Copilot Studio *agent*, not to a workflow *Agent node*.
Grounding in a flow rests on instruction wording alone, which is strictly
weaker. Say so plainly rather than implying a hard control exists.

### There is NO temperature control

Do not promise one.

### A Knowledge source leaks citation markers, and duplicates the whole answer

Observed on LU3 with a SharePoint Knowledge source and Claude Sonnet 4.6. Every
reply came back **twice** — once carrying `[doc:turn1doc11]`-style markers, then
again with `[1]`-style ones:

```
…priced at **SGD $680**, which includes ingredients…[doc:turn1doc11].
…priced at **SGD $680**, which includes ingredients…[1].
```

Both are artefacts of grounded generation, and both reach the customer verbatim.
The instruction line *"never mention brochures, searching, or that you are
reading documents"* does **not** suppress them — they are appended by the
grounding layer, not written by the model.

Add an explicit line:

```
Never include citation markers, reference numbers or source tags in your reply.
```

Neither defect appears in the Pinecone flow, where retrieved text arrives as
plain Compose output with no citation metadata attached. Budget for this when
converting a lab from a vector store to a Knowledge source.

### Output has three modes — and one of them removes the need for Parse JSON

The **Output** dropdown offers *Text response*, *Structured output*, and
**Custom structured output** (define your own JSON schema).

**Use Custom structured output whenever anything downstream needs fields.** With
*Text response* you are asking the model for JSON and hoping; it will eventually
wrap the answer in ```` ```json ```` fences, or open with "Here is the JSON", or
return a prose summary — and the Parse JSON node fails with:

```
The 'content' property of actions of type 'ParseJson' must be valid JSON.
Error parsing NaN value. Path '', line 1, position 1.
```

*Position 1* means the first character is not `{`. Read the failing node's
**content** input to see what the model actually said — it is usually explaining
itself in prose.

Once structured output is set, **delete the Parse JSON node** and reference the
fields directly. The syntax is **slash-separated, not nested brackets**:

```
body('Rapport_Agent')?['structuredOutput/draftReply']
```

Note the trap: with structured output the *text* output becomes a human-readable
narration ("Classified, flagged, and drafted. Summary: …"), so a Parse JSON node
left in place now fails on prose rather than on fences. Same error, new cause.

### Clicking "Agent" in the left Add panel CREATES A NEW NODE

`page.locator('text=Agent').nth(1)` matches the Add-panel item, not the canvas
node, and silently adds "Agent 2" to the flow. Ctrl+Z does **not** remove it.
Delete it with `button[aria-label="Delete Agent 2"]`.

---

## The Instructions box is a RICH-TEXT editor — it mangles pasted expressions

This cost more time than anything else in two nights of building. The Agent
node's **Instructions** field is a markdown-aware rich-text editor, and pasting
an expression into it is not the same as typing one.

**It escapes underscores in node names.** Paste
`@{outputs('Normalise_Enquiry')?['message']}` and the editor stores
`Normalise\_Enquiry`. That reference points at a node which does not exist — and
a reference to a missing node **resolves to empty rather than erroring**. The
node stays green, the run succeeds, and the agent silently receives nothing.

**It swallows braces.** A sentence like `Start your response with { and end it
with }` had the braces absorbed into a chip, leaving the instruction as
nonsense.

**Symptoms, in the order you will meet them:**

1. The agent replies *"No client enquiry was included in this submission — only
   the system configuration instructions"* (it is telling you exactly what is
   wrong, in the one place nobody looks: the failing node's `content` input)
2. Everything classifies as the null case — `urgency: Low`, no flags, `escalate:
   false` — because the model is classifying an empty string
3. A red banner on the node: `This input references action "Normalise\_Enquiry"`

**The fix: always insert via the ⚡ picker, never paste.** Write the surrounding
prose as plain text with blank slots, then click into each slot and pick the
field from the dynamic-content tree. There is no way around the manual clicks —
any pasted text is subject to the same escaping.

If escaping persists, **rename the node without underscores** (`NormaliseEnquiry`)
and re-point every reference.

> **Corollary for lab authors:** never hand a learner a block of instructions
> with `@{...}` tokens in it and say "paste this". Hand them the prose with gaps
> and a table of which field goes in which gap.

---

### Copying a flow carries its Instructions references — and they resolve to EMPTY

**LU3, 2026-08-02.** `Lab3a - RAG with Knowledge Base` was built by duplicating
`Lab 3b - RAG with Pinecone`. The Agent's Instructions came across verbatim,
including 3b's final line:

```
COURSE BROCHURES AND CUSTOMER QUESTION:{outputs('builtinFunction-d20387b9-…')}
```

That `builtinFunction-…` is 3b's Compose node, which does not exist in 3a. The
canvas showed `This input references action "builtinFunction-d2…", which is not
on the canvas` — and the flow **still ran green, returning `{ "reply": "" }` in
~25s**.

**The retrieval architecture differs, and the instruction wording must follow.**

| | Pinecone flow | Knowledge-source flow |
|---|---|---|
| How brochures reach the agent | **Injected** as text via a Compose chip | **Not injected** — the agent searches |
| Correct instruction | "…using only the brochures provided below" | "**Search your knowledge source** for … and answer from what you find there" |

Left as "provided below" with nothing below it, the agent is told its only
permitted source is empty — so it emits **nothing at all**, not even the refusal
sentence the instruction defines. An empty string, not a refusal, is the tell.

**Rule: after duplicating a flow, open the Agent's Instructions and re-read the
last paragraph before anything else.** And when a RAG flow returns an empty
string rather than a refusal, suspect the *instruction premise* — not the
knowledge source, not the Response node.

## Expressions

- Fields holding **only** an expression resolve reliably.
- Expressions **embedded in prose** in the Instructions box are the prime
  suspect when an Agent returns empty text. Build the whole prompt in a
  **Compose** node and put `@{outputs('Compose')}` alone in Instructions.
- Reference an action by name with underscores for spaces, parentheses kept:
  `body('Get_file_content')`, `outputs('Get_files_(properties_only)')`.
- **Prefer the ⚡ dynamic-content picker over typing expressions.** Typed paths
  failed repeatedly; picker-inserted tokens worked. This also applies to LU1's
  email `To` field, where every typed form failed with a trailing-`\n` error.
- Single-quoted strings need doubled apostrophes: `'I don''t have that'`.
- Escape file content into JSON with `string(outputs('Compose'))` and **no
  surrounding quotes** — `string()` supplies them and escapes newlines/quotes.
  Hand-written `concat`/`replace` escape chains fail to parse in this editor.

### Functions that do NOT exist here

- **`workflow()`** — classic Power Automate exposes it for run metadata
  (`workflow()?['run']?['name']` = the run ID). This designer does not: the node
  shows `Unknown function: workflow` and will not save. For a unique reference,
  use `substring(replace(guid(),'-',''),0,6)`.
  *Cost of the substitution:* the run ID tied a record back to a specific run in
  Activity; a GUID does not. Say so rather than pretending it is equivalent.

### Things that look like masking but are not

`last(split(accountRef,'-'))` on `MAM-88213` returns `88213` — the **whole**
number. Rendered after four bullet characters it looks masked and is not. Use
`substring(x, sub(length(x), 4), 4)`.

A control that looks like a control but is not one is worse than no control,
because nobody inspects it twice.

### Booleans in a Response body must be UNQUOTED

```json
"escalated": @{body('Agent')?['structuredOutput/escalate']},
```

Quote it and the field returns the *string* `"false"` — and in JavaScript
`Boolean("false")` is `true`. Every browser consumer then reads the flag as set.
Strings keep their quotes; booleans must not have them.

**And wrap the token: `@{toLower(string(...))}`** (verified live 7 Aug 2026). An
agent's structured-output "boolean" sometimes arrives as the capitalised string
`True`; a bare unquoted token then renders `"escalated": True` — invalid JSON —
and the calling page dies with `Unexpected token 'T' … is not valid JSON`.
`toLower(string(...))` yields the lowercase literal `true`/`false` whether the
model produced a real boolean or a Python-style string.

### Arrays need `join()` before they reach Excel or a text field

`join(body('Agent')?['structuredOutput/complianceFlags'], ', ')`. Without it the
cell reads `System.Object[]`.

---

## The Human review node (the human-in-the-loop gate)

The designer has a first-class **Human review** node in the left Add panel. It is
the equivalent of n8n's Gmail `sendAndWait`, and it genuinely blocks: the run sits
at *Running* indefinitely until a person responds.

### Do not confuse it with the two look-alikes

| | What it is | Fires when | Audit trail |
|---|---|---|---|
| **Human review** (node) | A gate in the flow | **Always** | Outcome recorded |
| *Request human assistance* (Agent toggle) | The agent asking for help | Only if the **model** feels unsure | None |
| *Request information* (agent **tool**) | Same, exposed as a tool | Agent decides | None |

Only the node is a control. The toggle and the tool both let a *confidently
wrong* output through untouched — which is the failure that matters.

### It publishes ONLY the inputs you define

There is **no built-in `outcome` or `result` property**. Searching the ⚡ picker
for "outcome" returns nothing until you have created an input called that. A
hand-typed `body('Human_review')?['result']` silently never matches, so **every**
run falls to the Else branch and nothing is ever sent.

**Inputs are mandatory** — the node will not save with zero. Define two:

| Name | Type | Default |
|---|---|---|
| `Outcome` | **Yes/No** | **leave blank** |
| `Name` | Text | **leave blank** |

Then the If/Else condition is that `Outcome` token (⚡ picker), `Equals`, `true`.

**There is NO Choice input type** (re-verified 7 Aug 2026). The type picker
offers Text, Yes/No, Email, Number, Date only — earlier guidance saying
"Choice: Approve/Reject" describes a control that no longer exists. A Yes/No
input publishes a **boolean**, so the If/Else must compare against `true`,
never the strings "Approve" or "Yes". Frame the approve/reject meaning in the
Message text instead ("Approve to send… Reject to hand over…").

**Deleting and re-creating an input silently breaks the If/Else.** The old
token keeps rendering with the same name in the condition but resolves to
nothing — every response then falls to Else. After any input rebuild, remove
the token and re-pick it. (Found live 7 Aug 2026: a learner-edited Lab 8 had
`Outcome Equals <empty value>` — approvals were processed and the run completed
via Else, which contained nothing, so approving "did nothing".)

**The request lands in the Teams "Workflows" bot CHAT as an adaptive card —
NOT in the Teams Approvals app** (re-verified 7 Aug 2026; earlier note saying
Approvals app is wrong for this node). Card title:
`Request information | Microsoft Copilot Studio`. Delivery and response
processing each take a minute or two — a run sitting at *Running* for a couple
of minutes after Submit is normal.

### It does not record WHO responded

No responder, no email, no timestamp — just the inputs. So an "Approved By"
audit column has to be a **self-declared text input**, which is a convention, not
evidence. Say this plainly in courseware rather than implying the platform
captured an identity.

### `assignedTo` fails at runtime while looking fine in the designer

```
BadRequest — Required field 'assignedTo' is missing or empty.
```

Three causes, all of which display a normal-looking chip:

- an **external address** (gmail.com, or any domain outside the tenant) cannot be
  resolved by the directory;
- **typing an address and tabbing away** without clicking the resolved suggestion;
- a chip carrying only a **display name** with no routable address.

Type the full address, wait for the directory lookup, and **click the
suggestion**. Safest choice is the account the connection authenticated as.

### ⚠️ Channel: use TEAMS, not Outlook

The **Channel** dropdown offers Outlook and Teams. On a live tenant, **Outlook
created the request but never delivered the email** — to any address tried,
including tenant users. The run reached *Running* correctly; the mail simply
never arrived.

**Switching Channel to Teams fixed it immediately.** The request appears in the
Teams **Approvals** app (teams.microsoft.com → ••• → Approvals, or
approvals.microsoft.com), and responding there resumes the run.

Default to Teams in any lab or build sheet. If someone reports "the approval
never arrives", that is the first thing to change.

### The default value on a choice input is a design decision

Pre-filling `Outcome` with `Approve` means the field arrives at the approver
already answered: confirming takes no thought, rejecting takes noticing. That
converts a gate into a rubber stamp via a one-word setting invisible on the
canvas. Leave it blank; if a default is forced, use `Reject` so inattention fails
safe.

---

## The HTTP action

- **Method is a separate dropdown.** Do not put `POST` in the URI field.
- Headers truncate visually; a header named `X-Pinecone-Api-Version` can silently
  lose its leading `X`. Re-check character by character when you get a 4xx.
- **Never paste an env-var NAME as a header value.** `PINECONE_API_KEY` as the
  literal value yields `Unauthorized`. Power Automate cannot read `.env`.
- The **Authentication** section is for built-in schemes only. An API key goes in
  **Headers**, not there.
- Body, headers etc. are hidden until you click **Show all** under *Advanced
  parameters*.

---

## The SharePoint connector

- There is no "Read file" action. Use **Get files (properties only)** to list,
  then **Get file content** per item.
- `Get file content` → **File Identifier** = `@item()?['{Identifier}']`. The
  braces are literal.
- Keep **Infer content type = On** so `.txt` returns text, not base64.
- **Limit Entries to Folder does not accept a typed path.** Not
  `/CourseBrochures`, not `/Shared Documents/CourseBrochures`, not the full
  server-relative path — all return **Folder Not Found**. It wants an
  identifier: use the picker and **double-click** the folder (single click only
  expands it).
- **The reliable workaround:** clear *Limit Entries to Folder* entirely and set
  **Include Nested Items = Yes**. Lists the whole library including subfolders.
- **Filter Query** is OData, not a path. `FSObjType eq 0` returns files only —
  useful because a recursive listing includes the folder itself, which then
  fails `Get file content`.

### Get items — looking a record up by key (the duplicate-check pattern)

LU1: *does this NRIC already exist in `Customers`?*

| Field | Value |
|---|---|
| Site Address | pick from the dropdown, not a typed URL |
| List Name | dropdown |
| Filter Query | literal text with a ⚡ token inside — see below |
| Top Count | `1` |

**Build the Filter Query as literal text wrapping a token:**

```
NRIC eq '<⚡ toUpper token>'
```

Type `NRIC eq '`, insert the value with the picker, type the closing `'`. The
quotes are characters you type; only the value is a token.

**`concat()` with escaped quotes validates green and then fails at run time:**

```
concat('NRIC eq ''', toUpper(trim(triggerBody()?['nric'])), '''')
```
```
The expression "concat('NRIC eq ''', …)" is not valid. Creating query failed.
```

**Normalise inside the filter, not after it.** `toUpper(trim(...))` on the key is
what makes a lowercase submission still match. Without it the lookup returns
nothing, the duplicate passes as a new customer, and **no error appears anywhere**
— the wrong answer looks exactly like a right one.

---

## The Outlook connector — `To` is the sharpest edge in the product

**Insert the recipient with the ⚡ picker. Never type an expression.**

Every typed form below failed identically on a live tenant:

```
@{triggerBody()?['email']}
@{toLower(trim(triggerBody()?['email']))}
@{triggerOutputs()?['body/email']}
@triggerOutputs()?['body/email']                       ← bare @, no braces
@{first(split(triggerOutputs()?['body/email'], decodeUriComponent('%0A')))}
```

All produce:

```
OpenApiOperationParameterTypeConversionFailed
Input parameter 'emailMessage/To' is required to be of type 'String/email'.
The runtime value '"someone@example.com\n"' to be converted doesn't have the
expected format 'string/email'.
```

**Read that `\n` correctly.** The obvious conclusion — "the value contains a
newline, strip it" — is wrong, and it drove six failed fixes. The payload was
proven clean by hex dump. `trim()` here strips **spaces, not line feeds**. And
the newline survived every stripping expression because *typing an expression
into this field is what creates it*.

Two things work:

- **A ⚡ picker token** — same value, different code path, no newline.
- **A hardcoded literal address** — useful when every decision should reach the
  trainer rather than the applicant.

A **Compose** node holding `trim(triggerBody()?['email'])` and referenced from
`To` also works, but is unnecessary once you use the picker.

> **Suspect the input method, not the value.** When a field rejects a value that
> is provably correct upstream, stop asking "what is wrong with this data" and
> start asking "what does this control do to whatever I put in it".

---

## Node order: put Response before side effects

```
Trigger → lookup → Agent → Response → Send an email
```

The caller gets its answer as soon as the decision exists, so a later email
failure cannot take down the user-facing response.

The cost: failures after the Response are **invisible from outside** — the
endpoint still returns 200. Right trade for a user-facing flow, but it means
success must be judged from the Activity tab, never from the HTTP status.

Position does **not** affect whether the Outlook `To` field works. Tested in both
orders; picker-vs-typed is the only thing that matters.

---

## Moving a node clears its configuration

Drag a node to a new position and it returns as **"Needs setup"** — every field
blank, connection included. Worse, an unconfigured node is **skipped silently at
run time**: the flow returns 200 and looks healthy.

Three consecutive test runs were read as "the email works now" when the node was
not running at all. After any move, reopen the node and refill every field.

---

## The Excel Online (Business) connector

- **It writes only to a named TABLE, never to a plain range.** A sheet with a
  header row is invisible to the *Table* dropdown. Select the headers and press
  **Ctrl+T** (*My table has headers*), then set the name in **Table Design →
  Table Name**.
- **It cannot reach a personal OneDrive.** The workbook must be in **OneDrive for
  Business** on the account the connector authenticated as. If the File picker
  shows files you recognise but not the one you just made, you are signed into
  two accounts and the workbook is in the other one's drive.
- **Excel Online may reject underscores in table names.** `Handover_Queue` can
  silently become `HandoverQueue`. Harmless — you pick the table from a dropdown
  — but note what Excel actually stored, and keep sheet-tab names separate from
  table names in any instructions.
- The fields cascade: **Connection → Location → Document Library → File →
  Table**. *"Could not load options"* on Location means the Connection above it
  is not set.

---

## The trigger and publishing

- **Relative path must be blank** — a value there breaks Publish.
- **Who can trigger:** *Anyone (no authentication)* for browser calls.
- The endpoint serves the **published** version. Saving is not enough. Check
  **⋯ → Version history**: `LIVE` and `CURRENT DRAFT` should match.
- A published flow runs on demand. Nothing needs to be left "running" — unlike
  n8n's Test URL, which must be armed before each request.
- Typical latency with a retrieval hop: **13–20s**. Set expectations in class.

---

## Diagnosing a flow that returns 200 with an empty body

Order of checks:

1. **Activity → latest run → the node → Run Details → Outputs.** This is the only
   way to tell "the Agent produced nothing" from "the Response read the wrong
   field". Do not theorise before reading it.
2. A **502 NoResponse** in ~1s means a node failed immediately, not a timeout.
   A 502 after ~20s means a node *before* the Response failed, so nothing was
   returned — the run did work, then died.
3. A green run does **not** mean the work happened. Anything after the Response
   node can fail invisibly, and a node left in "Needs setup" is skipped silently.

### Read the UPSTREAM node's Outputs, not the failing node's error

The single biggest time-waster across two builds. When node B fails on bad input,
the useful evidence is node **A's Outputs**, not B's error message — B only tells
you *that* the input was wrong, never *why*.

Concretely: `Parse_Draft` failed eight times with *"the enquiry was blank"*. Each
cycle produced a new theory about the reference path (`?['body']?['x']`, a
missing nesting level, a renamed node). One look at `Normalise_Enquiry`'s
**Outputs** — flat, populated, correct — eliminated every one of those theories
at once and pointed straight at the real cause, which was the Instructions editor
escaping the reference.

**Rule: before the second fix attempt, open the upstream node's Run Details.**
If you have proposed two theories without reading it, stop and read it.

### When several fixes fail the same way, the theory is wrong — not the fix

LU1's email error was met with six fixes in a row: `trim`, `toLower`, `split`,
`replace`, a bare `@`, and a Compose node. All six assumed *the value carries a
newline*. All six failed with byte-identical error text.

**Identical failure across materially different attempts is evidence about the
premise, not the attempt.** The premise here — "something upstream added a
newline" — was disprovable in one command:

```bash
printf '%s' '{"email":"a@b.com"}' | xxd     # no 0x0a anywhere
```

That check was run *after* the fifth failed fix. Run it after the first.

The actual cause was that typing an expression into that particular control
produces the newline. Nothing in the data, nothing in the expression.

**Rule: two identical failures ⇒ stop proposing fixes and go verify an
assumption instead.** Preferably the one so obvious nobody thought to test it.

### Other run-history traps

- **The status pill next to the flow name matters.** A run against a flow showing
  *Draft* executes the previously-published version, so an error can name a node
  you already deleted. Confirm *Published* before believing any run.
- **Works with "Run node", fails from the trigger** = the published version is
  stale, or the connection is valid interactively but not unattended. Check
  **⋯ → Version history** first, then re-create the connection.
- The **health center** ("N new issues detected" → *Open health center*)
  enumerates every unresolved reference at once. Faster than opening nodes one at
  a time.
- Deleting a node leaves **dangling references by internal ID**
  (`This input references action "builtinFunction-a2…"`). If you cannot find
  which field holds it, deleting and rebuilding the node is usually faster than
  hunting.

---

## Pinecone (verified working)

Two integration styles; pick deliberately.

### Integrated embedding — simplest, and what a 60-minute lab should use

Create the index *with* a hosted model:

```
POST https://api.pinecone.io/indexes/create-for-model
{"name":"...","cloud":"aws","region":"us-east-1",
 "embed":{"model":"llama-text-embed-v2","field_map":{"text":"chunk_text"}}}
```

- `field_map` **is** the embedding configuration. Whatever arrives in
  `chunk_text` gets embedded server-side. Rename that field and the record is
  stored with **no vector, and no error** — retrieval silently returns nothing.
- Upsert text: `POST https://{HOST}/records/namespaces/{NS}/upsert`,
  `Content-Type: application/x-ndjson`, one JSON object per line, no wrapping
  array, no commas.
- Search text: `POST https://{HOST}/records/namespaces/{NS}/search` with
  `{"query":{"inputs":{"text":"..."},"top_k":3},"fields":[...]}`.
- **`X-Pinecone-Api-Version: 2025-04` works** (docs showed conflicting values).
- The default namespace is `""` in stats output but **`__default__`** in the
  records API path.
- `llama-text-embed-v2` is 1024-dim, 2048-token max — a ~2.7 KB brochure fits
  whole in one vector.

### Bring-your-own embedding

- Index has no `embed` block; you supply vectors.
- Gemini `gemini-embedding-001` → **3072** dims. `taskType` must be
  `RETRIEVAL_DOCUMENT` on ingest and `RETRIEVAL_QUERY` on query. Both return
  3072, so getting it wrong throws **no error** — retrieval just degrades.
- Endpoints are `/vectors/upsert` and `/query` (note `topK` camelCase here,
  `top_k` on the records endpoints).

### Both

- A **401 on the data plane** may mean the index was deleted, not that the key
  is bad. Check `GET https://api.pinecone.io/indexes` first.
- The official **Pinecone connector in Power Automate is a trap**: independent
  publisher, legacy pod-based API, demands an "Environment" that serverless
  indexes do not have, and its upsert takes only float arrays — it cannot reach
  integrated embedding. Use HTTP actions.

---

## Wiring to a static website

### CORS: the `*.environment.api.powerplatform.com` gateway is WIDE OPEN

**Measured against a live tenant on 2026-08-02 — do not repeat the old advice.**
The long-standing claim "Power Automate's HTTP trigger sends no CORS header, so
serve the page from SharePoint" is **wrong for this gateway**. Verified with curl:

```
OPTIONS <flow url>  -H 'Origin: null' -H 'Access-Control-Request-Method: POST' \
                    -H 'Access-Control-Request-Headers: content-type'
→ HTTP/2 204
  access-control-allow-origin:  *
  access-control-allow-methods: GET,POST,PUT,DELETE,PATCH,HEAD
  access-control-allow-headers: content-type
  access-control-max-age:       7200
```

`Origin: null` **is** `file://`. So a learner can **double-click `index.html`**
and it works — no local web server, no SharePoint hosting, no proxy, no
`--disable-web-security`. Preflight passes and `POST` with
`Content-Type: application/json` is allowed from any origin.

**Verify before prescribing a workaround.** Two curl commands settle it:

```bash
# 1. does the preflight pass from file:// ?
curl -s -D - -o /dev/null -X OPTIONS "$URL" -H 'Origin: null' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type' | grep -i '^access-control\|^HTTP'

# 2. does the real POST carry the header back?
curl -s -D - -o /dev/null -X POST "$URL" -H 'Origin: null' \
  -H 'Content-Type: application/json' -d '{"message":"hi"}' | grep -i '^access-control\|^HTTP'
```

If both show `access-control-allow-origin: *`, CORS is **not** your problem and
`Failed to fetch` means something else — a truncated URL (missing `sig=`), an
unpublished flow, or a network block.

**Classic Power Automate (`*.logic.azure.com`) may still behave the old way.**
Check the host in the URL before assuming either way.

#### The `text/plain` "simple request" trick does NOT work here

A tempting CORS dodge is to send `Content-Type: text/plain` so the browser skips
preflight. **The trigger rejects it with HTTP 400** — it validates the content
type against the Request Body JSON Schema. Irrelevant anyway, since preflight
already passes.

#### Do not reach for `--disable-web-security` in a lab

`open -na "Google Chrome" --args --user-data-dir=/tmp/x --disable-web-security`
works on one machine, but it is the wrong answer for a class: every learner must
run it, on locked-down laptops, with a security banner; it disables protection
globally in that instance; and it teaches a habit they will misapply. Measure
first — on this gateway there is nothing to work around.
- The Response body shape must match what the widget reads:
  `{ "reply": "@{outputs('Agent')?['body/text']}" }`. Wrong shape shows
  `[object Object]`.
- **HTML form controls always yield strings.** The HTTP trigger validates
  strictly and returns `TriggerInputSchemaMismatch` for numbers/booleans. Cast
  in JS before POSTing.
- **Validate the pasted URL on its PATH, not its hostname.** The endpoint may be
  `*.environment.api.powerplatform.com` or `*.logic.azure.com` depending on
  environment. A validator matching the host will reject a perfectly good URL.
  Check instead:

  ```js
  url.startsWith("https://")
    && url.includes("triggers/manual/paths/invoke")
    && url.includes("sig=")
  ```

  The `sig=` check earns its place — a URL truncated on copy is a common and
  otherwise silent failure.
- Keep the URL in `localStorage` behind a *Lab configuration* panel so learners
  never edit a file. Give each lab its own storage key so two labs open in the
  same browser do not overwrite each other.
- **Put the Response node BEFORE any human gate.** The browser gets an instant
  receipt while the approval takes a person hours. A Response after the gate
  hangs the page until someone in another building clicks a button.
- **Decide deliberately what the browser is allowed to see.** An internal
  classification of a *person* — emotional tone, compliance flags, a risk score —
  should not be in the response body just because the agent produced it.

---

## Lab-design guidance

- **No silent fallbacks in a RAG lab.** A page that answers from a local keyword
  list when the webhook fails makes a dead pipeline look alive. Even a labelled
  fallback is a trap — the label is easy to miss when the answer beneath it is
  fluent and correct. Show an error instead. (Both LU3 pages had their fallback
  removed for exactly this reason.)
- **Ingestion is setup, not the lesson.** If a file-listing connector is eating
  the session, load the vector store out-of-band and document the API call.
  Debugging `FSObjType` teaches nothing about RAG.
- Watch for the moment a build turns into connector trivia and say so.
- Keep the API key out of screenshots destined for a Learner Guide, and rotate
  it if it leaks.
- **Never write "paste this" for a block containing `@{...}` tokens.** The
  Instructions editor escapes them (see above). Give prose with blank slots plus
  a table of which field goes in which slot.
- **The pause IS the deliverable in a human-in-the-loop lab.** If approval
  delivery breaks on the tenant, the lesson still lands: submit an enquiry, open
  Activity, and show the run sitting at *Running* — indefinitely, until a person
  acts. Do not let a broken email channel block the teaching point.
- **Structural controls beat procedural ones, and say which is which.** A
  disclaimer written into the Outlook node is safe because the model cannot reach
  it. A rule in the prompt is probabilistic. A self-declared approver name is a
  convention. Rank them explicitly in courseware — learners cannot see the
  difference from a canvas diagram.
- **A default value can quietly undo a control.** `Outcome` defaulting to
  `Approve` turns a gate into a rubber stamp, and the flow diagram looks
  identical either way. Worth showing both settings side by side.
- **Log before the gate, not after.** Writing the draft to the audit table
  *before* the human sees it is what lets someone later ask whether anything
  reached a customer that nobody reviewed.

---

## Working method (from two long debugging sessions)

- **Ask for the upstream node's Outputs before the second fix attempt.** Two
  theories without evidence means stop theorising.
- **Screenshots beat descriptions** for this product. Ask which panel is open;
  the same word (`Configure` vs `Run Details`, node vs Add-panel item) means
  different things in different places.
- **One change per publish-test cycle.** Multiple simultaneous edits make a
  failure uninterpretable, and each cycle costs ~25s plus a publish.
- **Confirm *Published*, not *Draft*, before believing any test result.** More
  than one "the fix didn't work" was actually testing the previous version.
- When something works in isolation but not end to end, suspect **version drift
  or connection context** before suspecting logic.
