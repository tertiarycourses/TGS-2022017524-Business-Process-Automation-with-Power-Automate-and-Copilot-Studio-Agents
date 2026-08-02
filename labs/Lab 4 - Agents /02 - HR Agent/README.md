# Agent 2 — HR Agent

**Pattern taught:** *the orchestrator and its children.* One agent that talks to staff and
candidates, and four child agents it hands over to. This is the agent that teaches **connected
agents**, and the reason the split is a governance decision rather than a tidiness one.

**Build time:** 75–90 minutes for the parent plus all four children. The parent plus
*Policy and Benefits* alone is a viable 40-minute version — see the note at the bottom.

---

## Folder contents

| Path | What it is |
|---|---|
| [`agent/instructions.md`](agent/instructions.md) | The parent agent's Instructions — routing and refusals |
| [`skills/`](skills/) | Two Skills — handover discipline, and personal-data handling |
| [`tools/tool-descriptions.md`](tools/tool-descriptions.md) | `LookupLeaveBalance`, `CreateHRCase` |
| [`knowledge/`](knowledge/) | `HR Policies.pdf`, mock HR policy, benefits summary, staff leave data |
| [`connected-agents/`](connected-agents/) | The four children, one folder each |

### The four children

| # | Agent | Owns | Talks to |
|---|---|---|---|
| 1 | [Screening Agent](connected-agents/01%20-%20Screening%20Agent/) | Applications against role criteria | Recruiters |
| 2 | [Interview Agent](connected-agents/02%20-%20Interview%20Agent/) | Scheduling and interview packs | Hiring managers |
| 3 | [Onboarding Agent](connected-agents/03%20-%20Onboarding%20Agent/) | Day-one checklists, IT and access requests | New joiners, managers |
| 4 | [Policy and Benefits Agent](connected-agents/04%20-%20Policy%20and%20Benefits%20Agent/) | Leave, benefits, claims — the everyday questions | All staff |

---

## The shape

```
                          HR Agent  (Teams — this is the one staff message)
                              │
      ┌──────────────┬────────┴────────┬──────────────────┐
      ▼              ▼                 ▼                  ▼
  Screening      Interview        Onboarding      Policy & Benefits
      │              │                 │                  │
      │              │                 └──► IT Support Agent (cross-tree)
      │              │                 └──► Procurement Agent (cross-tree)
      ▼              ▼                                     ▼
  candidates.csv  interview-       onboarding-      hr-policy.md
                  guide.md         checklist.md     benefits-summary.md
```

Two of the arrows leave the HR tree entirely. A new joiner needs a laptop and a mailbox, and those
are owned by IT Support and Procurement. That crossing is the most realistic thing in this lab and
the part worth the most discussion — see
[`connected-agents/03 - Onboarding Agent/`](connected-agents/03%20-%20Onboarding%20Agent/).

---

## Why four agents instead of one long instruction

The honest answer is **not** "the instructions were getting long". Length is a symptom. The real
reasons, in the order they matter:

**1. Different children may know different things.** Screening reads candidate records. Policy and
Benefits reads the staff handbook. A single agent holding both can answer a benefits question using
a candidate's salary expectation, and nothing on the canvas would show that it did.

**2. Different children have different audiences.** The Screening Agent talks to recruiters. If a
candidate reaches it, the failure is not a wrong answer — it is a candidate being told how they
scored against the criteria. A separate agent makes that boundary a *thing you configure* rather
than a sentence you hope the model honours.

**3. A handover is visible; a topic switch is not.** When the parent hands over, the transcript
records it. When one large agent silently moves from policy to screening mid-conversation, nothing
marks the moment.

Ask the class the counter-question too: **what did we lose?** Four agents is four sets of
instructions to keep aligned, four things to publish, and a user-visible pause at each handover.
Splitting is not free, and "one agent" is the right answer more often than architecture diagrams
suggest.

---

## Build order

1. Build **Policy and Benefits** first — it is the simplest and it is the one you can demonstrate
   immediately.
2. Build the **parent** and connect Policy and Benefits to it. Test the handover before adding more.
3. Add **Screening**, **Interview**, **Onboarding** one at a time, testing after each.

> **Do not build all five and then test.** When a handover misfires you need to know which addition
> broke it. One change per publish-test cycle — each cycle costs a publish plus ~25s.

---

## Shortened version for a 40-minute slot

Parent + **Policy and Benefits** only. You still teach the handover, the tool call and the Teams
deployment. You lose the cross-tree crossing, which is the best discussion in the lab — so if you
cut, cut Screening and Interview and keep Onboarding.
