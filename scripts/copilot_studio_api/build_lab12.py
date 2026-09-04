"""Lab 12 - HTTP and Application Approval Agent (DO NOT DELETE):
HTTP trigger -> SharePoint Get items (Lab 12 - Customers, NRIC eq '<toUpper(trim)>', top 1) -> Compose Application (normalised)
-> Agent (six ordered rules, custom structured output) -> Response (structured output) -> SharePoint Create item (Lab 12 - Onboarding Log)
-> Send an email to the trainer."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *; from wfapi_ext import *
SITE = "https://tertiaryinfotech.sharepoint.com/sites/WSQCourses"
LIST_CUSTOMERS = "6b0cbc95-291f-442c-a40a-d7ab779e95eb"      # Lab 12 - Customers (Title=FullName, NRIC, Email, Phone, DateOfBirth, Employment, Income, Decision)
LIST_LOG = "aa9ca135-5004-4936-b6f0-c2c50e78886d"            # Lab 12 - Onboarding Log (Title=reference, NRIC, Decision, Reason, SubmittedAt)
SCHEMA = {"type": "object", "properties": {
    "fullName": {"type": "string"}, "nric": {"type": "string"}, "dateOfBirth": {"type": "string"}, "nationality": {"type": "string"},
    "residencyStatus": {"type": "string"}, "email": {"type": "string"}, "mobile": {"type": "string"}, "address": {"type": "string"},
    "postalCode": {"type": "string"}, "accountType": {"type": "string"}, "employmentStatus": {"type": "string"}, "occupation": {"type": "string"},
    "employer": {"type": "string"}, "annualIncome": {"type": "number"}, "sourceOfFunds": {"type": "string"}, "purposeOfAccount": {"type": "string"},
    "initialDeposit": {"type": "number"}, "pep": {"type": "boolean"}, "foreignTaxResident": {"type": "boolean"}},
    "required": ["fullName", "nric", "dateOfBirth", "accountType", "employmentStatus", "annualIncome", "initialDeposit"]}
APPLICATION = """Application ID: APP-@{formatDateTime(utcNow(),'yyyyMMddHHmmss')}
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
Tax Resident Outside Singapore: @{triggerBody()?['foreignTaxResident']}"""
INSTR = """You are the Customer Onboarding Assistant for a Singapore retail bank (Marina Trust Bank). You process new account applications and must follow the bank's onboarding rules exactly, in the order given.

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

## Application to process

@{outputs('Application')}

Process this application now and return the decision JSON."""
OUT_SCHEMA = {"type": "object", "properties": {
    "applicationId": {"type": "string", "description": "The application reference, e.g. APP-20260801103045"},
    "decision": {"type": "string", "enum": ["APPROVED", "REJECTED", "DUPLICATE", "REVIEW"], "description": "The onboarding decision"},
    "reason": {"type": "string", "description": "One or two sentences stating the decision and the exact reason"},
    "riskFlags": {"type": "array", "items": {"type": "string"}, "description": "Risk flags raised, empty when none"}},
    "required": ["applicationId", "decision", "reason", "riskFlags"]}
SO = "body('Agent')?['structuredOutput']"
def build():
    wf = Workflow("Lab 12 - HTTP and Application Approval Agent (DO NOT DELETE)")
    s = wf.start_http(schema=SCHEMA)
    g = wf.connector("Get customer by NRIC", "shared_sharepointonline", "GetItems",
                     {"dataset": SITE, "table": LIST_CUSTOMERS, "$filter": "NRIC eq '@{toUpper(trim(triggerBody()?['nric']))}'", "$top": 1})
    c = wf.compose("Application", APPLICATION)
    a = wf.agent("Agent", INSTR, output_mode="structured", schema=OUT_SCHEMA, web_search=False)
    # structuredOutput when the agent ran; otherwise a readable error object (e.g. the environment is out of Copilot Credits)
    fallback = obj_expr({"applicationId": "''", "decision": "'ERROR'", "reason": "coalesce(body('Agent')?['message'], 'The onboarding agent returned no decision.')", "riskFlags": Raw("'[]'")})
    r = wf.response("Response", body=f"@coalesce({SO}, {fallback})")
    log = wf.connector("Log decision", "shared_sharepointonline", "PostItem",
                       {"dataset": SITE, "table": LIST_LOG,
                        "item/Title": f"@{{{SO}?['applicationId']}}",
                        "item/NRIC": "@{toUpper(trim(triggerBody()?['nric']))}",
                        "item/Decision": f"@{{{SO}?['decision']}}",
                        "item/Reason": f"@{{{SO}?['reason']}} Risk flags: @{{join(coalesce({SO}?['riskFlags'], json('[]')), ', ')}}",
                        "item/SubmittedAt": "@{utcNow()}"})
    m = wf.connector("Send an email", "shared_office365", "SendEmailV2",
                     {"emailMessage/To": TRAINER_EMAIL,
                      "emailMessage/Subject": f"Marina Trust Bank application @{{{SO}?['applicationId']}} - @{{{SO}?['decision']}}",
                      "emailMessage/Body": ("<p>Dear Trainer,</p><p>An onboarding application was processed by Lab 12.</p>"
                                            f"<p><b>Applicant:</b> @{{toUpper(trim(triggerBody()?['fullName']))}}<br><b>Account type:</b> @{{triggerBody()?['accountType']}}<br>"
                                            f"<b>Decision:</b> @{{{SO}?['decision']}}<br><b>Risk flags:</b> @{{join(coalesce({SO}?['riskFlags'], json('[]')), ', ')}}</p>"
                                            f"<p>@{{{SO}?['reason']}}</p><p>Reference @{{{SO}?['applicationId']}}. Logged to Lab 12 - Onboarding Log.</p>"
                                            "<p style=\"color:#888;font-size:12px\">Training lab - Marina Trust Bank is a fictitious institution created for a training course.</p>"),
                      "emailMessage/Importance": "Normal"})
    wf.chain(s, g, c, a, r, log, m)
    return wf
if __name__ == '__main__':
    wid = create(build())
    ids = json.load(open(SCRATCH + '/ids.json')); ids['lab12'] = wid; json.dump(ids, open(SCRATCH + '/ids.json', 'w'), indent=1)
    print(designer_url(wid))
