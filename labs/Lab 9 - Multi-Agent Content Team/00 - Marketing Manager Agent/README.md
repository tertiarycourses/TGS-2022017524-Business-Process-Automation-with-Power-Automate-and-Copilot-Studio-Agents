# Agent 0 — Marketing Manager Agent

**Pattern taught:** *orchestration by delegation, ending at a human.* The Manager owns the
conversation, hands each stage to a specialist, and may not call anything final until a person
approves it.

**Build LAST** — its three children must already exist and be published.

## Build steps (new designer)

1. **Create → New agent** in your **Training Class** environment. Name it
   `Lab 9 - Marketing Manager Agent`.
2. **Instructions** — paste [`agent/instructions.md`](agent/instructions.md) whole (no tokens).
3. **Model** — leave the default, or pick the strongest available; the Manager does the routing
   and the judgement.
4. **Knowledge** — remove **Search all websites**. The Manager needs no sources of its own: facts
   arrive in the Research Agent's brief.
5. **Connected agents → +** — add `Lab 9 - Research Agent`, `Lab 9 - Blog Agent`, `Lab 9 - Review Agent`. Each must be
   **published** to appear.
6. **Memory** — leave **off** for the lab. (Extension: switch it on and see the Manager remember
   your preferred tone across sessions — then discuss whether a shared training tenant should
   remember anything.)
7. **Publish**, then test from the **Preview** tab with the [test script](../index.md#test-script).

## What to watch in the Activity map

When you run test 1, the Preview pane's activity map shows the delegation chain: the Manager's
task to the Research Agent, the brief coming back, the task to the Blog Agent, the draft, the
task to the Review Agent, the verdict. That visible chain — who was asked, with what task, what
came back — is the multi-agent equivalent of a flow's run history, and it is how you debug a
pipeline that "answered wrong": find the first handoff whose content is already wrong.

## The one rule that matters

The instructions end with the approval rule — nothing is final until the person in the
conversation approves it. That rule is **probabilistic**: it holds because the model follows it,
not because anything blocks. Probe 3 in the test script attacks exactly this rule. If your class
finds a phrasing that talks the Manager past it, that is not a failed lab — that is the lesson,
and the [flow-based gate extension](../index.md#where-the-human-review-really-is--read-this-before-teaching)
is the remedy.
