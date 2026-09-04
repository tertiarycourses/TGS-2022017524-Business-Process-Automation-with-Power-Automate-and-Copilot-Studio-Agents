"""Lab 4 - Email Classification (DO NOT DELETE): Outlook 'When a new email arrives (V3)' -> Classify (Priority, Meeting,
Need Reply, Informational + built-in Other) -> per-category handlers exactly as labs/Lab 4 - Email Classification/index.md."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *

NAME = "Lab 4 - Email Classification (DO NOT DELETE)"
OUTLOOK = json.load(open(SCRATCH + "/outlook-params.json")) if os.path.exists(SCRATCH + "/outlook-params.json") else {}
CALENDAR = OUTLOOK.get("calendar", "Calendar")
OTHER_FOLDER = OUTLOOK.get("otherFolder", "Lab 4 - Other")
MODEL = "claude-sonnet-4.6"   # lab doc: Claude Sonnet 4.6 for Classify + the three Agent nodes

def T(field): return f"@{{triggerOutputs()?['body/{field}']}}"   # interpolated trigger token
def TT(field): return f"@triggerOutputs()?['body/{field}']"     # whole-field trigger token

CLASSIFY_INPUT = ("Classify the email below into exactly one category. Read the subject, the sender, the importance flag and the body. "
                  "Pick the FIRST category that applies, in the order the categories are listed.\n\n"
                  f"Subject: {T('subject')}\nFrom: {T('from')}\nImportance flag: {T('importance')}\nBody:\n{T('body')}")
CATS = [("Priority", "An email that is time-sensitive and needs action within 24 hours: a deadline, an outage, a complaint, a payment or contract at risk, the words urgent or ASAP, or a high-importance flag with a request for action."),
        ("Meeting", "An email asking to schedule, reschedule or confirm a meeting, call or visit."),
        ("Need Reply", "An email that asks a question or makes a request that expects an answer, but is not urgent and is not about scheduling a meeting."),
        ("Informational", "Newsletters, notifications, receipts, announcements, FYI messages and thank-you notes that need no action.")]

MEETING_INSTR = ("The email below asks for a meeting. Work out the meeting the sender wants and fill every output field. Do not explain your reasoning.\n\n"
 f"From: {T('from')}\nSubject: {T('subject')}\nReceived at: {T('receivedDateTime')}\nBody:\n{T('body')}\n\n"
 "Field rules:\n- meetingTitle: a short calendar subject in the form \"Discussion: <topic> with <sender's first name>\".\n"
 "- meetingStart and meetingEnd: Singapore local time in the format YYYY-MM-DDTHH:MM:SS with no time-zone suffix. If the sender proposes a date and time, use it. "
 "If the sender proposes only a day, use 10:00 on that day. If no time is given, use 10:00 on the next working day after the received date. Default duration is 30 minutes unless the email states another duration.\n"
 "- agenda: one or two plain sentences saying what the meeting is about, taken from the email. Never invent facts that are not in the email.")
MEETING_SCHEMA = {"type": "object", "properties": {
    "meetingTitle": {"type": "string"},
    "meetingStart": {"type": "string", "description": "YYYY-MM-DDTHH:MM:SS, Singapore local time, no suffix"},
    "meetingEnd": {"type": "string", "description": "YYYY-MM-DDTHH:MM:SS, Singapore local time, no suffix"},
    "agenda": {"type": "string"}}, "required": ["meetingTitle", "meetingStart", "meetingEnd", "agenda"]}

REPLY_INSTR = ("You write email replies on behalf of the Training Office at Tertiary Infotech Academy, Singapore. Produce ONLY the body of the reply, as plain text with normal paragraphs. "
 "No subject line, no markdown, no bullet symbols, no preamble such as \"Here is the reply\".\n\n"
 f"Original email\nFrom: {T('from')}\nSubject: {T('subject')}\nBody:\n{T('body')}\n\n"
 "Instructions\n- Start with \"Dear\" followed by the sender's first name taken from the From line; if no name is visible, use \"Dear Sir or Madam\".\n"
 "- Answer the sender's actual question or request. If the answer requires information you do not have (prices, dates, availability, policies), say that a colleague will confirm within one working day — do not invent the detail.\n"
 "- Keep it to three to six sentences, warm and professional, Singapore English.\n"
 "- End with \"Kind regards,\" on its own line followed by \"Training Office\" on the next line.\n"
 "- Never include citation markers, reference numbers or source tags.")

TRIAGE_INSTR = ("The email below has been classified as priority. Summarise it for a busy manager and draft the reply that should go back to the sender once a person has approved it. Do not explain your reasoning.\n\n"
 f"From: {T('from')}\nSubject: {T('subject')}\nImportance flag: {T('importance')}\nBody:\n{T('body')}\n\n"
 "Field rules:\n- summary: one or two plain sentences saying who needs what, and by when.\n"
 "- suggestedReply: a complete reply of three to six sentences addressed to the sender by first name, acknowledging the urgency, saying what will happen next, and signed \"Kind regards, Training Office\". "
 "Never promise a specific outcome, refund or time you cannot know. Never invent facts that are not in the email.\n"
 "- Never include citation markers, reference numbers or source tags.")
TRIAGE_SCHEMA = {"type": "object", "properties": {"summary": {"type": "string"}, "suggestedReply": {"type": "string"}}, "required": ["summary", "suggestedReply"]}

def build():
    wf = Workflow(NAME)
    s = wf.start_connector("When a new email arrives (V3)", "shared_office365", "OnNewEmailV3",
                           {"folderPath": "Inbox", "importance": "Any", "fetchOnlyWithAttachment": False, "includeAttachments": False},
                           operation_type="OpenApiConnectionNotification", split_on="@triggerOutputs()?['body/value']")
    cid, cats = wf.classify("Classify email", CLASSIFY_INPUT, [c for c, _ in CATS], model=MODEL)
    # category descriptions (if the node supports them)
    for c in wf.nodes[-1]["data"]["config"]["categories"]:
        c["description"] = dict(CATS)[c["name"]]
    wf.edge(s, cid)
    # --- Meeting ---
    mh = wf.agent("Meeting Handler", MEETING_INSTR, model=MODEL, output_mode="structured", schema=MEETING_SCHEMA, y=-300)
    ev = wf.connector("Create Meeting", "shared_office365", "CalendarPostItem_V4",
        {"calendar": CALENDAR, "item/subject": "@outputs('Meeting_Handler')?['body/structuredOutput/meetingTitle']",
         "item/start": "@outputs('Meeting_Handler')?['body/structuredOutput/meetingStart']",
         "item/end": "@outputs('Meeting_Handler')?['body/structuredOutput/meetingEnd']",
         "item/timeZone": "(UTC+08:00) Kuala Lumpur, Singapore", "item/requiredAttendees": TT('from'),
         "item/body": "@outputs('Meeting_Handler')?['body/structuredOutput/agenda']", "item/isOnlineMeeting": True}, y=-300)
    rb = wf.connector("Reply Meeting Booked", "shared_office365", "ReplyToV3",
        {"messageId": TT('id'),
         "replyParameters/Body": ("Thanks — I have placed a meeting on our calendars: @{outputs('Meeting_Handler')?['body/structuredOutput/meetingTitle']} starting "
                                  "@{outputs('Meeting_Handler')?['body/structuredOutput/meetingStart']}. Please let me know if the slot does not work."),
         "replyParameters/ReplyAll": False}, y=-300)
    wf.edge(cid, mh, source_handle=cats["Meeting"]); wf.chain(mh, ev, rb)
    # --- Need Reply ---
    wf._x = 250 + 350 * 2
    rd = wf.agent("Reply Drafter", REPLY_INSTR, model=MODEL, output_mode="text", y=-100)
    sr = wf.connector("Send Drafted Reply", "shared_office365", "ReplyToV3",
        {"messageId": TT('id'), "replyParameters/Body": "@outputs('Reply_Drafter')?['body/message']", "replyParameters/ReplyAll": False}, y=-100)
    wf.edge(cid, rd, source_handle=cats["Need Reply"]); wf.chain(rd, sr)
    # --- Priority ---
    wf._x = 250 + 350 * 2
    pt = wf.agent("Priority Triage", TRIAGE_INSTR, model=MODEL, output_mode="structured", schema=TRIAGE_SCHEMA, y=150)
    hr = wf.human_review("Priority check", title="Priority check",
        message=("A priority email needs your decision.\n" f"From: {T('from')}\nSubject: {T('subject')}\n"
                 "Summary: @{outputs('Priority_Triage')?['body/structuredOutput/summary']}\n"
                 "Proposed reply: @{outputs('Priority_Triage')?['body/structuredOutput/suggestedReply']}\n\n"
                 "Choose Yes to send the proposed reply now. Choose No to hand it to the trainer.\nType your name so the reply records who approved it."),
        assigned_to=TRAINER_EMAIL, inputs=[("Outcome", "boolean"), ("Name", "text")], channel="Teams", y=150)
    ie, yes_h, else_h = wf.if_else("Outcome Equals Yes", ("@outputs('Priority_check')?['body/boolean']", "equals", "Yes"), y=150)
    ar = wf.connector("Send Approved Reply", "shared_office365", "ReplyToV3",
        {"messageId": TT('id'),
         "replyParameters/Body": "@{outputs('Priority_Triage')?['body/structuredOutput/suggestedReply']}\nApproved by: @{outputs('Priority_check')?['body/text']}",
         "replyParameters/ReplyAll": False}, y=60)
    wf._x -= 350
    et = wf.connector("Escalate To Trainer", "shared_office365", "SendEmailV2",
        {"emailMessage/To": TRAINER_EMAIL, "emailMessage/Subject": f"Escalation: {T('subject')}",
         "emailMessage/Body": ("<p>Rejected by @{outputs('Priority_check')?['body/text']}. Original sender: " + T('from') +
                               ". Summary: @{outputs('Priority_Triage')?['body/structuredOutput/summary']}</p>"),
         "emailMessage/Importance": "High"}, y=260)
    wf.edge(cid, pt, source_handle=cats["Priority"]); wf.chain(pt, hr, ie)
    wf.edge(ie, ar, source_handle=yes_h); wf.edge(ie, et, source_handle=else_h)
    # --- Informational ---
    wf._x = 250 + 350 * 2
    fl = wf.connector("Flag Info", "shared_office365", "FlagV2", {"messageId": TT('id')}, y=450)
    wf.edge(cid, fl, source_handle=cats["Informational"])
    # --- Other ---
    wf._x = 250 + 350 * 2
    mv = wf.connector("Move To Other", "shared_office365", "MoveV2", {"messageId": TT('id'), "folderPath": OTHER_FOLDER}, y=600)
    wf.edge(cid, mv, source_handle="default-category")
    return wf

if __name__ == '__main__':
    wf = build()
    ids = json.load(open(SCRATCH + "/ids.json"))
    if ids.get("lab4") and os.environ.get("UPDATE"):
        update(ids["lab4"], wf); wid = ids["lab4"]
    else:
        wid = create(wf); ids["lab4"] = wid; json.dump(ids, open(SCRATCH + "/ids.json", "w"), indent=1)
    print(designer_url(wid))
