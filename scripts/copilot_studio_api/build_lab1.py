"""Lab 1 - Trigger and Actions (DO NOT DELETE): Forms trigger -> Get response details -> Send an email. Verified published 2026-09-04."""
import sys, json; sys.path.insert(0, __import__('os').path.dirname(__file__))
from wfapi import *
cd=json.load(open(SCRATCH+'/lab1-clientdata.json'))
g=cd['properties']['definition']['triggers']['When_a_new_response_is_submitted']['metadata']['associatedData']['graph']
grd_schema=[n for n in g['nodes'] if n['type']=='connector'][0]['data']['outcomes'][0]['outcomeSchema']
trig_schema=g['nodes'][0]['data']['outcomes'][0]['outcomeSchema']
Q={'Name':'ra7b2b2c768fe4bbfae38bd8bc152cb04','Email':'r34f434c08f984a8fa4bb1d0033e55dd3','Tel':'r07b82f997fa545ab86bb3b7879fa7e96','Message':'rf5e39878c6694d9d9bbe3fdfe7840b5b'}
def q(k): return f"@outputs('Get_response_details')?['body/{Q[k]}']"
def qi(k): return "@{" + q(k)[1:] + "}"
def build():
    wf = Workflow("Lab 1 - Trigger and Actions (DO NOT DELETE)")
    s = wf.start_connector("When a new response is submitted", "shared_microsoftforms", "CreateFormWebhook", {"form_id": FORM_LAB1}, split_on="@triggerOutputs()?['body/value']")
    wf.nodes[0]['data']['outcomes'][0]['outcomeSchema']=trig_schema
    ui_conn=g['nodes'][0]['data']['config']['connector']
    for k in ('parametersSchema','outputSchema','triggerBatchMode','iconUri'):
        wf.nodes[0]['data']['config']['connector'][k]=ui_conn[k]
    n1 = wf.connector("Get response details", "shared_microsoftforms", "GetFormResponseById", {"form_id": FORM_LAB1, "response_id": "@triggerOutputs()?['body/resourceData/responseId']"}, alias="shared_microsoftforms-1")
    wf.nodes[-1]['data']['outcomes'][0]['outcomeSchema']=grd_schema
    n2 = wf.connector("Send an email", "shared_office365", "SendEmailV2",
         {"emailMessage/To": q('Email'), "emailMessage/Subject": "Thank you for your enquiry",
          "emailMessage/Body": f"<p>Hello {qi('Name')},</p><p>Thank you for your enquiry. We received the following message:</p><p>{qi('Message')}</p><p>We will contact you shortly.</p><p>ACME Pte Ltd Training Team</p>",
          "emailMessage/Importance": "Normal"})
    wf.chain(s, n1, n2)
    return wf
if __name__ == '__main__':
    print(designer_url(create(build())))
