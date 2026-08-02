# Business Process Automation with Power Automate and Copilot Studio Agents

[![Duration](https://img.shields.io/badge/Duration-2%20Days-orange)]()
[![Labs](https://img.shields.io/badge/Labs-11%20Hands--On-purple)]()
[![Version](https://img.shields.io/badge/Courseware-7.0-blue)]()

This repository contains the Version 7.0 materials for the two-day WSQ course
**Business Process Automation with Power Automate and Copilot Studio Agents**
(`TGS-2022017524`).

The course is taught **concepts first**. Five concept modules introduce the ideas and the
decision rules; the labs that follow apply them. Day 1 moves from deterministic Power Automate
workflows to Copilot Studio agents and what they are made of. Day 2 puts an agent behind a
website over HTTP, adds a human review gate, and grounds an agent in documents with RAG — first
with built-in knowledge, then with an external Pinecone vector store.

## Learning outcomes

Participants will be able to:

- explain business process automation and the Trigger → Actions → Output model, and identify the
  four trigger families and the six action families;
- build Forms-driven Power Automate flows that send email, log data to Excel, branch on a
  condition and suspend for a human approval;
- describe an agent as instructions, skills, knowledge, tools and connected agents, and state
  which of those the model can ignore;
- create and ground Copilot Studio agents in approved SharePoint knowledge, test their refusals,
  and publish them to Microsoft Teams;
- connect a website to an HTTP-triggered agent flow, apply a JSON schema and use structured
  output to branch on the agent's decision;
- apply the boundary of agency and human-in-the-loop patterns so consequential actions require a
  person before they take effect;
- build a RAG chatbot with built-in knowledge and with an external Pinecone vector store, and
  justify the choice between them.

## Course structure

### Concept modules

| Module | Covers | Slides |
|---|---|---|
| [Module 1 — Business Process Automation and Power Automate](labs/Module%201%20-%20Business%20Process%20Automation%20and%20Power%20Automate.md) | BPA, the Power Platform, the environment, flow anatomy, all four trigger families, all six action families, dynamic content, run history, commit order | 12–20 |
| [Module 2 — Control Flow and Human in the Loop](labs/Module%202%20-%20Control%20Flow%20and%20Human%20in%20the%20Loop.md) | Conditions and branching; human in / on / out of the loop; how an approval suspends a run | 21–24 |
| [Module 3 — Copilot Studio Agents](labs/Module%203%20-%20Copilot%20Studio%20Agents.md) | Workflow versus agent; agent anatomy; what is actually enforced; instructions, knowledge, tools; connected agents; publishing | 25–33 |
| [Module 4 — Agent Flows, HTTP and the Boundary of Agency](labs/Module%204%20-%20Agent%20Flows,%20HTTP%20and%20the%20Boundary%20of%20Agency.md) | Agent flows, HTTP request/response, JSON schema, structured output, the boundary of agency, the human review gate | 34–40 |
| [Module 5 — Retrieval Augmented Generation](labs/Module%205%20-%20Retrieval%20Augmented%20Generation.md) | Why retrieval; ingestion and retrieval; chunking, embeddings, top_k; built-in versus external; probing for invention | 41–45 |

### Labs

| Lab | Title | Day | Platform |
|---|---|---|---|
| 0 | [Environment Setup](labs/Lab%200%20-%20Environment%20Setup/index.md) | 1 | Power Platform admin centre |
| 1 | [Trigger and Actions](labs/Lab%201%20-%20Trigger%20and%20Actions/index.md) | 1 | Power Automate + Forms + Outlook |
| 2 | [Log to Excel](labs/Lab%202%20-%20Log%20to%20Excel/index.md) | 1 | Power Automate + Excel Online |
| 3 | [Leave Application Approval](labs/Lab%203%20-%20Leave%20Application%20Approval/index.md) | 1 | Power Automate + Approvals |
| 4 | [Agents](labs/Lab%204%20-%20Agents%20/README.md) | 1 | Copilot Studio agents + agent flows |
| 5 | [Invoke Agents](labs/Lab%205%20-%20Invoke%20Agents/index.md) | 2 | Copilot Studio + SharePoint + Teams |
| 6 | [HTTP and Application Approval Agent](labs/Lab%206%20-%20HTTP%20and%20Application%20Approval%20Agent/README.md) | 2 | Copilot Studio agent flow + SharePoint |
| 7 | [HTTP and Chatbot](labs/Lab%207%20-%20HTTP%20and%20Chatbot/README.md) | 2 | Copilot Studio + knowledge + website |
| 8 | [HTTP and Human Review](labs/Lab%208%20-%20HTTP%20and%20Human%20Review/README.md) | 2 | Copilot Studio + Human review + Teams |
| 9 | [RAG with Knowledge Base](labs/Lab%209%20-%20RAG%20with%20Knowledge%20Base/README.md) | 2 | Copilot Studio Knowledge |
| 10 | [RAG with Pinecone](labs/Lab%2010%20-%20RAG%20with%20Pinecone/README.md) | 2 | Copilot Studio + Power Automate + Pinecone |

Full detail, including the ideas each lab teaches, is in [`labs/README.md`](labs/README.md).

## Supplied lab assets

- `Enquiry Log.xlsx` with named table `EnquiryLog`
- Searchable HR policy, investment FAQ and course brochure PDFs
- Static websites with chat widgets for Labs 6–10
- Sample question and probe sets (`sample-questions.csv`, `test-applications.csv`)
- JSON request schemas and agent instruction files
- Power Automate legacy import packages with the `(NEW)` postfix for Labs 1–3

> **Import packages are not stored in this repository.** The `.zip` flow packages are
> rebuildable distribution artifacts and are excluded from GitHub by policy. Learners
> download them from the course material link on
> [lms-tms.tertiaryinfotech.com](https://lms-tms.tertiaryinfotech.com).

The Lab 6–10 webpages have a visible **Power Automate webhook URL** field. The learner pastes
the generated URL at runtime and the page stores it in that browser. No tenant webhook or
data-provider API key is hard-coded.

Each lab is written as a click-by-click activity with prerequisites, scenario, expected result,
detailed build parts, test evidence and troubleshooting.

## Courseware

| Material | File |
|---|---|
| Learner Guide (Markdown) | [LEARNER-GUIDE.md](LEARNER-GUIDE.md) |
| Learner Guide (Word/PDF) | `courseware/LG-Business Process Automation with Power Automate and Copilot Studio Agents.docx/.pdf` |
| Lesson Plan (Word/PDF) | `courseware/LP-Business Process Automation with Power Automate and Copilot Studio Agents.docx/.pdf` |
| Facilitator deck | `courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v7.0.pptx/.pdf` |

`courseware/alignment_manifest.json` and `courseware/slide_map.json` are the single source of
truth that keeps the deck, Lesson Plan, Learner Guide and labs aligned.

Rebuild everything:

```bash
python3 scripts/build_v70_deck.py                                # facilitator deck
python3 scripts/check_deck_layout.py                             # layout guard
python3 .claude/skills/wsq-lesson-plan/build_lesson_plan.py      # Lesson Plan
python3 .claude/skills/wsq-learner-guide/build_learner_guide.py  # Learner Guide
```

## Prerequisites

- Microsoft 365 work or school account
- A Power Platform **Developer** environment named **Copilot Studio Training**, with Dataverse
  and **Copilot Credits** (built in Lab 0)
- Outlook, Microsoft Forms, Excel Online, SharePoint and Microsoft Teams
- Permission to publish course agents to Teams
- A free-tier **Pinecone** account, for Lab 10 only

## Assessment

Written Assessment (SAQ) 1 hour + Practical Performance (PP) 1 hour, on Day 2 from 4:00pm to
6:00pm, open book. WSQ funding requires at least 75% attendance and a Competent outcome.
