#!/usr/bin/env python3
"""
2-day WSQ Lesson Plan (DOCX) for
"Business Process Automation with Power Automate and Copilot Studio Agents"
(TGS-2022017524), Tertiary Infotech Academy Pte Ltd house format.

Daily window 9:00am - 6:00pm (1-hour lunch; tea breaks within).
Day 1: Power Automate workflows then Copilot Studio agents. Day 2: agent flows,
HTTP, human review and RAG, ending with the
assessment block: WA 1 hr + PP 1 hr, 4:00 - 6:00pm.
The Slides column maps every session to courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v7.0.pptx
(57 slides in the concept-first sequence: five concept modules, each followed by its labs).

Writes: courseware/LP-<course>.docx
"""
import json, os, sys
SKILL = "/Users/alfredang/.claude/skills/tertiary-lesson-plan"
sys.path.insert(0, SKILL)
import prodoc
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# script lives at .claude/skills/wsq-lesson-plan/ — repo root is 3 levels up
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TITLE = "Business Process Automation with Power Automate and Copilot Studio Agents"
VERSION = "7.0"
COURSE_CODE = "TGS-2022017524"
ORG = "Tertiary Infotech Academy Pte Ltd"
UEN = "201200696W"
LMS = "https://lms-tms.tertiaryinfotech.com/"
with open(os.path.join(REPO, "courseware", "slide_map.json"), encoding="utf-8") as fh:
    SLIDE_MAP = json.load(fh)
assert SLIDE_MAP["version"] == VERSION
LAB_SLIDES_RAW = SLIDE_MAP["labs"]
LAB_SLIDES = {lab_id: value.replace("-", "\u2013") for lab_id, value in LAB_SLIDES_RAW.items()}
# Module/section ranges come from the same map, so inserting slides can never
# leave the Slides column pointing at the wrong pages.
MOD = {k: v.replace("-", "\u2013") for k, v in SLIDE_MAP["modules"].items()}
SEC = {k: v.replace("-", "\u2013") for k, v in SLIDE_MAP["sections"].items()}
DECK_SLIDES = SLIDE_MAP["slides"]
with open(os.path.join(REPO, "courseware", "alignment_manifest.json"), encoding="utf-8") as fh:
    ALIGNMENT = json.load(fh)
assert ALIGNMENT["version"] == VERSION
LAB_META = {lab["id"]: lab for lab in ALIGNMENT["labs"]}
VERSIONS = [
    ["1.0", "24 Jun 2026", "Initial release — 3-day lesson plan (9:00am-5:00pm).",
     "Course Development Team"],
    ["2.0", "2 Jul 2026", "WSQ revision — new course title, 9:00am-6:00pm schedule, "
     "Day-3 assessment block (WA 1 hr + PP 1 hr), slide mapping for the 108-slide deck.",
     "Course Development Team"],
    ["3.0", "3 Jul 2026", "Course restructured from 3 days to 2 days — Day 1: Power Automate, "
     "Day 2: Copilot Studio agents ending with the assessment block (WA 1 hr + PP 1 hr, 4:00-6:00pm). "
     "Modules 4-5 and Labs 12-16 retired; slide mapping updated for the 86-slide v3 deck.",
     "Course Development Team"],
    ["3.1", "24 Jul 2026", "Labs 8-10 updated to paired Microsoft Teams and website "
     "experiences covering an ordinary HTTP flow, deterministic agent flow, and guarded "
     "AI prompt flow.",
     "Course Development Team"],
    ["3.2", "24 Jul 2026", "Day 2 now concludes at Lab 10; the former Lab 11 slot "
     "is integrated testing, troubleshooting, comparison and assessment preparation.",
     "Course Development Team"],
    ["3.3", "24 Jul 2026", "Reorganised Day 2 into two connected projects: prompt-created "
     "IT Support agent upgraded with RAG, followed by one Marina Trust agent progressively "
     "upgraded with HTTP, deterministic agent-flow and AI prompt-flow capabilities.",
     "Course Development Team"],
    ["3.4", "24 Jul 2026", "Reordered the practical journey from instant and scheduled "
     "flows through automated, approval and HTTP flows, then agent creation, RAG, "
     "Teams/website deployment, agent flow and prompt flow.",
     "Course Development Team"],
    ["5.0", "25 Jul 2026", "Rebuilt the course around Forms-driven workflows, "
     "specialised IT/HR agents, agent routing, HTTP/webhook websites and a "
     "multi-timeframe Finance Advisor capstone.",
     "Course Development Team"],
    ["5.1", "25 Jul 2026", "Aligned the lesson plan to the Version 5.1 deck and "
     "the expanded visual, click-by-click Labs 1-10.",
     "Course Development Team"],
    ["5.2", "25 Jul 2026", "Standardised canonical Lab 1-10 titles, durations and "
     "slide ranges against the shared alignment manifest and Version 5.2 deck.",
     "Course Development Team"],
    ["6.0", "25 Jul 2026", "Major concept-first overhaul: expanded cloud-flow types, "
     "trigger design, agent building blocks, HTTP/webhook foundations and finance-tool "
     "governance around the canonical 10-lab sequence and 113-slide deck.",
     "Course Development Team"],
    ["7.0", "2 Aug 2026", "Realigned to the rebuilt Lab 0-10 sequence (Copilot Studio "
     "Training Developer environment; trigger/actions, Excel logging, leave approval, "
     "Copilot Studio agents, agent invocation, three HTTP labs and two RAG labs). Deck "
     "rebuilt as five concept modules plus synthesis, with a workflow diagram slide for every lab, covering Power Automate, "
     "Copilot Studio, workflows, agent anatomy, multi-agent orchestration, every trigger "
     "and action family, RAG and human-in-the-loop.",
     "Course Development Team"],
]

BRAND = RGBColor(0x1F,0x6F,0xEB); DARK = RGBColor(0x16,0x1B,0x26); GREY = RGBColor(0x55,0x5B,0x66)
CENTER = WD_ALIGN_PARAGRAPH.CENTER

def _cline(doc, text, size, bold=False, color=DARK, before=0, after=4):
    p = doc.add_paragraph(); p.alignment = CENTER
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = "Arial"
    return p

def add_cover(doc):
    for _ in range(3): doc.add_paragraph()
    _cline(doc, ORG, 13, bold=True, after=2)
    _cline(doc, f"UEN: {UEN}", 10, color=GREY, after=20)
    _cline(doc, "LESSON PLAN", 26, bold=True, color=BRAND, after=12)
    _cline(doc, "For", 12, color=GREY, after=8)
    _cline(doc, TITLE, 20, bold=True, color=DARK, after=14)
    _cline(doc, f"TGS Ref No: {COURSE_CODE}", 12, color=GREY, after=6)
    _cline(doc, "Duration: 2 Days  ·  9:00am – 6:00pm", 12, color=GREY, after=20)
    _cline(doc, "Conducted by", 12, color=GREY, after=6)
    _cline(doc, ORG, 13, bold=True, after=2)
    _cline(doc, f"UEN: {UEN}", 10, color=GREY, after=18)
    _cline(doc, f"Version {VERSION}", 12, bold=True, color=BRAND)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def add_footer(doc):
    sec = doc.sections[0]; f = sec.footer; f.is_linked_to_previous = False
    p = f.paragraphs[0]; p.alignment = CENTER; p.text = ""
    r = p.add_run("Page "); r.font.size = Pt(9); r.font.color.rgb = GREY
    prodoc._field(p, "PAGE", "1").font.size = Pt(9)
    r2 = p.add_run(" of "); r2.font.size = Pt(9); r2.font.color.rgb = GREY
    prodoc._field(p, "NUMPAGES", "1").font.size = Pt(9)
    sp = f.add_paragraph(); sp.alignment = CENTER
    sr = sp.add_run(f"{TITLE} — Lesson Plan  ·  © {ORG}")
    sr.font.size = Pt(7.5); sr.font.color.rgb = GREY

def _shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),hexc); tcPr.append(shd)

def _borders(t, color="7A8190", sz=6):
    tblPr = t._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")): tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for edge in ("top","left","bottom","right","insideH","insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"),"single"); e.set(qn("w:sz"),str(sz))
        e.set(qn("w:space"),"0"); e.set(qn("w:color"),color)
        b.append(e)
    # WordprocessingML table-property order is significant. Borders must
    # precede layout/look/shading properties when those are present.
    inserted = False
    for later in ("w:tblCellMar", "w:tblLayout", "w:tblLook", "w:shd"):
        node = tblPr.find(qn(later))
        if node is not None:
            node.addprevious(b)
            inserted = True
            break
    if not inserted:
        tblPr.append(b)

def heading(doc, text, lvl=1):
    doc.add_paragraph(style=f"Heading {lvl}").add_run(text)
def para(doc, text):
    p = doc.add_paragraph(); p.add_run(text); return p
def bullets(doc, items):
    for it in items: doc.add_paragraph(style="List Bullet").add_run(it)

def _toc_field(doc):
    p = doc.add_paragraph()
    prodoc._field(p, 'TOC \\o "1-3" \\h \\z \\u', default="")


def add_static_toc(doc):
    # A real Word TOC field so the contents update and hyperlink when opened in
    # Word, followed by a readable outline for viewers that do not evaluate
    # fields (LibreOffice headless, and therefore the PDF we ship).
    _toc_field(doc)

    p = doc.add_paragraph()
    r = p.add_run("TABLE OF CONTENTS"); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = DARK
    for item in ("Course Overview", "Learning Outcomes", "Daily Schedule — Day 1",
                 "Daily Schedule — Day 2", "Lab Alignment Reference",
                 "Tools & Resources", "Assessment"):
        doc.add_paragraph(item, style="List Bullet")
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def info_table(doc, rows):
    t = doc.add_table(rows=0, cols=2); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for k, v in rows:
        c = t.add_row().cells
        c[0].text = ""; rr = c[0].paragraphs[0].add_run(k); rr.bold = True; rr.font.size = Pt(10); _shade(c[0], "EAF1FF")
        c[1].text = ""; c[1].paragraphs[0].add_run(v).font.size = Pt(10)
    _borders(t)

def schedule_table(doc, rows):
    """rows: (time, duration, activity, method, kind, slides); kind in {'topic','lab','break','assess',''}"""
    t = doc.add_table(rows=0, cols=5); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.add_row().cells
    hdr[0]._tc.getparent().get_or_add_trPr().append(OxmlElement("w:cantSplit"))
    for i, h in enumerate(["Time", "Duration", "Topic / Activity", "Method", "Slides"]):
        hdr[i].text = ""; rr = hdr[i].paragraphs[0].add_run(h)
        rr.bold = True; rr.font.size = Pt(9.5); rr.font.color.rgb = RGBColor(0xFF,0xFF,0xFF); _shade(hdr[i], "1F6FEB")
    for time, dur, act, method, kind, slides in rows:
        cells = t.add_row().cells
        # Keep each activity together so a lab description does not continue
        # as an orphaned fragment at the top of the following page.
        cells[0]._tc.getparent().get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        vals = [time, dur, act, method, slides]
        tint = {"break":"FFF4E5", "topic":"EAF1FF", "lab":"E8F7EE", "assess":"FDE8E8"}.get(kind)
        for i, v in enumerate(vals):
            cells[i].text = ""; pp = cells[i].paragraphs[0]
            rr = pp.add_run(v); rr.font.size = Pt(9.5)
            if i == 2 and kind in ("topic","lab","assess"): rr.bold = True
            if tint: _shade(cells[i], tint)
    for row in t.rows:
        row.cells[0].width = Pt(76); row.cells[1].width = Pt(50)
        row.cells[3].width = Pt(88); row.cells[4].width = Pt(56)
    _borders(t)

# ---------------------------------------------------------------- schedules
LEC = "Lecture & demo"; HND = "Hands-on lab"; DISC = "Facilitated discussion"
BRK = "—"; ASMT = "Individual assessment"

DAY1 = [
    ("9:00 – 9:45",  "45 min", "Welcome, WSQ admin & digital attendance, introductions, ground rules, course overview and lab map", DISC, "topic", SEC["course_overview"]),
    ("9:45 – 10:40", "55 min", "Module 1: business process automation, the Power Platform and the environment, flow anatomy, trigger families, action families", LEC, "topic", "12–17"),
    ("10:40 – 10:55","15 min", "Tea break", BRK, "break", "—"),
    ("10:55 – 11:35","40 min", f"{LAB_META['lab_0']['title']} — create the Copilot Studio Training (Developer) environment and verify connections", HND, "lab", LAB_SLIDES["lab_0"]),
    ("11:35 – 12:15","40 min", f"{LAB_META['lab_1']['title']} — build and verify the form-to-email flow", HND, "lab", LAB_SLIDES["lab_1"]),
    ("12:15 – 12:45","30 min", "Module 1 continued: dynamic content, the run history, and why order matters (commit before you confirm)", LEC, "topic", "18–20"),
    ("12:45 – 1:45", "60 min", "Lunch", BRK, "break", "—"),
    ("1:45 – 2:30",  "45 min", f"{LAB_META['lab_2']['title']} — write the audit row before sending the confirmation", HND, "lab", LAB_SLIDES["lab_2"]),
    ("2:30 – 3:15",  "45 min", "Module 2: conditions and branching; human in, on and out of the loop; how an approval suspends a running flow", LEC, "topic", MOD["m2"]),
    ("3:15 – 3:30",  "15 min", "Tea break", BRK, "break", "—"),
    ("3:30 – 4:15",  "45 min", f"{LAB_META['lab_3']['title']} — build and test the approved and rejected branches", HND, "lab", LAB_SLIDES["lab_3"]),
    ("4:15 – 5:05",  "50 min", "Module 3: workflow versus agent; agent anatomy — instructions, skills, knowledge, tools; what is actually enforced; connected agents; publishing", LEC, "topic", MOD["m3"]),
    ("5:05 – 5:50",  "45 min", f"{LAB_META['lab_4']['title']} — assemble the Procurement, HR, Sales and IT Support agents", HND, "lab", LAB_SLIDES["lab_4"]),
    ("5:50 – 6:00",  "10 min", "Day 1 recap and evidence check", DISC, "topic", MOD["m3"].split("–")[-1]),
]
DAY2 = [
    ("9:00 – 9:10",  "10 min", "Day 1 recap and Q&A", DISC, "topic", MOD["m3"]),
    ("9:10 – 9:40",  "30 min", f"{LAB_META['lab_5']['title']} — ground the HR agent in SharePoint, test its refusals, publish to Teams", HND, "lab", LAB_SLIDES["lab_5"]),
    ("9:40 – 10:10", "30 min", "Module 4: agent flows and the Agent node, HTTP request and response, JSON schema, structured output, the boundary of agency", LEC, "topic", MOD["m4"]),
    ("10:10 – 11:10","60 min", f"{LAB_META['lab_6']['title']} — web form to agent flow, six ordered rules, four decisions", HND, "lab", LAB_SLIDES["lab_6"]),
    ("11:10 – 11:25","15 min", "Tea break", BRK, "break", "—"),
    ("11:25 – 12:05","40 min", f"{LAB_META['lab_7']['title']} — the agent alone in public, and the probes that break it", HND, "lab", LAB_SLIDES["lab_7"]),
    ("12:05 – 1:05", "60 min", "Lunch", BRK, "break", "—"),
    ("1:05 – 2:05",  "60 min", f"{LAB_META['lab_8']['title']} — the Human review gate and the run that will not proceed", HND, "lab", LAB_SLIDES["lab_8"]),
    ("2:05 – 2:20",  "15 min", "Module 5: why retrieval rather than a bigger prompt; the RAG pipeline; chunking, embeddings and top_k", LEC, "topic", MOD["m5"]),
    ("2:20 – 3:00",  "40 min", f"{LAB_META['lab_9']['title']} — RAG as a product setting: three nodes, no ingestion", HND, "lab", LAB_SLIDES["lab_9"]),
    ("3:00 – 3:15",  "15 min", "Tea break", BRK, "break", "—"),
    ("3:15 – 3:55",  "40 min", f"{LAB_META['lab_10']['title']} — rebuild the same chatbot on Pinecone and compare the levers", HND, "lab", LAB_SLIDES["lab_10"]),
    ("3:55 – 4:00",  "5 min",  "Course synthesis and briefing before the assessment", DISC, "topic", SEC["synthesis"]),
    ("4:00 – 5:00",  "60 min", "Written Assessment (WA / SAQ) — 1 hour, open book", ASMT, "assess", SEC["assessment_and_closing"]),
    ("5:00 – 6:00",  "60 min", "Practical Performance (PP) Assessment — 1 hour, open book", ASMT, "assess", SEC["assessment_and_closing"]),
]


def total(rows):
    return sum(int(r[1].split()[0]) for r in rows)
for nm, rows in [("Day 1",DAY1),("Day 2",DAY2)]:
    assert total(rows) == 540, f"{nm} = {total(rows)} min (expected 540)"
for lab_id, meta in LAB_META.items():
    scheduled = sum(
        int(duration.split()[0])
        for _, duration, activity, _, _, _ in DAY1 + DAY2
        if activity.startswith(meta["title"])
    )
    assert scheduled == meta["duration_minutes"], (
        f"{lab_id} schedule = {scheduled} min; manifest = {meta['duration_minutes']} min"
    )

# ---------------------------------------------------------------- build doc
doc = Document()
nrm = doc.styles["Normal"]; nrm.font.name = "Arial"; nrm.font.size = Pt(11)
prodoc.style_headings(doc)
add_cover(doc)
prodoc.add_version_control(doc, VERSIONS)
add_static_toc(doc)

heading(doc, "Course Overview", 1)
para(doc, "This 2-day, hands-on WSQ course teaches participants to automate real business processes by combining "
          "Microsoft Power Automate flows with AI agents built in Microsoft Copilot Studio. The course is taught "
          "concepts first: five concept modules each introduce the ideas and the decision rules, and the labs that "
          "follow apply them. Day 1 moves from deterministic Forms-driven flows (email, Excel logging, approval "
          "branching) to Copilot Studio agents assembled from instructions, skills, knowledge, tools and connected "
          "agents. Day 2 puts an agent behind a website over HTTP, adds a human review gate, and grounds an agent in "
          "documents with RAG — first with built-in knowledge, then with an external Pinecone vector store. "
          "Participants finish with working automations and sit the WSQ assessment at the end of Day 2.")
info_table(doc, [
    ("Course Title", TITLE),
    ("TGS Ref No", COURSE_CODE),
    ("Duration", "2 Days (9:00am – 6:00pm), incl. 1-hour lunch and tea breaks; assessment on Day 2, 4:00 – 6:00pm"),
    ("Delivery", "Instructor-led, hands-on (physical / virtual)"),
    ("Audience", "Business and operations staff who want to automate repetitive work; no coding required"),
    ("Prerequisites", "Basic Microsoft 365 familiarity (Outlook, Excel); a Microsoft 365 work or school account and a Power Platform Developer environment with Copilot Credits (see Lab 0)"),
    ("Labs", "11 step-by-step labs across 2 days (Lab 0 setup plus Labs 1–10: five on Day 1 and six on Day 2), driven by 5 concept modules"),
    ("Assessment", "Written Assessment (SAQ) 1 hr + Practical Performance (PP) 1 hr — Day 2, 4:00 – 6:00pm, open book"),
])

heading(doc, "Learning Outcomes", 1)
para(doc, "By the end of the course, participants will be able to:")
bullets(doc, [
    "Explain business process automation and the Trigger → Actions → Output model, and identify the four trigger families and the six action families.",
    "Build Forms-driven Power Automate flows that send email, log data to Excel, branch on a condition and suspend for a human approval.",
    "Describe an agent as instructions, skills, knowledge, tools and connected agents, and state which of those the model can ignore.",
    "Create and ground Copilot Studio agents in approved SharePoint knowledge, test their refusals, and publish them to Microsoft Teams.",
    "Connect a website to an HTTP-triggered agent flow, apply a JSON schema and use structured output to branch on the agent's decision.",
    "Apply the boundary of agency and human-in-the-loop patterns so consequential actions require a person before they take effect.",
    "Build a Retrieval Augmented Generation chatbot with built-in knowledge and with an external Pinecone vector store, and justify the choice between them.",
])

heading(doc, "Daily Schedule", 1)
para(doc, "The Slides column maps each session to the matching slides in the facilitator deck "
          f"(Business Process Automation with Power Automate and Copilot Studio Agents-v7.0.pptx, {DECK_SLIDES} slides) so trainers can pace delivery against the deck.")
for nm, theme, rows in [
    ("Day 1 — Workflows, then Agents", "Modules 1–3: automation concepts, triggers and actions, control flow and human in the loop, then agent anatomy — Labs 0–4", DAY1),
    ("Day 2 — Agent Flows, Human Review, RAG & Assessment", "Modules 4–5: HTTP and the boundary of agency, the human review gate, and RAG twice over — Labs 5–10, then the assessment", DAY2),
]:
    heading(doc, nm, 2)
    para(doc, theme + ".")
    schedule_table(doc, rows)
    doc.add_paragraph()

heading(doc, "Lab Alignment Reference", 1)
para(doc, "This reference repeats the canonical lab title, duration and slide range used in the "
          "facilitator deck, Learner Guide and hands-on lab files. Use it to confirm that the "
          "correct activity is being delivered at each point in the schedule.")
for day_number in (1, 2):
    heading(doc, f"Day {day_number} Labs", 2)
    for lab in ALIGNMENT["labs"]:
        if lab["day"] != day_number:
            continue
        slide_range = LAB_SLIDES[lab["id"]]
        heading(doc, f"{lab['title']} · Slides {slide_range}", 3)
        para(doc, f"Duration: {lab['duration_minutes']} minutes. Follow the matching detailed, "
                  "step-by-step lab and its shared workflow visual in the Learner Guide.")

heading(doc, "Tools & Resources", 1)
info_table(doc, [
    ("Microsoft Power Automate", "make.powerautomate.com — build and run flows"),
    ("Microsoft Copilot Studio", "copilotstudio.microsoft.com — build and publish agents"),
    ("Power Platform admin center", "admin.powerplatform.microsoft.com — create the Copilot Studio Training Developer environment (Dataverse + Copilot Credits)"),
    ("Microsoft 365", "Outlook, Excel (OneDrive), Microsoft Forms, SharePoint and Microsoft Teams"),
    ("Pinecone", "pinecone.io — free-tier vector database, required for Lab 10 only"),
    ("Learner Guide", "Full step-by-step guide for every lab (LMS + course GitHub repository)"),
    ("LMS", LMS + " — courseware download, TRAQOM, assessment submission"),
])

heading(doc, "Assessment", 1)
para(doc, "The summative WSQ assessment is taken at the end of Day 2 and is open book "
          "(slides, Learner Guide and approved materials only):")
bullets(doc, [
    "Written Assessment (WA / SAQ) — 1 hour. Open-ended short-answer questions testing the knowledge from Modules 1–5.",
    "Practical Performance (PP) — 1 hour. Candidates build a working flow and agent, mirroring the hands-on labs.",
    "Assessment flow: TRAQOM survey (QR on the LMS) → Assessment digital attendance → WA then PP → submit answers on the LMS → sign the Assessment Summary Record.",
    "WSQ funding requires a minimum of 75% attendance AND a Competent (C) assessment outcome.",
    f"Courseware and the assessment are on the LMS: {LMS}",
])
para(doc, "Formative assessment is continuous: each lab includes a Checkpoint that the facilitator verifies before "
          "the class moves on. Labs 6–8 progressively verify an HTTP-triggered agent flow, an unsupervised public "
          "chatbot and a blocking human review gate; Labs 9–10 verify the same grounded chatbot built two different "
          "ways, including the probes that test whether either will invent an answer.")

add_footer(doc)
prodoc.enable_update_fields(doc)
settings = doc.settings._element
zoom = settings.find(qn("w:zoom"))
if zoom is not None and zoom.get(qn("w:percent")) is None:
    zoom.set(qn("w:percent"), "100")
update_fields = settings.find(qn("w:updateFields"))
compat = settings.find(qn("w:compat"))
if update_fields is not None and compat is not None:
    settings.remove(update_fields)
    compat.addprevious(update_fields)
out = os.path.join(REPO, f"courseware/LP-{TITLE}.docx")
doc.save(out)
print("Day totals:", {n: total(r) for n,r in [("D1",DAY1),("D2",DAY2)]})
print("Wrote", out)
