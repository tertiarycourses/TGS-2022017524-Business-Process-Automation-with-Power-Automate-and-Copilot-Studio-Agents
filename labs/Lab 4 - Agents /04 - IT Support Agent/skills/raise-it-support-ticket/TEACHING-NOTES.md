# Teaching notes — Raise IT Support Ticket

> Trainer notes. Kept out of `SKILL.md` on purpose.

**Where this goes:** `IT Support Agent` → **Build → Skills → Add skill → Upload a skill**, then
drop [`raise-it-support-ticket.zip`](../_packages/raise-it-support-ticket.zip) onto the upload box.

> **This is the skill every other skill ends at.** The other four decide *whether* a ticket is
> needed; this one decides what goes in it.

---

## Three things worth pausing on

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
