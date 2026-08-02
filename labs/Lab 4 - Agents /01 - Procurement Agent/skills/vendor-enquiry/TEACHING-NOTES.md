# Teaching notes — Vendor enquiry

> Trainer notes. Kept out of `SKILL.md` on purpose — everything in the skill file is read by the
> model.

**Where this goes:** Agent → **Build → Skills → Add skill → Upload a skill**, then drop
[`vendor-enquiry.zip`](../_packages/vendor-enquiry.zip) onto the upload box.

---

## Why the three statuses collapse to one answer

The register distinguishes *Suspended*, *Under Review* and *absent*, and the flow routes all three
differently. The **colleague** is told the same thing for all three.

That is deliberate, and it is worth a minute in class. "Woodlands Precision Tools is suspended
pending a quality investigation" is a judgement about a commercial relationship, and it reaches a
requester who has no need for it and every opportunity to repeat it — including to the vendor. The
distinction is preserved where it belongs, in `RequisitionLog`, for the people whose job it is.

Ask the class: who in the firm *does* have a legitimate claim to see `VENDOR_SUSPENDED`, and how
would you serve them without putting it in a requester's Teams chat?

## The structural half of this control

Note that `policyFlags` is deliberately **not** returned by the `CheckVendor` tool — see
[`../../tools/tool-descriptions.md`](../../tools/tool-descriptions.md). The instruction above asks
the model not to disclose the reason; the tool contract makes it impossible for the model to know
it. Only the second one holds under pressure.
