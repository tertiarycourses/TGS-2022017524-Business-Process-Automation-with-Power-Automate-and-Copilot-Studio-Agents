"""Lab 2 - Log to Excel (DO NOT DELETE): Forms trigger (Lab 1 form) -> Get response details -> Excel Add a row into a table
(Lab 2 - Enquiry Log.xlsx / EnquiryLog) -> Send an email (V2) saying the enquiry was logged."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *

NAME = "Lab 2 - Log to Excel (DO NOT DELETE)"
Q = {'Name': 'ra7b2b2c768fe4bbfae38bd8bc152cb04', 'Email': 'r34f434c08f984a8fa4bb1d0033e55dd3',
     'Tel': 'r07b82f997fa545ab86bb3b7879fa7e96', 'Message': 'rf5e39878c6694d9d9bbe3fdfe7840b5b'}
EXCEL = json.load(open(SCRATCH + "/excel-params.json")) if os.path.exists(SCRATCH + "/excel-params.json") else {}
# until the file/table ids are resolved once in the designer (see FORMATS.md), use the OneDrive path form
EX = EXCEL.get("lab2") or {"source": "me", "drive": "me", "file": "/Power Automate Lab Data/Lab 2 - Enquiry Log.xlsx", "table": "EnquiryLog"}

_cd = json.load(open(SCRATCH + '/lab1-clientdata.json'))
_g = _cd['properties']['definition']['triggers']['When_a_new_response_is_submitted']['metadata']['associatedData']['graph']
UI_CONN = _g['nodes'][0]['data']['config']['connector']            # Forms trigger config saved once by the UI (schemas + batch mode)
TRIG_SCHEMA = _g['nodes'][0]['data']['outcomes'][0]['outcomeSchema']
GRD_SCHEMA = [n for n in _g['nodes'] if n['type'] == 'connector'][0]['data']['outcomes'][0]['outcomeSchema']

def q(k): return f"@outputs('Get_response_details')?['body/{Q[k]}']"
def qi(k): return "@{" + q(k)[1:] + "}"

def build():
    wf = Workflow(NAME)
    s = wf.start_connector("When a new response is submitted", "shared_microsoftforms", "CreateFormWebhook",
                           {"form_id": FORM_LAB1}, split_on="@triggerOutputs()?['body/value']",
                           ui_connector=UI_CONN, outcome_schema=TRIG_SCHEMA)
    n1 = wf.connector("Get response details", "shared_microsoftforms", "GetFormResponseById",
                      {"form_id": FORM_LAB1, "response_id": "@triggerOutputs()?['body/resourceData/responseId']"},
                      alias="shared_microsoftforms-1")
    wf.nodes[-1]['data']['outcomes'][0]['outcomeSchema'] = GRD_SCHEMA
    xl = wf.connector("Add a row into a table", "shared_excelonlinebusiness", "AddRowV2",
        {"source": EX["source"], "drive": EX["drive"], "file": EX["file"], "table": EX["table"],
         "item/Timestamp": "@utcNow()", "item/Name": q('Name'), "item/Email": q('Email'), "item/Tel": q('Tel'),
         "item/Message": q('Message'), "item/Status": "New", "item/Source": "Lab 1 - Course Enquiry Form"})
    n2 = wf.connector("Send an email", "shared_office365", "SendEmailV2",
        {"emailMessage/To": q('Email'), "emailMessage/Subject": "Thank you for your enquiry",
         "emailMessage/Body": (f"<p>Hello {qi('Name')},</p><p>Thank you for your enquiry. We received the following message:</p>"
                               f"<p>{qi('Message')}</p><p>Your enquiry has been logged and will be reviewed by our training team.</p>"
                               "<p>ACME Pte Ltd Training Team</p>"),
         "emailMessage/Importance": "Normal"})
    wf.chain(s, n1, xl, n2)
    return wf

if __name__ == '__main__':
    wf = build()
    ids = json.load(open(SCRATCH + "/ids.json"))
    if ids.get("lab2") and os.environ.get("UPDATE"):
        update(ids["lab2"], wf); wid = ids["lab2"]
    else:
        wid = create(wf); ids["lab2"] = wid; json.dump(ids, open(SCRATCH + "/ids.json", "w"), indent=1)
    print(designer_url(wid))
