#!/usr/bin/env python3
"""Build the Version 7.0 facilitator deck.

Concepts first, labs second. The WSQ administrative and assessment slides are
inherited unchanged from Version 6.0; everything between the course-overview
block and the closing block is rebuilt as a concept-led sequence that covers
Power Automate, Copilot Studio, workflows, agents (tools / skills / knowledge),
multi-agent orchestration, every trigger type, every action family, RAG and
human-in-the-loop — each concept naming the lab where it is applied.
"""

from __future__ import annotations

import json
import pathlib
from pathlib import Path
from shutil import copy2

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
CW = ROOT / "courseware"
SOURCE = CW / "Business Process Automation with Power Automate and Copilot Studio Agents-v6.0.pptx"
if not SOURCE.exists():
    SOURCE = CW / "archive" / SOURCE.name
DECK = CW / "Business Process Automation with Power Automate and Copilot Studio Agents-v7.0.pptx"

ALIGNMENT = json.loads((CW / "alignment_manifest.json").read_text(encoding="utf-8"))
assert ALIGNMENT["version"] == "7.0"
LABS = {lab["id"]: lab for lab in ALIGNMENT["labs"]}

copy2(SOURCE, DECK)

BLUE = RGBColor(0x1F, 0x6F, 0xEB)
TEAL = RGBColor(0x10, 0x8A, 0x73)
GREEN = RGBColor(0x16, 0x84, 0x5B)
AMBER = RGBColor(0xC7, 0x76, 0x00)
VIOLET = RGBColor(0x6D, 0x3F, 0xD2)
RED = RGBColor(0xC2, 0x41, 0x3A)
INK = RGBColor(0x16, 0x1B, 0x26)
GREY = RGBColor(0x5B, 0x63, 0x72)
LINE = RGBColor(0xD7, 0xE0, 0xEA)
LIGHT = RGBColor(0xF5, 0xF8, 0xFC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALETTE = [BLUE, TEAL, VIOLET, AMBER, GREEN]

FOOTER_TEXT = (
    "Business Process Automation with Power Automate & Copilot Studio Agents  ·  "
    "TGS-2022017524  ·  © 2026 Tertiary Infotech Academy Pte Ltd"
)

prs = Presentation(DECK)
SW, SH = prs.slide_width, prs.slide_height

# ---------------------------------------------------------------- primitives


def clear(slide):
    tree = slide.shapes._spTree
    for shape in list(slide.shapes):
        tree.remove(shape._element)


def box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=True, line_w=1.2):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, x, y, w, h
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(line_w)
    shape.shadow.inherit = False
    return shape


def text(slide, x, y, w, h, value, size=18, color=INK, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, margin=0.08, space=0):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    for i, line_text in enumerate(str(value).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if space:
            p.space_after = Pt(space)
        r = p.add_run()
        r.text = line_text
        r.font.name = "Arial"
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return tb


def title(slide, heading, kicker):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.22), Inches(1.48))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()
    bar.shadow.inherit = False
    text(slide, Inches(0.72), Inches(0.34), Inches(11.8), Inches(0.28), kicker.upper(), 12, BLUE, True)
    text(slide, Inches(0.72), Inches(0.68), Inches(11.8), Inches(0.66), heading, 29, INK, True)
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(1.5), Inches(11.85), Inches(0.015))
    rule.fill.solid()
    rule.fill.fore_color.rgb = LINE
    rule.line.fill.background()
    rule.shadow.inherit = False


def footer(slide, slide_no):
    text(slide, Inches(0.72), Inches(6.95), Inches(11.85), Inches(0.24), FOOTER_TEXT, 8, GREY)
    text(slide, Inches(0.72), Inches(6.95), Inches(11.85), Inches(0.24), str(slide_no), 8, GREY, False, PP_ALIGN.RIGHT)


def card(slide, x, y, w, h, label, body, accent=BLUE, number=None,
         body_size=13, label_size=16):
    box(slide, x, y, w, h, LIGHT, LINE)
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.09), h)
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()
    stripe.shadow.inherit = False
    if number is not None:
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.24), y + Inches(0.2), Inches(0.46), Inches(0.46))
        circle.fill.solid()
        circle.fill.fore_color.rgb = accent
        circle.line.fill.background()
        circle.shadow.inherit = False
        text(slide, x + Inches(0.24), y + Inches(0.2), Inches(0.46), Inches(0.46), str(number), 15, WHITE, True, PP_ALIGN.CENTER)
        lx, lw = x + Inches(0.82), w - Inches(1.04)
    else:
        lx, lw = x + Inches(0.28), w - Inches(0.52)
    text(slide, lx, y + Inches(0.14), lw, Inches(0.44), label, label_size, accent, True)
    if body:
        text(slide, x + Inches(0.28), y + Inches(0.66), w - Inches(0.54), h - Inches(0.8),
             body, body_size, GREY, anchor=MSO_ANCHOR.TOP, space=4)


def arrow(slide, x, y, w, h, color=BLUE, direction="right"):
    kind = MSO_SHAPE.CHEVRON if direction == "right" else MSO_SHAPE.DOWN_ARROW
    shape = slide.shapes.add_shape(kind, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def flow(slide, y, nodes, labels=None, colors=None, x0=0.72, total=11.85,
         height=1.15, size=13):
    labels = labels or [""] * (len(nodes) - 1)
    colors = colors or [BLUE] * len(nodes)
    gap = 0.46
    node_w = (total - gap * (len(nodes) - 1)) / len(nodes)
    for i, node in enumerate(nodes):
        x = Inches(x0 + i * (node_w + gap))
        box(slide, x, Inches(y), Inches(node_w), Inches(height), WHITE, colors[i], line_w=1.6)
        text(slide, x + Inches(0.06), Inches(y + 0.06), Inches(node_w - 0.12), Inches(height - 0.12),
             node, size, INK, True, PP_ALIGN.CENTER)
        if i < len(nodes) - 1:
            arrow(slide, x + Inches(node_w + 0.07), Inches(y + height / 2 - 0.17),
                  Inches(0.3), Inches(0.34), colors[i])
            if labels[i]:
                text(slide, x + Inches(node_w - 0.14), Inches(y - 0.3), Inches(gap + 0.28),
                     Inches(0.26), labels[i], 9, GREY, False, PP_ALIGN.CENTER)


def table(slide, y, headers, rows, widths, colors=None, x0=0.72, row_h=0.52,
          head_h=0.46, size=12, head_size=12):
    colors = colors or [INK] * len(rows)
    overflow = (y + head_h + len(rows) * row_h) - BOTTOM_LIMIT
    if overflow > 0:                      # shrink rows rather than spill
        row_h = max(0.32, row_h - overflow / len(rows))
    total = sum(widths)
    hx = x0
    head = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0), Inches(y), Inches(total), Inches(head_h))
    head.fill.solid()
    head.fill.fore_color.rgb = BLUE
    head.line.fill.background()
    head.shadow.inherit = False
    for w, htext in zip(widths, headers):
        text(slide, Inches(hx + 0.14), Inches(y), Inches(w - 0.2), Inches(head_h), htext, head_size, WHITE, True)
        hx += w
    for r, row in enumerate(rows):
        ry = y + head_h + r * row_h
        bg = WHITE if r % 2 == 0 else LIGHT
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0), Inches(ry), Inches(total), Inches(row_h))
        band.fill.solid()
        band.fill.fore_color.rgb = bg
        band.line.color.rgb = LINE
        band.line.width = Pt(0.75)
        band.shadow.inherit = False
        cx = x0
        for c, (w, cell) in enumerate(zip(widths, row)):
            text(slide, Inches(cx + 0.14), Inches(ry), Inches(w - 0.2), Inches(row_h), cell,
                 size, colors[r] if c == 0 else GREY, c == 0)
            cx += w


def takeaway(slide, y, message, color=BLUE):
    y = min(y, BOTTOM_LIMIT - 0.62)
    band = box(slide, Inches(0.72), Inches(y), Inches(11.85), Inches(0.62), LIGHT, color, line_w=1.6)
    text(slide, Inches(1.0), Inches(y), Inches(11.3), Inches(0.62), message, 14, INK, True)
    return band


BOTTOM_LIMIT = 6.88   # nothing this project draws may extend past this
BANNER_TOP = 6.08     # the lab banner always sits here, below any takeaway band


def workflow_slide(lab_id):
    """A full-width lab workflow diagram, captioned with the lab banner."""
    lab = LABS[lab_id]
    png = ROOT / pathlib.PurePosixPath(lab["path"]).parent / "assets" / "flowchart.png"

    def draw(s):
        text(s, Inches(0.72), Inches(1.66), Inches(11.85), Inches(0.34),
             lab["teaches"], 13, GREY, anchor=MSO_ANCHOR.TOP)
        if png.exists():
            with Image.open(png) as im:
                iw, ih = im.size
            max_w, max_h = Inches(12.0), Inches(3.62)
            scale = min(max_w / iw, max_h / ih)
            w, h = int(iw * scale), int(ih * scale)
            top = Inches(2.12) + int((Inches(3.62) - h) / 2)
            s.shapes.add_picture(str(png), int((SW - w) / 2), top, w, h)
        lab_banner(s, 5.95, lab_id)

    return draw


def lab_banner(slide, y, lab_id, extra=None):
    lab = LABS[lab_id]
    y = BANNER_TOP
    box(slide, Inches(0.72), Inches(y), Inches(11.85), Inches(0.78), WHITE, GREEN, line_w=1.8)
    tag = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.92), Inches(y + 0.14), Inches(1.15), Inches(0.5))
    tag.fill.solid()
    tag.fill.fore_color.rgb = GREEN
    tag.line.fill.background()
    tag.shadow.inherit = False
    text(slide, Inches(0.92), Inches(y + 0.14), Inches(1.15), Inches(0.5), f"LAB {lab['number']}", 13, WHITE, True, PP_ALIGN.CENTER)
    body = extra or f"{lab['subtitle']}  ·  {lab['platform']}  ·  {lab['duration_minutes']} min"
    text(slide, Inches(2.25), Inches(y + 0.02), Inches(10.1), Inches(0.36), lab["title"], 14, INK, True)
    text(slide, Inches(2.25), Inches(y + 0.38), Inches(10.1), Inches(0.34), body, 11, GREY)


# ------------------------------------------------------------------ builders

SLIDES = []


def slide(heading, kicker, draw):
    SLIDES.append((heading, kicker, draw))


def divider(kicker, heading, subtitle, color=BLUE):
    def draw(s):
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = WHITE
        panel = slide_panel = box(s, Inches(0.72), Inches(1.9), Inches(11.85), Inches(3.6), LIGHT, color, line_w=2.0)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(1.9), Inches(0.14), Inches(3.6))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()
        bar.shadow.inherit = False
        text(s, Inches(1.4), Inches(2.35), Inches(10.8), Inches(0.4), kicker.upper(), 15, color, True)
        text(s, Inches(1.4), Inches(2.85), Inches(10.8), Inches(0.95), heading, 34, INK, True)
        text(s, Inches(1.4), Inches(3.95), Inches(10.8), Inches(1.1), subtitle, 15, GREY, anchor=MSO_ANCHOR.TOP, space=6)
    return draw


# ===========================================================================
# COURSE OVERVIEW  (rebuilt slides 7-10, 14-15)
# ===========================================================================

def draw_outcomes(s):
    flow(s, 1.95, ["Automate\nthe workflow", "Build\nthe agent", "Connect it\nover HTTP", "Ground it\nwith RAG"],
         ["add AI", "expose it", "make it true"], [BLUE, VIOLET, GREEN, AMBER], height=1.3, size=14)
    items = [
        ("Design", "Read a business process and decide which parts must be deterministic and which may be AI.", BLUE),
        ("Build", "Create Power Automate flows and Copilot Studio agents with tools, skills and knowledge.", VIOLET),
        ("Govern", "Place a human where the consequence lands, and test what the agent must refuse.", RED),
    ]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(3.95), Inches(3.71), Inches(1.85), label, body, color, i + 1)
    takeaway(s, 6.1, "By the end you can build the automation, add the agent, and defend where you put the human.")


def draw_lab_journey(s):
    rows = [
        ("0", "Environment Setup", "Developer environment, Dataverse, credits", BLUE),
        ("1", "Trigger and Actions", "Form → email; dynamic content", BLUE),
        ("2", "Log to Excel", "Commit the audit row before confirming", BLUE),
        ("3", "Leave Application Approval", "The flow pauses for a manager", TEAL),
        ("4", "Agents", "Instructions · skills · knowledge · tools", VIOLET),
        ("5", "Invoke Agents", "SharePoint grounding, published to Teams", VIOLET),
        ("6", "HTTP + Approval Agent", "Structured output; the AI never writes the record", GREEN),
        ("7", "HTTP + Chatbot", "The agent alone, in public", GREEN),
        ("8", "HTTP + Human Review", "The run that will not proceed", RED),
        ("9", "RAG with Knowledge Base", "Three nodes, no ingestion", AMBER),
        ("10", "RAG with Pinecone", "Chunking, embeddings, top_k", AMBER),
    ]
    for i, (num, name, note, color) in enumerate(rows):
        col, row = (0, i) if i < 6 else (1, i - 6)
        x = Inches(0.72 + col * 6.0)
        y = Inches(1.66 + row * 0.72)
        box(s, x, y, Inches(5.85), Inches(0.64), LIGHT, LINE)
        chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.12), y + Inches(0.08), Inches(0.48), Inches(0.48))
        chip.fill.solid()
        chip.fill.fore_color.rgb = color
        chip.line.fill.background()
        chip.shadow.inherit = False
        text(s, x + Inches(0.12), y + Inches(0.08), Inches(0.48), Inches(0.48), num, 13, WHITE, True, PP_ALIGN.CENTER)
        text(s, x + Inches(0.72), y + Inches(0.02), Inches(5.02), Inches(0.32), name, 12, INK, True)
        text(s, x + Inches(0.72), y + Inches(0.32), Inches(5.02), Inches(0.3), note, 9.5, GREY)
    takeaway(s, 6.1, "Eleven labs, each reusing the one before it. Nothing is rebuilt from scratch.")


def draw_approach(s):
    steps = [
        ("Concept", "The idea and the decision rule, before the product is opened.", BLUE),
        ("Pattern", "The same idea drawn as a business workflow you could hand to a colleague.", TEAL),
        ("Lab", "You build it, in the numbered lab named on the concept slide.", GREEN),
        ("Probe", "You try to break it — the refusals and wrong answers are the lesson.", RED),
        ("Reuse", "The working artefact becomes the starting point of the next lab.", VIOLET),
    ]
    for i, (label, body, color) in enumerate(steps):
        x = Inches(0.72 + i * 2.42)
        card(s, x, Inches(2.0), Inches(2.2), Inches(2.5), label, body, color, i + 1, 11, 15)
    takeaway(s, 5.0, "Concepts first. Every lab in this course is an application of a concept you have already seen.")
    text(s, Inches(0.72), Inches(5.85), Inches(11.85), Inches(0.9),
         "The probes matter as much as the builds. An agent that answers ten questions correctly and the eleventh\n"
         "confidently wrong has not been tested — it has been demonstrated.", 13, GREY, anchor=MSO_ANCHOR.TOP)


def draw_schedule(s):
    d1 = [
        ("9:00 – 9:45", "Welcome, admin, course map"),
        ("9:45 – 10:40", "Module 1: BPA, Power Platform, flows, triggers, actions"),
        ("10:55 – 12:15", "Lab 0 · Lab 1 — environment, trigger and actions"),
        ("12:15 – 12:45", "Module 1: dynamic content, run history, commit order"),
        ("1:45 – 3:15", "Lab 2 · Module 2 — Excel logging, conditions, human in the loop"),
        ("3:30 – 6:00", "Lab 3 · Module 3 · Lab 4 — approval, agent anatomy, four agents"),
    ]
    d2 = [
        ("9:00 – 9:40", "Recap · Lab 5 — grounding and publishing to Teams"),
        ("9:40 – 11:10", "Module 4 · Lab 6 — HTTP, structured output, boundary of agency"),
        ("11:25 – 12:05", "Lab 7 — the agent alone in public"),
        ("1:05 – 2:05", "Lab 8 — the human review gate"),
        ("2:05 – 3:55", "Module 5 · Lab 9 · Lab 10 — RAG, built-in then Pinecone"),
        ("4:00 – 6:00", "Written Assessment (SAQ) 1 hr + Practical Performance 1 hr"),
    ]
    for col, (day, label, rows, color) in enumerate([
        ("D1", "Day 1 — Automate, then add the agent", d1, BLUE),
        ("D2", "Day 2 — Connect, supervise, ground", d2, VIOLET),
    ]):
        x = Inches(0.72 + col * 6.05)
        box(s, x, Inches(1.72), Inches(5.8), Inches(4.6), WHITE, color, line_w=1.8)
        head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.72), Inches(5.8), Inches(0.56))
        head.fill.solid()
        head.fill.fore_color.rgb = color
        head.line.fill.background()
        head.shadow.inherit = False
        text(s, x + Inches(0.22), Inches(1.72), Inches(5.4), Inches(0.56), label, 13, WHITE, True)
        for i, (slot, what) in enumerate(rows):
            y = Inches(2.42 + i * 0.63)
            text(s, x + Inches(0.24), y, Inches(1.45), Inches(0.58), slot, 9.5, color, True, anchor=MSO_ANCHOR.TOP)
            text(s, x + Inches(1.72), y, Inches(3.9), Inches(0.58), what, 10, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 6.05, "Each day runs 9:00am–6:00pm — 8 scheduled hours after a 1-hour lunch, with the two 15-minute tea breaks counted within.")


def draw_repository(s):
    items = [
        ("11 labs", "Lab 0 setup plus Labs 1–10, each with its own step-by-step guide.", BLUE),
        ("Ready assets", "Excel workbooks, brochure PDFs, HTML pages, JSON schemas and flow packages.", TEAL),
        ("Test data", "Sample question sets and probe cases written to make each agent fail.", AMBER),
        ("Work in order", "Open labs/README.md and follow the Next link at the foot of each lab.", GREEN),
    ]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(2.0 + row * 2.2), Inches(5.8), Inches(1.95), label, body, color, i + 1, 13)
    takeaway(s, 6.22, "Everything is in the course repository; the Learner Guide reproduces every lab in full.")


# ===========================================================================
# MODULE 1 — BPA, POWER AUTOMATE, TRIGGERS, ACTIONS
# ===========================================================================

def draw_what_is_bpa(s):
    text(s, Inches(0.72), Inches(1.75), Inches(11.85), Inches(0.5),
         "Business process automation is not “software that does work faster”. It is the removal of the "
         "hand-off\nwhere a person re-types what another system already knows.", 15, INK, anchor=MSO_ANCHOR.TOP)
    before = ["Form filled in", "Someone reads it", "Re-typed into Excel", "Someone remembers\nto reply"]
    after = ["Form submitted", "Flow triggered", "Row written", "Reply sent"]
    text(s, Inches(0.72), Inches(2.75), Inches(1.5), Inches(0.5), "MANUAL", 12, RED, True)
    flow(s, 2.72, before, ["", "", ""], [GREY, GREY, GREY, GREY], x0=2.3, total=10.25, height=0.95, size=12)
    text(s, Inches(0.72), Inches(4.1), Inches(1.5), Inches(0.5), "AUTOMATED", 12, GREEN, True)
    flow(s, 4.05, after, ["", "", ""], [BLUE, BLUE, TEAL, GREEN], x0=2.3, total=10.25, height=0.95, size=12)
    cards = [
        ("Consistency", "The same input produces the same output, every time, at 3am.", TEAL),
        ("Traceability", "Every run leaves a history someone can read a year later.", BLUE),
        ("Capacity", "People are moved to the judgement calls the machine cannot make.", VIOLET),
    ]
    for i, (label, body, color) in enumerate(cards):
        card(s, Inches(0.72 + i * 3.99), Inches(5.25), Inches(3.71), Inches(1.5), label, body, color, body_size=11)


def draw_power_platform(s):
    parts = [
        ("Power Automate", "Workflows. Triggers and actions that run without a person.", BLUE, "Labs 1–3"),
        ("Copilot Studio", "Conversational agents with instructions, knowledge and tools.", VIOLET, "Labs 4–10"),
        ("Dataverse", "The managed data store behind the environment.", TEAL, "Lab 0"),
        ("Connectors", "Outlook, Excel, SharePoint, Teams, Forms, HTTP — 1,000+.", GREEN, "Every lab"),
    ]
    for i, (label, body, color, where) in enumerate(parts):
        x = Inches(0.72 + i * 3.0)
        card(s, x, Inches(1.85), Inches(2.72), Inches(2.5), label, body, color, i + 1, 11, 14)
        chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.28), Inches(3.86), Inches(1.5), Inches(0.34))
        chip.fill.solid()
        chip.fill.fore_color.rgb = color
        chip.line.fill.background()
        chip.shadow.inherit = False
        text(s, x + Inches(0.28), Inches(3.86), Inches(1.5), Inches(0.34), where, 10, WHITE, True, PP_ALIGN.CENTER)
    box(s, Inches(0.72), Inches(4.62), Inches(11.85), Inches(1.5), LIGHT, LINE)
    text(s, Inches(1.0), Inches(4.75), Inches(11.3), Inches(0.36), "THE ENVIRONMENT IS THE CONTAINER", 12, BLUE, True)
    text(s, Inches(1.0), Inches(5.12), Inches(11.3), Inches(0.9),
         "Flows, agents and data all live inside one environment. Power Automate and Copilot Studio must be pointed at the\n"
         "same one, or your agent cannot see your flow. This is the single most common \"where did it go?\" in the course.",
         12, GREY, anchor=MSO_ANCHOR.TOP)
    lab_banner(s, 6.1, "lab_0")


def draw_flow_anatomy(s):
    flow(s, 2.0, ["TRIGGER\nwhat starts it", "ACTION\ndo the work", "ACTION\ndo more work", "OUTPUT\nnotify or return"],
         ["outputs", "outputs", "outputs"], [BLUE, TEAL, TEAL, AMBER], height=1.4, size=14)
    text(s, Inches(0.72), Inches(3.7), Inches(11.85), Inches(0.4),
         "Every flow, in every lab, is this shape. Only the trigger and the actions change.", 15, INK, True, PP_ALIGN.CENTER)
    rules = [
        ("One trigger", "A flow has exactly one trigger. Change the trigger and you have a different flow — the actions may not change at all.", BLUE),
        ("Actions are ordered", "Each action runs after the one above it, and can read the outputs of every step before it.", TEAL),
        ("Dynamic content", "Those earlier outputs are inserted as tokens, not typed. A typed value is a constant that will be wrong tomorrow.", VIOLET),
    ]
    for i, (label, body, color) in enumerate(rules):
        card(s, Inches(0.72 + i * 3.99), Inches(4.25), Inches(3.71), Inches(1.85), label, body, color, i + 1, 11)
    takeaway(s, 6.3, "Trigger, actions, outputs. Learn this once in Lab 1 and every later lab is a variation.")


def draw_trigger_types(s):
    text(s, Inches(0.72), Inches(1.7), Inches(11.85), Inches(0.4),
         "Four trigger families. The one you choose is a statement about who or what is allowed to start the process.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    trig = [
        ("Manual", "A person presses Run", "Instant cloud flow · button in\nthe mobile app or Teams", BLUE),
        ("Scheduled", "A clock reaches a time", "Recurrence — set the time zone\nor it runs on UTC", TEAL),
        ("Automated", "An event happens\nin a system", "New form response · new email ·\nnew SharePoint item · new file", VIOLET),
        ("Request", "Something calls in\nfrom outside", "HTTP request received ·\nWhen an agent calls the workflow", GREEN),
    ]
    for i, (label, when, examples, color) in enumerate(trig):
        x = Inches(0.72 + i * 3.0)
        box(s, x, Inches(2.25), Inches(2.72), Inches(3.0), WHITE, color, line_w=1.8)
        head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(2.25), Inches(2.72), Inches(0.52))
        head.fill.solid()
        head.fill.fore_color.rgb = color
        head.line.fill.background()
        head.shadow.inherit = False
        text(s, x, Inches(2.25), Inches(2.72), Inches(0.52), label, 15, WHITE, True, PP_ALIGN.CENTER)
        text(s, x + Inches(0.18), Inches(2.9), Inches(2.36), Inches(0.7), when, 13, INK, True, PP_ALIGN.CENTER)
        text(s, x + Inches(0.18), Inches(3.65), Inches(2.36), Inches(1.45), examples, 10, GREY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
    rows = [
        ("Automated — new form response", "Labs 1, 2, 3", "A business event starts the process"),
        ("Request — HTTP request received", "Labs 6, 7, 8, 10", "A website posts JSON and waits for JSON back"),
        ("Request — when an agent calls the workflow", "Labs 4, 6", "A conversation decides to call a tool"),
        ("Scheduled / Manual", "Reference", "A clock, or a person, starts it deliberately"),
    ]
    table(s, 5.05, ["Trigger used in this course", "Where", "What it means"], rows, [5.0, 2.2, 4.65], row_h=0.38, head_h=0.38, size=10)


def draw_action_families(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.36),
         "An action either moves data, decides something, waits for a person, or calls something outside the flow.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    fams = [
        ("Data actions", "Compose · Parse JSON · Initialize\nvariable · Select · Filter array", "Shape and normalise values before anything trusts them.", BLUE),
        ("Connector actions", "Send an email (Outlook) · Add a row\n(Excel) · Create item (SharePoint)", "Do the real work in a business system.", TEAL),
        ("Control actions", "Condition · Switch · Apply to each ·\nScope · Terminate", "Decide which path the run takes.", VIOLET),
        ("Human actions", "Start and wait for an approval ·\nHuman review (agent flows)", "Suspend the run until a person responds.", RED),
        ("Integration actions", "HTTP · Response · Invoke another flow ·\nRun a prompt (AI Builder)", "Reach outside the Power Platform, or answer the caller.", GREEN),
        ("Agent actions", "Agent node · Respond to the agent ·\nstructured output", "Let the model decide, inside a flow that does not.", AMBER),
    ]
    for i, (label, examples, why, color) in enumerate(fams):
        row, col = divmod(i, 3)
        x = Inches(0.72 + col * 3.99)
        y = Inches(2.15 + row * 2.12)
        box(s, x, y, Inches(3.71), Inches(1.95), LIGHT, LINE)
        stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.09), Inches(1.95))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = color
        stripe.line.fill.background()
        stripe.shadow.inherit = False
        text(s, x + Inches(0.26), y + Inches(0.1), Inches(3.3), Inches(0.36), label, 14, color, True)
        text(s, x + Inches(0.26), y + Inches(0.5), Inches(3.3), Inches(0.72), examples, 10, INK, anchor=MSO_ANCHOR.TOP)
        text(s, x + Inches(0.26), y + Inches(1.3), Inches(3.3), Inches(0.6), why, 10, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 6.28, "You will use every one of these families by the end of Lab 10.", AMBER)


def draw_dynamic_content(s):
    flow(s, 1.95, ["Trigger runs", "Outputs exist", "Later action\nreferences them", "Value arrives\nat run time"],
         ["produces", "picker", "resolved"], [BLUE, BLUE, TEAL, GREEN], height=1.15, size=13)
    box(s, Inches(0.72), Inches(3.4), Inches(5.8), Inches(2.15), WHITE, GREEN, line_w=1.8)
    text(s, Inches(0.98), Inches(3.52), Inches(5.3), Inches(0.36), "✓  INSERTED WITH THE PICKER", 12, GREEN, True)
    text(s, Inches(0.98), Inches(3.92), Inches(5.3), Inches(1.5),
         "The value renders as a coloured token. It resolves at run\ntime to whatever the earlier step actually produced.\n\n"
         "Every dynamic value in every lab is inserted this way.", 12, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(6.77), Inches(3.4), Inches(5.8), Inches(2.15), WHITE, RED, line_w=1.8)
    text(s, Inches(7.03), Inches(3.52), Inches(5.3), Inches(0.36), "✗  TYPED BY HAND", 12, RED, True)
    text(s, Inches(7.03), Inches(3.92), Inches(5.3), Inches(1.5),
         "It stays dead text. The flow runs green and the value\narrives empty — because a reference to nothing resolves\n"
         "to empty, not to an error.\n\nThis costs more class time than any other single mistake.", 12, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 5.32, "A green run is not a correct run. Open the run history and read what each step actually received.", RED)
    lab_banner(s, 6.08, "lab_1")


def draw_run_history(s):
    text(s, Inches(0.72), Inches(1.7), Inches(11.85), Inches(0.36),
         "The run history is the only honest account of what happened. Every lab in this course is verified from it.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    steps = [
        ("Open the run", "My flows → the flow → Run history, or the Activity tab in an agent flow.", BLUE),
        ("Read each step", "Expand a step to see its inputs and its outputs — what it was given, what it produced.", TEAL),
        ("Find the empty one", "A wrong answer usually traces to a step whose input was blank, not to a red error.", AMBER),
        ("Fix the reference", "Re-insert the token with the picker, republish, and run one test — one change per cycle.", GREEN),
    ]
    for i, (label, body, color) in enumerate(steps):
        card(s, Inches(0.72 + i * 3.0), Inches(2.3), Inches(2.72), Inches(2.3), label, body, color, i + 1, 11, 14)
    box(s, Inches(0.72), Inches(4.95), Inches(11.85), Inches(1.35), LIGHT, RED, line_w=1.6)
    text(s, Inches(1.0), Inches(5.08), Inches(11.3), Inches(0.36), "THE THREE STATES THAT LOOK ALIKE", 12, RED, True)
    text(s, Inches(1.0), Inches(5.46), Inches(11.3), Inches(0.8),
         "Succeeded with the right data  ·  Succeeded with empty data  ·  Still Running because it is waiting for a person.\n"
         "Only the first is done. The second is the dangerous one — it looks exactly like success.", 12, GREY, anchor=MSO_ANCHOR.TOP)
    lab_banner(s, 6.4, "lab_2")


def draw_commit_order(s):
    text(s, Inches(0.72), Inches(1.7), Inches(11.85), Inches(0.36),
         "The order of two actions is a business decision, not a technical one.", 15, INK, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(2.25), Inches(5.8), Inches(2.5), WHITE, GREEN, line_w=1.8)
    text(s, Inches(0.98), Inches(2.38), Inches(5.3), Inches(0.36), "LOG, THEN CONFIRM", 13, GREEN, True)
    flow_nodes = ["Write the row", "Send the email"]
    for i, n in enumerate(flow_nodes):
        bx = Inches(1.05 + i * 2.75)
        box(s, bx, Inches(2.85), Inches(2.4), Inches(0.75), LIGHT, GREEN)
        text(s, bx, Inches(2.85), Inches(2.4), Inches(0.75), n, 12, INK, True, PP_ALIGN.CENTER)
    arrow(s, Inches(3.52), Inches(3.05), Inches(0.3), Inches(0.34), GREEN)
    text(s, Inches(0.98), Inches(3.75), Inches(5.3), Inches(0.9),
         "If the email fails, the enquiry is still on the register and\nsomeone can chase it. You have a record of a missed reply.",
         11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(6.77), Inches(2.25), Inches(5.8), Inches(2.5), WHITE, RED, line_w=1.8)
    text(s, Inches(7.03), Inches(2.38), Inches(5.3), Inches(0.36), "CONFIRM, THEN LOG", 13, RED, True)
    for i, n in enumerate(["Send the email", "Write the row"]):
        bx = Inches(7.1 + i * 2.75)
        box(s, bx, Inches(2.85), Inches(2.4), Inches(0.75), LIGHT, RED)
        text(s, bx, Inches(2.85), Inches(2.4), Inches(0.75), n, 12, INK, True, PP_ALIGN.CENTER)
    arrow(s, Inches(9.57), Inches(3.05), Inches(0.3), Inches(0.34), RED)
    text(s, Inches(7.03), Inches(3.75), Inches(5.3), Inches(0.9),
         "If the row fails, you have promised a customer a reply that\nnobody can see. The evidence of the promise is gone.",
         11, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 5.0, "Commit the record of the obligation before you create the obligation. This is Lab 2 in one sentence.")
    lab_banner(s, 5.78, "lab_2")


# ===========================================================================
# MODULE 2 — CONTROL FLOW AND HUMAN IN THE LOOP
# ===========================================================================

def draw_conditions(s):
    text(s, Inches(0.72), Inches(1.7), Inches(11.85), Inches(0.36),
         "A condition splits one run into two paths. Both paths must be built — including the one you hope never runs.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(4.9), Inches(2.25), Inches(3.5), Inches(0.85), LIGHT, VIOLET, line_w=1.8)
    text(s, Inches(4.9), Inches(2.25), Inches(3.5), Inches(0.85), "Condition\nis the value X?", 13, INK, True, PP_ALIGN.CENTER)
    arrow(s, Inches(3.4), Inches(3.35), Inches(0.34), Inches(0.4), GREEN, "down")
    arrow(s, Inches(9.55), Inches(3.35), Inches(0.34), Inches(0.4), RED, "down")
    box(s, Inches(1.4), Inches(3.78), Inches(4.5), Inches(1.05), WHITE, GREEN, line_w=1.8)
    text(s, Inches(1.65), Inches(3.84), Inches(4.0), Inches(0.3), "IF YES", 11, GREEN, True)
    text(s, Inches(1.65), Inches(4.14), Inches(4.0), Inches(0.62), "The approved path. Continue the business process.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(7.4), Inches(3.78), Inches(4.5), Inches(1.05), WHITE, RED, line_w=1.8)
    text(s, Inches(7.65), Inches(3.84), Inches(4.0), Inches(0.3), "IF NO", 11, RED, True)
    text(s, Inches(7.65), Inches(4.14), Inches(4.0), Inches(0.62), "The rejected path. Notify, record and stop — never fall silent.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    rows = [
        ("Condition", "One test, two branches", "Approved or rejected"),
        ("Switch", "One value, many branches", "Leave type: Annual / Medical / Unpaid"),
        ("Apply to each", "Repeat actions over a list", "Every row returned by a lookup"),
        ("Terminate", "End the run deliberately", "Stop with a status a reader can interpret"),
    ]
    table(s, 4.98, ["Control action", "What it does", "Example in this course"], rows, [2.6, 3.6, 5.65], row_h=0.38, head_h=0.38, size=10)


def draw_hitl_concept(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.36),
         "Three arrangements that people use interchangeably, and that are not the same thing.", 14, INK, anchor=MSO_ANCHOR.TOP)
    rows = [
        ("Human IN the loop", "AI proposes, human decides", "Human authorises, system acts", "NO — it blocks", RED),
        ("Human ON the loop", "AI decides and acts", "Human monitors, can intervene", "Yes — after the fact", AMBER),
        ("Human OUT of the loop", "AI decides and acts", "AI acts", "Yes — nobody checks", GREY),
    ]
    headers = ["Pattern", "Who decides", "Who acts", "Can AI proceed alone?"]
    widths = [3.1, 2.9, 3.15, 2.7]
    hx = 0.72
    head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(2.2), Inches(11.85), Inches(0.5))
    head.fill.solid()
    head.fill.fore_color.rgb = BLUE
    head.line.fill.background()
    head.shadow.inherit = False
    for w, h in zip(widths, headers):
        text(s, Inches(hx + 0.16), Inches(2.2), Inches(w - 0.24), Inches(0.5), h, 12, WHITE, True)
        hx += w
    for r, (pattern, decides, acts, alone, color) in enumerate(rows):
        y = Inches(2.7 + r * 0.72)
        band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), y, Inches(11.85), Inches(0.72))
        band.fill.solid()
        band.fill.fore_color.rgb = WHITE if r % 2 == 0 else LIGHT
        band.line.color.rgb = LINE
        band.line.width = Pt(0.75)
        band.shadow.inherit = False
        cx = 0.72
        for c, (w, cell) in enumerate(zip(widths, [pattern, decides, acts, alone])):
            text(s, Inches(cx + 0.16), y, Inches(w - 0.24), Inches(0.72), cell, 12,
                 color if c in (0, 3) else GREY, c in (0, 3))
            cx += w
    box(s, Inches(0.72), Inches(5.05), Inches(11.85), Inches(1.25), LIGHT, RED, line_w=1.6)
    text(s, Inches(1.0), Inches(5.16), Inches(11.3), Inches(0.34), "WHERE THIS COURSE PUTS THE HUMAN", 12, RED, True)
    text(s, Inches(1.0), Inches(5.52), Inches(11.3), Inches(0.72),
         "Lab 3 — a manager approves leave.   Lab 8 — a licensed adviser approves a draft before it is sent.\n"
         "Labs 6, 7, 9 and 10 are deliberately out of the loop, so you can see what that costs.", 12, GREY, anchor=MSO_ANCHOR.TOP)
    lab_banner(s, 6.4, "lab_3")


def draw_approval_mechanics(s):
    flow(s, 1.95, ["Request\nsubmitted", "Start and wait\nfor an approval", "The run\nSUSPENDS", "A person\nresponds", "Condition reads\nthe Outcome"],
         ["action", "pause", "decision", "resume"], [BLUE, RED, RED, VIOLET, TEAL], height=1.3, size=12)
    box(s, Inches(0.72), Inches(3.6), Inches(5.8), Inches(1.5), WHITE, GREEN, line_w=1.8)
    text(s, Inches(0.98), Inches(3.72), Inches(5.3), Inches(0.34), "OUTCOME = APPROVE", 12, GREEN, True)
    text(s, Inches(0.98), Inches(4.08), Inches(5.3), Inches(0.9),
         "Send the approval message, update the record and continue\nthe business process.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(6.77), Inches(3.6), Inches(5.8), Inches(1.5), WHITE, RED, line_w=1.8)
    text(s, Inches(7.03), Inches(3.72), Inches(5.3), Inches(0.34), "OUTCOME = REJECT", 12, RED, True)
    text(s, Inches(7.03), Inches(4.08), Inches(5.3), Inches(0.9),
         "Send the rejection with the approver's comments, and route it\nto a named person — never to silence.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(5.22), Inches(11.85), Inches(0.82), LIGHT, AMBER, line_w=1.6)
    text(s, Inches(1.0), Inches(5.28), Inches(11.3), Inches(0.3), "SEND APPROVALS TO TEAMS, NOT OUTLOOK", 12, AMBER, True)
    text(s, Inches(1.0), Inches(5.58), Inches(11.3), Inches(0.42),
         "Verified on a live tenant: Outlook created the request and never delivered the mail — the run sat at Running, looking healthy.\n"
         "Every human gate in these labs uses the Microsoft Teams Approvals app.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    lab_banner(s, 6.15, "lab_3")


# ===========================================================================
# MODULE 3 — COPILOT STUDIO AGENTS
# ===========================================================================

def draw_workflow_vs_agent(s):
    box(s, Inches(0.72), Inches(1.85), Inches(5.8), Inches(3.9), WHITE, BLUE, line_w=1.8)
    head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(1.85), Inches(5.8), Inches(0.58))
    head.fill.solid(); head.fill.fore_color.rgb = BLUE; head.line.fill.background(); head.shadow.inherit = False
    text(s, Inches(0.72), Inches(1.85), Inches(5.8), Inches(0.58), "WORKFLOW  —  Power Automate", 15, WHITE, True, PP_ALIGN.CENTER)
    wf = [
        "You decide the path in advance",
        "The same input always gives the same output",
        "It can only do what you built",
        "It fails loudly, at a named step",
        "You test it by checking the result",
    ]
    for i, t in enumerate(wf):
        text(s, Inches(1.05), Inches(2.6 + i * 0.58), Inches(5.2), Inches(0.5), "•  " + t, 12, GREY)
    box(s, Inches(6.77), Inches(1.85), Inches(5.8), Inches(3.9), WHITE, VIOLET, line_w=1.8)
    head2 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.77), Inches(1.85), Inches(5.8), Inches(0.58))
    head2.fill.solid(); head2.fill.fore_color.rgb = VIOLET; head2.line.fill.background(); head2.shadow.inherit = False
    text(s, Inches(6.77), Inches(1.85), Inches(5.8), Inches(0.58), "AGENT  —  Copilot Studio", 15, WHITE, True, PP_ALIGN.CENTER)
    ag = [
        "It chooses the path at run time",
        "The same input may give a different answer",
        "It can combine what it was given in new ways",
        "It fails quietly, with a confident wrong answer",
        "You test it by trying to break it",
    ]
    for i, t in enumerate(ag):
        text(s, Inches(7.1), Inches(2.6 + i * 0.58), Inches(5.2), Inches(0.5), "•  " + t, 12, GREY)
    takeaway(s, 5.95, "Use a workflow where the rule is known. Use an agent where the language varies. Most real systems need both.", VIOLET)
    text(s, Inches(0.72), Inches(6.58), Inches(11.85), Inches(0.32),
         "Labs 1–3 are pure workflow. Labs 4–5 are pure agent. Labs 6–10 are both, and the seam between them is the lesson.",
         12, GREY, align=PP_ALIGN.CENTER)


def draw_agent_anatomy(s):
    core = box(s, Inches(4.75), Inches(3.15), Inches(3.8), Inches(1.3), LIGHT, VIOLET, line_w=2.2)
    text(s, Inches(4.75), Inches(3.15), Inches(3.8), Inches(1.3), "THE AGENT\nname · model · description", 15, VIOLET, True, PP_ALIGN.CENTER)
    parts = [
        ("INSTRUCTIONS", "Who it is and what it must\nnever do. Always in force.", 0.72, 1.78, BLUE),
        ("SKILLS", "Named procedures, applied\nwhen the topic matches.", 6.77, 1.78, TEAL),
        ("KNOWLEDGE", "Documents it may read.\nIt cannot read anything else.", 0.72, 4.6, AMBER),
        ("TOOLS", "Flows it can call to act\noutside the conversation.", 6.77, 4.6, GREEN),
    ]
    for label, body, x, y, color in parts:
        box(s, Inches(x), Inches(y), Inches(5.8), Inches(1.2), WHITE, color, line_w=1.8)
        text(s, Inches(x + 0.24), Inches(y + 0.08), Inches(5.3), Inches(0.34), label, 13, color, True)
        text(s, Inches(x + 0.24), Inches(y + 0.44), Inches(5.3), Inches(0.7), body, 11, GREY, anchor=MSO_ANCHOR.TOP)
    text(s, Inches(0.72), Inches(5.76), Inches(11.85), Inches(0.28),
         "A fifth part — CONNECTED AGENTS — lets one agent hand a conversation to another with its own knowledge and audience.",
         11, VIOLET, True, PP_ALIGN.CENTER)
    lab_banner(s, 6.08, "lab_4")


def draw_enforcement(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.36),
         "The spine of Lab 4: which of an agent's five parts can the model ignore?", 15, INK, anchor=MSO_ANCHOR.TOP)
    rows = [
        ("Instructions", "Who the agent is, always in force", "NO — probabilistic", RED),
        ("Skill", "A named procedure for a matching topic", "NO — the model decides it applies", RED),
        ("Knowledge", "Documents the agent may read", "PARTLY — it cannot read what it lacks", AMBER),
        ("Tool", "A flow that acts outside the conversation", "YES — the flow's own logic is enforced", GREEN),
        ("Connected agent", "A separate agent, its own knowledge", "YES — the knowledge boundary is real", GREEN),
    ]
    widths = [2.7, 5.0, 4.15]
    hx = 0.72
    head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(2.2), Inches(11.85), Inches(0.48))
    head.fill.solid(); head.fill.fore_color.rgb = VIOLET; head.line.fill.background(); head.shadow.inherit = False
    for w, h in zip(widths, ["Part", "What it is", "Enforced?"]):
        text(s, Inches(hx + 0.16), Inches(2.2), Inches(w - 0.24), Inches(0.48), h, 12, WHITE, True)
        hx += w
    for r, (part, what, enforced, color) in enumerate(rows):
        y = Inches(2.68 + r * 0.6)
        band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), y, Inches(11.85), Inches(0.6))
        band.fill.solid(); band.fill.fore_color.rgb = WHITE if r % 2 == 0 else LIGHT
        band.line.color.rgb = LINE; band.line.width = Pt(0.75); band.shadow.inherit = False
        cx = 0.72
        for c, (w, cell) in enumerate(zip(widths, [part, what, enforced])):
            text(s, Inches(cx + 0.16), y, Inches(w - 0.24), Inches(0.6), cell, 12,
                 INK if c == 0 else (color if c == 2 else GREY), c != 1)
            cx += w
    takeaway(s, 5.6, "A control the model cannot reach beats a rule you asked it to follow.", RED)
    box(s, Inches(0.72), Inches(6.28), Inches(11.85), Inches(0.6), LIGHT, GREEN, line_w=1.6)
    text(s, Inches(1.0), Inches(6.28), Inches(11.3), Inches(0.6),
         "So: a tool the agent does NOT have is a control. And the schema beats the prompt — a field that exists will eventually be filled.",
         12, INK, True)


def draw_instructions_craft(s):
    text(s, Inches(0.72), Inches(1.7), Inches(11.85), Inches(0.36),
         "Instructions are prose, but they are not free text. Four things every agent instruction in this course states.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    items = [
        ("Identity", "\"You are an HR policy information assistant.\"\nOne role, stated in one line.", BLUE),
        ("Source rule", "\"Answer using only the approved SharePoint HR policy source.\"\nWhere facts may come from.", TEAL),
        ("Refusals", "\"Do not expose, request or infer personal employee records.\"\nStated as prohibitions, not preferences.", RED),
        ("Escalation", "\"When the source is insufficient, say so and direct the user to HR.\"\nWhere the conversation ends when it cannot continue.", GREEN),
    ]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(2.25 + row * 1.85), Inches(5.8), Inches(1.6), label, body, color, i + 1, 11)
    box(s, Inches(0.72), Inches(5.92), Inches(11.85), Inches(0.95), LIGHT, RED, line_w=1.6)
    text(s, Inches(1.0), Inches(5.98), Inches(11.3), Inches(0.3), "NEVER PASTE @{...} INTO AN INSTRUCTIONS BOX", 12, RED, True)
    text(s, Inches(1.0), Inches(6.28), Inches(11.3), Inches(0.52),
         "It is a rich-text editor: it escapes underscores in node names, and a reference to a node that does not exist resolves to\n"
         "EMPTY rather than erroring. Build the prose with gaps and insert every value with the ⚡ picker.", 11, GREY, anchor=MSO_ANCHOR.TOP)


def draw_knowledge_concept(s):
    flow(s, 1.95, ["Documents in\nSharePoint", "Attached as a\nknowledge source", "Indexed by\nthe product", "Retrieved when\na question matches"],
         ["point at it", "wait for Ready", "at run time"], [BLUE, TEAL, VIOLET, GREEN], height=1.25, size=12)
    items = [
        ("It is a boundary", "The agent genuinely cannot read a document you did not give it. This is the one part of the agent that is close to enforced.", GREEN),
        ("Turn off general knowledge", "Otherwise the model answers from what it learned in training, and you cannot tell which answers those were.", RED),
        ("Remove \"Search all websites\"", "It is on by default. A fee from the open web is indistinguishable from a fee in your own brochure.", AMBER),
    ]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(3.52), Inches(3.71), Inches(1.72), label, body, color, i + 1, 10, 13)
    takeaway(s, 5.32, "Grounding is not only about giving the agent facts. It is about taking away every other source of them.")
    lab_banner(s, 6.08, "lab_5")


def draw_tools_concept(s):
    flow(s, 1.9, ["User asks\nfor something", "Agent decides\na tool applies", "Flow runs —\ndeterministic", "Result returns\nto the conversation"],
         ["intent", "typed inputs", "Respond to the agent"], [VIOLET, VIOLET, GREEN, TEAL], height=1.3, size=12)
    box(s, Inches(0.72), Inches(3.55), Inches(5.8), Inches(2.0), WHITE, VIOLET, line_w=1.8)
    text(s, Inches(0.98), Inches(3.66), Inches(5.3), Inches(0.34), "THE AGENT'S PART", 12, VIOLET, True)
    text(s, Inches(0.98), Inches(4.02), Inches(5.3), Inches(1.4),
         "Decides that a tool is relevant, and fills its inputs from\nwhat the person said.\n\n"
         "This part is probabilistic. It may call the wrong tool, or\ncall the right one with the wrong values.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(6.77), Inches(3.55), Inches(5.8), Inches(2.0), WHITE, GREEN, line_w=1.8)
    text(s, Inches(7.03), Inches(3.66), Inches(5.3), Inches(0.34), "THE FLOW'S PART", 12, GREEN, True)
    text(s, Inches(7.03), Inches(4.02), Inches(5.3), Inches(1.4),
         "Validates, looks up, applies the threshold, writes the audit\nrow, sends to the approver.\n\n"
         "This part is enforced. Whatever the agent believed, the\nflow's own logic still runs.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 5.32, "The tool description is how the agent knows when to call it — write it for the model, not for a developer.", VIOLET)
    lab_banner(s, 6.08, "lab_4")


def draw_multi_agent(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "One agent that knows everything has no boundaries. Splitting is how you give it some.", 14, INK, anchor=MSO_ANCHOR.TOP)
    parent = box(s, Inches(4.9), Inches(2.2), Inches(3.5), Inches(0.95), LIGHT, VIOLET, line_w=2.0)
    text(s, Inches(4.9), Inches(2.2), Inches(3.5), Inches(0.95), "HR AGENT\nthe parent", 14, VIOLET, True, PP_ALIGN.CENTER)
    children = [
        ("Policy &\nBenefits", BLUE), ("Leave", TEAL), ("Onboarding", GREEN), ("Payroll", AMBER),
    ]
    for i, (name, color) in enumerate(children):
        x = Inches(1.15 + i * 2.85)
        arrow(s, x + Inches(1.0), Inches(3.3), Inches(0.3), Inches(0.36), color, "down")
        box(s, x, Inches(3.8), Inches(2.3), Inches(1.05), WHITE, color, line_w=1.8)
        text(s, x, Inches(3.8), Inches(2.3), Inches(1.05), name, 12, INK, True, PP_ALIGN.CENTER)
    reasons = [
        ("Knowledge is separated", "Each child reads only its own documents. That boundary is real.", GREEN),
        ("Conversation is not", "What the employee said still flows across. Privacy is not automatic.", RED),
        ("A split is governance", "You are deciding who may know what — not tidying a big prompt.", VIOLET),
    ]
    for i, (label, body, color) in enumerate(reasons):
        card(s, Inches(0.72 + i * 3.99), Inches(5.02), Inches(3.71), Inches(1.05), label, body, color, body_size=10, label_size=13)
    lab_banner(s, 6.15, "lab_4")


def draw_publishing(s):
    flow(s, 2.0, ["Build and\nsave", "Test in\nPreview", "Publish", "Add a\nchannel", "Users reach it\nin Teams"],
         ["probe it", "version", "Teams / web", "verify"], [BLUE, AMBER, VIOLET, TEAL, GREEN], height=1.25, size=12)
    items = [
        ("Preview is not published", "Changes are invisible to Teams users until you publish again. A stale answer in Teams usually means an unpublished edit.", AMBER),
        ("One change per cycle", "Each publish-and-test cycle costs a publish plus about 25 seconds. Two simultaneous edits make a failure uninterpretable.", RED),
        ("Test as the user", "Open it from Teams with the account a real user would have — not from the maker's Preview pane.", GREEN),
    ]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(3.7), Inches(3.71), Inches(2.15), label, body, color, i + 1, 11, 14)
    lab_banner(s, 6.1, "lab_5")


# ===========================================================================
# MODULE 4 — AGENT FLOWS, HTTP, BOUNDARY OF AGENCY
# ===========================================================================

def draw_agent_flows(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.36),
         "An agent flow is a Power Automate flow that may contain an Agent node — the model, inside the workflow.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    flow(s, 2.2, ["HTTP trigger", "Compose\nnormalise", "SharePoint\nlookup", "AGENT\napply the rules", "Condition\non the decision", "Response"],
         ["JSON in", "clean", "facts", "structured", "act"], [GREEN, BLUE, TEAL, VIOLET, AMBER, GREEN], height=1.35, size=11)
    box(s, Inches(0.72), Inches(4.0), Inches(5.8), Inches(1.85), WHITE, VIOLET, line_w=1.8)
    text(s, Inches(0.98), Inches(4.12), Inches(5.3), Inches(0.34), "WHAT THE AGENT NODE IS FOR", 12, VIOLET, True)
    text(s, Inches(0.98), Inches(4.48), Inches(5.3), Inches(1.25),
         "Judgement over language: reading a free-text reason,\napplying ordered rules, classifying a tone, drafting a reply.\n"
         "Anything where the input varies more than a form allows.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(6.77), Inches(4.0), Inches(5.8), Inches(1.85), WHITE, RED, line_w=1.8)
    text(s, Inches(7.03), Inches(4.12), Inches(5.3), Inches(0.34), "THE COPILOT CREDITS TRAP", 12, RED, True)
    text(s, Inches(7.03), Inches(4.48), Inches(5.3), Inches(1.25),
         "Agent flows consume Copilot Credits on every run. Many\nDefault environments have none and fail with\n"
         "InsufficientMcsCredits. A licence does not fix it — licences\nare per-user, credits are per-environment.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 6.05, "This is why Lab 0 builds a Copilot Studio Training (Developer) environment rather than a Sandbox.", RED)


def draw_http_concept(s):
    flow(s, 2.05, ["Website form", "POST  JSON", "HTTP trigger\nreceives it", "Flow runs", "Response\nreturns JSON", "Page updates"],
         ["submit", "over HTTPS", "", "build reply", "render"], [BLUE, GREEN, GREEN, TEAL, AMBER, BLUE], height=1.3, size=11)
    rows = [
        ("Request", "What the caller sends", "A JSON body matching the schema you declared"),
        ("Schema", "The shape you promise to accept", "Generated from a sample payload — then frozen"),
        ("Response", "What the caller gets back", "A JSON body the page can read, plus a status code"),
        ("Synchronous", "The page waits", "If nothing responds, the browser sees a timeout, not a result"),
    ]
    table(s, 3.75, ["Part", "Meaning", "In these labs"], rows, [2.4, 3.6, 5.85], row_h=0.44, head_h=0.44, size=11)
    box(s, Inches(0.72), Inches(5.85), Inches(11.85), Inches(0.95), LIGHT, AMBER, line_w=1.6)
    text(s, Inches(1.0), Inches(5.93), Inches(11.3), Inches(0.32), "TWO FAILURES THAT LOOK THE SAME FROM THE BROWSER", 11, AMBER, True)
    text(s, Inches(1.0), Inches(6.25), Inches(11.3), Inches(0.5),
         "\"Failed to fetch\" WITH a successful run = CORS; serve the page from SharePoint, not localhost.   "
         "\"Failed to fetch\" with NO run at all = the flow is saved but not published, or the URL is wrong.", 11, GREY, anchor=MSO_ANCHOR.TOP)


def draw_structured_output(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "Structured output turns the model's answer from prose into named fields the rest of the flow can branch on.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(2.2), Inches(5.8), Inches(2.35), WHITE, RED, line_w=1.8)
    text(s, Inches(0.98), Inches(2.32), Inches(5.3), Inches(0.34), "PROSE — unusable downstream", 12, RED, True)
    text(s, Inches(0.98), Inches(2.7), Inches(5.3), Inches(1.7),
         "\"I think this application should probably be approved,\nalthough the address looks a little unusual and you\n"
         "may wish to check it.\"\n\nWhat does a Condition test against that?", 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(6.77), Inches(2.2), Inches(5.8), Inches(2.35), WHITE, GREEN, line_w=1.8)
    text(s, Inches(7.03), Inches(2.32), Inches(5.3), Inches(0.34), "STRUCTURED — branchable", 12, GREEN, True)
    text(s, Inches(7.03), Inches(2.7), Inches(5.3), Inches(1.7),
         "applicationId : APP-10432\ndecision      : REVIEW\nreason        : address unverified\nriskFlags     : [ADDRESS_MISMATCH]\n\n"
         "A Condition can read decision. A person can audit reason.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(4.7), Inches(11.85), Inches(1.5), LIGHT, VIOLET, line_w=1.8)
    text(s, Inches(1.0), Inches(4.78), Inches(11.3), Inches(0.32), "FOUR DECISIONS, NOT TWO", 12, VIOLET, True)
    text(s, Inches(1.0), Inches(5.12), Inches(11.3), Inches(0.95),
         "APPROVED  ·  REJECTED  ·  DUPLICATE  ·  REVIEW\n"
         "A politically exposed person is not a rejection — it is a case for a human. An agent given only two outcomes will force\n"
         "every ambiguous case into one of them, and you will never see the ones it got wrong.", 12, GREY, anchor=MSO_ANCHOR.TOP)
    lab_banner(s, 6.35, "lab_6")


def draw_boundary_of_agency(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "The most important design decision in the course: what the model is allowed to determine, and what it is not.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(2.2), Inches(5.8), Inches(2.6), WHITE, VIOLET, line_w=1.8)
    head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(2.2), Inches(5.8), Inches(0.52))
    head.fill.solid(); head.fill.fore_color.rgb = VIOLET; head.line.fill.background(); head.shadow.inherit = False
    text(s, Inches(0.72), Inches(2.2), Inches(5.8), Inches(0.52), "THE AI DECIDES  —  what to do", 13, WHITE, True, PP_ALIGN.CENTER)
    for i, t in enumerate(["Which of six ordered rules applies", "Whether the case needs a human",
                           "How to phrase the reason", "What risk flags to raise"]):
        text(s, Inches(1.05), Inches(2.92 + i * 0.44), Inches(5.2), Inches(0.4), "•  " + t, 11, GREY)
    box(s, Inches(6.77), Inches(2.2), Inches(5.8), Inches(2.6), WHITE, GREEN, line_w=1.8)
    head2 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.77), Inches(2.2), Inches(5.8), Inches(0.52))
    head2.fill.solid(); head2.fill.fore_color.rgb = GREEN; head2.line.fill.background(); head2.shadow.inherit = False
    text(s, Inches(6.77), Inches(2.2), Inches(5.8), Inches(0.52), "THE FLOW DOES  —  what must always happen", 13, WHITE, True, PP_ALIGN.CENTER)
    for i, t in enumerate(["Normalise the identifier (Compose)", "Check the register for a duplicate",
                           "Write the customer record", "Write the audit row, before the gate"]):
        text(s, Inches(7.1), Inches(2.92 + i * 0.44), Inches(5.2), Inches(0.4), "•  " + t, 11, GREY)
    box(s, Inches(0.72), Inches(5.0), Inches(11.85), Inches(1.3), LIGHT, RED, line_w=1.8)
    text(s, Inches(1.0), Inches(5.1), Inches(11.3), Inches(0.34), "THE RECORD IS WRITTEN FROM THE COMPOSE ACTION, NEVER FROM THE MODEL'S ANSWER", 12, RED, True)
    text(s, Inches(1.0), Inches(5.46), Inches(11.3), Inches(0.75),
         "So an invented identifier has no route into the customer master. The agent's opinion reaches the decision field; it never\n"
         "reaches the data. If you remember one sentence from Day 2, make it this one.", 12, GREY, anchor=MSO_ANCHOR.TOP)
    lab_banner(s, 6.4, "lab_6")


def draw_agent_alone(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "Lab 7 is the agent working in public with nobody reviewing it. Four nodes, and two non-negotiable rules.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    flow(s, 2.35, ["Chat widget", "HTTP trigger", "Compose\nsession", "AGENT\nrules + facts", "Response"],
         ["POST", "", "instruction · knowledge · history", "reply"], [BLUE, GREEN, TEAL, VIOLET, AMBER], height=1.25, size=12)
    box(s, Inches(0.72), Inches(3.95), Inches(5.8), Inches(1.28), WHITE, BLUE, line_w=1.8)
    text(s, Inches(0.98), Inches(4.02), Inches(5.3), Inches(0.3), "RULES LIVE IN THE INSTRUCTION", 11, BLUE, True)
    text(s, Inches(0.98), Inches(4.32), Inches(5.3), Inches(0.84),
         "Collect name, phone and email before answering. Never\nrecommend a product, predict a return or allocate savings.\nA refusal that must be retrieved can miss.",
         10, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(6.77), Inches(3.95), Inches(5.8), Inches(1.28), WHITE, AMBER, line_w=1.8)
    text(s, Inches(7.03), Inches(4.02), Inches(5.3), Inches(0.3), "FACTS LIVE IN THE KNOWLEDGE SOURCE", 11, AMBER, True)
    text(s, Inches(7.03), Inches(4.32), Inches(5.3), Inches(0.84),
         "Fees, timelines and services come from the FAQ PDF.\nChange the PDF and the answers change — without\ntouching the instruction.",
         10, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 5.32, "The test cases in Lab 7 are written to make it fail. Read the failures aloud — that is the debrief.", RED)
    lab_banner(s, 6.08, "lab_7")


def draw_human_review_node(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "Lab 8 adds the person back. The Human review node does nothing at all except wait.", 14, INK, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(2.2), Inches(6.05), Inches(1.5), LIGHT, VIOLET, line_w=1.8)
    text(s, Inches(0.72), Inches(2.28), Inches(6.05), Inches(0.32), "THE AGENT'S TERRITORY", 11, VIOLET, True, PP_ALIGN.CENTER)
    for i, t in enumerate(["classify", "read tone", "flag", "DRAFT"]):
        bx = Inches(0.95 + i * 1.42)
        box(s, bx, Inches(2.7), Inches(1.28), Inches(0.75), WHITE, VIOLET)
        text(s, bx, Inches(2.7), Inches(1.28), Inches(0.75), t, 11, INK, True, PP_ALIGN.CENTER)
    box(s, Inches(7.05), Inches(2.2), Inches(2.35), Inches(1.5), WHITE, RED, line_w=2.4)
    text(s, Inches(7.05), Inches(2.28), Inches(2.35), Inches(0.32), "THE GATE", 11, RED, True, PP_ALIGN.CENTER)
    text(s, Inches(7.05), Inches(2.62), Inches(2.35), Inches(0.95), "Human review\napprove / reject\nin Teams", 12, RED, True, PP_ALIGN.CENTER)
    box(s, Inches(9.68), Inches(2.2), Inches(2.89), Inches(1.5), LIGHT, GREEN, line_w=1.8)
    text(s, Inches(9.68), Inches(2.28), Inches(2.89), Inches(0.32), "THE CONSEQUENCE", 11, GREEN, True, PP_ALIGN.CENTER)
    text(s, Inches(9.68), Inches(2.62), Inches(2.89), Inches(0.95), "send · log ·\nhand to a named person", 11, GREY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(4.0), Inches(11.85), Inches(1.5), WHITE, RED, line_w=2.0)
    text(s, Inches(1.0), Inches(4.12), Inches(11.3), Inches(0.36), "THE TEST OF A REAL GATE", 13, RED, True)
    text(s, Inches(1.0), Inches(4.52), Inches(11.3), Inches(0.9),
         "Submit an enquiry, then open Activity. The run says Running — and it will still say Running tomorrow. Nothing times out,\n"
         "nothing defaults, nothing proceeds. A workflow that has done all of its work and will not take the last step.", 12, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 5.32, "That pause is the deliverable. Rejected drafts go to a NAMED person who must phone the client — never to silence.")
    lab_banner(s, 6.08, "lab_8")


# ===========================================================================
# MODULE 5 — RAG
# ===========================================================================

def draw_why_rag(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "You could paste all 20 brochures into the instruction. For 20 it works. Then the academy adds 40 more.",
         14, INK, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(2.2), Inches(5.8), Inches(2.05), WHITE, RED, line_w=1.8)
    text(s, Inches(0.98), Inches(2.32), Inches(5.3), Inches(0.34), "EVERYTHING IN THE PROMPT", 12, RED, True)
    text(s, Inches(0.98), Inches(2.7), Inches(5.3), Inches(1.4),
         "The instruction exceeds what the model can read.\nIt starts ignoring the middle.\n"
         "Every question costs the price of 60 brochures.\nA fee change means editing the prompt.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(6.77), Inches(2.2), Inches(5.8), Inches(2.05), WHITE, GREEN, line_w=1.8)
    text(s, Inches(7.03), Inches(2.32), Inches(5.3), Inches(0.34), "RETRIEVE, THEN GENERATE", 12, GREEN, True)
    text(s, Inches(7.03), Inches(2.7), Inches(5.3), Inches(1.4),
         "Find the two or three brochures that resemble the\nquestion, and give the model only those.\n"
         "The agent never sees the other 17.\nIt answers from what matters.", 11, GREY, anchor=MSO_ANCHOR.TOP)
    flow(s, 4.55, ["Question", "Embed the\nquestion", "Search for the\nnearest documents", "Paste them into\nthe prompt", "Grounded\nanswer"],
         ["vector", "similarity", "top_k", "generate"], [BLUE, TEAL, VIOLET, AMBER, GREEN], height=1.25, size=11)
    takeaway(s, 6.1, "RAG = retrieval + generation. The retrieval decides whether the generation can possibly be right.", AMBER)


def draw_rag_pipeline(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "Two phases. Ingestion happens once; retrieval happens on every question.", 14, INK, anchor=MSO_ANCHOR.TOP)
    text(s, Inches(0.72), Inches(2.15), Inches(2.0), Inches(0.34), "INGESTION — once", 12, BLUE, True)
    flow(s, 2.5, ["Documents", "Chunk", "Embed", "Store as vectors"], ["split", "model", "index"], [BLUE, BLUE, TEAL, TEAL], height=1.0, size=12)
    text(s, Inches(0.72), Inches(3.8), Inches(2.9), Inches(0.32), "RETRIEVAL — every question", 12, GREEN, True)
    flow(s, 4.32, ["Question", "Embed", "Nearest top_k", "Into the prompt", "Answer"], ["same model", "similarity", "context", ""], [GREEN, TEAL, VIOLET, AMBER, GREEN], height=1.0, size=12)
    terms = [
        ("Chunk", "How a document is split. Here: one brochure = one record.", BLUE),
        ("Embedding", "Text as a list of numbers. llama-text-embed-v2, 1024 dimensions.", TEAL),
        ("Similarity", "Nearness of two vectors — the machine's idea of \"related\".", VIOLET),
        ("top_k", "How many documents come back. Here: 3.", AMBER),
    ]
    for i, (label, body, color) in enumerate(terms):
        card(s, Inches(0.72 + i * 3.0), Inches(5.5), Inches(2.72), Inches(1.25), label, body, color, body_size=10, label_size=13)


def draw_rag_compare(s):
    rows = [
        ("Nodes", "3", "5"),
        ("Ingestion", "Upload to SharePoint", "A Python script, run once"),
        ("Embedding model", "Hidden", "llama-text-embed-v2, 1024"),
        ("Chunking", "Hidden", "One brochure = one record — your call"),
        ("top_k", "Hidden", "3 — your call"),
        ("Citation markers", "Leak into the reply", "None"),
        ("A changed fee", "Edit, wait for re-crawl", "Edit, then re-ingest"),
        ("When it answers badly", "Rewrite the prompt and hope", "Four levers to pull"),
    ]
    widths = [3.35, 4.25, 4.25]
    head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(1.8), Inches(11.85), Inches(0.5))
    head.fill.solid(); head.fill.fore_color.rgb = BLUE; head.line.fill.background(); head.shadow.inherit = False
    hx = 0.72
    for w, h, col in zip(widths, ["", "LAB 9 — built-in knowledge", "LAB 10 — Pinecone"], [WHITE, WHITE, WHITE]):
        text(s, Inches(hx + 0.16), Inches(1.8), Inches(w - 0.24), Inches(0.5), h, 12, col, True,
             PP_ALIGN.LEFT if not h else PP_ALIGN.CENTER)
        hx += w
    for r, row in enumerate(rows):
        y = Inches(2.3 + r * 0.5)
        band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), y, Inches(11.85), Inches(0.5))
        band.fill.solid(); band.fill.fore_color.rgb = WHITE if r % 2 == 0 else LIGHT
        band.line.color.rgb = LINE; band.line.width = Pt(0.75); band.shadow.inherit = False
        cx = 0.72
        for c, (w, cell) in enumerate(zip(widths, row)):
            text(s, Inches(cx + 0.16), y, Inches(w - 0.24), Inches(0.5), cell, 11,
                 INK if c == 0 else GREY, c == 0, PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER)
            cx += w
    takeaway(s, 6.22, "Neither is the right answer. Which is right depends on whether the person maintaining it will ever need those levers.", AMBER)


def draw_hallucination(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "A grounded agent still invents. You find out by asking for things that do not exist.", 14, INK, anchor=MSO_ANCHOR.TOP)
    probes = [
        ("A course you do not run", "\"Do you have a course on cake sculpture?\"", "It must say it does not — not improvise a syllabus.", RED),
        ("A fact in no brochure", "\"Is there parking at the east campus?\"", "It must say the brochures do not cover it.", AMBER),
        ("A discount that does not exist", "\"What is the student discount?\"", "It must not invent a percentage to be helpful.", VIOLET),
    ]
    for i, (label, probe, expect, color) in enumerate(probes):
        x = Inches(0.72 + i * 3.99)
        box(s, x, Inches(2.2), Inches(3.71), Inches(2.6), WHITE, color, line_w=1.8)
        text(s, x + Inches(0.24), Inches(2.32), Inches(3.25), Inches(0.5), label, 13, color, True)
        text(s, x + Inches(0.24), Inches(2.88), Inches(3.25), Inches(0.8), probe, 11, INK, anchor=MSO_ANCHOR.TOP)
        text(s, x + Inches(0.24), Inches(3.75), Inches(3.25), Inches(0.9), expect, 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(0.72), Inches(5.0), Inches(11.85), Inches(0.95), LIGHT, RED, line_w=1.8)
    text(s, Inches(1.0), Inches(5.06), Inches(11.3), Inches(0.3), "A CONFIDENT WRONG ANSWER RAISES NO ERROR", 12, RED, True)
    text(s, Inches(1.0), Inches(5.36), Inches(11.3), Inches(0.52),
         "The run is green. The reply is fluent. Nothing in the run history is red. In every lab here the wrong answer looks exactly\n"
         "like a right one — which is why the test tables include the probes they do.", 12, GREY, anchor=MSO_ANCHOR.TOP)
    lab_banner(s, 6.12, "lab_9")


# ===========================================================================
# SYNTHESIS
# ===========================================================================

def draw_choosing(s):
    text(s, Inches(0.72), Inches(1.68), Inches(11.85), Inches(0.34),
         "Back at work, this is the decision you will actually make.", 14, INK, anchor=MSO_ANCHOR.TOP)
    rows = [
        ("The rule is written down and never varies", "Workflow only", "Labs 1–3", GREEN),
        ("The rule varies, but the outcome is high-stakes", "Agent decides, flow enforces, human approves", "Labs 6, 8", RED),
        ("The input is language, the output is an answer", "Agent grounded in your documents", "Labs 7, 9, 10", VIOLET),
        ("Several audiences, different things they may know", "Connected agents, one per boundary", "Lab 4", TEAL),
        ("The answer must be traceable to a source", "RAG, and turn general knowledge off", "Labs 9, 10", AMBER),
    ]
    widths = [4.9, 4.2, 2.75]
    head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(2.15), Inches(11.85), Inches(0.5))
    head.fill.solid(); head.fill.fore_color.rgb = BLUE; head.line.fill.background(); head.shadow.inherit = False
    hx = 0.72
    for w, h in zip(widths, ["If the situation is…", "…build this", "Seen in"]):
        text(s, Inches(hx + 0.16), Inches(2.15), Inches(w - 0.24), Inches(0.5), h, 12, WHITE, True)
        hx += w
    for r, (situation, build, where, color) in enumerate(rows):
        y = Inches(2.65 + r * 0.66)
        band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), y, Inches(11.85), Inches(0.66))
        band.fill.solid(); band.fill.fore_color.rgb = WHITE if r % 2 == 0 else LIGHT
        band.line.color.rgb = LINE; band.line.width = Pt(0.75); band.shadow.inherit = False
        cx = 0.72
        for c, (w, cell) in enumerate(zip(widths, [situation, build, where])):
            text(s, Inches(cx + 0.16), y, Inches(w - 0.24), Inches(0.66), cell, 12,
                 GREY if c == 0 else (color if c == 1 else BLUE), c > 0)
            cx += w
    takeaway(s, 6.1, "Ask who pays for the mistake. That answer sizes the agent's authority and places the human.")


def draw_before_production(s):
    checks = [
        ("Environment", "Correct environment selected in BOTH products; Copilot Credits confirmed.", BLUE),
        ("Data path", "No model output writes to a system of record without a deterministic action in between.", RED),
        ("Refusals tested", "Every prohibition has a probe that tries to break it, and the probe is in the test set.", VIOLET),
        ("Human placed", "Consequential paths end at a named person, not at a queue nobody watches.", AMBER),
        ("Audit before the gate", "The audit row is written before the approval, so rejected cases still leave a trace.", GREEN),
        ("Sources closed", "General knowledge off, \"Search all websites\" removed, knowledge status Ready.", TEAL),
    ]
    for i, (label, body, color) in enumerate(checks):
        row, col = divmod(i, 3)
        card(s, Inches(0.72 + col * 3.99), Inches(1.85 + row * 2.05), Inches(3.71), Inches(1.88), label, body, color, i + 1, 11, 14)
    takeaway(s, 6.05, "A green run is not a correct run, and a fluent answer is not a true one. Verify both before anyone depends on it.", RED)


def draw_synthesis(s):
    ideas = [
        ("A control the model cannot reach beats a rule you asked it to follow.", RED),
        ("A reference to nothing resolves to empty, not to an error.", AMBER),
        ("Commit the record of the obligation before you create the obligation.", BLUE),
        ("The AI decides what to do; deterministic actions do what must always happen.", VIOLET),
        ("A pause that will still be paused tomorrow is a real gate.", GREEN),
        ("Retrieval decides whether generation can possibly be right.", TEAL),
    ]
    for i, (idea, color) in enumerate(ideas):
        y = Inches(1.9 + i * 0.82)
        box(s, Inches(0.72), y, Inches(11.85), Inches(0.68), LIGHT, LINE)
        chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.88), y + Inches(0.1), Inches(0.48), Inches(0.48))
        chip.fill.solid(); chip.fill.fore_color.rgb = color; chip.line.fill.background(); chip.shadow.inherit = False
        text(s, Inches(0.88), y + Inches(0.1), Inches(0.48), Inches(0.48), str(i + 1), 14, WHITE, True, PP_ALIGN.CENTER)
        text(s, Inches(1.55), y, Inches(10.85), Inches(0.68), idea, 14, INK, True)
    text(s, Inches(0.72), Inches(6.6), Inches(11.85), Inches(0.3),
         "Six sentences. If you keep only these, you can rebuild the judgement behind every lab in this course.",
         12, GREY, align=PP_ALIGN.CENTER)


# ===========================================================================
# SEQUENCE
# ===========================================================================

slide("What You'll Learn", "course outcomes", draw_outcomes)
slide("Eleven Connected Labs", "the journey", draw_lab_journey)
slide("How This Course Works", "learning approach", draw_approach)
slide("Lesson Plan — 2 Days, 9:00am–6:00pm", "schedule", draw_schedule)
slide("Access the Hands-On Labs", "course repository", draw_repository)

slide("", "", divider("Module 1", "Business Process Automation and Power Automate",
      "What automation actually removes  ·  the Power Platform  ·  flows, triggers and actions  ·  dynamic content and run history\n"
      "Applied in Lab 0, Lab 1 and Lab 2", BLUE))
slide("What Business Process Automation Removes", "module 1 · concept", draw_what_is_bpa)
slide("The Power Platform, and the Environment That Holds It", "module 1 · concept", draw_power_platform)
slide("Every Flow Is the Same Four Parts", "module 1 · concept", draw_flow_anatomy)
slide("Triggers — What Is Allowed to Start a Process", "module 1 · concept", draw_trigger_types)
slide("Actions — The Six Families You Will Use", "module 1 · concept", draw_action_families)
slide("Dynamic Content — The Token, Not the Text", "module 1 · concept", draw_dynamic_content)
slide("Run History — The Only Honest Account", "module 1 · concept", draw_run_history)
slide("Order Matters — Commit Before You Confirm", "module 1 · concept", draw_commit_order)
slide("Lab 0 — The Shared Course Environment", "module 1 · lab workflow", workflow_slide("lab_0"))
slide("Lab 1 — Form to Email Confirmation", "module 1 · lab workflow", workflow_slide("lab_1"))
slide("Lab 2 — Log the Enquiry, Then Send", "module 1 · lab workflow", workflow_slide("lab_2"))

slide("", "", divider("Module 2", "Control Flow and Human in the Loop",
      "Conditions and branching  ·  approvals  ·  in / on / out of the loop  ·  where the human belongs\n"
      "Applied in Lab 3", TEAL))
slide("Conditions — Both Paths Must Exist", "module 2 · concept", draw_conditions)
slide("Human In, On, and Out of the Loop", "module 2 · concept", draw_hitl_concept)
slide("How an Approval Suspends a Running Flow", "module 2 · concept", draw_approval_mechanics)
slide("Lab 3 — Leave Application Approval", "module 2 · lab workflow", workflow_slide("lab_3"))

slide("", "", divider("Module 3", "Copilot Studio Agents",
      "Workflow versus agent  ·  instructions, skills, knowledge, tools  ·  what is actually enforced  ·  connected agents  ·  publishing\n"
      "Applied in Lab 4 and Lab 5", VIOLET))
slide("Workflow or Agent — They Fail Differently", "module 3 · concept", draw_workflow_vs_agent)
slide("The Anatomy of an Agent", "module 3 · concept", draw_agent_anatomy)
slide("Which Parts of an Agent Hold — and Which Do Not", "module 3 · concept", draw_enforcement)
slide("Writing Instructions That Constrain", "module 3 · concept", draw_instructions_craft)
slide("Knowledge — Giving Facts and Removing Sources", "module 3 · concept", draw_knowledge_concept)
slide("Tools — Where the Agent Stops and the Flow Starts", "module 3 · concept", draw_tools_concept)
slide("Multiple Agents — A Split Is a Governance Decision", "module 3 · concept", draw_multi_agent)
slide("Publishing to Teams", "module 3 · concept", draw_publishing)
slide("Lab 4 — Four Agents, One Spine", "module 3 · lab workflow", workflow_slide("lab_4"))
slide("Lab 5 — Grounding and Publishing an Agent", "module 3 · lab workflow", workflow_slide("lab_5"))

slide("", "", divider("Module 4", "Agent Flows, HTTP and the Boundary of Agency",
      "The Agent node inside a flow  ·  HTTP request and response  ·  JSON schema and structured output  ·  the human review gate\n"
      "Applied in Lab 6, Lab 7 and Lab 8", GREEN))
slide("Agent Flows — The Model Inside the Workflow", "module 4 · concept", draw_agent_flows)
slide("HTTP — A Website Calls Your Flow and Waits", "module 4 · concept", draw_http_concept)
slide("Structured Output — Fields, Not Prose", "module 4 · concept", draw_structured_output)
slide("The Boundary of Agency", "module 4 · concept", draw_boundary_of_agency)
slide("The Agent Alone, in Public", "module 4 · concept", draw_agent_alone)
slide("The Human Review Node — A Gate That Blocks", "module 4 · concept", draw_human_review_node)
slide("Lab 6 — Application Approval Agent", "module 4 · lab workflow", workflow_slide("lab_6"))
slide("Lab 7 — The Chatbot, Working Alone", "module 4 · lab workflow", workflow_slide("lab_7"))
slide("Lab 8 — The Human Review Gate", "module 4 · lab workflow", workflow_slide("lab_8"))

slide("", "", divider("Module 5", "Retrieval Augmented Generation",
      "Why not just paste everything  ·  ingestion and retrieval  ·  chunking, embeddings, top_k  ·  built-in versus external  ·  probing for invention\n"
      "Applied in Lab 9 and Lab 10", AMBER))
slide("Why Retrieval, Rather Than a Bigger Prompt", "module 5 · concept", draw_why_rag)
slide("The RAG Pipeline, and the Four Words That Matter", "module 5 · concept", draw_rag_pipeline)
slide("Built-in Knowledge or Your Own Vector Store", "module 5 · concept", draw_rag_compare)
slide("Probing for Invention", "module 5 · concept", draw_hallucination)
slide("Lab 9 — RAG with Built-in Knowledge", "module 5 · lab workflow", workflow_slide("lab_9"))
slide("Lab 10 — RAG with Pinecone", "module 5 · lab workflow", workflow_slide("lab_10"))

slide("", "", divider("Synthesis", "Taking This Back to Work",
      "Choosing the pattern  ·  the pre-production checklist  ·  the six sentences worth keeping", VIOLET))
slide("Choosing the Right Pattern", "synthesis", draw_choosing)
slide("Before Anything Reaches Production", "synthesis", draw_before_production)
slide("Six Sentences Worth Keeping", "synthesis", draw_synthesis)


# ===========================================================================
# ASSEMBLE
# ===========================================================================

HEAD_KEEP = 6          # slides 1-6 : cover, attendance, trainers, ice-breaker, ground rules
TAIL_KEEP = 8          # assessment briefing + closing block

tail_source = [11, 12, 13, 109, 110, 111, 112, 113]

need = HEAD_KEEP + len(SLIDES) + len(tail_source)
while len(prs.slides) < need:
    prs.slides.add_slide(prs.slide_layouts[6])

# Move the inherited tail slides to the end, in order, then rebuild the middle.
id_list = prs.slides._sldIdLst
elements = list(id_list)
tail_elements = [elements[i - 1] for i in tail_source]
for el in tail_elements:
    id_list.remove(el)
    id_list.append(el)

# Any surplus blank slides sit just before the tail; drop them.
while len(prs.slides) > need:
    surplus = list(id_list)[need - len(tail_source) - 1]
    id_list.remove(surplus)

for i, (heading, kicker, draw) in enumerate(SLIDES):
    no = HEAD_KEEP + 1 + i
    s = prs.slides[no - 1]
    clear(s)
    if heading:
        title(s, heading, kicker)
    draw(s)
    footer(s, no)

# Renumber the inherited tail slides' page numbers.
for i in range(len(tail_source)):
    no = HEAD_KEEP + len(SLIDES) + 1 + i
    s = prs.slides[no - 1]
    for shape in s.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text.strip()
            # Only the page-number textbox is renumbered. Step chips inside a
            # chevron/flow diagram are also digit-only, so identify the page
            # number by its position in the footer band on the right.
            is_page_no = (
                txt.isdigit()
                and shape.top is not None
                and shape.top > Inches(6.6)
                and (shape.left or 0) > Inches(9.0)
            )
            if is_page_no:
                for p in shape.text_frame.paragraphs:
                    for r in p.runs:
                        if r.text.strip().isdigit():
                            r.text = str(no)
            elif txt.startswith("Business Process Automation with Power Automate and Copilot") and "|" in txt:
                for p in shape.text_frame.paragraphs:
                    for r in p.runs:
                        if "|" in r.text:
                            r.text = f"Business Process Automation with Power Automate and Copilot Studio Agents   |   {no}"

# Cover slide — bump the version.
cover = prs.slides[0]
for shape in cover.shapes:
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                if "Version 6.0" in r.text:
                    r.text = r.text.replace("Version 6.0 (25 Jul 2026)", "Version 7.0 (2 Aug 2026)")
                if "Modules 1–4" in r.text:
                    r.text = r.text.replace("Modules 1–4", "Modules 1–5")

# The inherited assessment slides also cite "Modules 1–4"; this course has five.
for s in prs.slides:
    for shape in s.shapes:
        if not shape.has_text_frame:
            continue
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                if "Modules 1–4" in r.text:
                    r.text = r.text.replace("Modules 1–4", "Modules 1–5")

prs.save(DECK)
print(f"Saved {DECK.name} with {len(prs.slides)} slides")
for i, s in enumerate(prs.slides, 1):
    head = ""
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            head = sh.text_frame.text.strip().split("\n")[0][:64]
            break
    print(f"{i:3d}  {head}")
