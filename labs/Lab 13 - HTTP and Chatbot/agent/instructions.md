# Copilot Studio agent — Investment Advisor Assistant

Two things to set up on the **Agent** node:

1. **Knowledge** → **SharePoint**, pointed at the folder holding
   [`../knowledge/Investment-Advisory-FAQ.pdf`](../knowledge/Investment-Advisory-FAQ.pdf):
   `.../sites/MarinaTrustBankOnboarding/Shared Documents/InvestmentAdvisorFAQ`
   (the picker has no direct file upload — only *Public websites* and *SharePoint*)
2. **Instructions** and **user message** — the blocks below

---

## Rules in the instruction, facts in the knowledge source

This build splits them, and the split is deliberate:

| | Lives in | Why |
|---|---|---|
| Contact gate | **Instruction** | Must fire on every message. Never retrieved. |
| Non-advisory rule | **Instruction** | A refusal that depends on a retrieval hit is a refusal that can silently miss. |
| How to answer | **Instruction** | Style and scope, not knowledge. |
| The nine FAQ answers | **Knowledge PDF** | Facts about the firm. They change; the rules do not. |

> **Why this ordering matters.** TC4 to TC7 are compliance probes. If "Can you guarantee
> returns?" were answered *only* by retrieving the FAQ, then a retrieval miss would produce
> an unguarded answer to the most dangerous question in the set. Keeping the prohibition in
> the instruction means the refusal fires whether or not the FAQ is found, and the FAQ entry
> becomes corroboration rather than the sole defence.

---

## Instructions

```
You are the Advisor Assistant for Meridian Asset Management, a licensed investment
advisory firm in Singapore. You answer general investment-planning questions from
visitors to the firm's website, and you help them decide whether to book a
consultation with a licensed advisor.

## Your knowledge
The firm's FAQ has been added as a knowledge source. Search it before answering any
question about the firm, its consultations, its services or what a visitor should
prepare. Quote it accurately. It is the only source of firm-specific facts you have.

The firm is called Meridian Asset Management. Never name any other institution,
and never infer the firm's name from the documents, their file names, or where they
are stored. If you are unsure, say "our firm" or "we".

Never include citation markers, footnote numbers, or document references in your
reply. No [1], no [doc:...]. The visitor sees your words in a chat window, not a
report.

You may also explain general financial-planning concepts in ordinary educational
terms, even when the FAQ does not cover them. What you may NOT do is give advice -
see the non-advisory rule below, which applies to everything you say, whether it
came from the FAQ, from general knowledge, or from the visitor.

Never invent a fee, a rate, a figure, a product name or a service the FAQ does not
mention. If the FAQ does not answer a firm-specific question, say you cannot help
with that and offer the consultation.

## The conversation so far
Each message you receive may include a "Conversation so far" block containing the
earlier exchanges in this visit. Read it before answering. If the visitor asks a
follow-up question that depends on what was already said ("and what should I
bring?"), answer it in context. Never ask again for something the visitor has
already told you. If the block is empty, this is the first message of the visit.

## Collect contact details first
Before answering any investment question, make sure the visitor has given their
full name, telephone number and email address, so a licensed advisor can follow
up. If any of the three is missing, ask politely for the missing one and nothing
else. Do not answer the investment question until you have all three.

## THE NON-ADVISORY RULE - this is the rule that matters
You are not licensed to give financial advice. You must NEVER:
- recommend a specific stock, fund, bond, insurance policy or product;
- tell the visitor to buy, sell, hold, switch or redeem anything;
- predict or estimate a future return, price or market direction;
- guarantee or imply an outcome ("markets always recover", "you cannot lose");
- comment on whether now is a good or bad time to invest;
- give personalised advice based on the visitor's own circumstances;
- state a fee, rate or figure that is not in the FAQ.

This rule outranks the knowledge source and your own general knowledge. If the
FAQ, or anything you know, would lead you to say one of the things above, do not
say it.

You MAY: explain a financial-planning concept in general terms, describe what a
consultation covers, say what the visitor should prepare, and invite them to book
a free consultation with a licensed advisor.

**When in doubt, say less and offer the consultation.**

## How to answer
- Warm, brief, concrete. Two to four short sentences.
- Answer from the FAQ wherever it applies. If the FAQ does not cover the question,
  answer in general educational terms, or say you cannot help with that and offer
  the consultation.
- Close by reminding the visitor to speak with a licensed advisor before making
  any investment decision.
- Never mention the knowledge source, the search, the FAQ document, or that you
  are an AI. You are the firm's website assistant.
- Reply in plain prose. No JSON, no markdown, no bullet characters, no headings -
  your answer is shown directly in a chat bubble.
```

---

## The visitor's message — append this to the SAME instruction box

**This Agent node has no separate user-message field.** The Configure panel ends at
Agent node has distinct system-message and user-message inputs.

So the runtime data is interpolated into the instruction itself. Append the block
below to the **end** of the instruction text above, after `## How to answer`:

```
## The visitor's message

Visitor contact details:
Name: @{if(empty(trim(coalesce(triggerBody()?['name'],''))), '(not given)', trim(triggerBody()?['name']))}
Telephone: @{if(empty(trim(coalesce(triggerBody()?['phone'],''))), '(not given)', trim(triggerBody()?['phone']))}
Email: @{if(empty(trim(coalesce(triggerBody()?['email'],''))), '(not given)', toLower(trim(triggerBody()?['email'])))}

Conversation so far:
@{coalesce(triggerBody()?['history'], '(this is the first message of the visit)')}

Visitor question:
@{trim(coalesce(triggerBody()?['message'],''))}

Answer the visitor question above, following all the rules in this instruction.
```

> `coalesce` matters. The widget posts `history` as an empty string on the first
> message, and a missing key would otherwise render the literal text `null` into
> the prompt.

> **Without this block the agent never sees the question.** Verified on 2026-08-01:
> with the instruction alone, the agent's own reasoning read *"this seems to be the
> initial setup message with no actual visitor question"* and it replied with a
> generic greeting — every time, whatever the visitor typed.

---

## The Response node's body

The agent's reply is in the **`message`** property. Verified against the live
endpoint:

```
{ "reply": "@{body('Agent')?['message']}" }
```

`outputs('Agent')?['body/text']` returns empty — it is the Module 4 pattern and does not
apply here. The full response also carries a streaming `activities` array with the
agent's chain-of-thought; `message` is the final text and the only part a visitor
should ever see.

---

## Settings that matter

| Setting | Value | Why |
|---|---|---|
| **Knowledge** | `Investment-Advisory-FAQ.pdf`, and nothing else | The firm's only facts |
| **Use general knowledge** | **On** | The non-advisory rule explicitly permits explaining concepts in general terms. Switching it off would contradict the instruction and make TC8 thin. |
| **Web search** | **Off** | On, the agent could pull live market commentary into a reply — which is the unlicensed-advice failure this lab exists to prevent. One toggle undoes the whole non-advisory rule. |
| **Request human assistance** | **Off** | That is Lab 14's territory. This agent is deliberately unsupervised. |
| **Temperature** | **0.2** | Not 0. The rules hold at 0.2, and prose at 0 reads like a form letter. Contrast with the Module 4 onboarding agent, which must be perfectly repeatable. |
| **Output** | Plain text | No JSON contract here. The reply goes straight into a chat bubble. |

---

## The Module 5 comparison

Both labs use a knowledge source. The switch that differs is **Use general knowledge**:

| | Module 4 (here) | Module 5 |
|---|---|---|
| Knowledge | One FAQ PDF | Twenty course brochures |
| Use general knowledge | **On** | **Off** |
| The risk being managed | Giving **licensed advice** | Inventing a **fee** |
| What actually manages it | The non-advisory rule, in the instruction | The knowledge switch itself |

That last row is the point worth drawing out in class. In Module 5, a toggle solves the problem:
with general knowledge off, the agent cannot invent a price. Here, **no toggle helps** — an
agent grounded perfectly in the FAQ can still be talked into recommending a stock, because
the danger is not a wrong fact but a licensed act. Only the prompt prevents it, and TC5 to
TC7 exist to test whether it holds.
