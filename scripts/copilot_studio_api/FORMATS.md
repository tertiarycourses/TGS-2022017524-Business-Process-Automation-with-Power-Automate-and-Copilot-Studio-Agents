# Copilot Studio workflow (new experience) — graph formats verified live 2026-09-04

Create with `wfapi.py` (same folder). `create(wf)` POSTs a Dataverse `workflows` row (category 5, type 1, modernflowtype 1) whose
`clientdata` carries ONLY the designer GRAPH. The designer recompiles the Logic-Apps `actions` when the workflow is saved in the UI:
open `designer_url(wid)`, rename-nudge (click the title button, End, type a space, Backspace, Enter), click Save (button[aria-label="Save"]),
then Publish (role button "Publish"; wait for "Publishing..." to clear). A node shows **Needs setup** when a required field is missing —
open its panel to read the reason (`aria-label="Needs setup. <reason>"` on the canvas node).

## Expression rules (Logic Apps / Power Automate)
- Whole-field values: `"@outputs('Node_Name')?['body/field']"`, `"@triggerBody()?['field']"`, `"@triggerOutputs()?['body/resourceData/responseId']"`.
- Inside text (email body, instructions, Classify input, Human review title): interpolate `@{...}` e.g. `"Hello @{outputs('Get_response_details')?['body/rXXXX']}"`.
- Action names = node display name with spaces → underscores (`Get response details` → `Get_response_details`). Keep node names free of punctuation.
- Forms answers are `body/<questionId>`; Lab 1 form ids: Name ra7b2b2c768fe4bbfae38bd8bc152cb04, Email r34f434c08f984a8fa4bb1d0033e55dd3, Tel r07b82f997fa545ab86bb3b7879fa7e96, Message rf5e39878c6694d9d9bbe3fdfe7840b5b. Other forms: create the workflow with the Forms trigger + Get response details, open+save in the designer, then `GET` the row (header `MSCRM.includeunpublished: true`) and read `outcomeSchema` of the Get response details node → question ids.
- Human review outputs: `outputs('Human_review')?['body/boolean']` (the Yes/No answer), `['body/text']` (text). Compare the Yes/No with `equals(..., 'Yes')` first; if that never matches, read the run's Human review outputs in the Activity tab and switch to `true`.
- Agent node text output: `outputs('Draft_reply')?['body/message']`; structured: `outputs('Draft_reply')?['body/structuredOutput/field']`.
- Classify node: compiles to InvokeDefinition + a Switch on `outputs('Classify_email')?['body']?['structuredOutput']?['predictedCategory']`. Wire branches with `wf.edge(classify_id, target, source_handle=cats['Meeting'])`.
- If/Else: `wf.if_else("Name", ("@outputs('Human_review')?['body/boolean']", "equals", "Yes"))` → returns (id, yes_handle, else_handle); wire `wf.edge(id, target, source_handle=yes_handle)`.
- Excel Online: `AddRowV2` params: `source` (drive id: use "me"), `drive` ("me"), `file` (item id or path form "/Power Automate Lab Data/Lab 2 - Enquiry Log.xlsx" — use the path form: parameter `file` accepts the OneDrive path when `source`="me", `drive`="me"), `table` ("EnquiryLog"), `item/<Column>` per column.
- SharePoint `GetItems`: `dataset` (site URL), `table` (list GUID or name), `$filter`, `$top`. `PostItem`: `dataset`, `table`, `item/Title`, `item/<Col>`.
- Outlook `SendEmailV2`: `emailMessage/To`, `emailMessage/Subject`, `emailMessage/Body` (HTML), `emailMessage/Importance`. `ReplyToV3`: `messageId`, `replyParameters/Body`. `V3 email trigger`: `OnNewEmailV3` with `folderPath` "Inbox", `importance` "Any", `fetchOnlyWithAttachment` false, `includeAttachments` false. `FlagV2`: `messageId`. `Move (V2)`: `messageId`, `folderPath`. `CalendarPostItem_V4` (Create event V4): `calendar`, `item/subject`, `item/start`, `item/end`, `item/timeZone`, `item/body`.
- Teams `PostMessageToConversation`: `poster` "Flow bot", `location` "Channel", `body/recipient/groupId`, `body/recipient/channelId`, `body/messageBody`.
- M365 Copilot node (`wf.m365copilot(name, message)`): output `outputs('Node')?['body/response']`.
- HTTP trigger: `wf.start_http(schema=...)` (POST, anyone). Request body fields: `triggerBody()?['field']`. There is no separate Response action in the palette export yet — use the **End** node (Terminate) for now; a "Response" connector action (`shared_request`? or Function) must be verified in the designer before relying on it (search the Connectors tab for "Response").
- Agent-as-tool trigger: `wf.start_agent_call(schema={...})`; respond with a `Respond to the agent` connector action — search the Connectors tab for "Respond to the agent" to learn its operation name before building Labs 6/11 (write it into this file).

## Connection references (admin account)
Forms, Office 365 Outlook, Excel Online (Business), Agent node, SharePoint, Teams, Human review (advancedapprovals) are in `wfapi.CONN`. Standard `shared_approvals` has NO admin connection yet — use Human review instead of Start-and-wait where the lab allows, or create the connection in the designer once (add the node, it auto-connects) and copy the reference from the saved graph into CONN.

## Sample: Lab 1 (works end to end)
See `build_lab1.py` in this folder (Forms trigger → Get response details → Send an email).

## Forms trigger — splitOn (verified 2026-09-04 by a failed run)
The Forms `CreateFormWebhook` trigger delivers `{ "value": [ { resourceData: { responseId } } ] }`. The designer only compiles `splitOn` when the start node's connector config has `"triggerBatchMode": "Batch"` — `wfapi.start_connector(..., split_on=...)` now sets it. Without it `@triggerOutputs()?['body/resourceData/responseId']` is null and Get response details fails with BadRequest "The response ID in request URL is invalid".
- UPDATE: `triggerBatchMode` alone is not enough — the designer needs the trigger's `parametersSchema`/`outputSchema` (webhook body `value[]`) to emit `splitOn`. `start_connector(..., ui_connector=<connector config saved once by the UI>)` copies them; for the Forms trigger take it from lab1-clientdata.json: `g['nodes'][0]['data']['config']['connector']`. For other webhook triggers (Outlook V3 email), add the trigger once in the designer, save, GET the row and reuse its connector config the same way.
- Updating a workflow that the designer has already saved fails with 0x80040203 ("published update … unpublished active row"). Simplest fix: `create(wf)` again (it deletes the old row by name first, after deactivating) and re-open/save/publish. Deactivate first with PATCH {"statecode":0,"statuscode":1} if DELETE returns 400.

## Built-in function nodes (verified 2026-09-04 on probe workflow `ZZ Probe B - formats`, wid 04da5980-c4a7-f111-aaad-000d3a857861 — see probeB-clientdata.json)
All three are graph type **`builtinFunction`**; the designer compiles them to Logic-Apps actions and names the action after the node name (spaces → underscores). Helpers in `wfapi_ext.py` (`wf.response()`, `wf.http()`, `wf.compose()`).
- **Response** (Add step → Connectors tab, search "Response" → "Select action: Response"; category Request). Graph config: `operationId`/`operationName` `"response"`, `category` `providers/Microsoft.ProcessSimple/operationGroups/Request`, `parameters` `{statusCode: 200, headers: {"Content-Type": "application/json"}, body: "<string>"}`. Compiles to `{"type":"Response","inputs":{"statusCode":200,"headers":{...},"body":"..."}}`. In the UI the Status code field is the only visible one; Headers and Body are under *Advanced parameters → Show all*. **The Body token editor auto-closes `{` when typing** (`{"reply": "hello"}` became `{reply": "hello"}"`), so set the body through the API, as a JSON string with `@{...}` interpolation; booleans unquoted (`"escalated": @{toLower(string(...))}`).
- **HTTP** (search "HTTP" → "Select action: HTTP"; category HTTP). Graph config: `operationId` `"httpaction"`, `category` `providers/Microsoft.ProcessSimple/operationGroups/Http`, `parameters` `{method: "POST", uri, headers: {"Api-Key": "...", ...}, body: "<string>", queries?}`. Compiles to `{"type":"Http","inputs":{method,uri,headers,body}}`. Method is a dropdown (enum GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS); Headers/Queries/Body/Authentication under *Show all*. Output: `body('HTTP')` (the parsed JSON response).
- **Compose** (search "Compose" → "Select action: Compose"; single field **Inputs**) — see the Compose entry below for its operationId.
- The `End` node remains available (`Terminate`); the website contract is met by **Response**, so End is optional after it.

## Excel Online (Business) AddRowV2 — exact parameter values (picked once in the designer 2026-09-04, Lab 2)
When the four dropdowns are picked by hand the designer stores **ids, not names**:
- `source`: `"me"` (Location = OneDrive for Business)
- `drive`: `"b!SjecQDKqRUqeM67rgiO4VeKrsryxCPJLodXkA7TDWkyK1tEZN9r7TLlK5TAsG_h-"` (Document Library = OneDrive — the admin's OneDrive drive id; same for every workbook in `Power Automate Lab Data`)
- `file`: the OneDrive **item id**, e.g. `Lab 2 - Enquiry Log.xlsx` = `"01LGABAFVPE64FFLLAQVG2VQLXX7UTFNKU"`
- `table`: the table id `"{00000000-000C-0000-FFFF-FFFF00000000}"` (EnquiryLog is the first/only table in the workbook — this generic id is what the picker stores)
- The path form (`drive` `"me"`, `file` `"/Power Automate Lab Data/<name>.xlsx"`, `table` `"EnquiryLog"`) is **accepted by the designer** (no Needs setup; the Table dropdown and the Row columns resolve from it), so it is a usable fallback for workbooks whose ids have not been picked yet. All values live in `api/excel-params.json` (keys lab2/lab3/lab6).
- The designer keeps whole-field expressions (`@utcNow()`, `@outputs(...)`) in `item/<Column>` as given; it rewrote two of them to `@{...}` interpolation on save — both forms run.

## Lab 3 - Leave Application Form — question ids (from the designer-saved outcomeSchema of Get response details)
Name r5e2c4896d3354bb298d01c71a45f3016 · Leave from date rede11d6c3115421b8caf06a575673b10 · Leave end date r74ae6b1b572846a19adca1c37ac6be6b · Leave Type r6090f9f50a23490d808dcfb03d96c75e · Reason for Leave ra1e0aec0473e401ba4e13b64e8e8fca9 · plus `body/responder`, `body/submitDate`. Saved in `api/lab3-questions.json` and `api/lab3-stage1-clientdata.json` (full schema).
- To learn a form's ids: create trigger + Get response details, open the designer, **click the Get response details node** (the panel load fetches the dynamic schema), then Save → the node's `outcomeSchema` is in the saved graph. A save without opening the node does NOT populate it.
- The rename-nudge: clicking the title selects the whole name — typing replaces it. Use End → Space → Backspace → Enter only; never type a character (the stage-1 row was renamed to "x" that way and then had to be deleted by id).
- **Compose** graph config: `operationId`/`operationName` `"composeNew"`, `category` `providers/Microsoft.ProcessSimple/operationGroups/DataOperation`, `categoryDisplayName` "Data Operations", icon `.../icons/compose.svg`, brand `#8c6cff`, `parameters` `{"inputs": "<string>"}`. Compiles to `{"type":"Compose","inputs":"..."}`; reference `outputs('Node_Name')`. A whole-field `"@json(...)"` in `inputs` yields an object so `outputs('Enquiry')?['ticketId']` works.

## Agent node — SharePoint knowledge (verified 2026-09-04)
UI: Agent panel → Knowledge → **Add a knowledge** → dialog "Add knowledge" (Featured: *Public websites*, *SharePoint*) → SharePoint → field "SharePoint link" (aria-label) → **Add** (enabled only for a `%20`-encoded URL; a URL with raw spaces leaves Add disabled) → the source appears as Link/Name/Description → **Add to agent**.
Graph: `config.inlineKnowledge: [{"id": <guid>, "displayName": "Lab 13 - Investment FAQ", "description": "This knowledge source provides information found in <name> SharePoint.", "type": "sharepoint", "site": "<encoded folder URL>", "originalSite": "<same>"}]`.
Compiles into `body/botDefinition` as `"knowledgeSources":[{"type":"sharepoint","displayName","site","description"}]`. Helper: `wf.add_knowledge(agent_id, display_name, encoded_url)`.

## Expression functions that do NOT exist in this designer
`setProperty()` → canvas shows **"Unknown function: setProperty"** on the node (same class as `workflow()`); assume `addProperty()` is unavailable too. To build a JSON object safely (agent prose contains quotes/newlines):
`json(concat('{"reply":', substring(string(createArray(X)), 1, sub(length(string(createArray(X))), 2)), '}'))` — `string(createArray(X))` renders `["…"]` with proper JSON escaping; strip the brackets. Helpers `obj_expr({...})`, `jlit(expr)`, `Raw(...)` in `wfapi_ext.py`. Booleans: `Raw("toLower(string(x))")`.
Rename-nudge selector: the title is `[data-testid="command-bar"] span[role="button"]` (click, End, Space, Backspace, Enter).
- Lab 3 uses the **path form** for `Lab 3 - Leave Register.xlsx` (`drive` "me", `file` "/Power Automate Lab Data/Lab 3 - Leave Register.xlsx", `table` "LeaveRegister"): the designer resolved all nine LeaveRegister columns from it and saved/published without Needs setup. (The in-panel file picker could not be driven reliably a second time — clicking **Change** opens the folder tree but a stray "Select a connector" modal intercepts clicks; Escape closes both.)
- Human review outputs used by Lab 3: `outputs('Manager_approval')?['body/boolean']` (Outcome Yes/No) and `['body/text']` (Comments). Compiled fine as `If {"and":[{"equals":["@outputs('Manager_approval')?['body/boolean']","Yes"]}]}` with the two Send-an-email actions inside `actions` / `else.actions`.
- Publish runs a **server-side validator** whose findings appear under the **Review** button (badge count) as "Review problems": e.g. `The input parameter(s) of operation 'HTTP' contains invalid expression(s).`, `Action "X" references action "Y," which is not on the canvas`. The token editor's own parse error (`Expected ) after function arguments`) is shown on the canvas node and in the node panel. Expression length is NOT a limit (a 1600-char literal in a Response body passed both validators — probe D).
- Verified server-accepted expression shapes: `@json(concat('{"a":', string(1), '}'))`, `@json('{"a":1}')`, a plain JSON-text body with `@{triggerBody()?['q']}` interpolation, and the `jlit()` escaper.

## Parameter values used by Labs 12–16 (tenant, verified 2026-09-04)
- SharePoint `GetItems`/`PostItem`: `dataset` = `https://tertiaryinfotech.sharepoint.com/sites/WSQCourses`; `table` = list GUID — `Lab 12 - Customers` = `6b0cbc95-291f-442c-a40a-d7ab779e95eb` (columns Title=FullName, NRIC, Email, Phone, DateOfBirth, Employment, Income, Decision), `Lab 12 - Onboarding Log` = `aa9ca135-5004-4936-b6f0-c2c50e78886d` (Title, NRIC, Decision(text), Reason, SubmittedAt). `$filter`: `NRIC eq '@{toUpper(trim(triggerBody()?['nric']))}'` (string with interpolation — runs fine; lookup took 0.52 s), `$top`: 1. `PostItem` params `item/Title`, `item/NRIC`, `item/Decision`, `item/Reason`, `item/SubmittedAt`.
- Excel `AddRowV2` (Lab 14): `source` "me", `drive` "me", `file` "/Power Automate Lab Data/Lab 14 - Handover Queue.xlsx", `table` "Drafts" (columns Reference, Timestamp, Client, Enquiry, Draft, Urgency, Flags, Escalate, Status, ApprovedBy) / "HandoverQueue" (Reference, Timestamp, Client, Enquiry, Reason, Owner) — column names are from the workbook in labs/Lab 14/assets, NOT the ones in the lab BUILD-SHEET.
- Agent knowledge folders: `.../Shared%20Documents/Lab%2013%20-%20Investment%20FAQ`, `.../Shared%20Documents/Lab%2015%20-%20Course%20Brochures`.
- Pinecone (Lab 16): URI `https://lab16-course-brochures-XXXXXX.svc.aped-4627-b74a.pinecone.io/records/namespaces/__default__/search` (placeholder host from the lab doc — no real index host exists in the repo), headers `Api-Key` = `PASTE-PINECONE-API-KEY` (placeholder), `Content-Type: application/json`, `X-Pinecone-Api-Version: 2025-04`; body built with `obj_expr` (question JSON-escaped). Output `body('HTTP')`.
- Null-safety when the Agent produces nothing (e.g. no credits): `join(coalesce(x?['riskFlags'], json('[]')), ', ')`; Response fallback `@coalesce(body('Agent')?['structuredOutput'], json(...))`.

## Respond to the agent — verified 2026-09-04 (Lab 11, Lab 6)
- It is **not** the Skills connector action found by the Connectors search ("Skills → Respond to the agent" → that one demands a "Connect to Skills" connection whose listing fails with *Something went wrong* and the node stays Needs setup). The right one is in the **+ (Add a step) menu → Actions → Agent → Respond to the agent** (only offered when the trigger is *When an agent calls the workflow*).
- Graph node: `type` **`builtinFunction`**, config `{operationId:"response", operationName:"response", displayName:"Respond to the agent", category:"request", categoryDisplayName:"Request", kind:"Skills", parameters:{schema:{type:"object", properties:{text:{title:"BlogPost", type:"string", "x-ms-content-hint":"TEXT", "x-ms-dynamically-added":true}}, required:["text"]}, body:{text:"@{outputs('<node>')?['body/response']}"}}}`. Output property keys are typed names `text`, `text_1`, … (the label lives in `title`). Compiles to `{"type":"Response","kind":"Skills","inputs":{"schema":…,"statusCode":200,"body":{"text":…}}}`. Helper: `wf.respond_to_agent(name, {"BlogPost": "@outputs('Draft_the_blog_post')?['body/response']"})` in `wfapi_a.py`.
- The trigger `wf.start_agent_call(schema=...)` with `properties` keyed by the **input name** (`Topic`, `Item`…; `title`, `type`, `x-ms-content-hint` TEXT/NUMBER, `description`) is what the designer itself writes — the Start panel shows *When an agent calls the workflow* with the inputs listed (title + description) and the ⚡ picker lists them.
- Graph references saved by the UI use the node id (`outputs('m365Copilot-<uuid>')`); the compiler rewrites them to the action name. Hand-written `@outputs('Action_Name')` works too.

## M365 Copilot node connection (verified 2026-09-04)
The Copilot node needs the admin's `shared_m365copilotv2` connection reference: logical name `new_sharedm365copilotv2_8997c730`, connection `shared-m365copilotv2-1f7f5a7c-5abc-4f3d-ad8c-954767d4d850`, `runtimeSource` **"invoker"** (not embedded). `wf.m365copilot_connected(name, message)` in `wfapi_a.py` adds it; output `outputs('<Node>')?['body/response']` (the picker also offers Conversation ID and Citations).

## Compose (Function → Data Operations) — verified on probe B, used by Lab 6 `Reference`
`builtinFunction` with `operationId`/`operationName` **`composeNew`**, `category` `providers/Microsoft.ProcessSimple/operationGroups/DataOperation`, `parameters` `{"inputs": "<value or @expression>"}`; compiles to `{"type":"Compose","inputs":…}`; read it back with `@outputs('Reference')`. Helper `wf.compose(name, inputs)` in `wfapi_a.py`.

## Publish compiles too
For Lab 11 the Save button was disabled after the rename-nudge (nothing dirty) but **Publish alone compiled the actions** (`actions` populated, statecode 1). Still nudge+Save first when possible.

## Manual trigger inputs (verified 2026-09-04, Lab 10)
Start node → *Add an input* → Text stores the input under the **type name** as key (`text`, then `text_1`…) with the label in `title`:
`{"text": {"title": "Topic", "type": "string", "x-ms-content-hint": "TEXT", "x-ms-dynamically-added": true, "description": "The subject of the blog post"}}`, `required: ["text"]`.
The same schema is written to the trigger (`triggers.manual.inputs.schema`), to the start node `config.manual.inputsSchema` and to its `outcomeSchema`. Reference it with `triggerBody()?['text']`. Helper `wf.start_manual_inputs([("Topic","text","The subject of the blog post")])` in `wfapi_a.py`.

## Teams — Post message in a chat or channel (verified 2026-09-04, Lab 10)
Team dropdown lists the teams the admin belongs to: only **"Tertiary Infotech - WSQ Courses"** exists (there is NO "Training" team in the tenant). Picked values: `body/recipient/groupId` = `84ef327e-f12a-4c61-843e-90e376a6b402`, `body/recipient/channelId` (General) = `19:PD27Mfb011K4_c3jpgLriPIzDFnVowZyfLm7TT6MKhY1@thread.tacv2`; other channels: Resources, WSQ Course Applications, ACTA and ACLP Trainers, Planning, Announcements. `poster` "Flow bot", `location` "Channel", `body/messageBody` accepts a whole-field expression. Values in `api/teams-params.json`.
