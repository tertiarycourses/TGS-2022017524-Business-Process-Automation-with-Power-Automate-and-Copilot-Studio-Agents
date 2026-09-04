"""
wfapi.py — build Copilot Studio (new experience) WORKFLOWS as JSON and create them
in the Copilot Studio Training (Developer) environment through the Dataverse Web API.

Verified 2026-09-04 against the live tenant:
  * The Workflows list = Dataverse `workflows` rows with category=5, type=1, modernflowtype=1.
  * The designer stores the canvas as `clientdata.properties.definition.triggers.<trigger>.metadata.associatedData.graph`
    (nodes + edges + connectionReferences) and the compiled Logic-Apps actions in `definition.actions`.
  * The designer RE-COMPILES `actions` from the graph whenever the workflow is saved in the UI,
    so an API-created workflow only needs a correct GRAPH; open it, make any change (or none) and Save/Publish.
  * Drafts are only visible with the header `MSCRM.includeunpublished: true`.

Usage:
    from wfapi import *
    wf = Workflow("Lab 1 - Trigger and Actions (DO NOT DELETE)")
    start = wf.start_connector("When a new response is submitted", "shared_microsoftforms", "CreateFormWebhook",
                               inputs={"form_id": FORM_LAB1}, operation_type="OpenApiConnectionWebhook",
                               split_on="@triggerOutputs()?['body/value']")
    n1 = wf.connector("Get response details", "shared_microsoftforms", "Microsoft Forms", "GetFormResponseById",
                      {"form_id": FORM_LAB1, "response_id": "@triggerOutputs()?['body/resourceData/responseId']"})
    ...
    wf.chain(start, n1, n2)
    create(wf)
"""
import json, uuid, subprocess, os, sys, copy

SCRATCH = os.path.dirname(os.path.abspath(__file__))
ORG = "https://orgb195a02f.crm5.dynamics.com"
ENV_ID = "dd7a990d-5d41-e3a8-82ae-8ede6fe42d92"

# ---- known ids in the tenant (admin account) ---------------------------------------------------
FORM_LAB1 = "fhM3CmXWj0KZxBlaU1-dsJHN4KVxmTdLvxXfe8ZpcedUOUlUMkI3NjYwTFpXWERYS0s0RklSV1FKVS4u"   # Lab 1 - Course Enquiry Form
FORM_LAB3 = "fhM3CmXWj0KZxBlaU1-dsJHN4KVxmTdLvxXfe8ZpcedUNEszMTRJOVdCNzBVQkdFNDlNM05LMEc4RS4u"   # Lab 3 - Leave Application Form
TRAINER_EMAIL = "admin@tertiaryinfotech.onmicrosoft.com"

# connection references owned by the admin account (connectionreferences table, verified)
CONN = {
    "shared_microsoftforms":     ("new_sharedmicrosoftforms_1d67e88d", "shared-microsoftform-8af73895-2193-4fc8-8193-e432c05170a3"),
    "shared_office365":          ("new_sharedoffice365_a52e4c3d",      "shared-office365-2599ad3e-31dc-407f-bca5-97c5f216a882"),
    "shared_excelonlinebusiness":("new_sharedexcelonlinebusiness_ac935010", "shared-excelonlinebu-22709cc9-4a70-4fed-9f77-89ba3628bda6"),
    "shared_agentnode":          ("new_sharedagentnode_f07437c9",      "shared-agentnode-ff0bdafb-7982-4d43-896f-3f69023d3028"),
    "shared_sharepointonline":   ("new_sharedsharepointonline_9f92634a", "shared-sharepointonl-189de575-d3ef-4a59-837b-1eafd9ad9bef"),
    "shared_teams":              ("new_sharedteams_49623bcf",          "shared-teams-afae8bca-f10a-4a5b-9663-801043daff0d"),
    "shared_advancedapprovals":  ("new_sharedadvancedapprovals_9e27ab3d", "be21f80d62af446997b9cc4d05eb042f"),
}
ICON = {
    "shared_microsoftforms": "https://static.powerapps.com/resource/ppcr/releases/v1.0.1819/1.0.1819.4795/microsoftforms/icon.png",
}
DISPLAY = {
    "shared_microsoftforms": "Microsoft Forms", "shared_office365": "Office 365 Outlook",
    "shared_excelonlinebusiness": "Excel Online (Business)", "shared_sharepointonline": "SharePoint",
    "shared_teams": "Microsoft Teams", "shared_approvals": "Standard approvals",
    "shared_advancedapprovals": "Human review", "shared_agentnode": "Agent",
}

def _id(prefix): return f"{prefix}-{uuid.uuid4()}"

class Workflow:
    def __init__(self, name):
        self.name = name
        self.nodes, self.edges = [], []
        self.conn_refs = {}
        self.trigger_key = "manual"
        self.trigger_def = None
        self._x = 250

    # ---- helpers ------------------------------------------------------------------------------
    def _pos(self, y=256):
        x = self._x; self._x += 350
        return {"x": x, "y": y}

    def _use_conn(self, api, alias=None):
        alias = alias or api
        if api in CONN:
            logical, cname = CONN[api]
            self.conn_refs[alias] = {"api": {"name": api}, "connection": {"connectionReferenceLogicalName": logical},
                                     "runtimeSource": "embedded", "connectionName": cname}
        return alias

    def _add(self, node):
        self.nodes.append(node); return node["id"]

    # ---- triggers ------------------------------------------------------------------------------
    def start_manual(self, inputs=None):
        nid = _id("start")
        self.trigger_key = "manual"
        self.trigger_def = {"type": "Request", "kind": "Button",
                            "inputs": {"schema": {"type": "object", "properties": {}, "required": []}}}
        return self._add({"id": nid, "name": "Start", "type": "start", "version": 1, "position": self._pos(),
                          "data": {"config": {"triggerType": "manual"},
                                   "outcomes": [{"id": "default", "label": "Default",
                                                 "outcomeSchema": {"type": "object", "properties": {}, "required": []}}]}})

    def start_agent_call(self, name="When an agent calls the flow", schema=None):
        """Trigger for a workflow used as a tool of an agent. schema = JSON schema of the inputs."""
        nid = _id("start")
        schema = schema or {"type": "object", "properties": {}, "required": []}
        self.trigger_key = "manual"
        self.trigger_def = {"type": "Request", "kind": "Skills", "inputs": {"schema": schema}}
        return self._add({"id": nid, "name": name, "type": "start", "version": 1, "position": self._pos(),
                          "data": {"config": {"triggerType": "connector",
                                              "connector": {"apiName": "Skills", "operationName": "When_an_agent_calls_the_flow",
                                                            "displayName": name, "kind": "Skills",
                                                            "inputs": {"schema": schema}}},
                                   "outcomes": [{"id": "default", "label": "Default",
                                                 "outcomeSchema": {"type": "object", "description": "Trigger output (schema determined by connector)"}}]}})

    def start_http(self, name="When a HTTP request is received", schema=None, method="POST", anyone=True):
        nid = _id("start")
        schema = schema or {"type": "object", "properties": {}}
        self.trigger_key = "manual"
        self.trigger_def = {"type": "Request", "kind": "Http",
                            "inputs": {"method": method, "schema": schema,
                                       "triggerAuthenticationType": "All" if anyone else "Tenant"}}
        return self._add({"id": nid, "name": name, "type": "start", "version": 1, "position": self._pos(),
                          "data": {"config": {"triggerType": "http", "http": {"method": method, "schema": schema,
                                                                               "triggerAuthenticationType": "All" if anyone else "Tenant"}},
                                   "outcomes": [{"id": "default", "label": "Default"}]}})

    def start_connector(self, name, api, operation, inputs, operation_type="OpenApiConnectionWebhook", split_on=None, alias=None, ui_connector=None, outcome_schema=None):
        """ui_connector: the `data.config.connector` dict of the same trigger saved once by the UI (its parametersSchema /
        outputSchema / triggerBatchMode are needed for the designer to compile splitOn on batch webhooks such as Forms)."""
        nid = _id("start")
        alias = self._use_conn(api, alias or f"{api}-1")
        self.trigger_key = name.replace(" ", "_")
        self.trigger_def = {"type": operation_type,
                            "inputs": {"parameters": inputs,
                                       "host": {"apiId": f"/providers/Microsoft.PowerApps/apis/{api}", "operationId": operation,
                                                "connectionName": alias}}}
        if split_on: self.trigger_def["splitOn"] = split_on
        cfg = {"triggerType": "connector",
               "connector": {"apiName": api, "operationName": operation, "connectionName": alias, "inputs": inputs,
                             "displayName": name, "iconUri": ICON.get(api, ""), "brandColor": "", "operationType": operation_type}}
        if split_on: cfg["connector"]["triggerBatchMode"] = "Batch"
        if ui_connector:
            for k in ("parametersSchema", "outputSchema", "triggerBatchMode", "iconUri"):
                if k in ui_connector: cfg["connector"][k] = ui_connector[k]
        outcomes = [{"id": "default", "label": "Default"}]
        if outcome_schema: outcomes[0]["outcomeSchema"] = outcome_schema
        return self._add({"id": nid, "name": name, "type": "start", "version": 1, "position": self._pos(),
                          "data": {"config": cfg, "outcomes": outcomes}})

    # ---- action nodes --------------------------------------------------------------------------
    def connector(self, name, api, operation, params, display=None, operation_type="OpenApiConnection", alias=None, y=256):
        nid = _id("connector")
        alias = self._use_conn(api, alias or api)
        cfg = {"apiName": api, "displayName": display or DISPLAY.get(api, api), "operationName": operation,
               "connectionName": alias, "operationType": operation_type, "parameters": params}
        if api == "shared_advancedapprovals": cfg["paletteIconHint"] = "humanReview"
        return self._add({"id": nid, "name": name, "type": "connector", "version": 1, "position": self._pos(y),
                          "data": {"config": cfg, "outcomes": [{"id": "default", "label": "Default"}]}})

    def human_review(self, name, title, message, assigned_to=None, inputs=None, channel="Teams", y=256):
        """inputs: list of (label, kind) with kind in text | boolean | email | number | date. Outputs are published as
        body/<kind> (e.g. outputs('Human_review')?['body/boolean'] for the Yes/No answer, body/text for the text)."""
        inputs = inputs or [("Outcome", "boolean"), ("Name", "text")]
        hint = {"text": ("TEXT", "string", "Please enter your input"), "boolean": ("BOOLEAN", "boolean", "Please select yes or no"),
                "email": ("EMAIL", "string", "Please enter an email address"), "number": ("NUMBER", "number", "Please enter a number"),
                "date": ("DATE", "string", "Please select a date")}
        props, req, used = {}, [], {}
        for label, kind in inputs:
            key = kind if kind not in used else f"{kind}_{used[kind]}"
            used[kind] = used.get(kind, 0) + 1
            h, t, d = hint[kind]
            props[key] = {"title": label, "type": t, "x-ms-content-hint": h, "x-ms-dynamically-added": True, "description": d}
            req.append(key)
        params = {"RequestForInformationInput/channel": channel, "RequestForInformationInput/title": title,
                  "RequestForInformationInput/assignedTo": assigned_to or TRAINER_EMAIL,
                  "RequestForInformationInput/message": message,
                  "RequestForInformationInput/input": {"type": "object", "properties": props, "required": req}}
        return self.connector(name, "shared_advancedapprovals", "RequestForInformation", params,
                              display="Human review", operation_type="OpenApiConnectionWebhook", y=y)

    def agent(self, name, instructions, model="claude-opus-5", output_mode="text", schema=None, web_search=False, hitl=False, y=256):
        """Inline Agent node. output_mode: 'text' | 'structured' (with schema) ."""
        nid = _id("agent")
        self._use_conn("shared_agentnode")
        cfg = {"mode": "inline", "instructions": "", "botSchemaName": "", "isHitlEscalationEnabled": hitl,
               "webSearchEnabled": web_search, "inlineInstructions": instructions, "outputMode": output_mode,
               "inlineModel": model, "connectionName": "shared_agentnode"}
        if schema:
            cfg["jsonSchemaText"] = json.dumps(schema)
            cfg["jsonSchema"] = schema
        outcome = {"id": "default", "label": "Default",
                   "outcomeSchema": {"type": "object",
                                     "properties": {"message": {"type": "string", "title": "Agent Response", "description": "The agent response text"},
                                                    "activities": {"type": "array", "description": "Bot response activities (typing, message, and event types)"}},
                                     "required": ["activities"]}}
        if schema:
            outcome["outcomeSchema"]["properties"]["structuredOutput"] = schema
        return self._add({"id": nid, "name": name, "type": "agent", "version": 1, "position": self._pos(y),
                          "data": {"config": cfg, "outcomes": [outcome]}})

    def classify(self, name, input_expr, categories, examples=None, model="claude-opus-5", y=256):
        nid = _id("classifyOnInlineAgent")
        self._use_conn("shared_agentnode")
        cats = [{"id": str(uuid.uuid4()), "name": c} for c in categories]
        so = {"type": "object", "properties": {
                "category": {"type": "string", "title": "Category", "description": "The matched category name", "x-ms-property-name-alias": "body/structuredOutput/predictedCategory"},
                "confidence": {"type": "number", "title": "Confidence", "description": "Confidence score for the classification (0-1)"},
                "input": {"type": "string", "title": "Input", "description": "The original input that was classified"}},
              "required": ["category"], "title": ""}
        def oc(i, label):
            return {"id": i, "label": label, "outcomeSchema": {"type": "object", "properties": {
                "message": {"type": "string", "title": "Agent Response", "description": "Aggregated message text emitted before the structured output (may be null)"},
                "activities": {"type": "array", "description": "Bot response activities (typing, message, and event types)"},
                "structuredOutput": so}, "required": ["activities", "structuredOutput"]}}
        outcomes = [oc(f"category:{c['id']}", c["name"]) for c in cats] + [oc("default-category", "Other")]
        node = {"id": nid, "name": name, "type": "classifyOnInlineAgent", "version": 1, "position": self._pos(y),
                "data": {"config": {"input": input_expr, "categories": cats, "examples": examples or [], "model": model,
                                    "connectionName": "shared_agentnode"}, "outcomes": outcomes}}
        self._add(node)
        return nid, {c["name"]: f"category:{c['id']}" for c in cats}

    def if_else(self, name, expression, y=256):
        """expression: a Logic-Apps condition dict, e.g. {"and":[{"equals":["@outputs('Human_review')?['body/boolean']", "Yes"]}]}
        or a (left, operator, right) tuple with operator in equals/notEquals/contains/greater/less/startsWith/endsWith."""
        if isinstance(expression, tuple):
            left, op, right = expression
            expression = {"and": [{op: [left, right]}]}
        if isinstance(expression, dict):
            expression = json.dumps(expression, indent=2)
        nid = _id("ifElse"); cid = str(uuid.uuid4())
        self._add({"id": nid, "name": name, "type": "ifElse", "version": 1, "position": self._pos(y),
                   "data": {"config": {"conditions": [{"id": cid, "name": "If", "expression": expression}]},
                            "outcomes": [{"id": f"condition:{cid}", "label": "If"}, {"id": "else", "label": "Else"}]}})
        return nid, f"condition:{cid}", "else"

    def switch(self, name, expression, cases, y=256):
        nid = _id("switch")
        cs = [{"id": str(uuid.uuid4()), "name": c, "value": c} for c in cases]
        self._add({"id": nid, "name": name, "type": "switch", "version": 1, "position": self._pos(y),
                   "data": {"config": {"expression": expression, "cases": cs},
                            "outcomes": [{"id": f"case:{c['id']}", "label": c["name"]} for c in cs] + [{"id": "default", "label": "Default"}]}})
        return nid, {c["name"]: f"case:{c['id']}" for c in cs}

    def variable(self, name, var_name, value, vtype="string", mode="initialize", y=256):
        nid = _id("variable")
        return self._add({"id": nid, "name": name, "type": "variable", "version": 1, "position": self._pos(y),
                          "data": {"config": {"assignments": [{"id": str(uuid.uuid4()), "variableName": var_name, "mode": mode, "type": vtype, "value": value}]},
                                   "outcomes": [{"id": "default", "label": "Default", "outcomeSchema": {"type": "object", "properties": {}, "description": "Variables set by this node"}}]}})

    def end(self, name="End", status="Succeeded", y=256):
        nid = _id("end")
        return self._add({"id": nid, "name": name, "type": "end", "version": 1, "position": self._pos(y),
                          "data": {"config": {"runStatus": status}, "outcomes": []}})

    def m365copilot(self, name, message, y=256):
        nid = _id("m365Copilot")
        return self._add({"id": nid, "name": name, "type": "m365Copilot", "version": 1, "position": self._pos(y),
                          "data": {"config": {"apiName": "shared_m365copilotv2", "displayName": "Copilot", "operationName": "StartChat",
                                              "parameters": {"body/timezone": "Asia/Singapore", "body/message": message},
                                              "operationType": "OpenApiConnection"},
                                   "outcomes": [{"id": "default", "label": "Default"}]}})

    # ---- edges ---------------------------------------------------------------------------------
    def edge(self, src, dst, source_handle=None, target_handle=None):
        e = {"id": f"edge-{src}-{dst}" + (f"-{source_handle}" if source_handle else ""), "source": src, "target": dst}
        if source_handle: e["sourceHandle"] = source_handle
        if target_handle: e["targetHandle"] = target_handle
        self.edges.append(e)

    def chain(self, *ids):
        for a, b in zip(ids, ids[1:]): self.edge(a, b)

    # ---- serialise -----------------------------------------------------------------------------
    def clientdata(self):
        graph = {"name": self.name, "nodes": self.nodes, "edges": self.edges, "connectionReferences": self.conn_refs}
        trig = copy.deepcopy(self.trigger_def or {"type": "Request", "kind": "Button", "inputs": {"schema": {"type": "object", "properties": {}, "required": []}}})
        trig["metadata"] = {"associatedData": {"graph": graph, "nodeActionMapping": {}}}
        definition = {"$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
                      "contentVersion": "1.0.0.0",
                      "parameters": {"$authentication": {"defaultValue": {}, "type": "SecureObject"}, "$connections": {"defaultValue": {}, "type": "Object"}},
                      "triggers": {self.trigger_key: trig}, "actions": {}, "outputs": {},
                      "metadata": {"telemetryMetadata": {"creationSource": "WorkflowDesigner", "modifiedSources": "WorkflowDesigner"}}}
        return {"properties": {"connectionReferences": self.conn_refs, "definition": definition}, "schemaVersion": "1.0.0.0"}


def token():
    """Dataverse bearer token: env DATAVERSE_TOKEN (preferred) or a gitignored token.txt next to this file.
    Never commit token.txt. Get the token from the signed-in browser session (see CLAUDE.md)."""
    t = os.environ.get("DATAVERSE_TOKEN", "").strip()
    if not t:
        p = os.path.join(SCRATCH, "token.txt")
        if not os.path.exists(p):
            raise SystemExit("No Dataverse token: export DATAVERSE_TOKEN='Bearer eyJ…' or write it to " + p)
        t = open(p).read().strip()
    return t if t.lower().startswith("bearer ") else "Bearer " + t

def _curl(method, url, body=None, extra=None):
    cmd = ["curl", "-s", "-i", "-X", method, url, "-H", f"Authorization: {token()}", "-H", "Accept: application/json",
           "-H", "OData-MaxVersion: 4.0", "-H", "OData-Version: 4.0", "-H", "MSCRM.includeunpublished: true",
           "-H", "Content-Type: application/json"]
    for h in (extra or []): cmd += ["-H", h]
    if body is not None:
        path = os.path.join(SCRATCH, "_body.json"); json.dump(body, open(path, "w"))
        cmd += ["--data-binary", "@" + path]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.replace("\r\n", "\n")
    head, _, rest = out.partition("\n\n")
    return head, rest

def find(name):
    import urllib.parse
    q = urllib.parse.quote(f"$select=workflowid,name,statecode,statuscode&$filter=name eq '{name.replace(chr(39), chr(39)*2)}' and category eq 5", safe="=$&',")
    head, body = _curl("GET", f"{ORG}/api/data/v9.2/workflows?{q}")
    try: return json.loads(body).get("value", [])
    except Exception: return []

def create(wf, replace=True):
    """Create (or replace) the workflow; returns workflowid."""
    if replace:
        for w in find(wf.name):
            _curl("DELETE", f"{ORG}/api/data/v9.2/workflows({w['workflowid']})")
            print("deleted old", w["workflowid"])
    body = {"name": wf.name, "category": 5, "type": 1, "modernflowtype": 1, "primaryentity": "none",
            "clientdata": json.dumps(wf.clientdata())}
    head, rest = _curl("POST", f"{ORG}/api/data/v9.2/workflows", body)
    status = head.split("\n")[0]
    wid = None
    for line in head.split("\n"):
        if line.lower().startswith("odata-entityid"):
            wid = line.split("(")[-1].rstrip(")")
    print(status, wf.name, wid)
    if not wid: print(rest[:600])
    return wid

def update(wid, wf):
    """PATCH clientdata. A published (statecode 1) workflow rejects the PATCH with 400 — it is deactivated first
    (statecode 0/statuscode 1); re-publish it in the designer afterwards."""
    body = {"clientdata": json.dumps(wf.clientdata()), "name": wf.name}
    head, rest = _curl("PATCH", f"{ORG}/api/data/v9.2/workflows({wid})", body)
    if head.split("\n")[0].endswith("400"):
        _curl("PATCH", f"{ORG}/api/data/v9.2/workflows({wid})", {"statecode": 0, "statuscode": 1})
        head, rest = _curl("PATCH", f"{ORG}/api/data/v9.2/workflows({wid})", body)
    print(head.split("\n")[0], wf.name); return head

def designer_url(wid):
    return f"https://copilotstudio.microsoft.com/environments/{ENV_ID}/flows/{wid}?creationMechanism=WorkflowsNew"
