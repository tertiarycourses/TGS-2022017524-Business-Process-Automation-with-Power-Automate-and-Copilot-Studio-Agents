#!/usr/bin/env python3
"""
Emits the Power Automate legacy import package for LU1 Activity 1.

Package layout expected by make.powerautomate.com -> Import -> Import Package:

    manifest.json
    Microsoft.Flow/flows/<name>/definition.json
    Microsoft.Flow/flows/<name>/apisMap.json

Invoked by build-package.sh; not meant to be run directly.
"""
import json
import sys
import os

BUILD = sys.argv[1]
GEMINI_KEY = sys.argv[2]

SITE = "https://tertiaryinfotech.sharepoint.com/sites/MarinaTrustBankOnboarding"

# Trainer address that receives every decision, for lab verification.
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "angch@tertiaryinfotech.com")
FLOW_DIR = os.path.join(BUILD, "Microsoft.Flow", "flows", "LU1MarinaTrustOnboarding")

SYSTEM_INSTRUCTION = (
    "You are the Customer Onboarding Assistant for a Singapore retail bank "
    "(Marina Trust Bank). You process new account applications and must follow "
    "the bank's onboarding rules exactly, in the order given.\n\n"
    "## Definitions\n"
    "- \"Gainfully employed\" means Employment Status is one of: Employed, "
    "Self-Employed, Contract, Part-Time.\n"
    "- Every other status (Student, National Service, Homemaker, Retired, "
    "Unemployed) is NOT gainfully employed.\n"
    "- \"High-risk source of funds\" means Source of Funds is one of: Gift or "
    "Inheritance, Cryptocurrency Proceeds, Other.\n\n"
    "## Onboarding rules - evaluate in this order and STOP at the first rule that fires\n\n"
    "STEP 1 - DUPLICATE CHECK (always first)\n"
    "The application includes a field 'Existing customer found'. If it is true, "
    "the applicant is an EXISTING customer:\n"
    "  decision = \"DUPLICATE\", riskFlags = []. Stop.\n\n"
    "STEP 2 - AGE\n"
    "If Age is below 18:\n"
    "  decision = \"REJECTED\", riskFlags = [\"MINOR\"]. Stop.\n\n"
    "STEP 3 - KYC / AML SCREENING\n"
    "Raise a flag for each of these that is true:\n"
    "  - PEP is true                              -> flag \"PEP\"\n"
    "  - Tax Resident Outside Singapore is true   -> flag \"CRS_FATCA\"\n"
    "  - Source of Funds is high-risk             -> flag \"SOURCE_OF_FUNDS\"\n"
    "If one or more flags were raised:\n"
    "  decision = \"REVIEW\", riskFlags = the flags raised. Stop.\n\n"
    "STEP 4 - ACCOUNT ELIGIBILITY\n"
    "Apply only the rule for the account type actually requested:\n"
    "  - Savings          - no income or employment requirement.\n"
    "  - Joint Savings    - no income or employment requirement.\n"
    "  - Student Account  - Employment Status must be exactly \"Student\".\n"
    "  - Current          - applicant must be gainfully employed.\n"
    "  - Fixed Deposit    - Annual Income must be at least SGD 30,000.\n"
    "  - Multi-Currency   - Annual Income at least SGD 60,000 AND gainfully employed.\n"
    "If the applicant fails this rule:\n"
    "  decision = \"REJECTED\", riskFlags = []. Name the exact criterion not met "
    "and suggest a Savings account instead. Stop.\n\n"
    "STEP 5 - MINIMUM INITIAL DEPOSIT\n"
    "  Savings SGD 500 | Joint Savings SGD 1,000 | Student Account SGD 0 | "
    "Current SGD 3,000 | Fixed Deposit SGD 10,000 | Multi-Currency SGD 5,000\n"
    "If Initial Deposit is below the minimum for the requested account type:\n"
    "  decision = \"REJECTED\", riskFlags = []. State the minimum for that account "
    "type and invite them to reapply. Stop.\n\n"
    "STEP 6 - APPROVAL\n"
    "decision = \"APPROVED\", riskFlags = [].\n\n"
    "## Constraints\n"
    "- Never invent an NRIC, email address, income figure, deposit amount or "
    "account number.\n"
    "- Judge the applicant only against the rule for the account type they asked "
    "for. Never approve them into a different account type.\n"
    "- 'reason' must be one or two plain-English sentences stating the decision "
    "and the exact reason for it. Write as a Singapore bank writes: courteous, "
    "factual. No exclamation marks, no marketing language, no emoji.\n"
    "- Never put the NRIC in the reason text.\n\n"
    "## Output\n"
    "Return ONLY a JSON object with keys: applicationId, decision, reason, riskFlags.\n"
    "'decision' is one of \"APPROVED\", \"REJECTED\", \"DUPLICATE\", \"REVIEW\".\n"
    "'riskFlags' is an array of strings (empty when none)."
)

USER_PROMPT = (
    "New customer onboarding application received.\n\n"
    "Application ID: @{outputs('Compose_applicationId')}\n"
    "Existing customer found: @{greater(length(body('Check_for_duplicate_NRIC')?['value']), 0)}\n"
    "Full Name: @{outputs('Compose_fullName')}\n"
    "Date of Birth: @{triggerBody()?['dateOfBirth']}\n"
    "Age: @{outputs('Compose_age')}\n"
    "Nationality: @{triggerBody()?['nationality']}\n"
    "Residency Status: @{triggerBody()?['residencyStatus']}\n"
    "Email: @{outputs('Compose_email')}\n"
    "Mobile: @{triggerBody()?['mobile']}\n"
    "Account Type: @{triggerBody()?['accountType']}\n"
    "Employment Status: @{triggerBody()?['employmentStatus']}\n"
    "Occupation: @{triggerBody()?['occupation']}\n"
    "Employer: @{triggerBody()?['employer']}\n"
    "Annual Income (SGD): @{triggerBody()?['annualIncome']}\n"
    "Source of Funds: @{triggerBody()?['sourceOfFunds']}\n"
    "Purpose of Account: @{triggerBody()?['purposeOfAccount']}\n"
    "Initial Deposit (SGD): @{triggerBody()?['initialDeposit']}\n"
    "PEP: @{triggerBody()?['pep']}\n"
    "Tax Resident Outside Singapore: @{triggerBody()?['foreignTaxResident']}\n\n"
    "Process this application and return the decision JSON."
)

TRIGGER_SCHEMA = {
    "type": "object",
    "properties": {
        "fullName": {"type": "string"},
        "nric": {"type": "string"},
        "dateOfBirth": {"type": "string"},
        "nationality": {"type": "string"},
        "residencyStatus": {"type": "string"},
        "email": {"type": "string"},
        "mobile": {"type": "string"},
        "address": {"type": "string"},
        "postalCode": {"type": "string"},
        "accountType": {"type": "string"},
        "employmentStatus": {"type": "string"},
        "occupation": {"type": "string"},
        "employer": {"type": "string"},
        "annualIncome": {"type": "number"},
        "sourceOfFunds": {"type": "string"},
        "purposeOfAccount": {"type": "string"},
        "initialDeposit": {"type": "number"},
        "pep": {"type": "boolean"},
        "foreignTaxResident": {"type": "boolean"},
    },
    "required": [
        "fullName", "nric", "dateOfBirth", "accountType",
        "employmentStatus", "annualIncome", "initialDeposit",
    ],
}

DECISION_SCHEMA = {
    "type": "object",
    "properties": {
        "applicationId": {"type": "string"},
        "decision": {"type": "string"},
        "reason": {"type": "string"},
        "riskFlags": {"type": "array", "items": {"type": "string"}},
    },
}

GEMINI_BODY = {
    "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
    "contents": [{"role": "user", "parts": [{"text": USER_PROMPT}]}],
    "generationConfig": {
        "temperature": 0,
        "responseMimeType": "application/json",
        "responseSchema": {
            "type": "OBJECT",
            "properties": {
                "applicationId": {"type": "STRING"},
                "decision": {
                    "type": "STRING",
                    "enum": ["APPROVED", "REJECTED", "DUPLICATE", "REVIEW"],
                },
                "reason": {"type": "STRING"},
                "riskFlags": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": ["applicationId", "decision", "reason", "riskFlags"],
        },
    },
}

GEMINI_URI = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.6-flash:generateContent?key=" + GEMINI_KEY
)

# ---------------------------------------------------------------- definition

definition = {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "$connections": {"defaultValue": {}, "type": "Object"},
        "$authentication": {"defaultValue": {}, "type": "SecureObject"},
    },
    "triggers": {
        "manual": {
            "type": "Request",
            "kind": "Http",
            "inputs": {"schema": TRIGGER_SCHEMA, "method": "POST"},
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000001"},
        }
    },
    "actions": {
        # ---- normalise ----------------------------------------------------
        "Compose_nric": {
            "runAfter": {},
            "type": "Compose",
            "inputs": "@toUpper(trim(triggerBody()?['nric']))",
            "description": "Uppercase + trim the NRIC so the duplicate check matches.",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000002"},
        },
        "Compose_fullName": {
            "runAfter": {"Compose_nric": ["Succeeded"]},
            "type": "Compose",
            "inputs": "@toUpper(trim(triggerBody()?['fullName']))",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000003"},
        },
        "Compose_email": {
            "runAfter": {"Compose_fullName": ["Succeeded"]},
            "type": "Compose",
            "inputs": "@toLower(trim(triggerBody()?['email']))",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000004"},
        },
        "Compose_applicationId": {
            "runAfter": {"Compose_email": ["Succeeded"]},
            "type": "Compose",
            "inputs": "@concat('APP-', formatDateTime(utcNow(),'yyyyMMdd'), '-', string(rand(1000,9999)))",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000005"},
        },
        "Compose_age": {
            "runAfter": {"Compose_applicationId": ["Succeeded"]},
            "type": "Compose",
            "inputs": "@div(sub(ticks(utcNow()), ticks(triggerBody()?['dateOfBirth'])), 315360000000000)",
            "description": "Whole years between date of birth and now.",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000006"},
        },
        # ---- duplicate check ----------------------------------------------
        "Check_for_duplicate_NRIC": {
            "runAfter": {"Compose_age": ["Succeeded"]},
            "type": "OpenApiConnection",
            "inputs": {
                "host": {
                    "connectionName": "shared_sharepointonline",
                    "operationId": "GetItems",
                    "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
                },
                "parameters": {
                    "dataset": SITE,
                    "table": "Customers",
                    "$filter": "@concat('NRIC eq ''', outputs('Compose_nric'), '''')",
                    "$top": 1,
                },
                "authentication": "@parameters('$authentication')",
            },
            "description": "STEP 1 - look up the normalised NRIC in the Customers register.",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000007"},
        },
        # ---- gemini --------------------------------------------------------
        "Gemini_decision": {
            "runAfter": {"Check_for_duplicate_NRIC": ["Succeeded"]},
            "type": "Http",
            "inputs": {
                "method": "POST",
                "uri": GEMINI_URI,
                "headers": {"Content-Type": "application/json"},
                "body": GEMINI_BODY,
            },
            "description": "Applies the six ordered onboarding rules and returns the decision JSON.",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000008"},
        },
        "Parse_decision": {
            "runAfter": {"Gemini_decision": ["Succeeded"]},
            "type": "ParseJson",
            "inputs": {
                "content": "@body('Gemini_decision')?['candidates'][0]?['content']?['parts'][0]?['text']",
                "schema": DECISION_SCHEMA,
            },
            "description": (
                "Gemini returns the decision JSON as a string inside parts[0].text. "
                "(parts[0] also carries a thoughtSignature key; that is harmless.)"
            ),
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-000000000009"},
        },
        # ---- branch --------------------------------------------------------
        "If_approved": {
            "runAfter": {"Parse_decision": ["Succeeded"]},
            "type": "If",
            "expression": {
                "equals": [
                    "@body('Parse_decision')?['decision']",
                    "APPROVED",
                ]
            },
            "actions": {
                "Create_customer_record": {
                    "runAfter": {},
                    "type": "OpenApiConnection",
                    "inputs": {
                        "host": {
                            "connectionName": "shared_sharepointonline",
                            "operationId": "PostItem",
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
                        },
                        "parameters": {
                            "dataset": SITE,
                            "table": "Customers",
                            "item/Title": "@outputs('Compose_nric')",
                            "item/NRIC": "@outputs('Compose_nric')",
                            "item/FullName": "@outputs('Compose_fullName')",
                            "item/DateOfBirth": "@triggerBody()?['dateOfBirth']",
                            "item/Email": "@outputs('Compose_email')",
                            "item/AccountType/Value": "@triggerBody()?['accountType']",
                            "item/AnnualIncome": "@triggerBody()?['annualIncome']",
                            "item/OnboardedOn": "@utcNow()",
                        },
                        "authentication": "@parameters('$authentication')",
                    },
                    "description": "STEP 6 - only APPROVED applicants get a customer record.",
                    "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-00000000000a"},
                }
            },
            "else": {"actions": {}},
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-00000000000b"},
        },
        # ---- audit log (both branches) --------------------------------------
        "Write_audit_log": {
            "runAfter": {"If_approved": ["Succeeded"]},
            "type": "OpenApiConnection",
            "inputs": {
                "host": {
                    "connectionName": "shared_sharepointonline",
                    "operationId": "PostItem",
                    "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
                },
                "parameters": {
                    "dataset": SITE,
                    "table": "OnboardingLog",
                    "item/Title": "@outputs('Compose_applicationId')",
                    "item/Timestamp": "@utcNow()",
                    "item/ApplicationID": "@outputs('Compose_applicationId')",
                    "item/NRIC": "@outputs('Compose_nric')",
                    "item/AccountType/Value": "@triggerBody()?['accountType']",
                    "item/Decision/Value": "@body('Parse_decision')?['decision']",
                    "item/Reason": "@body('Parse_decision')?['reason']",
                },
                "authentication": "@parameters('$authentication')",
            },
            "description": "Every decision is logged - approved, rejected, duplicate or review.",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-00000000000c"},
        },
        # ---- email ----------------------------------------------------------
        "Email_decision": {
            "runAfter": {"Write_audit_log": ["Succeeded"]},
            "type": "OpenApiConnection",
            "inputs": {
                "host": {
                    "connectionName": "shared_office365",
                    "operationId": "SendEmailV2",
                    "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
                },
                "parameters": {
                    "emailMessage/To": NOTIFY_EMAIL,
                    "emailMessage/Subject": (
                        "@concat('Marina Trust Bank - ', "
                        "body('Parse_decision')?['decision'], ' - ', "
                        "outputs('Compose_applicationId'))"
                    ),
                    "emailMessage/Body": (
                        "<p><strong>Decision:</strong> @{body('Parse_decision')?['decision']}</p>"
                        "<p><strong>Reason:</strong> @{body('Parse_decision')?['reason']}</p>"
                        "<p><strong>Risk flags:</strong> @{join(body('Parse_decision')?['riskFlags'], ', ')}</p>"
                        "<hr>"
                        "<p><strong>Application:</strong> @{outputs('Compose_applicationId')}<br>"
                        "<strong>Applicant:</strong> @{outputs('Compose_fullName')}<br>"
                        "<strong>Account type:</strong> @{triggerBody()?['accountType']}<br>"
                        "<strong>Employment:</strong> @{triggerBody()?['employmentStatus']}<br>"
                        "<strong>Annual income:</strong> SGD @{triggerBody()?['annualIncome']}<br>"
                        "<strong>Initial deposit:</strong> SGD @{triggerBody()?['initialDeposit']}<br>"
                        "<strong>Age:</strong> @{outputs('Compose_age')}</p>"
                        "<p style=\"color:#888;font-size:12px\">Training lab - Marina Trust Bank is "
                        "fictitious and all applicant data is mock data.</p>"
                    ),
                    "emailMessage/Importance": "Normal",
                },
                "authentication": "@parameters('$authentication')",
            },
            "description": "Sends the decision to the trainer for verification.",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-00000000000e"},
        },
        # ---- response -------------------------------------------------------
        "Response": {
            "runAfter": {"Email_decision": ["Succeeded"]},
            "type": "Response",
            "kind": "Http",
            "inputs": {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": "@body('Parse_decision')",
            },
            "description": "Returns the decision to the website (script.js reads this).",
            "metadata": {"operationMetadataId": "a1000000-0000-0000-0000-00000000000d"},
        },
    },
    "outputs": {},
}

# ---------------------------------------------------------------- manifests

apis_map = {
    "shared_sharepointonline": {
        "apiName": "shared_sharepointonline",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
    },
    "shared_office365": {
        "apiName": "shared_office365",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
    },
}

manifest = {
    "schema": "1.0",
    "details": {
        "displayName": "LU1 Activity 1 - Marina Trust Bank Onboarding",
        "description": (
            "Retail banking onboarding assistant. HTTP trigger, SharePoint duplicate "
            "check, Gemini decision against six ordered rules, SharePoint customer "
            "record and audit log, JSON response. Training lab - fictitious data."
        ),
        "createdTime": "2026-08-01T00:00:00Z",
        "packageTelemetryId": "a1000000-0000-0000-0000-0000000000ff",
        "creator": "Tertiary Infotech Academy",
        "sourceEnvironment": "",
    },
    "resources": {
        "a1000000-0000-0000-0000-0000000000f1": {
            "id": None,
            "name": "LU1MarinaTrustOnboarding",
            "type": "Microsoft.Flow/flows",
            "suggestedCreationType": "New",
            "creationType": "New, Existing",
            "details": {"displayName": "LU1 Activity 1 - Marina Trust Bank Onboarding"},
            "configurableBy": "User",
            "hierarchy": "Root",
            "dependsOn": [
                "a1000000-0000-0000-0000-0000000000f2",
                "a1000000-0000-0000-0000-0000000000f3",
            ],
        },
        "a1000000-0000-0000-0000-0000000000f3": {
            "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
            "name": "shared_office365",
            "type": "Microsoft.PowerApps/apis",
            "suggestedCreationType": "Existing",
            "creationType": "Existing",
            "details": {
                "displayName": "Office 365 Outlook",
                "iconUri": "https://connectoricons-prod.azureedge.net/office365/icon.png",
            },
            "configurableBy": "System",
            "hierarchy": "Child",
            "dependsOn": [],
        },
        "a1000000-0000-0000-0000-0000000000f2": {
            "id": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
            "name": "shared_sharepointonline",
            "type": "Microsoft.PowerApps/apis",
            "suggestedCreationType": "Existing",
            "creationType": "Existing",
            "details": {
                "displayName": "SharePoint",
                "iconUri": "https://connectoricons-prod.azureedge.net/sharepointonline/icon.png",
            },
            "configurableBy": "System",
            "hierarchy": "Child",
            "dependsOn": [],
        },
    },
}

os.makedirs(FLOW_DIR, exist_ok=True)

with open(os.path.join(FLOW_DIR, "definition.json"), "w") as f:
    json.dump(definition, f, indent=2)

with open(os.path.join(FLOW_DIR, "apisMap.json"), "w") as f:
    json.dump(apis_map, f, indent=2)

# The importer looks for the manifest inside Microsoft.Flow/, not at the zip root.
# A copy is left at the root as well: some builds of the importer read it there.
for target in (
    os.path.join(BUILD, "Microsoft.Flow", "manifest.json"),
    os.path.join(BUILD, "manifest.json"),
):
    with open(target, "w") as f:
        json.dump(manifest, f, indent=2)

print("wrote definition.json, apisMap.json, manifest.json (root + Microsoft.Flow/)")
