# Lab 4 - Email Classification — the Classify node

> **Where this goes:** the **Classify** node (Add panel → **Classify**) in the workflow
> `Lab 4 - Email Classification`. The node has an instruction box, a model picker, and a
> list of **categories** — each category becomes an output port on the node.
>
> The instruction contains **slots** for ⚡ tokens. Type the prose, leave a gap at each slot,
> click into the gap and pick the token. **Never paste text containing `@{…}`** — the box is a
> rich-text editor and a pasted reference resolves to empty.

## Instruction (type this, filling the slots with ⚡)

```text
Classify the email below into exactly one category. Read the subject, the sender, the
importance flag and the body. Pick the FIRST category that applies, in the order the
categories are listed.

Subject: [SUBJECT]
From: [FROM]
Importance flag: [IMPORTANCE]
Body:
[BODY]
```

| Slot | ⚡ pick | Source node |
|---|---|---|
| `[SUBJECT]` | Subject | When a new email arrives (V3) |
| `[FROM]` | From | When a new email arrives (V3) |
| `[IMPORTANCE]` | Importance | When a new email arrives (V3) |
| `[BODY]` | Body | When a new email arrives (V3) |

## Categories (type the name and the description exactly)

| # | Category name | Description |
|---|---|---|
| 1 | `Priority` | An email that is time-sensitive and needs action within 24 hours: a deadline, an outage, a complaint, a payment or contract at risk, the words urgent or ASAP, or a high-importance flag with a request for action. |
| 2 | `Meeting` | An email asking to schedule, reschedule or confirm a meeting, call or visit. |
| 3 | `Need Reply` | An email that asks a question or makes a request that expects an answer, but is not urgent and is not about scheduling a meeting. |
| 4 | `Informational` | Newsletters, notifications, receipts, announcements, FYI messages and thank-you notes that need no action. |
| 5 | `Other` | The built-in fallback. Anything that fits none of the above — empty or unreadable messages, spam, automated bounces. |

The node starts with three category rows; select **Add category** until you have four named
ones. **Other** is the node's own fail-safe port and does not need to be typed.

## Optional examples (Add example → pick the category → paste the text)

| Category | Example text |
|---|---|
| Meeting | `Can we meet next Tuesday at 3pm to discuss the course? Teams is fine.` |
| Priority | `URGENT: the trainer for tomorrow's 9am class has cancelled. Please call me today.` |
| Informational | `Here are the new October intake dates. No reply needed.` |
