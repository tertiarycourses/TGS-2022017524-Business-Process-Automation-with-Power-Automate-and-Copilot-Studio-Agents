# Module 1: Business Process Automation and Power Automate

> **Read this before Labs 0, 1 and 2.** It explains the "why" behind everything you build on
> Day 1. ~20 minutes.

By the end of this reading you will be able to:

- Explain what business process automation actually removes from a process
- Place Copilot Studio, Power Automate, Dataverse and connectors on the Power Platform map,
  and say why the **environment** matters more than any of them
- Name the four parts of every workflow, the **four trigger families** and the node types in the
  Copilot Studio workflow designer
- Explain why a dynamic value must be *inserted*, never typed
- Read the **Activity** tab and tell the difference between the three states that look alike

---

## 1. What automation actually removes

A **business process** is a repeatable series of steps that gets work done. You already run
dozens by hand every week:

> *A customer submits an enquiry → someone reads it → they re-type it into a spreadsheet →
> someone remembers to reply.*

Business process automation is not "software that does the work faster". It is the removal of
the **hand-off** — the point where a person re-types what another system already knows. That
hand-off is where the delay, the typo and the forgotten reply all live.

| | Manual | Automated |
|---|---|---|
| Steps | Form filled in → someone reads it → re-typed into Excel → someone remembers to reply | Form submitted → workflow triggered → row written → reply sent |
| Consistency | Depends who is on duty | The same every time, including at 3am |
| Record | Whatever someone remembered to write down | A run history anyone can read a year later |
| People | Doing the copying | Doing the judgement calls the machine cannot make |

The best candidates for automation are **repetitive**, **rule-based** and **time-consuming**.

> **Rule of thumb:** if you find yourself doing the same clicking, copying and emailing over and
> over, it is probably a process waiting to be automated.

---

## 2. The Power Platform, and the environment that holds it

| Part | What it does | Where you meet it |
|---|---|---|
| **Copilot Studio** | The designer for **workflows** (Labs 1–4, 10, 12–16) and **agents** (Labs 5–9, 11, 17) — in the *New experience*, one place for both | Every lab |
| **Power Automate** | The connector engine that runs underneath every workflow: connections, triggers, actions, run history. You never open it directly in this course | Underneath Labs 1–4 and 10–16 |
| **Dataverse** | The managed data store behind the environment | Lab 0 |
| **Connectors** | Forms, Outlook, Excel, SharePoint, Teams, Approvals, HTTP — over 1,000 of them | Every lab |

**The environment is the container.** Workflows, agents, connections and data all live inside
one environment. This is the single most common "where did my workflow go?" in the course: it
was built in a different environment, and it simply does not appear when you switch.

In Lab 0 you switch into the **Training Class** Sandbox environment your trainer provisioned for
your class (for example **Training Class 1**), with Dataverse enabled. It is a **Sandbox** rather
than a Developer environment for one specific reason: a Developer environment belongs to a single
user, so a whole class cannot share one. A Sandbox supports multiple users and can be **reset**
between cohorts, which is what makes it disposable — you cannot damage anything that matters.

The trainer's finished reference builds do not live there. They sit in a separate **master
reference Sandbox**, named after the course code, where they are read-only for you: open them to
compare, and build your own copies in your class environment.

One thing the environment must have, whatever its type: **Copilot Credits**. From Lab 4 onwards
every workflow that contains an **Agent** or **Classify** node consumes credits on each run, and
an environment with none allocated fails with `InsufficientMcsCredits` — an environment capacity
error, not a workflow error. Assigning yourself a Copilot Studio *licence* does not fix it:
licences are per-user, credits are per-environment. Your trainer allocates them before class.

---

## 3. Every workflow is the same four parts

```
TRIGGER  ──▶  ACTION  ──▶  ACTION  ──▶  OUTPUT
what starts it  do the work  do more work  notify or return
```

Every workflow in every lab is this shape. Only the trigger and the actions change.

- **One trigger.** The **Start** node holds it. Change the trigger and you have a different
  workflow — even when the actions do not change at all.
- **Actions are ordered.** Each node runs after the one before it, and can read the outputs of
  every node before it.
- **Dynamic content.** Those earlier outputs are inserted as *tokens*, not typed. A typed value
  is a constant that will be wrong tomorrow.

---

## 4. The designer you build in

Copilot Studio → **Workflows** → **New workflow** opens a canvas with a **Start** node. Around it:

| Part | What it does |
|---|---|
| **Start** node | Its **Trigger type** defaults to *Manual*; click it to choose a **Connector** trigger (Forms *When a new response is submitted*, Outlook *When a new email arrives (V3)*), an **HTTP request**, a **Recurrence**, or **When an agent calls the flow** |
| **Add** panel (left) | Node types: **Agent, Classify, Copilot, Human review, Connector, Function, Variable, If/Else, Loop, Note** |
| **Connector** | Every business action — Forms *Get response details*, Outlook *Send an email (V2)*, Excel *Add a row into a table*, Approvals *Start and wait for an approval*, SharePoint *Get items*, HTTP |
| **Function → Data Operations → Compose** | A named value holder: normalise an input, build a prompt, keep a reference |
| **Agent · Classify · Copilot · Human review** | The nodes that make a workflow *agentic* — Module 2 and Module 4 |
| **Build \| Activity \| Monitor** tabs | Build is the canvas; **Activity** lists every run with per-node **Run details** |
| **Save · Publish** | Save keeps a draft; **Publish** is what makes a trigger live |

---

## 5. Triggers — what is allowed to start a process

Four families. The one you choose is a statement about who or what may start the process.

| Family | It fires when… | Examples |
|---|---|---|
| **Manual** | A person presses Run | The Start node's default |
| **Scheduled** | A clock reaches a time | Recurrence — **set the time zone** or it runs on UTC |
| **Automated** | An event happens in a system | New form response; new email; new SharePoint item |
| **Request** | Something calls in from outside | HTTP request received; **When an agent calls the flow** |

The triggers you actually use in this course:

| Trigger | Where | What it means |
|---|---|---|
| Automated — *When a new response is submitted* (Forms) | Labs 1, 2, 3 | A business event starts the process |
| Automated — *When a new email arrives (V3)* (Outlook) | Lab 4 | Every email becomes a run |
| Request — *When an agent calls the flow* | Labs 6, 11 | A conversation decides to call a tool |
| Request — *When a HTTP request is received* | Labs 12–16 | A website posts JSON and waits for JSON back |
| Manual | Lab 10 | A person starts it deliberately |

---

## 6. Actions — the six families

An action either moves data, decides something, waits for a person, or calls something outside
the workflow.

| Family | Examples | Why you reach for it |
|---|---|---|
| **Data** | Compose · Variable · expressions (`utcNow()`, `concat()`, `toUpper(trim())`) | Shape and normalise values before anything trusts them |
| **Connector** | Send an email (Outlook) · Add a row (Excel) · Get items (SharePoint) · Create event | Do the real work in a business system |
| **Control** | If/Else · Classify · Loop | Decide which path the run takes |
| **Human** | Start and wait for an approval (Approvals) · **Human review** | Suspend the run until a person responds |
| **Integration** | HTTP · Response · Respond to the agent | Reach outside the platform, or answer the caller |
| **Agent** | Agent node · Copilot node · structured output | Let the model decide, inside a workflow that does not |

You will use every one of these families by the end of Lab 16.

---

## 7. Dynamic content — the token, not the text

```
Trigger runs ──▶ Outputs exist ──▶ A later node references them ──▶ Value arrives at run time
```

| ✓ Inserted with the ⚡ picker | ✗ Typed by hand |
|---|---|
| Renders as a coloured token | Stays dead text |
| Resolves at run time to what the earlier node actually produced | The run goes **green** and the value arrives **empty** |

**A reference to nothing resolves to empty, not to an error.** This costs more class time than
any other single mistake, and it is the strongest thread across every lab in this course. Two
fields are especially sharp: the **Instructions** box of an Agent or Classify node (a rich-text
editor that escapes pasted expressions) and the Outlook **To** field (a typed expression arrives
with a trailing newline and is rejected). In both, the ⚡ picker is the only reliable route.

---

## 8. Activity — the only honest account

Every lab is verified from the **Activity** tab, not from the fact that a workflow "ran".

1. **Open the run** — the workflow → **Activity** → the newest run.
2. **Read each node** — select it and open **Run details** to see its inputs and outputs: what it was given, what it produced.
3. **Find the empty one** — a wrong answer usually traces to a node whose input was blank, not to a red error.
4. **Fix the reference** — re-insert the token with the picker, **Publish**, and run **one** test.

> **One change per publish-and-test cycle.** Two simultaneous edits make a failure uninterpretable.

**Three states that look alike:** *Succeeded with the right data* · *Succeeded with empty data* ·
*Still Running because it is waiting for a person.* Only the first is done. The second is the
dangerous one — it looks exactly like success. And a workflow only listens for its trigger once
it is **Published**: a saved draft never fires, and an edit that was not republished is not live.

---

## 9. Order matters — commit before you confirm

The order of two nodes is a business decision, not a technical one.

| Log, then confirm ✓ | Confirm, then log ✗ |
|---|---|
| Write the row → send the email | Send the email → write the row |
| If the email fails, the enquiry is still on the register and someone can chase it | If the row fails, you have promised a customer a reply that nobody can see |

**Commit the record of the obligation before you create the obligation.** That is Lab 2 in one
sentence.

---

**Next:** [Lab 0 — Environment Setup](Lab%200%20-%20Environment%20Setup/index.md)
