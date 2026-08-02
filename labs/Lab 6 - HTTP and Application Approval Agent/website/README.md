# Marina Trust Bank — onboarding website (Copilot Studio edition)


The form, styling and the ten trainer demo cases are unchanged. Only the
integration layer differs.

---

## Running it

```bash
cd website
python3 -m http.server 8900
```

Open <http://localhost:8900/index.html>.

> Serve it over HTTP. Opening `index.html` straight off the filesystem gives it
> an opaque `null` origin, which the browser will not let you POST from.

---

## Wiring it to your flow

1. In Copilot Studio, open the flow and click the
   **When a HTTP request is received** trigger.
2. Copy the **HTTP POST URL** from the bottom of the panel.
3. Paste it into **Lab configuration → HTTP POST URL** on the web page.

The URL is remembered in `localStorage`, so learners paste it once per browser.

The status line under the box validates the URL as you type:

| Message | Meaning |
|---|---|
| No HTTP POST URL set | Field is empty |
| The URL must start with https:// | Wrong scheme |
| This does not look like a Power Platform HTTP trigger URL | Missing `triggers/manual/paths/invoke` |
| URL is missing its `sig=` signature | The URL was truncated on copy |
| **HTTP POST URL detected** | Good — flow must be **published** |

---

## The publish trap

The HTTP endpoint serves the **published** version of the flow. Saving is not
enough. After any edit you must click **Publish**.

Symptom: you change something, resubmit the form, and the old behaviour comes
back. Confirm with **⋯ → Version history** — if `LIVE` and `CURRENT DRAFT` are
different version numbers, you have an unpublished draft.

---

## What the page expects back

`script.js` calls `response.json()` and reads:

```json
{
  "applicationId": "APP-20260801-1042",
  "decision": "APPROVED",
  "reason": "One or two sentences explaining the outcome.",
  "riskFlags": []
}
```

`decision` is one of `APPROVED`, `REJECTED`, `DUPLICATE`, `REVIEW`.

Until the flow returns that shape, the results panel falls back to
*"We could not read the decision"* — which is the correct behaviour for a flow
that only returns `{"status":"ok"}`.

---

## Trainer demo data

The **Trainer demo data** dropdown fills the form for ten cases, one per rule
path:

| Case | Expected |
|---|---|
| TC1 Happy path | APPROVED |
| TC2 Existing customer | DUPLICATE |
| TC3 Income too low for Fixed Deposit | REJECTED |
| TC4 Not employed, wants Current | REJECTED |
| TC5 Messy casing and spacing | APPROVED |
| TC6 Politically Exposed Person | REVIEW |
| TC7 Under 18 | REJECTED |
| TC8 Deposit below minimum | REJECTED |
| TC9 Foreign tax resident | REVIEW |
| TC10 Under 18 **and** a PEP | REJECTED — age fires first |

TC5 is the one worth demonstrating: it submits `tan wei ming` / `s8412345d` in
mixed case. If the flow's normalise step is missing, the duplicate check will
not match the `Customers` register and TC5 silently returns the wrong decision.

TC10 proves the rules are **ordered** — two rules apply, and only the first
one fires.

The demo autofill deliberately leaves **email blank**. The flow may send a real
message to whatever address is entered.

---

## Verified end to end on 2026-08-01

Against the **NUS Copilot (Developer)** environment, flow `Response`
(trigger → SharePoint lookup → Agent → email → Response):

**Through the website form**

| Submitted | Result panel |
|---|---|
| TC1 `S9512345F`, Savings, deposit 1000 | ✓ **Application approved** |
| `s9123456q` lowercase (Elena Petrova) | ! **You are already a customer** |

The second case is the important one: that NRIC exists **only in the SharePoint
`Customers` list**, and was submitted in lowercase. It proves the duplicate
check is a live list query, not a hardcoded list, and that the `toUpper()`
normalisation in the filter works.

**Direct against the endpoint** — 8 of 8 rule paths correct:

| Case | Decision | Flags |
|---|---|---|
| `S8412345D` | DUPLICATE | |
| `s8412345d` lowercase | DUPLICATE | |
| `S9123456Q` Elena — SharePoint only | DUPLICATE | |
| `S9078234B` — SharePoint only | DUPLICATE | |
| New applicant | APPROVED | |
| Under 18 | REJECTED | `MINOR` |
| PEP | REVIEW | `PEP` |
| Current + unemployed | REJECTED | |
| Deposit below minimum | REJECTED | |

**No CORS block.** The browser POSTs cross-origin to
`*.environment.api.powerplatform.com` and gets a normal response.

**Latency ~20s per submission** once the SharePoint lookup is in the chain.

### Bug fixed during testing

The form failed with `HTTP 400 TriggerInputSchemaMismatch`:

```
Expected Number but got String    (annualIncome, initialDeposit)
Expected Boolean but got String   (pep, foreignTaxResident)
```

HTML controls always yield strings. `script.js` now casts all four before POSTing — see the comment there.

### The confirmation email

The flow order is:

```
Trigger → Get_customer_by_NRIC → Agent → Response → Send an email
```

Response comes **before** the email so the applicant sees their decision even
if mail delivery fails.

Two things cost several hours to work out, both worth knowing before class:

**The To field needs the ⚡ picker, not a typed expression.** Every typed form
— `@{triggerBody()?['email']}`, `toLower(trim(...))`, `triggerOutputs()`, the
bare `@` form, even a `split()` to strip newlines — fails at run time with:

```
Input parameter 'emailMessage/To' is required to be of type 'String/email'.
The runtime value '"applicant@example.com\n"' ... doesn't have the expected
format 'string/email'.
```

The trailing `\n` is added somewhere between the trigger and the connector. A
**picker-inserted token carries the same value without it**. A hardcoded
literal address also works.

**A 200 does not mean the email sent.** Once Response runs first, anything
after it can fail invisibly — and a node left in "Needs setup" is skipped
silently. Judge success from the **Activity** tab, not the HTTP status.

### Still to add

`Create item` actions writing to `Customers` (on APPROVED) and to
`OnboardingLog` (every decision). Until those exist, an approved applicant is
not added to the register, so resubmitting the same NRIC still returns
APPROVED.
