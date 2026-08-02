# Lab 6 — HTTP and Application Approval Agent

*Marina Trust Bank customer onboarding · Copilot Studio agent flow build guide*

Everything in this guide has been built and tested end to end. Every expression
and prompt below can be copied and pasted directly into the node configuration.

## Workflow visual

![Lab 6 application approval agent workflow](assets/flowchart.png)

A public web form posts to the HTTP trigger; Compose normalises the input, SharePoint checks for a
duplicate, the Agent node applies the six ordered rules and returns structured output, and the
Condition branches on the decision before the Response goes back to the page.

**Scenario.** Marina Trust Bank (fictitious) takes new-account applications on
paper. Staff key them into a spreadsheet by hand. Applications sit in a queue
for days, the same customer ends up with two records under slightly different
spellings, and eligibility rules printed in a binder get applied differently by
different officers.

**What you build.** A public web form that posts to a Copilot Studio agent flow.
The flow checks the applicant against the bank's customer register, asks an AI
agent to apply six ordered eligibility rules, emails the decision to the
onboarding team, and returns the decision to the website — in about twenty
seconds, with no human involved.

---

# Part 0 — What you need before you start

| Requirement | Notes |
|---|---|
| Microsoft 365 account | With SharePoint and Outlook |
| Power Platform environment | Must have **Copilot Credits** — see below |
| Copilot Studio access | make.powerautomate.com / copilotstudio.microsoft.com |

> ### The Copilot Credits trap
>
> Agent flows consume **Copilot Credits** on every run. Many Default
> environments have none allocated, and the flow fails with:
>
> ```
> {"error":{"code":"InsufficientMcsCredits","message":"The environment
> '...' does not have sufficient Copilot Credits to run workflows."}}
> ```
>
> This is an environment capacity issue, not a flow problem. A
> **Developer environment** (free to create) usually has its own allocation.
> Check before class: build a two-node flow (trigger → Response) and `curl` it.
> If you get `InsufficientMcsCredits`, switch environments.
>
> Assigning a Copilot Studio *licence* to your user does **not** fix this —
> licences are per-user, credits are per-environment.

---

# Part 1 — Create the SharePoint site

The customer register lives in SharePoint. SharePoint is **tenant-level**, not
tied to a Power Platform environment, so the same site works from any
environment.

### 1.1 Create the site

1. Go to <https://YOURTENANT.sharepoint.com>
2. **+ Create site** → **Team site**
3. Template: **Standard team**
4. Site name: `Marina Trust Bank Onboarding`
5. Accept the generated address —
   `.../sites/MarinaTrustBankOnboarding`
6. Privacy: **Private**
7. Skip adding members → **Finish**

Site provisioning takes about 30 seconds.

### 1.2 Create the `Customers` list

**Site contents** → **New** → **List** → **Blank list** → name it `Customers`.

Then add these columns. **Type the names exactly as shown** — SharePoint fixes
the internal name at creation, and renaming later leaves the internal name
stale, which silently breaks the flow bindings.

| Column name | Type | Settings |
|---|---|---|
| NRIC | Single line of text | Max 20, **Required** |
| Full Name | Single line of text | Max 255 |
| Date of Birth | Date and time | Date only |
| Email | Single line of text | Max 255 |
| Account Type | Choice | Savings · Current · Fixed Deposit · Student Account |
| Annual Income | Number | 2 decimals |
| Onboarded On | Date and time | Date only |

> `Title` already exists and **cannot be removed**. It is mandatory on every
> SharePoint list item. The flow sets it to the NRIC — if you leave it empty,
> the Create item action fails with an unhelpful error.

### 1.3 Create the `OnboardingLog` list

Same steps, named `OnboardingLog`:

| Column name | Type | Settings |
|---|---|---|
| Timestamp | Date and time | Date and time |
| Application ID | Single line of text | Max 50 |
| NRIC | Single line of text | Max 20 |
| Account Type | Choice | Savings · Current · Fixed Deposit · Student Account |
| Decision | Choice | APPROVED · REJECTED · DUPLICATE · **REVIEW** |
| Reason | Multiple lines of text | Plain text, 4 lines |

> **Do not omit `REVIEW`.** Rule 3 (KYC/AML) produces it for any PEP or
> high-risk source of funds. Without the choice value, the audit write fails on
> exactly the applications you most need logged.

### 1.4 Show the columns in the list view

Newly created columns are **not** in the default view. The list will look empty
even though the data is there.

For each list: open it → the view dropdown (**All Items**) → **Edit current
view** → tick every column you created → **OK**.

### 1.5 Load the customer data

`customers.csv` in this folder holds five starter customers:

```csv
NRIC,Full Name,Date of Birth,Email,Account Type,Annual Income,Onboarded On
S8412345D,TAN WEI MING,1984-07-02,tanweiming@example.com,Savings,72000,2024-03-11
S9078234B,NURUL AISYAH BINTE RAHMAN,1990-11-15,nurul.aisyah@example.com,Current,95000,2024-07-02
S7623451A,RAJESH KUMAR,1976-04-08,rajesh.kumar@example.com,Fixed Deposit,120000,2025-01-19
T0145678C,CHLOE LIM HUI LING,2001-09-23,chloe.lim@example.com,Student Account,0,2025-05-28
S6534129E,GOH BEE CHOO,1965-02-11,goh.beechoo@example.com,Savings,18000,2023-11-04
```

**Option A — Edit in grid view (fastest).**
Open `Customers` → **Edit in grid view** → paste the rows straight from Excel or
the CSV. Set **Title** to the NRIC for each row.

**Option B — one at a time.**
**+ New** for each customer. Slower, but shows learners the column structure.

**Option C — Import from Excel.**
Save the CSV as `.xlsx`, format as a Table, then **Site contents → New → List →
From Excel**. Watch the column types: SharePoint often guesses text for dates
and numbers, and `Annual Income` must be a Number for the income rules to work.

Whichever route, confirm afterwards: `Customers` shows **5 items**, and
`Title` is populated on every row.

---

# Part 2 — Create the flow

Copilot Studio → **Flows** → **+ New agent flow**. Name it
`Module 4 Marina Trust Onboarding`.

You will build **five nodes**:

```
When a HTTP request is received     ← the webhook
  → Get_customer_by_NRIC            ← SharePoint duplicate lookup
  → Agent                           ← six ordered rules, AI decision
  → Response                        ← return the decision to the website
  → Send an email                   ← confirmation to the applicant
```

> **Why Response comes before the email.** The applicant sees the decision the
> moment the agent has made it. If the email step later fails, the website has
> already received its answer. Coupling the user's response to a side effect
> means one flaky mail server takes down the whole experience.

---

## Node 1 — When a HTTP request is received

This is the trigger. It gives the flow a public URL that any website can POST
to.

**Trigger type:** `When a HTTP request is received`

| Field | Value |
|---|---|
| Allowed HTTP method | `POST` |
| Who can trigger the flow? | **Anyone (no authentication)** |
| Relative path | **leave blank** |

> ### Two things that will stop you
>
> **Relative path must be empty.** Typing a path like
> `marina-trust-onboarding` causes Publish to fail with:
> *"The value ... provided in property 'inputs.relativePath' ... is not valid."*
> The field expects parameter placeholders, not a static route segment.
>
> **"Anyone" vs "Any user in my tenant".** With the tenant option, a plain
> browser POST returns 401 and learners will think the flow is broken. Choose
> URL itself the only credential — regenerate or delete the flow after class.

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

> **The trigger validates this schema strictly.** `annualIncome` and
> `initialDeposit` must arrive as JSON numbers, `pep` and `foreignTaxResident`
> as JSON booleans. HTML form controls always produce strings, so the website
> must cast them before sending, or every submission fails with:
>
> ```
> TriggerInputSchemaMismatch — Invalid type. Expected Number but got String.
> ```
>

**The HTTP POST URL appears only after you save**, at the bottom of this panel.

---

## Node 2 — Get_customer_by_NRIC

The duplicate check.
`check_duplicate_customer` Google Sheets tool.

**Connector → SharePoint → Get items**, renamed to `Get_customer_by_NRIC`.

| Field | Value |
|---|---|
| Site Address | `https://YOURTENANT.sharepoint.com/sites/MarinaTrustBankOnboarding` |
| List Name | `Customers` |
| Filter Query | see below |
| Top Count | `1` |

**Filter Query** — type the literal text, then insert the expression where shown:

```
NRIC eq '<expression>'
```

The expression, added via the ⚡ token picker or `fx`:

```
toUpper(trim(triggerBody()?['nric']))
```

The finished field reads `NRIC eq '` + a `toUpper` chip + `'`. At runtime it
becomes `NRIC eq 'S8412345D'`.

> ### Do not use concat() here
>
> This looks like it should work and does not:
>
> ```
> concat('NRIC eq ''', toUpper(trim(triggerBody()?['nric'])), '''')
> ```
>
> It validates in the editor and then fails at runtime with
> *"The expression ... is not valid. Creating query failed."* The escaped-quote
> form is rejected by this field. Use the literal-text-plus-token form above.
>
> `toUpper(trim(...))` is not decoration. Without it, an applicant who types
> `s8412345d` in lowercase will not match `S8412345D` in the register, and the
> duplicate check silently passes.

---

## Node 3 — Agent

The decision engine. Add an **Agent** node, create its connection when prompted,
and choose a model (Claude Sonnet 4.6 was used for this build).

> The Agent node has **no separate user-input field**. The application data goes
> at the bottom of the Instructions, after the rules.

### Instructions — copy the whole block

```
You are the Customer Onboarding Assistant for a Singapore retail bank (Marina Trust Bank). You process new account applications and must follow the bank's onboarding rules exactly, in the order given.

## Definitions
- "Gainfully employed" means Employment Status is one of: Employed, Self-Employed, Contract, Part-Time.
- Every other status (Student, National Service, Homemaker, Retired, Unemployed) is NOT gainfully employed.
- "High-risk source of funds" means Source of Funds is one of: Gift or Inheritance, Cryptocurrency Proceeds, Other.

## Onboarding rules - evaluate in this order and STOP at the first rule that fires

STEP 1 - DUPLICATE CHECK (always first)
The application below includes a field "Existing customer found". This is the result of a live lookup against the bank's Customers register.
If it is true, the applicant is an existing customer:
decision = "DUPLICATE", riskFlags = []. Stop.

STEP 2 - AGE
If Age is below 18:
decision = "REJECTED", riskFlags = ["MINOR"]. Stop.

STEP 3 - KYC / AML SCREENING
Raise a flag for each of these that is true:
- PEP is true -> flag "PEP"
- Tax Resident Outside Singapore is true -> flag "CRS_FATCA"
- Source of Funds is high-risk -> flag "SOURCE_OF_FUNDS"
If one or more flags were raised:
decision = "REVIEW", riskFlags = the flags raised. Stop.

STEP 4 - ACCOUNT ELIGIBILITY
Apply only the rule for the account type actually requested:
- Savings - no income or employment requirement.
- Joint Savings - no income or employment requirement.
- Student Account - Employment Status must be exactly "Student".
- Current - applicant must be gainfully employed.
- Fixed Deposit - Annual Income must be at least SGD 30,000.
- Multi-Currency - Annual Income at least SGD 60,000 AND gainfully employed.
If the applicant fails this rule:
decision = "REJECTED", riskFlags = []. Name the exact criterion not met and suggest a Savings account instead. Stop.

STEP 5 - MINIMUM INITIAL DEPOSIT
Savings SGD 500 | Joint Savings SGD 1,000 | Student Account SGD 0 | Current SGD 3,000 | Fixed Deposit SGD 10,000 | Multi-Currency SGD 5,000
If Initial Deposit is below the minimum for the requested account type:
decision = "REJECTED", riskFlags = []. State the minimum for that account type and invite them to reapply. Stop.

STEP 6 - APPROVAL
decision = "APPROVED", riskFlags = [].

## Constraints
- Never invent an NRIC, email address, income figure or deposit amount.
- Judge the applicant only against the rule for the account type they asked for. Never approve them into a different account type.
- 'reason' is one or two plain-English sentences stating the decision and the exact reason for it. Write as a Singapore bank writes: courteous, factual. No exclamation marks, no marketing language, no emoji.
- Never put the NRIC in the reason text.

## Output
Return ONLY a JSON object with exactly these keys: applicationId, decision, reason, riskFlags
'decision' is one of "APPROVED", "REJECTED", "DUPLICATE", "REVIEW".
'riskFlags' is an array of strings (empty when none).
Return raw JSON only - no markdown fences, no commentary.

## Application to process

Application ID: APP-@{formatDateTime(utcNow(),'yyyyMMddHHmmss')}
Existing customer found: @{greater(length(body('Get_customer_by_NRIC')?['value']), 0)}
Full Name: @{toUpper(trim(triggerBody()?['fullName']))}
NRIC: @{toUpper(trim(triggerBody()?['nric']))}
Date of Birth: @{triggerBody()?['dateOfBirth']}
Age: @{div(sub(ticks(utcNow()), ticks(triggerBody()?['dateOfBirth'])), 315360000000000)}
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

Process this application now and return the decision JSON.
```

Three expressions in that block do real work:

| Expression | Why |
|---|---|
| `greater(length(body('Get_customer_by_NRIC')?['value']), 0)` | Turns the SharePoint lookup into true/false for Rule 1 |
| `div(sub(ticks(utcNow()), ticks(...dateOfBirth)), 315360000000000)` | Age in whole years. The model cannot be trusted to do date arithmetic |
| `toUpper(trim(...))` on NRIC and name | Normalisation, so messy input still matches |

> Instructions is a **rich-text field**. Pasted `@{...}` may not become live
> expressions. Use the `</>` code-mode toggle to paste, then verify the
> expressions render differently from plain text. An expression left as dead
> text produces a silently wrong answer, not an error.
>
> Avoid underscores in action names you reference from rich-text fields — the
> editor escapes them (`Compose\_age`) and the reference breaks.

### Output

Set **Output** to **Custom structured output** and paste this JSON Schema:

```json
{
  "type": "object",
  "properties": {
    "applicationId": {
      "type": "string",
      "description": "The application reference, e.g. APP-20260801103045"
    },
    "decision": {
      "type": "string",
      "enum": ["APPROVED", "REJECTED", "DUPLICATE", "REVIEW"],
      "description": "The onboarding decision"
    },
    "reason": {
      "type": "string",
      "description": "One or two sentences stating the decision and the exact reason"
    },
    "riskFlags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Risk flags raised, empty when none"
    }
  },
  "required": ["applicationId", "decision", "reason", "riskFlags"]
}
```

The `enum` on `decision` is what stops the model inventing values like
`PENDING`, which the website would not know how to render. Structured output
also removes the need for a separate Parse JSON action.

---

## Node 4 — Response

Returns the decision to the website.

| Field | Value |
|---|---|
| Status Code | `200` |
| Headers | `Content-Type` : `application/json` |
| Body | `@{body('Agent')?['structuredOutput']}` |

---

## Node 5 — Send an email (V2)

The applicant's confirmation.
`send_confirmation_email` tool.

**Connector → Office 365 Outlook → Send an email (V2)**

### To — use the picker, never a typed expression

Click the **⚡** dynamic content button and choose:

```
When a HTTP request is received  ›  Email
```

The field should show a blue **Email** chip.

> ### The single most important thing on this page
>
> **Do not type an expression into the To field.** Every typed form fails —
> all of these were tried and every one produced the same error:
>
> ```
> @{triggerBody()?['email']}
> @{toLower(trim(triggerBody()?['email']))}
> @{triggerOutputs()?['body/email']}
> @triggerOutputs()?['body/email']
> @{first(split(triggerOutputs()?['body/email'], decodeUriComponent('%0A')))}
> ```
>
> They all fail at run time with:
>
> ```
> OpenApiOperationParameterTypeConversionFailed
> Input parameter 'emailMessage/To' is required to be of type 'String/email'.
> The runtime value '"applicant@example.com\n"' to be converted doesn't have
> the expected format 'string/email'.
> ```
>
> Note the `\n`. A typed expression arrives with a trailing newline and the
> connector rejects the address as malformed. **A picker-inserted token does
> not.** Same value, different code path.
>
> A literal typed address (`someone@example.com`) also works — useful if you
> want every decision to reach the trainer rather than the applicant.
>
> This is not documented by Microsoft. Expect learners to hit it.

### Subject

Type the text, then insert the reference with the ⚡ picker:

```
Your Marina Trust Bank application - [Agent › Application Id]
```

Deliberately no decision word. "REJECTED" in a subject line is not how a bank
writes to a customer, and the reason text already states the outcome.

### Body

Switch to code mode (`</>`) and paste:

```html
<div>Dear @{triggerBody()?['fullName']},</div>
<div>&nbsp;</div>
<div>Thank you for your application to Marina Trust Bank.</div>
<div>&nbsp;</div>
<div>@{body('Agent')?['structuredOutput/reason']}</div>
<div>&nbsp;</div>
<div>Your application reference is @{body('Agent')?['structuredOutput/applicationId']}. Please quote this in any correspondence.</div>
<div>&nbsp;</div>
<div>Yours sincerely,<br>Customer Onboarding<br>Marina Trust Bank</div>
<div>&nbsp;</div>
<div style="color:#888;font-size:12px">Training lab — Marina Trust Bank is a fictitious institution created for the Building AI Agents for Work Automation course. This is not a real bank and no real account has been opened.</div>
```

> **No NRIC. No risk flags. No income.** Those belong in the audit log, not in
> a customer's inbox. Sending an applicant their own `PEP` flag would be a
> genuine data-handling failure, not a style problem.

> **Subject accepts pasted expressions; Body does not.** Subject is plain text
> and parses `@{...}` automatically. Body is a rich-text/HTML editor and treats
> pasted text literally — use code mode or the token picker.

---

## Publish

Click **Publish** — saving is not enough. The HTTP endpoint always serves the
**published** version.

> If an edit does not seem to take effect, open **⋯ → Version history**. If
> `LIVE` and `CURRENT DRAFT` show different version numbers, you have an
> unpublished draft. This is the single most common source of "my change did
> nothing".

---

# Part 3 — Connect the website

1. Serve the site: `cd website && python3 -m http.server 8900`
2. Open <http://localhost:8900/index.html>
3. Copy the **HTTP POST URL** from the trigger node
4. Paste it into **Lab configuration → HTTP POST URL** on the page

> Serve over HTTP. Opening `index.html` directly from the filesystem gives the
> page a `null` origin and the browser blocks the POST.

The status line validates the URL as you type. Green means the URL is
well-formed — it does not mean the flow is published.

---

# Part 4 — Test

Use the **Trainer demo data** dropdown on the page.

| Case | Input | Expected | Rule |
|---|---|---|---|
| TC1 | New applicant, Savings, SGD 1,000 | **APPROVED** | 6 |
| TC2 | `S8412345D` | **DUPLICATE** | 1 |
| TC5 | `s8412345d` lowercase | **DUPLICATE** | 1 + normalisation |
| TC6 | PEP = Yes | **REVIEW** + `PEP` | 3 |
| TC7 | Date of birth 2010 | **REJECTED** + `MINOR` | 2 |
| TC4 | Current account, Unemployed | **REJECTED** | 4 |
| TC8 | Savings, SGD 200 | **REJECTED** | 5 |
| TC3 | Fixed Deposit, income SGD 20,000 | **REJECTED** | 4 |

Two cases worth demonstrating in class:

**TC5** proves normalisation. Same NRIC as TC2 but lowercase. If the
`toUpper()` were missing, this would come back APPROVED and create a duplicate
customer — the exact failure the automation exists to prevent.

**TC10** (under 18 *and* a PEP) proves the rules are **ordered**. Two rules
apply; only the first fires. The result is REJECTED with `MINOR`, not REVIEW.

Expect **~20 seconds** per submission. The SharePoint lookup and the model call
are both network round-trips. Tell learners, so they do not assume it has hung.

---

# Part 5 — Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `InsufficientMcsCredits` | No Copilot Credits in the environment | Use a Developer environment, or have an admin allocate credits |
| `TriggerInputSchemaMismatch` | Form sent strings where the schema wants number/boolean | Cast in the website before POSTing |
| Publish fails on `relativePath` | A static path was typed in Relative path | Clear the field |
| Empty response body | Response node has no Body, or flow not published | Set Body, then **Publish** |
| Edits have no effect | Draft not published | ⋯ → Version history; publish the draft |
| `Creating query failed` | `concat()` form in Filter Query | Use `NRIC eq '` + token + `'` |
| Duplicate check never fires | Missing `toUpper`, or the expression is dead text | Check the expression renders as a token |
| Create item fails | `Title` not set | Bind Title to the NRIC |
| Audit write fails on PEP cases | `REVIEW` missing from the Decision choices | Add the choice value |
| Website shows "could not read the decision" | Response returns something other than the decision object | Set Body to the agent's `structuredOutput` |
| **`OpenApiOperationParameterTypeConversionFailed` on the email** | **A typed expression in the To field — the value arrives with a trailing `\n`** | **Use the ⚡ picker to insert the Email token. Never type `@{...}` into To** |
| Node shows "Needs setup" after being moved | Moving a node clears its configuration | Reconfigure every field, and the Connection |
| A run returns HTTP 200 but nothing happened | The Response returned before a later action failed, or a node was unconfigured | Judge success from the **Activity** tab, not the HTTP status |

### How to tell whether something actually worked

A `200` from the endpoint means **the Response action ran** — nothing more.
Any action after it can fail silently, and an unconfigured node is skipped
without complaint.

Always confirm in the **Activity** tab: a green tick on the run, and green
ticks on each action. That is the only reliable signal.

**Where to look:** the **Activity** tab in the flow designer lists every run.
Open a failed run to see which action went red and read its actual error — far
faster than guessing.

---

# Appendix B — Extending the lab

Not yet built.

**Create item in `Customers`** on the APPROVED branch, behind an If/Else on
`@{body('Agent')?['structuredOutput/decision']}` equals `APPROVED`. Bind Title
to the NRIC. Once this exists, an approved applicant is added to the register —
so resubmitting the same NRIC returns DUPLICATE the second time, which is a
compelling thing to demonstrate live.

**Create item in `OnboardingLog`** after the branches rejoin, so every decision
is logged whatever the outcome. That is the audit requirement in the bank's
own service standards.

---

**Next:** [Lab 7 — HTTP and Chatbot](../Lab%207%20-%20HTTP%20and%20Chatbot/README.md)
