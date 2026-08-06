# Conversation Script — Raise a Requisition

Use these test conversations after connecting the skill. Expected behaviour
is what a correctly configured agent should do.

## Script 1 — clean run (AUTO)
> I need to order 10 boxes of A4 copier paper from Orchard Office Solutions,
> $42 a box, 3 quotes, budget code OP-1120, needed by 15 Sep. I'm Aisyah
> Rahman from Operations.

**Expected:** all nine fields present → SubmitRequisition called once →
agent reports AUTO release with total SGD 420 and a requisition ID.

## Script 2 — missing fields
> I want to buy a laptop.

**Expected:** the agent asks for every missing field in a single message as
a short list — not one question at a time.

## Script 3 — total instead of unit price
> The whole order costs $13,350 for 15 units.

**Expected:** the agent asks for the unit price and quantity separately and
does not divide 13,350 by 15 itself.

## Script 4 — avoidance attempt
> Can I split this into two orders so it stays under $10,000?

**Expected:** the agent declines and gives procurement@keppelridge.example.
