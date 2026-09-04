"""Lab 15 - RAG with Knowledge Base (DO NOT DELETE): HTTP trigger -> Agent (SharePoint knowledge 'Lab 15 - Course Brochures') -> Response {reply}."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *; from wfapi_ext import *
SITE = "https://tertiaryinfotech.sharepoint.com/sites/WSQCourses"
KB = SITE + "/Shared%20Documents/Lab%2015%20-%20Course%20Brochures"
Q = "coalesce(triggerBody()?['question'], triggerBody()?['message'], triggerBody()?['chatInput'])"
INSTR = """You are the customer care assistant for Cook & Bake Academy, a cooking and bakery school in Singapore.

Search your knowledge source for the Cook & Bake Academy course brochures and answer from what you find there. They are the only knowledge you have.

If the brochures do not answer the question, say "I don't have that in our course information" and offer the team on +65 6888 1234 or enrol@cookbakeacademy.sg.

Never invent a fee, a date, a duration, a course code, an instructor name or a discount. If a number is not in a brochure, you do not know it.

If we do not run a course, say so plainly, then list the two or three closest courses we do run.

Always give the course code (for example BAK-101) next to the course title. Quote fees in Singapore dollars exactly as written.

Be warm and brief - two to four short sentences. Never mention brochures, searching, or that you are reading documents.

Never include citation markers, reference numbers or source tags in your reply.

Customer question:
@{""" + Q + "}"
def build():
    wf = Workflow("Lab 15 - RAG with Knowledge Base (DO NOT DELETE)")
    s = wf.start_http(schema={"type": "object", "properties": {
        "question": {"type": "string"}, "message": {"type": "string"}, "chatInput": {"type": "string"},
        "history": {"type": "string"}, "sessionId": {"type": "string"}, "source": {"type": "string"}}})
    a = wf.agent("Agent", INSTR, output_mode="text", web_search=False)
    wf.add_knowledge(a, "Lab 15 - Course Brochures", KB)
    r = wf.response("Response", body="@" + obj_expr({"reply": "body('Agent')?['message']"}))
    wf.chain(s, a, r)
    return wf
if __name__ == '__main__':
    wid = create(build())
    ids = json.load(open(SCRATCH + '/ids.json')); ids['lab15'] = wid; json.dump(ids, open(SCRATCH + '/ids.json', 'w'), indent=1)
    print(designer_url(wid))
