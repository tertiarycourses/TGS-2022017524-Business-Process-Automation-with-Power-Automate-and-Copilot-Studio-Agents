"""Lab 3 - Leave Application Approval (DO NOT DELETE).
Forms trigger (Lab 3 form) -> Get response details -> Human review (Teams) -> If Outcome = Yes -> approved email / rejected email.
Stage 1 (STAGE=1): trigger + Get response details only, to learn the question ids from the designer-saved outcomeSchema.
Stage 2 (default): full build using the ids in Q3 below."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *

NAME = "Lab 3 - Leave Application Approval (DO NOT DELETE)"
# question ids of "Lab 3 - Leave Application Form" (filled after stage 1; see FORMATS.md)
Q3 = json.load(open(SCRATCH + "/lab3-questions.json")) if os.path.exists(SCRATCH + "/lab3-questions.json") else {}
EXCEL = json.load(open(SCRATCH + "/excel-params.json")) if os.path.exists(SCRATCH + "/excel-params.json") else None

_cd = json.load(open(SCRATCH + '/lab1-clientdata.json'))
_g = _cd['properties']['definition']['triggers']['When_a_new_response_is_submitted']['metadata']['associatedData']['graph']
UI_CONN = _g['nodes'][0]['data']['config']['connector']            # Forms trigger config saved once by the UI (schemas + batch mode)
TRIG_SCHEMA = _g['nodes'][0]['data']['outcomes'][0]['outcomeSchema']
# Get response details outcome schema for the Lab 3 form (captured from the stage-1 designer save)
GRD_SCHEMA = None
if os.path.exists(SCRATCH + '/lab3-stage1-clientdata.json'):
    _g3 = json.load(open(SCRATCH + '/lab3-stage1-clientdata.json'))['properties']['definition']['triggers']['When_a_new_response_is_submitted']['metadata']['associatedData']['graph']
    GRD_SCHEMA = [n for n in _g3['nodes'] if n['name'] == 'Get response details'][0]['data']['outcomes'][0]['outcomeSchema']

def q(k): return f"@outputs('Get_response_details')?['body/{Q3[k]}']"
def qi(k): return "@{" + q(k)[1:] + "}"

def build(stage=2):
    wf = Workflow(NAME)
    s = wf.start_connector("When a new response is submitted", "shared_microsoftforms", "CreateFormWebhook",
                           {"form_id": FORM_LAB3}, split_on="@triggerOutputs()?['body/value']",
                           ui_connector=UI_CONN, outcome_schema=TRIG_SCHEMA)
    n1 = wf.connector("Get response details", "shared_microsoftforms", "GetFormResponseById",
                      {"form_id": FORM_LAB3, "response_id": "@triggerOutputs()?['body/resourceData/responseId']"},
                      alias="shared_microsoftforms-1")
    if GRD_SCHEMA: wf.nodes[-1]['data']['outcomes'][0]['outcomeSchema'] = GRD_SCHEMA
    wf.chain(s, n1)
    if stage == 1:
        return wf
    hr = wf.human_review("Manager approval",
        title=f"Leave request - {qi('Name')}",
        message=("Applicant name: " + qi('Name') + "\nLeave from date: " + qi('From') + "\nLeave end date: " + qi('To') +
                 "\nLeave type: " + qi('Type') + "\nReason: " + qi('Reason') +
                 "\n\nChoose Yes to approve the leave request, No to reject it. Add your comments for the applicant."),
        assigned_to=TRAINER_EMAIL, inputs=[("Outcome", "boolean"), ("Comments", "text")], channel="Teams")
    wf.edge(n1, hr)
    prev = hr
    if EXCEL and EXCEL.get("lab3"):
        ex = EXCEL["lab3"]
        xl = wf.connector("Add a row into a table", "shared_excelonlinebusiness", "AddRowV2",
              {"source": ex["source"], "drive": ex["drive"], "file": ex["file"], "table": ex["table"],
               "item/Timestamp": "@utcNow()", "item/Name": q('Name'), "item/Leave Type": q('Type'),
               "item/From": q('From'), "item/To": q('To'), "item/Reason": q('Reason'),
               "item/Decision": "@outputs('Manager_approval')?['body/boolean']",
               "item/Comments": "@outputs('Manager_approval')?['body/text']",
               "item/Approver": TRAINER_EMAIL})
        wf.edge(hr, xl); prev = xl
    ie, yes_h, else_h = wf.if_else("Outcome is Yes", ("@outputs('Manager_approval')?['body/boolean']", "equals", "Yes"))
    wf.edge(prev, ie)
    ok = wf.connector("Send an email approved", "shared_office365", "SendEmailV2",
        {"emailMessage/To": "@outputs('Get_response_details')?['body/responder']",
         "emailMessage/Subject": "Leave request approved",
         "emailMessage/Body": ("<p>Hello " + qi('Name') + ",</p><p>Your " + qi('Type') + " leave request from " + qi('From') +
                               " to " + qi('To') + " has been <b>approved</b>.</p><p>Manager's comments: " +
                               "@{outputs('Manager_approval')?['body/text']}</p><p>Training Office</p>"),
         "emailMessage/Importance": "Normal"}, y=120)
    no = wf.connector("Send an email rejected", "shared_office365", "SendEmailV2",
        {"emailMessage/To": "@outputs('Get_response_details')?['body/responder']",
         "emailMessage/Subject": "Leave request not approved",
         "emailMessage/Body": ("<p>Hello " + qi('Name') + ",</p><p>Your " + qi('Type') + " leave request from " + qi('From') +
                               " to " + qi('To') + " has <b>not been approved</b>.</p><p>Manager's comments: " +
                               "@{outputs('Manager_approval')?['body/text']}</p><p>Please contact your manager if you need clarification.</p><p>Training Office</p>"),
         "emailMessage/Importance": "Normal"}, y=400)
    wf.edge(ie, ok, source_handle=yes_h)
    wf.edge(ie, no, source_handle=else_h)
    return wf

if __name__ == '__main__':
    stage = int(os.environ.get("STAGE", "2"))
    wf = build(stage)
    ids = json.load(open(SCRATCH + "/ids.json"))
    wid = create(wf); ids["lab3"] = wid; json.dump(ids, open(SCRATCH + "/ids.json", "w"), indent=1)
    print(designer_url(wid))
