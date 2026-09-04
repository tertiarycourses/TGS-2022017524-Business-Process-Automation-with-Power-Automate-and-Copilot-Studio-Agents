# Build sheet — Step 1: decision + email + response

Environment: the learner's **Training Class** Sandbox (for example **Training Class 1**)
Flow: **Response** (the existing one — trigger and Response node are already there)

Goal: the website form produces a **real approve/reject decision**, emails it to
you, and renders it on the results panel. No SharePoint yet — that is Step 2.

You will add **3 actions** between the existing trigger and the existing
Response node.

---

## Before you start

The trigger is already configured correctly — leave it alone:

- Who can trigger: **Anyone (no authentication)**
- Relative path: **blank** (a value here breaks Publish)
- Request body JSON schema: already has the 19 fields

---

## Action 1 — Compose: age

Click the **+** between the trigger and Response → **Function** → **Data
Operations** → **Compose**.

Rename it to **Compose_age** (click the title to rename — the name matters,
later actions reference it).

**Inputs** — paste this expression:

```
div(sub(ticks(utcNow()), ticks(triggerBody()?['dateOfBirth'])), 315360000000000)
```

That gives whole years between the applicant's date of birth and now. The agent
needs it for the age rule; it cannot reliably do date arithmetic itself.

---

## Action 2 — Agent

Click the **+** below Compose_age → **Agent**.

### Instructions

Paste the whole block below.

```
You are the Customer Onboarding Assistant for a Singapore retail bank (Marina
Trust Bank). You process new account applications and must follow the bank's
onboarding rules exactly, in the order given.

## Definitions
- "Gainfully employed" means Employment Status is one of: Employed,
  Self-Employed, Contract, Part-Time.
- Every other status (Student, National Service, Homemaker, Retired,
  Unemployed) is NOT gainfully employed.
- "High-risk source of funds" means Source of Funds is one of: Gift or
  Inheritance, Cryptocurrency Proceeds, Other.

## Known existing customers (NRIC)
S8412345D, S9078234B, S7623451A, T0145678C, S6534129E

## Onboarding rules - evaluate in this order and STOP at the first rule that fires

STEP 1 - DUPLICATE CHECK (always first)
If the applicant's NRIC appears in the Known existing customers list above:
  decision = "DUPLICATE", riskFlags = []. Stop.

STEP 2 - AGE
If Age is below 18:
  decision = "REJECTED", riskFlags = ["MINOR"]. Stop.

STEP 3 - KYC / AML SCREENING
Raise a flag for each of these that is true:
  - PEP is true                             -> flag "PEP"
  - Tax Resident Outside Singapore is true  -> flag "CRS_FATCA"
  - Source of Funds is high-risk            -> flag "SOURCE_OF_FUNDS"
If one or more flags were raised:
  decision = "REVIEW", riskFlags = the flags raised. Stop.

STEP 4 - ACCOUNT ELIGIBILITY
Apply only the rule for the account type actually requested:
  - Savings          - no income or employment requirement.
  - Joint Savings    - no income or employment requirement.
  - Student Account  - Employment Status must be exactly "Student".
  - Current          - applicant must be gainfully employed.
  - Fixed Deposit    - Annual Income must be at least SGD 30,000.
  - Multi-Currency   - Annual Income at least SGD 60,000 AND gainfully employed.
If the applicant fails this rule:
  decision = "REJECTED", riskFlags = []. Name the exact criterion not met and
  suggest a Savings account instead. Stop.

STEP 5 - MINIMUM INITIAL DEPOSIT
  Savings SGD 500 | Joint Savings SGD 1,000 | Student Account SGD 0 |
  Current SGD 3,000 | Fixed Deposit SGD 10,000 | Multi-Currency SGD 5,000
If Initial Deposit is below the minimum for the requested account type:
  decision = "REJECTED", riskFlags = []. State the minimum for that account
  type and invite them to reapply. Stop.

STEP 6 - APPROVAL
decision = "APPROVED", riskFlags = [].

## Constraints
- Never invent an NRIC, email address, income figure or deposit amount.
- Judge the applicant only against the rule for the account type they asked
  for. Never approve them into a different account type.
- 'reason' is one or two plain-English sentences stating the decision and the
  exact reason for it. Write as a Singapore bank writes: courteous, factual.
  No exclamation marks, no marketing language, no emoji.
- Never put the NRIC in the reason text.

## Output
Return ONLY a JSON object with exactly these keys:
  applicationId, decision, reason, riskFlags
'decision' is one of "APPROVED", "REJECTED", "DUPLICATE", "REVIEW".
'riskFlags' is an array of strings (empty when none).
Return raw JSON only - no markdown fences, no commentary.
```

### User message / input

Paste this. The `@{...}` parts pull from the form submission — if the designer
offers a dynamic-content picker instead, use it to select the same fields.

```
New customer onboarding application received.

Application ID: APP-@{formatDateTime(utcNow(),'yyyyMMddHHmmss')}
Full Name: @{toUpper(trim(triggerBody()?['fullName']))}
NRIC: @{toUpper(trim(triggerBody()?['nric']))}
Date of Birth: @{triggerBody()?['dateOfBirth']}
Age: @{outputs('Compose_age')}
Nationality: @{triggerBody()?['nationality']}
Residency Status: @{triggerBody()?['residencyStatus']}
Email: @{toLower(trim(triggerBody()?['email']))}
Account Type: @{triggerBody()?['accountType']}
Employment Status: @{triggerBody()?['employmentStatus']}
Occupation: @{triggerBody()?['occupation']}
Annual Income (SGD): @{triggerBody()?['annualIncome']}
Source of Funds: @{triggerBody()?['sourceOfFunds']}
Initial Deposit (SGD): @{triggerBody()?['initialDeposit']}
PEP: @{triggerBody()?['pep']}
Tax Resident Outside Singapore: @{triggerBody()?['foreignTaxResident']}

Process this application and return the decision JSON.
```

> The uppercase/lowercase wrapping is the normalisation step. It matters: TC5
> submits `s8412345d` in lowercase, and without `toUpper` the duplicate rule
> will not match `S8412345D` in the known-customers list.

---

## Action 3 — Parse JSON

Click the **+** below the Agent → **Function** → **Data Operations** →
**Parse JSON**. Rename it **Parse_decision**.

**Content:** the Agent's output. Use the dynamic-content picker and choose the
agent's text/output field. If you have to type it, it will look like:

```
@{outputs('Agent')?['body/text']}
```

**Schema:**

```json
{
  "type": "object",
  "properties": {
    "applicationId": { "type": "string" },
    "decision": { "type": "string" },
    "reason": { "type": "string" },
    "riskFlags": { "type": "array", "items": { "type": "string" } }
  }
}
```

---

## Action 4 — Send an email (V2)

Click the **+** below Parse_decision → **Connector** → **Office 365 Outlook** →
**Send an email (V2)**.

| Field | Value |
|---|---|
| To | `onboarding@marinatrust.example` |
| Subject | `Marina Trust Bank - @{body('Parse_decision')?['decision']}` |
| Body | see below |

Body:

```
Decision: @{body('Parse_decision')?['decision']}

Reason: @{body('Parse_decision')?['reason']}

Risk flags: @{join(body('Parse_decision')?['riskFlags'], ', ')}

Applicant: @{toUpper(trim(triggerBody()?['fullName']))}
Account type: @{triggerBody()?['accountType']}
Annual income: SGD @{triggerBody()?['annualIncome']}
Initial deposit: SGD @{triggerBody()?['initialDeposit']}
Age: @{outputs('Compose_age')}

Training lab - Marina Trust Bank is fictitious and all applicant data is mock data.
```

---

## Action 5 — Update the existing Response node

Do **not** add a new one. Open the Response node already at the end.

| Field | Value |
|---|---|
| Status Code | `200` (unchanged) |
| Headers | `Content-Type` : `application/json` (already set) |
| Body | **change** from `{ "status": "ok" }` to: `@{body('Parse_decision')}` |

That is what makes the decision appear on the website results panel.

---

## Finally — PUBLISH

Click **Publish**, not just save. The HTTP endpoint serves the *published*
version.

Check **⋯ → Version history**: `LIVE` and `CURRENT DRAFT` should be the same
version number. If they differ, the publish did not take.

---

## Then tell me

Send me the HTTP POST URL (it will not have changed unless the flow was
recreated) and I will:

1. Submit TC1 through the website with Playwright — expect **APPROVED**
2. Submit TC2 (`S8412345D`) — expect **DUPLICATE**
3. Submit TC5 (lowercase `s8412345d`) — expect **DUPLICATE**, proving normalisation
4. Submit TC7 (under 18) — expect **REJECTED** with `MINOR`
5. Confirm the decision renders on the results panel
6. Confirm the emails arrive

---

## Step 2 (after this works)

Add SharePoint — both connectors are now live in this environment:

- **Get items** on `Customers` filtered by NRIC, replacing the hardcoded list
- **Create item** in `Customers` when APPROVED
- **Create item** in `OnboardingLog` for every decision
