# Business Process Automation with Power Automate and Copilot Studio Agents

[![Duration](https://img.shields.io/badge/Duration-2%20Days-orange)]()
[![Labs](https://img.shields.io/badge/Labs-11%20Hands--On-purple)]()
[![Version](https://img.shields.io/badge/Courseware-6.0-blue)]()

This repository contains the Version 6.0 materials for the two-day WSQ course **Business Process Automation with Power Automate and Copilot Studio Agents** (`TGS-2022017524`) plus a supplementary Lab 11 extension.

The course follows a concept → demonstration → lab pattern. Learners first compare instant, scheduled and automated flows and understand triggers, actions and outputs. They then build Forms-driven workflows, add Excel logging, conditions and approvals, study the six Copilot agent building blocks, build specialised agents, and connect agent experiences to websites through HTTP requests and learner-entered webhook URLs.

## Learning outcomes

Participants will be able to:

- explain the difference between instant, scheduled and automated cloud flows;
- build Forms-triggered email, Excel, branching and approval automations;
- describe agent knowledge, skills, tools, memory, model and system instructions;
- build grounded IT, HR and Finance agents;
- publish appropriate support agents to Microsoft Teams;
- route a form request to the correct specialised agent;
- connect websites to HTTP-triggered flows using JSON request/response contracts;
- design a governed Finance Advisor Agent using three Twelve Data candle intervals and NewsAPI;
- compare an agent calling an agent flow with an agent flow calling an agent.

## Course structure

### Day 1 — Forms, flows and business agents

| Item | Outcome |
|---|---|
| [Module 1](labs/Day%201/Module%201%20-%20Workflow%20Automation%20Concepts.md) | Workflow foundations |
| [Module 2](labs/Day%201/Module%202%20-%20Introduction%20to%20Power%20Automate.md) | Instant, scheduled and automated cloud flows |
| [Lab 0](labs/Day%201/Lab%200%20-%20Environment%20Setup/index.md) | Course environment setup |
| [Lab 1 — Form to Email Confirmation](labs/Day%201/Lab%201%20-%20Forms%20Email%20Confirmation/index.md) | Form submission → user confirmation email |
| [Lab 2 — Log the Enquiry and Send Email](labs/Day%201/Lab%202%20-%20Forms%20Enquiry%20Logging/index.md) | Form → `Enquiry Log.xlsx` → email |
| [Lab 3 — Event Registration Branching](labs/Day%201/Lab%203%20-%20Event%20Registration%20Branching/index.md) | Event Yes/No condition → log and correct notification |
| [Lab 4 — Leave Application Approval](labs/Day%201/Lab%204%20-%20Leave%20Approval/index.md) | Leave form → manager approval/rejection |
| [Module 3](labs/Day%201/Module%203%20-%20Business%20Agents%20Concepts.md) | Six Copilot agent building blocks |
| [Lab 5 — IT Support Agent](labs/Day%201/Lab%205%20-%20IT%20Support%20Agent/index.md) | FAQ knowledge + Teams deployment |
| [Lab 6 — HR Support Agent](labs/Day%201/Lab%206%20-%20HR%20Support%20Agent/index.md) | SharePoint policy knowledge + Teams deployment |
| [Lab 7 — Support Request Routing](labs/Day%201/Lab%207%20-%20Support%20Request%20Routing/index.md) | Support form → IT/HR agent → emailed reply |

### Day 2 — HTTP, webhooks and agent websites

| Item | Outcome |
|---|---|
| [Module 4](labs/Day%202/Module%204%20-%20HTTP%20Requests%20and%20Webhooks.md) | HTTP requests, webhooks, JSON and endpoint safety |
| [Lab 8 — Website HTTP Enquiry](labs/Day%202/Lab%208%20-%20Website%20HTTP%20Enquiry/index.md) | Website → learner-entered webhook → email + JSON response |
| [Lab 9 — Finance Agent Web Chat](labs/Day%202/Lab%209%20-%20Finance%20Agent%20Web%20Chat/index.md) | Website prompt → Finance Agent → grounded chat reply |
| [Lab 10 — AI Trading Advisor Website](labs/Day%202/Lab%2010%20-%20AI%20Trading%20Advisor%20Website/index.md) | TradingView → Finance Advisor Agent → candles + news |
| [Lab 11 — Procurement Request Approval Workflow](labs/Day%202/Lab%2011%20-%20Procurement%20Request%20Approval/index.md) | Optional extension: Forms request → human approval → outcome email |
| [Lab 11 — Travel Expense Agent and Agent Flow](labs/Day%202/Lab%2011%20-%20Travel%20Expense%20Agent%20and%20Agent%20Flow/index.md) | Optional extension: agent → agent flow, and agent flow → agent |

Day 2 concludes with the WSQ written and practical assessment from 4:00–6:00 PM.

## Supplied lab assets

- `Enquiry Log.xlsx` with named table `EnquiryLog`
- `Event Log.xlsx` with named table `EventLog`
- searchable IT FAQ, HR policy and Finance knowledge PDFs
- Lab 8 enquiry webpage
- Lab 9 Finance chat webpage
- Lab 10 TradingView and Finance Advisor webpage
- Lab 11 procurement approval import package
- JSON request schemas
- nine individual Power Automate legacy import packages with the `(NEW)`
  postfix for Labs 1–4 and 7–11, plus a combined bundle
- [import/remapping guide](labs/IMPORT-PACKAGES.md)

> **Import packages are not stored in this repository.** The `.zip` flow packages are
> rebuildable distribution artifacts and are excluded from GitHub by policy. Learners
> download them from the course material link on
> [lms-tms.tertiaryinfotech.com](https://lms-tms.tertiaryinfotech.com); trainers can
> regenerate them locally with `python3 scripts/build_v60_flow_packages.py`.

All Lab 8–10 webpages have a visible **Power Automate webhook URL** field. The learner pastes the generated URL at runtime, and the page stores it in that browser. No tenant webhook or data-provider API key is hard-coded.

Every lab folder also contains a labelled `flowchart.png` used in
the Learner Guide. Labs 1–10 also use the matching visual in the Version 6.0
facilitator deck; the two Lab 11 folders are supplementary extensions outside
the two-day timetable and the WSQ assessment. Each lab is
written as a click-by-click activity with prerequisites, scenario, expected
result, detailed build parts, test evidence and troubleshooting.

## Courseware

| Material | File |
|---|---|
| Learner Guide (Markdown) | [LEARNER-GUIDE.md](LEARNER-GUIDE.md) |
| Learner Guide (Word/PDF) | `courseware/LG-Business Process Automation with Power Automate and Copilot Studio Agents.docx/.pdf` |
| Lesson Plan (Word/PDF) | `courseware/LP-Business Process Automation with Power Automate and Copilot Studio Agents.docx/.pdf` |
| Facilitator deck | `courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v6.0.pptx/.pdf` |

The Learner Guide is compiled from the Markdown modules and lab instructions:

```bash
python3 .claude/skills/wsq-learner-guide/build_learner_guide.py
python3 .claude/skills/wsq-lesson-plan/build_lesson_plan.py
python3 scripts/restructure_course_deck.py
python3 scripts/build_v60_flow_packages.py
python3 scripts/validate_v60_flow_packages.py
python3 scripts/validate_v60_alignment.py
```

## Prerequisites

- Microsoft 365 work or school account
- Power Automate and Copilot Studio access
- Outlook, Microsoft Forms, Excel Online and SharePoint
- permission to publish course agents to Teams
- modern browser
- classroom API access for Twelve Data and NewsAPI in Lab 10
- Copilot Studio Workflows, Approvals and Outlook connections for Lab 11

Never place API keys, passwords, MFA codes, recovery keys or production personal data in source files, forms, agent instructions or screenshots.
