# Agent 3 — Sales Agent

**Business:** Cook & Bake Academy, a cooking and bakery school in Singapore — the same business as
[Lab 9](../../Lab%209%20-%20RAG%20with%20Knowledge%20Base/). The 20 course brochures are the agent's
knowledge.

**Pattern taught:** *grounding, and the discipline of not selling.* This is the only agent in Lab 4
that talks to **people outside the company**, and the only one whose failure mode is a customer
acting on an invented fee.

**Build time:** 50–60 minutes.

> **Why this agent uses a different company.** Procurement, HR and IT Support all serve Keppel Ridge
> staff. Sales serves *customers*, and reusing Lab 9's brochures gives you 20 real documents with
> real fees, codes and dates — enough for retrieval to actually be tested. An agent grounded in three
> made-up products cannot demonstrate the failure this lab is about.

---

## Folder contents

| Path | What it is |
|---|---|
| [`agent/instructions.md`](agent/instructions.md) | Parent agent Instructions |
| [`skills/`](skills/) | Two Skills — course enquiry, and enrolment intake |
| [`tools/tool-descriptions.md`](tools/tool-descriptions.md) | `CheckCourseAvailability`, `CreateEnrolmentEnquiry` |
| [`knowledge/brochures/`](knowledge/brochures/) | **The 20 course brochures**, copied from Lab 9 |
| [`knowledge/pricing-rules.md`](knowledge/pricing-rules.md) | Discounts — what exists and what does not |
| [`connected-agents/`](connected-agents/) | Three children |

### The three children

| # | Agent | Owns |
|---|---|---|
| 1 | [Lead Qualification Agent](connected-agents/01%20-%20Lead%20Qualification%20Agent/) | Working out what a caller actually needs |
| 2 | [Quotation Agent](connected-agents/02%20-%20Quotation%20Agent/) | Group and corporate quotes — the one with a human gate |
| 3 | [Account Health Agent](connected-agents/03%20-%20Account%20Health%20Agent/) | Existing corporate clients, renewals |

---

## Uploading the brochures

**SharePoint → a folder named `Course Brochures` → upload all 20 `.txt` files**, then attach the
folder as **Knowledge** on the Sales Agent and the Lead Qualification Agent.

| Do | Don't |
|---|---|
| Upload all 20 | Upload a subset — TC7-style probes stop working |
| Attach the **folder** | Attach files one at a time |
| Confirm the Copilot Studio account has read access | Grant anonymous access |

> ⚠️ **A Knowledge source appends citation markers the model did not write.** On a live tenant every
> reply came back **twice** — once with `[doc:turn1doc11]`-style markers and again with `[1]`-style
> ones, both reaching the customer verbatim. Telling the agent "never mention documents" does not
> suppress them; they are added by the grounding layer. The instruction file carries the explicit
> line that does:
>
> ```
> Never include citation markers, reference numbers or source tags in your reply.
> ```

> ⚠️ **Remove the "Search all websites" chip.** On a sales agent this is not a tidiness point. With
> web search on, a question about a course we do not run gets answered from somebody else's website
> — in the same confident voice used for our own fees. The customer cannot tell the two apart.

---

## The 20 courses

| Bakery | | Cooking | |
|---|---|---|---|
| BAK-101 Artisan Sourdough | $680 | CUL-201 Italian Cuisine Mastery | $1180 |
| BAK-102 French Pastry & Viennoiserie | $1480 | CUL-202 Thai Street Food | $540 |
| BAK-103 Wedding Cake Design | $1280 | CUL-203 Japanese Sushi & Sashimi | $980 |
| BAK-104 Macaron Masterclass | $420 | CUL-204 French Culinary Foundations | $1580 |
| BAK-105 Chocolate & Confectionery | $760 | CUL-205 Chinese Wok Cooking | $520 |
| BAK-106 Cupcake & Cake Pops | $220 | CUL-206 Indian Curry & Spices | $500 |
| BAK-107 Bread Making Fundamentals | $480 | CUL-207 Healthy Meal Prep | $360 |
| BAK-108 Cookie & Biscuit Baking | $180 | CUL-208 Vegetarian & Vegan | $540 |
| BAK-109 Pie & Tart Specialist | $560 | CUL-209 Grilling & BBQ Mastery | $460 |
| BAK-110 Korean & Asian Bakery | $720 | CUL-210 Knife Skills & Kitchen Essentials | $160 |

All fees SGD, inclusive of GST. The only discount that exists is **10% early-bird** for sign-ups
4 weeks before intake — see [`knowledge/pricing-rules.md`](knowledge/pricing-rules.md).

---

## What makes this agent different from the other three

**It talks to people who do not work here.** Procurement's worst case is an internal requisition
routed wrongly, and someone notices. Sales' worst case is a member of the public enrolling on the
strength of a fee the agent invented — and *they* find out at the point of payment.

**Every number it says is checkable.** A customer told "$680" can hold the agent to it. That is why
the instructions forbid quoting a fee that is not in a brochure, and why the pricing rules file
exists to state plainly which discounts do **not** exist.

**A confident wrong answer is worse than a refusal here.** "I don't have that — the team can help on
+65 6888 1234" costs the academy a moment. An invented Vietnamese cooking course costs it a customer
who turns up expecting one.
