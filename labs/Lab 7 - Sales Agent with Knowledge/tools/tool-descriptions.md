# Tools — Sales Agent

| Tool | Reads or writes | Gate |
|---|---|---|
| `CheckCourseAvailability` | Reads | None |
| `CreateEnrolmentEnquiry` | Writes | None — an enquiry is not an enrolment |

Neither tool takes payment, and neither confirms a place. Say that out loud in class: the agent
that talks to the public is the one with the **least** authority in this lab, and that is the
correct design.

---

## Tool 1 — `CheckCourseAvailability`

**Source:** agent flow `Course Intake Availability`.

```
When an agent calls the workflow   (input: courseCode, Text)
  → Get items (SharePoint, CourseIntakes)
  → Respond to the agent
```

**Filter Query** — literal text, value inserted with the **⚡ picker**:

```
CourseCode eq '<⚡ toUpper(trim(courseCode)) token>'
```

> **`toUpper(trim(...))` belongs inside the filter.** A customer types "bak-101" and the brochure
> says "BAK-101". Without normalisation the lookup returns nothing, the agent reports no intakes
> found, and **no error appears anywhere** — a green run and a wrong answer that looks right. This is
> the same failure as TC12 in the Procurement lab; name it as a recurring shape.

> ⚠️ **Do not use `concat()`** to build the filter — it validates green and fails at run time with
> *"Creating query failed"*.

**Outputs:** `found`, `nextIntake`, `seatsRemaining`, `status` (`Open` / `Waitlist` / `Closed`).

**Description:**

```
Check when a course next runs and whether places are available. Call this when someone
asks when a course starts, whether there are seats left, or whether they can still join
an intake. Pass the course code, for example BAK-101. Returns the next intake date, the
seats remaining and whether the intake is open, waitlisted or closed.
```

> **`seatsRemaining` is the dangerous field.** An agent that reads "3" will want to say "hurry, only
> 3 left". Add to the agent's instructions:
>
> ```
> Never use the number of seats remaining to create urgency. Report whether an intake is
> open, waitlisted or closed. A customer must not be pressured by a number that may be
> stale by the time they act on it.
> ```
>
> Two reasons, and give both. The figure is a **cache** — it was true when the flow ran and a phone
> enrolment can change it a minute later. And manufactured scarcity aimed at a member of the public
> is a sales practice the academy has to defend. The agent has no idea it is doing either.

---

## Tool 2 — `CreateEnrolmentEnquiry`

**Source:** agent flow `Enrolment Enquiry Intake`.

```
When an agent calls the workflow
   (inputs: name, contact, courseCode, preferredIntake, notes)
  → Create item (SharePoint, EnrolmentEnquiries)
  → Send an email (Outlook) to the enrolment team
  → Respond to the agent      ← returns the enquiry reference
```

**Description:**

```
Record an enrolment enquiry for the team to follow up. Call this when someone wants to
enrol, wants a place on a course, or asks to be contacted. Collect their name, an email
or phone number, the course code and their preferred intake first. Returns a reference
number. This records an enquiry only — it does not enrol anyone, does not reserve a
place and does not take payment.
```

> **The last sentence is doing real work.** Without it the agent infers from the tool's *name* that
> calling it enrols someone, and reports accordingly. Describe what a tool does **not** do whenever
> the obvious reading is wrong — the description is a prompt, and the model has nothing else to go
> on.

> ⚠️ **Insert the recipient with the ⚡ picker.** A typed expression in the Outlook `To` field fails
> with `OpenApiOperationParameterTypeConversionFailed` and a trailing-`\n` — typing an expression
> into that control is what creates the newline, so no amount of `trim()` fixes it.

**Do not add a `payment` field to this tool.** If a learner asks why not: a field that exists will
eventually be filled, and the moment the contract can carry card details, the instruction telling
the agent not to collect them is the only thing standing between a customer and a card number in a
Teams transcript. **The safest place to stop a data flow is the schema, not the prompt.**

---

## Knowledge, not tools

Course content, fees, durations and locations come from the **brochures**, not from a tool. Do not
build a `GetCourseFee` action — the brochures are the source of truth, and a second source that can
drift from them is a defect waiting to happen.

Remove the **Search all websites** chip before the first test.
