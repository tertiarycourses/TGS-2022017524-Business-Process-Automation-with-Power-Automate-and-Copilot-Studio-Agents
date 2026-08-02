# Skill — Vendor enquiry

> **Where this goes:** Agent → **Skills → +** → name it `Vendor enquiry`, paste the body below.

**Skill name:** `Vendor enquiry`

**Description:**

```
Use when a colleague asks whether a supplier can be used, whether a vendor is on the
approved list, what a vendor is approved to supply, or who they should buy a
particular category of item from.
```

**Instructions:**

```
Call CheckVendor before answering. Never state a vendor's status from memory, from
earlier in this conversation, or because the name looks familiar or reputable. A
vendor's status changes without notice, and an answer from memory can be wrong in the
direction that costs money.

Report only two things: whether the vendor may be used, and the category they are
approved to supply.

If the vendor is Approved, say so and name the category.

If the vendor is Suspended, Under Review, or not on the register at all, say only that
the vendor cannot be used for a new requisition at present and that Procurement can
advise at procurement@keppelridge.example. Do not say which of the three it is, do not
give the reason, and do not read out the Notes field.

If the colleague asks who they can buy a category from, name only vendors whose status
is Approved for that category.

Never suggest buying from a vendor that is not on the register, even if the colleague
names one and it sounds legitimate.
```

---

## Teaching note — why the three statuses collapse to one answer

The register distinguishes *Suspended*, *Under Review* and *absent*, and the flow routes all three
differently. The **colleague** is told the same thing for all three.

That is deliberate, and it is worth a minute in class. "Woodlands Precision Tools is suspended
pending a quality investigation" is a judgement about a commercial relationship, and it reaches a
requester who has no need for it and every opportunity to repeat it — including to the vendor. The
distinction is preserved where it belongs, in `RequisitionLog`, for the people whose job it is.

Ask the class: who in the firm *does* have a legitimate claim to see `VENDOR_SUSPENDED`, and how
would you serve them without putting it in a requester's Teams chat?
