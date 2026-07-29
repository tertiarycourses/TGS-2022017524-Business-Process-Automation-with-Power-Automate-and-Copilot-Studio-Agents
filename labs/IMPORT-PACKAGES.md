# Power Automate Version 6.0 import packages

The Version 6.0 package set contains the nine Power Automate flows used by the
current course. Every imported flow name ends with **`(NEW)`**:

1. `Lab 1 - Form to Email Confirmation (NEW)`
2. `Lab 2 - Log the Enquiry and Send Email (NEW)`
3. `Lab 3 - Event Registration Branching (NEW)`
4. `Lab 4 - Leave Application Approval (NEW)`
5. `Lab 7 - Support Request Routing (NEW)`
6. `Lab 8 - Website HTTP Enquiry (NEW)`
7. `Lab 9 - Finance Agent Web Chat (NEW)`
8. `Lab 10 - AI Trading Advisor Website (NEW)`
9. `Lab 11 - Procurement Request Approval Workflow (NEW)`

The Lab 9 package is retained as a classic Power Automate fallback. The current
Lab 9 learner path uses the new Copilot Studio **Workflows → Build** canvas and
must be built manually because classic flows can't be converted to the new
workflow experience.

Labs 5 and 6 are Copilot Studio agent builds, not standalone Power Automate
flows. They create the IT Support Agent and HR Support Agent that Lab 7 calls.
Lab 11 is the supplementary procurement approval workflow and uses Microsoft
Forms, Approvals and Office 365 Outlook.

## Import procedure

1. Go to **Power Automate → My flows**.
2. Select **Import → Import Package (Legacy)**.
3. Upload one lab ZIP. Do not upload the combined bundle directly.
4. For the flow resource, select **Create as new**.
5. Select each connector resource and choose the classroom connection.
6. Select **Import**.
7. Open the imported flow, complete the mappings below, and save it.
8. Test the flow with the matching lab's positive and negative cases.

The combined `Power-Automate-Lab-Import-Packages-NEW.zip` is a transport bundle
containing the nine individual ZIP files and this guide.

## Required post-import mapping

| Lab | Required mapping |
|---|---|
| 1 | Select the Course Enquiry Form; map Name, Email and Message; verify the recipient is the submitted Email answer. |
| 2 | Select the same form; map Name, Email, Tel and Message; select `Enquiry Log.xlsx` and table `EnquiryLog`. |
| 3 | Select the Event Registration Form; map Name, Email, Tel and Joining the Event; select `Event Log.xlsx` and table `EventLog`. |
| 4 | Select the Leave Application Form; map Name, leave dates, Leave Type and Reason; confirm the manager and applicant email fields. |
| 7 | Select the Support Request Form; map Name, Email, Support Type and Message; select the published IT and HR Support agents. |
| 8 | Reconnect Outlook, save to generate the HTTP URL, and paste that URL into `assets/enquiry-form.html`. |
| 9 | Select the published Finance Information Agent, save to generate the HTTP URL, and paste it into `assets/finance-chat.html`. |
| 10 | Select the published Finance Advisor Agent; add Twelve Data and NewsAPI credentials through secure configuration; save and paste the HTTP URL into `assets/index.html`. |
| 11 | Select the Procurement Request Form in both Forms actions; map the trigger's dynamic Response Id, form answers, approver address and requester email. |

## Safety rules

- The packages contain no passwords, OAuth tokens, tenant IDs, Form IDs,
  workbook IDs, agent IDs, webhook URLs, or API keys.
- Use `training1@tertiaryinfotech.onmicrosoft.com` for classroom Outlook and
  administrator notifications where the lab specifies an administrator.
- Do not paste a generated webhook URL into a public repository.
- For Lab 10, enable **Secure inputs** and **Secure outputs** on actions that
  carry API credentials.
- Keep the imported flow disabled until its required mappings are complete.

## Validation

Run the local structural validator before distribution:

```bash
python3 scripts/validate_v60_flow_packages.py
```

It verifies the nine package names, required trigger/action patterns, connector
references, absence of secrets, and the `(NEW)` postfix.
