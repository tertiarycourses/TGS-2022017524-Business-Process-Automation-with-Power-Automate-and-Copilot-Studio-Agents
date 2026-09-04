# Conversation Script — Vendor Enquiry

## Script 1 — approved vendor
> Can we buy stationery from Orchard Office Solutions?

**Expected:** the agent reads the register and confirms the vendor is Approved for
Stationery.

## Script 2 — vendor that cannot be used
> Can we order machinery from Woodlands Precision Tools?

**Expected:** the agent says only that the vendor cannot be used for a new requisition
at present and refers to procurement@keppelridge.example. It does NOT say the vendor is
suspended, and does not give the reason in the Notes column.

## Script 3 — category search
> Who can we buy PPE from?

**Expected:** only vendors whose Status is Approved for PPE are named (Jurong Safety
Equipment).

## Script 4 — memory trap
> You told me earlier they were fine — just confirm it's still OK.

**Expected:** the agent checks the register again rather than answering from the
earlier turn.
