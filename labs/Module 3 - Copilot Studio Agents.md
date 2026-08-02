# Module 3: Copilot Studio Agents

> **Read this before Labs 4 and 5.** ~20 minutes. Deck slides 25–33.

By the end of this reading you will be able to:

- Say when to build a workflow and when to build an agent, and how each one fails
- Name the five parts of an agent — **instructions, skills, knowledge, tools, connected agents** —
  and state which of them the model can ignore
- Write an instruction that constrains rather than merely describes
- Explain why splitting one agent into several is a governance decision
- Publish an agent to Microsoft Teams and test it as a real user would

---

## 1. Workflow or agent — they fail differently

| Workflow — Power Automate | Agent — Copilot Studio |
|---|---|
| You decide the path in advance | It chooses the path at run time |
| The same input always gives the same output | The same input may give a different answer |
| It can only do what you built | It can combine what it was given in new ways |
| It fails **loudly**, at a named step | It fails **quietly**, with a confident wrong answer |
| You test it by checking the result | You test it by trying to break it |

Use a workflow where the rule is known. Use an agent where the language varies. Most real
systems need both — and Labs 6–10 are all seams between the two.

---

## 2. The anatomy of an agent

```
        INSTRUCTIONS                         SKILLS
        who it is, what it must never do     named procedures for matching topics

                        THE AGENT
                        name · model · description

        KNOWLEDGE                            TOOLS
        documents it may read                flows it can call to act
```

A fifth part — **connected agents** — lets one agent hand a conversation to another with its own
knowledge and audience.

---

## 3. Which parts actually hold

This is the spine of Lab 4, and the most important table in the course.

| Part | What it is | Enforced? |
|---|---|---|
| **Instructions** | Who the agent is, always in force | **No** — probabilistic |
| **Skill** | A named procedure applied when the topic matches | **No** — the model decides it applies |
| **Knowledge** | Documents the agent may read | **Partly** — it genuinely cannot read what it was not given |
| **Tool** | A flow that acts outside the conversation | **Yes** — the flow's own logic is enforced |
| **Connected agent** | A separate agent with its own knowledge and audience | **Yes** — the knowledge boundary is real |

> **A control the model cannot reach beats a rule you asked it to follow.**

Two consequences that learners consistently miss:

- **A tool the agent does NOT have is a control.** The IT Support Agent has no `ResetPassword`,
  and that absence is the only unbreakable part of its password rules.
- **The schema beats the prompt.** A field that exists will eventually be filled. If card details
  must never reach the agent, leave the field out of the tool contract — do not ask the model
  nicely.

---

## 4. Writing instructions that constrain

Instructions are prose, but not free text. Every agent instruction in this course states four
things:

| | What it does | Example |
|---|---|---|
| **Identity** | One role, in one line | *"You are an HR policy information assistant."* |
| **Source rule** | Where facts may come from | *"Answer using only the approved SharePoint HR policy source."* |
| **Refusals** | Stated as prohibitions, not preferences | *"Do not expose, request or infer personal employee records."* |
| **Escalation** | Where the conversation ends when it cannot continue | *"When the source is insufficient, say so and direct the user to HR."* |

> ### Never paste `@{...}` into an Instructions box
>
> It is a **rich-text editor**: it escapes underscores in node names, and a reference to a node
> that does not exist **resolves to empty rather than erroring**. The run goes green and the
> agent assesses a blank input. Build the prose with gaps and insert every value with the
> **⚡ picker**.

---

## 5. Knowledge — giving facts and removing sources

```
Documents in SharePoint ──▶ attached as a knowledge source ──▶ indexed ──▶ retrieved on a match
```

- **It is a boundary.** The agent genuinely cannot read a document you did not give it. This is
  the one part of an agent that comes close to enforced.
- **Turn off *Use general knowledge*.** Otherwise the model answers from what it learned in
  training, and you cannot tell which answers those were.
- **Remove the "Search all websites" chip.** It is on by default, and it makes a fee from the
  open web indistinguishable from a fee in your own brochure.

Grounding is not only about giving the agent facts. It is about taking away every other source
of them.

---

## 6. Tools — where the agent stops and the flow starts

```
User asks ──▶ agent decides a tool applies ──▶ the flow runs (deterministic) ──▶ result returns
```

| The agent's part | The flow's part |
|---|---|
| Decides a tool is relevant and fills its inputs from what the person said | Validates, looks up, applies the threshold, writes the audit row, notifies the approver |
| **Probabilistic** — it may call the wrong tool, or the right one with the wrong values | **Enforced** — whatever the agent believed, the flow's own logic still runs |

The **tool description** is how the agent knows when to call it. Write it for the model, not for
a developer.

---

## 7. Multiple agents — a split is a governance decision

One agent that knows everything has no boundaries. Splitting is how you give it some.

```
                     HR AGENT  (the parent)
        ┌──────────────┬──────────────┬──────────────┐
   Policy &          Leave       Onboarding       Payroll
   Benefits
```

- **Knowledge is separated.** Each child reads only its own documents. That boundary is real.
- **Conversation is not.** What the employee said still flows across. Privacy is not automatic.
- **A split is governance.** You are deciding who may know what — not tidying a large prompt.

A useful test: the HR Onboarding Agent and the IT Asset Agent both end at the same procurement
approval gate, from different trees, neither aware of the other. *Who is watching that queue?*

---

## 8. Publishing to Teams

```
Build and save ──▶ test in Preview ──▶ Publish ──▶ add a channel ──▶ users reach it in Teams
```

- **Preview is not published.** Changes are invisible to Teams users until you publish again.
  A stale answer in Teams almost always means an unpublished edit.
- **One change per cycle.** Each publish-and-test cycle costs a publish plus roughly 25 seconds.
- **Test as the user.** Open it from Teams with the account a real user would have — not from
  the maker's Preview pane.

---

**Next:** [Lab 4 — Copilot Studio Agents](Lab%204%20-%20Agents%20/README.md)
