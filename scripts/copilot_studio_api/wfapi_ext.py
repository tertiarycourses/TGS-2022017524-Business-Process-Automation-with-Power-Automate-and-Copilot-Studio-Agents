"""wfapi_ext.py — builtinFunction nodes verified live 2026-09-04 (probe workflow ZZ Probe B):
Response (operationId 'response' -> Logic Apps type 'Response'), HTTP (operationId 'httpaction' -> type 'Http'),
Compose (see FORMATS.md). Import after wfapi: `from wfapi import *; from wfapi_ext import *`."""
import json, uuid
from wfapi import Workflow, _id

def _bf(self, name, operation_id, display, category, cat_display, icon, brand, params, schema, description, y=256):
    nid = _id("builtinFunction")
    return self._add({"id": nid, "name": name, "type": "builtinFunction", "version": 1, "position": self._pos(y),
                      "data": {"config": {"operationId": operation_id, "operationName": operation_id, "displayName": display,
                                          "category": category, "categoryDisplayName": cat_display, "iconUri": icon, "brandColor": brand,
                                          "parameters": params, "description": description, "parametersSchema": schema},
                               "outcomes": [{"id": "default", "label": "Default", "outcomeSchema": {"type": "object", "description": "Function output"}}]}})

def response(self, name="Response", body="", status=200, headers=None, y=256):
    """HTTP Response action. body: string (JSON text with @{...} interpolation). Compiles to {"type":"Response","inputs":{"body","statusCode","headers"}}."""
    params = {"statusCode": status, "body": body, "headers": headers or {"Content-Type": "application/json"}}
    schema = {"type": "object", "required": ["statusCode"], "properties": {
        "statusCode": {"type": "integer", "title": "Status Code", "description": "HTTP status code", "default": 200},
        "headers": {"type": "object", "title": "Headers", "description": "Response headers"},
        "body": {"title": "Body", "description": "Response body"}}}
    return _bf(self, name, "response", "Response", "providers/Microsoft.ProcessSimple/operationGroups/Request", "Request",
               "https://logicappsv2resources.blob.core.windows.net/icons/request.svg", "#009DA5", params, schema, "Send a response to an HTTP request.", y)

def http(self, name="HTTP", method="POST", uri="", headers=None, body=None, queries=None, y=256):
    """Built-in HTTP action. Compiles to {"type":"Http","inputs":{"method","uri","headers","body"}}. Output: body('HTTP')."""
    params = {"method": method, "uri": uri}
    if headers: params["headers"] = headers
    if queries: params["queries"] = queries
    if body is not None: params["body"] = body
    schema = {"type": "object", "required": ["method", "uri"], "properties": {
        "method": {"type": "string", "title": "Method", "description": "HTTP method", "enum": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"], "default": "GET"},
        "uri": {"type": "string", "title": "URI", "description": "Request URL"},
        "headers": {"type": "object", "title": "Headers", "description": "Request headers"},
        "queries": {"type": "object", "title": "Queries", "description": "Query parameters"},
        "body": {"title": "Body", "description": "Request body"},
        "authentication": {"type": "object", "title": "Authentication", "description": "Authentication configuration"}}}
    return _bf(self, name, "httpaction", "HTTP", "providers/Microsoft.ProcessSimple/operationGroups/Http", "HTTP",
               "https://logicappsv2resources.blob.core.windows.net/icons/http.svg", "#709727", params, schema, "Make an HTTP request to any endpoint.", y)

Workflow.response = response
Workflow.http = http

def compose(self, name, inputs, y=256):
    """Function -> Data Operations -> Compose. Graph operationId 'composeNew'; compiles to {"type":"Compose","inputs": <inputs>}.
    inputs: a string (may contain @{...} interpolation) or a whole-field expression "@setProperty(...)" that yields an object.
    Output: outputs('<Name_with_underscores>'). Keep the node name free of spaces/underscores when it is referenced from an
    Agent's Instructions (the rich-text editor escapes underscores)."""
    schema = {"type": "object", "required": ["inputs"], "properties": {"inputs": {"type": "string", "title": "Inputs", "description": "Value to compose"}}}
    return _bf(self, name, "composeNew", "Compose", "providers/Microsoft.ProcessSimple/operationGroups/DataOperation", "Data Operations",
               "https://logicappsv2resources.blob.core.windows.net/icons/compose.svg", "#8c6cff", {"inputs": inputs}, schema,
               "Compose outputs from multiple actions into a single output.", y)

def add_knowledge(self, agent_id, display_name, site_url):
    """Attach a SharePoint folder as knowledge to an inline Agent node (format verified: config.inlineKnowledge[]).
    site_url must be %20-encoded (the UI picker only accepts the encoded form)."""
    node = next(n for n in self.nodes if n["id"] == agent_id)
    node["data"]["config"].setdefault("inlineKnowledge", []).append({
        "id": str(uuid.uuid4()), "displayName": display_name,
        "description": f"This knowledge source provides information found in {display_name} SharePoint.",
        "type": "sharepoint", "site": site_url, "originalSite": site_url})

class Raw(str):
    """Marks a value for obj_expr as an expression that already yields JSON text (number, boolean, nested obj_expr, string(obj))."""

def jlit(expr):
    """Expression that renders <expr> (a string) as a quoted, escaped JSON string literal.
    string(createArray(x)) -> ["..."] ; strip the brackets. Verified route because this designer has NO setProperty()/addProperty()."""
    s = f"string(createArray({expr}))"
    return f"substring({s}, 1, sub(length({s}), 2))"

def obj_expr(fields):
    """Expression (without leading @) yielding a JSON object: json(concat('{', '"k":', <value>, ... '}')).
    Values: a plain str = an expression whose STRING result is JSON-escaped via jlit(); a Raw(...) = an expression that already
    yields JSON text (e.g. Raw("toLower(string(x))") for a boolean, Raw("3"), Raw(obj_expr({...})) for nesting)."""
    parts = []
    for i, (k, v) in enumerate(fields.items()):
        sep = "'{" if i == 0 else "',"
        val = f"string({v})" if isinstance(v, Raw) else jlit(v)
        parts.append(f"{sep}\"{k}\":', {val}")
    return "json(concat(" + ", ".join(parts) + ", '}'))"

def lit(s):
    return "'" + s.replace("'", "''") + "'"

Workflow.compose = compose
Workflow.add_knowledge = add_knowledge
__all__ = ["response", "http", "compose", "add_knowledge", "obj_expr", "jlit", "lit", "Raw"]
