# Agent 1 — Procurement Agent

**Pattern taught:** *the agent as a caller of a governed flow.* The policy decision is made by a
model, but every consequential path ends at a control the model cannot reach — an audit row that is
always written, and a human gate that always fires.

**Build time:** 60–75 minutes (the longest of the four — build this one first).

---

## Folder contents

| Path | What it is | Where it goes in Copilot Studio |
|---|---|---|
| [`agent/instructions.md`](agent/instructions.md) | The agent-flow **Agent node** instruction — the procurement policy | Flow → Agent node → **Instructions** |
| [`agent/orchestrator-instructions.md`](agent/orchestrator-instructions.md) | The **top-level agent** instruction — how it talks to colleagues | Agent → **Instructions** |
| [`skills/`](skills/) | Two skill **packages** — [`raise-requisition.zip`](skills/_packages/raise-requisition.zip), [`vendor-enquiry.zip`](skills/_packages/vendor-enquiry.zip) | Agent → **Build → Skills → Add skill → Upload a skill** |
| [`tools/`](tools/) | The tool contract + tool descriptions | Agent → **Tools → + Add a tool** |
| [`knowledge/`](knowledge/) | `vendors.csv`, `procurement-policy.md`, `test-requisitions.csv` | SharePoint list + Agent → **Knowledge** |
| [`connected-agents/`](connected-agents/) | How Procurement is *consumed by* the other three agents | Agent → **Connected agents** |

---

## Order of build

1. **SharePoint** — create `ApprovedVendors` and `RequisitionLog`, import
   [`knowledge/vendors.csv`](knowledge/vendors.csv).
2. **The agent flow** — build `Lab 6 - Procurement Requisition Approval` per the main
   [Lab 6 README](../index.md), pasting [`agent/instructions.md`](agent/instructions.md) into
   the Agent node. **Publish it.**
3. **The agent** — create `Lab 6 - Procurement Agent`, paste
   [`agent/orchestrator-instructions.md`](agent/orchestrator-instructions.md) into Instructions.
4. **Tools** — attach the published flow, and give it the description from
   [`tools/tool-descriptions.md`](tools/tool-descriptions.md).
5. **Knowledge** — upload [`knowledge/procurement-policy.md`](knowledge/procurement-policy.md).
6. **Skills** — upload the two packages in [`skills/_packages/`](skills/_packages/), one at a time.
7. **Test** with [`knowledge/test-requisitions.csv`](knowledge/test-requisitions.csv) — all 13 cases.
8. **Deploy to Teams** — see [`publish-to-teams.md`](../../Lab%2017%20-%20Publish%20to%20Teams%2C%20Microsoft%20365%20Copilot%20and%20the%20Web/publish-to-teams.md).

---

## The two things learners get wrong

**They build the amount check and miss the status check.** TC5 (SGD 2,400, suspended vendor) and
TC7 (SGD 900, vendor under review) both must stop, and both are cheap. Ten cases pass, those two
fail, and in a real firm those are precisely the ones that cost you.

**They turn off "Search all websites" too late.** The panel in the screenshot has it *on* by
default. A procurement agent that can reach the open web will happily tell a colleague what a
workstation costs on Lazada. Remove that knowledge source before the first test — Knowledge → the
**✕** on the *Search all websites* chip.

---

## What this agent must NOT be used for

Releasing payment. The routing decision is a language model reading prose, and TC12 shows exactly
how that frays — a lowercase vendor name can produce a green run, a plausible reason and a wrong
answer, with no error anywhere. Rank the controls explicitly for learners:

> a control the model cannot reach **beats** a rule you asked it to follow, and neither of those is
> the same as a name someone typed into a text box.
