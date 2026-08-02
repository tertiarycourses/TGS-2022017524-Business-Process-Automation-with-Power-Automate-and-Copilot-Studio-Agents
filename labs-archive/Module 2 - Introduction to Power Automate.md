# Module 2: Power Automate Cloud Flows

Power Automate cloud flows connect Microsoft 365 services and other systems. Every cloud flow has exactly one **trigger** and at least one **action**.

## Instant, scheduled and automated flows

| Cloud flow | What starts it | Use it when | Course example |
|---|---|---|---|
| **Instant cloud flow** | A person deliberately selects a button, runs a flow, or invokes it from an app | The user controls the exact start time | A staff member runs a one-off test or approval |
| **Scheduled cloud flow** | A **Recurrence** trigger reaches a defined time | Work must happen at fixed intervals even when no new business event occurs | Send a daily digest every weekday at 9:00 AM |
| **Automated cloud flow** | A business event occurs in a connected service | The process should react immediately to new information | A Microsoft Form response starts Labs 1–4 and 7 |

The difference is the **trigger**, not the actions. All three types can send email, update Excel, call an agent, create an approval, or branch on a condition.

> **Decision rule:** ask “Who or what should start this process?” A person suggests instant; a clock suggests scheduled; a new record, form, file or message suggests automated.

### Instant cloud flow

An **instant** flow waits for a person or application to invoke it deliberately. Typical triggers include **Manually trigger a flow**, **Power Apps**, and a selected-item button in a Microsoft 365 app.

Use an instant flow when:

- the user must decide exactly when the process starts;
- the user needs to supply values at run time; or
- the action is exceptional rather than continuously monitored.

Do not choose an instant flow for unattended monitoring. If a form submission should always be processed, an automated flow is the better design.

### Scheduled cloud flow

A **scheduled** flow starts from a **Recurrence** trigger. Its configuration defines the start time, frequency, interval and time zone.

Use a scheduled flow for work such as:

- a weekday 9:00 AM reminder;
- an overnight reconciliation;
- a weekly summary; or
- a periodic check of items that have not been updated.

Scheduled flows are driven by the clock. They may find no work on a particular run, so design them to handle an empty result safely.

### Automated cloud flow

An **automated** flow listens for a business event in a connector. Examples include **When a new response is submitted**, **When a file is created**, and **When an email arrives**.

Use an automated flow when every qualifying event should receive a consistent response. Labs 1–4 and 7 use this type because a Microsoft Forms submission is the business event.

### Compare the trigger, not the action

The same **Send an email** action can appear in all three flow types. The flow type is determined by how it starts:

```text
Person selects Run     → Instant
Recurrence time arrives → Scheduled
Business event occurs   → Automated
```

## Trigger selection and trigger outputs

A trigger is the first card and the event subscription for the flow. It answers four design questions:

1. **Event:** what exactly has to happen?
2. **Scope:** which form, mailbox, folder, list or environment is monitored?
3. **Identity:** which connection has permission to listen?
4. **Output:** which identifiers and values become available to later actions?

The trigger output is not always the complete business record. In the Microsoft Forms pattern, the trigger returns a **Response Id**, and **Get response details** uses that identifier to retrieve the answers. This is why the first two cards are both necessary.

> A valid cloud flow needs one trigger and at least one action. An HTTP trigger by itself still produces the designer message that the flow needs a trigger **and an action**.

## The course pattern

The Day 1 labs use one connected scenario and expand it gradually:

1. **Lab 1:** form response → confirmation email.
2. **Lab 2:** form response → Excel audit record → confirmation email.
3. **Lab 3:** event form → condition → different logging and email outcomes.
4. **Lab 4:** leave form → approval → approved or rejected notification.
5. **Labs 5–6:** build and publish specialised Copilot agents.
6. **Lab 7:** form response → route to the appropriate agent → email its reply.

## Form-trigger pattern

A Microsoft Forms automation normally uses these first two cards:

1. **Microsoft Forms — When a new response is submitted**
2. **Microsoft Forms — Get response details**

The trigger supplies the **Response Id**. The second action retrieves the answers, which then appear as dynamic content.

```text
Form submitted
    ↓
Get response details
    ↓
Use the answers in later actions
```

## Actions, dynamic content and expressions

- An **action** changes or retrieves something after the trigger.
- **Dynamic content** is an output token selected from an earlier card, such as the respondent's Email answer.
- An **expression** calculates a value, such as `utcNow()` for an audit timestamp.

Use tokens and expressions through the designer rather than typing their labels as plain text. A typed word such as `Email` is only text; the coloured Email token carries the actual submitted value.

## Conditions and approvals

A **Condition** evaluates a rule and creates **If yes** and **If no** branches. Test both branches with different submissions. An approval is different: **Start and wait for an approval** pauses the run until the assigned approver responds, then exposes an **Outcome** that a condition can evaluate.

## Connections and verification

Each connector uses a saved connection. Microsoft Forms, Office 365 Outlook, Excel Online (Business), Approvals, SharePoint and Copilot Studio may each ask you to sign in.

For every flow:

1. Confirm the correct environment and account.
2. Save the flow.
3. Trigger a realistic test.
4. Open the run history and inspect inputs and outputs.
5. Confirm the real-world result: email, row, approval or agent reply.

## Data design rules

- Use dynamic-content tokens, not typed field names.
- Keep Excel data inside a named **table**.
- Record timestamps and outcomes for auditability.
- Test every condition branch.
- Do not put passwords, API keys or confidential information in instructions, source code or email bodies.

**Next:** [Lab 1 — Form to Email Confirmation](Lab%201%20-%20Forms%20Email%20Confirmation/index.md)
