"""Lab 6 - Raise Requisition (DO NOT DELETE): When an agent calls the flow (Item, Quantity, Justification, Requester)
-> Compose 'Reference' -> Excel Add a row into RequisitionLog -> Respond to the agent (Reference, Status)."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *
from wfapi_a import *

NAME = "Lab 6 - Raise Requisition (DO NOT DELETE)"
EXCEL = json.load(open(SCRATCH + "/excel-params.json")) if os.path.exists(SCRATCH + "/excel-params.json") else {}
EX = EXCEL.get("lab6") or {"source": "me", "drive": "me", "file": "/Power Automate Lab Data/Lab 6 - Requisition Log.xlsx", "table": "RequisitionLog"}
def inp(title, typ, desc, hint):
    return {"title": title, "type": typ, "x-ms-content-hint": hint, "x-ms-dynamically-added": True, "description": desc}
SCHEMA = {"type": "object", "properties": {
    "Item": inp("Item", "string", "What is to be bought, with the vendor name if known, e.g. Laptop 14-inch 16 GB from Tampines IT Distributors", "TEXT"),
    "Quantity": inp("Quantity", "number", "How many units", "NUMBER"),
    "Justification": inp("Justification", "string", "The business reason for the purchase", "TEXT"),
    "Requester": inp("Requester", "string", "Full name of the colleague raising the requisition", "TEXT")},
    "required": ["Item", "Quantity", "Justification", "Requester"]}
REF_EXPR = "@concat('REQ-', formatDateTime(utcNow(),'yyyyMMdd'), '-', toUpper(substring(replace(guid(),'-',''),0,6)))"

def build(stage=2):
    wf = Workflow(NAME)
    s = wf.start_agent_call(schema=SCHEMA)
    prev = s
    ref_out = REF_EXPR
    if hasattr(wf, "compose"):
        c = wf.compose("Reference", REF_EXPR)
        wf.edge(s, c); prev = c
        ref_out = "@outputs('Reference')"
    xl = wf.connector("Add a row into a table", "shared_excelonlinebusiness", "AddRowV2",
        {"source": EX["source"], "drive": EX["drive"], "file": EX["file"], "table": EX["table"],
         "item/Reference": ref_out, "item/Timestamp": "@utcNow()", "item/Requester": "@triggerBody()?['Requester']",
         "item/Item": "@triggerBody()?['Item']", "item/Quantity": "@triggerBody()?['Quantity']",
         "item/Justification": "@triggerBody()?['Justification']", "item/Status": "Submitted"})
    wf.edge(prev, xl)
    if stage >= 2 and hasattr(wf, "respond_to_agent"):
        r = wf.respond_to_agent("Respond to the agent", {"Reference": ref_out, "Status": "Submitted for approval"})
        wf.edge(xl, r)
    return wf

if __name__ == '__main__':
    stage = int(os.environ.get("STAGE", "2"))
    wf = build(stage)
    ids = json.load(open(SCRATCH + "/ids.json"))
    wid = create(wf); ids["lab6"] = wid; json.dump(ids, open(SCRATCH + "/ids.json", "w"), indent=1)
    print(designer_url(wid))
