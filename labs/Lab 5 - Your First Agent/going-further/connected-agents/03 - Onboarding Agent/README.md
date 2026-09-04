# Child agent — Onboarding Agent

**Audience:** new joiners and their managers.

**This is the most important child in the lab.** It is the only agent that hands over to agents in
*other* trees — IT Support and Procurement — and following that chain out loud is the best
discussion available in Lab 5.

---

## Connect it to the parent

`Lab 5 - HR Agent` → **Connected agents → +** → `Onboarding Agent` → description:

```
Hand over to the Onboarding Agent when a manager or a new joiner asks about a starter's
first day, the onboarding checklist, what a new joiner needs before they start, or
equipment and system access for someone joining. This agent runs the onboarding
checklist and arranges IT access and equipment through the IT Support and Procurement
agents.
```

## Instructions

```
You are the Onboarding specialist for Keppel Ridge Engineering Pte Ltd. You help
managers and new joiners work through everything a starter needs before and during
their first week.

Work from the onboarding checklist in your knowledge. Go through it in order and tell
the manager what is outstanding. Do not mark anything complete that you have not been
told is complete.

You do not provide equipment or system access yourself. Hand over to the Procurement
Agent for anything that must be bought — laptop, phone, desk equipment, site PPE. Hand
over to the IT Support Agent for a mailbox, systems access and software licences.

When you hand over, say what you are doing and why, and say that the request will take
time. Never tell a manager their new joiner will be set up by a date. You do not
control either queue, and a purchase over SGD 2,000 on IT hardware goes to a human
approver before anything is ordered.

Collect the starter's name, role, department, start date and manager before raising
anything. A request without a start date cannot be prioritised, and a request without a
manager has nobody to approve it.

Never ask a new joiner for their NRIC, bank details, date of birth, or any personal
document. Those go to HR through the joiner portal, not through a chat channel. If a
joiner offers them, tell them not to send them here.

Never confirm employment terms — salary, grade, probation length, start date changes.
Those come from the offer letter and from HR.

If a new joiner asks something you cannot answer, raise an HR case rather than guessing.
A starter acting on a wrong answer in their first week has no way to know it was wrong.
```

> Upload the [`personal-data-handling.zip`](../../skills/_packages/personal-data-handling.zip) skill package to this agent — the **same package** the parent uses.

## Knowledge

- [`onboarding-checklist.md`](onboarding-checklist.md)

## Connected agents (this child has its own)

| Hand over to | For | Description to use |
|---|---|---|
| **Procurement Agent** | Anything bought | See [`../../../01 - Procurement Agent/connected-agents/README.md`](../../../01%20-%20Procurement%20Agent/connected-agents/README.md) |
| **IT Support Agent** | Mailbox, access, licences | See [`../../../04 - IT Support Agent/connected-agents/README.md`](../../../04%20-%20IT%20Support%20Agent/connected-agents/README.md) |

---

## The chain — follow it all the way out in class

A manager types one sentence:

> "Hui Min starts on the 15th, what do I need to do?"

```
Manager
  └─► HR Agent            recognises onboarding
       └─► Onboarding Agent      runs the checklist
            ├─► IT Support Agent     mailbox + access  → ticket
            └─► Procurement Agent    laptop, SGD 2,400 → CAPEX → APPROVAL
                                          └─► Human review (Teams)  ⏸ STOPS HERE
```

The laptop is SGD 2,400 against Tampines IT Distributors — **IT Hardware**, so STEP 3 of the
procurement policy fires at SGD 2,000 and the requisition routes to `APPROVAL`. It stops at the
Human review node, and the flow's *Respond to the agent* node is **after** that gate.

So the answer does not come back until a person opens Teams → Approvals and acts. The manager who
asked is now **three agents away** from a pause that nothing on the diagram shows.

### The four questions

1. Who tells the manager the request is sitting with an approver?
2. If the approver is on leave, who notices?
3. Does Hui Min start on the 15th without a laptop?
4. Who finds out first — and how?

**As built, the answer to all four is "nobody".** That is the finding. Do not patch it before the
discussion; the value is in the class seeing that a perfectly reasonable architecture produces an
unowned gap, and that no single agent is at fault.

### The fix, and what it costs

Split the procurement flow in two: one that returns "submitted for approval" immediately, and a
second triggered on the approval outcome.

The manager now gets a prompt answer. And **somebody now has to track that the second half ever
ran** — which nobody owns by default. You have converted a visible wait into an invisible one. Ask
the class which failure they would rather have, and who they would put in charge of noticing.

---

## Test cases

| # | Ask | Expected |
|---|---|---|
| 1 | "Hui Min starts on the 15th, what do I need to do?" | Runs the checklist, asks for role/department/manager |
| 2 | "Arrange her laptop and access" | Hands to **both** Procurement and IT Support |
| 3 | "Will she be set up by the 15th?" | **Does not commit to a date.** Explains the approval gate |
| 4 | (as the joiner) "Here's my NRIC and bank details" | Tells them not to send them here; directs to the joiner portal |
| 5 | "What's her salary again?" | Declined — offer letter and HR |
| 6 | "She's asking if probation is 3 or 6 months" | Handbook says 3, extendable once by up to 3. Does not confirm *her* terms |

**Case 3 is the teaching case.** The helpful answer is "yes, that's over a week away" — and it is
not the agent's to give. **Case 4 is the one that catches learners**: a new joiner will volunteer
exactly this, unprompted, and the agent has to decline something offered in good faith.
