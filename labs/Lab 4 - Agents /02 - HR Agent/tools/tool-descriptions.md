# Tools — HR Agent

The parent holds **three** tools. Everything else it does is a handover.

| Tool | Reads or writes | Gate |
|---|---|---|
| [`LookupLeaveBalance`](#tool-1--lookupleavebalance) | Reads | None |
| [`SubmitLeaveRequest`](#tool-2--submitleaverequest) | **Writes** | **Manager approval, Teams** |
| [`CreateHRCase`](#tool-3--createhrcase) | Writes | None — a case is a request, not a decision |

That ratio is the point: an orchestrator that accumulates tools stops being an orchestrator. If you
find yourself adding a fourth tool here, ask whether it belongs to a child instead.

> **`SubmitLeaveRequest` is the one that changes the shape of this agent.** The other two read a
> record or open a ticket. This one applies for something on a colleague's behalf, and it is the
> only place in the HR tree where a human gate sits behind the agent. Build it second, after
> `LookupLeaveBalance`, so the class sees the difference between an agent that answers and an agent
> that acts.

---

## Tool 1 — `LookupLeaveBalance`

**Source:** agent flow `HR Leave Balance Lookup`.

```
When an agent calls the workflow   (input: employeeEmail, Text)
  → Get items (SharePoint, StaffLeave, Top Count 1)
  → Respond to the agent
```

**Filter Query** — literal text, value inserted with the **⚡ picker**:

```
EmployeeEmail eq '<⚡ toLower(trim(employeeEmail)) token>'
```

> **Normalise inside the filter, not in the instruction.** `toLower(trim(...))` is what makes a
> mixed-case address still match. Left out, the lookup returns nothing, the agent reports "no record
> found", and **no error appears anywhere** — the wrong answer looks exactly like a right one. This
> is the same failure as TC12 in the Procurement lab, and it is worth naming as a recurring shape
> rather than a one-off quirk.

> ⚠️ **Do not use `concat()` to build the filter.** It validates green and fails at run time with
> *"Creating query failed"*.

**Respond to the agent** outputs: `found`, `annualLeaveRemaining`, `medicalLeaveRemaining`,
`asAtDate`.

**Description:**

```
Look up an employee's remaining leave balance. Call this when a colleague asks how much
leave they have left, how many days they have taken, or what their medical leave balance
is. Pass the signed-in user's email address. Returns annual and medical leave remaining
and the date the figures are correct as at.
```

> **`asAtDate` earns its place.** A balance without a date is a number a colleague will still be
> quoting three weeks later. Instruct the agent to always report it alongside the figure.

---

## Tool 2 — `SubmitLeaveRequest`

**Source:** agent flow `HR Leave Application`. This is the leave application form, as a tool.

```
When an agent calls the workflow
   (inputs: employeeEmail, leaveType, startDate, endDate, numberOfDays, reason, managerEmail)
  → Get items (SharePoint, StaffLeave)          ← re-check the balance server-side
  → If/Else   numberOfDays  >  AnnualLeaveRemaining
       ├─ true  → Respond to the agent  (rejected: insufficient balance)   ← stops here
       └─ false ↓
  → Create item (SharePoint, LeaveRequests)     ← the audit row, BEFORE the gate
  → Human review                                ← the manager, in Teams
  → If/Else   Outcome == Approve
       ├─ true  → Update item (Approved)  → Send an email (confirmed)
       └─ false → Update item (Rejected)  → Send an email (declined)
  → Respond to the agent
```

**Inputs:**

| Input | Type | Note |
|---|---|---|
| `employeeEmail` | Text | The **signed-in** user, never a typed name |
| `leaveType` | Text | Annual, Medical, Childcare, Compassionate, Marriage, Examination |
| `startDate` | Text | Keep as **Text** — see below |
| `endDate` | Text | Keep as Text |
| `numberOfDays` | Number | Working days |
| `reason` | Text | Optional. See the warning below |
| `managerEmail` | Text | Who approves |

> **Keep the dates as Text, not Date.** A Date input makes the agent responsible for turning
> "the week after National Day" into a valid ISO date, and it will sometimes fail the type check
> rather than ask. Same reasoning as `neededBy` in the Procurement tool.

**Description:**

```
Submit a leave application on a colleague's behalf. Call this when a colleague wants to
apply for leave, book time off, or take days off. Collect the leave type, start date,
end date and number of working days before calling. The application goes to their
manager for approval in Teams. Returns a reference number. This submits an application
— it does not approve leave, and approval is the manager's decision.
```

### Three things this tool must be built to do

**1. Re-check the balance in the flow, not in the prompt.** The `If/Else` on
`AnnualLeaveRemaining` is a structural control the model cannot reach. Without it, the only thing
stopping a colleague applying for 30 days they do not have is a sentence asking the agent to check —
and the agent has to be *right* every time for that to hold.

Demonstrate it: tell the agent "I'd like to book four weeks off in December". Jonathan Chee has
**1 day** remaining in [`staff-leave.csv`](../knowledge/staff-leave.csv).

**2. Write the audit row before the gate.** Same rule as the Procurement flow. A leave request
declined by a manager should still leave a trace; log after the gate and the declined applications
are precisely the ones that vanish.

**3. `reason` is optional and the agent must not press for it.** Add this to the agent's
instructions:

```
Never ask why a colleague wants leave. If they volunteer a reason, pass it on only if
it is needed for the leave type — a medical certificate reference for medical leave, a
date for compassionate leave. Never pass on a health condition, a family circumstance
or anything a manager does not need in order to approve dates.
```

> **This is the sharpest teaching moment in the HR agent.** The staff handbook says a manager is
> told the *dates*, not the *diagnosis* (§3). The moment leave is applied for through a
> conversational agent, a colleague will explain themselves — unprompted, in a chat window — and
> whatever they say is one instruction away from arriving in the manager's Teams approval card.
>
> Ask the class where that sentence ends up under each design, and note what the platform
> contributes: nothing. There is no field-level control here. The `reason` input either carries the
> disclosure or it does not, and which one happens is decided by prose.

### Human review — the build notes that cost time

| Setting | Value |
|---|---|
| **Channel** | **Teams**, not Outlook |
| Assigned to | `managerEmail` — type it, **wait for the directory lookup, click the suggestion** |
| Inputs | `Outcome` (Choice: `Approve` / `Reject`, **default blank**) and `ApproverName` (Text) |

> ⚠️ **Channel must be Teams.** On a live tenant, Outlook created the approval request and never
> delivered the email — to any address, including tenant users. The run reaches *Running* correctly;
> the mail simply never arrives. The request appears in the Teams **Approvals** app.

> ⚠️ **There is no built-in `outcome` property.** Searching the ⚡ picker for "outcome" returns
> nothing until you create the input. A hand-typed `body('Human_review')?['result']` silently never
> matches, so **every** run falls to the Else branch and every leave request is declined.

> ⚠️ **Leave the `Outcome` default blank.** Defaulting to `Approve` means the request arrives at the
> manager already answered — approving takes no thought, declining takes noticing.

> ⚠️ **Insert the email recipient with the ⚡ picker.** Never type an expression into the Outlook
> `To` field; every typed form fails with a trailing-`\n` conversion error.

---

## Tool 3 — `CreateHRCase`

**Source:** agent flow `HR Case Intake`.

```
When an agent calls the workflow   (inputs: requesterEmail, category, summary)
  → Create item (SharePoint, HRCases)
  → Respond to the agent      ← returns the case reference
```

**Description:**

```
Raise an HR case for a person to handle. Call this when a colleague needs something an
assistant cannot resolve — a question about their own circumstances, a request for a
document or letter, or anything requiring an HR decision. Returns a case reference to
give the colleague. Do not call this for grievances, allegations, disciplinary matters
or anything involving someone's safety; those go directly to hr@keppelridge.example.
```

> **Read that last sentence carefully — it is a design decision, not caution.** A grievance routed
> into a SharePoint case list is a grievance sitting in a list that other people can read, created
> by an assistant that has already recorded the allegation in a Teams transcript. The right handling
> is a direct human channel, and the agent's job is to get out of the way. Ask the class where the
> allegation would have been stored under each design, and who could read it.

---

## What the parent deliberately does **not** have

| Not a parent tool | Why |
|---|---|
| Candidate lookup | Belongs to Screening. The parent talks to staff; candidate records have no business in that context. |
| Interview scheduling | Belongs to Interview. |
| Equipment ordering | Belongs to Onboarding, which hands over to IT Support and Procurement. |
| Anything that writes to an employee **record** | `SubmitLeaveRequest` writes a *request*, which a manager then approves — it does not alter anyone's record. Nothing in this lab updates a personnel record directly, and an agent with that access is a materially different risk conversation. Say so explicitly; learners assume an HR agent updates HR data. |

---

## Turn off "Search all websites"

Knowledge → click the **✕** on the *Search all websites* chip, on the parent **and every child**.

An HR agent with open-web access will answer a question about Singapore employment law from a
search result, in the same voice it uses for the staff handbook. The parent's instructions forbid
interpreting the Employment Act; the web chip quietly makes it possible anyway.
