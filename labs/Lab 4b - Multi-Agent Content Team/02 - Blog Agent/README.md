# Agent 2 — Blog Agent

**Pattern taught:** *writing from a brief — and only from the brief.* This agent has **no web
search and no brochures**. Everything it may say arrives in the research brief it is handed, which
makes the brief the single artefact worth checking.

**Build SECOND.**

## Folder contents

| Path | What it is |
|---|---|
| [`agent/instructions.md`](agent/instructions.md) | The agent's Instructions |
| [`skills/blog-writing/`](skills/blog-writing/) | The **Blog Writing** skill, as an uploadable package |

## Build steps (new designer)

1. **Create → New agent** in the **Copilot Studio Training** environment. Name it `Blog Agent`.
2. **Instructions** — paste [`agent/instructions.md`](agent/instructions.md) whole.
3. **Knowledge** — **remove "Search all websites"**, and attach nothing else. The empty Knowledge
   rail is this agent's defining feature, not an oversight.
4. **Skills → + → Upload a skill** — upload
   [`skills/_packages/blog-writing.zip`](skills/_packages/blog-writing.zip).
5. **Publish.**

## Quick test (before wiring the Manager)

Paste a research brief into Preview (run the Research Agent's quick test and copy its output),
then:

| Say | Expect |
|---|---|
| *"Write the blog post for this brief: …"* | 500–700 words, structure per the skill, every course fact traceable to section 2 of the brief |
| *"Add the course fee"* (when the brief's section 5 lists the fee as not established) | Refuses — the brief does not state it; asks for an updated brief |

## Why this agent is deliberately starved

In Lab 4 the Sales Agent was grounded by *giving* it the brochures. This agent is grounded by
*withholding* everything: no web, no documents, one input. The two produce the same discipline by
opposite means — and the second is stronger, because there is no source available for the model
to misread. When the draft contains a wrong fee, there is exactly one place it can have come
from, and exactly one artefact to fix. That is what "the boundary of agency" looks like applied
to content instead of transactions.
