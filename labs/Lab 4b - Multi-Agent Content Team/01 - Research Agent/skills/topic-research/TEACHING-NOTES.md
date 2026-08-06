# Topic Research — teaching notes (trainer only, not packaged)

**What this skill is for.** The brief's five sections are the whole governance story of the
pipeline in miniature: section 2 is the only place course facts may enter, section 3 quarantines
the web, and section 5 — *Not established* — is the one learners underrate. A writer who is told
what is *not* known does not invent it; a writer who is not told fills the silence fluently.

**Why the structure is in a skill and not the instructions.** The agent also answers ad-hoc
questions ("what does the sourdough course cost?") where a five-section brief would be absurd.
The skill fires when the task is *research*; the instructions carry only the always-true rules
(brochures for facts, web for context, refuse absent courses). This is the instructions-vs-skill
split from Module 3, live.

**The probe that matters.** Ask for the knife-throwing masterclass (probe 4 in the lab README).
The correct behaviour is defined in section 2 of the skill: brief stops, no angle, no draft
material. If the agent produces an enthusiastic section 3 and 4 anyway, the model decided the
skill's stop rule did not apply — a perfect classroom demonstration that a skill is followed,
not enforced.

**Watch the citations.** Section 2 asks for the brochure name in parentheses. If answers come
back with `[1]`-style or `[doc:...]` citation markers instead, that is the grounding layer's
marker leakage (see the course's Copilot Studio notes) — harmless in a working brief, but worth
naming so learners recognise it when it surfaces in customer-facing output.
