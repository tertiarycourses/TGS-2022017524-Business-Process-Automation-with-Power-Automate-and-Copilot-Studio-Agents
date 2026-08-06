# Hands-on Labs — Power Automate & Microsoft Copilot Studio

Labs for **Business Process Automation with Power Automate and Copilot Studio Agents**
(TGS-2022017524).

Eleven labs, built in order. Lab 0 prepares the environment; Labs 1–3 build deterministic
Power Automate workflows; Labs 4–5 build and invoke Copilot Studio agents; Labs 6–8 put an
agent behind a website over HTTP and add a human gate; Labs 9–10 ground an agent in documents
with RAG, first the built-in way and then with an external vector database.

| Lab | Title | Platform | The idea it teaches |
|---|---|---|---|
| **0** | [Environment Setup](Lab%200%20-%20Environment%20Setup/index.md) | Power Platform admin | One **Copilot Studio Training (Developer)** environment behind every later lab |
| **1** | [Trigger and Actions](Lab%201%20-%20Trigger%20and%20Actions/index.md) | Power Automate + Forms + Outlook | A **trigger** starts a flow; **actions** consume its outputs as dynamic content |
| **2** | [Log to Excel](Lab%202%20-%20Log%20to%20Excel/index.md) | Power Automate + Excel Online | **Commit before you confirm** — write the audit row, then send the mail |
| **3** | [Leave Application Approval](Lab%203%20-%20Leave%20Application%20Approval/index.md) | Power Automate + Approvals | **Human in the loop** — the flow pauses until a manager decides, then branches |
| **4** | [Agents](Lab%204%20-%20Agents%20/README.md) | Copilot Studio agents | An agent is **instructions, skills, knowledge, tools and connected agents** — and which of those actually hold |
| **4b** | [Multi-Agent Content Team](Lab%204b%20-%20Multi-Agent%20Content%20Team/README.md) *(optional)* | Copilot Studio connected agents | A **pipeline of specialists** — research → draft → review — ending at a human who approves |
| **5** | [Invoke Agents](Lab%205%20-%20Invoke%20Agents/index.md) | Copilot Studio + SharePoint + Teams | **Grounding and publishing** — a SharePoint knowledge source, privacy boundaries, deployed to Teams |
| **6** | [HTTP and Application Approval Agent](Lab%206%20-%20HTTP%20and%20Application%20Approval%20Agent/README.md) | Copilot Studio agent flow + SharePoint | The **boundary of agency** — the AI decides, deterministic actions do what must always happen |
| **7** | [HTTP and Chatbot](Lab%207%20-%20HTTP%20and%20Chatbot/README.md) | Copilot Studio + knowledge | **The agent alone** — rules in the instruction, facts in the knowledge source, and a refusal it must never break |
| **8** | [HTTP and Human Review](Lab%208%20-%20HTTP%20and%20Human%20Review/README.md) | Copilot Studio + Human review + Teams | **Human oversight** — the AI drafts, a licensed person approves, and the flow physically cannot proceed alone |
| **9** | [RAG with Knowledge Base](Lab%209%20-%20RAG%20with%20Knowledge%20Base/README.md) | Copilot Studio Knowledge | **RAG as a setting** — three nodes, no ingestion, and nothing you can inspect |
| **10** | [RAG with Pinecone](Lab%2010%20-%20RAG%20with%20Pinecone/README.md) | Copilot Studio + Power Automate + Pinecone | **What the convenience cost** — chunking, embeddings, dimension and `top_k`, back in your hands |

---

## What you need

- A Microsoft 365 **work or school** account with **Outlook**, **Excel/OneDrive**, **SharePoint**
  and **Microsoft Teams**.
- A Power Platform **Developer** environment named **Copilot Studio Training**, with Dataverse —
  built in Lab 0.
- **Copilot Credits** in that environment. Agent flows (Labs 6–10) consume credits on every run;
  Default and Sandbox environments frequently have none. This is why Lab 0 uses a Developer
  environment.
- A **Pinecone** account (free tier) — for Lab 10 only.

---

## The ideas, in order

**Labs 1–3 — the workflow, with no AI in it.**
A Microsoft Form submission starts a flow (Lab 1), the answers are written to an Excel table
before the confirmation goes out (Lab 2), and a manager's decision suspends the run partway
through and steers it down an approved or rejected branch (Lab 3). Nothing here is
probabilistic: the same input produces the same output every time. That is the baseline every
later lab is measured against.

**Labs 4–5 — the agent, and what it is made of.**
Lab 4 assembles four agents — Procurement, HR, Sales and IT Support — from the same five parts,
and is explicit about which parts the model can ignore:

| Part | What it is | Enforced? |
|---|---|---|
| **Instructions** | Who the agent is, always in force | **No** — probabilistic |
| **Skill** | A named procedure applied when the topic matches | **No** — the model decides it applies |
| **Knowledge** | Documents the agent may read | **Partly** — it cannot read what it was not given |
| **Tool** | A flow that acts outside the conversation | **The flow's own logic is enforced** |
| **Connected agent** | A separate agent with its own knowledge and audience | **The knowledge boundary is real** |

A control the model cannot reach beats a rule you asked it to follow. The optional **Lab 4b**
turns the same parts into a pipeline: a Marketing Manager delegates a topic through Research,
Blog and Review agents, and nothing is final until the person in the conversation approves it.
Lab 5 then grounds an HR
agent in a SharePoint policy source, tests its privacy refusals, and publishes it to Teams.

**Labs 6–8 — the agent behind a website, and the human gate.**
Lab 6 puts a public web form in front of an agent flow: a Compose action normalises the input, a
SharePoint lookup checks for duplicates, and an Agent node applies six ordered eligibility rules
and returns **structured output**. The customer record is written from the Compose action, never
from the model's answer, so an invented value has no route into the master data. There are four
decisions, not two — `APPROVED`, `REJECTED`, `DUPLICATE` and `REVIEW` — because some cases are
for a human, not for a rejection.

Lab 7 is the agent working alone in public: it collects contact details before it will answer,
answers from a grounded FAQ, and refuses to give financial advice. Nobody reviews anything, and
the test cases are written to make it fail.

Lab 8 adds the person back. The same website, but the flow drafts a reply and then stops at a
**Human review** node until a licensed human approves it in the Microsoft Teams Approvals app.

| Pattern | Who decides | Who acts | Can the AI proceed alone? |
|---|---|---|---|
| **Human *in* the loop** | AI proposes, human decides | Human authorises, system acts | **No** — it blocks |
| **Human *on* the loop** | AI decides and acts | Human monitors, can intervene | Yes — supervision is after the fact |
| **Human *out of* the loop** | AI decides and acts | AI | Yes — nobody checks |

Submit an enquiry in Lab 8 and watch the Activity tab: the run says *Running*, and it will still
say Running tomorrow. **That pause is the deliverable.**

**Labs 9–10 — RAG, twice.**
Lab 9 attaches a SharePoint folder of 20 brochures to the Agent node as a knowledge source and
turns *Use general knowledge* off. Three nodes, no ingestion, a working grounded chatbot in 45
minutes — and no way to see the chunks, the embedding model, the dimension or how many documents
came back. Lab 10 rebuilds the same chatbot on **Pinecone**, where each of those is yours to set.

| | Lab 9 — built-in | Lab 10 — external |
|---|---|---|
| Nodes | 3 | 5 |
| Ingestion | Upload to SharePoint | A Python script, run once |
| Embedding model | Hidden | `llama-text-embed-v2`, 1024 |
| Chunking | Hidden | One brochure = one record, **your call** |
| `top_k` | Hidden | 3, **your call** |
| Citation markers | Leak into the reply | None |
| A changed fee | Edit, wait for re-crawl | Edit, **re-ingest** |
| When it answers badly | Rewrite the prompt and hope | Four levers to pull |

Neither is the right answer. Which one is right depends on whether the person maintaining it will
ever need those levers — and that is a staffing question, not a technical one.

---

## Two things that will cost you an afternoon if you skip them

**The Instructions box is a rich-text editor.** Type an `@{...}` expression by hand and it stays
dead text — the flow runs green and the value arrives empty. Every dynamic value must be inserted
with the **⚡ picker** so it renders as a coloured token.

**A reference to nothing resolves to empty, not to an error.** This is the strongest thread across
every lab here. An empty reply is almost never a broken node; it is an instruction whose premise is
wrong, a knowledge source still indexing, or a chip pointing at a deleted action.

Two more, close behind: **approvals must go to Teams, not Outlook** (on a live tenant Outlook
created the request and never delivered the mail — the run sits at *Running*, looking healthy),
and **remove the "Search all websites" chip**, which is on by default and makes a fact from the
open web indistinguishable from one of your own.

---

## A note on the fictitious institutions

ACME Pte Ltd, Marina Trust Bank, Meridian Asset Management and Cook & Bake Academy do not exist.
They were created for this course. No banking, investment or education service is offered, and
nothing in these labs is financial advice.
