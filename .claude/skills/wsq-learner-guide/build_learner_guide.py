#!/usr/bin/env python3
"""
Single-source Learner Guide generator for
"Microsoft Copilot Studio & Power Automate for Business Workflow Automation".

Compiles the actual lab + module markdown under ./labs/ into BOTH:
  - LEARNER-GUIDE.md                                            (repo root)
  - courseware/Microsoft Copilot Studio & Power Automate ... Learner Guide.docx
so the two are always aligned. Re-run after editing any lab.
"""
import os, re, sys

SKILL = "/Users/alfredang/.claude/skills/tertiary-learner-guide"
sys.path.insert(0, SKILL)
import prodoc
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE as RT

# script lives at .claude/skills/wsq-learner-guide/ — repo root is 3 levels up
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TITLE = "Business Process Automation with Power Automate and Copilot Studio Agents"
VERSION = "7.3.2"
COURSE_CODE = "TGS-2022017524"
ORG = "Tertiary Infotech Academy Pte Ltd"
UEN = "201200696W"
VERSIONS = [
    ["1.0", "24 Jun 2026", "Initial release — full 3-day, 17-lab learner guide.",
     "Course Development Team"],
    ["2.0", "2 Jul 2026", "WSQ revision — new course title, labs updated to the current "
     "Copilot Studio / Power Automate UI, dedicated course environment, WSQ cover page.",
     "Course Development Team"],
    ["3.0", "3 Jul 2026", "Course restructured from 3 days to 2 days — Day 1: Power Automate "
     "(Labs 0-5), Day 2: Copilot Studio agents (Labs 6-11) ending with the WSQ assessment. "
     "Modules 4-5 and Labs 12-16 retired.",
     "Course Development Team"],
    ["3.1", "24 Jul 2026", "Added Day 1 Labs 6A-6B: external online-form and browser-chatbot "
     "webhooks using the Power Automate HTTP Request trigger, with both new and classic "
     "designer guidance.",
     "Course Development Team"],
    ["3.2", "24 Jul 2026", "Reframed Lab 7 as the complete Copilot Studio IT Support RAG "
     "Chatbot outcome: approved FAQ retrieval, citations, negative testing, and grounded refusal.",
     "Course Development Team"],
    ["3.3", "24 Jul 2026", "Restructured Labs 8-10 into two-part Teams and website "
     "experiences: ordinary HTTP Power Automate flow, deterministic agent flow, and guarded "
     "AI prompt flow.",
     "Course Development Team"],
    ["3.4", "24 Jul 2026", "Day 2 now concludes at Lab 10. Retired Lab 11 and "
     "allocated the remaining guided time to integrated testing, troubleshooting and recap.",
     "Course Development Team"],
    ["3.5", "24 Jul 2026", "Made importable Power Automate packages the recommended "
     "classroom path and added a ready-made Lab 8 website enquiry flow package.",
     "Course Development Team"],
    ["3.6", "24 Jul 2026", "Made natural-language flow creation the primary Lab 1 "
     "route: prompt Copilot, inspect and correct the generated draft, then test; "
     "retained manual and import recovery routes.",
     "Course Development Team"],
    ["3.7", "24 Jul 2026", "Reorganised Copilot Studio Labs 6-10 into two coherent "
     "projects: prompt-created IT Support agent upgraded with RAG, then one Marina Trust "
     "agent progressively upgraded with HTTP, deterministic and AI prompt flows.",
     "Course Development Team"],
    ["3.8", "24 Jul 2026", "Added a visual architecture flowchart to every lab, "
     "standardised manual-build and packaged-import routes, and clarified how a "
     "Copilot Studio agent calls Power Automate agent flows as tools.",
     "Course Development Team"],
    ["3.9", "24 Jul 2026", "Reordered the labs from simple to complex: instant, "
     "scheduled, automated, human approval, HTTP, agent creation, RAG, channel "
     "deployment, deterministic agent flow and controlled prompt flow.",
     "Course Development Team"],
    ["4.0", "24 Jul 2026", "Aligned Lab 6A with the current sandbox flow: POST "
     "string trigger contract, imported manual label, training Outlook connection, "
     "classroom recipient, business-banking subject and exact JSON response.",
     "Course Development Team"],
    ["5.0", "25 Jul 2026", "Rebuilt the two-day learning journey around Forms-driven "
     "enquiry, event and leave workflows; specialised IT, HR and Finance agents; "
     "HTTP/webhook websites; and a multi-timeframe trading-information capstone.",
     "Course Development Team"],
    ["5.1", "25 Jul 2026", "Expanded Labs 1-10 into detailed click-by-click activities "
     "and added a shared labelled workflow flowchart to every lab, Learner Guide activity "
     "and matching facilitator-deck lab overview.",
     "Course Development Team"],
    ["5.2", "25 Jul 2026", "Standardised canonical Lab 1-10 titles, durations, slide ranges "
     "and shared flowchart mappings across the labs, Learner Guide Markdown, DOCX/PDF, "
     "Lesson Plan and facilitator deck.",
     "Course Development Team"],
    ["6.0", "25 Jul 2026", "Major concept-first overhaul aligned to the 113-slide deck: "
     "expanded cloud-flow types, trigger design, six Copilot agent building blocks, "
     "HTTP/webhook foundations, finance tools and the canonical Lab 1-10 sequence.",
     "Course Development Team"],
    ["6.0-S1", "25 Jul 2026", "Added supplementary Lab 11 to compare a Copilot agent "
     "calling a deterministic agent flow with a triggered agent flow calling a "
     "published agent for structured travel-expense review.",
     "Course Development Team"],
    ["6.1", "26 Jul 2026", "Updated Copilot Studio labs for the new agent and workflow interfaces.",
     "Course Development Team"],
    ["6.2", "26 Jul 2026", "Updated Lab 9 to use the new Copilot Studio HTTP workflow canvas and Agent node.",
     "Course Development Team"],
    ["6.2-S1", "29 Jul 2026", "Retained the AI Trading Advisor as Lab 10 and "
     "replaced the supplementary Lab 11 activity with the published Forms-based "
     "Procurement Request approval and outcome-notification workflow.",
     "Course Development Team"],
    ["7.0", "2 Aug 2026", "Rebuilt around the canonical Lab 0-10 sequence and five new "
     "concept modules (business process automation and Power Automate; control flow and "
     "human in the loop; Copilot Studio agents; agent flows, HTTP and the boundary of "
     "agency; retrieval augmented generation). Lab 0 now creates a Copilot Studio Training "
     "Developer environment with Copilot Credits. Labs cover trigger and actions, Excel "
     "logging, leave approval, four Copilot Studio agents, agent invocation and grounding, "
     "three HTTP labs including a blocking human review gate, and RAG built twice - with "
     "built-in knowledge and with Pinecone.",
     "Course Development Team"],
    ["7.1", "6 Aug 2026", "House cover updated with the Tertiary Infotech Academy logo; "
     "aligned to the expanded 75-slide v7.1 deck (new Copilot Studio design content and "
     "the training-accounts slide).",
     "Course Development Team"],
    ["7.2", "6 Aug 2026", "Lab 5 replaced — renamed from Invoke Agents to Calling Agent "
     "from Workflow: an agent flow that collects a blog topic at the Start node, drafts "
     "the post with M365 Copilot and posts it to the Training team's General channel.",
     "Course Development Team"],
    ["7.3", "6 Aug 2026", "Aligned to the 13-lab structure and the 80-slide v7.3 deck — "
     "added Lab 4b (Multi-Agent Content Team, optional) and Lab 5b (Calling Workflow from "
     "Agent) as full activities, and expanded Lab 4 with detailed step-by-step "
     "skill-package upload instructions.",
     "Course Development Team"],
    ["7.3.1", "7 Aug 2026", "Lab 8 updated to the current Human review node: input types "
     "are Text/Yes-No/Email/Number/Date (no Choice type), Outcome is a Yes/No boolean compared "
     "against true in the If/Else, and the approval card arrives in the Teams Workflows bot chat "
     "rather than the Approvals app. Verified live and the classroom flow repaired end to end.",
     "Course Development Team"],
    ["7.3.2", "7 Aug 2026", "Lab 8 build screenshots added — the finished designer canvas and "
     "the If/Else condition (Outcome Equals Yes) — captured from the live repaired flow.",
     "Course Development Team"],
]

# ---- neutral (un-branded) cover + footer: this is client training, no Tertiary branding ----
from docx.enum.text import WD_BREAK, WD_ALIGN_PARAGRAPH
BRAND = RGBColor(0x1F, 0x6F, 0xEB); DARK = RGBColor(0x16, 0x1B, 0x26)
def _cline(doc, text, size, bold=False, color=DARK, before=0, after=4):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = "Arial"
    return p
def add_cover_neutral(doc, kind, title, version, course_code):
    for _ in range(2): doc.add_paragraph()
    lp_ = doc.add_paragraph(); lp_.alignment = WD_ALIGN_PARAGRAPH.CENTER
    lp_.add_run().add_picture(os.path.join(REPO, ".claude", "skills", "tertiary-learner-guide", "assets", "tertiary-infotech-logo.png"), width=Inches(1.1))
    doc.add_paragraph()
    _cline(doc, ORG, 13, bold=True, after=2)
    _cline(doc, f"UEN: {UEN}", 10, color=GREY, after=20)
    _cline(doc, kind.upper(), 26, bold=True, color=BRAND, after=12)
    _cline(doc, "For", 12, color=GREY, after=8)
    _cline(doc, title, 20, bold=True, color=DARK, after=14)
    _cline(doc, f"TGS Ref No: {course_code}", 12, color=GREY, after=20)
    _cline(doc, "Conducted by", 12, color=GREY, after=6)
    _cline(doc, ORG, 13, bold=True, after=2)
    _cline(doc, f"UEN: {UEN}", 10, color=GREY, after=18)
    _cline(doc, f"Version {version}", 12, bold=True, color=BRAND)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
def add_footer_neutral(doc, title):
    sec = doc.sections[0]; footer = sec.footer; footer.is_linked_to_previous = False
    p = footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.text = ""
    r = p.add_run("Page "); r.font.size = Pt(9); r.font.color.rgb = GREY
    prodoc._field(p, "PAGE", "1").font.size = Pt(9)
    r2 = p.add_run(" of "); r2.font.size = Pt(9); r2.font.color.rgb = GREY
    prodoc._field(p, "NUMPAGES", "1").font.size = Pt(9)
    sp = footer.add_paragraph(); sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = sp.add_run(f"{title}  ·  © {ORG}"); sr.font.size = Pt(7.5); sr.font.color.rgb = GREY

# ---- course structure: ordered (day-heading, [files]) ----
DAYS = [
    ("Day 1 — Workflows, then Agents", [
        "labs/Module 1 - Business Process Automation and Power Automate.md",
        "labs/Lab 0 - Environment Setup/index.md",
        "labs/Lab 1 - Trigger and Actions/index.md",
        "labs/Lab 2 - Log to Excel/index.md",
        "labs/Module 2 - Control Flow and Human in the Loop.md",
        "labs/Lab 3 - Leave Application Approval/index.md",
        "labs/Module 3 - Copilot Studio Agents.md",
        "labs/Lab 4 - Agents /README.md",
        "labs/Lab 4b - Multi-Agent Content Team/README.md",
    ]),
    ("Day 2 — Agent Flows, Human Review and RAG", [
        "labs/Lab 5 - Calling Agent from Workflow/index.md",
        "labs/Lab 5b - Calling Workflow from Agent/index.md",
        "labs/Module 4 - Agent Flows, HTTP and the Boundary of Agency.md",
        "labs/Lab 6 - HTTP and Application Approval Agent/README.md",
        "labs/Lab 7 - HTTP and Chatbot/README.md",
        "labs/Lab 8 - HTTP and Human Review/README.md",
        "labs/Module 5 - Retrieval Augmented Generation.md",
        "labs/Lab 9 - RAG with Knowledge Base/README.md",
        "labs/Lab 10 - RAG with Pinecone/README.md",
    ]),
]


# ============================================================================
# Markdown -> generic blocks
# ============================================================================
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
# Lab markdown carries raw <a href="..." target="_blank">text</a> for new-tab links.
# Word has no equivalent, and the raw tag would print literally — keep the text only.
_ANCHOR_RE = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S)
_TAG_RE = re.compile(r"</?(?:a|span|div|br)\b[^>]*>", re.I)


def strip_html(t):
    t = _ANCHOR_RE.sub(lambda m: m.group(2).strip() or m.group(1), t)
    return _TAG_RE.sub("", t)
def clean(t):
    return LINK.sub(r"\1", strip_html(t)).rstrip()

def link_copilot_studio(t):
    return t.replace(
        "Open Copilot Studio",
        "[Open Copilot Studio](https://copilotstudio.microsoft.com)",
    )

def md_to_blocks(text, source_path):
    lines = text.split("\n")
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        s = ln.strip()
        # code fence
        if s.startswith("```"):
            buf = []; i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            blocks.append(("code", "\n".join(buf))); continue
        # blank
        if not s:
            i += 1; continue
        # heading
        m = re.match(r"(#{1,6})\s+(.*)", s)
        if m:
            blocks.append(("h", len(m.group(1)), clean(m.group(2)))); i += 1; continue
        # image
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", s)
        if m:
            alt, target = m.group(1), m.group(2)
            absolute = os.path.normpath(os.path.join(os.path.dirname(source_path), target))
            repo_relative = os.path.relpath(absolute, REPO).replace(os.sep, "/")
            blocks.append(("image", absolute, alt, repo_relative)); i += 1; continue
        # horizontal rule
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            blocks.append(("rule",)); i += 1; continue
        # table
        if s.startswith("|") and "|" in s[1:]:
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not re.match(r"^:?-{2,}:?$", cells[0]):  # skip separator row
                    rows.append([clean(c) for c in cells])
                i += 1
            if rows: blocks.append(("table", rows))
            continue
        # blockquote (collect consecutive)
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]).rstrip()); i += 1
            # A callout often opens with its own "### Heading" line and may carry a
            # fenced code sample. Word has no nested heading or fence inside a Note
            # box, so drop the markers and keep the words.
            buf = [re.sub(r"^\s*#{1,6}\s*", "", x) for x in buf]
            buf = [x for x in buf if not x.strip().startswith("```")]
            content = clean(" ".join(x for x in buf if x.strip()))
            if content: blocks.append(("note", content))
            continue
        # numbered list. Each item is [text, [sub-bullets]]: indented "- " lines
        # become nested bullets; other indented lines are source line-wraps and
        # join their step (or the open sub-bullet) with a single space.
        if re.match(r"^\d+\.\s+", s):
            items = []
            start_number = None
            while i < n:
                raw = lines[i]
                mm = re.match(r"^\s*(\d+)\.\s+(.*)", raw)
                if mm:
                    if start_number is None:
                        start_number = int(mm.group(1))
                    items.append([clean(mm.group(2)), []])
                elif re.match(r"^\s{2,}\S", raw) and not raw.strip().startswith("```"):
                    if not items:
                        pass
                    elif re.match(r"^\s+[-*]\s+", raw):
                        items[-1][1].append(clean(re.sub(r"^\s*[-*]\s+", "", raw.strip())))
                    elif items[-1][1]:
                        items[-1][1][-1] = items[-1][1][-1] + " " + clean(raw.strip())
                    else:
                        items[-1][0] = items[-1][0] + " " + clean(raw.strip())
                elif raw.strip() == "":
                    # blank: peek if list continues
                    j = i + 1
                    if j < n and re.match(r"^\s*\d+\.\s+", lines[j]):
                        i += 1; continue
                    else:
                        break
                else:
                    break
                i += 1
            blocks.append(("steps", items, start_number or 1)); continue
        # bullet list (indented non-bullet lines are source line-wraps of the
        # open item and join it with a single space)
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n:
                raw = lines[i]
                if re.match(r"^\s*[-*]\s+", raw):
                    items.append(clean(re.sub(r"^\s*[-*]\s+", "", raw.strip())))
                elif (re.match(r"^\s{2,}\S", raw) and items
                      and not raw.strip().startswith("```")):
                    items[-1] = items[-1] + " " + clean(raw.strip())
                else:
                    break
                i += 1
            blocks.append(("bullets", items)); continue
        # plain paragraph: join source-wrapped lines so inline Markdown tokens
        # are not split across separate DOCX paragraphs or page boundaries.
        buf = [s]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if not nxt:
                break
            if (
                nxt.startswith("```")
                or re.match(r"(#{1,6})\s+", nxt)
                or re.match(r"!\[([^\]]*)\]\(([^)]+)\)", nxt)
                or re.match(r"^(-{3,}|\*{3,}|_{3,})$", nxt)
                or (nxt.startswith("|") and "|" in nxt[1:])
                or nxt.startswith(">")
                or re.match(r"^\d+\.\s+", nxt)
                or re.match(r"^[-*]\s+", nxt)
            ):
                break
            buf.append(nxt)
            i += 1
        blocks.append(("p", clean(" ".join(buf))))
    return blocks

# ============================================================================
# Assemble the DSL block list B
# ============================================================================
B = []
def h2(t): B.append(("h2", t))
def h3(t): B.append(("h3", t))
def p(t):  B.append(("p", t))
def note(t):
    # A blockquote may contain its own "### Heading" line; Word has no nested
    # heading inside a callout, so print the words without the hash markers.
    B.append(("note", re.sub(r"(?m)^\s*#{1,6}\s*", "", t)))
def rule(): B.append(("rule",))

# Title + intro
B.append(("h1", "Learner Guide"))
p(f"Welcome! This Learner Guide takes you **click-by-click** through every hands-on lab in the WSQ course "
  f"**{TITLE}** (Course Code: {COURSE_CODE}). Over two days you go from your first Power Automate flow "
  f"to AI business agents in Microsoft Copilot Studio — and finish by connecting an agent to your flows in a "
  f"complete end-to-end automated workflow.")
p("Work through the labs **in order**: each one builds on the skills of the lab before it. Whenever you see a "
  "**Checkpoint**, stop and confirm your flow or agent behaves as described before moving on. The "
  "**Common Errors & Quick Fixes** and per-lab **Troubleshooting** tables will get you unstuck fast.")
note("Course flow at a glance — Day 1: Forms-driven email, Excel, branching and approval "
     "flows - trigger and actions, Excel logging and a leave approval that pauses for a "
     "manager - then Copilot Studio agents and what they are made of (Labs 0-4, with the "
     "optional multi-agent Lab 4b). Day 2: the agent and the workflow calling each other "
     "(Labs 5 and 5b), three HTTP labs including a blocking human review "
     "gate, and RAG built twice - with built-in knowledge and with Pinecone (Labs 6-10), "
     "then the WSQ assessment (4:00-6:00 PM).")
rule()

# Common errors reference (mirrors the deck's quick-fix slide)
h2("Common Errors & Quick Fixes")
p("Keep this handy — these are the issues learners hit most often, with the one-line fix:")
B.append(("table", [
    ["Symptom", "Cause", "Fix"],
    ["“Unauthorized” when sending email", "Outlook connection expired or the account has no mailbox",
     "Reconnect the Office 365 Outlook connection with a mailbox-enabled account; both connections must be green ✓"],
    ["Approval fails: “valid users in the organization”", "Approver typed as an external email, not a tenant user",
     "Pick the approver from the people-picker dropdown (a real user in your tenant; yourself is fine for testing)"],
    ["Date logs as literal text ‘utcNow()’", "Expression typed into the field as text",
     "Enter it via the fx / Expression editor so it becomes a coloured token"],
    ["Excel cell shows ########", "The column is only too narrow", "Auto-fit the column — the value is fine"],
    ["An unwanted ‘For each’ wraps your action", "You inserted a list/array value into a single-value field",
     "Use single-value fields (Outcome, trigger inputs); delete the For each and re-add a plain action"],
    ["Agent can’t see its flow", "Agent and flow are in different environments",
     "Set both Copilot Studio and Power Automate to the same environment (Copilot Studio Training)"],
]))
rule()

for day_title, files in DAYS:
    h2(day_title)
    for rel in files:
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            print("  [missing]", rel); continue
        raw = open(path, encoding="utf-8").read()
        gblocks = md_to_blocks(raw, path)
        first_h1_done = False
        for gb in gblocks:
            if gb[0] == "h":
                lvl, txt = gb[1], gb[2]
                if lvl == 1 and not first_h1_done:
                    h3(txt); first_h1_done = True            # lab/module title -> Heading 2
                else:
                    p(f"**{txt}**")                           # sections / steps -> bold line
            else:
                B.append(gb)
        rule()

# ============================================================================
# Renderers (markdown + docx)
# ============================================================================
def _anchor(txt):
    # GitHub slug rules: lowercase, strip punctuation, EACH space becomes a
    # hyphen (so "A — B" and "A & B" produce double hyphens, not one).
    return re.sub(r"[^\w\- ]", "", txt.lower()).replace(" ", "-")

def _toc(blocks):
    out = ["## Table of Contents", ""]
    for b in blocks:
        if b[0] == "h2":
            out.append(f"- [{b[1]}](#{_anchor(b[1])})")
        elif b[0] == "h3":
            out.append(f"  - [{b[1]}](#{_anchor(b[1])})")
    out.append("")
    return "\n".join(out)

def render_markdown(blocks):
    out = []; injected = False
    for index, b in enumerate(blocks):
        k = b[0]
        if k == "h1":
            out.append(f"# {b[1]}\n")
            if not injected:
                out.append(f"**Course Code:** {COURSE_CODE}  ·  **Version {VERSION}**\n")
                out.append("### Document Version Control Record\n")
                out.append("| Version | Effective Date | Summary of Changes | Author |")
                out.append("| --- | --- | --- | --- |")
                for v in VERSIONS:
                    out.append(f"| {v[0]} | {v[1]} | {v[2]} | {v[3]} |")
                out.append("")
                out.append(_toc(blocks)); injected = True
            continue
        if k == "h2": out.append(f"## {b[1]}\n")
        elif k == "h3": out.append(f"### {b[1]}\n")
        elif k == "p": out.append(f"{b[1]}\n")
        elif k == "steps":
            step_lines = []
            for num, (txt, subs) in enumerate(b[1], b[2]):
                step_lines.append(f"{num}. {link_copilot_studio(txt)}")
                step_lines.extend(f"   - {sub}" for sub in subs)
            out.append("\n".join(step_lines) + "\n")
        elif k == "bullets": out.append("\n".join(f"- {s}" for s in b[1]) + "\n")
        elif k == "code": out.append("```\n" + b[1] + "\n```\n")
        elif k == "table":
            rows = b[1]
            out.append("| " + " | ".join(rows[0]) + " |")
            out.append("| " + " | ".join("---" for _ in rows[0]) + " |")
            for r in rows[1:]:
                out.append("| " + " | ".join(r) + " |")
            out.append("")
        elif k == "note": out.append(f"> {b[1]}\n")
        elif k == "image":
            # Angle brackets keep repository-relative image paths containing
            # spaces valid in CommonMark and GitHub Markdown.
            out.append(f"![{b[2]}](<{b[3]}>)\n")
        elif k == "rule": out.append("---\n")
    return "\n".join(out).strip() + "\n"

GREY = RGBColor(0x55,0x5B,0x66)
def _shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),hexc); tcPr.append(shd)
def _shade_para(pr, hexc="F3F5F8"):
    ppr = pr._p.get_or_add_pPr(); shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),hexc); ppr.append(shd)
def _add_hyperlink(par, text, url):
    relationship_id = par.part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)
    run = OxmlElement("w:r")
    run_properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); run_properties.append(color)
    underline = OxmlElement("w:u"); underline.set(qn("w:val"), "single"); run_properties.append(underline)
    run.append(run_properties)
    label = OxmlElement("w:t"); label.text = text; run.append(label)
    hyperlink.append(run)
    par._p.append(hyperlink)
def _runs(par, text):
    for part in re.split(r"(\*\*.*?\*\*|(?<!\*)\*[^*]+\*(?!\*)|`[^`]+`)", text):
        if not part: continue
        if part.startswith("**") and part.endswith("**"):
            r = par.add_run(re.sub(r"[*`]", "", part[2:-2])); r.bold = True
        elif part.startswith("*") and part.endswith("*"):
            r = par.add_run(part[1:-1]); r.italic = True
        elif part.startswith("`") and part.endswith("`"):
            r = par.add_run(part[1:-1]); r.font.name = "Consolas"; r.font.color.rgb = RGBColor(0xC7,0x25,0x4E)
        else:
            segments = part.split("Open Copilot Studio")
            for index, segment in enumerate(segments):
                if segment:
                    par.add_run(segment)
                if index < len(segments) - 1:
                    _add_hyperlink(par, "Open Copilot Studio", "https://copilotstudio.microsoft.com")

def _toc_field(doc):
    p = doc.add_paragraph()
    prodoc._field(p, 'TOC \\o "1-3" \\h \\z \\u', default="")


def add_static_toc(doc):
    # A real Word TOC field so the contents update and hyperlink when opened in
    # Word, followed by a readable outline for viewers that do not evaluate
    # fields (LibreOffice headless, and therefore the PDF we ship).
    _toc_field(doc)

    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = True
    r = p.add_run("TABLE OF CONTENTS"); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = DARK
    entries = []
    for day_name, files in DAYS:
        entries.append(day_name)
        for rel in files:
            stem = os.path.basename(os.path.dirname(rel)) if os.path.basename(rel) in ("index.md", "README.md") else os.path.basename(rel)[:-3]
            entries.append("    " + stem)
    for entry in entries:
        doc.add_paragraph(entry, style="List Bullet")
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def render_docx(blocks):
    doc = Document()
    nrm = doc.styles["Normal"]; nrm.font.name = "Arial"; nrm.font.size = Pt(11)
    prodoc.style_headings(doc)
    add_cover_neutral(doc, "Learner Guide", TITLE, VERSION, COURSE_CODE)
    prodoc.add_version_control(doc, VERSIONS)
    # prodoc adds an explicit page-break paragraph. Remove it and let the TOC
    # heading's page-break-before control pagination; otherwise a version table
    # that exactly fills a page can produce a blank footer-only page.
    version_break = doc.paragraphs[-1]
    version_break._element.getparent().remove(version_break._element)
    add_static_toc(doc)
    for index, b in enumerate(blocks):
        k = b[0]
        if k == "h1": continue
        elif k == "h2":
            doc.add_paragraph(style="Heading 1").add_run(b[1])
        elif k == "h3":
            paragraph = doc.add_paragraph(style="Heading 2")
            paragraph.add_run(b[1])
            if b[1].strip().lower() == "workflow visual":
                paragraph.paragraph_format.page_break_before = True
            if index + 1 < len(blocks) and blocks[index + 1][0] == "image":
                paragraph.paragraph_format.keep_with_next = True
        elif k == "p":
            paragraph = doc.add_paragraph()
            _runs(paragraph, b[1])
            if re.fullmatch(r"\*\*[^*]+\*\*", b[1].strip()):
                paragraph.paragraph_format.keep_with_next = True
            if b[1].strip("* ").lower() == "workflow visual":
                paragraph.paragraph_format.page_break_before = True
                paragraph.paragraph_format.keep_with_next = True
        elif k == "steps":
            # Preserve the list's source start number. This keeps numbered
            # procedures continuous when a code block splits the Markdown list.
            for number, (step_text, step_subs) in enumerate(b[1], start=b[2]):
                paragraph = doc.add_paragraph()
                paragraph.paragraph_format.left_indent = Inches(0.25)
                paragraph.paragraph_format.first_line_indent = Inches(-0.25)
                paragraph.add_run(f"{number}.  ")
                _runs(paragraph, step_text)
                for sub in step_subs:
                    sp = doc.add_paragraph()
                    sp.paragraph_format.left_indent = Inches(0.55)
                    sp.paragraph_format.first_line_indent = Inches(-0.18)
                    sp.add_run("•  ")
                    _runs(sp, sub)
        elif k == "bullets":
            for s in b[1]:
                _runs(doc.add_paragraph(style="List Bullet"), s)
        elif k == "code":
            pr = doc.add_paragraph(); _shade_para(pr)
            pr.paragraph_format.keep_together = True
            r = pr.add_run(b[1]); r.font.name = "Consolas"; r.font.size = Pt(9)
        elif k == "table":
            rows = b[1]
            t = doc.add_table(rows=0, cols=len(rows[0])); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for ri, row in enumerate(rows):
                cells = t.add_row().cells
                for ci, val in enumerate(row):
                    cells[ci].text = ""; pp = cells[ci].paragraphs[0]
                    if ri == 0:
                        rr = pp.add_run(re.sub(r"[*`]", "", val)); rr.bold = True; rr.font.color.rgb = RGBColor(0xFF,0xFF,0xFF); rr.font.size = Pt(9.5)
                        _shade(cells[ci], "1F6FEB")
                    else:
                        _runs(pp, val)
                        for rn in pp.runs: rn.font.size = Pt(9.5)
        elif k == "note":
            pr = doc.add_paragraph(); _shade_para(pr, "FFF4E5")
            rr = pr.add_run("Note:  "); rr.bold = True; rr.font.color.rgb = RGBColor(0xB5,0x6A,0x00)
            _runs(pr, b[1])
        elif k == "image":
            if os.path.exists(b[1]):
                pr = doc.add_paragraph()
                pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pr.paragraph_format.keep_with_next = True
                pr.add_run().add_picture(b[1], width=Inches(6.25))
                cap = doc.add_paragraph()
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.paragraph_format.space_after = Pt(8)
                rr = cap.add_run(f"Figure: {b[2]}")
                rr.italic = True
                rr.font.size = Pt(9)
                rr.font.color.rgb = GREY
        elif k == "rule":
            pr = doc.add_paragraph(); pr.paragraph_format.space_before = Pt(2); pr.paragraph_format.space_after = Pt(2)
            ppr = pr._p.get_or_add_pPr(); bdr = OxmlElement("w:pBdr"); bot = OxmlElement("w:bottom")
            bot.set(qn("w:val"),"single"); bot.set(qn("w:sz"),"6"); bot.set(qn("w:space"),"1"); bot.set(qn("w:color"),"D0D7DE")
            bdr.append(bot)
            # Paragraph properties are order-sensitive in WordprocessingML;
            # borders precede the spacing element created above.
            ppr.insert(0, bdr)
    add_footer_neutral(doc, TITLE)
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
    return doc

md = render_markdown(B)
with open(os.path.join(REPO, "LEARNER-GUIDE.md"), "w", encoding="utf-8") as f:
    f.write(md)
out_docx = os.path.join(REPO, f"courseware/LG-{TITLE}.docx")
render_docx(B).save(out_docx)
print("Wrote LEARNER-GUIDE.md (%d blocks, %d labs/modules headings)" %
      (len(B), sum(1 for b in B if b[0]=="h3")))
print("Wrote", out_docx)
