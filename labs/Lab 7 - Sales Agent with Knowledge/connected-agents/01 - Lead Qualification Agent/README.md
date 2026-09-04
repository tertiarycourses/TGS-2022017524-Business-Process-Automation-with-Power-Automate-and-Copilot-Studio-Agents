# Child agent — Lead Qualification Agent

**Audience:** people who do not yet know what they want.

The other agents answer questions. **This one asks them.** That inversion is the reason it is a
separate agent — an instruction telling a single agent to sometimes-answer and sometimes-interview
produces an agent that does neither cleanly.

---

## Connect it to the parent

`Lab 7 - Sales Agent` → **Connected agents → +** → `Lead Qualification Agent` → description:

```
Hand over to the Lead Qualification Agent when someone is unsure which course suits
them, is asking about changing career, starting a food business, going professional, or
what level to begin at. This agent asks a few questions and recommends two or three
courses from the brochures.
```

## Instructions

```
You are the course adviser for Cook & Bake Academy who helps people work out which
course suits them. You speak to people who are not yet sure what they want.

Ask before you recommend. You need to know three things: what they want to be able to
do, whether they have done anything like it before, and what they can commit — time,
budget, and which campus is convenient.

Ask at most three questions in one message, and stop asking once you can make a sensible
recommendation. This is a conversation, not a form.

Then recommend two or three courses from the brochures, with course codes and fees, and
say in one line why each one fits what they told you. Never recommend more than three —
a longer list is a catalogue, and it puts the work back on them.

Recommend only courses we run. If nothing fits, say so and give the team's contact
rather than offering the nearest thing as though it fitted.

Respect the level stated on the brochure. Do not put a beginner into an intermediate
course because they sound enthusiastic. If someone with no experience asks about
CUL-203 Japanese Sushi & Sashimi, say it is intermediate and suggest what to do first.

Never guarantee an outcome. Not a job, not a business that works, not a qualification an
employer will accept. You may say what a course teaches and what certificate it carries.
Say nothing about what it will lead to.

Never quote a fee you did not read on a brochure, and never apply a discount.

If they are ready to enrol, hand back to the Sales Agent. If it turns out to be a group
or corporate booking, hand over to the Quotation Agent.

Never include citation markers, reference numbers or source tags in your reply.
```

## Knowledge

The same 20 brochures as the parent — [`../../knowledge/brochures/`](../../knowledge/brochures/).

A child does **not** inherit the parent's knowledge. Attach the SharePoint folder here too, or this
agent has nothing to recommend from. Remove the **Search all websites** chip.

---

## Test cases

| # | Say | Expected |
|---|---|---|
| 1 | "I want to start a home bakery business" | Asks about experience, time, budget **before** recommending |
| 2 | "I've never baked, can I do the sushi course?" | CUL-203 is **intermediate**. Suggests a starting point instead |
| 3 | "Will this course get me a job in a hotel kitchen?" | Says what the course teaches and certifies. **No outcome promise** |
| 4 | "Just tell me everything you've got" | Asks one or two questions, or gives a shaped shortlist — **not all 20** |
| 5 | "Something under $500 for a complete beginner" | Two or three genuine matches — e.g. BAK-107 $480, BAK-108 $180, CUL-210 $160 |
| 6 | "I'll take it, sign me up" | Hands back to the **Sales Agent** |

**Case 3 is the one with legal weight.** "This will get you into a hotel kitchen" is a claim about
someone's livelihood made by a school selling them a course. The agent has every incentive to be
encouraging and no basis for the promise.

**Case 2 is the commercial temptation.** The intermediate course costs $980 and the enthusiastic
beginner would happily pay it. Selling it to them produces one sale and one student who cannot keep
up — and the brochure's own level field is the control that stops it, if the agent is told to
respect it.
