# Tools — IT Support Agent

| Tool | Reads or writes | Gate |
|---|---|---|
| `RaiseTicket` | Writes | None — a ticket is a request |
| `CheckTicketStatus` | Reads | None |
| `LookupAsset` | Reads | None |

**None of these tools changes anything on a device or an account.** They open a ticket, read a
ticket, and read the asset register. Every action a colleague actually wants — a reset, an install,
a replacement — is performed by a person.

Say that plainly in class, because the agent's *name* implies otherwise, and so does the
conversation. A colleague who has just been walked through six troubleshooting steps reasonably
assumes the thing that then happens is a fix.

---

## Tool 1 — `RaiseTicket`

**Source:** agent flow `IT Ticket Intake`.

```
When an agent calls the workflow
   (inputs: requesterEmail, category, summary, description, assetTag,
            errorMessage, stepsAlreadyTried, othersAffected)
  → Create item (SharePoint, ITTickets)
  → Send an email (Outlook) to the service desk
  → Respond to the agent      ← returns the ticket reference
```

**Description:**

```
Raise an IT support ticket. Call this when an issue cannot be resolved in the
conversation. Collect the category, what is happening, the exact error message, when it
started, the asset tag if a device is involved, whether others are affected, and what has
already been tried. Returns a ticket reference. This queues the ticket for a technician —
it does not resolve the issue, reset anything or install anything.
```

> **`stepsAlreadyTried` is a required input for a reason.** Make it required in the contract, not
> optional. An optional field that the agent must be *instructed* to fill will be empty on the
> tickets where the conversation ran long — which are exactly the tickets where it matters most.
> **Put the requirement in the schema, where the model cannot skip it.**

> ⚠️ **Insert the service-desk address with the ⚡ picker.** A typed expression in the Outlook `To`
> field fails with a trailing-`\n` conversion error; typing the expression is what creates the
> newline, so `trim()` does not fix it.

---

## Tool 2 — `CheckTicketStatus`

```
When an agent calls the workflow   (inputs: ticketRef, requesterEmail)
  → Get items (SharePoint, ITTickets, Top Count 1)
  → Respond to the agent
```

**Filter Query** — literal text, value inserted with the **⚡ picker**:

```
TicketRef eq '<⚡ toUpper(trim(ticketRef)) token>'
```

**Description:**

```
Check the status of an existing IT ticket. Call this when a colleague asks for an update
on a ticket they have already raised, or comes back about an issue that already has a
reference. Returns the status and when it was last updated. Use this instead of raising a
second ticket for the same issue.
```

> **Pass `requesterEmail` and have the flow check it against the ticket's requester.** Otherwise
> anyone with a reference — or guessing one — reads anyone's ticket, and ticket descriptions
> routinely contain a colleague's name, device, location and what they were doing.
>
> This is a **structural** control: the check is in the flow, not in the prompt. Contrast it with the
> Account Health Agent, where the equivalent boundary is only an instruction. Ask the class which
> they trust and why.

---

## Tool 3 — `LookupAsset`

```
When an agent calls the workflow   (input: assetTag, Text)
  → Get items (SharePoint, AssetRegister, Top Count 1)
  → Respond to the agent
```

```
Filter Query:  AssetTag eq '<⚡ toUpper(trim(assetTag)) token>'
```

> **`toUpper(trim(...))` inside the filter.** A colleague reads "kr-lt-0142" off a label. Without
> normalisation the lookup returns nothing, the agent says the asset does not exist, and **no error
> appears anywhere**. Same shape as TC12 in Procurement, and the third time this trap appears in Lab
> 4 — name it as a pattern, not a quirk.

**Description:**

```
Look up a device in the asset register by asset tag, for example KR-LT-0142. Call this
when a colleague reports a problem with a specific device. Returns the model, purchase
date, warranty status and who the device is assigned to.
```

**Outputs:** `found`, `model`, `purchaseDate`, `warrantyStatus`, `assignedTo`, `location`.

> **`assignedTo` needs a rule around it.** If the device is assigned to someone other than the
> colleague you are speaking to, the agent must stop and ask — and it must **not** read the assigned
> name out. "That tag is registered to someone else, can you double-check it" helps; naming the
> person turns an asset lookup into a directory lookup for anyone who can read a label.

---

## What is deliberately absent

| Not a tool | Why |
|---|---|
| `ResetPassword` | A reset needs identity verification the agent cannot perform. The whole [Password Reset Procedure](../skills/password-reset-procedure.md) skill rests on this being impossible. |
| `GrantAccess` | Access changes go through the Access Request Agent, which has a **human gate**. |
| `InstallSoftware` | Needs admin rights, licence checks and approval for non-catalogue software. |
| `OrderReplacement` | Purchases belong to Procurement, where the CAPEX rule and the approval gate live. |

**Every one of these absences is a control.** An agent cannot misuse a tool it does not have, and
that is the only guarantee in this lab that does not depend on the model behaving. If a learner asks
why the agent cannot just reset a password when it clearly knows how — that is the answer.

Remove the **Search all websites** chip before the first test.
