#!/usr/bin/env python3
"""
2-day WSQ Lesson Plan (DOCX) for
"Business Process Automation with Power Automate and Copilot Studio Agents"
(TGS-2022017524), Tertiary Infotech Academy Pte Ltd house format.

Daily window 9:30am - 6:30pm = 480 instructional minutes per day (1-hour lunch
deducted; the two 15-minute tea breaks are counted within). 18 labs, Lab 0-17,
all built in the new Copilot Studio designer (classic Power Automate is only the
connector engine). Day 1: Modules 1-3, Labs 0-8 (workflows, email classification, then
one agent per lab). Day 2: Labs 9-17 (multi-agent, agent flows, HTTP, human review, RAG,
publishing) ending with the assessment block: WA 1 hr + PP 1 hr, 4:30 - 6:30pm.
The Slides column maps every session to courseware/<deck>-v{VERSION}.pptx via
courseware/slide_map.json (the concept-first sequence: five concept modules, each
followed by its labs). Day 1 / Day 2 rows are generated from a minute list so the
time ranges can never disagree with the durations.

Writes: courseware/LP-<course>.docx
"""
import json, os, sys
SKILL = "/Users/alfredang/.claude/skills/tertiary-lesson-plan"
sys.path.insert(0, SKILL)
import prodoc
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# script lives at .claude/skills/wsq-lesson-plan/ — repo root is 3 levels up
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TITLE = "Business Process Automation with Power Automate and Copilot Studio Agents"
VERSION = "8.1"
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
assert ALIGNMENT["version"] in ("7.0", VERSION)
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
    ["7.1", "6 Aug 2026", "Slide references realigned to the expanded 75-slide v7.1 deck: new Copilot Studio content folded into Modules 3-4 (model and harness, choosing a harness, modern orchestration, the new agent and workflow designers, skills as instructions on demand) plus a training-accounts slide in the course overview.",
     "Course Development Team"],
    ["7.2", "6 Aug 2026", "Lab 5 replaced — renamed from Invoke Agents to Calling Agent from Workflow: an agent flow that collects a blog topic at the Start node, drafts the post with M365 Copilot and posts it to the Training team's General channel. Day 2 session and deck references updated to the v7.2 deck.",
     "Course Development Team"],
    ["7.3", "6 Aug 2026", "Aligned to the 13-lab structure and the 80-slide v7.3 deck — Lab 4b (Multi-Agent Content Team) added as the optional Day 1 extension of Lab 4, Lab 5b (Calling Workflow from Agent) scheduled after Lab 5 on Day 2 (recap, Module 4, Lab 6 and Module 5 retimed to fit), and all slide mappings updated.",
     "Course Development Team"],
    ["7.4", "7 Aug 2026", "Deck v7.4 — the Lab 8 workflow slide now shows the live simplified classroom flow (Excel logging removed) captured from the repaired designer build; slide count and mappings unchanged.",
     "Course Development Team"],
    ["8.0", "4 September 2026", "Restructured to 18 individual labs (Lab 0–17) built in the new "
     "Copilot Studio; new Lab 4 Email Classification, Labs 5–8 one agent each, Lab 17 "
     "publishing; all flows rebuilt as Copilot Studio workflows; real new-designer screenshots "
     "embedded in every lab; tenant naming aligned to the built environment (workflows "
     "(DO NOT DELETE) on workflows and agents, 30-character agent-name cap); Copilot Credits note",
     "Course Development Team"],
    ["8.0.1", "4 September 2026", "Environment model updated — learners now build in a dedicated "
     "per-class Training Class Sandbox environment (reset between cohorts) instead of the trainer's "
     "build environment; the reference (DO NOT DELETE) workflows and agents were moved to a separate "
     "master reference Sandbox and are read-only for learners. Lab 0 rewritten around switching to "
     "the assigned class environment, with a Developer/Sandbox/Trial comparison and a self-study "
     "path for creating a personal Developer environment.",
     "Course Development Team"],
    ["8.0.2", "4 September 2026", "Both days re-timed to the house standard 9:30am – 6:30pm — "
     "exactly 480 instructional minutes per day (1-hour lunch deducted; the two 15-minute tea "
     "breaks counted within), replacing the 9:00am – 6:00pm frame that gave Day 1 450 and Day 2 "
     "450 instructional minutes. No lab duration changed; the assessment block moves to "
     "4:30 – 6:30pm. Lab 0 environment references corrected to the Training Class Sandbox.",
     "Course Development Team"],
    ["8.1", "4 September 2026", "Deck lab order corrected — Lab 17 (Publish to Teams, Microsoft 365 Copilot and the Web) now appears LAST, after the two RAG labs, matching the order the Lesson Plan schedules and the Learner Guide follows. Previously the deck grouped it with the Module 3 agent labs, so the slides jumped Lab 11 to Lab 17 and back to Lab 12. No lab content, duration or timing changed.",
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
    for _ in range(2): doc.add_paragraph()
    lp_ = doc.add_paragraph(); lp_.alignment = CENTER
    lp_.add_run().add_picture(os.path.join(REPO, ".claude", "skills", "tertiary-lesson-plan", "assets", "tertiary-infotech-logo.png"), width=Inches(1.1))
    doc.add_paragraph()
    _cline(doc, ORG, 13, bold=True, after=2)
    _cline(doc, f"UEN: {UEN}", 10, color=GREY, after=20)
    _cline(doc, "LESSON PLAN", 26, bold=True, color=BRAND, after=12)
    _cline(doc, "For", 12, color=GREY, after=8)
    _cline(doc, TITLE, 20, bold=True, color=DARK, after=14)
    _cline(doc, f"TGS Ref No: {COURSE_CODE}", 12, color=GREY, after=6)
    _cline(doc, "Duration: 2 Days  ·  9:30am – 6:30pm", 12, color=GREY, after=20)
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

def _clock(minutes_from_midnight):
    h, m = divmod(minutes_from_midnight, 60)
    return f"{(h - 12) if h > 12 else h}:{m:02d}"

def _sched(start_hhmm, entries):
    """entries: (minutes, activity, method, kind, slides) -> the 6-tuple rows the
    schedule table consumes: (time range, 'N min', activity, method, kind, slides)."""
    h, m = (int(x) for x in start_hhmm.split(":"))
    t = h * 60 + m
    rows = []
    for minutes, act, method, kind, slides in entries:
        rows.append((f"{_clock(t)} – {_clock(t + minutes)}", f"{minutes} min", act, method, kind, slides))
        t += minutes
    return rows

def _lab(lab_id, blurb):
    return f"{LAB_META[lab_id]['title']} — {blurb}"

# PLAN-v8 Day 1: admin 30 · M1 50 · tea 15 · L0 20 · L1 30 · L2 30 · lunch 60 · M2 25 · L3 35 ·
# L4 45 · tea 15 · M3 45 · L5 35 · L6 35 · L7 30 · L8 30 · recap 10 = 540 elapsed / 480 instructional
DAY1 = _sched("9:30", [
    (30, "Welcome, WSQ admin & digital attendance, introductions, ground rules, course overview and the 18-lab map", DISC, "topic", SEC["course_overview"]),
    (50, "Module 1: business process automation, the Power Platform and the environment, the Copilot Studio workflow designer, flow anatomy, trigger families, connector action families, dynamic content and Activity", LEC, "topic", MOD["m1"]),
    (15, "Tea break", BRK, "break", "—"),
    (20, _lab("lab_0", "switch to the assigned Training Class Sandbox environment, turn on the new experience and verify connections"), HND, "lab", LAB_SLIDES["lab_0"]),
    (30, _lab("lab_1", "a Forms trigger and two connector actions: build and verify the form-to-email workflow"), HND, "lab", LAB_SLIDES["lab_1"]),
    (30, _lab("lab_2", "commit before you confirm: write the Excel audit row, then send the confirmation"), HND, "lab", LAB_SLIDES["lab_2"]),
    (60, "Lunch", BRK, "break", "—"),
    (25, "Module 2: If/Else and Classify; human in, on and out of the loop; how an approval suspends a running workflow; the Human review node and where the card arrives", LEC, "topic", MOD["m2"]),
    (35, _lab("lab_3", "the workflow pauses for a manager; build and test the approved and rejected branches"), HND, "lab", LAB_SLIDES["lab_3"]),
    (45, _lab("lab_4", "Outlook trigger, a Classify node with five categories, a deterministic handler on every port and a Human review gate in Teams for Priority mail"), HND, "lab", LAB_SLIDES["lab_4"]),
    (15, "Tea break", BRK, "break", "—"),
    (45, "Module 3: workflow versus agent; the new Copilot Studio (model and harness, the new agent designer); agent anatomy — instructions, knowledge, tools, skills, connected agents; what is actually enforced; tools vs skills vs MCP; publishing and channels", LEC, "topic", MOD["m3"]),
    (35, _lab("lab_5", "instructions plus knowledge: build the HR agent, test it in Preview and find out what it refuses"), HND, "lab", LAB_SLIDES["lab_5"]),
    (35, _lab("lab_6", "a workflow as a tool: the agent fills the inputs, the workflow's logic is enforced, the reference number proves it ran"), HND, "lab", LAB_SLIDES["lab_6"]),
    (30, _lab("lab_7", "grounding for the public: 20 SharePoint brochures, and refusing to invent a fee"), HND, "lab", LAB_SLIDES["lab_7"]),
    (30, _lab("lab_8", "five uploaded skill packages, and the demonstration that a skill is a procedure, not a permission"), HND, "lab", LAB_SLIDES["lab_8"]),
    (10, "Day 1 recap and evidence check", DISC, "topic", MOD["m3"]),
])
# PLAN-v8 Day 2: recap 5 · L9 35 · L10 25 · L11 25 · tea 15 · M4 25 · L12 45 · lunch 60 · L13 30 ·
# L14 35 · M5 15 · L15 30 · L16 30 · tea 15 · L17 25 · synthesis 5 · WA 60 · PP 60 = 540 elapsed / 480 instructional
DAY2 = _sched("9:30", [
    (5,  "Day 1 recap and Q&A", DISC, "topic", MOD["m3"]),
    (35, _lab("lab_9", "one topic, four connected agents: the manager delegates to Research, Blog and Review, and a person approves at the end"), HND, "lab", LAB_SLIDES["lab_9"]),
    (25, _lab("lab_10", "the workflow calls the model at a fixed step: Start-node topic input, the draft posted to the Training team's General channel"), HND, "lab", LAB_SLIDES["lab_10"]),
    (25, _lab("lab_11", "the boundary crossed the other way: the Blog Writer Agent runs the published workflow as its tool"), HND, "lab", LAB_SLIDES["lab_11"]),
    (15, "Tea break", BRK, "break", "—"),
    (25, "Module 4: agent flows and the Agent node, the HTTP trigger (GET vs POST, the URL generated on Save), request body JSON schema, Response node and status codes, structured output, Compose, the boundary of agency", LEC, "topic", MOD["m4"]),
    (45, _lab("lab_12", "web form to workflow over HTTP: SharePoint duplicate check, six ordered rules, structured output, four decisions"), HND, "lab", LAB_SLIDES["lab_12"]),
    (60, "Lunch", BRK, "break", "—"),
    (30, _lab("lab_13", "the agent alone in public: contact gate, grounded FAQ, the refusal it must never break, and the probes that break it"), HND, "lab", LAB_SLIDES["lab_13"]),
    (35, _lab("lab_14", "the Human review gate in Teams and the run that will not proceed"), HND, "lab", LAB_SLIDES["lab_14"]),
    (15, "Module 5: why retrieval rather than a bigger prompt; the RAG pipeline; chunking, embeddings, dimension and top_k; built-in knowledge versus an external vector store", LEC, "topic", MOD["m5"]),
    (30, _lab("lab_15", "RAG as a product setting: three nodes, no ingestion, nothing you can inspect"), HND, "lab", LAB_SLIDES["lab_15"]),
    (30, _lab("lab_16", "rebuild the same chatbot on Pinecone and compare the levers"), HND, "lab", LAB_SLIDES["lab_16"]),
    (15, "Tea break", BRK, "break", "—"),
    (25, _lab("lab_17", "Publish, then Channels +: the HR agent to Microsoft Teams and Microsoft 365 Copilot, the Sales agent to a website — and why a channel is a door, not a brain"), HND, "lab", LAB_SLIDES["lab_17"]),
    (5,  "Course synthesis and briefing before the assessment", DISC, "topic", SEC["synthesis"]),
    (60, "Written Assessment (WA / SAQ) — 1 hour, open book", ASMT, "assess", SEC["assessment_and_closing"]),
    (60, "Practical Performance (PP) Assessment — 1 hour, open book", ASMT, "assess", SEC["assessment_and_closing"]),
])
assert DAY1[-1][0].endswith("6:30") and DAY2[-1][0].endswith("6:30"), (DAY1[-1][0], DAY2[-1][0])


def total(rows):
    return sum(int(r[1].split()[0]) for r in rows)


def instructional(rows):
    """House standard: 9:30am-6:30pm = 540 elapsed minutes, less the 1-hour lunch,
    leaves exactly 480 instructional minutes per day. Tea breaks are counted
    WITHIN the instructional window, so only lunch is deducted."""
    return total(rows) - sum(
        int(r[1].split()[0]) for r in rows if r[2].strip().lower() == "lunch"
    )


for nm, rows in [("Day 1", DAY1), ("Day 2", DAY2)]:
    assert total(rows) == 540, f"{nm} elapsed = {total(rows)} min (expected 540: 9:30am-6:30pm)"
    assert instructional(rows) == 480, (
        f"{nm} instructional = {instructional(rows)} min (expected 480)"
    )
for lab_id, meta in LAB_META.items():
    if meta.get("optional"):
        continue  # optional labs run self-paced and hold no schedule slot (none in v8.0)
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
          "Power Automate workflows with AI agents, all built in one designer — Microsoft Copilot Studio (new "
          "experience), where workflows and agents live side by side; classic Power Automate is only the connector "
          "engine underneath. The course is taught concepts first: five concept modules each introduce the ideas "
          "and the decision rules, and the 18 labs (Lab 0–17) that follow apply them. Day 1 moves from "
          "deterministic Forms-driven workflows (email, Excel logging, approval branching) through an inbox "
          "workflow where a Classify node chooses the branch, to Copilot Studio agents built one part at a time — "
          "instructions and knowledge, tools, public knowledge, skills. Day 2 orchestrates a multi-agent team, "
          "crosses the workflow/agent boundary in both directions, puts an agent behind a website over HTTP, adds "
          "a human review gate, grounds an agent in documents with RAG — first with built-in knowledge, then with "
          "an external Pinecone vector store — and publishes an agent to Teams, Microsoft 365 Copilot and the web. "
          "Participants finish with working automations and sit the WSQ assessment at the end of Day 2.")
info_table(doc, [
    ("Course Title", TITLE),
    ("TGS Ref No", COURSE_CODE),
    ("Duration", "2 Days (9:30am – 6:30pm; 8 instructional hours per day, excluding a 1-hour lunch; two 15-minute tea breaks counted within); assessment on Day 2, 4:30 – 6:30pm"),
    ("Delivery", "Instructor-led, hands-on (physical / virtual)"),
    ("Audience", "Business and operations staff who want to automate repetitive work; no coding required"),
    ("Prerequisites", "Basic Microsoft 365 familiarity (Outlook, Excel, Teams); a Microsoft 365 work or school account, a Power Platform Developer environment with Dataverse and Copilot Credits, and Copilot Studio switched to the new experience (all set up in Lab 0); a free Pinecone account for Lab 16"),
    ("Labs", "18 step-by-step labs (Lab 0–17) across 2 days, every one built in the new Copilot Studio designer: Labs 0–8 on Day 1 (environment, three workflows, email classification, four agents), Labs 9–17 on Day 2 (multi-agent, agent flows, three HTTP labs, two RAG labs, publishing), driven by 5 concept modules"),
    ("Assessment", "Written Assessment (SAQ) 1 hr + Practical Performance (PP) 1 hr — Day 2, 4:30 – 6:30pm, open book"),
])

heading(doc, "Learning Outcomes", 1)
para(doc, "By the end of the course, participants will be able to:")
bullets(doc, [
    "Explain business process automation and the Trigger → Actions → Output model, and identify the four trigger families and the six action families.",
    "Build Forms-driven Copilot Studio workflows that send email, log data to Excel, branch on a condition and suspend for a human approval, and use a Classify node to route incoming email.",
    "Describe an agent as instructions, skills, knowledge, tools and connected agents, and state which of those the model can ignore.",
    "Create and ground Copilot Studio agents in approved SharePoint knowledge, add tools and skills, orchestrate connected agents, test their refusals, and publish them to Microsoft Teams, Microsoft 365 Copilot and a website.",
    "Connect a website to an HTTP-triggered agent flow, apply a JSON schema and use structured output to branch on the agent's decision.",
    "Apply the boundary of agency and human-in-the-loop patterns so consequential actions require a person before they take effect.",
    "Build a Retrieval Augmented Generation chatbot with built-in knowledge and with an external Pinecone vector store, and justify the choice between them.",
])

heading(doc, "Daily Schedule", 1)
para(doc, "The Slides column maps each session to the matching slides in the facilitator deck "
          f"(Business Process Automation with Power Automate and Copilot Studio Agents-v{VERSION}.pptx, {DECK_SLIDES} slides) so trainers can pace delivery against the deck.")
for nm, theme, rows in [
    ("Day 1 — Workflows, then Agents", "Modules 1–3: automation concepts, triggers and actions, control flow and human in the loop, email classification, then the agent one part at a time — Labs 0–8", DAY1),
    ("Day 2 — Multi-Agent, Agent Flows, Human Review, RAG, Publishing & Assessment", "Module 3 continued, then Modules 4–5: the multi-agent content team, the workflow/agent boundary crossed both ways, HTTP and the boundary of agency, the human review gate, RAG twice over, and publishing to channels — Labs 9–17, then the assessment", DAY2),
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
        shown = lab.get("duration_label", lab["duration_minutes"])
        duration = (f"Duration: {shown} minutes (optional — self-paced extension). "
                    if lab.get("optional") else f"Duration: {shown} minutes. ")
        para(doc, duration + "Follow the matching detailed, "
                  "step-by-step lab and its shared workflow visual in the Learner Guide.")

heading(doc, "Tools & Resources", 1)
info_table(doc, [
    ("Microsoft Copilot Studio (new experience)", "copilotstudio.microsoft.com — the one designer for every lab: build and run workflows, build and publish agents"),
    ("Microsoft Power Automate", "make.powerautomate.com — the connector engine underneath the workflows; never opened directly in this course"),
    ("Power Platform admin center", "admin.powerplatform.microsoft.com — provision/reset one Training Class Sandbox per cohort (Dataverse + Copilot Credits)"),
    ("Microsoft 365", "Outlook, Excel (OneDrive), Microsoft Forms, SharePoint and Microsoft Teams"),
    ("Pinecone", "pinecone.io — free-tier vector database, required for Lab 16 only"),
    ("Learner Guide", "Full step-by-step guide for every lab (LMS + course GitHub repository)"),
    ("LMS", LMS + " — courseware download, TRAQOM, assessment submission"),
])

heading(doc, "Assessment", 1)
para(doc, "The summative WSQ assessment is taken at the end of Day 2 and is open book "
          "(slides, Learner Guide and approved materials only):")
bullets(doc, [
    "Written Assessment (WA / SAQ) — 1 hour. Open-ended short-answer questions testing the knowledge from Modules 1–5.",
    "Practical Performance (PP) — 1 hour. Candidates build a working workflow and agent in Copilot Studio, mirroring the hands-on labs.",
    "Assessment flow: TRAQOM survey (QR on the LMS) → Assessment digital attendance → WA then PP → submit answers on the LMS → sign the Assessment Summary Record.",
    "WSQ funding requires a minimum of 75% attendance AND a Competent (C) assessment outcome.",
    f"Courseware and the assessment are on the LMS: {LMS}",
])
para(doc, "Formative assessment is continuous: each lab includes a Checkpoint that the facilitator verifies before "
          "the class moves on. Labs 1–4 verify deterministic workflows and the first model-chosen branch; Labs 5–8 "
          "verify one agent part at a time; Labs 9–11 verify multi-agent delegation and the workflow/agent boundary "
          "in both directions; Labs 12–14 progressively verify an HTTP-triggered agent flow, an unsupervised public "
          "chatbot and a blocking human review gate; Labs 15–16 verify the same grounded chatbot built two different "
          "ways, including the probes that test whether either will invent an answer; Lab 17 verifies the published "
          "agent in each channel.")

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
