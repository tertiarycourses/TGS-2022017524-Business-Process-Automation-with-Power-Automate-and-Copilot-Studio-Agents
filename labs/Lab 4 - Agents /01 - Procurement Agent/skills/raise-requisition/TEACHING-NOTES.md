# Teaching notes — Raise a requisition

> These notes are **for the trainer**. They are deliberately kept out of `SKILL.md`, because
> everything inside `SKILL.md` is read by the model and becomes part of the agent's behaviour.
> Commentary in a skill file is not neutral — it is more instruction text competing for attention.

**Where this goes:** Agent → **Build → Skills → Add skill → Upload a skill**, then drop
[`raise-requisition.zip`](../_packages/raise-requisition.zip) onto the upload box.

A Skill is a named behaviour the agent applies when the conversation matches its description. It is
instruction text, not code, and it is *advisory* — the model decides when it applies. That is the
whole reason the threshold logic lives in the flow and not here.

---

## The paragraph worth stopping on

The last paragraph of the skill is the one to dwell on. It is a **procedural** control: the model
is asked not to help someone route around the policy. Ask the class what happens if the model
ignores it — and then point at the flow, where the audit row is written before the gate. The
procedural control can fail; the structural one cannot. Both are needed, and they are not the same
kind of thing.

## Why the description matters more than the instructions

The `description:` line in the YAML front matter is what the orchestrator reads to decide whether
this skill is relevant at all. If it never fires, the instructions never run — however good they
are. Write the description as a trigger ("use when someone…"), not as documentation of what the
skill contains.
