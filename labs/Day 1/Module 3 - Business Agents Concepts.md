# Module 3: Copilot Studio Agent Building Blocks

A Copilot Studio agent combines instructions, trusted information and actions so it can help a user complete a defined task. A useful agent is not just a chat box; it is a governed system with clear boundaries.

> **Interface used in this course:** Use the new Copilot Studio experience. Agent
> components are configured from **Build**, conversations are tested in
> **Preview**, repeatable tests are managed in **Evaluate**, and recent activity
> is reviewed in **Monitor**. The new agent experience is production-ready
> preview; the redesigned workflow canvas is public preview and can change.

## The six building blocks

| Building block | Meaning | Design question |
|---|---|---|
| **Knowledge base** | Approved sources the agent can search to ground an answer, such as uploaded files or SharePoint content | Which source is authoritative, current and permitted? |
| **Skills** | Reusable, structured instructions that define a capability the agent can activate | What job should the agent be able to complete? |
| **Tools** | Connected functions, APIs or workflows that read data, call services or create outcomes | Which system action is safe, authenticated and auditable? |
| **Memory** | Context retained during a conversation through conversation history and variables; persistent memory depends on enabled product features and governance | What should be remembered, for how long and with what consent? |
| **Model** | The generative AI model that interprets the request and composes a response | Does the selected model provide the required quality, latency and governance? |
| **Instructions** | The behavioural rules defining role, tone, scope, safety and escalation | What must the agent always do or never do? |

> In the new experience, **Instructions** are edited directly on the **Build**
> tab. Treat them as policy, not decoration.

### 1. Knowledge base

Knowledge grounds answers in approved content. Uploaded FAQ files suit a small, stable source; SharePoint suits governed organisational documents that owners already maintain. Knowledge is not a substitute for live transactional data.

### 2. Skills

A skill is a reusable business capability, such as answering an IT question,
triaging a request or obtaining a finance explanation. In the new experience,
skills are structured instructions managed from the **Skills** component on
**Build**. Define the user outcome first, then add only the components needed
to achieve it.

### 3. Tools

A tool lets the agent perform or retrieve something beyond generating text.
Examples include a workflow, a connector action, an API or another approved
agent. Give a tool a clear name and description so the orchestrator knows when
to call it, and validate its inputs and outputs.

### 4. Memory

Memory is the conversational context available to the agent. Short-term context helps it understand follow-up questions. Persistent personalisation, if enabled and approved, requires stronger privacy, retention and consent controls. Never treat memory as an authoritative database.

### 5. Model

The model interprets language, reasons over context and composes the answer. Model selection affects quality, latency, cost and governance. The model does not replace trusted knowledge, deterministic tools or explicit safety instructions.

### 6. Instructions

Instructions define the agent's role, tone, boundaries, evidence rules and escalation behaviour. Write them as testable rules: what sources to use, what data never to request, how to handle uncertainty and where to redirect an unsupported request.

## New interface map

| Authoring task | New agent experience | New workflow experience |
|---|---|---|
| Configure | **Build** tab: Instructions editor and components panel | **Build** tab: Start card, Add pane and node configuration panel |
| Add knowledge | **Build → Knowledge** in the components panel | Add knowledge inside an **Agent** node when that workflow step needs grounding |
| Add an action | **Build → Tools** | Select **+** or **Add a step**, then choose **Agent**, **Connector**, **Function**, **Variable**, **If/Else**, **Loop** or another Add category |
| Test | **Preview** for interactive chat; **Evaluate** for repeatable test sets | Play button for an end-to-end test; node **Test** panel for one step |
| Review runs | **Monitor** | **Activity** for run details and **Monitor** for operational review |
| Release | **Publish** | Fix every health error, then select **Publish** |

## Knowledge versus tools

Knowledge answers **“What should the agent know?”** Tools answer **“What may the agent do?”**

```text
User asks a question
    ↓
Instructions set scope and behaviour
    ↓
Knowledge grounds the answer
    ↓
Tool performs an authorised action when required
    ↓
Agent returns a traceable response
```

An HR policy PDF can explain annual leave. A leave-balance tool can retrieve a user's current balance. Do not use a static document where live data is required, and do not call a tool when a grounded explanation is enough.

## Agent orchestration

When a request arrives, the agent interprets the intent, follows its instructions, retrieves relevant knowledge and decides whether a tool is required. The returned answer should make the outcome clear without exposing internal prompts, secrets or raw tool errors.

In Lab 7, the Power Automate condition makes the routing decision first. The flow then invokes the selected IT or HR agent and waits for its reply before emailing the user. This keeps routing deterministic while allowing the specialist response to be generative.

## Agent design checklist

1. Give the agent one clear business role.
2. Add only approved knowledge.
3. Write instructions for scope, uncertainty, privacy and escalation.
4. Add the minimum tools needed.
5. Test expected questions, vague questions, out-of-scope questions and malicious instructions in **Preview**.
6. Publish only after the latest version passes testing.
7. Use **Evaluate** for repeatable quality checks and **Monitor** for recent activity.

## Example Instructions

```text
You are the ACME IT Support Agent.
Answer using approved IT FAQ knowledge.
Ask one concise clarifying question when essential.
Never request passwords, MFA codes or recovery keys.
If the answer is not grounded in the approved source, say so and direct the
user to the service desk.
```

**Next:** [Lab 5 — IT Support Agent](../Day%201/Lab%205%20-%20IT%20Support%20Agent/index.md)
