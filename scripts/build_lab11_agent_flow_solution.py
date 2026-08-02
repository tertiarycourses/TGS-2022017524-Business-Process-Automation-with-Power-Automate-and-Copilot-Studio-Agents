#!/usr/bin/env python3
"""Build the Lab 11 connector-free agent-flow solution package."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "labs/Lab 11 - Travel Expense Agent and Agent Flow"
    / "Lab11-Check-Travel-Expense-Agent-Flow-Solution.zip"
)
FLOW_ID = "a6959ce7-6317-51f5-a776-a5d4a76f3411"
FLOW_NAME = "Lab 11 - Check Travel Expense Eligibility"
FLOW_FILENAME = f"Lab11CheckTravelExpenseEligibility-{FLOW_ID.upper()}.json"


def compose(inputs: str, run_after: dict[str, list[str]]) -> dict:
    return {
        "type": "Compose",
        "inputs": inputs,
        "runAfter": run_after,
    }


INPUTS = {
    "category": ("string", "Airfare, Hotel, Meal, Local Transport or Other"),
    "amountSGD": ("number", "Total claim amount in Singapore dollars"),
    "receiptAvailable": ("string", "Yes or No"),
    "businessPurpose": ("string", "Short work-related business purpose"),
    "preApproved": ("string", "Yes or No"),
    "daysSinceExpense": ("number", "Whole days since the expense"),
}

input_properties = {
    name: {
        "title": name,
        "type": data_type,
        "x-ms-dynamically-added": True,
        "description": description,
        "x-ms-content-hint": "NUMBER" if data_type == "number" else "TEXT",
    }
    for name, (data_type, description) in INPUTS.items()
}

decision_expression = (
    "@if(empty(trim(triggerBody()?['businessPurpose'])),"
    "'MORE_INFORMATION_REQUIRED',"
    "if(and(greater(float(triggerBody()?['amountSGD']),50),"
    "not(equals(toLower(triggerBody()?['receiptAvailable']),'yes'))),"
    "'MORE_INFORMATION_REQUIRED',"
    "if(greater(int(triggerBody()?['daysSinceExpense']),30),"
    "'HUMAN_REVIEW',"
    "if(and(equals(toLower(triggerBody()?['category']),'airfare'),"
    "not(equals(toLower(triggerBody()?['preApproved']),'yes'))),"
    "'HUMAN_REVIEW',"
    "if(and(equals(toLower(triggerBody()?['category']),'meal'),"
    "greater(float(triggerBody()?['amountSGD']),60)),"
    "'OUTSIDE_POLICY',"
    "if(and(equals(toLower(triggerBody()?['category']),'hotel'),"
    "greater(float(triggerBody()?['amountSGD']),300)),"
    "'OUTSIDE_POLICY',"
    "if(and(equals(toLower(triggerBody()?['category']),'local transport'),"
    "greater(float(triggerBody()?['amountSGD']),80)),"
    "'OUTSIDE_POLICY',"
    "if(not(or("
    "equals(toLower(triggerBody()?['category']),'airfare'),"
    "equals(toLower(triggerBody()?['category']),'hotel'),"
    "equals(toLower(triggerBody()?['category']),'meal'),"
    "equals(toLower(triggerBody()?['category']),'local transport'))),"
    "'HUMAN_REVIEW','ELIGIBLE_FOR_APPROVAL'))))))))"
)

reason_expression = (
    "@if(empty(trim(triggerBody()?['businessPurpose'])),"
    "'A business purpose is required.',"
    "if(and(greater(float(triggerBody()?['amountSGD']),50),"
    "not(equals(toLower(triggerBody()?['receiptAvailable']),'yes'))),"
    "'An itemised receipt is required above SGD 50.',"
    "if(greater(int(triggerBody()?['daysSinceExpense']),30),"
    "'Claims older than 30 days require human review.',"
    "if(and(equals(toLower(triggerBody()?['category']),'airfare'),"
    "not(equals(toLower(triggerBody()?['preApproved']),'yes'))),"
    "'Airfare without documented pre-approval requires human review.',"
    "if(and(equals(toLower(triggerBody()?['category']),'meal'),"
    "greater(float(triggerBody()?['amountSGD']),60)),"
    "'The meal amount is above the SGD 60 policy limit.',"
    "if(and(equals(toLower(triggerBody()?['category']),'hotel'),"
    "greater(float(triggerBody()?['amountSGD']),300)),"
    "'The hotel amount is above the SGD 300 per-night policy limit.',"
    "if(and(equals(toLower(triggerBody()?['category']),'local transport'),"
    "greater(float(triggerBody()?['amountSGD']),80)),"
    "'The local-transport amount is above the SGD 80 daily policy limit.',"
    "if(not(or("
    "equals(toLower(triggerBody()?['category']),'airfare'),"
    "equals(toLower(triggerBody()?['category']),'hotel'),"
    "equals(toLower(triggerBody()?['category']),'meal'),"
    "equals(toLower(triggerBody()?['category']),'local transport'))),"
    "'The category requires human interpretation.',"
    "'The supplied facts fit the published thresholds; a manager still makes "
    "the final approval.'))))))))"
)

ACTIONS = {
    "Evaluate_decision": compose(decision_expression, {}),
    "Explain_decision": compose(reason_expression, {"Evaluate_decision": ["Succeeded"]}),
    "Create_reference": compose(
        "@concat('EXP-',formatDateTime(utcNow(),'yyyyMMdd-HHmmss'))",
        {"Explain_decision": ["Succeeded"]},
    ),
}

FLOW = {
    "schemaVersion": "1.0.0.0",
    "properties": {
        "connectionReferences": {},
        "definition": {
            "$schema": (
                "https://schema.management.azure.com/providers/"
                "Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#"
            ),
            "contentVersion": "1.0.0.0",
            "parameters": {
                "$connections": {"defaultValue": {}, "type": "Object"},
                "$authentication": {"defaultValue": {}, "type": "SecureObject"},
            },
            "triggers": {
                "manual": {
                    "type": "Request",
                    "kind": "PowerVirtualAgents",
                    "inputs": {
                        "schema": {
                            "type": "object",
                            "properties": input_properties,
                            "required": list(INPUTS),
                        }
                    },
                }
            },
            "actions": ACTIONS
            | {
                "Respond_to_the_agent": {
                    "runAfter": {"Create_reference": ["Succeeded"]},
                    "type": "Response",
                    "kind": "PowerVirtualAgents",
                    "inputs": {
                        "statusCode": 200,
                        "body": {
                            "decision": "@outputs('Evaluate_decision')",
                            "reason": "@outputs('Explain_decision')",
                            "reference": "@outputs('Create_reference')",
                        },
                        "schema": {
                            "type": "object",
                            "properties": {
                                "decision": {
                                    "title": "decision",
                                    "type": "string",
                                    "x-ms-dynamically-added": True,
                                },
                                "reason": {
                                    "title": "reason",
                                    "type": "string",
                                    "x-ms-dynamically-added": True,
                                },
                                "reference": {
                                    "title": "reference",
                                    "type": "string",
                                    "x-ms-dynamically-added": True,
                                },
                            },
                        },
                    },
                }
            },
            "outputs": {},
        },
    },
}


def write_entry(archive: zipfile.ZipFile, name: str, content: str) -> None:
    info = zipfile.ZipInfo(name, date_time=(2026, 7, 25, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, content.encode("utf-8"))


SOLUTION_XML = f"""<?xml version="1.0" encoding="utf-8"?>
<ImportExportXml version="9.2.0.0" SolutionPackageVersion="9.2" languagecode="1033" generatedBy="CrmLive" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SolutionManifest>
    <UniqueName>TertiaryLab11TravelExpenseAgentFlow</UniqueName>
    <LocalizedNames>
      <LocalizedName description="Tertiary Lab 11 Travel Expense Agent Flow" languagecode="1033" />
    </LocalizedNames>
    <Descriptions>
      <Description description="Connector-free deterministic tool flow for the Lab 11 Expense Claim Agent." languagecode="1033" />
    </Descriptions>
    <Version>1.0.0.0</Version>
    <Managed>0</Managed>
    <Publisher>
      <UniqueName>TertiaryInfotechTraining</UniqueName>
      <LocalizedNames>
        <LocalizedName description="Tertiary Infotech Training" languagecode="1033" />
      </LocalizedNames>
      <Descriptions>
        <Description description="Reusable training solutions for Copilot Studio and Power Automate labs." languagecode="1033" />
      </Descriptions>
      <EMailAddress xsi:nil="true"></EMailAddress>
      <SupportingWebsiteUrl xsi:nil="true"></SupportingWebsiteUrl>
      <CustomizationPrefix>tif</CustomizationPrefix>
      <CustomizationOptionValuePrefix>52846</CustomizationOptionValuePrefix>
      <Addresses />
    </Publisher>
    <RootComponents>
      <RootComponent type="29" id="{{{FLOW_ID}}}" behavior="0" />
    </RootComponents>
    <MissingDependencies />
  </SolutionManifest>
</ImportExportXml>
"""

CUSTOMIZATIONS_XML = f"""<?xml version="1.0" encoding="utf-8"?>
<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Entities />
  <Roles />
  <Workflows>
    <Workflow WorkflowId="{{{FLOW_ID}}}" Name="{FLOW_NAME}">
      <JsonFileName>/Workflows/{FLOW_FILENAME}</JsonFileName>
      <Type>1</Type>
      <Subprocess>0</Subprocess>
      <Category>5</Category>
      <Mode>0</Mode>
      <Scope>4</Scope>
      <OnDemand>0</OnDemand>
      <TriggerOnCreate>0</TriggerOnCreate>
      <TriggerOnDelete>0</TriggerOnDelete>
      <AsyncAutodelete>0</AsyncAutodelete>
      <SyncWorkflowLogOnFailure>0</SyncWorkflowLogOnFailure>
      <RunAs>1</RunAs>
      <IsTransacted>1</IsTransacted>
      <IntroducedVersion>1.0.0.0</IntroducedVersion>
      <IsCustomizable>1</IsCustomizable>
      <BusinessProcessType>0</BusinessProcessType>
      <IsCustomProcessingStepAllowedForOtherPublishers>1</IsCustomProcessingStepAllowedForOtherPublishers>
      <PrimaryEntity>none</PrimaryEntity>
      <LocalizedNames>
        <LocalizedName languagecode="1033" description="{FLOW_NAME}" />
      </LocalizedNames>
    </Workflow>
  </Workflows>
  <FieldSecurityProfiles />
  <Templates />
  <EntityMaps />
  <EntityRelationships />
  <OrganizationSettings />
  <optionsets />
  <CustomControls />
  <EntityDataProviders />
  <connectionreferences />
  <Languages><Language>1033</Language></Languages>
</ImportExportXml>
"""

CONTENT_TYPES_XML = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="xml" ContentType="application/octet-stream" />
  <Default Extension="json" ContentType="application/octet-stream" />
</Types>
"""


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w") as archive:
        write_entry(archive, "solution.xml", SOLUTION_XML)
        write_entry(archive, "customizations.xml", CUSTOMIZATIONS_XML)
        write_entry(archive, "[Content_Types].xml", CONTENT_TYPES_XML)
        write_entry(archive, f"Workflows/{FLOW_FILENAME}", json.dumps(FLOW, indent=2))
    print(OUTPUT)


if __name__ == "__main__":
    main()
