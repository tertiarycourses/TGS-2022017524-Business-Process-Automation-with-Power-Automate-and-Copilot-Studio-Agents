# Agent 3 — Review Agent

**Pattern taught:** *a reviewer that did not write the draft.* A model reviewing its own words
agrees with itself; a separate agent, holding a checklist and the brief, has something to push
against. Its verdict then travels with the draft to the human — it recommends, it does not
approve.

**Build THIRD.**

## Folder contents

| Path | What it is |
|---|---|
| [`agent/instructions.md`](agent/instructions.md) | The agent's Instructions |
| [`skills/editorial-review/`](skills/editorial-review/) | The **Editorial Review** skill, as an uploadable package |

## Build steps (new designer)

1. **Create → New agent** in the **Copilot Studio Training** environment. Name it `Review Agent`.
2. **Instructions** — paste [`agent/instructions.md`](agent/instructions.md) whole.
3. **Knowledge** — **remove "Search all websites"**; attach nothing. The review compares the
   draft against the brief it is handed — the same discipline as the Blog Agent, applied to
   checking instead of writing.
4. **Skills → + → Upload a skill** — upload
   [`skills/_packages/editorial-review.zip`](skills/_packages/editorial-review.zip).
5. **Publish.**

## Quick test (before wiring the Manager)

Paste a draft *and* its brief into Preview, with one planted defect — change a fee by $50, or add
"limited time offer" to the closing:

| Say | Expect |
|---|---|
| *"Review this draft against this brief: …"* | A verdict per the skill: the planted defect found, named, and quoted — not a general "looks good" |
| The same, with a clean draft | **Recommend approval** — with the checks listed as passed, not an unconditional "approved" |

## Why the reviewer's verdict is not an approval

The skill's verdicts are *recommend approval* and *needs changes* — deliberately not *approved*.
Approval is the human's word, and this lab keeps it that way: the Review Agent's output is
evidence for the person's decision, not a substitute for it. When you later add the flow-based
Teams gate (see the lab README's extension), the vocabulary is already right: the machine
recommends, the run suspends, a person approves.
