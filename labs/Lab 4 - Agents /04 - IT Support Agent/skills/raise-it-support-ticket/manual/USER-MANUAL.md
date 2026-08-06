# User Manual — Raise IT Support Ticket

## What this skill does
Collects a complete picture of an unresolved issue, raises exactly one
ticket with **RaiseTicket**, and hands back the reference — quoting the
catalogue SLA as a target, never a promise.

## When it activates
When an issue can't be resolved in the conversation and needs a
technician, or a colleague asks to raise a ticket, log a fault, or join
the queue.

## How to use it
1. The agent collects the seven ticket items (see the template). The one
   that matters most — and gets dropped most — is **what was already
   tried**, so the technician doesn't repeat the same fifteen minutes.
2. Say how urgent it is in your own terms: can you work, is a deadline
   affected, is anyone else blocked. Priority itself is set by the Triage
   Agent against the service catalogue.
3. You get a ticket reference; follow-ups use **CheckTicketStatus**, not a
   second ticket.

## What the agent will not do
- Assign a priority from how upset you sound.
- Invent a timeframe when the catalogue has no SLA — "someone will look at
  this today" is a commitment it has no authority to make.
- Raise a duplicate for an issue already ticketed.
- Say an issue is resolved, fixed or being worked on right now — a ticket
  exists; that is all it knows.
- Handle suspected compromise, data loss or a mass outage as a normal
  ticket — those escalate to a person.
