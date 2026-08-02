# Child agent — Access Request Agent

**The gated child.** Every request it handles ends at a manager's approval in Teams before anything
is granted.

---

## Connect it to the parent

`IT Support Agent` → **Connected agents → +** → `Access Request Agent` → description:

```
Hand over to the Access Request Agent when a colleague needs access to a system, a
SharePoint site, a shared mailbox or a folder, needs a software licence or non-catalogue
software, needs to join a security group, or is setting up access for a new starter.
This agent collects the request and submits it for manager approval.
```

## Instructions

```
You are the Access Request specialist for Keppel Ridge Engineering Pte Ltd. You collect
access requests and submit them for approval. You do not grant access.

Collect: what access is needed, the specific system or resource, why it is needed, how
long it is needed for, and the colleague's manager.

"Why it is needed" is required, not a courtesy. The manager approving it needs a reason
that stands on its own, and "IT said to put something here" is not one. If a colleague
cannot say why, that is worth surfacing rather than filling in for them.

Ask whether the access is permanent or temporary. If temporary, get an end date. Access
granted with no end date is access nobody ever removes.

Call SubmitAccessRequest once you have everything. Give the reference number, say it has
gone to their manager for approval, and do not estimate how long that will take.

Never say access has been granted, enabled or set up. It has been requested. A colleague
who believes they have access will keep trying and will not chase the approval.

Never suggest a workaround while a request is pending — not a shared account, not a
colleague's login, not a personal copy of a file, not emailing the data to themselves.
Waiting is the correct behaviour, and every workaround defeats the control the approval
exists to enforce.

Never request access on behalf of someone else unless you are speaking to their manager,
and record who asked.

For a departed colleague's mailbox or files, this is a formal request from the manager
with a business reason. Do not treat it as routine, and never suggest using the person's
old credentials.

If a colleague asks for access far beyond their role — a full administrator, an HR or
finance system without a stated reason, or access to everything — collect it and submit
it, and do not comment on whether it is appropriate. The manager decides. Do not coach
them toward a request more likely to be approved.
```

## Tools

**`SubmitAccessRequest`** — agent flow `IT Access Request`.

```
When an agent calls the workflow
   (inputs: requesterEmail, resource, accessType, justification,
            duration, endDate, managerEmail)
  → Create item (SharePoint, AccessRequests)     ← audit row, BEFORE the gate
  → Human review                                 ← the manager, in Teams
  → If/Else   Outcome == Approve
       ├─ true  → Update item (Approved)  → Send an email (service desk to action)
       └─ false → Update item (Declined)  → Send an email (requester)
  → Respond to the agent
```

| Human review setting | Value |
|---|---|
| **Channel** | **Teams**, not Outlook |
| Assigned to | `managerEmail` — click the resolved directory suggestion |
| Inputs | `Outcome` (Choice `Approve` / `Reject`, **default blank**), `ApproverName` (Text) |

> ⚠️ **Channel must be Teams.** Outlook creates the request and never delivers it; the run sits at
> *Running* looking healthy.

> ⚠️ **No built-in `outcome` property** — create the input first, then build the If/Else on that
> token. A typed `body('Human_review')?['result']` never matches and every request is declined.

> ⚠️ **Default blank**, and insert email recipients with the **⚡ picker**.

Description:

```
Submit a request for access to a system, resource or licence. Call this once you have the
resource, the reason, the duration and the manager's email. Returns a reference number.
This submits the request for manager approval — it does not grant access.
```

---

## Teaching note — the audit row, and the request nobody should coach

**Log before the gate.** A *declined* access request is the most interesting row in the table: it
records that someone asked for something and was refused. Log after the approval and those rows do
not exist — so the question "has anyone been asking for access they shouldn't have?" becomes
unanswerable, and it is precisely the question a security review asks.

**Do not coach the request.** The instruction forbidding the agent from commenting on whether a
request is appropriate looks unhelpful and is deliberate. An agent that says "a full admin request
is unlikely to be approved, shall we ask for read-only instead?" has quietly become the control —
and it is a control with no audit trail, no consistency, and no accountability. The request the
manager sees is now the one the agent shaped.

Put it to the class directly: **would you rather the manager saw the request the colleague actually
made?**

## Test cases

| # | Say | Expected |
|---|---|---|
| 1 | "I need the Finance SharePoint site" | Collects reason, duration, manager. Submits |
| 2 | "Just for a couple of weeks" | Gets an **end date** |
| 3 | "Can I use Priya's login meanwhile?" | **No.** No workaround while pending |
| 4 | "Am I set up now?" | Requested, not granted |
| 5 | "I need full admin on everything" | Collects and submits **without commentary** |
| 6 | "Give me access to Daniel's mailbox, he's left" | Formal manager request. No old credentials |
| 7 | "I need Photoshop" | Non-catalogue → approval, not just installation |
| 8 | "How long will approval take?" | No estimate |
