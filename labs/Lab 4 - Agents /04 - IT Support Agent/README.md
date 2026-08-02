# Agent 4 — IT Support Agent

**Pattern taught:** *skills as the unit of behaviour.* This is the only agent in Lab 4 with a full
set of named **Skills** — five of them — and the one that shows what a Skill is for as against an
instruction, a tool or a child agent.

**Build time:** 45–55 minutes.

---

## Folder contents

| Path | What it is |
|---|---|
| [`agent/instructions.md`](agent/instructions.md) | The parent agent's Instructions |
| [`skills/`](skills/) | **The five skills** — one file each |
| [`tools/tool-descriptions.md`](tools/tool-descriptions.md) | `RaiseTicket`, `CheckTicketStatus`, `LookupAsset` |
| [`knowledge/`](knowledge/) | Known-issues log, service catalogue, asset register |
| [`connected-agents/`](connected-agents/) | Three children |

### The five skills

These match the tenant build exactly. Add each one at **Agent → Skills → +**.

| # | Skill | File |
|---|---|---|
| 1 | Hardware Issue Handling | [`skills/hardware-issue-handling.md`](skills/hardware-issue-handling.md) |
| 2 | Network Troubleshooting | [`skills/network-troubleshooting.md`](skills/network-troubleshooting.md) |
| 3 | Software Troubleshooting | [`skills/software-troubleshooting.md`](skills/software-troubleshooting.md) |
| 4 | Raise IT Support Ticket | [`skills/raise-it-support-ticket.md`](skills/raise-it-support-ticket.md) |
| 5 | Password Reset Procedure | [`skills/password-reset-procedure.md`](skills/password-reset-procedure.md) |

### The three children

| # | Agent | Owns |
|---|---|---|
| 1 | [Triage Agent](connected-agents/01%20-%20Triage%20Agent/) | Priority and routing — including the security path |
| 2 | [Access Request Agent](connected-agents/02%20-%20Access%20Request%20Agent/) | Accounts, licences, permissions — **has a human gate** |
| 3 | [Asset and Hardware Agent](connected-agents/03%20-%20Asset%20and%20Hardware%20Agent/) | The asset register, replacements → Procurement |

---

## Skills vs everything else — the distinction this agent teaches

Learners conflate these four constantly. IT Support is the clearest place to separate them, because
it has all four doing visibly different jobs.

| | What it is | Example here | Enforced? |
|---|---|---|---|
| **Instructions** | Who the agent is, always in force | "Never ask for a password" | No — probabilistic |
| **Skill** | A named procedure, applied when the topic matches | *Password Reset Procedure* | No — the model decides it applies |
| **Tool** | A flow that does something outside the conversation | `RaiseTicket` | The flow's own logic **is** enforced |
| **Connected agent** | A different agent with its own knowledge and audience | Access Request Agent | The knowledge boundary is real |

**A Skill is a procedure, not a permission.** Naming a skill *Password Reset Procedure* does not
give the agent the power to reset a password, and does not stop it claiming it did. The tool
decides what happens; the skill only shapes how the conversation goes.

Make this concrete in class: the five skills below are all *advisory*. The only hard control in
this agent is the human gate inside the Access Request flow.

---

## Build order

1. Instructions.
2. All five skills.
3. Tools — `RaiseTicket` first; it is the one every skill ends at.
4. Knowledge.
5. Children, one at a time, testing after each.

> **Remove the "Search all websites" chip.** An IT agent with web access will hand a colleague a
> registry edit from a forum. It will be confident, it will look like the rest of its answers, and
> it may be for the wrong OS version.

---

## The failure this agent is designed to produce

Ask the class to get the agent to reveal a password reset code, or to confirm it has reset an
account it has not. Both are reachable, and both look like success:

- "I've reset your password, try again now" — when nothing was reset, because `RaiseTicket` opens a
  ticket and a human resets accounts.
- Coaching a caller through a reset for **someone else's** account, because the caller said they
  were that person's manager.

Neither produces an error. Both look exactly like the agent working.
