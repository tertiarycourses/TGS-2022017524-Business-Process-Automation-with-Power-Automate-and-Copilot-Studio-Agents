# Deploying the agents to Microsoft Teams

How to publish a Copilot Studio agent and make it reachable in Teams. Applies to all four agents in
Lab 4.

**Time:** 20–25 minutes for the first agent, ~5 minutes for each after that.

---

## The rule that determines everything else

> **You deploy the PARENT only. Child agents are never deployed.**

A connected agent is reachable **through** its parent and has no channel of its own. Deploying a
child to Teams gives colleagues a way to reach the Screening Agent, or the Quotation Agent, without
passing the parent's routing and refusals.

| Deploy to Teams | Do **not** deploy |
|---|---|
| Procurement Agent | — (it has no children) |
| HR Agent | Screening, Interview, Onboarding, Policy & Benefits |
| Sales Agent | Lead Qualification, Quotation, Account Health |
| IT Support Agent | Triage, Access Request, Asset & Hardware |

Seven children stay undeployed. If a learner deploys one "so it's easier to test", they have created
a door past the boundary the parent exists to enforce.

---

## Before you start

| Check | Why |
|---|---|
| The agent is **Published**, not Draft | ⋯ → **Version history**: `LIVE` and `CURRENT DRAFT` must match |
| Every **child** is published | An unpublished child does not appear in the parent's list — and stops working after the parent is published |
| Every **flow** the agent calls is published | An unpublished flow is invisible to the agent's tool list |
| The **Search all websites** chip is removed | On every agent, parent and child |
| You are in the right **environment** | Agents, flows and SharePoint lists must all be in the same one |

> **The commonest first failure is an environment mismatch**, and it shows up as "the flow isn't in
> the list" or "the child isn't there". Check the environment picker in the top bar before
> debugging anything else.

---

## Step 1 — Publish

**Publish** (top right) → wait for confirmation.

Publishing takes a minute or two. A channel added to an unpublished agent will not work, and the
error you get later says nothing about publishing.

**Re-publish after every change** — instructions, skills, tools, knowledge, connected agents. Teams
serves the *published* version, so an untested edit and an unpublished fix look identical from the
chat window.

## Step 2 — Add the Teams channel

**Channels** → **Microsoft Teams** → **Add channel**.

Then choose availability:

| Option | Who can use it | Use for |
|---|---|---|
| **Show to my teammates and shared users** | People you share the link with | **Classroom — use this** |
| **Show to everyone in my org** | The whole tenant | Needs admin approval |

For the lab, choose the first. The second submits your agent for tenant-wide admin approval, which
will not complete inside the session.

## Step 3 — Turn it on and get the link

**Turn on Teams** → **Availability options** → **Copy link**.

The link opens the agent in Teams as a personal chat.

> **Test the link yourself before sharing it.** A link to an unpublished agent opens a chat that
> answers nothing, and the failure looks like the agent being broken rather than not deployed.

## Step 4 — Open it in Teams

Paste the link → Teams opens → **Add**.

The agent appears in the Teams left rail and in **Chat**. It is now a personal chat, like messaging
a colleague.

## Step 5 — Test in Teams, not just in Copilot Studio

**The Test pane and Teams are different environments.** Test both.

| | Test pane | Teams |
|---|---|---|
| Version | Current draft | **Published** |
| Signed-in identity | Yours, as maker | The **actual colleague** |
| Connections | Your interactive session | May be unattended |

Run at least one test from each agent's test table in **Teams**:

| Agent | Test in Teams |
|---|---|
| Procurement | TC2 — "15 boxes of cleaning consumables from Bukit Timah Consumables at $890 each…" → `APPROVAL` / `ABOVE_THRESHOLD` |
| HR | "How much annual leave do I have left?" → **the signed-in user's** balance, with the as-at date |
| Sales | "Can I get the 40% alumni discount on the sushi course?" → corrects the premise |
| IT Support | "I clicked a link in a weird email" → P1, disconnect, **do not power off** |

> **The HR test is the one that behaves differently in Teams**, and it is the reason this step
> exists. In the Test pane the signed-in user is *you, the maker*. In Teams it is the colleague. An
> agent that looks correct in testing can be reading the wrong person's record in production.

---

## Adding an agent to a Team or a channel

A personal chat is per-person. To put an agent in a shared channel:

**Teams → the channel → + (Add a tab)** → find the agent → **Add**.

**Think before you do this for HR.** In a channel, everyone sees everyone's questions. "How much
leave do I have left?" is fine in a personal chat and is a disclosure in a channel — and the
colleague asking may not realise which one they are in.

| Agent | Personal chat | Team channel |
|---|---|---|
| Procurement | Yes | Reasonable — a Procurement channel |
| HR | **Yes — personal only** | **No.** Leave, benefits and cases are personal |
| Sales | Yes | Reasonable — an enrolment team channel |
| IT Support | Yes | Reasonable — an IT support channel |

---

## Sharing with the class

**Share** (top bar) → add users or copy the sharing link.

Colleagues need the link **and** access to the agent. Sharing the link alone gives them a chat that
refuses to load.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Agent doesn't respond in Teams | Not published, or published after the channel was added — **re-publish** |
| "Something went wrong" on the link | Not shared with that user, or wrong environment |
| Works in the Test pane, fails in Teams | Teams serves the **published** version — check ⋯ → Version history |
| Agent answers but never calls its tool | Flow not published, or the tool description too narrow — the description is a prompt |
| Handover to a child never happens | Child unpublished, or its connected-agent description doesn't match how colleagues actually phrase it |
| Child answers but has no knowledge | **Children do not inherit the parent's knowledge.** Attach the source to the child too |
| Reads the wrong person's record | Agent is using a name from the message instead of the signed-in identity |
| Approval never arrives | Human review **Channel is Outlook** — switch to **Teams** |
| Citation markers `[1]` in replies | Missing the "never include citation markers" line — the grounding layer adds them |
| Every approval is declined | If/Else built on a hand-typed `body('Human_review')?['result']` — use the `Outcome` token |

> **After any change: re-publish, then re-test in Teams.** Most "the fix didn't work" reports in
> this lab are a stale published version.

---

## What deployment does not give you

Worth saying explicitly before the class leaves.

**No approval routing.** Teams delivers the *conversation*. The approval gates in the Procurement,
HR leave, Access Request and Quotation flows are separate — they arrive in the Teams **Approvals**
app (teams.microsoft.com → ••• → Approvals), not in the agent chat. A colleague chatting to the
agent sees nothing of the approval waiting for their manager.

**No identity guarantee beyond the signed-in user.** The agent knows who is signed in. It does not
know whether the person typing "I'm Priya's manager" is anyone's manager. Every rule in the four
agents about not accepting a claimed identity is doing real work, and Teams does not do it for you.

**No retention control you chose.** Conversations are stored under the tenant's Teams retention
policy. Anything a colleague types — a health disclosure while asking about leave, an allegation
about a colleague — is retained under a policy the agent's designer did not set and may not know.
That is the strongest argument for the HR Agent's escalation list: the safest way to keep something
out of a transcript is for it never to reach the agent.

**No audit of the model's reasoning.** The SharePoint audit rows record what the *flows* did. Nothing
records why the agent chose to hand over, or to call a tool, or not to. On a canvas you can see every
step; the decision to invoke the whole thing is not on any canvas.
