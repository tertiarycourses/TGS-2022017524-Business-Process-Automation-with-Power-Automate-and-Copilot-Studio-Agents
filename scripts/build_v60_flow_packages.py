#!/usr/bin/env python3
"""Build Version 6.0 Power Automate legacy import packages.

The packages intentionally contain no tenant IDs, Form IDs, workbook IDs,
agent IDs, webhook URLs, API keys, or connection tokens. Importers reconnect
the listed connectors and select tenant-owned resources after import.
"""

from __future__ import annotations

import json
import tempfile
import uuid
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "labs"
CREATED_TIME = "2026-07-25T00:00:00Z"
NAMESPACE = uuid.UUID("b4bb93ee-b4f3-46e2-abba-f8304b7820a9")

CONNECTORS = {
    "shared_microsoftforms": ("Microsoft Forms", "microsoftforms"),
    "shared_office365": ("Office 365 Outlook", "office365"),
    "shared_excelonlinebusiness": ("Excel Online (Business)", "excelonlinebusiness"),
    "shared_approvals": ("Approvals", "approvals"),
    "shared_microsoftcopilotstudio": (
        "Microsoft Copilot Studio",
        "microsoftcopilotstudio",
    ),
}


def stable_uuid(label: str) -> str:
    return str(uuid.uuid5(NAMESPACE, label))


def forms_trigger() -> dict:
    return {
        "When_a_new_response_is_submitted": {
            "type": "OpenApiConnectionWebhook",
            "inputs": {
                "host": {
                    "connectionName": "shared_microsoftforms",
                    "operationId": "CreateFormWebhook",
                    "apiId": (
                        "/providers/Microsoft.PowerApps/apis/"
                        "shared_microsoftforms"
                    ),
                },
                "parameters": {"form_id": "SELECT_FORM_AFTER_IMPORT"},
                "authentication": "@parameters('$authentication')",
            },
        }
    }


def http_trigger(schema: dict) -> dict:
    return {
        "manual": {
            "type": "Request",
            "kind": "Http",
            "inputs": {"schema": schema},
        }
    }


def action(
    connector: str,
    operation: str,
    parameters: dict,
    run_after: dict,
) -> dict:
    return {
        "runAfter": run_after,
        "type": "OpenApiConnection",
        "inputs": {
            "host": {
                "connectionName": connector,
                "operationId": operation,
                "apiId": f"/providers/Microsoft.PowerApps/apis/{connector}",
            },
            "parameters": parameters,
            "authentication": "@parameters('$authentication')",
        },
    }


def get_response(run_after: dict | None = None) -> dict:
    return action(
        "shared_microsoftforms",
        "GetFormResponseById",
        {
            "form_id": "SELECT_FORM_AFTER_IMPORT",
            "response_id": "@triggerBody()?['resourceData/responseId']",
        },
        run_after or {},
    )


def email(to: str, subject: str, body: str, run_after: dict) -> dict:
    return action(
        "shared_office365",
        "SendEmailV2",
        {
            "emailMessage/To": to,
            "emailMessage/Subject": subject,
            "emailMessage/Body": body,
            "emailMessage/Importance": "Normal",
        },
        run_after,
    )


def add_excel_row(
    workbook: str,
    table: str,
    columns: dict[str, str],
    run_after: dict,
) -> dict:
    parameters = {
        "source": "me",
        "drive": "SELECT_ONEDRIVE_AFTER_IMPORT",
        "file": workbook,
        "table": table,
    }
    parameters.update({f"item/{key}": value for key, value in columns.items()})
    return action(
        "shared_excelonlinebusiness",
        "AddRowV2",
        parameters,
        run_after,
    )


def execute_agent(agent_placeholder: str, message: str, run_after: dict) -> dict:
    return action(
        "shared_microsoftcopilotstudio",
        "ExecuteCopilotAsyncV2",
        {
            "Copilot": agent_placeholder,
            "message": message,
            "locale": "en-US",
        },
        run_after,
    )


def http_response(body: dict, run_after: dict) -> dict:
    return {
        "type": "Response",
        "kind": "Http",
        "inputs": {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": body,
        },
        "runAfter": run_after,
    }


def workflow(
    display_name: str,
    triggers: dict,
    actions: dict,
    connectors: list[str],
) -> dict:
    flow_id = stable_uuid(display_name)
    parameters = {
        "$authentication": {"defaultValue": {}, "type": "SecureObject"},
    }
    if connectors:
        parameters["$connections"] = {"defaultValue": {}, "type": "Object"}
    return {
        "name": flow_id,
        "id": f"/providers/Microsoft.Flow/flows/{flow_id}",
        "type": "Microsoft.Flow/flows",
        "properties": {
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
            "displayName": display_name,
            "definition": {
                "$schema": (
                    "https://schema.management.azure.com/providers/"
                    "Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#"
                ),
                "contentVersion": "1.0.0.0",
                "parameters": parameters,
                "triggers": triggers,
                "actions": actions,
                "outputs": {},
            },
            "connectionReferences": {
                connector: {
                    "connectionName": connector.replace("_", "-"),
                    "source": "Embedded",
                    "id": f"/providers/Microsoft.PowerApps/apis/{connector}",
                    "tier": "NotSpecified",
                    "apiName": CONNECTORS[connector][1],
                    "isProcessSimpleApiReferenceConversionAlreadyDone": False,
                }
                for connector in connectors
            },
            "flowFailureAlertSubscribed": False,
            "isManaged": False,
        },
    }


def lab_specs() -> list[dict]:
    lab1 = workflow(
        "Lab 1 - Form to Email Confirmation (NEW)",
        forms_trigger(),
        {
            "Get_response_details": get_response(),
            "Send_confirmation_email": email(
                "MAP_EMAIL_ANSWER_AFTER_IMPORT",
                "Thank you for your enquiry",
                (
                    "<p>Hello MAP_NAME_ANSWER_AFTER_IMPORT,</p>"
                    "<p>Thank you for contacting us. We received your message:</p>"
                    "<p><em>MAP_MESSAGE_ANSWER_AFTER_IMPORT</em></p>"
                    "<p>We will respond using the contact details you supplied.</p>"
                ),
                {"Get_response_details": ["Succeeded"]},
            ),
        },
        ["shared_microsoftforms", "shared_office365"],
    )

    lab2 = workflow(
        "Lab 2 - Log the Enquiry and Send Email (NEW)",
        forms_trigger(),
        {
            "Get_response_details": get_response(),
            "Add_row_to_Enquiry_Log": add_excel_row(
                "SELECT_ENQUIRY_LOG_XLSX_AFTER_IMPORT",
                "EnquiryLog",
                {
                    "Timestamp": "@utcNow()",
                    "Name": "MAP_NAME_ANSWER_AFTER_IMPORT",
                    "Email": "MAP_EMAIL_ANSWER_AFTER_IMPORT",
                    "Tel": "MAP_TEL_ANSWER_AFTER_IMPORT",
                    "Message": "MAP_MESSAGE_ANSWER_AFTER_IMPORT",
                    "Status": "New",
                    "Source": "Microsoft Forms",
                },
                {"Get_response_details": ["Succeeded"]},
            ),
            "Send_confirmation_email": email(
                "MAP_EMAIL_ANSWER_AFTER_IMPORT",
                "Thank you for your enquiry",
                (
                    "<p>Hello MAP_NAME_ANSWER_AFTER_IMPORT,</p>"
                    "<p>Your enquiry has been logged successfully.</p>"
                ),
                {"Add_row_to_Enquiry_Log": ["Succeeded"]},
            ),
        },
        [
            "shared_microsoftforms",
            "shared_excelonlinebusiness",
            "shared_office365",
        ],
    )

    yes_actions = {
        "Add_Yes_row_to_Event_Log": add_excel_row(
            "SELECT_EVENT_LOG_XLSX_AFTER_IMPORT",
            "EventLog",
            {
                "Timestamp": "@utcNow()",
                "Name": "MAP_NAME_ANSWER_AFTER_IMPORT",
                "Email": "MAP_EMAIL_ANSWER_AFTER_IMPORT",
                "Tel": "MAP_TEL_ANSWER_AFTER_IMPORT",
                "JoiningEvent": "Yes",
                "NotificationSent": "Administrator",
                "Notes": "Joining the event",
            },
            {},
        ),
        "Email_participant_details_to_admin": email(
            "training1@tertiaryinfotech.onmicrosoft.com",
            "Event participant: MAP_NAME_ANSWER_AFTER_IMPORT",
            (
                "<p>Name: MAP_NAME_ANSWER_AFTER_IMPORT<br>"
                "Email: MAP_EMAIL_ANSWER_AFTER_IMPORT<br>"
                "Tel: MAP_TEL_ANSWER_AFTER_IMPORT</p>"
            ),
            {"Add_Yes_row_to_Event_Log": ["Succeeded"]},
        ),
    }
    no_actions = {
        "Add_No_row_to_Event_Log": add_excel_row(
            "SELECT_EVENT_LOG_XLSX_AFTER_IMPORT",
            "EventLog",
            {
                "Timestamp": "@utcNow()",
                "Name": "MAP_NAME_ANSWER_AFTER_IMPORT",
                "Email": "MAP_EMAIL_ANSWER_AFTER_IMPORT",
                "Tel": "MAP_TEL_ANSWER_AFTER_IMPORT",
                "JoiningEvent": "No",
                "NotificationSent": "User",
                "Notes": "Not joining this event",
            },
            {},
        ),
        "Email_thanks_to_user": email(
            "MAP_EMAIL_ANSWER_AFTER_IMPORT",
            "Thank you for your response",
            (
                "<p>Hello MAP_NAME_ANSWER_AFTER_IMPORT,</p>"
                "<p>Thank you for letting us know. We look forward to "
                "welcoming you at a future event.</p>"
            ),
            {"Add_No_row_to_Event_Log": ["Succeeded"]},
        ),
    }
    lab3 = workflow(
        "Lab 3 - Event Registration Branching (NEW)",
        forms_trigger(),
        {
            "Get_response_details": get_response(),
            "Joining_the_Event": {
                "type": "If",
                "expression": {
                    "and": [
                        {
                            "equals": [
                                "MAP_JOINING_EVENT_ANSWER_AFTER_IMPORT",
                                "Yes",
                            ]
                        }
                    ]
                },
                "actions": yes_actions,
                "else": {"actions": no_actions},
                "runAfter": {"Get_response_details": ["Succeeded"]},
            },
        },
        [
            "shared_microsoftforms",
            "shared_excelonlinebusiness",
            "shared_office365",
        ],
    )

    approval = action(
        "shared_approvals",
        "StartAndWaitForAnApproval",
        {
            "approvalType": "Basic",
            "WebhookApprovalCreationInput/title": (
                "Leave request: MAP_NAME_ANSWER_AFTER_IMPORT"
            ),
            "WebhookApprovalCreationInput/assignedTo": (
                "training1@tertiaryinfotech.onmicrosoft.com"
            ),
            "WebhookApprovalCreationInput/details": (
                "Employee: MAP_NAME_ANSWER_AFTER_IMPORT<br>"
                "From: MAP_LEAVE_FROM_ANSWER_AFTER_IMPORT<br>"
                "To: MAP_LEAVE_TO_ANSWER_AFTER_IMPORT<br>"
                "Type: MAP_LEAVE_TYPE_ANSWER_AFTER_IMPORT<br>"
                "Reason: MAP_REASON_ANSWER_AFTER_IMPORT"
            ),
            "WebhookApprovalCreationInput/enableNotifications": True,
            "WebhookApprovalCreationInput/enableReassignment": True,
        },
        {"Get_response_details": ["Succeeded"]},
    )
    # This Approvals operation waits for an external response and is exposed
    # by the connector as a webhook operation, not a standard connection call.
    approval["type"] = "OpenApiConnectionWebhook"
    lab4 = workflow(
        "Lab 4 - Leave Application Approval (NEW)",
        forms_trigger(),
        {
            "Get_response_details": get_response(),
            "Start_and_wait_for_approval": approval,
            "Approval_outcome": {
                "type": "If",
                "expression": {
                    "and": [
                        {
                            "equals": [
                                (
                                    "@outputs('Start_and_wait_for_approval')"
                                    "?['body/outcome']"
                                ),
                                "Approve",
                            ]
                        }
                    ]
                },
                "actions": {
                    "Email_approved_result": email(
                        "@outputs('Get_response_details')?['body/responder']",
                        "Leave application approved",
                        (
                            "<p>Your leave request has been approved.</p>"
                            "<p>Manager comments: "
                            "@{outputs('Start_and_wait_for_approval')"
                            "?['body/responses'][0]['comments']}</p>"
                        ),
                        {},
                    )
                },
                "else": {
                    "actions": {
                        "Email_rejected_result": email(
                            "@outputs('Get_response_details')?['body/responder']",
                            "Leave application not approved",
                            (
                                "<p>Your leave request was not approved.</p>"
                                "<p>Manager comments: "
                                "@{outputs('Start_and_wait_for_approval')"
                                "?['body/responses'][0]['comments']}</p>"
                            ),
                            {},
                        )
                    }
                },
                "runAfter": {"Start_and_wait_for_approval": ["Succeeded"]},
            },
        },
        ["shared_microsoftforms", "shared_approvals", "shared_office365"],
    )

    it_message = (
        "Support request from MAP_NAME_ANSWER_AFTER_IMPORT. "
        "Message: MAP_MESSAGE_ANSWER_AFTER_IMPORT"
    )
    lab7 = workflow(
        "Lab 7 - Support Request Routing (NEW)",
        forms_trigger(),
        {
            "Get_response_details": get_response(),
            "Support_Type_is_IT": {
                "type": "If",
                "expression": {
                    "and": [
                        {
                            "equals": [
                                "MAP_SUPPORT_TYPE_ANSWER_AFTER_IMPORT",
                                "IT Support",
                            ]
                        }
                    ]
                },
                "actions": {
                    "Execute_IT_Support_Agent_and_wait": execute_agent(
                        "SELECT_IT_SUPPORT_AGENT_AFTER_IMPORT",
                        it_message,
                        {},
                    ),
                    "Email_IT_Agent_reply": email(
                        "MAP_EMAIL_ANSWER_AFTER_IMPORT",
                        "Your IT support response",
                        (
                            "<p>@{string(body("
                            "'Execute_IT_Support_Agent_and_wait'))}</p>"
                        ),
                        {"Execute_IT_Support_Agent_and_wait": ["Succeeded"]},
                    ),
                },
                "else": {
                    "actions": {
                        "Execute_HR_Support_Agent_and_wait": execute_agent(
                            "SELECT_HR_SUPPORT_AGENT_AFTER_IMPORT",
                            it_message,
                            {},
                        ),
                        "Email_HR_Agent_reply": email(
                            "MAP_EMAIL_ANSWER_AFTER_IMPORT",
                            "Your HR support response",
                            (
                                "<p>@{string(body("
                                "'Execute_HR_Support_Agent_and_wait'))}</p>"
                            ),
                            {"Execute_HR_Support_Agent_and_wait": ["Succeeded"]},
                        ),
                    }
                },
                "runAfter": {"Get_response_details": ["Succeeded"]},
            },
        },
        [
            "shared_microsoftforms",
            "shared_microsoftcopilotstudio",
            "shared_office365",
        ],
    )

    enquiry_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "tel": {"type": "string"},
            "message": {"type": "string"},
        },
        "required": ["name", "email", "tel", "message"],
    }
    lab8 = workflow(
        "Lab 8 - Website HTTP Enquiry (NEW)",
        http_trigger(enquiry_schema),
        {
            "Email_administrator": email(
                "training1@tertiaryinfotech.onmicrosoft.com",
                "Website enquiry from @{triggerBody()?['name']}",
                (
                    "<p>Name: @{triggerBody()?['name']}<br>"
                    "Email: @{triggerBody()?['email']}<br>"
                    "Tel: @{triggerBody()?['tel']}<br>"
                    "Message: @{triggerBody()?['message']}</p>"
                ),
                {},
            ),
            "Response": http_response(
                {
                    "success": True,
                    "message": "Thank you. Your enquiry has been received.",
                },
                {"Email_administrator": ["Succeeded"]},
            ),
        },
        ["shared_office365"],
    )

    prompt_schema = {
        "type": "object",
        "properties": {
            "sessionId": {"type": "string"},
            "prompt": {"type": "string"},
        },
        "required": ["sessionId", "prompt"],
    }
    lab9 = workflow(
        "Lab 9 - Finance Agent Web Chat (NEW)",
        http_trigger(prompt_schema),
        {
            "Execute_Finance_Agent_and_wait": execute_agent(
                "SELECT_FINANCE_INFORMATION_AGENT_AFTER_IMPORT",
                "@triggerBody()?['prompt']",
                {},
            ),
            "Response": http_response(
                {
                    "reply": (
                        "@{string(body("
                        "'Execute_Finance_Agent_and_wait'))}"
                    ),
                    "disclaimer": (
                        "Educational information only; not personalised "
                        "financial advice."
                    ),
                },
                {"Execute_Finance_Agent_and_wait": ["Succeeded"]},
            ),
        },
        ["shared_microsoftcopilotstudio"],
    )

    trading_schema = {
        "type": "object",
        "properties": {
            "symbol": {"type": "string"},
            "prompt": {"type": "string"},
        },
        "required": ["symbol", "prompt"],
    }
    lab10 = workflow(
        "Lab 10 - AI Trading Advisor Website (NEW)",
        http_trigger(trading_schema),
        {
            "Get_1_minute_candles": {
                "type": "Http",
                "inputs": {
                    "method": "GET",
                    "uri": (
                        "https://api.twelvedata.com/time_series?"
                        "symbol=@{uriComponent(triggerBody()?['symbol'])}"
                        "&interval=1min&outputsize=50"
                        "&apikey=REPLACE_TWELVE_DATA_KEY_AFTER_IMPORT"
                    ),
                },
                "runAfter": {},
            },
            "Get_15_minute_candles": {
                "type": "Http",
                "inputs": {
                    "method": "GET",
                    "uri": (
                        "https://api.twelvedata.com/time_series?"
                        "symbol=@{uriComponent(triggerBody()?['symbol'])}"
                        "&interval=15min&outputsize=50"
                        "&apikey=REPLACE_TWELVE_DATA_KEY_AFTER_IMPORT"
                    ),
                },
                "runAfter": {"Get_1_minute_candles": ["Succeeded"]},
            },
            "Get_1_hour_candles": {
                "type": "Http",
                "inputs": {
                    "method": "GET",
                    "uri": (
                        "https://api.twelvedata.com/time_series?"
                        "symbol=@{uriComponent(triggerBody()?['symbol'])}"
                        "&interval=1h&outputsize=50"
                        "&apikey=REPLACE_TWELVE_DATA_KEY_AFTER_IMPORT"
                    ),
                },
                "runAfter": {"Get_15_minute_candles": ["Succeeded"]},
            },
            "Get_recent_news": {
                "type": "Http",
                "inputs": {
                    "method": "GET",
                    "uri": (
                        "https://newsapi.org/v2/everything?"
                        "q=@{uriComponent(triggerBody()?['symbol'])}"
                        "&pageSize=5&apiKey=REPLACE_NEWSAPI_KEY_AFTER_IMPORT"
                    ),
                },
                "runAfter": {"Get_1_hour_candles": ["Succeeded"]},
            },
            "Execute_Finance_Advisor_Agent_and_wait": execute_agent(
                "SELECT_FINANCE_ADVISOR_AGENT_AFTER_IMPORT",
                (
                    "Analyse @{triggerBody()?['symbol']} for the learner's "
                    "question: @{triggerBody()?['prompt']}. Compare this "
                    "1-minute data: @{string(body('Get_1_minute_candles'))}; "
                    "15-minute data: @{string(body('Get_15_minute_candles'))}; "
                    "1-hour data: @{string(body('Get_1_hour_candles'))}; "
                    "and recent news: @{string(body('Get_recent_news'))}. "
                    "State uncertainty and provide educational analysis only."
                ),
                {"Get_recent_news": ["Succeeded"]},
            ),
            "Response": http_response(
                {
                    "symbol": "@{triggerBody()?['symbol']}",
                    "analysis": (
                        "@{string(body("
                        "'Execute_Finance_Advisor_Agent_and_wait'))}"
                    ),
                    "riskNote": (
                        "Educational analysis only; not personalised "
                        "financial advice."
                    ),
                },
                {"Execute_Finance_Advisor_Agent_and_wait": ["Succeeded"]},
            ),
        },
        ["shared_microsoftcopilotstudio"],
    )

    procurement_approval = action(
        "shared_approvals",
        "StartAndWaitForAnApproval",
        {
            "approvalType": "Basic",
            "WebhookApprovalCreationInput/title": (
                "Procurement request: MAP_ITEM_ANSWER_AFTER_IMPORT"
            ),
            "WebhookApprovalCreationInput/assignedTo": (
                "training1@tertiaryinfotech.onmicrosoft.com"
            ),
            "WebhookApprovalCreationInput/details": (
                "Requester: MAP_REQUESTER_NAME_ANSWER_AFTER_IMPORT<br>"
                "Email: MAP_REQUESTER_EMAIL_ANSWER_AFTER_IMPORT<br>"
                "Item: MAP_ITEM_ANSWER_AFTER_IMPORT<br>"
                "Quantity: MAP_QUANTITY_ANSWER_AFTER_IMPORT<br>"
                "Estimated cost: SGD MAP_ESTIMATED_COST_ANSWER_AFTER_IMPORT<br>"
                "Business reason: MAP_BUSINESS_REASON_ANSWER_AFTER_IMPORT"
            ),
            "WebhookApprovalCreationInput/enableNotifications": True,
            "WebhookApprovalCreationInput/enableReassignment": True,
        },
        {"Get_response_details": ["Succeeded"]},
    )
    procurement_approval["type"] = "OpenApiConnectionWebhook"
    lab11 = workflow(
        "Lab 11 - Procurement Request Approval Workflow (NEW)",
        forms_trigger(),
        {
            "Get_response_details": get_response(),
            "Start_and_wait_for_approval": procurement_approval,
            "Check_approval_outcome": {
                "type": "If",
                "expression": {
                    "and": [
                        {
                            "equals": [
                                (
                                    "@outputs('Start_and_wait_for_approval')"
                                    "?['body/outcome']"
                                ),
                                "Approve",
                            ]
                        }
                    ]
                },
                "actions": {
                    "Send_approval_email": email(
                        "MAP_REQUESTER_EMAIL_ANSWER_AFTER_IMPORT",
                        (
                            "Procurement request approved: "
                            "MAP_ITEM_ANSWER_AFTER_IMPORT"
                        ),
                        (
                            "<p>Hello MAP_REQUESTER_NAME_ANSWER_AFTER_IMPORT,</p>"
                            "<p>Your request for "
                            "MAP_QUANTITY_ANSWER_AFTER_IMPORT × "
                            "MAP_ITEM_ANSWER_AFTER_IMPORT has been approved.</p>"
                            "<p>Approver comments: "
                            "@{outputs('Start_and_wait_for_approval')"
                            "?['body/responses'][0]['comments']}</p>"
                        ),
                        {},
                    )
                },
                "else": {
                    "actions": {
                        "Send_rejection_email": email(
                            "MAP_REQUESTER_EMAIL_ANSWER_AFTER_IMPORT",
                            (
                                "Procurement request not approved: "
                                "MAP_ITEM_ANSWER_AFTER_IMPORT"
                            ),
                            (
                                "<p>Hello "
                                "MAP_REQUESTER_NAME_ANSWER_AFTER_IMPORT,</p>"
                                "<p>Your request for "
                                "MAP_QUANTITY_ANSWER_AFTER_IMPORT × "
                                "MAP_ITEM_ANSWER_AFTER_IMPORT was not approved."
                                "</p><p>Approver comments: "
                                "@{outputs('Start_and_wait_for_approval')"
                                "?['body/responses'][0]['comments']}</p>"
                            ),
                            {},
                        )
                    }
                },
                "runAfter": {"Start_and_wait_for_approval": ["Succeeded"]},
            },
        },
        ["shared_microsoftforms", "shared_approvals", "shared_office365"],
    )

    return [
        {
            "id": "lab_1",
            "folder": "Lab 1 - Forms Email Confirmation",
            "filename": "Lab1-Form-to-Email-Confirmation-NEW.zip",
            "description": "Forms response, response details and user confirmation email.",
            "connectors": ["shared_microsoftforms", "shared_office365"],
            "flow": lab1,
        },
        {
            "id": "lab_2",
            "folder": "Lab 2 - Forms Enquiry Logging",
            "filename": "Lab2-Log-Enquiry-and-Send-Email-NEW.zip",
            "description": "Forms response, Enquiry Log.xlsx row and confirmation email.",
            "connectors": [
                "shared_microsoftforms",
                "shared_excelonlinebusiness",
                "shared_office365",
            ],
            "flow": lab2,
        },
        {
            "id": "lab_3",
            "folder": "Lab 3 - Event Registration Branching",
            "filename": "Lab3-Event-Registration-Branching-NEW.zip",
            "description": "Forms response, Yes/No branch, Event Log.xlsx and email.",
            "connectors": [
                "shared_microsoftforms",
                "shared_excelonlinebusiness",
                "shared_office365",
            ],
            "flow": lab3,
        },
        {
            "id": "lab_4",
            "folder": "Lab 4 - Leave Approval",
            "filename": "Lab4-Leave-Application-Approval-NEW.zip",
            "description": "Leave form, manager approval and outcome emails.",
            "connectors": [
                "shared_microsoftforms",
                "shared_approvals",
                "shared_office365",
            ],
            "flow": lab4,
        },
        {
            "id": "lab_7",
            "folder": "Lab 7 - Support Request Routing",
            "filename": "Lab7-Support-Request-Routing-NEW.zip",
            "description": "Forms response routed to IT or HR agent, then emailed.",
            "connectors": [
                "shared_microsoftforms",
                "shared_microsoftcopilotstudio",
                "shared_office365",
            ],
            "flow": lab7,
        },
        {
            "id": "lab_8",
            "folder": "Lab 8 - Website HTTP Enquiry",
            "filename": "Lab8-Website-HTTP-Enquiry-NEW.zip",
            "description": "Website HTTP request, admin email and JSON response.",
            "connectors": ["shared_office365"],
            "flow": lab8,
        },
        {
            "id": "lab_9",
            "folder": "Lab 9 - Finance Agent Web Chat",
            "filename": "Lab9-Finance-Agent-Web-Chat-NEW.zip",
            "description": "Website prompt, Finance agent and JSON response.",
            "connectors": ["shared_microsoftcopilotstudio"],
            "flow": lab9,
        },
        {
            "id": "lab_10",
            "folder": "Lab 10 - AI Trading Advisor Website",
            "filename": "Lab10-AI-Trading-Advisor-Website-NEW.zip",
            "description": "Multi-timeframe data, news, Finance Advisor agent and JSON.",
            "connectors": ["shared_microsoftcopilotstudio"],
            "flow": lab10,
        },
        {
            "id": "lab_11",
            "folder": "Lab 11 - Procurement Request Approval",
            "filename": "Lab11-Procurement-Request-Approval-NEW.zip",
            "description": (
                "Procurement form, human approval and outcome notification emails."
            ),
            "connectors": [
                "shared_microsoftforms",
                "shared_approvals",
                "shared_office365",
            ],
            "flow": lab11,
        },
    ]


def package_manifest(spec: dict) -> tuple[dict, dict, dict]:
    flow = spec["flow"]
    flow_id = flow["name"]
    resources: dict[str, dict] = {}
    dependencies: list[str] = []
    apis_map: dict[str, str] = {}
    connections_map: dict[str, str] = {}
    for connector in spec["connectors"]:
        api_uuid = stable_uuid(f"{flow_id}:{connector}:api")
        connection_uuid = stable_uuid(f"{flow_id}:{connector}:connection")
        connection_name = connector.replace("_", "-")
        display, icon_slug = CONNECTORS[connector]
        icon = (
            "https://connectoricons-prod.azureedge.net/releases/"
            f"v1.0.1664/1.0.1664.3477/{icon_slug}/icon.png"
        )
        dependencies.extend([api_uuid, connection_uuid])
        apis_map[connector] = api_uuid
        connections_map[connector] = connection_uuid
        resources[api_uuid] = {
            "id": f"/providers/Microsoft.PowerApps/apis/{connector}",
            "name": connector,
            "type": "Microsoft.PowerApps/apis",
            "suggestedCreationType": "Existing",
            "creationType": "Existing",
            "details": {"displayName": display, "iconUri": icon},
            "configurableBy": "System",
            "hierarchy": "Child",
            "dependsOn": [],
        }
        resources[connection_uuid] = {
            "type": "Microsoft.PowerApps/apis/connections",
            "suggestedCreationType": "Existing",
            "creationType": "Existing",
            "details": {"displayName": display, "iconUri": icon},
            "configurableBy": "User",
            "hierarchy": "Child",
            "dependsOn": [api_uuid],
        }
    resources[flow_id] = {
        "id": f"/providers/Microsoft.Flow/flows/{flow_id}",
        "name": flow_id,
        "type": "Microsoft.Flow/flows",
        "suggestedCreationType": "New",
        "creationType": "Existing, New, Update",
        "details": {"displayName": flow["properties"]["displayName"]},
        "configurableBy": "User",
        "hierarchy": "Root",
        "dependsOn": dependencies,
    }
    return (
        {
            "schema": "1.0",
            "details": {
                "displayName": flow["properties"]["displayName"],
                "description": (
                    f"{spec['description']} Version 6.0 teaching package; "
                    "reconnect connectors and map tenant resources after import."
                ),
                "createdTime": CREATED_TIME,
                "packageTelemetryId": stable_uuid(f"{flow_id}:telemetry"),
                "creator": "Tertiary Infotech Academy",
                "sourceEnvironment": "",
            },
            "resources": resources,
        },
        apis_map,
        connections_map,
    )


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def build_package(spec: dict) -> Path:
    destination = LABS / spec["folder"] / spec["filename"]
    manifest, apis_map, connections_map = package_manifest(spec)
    flow_id = spec["flow"]["name"]
    with tempfile.TemporaryDirectory() as temp_name:
        temp = Path(temp_name)
        flow_folder = temp / "Microsoft.Flow" / "flows" / flow_id
        flow_folder.mkdir(parents=True)
        write_json(temp / "manifest.json", manifest)
        # The provider manifest is separate from the root package manifest.
        # Power Automate's native exports place it under Microsoft.Flow/flows
        # and use it to enumerate the flow asset folders during final import.
        write_json(
            temp / "Microsoft.Flow" / "flows" / "manifest.json",
            {
                "packageSchemaVersion": "1.0",
                "flowAssets": {"assetPaths": [flow_id]},
            },
        )
        write_json(flow_folder / "definition.json", spec["flow"])
        write_json(flow_folder / "apisMap.json", apis_map)
        write_json(flow_folder / "connectionsMap.json", connections_map)
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(temp.rglob("*")):
                if path.is_file():
                    info = zipfile.ZipInfo(path.relative_to(temp).as_posix())
                    info.date_time = (2026, 7, 25, 0, 0, 0)
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, path.read_bytes())
    return destination


def build_bundle(packages: list[Path]) -> Path:
    bundle = LABS / "Power-Automate-Lab-Import-Packages-NEW.zip"
    guide = LABS / "IMPORT-PACKAGES.md"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in [guide, *packages]:
            info = zipfile.ZipInfo(
                "README.md" if path == guide else path.name,
                date_time=(2026, 7, 25, 0, 0, 0),
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    return bundle


def main() -> None:
    packages = [build_package(spec) for spec in lab_specs()]
    bundle = build_bundle(packages)
    for package in packages:
        print(package.relative_to(ROOT))
    print(bundle.relative_to(ROOT))


if __name__ == "__main__":
    main()
