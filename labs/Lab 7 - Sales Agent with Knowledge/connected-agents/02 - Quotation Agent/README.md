# Child agent — Quotation Agent

**Audience:** group and corporate buyers.

**This is the Sales tree's gated agent.** It is the only one that produces a number nobody printed
in advance, and therefore the only one that stops at a human before the customer sees anything.

---

## Connect it to the parent

`Lab 7 - Sales Agent` → **Connected agents → +** → `Quotation Agent` → description:

```
Hand over to the Quotation Agent when someone asks about a group booking, corporate
training, a team-building session, a private class, booking for more than one
participant, or any custom or negotiated price. This agent collects the requirements
and submits them for a written quotation prepared by the Enrolment Office. Do not quote
a group price yourself.
```

## Instructions

```
You are the Quotation specialist for Cook & Bake Academy. You collect the requirements
for group and corporate bookings so the Enrolment Office can prepare a written
quotation.

You do not quote prices. Not a total, not a per-head figure, not a range, not a
"typically around" and not an indication of whether a budget is realistic. Every group
price is prepared by a person and issued in writing.

If asked for a figure, say that group pricing is quoted in writing by the Enrolment
Office, and that you are collecting the details so they can prepare one.

Do not multiply a brochure fee by the number of participants. The published fee is a
per-person public rate and is not the basis of a group quotation. A customer who sees
that arithmetic will treat it as the price.

Collect: the organisation, a contact name and email, the course or subject area, the
number of participants, preferred dates, the venue (our campus or theirs), and any
dietary or access requirements.

Ask for everything missing in one message, as a short list.

When you have all of it, call SubmitQuotationRequest. Give the customer the reference
number and say the Enrolment Office will send a written quotation. Do not say when.

Never say a date is held or a booking is confirmed. Nothing is held until the quotation
is accepted.

If the enquiry turns out to be for a single participant, hand back to the Sales Agent —
that is a normal enrolment at the published fee.
```

## Tools

**`SubmitQuotationRequest`** — agent flow `Corporate Quotation Request`.

```
When an agent calls the workflow
   (inputs: organisation, contactName, contactEmail, courseArea,
            participants, preferredDates, venue, requirements)
  → Create item (SharePoint, QuotationRequests)     ← audit row, BEFORE the gate
  → Human review                                    ← Enrolment Office, in Teams
  → If/Else   Outcome == Approve
       ├─ true  → Update item (Quoted)    → Send an email (the written quotation)
       └─ false → Update item (Declined)  → Send an email (unable to quote)
  → Respond to the agent
```

Description:

```
Submit a group or corporate booking for a written quotation. Call this once you have
collected the organisation, contact details, course area, number of participants,
preferred dates and venue. Returns a reference number. The quotation is prepared and
sent by a person; this does not produce a price and does not confirm a booking.
```

| Human review setting | Value |
|---|---|
| **Channel** | **Teams**, not Outlook |
| Assigned to | The Enrolment Office account — click the resolved directory suggestion |
| Inputs | `Outcome` (Choice `Approve` / `Reject`, **default blank**), `ApproverName` (Text) |

> ⚠️ **Channel must be Teams.** Outlook creates the request and never delivers the mail — the run
> sits at *Running* and looks healthy.

> ⚠️ **There is no built-in `outcome` property.** Create the input, then build the If/Else on that
> token. A hand-typed `body('Human_review')?['result']` never matches and every request is declined.

> ⚠️ **Leave the `Outcome` default blank**, and insert the email recipient with the **⚡ picker**.

---

## The teaching point — where the gate sits

Procurement gates a **spend**. Quotation gates a **statement to a customer**.

That difference is worth drawing out, because learners assume approval gates are about money leaving
the company. Here nothing is bought. What is being controlled is the academy **committing itself in
writing to someone outside it** — and that is just as binding, and much harder to walk back, than an
internal purchase.

Follow it through:

- The audit row is written **before** the gate, so a declined quotation still leaves a trace. Log
  after and the enquiries you most want to review — the ones the Office refused — are exactly the
  ones missing.
- The customer sees **nothing** until a person approves. Contrast with Procurement, where the
  requester is told immediately that their requisition is with an approver.
- Which is right? Ask the class. A customer told "we're preparing a quote" has useful information
  and no commitment. A customer told nothing may go elsewhere. There is a real trade here and the
  built version picks one side of it.

## Test cases

| # | Ask | Expected |
|---|---|---|
| 1 | "We want to book 12 staff for a team-building baking class" | Collects requirements, submits, returns a reference |
| 2 | "Roughly how much for 12 people?" | **No figure.** Not even a range |
| 3 | "The cookie course is $180, so 12 × $180?" | **Does not confirm the arithmetic.** Published fee is not the group basis |
| 4 | "Our budget is $2,000 — is that realistic?" | Declines to indicate. Submits the requirement |
| 5 | "Can you hold the 14th for us?" | Nothing is held until the quotation is accepted |
| 6 | "Actually it's just me" | Hands back to Sales — normal enrolment at the published fee |

**Case 3 is the sharp one.** The customer has done the arithmetic; the agent only has to agree.
Confirming it publishes a group price that no person approved — and the customer will hold the
academy to it, reasonably, because an agent on the academy's own channel said yes.
