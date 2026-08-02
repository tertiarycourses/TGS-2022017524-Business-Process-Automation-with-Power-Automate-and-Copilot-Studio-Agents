# Module 1: Business Process Automation and Power Automate

> **Read this before Labs 0, 1 and 2.** It explains the "why" behind everything you build on
> Day 1. ~20 minutes. Deck slides 12–20.

By the end of this reading you will be able to:

- Explain what business process automation actually removes from a process
- Place Power Automate, Copilot Studio, Dataverse and connectors on the Power Platform map,
  and say why the **environment** matters more than any of them
- Name the four parts of every flow, the **four trigger families** and the **six action families**
- Explain why a dynamic value must be *inserted*, never typed
- Read a run history and tell the difference between the three states that look alike

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
| Steps | Form filled in → someone reads it → re-typed into Excel → someone remembers to reply | Form submitted → flow triggered → row written → reply sent |
| Consistency | Depends who is on duty | The same every time, including at 3am |
| Record | Whatever someone remembered to write down | A run history anyone can read a year later |
| People | Doing the copying | Doing the judgement calls the machine cannot make |

The best candidates for automation are **repetitive**, **rule-based** and **time-consuming**.

> **Rule of thumb:** if you find yourself doing the same clicking, copying and emailing over and
> over, it is probably a process waiting to be automated.

---

## 2. The Power Platform, and the environment that holds it

| Part | What it does | Where you use it |
|---|---|---|
| **Power Automate** | Workflows — triggers and actions that run without a person | Labs 1–3 |
| **Copilot Studio** | Conversational agents with instructions, knowledge and tools | Labs 4–10 |
| **Dataverse** | The managed data store behind the environment | Lab 0 |
| **Connectors** | Outlook, Excel, SharePoint, Teams, Forms, HTTP — over 1,000 of them | Every lab |

**The environment is the container.** Flows, agents and data all live inside one environment.
Power Automate and Copilot Studio must be pointed at the **same** one, or your agent cannot see
your flow. This is the single most common "where did my flow go?" in the course.

In Lab 0 you create a **Developer** environment named **Copilot Studio Training**, with Dataverse
enabled. It is a Developer environment rather than a Sandbox for one specific reason: from Lab 6
onwards every **agent flow** consumes **Copilot Credits** on each run, and most Default and
Sandbox environments have none allocated. The flow then fails with `InsufficientMcsCredits` —
which is an environment capacity error, not a flow error. Assigning yourself a Copilot Studio
*licence* does not fix it: licences are per-user, credits are per-environment.

---

## 3. Every flow is the same four parts

```
TRIGGER  ──▶  ACTION  ──▶  ACTION  ──▶  OUTPUT
what starts it  do the work  do more work  notify or return
```

Every flow in every lab is this shape. Only the trigger and the actions change.

- **One trigger.** A flow has exactly one. Change the trigger and you have a different flow —
  even when the actions do not change at all.
- **Actions are ordered.** Each action runs after the one above it, and can read the outputs of
  every step before it.
- **Dynamic content.** Those earlier outputs are inserted as *tokens*, not typed. A typed value
  is a constant that will be wrong tomorrow.

---

## 4. Triggers — what is allowed to start a process

Four families. The one you choose is a statement about who or what may start the process.

| Family | It fires when… | Examples |
|---|---|---|
| **Manual** | A person presses Run | Instant cloud flow; a button in the mobile app or Teams |
| **Scheduled** | A clock reaches a time | Recurrence — **set the time zone** or it runs on UTC |
| **Automated** | An event happens in a system | New form response; new email; new SharePoint item; new file |
| **Request** | Something calls in from outside | HTTP request received; **When an agent calls the workflow** |

The triggers you actually use in this course:

| Trigger | Where | What it means |
|---|---|---|
| Automated — *When a new response is submitted* | Labs 1, 2, 3 | A business event starts the process |
| Request — *When an HTTP request is received* | Labs 6, 7, 8, 10 | A website posts JSON and waits for JSON back |
| Request — *When an agent calls the workflow* | Labs 4, 6 | A conversation decides to call a tool |
| Scheduled / Manual | Reference | A clock, or a person, starts it deliberately |

---

## 5. Actions — the six families

An action either moves data, decides something, waits for a person, or calls something outside
the flow.

| Family | Examples | Why you reach for it |
|---|---|---|
| **Data** | Compose · Parse JSON · Initialize variable · Select · Filter array | Shape and normalise values before anything trusts them |
| **Connector** | Send an email (Outlook) · Add a row (Excel) · Create item (SharePoint) | Do the real work in a business system |
| **Control** | Condition · Switch · Apply to each · Scope · Terminate | Decide which path the run takes |
| **Human** | Start and wait for an approval · Human review (agent flows) | Suspend the run until a person responds |
| **Integration** | HTTP · Response · Invoke another flow · Run a prompt (AI Builder) | Reach outside the Power Platform, or answer the caller |
| **Agent** | Agent node · Respond to the agent · structured output | Let the model decide, inside a flow that does not |

You will use every one of these families by the end of Lab 10.

---

## 6. Dynamic content — the token, not the text

```
Trigger runs ──▶ Outputs exist ──▶ A later action references them ──▶ Value arrives at run time
```

| ✓ Inserted with the ⚡ picker | ✗ Typed by hand |
|---|---|
| Renders as a coloured token | Stays dead text |
| Resolves at run time to what the earlier step actually produced | The flow runs **green** and the value arrives **empty** |

**A reference to nothing resolves to empty, not to an error.** This costs more class time than
any other single mistake, and it is the strongest thread across every lab in this course.

---

## 7. Run history — the only honest account

Every lab is verified from the run history, not from the fact that a flow "ran".

1. **Open the run** — My flows → the flow → Run history; or the **Activity** tab in an agent flow.
2. **Read each step** — expand it to see its inputs and outputs: what it was given, what it produced.
3. **Find the empty one** — a wrong answer usually traces to a step whose input was blank, not to a red error.
4. **Fix the reference** — re-insert the token with the picker, republish, and run **one** test.

> **One change per publish-and-test cycle.** Two simultaneous edits make a failure uninterpretable.

**Three states that look alike:** *Succeeded with the right data* · *Succeeded with empty data* ·
*Still Running because it is waiting for a person.* Only the first is done. The second is the
dangerous one — it looks exactly like success.

---

## 8. Order matters — commit before you confirm

The order of two actions is a business decision, not a technical one.

| Log, then confirm ✓ | Confirm, then log ✗ |
|---|---|
| Write the row → send the email | Send the email → write the row |
| If the email fails, the enquiry is still on the register and someone can chase it | If the row fails, you have promised a customer a reply that nobody can see |

**Commit the record of the obligation before you create the obligation.** That is Lab 2 in one
sentence.

---

**Next:** [Lab 0 — Environment Setup](Lab%200%20-%20Environment%20Setup/index.md)
