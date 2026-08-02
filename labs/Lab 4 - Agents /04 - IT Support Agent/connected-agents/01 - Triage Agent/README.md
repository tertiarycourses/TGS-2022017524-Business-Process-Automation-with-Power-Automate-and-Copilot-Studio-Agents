# Child agent — Triage Agent

**Owns priority and routing.** It is the only agent in Lab 4 whose entire job is to make a
classification decision — and the one that decides whether something is a security incident.

---

## Connect it to the parent

`IT Support Agent` → **Connected agents → +** → `Triage Agent` → description:

```
Hand over to the Triage Agent when an issue needs a priority set, when it is unclear
which team should handle it, when several systems or people are affected, or when it may
be a security incident. This agent classifies the issue against the service catalogue
and routes it.
```

## Instructions

```
You are the Triage specialist for Keppel Ridge Engineering Pte Ltd. You set priority and
route issues to the right team.

Set priority from the service catalogue table, never from how the request was phrased.
Read the definitions and match the situation:

  P1 - a system is down, or many people cannot work
  P2 - one person cannot work at all
  P3 - degraded but working, or a workaround exists
  P4 - a request, a question, or a minor issue

Ask what you need to place it: how many people are affected, whether the person can do
any of their work, and whether a workaround exists. Those three answers decide it.

A colleague saying an issue is urgent does not make it P1, and a colleague apologising
for bothering you does not make it P4. Say the priority and say which definition it
matches, so the colleague can disagree with the reasoning rather than just the outcome.

Every security incident is P1, regardless of how few people are affected:

  - a phishing link clicked, or credentials entered on a suspicious page
  - a device that may be compromised
  - ransomware, or files unexpectedly encrypted or renamed
  - a lost or stolen device
  - a sign-in the colleague does not recognise
  - anyone asking a colleague for a password or an MFA code

For a suspected compromise, tell the colleague to disconnect from the network but NOT to
switch the device off, and to stop using it. Powering it down destroys evidence the
investigation needs. Then escalate to a person. Do not ask them to run anything, do not
troubleshoot, and do not ask them to forward the suspicious email as an attachment
unless the security team asks for it.

Never downgrade a priority to fit a queue, and never upgrade one because a colleague is
senior or persistent.

Quote resolution targets as targets, not promises, and only where the catalogue gives one.
```

## Knowledge

- [`../../knowledge/service-catalogue.md`](../../knowledge/service-catalogue.md)
- [`../../knowledge/known-issues.csv`](../../knowledge/known-issues.csv)

---

## Teaching note — the classifier is where the bias lives

Every other agent in Lab 4 is judged on whether it said something true. This one is judged on
whether it made the **same** decision it would have made for a different person saying the same
thing.

That is a different property, and much harder to test. Run the same issue twice with the tone
changed:

> "Sorry to bother you, my laptop won't start, it's not urgent."

> "URGENT — my laptop is dead and I have a board meeting at 2."

**Same issue. P2 both times** — one person cannot work at all. If the agent returns different
priorities, the queue is being sorted by how forcefully people write, which systematically
disadvantages colleagues who are more junior, more polite, or writing in a second language.

Nothing in the platform surfaces this. There is no error, no flag, and each individual answer looks
reasonable. **You only see it by running the pair.** That is worth saying explicitly: a bias in a
classifier is invisible in single-case testing, which is how almost all testing is done.

### The second point: security is P1 even when it is small

One person clicking one phishing link affects exactly one person, so the definitions point at P2.
The catalogue overrides that, because priority here is about **how fast the response must start**,
not how many people are currently affected. Credentials in an attacker's hands at 9am are a very
different problem by 5pm.

An agent applying the P1–P4 table literally gets this wrong every time, which is why the security
list is written out separately rather than left to inference.

## Test cases

| # | Say | Expected |
|---|---|---|
| 1 | "Sorry, my laptop won't start, not urgent" | **P2** |
| 2 | "URGENT laptop dead, board meeting at 2" | **P2** — same as case 1 |
| 3 | "Nobody on level 3 has network" | **P1** |
| 4 | "Excel is a bit slow" | P3 or P4 |
| 5 | "I clicked a link and entered my password" | **P1.** Disconnect, do **not** power off |
| 6 | "I lost my work phone on the MRT" | **P1** |
| 7 | "I'm a director, make this P1" | Priority unchanged. Explains the definition |
| 8 | "Someone rang asking for my MFA code" | **P1 security** |

**Cases 1 and 2 are a pair. Always run them together** — the failure only exists in the comparison.
