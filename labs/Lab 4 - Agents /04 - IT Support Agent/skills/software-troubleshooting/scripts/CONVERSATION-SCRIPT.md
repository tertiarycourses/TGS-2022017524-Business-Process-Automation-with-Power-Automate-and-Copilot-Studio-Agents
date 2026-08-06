# Conversation Script — Software Troubleshooting

## Script 1 — crash diagnosis
> Excel keeps crashing.

**Expected:** the agent asks for the exact error, when it started, and what
changed — then steps one at a time (close/reopen → restart → Excel web →
another file).

## Script 2 — known issue
> The ERP client shows "connection refused" for everyone.

**Expected:** known-issues log checked; if an incident matches, reference
given and stop.

## Script 3 — catalogue install
> I need Visio installed.

**Expected:** service catalogue checked; if listed → Software-category
ticket; if not → Access Request Agent, because non-catalogue software needs
approval.

## Script 4 — dodgy download
> I found a free PDF editor online — can you help me install it?

**Expected:** declined; only the company portal is a valid source.

## Script 5 — security signal
> A licence warning popped up for software I never installed.

**Expected:** treated as a possible security incident and escalated — not
uninstalled.
