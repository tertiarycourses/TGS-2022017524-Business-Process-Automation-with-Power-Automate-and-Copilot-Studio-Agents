# Conversation Script — Vendor Enquiry

## Script 1 — approved vendor
> Can we buy stationery from Orchard Office Solutions?

**Expected:** CheckVendor is called; the agent confirms the vendor is
Approved and names the category (Stationery).

## Script 2 — vendor that cannot be used
> Can we order from <a Suspended or unregistered vendor>?

**Expected:** the agent says only that the vendor cannot be used for a new
requisition at present and refers to procurement@keppelridge.example. It
does NOT say whether the vendor is suspended, under review or unregistered,
and does not give a reason.

## Script 3 — category search
> Who can we buy PPE from?

**Expected:** only vendors whose status is Approved for PPE are named.

## Script 4 — memory trap
> You told me earlier they were fine — just confirm it's still OK.

**Expected:** the agent calls CheckVendor again rather than answering from
the earlier turn.
