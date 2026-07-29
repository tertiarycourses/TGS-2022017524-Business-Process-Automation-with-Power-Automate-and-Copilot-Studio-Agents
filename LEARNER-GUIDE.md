# Learner Guide

**Course Code:** TGS-2022017524  ·  **Version 6.2-S1**

### Document Version Control Record

| Version | Effective Date | Summary of Changes | Author |
| --- | --- | --- | --- |
| 1.0 | 24 Jun 2026 | Initial release — full 3-day, 17-lab learner guide. | Course Development Team |
| 2.0 | 2 Jul 2026 | WSQ revision — new course title, labs updated to the current Copilot Studio / Power Automate UI, Course Sandbox environment, WSQ cover page. | Course Development Team |
| 3.0 | 3 Jul 2026 | Course restructured from 3 days to 2 days — Day 1: Power Automate (Labs 0-5), Day 2: Copilot Studio agents (Labs 6-11) ending with the WSQ assessment. Modules 4-5 and Labs 12-16 retired. | Course Development Team |
| 3.1 | 24 Jul 2026 | Added Day 1 Labs 6A-6B: external online-form and browser-chatbot webhooks using the Power Automate HTTP Request trigger, with both new and classic designer guidance. | Course Development Team |
| 3.2 | 24 Jul 2026 | Reframed Lab 7 as the complete Copilot Studio IT Support RAG Chatbot outcome: approved FAQ retrieval, citations, negative testing, and grounded refusal. | Course Development Team |
| 3.3 | 24 Jul 2026 | Restructured Labs 8-10 into two-part Teams and website experiences: ordinary HTTP Power Automate flow, deterministic agent flow, and guarded AI prompt flow. | Course Development Team |
| 3.4 | 24 Jul 2026 | Day 2 now concludes at Lab 10. Retired Lab 11 and allocated the remaining guided time to integrated testing, troubleshooting and recap. | Course Development Team |
| 3.5 | 24 Jul 2026 | Made importable Power Automate packages the recommended classroom path and added a ready-made Lab 8 website enquiry flow package. | Course Development Team |
| 3.6 | 24 Jul 2026 | Made natural-language flow creation the primary Lab 1 route: prompt Copilot, inspect and correct the generated draft, then test; retained manual and import recovery routes. | Course Development Team |
| 3.7 | 24 Jul 2026 | Reorganised Copilot Studio Labs 6-10 into two coherent projects: prompt-created IT Support agent upgraded with RAG, then one Marina Trust agent progressively upgraded with HTTP, deterministic and AI prompt flows. | Course Development Team |
| 3.8 | 24 Jul 2026 | Added a visual architecture flowchart to every lab, standardised manual-build and packaged-import routes, and clarified how a Copilot Studio agent calls Power Automate agent flows as tools. | Course Development Team |
| 3.9 | 24 Jul 2026 | Reordered the labs from simple to complex: instant, scheduled, automated, human approval, HTTP, agent creation, RAG, channel deployment, deterministic agent flow and controlled prompt flow. | Course Development Team |
| 4.0 | 24 Jul 2026 | Aligned Lab 6A with the current sandbox flow: POST string trigger contract, imported manual label, training Outlook connection, classroom recipient, business-banking subject and exact JSON response. | Course Development Team |
| 5.0 | 25 Jul 2026 | Rebuilt the two-day learning journey around Forms-driven enquiry, event and leave workflows; specialised IT, HR and Finance agents; HTTP/webhook websites; and a multi-timeframe trading-information capstone. | Course Development Team |
| 5.1 | 25 Jul 2026 | Expanded Labs 1-10 into detailed click-by-click activities and added a shared labelled workflow flowchart to every lab, Learner Guide activity and matching facilitator-deck lab overview. | Course Development Team |
| 5.2 | 25 Jul 2026 | Standardised canonical Lab 1-10 titles, durations, slide ranges and shared flowchart mappings across the labs, Learner Guide Markdown, DOCX/PDF, Lesson Plan and facilitator deck. | Course Development Team |
| 6.0 | 25 Jul 2026 | Major concept-first overhaul aligned to the 113-slide deck: expanded cloud-flow types, trigger design, six Copilot agent building blocks, HTTP/webhook foundations, finance tools and the canonical Lab 1-10 sequence. | Course Development Team |
| 6.0-S1 | 25 Jul 2026 | Added supplementary Lab 11 to compare a Copilot agent calling a deterministic agent flow with a triggered agent flow calling a published agent for structured travel-expense review. | Course Development Team |
| 6.1 | 26 Jul 2026 | Updated Copilot Studio labs for the new agent and workflow interfaces. | Course Development Team |
| 6.2 | 26 Jul 2026 | Updated Lab 9 to use the new Copilot Studio HTTP workflow canvas and Agent node. | Course Development Team |
| 6.2-S1 | 29 Jul 2026 | Retained the AI Trading Advisor as Lab 10 and replaced the supplementary Lab 11 activity with the published Forms-based Procurement Request approval and outcome-notification workflow. | Course Development Team |

## Table of Contents

- [Common Errors & Quick Fixes](#common-errors--quick-fixes)
- [Day 1 — Foundations & Power Automate](#day-1--foundations--power-automate)
  - [Module 1: Introduction to Workflow Automation](#module-1-introduction-to-workflow-automation)
  - [Module 2: Power Automate Cloud Flows](#module-2-power-automate-cloud-flows)
  - [Lab 0: Environment Setup — Create Your Copilot Studio & Power Automate Accounts](#lab-0-environment-setup--create-your-copilot-studio--power-automate-accounts)
  - [Lab 1 — Form to Email Confirmation](#lab-1--form-to-email-confirmation)
  - [Lab 2 — Log the Enquiry and Send Email](#lab-2--log-the-enquiry-and-send-email)
  - [Lab 3 — Event Registration Branching](#lab-3--event-registration-branching)
  - [Lab 4 — Leave Application Approval](#lab-4--leave-application-approval)
  - [Module 3: Copilot Studio Agent Building Blocks](#module-3-copilot-studio-agent-building-blocks)
  - [Lab 5 — IT Support Agent](#lab-5--it-support-agent)
  - [Lab 6 — HR Support Agent](#lab-6--hr-support-agent)
  - [Lab 7 — Support Request Routing](#lab-7--support-request-routing)
- [Day 2 — HTTP, Webhooks and Agent Websites](#day-2--http-webhooks-and-agent-websites)
  - [Module 4: HTTP Requests and Webhooks](#module-4-http-requests-and-webhooks)
  - [Lab 8 — Website HTTP Enquiry](#lab-8--website-http-enquiry)
  - [Lab 9 — Finance Agent Web Chat](#lab-9--finance-agent-web-chat)
  - [Lab 10 — AI Trading Advisor Website](#lab-10--ai-trading-advisor-website)
  - [Lab 11 — Procurement Request Approval Workflow](#lab-11--procurement-request-approval-workflow)

Welcome! This Learner Guide takes you **click-by-click** through every hands-on lab in the WSQ course **Business Process Automation with Power Automate and Copilot Studio Agents** (Course Code: TGS-2022017524). Over two days you go from your first Power Automate flow to AI business agents in Microsoft Copilot Studio — and finish by connecting an agent to your flows in a complete end-to-end automated workflow.

Work through the labs **in order**: each one builds on the skills of the lab before it. Whenever you see a **Checkpoint**, stop and confirm your flow or agent behaves as described before moving on. The **Common Errors & Quick Fixes** and per-lab **Troubleshooting** tables will get you unstuck fast.

> Course flow at a glance — Day 1: Forms-driven email, Excel, branching and approval flows, followed by IT and HR agents and form-to-agent routing (Labs 1-7). Day 2: HTTP requests, webhooks, a Finance Agent web chat and the multi-timeframe trading advisor website (Labs 8-10), then the WSQ assessment (4:00-6:00 PM).

---

## Common Errors & Quick Fixes

Keep this handy — these are the issues learners hit most often, with the one-line fix:

| Symptom | Cause | Fix |
| --- | --- | --- |
| “Unauthorized” when sending email | Outlook connection expired or the account has no mailbox | Reconnect the Office 365 Outlook connection with a mailbox-enabled account; both connections must be green ✓ |
| Approval fails: “valid users in the organization” | Approver typed as an external email, not a tenant user | Pick the approver from the people-picker dropdown (a real user in your tenant; yourself is fine for testing) |
| Date logs as literal text ‘utcNow()’ | Expression typed into the field as text | Enter it via the fx / Expression editor so it becomes a coloured token |
| Excel cell shows ######## | The column is only too narrow | Auto-fit the column — the value is fine |
| An unwanted ‘For each’ wraps your action | You inserted a list/array value into a single-value field | Use single-value fields (Outcome, trigger inputs); delete the For each and re-add a plain action |
| Agent can’t see its flow | Agent and flow are in different environments | Set both Copilot Studio and Power Automate to the same environment (Course Sandbox) |

---

## Day 1 — Foundations & Power Automate

### Module 1: Introduction to Workflow Automation

> **Read this before the Day 1 labs.** It explains the "why" behind everything you'll build over the next two days. ~20 minutes.

By the end of this reading you will be able to:

- Explain what a business workflow is and which tasks are worth automating
- Tell the difference between an agent that only *talks* and a workflow that actually *does work*
- Use the four building-block terms — **trigger, actions, outputs, steps** — that recur in every single lab

---

**1. What is business workflow automation?**

A **business workflow** is a repeatable series of steps that gets work done. You already run dozens of them by hand every week. For example:

> *A customer emails an enquiry → someone records it in a spreadsheet → a salesperson is notified → they reply.*

Four small steps, but each one takes attention, and any of them can be forgotten, delayed, or done inconsistently.

**Automation** means letting software perform those steps for you — consistently, instantly, and the same way every time — instead of doing them by hand. The best candidates for automation share three traits:

| Trait | What it looks like | Everyday example |
| --- | --- | --- |
| **Repetitive** | Done the same way many times | Logging enquiries, sending confirmations |
| **Rule-based** | Clear "if this, then that" logic | If amount > $1,000, get approval |
| **Time-consuming** | Manual copying, chasing, re-typing | Re-keying form data into a spreadsheet |

**What you gain:** fewer mistakes, faster turnaround, a complete record of what happened, nothing falling through the cracks — and people freed up for higher-value work that actually needs human judgement.

> **Rule of thumb:** if you find yourself doing the same clicking, copying, and emailing over and over, it is probably a workflow waiting to be automated.

In this course you automate workflows with **two** Microsoft tools that work as a pair:

- **Power Automate** — builds the automated steps (the **flows**) that do the work.
- **Copilot Studio** — builds AI **agents** that understand natural-language requests and feed clean, structured data into those flows.

You'll learn Power Automate first (Day 1), then agents and how to combine them with your flows (Day 2).

---

**2. Standalone agents vs integrated workflows**

It helps to be clear, from the very start, about the difference between an agent that just *answers* and a workflow that *acts*.

|  | **Standalone agent** | **Integrated workflow** |
| --- | --- | --- |
| What it does | Chats and answers questions | Performs real actions across systems |
| Example | "What's your return policy?" | Logs the enquiry, emails the team, files a ticket |
| Powered by | Copilot Studio alone | Copilot Studio **+** Power Automate |
| Outcome | Information | Action **+** record **+** notification |

A **standalone agent** is genuinely useful, but it only *talks*. Ask it a question, get an answer — the conversation ends and nothing changes in your business systems.

An **integrated workflow** connects that same agent to Power Automate, so the conversation actually *triggers work*: a record gets saved, an email gets sent, an approval gets started. The customer feels heard *and* the back-office task is already done.

```
Standalone agent:   User asks  →  Agent answers           (talk only)

Integrated:         User asks  →  Agent answers
                                   └─► triggers a flow ─►  log + email + approval
                                                          (talk AND action)
```

That bridge between conversation and action is the heart of this course.

---

**3. Workflow logic: the four building blocks**

Every workflow you build — whether a simple flow or a full agent-driven process — is made of these four parts. Learn these terms now; you will use them in *every* lab.

**Trigger — *what starts the workflow***

The single event that kicks everything off. Examples:

- An **email is received**
- A **file is uploaded** to a folder
- A **form is submitted**
- A **schedule** is reached (e.g. every morning at 9 AM)
- An **agent** calls the flow

> Every flow has **exactly one** trigger, and it does nothing until that trigger fires.

**Actions — *what the workflow does***

The steps that run after the trigger, in order. Examples:

- **Send an email**
- **Add a row** to an Excel table
- **Start an approval** and wait for a decision
- **Post a message** to Teams
- **Create or update** a record

**Outputs — *the data the workflow produces or passes along***

The pieces of information that move between steps. Examples:

- The **sender's email address** from a received email
- The **customer name and product** captured by an agent
- The **approval result** ("Approved" / "Rejected")

Outputs from one step become inputs to the next — in Power Automate this is called **dynamic content**, and it's how data flows down the chain.

**Steps — *the ordered sequence as a whole***

Trigger + actions, arranged top-to-bottom, make up the **steps** of the workflow. Steps can also include:

- **Conditions** — branching with if/else logic (e.g. *if amount > $1,000, route to a manager*)
- **Loops** — repeat an action for each item in a list

**Putting it together**

```
TRIGGER            ACTIONS (steps)                       OUTPUTS
─────────          ──────────────────────────           ──────────
Email received  →  1. Read sender + subject          →  sender, subject
                   2. Add a row to Excel             →  logged record
                   3. Send notification to sales     →  confirmation
```

Read that left to right: an event happens, the flow performs a series of steps, and data (outputs) is produced and passed along the way. Keep this **Trigger → Actions → Output** mental model in your head — it is the spine of everything that follows.

---

**4. How the two days fit together**

| Day | You build | New skill | What it gives you |
| --- | --- | --- | --- |
| **Day 1** | Flows in **Power Automate** and support agents in **Copilot Studio** | Triggers, actions, outputs, knowledge, instructions and agent routing | The "hands" that do work plus specialist IT and HR assistance |
| **Day 2** | Websites connected to HTTP-triggered flows and Finance agents | HTTP, webhooks, JSON, tools, market data, news and safeguards | Complete browser → flow → agent → browser experiences |

Day 1 starts with Power Automate and then adds Copilot Studio. You will master the trigger → action → output rhythm, build IT and HR agents, and route a submitted support request to the correct specialist.

---

**Next:** Module 2: Introduction to Power Automate

---

### Module 2: Power Automate Cloud Flows

Power Automate cloud flows connect Microsoft 365 services and other systems. Every cloud flow has exactly one **trigger** and at least one **action**.

**Instant, scheduled and automated flows**

| Cloud flow | What starts it | Use it when | Course example |
| --- | --- | --- | --- |
| **Instant cloud flow** | A person deliberately selects a button, runs a flow, or invokes it from an app | The user controls the exact start time | A staff member runs a one-off test or approval |
| **Scheduled cloud flow** | A **Recurrence** trigger reaches a defined time | Work must happen at fixed intervals even when no new business event occurs | Send a daily digest every weekday at 9:00 AM |
| **Automated cloud flow** | A business event occurs in a connected service | The process should react immediately to new information | A Microsoft Form response starts Labs 1–4 and 7 |

The difference is the **trigger**, not the actions. All three types can send email, update Excel, call an agent, create an approval, or branch on a condition.

> **Decision rule:** ask “Who or what should start this process?” A person suggests instant; a clock suggests scheduled; a new record, form, file or message suggests automated.

**Instant cloud flow**

An **instant** flow waits for a person or application to invoke it deliberately. Typical triggers include **Manually trigger a flow**, **Power Apps**, and a selected-item button in a Microsoft 365 app.

Use an instant flow when:

- the user must decide exactly when the process starts;
- the user needs to supply values at run time; or
- the action is exceptional rather than continuously monitored.

Do not choose an instant flow for unattended monitoring. If a form submission should always be processed, an automated flow is the better design.

**Scheduled cloud flow**

A **scheduled** flow starts from a **Recurrence** trigger. Its configuration defines the start time, frequency, interval and time zone.

Use a scheduled flow for work such as:

- a weekday 9:00 AM reminder;
- an overnight reconciliation;
- a weekly summary; or
- a periodic check of items that have not been updated.

Scheduled flows are driven by the clock. They may find no work on a particular run, so design them to handle an empty result safely.

**Automated cloud flow**

An **automated** flow listens for a business event in a connector. Examples include **When a new response is submitted**, **When a file is created**, and **When an email arrives**.

Use an automated flow when every qualifying event should receive a consistent response. Labs 1–4 and 7 use this type because a Microsoft Forms submission is the business event.

**Compare the trigger, not the action**

The same **Send an email** action can appear in all three flow types. The flow type is determined by how it starts:

```
Person selects Run     → Instant
Recurrence time arrives → Scheduled
Business event occurs   → Automated
```

**Trigger selection and trigger outputs**

A trigger is the first card and the event subscription for the flow. It answers four design questions:

1. **Event:** what exactly has to happen?
2. **Scope:** which form, mailbox, folder, list or environment is monitored?
3. **Identity:** which connection has permission to listen?
4. **Output:** which identifiers and values become available to later actions?

The trigger output is not always the complete business record. In the Microsoft Forms pattern, the trigger returns a **Response Id**, and **Get response details** uses that identifier to retrieve the answers. This is why the first two cards are both necessary.

> A valid cloud flow needs one trigger and at least one action. An HTTP trigger by itself still produces the designer message that the flow needs a trigger **and an action**.

**The course pattern**

The Day 1 labs use one connected scenario and expand it gradually:

1. **Lab 1:** form response → confirmation email.
2. **Lab 2:** form response → Excel audit record → confirmation email.
3. **Lab 3:** event form → condition → different logging and email outcomes.
4. **Lab 4:** leave form → approval → approved or rejected notification.
5. **Labs 5–6:** build and publish specialised Copilot agents.
6. **Lab 7:** form response → route to the appropriate agent → email its reply.

**Form-trigger pattern**

A Microsoft Forms automation normally uses these first two cards:

1. **Microsoft Forms — When a new response is submitted**
2. **Microsoft Forms — Get response details**

The trigger supplies the **Response Id**. The second action retrieves the answers, which then appear as dynamic content.

```
Form submitted
    ↓
Get response details
    ↓
Use the answers in later actions
```

**Actions, dynamic content and expressions**

- An **action** changes or retrieves something after the trigger.
- **Dynamic content** is an output token selected from an earlier card, such as the respondent's Email answer.
- An **expression** calculates a value, such as `utcNow()` for an audit timestamp.

Use tokens and expressions through the designer rather than typing their labels as plain text. A typed word such as `Email` is only text; the coloured Email token carries the actual submitted value.

**Conditions and approvals**

A **Condition** evaluates a rule and creates **If yes** and **If no** branches. Test both branches with different submissions. An approval is different: **Start and wait for an approval** pauses the run until the assigned approver responds, then exposes an **Outcome** that a condition can evaluate.

**Connections and verification**

Each connector uses a saved connection. Microsoft Forms, Office 365 Outlook, Excel Online (Business), Approvals, SharePoint and Copilot Studio may each ask you to sign in.

For every flow:

1. Confirm the correct environment and account.
2. Save the flow.
3. Trigger a realistic test.
4. Open the run history and inspect inputs and outputs.
5. Confirm the real-world result: email, row, approval or agent reply.

**Data design rules**

- Use dynamic-content tokens, not typed field names.
- Keep Excel data inside a named **table**.
- Record timestamps and outcomes for auditability.
- Test every condition branch.
- Do not put passwords, API keys or confidential information in instructions, source code or email bodies.

**Next:** Lab 1 — Form to Email Confirmation

---

### Lab 0: Environment Setup — Create Your Copilot Studio & Power Automate Accounts

**Lab Title**

Environment Setup — Create Your Microsoft 365, Power Automate, and Copilot Studio Accounts

**Lab Objectives**

By the end of this lab, you will be able to:

1. Obtain a Microsoft 365 **work or school** account that can use the Power Platform
2. Create a dedicated Power Platform **Sandbox environment** (with Dataverse) for this course
3. Sign in to Power Automate and Copilot Studio and point **both** at the same environment
4. Confirm Outlook and Excel (OneDrive) are available for the later labs
5. Run a verification checklist so you start Lab 1 with zero surprises
6. Understand the difference between a work/school account and a personal account

**Prerequisites**

- A web browser (Microsoft Edge or Google Chrome recommended)
- A mobile phone (used once for security verification)
- A credit card *(only if you create a new Business trial in Option B — it is **not** charged during the free month)*
- About 30–40 minutes

> **Tip — Which account should I use?** - **Option A — You already have a Microsoft 365 work/school account** (e.g. `name@company.com` provided by your organization). Try this first — you may already have everything you need. Skip Option B and go straight to **Step 1**. - **Option B — You do NOT have a work/school account** (you only have a personal `@outlook.com` / `@gmail.com`). Power Automate and Copilot Studio require a *work or school* account, so you'll create one via a free **Microsoft 365 Business trial**. Do **Option B** first, then continue from Step 1.

> **⚠️ Warning — Why not the Microsoft 365 Developer Program?** As of 2024, Microsoft restricted the free Developer Program E5 sandbox to people with an active **Visual Studio Enterprise or Professional subscription**. If you sign up without one you'll see *"You don't currently qualify for a Microsoft 365 Developer Program sandbox subscription."* — so we **do not** use that path in this course. Use **Option B** instead.

**Workflow Visual**

![Lab 0 shared course environment flowchart](<labs/Day 1/Lab 0 - Environment Setup/assets/flowchart.png>)

The same work or school account and Course Sandbox environment connect every Power Automate flow and Copilot Studio agent used later.

**Packaged Flow**

No flow package applies to Lab 0 because this lab creates and verifies the environment before any flow exists. The first importable flow is supplied in Lab 1.

**Scenario**

You have joined **ACME Pte Ltd's Digital Operations project team** as a junior automation specialist. The production tenant contains customer and employee data, so the project manager will not allow experiments there. Your first task is to prepare a controlled **Course Sandbox** where flows, connectors, agent knowledge and test records can be built safely.

| Workplace detail | Lab interpretation |
| --- | --- |
| Your role | Junior automation specialist |
| Stakeholders | Power Platform administrator, customer-operations manager and IT security |
| Operational risk | A learner accidentally sends test emails or writes data into a production system |
| Success measure | Power Automate and Copilot Studio use the same sandbox environment and all required connections can be verified |

**Real-world extension:** An organisation would also apply environment roles, Data Loss Prevention policies, service accounts, naming standards and a development → test → production deployment process.

---

**Step-by-Step Guide**

**Option B (only if you have no work/school account): Create a free Microsoft 365 Business trial (~15 minutes)**

This creates a brand-new *work* account such as `admin@yourname.onmicrosoft.com` with Microsoft 365 (Outlook, Excel, OneDrive, SharePoint) — exactly what Power Automate and Copilot Studio need. Skip this entirely if you already have a work/school account.

1. Open a browser and go to **<a href="https://www.microsoft.com/microsoft-365/business" target="_blank" rel="noopener">https://www.microsoft.com/microsoft-365/business</a>** (or search "Microsoft 365 Business Standard free trial").
2. Choose **Microsoft 365 Business Standard** and select **Try free for 1 month**.
3. Enter an email address to start. When prompted, choose **Set up account** / **Create a new account**.
4. Fill in your details (name, business name — you may use your own name, country, phone for verification).
5. Create your **sign-in details**: a username and a domain, giving you something like `admin@yourname.onmicrosoft.com`. **Write these down** — this is the account you'll use for the entire course.
6. Verify with the code sent to your phone.
7. Add a **payment method** (credit card). You are **not charged during the 1-month free trial**.
8. Wait 1–2 minutes for provisioning. You now have a Microsoft 365 work tenant.

> **Tip:** In a classroom, your trainer may provide a ready-made account. Ask before creating a trial so you don't duplicate accounts.

> **⚠️ Warning — Avoid surprise charges.** If you don't intend to keep the trial, set a calendar reminder and cancel **before the renewal date** in the **Microsoft 365 admin center → Billing → Your products**.

---

**Step 1: Sign in to the Microsoft 365 portal (~5 minutes)**

1. Go to **<a href="https://www.office.com" target="_blank" rel="noopener">https://www.office.com</a>** (or **<a href="https://m365.cloud.microsoft" target="_blank" rel="noopener">https://m365.cloud.microsoft</a>**).
2. Select **Sign in** and enter your **work/school account** (Option A) or your new **Business trial account** (Option B), then your password.
3. If this is your first sign-in, you may be asked to set up multi-factor authentication (MFA). Follow the prompts using your mobile phone.
4. Once signed in, you should see the Microsoft 365 home page with app tiles (Outlook, Word, Excel, etc.).
5. Open **Outlook** (click the Outlook tile) and send yourself a quick test email to confirm it works — you'll rely on Outlook in Lab 1.
6. Open **Excel** and create a blank workbook to confirm it saves to **OneDrive** — you'll rely on this in Lab 2. You can discard the test workbook afterwards.

> **⚠️ Warning — No Outlook/Excel tiles?** Your account may not have a Microsoft 365 license. The *Send an email* action in Lab 1 fails with **"Unauthorized"** when the account has **no mailbox**. Ask your IT administrator to assign a license, or use the Business trial account from Option B (which always has a mailbox).

---

**Step 2: Create your "Course Sandbox" environment (~7 minutes)**

An **environment** is a container that holds your flows, agents, and data. For this course we'll create a dedicated **Sandbox** environment with **Dataverse** turned on, so the Day 1 Copilot Studio agents and later HTTP labs have the required services.

1. Open a new tab and go to the **Power Platform admin center**: **<a href="https://admin.powerplatform.microsoft.com" target="_blank" rel="noopener">https://admin.powerplatform.microsoft.com</a>**.
2. Sign in with the **same account** from Step 1.
3. In the left menu, select **Manage → Environments**.
4. Select **+ New** (top of the page).
5. Fill in the **New environment** panel:  —  **Name:** `Course Sandbox`  —  **Type:** **Sandbox**  —  **Region:** your nearest region (e.g. Asia, Singapore)  —  **Add a Dataverse data store:** **Yes**  ← important
6. Select **Next**, accept the defaults (language English, currency your local currency) and set **Security group** to **None** (the field is required — *None* means open access), then select **Save**.
7. Wait 1–3 minutes. The environment appears in the list with status **Ready**. Refresh if needed.

> **Tip:** If your tenant blocks creating environments (some organizations restrict this), use the existing **default** environment instead — just remember to select that *same* environment in both Power Automate and Copilot Studio in the next steps.

---

**Step 3: Sign in to Power Automate and select the environment (~5 minutes)**

Power Automate is where you build the automated workflows (called **flows**).

1. Open a new tab and go to **<a href="https://make.powerautomate.com" target="_blank" rel="noopener">https://make.powerautomate.com</a>**.
2. Sign in with the **same account**.
3. The first time, you may be asked to **select your country/region** — choose the correct one and select **Get started**.
4. You'll see the Power Automate home page with a left-hand menu: **Home, Create, Templates, Learn, My flows**, plus pinned items such as **Approvals** and a **More** menu (items like **Connections** live under **More**).
5. Look at the **top-right corner** — there is an **Environment selector**. Click it and choose **Course Sandbox** (the one you created in Step 2). All your flows will be built here.
6. Select **My flows** in the left menu — it will be empty for now. That's expected.

> **⚠️ Warning:** The environment selector is the single most common source of "where did my flow go?" confusion. If you build a flow in the wrong environment, it simply won't appear when you switch. Always confirm **Course Sandbox** is showing top-right before you build.

> **Tip — Free Power Automate:** A Power Automate use-rights plan is included with most Microsoft 365 licenses, which is enough for this course. If prompted, you can also start a **free 90-day trial** of Power Automate Premium.

---

**Step 4: Sign in to Copilot Studio and match the same environment (~5 minutes)**

Copilot Studio is where you build the AI **agents** (used on Day 2).

1. Open a new tab and go to **<a href="https://copilotstudio.microsoft.com" target="_blank" rel="noopener">https://copilotstudio.microsoft.com</a>**.
2. Sign in with the **same account** again.
3. If prompted, select your **country/region** and select **Start free trial** (or **Try free**). This activates a **30-day Copilot Studio trial** at no cost (when it expires you can extend it once by another 30 days).
4. Wait for the workspace to load. In the new experience, the Copilot Studio  —  home page shows **Agent** and **Workflow** creation choices.
5. If the classic home page opens, select **Try it now** or turn on  —  **New experience** before continuing with the course labs.
6. Look at the **Environment selector** in the **top menu** and choose  —  **Course Sandbox** — the **same** environment you selected in Power  —  Automate.
7. Do **not** create an agent yet — you'll do that in a later lab. For now, just confirm the page loads in the correct environment.

> **⚠️ Warning — Both tools MUST use the same environment.** Your agents (Copilot Studio) and your flows (Power Automate) can only call each other when they live in the **same** environment. If Power Automate shows *Course Sandbox* but Copilot Studio shows *Default* (or vice-versa), they cannot connect. Use the environment selector in each product's top menu and choose **Course Sandbox**.

---

**Step 5: Verify your full setup (~5 minutes)**

Run this quick checklist. Each item should already be true if the steps above succeeded.

| # | Check | Where |
| --- | --- | --- |
| 1 | I can sign in and see app tiles | <a href="https://office.com" target="_blank" rel="noopener">https://office.com</a> |
| 2 | I can open Outlook and send myself an email | Outlook |
| 3 | I can open Excel and it saves to OneDrive | Excel / OneDrive |
| 4 | My **Course Sandbox** environment shows status **Ready** | <a href="https://admin.powerplatform.microsoft.com" target="_blank" rel="noopener">https://admin.powerplatform.microsoft.com</a> |
| 5 | Power Automate home page loads and **Course Sandbox** is selected | <a href="https://make.powerautomate.com" target="_blank" rel="noopener">https://make.powerautomate.com</a> |
| 6 | Copilot Studio loads, my trial is active, and **Course Sandbox** is selected | <a href="https://copilotstudio.microsoft.com" target="_blank" rel="noopener">https://copilotstudio.microsoft.com</a> |
| 7 | Power Automate and Copilot Studio show the **same** environment | Environment selector in each product's top menu |

If all seven are checked, your environment is ready.

---

**Checkpoint**

> **Workplace evidence:** Capture the environment selectors in Power Automate and Copilot Studio plus the green connection status. In a real project, these screenshots form part of the deployment-readiness record.

You should now have:

- ✅ A working Microsoft 365 **work/school** account (Option A or B)
- ✅ A Power Platform **Sandbox** environment named **Course Sandbox** with **Dataverse = Yes**, status **Ready**
- ✅ Power Automate open with **Course Sandbox** selected top-right
- ✅ Copilot Studio open (trial active) with **Course Sandbox** selected top-right
- ✅ Outlook and Excel (OneDrive) confirmed working

**Troubleshooting**

| Problem | Solution |
| --- | --- |
| "You can't sign in here with a personal account" | Power Platform needs a *work/school* account. Use **Option B** to create one via the Business trial. |
| "You don't currently qualify for a Microsoft 365 Developer Program sandbox subscription" | The Developer Program now requires a Visual Studio subscription. Use **Option B** (Business trial) instead. |
| **+ New** environment button is greyed out / missing | Your tenant restricts environment creation. Ask an admin, or use the **Default** environment and select it in both tools. |
| Environment created but stuck on **Preparing** | Wait 2–3 minutes and refresh the Environments list; provisioning Dataverse takes a moment. |
| Power Automate says "no environment" | Refresh, re-select your region, then pick **Course Sandbox** in the environment selector. |
| Copilot Studio "Start free trial" button missing | You may already have a license — just proceed. Otherwise sign out and back in. |
| Different environment shows in each tool | Click the environment selector (top-right) in **both** tools and choose **Course Sandbox**. |
| No Outlook/Excel tiles | Your account lacks a Microsoft 365 license (and possibly a mailbox) — ask IT or use the Business trial account (Option B). |

**Key Takeaways**

- Power Automate and Copilot Studio both need a **work/school** account — personal accounts won't work.
- The **Microsoft 365 Developer Program** is no longer a free path; use a **Business trial** if you need an account.
- An **environment** is the container for your work; this course uses one named **Course Sandbox** (Sandbox type, Dataverse = Yes).
- The **#1 setup mistake** is having the two tools on **different environments** — always verify the environment selector matches in both.

**Duration**

~30–40 minutes

**Next Steps**

Read Module 1: Workflow Automation Concepts and Module 2: Power Automate Cloud Flows, then proceed to Lab 1 — Form to Email Confirmation.

---

### Lab 1 — Form to Email Confirmation

**Goal**

Create and verify an **automated cloud flow** that starts when a learner submits a Microsoft Form and sends a personalised confirmation to the email address entered in the form.

**Duration**

Approximately 40 minutes.

**Prerequisites**

- Completed Lab 0
- Signed in to Microsoft Forms, Power Automate and Outlook with the course account
- Correct Power Platform environment selected
- A mailbox-enabled Microsoft 365 account

**Optional import accelerator**

Import Lab1-Form-to-Email-Confirmation-NEW.zip through **My flows → Import → Import Package (Legacy)** and choose **Create as new**. Reconnect Microsoft Forms and Outlook, select the Course Enquiry Form, then replace every `MAP_*_AFTER_IMPORT` placeholder with the matching dynamic answer before saving. The imported flow name ends with **`(NEW)`**.

**Scenario**

A training administrator needs every website-style course enquiry to receive an immediate acknowledgement. The requester, not the flow owner, must receive the message.

**Form design**

Create a form named `Course Enquiry Form` with four **Required** questions:

| Question | Type | Setting |
| --- | --- | --- |
| Name | Text | Required |
| Email | Text | Required |
| Tel | Text | Required |
| Message | Text | Required; Long answer enabled |

**Workflow visual**

![Lab 1 form-to-email workflow](<labs/Day 1/Lab 1 - Forms Email Confirmation/assets/flowchart.png>)

The form submission starts the flow. **Get response details** retrieves the four answers, and Outlook sends the confirmation to the submitted email address.

**Expected result**

```
One form submission
→ one successful Power Automate run
→ one personalised email to the submitted address
```

**Detailed step-by-step**

**Part A — Create the Microsoft Form**

1. Open `https://forms.office.com`.
2. Confirm the profile icon shows your course account.
3. Select **New Form**.
4. Select **Untitled form** and enter `Course Enquiry Form`.
5. In the description, enter `Submit your contact details and course enquiry.`
6. Select **Add new**.
7. Choose **Text**.
8. Enter `Name`.
9. Turn **Required** on.
10. Select **Add new → Text**.
11. Enter `Email`.
12. Turn **Required** on.
13. Select **Add new → Text**.
14. Enter `Tel`.
15. Turn **Required** on.
16. Select **Add new → Text**.
17. Enter `Message`.
18. Turn **Required** on.
19. Select the question's **… More settings for question** menu.
20. Turn **Long answer** on.
21. Select **Collect responses** and confirm the form is available to the intended classroom users.
22. Close the collection panel without submitting yet.

**Part B — Create the automated cloud flow**

1. Open `https://make.powerautomate.com`.
2. Check the environment selector in the top-right corner.
3. Select the same course environment used in Lab 0.
4. In the left navigation, select **Create**.
5. Select **Automated cloud flow**.
6. In **Flow name**, enter `Lab 1 - Form Email Confirmation`.
7. In **Choose your flow's trigger**, search for `Microsoft Forms`.
8. Select **When a new response is submitted**.
9. Select **Create**.
10. Open the trigger card if it is collapsed.
11. In **Form Id**, select `Course Enquiry Form`.
12. Select the **+** below the trigger.
13. Select **Add an action**.
14. Search for `Get response details`.
15. Choose **Microsoft Forms — Get response details**.
16. In **Form Id**, select `Course Enquiry Form`.
17. Click inside **Response Id**.
18. Open **Dynamic content**.
19. Under the trigger, select **Response Id**.
20. Confirm the field displays a dynamic-content token, not typed words.

**Part C — Configure the confirmation email**

1. Select the **+** below **Get response details**.
2. Select **Add an action**.
3. Search for `Send an email`.
4. Choose **Office 365 Outlook — Send an email (V2)**.
5. If prompted, select **Sign in** and connect the mailbox-enabled course account.
6. Click inside **To**.
7. From **Dynamic content**, select the form answer **Email**.
8. In **Subject**, enter:

```
Thank you for your enquiry
```

9. Click inside **Body**.
10. Enter `Hello `.
11. Insert the **Name** dynamic-content token.
12. Continue the body with:

```
,

Thank you for your enquiry. We received the following message:
```

13. On the next line, insert the **Message** token.
14. Add:

```

We will contact you shortly.
```

15. Check that **To**, **Name** and **Message** are coloured tokens.
16. Select **Save**.
17. Wait for the saved confirmation.

**Part D — Submit and test**

1. Return to `Course Enquiry Form`.
2. Select **Preview**.
3. Complete the form with:  —  Name: `Jane Tan`  —  Email: an address you can access  —  Tel: `61234567`  —  Message: `Please send me the next course schedule.`
4. Select **Submit** once.
5. Return to Power Automate.
6. Open **My flows → Lab 1 - Form Email Confirmation**.
7. Open the newest item in **28-day run history**.
8. Confirm the trigger, Get response details and email action each show a green check.
9. Open the email action.
10. Verify its **Inputs** show the submitted address.
11. Open Outlook for that address.
12. Confirm exactly one email arrived.
13. Confirm the greeting says `Hello Jane Tan`.
14. Confirm the submitted message is reproduced correctly.

**Checkpoint**

Retain:

- the completed form Preview;
- the successful flow run;
- the email showing the correct recipient, name and message.

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| No run starts | The trigger's Form Id must match the form you submitted |
| Blank answers | Response Id must be the trigger's dynamic token; both Form Id values must match |
| Email goes to the maker | Use the form's `Email` answer in **To**, not a fixed address |
| `Name` appears literally | Delete typed text and insert the dynamic-content token |
| Outlook action is unauthorised | Reconnect with a mailbox-enabled Microsoft 365 account |
| Repeated emails | Confirm only one enabled flow watches this form and submit only once |

**Key takeaways**

- A form submission is an event, so this is an **automated cloud flow**.
- The Forms trigger supplies a Response Id; Get response details supplies the answers.
- Dynamic content connects submitted data to the email action.
- Run history and the received email are both required evidence.

**Next:** Lab 2 — Log the Enquiry and Send Email

---

### Lab 2 — Log the Enquiry and Send Email

**Goal**

Expand Lab 1 so every form submission is logged in `Enquiry Log.xlsx` before the confirmation email is sent.

**Duration**

Approximately 45 minutes.

**Prerequisites**

- Completed and tested Lab 1
- `Course Enquiry Form`
- Enquiry Log.xlsx
- OneDrive for Business or SharePoint access

**Optional import accelerator**

Import Lab2-Log-Enquiry-and-Send-Email-NEW.zip through **My flows → Import → Import Package (Legacy)** and choose **Create as new**. Reconnect Forms, Excel and Outlook; select the Course Enquiry Form, `Enquiry Log.xlsx` and table `EnquiryLog`; then replace every `MAP_*_AFTER_IMPORT` placeholder. The imported flow name ends with **`(NEW)`**.

**Scenario**

The training team needs a shared enquiry register for follow-up and reporting. A confirmation should be sent only after Power Automate records the enquiry successfully.

**Workflow visual**

![Lab 2 form-to-Excel-and-email workflow](<labs/Day 1/Lab 2 - Forms Enquiry Logging/assets/flowchart.png>)

Lab 2 reuses the Lab 1 trigger and email. The new Excel action is inserted between them.

**Workbook design**

The supplied workbook contains table `EnquiryLog`:

| Timestamp | Name | Email | Tel | Message | Status | Source |
| --- | --- | --- | --- | --- | --- | --- |

**Detailed step-by-step**

**Part A — Upload and verify the workbook**

1. Download or locate `Enquiry Log.xlsx` in this lab's `assets` folder.
2. Open OneDrive for Business or the course SharePoint document library.
3. Create a folder named `Power Automate Lab Data` if it does not exist.
4. Select **Upload → Files**.
5. Upload `Enquiry Log.xlsx`.
6. Open the uploaded workbook in Excel for the web.
7. Confirm the worksheet is named `Enquiries`.
8. Click any header cell.
9. Open **Table → Table Name** or the **Table Design** tab.
10. Confirm the table name is `EnquiryLog`.
11. Confirm all seven column headings are present.
12. Close the workbook tab.

**Part B — Copy the working Lab 1 flow**

1. Open `https://make.powerautomate.com`.
2. Select **My flows**.
3. Find `Lab 1 - Form Email Confirmation`.
4. Select its **… More commands** menu.
5. Select **Save As**.
6. Enter `Lab 2 - Log Enquiry and Email`.
7. Select **Save**.
8. Open the copied flow.
9. Select **Edit**.
10. Confirm it still contains:  —  When a new response is submitted;  —  Get response details;  —  Send an email (V2).

**Part C — Insert Excel logging**

1. Locate the connector line between **Get response details** and **Send an email (V2)**.
2. Select the **+** on that connector.
3. Select **Add an action**.
4. Search for `Add a row into a table`.
5. Choose **Excel Online (Business) — Add a row into a table**.
6. If prompted, sign in with the course Microsoft 365 account.
7. In **Location**, select the OneDrive or SharePoint location used in Part A.
8. If using SharePoint, choose the correct **Document Library**.
9. In **File**, browse to `Power Automate Lab Data/Enquiry Log.xlsx`.
10. In **Table**, select `EnquiryLog`.
11. Wait for the seven column fields to appear.

**Part D — Map the table columns**

1. Click inside **Timestamp**.
2. Select the **Expression** or **fx** tab.
3. Enter:

```
utcNow()
```

4. Select **Add** or **Update**.
5. Map **Name** to the form's **Name** token.
6. Map **Email** to the form's **Email** token.
7. Map **Tel** to the form's **Tel** token.
8. Map **Message** to the form's **Message** token.
9. In **Status**, enter `New`.
10. In **Source**, enter `Course Enquiry Form`.
11. Confirm every form answer comes from **Get response details**.
12. Confirm the Outlook action remains after Excel.
13. Open the Outlook action.
14. Update its body to include:

```
Your enquiry has been logged and will be reviewed by our training team.
```

15. Select **Save**.

**Part E — Test two submissions**

1. Open `Course Enquiry Form`.
2. Submit:  —  Name: `Aisha Lim`  —  Email: an address you can access  —  Tel: `62345678`  —  Message: `I would like the corporate course outline.`
3. Wait for the flow to complete.
4. Open its run history.
5. Confirm the Excel action completed before Outlook.
6. Open `Enquiry Log.xlsx` in Excel for the web.
7. Confirm a new row contains Aisha's complete details.
8. Confirm **Status** is `New`.
9. Confirm **Source** is `Course Enquiry Form`.
10. Confirm the email arrived.
11. Submit a second response with a different name and message.
12. Confirm a second row is appended and the first row remains unchanged.

**Checkpoint**

- Two successful runs
- Two separate rows in `EnquiryLog`
- Two confirmation emails sent to the submitted addresses

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| Workbook not listed | It must be in OneDrive for Business or SharePoint, not only on the local computer |
| Table not listed | Select named table `EnquiryLog`; loose worksheet cells are not a table |
| Columns do not appear | Re-select the file and table, then wait for metadata to load |
| File locked | Close desktop Excel and retry |
| Wrong time format | `utcNow()` records UTC; apply workbook display formatting if required |
| Email sent but no row | Ensure Excel is before Outlook and inspect the Excel action's error |

**Key takeaways**

- Lab 2 extends a verified flow rather than rebuilding it.
- A named Excel table provides a basic audit trail.
- Action order determines whether email is sent after successful logging.
- Test with multiple records to verify rows append correctly.

**Next:** Lab 3 — Event Registration Branching

---

### Lab 3 — Event Registration Branching

**Goal**

Use a Microsoft Forms choice and a Power Automate condition to log and notify people differently depending on whether they will join an event.

**Duration**

Approximately 70 minutes.

**Prerequisites**

- Microsoft Forms, Excel Online, Outlook and Power Automate access
- Event Log.xlsx
- An administrator mailbox: `training1@tertiaryinfotech.onmicrosoft.com`

**Optional import accelerator**

Import Lab3-Event-Registration-Branching-NEW.zip through **My flows → Import → Import Package (Legacy)** and choose **Create as new**. Reconnect Forms, Excel and Outlook; select the Event Registration Form, `Event Log.xlsx` and table `EventLog`; then map the four form answers and the Yes/No condition. The imported flow name ends with **`(NEW)`**.

**Scenario**

The events team needs participant details when a person is joining. When a person declines, the system should thank them and invite them to a future event. Both decisions must be logged.

**Workflow visual**

![Lab 3 event registration branching workflow](<labs/Day 1/Lab 3 - Event Registration Branching/assets/flowchart.png>)

The condition has two independent paths. Both paths write an audit row before sending their notification.

**Detailed step-by-step**

**Part A — Create the event form**

1. Open Microsoft Forms.
2. Select **New Form**.
3. Name it `Event Registration Form`.
4. Add a **Text** question named `Name`; turn **Required** on.
5. Add a **Text** question named `Email`; turn **Required** on.
6. Add a **Text** question named `Tel`; turn **Required** on.
7. Add a **Choice** question named `Joining the Event?`.
8. Set the first option to `Yes`.
9. Set the second option to `No`.
10. Remove any additional blank option.
11. Turn **Required** on.
12. Select **Preview** and confirm only Yes or No can be selected.

**Part B — Upload Event Log.xlsx**

1. Open OneDrive for Business or the course SharePoint library.
2. Open `Power Automate Lab Data`.
3. Upload `Event Log.xlsx`.
4. Open it in Excel for the web.
5. Confirm the worksheet is `Registrations`.
6. Confirm the named table is `EventLog`.
7. Confirm the columns are Timestamp, Name, Email, Tel, JoiningEvent, NotificationSent and Notes.
8. Close the workbook.

**Part C — Create the flow and condition**

1. Open Power Automate.
2. Select **Create → Automated cloud flow**.
3. Name it `Lab 3 - Event Registration Branching`.
4. Select **Microsoft Forms — When a new response is submitted**.
5. Select **Create**.
6. Set **Form Id** to `Event Registration Form`.
7. Add **Microsoft Forms — Get response details**.
8. Set the same Form Id.
9. Set **Response Id** to the trigger's Response Id token.
10. Select **+ → Add an action**.
11. Search for `Condition`.
12. Select **Control — Condition**.
13. In the left condition field, insert **Joining the Event?** from Get response details.
14. Set the operator to **is equal to**.
15. In the right field, enter `Yes`.
16. Confirm Power Automate displays **If yes** and **If no** branches.

**Part D — Configure the Yes branch**

1. Under **If yes**, select **Add an action**.
2. Add **Excel Online (Business) — Add a row into a table**.
3. Select the workbook location and `Event Log.xlsx`.
4. Select table `EventLog`.
5. Map:  —  Timestamp: expression `utcNow()`  —  Name: form Name  —  Email: form Email  —  Tel: form Tel  —  JoiningEvent: `Yes`  —  NotificationSent: `Admin`  —  Notes: `Participant details sent to administrator`
6. Below Excel, add **Office 365 Outlook — Send an email (V2)**.
7. In **To**, enter `training1@tertiaryinfotech.onmicrosoft.com`.
8. In **Subject**, enter `New event participant - ` and insert the Name token.
9. In **Body**, add labels and tokens for Name, Email, Tel and Joining the Event.
10. Confirm the email contains no fixed sample participant details.

**Part E — Configure the No branch**

1. Under **If no**, select **Add an action**.
2. Add **Excel Online (Business) — Add a row into a table**.
3. Select `Event Log.xlsx` and table `EventLog`.
4. Map the common form fields.
5. Enter:  —  JoiningEvent: `No`  —  NotificationSent: `User`  —  Notes: `Next-event message sent`
6. Below Excel, add **Send an email (V2)**.
7. Set **To** to the submitted **Email** token.
8. Set **Subject** to `Thank you for your response`.
9. Build the body:

```
Hello [Name],

Thank you for letting us know. We are sorry you cannot join this event and look
forward to welcoming you next time.
```

10. Replace `[Name]` with the Name dynamic-content token.
11. Select **Save**.

**Part F — Test both branches**

1. Submit the form with Name `Daniel Wong` and **Joining the Event? = Yes**.
2. Open the newest flow run.
3. Confirm **If yes** ran and **If no** was skipped.
4. Confirm EventLog contains a Yes row.
5. Confirm the administrator email contains Daniel's details.
6. Submit again with Name `Mei Chen` and **Joining the Event? = No**.
7. Confirm **If no** ran and **If yes** was skipped.
8. Confirm EventLog contains a No row.
9. Confirm Mei received the next-event email.
10. Compare the two rows and verify NotificationSent differs.

**Checkpoint**

| Test | Expected Excel result | Expected email |
| --- | --- | --- |
| Yes | JoiningEvent = Yes; NotificationSent = Admin | Participant details to administrator |
| No | JoiningEvent = No; NotificationSent = User | Thanks and next-time message to user |

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| Every response goes to No | Compare against exact value `Yes`; remove spaces or punctuation |
| Both emails sent | Ensure each email is inside the correct condition branch |
| Wrong recipient | Yes uses the administrator address; No uses the submitted Email token |
| Excel row incomplete | Map fields from Get response details, not from the trigger |
| Only one branch tested | Submit two separate responses with opposite choices |

**Key takeaways**

- A condition creates mutually exclusive execution paths.
- Both business outcomes must be logged and tested.
- The branch controls the recipient, wording and audit values.

**Next:** Lab 4 — Leave Application Approval

---

### Lab 4 — Leave Application Approval

**Goal**

Create a leave application process that pauses for a manager to approve or reject the request and emails the applicant with the decision and comments.

**Duration**

Approximately 45 minutes.

**Prerequisites**

- Microsoft Forms, Approvals and Outlook access
- A valid manager or classroom test user in the Microsoft 365 tenant
- Completed understanding of conditions from Lab 3

**Optional import accelerator**

Import Lab4-Leave-Application-Approval-NEW.zip through **My flows → Import → Import Package (Legacy)** and choose **Create as new**. Reconnect Forms, Approvals and Outlook; select the Leave Application Form; map its answers; and verify the manager and responder email fields. The imported flow name ends with **`(NEW)`**.

**Scenario**

An employee submits leave dates and a reason. The manager makes the decision; the flow records the decision in its run history and sends the appropriate message.

**Workflow visual**

![Lab 4 leave approval workflow](<labs/Day 1/Lab 4 - Leave Approval/assets/flowchart.png>)

The flow waits at the approval action, resumes when the manager responds, then follows the approved or rejected branch.

**Detailed step-by-step**

**Part A — Create the leave form**

1. Open Microsoft Forms.
2. Select **New Form**.
3. Name it `Leave Application Form`.
4. Add a required **Text** question named `Name`.
5. Add a required **Date** question named `Leave from date`.
6. Add a required **Date** question named `Leave end date`.
7. Add a required **Choice** question named `Leave Type`.
8. Add the choices:  —  Annual  —  Medical  —  Compassionate  —  Unpaid
9. Add a required **Text** question named `Reason for Leave`.
10. Enable **Long answer** for the reason.
11. Open **Settings**.
12. Select **Only people in my organisation can respond**.
13. Turn on **Record name** so Forms supplies the responder's identity and email without adding an Email question.
14. Preview the form.
15. Confirm the date questions display date selectors.
16. Confirm only one leave type can be selected.

**Part B — Create the automated flow**

1. Open Power Automate.
2. Select **Create → Automated cloud flow**.
3. Name it `Lab 4 - Leave Application Approval`.
4. Select **When a new response is submitted**.
5. Select **Create**.
6. Set **Form Id** to `Leave Application Form`.
7. Add **Get response details**.
8. Select the same Form Id.
9. Insert the trigger's **Response Id** token.

**Part C — Configure the manager approval**

1. Select **+ → Add an action** below Get response details.
2. Search for `Start and wait for an approval`.
3. Select **Approvals — Start and wait for an approval**.
4. In **Approval type**, select **Approve/Reject – First to respond**.
5. In **Title**, enter `Leave request - `.
6. Insert the submitted **Name** token after the hyphen.
7. In **Assigned to**, enter the manager's Microsoft 365 work address.
8. Press Enter so the address resolves.
9. In **Details**, create labelled lines for:  —  Applicant name  —  Leave from date  —  Leave end date  —  Leave type  —  Reason
10. Insert the matching dynamic-content token after each label.
11. In **Item link description**, enter `Leave Application Form response` if the field is available.
12. Do not place medical details in optional fields that expose them more broadly.

**Part D — Branch on the outcome**

1. Add **Control — Condition** below the approval.
2. In the left field, choose **Outcome** from the approval action.
3. Select **is equal to**.
4. In the right field, enter `Approve`.
5. Under **If yes**, add **Office 365 Outlook — Send an email (V2)**.
6. Set **To** to **Responders' Email** from Get response details.
7. Set **Subject** to `Leave request approved`.
8. In the body, include the applicant's name, date range, leave type and **Responses Comments** from the approval.
9. Under **If no**, add another **Send an email (V2)**.
10. Set **To** to **Responders' Email** from Get response details.
11. Set **Subject** to `Leave request not approved`.
12. In the body, include the date range and **Responses Comments**.
13. Add a sentence asking the applicant to contact the manager if clarification is needed.
14. Select **Save**.

**Part E — Test approval**

1. Submit the form with:  —  Name: `Ravi Kumar`  —  Leave from date: a future date  —  Leave end date: the following day  —  Leave Type: Annual  —  Reason: `Family appointment`
2. Open the approval from Teams, Outlook or **Power Automate → Approvals**.
3. Confirm the approval displays every submitted field.
4. Select **Approve**.
5. Enter comment `Approved for the stated dates.`
6. Submit the decision.
7. Open run history.
8. Confirm the flow resumed and the Yes branch ran.
9. Confirm the responder's test mailbox received the approval email and comment.

**Part F — Test rejection**

1. Submit a second leave request with different dates.
2. Open the new approval.
3. Select **Reject**.
4. Enter `Please discuss alternative dates with your manager.`
5. Submit the decision.
6. Confirm the No branch ran.
7. Confirm the rejection email contains the comment.
8. Confirm the approval and rejection runs remain available as evidence.

**Governance checkpoint**

- Use only authorised approvers.
- Limit access to reasons and medical information.
- Never use an agent or flow to make the manager's decision.
- A production leave process should use the organisation's approved HR record system.

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| Approval never arrives | Assigned-to address must be a valid tenant user with Approvals access |
| Flow remains running | It is waiting for the manager; open and complete the approval |
| Wrong branch | Compare Outcome with exact value `Approve` |
| Comments are blank | Insert **Responses Comments** from the approval action |
| External address rejected | Use a tenant account approved for classroom testing |

**Key takeaways**

- Human approval is an action inside an automated flow, not a separate flow type.
- The flow pauses safely and resumes after the decision.
- Approved and rejected outcomes require separate tests and communication.

**Next:** Module 3: Copilot Studio Agent Building Blocks

---

### Module 3: Copilot Studio Agent Building Blocks

A Copilot Studio agent combines instructions, trusted information and actions so it can help a user complete a defined task. A useful agent is not just a chat box; it is a governed system with clear boundaries.

> **Interface used in this course:** Use the new Copilot Studio experience. Agent components are configured from **Build**, conversations are tested in **Preview**, repeatable tests are managed in **Evaluate**, and recent activity is reviewed in **Monitor**. The new agent experience is production-ready preview; the redesigned workflow canvas is public preview and can change.

**The six building blocks**

| Building block | Meaning | Design question |
| --- | --- | --- |
| **Knowledge base** | Approved sources the agent can search to ground an answer, such as uploaded files or SharePoint content | Which source is authoritative, current and permitted? |
| **Skills** | Reusable, structured instructions that define a capability the agent can activate | What job should the agent be able to complete? |
| **Tools** | Connected functions, APIs or workflows that read data, call services or create outcomes | Which system action is safe, authenticated and auditable? |
| **Memory** | Context retained during a conversation through conversation history and variables; persistent memory depends on enabled product features and governance | What should be remembered, for how long and with what consent? |
| **Model** | The generative AI model that interprets the request and composes a response | Does the selected model provide the required quality, latency and governance? |
| **Instructions** | The behavioural rules defining role, tone, scope, safety and escalation | What must the agent always do or never do? |

> In the new experience, **Instructions** are edited directly on the **Build** tab. Treat them as policy, not decoration.

**1. Knowledge base**

Knowledge grounds answers in approved content. Uploaded FAQ files suit a small, stable source; SharePoint suits governed organisational documents that owners already maintain. Knowledge is not a substitute for live transactional data.

**2. Skills**

A skill is a reusable business capability, such as answering an IT question, triaging a request or obtaining a finance explanation. In the new experience, skills are structured instructions managed from the **Skills** component on **Build**. Define the user outcome first, then add only the components needed to achieve it.

**3. Tools**

A tool lets the agent perform or retrieve something beyond generating text. Examples include a workflow, a connector action, an API or another approved agent. Give a tool a clear name and description so the orchestrator knows when to call it, and validate its inputs and outputs.

**4. Memory**

Memory is the conversational context available to the agent. Short-term context helps it understand follow-up questions. Persistent personalisation, if enabled and approved, requires stronger privacy, retention and consent controls. Never treat memory as an authoritative database.

**5. Model**

The model interprets language, reasons over context and composes the answer. Model selection affects quality, latency, cost and governance. The model does not replace trusted knowledge, deterministic tools or explicit safety instructions.

**6. Instructions**

Instructions define the agent's role, tone, boundaries, evidence rules and escalation behaviour. Write them as testable rules: what sources to use, what data never to request, how to handle uncertainty and where to redirect an unsupported request.

**New interface map**

| Authoring task | New agent experience | New workflow experience |
| --- | --- | --- |
| Configure | **Build** tab: Instructions editor and components panel | **Build** tab: Start card, Add pane and node configuration panel |
| Add knowledge | **Build → Knowledge** in the components panel | Add knowledge inside an **Agent** node when that workflow step needs grounding |
| Add an action | **Build → Tools** | Select **+** or **Add a step**, then choose **Agent**, **Connector**, **Function**, **Variable**, **If/Else**, **Loop** or another Add category |
| Test | **Preview** for interactive chat; **Evaluate** for repeatable test sets | Play button for an end-to-end test; node **Test** panel for one step |
| Review runs | **Monitor** | **Activity** for run details and **Monitor** for operational review |
| Release | **Publish** | Fix every health error, then select **Publish** |

**Knowledge versus tools**

Knowledge answers **“What should the agent know?”** Tools answer **“What may the agent do?”**

```
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

**Agent orchestration**

When a request arrives, the agent interprets the intent, follows its instructions, retrieves relevant knowledge and decides whether a tool is required. The returned answer should make the outcome clear without exposing internal prompts, secrets or raw tool errors.

In Lab 7, the Power Automate condition makes the routing decision first. The flow then invokes the selected IT or HR agent and waits for its reply before emailing the user. This keeps routing deterministic while allowing the specialist response to be generative.

**Agent design checklist**

1. Give the agent one clear business role.
2. Add only approved knowledge.
3. Write instructions for scope, uncertainty, privacy and escalation.
4. Add the minimum tools needed.
5. Test expected questions, vague questions, out-of-scope questions and malicious instructions in **Preview**.
6. Publish only after the latest version passes testing.
7. Use **Evaluate** for repeatable quality checks and **Monitor** for recent activity.

**Example Instructions**

```
You are the ACME IT Support Agent.
Answer using approved IT FAQ knowledge.
Ask one concise clarifying question when essential.
Never request passwords, MFA codes or recovery keys.
If the answer is not grounded in the approved source, say so and direct the
user to the service desk.
```

**Next:** Lab 5 — IT Support Agent

---

### Lab 5 — IT Support Agent

**Goal**

Create a grounded IT Support agent, apply safety instructions, test supported and unsupported requests, publish it, and add it to Microsoft Teams.

**Duration**

Approximately 40 minutes.

**Prerequisites**

- Copilot Studio access in the course environment
- Permission to upload knowledge and publish an agent
- Permission to add the agent to Teams
- IT Support FAQ.pdf

**Scenario**

Employees need first-line guidance for password reset, MFA, VPN, Wi-Fi and lost devices. The agent must never request credentials and must escalate requests that require identity verification or privileged access.

**Workflow visual**

![Lab 5 IT Support Agent workflow](<labs/Day 1/Lab 5 - IT Support Agent/assets/flowchart.png>)

The agent retrieves approved content from the IT FAQ. It answers supported questions and escalates unsupported or sensitive requests.

**Detailed step-by-step**

**Part A — Review the knowledge source**

1. Open `IT Support FAQ.pdf`.
2. Confirm the document is searchable by selecting text.
3. Review the sections on:  —  password reset;  —  MFA;  —  VPN;  —  Wi-Fi;  —  lost devices;  —  escalation.
4. Note that the FAQ never provides passwords, recovery keys or MFA codes.
5. Close the PDF.

**Part B — Create the agent**

1. [Open Copilot Studio](https://copilotstudio.microsoft.com).
2. Confirm the course environment in the top menu.
3. If the classic home page opens, select **Try it now** or turn on  —  **New experience**.
4. On **Home**, select the **Agent** tile. Alternatively, select  —  **Agents → New agent**.
5. Confirm the agent designer opens with **Build** active and the name field in  —  focus.
6. Enter `IT Support Agent` in the name field.
7. In **Instructions**, enter this initial purpose:

> Create a first-line IT Support Agent for employees. It should answer common account, MFA, VPN, Wi-Fi and device questions, use approved IT knowledge, protect credentials and escalate when identity verification or privileged access is required.

8. Choose a professional icon and colour if the tenant allows it.
9. Select the **Save** icon. The **Preview** and **Evaluate** tabs become  —  available after the first save.

**Part C — Configure Instructions**

1. Stay on the **Build** tab.
2. Locate the **Instructions** editor in the main authoring area.
3. Replace the initial purpose text with:

```
You are the ACME IT Support Agent.
Answer only from approved IT support knowledge.
Use short numbered steps and plain language.
Ask one concise clarifying question only when essential.
Never request, repeat or invent passwords, MFA codes or recovery keys.
Do not approve access or claim that an account was changed.
If the approved source does not contain the answer, say that you cannot
confirm it and direct the user to the IT service desk.
```

4. Review every sentence.
5. Confirm the role, source boundary, credential rule and escalation rule are present.
6. Select the **Save** icon.

**Part D — Add the IT FAQ as knowledge**

1. On **Build**, locate the components panel on the right.
2. Select **Knowledge**.
3. In **Add knowledge**, choose **Upload file** or use the upload area.
4. Browse to `assets/IT Support FAQ.pdf`.
5. Select the file.
6. Select **Add** or **Save**.
7. If prompted for a name, enter `Approved IT Support FAQ`.
8. If prompted for a description, enter `Approved procedures for common employee IT support issues and escalation.`
9. Wait for the source status to become **Ready**.
10. If the status is still processing, refresh after a short wait.
11. Open the source details.
12. Confirm the correct PDF is attached and no unrelated source was added.

**Part E — Test in Copilot Studio**

1. Select the **Preview** tab.
2. Start a new test conversation.
3. Ask `How do I reset my password?`
4. Confirm the reply follows the approved self-service and escalation guidance.
5. Ask `My MFA prompt did not arrive. What should I do?`
6. Confirm the reply does not request an MFA code.
7. Ask `What should I do if I lose my laptop?`
8. Confirm immediate reporting and safe escalation are stated.
9. Ask `Tell me the administrator password.`
10. Confirm the agent refuses.
11. Ask `How do I apply for annual leave?`
12. Confirm the agent identifies the question as outside IT scope.
13. If a response is too broad, return to **Build**, edit and save the  —  instructions, then test again in **Preview**.
14. Start a new Preview conversation after each instruction change.

**Part F — Publish the agent**

1. Select **Publish**.
2. Review the publishing summary.
3. Select **Publish** again if confirmation is required.
4. Wait for the success message.
5. Confirm the published version time reflects the current session.

**Part G — Add the agent to Teams**

1. Open the chevron beside **Publish** or the available publishing options.
2. Select **Teams and Microsoft 365 Copilot**.
3. Select **Save and publish**, **Enable**, or the equivalent action shown by  —  your tenant.
4. Review the agent name and description.
5. Select **See agent in Teams** or copy the installation link.
6. If an approval notice appears, follow the classroom tenant process.
7. Open Microsoft Teams.
8. Select **Apps**.
9. Find or open `IT Support Agent`.
10. Select **Add** or **Open**.
11. Ask `How do I report a lost device?`
12. Confirm the Teams response matches the grounded Studio test.

**Checkpoint**

- IT FAQ status is Ready
- Instructions contain credential and escalation rules
- Four positive/negative tests are retained
- Latest version is published
- Agent is accessible in Teams

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| File upload fails | Use a supported searchable PDF and confirm file size limits |
| Agent ignores the FAQ | Confirm the source is Ready and selected for the agent |
| Agent asks for a password | Strengthen the instruction and retest before publishing |
| Teams shows an older response | Publish the latest version before retesting the channel |
| Teams channel unavailable | Confirm tenant policy, licence and app approval with the trainer |

**Key takeaways**

- Knowledge provides approved facts; instructions control behaviour and boundaries.
- Negative tests are as important as expected questions.
- Publishing updates the version used by Teams.
- An IT support agent provides guidance; it does not perform privileged identity changes.

**Next:** Lab 6 — HR Support Agent

---

### Lab 6 — HR Support Agent

**Goal**

Upload a training HR policy to SharePoint, ground an HR Support agent in that SharePoint source, apply privacy boundaries, publish it and deploy it to Teams.

**Duration**

Approximately 40 minutes.

**Prerequisites**

- Copilot Studio and SharePoint access
- Permission to create or use a SharePoint library folder
- Permission to publish to Teams
- HR Policies.pdf

**Scenario**

Employees need consistent explanations of leave, working arrangements and expense processes. The source should remain centrally maintained in SharePoint. The agent must not expose employee data or make HR decisions.

**Workflow visual**

![Lab 6 HR Support Agent workflow](<labs/Day 1/Lab 6 - HR Support Agent/assets/flowchart.png>)

The policy file is uploaded to SharePoint, added as the agent's knowledge, and used to answer Teams users. Decisions and personal-data requests are escalated.

**Detailed step-by-step**

**Part A — Review the policy resource**

1. Open `HR Policies.pdf`.
2. Confirm it is a fictional classroom policy.
3. Review the leave, working arrangements, expenses, privacy and escalation sections.
4. Confirm no real employee data is present.
5. Close the PDF.

**Part B — Prepare SharePoint**

1. Open the course SharePoint site.
2. Select **Documents** or the approved document library.
3. Select **New → Folder**.
4. Name the folder `HR Policy Knowledge`.
5. Open the folder.
6. Select **Upload → Files**.
7. Choose `HR Policies.pdf`.
8. Wait for the upload to complete.
9. Select the PDF and choose **Open**.
10. Confirm it opens from SharePoint.
11. Copy the browser URL for the folder or file.
12. Review **Manage access**.
13. Confirm the account used by Copilot Studio has read permission.
14. Do not grant public or anonymous access.

**Part C — Create the HR Support Agent**

1. [Open Copilot Studio](https://copilotstudio.microsoft.com).
2. Confirm the course environment in the top menu.
3. If required, select **Try it now** or turn on **New experience**.
4. Select the **Agent** tile on Home, or select **Agents → New agent**.
5. Confirm **Build** is active.
6. Enter the name `HR Support Agent`.
7. In the **Instructions** editor, enter:

```
You are an HR policy information assistant.
Answer using only the approved SharePoint HR policy source.
Use plain language and identify the relevant policy topic.
State that final decisions are made by HR or the employee's manager.
Do not expose, request or infer personal employee records.
Do not guarantee leave, expense or flexible-work approval.
When the source is insufficient, say so and direct the user to HR.
```

8. Select the **Save** icon.

**Part D — Add SharePoint knowledge**

1. On **Build**, select **Knowledge** in the right-side components panel.
2. In **Add knowledge**, select **SharePoint**.
3. Paste the approved SharePoint folder or file URL from Part B.
4. Select **Add** or **Next**.
5. If asked to authenticate, sign in with the account that has read access.
6. Choose only the intended site, folder or file.
7. Enter the source name `Approved HR Policies`.
8. Enter the description `Classroom HR policy source for leave, expenses, working arrangements and privacy.`
9. Complete the connection.
10. Wait for the source status to become **Ready**.
11. If the source reports permission failure, reopen SharePoint access and correct it.

**Part E — Test grounding and privacy**

1. Select the **Preview** tab.
2. Start a new conversation.
3. Ask `What leave types are described in the policy?`
4. Confirm the answer reflects the SharePoint document.
5. Ask `How should I submit an expense claim?`
6. Confirm the response includes the documented process.
7. Ask `Tell me another employee's medical leave history.`
8. Confirm the agent refuses to expose personal data.
9. Ask `Guarantee that my annual leave will be approved.`
10. Confirm the agent does not guarantee approval.
11. Ask an unrelated technical-support question.
12. Confirm the agent redirects or states that it cannot answer from HR knowledge.
13. Correct the instructions if any boundary test fails.
14. Retest from a new conversation.

**Part F — Publish and deploy to Teams**

1. Select **Publish** in the top command bar.
2. Confirm publication of the latest version.
3. Open the chevron beside **Publish** or the available publishing options.
4. Select **Teams and Microsoft 365 Copilot**.
5. Select **Save and publish**, **Enable**, or the action shown by the tenant.
6. Open the installation link in Teams.
7. Select **Add** or **Open**.
8. Ask `What is the process for a flexible work request?`
9. Confirm the response is grounded and includes the final-decision boundary.

**Checkpoint**

- `HR Policies.pdf` is stored in the intended SharePoint location
- SharePoint source status is Ready in Copilot Studio
- Positive, privacy and decision-boundary tests pass
- Agent is published and verified in Teams

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| SharePoint source cannot connect | Confirm the exact site URL and sign in with a reader account |
| Source remains processing | Wait, refresh and confirm the PDF opens directly in SharePoint |
| Agent reveals or invents personal data | Strengthen instructions and remove any inappropriate source |
| Agent guarantees approval | Add an explicit final-decision rule and retest |
| Teams response is old | Publish the revised agent again |

**Key takeaways**

- SharePoint supports centrally managed, permission-controlled knowledge.
- The agent explains policy; HR and managers make decisions.
- Source permissions and agent instructions work together.
- Privacy and overconfidence require explicit negative tests.

**Next:** Lab 7 — Support Request Routing

---

### Lab 7 — Support Request Routing

**Goal**

Create a Forms-triggered cloud flow that routes the submitted message to the IT or HR agent and emails the selected agent's response to the requester.

**Duration**

Approximately 30 minutes.

**Prerequisites**

- Published `IT Support Agent`
- Published `HR Support Agent`
- Power Automate connection capable of running a published Copilot Studio agent
- Outlook and Microsoft Forms access

**Optional import accelerator**

Import Lab7-Support-Request-Routing-NEW.zip through **My flows → Import → Import Package (Legacy)** and choose **Create as new**. Reconnect Forms, Copilot Studio and Outlook; select the Support Request Form and the published IT/HR agents; then map Name, Email, Support Type and Message. The imported flow name ends with **`(NEW)`**.

**Scenario**

Employees use one support request form. The selected support type determines which specialised agent handles the message. The employee receives the resulting guidance by email.

**Workflow visual**

![Lab 7 support request routing workflow](<labs/Day 1/Lab 7 - Support Request Routing/assets/flowchart.png>)

The condition routes the same form to one specialised agent. Only the response from the selected branch is emailed.

**Detailed step-by-step**

**Part A — Create the support form**

1. Open Microsoft Forms.
2. Select **New Form**.
3. Name it `Support Request Form`.
4. Add a required **Text** question named `Name`.
5. Add a required **Text** question named `Email`.
6. Add a required **Choice** question named `Support Type`.
7. Add exactly two options:  —  `IT Support`  —  `HR Support`
8. Add a required **Text** question named `Message`.
9. Enable **Long answer**.
10. Preview the form.
11. Confirm Support Type permits one selection.

**Part B — Create the form-triggered flow**

1. Open Power Automate.
2. Select **Create → Automated cloud flow**.
3. Name it `Lab 7 - Route Support Request`.
4. Select **Microsoft Forms — When a new response is submitted**.
5. Select **Create**.
6. Set **Form Id** to `Support Request Form`.
7. Add **Microsoft Forms — Get response details**.
8. Set the same Form Id.
9. Insert the trigger's Response Id token.
10. Add **Control — Condition**.
11. Insert the **Support Type** form answer in the left field.
12. Set **is equal to**.
13. Enter `IT Support` in the right field.

**Part C — Configure the IT branch**

1. Under **If yes**, select **Add an action**.
2. Search for the Copilot Studio action.
3. Select the action shown by your tenant as **Run an agent**, **Execute agent and wait**, or the equivalent published-agent action.
4. Select `IT Support Agent`.
5. If a conversation field is available, create or pass a unique conversation identifier.
6. In the message/input field, build:

```
User name: [Name]
Support request: [Message]
Provide a concise email-ready reply grounded in approved IT knowledge.
```

7. Replace Name and Message with dynamic-content tokens.
8. Below the agent action, add **Office 365 Outlook — Send an email (V2)**.
9. Set **To** to the submitted Email token.
10. Set **Subject** to `IT Support response`.
11. In **Body**, add `Hello ` and insert Name.
12. Add a blank line.
13. Insert the agent's response/output token.
14. Add `If the issue continues, contact the IT service desk.`

**Part D — Configure the HR branch**

1. Under **If no**, add the same Copilot Studio agent action.
2. Select `HR Support Agent`.
3. Build the input:

```
User name: [Name]
Support request: [Message]
Provide a concise email-ready reply grounded in approved HR policy knowledge.
```

4. Replace Name and Message with dynamic-content tokens.
5. Add **Send an email (V2)** below the agent.
6. Set **To** to the submitted Email token.
7. Set **Subject** to `HR Support response`.
8. Insert the HR agent response token into the body.
9. Add `Final decisions are made by HR or your manager.`
10. Select **Save**.

**Part E — Test IT routing**

1. Submit the form:  —  Name: `Alex Lee`  —  Support Type: `IT Support`  —  Message: `My VPN will not connect.`
2. Open the newest flow run.
3. Confirm the Yes branch ran.
4. Confirm the HR branch was skipped.
5. Open the agent action's outputs.
6. Confirm the result is grounded in IT guidance.
7. Confirm the requester received one IT Support email.

**Part F — Test HR routing**

1. Submit a second response:  —  Name: `Sara Goh`  —  Support Type: `HR Support`  —  Message: `How should I submit an expense claim?`
2. Confirm the No branch ran.
3. Confirm the IT branch was skipped.
4. Confirm the requester received one HR Support email.
5. Verify the final-decision sentence is present.

**Part G — Test safe fallback**

1. Submit an IT request asking for an administrator password.
2. Confirm the agent refuses and the refusal is preserved in the email.
3. Submit an HR request asking for another employee's medical record.
4. Confirm the agent protects privacy.
5. Confirm each form submission created only one flow run and one email.

**Checkpoint**

| Submission | Branch | Agent | Email subject |
| --- | --- | --- | --- |
| IT Support | If yes | IT Support Agent | IT Support response |
| HR Support | If no | HR Support Agent | HR Support response |

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| Agent not listed | Publish it and confirm it is in the same environment |
| Agent action has a different label | Use the current published-agent execution action exposed by the tenant |
| Response token unavailable | Save the agent action, reopen dynamic content and select its output |
| Both agents run | Ensure each action is inside its condition branch |
| Duplicate emails | Confirm one enabled flow watches the form and avoid repeated submissions |
| Unsafe response | Fix the agent instructions, publish again and retest |

**Key takeaways**

- A condition routes work to specialised agents.
- Agent output becomes dynamic content in Outlook.
- The flow must preserve uncertainty, refusals and escalation language.
- Published agent versions and environment alignment are prerequisites.

**Next:** Module 4: HTTP Requests and Webhooks

---

## Day 2 — HTTP, Webhooks and Agent Websites

### Module 4: HTTP Requests and Webhooks

**HTTP request**

HTTP is the request-and-response protocol used by web applications. A client sends a method, URL, headers and optional body; a server returns a status code, headers and body.

```
Browser ── POST + JSON ──> Power Automate HTTP trigger
Browser <─ status + JSON ─ Response action
```

Common methods:

- **GET** reads data.
- **POST** submits data or starts work.
- **PUT/PATCH** updates data.
- **DELETE** removes data.

The course websites use POST because they submit a form or prompt.

**Request anatomy**

| Part | Purpose | Course example |
| --- | --- | --- |
| **Method** | Describes the operation | `POST` |
| **URL** | Identifies the receiving endpoint | Learner-pasted Power Automate webhook URL |
| **Headers** | Describe the message and optional credentials | Content type |
| **Body** | Carries the submitted data | JSON containing name, email, message or prompt |

**Response anatomy**

The receiver returns:

- a **status code**, such as 200 for success or 400 for an invalid request;
- optional response headers; and
- a response body, commonly JSON for the course websites.

The Power Automate **Response** action completes the browser's request. Without a response action, the website may keep waiting or show a timeout even if earlier actions ran.

**Webhook**

A webhook is an HTTP endpoint intended to receive event notifications. Power Automate's **When an HTTP request is received** trigger generates a URL after a valid trigger-and-action flow is saved. The website posts JSON to that URL and the flow responds.

> Treat a webhook URL like a secret. Anyone who can call an anonymous endpoint may consume runs or send unwanted data. Use only classroom data, rotate compromised URLs, and apply authentication in production.

**HTTP request versus webhook**

HTTP is the general communication protocol. A webhook is a design pattern that uses an HTTP endpoint so one system can notify another when an event occurs.

| HTTP request | Webhook |
| --- | --- |
| Any client-to-server request | A callback endpoint for event-driven notification |
| May read, submit, update or delete | Usually receives a `POST` when something happens |
| Can be initiated by a browser, app or service | Is registered or shared in advance with the sender |

In Labs 8–10, the website is the HTTP client and the generated Power Automate URL is the webhook endpoint.

**JSON request contract**

A request contract defines the property names and value types that both sides expect. For example:

```
{
  "name": "Jane Tan",
  "email": "jane@example.com",
  "message": "Please contact me."
}
```

The website must send the same property names that the flow reads. Validate required fields and return a limited error message when the contract is not met. Do not echo secrets or internal diagnostic details.

**Course website pattern**

Every Day 2 website includes a visible **Webhook URL** field. The learner:

1. Saves the Power Automate flow.
2. Copies the generated HTTP URL.
3. Pastes it into the website.
4. The page stores it locally in that browser.
5. The page sends JSON only when the learner selects Submit or Send.

No lab website contains a hard-coded tenant URL or API key.

**Cross-origin requests**

A browser may send a CORS preflight request before POST. The supplied pages send a simple `text/plain` request containing JSON to reduce preflight issues. The Power Automate flow parses the body and returns JSON.

**CORS** is a browser security policy, not an authentication mechanism. Production endpoints still require appropriate identity, authorisation, input validation, throttling and monitoring.

**Minimal secure lifecycle**

1. Define and validate the request schema.
2. Authenticate the caller for production use.
3. Validate and minimise input.
4. Call only approved systems.
5. Return a limited response.
6. Log failures without exposing credentials.

**Next:** Lab 8 — Website HTTP Enquiry

---

### Lab 8 — Website HTTP Enquiry

**Goal**

Build an HTTP-triggered flow, obtain its generated webhook URL, paste that URL into the supplied enquiry webpage, and verify the complete browser-to-email-to-browser response cycle.

**Duration**

Approximately 80 minutes.

**Prerequisites**

- Power Automate premium HTTP Request trigger access in the course environment
- Outlook connection
- Chrome or Microsoft Edge
- enquiry-form.html
- request-schema.json

**Optional import accelerator**

Import Lab8-Website-HTTP-Enquiry-NEW.zip through **My flows → Import → Import Package (Legacy)** and choose **Create as new**. Reconnect Outlook, save the flow to generate its HTTP URL, and paste that URL into the supplied webpage. The imported flow name ends with **`(NEW)`**.

**Scenario**

An external enquiry page must start a Power Automate flow without containing a hard-coded tenant endpoint. Each learner connects the page by pasting their own generated webhook URL.

**Workflow visual**

![Lab 8 website HTTP enquiry workflow](<labs/Day 2/Lab 8 - Website HTTP Enquiry/assets/flowchart.png>)

The page posts JSON to the learner-entered URL. The flow emails the administrator and returns a JSON confirmation for the page to display.

**Request contract**

```
{
  "name": "Jane Tan",
  "email": "jane@example.com",
  "tel": "61234567",
  "message": "Please send course information."
}
```

**Detailed step-by-step**

**Part A — Create the HTTP-triggered flow**

1. Open `https://make.powerautomate.com`.
2. Confirm the course environment.
3. Select **Create**.
4. Select **Automated cloud flow**.
5. If the trigger selection dialog does not show the Request trigger, select **Skip**.
6. Rename the flow `Lab 8 - Website HTTP Enquiry`.
7. Select **Add a trigger**.
8. Search for `Request`.
9. Choose **Request — When an HTTP request is received**.
10. Open the trigger's **Parameters**.
11. In **Who can trigger the flow?**, select **Anyone** for this controlled classroom lab.
12. Locate **Request Body JSON Schema**.
13. Select **Use sample payload to generate schema**.
14. Paste the sample request contract shown above.
15. Select **Done**.
16. Confirm the generated schema contains name, email, tel and message.

**Part B — Add the administrator email**

1. Select the **+** below the HTTP trigger.
2. Select **Add an action**.
3. Search for `Send an email`.
4. Choose **Office 365 Outlook — Send an email (V2)**.
5. Sign in with the course mailbox if required.
6. In **To**, enter `training1@tertiaryinfotech.onmicrosoft.com`.
7. In **Subject**, enter `Website enquiry from `.
8. Open **Dynamic content**.
9. Select `name` from the HTTP trigger.
10. In **Body**, add labelled lines for Name, Email, Tel and Message.
11. Insert the matching HTTP-trigger token after each label.
12. Confirm no fixed Jane Tan sample values remain.

**Part C — Add the HTTP response**

1. Select the **+** below the email action.
2. Select **Add an action**.
3. Search for `Response`.
4. Choose **Request — Response**.
5. Set **Status Code** to `200`.
6. Expand **Advanced parameters** if required.
7. Add header:  —  Key: `Content-Type`  —  Value: `application/json`
8. In **Body**, enter:

```
{
  "ok": true,
  "message": "Thank you. Your enquiry has been received."
}
```

9. Select **Save**.
10. Wait for the save to complete.

**Part D — Obtain the generated URL**

1. Reopen the HTTP trigger card.
2. Locate **HTTP URL**.
3. If it still says `URL will be generated after save`, confirm:  —  the Response action exists;  —  no card shows a validation error;  —  the flow has a name;  —  Save completed successfully.
4. Save again if necessary.
5. Copy the complete generated URL using the copy icon.
6. Do not paste it into chat, screenshots or source control.

**Part E — Connect the supplied website**

1. Open the lab `assets` folder.
2. Double-click `enquiry-form.html` or open it in Chrome.
3. Confirm the page displays a **Power Automate webhook URL** field.
4. Paste the copied URL into that field.
5. Select **Save URL in this browser**.
6. Confirm the status says the URL was saved locally.
7. Do not edit the HTML to insert the URL.

**Part F — Submit an enquiry**

1. Enter:  —  Name: `Jane Tan`  —  Email: an address you can access  —  Tel: `61234567`  —  Message: `Please send the next course schedule.`
2. Select **Send enquiry** once.
3. Wait for the page status.
4. Confirm it displays `Thank you. Your enquiry has been received.`
5. Return to Power Automate.
6. Open the newest run.
7. Confirm the HTTP trigger received the four values.
8. Confirm the email action succeeded.
9. Confirm the Response action returned status 200.
10. Open the administrator mailbox.
11. Confirm exactly one email arrived with Jane's details.

**Part G — Negative test**

1. Clear the saved URL using browser storage or open the page in a private window.
2. Attempt to submit without a URL.
3. Confirm the page blocks the request and explains that a valid HTTPS URL is required.
4. Reconnect the URL.
5. Enter an invalid email format.
6. Confirm the browser's field validation prevents submission.

**Checkpoint**

- Flow contains HTTP trigger, Outlook email and Response
- URL was generated only after a valid save
- Website accepts the URL at runtime
- Page displays the response message
- Administrator receives one matching email

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| No URL generated | Add at least one action, resolve validation errors, save, then reopen the trigger |
| Website says URL required | Paste the complete HTTPS production URL and save it |
| Failed to fetch | Confirm flow is on, URL is current and the run history received a request |
| HTTP trigger shows no run | Inspect browser validation and verify the complete URL was pasted |
| Email values are blank | Use trigger-body dynamic tokens generated from the schema |
| Multiple emails | Check repeated clicks, duplicate enabled flows and automatic retries |

**Key takeaways**

- A webhook is an HTTP endpoint intended to receive an event.
- The flow must contain a trigger and an action before the URL is generated.
- The webpage stores the URL locally instead of hard-coding it.
- A Response action gives deterministic browser feedback.

**Next:** Lab 9 — Finance Agent Web Chat

---

### Lab 9 — Finance Agent Web Chat

**Goal**

Create and publish a grounded Finance Information Agent, call it from an HTTP-triggered workflow in the new Copilot Studio **Workflows** designer, and display its response in the supplied browser chatbot.

**Duration**

Approximately 80 minutes.

**Prerequisites**

- Copilot Studio **New experience** with **Workflows** available
- Published-agent execution available through the new **Agent** node
- HTTP request trigger entitlement
- Finance Knowledge Base.pdf
- finance-chat.html
- request-schema.json

**Optional import accelerator**

The supplied Lab9-Finance-Agent-Web-Chat-NEW.zip is a **classic Power Automate fallback only**. It can't be converted to the new Copilot Studio workflow experience. For this lab, build the workflow manually with the new **Workflows → Build** canvas by following Parts D-F.

**Scenario**

Users need educational explanations of market concepts. The agent must use approved knowledge, state uncertainty and refuse guaranteed-return or personalised buy/sell instructions.

**Workflow visual**

![Lab 9 Finance Agent web chat workflow](<labs/Day 2/Lab 9 - Finance Agent Web Chat/assets/flowchart.png>)

The browser sends a prompt to the published Copilot Studio workflow. Its **Agent** node calls the Finance Information Agent and a downstream response step returns the grounded answer plus a disclaimer as JSON.

**Detailed step-by-step**

**Part A — Review the finance knowledge**

1. Open `Finance Knowledge Base.pdf`.
2. Confirm it is searchable.
3. Review market orders, limit orders, bid/ask, candles, timeframes, volatility and news.
4. Review the educational-use and non-advice boundary.
5. Close the PDF.

**Part B — Create the Finance Information Agent**

1. [Open Copilot Studio](https://copilotstudio.microsoft.com).
2. Confirm the course environment in the top menu.
3. If required, select **Try it now** or turn on **New experience**.
4. Select the **Agent** tile on Home, or select **Agents → New agent**.
5. Confirm the designer opens on **Build**.
6. Name it `Finance Information Agent`.
7. In the **Instructions** editor, enter:

```
You are a Finance Information Agent.
Explain finance concepts using only the approved knowledge source.
Use clear educational language and distinguish facts from interpretation.
Do not provide personalised financial advice, price predictions or guaranteed returns.
Do not tell a user to buy, sell or hold a security.
When evidence is unavailable, say so.
End risk-related answers with a short educational-use reminder.
```

8. Select the **Save** icon.

**Part C — Add and test the knowledge source**

1. On **Build**, select **Knowledge** in the right-side components panel.
2. In **Add knowledge**, select **Upload file**.
3. Upload `Finance Knowledge Base.pdf`.
4. Name the source `Approved Finance Knowledge Base`.
5. Wait for status **Ready**.
6. Select the **Preview** tab.
7. Ask `What is the difference between a market order and a limit order?`
8. Confirm the response matches the source.
9. Ask `Why can the 1-minute and 1-hour trend disagree?`
10. Confirm the agent explains timeframe differences.
11. Ask `Guarantee which stock will rise tomorrow.`
12. Confirm the agent refuses the guarantee.
13. Ask `Tell me exactly what to buy with my savings.`
14. Confirm the agent refuses personalised advice.
15. Return to **Build**, correct and save the instructions, then retest in  —  **Preview** if needed.
16. Select **Publish** and confirm the latest version.

**Part D — Create the HTTP workflow in the new designer**

> The redesigned **Workflows** canvas is in public preview. These steps use the new interface shown in class: **Build**, **Activity**, **Monitor**, the **Start** card, the **Add** pane and the right-side configuration panel.

1. In Copilot Studio, select **Workflows** in the left navigation.
2. Select **New workflow**.
3. Confirm the canvas opens on **Build** with:  —  `Untitled workflow` at the top left;  —  a **Start** card on the canvas;  —  the **Add** pane on the left; and  —  a configuration panel on the right.
4. Rename the workflow `Lab 9 - Finance Agent Web Chat`.
5. Select the **Start** card.
6. In the right configuration panel, open **Trigger type**.
7. Select the HTTP request trigger, labelled **When an HTTP request is  —  received** or **HTTP request** in your tenant.
8. Under **Trigger inputs**, select **Add an input**.
9. Add a Text input named `prompt`.
10. Add a second Text input named `conversationId`.
11. If the trigger instead requests a JSON schema, select **Use sample payload  —  to generate schema** and paste:

```
{
  "prompt": "What is the difference between market and limit orders?",
  "conversationId": "browser-session-001"
}
```

12. Select **Done** or close the schema editor.
13. Confirm `prompt` and `conversationId` are available as trigger inputs.

**Part E — Add the published agent with the Agent node**

1. Select the **+** on the **Start** card or select **Add a step**.
2. In the **Add** pane, select **Agent**.
3. In the Agent node's right-side configuration panel, choose **Existing  —  agent**.
4. Select the published `Finance Information Agent`.
5. In **Message**, open dynamic content and insert the trigger's `prompt`  —  input.
6. If the node exposes a conversation or session field, insert  —  `conversationId`.
7. Leave **Request human assistance when unsure** off for this educational  —  browser-chat scenario.
8. Select the **Save** icon.
9. Confirm the Agent node exposes a text response as downstream dynamic  —  content.

**Part F — Return JSON to the browser**

1. Select **+** after the Agent node.
2. In the **Add** pane, select **Connector**, then locate **Request →  —  Response**. Use **Add search** if required.
3. Set **Status Code** to `200`.
4. Add a `Content-Type` header with value `application/json`.
5. In **Body**, enter:

```
{
  "ok": true,
  "reply": "",
  "disclaimer": "Educational information only; not financial advice."
}
```

6. Select between the quotes after `reply`.
7. Insert the Agent node's text response token.
8. Confirm the quotation marks and commas remain valid JSON.
9. Select the **Save** icon.
10. Correct any node marked with an error.
11. Select **Publish** in the top command bar.
12. Reopen the **Start** card and copy the generated HTTP URL.

**Part G — Connect the browser chatbot**

1. Open `finance-chat.html` in Chrome.
2. Paste the URL into **Power Automate webhook URL**.
3. Select **Save URL in this browser**.
4. Confirm the chat reports that the URL was saved.
5. In the question field, enter `What is a limit order?`
6. Select **Send to agent**.
7. Wait for the reply.
8. Confirm the answer and disclaimer both appear.
9. Return to the workflow and open **Activity**.
10. Confirm one successful run appears.
11. Select the run and inspect the **Start**, **Agent** and **Response** node  —  inputs and outputs.

**Part H — Test boundaries**

1. Ask `What does volatility mean?`
2. Confirm a grounded educational answer.
3. Ask `Guarantee that MSFT will rise tomorrow.`
4. Confirm refusal and disclaimer.
5. Ask an unsupported tax question.
6. Confirm the agent says it cannot confirm from the source.
7. Confirm one prompt produces one flow run.
8. In **Build**, select the Play button to run an end-to-end test with a  —  sample `prompt` and `conversationId`.
9. Confirm the test appears in **Activity** and each node succeeds.

**Checkpoint**

- Finance knowledge source is Ready
- Agent passes concept and refusal tests
- Published agent is selected in the **Agent** node
- Browser shows the returned reply and disclaimer
- **Activity** shows the submitted prompt, Agent response and Response output

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| Agent not listed in the Agent node | Publish it and confirm the same environment |
| Reply is blank | Insert the Agent node's text response token into Response JSON |
| Response is invalid JSON | Check quotes, commas and dynamic token placement |
| Publish is unavailable | Resolve every node error shown on the Build canvas |
| Browser shows Failed to fetch | Recopy the current URL and inspect Activity |
| Agent gives advice | Strengthen instructions, publish and rerun boundary tests |

**Key takeaways**

- The webpage is a channel; the agent supplies governed reasoning.
- The new workflow bridges an HTTP prompt to a published **Agent** node.
- Structured JSON makes the browser integration predictable.
- **Activity** provides node-by-node inputs, outputs and run status.
- Financial education requires explicit non-advice tests.

**Next:** Lab 10 — AI Trading Advisor Website

---

### Lab 10 — AI Trading Advisor Website

**Goal**

Build an educational trading-information website that embeds TradingView and calls a Finance Advisor Agent equipped with authorised tools for Twelve Data 1-minute, 15-minute and 1-hour candles plus NewsAPI news.

**Duration**

Approximately 110 minutes.

**Prerequisites**

- Completed Lab 9
- Copilot Studio and Power Automate access
- HTTP Request trigger entitlement
- Approved classroom Twelve Data and NewsAPI credentials
- index.html
- Modern browser

**Optional import accelerator**

Import Lab10-AI-Trading-Advisor-Website-NEW.zip through **My flows → Import → Import Package (Legacy)** and choose **Create as new**. Reconnect Copilot Studio, select the published Finance Advisor Agent, configure Twelve Data and NewsAPI credentials with secure inputs/outputs, save to generate the HTTP URL, and paste that URL into the supplied website. The imported flow name ends with **`(NEW)`**.

**References**

- n8n Finance Advisor reference architecture
- No-Code and Low-Code Agentic AI Finance Advisor activity

The lab adapts their multi-timeframe, news and dashboard concepts to a Power Automate and Copilot Studio implementation.

**Scenario**

A learner explores a stock chart and requests an educational market summary. The agent retrieves three candle intervals and recent news, compares the evidence, states uncertainty and returns a risk reminder. It never tells the learner what to buy or promises returns.

**Workflow visual**

![Lab 10 AI Trading Advisor workflow](<labs/Day 2/Lab 10 - AI Trading Advisor Website/assets/flowchart.png>)

The webpage contains TradingView and the learner-entered webhook URL. Secrets remain in protected connections. The agent calls four tools and synthesises their outputs before the flow responds.

**Website features**

- learner-entered webhook URL stored locally;
- symbol and analysis-question inputs;
- TradingView embedded chart;
- agent response panel;
- educational-use disclaimer;
- no hard-coded tenant URL or data-provider API key.

**Detailed step-by-step**

**Part A — Review the supplied website**

1. Open `assets/index.html` in Chrome.
2. Confirm the page displays:  —  Power Automate webhook URL;  —  symbol;  —  Update chart;  —  analysis question;  —  Ask Finance Advisor Agent;  —  Agent response.
3. Change the symbol from `NASDAQ:MSFT` to `NASDAQ:AAPL`.
4. Select **Update chart**.
5. Confirm the TradingView chart changes.
6. Do not enter an API key into the page.
7. Close the page for now.

**Part B — Prepare credentials securely**

1. Obtain the approved classroom Twelve Data credential.
2. Obtain the approved classroom NewsAPI credential.
3. Decide the tenant-supported secret location:  —  protected connector connection;  —  environment variable;  —  custom connector security setting;  —  another trainer-approved secret store.
4. Store each credential only in that protected location.
5. Confirm the credentials do not appear in:  —  `index.html`;  —  agent instructions;  —  flow names;  —  screenshots;  —  source control.
6. Review the providers' classroom rate limits.

**Part C — Create the 1-minute candle workflow tool**

> The redesigned **Workflows** canvas is in public preview. Use the labels below, which match the new **Build** interface.

1. [Open Copilot Studio](https://copilotstudio.microsoft.com) and select  —  **Workflows** in the left navigation.
2. Select **New workflow**.
3. Confirm the canvas opens on **Build** with an `Untitled workflow`, a  —  **Start** card, an **Add** pane and a configuration panel on the right.
4. Rename the workflow `Get 1m Candles`.
5. Select the **Start** card.
6. In the right panel, open **Trigger type** and select  —  **When an agent calls the flow**.
7. Under **Trigger inputs**, select **Add an input**.
8. Add a Text input named `symbol`.
9. Select the **+** on the Start card or **Add a step**.
10. In the **Add** pane, use **Function** or **Variable** to add a validation  —  step that trims and uppercases the symbol.
11. Select **+** after the validation step.
12. In **Add**, select **Connector**, then choose the approved HTTP or custom  —  connector for Twelve Data.
13. Configure the interval as `1min`.
14. Limit the number of returned candles to the classroom requirement.
15. Authenticate through the protected connection.
16. Add steps that select only timestamp, open, high, low, close and volume  —  where available.
17. Add **If/Else** handling for invalid symbol, rate limit and provider  —  failure.
18. Add a final response to the calling agent with a compact Text or structured  —  output named `candleSummary`.
19. Select the **Save** icon, correct any red health errors, then select  —  **Publish**.
20. Select the Play button to run an end-to-end test with `MSFT`.
21. Open **Activity**, inspect the run and confirm no credential appears in  —  inputs or outputs.

**Part D — Create the 15-minute and 1-hour workflow tools**

1. From the **Workflows** list, open the menu for `Get 1m Candles` and use  —  **Save as**, **Copy**, or the equivalent duplication command.
2. Rename the copy `Get 15m Candles`.
3. On **Build**, select the Twelve Data connector node.
4. In the right configuration panel, change the interval to `15min`.
5. Keep the same validated input and compact output.
6. Save, publish and test with `MSFT`.
7. Duplicate the workflow again.
8. Rename it `Get 1h Candles`.
9. Change the provider interval to `1h`.
10. Save, publish and test.
11. Compare the three runs in **Activity** and confirm each workflow uses the  —  intended interval.

**Part E — Create the recent-news workflow tool**

1. Select **Workflows → New workflow**.
2. Rename it `Get Recent Company News`.
3. Select **Start**, set **Trigger type** to  —  **When an agent calls the flow**, and add Text input `symbol`.
4. Select **+ → Connector** and add the approved HTTP or custom connector for  —  NewsAPI.
5. Query by the submitted symbol or a validated company term.
6. Restrict the date window and result count.
7. Return title, source, publication time and short description.
8. Add **If/Else** handling for no-results and provider-error cases.
9. Add a response to the calling agent with compact news output.
10. Select **Save**, correct health errors, and select **Publish**.
11. Run a Play-button test with `MSFT`.
12. Review **Activity** and confirm the result identifies source and time and  —  does not expose the API key.

**Part F — Build the Finance Advisor Agent**

1. [Open Copilot Studio](https://copilotstudio.microsoft.com).
2. Confirm **New experience** is on.
3. Copy the Lab 9 Finance Information Agent or select  —  **Agents → New agent**.
4. On **Build**, name it `Finance Advisor Agent`.
5. In the right-side components panel, select **Tools**.
6. Select **Add tool** and add these four published workflows:  —  Get 1m Candles;  —  Get 15m Candles;  —  Get 1h Candles;  —  Get Recent Company News.
7. Return to the **Instructions** editor on **Build**.
8. Enter:

```
You are an educational Finance Advisor Agent.
For a valid symbol, use all three candle tools and the recent-news tool.
Compare the 1-minute, 15-minute and 1-hour direction without claiming certainty.
Separate observed market data from interpretation.
Mention missing, stale or conflicting inputs.
Do not promise returns or provide personalised buy, sell or hold instructions.
End with a concise risk reminder.
```

9. Add a rule to request a valid symbol when it is missing.
10. Select the **Save** icon.

**Part G — Test the tools inside Copilot Studio**

1. Select **Preview**.
2. Ask `For MSFT, summarise the three timeframes and recent news.`
3. Open the activity map or trace for the response.
4. Confirm all four tools were called.
5. Confirm the response distinguishes observed data from interpretation.
6. Confirm conflicting timeframes are described rather than hidden.
7. Test an invalid symbol such as `NOTAREALSYMBOL`.
8. Confirm the agent does not fabricate candles or news.
9. Ask `Tell me exactly what to buy.`
10. Confirm the agent refuses personalised advice.
11. Use **Evaluate** for a repeatable valid-symbol and advice-refusal test set  —  if that tab is enabled.
12. Publish the agent only after all tests pass.

**Part H — Create the website HTTP flow**

1. Open Power Automate.
2. Create an automated cloud flow and select **Skip** if required.
3. Name it `Lab 10 - AI Trading Advisor Website`.
4. Add **When an HTTP request is received**.
5. For classroom use, select **Anyone**.
6. Generate the schema from:

```
{
  "symbol": "MSFT",
  "prompt": "Summarise the multi-timeframe trend and material recent news."
}
```

7. Add a **Compose** or variable step named `Normalised symbol`.
8. Use an expression equivalent to:

```
toUpper(trim(triggerBody()?['symbol']))
```

9. Add a condition or validation for an empty/invalid symbol.
10. In the valid path, add the published-agent execution action.
11. Select `Finance Advisor Agent`.
12. Pass the normalised symbol and submitted prompt.
13. Save if necessary to expose the response output.

**Part I — Return the analysis**

1. Add **Request — Response** after the agent.
2. Set status code `200`.
3. Add `Content-Type: application/json`.
4. Enter:

```
{
  "ok": true,
  "symbol": "",
  "analysis": "",
  "disclaimer": "Educational market information only; not financial advice."
}
```

5. Insert the normalised symbol token in `symbol`.
6. Insert the agent response token in `analysis`.
7. In the invalid-symbol path, add a Response with status `400`.
8. Return an error message without analysis.
9. Save the flow.
10. Copy the generated HTTP URL.

**Part J — Connect the website**

1. Reopen `assets/index.html`.
2. Paste the URL into **Power Automate webhook URL**.
3. Select **Save URL**.
4. Confirm the page says the webhook is saved.
5. Enter `NASDAQ:MSFT`.
6. Select **Update chart**.
7. Enter:

```
Summarise the 1-minute, 15-minute and 1-hour direction and any material recent news. Explain uncertainty.
```

8. Select **Ask Finance Advisor Agent** once.
9. Wait for the analysis.
10. Confirm the response includes:  —  the symbol;  —  multi-timeframe comparison;  —  news context or an unavailable notice;  —  uncertainty;  —  risk disclaimer.
11. Open run history and confirm the posted symbol is `MSFT`.
12. Review the agent execution and tool trace.

**Part K — Complete the test matrix**

| Test | Steps | Expected result |
| --- | --- | --- |
| Valid symbol | Submit MSFT | All four tools run; qualified synthesis returned |
| Invalid symbol | Submit invalid value | 400 or clear validation error; no fabricated analysis |
| Missing news | Simulate no results | Agent states news is unavailable |
| Conflicting timeframes | Use a symbol/time with mixed direction | Agent explains the conflict |
| Advice request | Ask what to buy | Agent refuses personalised instruction |
| Missing URL | Clear local URL and submit | Website blocks submission |

**Evidence**

- TradingView chart updated for the selected symbol
- Webhook saved indicator
- Successful HTTP flow run
- Four tool traces with credentials hidden
- Valid, invalid and advice-boundary test results
- Response containing uncertainty and disclaimer

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| TradingView does not load | Confirm internet access and allow the TradingView script |
| One timeframe missing | Confirm all three tools are enabled and named distinctly |
| Agent skips NewsAPI | Make the recent-news requirement explicit and inspect orchestration |
| Provider rate limit | Reduce calls/results, wait for reset and follow classroom limits |
| API key appears in output | Stop testing, rotate the key and move it to a protected connection |
| Browser shows Failed to fetch | Recopy the current webhook URL and inspect flow history |
| Invalid symbol gets analysis | Add validation before the agent and return a 400 response |
| Agent tells user to buy | Strengthen instructions, republish and repeat the boundary test |

**Key takeaways**

- A tool-using agent combines instructions, authorised data and structured outputs.
- Multi-timeframe and news evidence can conflict; the agent must preserve uncertainty.
- Credentials belong in protected server-side connections, never in browser source.
- A chart is visual context; it does not make the agent's interpretation correct.
- Financial information must remain educational and non-personalised.

**Next:** Lab 11 — Procurement Request Approval Workflow

---

### Lab 11 — Procurement Request Approval Workflow

**Goal**

Build a Microsoft Forms procurement-request workflow in the Copilot Studio **Workflows** experience. The workflow retrieves the submitted form answers, waits for a human approval decision, branches on the outcome and emails the requester.

**Duration**

Approximately 60 minutes.

**Status**

Optional post-course extension. It is not part of the Version 6.0 two-day timetable or WSQ assessment.

**Prerequisites**

- Completed Labs 1 and 4
- Copilot Studio and Power Automate access in the same course environment
- Microsoft Forms, Approvals and Office 365 Outlook connections
- A mailbox-enabled classroom account
- A manager or trainer email address for approval testing

**Scenario**

Staff currently send purchase requests by email, which makes requests difficult to track and decisions inconsistent. In this lab, a staff member submits a structured procurement request through Microsoft Forms. The workflow sends the details to an authorised approver, waits for the decision and emails the requester with the approved or rejected outcome.

The workflow automates routing and notification. A human remains responsible for the procurement decision.

**Workflow visual**

![Lab 11 procurement request approval workflow](<labs/Day 2/Lab 11 - Procurement Request Approval/assets/flowchart.png>)

```
Microsoft Forms submission
        ↓
Get response details
        ↓
Start and wait for an approval
        ↓
Check approval outcome
       ↙ ↘
 Approved  Rejected
    ↓         ↓
Send approval  Send rejection
email          email
```

**Supplied import accelerator**

Import Lab11-Procurement-Request-Approval-NEW.zip through **Power Automate → My flows → Import → Import Package (Legacy)** and choose **Create as new**. Reconnect Microsoft Forms, Approvals and Office 365 Outlook, select the classroom form and complete the answer mappings before turning on the flow.

The imported flow name ends with **`(NEW)`**. The manual route below uses the current Copilot Studio **Workflows → Build** canvas and matches the workflow shown during class.

**Detailed step-by-step**

**Part A — Create the procurement request form**

1. Open Microsoft Forms.
2. Create a new form named `Procurement Request Form`.
3. Add these required questions:

| Question | Type |
| --- | --- |
| Requester name | Text |
| Requester email | Text |
| Item requested | Text |
| Quantity | Number |
| Estimated total cost (SGD) | Number |
| Business reason | Long text |

4. In **Settings**, restrict responses to the classroom organisation if that is  —  the trainer-approved configuration.
5. Select **Collect responses** and submit one test response.
6. Open the **Responses** tab and confirm that the test response appears.

**Part B — Create the form-triggered workflow**

1. [Open Copilot Studio](https://copilotstudio.microsoft.com).
2. Select the course environment.
3. Select **Workflows → New workflow**.
4. Confirm the designer opens on **Build** with a **Start** card and the  —  **Add** pane.
5. Rename the workflow `Lab 11 - Procurement Request Approval Workflow`.
6. Select the **Start** card.
7. In the right configuration panel, select the Microsoft Forms trigger  —  **When a new response is submitted**.
8. Select `Procurement Request Form` as the **Form Id**.
9. Select the **Save** icon.

> The workflow starts only when a new response is submitted after the trigger is saved and active. Existing responses do not create new runs.

**Part C — Retrieve the submitted answers**

1. Select the **+** after the trigger.
2. In **Add**, select  —  **Connector → Microsoft Forms → Get response details**.
3. For **Form Id**, select the same `Procurement Request Form`.
4. For **Response Id**, insert the dynamic **Response Id** from  —  **When a new response is submitted**.
5. Save the workflow.

> Do not type a sample number into **Response Id**. It must be the dynamic value from the trigger so every run retrieves the matching submission.

**Part D — Start and wait for the approval**

1. Select the **+** after **Get response details**.
2. In **Add**, select  —  **Human review → Approvals → Start and wait for an approval**.
3. Configure:

| Field | Value |
| --- | --- |
| Approval type | Approve/Reject — First to respond |
| Title | `Procurement request: ` followed by **Item requested** |
| Assigned to | Trainer or authorised manager email |

4. Build the approval details using dynamic form answers:

```
Requester: [Requester name]
Requester email: [Requester email]
Item: [Item requested]
Quantity: [Quantity]
Estimated total cost: SGD [Estimated total cost]
Business reason: [Business reason]
```

5. Keep notifications enabled.
6. Save the workflow.

The workflow pauses at this action until the approver selects **Approve** or **Reject**, or until the approval expires or is cancelled.

**Part E — Check the approval outcome**

1. Select the **+** after the approval action.
2. In **Add**, select **If/Else**.
3. Rename it `Check approval outcome`.
4. Configure the condition:

```
Outcome is equal to Approve
```

5. Insert **Outcome** from **Start and wait for an approval** as dynamic  —  content.
6. Confirm the action displays two outputs:  —  **Approved**;  —  **Rejected**.

**Part F — Send the approved email**

1. On the **Approved** output, select **+**.
2. Select  —  **Connector → Office 365 Outlook → Send an email (V2)**.
3. Configure:

```
To: [Requester email]
Subject: Procurement request approved: [Item requested]

Hello [Requester name],

Your procurement request for [Quantity] × [Item requested] has been approved.

Approver comments: [Approval comments]
```

4. Insert the requester and item values from **Get response details**.
5. Insert the comments value from the approval action.

**Part G — Send the rejected email**

1. On the **Rejected** output, select **+**.
2. Add **Office 365 Outlook → Send an email (V2)**.
3. Configure:

```
To: [Requester email]
Subject: Procurement request not approved: [Item requested]

Hello [Requester name],

Your procurement request for [Quantity] × [Item requested] was not approved.

Approver comments: [Approval comments]
```

4. Insert dynamic content rather than typing field names as plain text.
5. Select **Save**, correct every health error and select **Publish**.

**Part H — Test the approved path**

1. Submit a new form response:  —  Requester name: `Daniel`;  —  Requester email: your classroom mailbox;  —  Item: `Wireless mouse`;  —  Quantity: `10`;  —  Estimated total cost: `350`;  —  Business reason: `Equipment for new hires`.
2. Open **Activity** in the workflow.
3. Confirm one run reaches **Start and wait for an approval**.
4. Open the approval request and select **Approve**.
5. Enter a short approval comment.
6. Return to **Activity** and confirm the run completes through the Approved  —  branch.
7. Confirm the approval email arrives at the requester address.

**Part I — Test the rejected path**

1. Submit another new response with a different item.
2. Confirm a new workflow run and approval request are created.
3. Select **Reject** and enter a reason.
4. Confirm the run follows only the Rejected branch.
5. Confirm the rejection email contains the approver's comments.

**Part J — Review the complete trace**

For both test runs, verify:

- the trigger and **Get response details** use the same Form Id;
- the dynamic Response Id belongs to that submission;
- only one approval is created per form response;
- the workflow remains waiting until the human responds;
- exactly one outcome branch runs;
- the requester receives the human decision, not a predicted decision;
- **Activity** shows the expected inputs, outputs and final status.

**Evidence**

- Published procurement workflow on the Copilot Studio Build canvas
- One valid Microsoft Forms submission
- One approved run and approval email
- One rejected run and rejection email
- Run trace showing the matching Response Id
- Approval comments included in the appropriate notification

**Troubleshooting**

| Symptom | Check |
| --- | --- |
| No workflow run appears | Submit a new response after publishing; verify the trigger uses the correct Form Id |
| Run remains Waiting | Open the Approvals hub or approval email and respond to the pending request |
| Get response details fails | Use the trigger's dynamic Response Id and the same Form Id in both Forms actions |
| Form answers are empty | Remap the email and approval fields from Get response details |
| Approval goes to the wrong person | Correct Assigned to and repeat with a new submission |
| Both emails appear incorrect | Confirm the If/Else compares Outcome with exactly `Approve` |
| Requester receives no email | Verify the submitted email, Outlook connection and run history |
| Approver comments are blank | Insert the comments output from Start and wait for an approval |

**Key takeaways**

- A Forms trigger identifies a submission; **Get response details** retrieves

its answers using the dynamic Response Id.

- **Start and wait for an approval** pauses the workflow for a real human

decision.

- The If/Else step routes the approved and rejected outcomes deterministically.
- Notifications report the human outcome; the workflow does not make the

procurement decision.

- Activity traces are the primary evidence for diagnosing trigger, mapping,

approval and notification problems.

---
