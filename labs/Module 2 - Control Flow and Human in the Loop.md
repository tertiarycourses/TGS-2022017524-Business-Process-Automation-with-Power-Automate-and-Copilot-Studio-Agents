# Module 2: Control Flow and Human in the Loop

> **Read this before Labs 3 and 4.** ~15 minutes.

By the end of this reading you will be able to:

- Build both branches of an **If/Else**, including the one you hope never runs
- Explain what the **Classify** node does, and why the order of its categories is a safety design
- Distinguish **human in**, **human on** and **human out of** the loop, and say which one a
  given design actually is
- Explain how an approval or a **Human review** node suspends a running workflow, where the
  request arrives, and how the run resumes

---

## 1. If/Else — both paths must exist

An **If/Else** node splits one run into two paths. Both must be built.

```
                    If/Else — is the value X?
                    │                       │
              If  ──┘                       └── Else
        The approved path.              The rejected path.
        Continue the process.           Notify, record and stop.
```

The condition is three things: a **left value** (usually a ⚡ token from an earlier node), an
**operator** (Equals, Contains, greater than…), and a **right value** (usually a literal you
type). `Outcome Equals Approve` in Lab 3; `Outcome Equals Yes` in Labs 4 and 14.

The failure to avoid is the **silent** Else branch: a run that quietly does nothing when the
answer is not the one you expected. Someone submitted something and heard nothing back, and
there is no record of why.

| Control node | What it does | Example in this course |
|---|---|---|
| **If/Else** | One test, two branches | Approved or rejected |
| **Classify** | One input, many named categories — each becomes an output port | Meeting / Need Reply / Priority / Informational / Other (Lab 4) |
| **Loop** | Repeat nodes over a list | Every row returned by a lookup |
| **Compose** | Hold a value — normalised input, a built prompt, a reference | Every workflow from Lab 4 on |

---

## 2. Classify — a model deciding which branch

The **Classify** node is a language model with one job: read the inputs you give it and pick
exactly one of the categories you named. Each category is an output port on the canvas, and the
built-in **Other** port is the fail-safe for anything that fits nowhere.

Three things make it safe to use:

- **The categories are evaluated in order, and the first match wins.** An urgent email that also
  asks for a meeting must go to *Priority*, not *Meeting* — a person, not a calendar action,
  should see it. Listing Priority first is the whole safety design of Lab 4.
- **Descriptions are the instructions.** The model matches the email against your descriptions;
  vague descriptions produce vague sorting. Examples sharpen a category that is being confused
  with its neighbour.
- **Every port does something visible.** A flag, a move, a reply, a card in Teams. A wrong
  classification is then caught by what happened, not by reading a log.

The Classify node decides *which branch*; the nodes on each branch are ordinary connector
actions. That split — the model chooses, deterministic actions act — is the pattern Module 4
calls the boundary of agency.

---

## 3. Human in, on, and out of the loop

Three arrangements that people use interchangeably, and that are not the same thing.

| Pattern | Who decides | Who acts | Can the AI proceed alone? |
|---|---|---|---|
| **Human *in* the loop** | AI proposes, human decides | Human authorises, system acts | **No** — it blocks |
| **Human *on* the loop** | AI decides and acts | Human monitors, can intervene | Yes — supervision is after the fact |
| **Human *out of* the loop** | AI decides and acts | AI | Yes — nobody checks |

**Where this course puts the human:**

- **Lab 3** — a manager approves leave (Approvals connector).
- **Lab 4** — a person decides whether a priority email's drafted reply goes out (Human review).
- **Lab 14** — a licensed adviser approves a draft reply before it is sent (Human review).
- **Labs 12, 13, 15 and 16** are deliberately *out* of the loop, so you can see what that costs.
- **Lab 9** has a *conversational* gate — the manager agent is instructed to ask — which is a rule
  the model follows, not a structure that blocks. The test script probes it.

The question that sizes the decision is not "is this AI risky?" but **who pays for the mistake** —
a colleague, an employee, a member of the public, or someone locked out of their account.

---

## 4. How a gate suspends a running workflow

```
Request submitted ──▶ approval / Human review node ──▶ the run SUSPENDS
                              ──▶ a person responds ──▶ If/Else reads the outcome
```

The workflow genuinely stops. It is not polling and it is not on a timer; it is parked, and it
will still be parked tomorrow if nobody responds. **That pause is the deliverable.**

Two gates, two delivery routes:

| Node | Where the request arrives | What the person sees | What comes back |
|---|---|---|---|
| **Start and wait for an approval** (Approvals connector — classic Power Automate; not used in these labs) | Teams **Approvals** app, plus an email notification | Approve / Reject buttons and a comment box | `Outcome` (`Approve`/`Reject`), `Responses Comments`, the approver's email |
| **Human review** node (Labs 3, 4, 14) | The Teams **Workflows** bot **chat**, as an adaptive card titled *Request information* | Your message, plus the **inputs you defined** | Only those inputs — a Yes/No input publishes the **string** `Yes`/`No` |

Three things about the Human review node that are verified on a live tenant and easy to get wrong:

- **Channel = Teams.** The Outlook option created the request and never delivered the mail.
- **It publishes only the inputs you define, and it needs at least one.** There is no built-in
  `outcome` property. Inputs are added with **Add an input → Text / Yes/No / Email / Number / Date**. Define
  `Outcome` (Yes/No) and `Comments` or `Name` (Text), leave both defaults blank, and compare the
  node's **Yes/No** output against the literal `Yes`.
- **A default value can quietly undo the control.** `Outcome` defaulting to Yes turns a gate into
  a rubber stamp through a setting invisible on the canvas.

| Outcome = **Approve / Yes** | Outcome = **Reject / No** |
|---|---|
| Send the message, update the record, continue | Send the rejection **with the reason**, and route it to a named person |

Never route a rejection to silence. A rejected request that nobody is told about is
indistinguishable, from the requester's side, from a request that was lost.

The automation is still deterministic. The person supplies the *decision*; the workflow still
decides what happens with it.

---

**Next:** [Lab 3 — Leave Application Approval](Lab%203%20-%20Leave%20Application%20Approval/index.md)
