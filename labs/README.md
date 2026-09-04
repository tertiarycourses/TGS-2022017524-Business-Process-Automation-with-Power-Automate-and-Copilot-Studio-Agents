# Hands-on Labs — Copilot Studio Workflows and Agents

Labs for **Business Process Automation with Power Automate and Copilot Studio Agents**
(TGS-2022017524).

Eighteen labs, Lab 0 to Lab 17, built in order over two days. Every hands-on build is made in
**one designer** — Copilot Studio in the **New experience** (`copilotstudio.microsoft.com`) —
and every lab's entry file is `index.md`. Power Automate is the connector engine running
underneath the workflows; you never open it directly.

| Lab | Title | Day · min | Platform | The idea it teaches |
|---|---|---|---|---|
| **0** | [Environment Setup](Lab%200%20-%20Environment%20Setup/index.md) | 1 · 20 | Power Platform admin centre | One **Training Class** Sandbox environment per class, with Copilot Credits, behind every later lab |
| **1** | [Trigger and Actions](Lab%201%20-%20Trigger%20and%20Actions/index.md) | 1 · 30 | Workflow + Forms + Outlook | A **trigger** starts a workflow; **connector actions** consume its outputs as dynamic content |
| **2** | [Log to Excel](Lab%202%20-%20Log%20to%20Excel/index.md) | 1 · 30 | Workflow + Excel Online | **Commit before you confirm** — write the audit row, then send the mail |
| **3** | [Leave Application Approval](Lab%203%20-%20Leave%20Application%20Approval/index.md) | 1 · 35 | Workflow + Approvals | **Human in the loop** — the run pauses until a manager decides, then **If/Else** branches |
| **4** | [Email Classification](Lab%204%20-%20Email%20Classification/index.md) | 1 · 45 | Workflow + Outlook + Classify + Human review | The **Classify** node sorts each email into five ports; every port acts; Priority stops at a human in Teams |
| **5** | [Your First Agent](Lab%205%20-%20Your%20First%20Agent/index.md) | 1 · 35 | Agent designer | An agent is **instructions + model + knowledge** — and Preview is where you find out what it refuses |
| **6** | [Procurement Agent with Tools](Lab%206%20-%20Procurement%20Agent%20with%20Tools/index.md) | 1 · 35 | Agent + workflow as a tool + Excel | **A tool is a contract** — the agent fills the inputs, the workflow's logic is enforced, the reference proves it ran |
| **7** | [Sales Agent with Knowledge](Lab%207%20-%20Sales%20Agent%20with%20Knowledge/index.md) | 1 · 30 | Agent + SharePoint knowledge | **Grounding** in 20 brochures, and refusing to invent — for the public |
| **8** | [IT Support Agent with Skills](Lab%208%20-%20IT%20Support%20Agent%20with%20Skills/index.md) | 1 · 30 | Agent + skill packages | **A skill is a procedure, not a permission** — and a tool the agent does not have is a control |
| **9** | [Multi-Agent Content Team](Lab%209%20-%20Multi-Agent%20Content%20Team/index.md) | 2 · 35 | Connected agents | A **pipeline of specialists** — research → draft → review — ending at a human who approves |
| **10** | [Calling Agent from Workflow](Lab%2010%20-%20Calling%20Agent%20from%20Workflow/index.md) | 2 · 25 | Workflow + M365 Copilot + Teams | **The workflow calls the model** at a fixed step and posts the draft to Teams |
| **11** | [Calling Workflow from Agent](Lab%2011%20-%20Calling%20Workflow%20from%20Agent/index.md) | 2 · 25 | Agent + workflow as a tool | **The agent calls the workflow** — *When an agent calls the flow* in, *Respond to the agent* out |
| **12** | [HTTP and Application Approval Agent](Lab%2012%20-%20HTTP%20and%20Application%20Approval%20Agent/index.md) | 2 · 45 | Workflow + SharePoint + Outlook | The **boundary of agency** — the AI decides, deterministic actions do what must always happen |
| **13** | [HTTP and Chatbot](Lab%2013%20-%20HTTP%20and%20Chatbot/index.md) | 2 · 30 | Workflow + knowledge + website | **The agent alone** — rules in the instruction, facts in the knowledge source, and a refusal it must never break |
| **14** | [HTTP and Human Review](Lab%2014%20-%20HTTP%20and%20Human%20Review/index.md) | 2 · 35 | Workflow + Human review + Excel + Teams | **Human oversight** — the AI drafts, a licensed person approves, and the run physically cannot proceed alone |
| **15** | [RAG with Knowledge Base](Lab%2015%20-%20RAG%20with%20Knowledge%20Base/index.md) | 2 · 30 | Workflow + Knowledge + SharePoint | **RAG as a setting** — three nodes, no ingestion, and nothing you can inspect |
| **16** | [RAG with Pinecone](Lab%2016%20-%20RAG%20with%20Pinecone/index.md) | 2 · 30 | Workflow + Pinecone | **What the convenience cost** — chunking, embeddings, dimension and `top_k`, back in your hands |
| **17** | [Publish to Teams, Microsoft 365 Copilot and the Web](Lab%2017%20-%20Publish%20to%20Teams%2C%20Microsoft%20365%20Copilot%20and%20the%20Web/index.md) | 2 · 25 | Channels + | **A channel is a door, not a brain** — each door needs something different, and none of them changes the agent |

Readings: [Module 1](Module%201%20-%20Business%20Process%20Automation%20and%20Power%20Automate.md) (before Labs 0–2) ·
[Module 2](Module%202%20-%20Control%20Flow%20and%20Human%20in%20the%20Loop.md) (Labs 3–4) ·
[Module 3](Module%203%20-%20Copilot%20Studio%20Agents.md) (Labs 5–9, 11, 17) ·
[Module 4](Module%204%20-%20Agent%20Flows%2C%20HTTP%20and%20the%20Boundary%20of%20Agency.md) (Labs 12–14) ·
[Module 5](Module%205%20-%20Retrieval%20Augmented%20Generation.md) (Labs 15–16).

---

## The naming rule

Everything you build in the tenant is named after its lab, so eighteen labs' worth of artefacts
can be told apart at a glance:

| Kind | Rule | Examples |
|---|---|---|
| **Workflow** | Exactly the lab title | `Lab 1 - Trigger and Actions` · `Lab 4 - Email Classification` · `Lab 12 - HTTP and Application Approval Agent` |
| **Helper workflow** (a tool) | Lab prefix + what it does | `Lab 6 - Raise Requisition` · `Lab 11 - Blog Writer Tool` |
| **Agent** | Lab prefix + the agent's name, **30 characters or fewer** (Copilot Studio rejects longer names) | `Lab 5 - HR Agent` · `Lab 6 - Procurement Agent` · `Lab 7 - Sales Agent` · `Lab 8 - IT Support Agent` · `Lab 9 - Marketing Manager` / `Lab 9 - Research Agent` / `Lab 9 - Blog Agent` / `Lab 9 - Review Agent` · `Lab 11 - Blog Writer Agent` |
| **Form** | Lab prefix | `Lab 1 - Course Enquiry Form` (Labs 1–2) · `Lab 3 - Leave Application Form` |
| **Excel workbook** (folder `Power Automate Lab Data`) | Lab prefix; tables keep plain names | `Lab 2 - Enquiry Log.xlsx` (EnquiryLog) · `Lab 3 - Leave Register.xlsx` · `Lab 6 - Requisition Log.xlsx` · `Lab 14 - Handover Queue.xlsx` (Drafts, HandoverQueue) |
| **SharePoint list / folder** | Lab prefix | `Lab 5 - HR Policies` · `Lab 7 - Course Brochures` · `Lab 12 - Customers` · `Lab 12 - Onboarding Log` · `Lab 13 - Investment FAQ` · `Lab 15 - Course Brochures` |
| **Other** | Lab prefix | Outlook folder `Lab 4 - Other` · Pinecone index `lab16-course-brochures` |

**The trainer's canonical copies — two suffixes, because agent names are capped.**

| Kind | Trainer's reference copy | Why |
|---|---|---|
| **Workflow** | `Lab N - <Title> (DO NOT DELETE)` — `Lab 1 - Trigger and Actions (DO NOT DELETE)`, `Lab 6 - Raise Requisition (DO NOT DELETE)`, `Lab 14 - HTTP and Human Review (DO NOT DELETE)` … | Workflow names have no length limit |
| **Agent** | `<short name> (DO NOT DELETE)` — `Lab 5 - HR (DO NOT DELETE)` · `Lab 6 - Proc (DO NOT DELETE)` · `Lab 7 - Sales (DO NOT DELETE)` · `Lab 8 - IT (DO NOT DELETE)` · `Lab 9 - Res (DO NOT DELETE)` · `Lab 9 - Blog (DO NOT DELETE)` · `Lab 9 - Review (DO NOT DELETE)` · `Lab 9 - Mgr (DO NOT DELETE)` · `Lab 11 - Blog (DO NOT DELETE)` | **Agent names must be 30 characters or fewer** (`Agent name must be 30 characters or fewer`), so the base name is shortened until the full `(DO NOT DELETE)` suffix fits |

They live in the **master reference environment** — the Sandbox named
`TGS-2022017524-Business Process Automation with Power Automate and Copilot Studio Agents` — as
finished reference builds for you to open and compare against. They are read-only for learners;
never edit, disable or delete them. You build your own copies in **your class environment**, named
plainly, without either suffix — and keep every agent name within 30 characters
(`Lab 9 - Marketing Manager` is 25; `Lab 9 - Marketing Manager Agent` is 31 and is rejected).

---

## Three environments, and which one you work in

| Environment | Type | Who works in it |
|---|---|---|
| `Training Class 1` / `Training Class 2` / `Training Class 3` | Sandbox | **You.** One per class; your trainer tells you which one is yours. Everything you build in Labs 0–17 goes here |
| `TGS-2022017524-Business Process Automation…` | Sandbox | The **master reference environment**. Holds every `Lab N - … (DO NOT DELETE)` workflow and agent. Read-only for learners — open to compare, never to edit |
| `Copilot Studio Training (Developer)` | Developer | The original build environment. **Retired from classroom use** — a Developer environment is single-user, so a class cannot share it |

Your class environment is **disposable on purpose**. The trainer **resets** it between cohorts, so
the next class starts empty. That is exactly why learners no longer work in the reference
environment: nothing you do can damage the builds everyone else compares against.

**Why a Sandbox, and not a Developer or Trial environment?**

| | Developer | **Sandbox** | Trial |
|---|---|---|---|
| Who can access it | One user only | **Everyone in the class** | Users you assign |
| Lifespan | Persistent | **Persistent** | **Self-deletes after 30 days** |
| Reset between classes | No | **Yes** | No |

Sandbox is the only one of the three that is both multi-user and resettable — which is what a
classroom needs.

---

## What you need

- A Microsoft 365 **work or school** account with **Outlook**, **Excel/OneDrive**, **SharePoint**
  and **Microsoft Teams** (a Microsoft 365 Copilot licence is needed only for one part of Lab 17).
- Access to the **Training Class** Sandbox environment your trainer assigned (for example
  **Training Class 1**), with Dataverse — you switch into it in Lab 0 — and Copilot Studio
  switched to the **New experience**.
- **Copilot Credits** in that environment. Every agent Preview, demo-website chat and every workflow
  with an Agent, Classify or Copilot node (Labs 4–16) consumes credits on each run; an environment
  with none allocated fails every one of them. Without them every reply is *"You need credits to continue …
  Error code: EnforcementUsageCredits"* — building and publishing still work. The trainer allocates
  credits in the Power Platform admin center → **Licensing → Copilot Studio → Manage Copilot Credits**
  before class (see Lab 0).
- A **Pinecone** account (free tier) — for Lab 16 only.

---

## The ideas, in order

**Labs 1–3 — the workflow, with no AI in it.**
A Microsoft Form submission starts a workflow (Lab 1), the answers are written to an Excel table
before the confirmation goes out (Lab 2), and a manager's decision suspends the run partway
through and steers it down an If or an Else branch (Lab 3). Nothing here is probabilistic: the
same input produces the same output every time. That is the baseline every later lab is measured
against.

**Lab 4 — the model chooses the branch; the actions still act.**
An Outlook trigger, a **Classify** node with five categories in a deliberate order, and a
different deterministic handler on every port. The Priority port stops at a **Human review** card
in Teams. It is the first time a model decides something in your workflow, and the first time a
gate blocks a run.

**Labs 5–8 — the agent, one part at a time.**
Lab 5 is instructions plus knowledge (the HR agent). Lab 6 adds a **tool** — a workflow the agent
calls, whose logic is enforced. Lab 7 is **knowledge** for the public — 20 brochures and the
discipline of not inventing a fee. Lab 8 is **skills** — five uploaded packages, and the
demonstration that a skill is a procedure, not a permission.

| Part | What it is | Enforced? |
|---|---|---|
| **Instructions** | Who the agent is, always in force | **No** — probabilistic |
| **Knowledge** | Documents the agent may read | **Partly** — it cannot read what it was not given |
| **Tool** | A workflow that acts outside the conversation | **The workflow's own logic is enforced** |
| **Skill** | A named procedure applied when the topic matches | **No** — the model decides it applies |
| **Connected agent** | A separate agent with its own knowledge and audience | **The knowledge boundary is real** |

A control the model cannot reach beats a rule you asked it to follow.

**Labs 9–11 — many agents, and the two directions across the boundary.**
Lab 9 turns the same parts into a pipeline: a manager delegates one topic through Research, Blog
and Review agents, and nothing is final until the person approves. Lab 10 crosses the boundary in
one direction — a workflow that calls the model at a fixed step and posts to Teams — and Lab 11
crosses it in the other: an agent that calls a published workflow as a tool, with the trigger's
input and the *Respond to the agent* output as the contract.

**Labs 12–14 — the agent behind a website, and the human gate.**
Lab 12 puts a public web form in front of a workflow: a SharePoint lookup checks for duplicates, a
Compose node assembles the application, and an Agent node applies six ordered rules and returns
**structured output**. There are four decisions, not two, because some cases are for a human. Lab
13 is the agent working alone in public: it collects contact details, answers from a grounded FAQ,
and refuses to give financial advice — and the test cases are written to make it fail. Lab 14 adds
the person back: the same website, but the workflow drafts a reply and stops at a **Human review**
node until a licensed human approves it in Teams. Submit an enquiry and watch Activity: the run
says *Running*, and it will still say Running tomorrow. **That pause is the deliverable.**

**Labs 15–16 — RAG, twice.**
Lab 15 attaches a SharePoint folder of 20 brochures to the Agent node as a knowledge source: three
nodes, no ingestion, a working grounded chatbot — and no way to see the chunks, the embedding
model, the dimension or how many documents came back. Lab 16 rebuilds the same chatbot on
**Pinecone**, where each of those is yours to set, and the Compose node's Outputs show exactly what
the agent was given.

**Lab 17 — the doors.**
Publish, then **Channels +**: Microsoft Teams, Microsoft 365 Copilot, a public website. The HR
agent goes to Teams and Copilot; the Sales agent goes to the web; and the reason the HR agent must
never be made anonymous for an embed code is the last governance lesson of the course.

---

## Two things that will cost you an afternoon if you skip them

**The Instructions box of an Agent node is a rich-text editor.** Paste an `@{...}` expression and
it stays dead text or gets its underscores escaped — the run goes green and the value arrives
empty. Build the per-call block in a **Compose** node and insert one **⚡** chip. The same applies
to the Outlook **To** field: a typed expression fails with a trailing-newline error; a ⚡ token
does not.

**A reference to nothing resolves to empty, not to an error.** This is the strongest thread across
every lab here. An empty reply is almost never a broken node; it is an instruction whose premise is
wrong, a knowledge source still indexing, or a chip pointing at a deleted action.

Two more, close behind: **Human review must go to Teams, not Outlook** (the card arrives in the
Teams **Workflows** bot chat; on a live tenant Outlook created the request and never delivered
the mail), and **remove the "Search all websites" chip**, which is on by default and makes a fact
from the open web indistinguishable from one of your own.

---

## A note on the fictitious institutions

ACME Pte Ltd, Keppel Ridge Engineering, Tertiary Infotech Academy's Training Office as portrayed
here, Marina Trust Bank, Meridian Asset Management and Cook & Bake Academy are fictional or
fictionalised for this course. No banking, investment or education service is offered, and
nothing in these labs is financial advice.
