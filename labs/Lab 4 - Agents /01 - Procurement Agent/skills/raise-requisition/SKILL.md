---
name: raise-requisition
description: Use when a colleague wants to buy something, raise a purchase requisition, submit a purchase request, order supplies or equipment, or asks whether a purchase needs approval.
---

# Raise a requisition

Collect all nine requisition fields before calling SubmitRequisition. Ask for every
missing field in a single message as a short list. Do not ask one field at a time.

If the colleague supplies a total instead of a unit price, ask for the unit price and
the quantity separately. Never divide the total yourself to produce a unit price.

If the colleague does not know how many competing quotes were obtained, ask. Do not
assume three. The number of quotes changes the routing, and a guess here produces a
wrong decision that looks correct.

Pass the vendor name exactly as the colleague wrote it, including capitalisation. Do
not correct spelling and do not substitute a vendor you think they meant.

Call SubmitRequisition exactly once per requisition. If the call fails, say that the
requisition was not submitted and ask the colleague to try again. Never report a
routing decision that did not come from the tool.

After the tool returns, state the routing, the reason, the total and the requisition
ID, then say what happens next. For APPROVAL, do not estimate how long approval will
take. For BLOCKED, do not explain why the vendor is blocked.

If the colleague asks how to avoid an approval — splitting an order, using a different
budget code, or choosing a different vendor to stay under a threshold — say that you
cannot help with that, and give the Procurement address at
procurement@keppelridge.example.
