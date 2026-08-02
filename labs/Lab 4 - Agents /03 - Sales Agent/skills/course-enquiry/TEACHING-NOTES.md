# Teaching notes — Course enquiry

> Trainer notes. Kept out of `SKILL.md` on purpose.

**Where this goes:** `Sales Agent` → **Build → Skills → Add skill → Upload a skill**, then drop
[`course-enquiry.zip`](../_packages/course-enquiry.zip) onto the upload box.

---

## The false premise is the hard one

Most grounding failures learners expect are of the form *"invent an answer to a question with no
answer"*. Those are easy to demonstrate and reasonably easy to instruct away.

The harder failure is the **planted premise**: "Can I get the 40% alumni discount on the sushi
course?" There is no alumni discount, and a model trying to be helpful has three tempting moves —
confirm it, offer to check it, or answer the *rest* of the question and let the premise stand.

All three are failures, and the third is the one that gets missed in testing, because the reply
looks correct. "CUL-203 Japanese Sushi & Sashimi is SGD $980" is a true sentence that has silently
conceded that a 40% discount might apply to it.

This is why [`../../knowledge/pricing-rules.md`](../../knowledge/pricing-rules.md) states the
absences explicitly. The agent can only correct a premise it has been told is false.

## A note on supporting files

This skill is grounded by 20 brochures in `knowledge/brochures/`, which are uploaded as
**Knowledge**, not bundled into the skill package. A skill package *can* carry supporting files,
but knowledge belongs in the knowledge store where it is indexed and retrievable. Worth naming in
class — the package format tempts learners to put everything in one zip.
