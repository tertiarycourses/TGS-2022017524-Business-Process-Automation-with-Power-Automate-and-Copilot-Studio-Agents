"""Lab 11 - Blog Writer Tool (DO NOT DELETE): When an agent calls the flow (Topic) -> Copilot (M365 Copilot) drafts the post
-> Respond to the agent (BlogPost)."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *
from wfapi_a import *

NAME = "Lab 11 - Blog Writer Tool (DO NOT DELETE)"
PROMPT = ("Write a short, engaging blog post of about 300 words on the topic below. Give it a title line, a two-sentence introduction, "
          "three short paragraphs with one key point each, and a one-sentence conclusion. Write in plain professional English for a "
          "general business audience.\n\nTopic: @{triggerBody()?['Topic']}")
SCHEMA = {"type": "object", "properties": {"Topic": {"title": "Topic", "type": "string", "x-ms-content-hint": "TEXT",
                                                     "x-ms-dynamically-added": True, "description": "The subject of the blog post"}},
          "required": ["Topic"]}

def build(stage=2):
    wf = Workflow(NAME)
    s = wf.start_agent_call(schema=SCHEMA)
    c = wf.m365copilot_connected("Draft the blog post", PROMPT)
    wf.chain(s, c)
    if stage >= 2 and hasattr(wf, "respond_to_agent"):
        r = wf.respond_to_agent("Respond to the agent", {"BlogPost": "@outputs('Draft_the_blog_post')?['body/response']"})
        wf.edge(c, r)
    return wf

if __name__ == '__main__':
    stage = int(os.environ.get("STAGE", "2"))
    wf = build(stage)
    ids = json.load(open(SCRATCH + "/ids.json"))
    wid = create(wf); ids["lab11"] = wid; json.dump(ids, open(SCRATCH + "/ids.json", "w"), indent=1)
    print(designer_url(wid))
