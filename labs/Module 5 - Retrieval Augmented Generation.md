# Module 5: Retrieval Augmented Generation

> **Read this before Labs 15 and 16.** ~15 minutes.

By the end of this reading you will be able to:

- Explain why retrieval beats a bigger prompt
- Describe the two phases of a RAG pipeline and define **chunk**, **embedding**, **similarity**
  and **top_k**
- Compare built-in Copilot Studio knowledge with an external vector store, and justify a choice
- Probe a grounded agent for invention, and recognise why a wrong answer raises no error

---

## 1. Why retrieval, rather than a bigger prompt

You could paste all 20 brochures into the agent's instructions. For 20 short brochures that
would even work. Then the academy adds 40 more.

| Everything in the prompt | Retrieve, then generate |
|---|---|
| The instruction exceeds what the model can read | Find the two or three brochures that resemble the question |
| It starts ignoring the middle | Give the model only those |
| Every question costs the price of 60 brochures | The agent never sees the other 17 |
| A fee change means editing the prompt | It answers from what matters |

**RAG** — Retrieval Augmented Generation — turns the problem around. Instead of giving the model
everything and hoping it finds the answer, you *retrieve* what is relevant and give it only that.

**Retrieval decides whether the generation can possibly be right.** If the right brochure is not
in the three that came back, no amount of prompt engineering will recover the answer.

---

## 2. The pipeline, and the four words that matter

**Ingestion — done once:**

```
Documents ──▶ chunk ──▶ embed ──▶ store as vectors
```

**Retrieval — on every question:**

```
Question ──▶ embed ──▶ nearest top_k ──▶ into the prompt ──▶ answer
```

| Term | What it means | In Lab 16 |
|---|---|---|
| **Chunk** | How a document is split | One brochure = one record |
| **Embedding** | Text as a list of numbers | `llama-text-embed-v2`, 1024 dimensions |
| **Similarity** | Nearness of two vectors — the machine's idea of "related" | Cosine distance in Pinecone |
| **top_k** | How many documents come back | 3 |

The question is embedded with the **same model** used at ingestion. Mixing models — or changing
the dimension — makes every distance meaningless, and the symptom is not an error: it is
plausible answers that are subtly wrong. Pinecone's *integrated embedding* removes that whole
class of fault by keeping the model inside the index.

---

## 3. Built-in knowledge or your own vector store

You met built-in knowledge three times already: Lab 5's HR handbook, Lab 7's brochures on an
*agent*, and Lab 13's FAQ on an *Agent node*. In all three, **RAG is not a node**. Attach a
knowledge source and retrieval happens *inside* the agent: the product does the chunking,
embedding, indexing and searching. That convenience is genuinely valuable, and it has a price.

| | Lab 15 — built-in | Lab 16 — Pinecone |
|---|---|---|
| Nodes | 3 | 5 |
| Ingestion | Upload to SharePoint | A Python script, run once |
| Embedding model | Hidden | `llama-text-embed-v2`, 1024 |
| Chunking | Hidden | One brochure = one record — **your call** |
| `top_k` | Hidden | 3 — **your call** |
| Citation markers | Leak into the reply | None |
| A changed fee | Edit, wait for re-crawl | Edit, then **re-ingest** |
| What you can inspect when it answers badly | Nothing — rewrite the prompt and hope | The Compose node's Outputs show exactly which brochures came back |

**Neither is the right answer.** Which one is right depends on whether the person maintaining it
will ever need those levers — and that is a staffing question, not a technical one.

> **Build order.** Lab 15 first, then Lab 16. Build the easy one, get a working chatbot, then
> discover what it hid from you.

Two wording traps that follow from the architecture: a built-in source needs the instruction to
say **"search your knowledge source"**, while the Pinecone flow says **"using only the brochures
provided below"** — because a Compose node injects them. Swap the two and the agent is told its
only permitted source is empty, so it returns **nothing at all**, not even a refusal, on a green
run. And a built-in source appends **citation markers** the model did not write; only an explicit
instruction line suppresses them.

---

## 4. Probing for invention

A grounded agent still invents. You find out by asking for things that do not exist.

| Probe | Ask | It must |
|---|---|---|
| **A course you do not run** | *"Do you offer a Vietnamese pho course?"* | Say it does not — not improvise a syllabus |
| **A fact in no brochure** | *"Who teaches the macaron class?"* | Say the brochures do not cover it |
| **A discount that does not exist** | *"Can I get the 40% alumni discount?"* | Not confirm a premise to be helpful |

> ### A confident wrong answer raises no error
>
> The run is green. The reply is fluent. Nothing in Activity is red. In every lab here the wrong
> answer looks exactly like a right one — which is why the test tables include the probes they do.

An empty or wrong reply is almost never a broken node. It is an instruction whose premise is
wrong, a knowledge source still indexing, or a chip pointing at a deleted action.

---

**Next:** [Lab 15 — RAG with Knowledge Base](Lab%2015%20-%20RAG%20with%20Knowledge%20Base/index.md)
