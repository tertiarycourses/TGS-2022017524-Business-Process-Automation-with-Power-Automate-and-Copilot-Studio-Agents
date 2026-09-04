"""wfapi_a.py — extra node helpers verified live 2026-09-04 (agent A): Respond to the agent, Compose, M365 Copilot connection.
Import after wfapi: `from wfapi import *; from wfapi_a import *`."""
import json, uuid
import wfapi
from wfapi import Workflow, _id

# M365 Copilot node connection reference (created by the designer when the Copilot node was first saved, Lab 11)
wfapi.CONN["shared_m365copilotv2"] = ("new_sharedm365copilotv2_8997c730", "shared-m365copilotv2-1f7f5a7c-5abc-4f3d-ad8c-954767d4d850")

def respond_to_agent(self, name="Respond to the agent", outputs=None, y=256):
    """'Respond to the agent' node (+ menu → Agent → Respond to the agent). outputs: dict label -> value (string expression or literal);
    every output is a Text output. Graph: builtinFunction/operationId 'response'/kind 'Skills'; compiles to {"type":"Response","kind":"Skills",
    "inputs":{"schema":{...},"statusCode":200,"body":{...}}}. Property keys are 'text', 'text_1', ... (label kept in `title`)."""
    outputs = outputs or {}
    props, body, req = {}, {}, []
    for i, (label, value) in enumerate(outputs.items()):
        key = "text" if i == 0 else f"text_{i}"
        props[key] = {"title": label, "type": "string", "x-ms-content-hint": "TEXT", "x-ms-dynamically-added": True}
        body[key] = value; req.append(key)
    nid = _id("builtinFunction")
    return self._add({"id": nid, "name": name, "type": "builtinFunction", "version": 1, "position": self._pos(y),
                      "data": {"config": {"operationId": "response", "operationName": "response", "displayName": "Respond to the agent",
                                          "category": "request", "categoryDisplayName": "Request", "iconUri": "", "brandColor": "",
                                          "parameters": {"schema": {"type": "object", "properties": props, "required": req}, "body": body},
                                          "description": "Respond to the calling agent with typed outputs.", "kind": "Skills"},
                               "outcomes": [{"id": "default", "label": "Default", "outcomeSchema": {"type": "object", "description": "Function output"}}]}})

def m365copilot_connected(self, name, message, y=256):
    """M365 Copilot node with the admin connection reference attached (the designer adds it on first save; adding it here avoids a Needs setup)."""
    nid = self.m365copilot(name, message, y=y)
    node = self.nodes[-1]
    node["data"]["config"]["connectionName"] = "shared_m365copilotv2"
    logical, cname = wfapi.CONN["shared_m365copilotv2"]
    self.conn_refs["shared_m365copilotv2"] = {"api": {"name": "shared_m365copilotv2"}, "connection": {"connectionReferenceLogicalName": logical},
                                              "runtimeSource": "invoker", "connectionName": cname}
    return nid

Workflow.respond_to_agent = respond_to_agent
Workflow.m365copilot_connected = m365copilot_connected

def compose(self, name="Compose", inputs="", y=256):
    """Compose (Function → Data Operations → Compose). Graph: builtinFunction/operationId 'composeNew' (verified on probe B);
    compiles to {"type":"Compose","inputs":<value>}. Reference its result with @outputs('<Node_Name>')."""
    nid = _id("builtinFunction")
    return self._add({"id": nid, "name": name, "type": "builtinFunction", "version": 1, "position": self._pos(y),
                      "data": {"config": {"operationId": "composeNew", "operationName": "composeNew", "displayName": "Compose",
                                          "category": "providers/Microsoft.ProcessSimple/operationGroups/DataOperation", "categoryDisplayName": "Data Operation",
                                          "iconUri": "https://logicappsv2resources.blob.core.windows.net/icons/compose.svg", "brandColor": "#8C6CFF",
                                          "parameters": {"inputs": inputs}, "description": "Construct an arbitrary object, array or value.",
                                          "parametersSchema": {"type": "object", "required": ["inputs"], "properties": {"inputs": {"type": "string", "title": "Inputs", "description": "Value to compose"}}}},
                               "outcomes": [{"id": "default", "label": "Default", "outcomeSchema": {"type": "object", "description": "Function output"}}]}})

Workflow.compose = compose

def start_manual_inputs(self, inputs):
    """Manual (Button) trigger with typed inputs. inputs: list of (label, kind, description); kind text|number|boolean|email|date.
    Verified 2026-09-04 (Lab 10): property keys are the TYPE name (`text`, `text_1`, `number`…), label in `title`; the schema is stored
    three times — trigger inputs.schema, node config.manual.inputsSchema, and the start node's outcomeSchema. Reference: triggerBody()?['text']."""
    hint = {"text": ("TEXT", "string"), "number": ("NUMBER", "number"), "boolean": ("BOOLEAN", "boolean"), "email": ("EMAIL", "string"), "date": ("DATE", "string")}
    props, req, used = {}, [], {}
    for label, kind, desc in inputs:
        key = kind if kind not in used else f"{kind}_{used[kind]}"
        used[kind] = used.get(kind, 0) + 1
        h, t = hint[kind]
        props[key] = {"title": label, "type": t, "x-ms-content-hint": h, "x-ms-dynamically-added": True, "description": desc}
        req.append(key)
    schema = {"type": "object", "properties": props, "required": req}
    nid = self.start_manual()
    node = self.nodes[-1]
    node["data"]["config"]["manual"] = {"inputsSchema": schema}
    node["data"]["outcomes"][0]["outcomeSchema"] = schema
    self.trigger_def["inputs"]["schema"] = schema
    return nid

Workflow.start_manual_inputs = start_manual_inputs
