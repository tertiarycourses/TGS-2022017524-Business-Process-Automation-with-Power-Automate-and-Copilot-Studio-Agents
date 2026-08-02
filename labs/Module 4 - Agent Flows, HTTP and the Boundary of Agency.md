# Module 4: Agent Flows, HTTP and the Boundary of Agency

> **Read this before Labs 6, 7 and 8.** ~20 minutes. Deck slides 34–40.

By the end of this reading you will be able to:

- Explain what an **agent flow** is and where the Agent node belongs inside it
- Describe an HTTP request and response, and diagnose the two "Failed to fetch" cases
- Use **structured output** so the rest of the flow can branch on the agent's decision
- State the **boundary of agency** — what the model may determine, and what it may not
- Explain what a **Human review** node does, and how to prove it is a real gate

---

## 1. Agent flows — the model inside the workflow

An **agent flow** is a Power Automate flow that may contain an **Agent node** — the model,
running inside the workflow.

```
HTTP trigger ─▶ Compose ─▶ SharePoint ─▶ AGENT ─▶ Condition ─▶ Response
                normalise    lookup      the rules   on the decision
```

**What the Agent node is for:** judgement over language — reading a free-text reason, applying
ordered rules, classifying a tone, drafting a reply. Anything where the input varies more than a
form allows.

> ### The Copilot Credits trap
>
> Agent flows consume **Copilot Credits** on every run. Many Default environments have none and
> fail with:
>
> ```
> {"error":{"code":"InsufficientMcsCredits","message":"The environment '...' does not have
> sufficient Copilot Credits to run workflows."}}
> ```
>
> This is an environment capacity issue, not a flow problem — which is exactly why Lab 0 builds a
> **Copilot Studio Training (Developer)** environment rather than a Sandbox. Check before class:
> build a two-node flow (trigger → Response) and call it.

---

## 2. HTTP — a website calls your flow and waits

```
Website form ─▶ POST JSON ─▶ HTTP trigger ─▶ flow runs ─▶ Response returns JSON ─▶ page updates
```

| Part | Meaning | In these labs |
|---|---|---|
| **Request** | What the caller sends | A JSON body matching the schema you declared |
| **Schema** | The shape you promise to accept | Generated from a sample payload — then frozen |
| **Response** | What the caller gets back | A JSON body the page can read, plus a status code |
| **Synchronous** | The page waits | If nothing responds, the browser sees a timeout, not a result |

> ### Two failures that look identical from the browser
>
> - **"Failed to fetch" *with* a successful run** = **CORS**. Serve the page from SharePoint,
>   not from `localhost`.
> - **"Failed to fetch" with *no* run at all** = the flow is saved but **not Published**, or the
>   URL is wrong.
> - **`502 NoResponse`** = a node *before* the Response failed, so nothing was returned. Open
>   **Activity** and find the red node.

---

## 3. Structured output — fields, not prose

Structured output turns the model's answer from prose into named fields the rest of the flow can
branch on.

| Prose — unusable downstream | Structured — branchable |
|---|---|
| *"I think this application should probably be approved, although the address looks a little unusual and you may wish to check it."* | `applicationId: APP-10432`<br>`decision: REVIEW`<br>`reason: address unverified`<br>`riskFlags: [ADDRESS_MISMATCH]` |
| What does a Condition test against that? | A Condition can read `decision`. A person can audit `reason`. |

### Four decisions, not two

`APPROVED` · `REJECTED` · `DUPLICATE` · `REVIEW`

A politically exposed person is not a rejection — it is a case for a human. An agent given only
two outcomes will force every ambiguous case into one of them, and you will never see the ones
it got wrong.

---

## 4. The boundary of agency

The most important design decision in the course.

| The AI decides — *what to do* | The flow does — *what must always happen* |
|---|---|
| Which of six ordered rules applies | Normalise the identifier (Compose) |
| Whether the case needs a human | Check the register for a duplicate |
| How to phrase the reason | Write the customer record |
| What risk flags to raise | Write the audit row, **before** the gate |

> **The record is written from the Compose action, never from the model's answer.**

So an invented identifier has no route into the customer master. The agent's opinion reaches the
*decision* field; it never reaches the *data*. If you remember one sentence from Day 2, make it
this one.

The audit row is written **before** the human gate, so a rejected requisition still leaves a
trace. A year from now you can answer "what did we decide, and why" — which you could not if the
row were written after.

---

## 5. The agent alone, in public

Lab 7 is the agent working with nobody reviewing it. Four nodes, two non-negotiable rules.

```
chat widget ─▶ HTTP trigger ─▶ Compose_session ─▶ AGENT ─▶ Response
                                          instruction (the RULES)
                                          knowledge (the FACTS)
                                          the conversation so far
```

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
                                                          who must phone the client
```

The node between them does nothing at all except wait.

> ### The test of a real gate
>
> Submit an enquiry, then open **Activity**. The run says *Running* — and it will still say
> *Running* tomorrow. Nothing times out, nothing defaults, nothing proceeds. A workflow that has
> done all of its work and will not take the last step.
>
> **That pause is the deliverable.**

---

**Next:** [Lab 6 — HTTP and Application Approval Agent](Lab%206%20-%20HTTP%20and%20Application%20Approval%20Agent/README.md)
