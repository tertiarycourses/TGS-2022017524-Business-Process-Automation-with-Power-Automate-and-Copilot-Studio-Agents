# Lab 3 - Leave Application Form — Microsoft Forms specification

One-page rebuild sheet. A trainer can recreate this form from scratch in about two minutes.
It is used by **Lab 3 — Leave Application Approval**. The trainer's own copy in the tenant carries
the ` (DO NOT DELETE)` suffix; learners create their own.

| Setting | Value |
|---|---|
| Where | `https://forms.office.com`, signed in with the course account |
| Form title | `Lab 3 - Leave Application Form` |
| Description | `Apply for leave. Your manager will be notified and will approve or reject the request.` |
| Question order | Name → Leave from date → Leave end date → Leave Type → Reason for Leave |

## Questions

| # | Question title | Type | Required | Extra settings |
|---|---|---|---|---|
| 1 | `Name` | Text | **Yes** | Short answer |
| 2 | `Leave from date` | **Date** | **Yes** | The date picker appears automatically |
| 3 | `Leave end date` | **Date** | **Yes** | |
| 4 | `Leave Type` | **Choice** | **Yes** | Options, one per line: `Annual` · `Medical` · `Compassionate` · `Unpaid`. **Multiple answers = Off** (only one leave type may be chosen). **Drop-down = Off** so all four show as radio buttons |
| 5 | `Reason for Leave` | Text | **Yes** | **… → Long answer = On** |

Type the titles exactly as shown. The workflow's **Get response details** action exposes the
answers by these titles, and the approval card in Lab 3 Part C labels each line with them.

## Settings (the **…** menu top-right → **Settings**)

| Setting | Value | Why |
|---|---|---|
| Who can fill out this form | **Only people in my organisation can respond** | Required for the next setting |
| **Record name** | **On** | Forms then supplies **Responders' Email** and **Responder** name to the workflow, so the applicant's address does not have to be typed as a question and the decision email goes to the signed-in person |
| One response per person | **Off** | Lab 3 submits the form twice (one approval test, one rejection test) |
| Accept responses | On | |
| Shuffle questions | Off | Dates must stay in order |

> **Why no Email question?** Lab 1 asked for an email because anyone could respond. Here the
> respondent is a signed-in colleague, and *Record name* gives the workflow a trustworthy address —
> one the applicant cannot mistype or spoof. That difference is a small governance point worth
> saying aloud in class.

## Test data used in the lab

| Test | Name | From | To | Leave Type | Reason |
|---|---|---|---|---|---|
| Part E — approval | `Ravi Kumar` | a future date | the following day | Annual | `Family appointment` |
| Part E — rejection | any name | a different future date | +1 day | Unpaid | `Overseas travel` |
