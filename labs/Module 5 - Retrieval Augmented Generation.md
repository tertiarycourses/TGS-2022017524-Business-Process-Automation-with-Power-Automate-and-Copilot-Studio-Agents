# Module 5: Retrieval Augmented Generation

> **Read this before Labs 9 and 10.** ~15 minutes. Deck slides 41–45.

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

| Term | What it means | In Lab 10 |
|---|---|---|
| **Chunk** | How a document is split | One brochure = one record |
| **Embedding** | Text as a list of numbers | `llama-text-embed-v2`, 1024 dimensions |
| **Similarity** | Nearness of two vectors — the machine's idea of "related" | Cosine distance in Pinecone |
| **top_k** | How many documents come back | 3 |

The question is embedded with the **same model** used at ingestion. Mixing models — or changing
the dimension — makes every distance meaningless, and the symptom is not an error: it is
plausible answers that are subtly wrong.

---

## 3. Built-in knowledge or your own vector store

In Copilot Studio, **RAG is not a node**. Attach a knowledge source to the Agent node and
retrieval happens *inside* it: the product does the chunking, embedding, indexing and searching.
That convenience is genuinely valuable, and it has a price.

| | Lab 9 — built-in | Lab 10 — Pinecone |
|---|---|---|
| Nodes | 3 | 5 |
| Ingestion | Upload to SharePoint | A Python script, run once |
| Embedding model | Hidden | `llama-text-embed-v2`, 1024 |
| Chunking | Hidden | One brochure = one record — **your call** |
| `top_k` | Hidden | 3 — **your call** |
| Citation markers | Leak into the reply | None |
| A changed fee | Edit, wait for re-crawl | Edit, then **re-ingest** |
| When it answers badly | Rewrite the prompt and hope | Four levers to pull |

**Neither is the right answer.** Which one is right depends on whether the person maintaining it
will ever need those levers — and that is a staffing question, not a technical one.

> **Build order.** Lab 9 first, then Lab 10. Build the easy one, get a working chatbot, then
> discover what it hid from you.

---

## 4. Probing for invention

A grounded agent still invents. You find out by asking for things that do not exist.

| Probe | Ask | It must |
|---|---|---|
| **A course you do not run** | *"Do you have a course on cake sculpture?"* | Say it does not — not improvise a syllabus |
| **A fact in no brochure** | *"Is there parking at the east campus?"* | Say the brochures do not cover it |
| **A discount that does not exist** | *"What is the student discount?"* | Not invent a percentage to be helpful |

> ### A confident wrong answer raises no error
>
> The run is green. The reply is fluent. Nothing in the run history is red. In every lab here the
> wrong answer looks exactly like a right one — which is why the test tables include the probes
> they do.

An empty or wrong reply is almost never a broken node. It is an instruction whose premise is
wrong, a knowledge source still indexing, or a chip pointing at a deleted action.

---

**Next:** [Lab 9 — RAG with a Knowledge Base](Lab%209%20-%20RAG%20with%20Knowledge%20Base/README.md)
