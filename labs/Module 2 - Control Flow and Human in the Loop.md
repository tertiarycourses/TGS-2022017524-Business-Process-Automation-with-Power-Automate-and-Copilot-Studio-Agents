# Module 2: Control Flow and Human in the Loop

> **Read this before Lab 3.** ~12 minutes. Deck slides 21–24.

By the end of this reading you will be able to:

- Build both branches of a condition, including the one you hope never runs
- Distinguish **human in**, **human on** and **human out of** the loop, and say which one a
  given design actually is
- Explain how an approval suspends a running flow and how the run resumes

---

## 1. Conditions — both paths must exist

A condition splits one run into two paths. Both must be built.

```
                    Condition — is the value X?
                    │                       │
              YES ──┘                       └── NO
        The approved path.              The rejected path.
        Continue the process.           Notify, record and stop.
```

The failure to avoid is the **silent** No branch: a run that quietly does nothing when the
answer is not the one you expected. Someone submitted something and heard nothing back, and
there is no record of why.

| Control action | What it does | Example in this course |
|---|---|---|
| **Condition** | One test, two branches | Approved or rejected |
| **Switch** | One value, many branches | Leave type: Annual / Medical / Compassionate / Unpaid |
| **Apply to each** | Repeat actions over a list | Every row returned by a lookup |
| **Terminate** | End the run deliberately | Stop with a status a reader can interpret |

---

## 2. Human in, on, and out of the loop

Three arrangements that people use interchangeably, and that are not the same thing.

| Pattern | Who decides | Who acts | Can the AI proceed alone? |
|---|---|---|---|
| **Human *in* the loop** | AI proposes, human decides | Human authorises, system acts | **No** — it blocks |
| **Human *on* the loop** | AI decides and acts | Human monitors, can intervene | Yes — supervision is after the fact |
| **Human *out of* the loop** | AI decides and acts | AI | Yes — nobody checks |

**Where this course puts the human:**

- **Lab 3** — a manager approves leave.
- **Lab 8** — a licensed adviser approves a draft reply before it is sent.
- **Labs 6, 7, 9 and 10** are deliberately *out* of the loop, so you can see what that costs.

The question that sizes the decision is not "is this AI risky?" but **who pays for the mistake** —
a colleague, an employee, a member of the public, or someone locked out of their account.

---

## 3. How an approval suspends a running flow

```
Request submitted ──▶ Start and wait for an approval ──▶ the run SUSPENDS
                              ──▶ a person responds ──▶ Condition reads the Outcome
```

The flow genuinely stops. It is not polling and it is not on a timer; it is parked, and it will
still be parked tomorrow if nobody responds.

| Outcome = **Approve** | Outcome = **Reject** |
|---|---|
| Send the approval message, update the record, continue the process | Send the rejection **with the approver's comments**, and route it to a named person |

Never route a rejection to silence. A rejected request that nobody is told about is
indistinguishable, from the requester's side, from a request that was lost.

> ### Send approvals to Teams, not Outlook
>
> Verified on a live tenant: **Outlook created the approval request and never delivered the
> mail.** The run sat at *Running*, looking perfectly healthy. Every human gate in these labs
> uses the **Microsoft Teams Approvals** app.

The automation is still deterministic. The person supplies the *decision*; the flow still
decides what happens with it.

---

**Next:** [Lab 3 — Leave Application Approval](Lab%203%20-%20Leave%20Application%20Approval/index.md)
