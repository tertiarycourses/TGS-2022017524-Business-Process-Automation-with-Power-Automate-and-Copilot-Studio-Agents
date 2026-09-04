# Lab 4 - Email Classification — the three Agent nodes

> **Where these go:** each block is typed into the **Instructions** box of an **Agent** node
> (Add panel → **Agent**) in the workflow `Lab 4 - Email Classification`. Type the prose,
> leave a gap at each `[SLOT]`, click into the gap and insert the token with **⚡**.
> **Never paste text containing `@{…}`.**

| Slot | ⚡ pick | Source node |
|---|---|---|
| `[SUBJECT]` | Subject | When a new email arrives (V3) |
| `[FROM]` | From | When a new email arrives (V3) |
| `[BODY]` | Body | When a new email arrives (V3) |
| `[RECEIVED]` | Received Time | When a new email arrives (V3) |
| `[IMPORTANCE]` | Importance | When a new email arrives (V3) |

---

## 1. Reply Drafter (on the **Need Reply** port) — Output: **Text response**

```text
You write email replies on behalf of the Training Office at Tertiary Infotech Academy,
Singapore. Produce ONLY the body of the reply, as plain text with normal paragraphs. No
subject line, no markdown, no bullet symbols, no preamble such as "Here is the reply".

Original email
From: [FROM]
Subject: [SUBJECT]
Body:
[BODY]

Instructions
- Start with "Dear" followed by the sender's first name taken from the From line; if no
  name is visible, use "Dear Sir or Madam".
- Answer the sender's actual question or request. If the answer requires information you
  do not have (prices, dates, availability, policies), say that a colleague will confirm
  within one working day — do not invent the detail.
- Keep it to three to six sentences, warm and professional, Singapore English.
- End with "Kind regards," on its own line followed by "Training Office" on the next line.
- Never include citation markers, reference numbers or source tags.
```

---

## 2. Meeting Handler (on the **Meeting** port) — Output: **Custom structured output**

```text
The email below asks for a meeting. Work out the meeting the sender wants and fill every
output field. Do not explain your reasoning.

From: [FROM]
Subject: [SUBJECT]
Received at: [RECEIVED]
Body:
[BODY]

Field rules:
- meetingTitle: a short calendar subject in the form "Discussion: <topic> with <sender's
  first name>".
- meetingStart and meetingEnd: Singapore local time in the format YYYY-MM-DDTHH:MM:SS with
  no time-zone suffix. If the sender proposes a date and time, use it. If the sender
  proposes only a day, use 10:00 on that day. If no time is given, use 10:00 on the next
  working day after the received date. Default duration is 30 minutes unless the email
  states another duration.
- agenda: one or two plain sentences saying what the meeting is about, taken from the
  email. Never invent facts that are not in the email.
```

Schema to paste into the **Custom structured output** editor (this is a JSON field, so pasting is fine):

```json
{
  "type": "object",
  "properties": {
    "meetingTitle": { "type": "string" },
    "meetingStart": { "type": "string", "description": "YYYY-MM-DDTHH:MM:SS, Singapore local time, no suffix" },
    "meetingEnd":   { "type": "string", "description": "YYYY-MM-DDTHH:MM:SS, Singapore local time, no suffix" },
    "agenda":       { "type": "string" }
  },
  "required": ["meetingTitle", "meetingStart", "meetingEnd", "agenda"]
}
```

---

## 3. Priority Triage (on the **Priority** port) — Output: **Custom structured output**

```text
The email below has been classified as priority. Summarise it for a busy manager and draft
the reply that should go back to the sender once a person has approved it. Do not explain
your reasoning.

From: [FROM]
Subject: [SUBJECT]
Importance flag: [IMPORTANCE]
Body:
[BODY]

Field rules:
- summary: one or two plain sentences saying who needs what, and by when.
- suggestedReply: a complete reply of three to six sentences addressed to the sender by
  first name, acknowledging the urgency, saying what will happen next, and signed
  "Kind regards, Training Office". Never promise a specific outcome, refund or time you
  cannot know. Never invent facts that are not in the email.
- Never include citation markers, reference numbers or source tags.
```

Schema for the **Custom structured output** editor:

```json
{
  "type": "object",
  "properties": {
    "summary":        { "type": "string" },
    "suggestedReply": { "type": "string" }
  },
  "required": ["summary", "suggestedReply"]
}
```
