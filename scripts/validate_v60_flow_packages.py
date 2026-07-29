#!/usr/bin/env python3
"""Validate the Version 6.0 legacy Power Automate import packages."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "labs"
EXPECTED = {
    "Lab1-Form-to-Email-Confirmation-NEW.zip": {
        "name": "Lab 1 - Form to Email Confirmation (NEW)",
        "trigger": "OpenApiConnectionWebhook",
        "trigger_operation": "CreateFormWebhook",
        "actions": {"Get_response_details", "Send_confirmation_email"},
    },
    "Lab2-Log-Enquiry-and-Send-Email-NEW.zip": {
        "name": "Lab 2 - Log the Enquiry and Send Email (NEW)",
        "trigger": "OpenApiConnectionWebhook",
        "trigger_operation": "CreateFormWebhook",
        "actions": {
            "Get_response_details",
            "Add_row_to_Enquiry_Log",
            "Send_confirmation_email",
        },
    },
    "Lab3-Event-Registration-Branching-NEW.zip": {
        "name": "Lab 3 - Event Registration Branching (NEW)",
        "trigger": "OpenApiConnectionWebhook",
        "trigger_operation": "CreateFormWebhook",
        "actions": {"Get_response_details", "Joining_the_Event"},
    },
    "Lab4-Leave-Application-Approval-NEW.zip": {
        "name": "Lab 4 - Leave Application Approval (NEW)",
        "trigger": "OpenApiConnectionWebhook",
        "trigger_operation": "CreateFormWebhook",
        "actions": {
            "Get_response_details",
            "Start_and_wait_for_approval",
            "Approval_outcome",
        },
    },
    "Lab7-Support-Request-Routing-NEW.zip": {
        "name": "Lab 7 - Support Request Routing (NEW)",
        "trigger": "OpenApiConnectionWebhook",
        "trigger_operation": "CreateFormWebhook",
        "actions": {"Get_response_details", "Support_Type_is_IT"},
    },
    "Lab8-Website-HTTP-Enquiry-NEW.zip": {
        "name": "Lab 8 - Website HTTP Enquiry (NEW)",
        "trigger": "Request",
        "trigger_operation": None,
        "actions": {"Email_administrator", "Response"},
    },
    "Lab9-Finance-Agent-Web-Chat-NEW.zip": {
        "name": "Lab 9 - Finance Agent Web Chat (NEW)",
        "trigger": "Request",
        "trigger_operation": None,
        "actions": {"Execute_Finance_Agent_and_wait", "Response"},
    },
    "Lab10-AI-Trading-Advisor-Website-NEW.zip": {
        "name": "Lab 10 - AI Trading Advisor Website (NEW)",
        "trigger": "Request",
        "trigger_operation": None,
        "actions": {
            "Get_1_minute_candles",
            "Get_15_minute_candles",
            "Get_1_hour_candles",
            "Get_recent_news",
            "Execute_Finance_Advisor_Agent_and_wait",
            "Response",
        },
    },
    "Lab11-Procurement-Request-Approval-NEW.zip": {
        "name": "Lab 11 - Procurement Request Approval Workflow (NEW)",
        "trigger": "OpenApiConnectionWebhook",
        "trigger_operation": "CreateFormWebhook",
        "actions": {
            "Get_response_details",
            "Start_and_wait_for_approval",
            "Check_approval_outcome",
        },
    },
}

SECRET_PATTERNS = [
    re.compile(r"https://[^\"'\s]+logic\.azure\.com/workflows/", re.I),
    re.compile(r"[?&]sig=[A-Za-z0-9_%\-]{16,}", re.I),
    re.compile(r"(?i)(api[_-]?key|token|secret)[\"']?\s*[:=]\s*[\"'][A-Za-z0-9_\-]{16,}"),
]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    packages = sorted(LABS.rglob("*-NEW.zip"))
    individuals = [path for path in packages if path.name in EXPECTED]
    if {path.name for path in individuals} != set(EXPECTED):
        missing = sorted(set(EXPECTED) - {path.name for path in individuals})
        extra = sorted({path.name for path in individuals} - set(EXPECTED))
        fail(f"package mismatch; missing={missing}; extra={extra}")

    for path in individuals:
        expected = EXPECTED[path.name]
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if "manifest.json" not in names:
                fail(f"{path.name}: manifest.json missing")
            if "Microsoft.Flow/flows/manifest.json" not in names:
                fail(f"{path.name}: Microsoft.Flow/flows/manifest.json missing")
            definition_name = next(
                (
                    name
                    for name in names
                    if name.startswith("Microsoft.Flow/flows/")
                    and name.endswith("/definition.json")
                ),
                None,
            )
            if not definition_name:
                fail(f"{path.name}: definition.json missing")
            manifest = json.loads(archive.read("manifest.json"))
            flow = json.loads(archive.read(definition_name))

        display_name = flow["properties"]["displayName"]
        if display_name != expected["name"]:
            fail(f"{path.name}: display name is {display_name!r}")
        if not display_name.endswith("(NEW)"):
            fail(f"{path.name}: missing (NEW) postfix")

        definition = flow["properties"]["definition"]
        triggers = definition["triggers"]
        if len(triggers) != 1:
            fail(f"{path.name}: expected exactly one trigger")
        trigger = next(iter(triggers.values()))
        trigger_type = trigger["type"]
        if trigger_type != expected["trigger"]:
            fail(f"{path.name}: trigger is {trigger_type}, expected {expected['trigger']}")
        trigger_operation = (
            trigger.get("inputs", {}).get("host", {}).get("operationId")
        )
        if trigger_operation != expected["trigger_operation"]:
            fail(
                f"{path.name}: trigger operation is {trigger_operation!r}, "
                f"expected {expected['trigger_operation']!r}"
            )
        missing_actions = expected["actions"] - set(definition["actions"])
        if missing_actions:
            fail(f"{path.name}: actions missing {sorted(missing_actions)}")
        if trigger_operation == "CreateFormWebhook":
            get_details = definition["actions"].get("Get_response_details")
            get_details_operation = (
                get_details.get("inputs", {}).get("host", {}).get("operationId")
                if get_details
                else None
            )
            if get_details_operation != "GetFormResponseById":
                fail(
                    f"{path.name}: Forms flow must retrieve response details; "
                    f"found {get_details_operation!r}"
                )

        resources = manifest["resources"]
        if flow["name"] not in resources:
            fail(f"{path.name}: flow resource missing from manifest")
        if resources[flow["name"]]["suggestedCreationType"] != "New":
            fail(f"{path.name}: flow import is not Create as new")

        payload = json.dumps({"manifest": manifest, "flow": flow})
        for pattern in SECRET_PATTERNS:
            if pattern.search(payload):
                fail(f"{path.name}: possible secret or live webhook detected")

    bundle = LABS / "Power-Automate-Lab-Import-Packages-NEW.zip"
    if not bundle.exists():
        fail("combined NEW bundle missing")
    with zipfile.ZipFile(bundle) as archive:
        bundle_names = set(archive.namelist())
    expected_bundle = {"README.md", *EXPECTED.keys()}
    if bundle_names != expected_bundle:
        fail(
            "combined bundle contents differ: "
            f"missing={sorted(expected_bundle - bundle_names)}, "
            f"extra={sorted(bundle_names - expected_bundle)}"
        )

    print("PASS: Version 6.0 Power Automate packages validated")
    print("  9 individual (NEW) flow packages")
    print("  Forms triggers: Labs 1–4, 7 and 11")
    print("  HTTP triggers: Labs 8–10")
    print("  No live webhook URLs, credentials, or tokens detected")


if __name__ == "__main__":
    main()
