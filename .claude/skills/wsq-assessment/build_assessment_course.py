#!/usr/bin/env python3
"""
WSQ Assessments (DOCX) for
"Business Process Automation with Power Automate and Copilot Studio Agents"
(TGS-2022017524).

Two instruments, each as a question paper + a model-answer / marking guide:

  1. Written Assessment (WA / SAQ) — tests KNOWLEDGE. 6 open-ended
     short-answer questions (K1-K6) drawn from Modules 1-3 and the slides.
     Duration: 1 hour, open book.
  2. Practical Performance (PP) Assessment — tests PRACTICAL ability.
     One ACME Pte Ltd scenario with 3 tasks (criteria A1-A7) whose model
     answers are the hands-on lab build steps (Labs 1-15).
     Duration: 1 hour, open book.

The question counts (WA 6 / PP 3) intentionally match the previous versions.
Writes four files into ../assessemnt/.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# script lives at .claude/skills/wsq-assessment/ — repo root is 3 levels up
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.join(REPO, "assessment")
TITLE = "Business Process Automation with Power Automate and Copilot Studio Agents"
COURSE_CODE = "TGS-2022017524"
ORG = "Tertiary Infotech Academy Pte Ltd"
UEN = "201200696W"
DARK = RGBColor(0x16, 0x1B, 0x26); BRAND = RGBColor(0x1F, 0x6F, 0xEB); GREY = RGBColor(0x55, 0x5B, 0x66)

# ================================================================ doc helpers
def new_doc():
    d = Document(); n = d.styles["Normal"]; n.font.name = "Arial"; n.font.size = Pt(11); return d

def line(d, text="", bold=False, size=11, color=DARK, after=6, align=None):
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(after)
    if align is not None: p.alignment = align
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = "Arial"
    return p

def runs(d, segments, after=6, style=None):
    p = d.add_paragraph(style=style); p.paragraph_format.space_after = Pt(after)
    for text, bold in segments:
        r = p.add_run(text); r.bold = bold; r.font.size = Pt(11); r.font.name = "Arial"; r.font.color.rgb = DARK
    return p

def bullet(d, text):
    return runs(d, [(text, False)], after=3, style="List Bullet")

def numbered(d, text):
    return runs(d, [(text, False)], after=3, style="List Number")

def cover(d, subtitle):
    for _ in range(4): d.add_paragraph()
    line(d, ORG, bold=True, size=13, align=AL.CENTER, after=2)
    line(d, f"UEN: {UEN}", size=10, color=GREY, align=AL.CENTER, after=20)
    line(d, subtitle.upper(), bold=True, size=24, color=BRAND, align=AL.CENTER, after=12)
    line(d, "For", size=12, color=GREY, align=AL.CENTER, after=8)
    line(d, TITLE, bold=True, size=18, align=AL.CENTER, after=14)
    line(d, f"TGS Ref No: {COURSE_CODE}", size=12, color=GREY, align=AL.CENTER, after=20)
    line(d, "Conducted by", size=12, color=GREY, align=AL.CENTER, after=6)
    line(d, ORG, bold=True, size=13, align=AL.CENTER, after=2)
    line(d, f"UEN: {UEN}", size=10, color=GREY, align=AL.CENTER, after=2)
    d.add_page_break()

def title_block(d, subtitle):
    line(d, TITLE, bold=True, size=15, color=BRAND, after=2, align=AL.CENTER)
    line(d, subtitle, bold=True, size=12, color=DARK, after=2, align=AL.CENTER)
    line(d, f"Course Code: {COURSE_CODE}", size=10, color=GREY, after=12, align=AL.CENTER)

# Page 2 blocks (house standard — see the wsq-assessment skill's build_assessment.py):
# Trainee Information + Instructions to Candidate + Grading, then a page break so the
# questions/tasks always begin on page 3.
BRIEFING = [
    "Place phones and other materials under the table or on the floor.",
    "No photos or recording of assessment scripts.",
    "No discussion during the assessment.",
    "Use a black/blue pen for hard-copy assessments.",
    "No liquid paper / correction tape.",
    "Scripts are collected when time is up.",
]

def trainee_info(d):
    line(d, "Trainee Information", bold=True, size=12, after=6)
    for t in ["Trainee Name (as per NRIC): ______________________________________",
              "Last 3 digits and alphabet of NRIC / FIN: ____________________",
              "Date: ____________________"]:
        p = line(d, t, after=6); p.paragraph_format.line_spacing = 2.0

def instructions_block(d, time_text, extra):
    line(d, "Instructions to Candidate", bold=True, size=12, after=6)
    items = ["This is an individual exercise.",
             "This is an open-book assessment (slides and Learner Guide may be used).",
             f"A total of {time_text} is given to complete this assessment.",
             extra,
             "Complete your answers on the document provided and upload the completed "
             "answers to the LMS at https://lms-tms.tertiaryinfotech.com/."] + BRIEFING
    for i, s in enumerate(items, 1):
        line(d, f"{i}.  {s}", after=3)
    line(d, "", after=2)

def grading_block(d, statement):
    line(d, "Grading", bold=True, size=12, after=6)
    line(d, statement, after=10)
    for t in ["Grade: _______  (C / NYC)",
              "Assessor Name: __________________________   Assessor NRIC: ________________",
              "Date: ________________________                    Signature: ____________________"]:
        p = line(d, t, after=6); p.paragraph_format.line_spacing = 2.0

def answer_box(d, height_cm=5.0, hint=""):
    t = d.add_table(rows=1, cols=1); t.style = "Table Grid"
    cell = t.rows[0].cells[0]
    cell.text = ""
    if hint:
        p = cell.paragraphs[0]; r = p.add_run(hint); r.font.size = Pt(9); r.font.color.rgb = GREY; r.font.name = "Arial"
    trPr = t.rows[0]._tr.get_or_add_trPr()
    h = OxmlElement("w:trHeight"); h.set(qn("w:val"), str(int(height_cm * 567))); h.set(qn("w:hRule"), "atLeast")
    trPr.append(h)
    d.add_paragraph()

# ================================================================ WRITTEN (6 questions, K1-K6)
# (tag, question, model answer points, source)
WRITTEN = [
    ("K1",
     "ACME Pte Ltd still records every course enquiry by hand: a learner submits a form, someone reads it and "
     "re-types the details into a spreadsheet, then someone remembers to reply. Explain what business process "
     "automation actually removes from a process like this, and describe how the Trigger \u2192 Actions \u2192 Output "
     "model would apply if ACME automated it.",
     ["Business process automation is not simply doing the work faster \u2014 it removes the HAND-OFF, the point where "
      "a person re-types what another system already knows. That hand-off is where the delay, the typo and the "
      "forgotten reply live (Module 1).",
      "Trigger \u2014 the event that starts the flow: a new response is submitted to the Microsoft Form.",
      "Actions \u2014 what the flow does: get the response details, add a row to the Excel enquiry table, send the "
      "confirmation email to the address the learner entered.",
      "Output \u2014 the result: the logged audit row, the confirmation email, and a run history a supervisor can read.",
      "Benefits to name: consistency (same result every time, including at 3am), traceability (every run leaves a "
      "history), capacity (people move to the judgement calls the machine cannot make).",
      "(Any equivalent mapping of trigger/actions/output to the enquiry process is acceptable.)"],
     "Module 1 \u00b7 Slides 13\u201315"),

    ("K2",
     "Power Automate groups triggers into four families. Name all FOUR families, state what makes each one fire, "
     "and give the business example used in this course for each. Then explain why the order of the two actions in "
     "Lab 2 \u2014 writing the Excel audit row and sending the confirmation email \u2014 is a business decision rather "
     "than a technical one.",
     ["Manual \u2014 a person presses Run. Example: an instant cloud flow, or a button in the mobile app or Teams.",
      "Scheduled \u2014 a clock reaches a time. Example: a Recurrence trigger; the time zone must be set or it runs "
      "on UTC.",
      "Automated \u2014 an event happens in a system. Example: 'When a new response is submitted' from Microsoft "
      "Forms (Labs 1, 2, 3).",
      "Request \u2014 something calls in from outside. Example: 'When an HTTP request is received' (Labs 6\u201310) or "
      "'When an agent calls the workflow' (Labs 4, 6).",
      "Order: LOG, THEN CONFIRM. If the email fails, the enquiry is still on the register and someone can chase "
      "it \u2014 you have a record of a missed reply.",
      "If you confirm first and the row fails, you have promised a customer a reply that nobody can see; the "
      "evidence of the promise is gone.",
      "The principle: commit the record of the obligation BEFORE you create the obligation."],
     "Module 1 \u00b7 Slides 16, 20"),

    ("K3",
     "A colleague's flow finishes with a green tick, but the confirmation email arrives with an empty name. "
     "Explain why a green run is not proof of a correct run, describe what most likely went wrong with the "
     "dynamic value, and outline how you would use the run history to find and fix it.",
     ["A reference to nothing resolves to EMPTY, not to an error \u2014 so the flow succeeds while carrying a blank "
      "value. This is the single most common fault in the course.",
      "Most likely cause: the dynamic value was TYPED by hand instead of being inserted with the \u26a1 picker, so it "
      "stayed dead text and never resolved to the earlier step's output.",
      "Fix: delete the typed text and re-insert the value with the picker so it renders as a coloured token.",
      "Run history procedure: open My flows \u2192 the flow \u2192 Run history (or the Activity tab in an agent flow); "
      "expand each step to see its inputs and outputs; find the step whose input was blank \u2014 not a red error.",
      "Three states that look alike: Succeeded with the right data; Succeeded with EMPTY data; still Running "
      "because it is waiting for a person. Only the first is done; the second is the dangerous one.",
      "Republish and run ONE test \u2014 one change per publish-and-test cycle, or a failure becomes uninterpretable."],
     "Module 1 \u00b7 Slides 18\u201319"),

    ("K4",
     "Distinguish human IN the loop, human ON the loop and human OUT of the loop \u2014 stating for each who decides, "
     "who acts, and whether the AI can proceed alone. Identify which pattern the Lab 3 leave approval and the "
     "Lab 8 client-reply gate use, and explain how you would prove in class that the Lab 8 gate is real.",
     ["Human IN the loop: AI proposes, the human decides; the human authorises and the system acts. The AI CANNOT "
      "proceed \u2014 it blocks.",
      "Human ON the loop: the AI decides and acts; a human monitors and can intervene. Supervision is after the fact.",
      "Human OUT of the loop: the AI decides and acts, and nobody checks.",
      "Lab 3 and Lab 8 are both human IN the loop \u2014 the run genuinely suspends until a person responds. Labs 6, "
      "7, 9 and 10 are deliberately out of the loop.",
      "Proof: submit an enquiry, then open Activity. The run says Running \u2014 and it will still say Running "
      "tomorrow. Nothing times out, nothing defaults, nothing proceeds. That pause is the deliverable.",
      "Also acceptable: approvals must be sent to the Microsoft Teams Approvals app, not Outlook \u2014 on a live "
      "tenant Outlook created the request and never delivered the mail, and the run sat at Running looking healthy.",
      "A rejection must be routed to a NAMED person, never to silence."],
     "Module 2 \u00b7 Slides 22\u201324"),

    ("K5",
     "A Copilot Studio agent is assembled from instructions, skills, knowledge, tools and connected agents. For "
     "each of these five parts, state what it is and whether it is ENFORCED. Then explain the design principle "
     "this leads to, and why 'a tool the agent does not have' is itself a control.",
     ["Instructions \u2014 who the agent is, always in force. NOT enforced: probabilistic.",
      "Skill \u2014 a named procedure applied when the topic matches. NOT enforced: the model decides it applies.",
      "Knowledge \u2014 documents the agent may read. PARTLY enforced: it genuinely cannot read what it was not given.",
      "Tool \u2014 a flow that acts outside the conversation. ENFORCED: the flow's own logic runs whatever the agent "
      "believed.",
      "Connected agent \u2014 a separate agent with its own knowledge and audience. ENFORCED: the knowledge boundary "
      "is real (though the conversation still crosses it).",
      "The principle: A CONTROL THE MODEL CANNOT REACH BEATS A RULE YOU ASKED IT TO FOLLOW.",
      "A tool the agent does not have is a control because the absence is structural, not probabilistic \u2014 the IT "
      "Support Agent has no ResetPassword tool, and that absence is the only unbreakable part of its password rules.",
      "Related: the schema beats the prompt \u2014 a field that exists will eventually be filled, so leave it out of "
      "the tool contract rather than asking the model nicely."],
     "Module 3 \u00b7 Slides 27\u201328"),

    ("K6",
     "Explain what Retrieval Augmented Generation (RAG) is and why it is preferred to pasting every document into "
     "the agent's instructions. Define chunk, embedding and top_k. Then compare the built-in Copilot Studio "
     "knowledge source (Lab 9) with an external Pinecone vector store (Lab 10), and state what determines which "
     "one is the right choice.",
     ["RAG = retrieve, then generate. Instead of giving the model everything and hoping it finds the answer, you "
      "retrieve only the two or three documents that resemble the question and give it only those.",
      "Why not paste everything: the instruction exceeds what the model can read, it starts ignoring the middle, "
      "every question costs the price of all the documents, and a fee change means editing the prompt.",
      "Chunk \u2014 how a document is split (in Lab 10, one brochure = one record).",
      "Embedding \u2014 text represented as a list of numbers (llama-text-embed-v2, 1024 dimensions).",
      "top_k \u2014 how many documents come back from the search (3 in Lab 10).",
      "Built-in (Lab 9): 3 nodes, no ingestion, but the embedding model, chunking and top_k are all HIDDEN, and "
      "citation markers leak into the reply; a changed fee means waiting for a re-crawl.",
      "Pinecone (Lab 10): 5 nodes and a one-off ingestion script, but chunking, the embedding model and top_k are "
      "YOUR call, there are no citation markers, and a changed fee means re-ingesting.",
      "Neither is the right answer in general. Which is right depends on whether the person maintaining it will "
      "ever need those levers \u2014 a staffing question, not a technical one.",
      "Also creditable: retrieval decides whether generation can possibly be right; and a grounded agent must "
      "still be probed for invention because a confident wrong answer raises no error."],
     "Module 5 \u00b7 Slides 42\u201345"),
]

WA_NAME = f"WA (SAQ) - {TITLE}"
PP_NAME = f"PP Assessment - {TITLE}"

def build_written_paper():
    d = new_doc()
    cover(d, "Written Assessment (SAQ)")
    title_block(d, "Written Assessment (SAQ) — Knowledge")
    # Page 2: trainee info + instructions + grading; questions begin on page 3.
    trainee_info(d)
    instructions_block(d, "1 hour", "Answer ALL 6 questions in the boxes provided.")
    grading_block(d, "Candidate has answered all written questions and demonstrated the underpinning "
                     "knowledge required for the course learning outcomes.")
    d.add_page_break()
    line(d, "Short-Answer Questions (Knowledge)", bold=True, size=12, after=8)
    for i, (tag, q, _pts, _src) in enumerate(WRITTEN, 1):
        runs(d, [(f"Question {i}: ", True), (q, False), (f"  ({tag})", True)], after=6)
        answer_box(d, 5.0)
    out = os.path.join(OUT, f"{WA_NAME}.docx"); d.save(out); return out

def build_written_answers():
    d = new_doc()
    cover(d, "Answers to Written Assessment (SAQ)")
    title_block(d, "Written Assessment (SAQ) — Model Answers / Marking Guide")
    line(d, "Assessor note: answers are model points — accept equivalent wording. A response is Competent for a "
            "question when it covers the substance of the points shown.", color=GREY, after=10)
    for i, (tag, q, pts, src) in enumerate(WRITTEN, 1):
        runs(d, [(f"Question {i} ({tag}): ", True), (q, False)], after=4)
        for pt in pts: bullet(d, pt)
        runs(d, [("Source: ", True), (src, False)], after=12)
    out = os.path.join(OUT, f"Answers to {WA_NAME}.docx"); d.save(out); return out

# ================================================================ PRACTICAL (3 tasks, A1-A7)
SCENARIO = (
    "Scenario: ACME Pte Ltd runs a small training academy. Learners submit course enquiries on a form, staff "
    "re-type them into a spreadsheet, and someone eventually replies by hand. Managers approve staff leave over "
    "email, and nobody can find the decision afterwards. ACME wants you \u2014 as taught in this course \u2014 to "
    "automate the enquiry process, put a human gate on an approval, and stand up a grounded agent that answers "
    "policy questions without inventing anything. Build everything in your Copilot Studio Training (Developer) "
    "environment. Power Automate and Copilot Studio must be pointed at the SAME environment."
)

PP_TASKS = [
    ("Task 1 \u2014 Build the enquiry flow: trigger, actions and the audit row (Power Automate) \u2014 mirrors Lab 1 and Lab 2",
     "In make.powerautomate.com, create an automated cloud flow named PP Course Enquiry that: "
     "(a) is started by the Microsoft Forms trigger \"When a new response is submitted\" on a form with the "
     "questions Name, Email, Tel and Message; "
     "(b) uses \"Get response details\" so the four answers become dynamic content; "
     "(c) adds a row into an Excel Online (Business) table with the enquiry details AND a timestamp \u2014 use the "
     "fx expression editor for the date, not typed text; and "
     "(d) THEN sends a personalised confirmation email to the address the learner entered in the form. "
     "The audit row must be written BEFORE the email is sent. Submit the form once and confirm the run succeeds. "
     "Every dynamic value must be inserted with the \u26a1 picker.",
     "Take a screenshot of the whole flow in the designer, a screenshot of the successful run history showing the "
     "step inputs/outputs, AND a screenshot of the Excel row, and paste them in the box below: (A1, A2, A3)"),
    ("Task 2 \u2014 Add a human gate: the approval that suspends the run (Power Automate) \u2014 mirrors Lab 3",
     "Create a second automated cloud flow named PP Leave Approval that: "
     "(a) is started by a Microsoft Forms leave-application response; "
     "(b) uses \"Start and wait for an approval\" assigned to a tenant user (yourself), sent to Microsoft Teams "
     "\u2014 not Outlook; and "
     "(c) uses a Condition on the approval Outcome so that Approve sends an approval email to the applicant and "
     "Reject sends a rejection email that includes the approver's comments. Both branches must be built. "
     "Submit the form, show the run SUSPENDED at the approval while it waits, then respond and let it complete.",
     "Take a screenshot of the flow showing BOTH condition branches, a screenshot of the run while it is still "
     "waiting at the approval, AND a screenshot of the completed run with the correct email, and paste them in "
     "the box below: (A4, A5)"),
    ("Task 3 \u2014 Build and ground a Copilot Studio agent, then prove it refuses (Copilot Studio) \u2014 mirrors Lab 5 and Lab 9",
     "In copilotstudio.microsoft.com (SAME environment), create an agent named PP Policy Assistant that: "
     "(a) has instructions stating its identity, that it must answer only from the approved source, at least one "
     "explicit refusal, and where to escalate; "
     "(b) has a SharePoint document as a knowledge source, with the source status Ready, \"Use general knowledge\" "
     "turned OFF and the \"Search all websites\" chip REMOVED; and "
     "(c) is tested in the Preview pane with THREE probes: one question the document answers, one question the "
     "document does not cover, and one request the agent must refuse. The agent must say it does not know rather "
     "than invent an answer.",
     "Take a screenshot of the Instructions, a screenshot of the knowledge source showing status Ready, AND a "
     "screenshot of the Preview conversation showing all three probes and their answers, and paste them in the "
     "box below: (A6, A7)"),
]

PP_ANSWERS = [
    ("Task 1 (A1, A2, A3) \u2014 model build steps (mirrors Lab 1 and Lab 2)", [
        "Confirm the environment selector shows Copilot Studio Training in BOTH products before building (Lab 0).",
        "Create \u2192 Automated cloud flow \u2192 name PP Course Enquiry \u2192 trigger \"When a new response is "
        "submitted\" \u2192 select the Course Enquiry Form (Lab 1).",
        "+ New step \u2192 \"Get response details\" \u2192 same Form Id \u2192 insert the trigger's Response Id token "
        "with the \u26a1 picker. Without this step the four answers are not available as dynamic content (Lab 1).",
        "+ New step \u2192 Excel Online (Business) \u2192 \"Add a row into a table\" \u2192 pick Location / Document "
        "Library / File / Table (EnquiryLog); map Name, Email, Tel and Message as tokens; for Timestamp use the fx "
        "expression editor with formatDateTime(utcNow(),'yyyy-MM-dd HH:mm') so it resolves at run time (Lab 2).",
        "+ New step \u2192 Office 365 Outlook \u2192 \"Send an email (V2)\" \u2192 To = the Email answer token from "
        "Get response details (NOT the flow owner); write a personalised body using the Name token (Lab 1).",
        "ORDER IS ASSESSED: the Excel action must sit ABOVE the email action. Commit the record of the obligation "
        "before creating the obligation \u2014 if the email fails the enquiry is still on the register (Lab 2).",
        "Save \u2192 submit the form \u2192 open Run history \u2192 expand each step and confirm the inputs are populated, "
        "not blank.",
        "Competent when: the run succeeds; the Excel row contains the submitted values and a real timestamp; the "
        "email reaches the address entered on the form; the Excel action precedes the email action; no value was "
        "typed by hand where a token was required."]),
    ("Task 2 (A4, A5) \u2014 model build steps (mirrors Lab 3)", [
        "Create \u2192 Automated cloud flow \u2192 name PP Leave Approval \u2192 Forms trigger on the Leave Application "
        "Form \u2192 add \"Get response details\" (Lab 3).",
        "+ New step \u2192 Approvals \u2192 \"Start and wait for an approval\" \u2192 Approval type: Approve/Reject \u2013 "
        "First to respond; Title and Details built from the response tokens; Assigned to: a real tenant user chosen "
        "from the people picker (Lab 3).",
        "The request must go to the Microsoft Teams Approvals app. On a live tenant Outlook created the request and "
        "never delivered the mail \u2014 the run then sits at Running looking perfectly healthy (Lab 3).",
        "+ New step \u2192 Condition \u2192 Outcome is equal to Approve. TRUE branch: Send an email (V2) confirming "
        "approval. FALSE branch: Send an email (V2) with the rejection AND the approver's Comments token (Lab 3).",
        "Both branches must be built. A rejection routed to silence is indistinguishable, from the applicant's "
        "side, from a request that was lost.",
        "Evidence of the gate: after submitting, the run shows as Running and stays suspended at the approval "
        "action until a person responds \u2014 nothing times out and nothing defaults (Module 2).",
        "Competent when: the run genuinely suspends at the approval; the approval is actioned from Teams; the "
        "Condition reads Outcome; and the correct email is sent on each of the two branches."]),
    ("Task 3 (A6, A7) \u2014 model build steps (mirrors Lab 5 and Lab 9)", [
        "Copilot Studio \u2192 confirm the environment selector shows Copilot Studio Training \u2014 the SAME "
        "environment as Power Automate, or the agent cannot see the flow (Lab 0, Lab 5).",
        "Agents \u2192 New agent \u2192 name PP Policy Assistant (Lab 5).",
        "Instructions must state four things (Module 3): IDENTITY \u2014 'You are ACME's policy information "
        "assistant.'; SOURCE RULE \u2014 'Answer using only the approved SharePoint policy source.'; REFUSAL \u2014 "
        "'Do not expose, request or infer personal employee records' / 'Do not guarantee approval.'; ESCALATION "
        "\u2014 'When the source is insufficient, say so and direct the user to HR.'",
        "Never paste an @{...} expression into the Instructions box \u2014 it is a rich-text editor and a reference "
        "to a node that does not exist resolves to EMPTY rather than erroring (Module 3).",
        "Knowledge \u2192 Add knowledge \u2192 SharePoint \u2192 paste the approved folder/file URL \u2192 name and "
        "describe the source \u2192 wait for status Ready. If it reports a permission failure, fix SharePoint access "
        "(Lab 5).",
        "Turn OFF 'Use general knowledge' and REMOVE the 'Search all websites' chip, which is on by default. "
        "Otherwise a fact from the open web is indistinguishable from one in the approved document (Lab 9).",
        "Grounding is not only about giving the agent facts \u2014 it is about taking away every other source of them.",
        "Probe in Preview with three cases: (1) a question the document answers \u2014 the answer must reflect the "
        "document; (2) a question the document does not cover \u2014 it must say so, not improvise; (3) a request it "
        "must refuse, e.g. another employee's records or a guarantee of approval \u2014 it must refuse and escalate.",
        "A confident wrong answer raises no error: the run is green and the reply is fluent, which is exactly why "
        "the refusal probes are assessed (Module 5).",
        "Competent when: the instructions carry identity, source rule, refusal and escalation; the knowledge source "
        "is Ready with general knowledge off; and all three probes behave correctly, including the refusal."]),
]

def build_pp_paper():
    d = new_doc()
    cover(d, "Practical Performance (PP) Assessment")
    title_block(d, "Practical Performance (PP) Assessment")
    # Page 2: trainee info + instructions + grading; the practical problem begins on page 3.
    trainee_info(d)
    instructions_block(d, "1 hour", "Complete ALL 3 tasks and paste the required screenshots in the boxes provided.")
    grading_block(d, "Candidate has successfully completed all the tasks for PP and is able to explain "
                     "the overall functions and features used to achieve these tasks.")
    d.add_page_break()
    line(d, "Practical Performance", bold=True, size=12, after=6)
    line(d, SCENARIO, after=10)
    for head, body, evidence in PP_TASKS:
        runs(d, [(head + ": ", True), (body, False)], after=6)
        line(d, evidence, bold=True, after=4)
        answer_box(d, 6.0, hint="Paste screenshot(s) here")
    out = os.path.join(OUT, f"{PP_NAME}.docx"); d.save(out); return out

def build_pp_answers():
    d = new_doc()
    cover(d, "Answers to Practical Performance (PP) Assessment")
    title_block(d, "Practical Performance (PP) — Model Answers / Marking Guide")
    line(d, "Assessor note: the model answers below are the in-class lab build steps. Accept any working build that "
            "meets the Competent-when criteria; the cited labs show the exact click paths.", color=GREY, after=8)
    line(d, SCENARIO, after=10)
    for head, steps in PP_ANSWERS:
        line(d, head, bold=True, after=4)
        for s in steps: numbered(d, s)
        line(d, "", after=6)
    out = os.path.join(OUT, f"Answer to {PP_NAME}.docx"); d.save(out); return out

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (build_written_paper, build_written_answers, build_pp_paper, build_pp_answers):
        print("Wrote", fn())
