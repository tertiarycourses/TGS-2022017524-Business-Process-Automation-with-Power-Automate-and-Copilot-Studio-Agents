# Skill 4 — Raise IT Support Ticket

> **Agent → Skills → +** → name it exactly `Raise IT Support Ticket`.
>
> **This is the skill every other skill ends at.** The other four decide *whether* a ticket is
> needed; this one decides what goes in it.

**Skill name:** `Raise IT Support Ticket`

**Description:**

```
Use when an issue cannot be resolved in the conversation and needs a technician, or when
a colleague asks to raise a ticket, log a fault, or be put in the queue.
```

**Instructions:**

```
Before raising a ticket, collect:

  - Category: Password, Software, Hardware, Network or Access
  - What is happening, in the colleague's own words
  - The exact error message if there is one
  - When it started
  - The asset tag if a specific device is involved
  - Whether anyone else is affected
  - What has already been tried in this conversation

The last one matters most and is the one that gets dropped. A ticket that does not say
what was already tried sends a technician through the same fifteen minutes the colleague
just spent, and the colleague has to describe it all again.

Ask for anything missing in one message, as a short list.

Say how urgent it is in the colleague's own terms — whether they can work, whether a
deadline is affected, whether anyone else is blocked. Do not assign a priority yourself.
Priority is set by the Triage Agent against the service catalogue, and an agent that
assigns it from how upset the caller sounds produces a queue ordered by tone.

Call RaiseTicket once. Give the colleague the ticket reference.

If the ticket has an SLA in the service catalogue for that category, quote it as a
target, not a promise. If there is no SLA, do not invent a timeframe. "Someone will look
at this today" is a commitment you have no authority to make, and the colleague will
remember it.

Never raise more than one ticket for the same issue. If a colleague comes back about
something already raised, use CheckTicketStatus and give the current status instead.

Never say an issue is resolved, fixed, or being worked on right now. A ticket has been
raised; that is all you know.

For anything involving suspected compromise, data loss, or an outage affecting many
people, escalate to a person rather than raising a normal ticket.
```

---

## Teaching note — three things worth pausing on

**1. "What has already been tried" is the field that makes a ticket worth having.** It is also the
one an agent drops first, because it is the only field that requires remembering the conversation
rather than asking a question. Test for it explicitly.

**2. Priority does not belong here.** An agent that sets priority from the conversation is setting
it from the caller's *tone* — so the colleague who says "this is a disaster" outranks the one who
says "sorry to bother you", regardless of what is actually broken. Priority against a published
catalogue is a policy; priority from tone is a bias with a queue attached.

**3. "A ticket has been raised" is not "someone is working on it".** The gap between the two is
where the agent's language does the damage. A colleague who believes a technician is looking at it
now will not chase, and will be angry in four hours — at a promise the agent never had the standing
to make.

## Test cases

| # | Say | Expected |
|---|---|---|
| 1 | (after failed network troubleshooting) "Can you log this?" | Collects the fields; ticket **includes what was tried** |
| 2 | "This is urgent, I have a board meeting" | Records the impact. **Does not set priority** |
| 3 | "When will it be fixed?" | SLA as a target, or no timeframe at all |
| 4 | "I raised this yesterday, any update?" | `CheckTicketStatus`. **No second ticket** |
| 5 | "I think I clicked a phishing link" | **Escalates.** Not a normal ticket |
| 6 | "Is someone looking at it now?" | Says a ticket is raised. Nothing more |
