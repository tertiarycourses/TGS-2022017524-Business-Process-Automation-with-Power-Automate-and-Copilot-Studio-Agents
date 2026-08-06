# Lab 5 — Calling Agent from Workflow

*A blog-writer agent flow: topic in, Teams post out*

## Goal

Build an agent flow in the Copilot Studio workflow designer that collects a blog topic at the Start node, has M365 Copilot draft the blog post, and posts the draft to the **General** channel of the **Training** team in Microsoft Teams.

## Duration

Approximately 30 minutes.

## Prerequisites

- Copilot Studio access in the course environment (Copilot Studio Training), with Copilot credits
- Microsoft Teams access, and membership of the **Training** team (or any team the trainer designates)
- Permission to post messages to that team's **General** channel

## Scenario

The Learning & Development team wants a one-step way to turn an idea into a shareable draft. Anyone runs the flow and types a topic; the model writes a short blog post; the draft lands in the Training team's General channel where colleagues can read and comment. Unlike Lab 4, nobody converses with an agent here — the **workflow calls the model** at a fixed step, then acts on the result deterministically.

## Workflow visual

![Lab 5 Calling Agent from Workflow](assets/flowchart.png)

Three nodes: **Start** (with a Topic input) → **M365 Copilot** (draft the blog post) → **Post message in a chat or channel** (Training · General).

## Detailed step-by-step

### Part A — Create the agent flow

1. [Open Copilot Studio](https://copilotstudio.microsoft.com).
2. Confirm the environment selector (top right) shows the course environment — **Copilot Studio Training**. Agent flows consume Copilot credits, and the Default environment may have none.
3. In the left navigation, select **Flows**.
4. Select **New agent flow** (or **+ Create → Agent flow**).
5. The workflow designer opens with a **Start** node already on the canvas.
6. Rename the flow to `Blog Writer Flow`: select the flow name at the top left, type the new name, and confirm.
7. Select **Save** so the flow exists before you configure it.

### Part B — Configure the Start node with a Topic input

1. Select the **Start** node to open its configuration panel.
2. Choose the manual/run-on-demand trigger if the designer asks how the flow starts (the classroom flow is run by a person, not by an event).
3. In the trigger's inputs section, select **Add an input**.
4. Choose **Text**.
5. Name the input `Topic`.
6. In the description or placeholder, enter `The subject of the blog post`.
7. Leave the input required (do not give it a default value — every run should state its topic).
8. Select **Save**.

### Part C — Add the M365 Copilot node to draft the blog

1. On the canvas, select **+** on the connector after **Start**.
2. In the Add panel, select the **M365 Copilot** node. Be precise here — selecting an item in the Add panel *creates* a node, and an accidental extra node must be deleted (undo does not remove it).
3. Select the new **M365 Copilot** node to open its configuration.
4. If a **Connection** field is shown, confirm it is signed in as your course account.
5. In the instructions/prompt area, **type** the following as plain text, leaving a gap where the topic goes:

   > Write a short, engaging blog post of about 300 words on the topic below. Give it a title line, a two-sentence introduction, three short paragraphs with one key point each, and a one-sentence conclusion. Write in plain professional English for a general business audience.
   >
   > Topic:

6. Place the cursor after `Topic:` and insert the **Topic** input using the **⚡ dynamic content picker** — select the lightning-bolt icon and pick **Topic** from the Start node's outputs.
   - **Never paste an expression** such as `@{...}` into this editor. It is a rich-text editor and silently mangles pasted references; the flow then runs green while the model receives an empty topic.
7. If an **Output** option is shown, leave it as the default **Text response** — the next node needs plain text, not structured fields.
8. Select **Save**.

### Part D — Post the draft to the Training team's General channel

1. Select **+** on the connector after the **M365 Copilot** node.
2. In the Add panel, search for `Post message in a chat or channel` (Microsoft Teams connector) and select it.
3. Select the new node to open its configuration.
4. If prompted, create or confirm the **Microsoft Teams connection** with your course account.
5. Set **Post as** to `Flow bot` (posting as `User` requires the flow to act as you; the bot makes the automation visible as automation).
6. Set **Post in** to `Channel`.
7. Set **Team** to `Training` — pick it from the dropdown; do not type a name the dropdown has not offered.
8. Set **Channel** to `General`.
9. Click into the **Message** field and insert the M365 Copilot node's text output with the **⚡ dynamic content picker** — again, pick the token; do not type an expression.
10. Select **Save**.
11. Do not drag nodes to rearrange them afterwards — **moving a node clears its configuration** and the unconfigured node is then skipped silently at run time. If a node is ever moved, reopen it and refill every field.

### Part E — Test and verify in Teams

1. Select **Publish** (or **Save** then **Test**, as the designer offers). The runnable flow is the **published** version — saving a draft is not enough. If a version history is shown, confirm `LIVE` matches `CURRENT DRAFT`.
2. Run the flow: select **Test** / **Run**, and when prompted for **Topic**, enter `How AI agents are changing business process automation`.
3. Wait for the run to complete — a run with one model call typically takes 10–20 seconds.
4. Open Microsoft Teams → **Training** team → **General** channel.
5. Confirm the blog post appears, posted by the Flow bot, with a title, introduction, three paragraphs and a conclusion.
6. Confirm the post is actually about the topic you typed. If it is generic or empty, the Topic token did not reach the model — reopen the M365 Copilot node and re-insert the token with the ⚡ picker.
7. Run the flow again with a second topic, e.g. `Five tips for running effective hybrid meetings`, and confirm a second, different post arrives.
8. In Copilot Studio, open the flow's **Activity** (run history) and review the run: select the M365 Copilot node and read its **Run Details → Outputs** to see exactly what the model produced. This is the habit that matters — when a flow misbehaves, read the upstream node's outputs before theorising.

## Checkpoint

- The flow has exactly three configured nodes: Start (with a required `Topic` text input) → M365 Copilot → Post message in a chat or channel
- The Topic token and the blog-text token were both inserted with the ⚡ picker, not typed
- A test run posts a topic-specific blog draft to the Training team's General channel
- A second run with a different topic produces a different post
- The run history shows the model's actual output under the M365 Copilot node

## Troubleshooting

| Symptom | Check |
|---|---|
| Run fails with `InsufficientMcsCredits` | You are in the wrong environment — switch to the course environment (Copilot Studio Training); a licence does not fix this, credits are per-environment |
| Post appears but the blog ignores the topic, or is empty | The Topic reference was pasted or typed, not picked — reopen the M365 Copilot node, delete the reference, re-insert with the ⚡ picker |
| Teams node cannot find the Training team | You are not a member of the team, or the connection is signed into a different account — join the team, or fix the connection |
| A node shows "Needs setup" | It was moved or duplicated — reopen it and refill every field, including the connection |
| Message field rejects your typed expression | Expected — this field wants a ⚡ picker token, not a typed expression |
| Test runs an old version of the flow | The published version is stale — publish again and confirm `LIVE` matches `CURRENT DRAFT` |
| Nothing arrives in Teams but the run is green | Open the run in Activity and check each node's Run Details — an unconfigured node is skipped silently |

## Key takeaways

- An agent flow **calls the model as one step in a deterministic workflow** — the flow decides when the model runs and what happens to its output, which is the opposite of a chat agent deciding for itself.
- The Start node's inputs are the flow's contract: one required `Topic` field is what turns a private automation into a reusable team tool.
- Dynamic content must be inserted with the ⚡ picker. Typed or pasted expressions in these editors fail silently — the flow stays green while the model receives nothing.
- The Teams post is the *action* half of the pattern: model output is only useful once the workflow delivers it where people already work.

---

**Next:** [Lab 5b — Calling Workflow from Agent](../Lab%205b%20-%20Calling%20Workflow%20from%20Agent/index.md)
