"""Lab 16 - RAG with Pinecone (DO NOT DELETE): HTTP trigger -> HTTP (Pinecone records search) -> Compose Brochures -> Agent -> Response {reply}.
The Pinecone API key is NOT available to the build agent: header Api-Key is the literal placeholder PASTE-PINECONE-API-KEY, and the index
host is the lab doc's placeholder lab16-course-brochures-XXXXXX.svc.aped-4627-b74a.pinecone.io — both must be replaced by the trainer."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *; from wfapi_ext import *
PINECONE_HOST = "lab16-course-brochures-XXXXXX.svc.aped-4627-b74a.pinecone.io"
PINECONE_URL = f"https://{PINECONE_HOST}/records/namespaces/__default__/search"
Q = "coalesce(triggerBody()?['question'], triggerBody()?['message'], triggerBody()?['chatInput'])"
INSTR = """You are the customer care assistant for Cook & Bake Academy, a cooking and bakery school in Singapore.

Answer the customer's question using only the course brochures provided below. They are the only knowledge you have.

If the brochures do not answer the question, say "I don't have that in our course information" and offer the team on +65 6888 1234 or enrol@cookbakeacademy.sg.

Never invent a fee, a date, a duration, a course code, an instructor name or a discount. If a number is not in a brochure, you do not know it.

If we do not run a course, say so plainly, then list the two or three closest courses we do run.

Always give the course code (for example BAK-101) next to the course title. Quote fees in Singapore dollars exactly as written.

Be warm and brief - two to four short sentences. Never mention brochures, searching, or that you are reading documents.

COURSE BROCHURES AND CUSTOMER QUESTION:
@{outputs('Brochures')}"""
def build():
    wf = Workflow("Lab 16 - RAG with Pinecone (DO NOT DELETE)")
    s = wf.start_http(schema={"type": "object", "properties": {
        "question": {"type": "string"}, "message": {"type": "string"}, "chatInput": {"type": "string"},
        "history": {"type": "string"}, "sessionId": {"type": "string"}, "source": {"type": "string"}}})
    # {"query":{"inputs":{"text":<q>},"top_k":3},"fields":["course_code","chunk_text"]} built as an object expression (no hand-quoting of the question)
    body = "@" + obj_expr({"query": Raw(obj_expr({"inputs": Raw(obj_expr({"text": Q})), "top_k": Raw("3")})),
                           "fields": Raw("createArray('course_code','chunk_text')")})
    h = wf.http("HTTP", method="POST", uri=PINECONE_URL,
                headers={"Api-Key": "PASTE-PINECONE-API-KEY", "Content-Type": "application/json", "X-Pinecone-Api-Version": "2025-04"},
                body=body)
    c = wf.compose("Brochures", "@{concat('Customer question: ', " + Q + ", '\n\nCourse brochures:\n', string(body('HTTP')))}")
    a = wf.agent("Agent", INSTR, output_mode="text", web_search=False)
    r = wf.response("Response", body="@" + obj_expr({"reply": "body('Agent')?['message']"}))
    wf.chain(s, h, c, a, r)
    return wf
if __name__ == '__main__':
    wid = create(build())
    ids = json.load(open(SCRATCH + '/ids.json')); ids['lab16'] = wid; json.dump(ids, open(SCRATCH + '/ids.json', 'w'), indent=1)
    print(designer_url(wid))
