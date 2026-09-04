# Agent node — Instructions (Lab 16 — Pinecone)

The retrieval half of this lab happens **before** the Agent node: the HTTP node
queries Pinecone and the Compose node pastes the three nearest brochures into a
single block of text. The agent's only job is to answer from that block.

The companion build, [Lab 15](../Lab 15 - RAG with Knowledge Base/),
uses a different instruction — the agent searches a knowledge source itself
rather than being handed the text.

---

## The instruction

Paste into the **Agent** node's **Instructions** box.

---

You are the customer care assistant for Cook & Bake Academy, a cooking and bakery school in Singapore.

Answer the customer's question using only the course brochures provided below. They are the only knowledge you have.

If the brochures do not answer the question, say "I don't have that in our course information" and offer the team on +65 6888 1234 or enrol@cookbakeacademy.sg.

Never invent a fee, a date, a duration, a course code, an instructor name or a discount. If a number is not in a brochure, you do not know it.

If we do not run a course, say so plainly, then list the two or three closest courses we do run.

Always give the course code (for example BAK-101) next to the course title. Quote fees in Singapore dollars exactly as written.

Be warm and brief — two to four short sentences. Never mention brochures, searching, or that you are reading documents.

COURSE BROCHURES AND CUSTOMER QUESTION:

---

### Then add the Compose reference — with the ⚡ picker, not by pasting

The text above ends with a label and nothing after it. That is deliberate.

Put the cursor at the very end, after `COURSE BROCHURES AND CUSTOMER QUESTION:`,
then:

1. Click the **⚡** icon in the toolbar above the Instructions box
2. Find **Compose** in the dynamic content list
3. Click **Outputs**

A blue **chip** appears. That chip is the entire connection between retrieval and
generation — it carries both the customer's question and the three retrieved
brochures into the prompt.

**Do not type or paste `@{outputs('Compose')}`.** The Instructions box is a
rich-text editor. A pasted expression is stored as plain characters, and node
names with underscores get escaped (`Compose_1` → `Compose\_1`). Either way the
reference points at nothing.

**And a reference to nothing resolves to empty rather than erroring.** The node
stays green, the run succeeds, and the agent silently receives no question and no
brochures.

The symptom, if you get it wrong: the agent replies *"It looks like the course
brochures weren't included in your message, and no customer question came through
either."* It is telling you exactly what is wrong — check
**Agent → Run Details → Outputs**.

---

---

## The trap: copying one flow to make the other

Lab 15 was built by duplicating Lab 16. The Instructions came across verbatim,
including Lab 16's final line:

```
COURSE BROCHURES AND CUSTOMER QUESTION:{outputs('builtinFunction-d20387b9-…')}
```

That `builtinFunction-…` is Lab 16's Compose node, which does not exist in Lab 15. The
canvas showed `This input references action "builtinFunction-d2…", which is not
on the canvas` — and **the flow still ran green, returning `{ "reply": "" }` in
~25 seconds.**

The agent was told its only permitted source was "the brochures provided below",
and nothing was below. So it produced **nothing at all** — not even the refusal
sentence the instruction defines.

> **An empty string, rather than a refusal, means the instruction premise is
> wrong.** Not the knowledge source, not the Response node. Check the last
> paragraph of Instructions first.

**After duplicating a flow, re-read the last paragraph of the Agent's
Instructions before anything else.**

---

## The four lines that do the real work

- *Answer from the course brochures — and only those.*
- *If the brochures do not answer the question, say "I don't have that in our course information."*
- *Never invent a fee, a date, a duration, a course code, an instructor name or a discount.*
- *If we do not run a course, say so plainly, then list the closest ones we do.*

That third line is the point of RAG in a customer-facing setting. A language
model asked *"how much is the sourdough course?"* with no grounding will produce
a number. It will be a plausible number. It will be wrong, and the customer will
quote it back to you.

The fourth line is what turns a weak retrieval match into an honest refusal.
Vector search **always** returns something — ask about a course the academy does
not run and it will still hand back the three nearest brochures. Without that
line, the model sees three Thai and vegetarian brochures and a question about
pho, and helpfully splits the difference.

---

## Settings on this node

| Setting | Value | Why |
|---|---|---|
| **Web search** | **Off** | On, the agent can pull course fees off the open web — the exact uncontrolled-source risk this lab exists to prevent. |
| **Request human assistance** | **Off** | Not used in this lab. |
| **Output** | **Text response** | The Response node reads `Agent Response`. |

> **There is no *Use general knowledge* toggle here, and no temperature control.**
> Those belong to a Copilot Studio **agent**, not to a workflow **Agent node**.
> In this flow, grounding rests entirely on the instruction wording above —
> which is weaker than a platform switch that makes ungrounded answers
> impossible. Worth raising in the debrief.

> **There is no user-message or input field either.** The Configure tab ends at
> **Output**. Instructions is the only place per-call data can go — which is why
> both versions above end with a ⚡ chip.
