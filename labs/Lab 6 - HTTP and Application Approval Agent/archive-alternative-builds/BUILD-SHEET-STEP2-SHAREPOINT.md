# Build sheet — Step 2: SharePoint as the customer register

Replaces the hardcoded NRIC list in the agent's instructions with a live
SharePoint lookup, and writes records back.

**Current flow (working):**

```
Trigger → Agent → Send an email → Response
```

**Target flow:**

```
Trigger
  → Get_customer_by_NRIC     (SharePoint, NEW)
  → Agent                    (instructions edited)
  → Condition: APPROVED?     (NEW)
      yes → Create_customer_record  (SharePoint, NEW)
  → Write_audit_log          (SharePoint, NEW)
  → Send an email            (unchanged)
  → Response                 (unchanged)
```

Site: `https://YOURTENANT.sharepoint.com/sites/MarinaTrustBankOnboarding`

---

## Action A — Get_customer_by_NRIC

Insert **between the trigger and the Agent**.

**Connector → SharePoint → Get items**. Rename it `Get_customer_by_NRIC`.

| Field | Value |
|---|---|
| Site Address | `https://YOURTENANT.sharepoint.com/sites/MarinaTrustBankOnboarding` |
| List Name | `Customers` |
| Filter Query | see below |
| Top Count | `1` |

**Filter Query** — switch the field to code mode (`</>`) and paste:

```
@{concat('NRIC eq ''', toUpper(trim(triggerBody()?['nric'])), '''')}
```

Those are **three single quotes** in a row, twice. OData needs the value quoted,
and a literal `'` inside a Power Automate string is escaped by doubling it. The
expression produces `NRIC eq 'S8412345D'`.

`toUpper(trim(...))` is what makes the lowercase test case work.

---

## Action B — edit the Agent instructions

**Delete** this block:

```
## Known existing customers (NRIC)
S8412345D, S9078234B, S7623451A, T0145678C, S6534129E
```

**Replace** STEP 1 with:

```
STEP 1 - DUPLICATE CHECK (always first)
The application below includes a field "Existing customer found".
If it is true, the applicant is an existing customer:
decision = "DUPLICATE", riskFlags = []. Stop.
```

**Add** this line to the `## Application to process` block, just under
`Application ID`:

```
Existing customer found: @{greater(length(body('Get_customer_by_NRIC')?['value']), 0)}
```

`length(...)` counts the rows returned by the lookup; `greater(..., 0)` turns
that into true/false.

---

## Action C — Condition: APPROVED?

Insert **after the Agent**.

**If/Else**. Rename it `If_approved`.

Condition — left side (code mode):

```
@{body('Agent')?['structuredOutput/decision']}
```

Operator: **is equal to**  ·  Right side: `APPROVED`

Leave the **else** branch empty. Rejected, duplicate and review applications
must not create a customer record.

---

## Action D — Create_customer_record

Inside the **yes** branch of `If_approved`.

**Connector → SharePoint → Create item**. Rename it `Create_customer_record`.

| Field | Value |
|---|---|
| Site Address | same site |
| List Name | `Customers` |

Then the columns (code mode for each):

| Column | Value |
|---|---|
| Title | `@{toUpper(trim(triggerBody()?['nric']))}` |
| NRIC | `@{toUpper(trim(triggerBody()?['nric']))}` |
| Full Name | `@{toUpper(trim(triggerBody()?['fullName']))}` |
| Date of Birth | `@{triggerBody()?['dateOfBirth']}` |
| Email | `@{toLower(trim(triggerBody()?['email']))}` |
| Account Type | `@{triggerBody()?['accountType']}` |
| Annual Income | `@{triggerBody()?['annualIncome']}` |
| Onboarded On | `@{utcNow()}` |

> **Title is mandatory.** SharePoint rejects the create if it is empty, and the
> error message does not make that obvious. Setting it to the NRIC keeps the
> list readable.

---

## Action E — Write_audit_log

**After** the If/Else — outside both branches, so it runs for every decision.

**Connector → SharePoint → Create item**. Rename it `Write_audit_log`.

| Field | Value |
|---|---|
| Site Address | same site |
| List Name | `OnboardingLog` |

| Column | Value |
|---|---|
| Title | `@{body('Agent')?['structuredOutput/applicationId']}` |
| Timestamp | `@{utcNow()}` |
| Application ID | `@{body('Agent')?['structuredOutput/applicationId']}` |
| NRIC | `@{toUpper(trim(triggerBody()?['nric']))}` |
| Account Type | `@{triggerBody()?['accountType']}` |
| Decision | `@{body('Agent')?['structuredOutput/decision']}` |
| Reason | `@{body('Agent')?['structuredOutput/reason']}` |

`Decision` accepts `APPROVED / REJECTED / DUPLICATE / REVIEW` — the `REVIEW`
choice was added on 2026-08-01, so the PEP path will not fail.

---

## Then Publish

Publish, not save. Check **⋯ → Version history**: `LIVE` and `CURRENT DRAFT`
must show the same version.

---

## What changes about the lab


- `Customers` already holds 15 records, seeded from `customers.csv`
- An APPROVED applicant is **added** to the register, so resubmitting the same
  NRIC returns DUPLICATE the second time — a good thing to demonstrate in class
- Every decision writes an audit row, which is the requirement in
  `Onboarding-Service-Standards.txt` (MTB-STD-003)

---

## Tests I will run afterwards

| Case | NRIC | Expect |
|---|---|---|
| Existing customer | `S8412345D` | DUPLICATE — from the list, not the prompt |
| Lowercase | `s8412345d` | DUPLICATE — proves `toUpper` in the filter |
| New applicant | `S9512345F` | APPROVED **and** a new row in `Customers` |
| Resubmit the same | `S9512345F` | DUPLICATE — proves the write took effect |
| PEP | any | REVIEW, `OnboardingLog` row, no customer row |
