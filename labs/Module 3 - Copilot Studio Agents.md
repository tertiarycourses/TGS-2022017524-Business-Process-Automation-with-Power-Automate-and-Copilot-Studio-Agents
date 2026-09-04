# Module 3: Copilot Studio Agents

> **Read this before Labs 5 to 9, 11 and 17.** ~20 minutes.

By the end of this reading you will be able to:

- Find your way around the **new experience** agent designer — where the instructions go, and
  what each item in the right panel does
- Say when to build a workflow and when to build an agent, and how each one fails
- Name the parts of an agent — **instructions, model, knowledge, tools, skills, connected
  agents** — and state which of them the model can ignore
- Write an instruction that constrains rather than merely describes
- Explain why splitting one agent into several is a governance decision
- Explain what **Publish** and **Channels +** do, and why Preview is not published

---

## 1. Workflow or agent — they fail differently

| Workflow | Agent |
|---|---|
| You decide the path in advance | It chooses the path at run time |
| The same input always gives the same output | The same input may give a different answer |
| It can only do what you built | It can combine what it was given in new ways |
| It fails **loudly**, at a named node | It fails **quietly**, with a confident wrong answer |
| You test it by checking the result | You test it by trying to break it |

Use a workflow where the rule is known. Use an agent where the language varies. Most real
systems need both — Labs 6, 10 and 11 are the seams between the two, and Labs 12–16 put an
agent *inside* a workflow.

---

## 2. The designer — where everything goes

**Agents → New agent** opens one page. Learn it once and every agent lab reads the same way.

| Where | What | What you do there |
|---|---|---|
| **Top bar** | Agent name · tabs **Build \| Preview \| Evaluate \| Monitor** · Save · Share · Settings · **Publish** | Name it; test in Preview; release with Publish |
| **Centre, Build tab** | The **name box**, and directly under it the **Instructions** box — a large rich-text box with a small toolbar | Click into the Instructions box and paste the whole `agent/instructions.md`. **This is the only place the system instructions go** — there is no separate prompt, description or settings page |
| **Right panel** | **Model** dropdown | Leave the default unless told otherwise |
| | **Channels +** | Teams, Microsoft 365 Copilot, website — Lab 17 |
| | **Skills +** | Upload a skill package (`.zip` with `SKILL.md` at the top) — Lab 8 |
| | **Tools +** | Attach a published workflow or connector action — Lab 6 |
| | **Knowledge +** | Upload files or add a SharePoint folder; **remove the *Search all websites* chip** that is there by default — Labs 5, 7 |
| | **Connected agents +** | Add other published agents it may hand over to — Lab 9 |
| | **Memory** (Preview) | Off for every lab |
| **Preview tab** | A chat pane | Reads your latest **saved draft**, as you, the maker |

---

## 3. The anatomy of an agent, and which parts actually hold

| Part | What it is | Enforced? | Lab |
|---|---|---|---|
| **Instructions** | Who the agent is, always in force | **No** — probabilistic | 5 |
| **Model** | The language model that reads them | — | 5 |
| **Knowledge** | Documents the agent may read | **Partly** — it genuinely cannot read what it was not given | 5, 7 |
| **Tool** | A workflow it can call to act | **Yes** — the workflow's own logic is enforced | 6 |
| **Skill** | A named procedure, uploaded as a package, applied when the topic matches | **No** — the model decides it applies | 8 |
| **Connected agent** | A separate agent with its own knowledge and audience | **Yes** — the knowledge boundary is real | 9 |

> **A control the model cannot reach beats a rule you asked it to follow.**

Two consequences that learners consistently miss:

- **A tool the agent does NOT have is a control.** The IT Support agent has no `ResetPassword`,
  and that absence is the only unbreakable part of its password rules.
- **The schema beats the prompt.** A field that exists will eventually be filled. If card details
  must never reach the agent, leave the field out of the tool contract — do not ask the model
  nicely.

### Tools, skills and MCP — the comparison worth memorising

| | What it is | When it fires | Enforced? | Example |
|---|---|---|---|---|
| **Tool** | An action the agent can call that acts outside the conversation — a workflow, a connector action, or a tool from an MCP server | When the agent decides its description matches | The action's own logic, yes | `Lab 6 - Raise Requisition` |
| **Skill** | Instructions on demand — a `SKILL.md` package that changes how the agent behaves on a topic | When the agent decides its `description` matches | No | `password-reset-procedure` |
| **MCP** | Model Context Protocol — a server exposing many tools over a standard interface, so an agent can be given a whole catalogue at once | Per tool, as above | Per tool | A Calendar or Mail MCP server |

---

## 4. Writing instructions that constrain

Instructions are prose, but not free text. Every agent instruction in this course states four
things:

| | What it does | Example |
|---|---|---|
| **Identity** | One role, in one line | *"You are the HR Assistant for Keppel Ridge Engineering."* |
| **Source rule** | Where facts may come from | *"Answer only from the HR Policies document in your knowledge."* |
| **Refusals** | Stated as prohibitions, not preferences | *"Never disclose one person's information to another."* |
| **Escalation** | Where the conversation ends when it cannot continue | *"Give hr@keppelridge.example and ask no follow-up questions."* |

> ### Never paste `@{...}` into an Instructions box
>
> Agent instructions in the *agent designer* carry no tokens and are safe to paste whole. The
> **Agent node inside a workflow** is different: its Instructions box is a rich-text editor that
> escapes underscores in node names, and a reference to a node that does not exist **resolves to
> empty rather than erroring**. Build the per-call data in a **Compose** node and insert one ⚡
> chip.

---

## 5. Knowledge — giving facts and removing sources

```
Files or a SharePoint folder ──▶ Knowledge + ──▶ indexed (wait for Ready) ──▶ retrieved on a match
```

- **It is a boundary.** The agent genuinely cannot read a document you did not give it.
- **Remove the "Search all websites" chip.** It is on by default, and it makes a fee from the
  open web indistinguishable from a fee in your own brochure.
- **A folder of its own.** The connector indexes at folder level; a shared library makes an HR
  agent answer from a bank's KYC policy.
- **Wait for Ready.** A source that is still indexing answers as if it does not exist.
- **Expect citation markers.** The grounding layer appends `[1]`-style markers the model did not
  write; only an explicit instruction line suppresses them.

Grounding is not only about giving the agent facts. It is about taking away every other source
of them.

---

## 6. Tools — where the agent stops and the workflow starts

```
User asks ──▶ agent decides a tool applies ──▶ the workflow runs (deterministic) ──▶ result returns
```

| The agent's part | The workflow's part |
|---|---|
| Decides a tool is relevant and fills its inputs from what the person said | Validates, writes the row, returns the reference |
| **Probabilistic** — it may call the wrong tool, or the right one with the wrong values | **Enforced** — whatever the agent believed, the workflow's own logic still runs |

A workflow is callable as a tool only when its trigger is **When an agent calls the flow** and it
is **published** in the same environment. Its inputs — with descriptions the agent reads — and
its *Respond to the agent* outputs are the contract. The **tool description** is how the agent
knows when to call it; write it for the model, not for a developer. And verify with the
workflow's **Activity**, never with the reply: a fluent "done" proves nothing.

---

## 7. Multiple agents — a split is a governance decision

One agent that knows everything has no boundaries. Splitting is how you give it some.

```
                 Lab 9 - Marketing Manager  (the parent)
        ┌──────────────────┬──────────────────┐
   Research Agent     Blog Agent        Review Agent
```

- **Knowledge is separated.** Each child reads only its own documents. That boundary is real.
- **Conversation is not.** What the person said still flows across. Privacy is not automatic.
- **A split is governance.** By *stage of work* (Lab 9) or by *who may know what* (the HR kit) —
  not tidying a large prompt.
- **Connect from the parent** (**Connected agents +**), children published first, and **deploy the
  parent only**.

---

## 8. Publishing and channels

```
Build and save ──▶ test in Preview ──▶ Publish ──▶ Channels + ──▶ users reach it
```

- **Preview is not published.** Preview reads the draft, as the maker. Every channel serves the
  **published** version, as the real user. A stale answer in Teams almost always means an
  unpublished edit.
- **Each channel needs something different** — Teams needs an availability choice (org-wide means
  admin approval of a Teams app); Microsoft 365 Copilot needs a licence on the user; a public
  website needs *No authentication*, which is exactly why an HR agent must never have one.
- **One change per cycle,** and **test as the user, in the channel** — the agent that reads the
  signed-in person's record is the one that behaves differently.

---

**Next:** [Lab 5 — Your First Agent](Lab%205%20-%20Your%20First%20Agent/index.md)
