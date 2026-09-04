# Lab 12's alternative build — SharePoint as an Agent Tool

The same onboarding decision, built a different way.

**Lab 12** runs the SharePoint lookup as a **step before** the agent. The
lookup always happens; the agent is handed the answer.

**Lab 9b** gives the agent SharePoint as a **tool**. The agent decides for
itself when to look a customer up, calls it, reads the result, and continues
reasoning.

Build this as a **separate flow** so both can be run side by side. Keep
Lab 12 intact.

---

## Why this matters

This is the difference between **workflow automation** and an **agent**.

| | Lab 12 — step | Lab 9b — tool |
|---|---|---|
| Who decides to look up? | You did, at design time | The agent, at run time |
| Does the lookup always run? | Yes, guaranteed | Only when the agent chooses |
| Model calls per application | 1 | 2 or more |
| Where the logic lives | The flow structure | The agent's reasoning |
| Debugging | Read the run history | Read the agent's tool calls |
| Cost | Lower | Higher |
| Rule 1 "always first" | Structurally enforced | Instructed, not enforced |

Neither is "better". Lab 12 is what you want for a regulated decision that
must be auditable. Lab 9b is what you want when the task is open-ended and
the agent needs to choose its own path.

---

## Step 1 — Create the flow

Copilot Studio → **Flows** → **+ New agent flow** → name it
`Lab 12's alternative build - Onboarding with Agent Tools`.

Build **four** nodes. Note there is no separate SharePoint step — that is the
whole point:

```
When a HTTP request is received
  → Agent            ← has SharePoint as a TOOL
  → Response
  → Send an email
```

### Trigger

Identical to Lab 12:

- Allowed HTTP method: `POST`
- Who can trigger: **Anyone (no authentication)**
- Relative path: **blank**
- Request Body JSON Schema: copy from `LAB-GUIDE.md` Part 2, Node 1

---

## Step 2 — Add the Agent and attach the tool

Add an **Agent** node and create its connection.

In the Agent panel, find **Tools** → **+** → **SharePoint**.

Choose the **Get items** action, then configure it as the tool:

| Field | Value |
|---|---|
| Site Address | `https://YOURTENANT.sharepoint.com/sites/MarinaTrustBankOnboarding` |
| List Name | `Customers` |

**Leave Filter Query empty.** This is the key difference. In Lab 12 you
wrote the filter yourself. Here the agent supplies it at run time, because only
the agent knows which NRIC it is checking.

Give the tool a clear name and description — the agent reads these to decide
when to call it:

- **Name:** `check_customer_register`
- **Description:**
  `Look up an applicant in the Marina Trust Bank customer register by NRIC.
  Returns matching customer records. An empty result means the applicant is
  not an existing customer.`

> The description is not documentation — it is a prompt. A vague description
> gives you an agent that calls the tool at the wrong time, or not at all.
> This is the single most common reason a tool-based agent misbehaves.

---

## Step 3 — Agent Instructions

Rewritten for tool use. Three things changed from Lab 12:

1. Step 1 now tells the agent to **call the tool**, rather than read a field
2. A **Tools** section explains what is available and when to use it
3. The application block no longer carries `Existing customer found`

Copy the whole block:

```
You are the Customer Onboarding Assistant for a Singapore retail bank (Marina Trust Bank). You process new account applications and must follow the bank's onboarding rules exactly, in the order given.

## Your tools

check_customer_register — looks up an applicant in the bank's customer register by NRIC. Returns any matching customer records. An empty result means the applicant is NOT an existing customer.

You MUST call check_customer_register exactly once, before applying any other rule. Pass the applicant's NRIC in uppercase, with surrounding spaces removed. Never guess whether someone is an existing customer, and never skip this call, even when the applicant looks new.

## Definitions
- "Gainfully employed" means Employment Status is one of: Employed, Self-Employed, Contract, Part-Time.
- Every other status (Student, National Service, Homemaker, Retired, Unemployed) is NOT gainfully employed.
- "High-risk source of funds" means Source of Funds is one of: Gift or Inheritance, Cryptocurrency Proceeds, Other.

## Onboarding rules - evaluate in this order and STOP at the first rule that fires

STEP 1 - DUPLICATE CHECK (always first)
Call check_customer_register with the applicant's NRIC in uppercase.
If it returns one or more records, the applicant is an existing customer:
decision = "DUPLICATE", riskFlags = []. Stop.
If it returns nothing, continue to STEP 2.

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
- Never assume the result of check_customer_register. Call it and read what comes back.
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

Process this application now. Check the customer register first, then apply the rules in order, then return the decision JSON.
```

### What changed, and why

| Lab 12 | Lab 9b | Reason |
|---|---|---|
| `Existing customer found: @{greater(length(...)...)}` | Line removed | The agent finds this out itself |
| "If it is true, the applicant is an existing customer" | "Call check_customer_register ... If it returns records" | The agent must act, not read |
| No Tools section | `## Your tools` section added | The agent needs to know what it has |
| — | "You MUST call it exactly once, before any other rule" | Without this the agent sometimes skips it |
| — | "Never assume the result. Call it and read what comes back." | Stops the agent guessing from the name |

Note how much **more instruction** the tool version needs. That is the honest
cost of handing control to the model: you spend the effort you saved on flow
structure writing guardrails in prose instead.

### Output

Same as Lab 12 — **Custom structured output** with the same JSON Schema.
Copy it from `LAB-GUIDE.md` Part 2, Node 3.

---

## Step 4 — Response and Email

Identical to Lab 12. Copy both from `LAB-GUIDE.md` Part 2, Nodes 4 and 5.

Response comes **before** the email, so a mail failure cannot stop the website
receiving its decision.

> Remember the To field: insert the applicant's address with the **⚡ picker**
> (`When a HTTP request is received › Email`). A typed `@{...}` expression
> fails with a trailing-newline error. See the boxed note in `LAB-GUIDE.md`.

Then **Publish**.

---

## Step 5 — Compare the two

Run the same application through both flows and look at the differences.

| What to compare | Where to look |
|---|---|
| Decision | Should be identical for every test case |
| Run duration | Activity tab — 1b is usually slower |
| Number of actions | 1b shows the agent's tool call as a nested step |
| Model calls | 1b reasons, calls, then reasons again |

### The interesting failure

Run **TC5** — lowercase `s8412345d` — through Lab 9b several times.

In Lab 12 the `toUpper()` is in the filter expression, so the match is
guaranteed. In 1b the agent is *instructed* to uppercase the NRIC before
calling the tool. Usually it does. Occasionally it may not.

That inconsistency is the lesson, not a bug to fix. Ask the class: would you
put this version in front of a regulator?

---

## Discussion questions

1. Lab 9b needed far more instruction to get the same behaviour. What
   does that tell you about where complexity goes when you make something
   "more agentic"?

2. Lab 12's flow diagram shows the duplicate check. Lab 9b's does
   not — it is hidden inside the agent. What does that mean for someone
   auditing the process a year from now?

3. When would you actually want the agent to decide whether to check? What
   kind of task makes the tool approach clearly better?

4. Lab 9b costs more per run. For 10 applications a day that is nothing.
   For 10,000, it is a budget line. How would that change your design?

---

## When to use which

**Use the step approach (Lab 12) when:**
- The check is mandatory and must be provable
- The order of operations is a compliance requirement
- You need the same behaviour on every single run
- Cost per run matters at volume

**Use the tool approach (Lab 9b) when:**
- The task is open-ended and the path is not known in advance
- Some lookups are only needed sometimes
- The agent may need to call something repeatedly, or in a varying order
- Flexibility is worth more than predictability

Most production systems use both: deterministic steps for the parts that must
happen, tools for the parts where judgement is genuinely required.
