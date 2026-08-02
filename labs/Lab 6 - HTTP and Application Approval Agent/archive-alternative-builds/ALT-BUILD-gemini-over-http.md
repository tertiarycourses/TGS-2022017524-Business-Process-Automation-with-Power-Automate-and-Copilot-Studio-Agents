# Module 4 Lab 6 — Power Automate + Gemini hybrid build

> **Fastest path: import the package.** Run `./build-package.sh` and import the
> resulting `Module 4-Activity1-MarinaTrust-PowerAutomate.zip` at
> make.powerautomate.com → **My flows → Import → Import Package**. The manual
> steps below document what the package contains, for teaching and for repair.
>
> Verified against the live Gemini API on 2026-08-01: all 9 rule paths
> (duplicate, minor, PEP, source-of-funds, employment, income, deposit,
> approval, student) return the correct decision and risk flags.


The AI decision step calls the **Gemini API over HTTP**, which is the same model
 Gemini's free tier covers a
classroom comfortably.

|---|---|---|
| Trigger | Webhook node | When a HTTP request is received |
| AI | Gemini via Agent node | Gemini via HTTP action |
| Duplicate check | Google Sheets tool | SharePoint — Get items |
| Customer store | Google Sheets | SharePoint list `Customers` |
| Audit log | Google Sheets | SharePoint list `OnboardingLog` |
| Email | Gmail tool | Outlook — Send an email |
| Response | Respond to Webhook | Response action |

---

## Prerequisites

1. **Gemini API key** — https://aistudio.google.com/apikey (free, no billing card)
2. **SharePoint site** — https://YOURTENANT.sharepoint.com/sites/MarinaTrustBankOnboarding
   with lists `Customers` and `OnboardingLog` (already built)
3. Power Automate access at https://make.powerautomate.com

> **Never paste the API key into chat, a screenshot, or the repo.**
> Type it directly into the HTTP action, or store it in Azure Key Vault.

---

## Step 1 — Create the flow

make.powerautomate.com → **Create** → **Instant cloud flow**
→ name it `Module 4 Marina Trust Onboarding`
→ trigger: **When a HTTP request is received**

### Request Body JSON Schema

```json
{
  "type": "object",
  "properties": {
    "fullName": { "type": "string" },
    "nric": { "type": "string" },
    "dateOfBirth": { "type": "string" },
    "nationality": { "type": "string" },
    "residencyStatus": { "type": "string" },
    "email": { "type": "string" },
    "mobile": { "type": "string" },
    "address": { "type": "string" },
    "postalCode": { "type": "string" },
    "accountType": { "type": "string" },
    "employmentStatus": { "type": "string" },
    "occupation": { "type": "string" },
    "employer": { "type": "string" },
    "annualIncome": { "type": "number" },
    "sourceOfFunds": { "type": "string" },
    "purposeOfAccount": { "type": "string" },
    "initialDeposit": { "type": "number" },
    "pep": { "type": "boolean" },
    "foreignTaxResident": { "type": "boolean" }
  },
  "required": ["fullName", "nric", "dateOfBirth", "accountType",
               "employmentStatus", "annualIncome", "initialDeposit"]
}
```

Set **Who can trigger** → *Anyone* (Settings on the trigger). The website posts

---

## Step 2 — Normalise (Compose actions)

 Without it the duplicate check misses,
because `s8412345d` will not match `S8412345D`.

Add one **Compose** per value:

| Name | Expression |
|---|---|
| `nric` | `toUpper(trim(triggerBody()?['nric']))` |
| `fullName` | `toUpper(trim(triggerBody()?['fullName']))` |
| `email` | `toLower(trim(triggerBody()?['email']))` |
| `applicationId` | `concat('APP-', formatDateTime(utcNow(),'yyyyMMdd'), '-', rand(1000,9999))` |
| `age` | `div(div(div(div(sub(ticks(utcNow()), ticks(triggerBody()?['dateOfBirth'])), 10000000), 60), 60), 24)` then `div(..., 365)` |

Simpler `age` alternative — one Compose:

```
div(sub(ticks(utcNow()), ticks(triggerBody()?['dateOfBirth'])), 315360000000000)
```

---

## Step 3 — Duplicate check (SharePoint — Get items)

- **Site Address:** `https://YOURTENANT.sharepoint.com/sites/MarinaTrustBankOnboarding`
- **List Name:** `Customers`
- **Filter Query:** `NRIC eq '<outputs of the nric Compose>'`
- **Top Count:** `1`

---

## Step 4 — Gemini decision (HTTP action)

- **Method:** POST
- **URI:**
  `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=YOUR_API_KEY`

> `gemini-2.0-flash` and `gemini-2.5-flash` return
> *"no longer available to new users"* (HTTP 404) on keys issued recently.
> Use `gemini-3.6-flash`.
- **Headers:** `Content-Type: application/json`
- **Body:** see `gemini-request-body.json` in this folder.

`responseMimeType: application/json` plus `responseSchema` forces Gemini to

`Decision Parser` node.

---

## Step 5 — Parse the response (Parse JSON)

**Content:**

```
body('HTTP')?['candidates'][0]?['content']?['parts'][0]?['text']
```

Gemini returns the JSON as a *string* inside `parts[0].text`, so it must be
parsed before the fields are usable.

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

## Step 6 — Branch on the decision (Condition)

Condition: `body('Parse_JSON')?['decision']` **is equal to** `APPROVED`

### If yes — SharePoint Create item in `Customers`

| Field | Value |
|---|---|
| Title | the normalised `nric` (**required** — the call fails if empty) |
| NRIC | normalised `nric` |
| FullName | normalised `fullName` |
| DateOfBirth | `triggerBody()?['dateOfBirth']` |
| Email | normalised `email` |
| AccountType | `triggerBody()?['accountType']` |
| AnnualIncome | `triggerBody()?['annualIncome']` |
| OnboardedOn | `utcNow()` |

### If no — no customer record

Rejected, duplicate and review applications must **not** create a customer row.

---

## Step 7 — Audit log (runs on BOTH branches)

SharePoint **Create item** in `OnboardingLog`:

| Field | Value |
|---|---|
| Title | `applicationId` |
| Timestamp | `utcNow()` |
| ApplicationID | `applicationId` |
| NRIC | normalised `nric` |
| AccountType | `triggerBody()?['accountType']` |
| Decision | `body('Parse_JSON')?['decision']` |
| Reason | `body('Parse_JSON')?['reason']` |

`OnboardingLog.Decision` accepts `APPROVED / REJECTED / DUPLICATE / REVIEW`.
`REVIEW` was added on 2026-08-01 — the KYC step (Step 3) emits it, and the
SharePoint write fails without it.

---

## Step 8 — Email (Outlook — Send an email V2)

- **To:** normalised `email`
- **Subject:** `Your Marina Trust Bank application <applicationId>`
- **Body:** `body('Parse_JSON')?['reason']`

 Place this after the branches
rejoin so it fires once, not twice.

---

## Step 9 — Response

- **Status Code:** `200`
- **Headers:** `Content-Type: application/json`
- **Body:** `body('Parse_JSON')`

`script.js` calls `response.json()` and reads `decision`, `reason`, `riskFlags`,
so the shape must match.

---

## Step 10 — Wire up the website

Save the flow, copy the **HTTP POST URL** from the trigger, and paste it into the
**Lab configuration** panel on `index.html`. No file edit needed — the page stores
it in `localStorage`.

---

## Test cases

| NRIC | Expected | Rule |
|---|---|---|
| `S8412345D` | DUPLICATE | Step 1 — already in `Customers` |
| any, DOB 2010-01-01 | REJECTED | Step 2 — under 18 |
| any, `pep: true` | REVIEW | Step 3 — KYC flag |
| any, Current + Unemployed | REJECTED | Step 4 — not gainfully employed |
| any, Savings + deposit 200 | REJECTED | Step 5 — below SGD 500 |
| `S9556123X`, Savings, 2500 | APPROVED | Step 6 |

Send lowercase `nric` in at least one test — it proves Step 2 normalisation works.

---
