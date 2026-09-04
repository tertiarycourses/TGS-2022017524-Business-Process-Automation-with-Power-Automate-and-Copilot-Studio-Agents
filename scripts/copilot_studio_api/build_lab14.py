"""Lab 14 - HTTP and Human Review (DO NOT DELETE):
HTTP trigger -> Compose Enquiry (normalised JSON object) -> Agent 'Rapport Agent' (structured: draftReply, urgency, complianceFlags, escalate, ...)
-> Response {status, ticketId, urgency, escalated, message} BEFORE the gate -> Excel Add a row (Lab 14 - Handover Queue.xlsx / Drafts)
-> Human review (Teams; Outcome Yes/No + Name) -> If Outcome = Yes -> Send an email to the client ; Else -> Excel Add a row (HandoverQueue)."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *; from wfapi_ext import *
XLSX = "/Power Automate Lab Data/Lab 14 - Handover Queue.xlsx"
SCHEMA = {"type": "object", "properties": {
    "clientName": {"type": "string"}, "clientEmail": {"type": "string"}, "accountRef": {"type": "string"},
    "portfolio": {"type": "string"}, "message": {"type": "string"}, "channel": {"type": "string"}},
    "required": ["clientName", "clientEmail", "message"]}
def E(k): return f"outputs('Enquiry')?['{k}']"
def Ei(k): return "@{" + E(k) + "}"
SO = "body('Rapport_Agent')?['structuredOutput']"
def R(k): return f"{SO}?['{k}']"
def Ri(k): return "@{" + R(k) + "}"
FLAGS = f"join(coalesce({R('complianceFlags')}, json('[]')), ', ')"
INSTR = """You are the Client Rapport Assistant for Meridian Asset Management, a licensed fund manager in Singapore. Client relationship managers use you to draft replies to concerned investment clients.

You do not speak to clients. Everything you write is a DRAFT that a licensed relationship manager reads and approves before it is sent. Write as if a regulator will read it, because one might.

## What you must do for every enquiry
1. Classify the concern.
2. Read the client's emotional tone honestly - do not soften it. A furious client is "Angry", not "Concerned".
3. Raise a compliance flag for anything that needs a human's attention.
4. Draft a reply that is warm, specific to what they actually said, and strictly non-advisory.

## THE NON-ADVISORY RULE - this is the rule that matters
You are NOT licensed to give financial advice, and neither is this workflow. In the draft you must NEVER:
- recommend buying, selling, holding, switching or redeeming anything;
- predict, forecast or estimate future returns, prices or NAV;
- guarantee, promise or imply any outcome ("markets always recover", "it will bounce back", "you will not lose money");
- tell the client their portfolio is suitable, unsuitable, safe, risky, or right for them;
- comment on whether now is a good or bad time to invest, redeem or wait;
- name a specific product, fund or asset as a course of action;
- state a fee, NAV, return figure or holding that was not given to you in the enquiry.

You MAY: acknowledge the emotion by name, restate their concern accurately, explain the process and what happens next, describe factual and publicly known context in neutral terms, point to their statement or factsheet, and offer a call with their licensed relationship manager.

When in doubt, say less and offer the call.

## Compliance flags - raise every one that applies
- ADVICE_REQUESTED - the client asks what they should do, or asks you to decide for them.
- GUARANTEE_SOUGHT - the client asks you to promise a return, a recovery, or that they will not lose money.
- COMPLAINT - the client expresses dissatisfaction with Meridian, its staff, its fees or its conduct.
- WITHDRAWAL_INTENT - the client raises redeeming, withdrawing, closing or moving their account.
- VULNERABLE_CLIENT - the client mentions distress, illness, bereavement, retirement savings they cannot afford to lose, or an inability to cope.
- LEGAL_OR_MEDIA_THREAT - the client mentions a lawyer, a regulator, MAS, the press or social media.

Set escalate to true if you raise ANY of: ADVICE_REQUESTED, GUARANTEE_SOUGHT, VULNERABLE_CLIENT, LEGAL_OR_MEDIA_THREAT. Those four cannot be answered by a drafted email alone.

## The draft
draftReply is the body of the letter only: 2 to 4 short paragraphs, each wrapped in <p style="margin:0 0 16px;">.
Do NOT write a greeting, a sign-off, a disclaimer or a reference number - the letterhead, "Dear <name>", the sign-off and the regulatory disclaimer are added automatically by the system and must not be duplicated.

Structure the body: acknowledge what they said and how they feel (first sentence, no throat-clearing) -> give factual, non-advisory context -> say exactly what happens next and offer the call. Under 180 words. Plain English. No exclamation marks, no jargon, no "rest assured", no "unprecedented times".

If you raised ADVICE_REQUESTED or GUARANTEE_SOUGHT, the draft must politely explain that the relationship manager cannot give a recommendation or a guarantee by email, and must offer a call instead.

## Output
Return the structured fields: ticketId, concernCategory, emotionalTone, urgency, complianceFlags, escalate, suggestedSubject, draftReply.
- concernCategory: one of "Portfolio Performance", "Market Volatility", "NAV Fluctuation", "Fees & Charges", "Withdrawal / Redemption", "Statement or Reporting", "Other".
- emotionalTone: one of "Calm", "Concerned", "Anxious", "Frustrated", "Angry", "Distressed".
- urgency: one of "Low", "Medium", "High".
- complianceFlags: an array of the flag strings above (empty array when none).
- suggestedSubject: a short professional subject line ending with the ticket reference in brackets.

## The enquiry to process

A client of Meridian Asset Management has raised a concern.

Ticket: @{outputs('Enquiry')?['ticketId']}
Client: @{outputs('Enquiry')?['clientName']}
Account reference: @{outputs('Enquiry')?['accountRef']}
Portfolio: @{outputs('Enquiry')?['portfolio']}
Channel: @{outputs('Enquiry')?['channel']}
Received: @{outputs('Enquiry')?['receivedAt']}

Their message, verbatim:
\"\"\"
@{outputs('Enquiry')?['message']}
\"\"\"

Classify it, flag it, and draft the relationship manager's reply."""
OUT_SCHEMA = {"type": "object", "properties": {
    "ticketId": {"type": "string"},
    "concernCategory": {"type": "string", "enum": ["Portfolio Performance", "Market Volatility", "NAV Fluctuation", "Fees & Charges", "Withdrawal / Redemption", "Statement or Reporting", "Other"]},
    "emotionalTone": {"type": "string", "enum": ["Calm", "Concerned", "Anxious", "Frustrated", "Angry", "Distressed"]},
    "urgency": {"type": "string", "enum": ["Low", "Medium", "High"]},
    "complianceFlags": {"type": "array", "items": {"type": "string"}},
    "escalate": {"type": "boolean"},
    "suggestedSubject": {"type": "string"},
    "draftReply": {"type": "string"}},
    "required": ["ticketId", "concernCategory", "emotionalTone", "urgency", "complianceFlags", "escalate", "suggestedSubject", "draftReply"]}
LETTER = ("<div style=\"max-width:620px;font-family:Arial,Helvetica,sans-serif;color:#1b2733;font-size:15px;line-height:1.65;\">"
          "<div style=\"background:#10243e;padding:20px 28px;color:#ffffff;font-size:17px;font-weight:bold;\">Meridian Asset Management"
          "<div style=\"color:#8fa6c0;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;margin-top:6px;font-weight:normal;\">Client Relationship Team &middot; Singapore</div></div>"
          f"<div style=\"padding:28px;\"><p style=\"margin:0 0 18px;\">Dear {Ei('clientName')},</p>{Ri('draftReply')}"
          f"<p style=\"margin:20px 0 4px;\">Reference: <b>{Ei('ticketId')}</b><br>Portfolio: <b>{Ei('portfolio')}</b></p>"
          "<p style=\"margin:16px 0 4px;\">Yours sincerely,</p><p style=\"margin:0;font-weight:bold;\">Client Relationship Team</p>"
          "<p style=\"margin:2px 0 0;color:#5b6b7b;font-size:13px;\">Meridian Asset Management, Singapore &middot; +65 6800 5678</p></div>"
          "<div style=\"background:#f5f7fa;border-top:1px solid #e3e8ee;padding:18px 28px;color:#5b6b7b;font-size:11.5px;line-height:1.6;\">"
          "<p style=\"margin:0 0 8px;\"><strong>Important.</strong> This email is provided for information only. It does not constitute financial advice, an offer, or a recommendation to buy, sell or hold any investment product, and it does not take account of your objectives, financial situation or particular needs. Past performance is not indicative of future performance. The value of investments and the income from them may fall as well as rise, and you may not get back the amount you invested.</p>"
          "<p style=\"margin:0 0 8px;\">This message was drafted with assistance from an AI system and reviewed and approved by a licensed representative of Meridian Asset Management before it was sent.</p>"
          "<p style=\"margin:0;color:#8b98a5;\">Meridian Asset Management is a fictitious institution created for a training course. No investment service is offered and no advice of any kind is given.</p></div></div>")
def build():
    wf = Workflow("Lab 14 - HTTP and Human Review (DO NOT DELETE)")
    s = wf.start_http(schema=SCHEMA)
    enq = wf.compose("Enquiry", "@" + obj_expr({
        "ticketId": "concat('MAM-', formatDateTime(utcNow(),'yyyyMMdd'), '-', substring(replace(guid(),'-',''),0,6))",
        "receivedAt": "utcNow()",
        "clientName": "trim(triggerBody()?['clientName'])",
        "clientEmail": "toLower(trim(triggerBody()?['clientEmail']))",
        "accountRef": "toUpper(trim(coalesce(triggerBody()?['accountRef'],'')))",
        "portfolio": "coalesce(triggerBody()?['portfolio'],'Not stated')",
        "channel": "coalesce(triggerBody()?['channel'],'Website chat')",
        "message": "trim(triggerBody()?['message'])"}))
    a = wf.agent("Rapport Agent", INSTR, output_mode="structured", schema=OUT_SCHEMA, web_search=False)
    r = wf.response("Response", body="@" + obj_expr({
        "status": "'received'", "ticketId": E('ticketId'), "urgency": R('urgency'),
        "escalated": Raw(f"toLower(string({R('escalate')}))"),
        "message": "'Thank you. Your message has reached the Meridian client relationship team and has been logged under the reference below. A licensed relationship manager will review it personally and reply to you by email. We do not send investment advice through this chat.'"}))
    log = wf.connector("Log draft", "shared_excelonlinebusiness", "AddRowV2",
                       {"source": "me", "drive": "me", "file": XLSX, "table": "Drafts",
                        "item/Reference": Ei('ticketId'), "item/Timestamp": "@{utcNow()}", "item/Client": f"{Ei('clientName')} <{Ei('clientEmail')}>",
                        "item/Enquiry": Ei('message'), "item/Draft": Ri('draftReply'), "item/Urgency": Ri('urgency'),
                        "item/Flags": "@{" + FLAGS + "}", "item/Escalate": Ri('escalate'), "item/Status": "Awaiting human review", "item/ApprovedBy": ""})
    hr = wf.human_review("Human review",
        title=f"@{{if(equals(toLower(string(coalesce({R('escalate')}, false))), 'true'), '[ESCALATE] ', '[REVIEW] ')}}Draft reply to {Ei('clientName')} ({Ei('ticketId')})",
        message=(f"APPROVAL REQUIRED - draft reply to a client\n\nTicket: {Ei('ticketId')}\nClient: {Ei('clientName')} <{Ei('clientEmail')}>\n"
                 f"Account: {Ei('accountRef')} - {Ei('portfolio')}\n\nAGENT ASSESSMENT\nCategory: {Ri('concernCategory')}\nTone: {Ri('emotionalTone')}\n"
                 f"Urgency: {Ri('urgency')}\nFlags: @{{{FLAGS}}}\nEscalate: {Ri('escalate')}\n\nCLIENT SAID\n{Ei('message')}\n\nPROPOSED SUBJECT\n{Ri('suggestedSubject')}\n\n"
                 f"PROPOSED REPLY\n{Ri('draftReply')}\n\n----\nOutcome = Yes: send this reply to the client as-is. Outcome = No: hand the ticket to a human agent who will call the client instead. "
                 "Enter your name so the approval is recorded. You are the licensed representative. Nothing reaches the client unless you approve it."),
        inputs=[("Outcome", "boolean"), ("Name", "text")], channel="Teams")
    cond, yes, no = wf.if_else("Outcome is Yes", ("@outputs('Human_review')?['body/boolean']", "equals", "Yes"))
    send = wf.connector("Send approved reply", "shared_office365", "SendEmailV2",
                        {"emailMessage/To": "@" + E('clientEmail'), "emailMessage/Subject": Ri('suggestedSubject'),
                         "emailMessage/Body": LETTER, "emailMessage/Importance": "Normal"}, y=100)
    handover = wf.connector("Assign to human agent", "shared_excelonlinebusiness", "AddRowV2",
                       {"source": "me", "drive": "me", "file": XLSX, "table": "HandoverQueue",
                        "item/Reference": Ei('ticketId'), "item/Timestamp": "@{utcNow()}", "item/Client": f"{Ei('clientName')} <{Ei('clientEmail')}>",
                        "item/Enquiry": Ei('message'),
                        "item/Reason": f"Draft declined by @{{outputs('Human_review')?['body/text']}}. Flags: @{{{FLAGS}}}. Tone: {Ri('emotionalTone')}.",
                        "item/Owner": TRAINER_EMAIL}, y=420)
    wf.chain(s, enq, a, r, log, hr, cond)
    wf.edge(cond, send, source_handle=yes); wf.edge(cond, handover, source_handle=no)
    return wf
if __name__ == '__main__':
    wid = create(build())
    ids = json.load(open(SCRATCH + '/ids.json')); ids['lab14'] = wid; json.dump(ids, open(SCRATCH + '/ids.json', 'w'), indent=1)
    print(designer_url(wid))
