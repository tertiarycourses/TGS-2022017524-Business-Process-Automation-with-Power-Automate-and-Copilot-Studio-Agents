# Lab 1 - Course Enquiry Form — Microsoft Forms specification

One-page rebuild sheet. A trainer can recreate this form from scratch in about two minutes.
It is used by **Lab 1 — Trigger and Actions** and **Lab 2 — Log to Excel**. The trainer's own
copy in the tenant is the one that carries the ` (DO NOT DELETE)` suffix; learners create their own.

| Setting | Value |
|---|---|
| Where | `https://forms.office.com`, signed in with the course account |
| Form title | `Lab 1 - Course Enquiry Form` |
| Description | `Submit your contact details and course enquiry.` |
| Question order | Name → Email → Tel → Message (the workflow maps answers by question title, not position, but keep this order so the screenshots match) |

## Questions

| # | Question title | Type | Required | Extra settings |
|---|---|---|---|---|
| 1 | `Name` | Text | **Yes** | Short answer (default) |
| 2 | `Email` | Text | **Yes** | Short answer. *Optional:* under **… → Restrictions**, choose **Text → Contains** `@` so a typo without an `@` is rejected before it reaches the workflow |
| 3 | `Tel` | Text | **Yes** | Short answer |
| 4 | `Message` | Text | **Yes** | **… → Long answer = On** |

Type the question titles exactly as shown — `Name`, `Email`, `Tel`, `Message`. The workflow's
**Get response details** action exposes each answer under its question title, and the
learner guide refers to those four names.

## Settings (the **…** menu top-right → **Settings**)

| Setting | Value | Why |
|---|---|---|
| Who can fill out this form | **Anyone can respond** | The form collects the respondent's email itself (question 2), so the workflow does not depend on a signed-in identity. Learners can submit from the Preview link without switching accounts |
| Record name | Off (not available for anonymous forms) | The `Email` question is what the workflow uses for the **To** field |
| One response per person | Off | Learners submit the form several times during Labs 1 and 2 |
| Accept responses | On | |
| Shuffle questions | Off | |
| Customise thank-you message | Optional: `Thanks — a confirmation email is on its way.` | |

## How to share for the labs

**Collect responses** (top right) → copy the link, or simply use **Preview** during class.
Every submission starts the workflow; submit **once** per test so the Activity tab stays readable.

## Test data used in the labs

| Lab | Name | Email | Tel | Message |
|---|---|---|---|---|
| Lab 1, Part D | `Jane Tan` | an address you can open | `61234567` | `Please send me the next course schedule.` |
| Lab 2, Part E | `Aisha Lim` | an address you can open | `62345678` | `I would like the corporate course outline.` |
