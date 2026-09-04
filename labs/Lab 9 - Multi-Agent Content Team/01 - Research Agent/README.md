# Agent 1 — Research Agent

**Pattern taught:** *research grounded in your facts, with the web for context.* This is the only
agent in the pipeline allowed to touch the web — and its skill forces it to keep web material and
brochure facts labelled apart.

**Build FIRST.**

## Folder contents

| Path | What it is |
|---|---|
| [`agent/instructions.md`](agent/instructions.md) | The agent's Instructions |
| [`skills/topic-research/`](skills/topic-research/) | The **Topic Research** skill, as an uploadable package |
| [`knowledge/`](knowledge/) | Brand voice, audience personas, campaign insights |

## Build steps (new designer)

1. **Create → New agent** in your **Training Class** environment. Name it
   `Lab 9 - Research Agent`.
2. **Instructions** — paste [`agent/instructions.md`](agent/instructions.md) whole.
3. **Knowledge → +** — upload the three files in [`knowledge/`](knowledge/), **and** the
   [20 course brochures from Lab 5's Sales Agent](../../Lab%207%20-%20Sales%20Agent%20with%20Knowledge/knowledge/brochures/)
   (or attach the same SharePoint folder you used there). Wait for every source to show
   **Ready** — an indexing source answers as if it does not exist.
4. **Knowledge** — **keep "Search all websites"** on this agent. That is deliberate, and it is
   the only agent in this lab that keeps it.
5. **Skills → + → Upload a skill** — upload
   [`skills/_packages/topic-research.zip`](skills/_packages/topic-research.zip).
6. **Publish.**

## Quick test (before wiring the Manager)

In Preview:

| Say | Expect |
|---|---|
| *"Research brief: promote the artisan sourdough course to career switchers."* | A brief with the sections the skill defines — course facts cited from the brochure, trends marked as from the web |
| *"Research brief: our knife-throwing masterclass."* | *We do not offer this* — from the brochures' absence, not an invented syllabus |

## Why this agent keeps the web

A marketing brief needs two kinds of material: **facts about our courses** (fees, dates, content
— these exist only in the brochures) and **context about the world** (what audiences search for,
seasonal angles — these live on the web). Removing web search would starve the second; letting
the web answer the first is how a wrong fee ends up in a published post. The skill's whole job is
keeping the two in separate, labelled sections so the Blog Agent — which sees only this brief —
inherits the boundary.
