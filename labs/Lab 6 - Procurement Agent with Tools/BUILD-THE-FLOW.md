# Building the Procurement Requisition Approval flow

**Platform:** Copilot Studio agent flow (agent-invoked) + SharePoint + Human review + Outlook
**Time:** 60–75 minutes
**The idea it teaches:** **the agent as a tool, and the threshold that stops it** — the flow is
published as a tool an agent calls in conversation, and a policy threshold decides whether the
answer is released or held for a human.

---

## Why this lab exists

Every earlier lab was triggered by something that is not a person talking: a website POST, a form
submission. Lab 6 is the first one where **a Copilot Studio agent decides to call the flow**,
mid-conversation, because a colleague asked it to.

That changes what you are building. The flow is no longer a workflow with a URL — it is a **tool**,
and its trigger is a **contract**: the typed inputs the calling agent must supply. Nothing in the
trigger points at a particular agent, and no agent is bound to it until you attach it from the
agent's side.

It also teaches the thing procurement is actually about: **an amount is not the only reason to
stop.** A SGD 900 requisition against a vendor under review must reach a human. A SGD 9,999
requisition against a clean vendor need not. Learners routinely build the amount check and miss
the status check, then discover TC7 fails.

| | Earlier labs | Lab 6 |
|---|---|---|
| What starts the flow | A website POST | **An agent, mid-conversation** |
| Who supplies the inputs | A form | The agent, from what the user said |
| What the trigger defines | A JSON schema | **A typed tool contract** |
| Where the gate sits | After the agent | After the agent, **conditionally** |

---

## What you are building

```
When an agent calls the workflow      ← the tool contract
  → Get items (SharePoint)            ← vendor register lookup
  → Agent                             ← applies the procurement policy
  → Create item (SharePoint)          ← audit row, written BEFORE the gate
  → If/Else  routing == "APPROVAL"
       ├─ true  → Human review  → If/Else Outcome == Approve
       │                            ├─ true  → Update item  → Send an email (released)
       │                            └─ false → Update item  → Send an email (rejected)
       └─ false → (nothing)
  → Respond to the agent              ← what the calling agent says back
```

Two things about that shape are deliberate and worth saying out loud in class:

**The audit row is written before the gate.** That is what lets someone ask, a year later, whether
anything was released that nobody reviewed. Log after the gate and rejected requisitions leave no
trace at all.

**The Response is the last node, not an early one.** This is the opposite of the website labs, and
the reason is that here the *caller is an agent*, not a browser waiting on a spinner. The agent
needs the routing decision in order to say something useful. But note the cost: a requisition
routed to APPROVAL will sit at the Human review node, so the calling agent waits too. Step 9
covers what to do about that.

---

## Before you start

- Copilot Studio (copilotstudio.microsoft.com) in an environment where you can publish.
- SharePoint, Outlook and **Microsoft Teams** (approvals must go to Teams — see Step 7).
- An existing Copilot Studio **agent** to attach the tool to, or create a blank one in Step 10.

---

## Part 1 — SharePoint setup

### Step 1 — The vendor register

Create a SharePoint list named **`ApprovedVendors`** with these columns:

| Column | Type | Notes |
|---|---|---|
| `Title` | Single line of text | Rename it **VendorName** in the column settings |
| `Status` | Choice | `Approved`, `Suspended`, `Under Review` |
| `Category` | Choice | `IT Hardware`, `Machinery`, `Vehicles`, `Facilities`, `Stationery`, `PPE`, `Consumables`, `Software Subscription` |
| `ContractExpiry` | Date | |
| `Notes` | Single line of text | |

Import the twelve rows from [`knowledge/vendors.csv`](knowledge/vendors.csv). Four of them are not `Approved`, and one
vendor used in the tests is missing from the register entirely — between them, that is what makes
TC5, TC6 and TC7 interesting.

> **Why a register with three statuses, not a yes/no flag.** A boolean would make the lab easier
> and the lesson smaller. "Suspended" and "Under Review" route differently from each other and from
> absent, and that is the realistic case: a vendor you have a contract with, whom you may not buy
> from this week.

### Step 2 — The audit list

Create a second list named **`RequisitionLog`**:

| Column | Type |
|---|---|
| `Title` | Single line of text (holds the requisition ID) |
| `Requester` | Single line of text |
| `Vendor` | Single line of text |
| `RequisitionTotal` | Number |
| `Routing` | Single line of text |
| `PolicyFlags` | Single line of text |
| `Reason` | Multiple lines of text |
| `ApprovedBy` | Single line of text |

---

## Part 2 — Build the flow

Copilot Studio → **Flows** → **+ New agent flow** → name it
`Lab 6 - Procurement Requisition Approval`.

### Step 3 — The trigger (the tool contract)

The trigger is **When an agent calls the workflow**. This is the node in the screenshot at the top
of this lab — its whole job is to declare what the calling agent must pass.

Click **+ Add an input** once per row:

| Input name | Type | What the agent will put here |
|---|---|---|
| `requester` | Text | Who is raising it |
| `department` | Text | Their department |
| `vendor` | Text | Vendor name as the user said it |
| `itemDescription` | Text | What is being bought |
| `unitPrice` | Number | Price per unit in SGD |
| `quantity` | Number | How many |
| `competingQuotes` | Number | How many quotes were obtained |
| `budgetCode` | Text | e.g. `EN-2041` |
| `neededBy` | Text | Date as text — keep it Text, not Date |

> **Keep `neededBy` as Text.** A Date input makes the calling agent responsible for producing a
> valid ISO date from whatever the user typed ("end of the month"), and it will sometimes fail the
> type check rather than ask. Text accepts it, and nothing downstream does date arithmetic.

> **Name the inputs exactly as above.** These names are what the calling agent sees, and they are
> what your Instructions block references in Step 5. A rename here means a re-point there.

### Step 4 — SharePoint vendor lookup

Add **SharePoint → Get items**:

| Field | Value |
|---|---|
| Site Address | pick from the dropdown, **not** a typed URL |
| List Name | `ApprovedVendors` |
| Filter Query | see below |
| Top Count | `1` |

**Build the Filter Query as literal text wrapping a token.** Type `VendorName eq '`, insert the
`vendor` input with the **⚡ picker**, then type the closing `'`:

```
VendorName eq '<⚡ vendor token>'
```

The quotes are characters you type. Only the value is a token.

> ⚠️ **Do not use `concat()` here.** `concat('VendorName eq ''', ..., '''')` validates green in the
> editor and then fails at run time with *"Creating query failed"*. This is documented behaviour on
> a live tenant.

> **Note what is deliberately missing: there is no `toUpper()` or `trim()` wrapper.** In the Module 4
> onboarding lab the normalisation sat inside the filter, which guaranteed the match. Here it does
> not — and TC12 (lowercase vendor name) exists to show you what that costs. Leave it out for now;
> Step 11 asks you to fix it.

### Step 5 — The Agent node

Add an **Agent** node and create its connection.

**Instructions:** open [`agent/instructions.md`](agent/instructions.md) and follow the note at the
top. Paste the prose down to `## Requisition to assess`, then build that block by typing each label
and inserting the value with the **⚡ picker**:

| Line | Insert with ⚡ |
|---|---|
| Requester | trigger → `requester` |
| Department | trigger → `department` |
| Vendor | trigger → `vendor` |
| Item Description | trigger → `itemDescription` |
| Unit Price (SGD) | trigger → `unitPrice` |
| Quantity | trigger → `quantity` |
| Competing Quotes | trigger → `competingQuotes` |
| Budget Code | trigger → `budgetCode` |
| Needed By | trigger → `neededBy` |
| Vendor register result | `Get items` → `value` |

> ⚠️ **Never paste a block containing `@{...}` into the Instructions box.** It is a rich-text
> editor: it escapes underscores in node names (`Get_items` becomes `Get\_items`), and a reference
> to a node that does not exist **resolves to empty rather than erroring**. The node stays green,
> the run succeeds, and the agent silently assesses a blank requisition. The tell is a reply that
> says something like *"no requisition was included in this submission"*.

**Output:** set the dropdown to **Custom structured output** and paste this schema:

```json
{
  "type": "object",
  "properties": {
    "requisitionId":    { "type": "string" },
    "routing":          { "type": "string" },
    "reason":           { "type": "string" },
    "policyFlags":      { "type": "array", "items": { "type": "string" } },
    "requisitionTotal": { "type": "number" }
  },
  "required": ["requisitionId", "routing", "reason", "policyFlags", "requisitionTotal"]
}
```

With structured output set, **do not add a Parse JSON node.** Reference the fields directly, and
note the syntax is slash-separated:

```
body('Agent')?['structuredOutput/routing']
```

### Step 6 — The audit row (before the gate)

Add **SharePoint → Create item** against `RequisitionLog`:

| Column | Value |
|---|---|
| Title | `body('Agent')?['structuredOutput/requisitionId']` |
| Requester | ⚡ trigger → `requester` |
| Vendor | ⚡ trigger → `vendor` |
| RequisitionTotal | `body('Agent')?['structuredOutput/requisitionTotal']` |
| Routing | `body('Agent')?['structuredOutput/routing']` |
| PolicyFlags | `join(body('Agent')?['structuredOutput/policyFlags'], ', ')` |
| Reason | `body('Agent')?['structuredOutput/reason']` |
| ApprovedBy | leave empty — filled in Step 7 |

> ⚠️ **`policyFlags` needs `join()`.** Without it the column reads `System.Object[]`.

### Step 7 — The conditional gate

Add an **If/Else** node with the condition:

```
body('Agent')?['structuredOutput/routing']   Equals   APPROVAL
```

On the **true** branch, add a **Human review** node.

**Inputs** (the node will not save with zero, and there is **no built-in `outcome` property** —
searching the ⚡ picker for "outcome" returns nothing until you create it):

| Name | Type | Default |
|---|---|---|
| `Outcome` | Choice: `Approve` / `Reject` | **leave blank** |
| `ApproverName` | Text | — |

> **Leave the default blank.** Pre-filling `Outcome` with `Approve` means the request arrives at the
> approver already answered — confirming takes no thought, rejecting takes noticing. That converts a
> gate into a rubber stamp through a one-word setting invisible on the canvas. If a default is
> forced on you, use `Reject` so inattention fails safe.

| Field | Value |
|---|---|
| **Channel** | **Teams** — see below |
| Assigned to | type your full address, **wait for the directory lookup, and click the suggestion** |
| Title | `Requisition approval: ` + ⚡ requisitionId |
| Details | vendor, total, flags and reason |

> ⚠️ **Channel must be Teams, not Outlook.** On a live tenant Outlook created the approval request
> and **never delivered the email** — to any address tried, including tenant users. The run reaches
> *Running* correctly; the mail simply never arrives. Teams works: the request appears in the Teams
> **Approvals** app (teams.microsoft.com → ••• → Approvals). If someone reports "the approval never
> arrives", this is the first thing to change.

> ⚠️ **`assignedTo` fails at run time while looking fine on the canvas** — `BadRequest — Required
> field 'assignedTo' is missing or empty` — if you typed an address and tabbed away without clicking
> the resolved suggestion, or used an address outside the tenant. Safest choice is the account the
> connection authenticated as.

Then add a nested **If/Else** on `Outcome` `Equals` `Approve`, with an **Outlook → Send an email**
on each branch: released on true, returned-to-requester on false.

> ⚠️ **Insert the recipient with the ⚡ picker. Never type an expression into the `To` field.**
> Every typed form fails with `OpenApiOperationParameterTypeConversionFailed ... the runtime value
> '"someone@example.com\n"'`. The newline is not in your data — *typing an expression into that
> control is what creates it*. Six fixes were burned on this in an earlier lab before someone
> switched to the picker.

Then, on **both** branches, stamp the approver onto the audit row with **SharePoint → Update item**:

| Field | Value |
|---|---|
| Site Address / List Name | same as Step 6 — `RequisitionLog` |
| **Id** | `body('Create_item')?['ID']` |
| ApprovedBy | ⚡ Human review → `ApproverName` |

> **The `Id` is the part learners get stuck on.** *Update item* needs the SharePoint list item ID,
> and the only place it exists is in the output of the `Create item` node from Step 6. If the field
> shows red, check that the node is genuinely named `Create_item` — underscores replace spaces in
> action references, and a renamed node breaks this silently.

> **Say plainly what this is.** The Human review node does **not** record who responded — no
> responder, no email, no timestamp, just the inputs you defined. So `ApprovedBy` is a
> **self-declared text field**: a convention, not evidence. Do not let courseware imply the platform
> captured an identity.

### Step 8 — Respond to the agent

The **Respond to the agent** node defines what the calling agent receives. Add outputs:

| Output | Value |
|---|---|
| `routing` | `body('Agent')?['structuredOutput/routing']` |
| `reason` | `body('Agent')?['structuredOutput/reason']` |
| `requisitionTotal` | `body('Agent')?['structuredOutput/requisitionTotal']` |
| `requisitionId` | `body('Agent')?['structuredOutput/requisitionId']` |

> **Decide deliberately what the calling agent is allowed to see.** `policyFlags` is deliberately
> *not* returned. `VENDOR_SUSPENDED` is an internal procurement judgement about a business
> relationship, and the requester does not need it to act — "this vendor cannot be used, please
> contact Procurement" is enough. The flag is in the audit row, where it belongs.

Then **Publish**. An unpublished flow does not appear in any agent's tool list.

---

## Part 3 — Attach it to an agent

### Step 9 — A note on the wait

A requisition that routes to `APPROVAL` stops at the Human review node, and the **Respond to the
agent** node is after it. The calling agent therefore waits — potentially for hours.

For this lab, accept it and watch it happen: it is the most honest demonstration in the whole
course that a human gate is a *real* pause, not a UI flourish. In production you would split this
into two flows — one that returns "submitted for approval" immediately, and a second triggered on
the approval outcome. Say which one you are building and why.

### Step 10 — Wire the flow to an agent

Copilot Studio → **Agents** → pick or create an agent → **Tools** → **+ Add a tool** → **Flow**.
Your published flow appears by name.

> The exact label shifts between tenant versions — it may read *Add a tool* or *Add an action*.
> Screenshot what you actually see before writing it into a build sheet.

Give the tool a **description**. This is not documentation — it is a prompt, and it is the single
most common reason a tool-based agent misbehaves:

```
Assess a purchase requisition against Keppel Ridge procurement policy. Call this
whenever a colleague wants to raise, submit or check a purchase request, or asks
whether a purchase needs approval. Returns the routing decision (AUTO, APPROVAL,
RETURNED or BLOCKED) and the reason. Collect every input before calling: requester,
department, vendor, item description, unit price, quantity, number of competing
quotes, budget code and needed-by date.
```

Test from the **agent's Test pane**, not the flow canvas:

> "I need to order 15 boxes of warehouse cleaning consumables from Bukit Timah Consumables at $890
> each, budget code OP-1120, we have three quotes, needed by end September. I'm Daniel Lim in
> Operations."

That is TC2 — 13,350 against a non-capex vendor, so the agent should come back with `APPROVAL` and
`ABOVE_THRESHOLD`.

The agent should collect anything missing, call the flow, and report the routing.

> **Testing the flow standalone with ▶ Run verifies the flow logic only — it does not test the
> agent binding.** Those are two separate checks, and passing the first tells you nothing about
> the second.

> **If the flow does not appear in the agent's tool list:** it is almost always because it was
> created in a different environment than the agent, or it is still **Draft** rather than
> Published. Check **⋯ → Version history** — `LIVE` and `CURRENT DRAFT` should match.

---

## Part 4 — Test and break it

### Step 11 — Run the test cases

Run all thirteen from [`knowledge/test-requisitions.csv`](knowledge/test-requisitions.csv). Each isolates one rule, so a
wrong routing points at exactly one step.

| TC | Total | Expected | What it proves |
|---|---|---|---|
| TC1 | 420 | `AUTO` | Clean run |
| TC2 | 13,350 | `APPROVAL` / `ABOVE_THRESHOLD` | Crosses 10,000 on a **non-capex** vendor |
| TC3 | 2,450 | `APPROVAL` / `CAPEX` | Far under threshold, but capital expenditure |
| TC4 | 7,800 | `APPROVAL` / `SINGLE_SOURCE` | One quote — fires before CAPEX, though Facilities *is* capex |
| TC5 | 2,400 | `BLOCKED` / `VENDOR_SUSPENDED` | **On the register ≠ approved** |
| TC6 | 1,200 | `BLOCKED` / `UNAPPROVED_VENDOR` | Absent entirely |
| TC7 | 900 | `APPROVAL` / `VENDOR_UNDER_REVIEW` | **Status beats amount** |
| TC8 | 560 | `RETURNED` / `INVALID_BUDGET_CODE` | Missing code — returned, not escalated |
| TC9 | 1,080 | `RETURNED` / `INVALID_BUDGET_CODE` | Malformed code |
| TC10 | 10,000 | `APPROVAL` / `ABOVE_THRESHOLD` | Exactly 10,000 is *at* the threshold |
| TC11 | 1,900 | `AUTO` | One quote, but single-source needs 5,000+ |
| TC12 | 1,200 | `AUTO` | **See below** |
| TC13 | 12,600 | `APPROVAL` / `SINGLE_SOURCE` | Two rules both apply — **proves the order** |

**TC5 and TC7 are the two that matter.** Both are cheap. Both must stop. Anyone who built only an
amount check passes ten cases and fails these two — and in a real firm those are precisely the ones
that cost you.

### The rule order is doing more work than it looks

Trace TC2, TC3 and TC13 side by side and a design consequence falls out that catches most people:

**`ABOVE_THRESHOLD` can never fire for a capital-expenditure vendor.** STEP 3 catches capex at
SGD 2,000, so by the time a Machinery or IT Hardware requisition reaches 10,000 it has already
stopped at `CAPEX`. That is why TC2 and TC10 are deliberately raised against **Consumables** and
**Software Subscription** vendors — on any capex vendor they would return `CAPEX` and the threshold
rule would look broken when it is merely unreachable.

Is that a bug? No — the requisition still routes to a human either way, which is what matters. But
the *flag* is what an auditor reads six months later, and "this was held because it was capital
expenditure" is a different claim from "this was held because it was large". Worth asking the class
whether the two rules should be ordered the other way round, and who is harmed if they are not.

TC13 is the honest ordering test: at 12,600 with one quote, **both** STEP 2 and STEP 4 apply. It
reports `SINGLE_SOURCE` only because STEP 2 is evaluated first.

### The interesting failure — TC12

TC12 sends `sembawang industrial supplies` in lowercase. Run it several times.

Its total is deliberately **1,200** — under the capex floor, under the single-source floor, under the
threshold, with a valid budget code. Every rule after STEP 1 is inert, so the *only* thing this case
can be testing is whether the lookup matched.

The Filter Query in Step 4 has **no `toUpper()` or `trim()`** — the agent is merely *instructed* to
pass the vendor name as written. Usually the lookup matches, because SharePoint's OData `eq` is
often case-insensitive. Sometimes the agent helpfully "corrects" the name first, and sometimes it
does not.

Now notice the failure mode. If the lookup returns nothing, the agent concludes `UNAPPROVED_VENDOR`
and blocks a perfectly good vendor — **and no error appears anywhere.** A green run, a plausible
reason, a wrong answer. The wrong answer looks exactly like a right one.

**Then fix it:** wrap the token in `trim()` inside the Filter Query and re-run. Ask the class where
that normalisation belongs — in the filter, where it is structural, or in the instruction, where it
is probabilistic.

### Step 12 — Watch the gate hold

Submit TC2. Open **Activity** → the latest run. It sits at *Running*, and it will still say
*Running* tomorrow unless someone opens Teams → Approvals and acts.

Then check `RequisitionLog`. **The audit row is already there**, before anyone approved anything.
That is Step 6 earning its position.

---

## Debugging

| Symptom | Cause |
|---|---|
| Agent replies about a blank requisition | Instructions box escaped a pasted reference — rebuild that line with ⚡ |
| Everything routes `BLOCKED` / `UNAPPROVED_VENDOR` | Filter Query wrong, or the vendor list did not import |
| `Creating query failed` | You used `concat()` in the Filter Query — use literal text + ⚡ token |
| Every run falls to the Else branch | Hand-typed `body('Human_review')?['result']` — there is no such property; use the `Outcome` token |
| Approval never arrives | Channel is Outlook — switch to Teams |
| `assignedTo is missing or empty` | Address typed without clicking the directory suggestion |
| Email fails with `...\n` | Typed expression in `To` — use the ⚡ picker |
| `PolicyFlags` reads `System.Object[]` | Missing `join()` |
| Node does nothing, run still green | Node is in **"Needs setup"** — moving a node clears every field, including the connection, and an unconfigured node is **skipped silently** |
| Flow missing from the agent's tool list | Wrong environment, or still Draft |

**Before your second fix attempt, open the *upstream* node's Run Details → Outputs.** When a node
fails on bad input, the useful evidence is the previous node's output, not this node's error — the
error only tells you *that* the input was wrong, never *why*. Two theories without reading it means
stop theorising.

**And if several materially different fixes fail identically, the premise is wrong, not the fix.**
Identical failure across different attempts is evidence about your assumption. Go verify the one so
obvious nobody thought to test it.

---

## Discussion questions

1. TC7 is a SGD 900 requisition that must reach a human, and TC11 is a SGD 1,900 one that need not.
   What does that tell you about designing approval rules around amount alone?

2. The audit row is written before the gate. What question can you answer a year from now that you
   could not if it were written after?

3. `ApprovedBy` is typed in by the approver. What would it take to make that evidence rather than a
   convention — and is the platform able to give you that?

4. `policyFlags` is deliberately withheld from the calling agent. Who else in the firm might have a
   legitimate claim to see `VENDOR_SUSPENDED`, and how would you serve them without putting it in
   the requester's chat window?

5. In Lab 12 the duplicate check was a step in the flow and you could see it on the canvas. Here
   the vendor check is a step too — but the *decision to call this whole flow* belongs to an agent
   whose reasoning is not on any canvas. What does that mean for auditing the process?

6. The gate makes the calling agent wait. Step 9 suggests splitting into two flows. What do you lose
   when you do that, and who now has to track that the second half ever ran?

---

## What this lab is not

The routing decision is made by a language model reading a policy written in prose. That is
appropriate here because a requisition is low-stakes and reversible, and because every consequential
path ends at a human.

It would **not** be appropriate for releasing payment. The structural controls in this flow — the
audit row that is always written, the gate that always fires on `APPROVAL` — are real, and the model
cannot reach them. The rules in the instruction are probabilistic, and TC12 shows exactly how they
fray. Rank them explicitly for learners: **a control the model cannot reach beats a rule you asked
it to follow**, and neither of those is the same as a name someone typed into a text box.
