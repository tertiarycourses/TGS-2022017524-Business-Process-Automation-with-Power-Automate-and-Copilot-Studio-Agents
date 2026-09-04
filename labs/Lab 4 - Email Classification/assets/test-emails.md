# Lab 4 - Email Classification — test emails

Send each email to the course mailbox (the Inbox the trigger watches). Sending from a
**second** mailbox is best; sending from the course account to itself also fires the trigger.
Send them **one at a time** and check the **Activity** tab between sends, so each run can be
matched to its email. Whole runs take 20–40 seconds; the Priority run stays at **Running**
until the Teams card is answered.

| # | Subject | Body | Extra | Expected category | Expected visible result |
|---|---|---|---|---|---|
| 1 | `Can we meet next Tuesday about the Copilot course?` | `Hi, I'd like a 30-minute chat next Tuesday 10 September at 3pm to discuss running the Copilot Studio course for my team of eight. Teams is fine. Thanks, Priya` | — | **Meeting** | A calendar event on the course account's calendar, 10 Sep 15:00–15:30 Singapore time, with a Teams link and the sender as attendee; an auto-reply "meeting booked" in the sender's inbox |
| 2 | `Question on WSQ funding for the Power Automate course` | `Hello, does the two-day Power Automate course qualify for SkillsFuture funding for a Singapore PR aged 45, and is there a minimum class size? No rush, just planning for Q4. Regards, Marcus Tan` | — | **Need Reply** | A reply beginning "Dear Marcus" that promises a colleague will confirm the funding details — with **no invented figures** |
| 3 | `URGENT: trainer no-show for tomorrow 9am class` | `The trainer for tomorrow's 9am session at our Jurong office has just cancelled. We have 12 learners booked and the room paid for. Please call me today on 9123 4567 or we will have to cancel and request a refund. — Daniel Lim, HR` | Set **Importance = High** before sending | **Priority** | An adaptive card in the Teams **Workflows** bot chat titled `Request information \| Microsoft Copilot Studio`; the run sits at **Running**. Answer **Yes** → the sender receives the approved reply ending `Approved by: <your name>`. Answer **No** → the trainer receives `Escalation: URGENT: trainer no-show…` |
| 4 | `Your September newsletter: new AI course dates` | `Hi everyone, here are the new intakes for October: Data Analytics 6–7 Oct, Copilot Studio 13–14 Oct. Registration links are on the website. No reply needed.` | — | **Informational** | The email is **flagged** in the course Inbox; no reply is sent |
| 5 | *(no subject)* | `asdf qwerty 12345` | — | **Other** | The email is **moved** to the Outlook folder `Lab 4 - Other` |

## What each test proves

- **1** — the Meeting Handler's structured fields (title, start, end) drove a deterministic **Create event (V4)**; the model never touched the calendar directly.
- **2** — the Reply Drafter answered without inventing a fee or a policy. Read the reply aloud: any figure in it is a failure.
- **3** — the run **physically stopped** at Human review. Open Activity before you answer the card and show the class the run sitting at Running.
- **4** and **5** — every port does something visible, so a wrong classification is caught by what happened, not by reading a log.

## Re-running

Send the same five again after any change to the Classify categories or an Agent's instructions — and **Publish** first. The trigger runs the published version, so an unpublished fix looks identical to no fix.
