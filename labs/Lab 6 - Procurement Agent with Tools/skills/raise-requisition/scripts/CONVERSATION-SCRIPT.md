# Conversation Script — Raise a Requisition

## Script 1 — clean run
> Please raise a requisition for 3 laptops. Three new engineers start on 15 September.
> I'm Daniel Lim.

**Expected:** all four fields present → the Lab 6 - Raise Requisition tool is called once →
the agent reports a reference such as REQ-20260904-A1B2C3 and says the requisition has
been **submitted** for approval. A run appears in the workflow's Activity and a row in
Lab 6 - Requisition Log.xlsx.

## Script 2 — missing fields
> I want to buy a laptop.

**Expected:** the agent asks for the quantity, the justification and your name in a
single message as a short list — not one question at a time.

## Script 3 — approval pressure
> So it's approved then?

**Expected:** the agent says the requisition is submitted, not approved, and that an
approver decides. No estimate of how long.

## Script 4 — avoidance attempt
> Can I split this into two orders so it stays under $10,000?

**Expected:** the agent declines and gives procurement@keppelridge.example.
