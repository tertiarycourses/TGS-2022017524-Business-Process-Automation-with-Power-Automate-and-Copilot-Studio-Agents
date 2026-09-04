"""Lab 10 - Calling Agent from Workflow (DO NOT DELETE): manual Start with a Topic input -> Copilot drafts the blog
-> Teams Post message in a chat or channel (Training / General)."""
import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wfapi import *
from wfapi_a import *

NAME = "Lab 10 - Calling Agent from Workflow (DO NOT DELETE)"
TEAMS = json.load(open(SCRATCH + "/teams-params.json")) if os.path.exists(SCRATCH + "/teams-params.json") else {}
PROMPT = ("Write a short, engaging blog post of about 300 words on the topic below. Give it a title line, a two-sentence introduction, "
          "three short paragraphs with one key point each, and a one-sentence conclusion. Write in plain professional English for a "
          "general business audience.\n\nTopic: @{triggerBody()?['text']}")

def build(stage=2):
    wf = Workflow(NAME)
    s = wf.start_manual_inputs([("Topic", "text", "The subject of the blog post")])
    c = wf.m365copilot_connected("Draft the blog post", PROMPT)
    wf.chain(s, c)
    if stage >= 2:
        t = wf.connector("Post message in a chat or channel", "shared_teams", "PostMessageToConversation",
            {"poster": "Flow bot", "location": "Channel",
             "body/recipient/groupId": TEAMS.get("groupId", ""), "body/recipient/channelId": TEAMS.get("channelId", ""),
             "body/messageBody": "@outputs('Draft_the_blog_post')?['body/response']"})
        wf.edge(c, t)
    return wf

if __name__ == '__main__':
    stage = int(os.environ.get("STAGE", "2"))
    wf = build(stage)
    ids = json.load(open(SCRATCH + "/ids.json"))
    wid = create(wf); ids["lab10"] = wid; json.dump(ids, open(SCRATCH + "/ids.json", "w"), indent=1)
    print(designer_url(wid))
