# Module 4: Agent Flows, HTTP and the Boundary of Agency

> **Read this before Labs 12, 13 and 14.** ~20 minutes.

By the end of this reading you will be able to:

- Explain what the **Agent node** inside a workflow is for, and how it differs from an agent
- Describe an HTTP request and response, GET versus POST, and where the trigger URL comes from
- Use **structured output** so the rest of the workflow can branch on the agent's decision
- State the **boundary of agency** — what the model may determine, and what it may not
- Explain what a **Human review** node does, and how to prove it is a real gate

---

## 1. The model inside the workflow

An **Agent node** is the model, running as one step of a workflow. The workflow decides *when*
it runs and *what happens to its output*; the model decides only what it is asked to decide.

```
HTTP trigger ─▶ SharePoint ─▶ Compose ─▶ AGENT ─▶ Response ─▶ Send an email
                lookup       assemble    the rules   answer      side effect
```

**What the Agent node is for:** judgement over language — reading a free-text reason, applying
ordered rules, classifying a tone, drafting a reply. Anything where the input varies more than a
form allows.

**What it is not:** a Copilot Studio agent. Its Configure panel runs *Connection · Model ·
Instructions · Tools · Knowledge · Request human assistance · Web search · Output* and stops.
There is **no user-message field** — the only place per-call data can go is Instructions — and
there is **no *Use general knowledge* toggle and no temperature**. Grounding inside a workflow
rests on instruction wording alone.

> ### The Instructions box is a rich-text editor
>
> It escapes underscores in node names (`Get_customer_by_NRIC` → `Get\_customer\_by\_NRIC`) and
> swallows braces, and a reference to a node that does not exist **resolves to empty rather than
> erroring**. The run goes green and the agent assesses a blank input — its reply says so, in the
> one place nobody looks (its Run details → Outputs). **Build the per-call block in a Compose
> node and insert one ⚡ chip.** Never write "paste this" for text containing `@{…}`.

> ### The Copilot Credits trap
>
> Every run of a workflow with an Agent or Classify node consumes **Copilot Credits**. Many
> Default environments have none and fail with `{"error":{"code":"InsufficientMcsCredits", …}}`.
> An environment capacity issue, not a workflow problem — which is why Lab 0 builds a Developer
> environment.

---

## 2. HTTP — a website calls your workflow and waits

```
Website form ─▶ POST JSON ─▶ HTTP trigger ─▶ workflow runs ─▶ Response returns JSON ─▶ page updates
```

| Part | Meaning | In these labs |
|---|---|---|
| **Trigger** | *When a HTTP request is received* — gives the workflow a public URL | Labs 12–16 |
| **GET vs POST** | GET asks for something and carries no body; **POST** sends a body. Forms and chat widgets POST | Allowed method = POST |
| **The URL** | Generated **only after you Save** — it carries a `sig=` signature that is the only credential | Copy it from the trigger; a truncated URL fails silently |
| **Request body schema** | The JSON shape you promise to accept; validated strictly (a string where a number is declared → `TriggerInputSchemaMismatch`) | Pasted once, then frozen |
| **Response node** | Status code + headers + a JSON body the page can read | `{ "reply": … }`, `200` |
| **Who can trigger** | *Anyone (no authentication)* for a browser | The tenant option returns 401 to a plain POST |
| **Relative path** | Must be **blank** — a value breaks Publish | |

| Status | Meaning |
|---|---|
| `200` | The Response node ran. **Nothing more** — a node after it can still fail invisibly |
| `202` | No Response node; the trigger accepted the request and returned nothing |
| `400` | The body failed the schema, or a header is malformed |
| `502 NoResponse` | A node *before* the Response failed, so nothing was returned. Open Activity, find the red node |

**The endpoint serves the published version.** Check **⋯ → Version history**: `LIVE` and
`CURRENT DRAFT` must match. And this gateway sends `access-control-allow-origin: *`, so a page
opened from `file://` can call it — *Failed to fetch* is a truncated URL or an unpublished
workflow, not CORS.

---

## 3. Structured output — fields, not prose

Structured output turns the model's answer from prose into named fields the rest of the workflow
can branch on. Set the Agent node's **Output** to **Custom structured output**, paste a JSON
schema, and reference fields with the slash form `body('Agent')?['structuredOutput/decision']`.
No Parse JSON node.

| Prose — unusable downstream | Structured — branchable |
|---|---|
| *"I think this application should probably be approved, although the address looks a little unusual…"* | `decision: REVIEW` · `reason: address unverified` · `riskFlags: [ADDRESS_MISMATCH]` |
| What does an If/Else test against that? | An If/Else can read `decision`. A person can audit `reason`. |

An `enum` on the decision field is what stops the model inventing `PENDING`. Arrays need
`join()` before they reach Excel. Booleans in a Response body must be unquoted **and** wrapped in
`toLower(string(…))`.

### Four decisions, not two

`APPROVED` · `REJECTED` · `DUPLICATE` · `REVIEW`

A politically exposed person is not a rejection — it is a case for a human. An agent given only
two outcomes will force every ambiguous case into one of them, and you will never see the ones it
got wrong.

---

## 4. The boundary of agency

The most important design decision in the course.

| The AI decides — *what to do* | The workflow does — *what must always happen* |
|---|---|
| Which of six ordered rules applies | Normalise the identifier (`toUpper(trim(…))`) in a Compose node |
| Whether the case needs a human | Check the register for a duplicate |
| How to phrase the reason | Compute the age — never ask the model to do date arithmetic |
| What risk flags to raise | Write the audit row, **before** the gate |

> **The record is written from the Compose node, never from the model's answer.**

So an invented identifier has no route into the customer master. The agent's opinion reaches the
*decision* field; it never reaches the *data*. If you remember one sentence from Day 2, make it
this one.

---

## 5. The agent alone, in public

Lab 13 is the agent working with nobody reviewing it. Four nodes, two non-negotiable rules.

| Rules live in the instruction | Facts live in the knowledge source |
|---|---|
| Collect name, phone and email before answering | Fees, timelines and services come from the FAQ |
| Never recommend a product, predict a return, or allocate savings | Change the PDF and the answers change |
| A refusal that has to be *retrieved* is a refusal that can **miss** | …without touching the instruction |

The test cases are written to make it fail. Read the failures aloud — that is the debrief.

---

## 6. The Human review node — a gate that blocks

```
┌──── the agent's territory ────┐  ┌── the human's ──┐
classify · read tone · flag ·    ▶  approve or reject  ▶  reply sent + logged
DRAFT (never sends)                                    └▶ assigned to a NAMED person
```

The node between them does nothing at all except wait. Verified on a live tenant: **Channel must
be Teams** (Outlook never delivered); the card lands in the Teams **Workflows** bot chat; the node
publishes **only the inputs you define** (`Outcome` Yes/No + `Name` Text, defaults blank), and the
Yes/No input publishes the string `Yes` — compare against that, not `true`.

> ### The test of a real gate
>
> Submit an enquiry, then open **Activity**. The run says *Running* — and it will still say
> *Running* tomorrow. Nothing times out, nothing defaults, nothing proceeds. **That pause is the
> deliverable.**

Three controls, ranked: the disclaimer in the Outlook node is **structural** (the model cannot
reach it); the gate is **structural** (it always fires); the non-advisory rule in the prompt is
**probabilistic**; the approver's typed name is a **convention**. Say which is which.

---

**Next:** [Lab 12 — HTTP and Application Approval Agent](Lab%2012%20-%20HTTP%20and%20Application%20Approval%20Agent/index.md)
