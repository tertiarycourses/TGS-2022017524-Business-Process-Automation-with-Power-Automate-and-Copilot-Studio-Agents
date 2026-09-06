# Business Process Automation with Power Automate and Copilot Studio Agents

[![Duration](https://img.shields.io/badge/Duration-2%20Days-orange)]()
[![Labs](https://img.shields.io/badge/Labs-18%20Hands--On-purple)]()
[![Version](https://img.shields.io/badge/Courseware-8.0-blue)]()

This repository contains the Version 8.0 materials for the two-day WSQ course
**Business Process Automation with Power Automate and Copilot Studio Agents**
(`TGS-2022017524`).

Every hands-on build in this course is made **entirely in the new Copilot Studio**
(`copilotstudio.microsoft.com`, **New experience** on): workflows in the workflow designer,
agents in the agent designer. Power Automate is the connector engine running underneath the
workflows — learners never open it directly, and nothing is imported from a package.

The course is taught **concepts first**. Five concept modules introduce the ideas and the
decision rules; the eighteen labs that follow apply them. Day 1 moves from deterministic
workflows to Copilot Studio agents and what they are made of. Day 2 chains agents, puts an agent
behind a website over HTTP, adds a human review gate, grounds an agent in documents with RAG —
first with built-in knowledge, then with an external Pinecone vector store — and publishes an
agent to Teams, Microsoft 365 Copilot and the web.

## Learning outcomes

Participants will be able to:

- explain business process automation and the Trigger → Actions → Output model, and identify the
  trigger families and the action families of a Copilot Studio workflow;
- build Forms-driven workflows that send email, log data to Excel, branch on a condition and
  suspend for a human decision (Human review in Teams);
- use the Classify and Agent nodes so a model chooses the branch while deterministic actions act;
- describe an agent as instructions, model, knowledge, skills, tools and connected agents, and
  state which of those the model can ignore;
- create and ground Copilot Studio agents in approved SharePoint knowledge, attach skills and
  workflow tools, connect agents into a pipeline, and test their refusals;
- connect a website to an HTTP-triggered workflow, apply a JSON schema and use structured
  output to branch on the agent's decision;
- apply the boundary of agency and human-in-the-loop patterns so consequential actions require a
  person before they take effect;
- build a RAG chatbot with built-in knowledge and with an external Pinecone vector store, and
  justify the choice between them;
- publish an agent to Microsoft Teams, Microsoft 365 Copilot and a demo website, and explain what
  each channel needs.

## Course structure

### Concept modules

| Module | Covers | Labs |
|---|---|---|
| [Module 1 — Business Process Automation and Power Automate](labs/Module%201%20-%20Business%20Process%20Automation%20and%20Power%20Automate.md) | BPA, the Power Platform, the environment, workflow anatomy, trigger and action families, dynamic content, run history, commit order | 0–2 |
| [Module 2 — Control Flow and Human in the Loop](labs/Module%202%20-%20Control%20Flow%20and%20Human%20in%20the%20Loop.md) | If/Else, Switch and Compose; human in / on / out of the loop; Human review via Teams versus email; how a gate suspends a run | 3–4 |
| [Module 3 — Copilot Studio Agents](labs/Module%203%20-%20Copilot%20Studio%20Agents.md) | Workflow versus agent; the new Copilot Studio (model + harness, the new agent designer); agent anatomy; what is enforced; instructions, skills, knowledge, tools, MCP, connected agents; settings; publishing and channels | 5–11, 17 |
| [Module 4 — Agent Flows, HTTP and the Boundary of Agency](labs/Module%204%20-%20Agent%20Flows,%20HTTP%20and%20the%20Boundary%20of%20Agency.md) | The workflow designer, the HTTP trigger and Response, GET vs POST, JSON schema, structured output, the boundary of agency, the human review gate | 12–14 |
| [Module 5 — Retrieval Augmented Generation](labs/Module%205%20-%20Retrieval%20Augmented%20Generation.md) | Why retrieval; ingestion and retrieval; chunking, embeddings, top_k; built-in versus external; probing for invention | 15–16 |

### Labs (18 — Lab 0 to Lab 17, every entry file is `index.md`)

| Lab | Title | Day | Platform |
|---|---|---|---|
| 0 | [Environment Setup](labs/Lab%200%20-%20Environment%20Setup/index.md) | 1 | Power Platform admin centre + Copilot Studio |
| 1 | [Trigger and Actions](labs/Lab%201%20-%20Trigger%20and%20Actions/index.md) | 1 | Workflow + Forms + Outlook |
| 2 | [Log to Excel](labs/Lab%202%20-%20Log%20to%20Excel/index.md) | 1 | Workflow + Excel Online |
| 3 | [Leave Application Approval](labs/Lab%203%20-%20Leave%20Application%20Approval/index.md) | 1 | Workflow + Human review (Teams) + Excel |
| 4 | [Email Classification](labs/Lab%204%20-%20Email%20Classification/index.md) | 1 | Workflow + Outlook + Classify + Human review |
| 5 | [Your First Agent](labs/Lab%205%20-%20Your%20First%20Agent/index.md) | 1 | Agent designer |
| 6 | [Procurement Agent with Tools](labs/Lab%206%20-%20Procurement%20Agent%20with%20Tools/index.md) | 1 | Agent + workflow as a tool + Excel |
| 7 | [Sales Agent with Knowledge](labs/Lab%207%20-%20Sales%20Agent%20with%20Knowledge/index.md) | 1 | Agent + knowledge |
| 8 | [IT Support Agent with Skills](labs/Lab%208%20-%20IT%20Support%20Agent%20with%20Skills/index.md) | 1 | Agent + skill packages |
| 9 | [Multi-Agent Content Team](labs/Lab%209%20-%20Multi-Agent%20Content%20Team/index.md) | 2 | Connected agents |
| 10 | [Calling Agent from Workflow](labs/Lab%2010%20-%20Calling%20Agent%20from%20Workflow/index.md) | 2 | Workflow + Copilot node + Teams |
| 11 | [Calling Workflow from Agent](labs/Lab%2011%20-%20Calling%20Workflow%20from%20Agent/index.md) | 2 | Agent + workflow as a tool |
| 12 | [HTTP and Application Approval Agent](labs/Lab%2012%20-%20HTTP%20and%20Application%20Approval%20Agent/index.md) | 2 | Workflow + SharePoint + Outlook + website |
| 13 | [HTTP and Chatbot](labs/Lab%2013%20-%20HTTP%20and%20Chatbot/index.md) | 2 | Workflow + knowledge + website |
| 14 | [HTTP and Human Review](labs/Lab%2014%20-%20HTTP%20and%20Human%20Review/index.md) | 2 | Workflow + Human review + Excel + Teams |
| 15 | [RAG with Knowledge Base](labs/Lab%2015%20-%20RAG%20with%20Knowledge%20Base/index.md) | 2 | Workflow + SharePoint knowledge |
| 16 | [RAG with Pinecone](labs/Lab%2016%20-%20RAG%20with%20Pinecone/index.md) | 2 | Workflow + HTTP + Pinecone |
| 17 | [Publish to Teams, Microsoft 365 Copilot and the Web](labs/Lab%2017%20-%20Publish%20to%20Teams%2C%20Microsoft%20365%20Copilot%20and%20the%20Web/index.md) | 2 | Channels + |

Full detail, including the ideas each lab teaches, is in [`labs/README.md`](labs/README.md).
Every lab folder carries a `screenshots/` folder of the real new-designer UI, embedded in the
lab guide and on the deck's "What You Will See" slides.

## Environments

Three environments back this course:

| Environment | Type | Id | Purpose |
|---|---|---|---|
| `Training Class 1` / `2` / `3` | Sandbox | — | **Where learners work.** One per class; the trainer resets or refreshes it between cohorts |
| `TGS-2022017524-Business Process Automation with Power Automate and Copilot Studio Agents` | Sandbox | `f4e94101-0889-e2f3-a0f4-dfd6d06ab28e` (org `org77fbcb45.crm5.dynamics.com`) | The **master reference environment**: all 12 `Lab N - … (DO NOT DELETE)` workflows and all 9 reference agents. Kept pristine; read-only for learners |
| `Copilot Studio Training (Developer)` | Developer | `dd7a990d-5d41-e3a8-82ae-8ede6fe42d92` | The original build environment — **retired from classroom use** (Developer environments are single-user) |

Learners work only in their class Sandbox. A Sandbox is used rather than Developer (single-user)
or Trial (self-deletes after 30 days) because it is the only type that supports multi-user access
and a **Reset** between classes — so a class cannot damage the reference builds, and the next
cohort starts clean.

## Tenant naming

Everything is named after its lab:

- **Workflows** — exactly the lab title: `Lab 1 - Trigger and Actions`, `Lab 12 - HTTP and
  Application Approval Agent`; helper workflows `Lab 6 - Raise Requisition`, `Lab 11 - Blog Writer
  Tool`. The trainer's reference copies carry ` (DO NOT DELETE)`.
- **Agents** — lab prefix + name, **30 characters or fewer** (Copilot Studio rejects longer names
  with *Agent name must be 30 characters or fewer*): `Lab 5 - HR Agent`, `Lab 9 - Marketing
  Manager`. The trainer's reference copies carry ` (DO NOT DELETE)` as well, with the base name
  shortened so the suffix fits — `Lab 5 - HR (DO NOT DELETE)`, `Lab 6 - Proc (DO NOT DELETE)`,
  `Lab 7 - Sales (DO NOT DELETE)`, `Lab 8 - IT (DO NOT DELETE)`, `Lab 9 - Res (DO NOT DELETE)`,
  `Lab 9 - Blog (DO NOT DELETE)`, `Lab 9 - Review (DO NOT DELETE)`, `Lab 9 - Mgr (DO NOT DELETE)`,
  `Lab 11 - Blog (DO NOT DELETE)`.
- **Forms, workbooks, SharePoint folders and lists** — lab prefix: `Lab 1 - Course Enquiry Form`,
  `Lab 3 - Leave Application Form`; OneDrive folder `Power Automate Lab Data` with
  `Lab 2 - Enquiry Log.xlsx`, `Lab 3 - Leave Register.xlsx`, `Lab 6 - Requisition Log.xlsx`,
  `Lab 14 - Handover Queue.xlsx`; SharePoint site *Tertiary Infotech - WSQ Courses* with folders
  `Lab 5 - HR Policies`, `Lab 6 - Procurement Knowledge`, `Lab 7 - Course Brochures`,
  `Lab 8 - IT Knowledge`, `Lab 13 - Investment FAQ`, `Lab 15 - Course Brochures` and lists
  `Lab 12 - Customers`, `Lab 12 - Onboarding Log`.

> **Copilot Credits.** Every agent Preview, demo-website chat and every Agent / Classify / Copilot
> node run consumes Copilot Credits. An environment with none answers every prompt with
> *"You need credits to continue … Error code: EnforcementUsageCredits"* — building, saving and
> publishing still work. Before class the trainer allocates credits in the Power Platform admin
> center → **Licensing → Copilot Studio → Manage Copilot Credits** to each `Training Class`
> environment.

## Supplied lab assets

- Rebuild sheets for both Microsoft Forms and generators for the four Excel workbooks
- Agent build kits for Labs 5–9 and 11 — instructions, uploadable skill packages
  (`skills/_packages/*.zip`), tool contracts, mock knowledge (HR policies, vendor register,
  IT service catalogue, 20 course brochures, marketing personas) and connected-agent definitions
- Static websites with chat widgets for Labs 12–16, each with a visible **workflow URL** field —
  the learner pastes the HTTP trigger URL at run time; no tenant URL or API key is hard-coded
- Sample question and probe sets (`sample-questions.csv`, `test-applications.csv`,
  `test-emails.md`), JSON request schemas and agent instruction files
- Graphviz flowcharts (`assets/flowchart.png`) and real UI screenshots (`screenshots/`) per lab
- Going-further kits: HR connected agents (Lab 5), IT agent Teams deployment (Lab 8), the HR agent
  as a web chat via the Microsoft 365 Agents SDK (Lab 17)

Each lab is written as a click-by-click activity with prerequisites, scenario, expected result,
detailed build parts, test evidence, troubleshooting and key takeaways.

## Courseware

| Material | File |
|---|---|
| Learner Guide (Markdown) | [LEARNER-GUIDE.md](LEARNER-GUIDE.md) |
| Learner Guide (Word/PDF) | `courseware/LG-Business Process Automation with Power Automate and Copilot Studio Agents.docx/.pdf` |
| Lesson Plan (Word/PDF) | `courseware/LP-Business Process Automation with Power Automate and Copilot Studio Agents.docx/.pdf` |
| Facilitator deck | `courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v8.2.pptx/.pdf` |

`courseware/alignment_manifest.json` (lab table, durations, tenant names) and
`courseware/slide_map.json` (written by the deck builder) keep the deck, Lesson Plan, Learner
Guide and labs aligned. Superseded deck versions live in `courseware/archive/`.

Rebuild everything (labs/ is the ground truth — never hand-edit the LG/LP DOCX):

```bash
python3 scripts/build_v80_deck.py                                # facilitator deck v8.2 (self-contained; picks up labs/*/screenshots, writes slide_map.json, archives the previous copy)
python3 .claude/skills/wsq-lesson-plan/build_lesson_plan.py      # Lesson Plan
python3 .claude/skills/wsq-learner-guide/build_learner_guide.py  # Learner Guide DOCX + LEARNER-GUIDE.md
soffice --headless --convert-to pdf --outdir courseware "courseware/<file>.pptx|.docx"
```

The trainer's reference workflows were built through the Dataverse API with
`scripts/copilot_studio_api/` (`wfapi.py`, `wfapi_ext.py`, `build_labN.py`, `FORMATS.md`) and
then saved and published in the designer; the agents were built by hand in the agent designer.
See `CLAUDE.md` for the build route.

## Prerequisites

- Microsoft 365 work or school account with Outlook, Microsoft Forms, Excel Online/OneDrive,
  SharePoint and Microsoft Teams
- Access to the **Training Class** Sandbox environment assigned to the class, with Dataverse
  and **Copilot Credits** (Lab 0), Copilot Studio switched to the **New experience**
  (self-study: a personal Developer environment instead)
- A Microsoft 365 Copilot licence only for the Copilot channel part of Lab 17
- A free-tier **Pinecone** account, for Lab 16 only

## Assessment

Written Assessment (SAQ) 1 hour + Practical Performance (PP) 1 hour, on Day 2 from 4:30pm to
6:30pm, open book. WSQ funding requires at least 75% attendance and a Competent outcome.
