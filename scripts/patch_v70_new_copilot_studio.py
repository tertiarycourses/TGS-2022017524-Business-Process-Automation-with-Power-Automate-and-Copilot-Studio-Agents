#!/usr/bin/env python3
"""Fold the pasted reference slides (2-16) into real course content.

The Version 7.0 deck received fifteen screenshot slides taken from the
Microsoft "Copilot Studio - Technical Deep Dive" material (the new Copilot
Studio: model + harness, the GitHub Copilot harness, skills, the new agent
and workflow designers, consumption licensing).  This patch:

  1. adds seven new house-style slides carrying that content into the
     modules where it belongs (Module 3 agents, Module 4 workflows), plus a
     training-accounts slide in the course-overview block;
  2. deletes the fifteen pasted reference slides;
  3. renumbers every footer page number.

Content sources: courseware/reference/Copilot Studio - Technical Deep Dive
v1.1.PPTX, the Copilot Credits Guide (August 2026), and the reference
screenshots themselves (two of which are cropped and reused as real UI
figures).
"""

from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CW = ROOT / "courseware"
DECK_IN = CW / "Business Process Automation with Power Automate and Copilot Studio Agents-v7.0.pptx"
DECK = CW / "Business Process Automation with Power Automate and Copilot Studio Agents-v7.1.pptx"
ASSETS = Path(sys.argv[1]) if len(sys.argv) > 1 else CW / "reference"

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

FOOTER_TEXT = (
    "Business Process Automation with Power Automate & Copilot Studio Agents  ·  "
    "TGS-2022017524  ·  © 2026 Tertiary Infotech Academy Pte Ltd"
)

BOTTOM_LIMIT = 6.88

prs = Presentation(DECK_IN)
SW, SH = prs.slide_width, prs.slide_height

# ---------------------------------------------------------------- primitives


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


def arrow(slide, x, y, w, h, color=BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def table(slide, y, headers, rows, widths, colors=None, x0=0.72, row_h=0.52,
          head_h=0.46, size=12, head_size=12):
    colors = colors or [INK] * len(rows)
    overflow = (y + head_h + len(rows) * row_h) - BOTTOM_LIMIT
    if overflow > 0:
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
    box(slide, Inches(0.72), Inches(y), Inches(11.85), Inches(0.62), LIGHT, color, line_w=1.6)
    text(slide, Inches(1.0), Inches(y), Inches(11.3), Inches(0.62), message, 14, INK, True)


def picture(slide, path, x, y, max_w, max_h, border=True):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(max_w / iw, max_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    pic = slide.shapes.add_picture(str(path), x, y, w, h)
    if border:
        pic.line.color.rgb = LINE
        pic.line.width = Pt(1.2)
    return pic


# ------------------------------------------------------------------ builders


def mini_card(slide, x, y, w, h, label, body, accent):
    """A compact feature card: label row + up to two body lines."""
    box(slide, x, y, w, h, LIGHT, LINE)
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.09), h)
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()
    stripe.shadow.inherit = False
    text(slide, x + Inches(0.24), y + Inches(0.06), w - Inches(0.44), Inches(0.3), label, 13, accent, True)
    text(slide, x + Inches(0.24), y + Inches(0.38), w - Inches(0.44), h - Inches(0.46), body, 9.5, GREY,
         anchor=MSO_ANCHOR.TOP, space=2)


def draw_training_accounts(s):
    text(s, Inches(0.72), Inches(1.62), Inches(11.85), Inches(0.34),
         "One assigned Microsoft 365 training account per learner — the same login for every lab.",
         13, GREY, anchor=MSO_ANCHOR.TOP)
    accounts = [(f"training{n}@tertiaryinfotech.onmicrosoft.com",
                 "Reserved for the trainer" if n == 1 else f"Learner account {n - 1}")
                for n in range(1, 11)]
    for i, (email, who) in enumerate(accounts):
        row, col = divmod(i, 2)
        x = Inches(0.72 + col * 6.05)
        y = Inches(2.12 + row * 0.66)
        accent = VIOLET if i == 0 else BLUE
        box(s, x, y, Inches(5.8), Inches(0.54), LIGHT if i == 0 else WHITE, accent if i == 0 else LINE,
            line_w=1.6 if i == 0 else 1.2)
        text(s, x + Inches(0.16), y + Inches(0.02), Inches(3.9), Inches(0.5), email, 12, INK, True)
        text(s, x + Inches(4.0), y + Inches(0.02), Inches(1.75), Inches(0.5), who, 10, VIOLET if i == 0 else GREY,
             False, PP_ALIGN.RIGHT)
    takeaway(s, 5.62, "Passwords are issued by your trainer in class.", VIOLET)
    text(s, Inches(0.72), Inches(6.34), Inches(11.85), Inches(0.3),
         "Sign in at copilotstudio.microsoft.com and make.powerautomate.com with the account the trainer "
         "assigns you — stay in the shared training environment and do not change the password.", 11, GREY)


def draw_model_and_harness(s):
    text(s, Inches(0.72), Inches(1.6), Inches(11.85), Inches(0.32),
         "Copilot Studio now separates the part that reasons from the part that governs. Two ideas name that split.",
         13, GREY, anchor=MSO_ANCHOR.TOP)
    card(s, Inches(0.72), Inches(2.06), Inches(5.8), Inches(1.72), "The AI model — the brain",
         "The reasoning engine. It understands language, spots patterns, generates content and decides "
         "what to do next. You choose it per agent — GPT-5.x or Claude — from the Model dropdown.",
         VIOLET, 1, 12)
    card(s, Inches(6.77), Inches(2.06), Inches(5.8), Inches(1.72), "The harness — around it",
         "The orchestration layer the model works inside: context, tools, governance, workflows and "
         "security. The harness is model-agnostic — it turns reasoning into governed work.",
         BLUE, 2, 12)
    harnesses = [
        ("GitHub Copilot harness", "Reasoning-heavy agents and workflows. Takes a goal, breaks it into steps, "
         "uses skills and memory, edits files in a governed sandbox. Billed in Copilot Credits.", VIOLET),
        ("Standard harness", "Rule-based agents and structured, repeatable conversations. You author the "
         "topics and paths, so the behaviour is predictable for well-understood requests.", TEAL),
        ("Copilot chat harness", "Extends Microsoft 365 Copilot Chat with your enterprise knowledge, so "
         "employees get grounded answers inside the chat they already use.", AMBER),
    ]
    text(s, Inches(0.72), Inches(3.94), Inches(11.85), Inches(0.3),
         "ONE MODEL, THREE HARNESSES IT CAN WORK INSIDE", 11, GREY, True)
    for i, (label, body, color) in enumerate(harnesses):
        card(s, Inches(0.72 + i * 4.05), Inches(4.28), Inches(3.75), Inches(1.62), label, body, color,
             None, 10.5, 13)
    takeaway(s, 6.1, "Everything you build in Labs 4–10 is a model you chose, inside a harness you configure.")


def draw_choose_harness(s):
    table(s, 1.78,
          ["Consideration", "GitHub Copilot harness", "Standard harness", "Copilot chat harness"],
          [
              ["Best for", "Complex, multi-step business processes", "Rule-based agents, structured conversations",
               "Extending M365 Copilot Chat"],
              ["How it works", "Reasons through a goal, step by step", "Follows the topics and rules you define",
               "Connects enterprise knowledge to chat"],
              ["When a step fails", "Retries, or finds another path", "Follows only the paths you built",
               "Not a focus"],
              ["Works with files", "Creates and edits Word, Excel, PowerPoint, PDF", "Not a focus", "Not a focus"],
              ["Skills and memory", "Yes — core building blocks", "Not a focus", "Not a focus"],
              ["Billing", "Copilot Credits — you pay for usage when you build and when you publish",
               "Copilot Studio licensing", "Consumption, or M365 Copilot seats"],
          ],
          [2.0, 3.6, 3.25, 3.0], row_h=0.56)
    takeaway(s, 6.1, "Start with the simplest harness that meets the need — a retrieval agent that only answers "
                     "from documents does not need the reasoning loop.", TEAL)


def draw_modern_orchestration(s):
    text(s, Inches(0.72), Inches(1.6), Inches(11.85), Inches(0.32),
         "The standard harness builds a plan, then runs it. The GitHub Copilot harness keeps deciding from "
         "the latest state.", 13, GREY, anchor=MSO_ANCHOR.TOP)
    # left — plan then execute
    box(s, Inches(0.72), Inches(2.06), Inches(5.8), Inches(3.1), LIGHT, TEAL, line_w=1.6)
    text(s, Inches(0.94), Inches(2.18), Inches(5.4), Inches(0.32), "STANDARD — PLAN, THEN EXECUTE", 12, TEAL, True)
    steps = ["1. INTENT\nunderstand", "2. PLAN\nsynthesise steps", "3. EXECUTE\nrun the plan"]
    for i, label in enumerate(steps):
        x = Inches(0.98 + i * 1.86)
        box(s, x, Inches(2.62), Inches(1.62), Inches(0.84), WHITE, TEAL, line_w=1.4)
        text(s, x + Inches(0.04), Inches(2.66), Inches(1.54), Inches(0.76), label, 10.5, INK, True, PP_ALIGN.CENTER)
        if i < 2:
            arrow(s, x + Inches(1.65), Inches(2.9), Inches(0.2), Inches(0.28), TEAL)
    text(s, Inches(0.94), Inches(3.66), Inches(5.4), Inches(1.4),
         "An explicit plan object: collect inputs, execute actions, summarise. Less live replanning and "
         "easier to inspect — but a detour or a failed step ends the plan.", 11.5, GREY,
         anchor=MSO_ANCHOR.TOP, space=4)
    # right — the loop
    box(s, Inches(6.77), Inches(2.06), Inches(5.8), Inches(3.1), LIGHT, VIOLET, line_w=1.6)
    text(s, Inches(6.99), Inches(2.18), Inches(5.4), Inches(0.32), "GITHUB COPILOT — THOUGHT · ACTION · OBSERVATION",
         12, VIOLET, True)
    loop = [("THOUGHT", 7.05, 2.62), ("ACTION", 9.85, 2.62), ("OBSERVE", 9.85, 3.62), ("DECIDE", 7.05, 3.62)]
    for label, lx, ly in loop:
        box(s, Inches(lx), Inches(ly), Inches(1.55), Inches(0.62), WHITE, VIOLET, line_w=1.4)
        text(s, Inches(lx), Inches(ly), Inches(1.55), Inches(0.62), label, 11, INK, True, PP_ALIGN.CENTER)
    for kind, ax, ay, aw, ah in [
        (MSO_SHAPE.CHEVRON, 8.98, 2.79, 0.5, 0.28),       # thought -> action
        (MSO_SHAPE.DOWN_ARROW, 10.5, 3.28, 0.26, 0.3),    # action -> observe
        (MSO_SHAPE.LEFT_ARROW, 8.98, 3.79, 0.5, 0.26),    # observe -> decide
        (MSO_SHAPE.UP_ARROW, 7.7, 3.28, 0.26, 0.3),       # decide -> thought
    ]:
        sh = s.shapes.add_shape(kind, Inches(ax), Inches(ay), Inches(aw), Inches(ah))
        sh.fill.solid()
        sh.fill.fore_color.rgb = VIOLET
        sh.line.fill.background()
        sh.shadow.inherit = False
    text(s, Inches(8.62), Inches(2.92), Inches(1.2), Inches(0.9), "latest\nstate", 10, VIOLET, True, PP_ALIGN.CENTER)
    text(s, Inches(6.99), Inches(4.42), Inches(5.4), Inches(0.64),
         "Reason over the latest state, call a tool, read the result, choose the next step live. "
         "It retries or reroutes on failure, and picks the task back up after a detour.", 11.5, GREY,
         anchor=MSO_ANCHOR.TOP, space=4)
    text(s, Inches(0.72), Inches(5.32), Inches(11.85), Inches(0.6),
         "What the loop buys: fewer, smarter questions (it infers what it already knows) · handles detours "
         "without losing the task · chains and parallelises tools · recovers from errors instead of "
         "surfacing them.", 12, INK, anchor=MSO_ANCHOR.TOP, space=4)
    takeaway(s, 6.1, "The loop fits problem spaces you cannot map upfront. Where the path is known, that freedom "
                     "is cost, not value — keep it in a workflow.", VIOLET)


def draw_new_agent_designer(s):
    picture(s, ASSETS / "ui_agent_designer.png", Inches(2.16), Inches(1.72), Inches(9.0), Inches(3.15))
    feats = [
        ("One page", "Skills, Tools, Knowledge, Connected agents and Memory, all on one rail.", VIOLET),
        ("Four tabs", "Build · Preview · Evaluate · Monitor — author, probe, score, then watch it live.", BLUE),
        ("Model picker", "GPT-5.x or Claude, chosen per agent — the harness stays the same.", TEAL),
        ("Memory (preview)", "Per-user remembered context. A maker toggle — off means unused.", AMBER),
    ]
    for i, (label, body, color) in enumerate(feats):
        mini_card(s, Inches(0.72 + i * 3.03), Inches(5.02), Inches(2.85), Inches(0.94), label, body, color)
    takeaway(s, 6.1, "Everything Lab 4 builds — instructions, skills, knowledge, tools — has a single home in "
                     "this designer.", VIOLET)


def draw_skills_on_demand(s):
    # topics -> skills
    box(s, Inches(0.72), Inches(1.86), Inches(2.6), Inches(1.06), LIGHT, LINE)
    text(s, Inches(0.72), Inches(1.96), Inches(2.6), Inches(0.4), "TOPICS", 15, GREY, True, PP_ALIGN.CENTER)
    text(s, Inches(0.72), Inches(2.34), Inches(2.6), Inches(0.5), "authored conversational paths —\nthe legacy way to build chatbots", 9.5, GREY, False, PP_ALIGN.CENTER)
    arrow(s, Inches(3.48), Inches(2.2), Inches(0.5), Inches(0.4), VIOLET)
    box(s, Inches(4.14), Inches(1.86), Inches(2.6), Inches(1.06), VIOLET, VIOLET)
    text(s, Inches(4.14), Inches(1.96), Inches(2.6), Inches(0.4), "SKILLS", 15, WHITE, True, PP_ALIGN.CENTER)
    text(s, Inches(4.14), Inches(2.34), Inches(2.6), Inches(0.5), "reusable procedures, loaded\nwhen the scenario matches", 9.5, WHITE, False, PP_ALIGN.CENTER)
    text(s, Inches(7.1), Inches(1.86), Inches(5.45), Inches(1.1),
         "Topics were built for scripted chatbots — not for how these models think. A skill gives the agent "
         "a specific, repeatable task and the material to carry it out.", 12, GREY, anchor=MSO_ANCHOR.TOP, space=4)
    cards = [
        ("What a skill is", "Name + description are the routing metadata; the instructions are the core, with "
         "examples, resources and scripts alongside. Metadata sits in context — the full content loads only "
         "when the scenario fires.", VIOLET),
        ("Why it works", "The instruction page stays short and readable, and context loads on demand. A large "
         "always-on prompt makes the model weigh irrelevant guidance on every turn.", GREEN),
        ("What to avoid", "Vague descriptions (the skill mis-fires or never triggers) · mega-skills that do "
         "everything · fact dumps — a skill guides, it does not replace a knowledge source.", RED),
    ]
    for i, (label, body, color) in enumerate(cards):
        card(s, Inches(0.72 + i * 4.05), Inches(3.24), Inches(3.75), Inches(2.55), label, body, color,
             None, 11, 14)
    takeaway(s, 6.1, "A skill is still not enforced — the model decides that it applies. The enforcement table "
                     "you just saw is unchanged.", RED)


def draw_new_workflow_designer(s):
    picture(s, ASSETS / "ui_workflow_canvas.png", Inches(0.72), Inches(1.76), Inches(7.35), Inches(4.1))
    feats = [
        ("A visual canvas", "Deterministic steps drawn as nodes — AI only where a step needs judgement.", BLUE),
        ("Node-by-node testing", "Run test on one node, with values loaded from a previous run.", GREEN),
        ("Agents inside workflows", "Drop an inline agent into one step, or call a published agent as a tool.",
         VIOLET),
        ("MCP-enabled tools", "Connectors and MCP tools, inside the Microsoft security boundary.", AMBER),
    ]
    for i, (label, body, color) in enumerate(feats):
        mini_card(s, Inches(8.32), Inches(1.76 + i * 1.06), Inches(4.25), Inches(0.94), label, body, color)
    takeaway(s, 6.1, "Workflows keep the structure of agent flows and add the intelligence of agents — without "
                     "the unpredictability.", GREEN)


# ===========================================================================
# APPLY
# ===========================================================================

id_list = prs.slides._sldIdLst

# --- 1. delete the pasted reference slides (positions 2-16, 1-based) -------
for sld_id in list(id_list)[1:16]:
    prs.part.drop_rel(sld_id.rId)
    id_list.remove(sld_id)
print(f"After deleting reference slides: {len(prs.slides)} slides")
assert len(prs.slides) == 68

# --- 1b. make new-slide partnames collision-safe ---------------------------
# python-pptx names a new slide part "slide{len+1}.xml", which collides with a
# live part when existing partnames have gaps (PowerPoint numbered this file's
# parts 1-83 and we just deleted 2-16).  Allocate above the highest used
# number instead — a collision would silently overwrite a live slide on save.
import re as _re

from pptx.opc.packuri import PackURI
from pptx.parts.presentation import PresentationPart

_used_nums = set()
for _s in prs.slides:
    _m = _re.search(r"slide(\d+)\.xml$", str(_s.part.partname))
    if _m:
        _used_nums.add(int(_m.group(1)))


def _next_free_slide_partname(self):
    n = max(_used_nums) + 1
    _used_nums.add(n)
    return PackURI("/ppt/slides/slide%d.xml" % n)


PresentationPart._next_slide_partname = property(_next_free_slide_partname)

# --- 2. build the new slides (appended, then repositioned) -----------------
NEW = [
    ("Your Training Account", "course environment", draw_training_accounts, "after", "Access the Hands-On Labs"),
    ("The New Copilot Studio — a Model Inside a Harness", "module 3 · concept", draw_model_and_harness,
     "after", "Workflow or Agent — They Fail Differently"),
    ("Choosing a Harness", "module 3 · concept", draw_choose_harness,
     "after", "The New Copilot Studio — a Model Inside a Harness"),
    ("Modern Orchestration — the Loop Replaces the Plan", "module 3 · concept", draw_modern_orchestration,
     "after", "Choosing a Harness"),
    ("The New Agent Designer", "module 3 · concept", draw_new_agent_designer,
     "after", "Modern Orchestration — the Loop Replaces the Plan"),
    ("Skills — Instructions on Demand", "module 3 · concept", draw_skills_on_demand,
     "after", "Writing Instructions That Constrain"),
    ("The New Workflow Designer", "module 4 · concept", draw_new_workflow_designer,
     "after", "Agent Flows — The Model Inside the Workflow"),
]


def slide_heading(s):
    best = None
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            t = sh.text_frame.text.strip().split("\n")[0]
            if sh.top is not None and Inches(0.5) < sh.top < Inches(1.2):
                return t
            if best is None:
                best = t
    return best or ""


for heading, kicker, draw, mode, anchor_title in NEW:
    s = prs.slides.add_slide(prs.slide_layouts[6])
    title(s, heading, kicker)
    draw(s)
    footer(s, 0)  # renumbered below
    el = list(id_list)[-1]
    # find anchor position
    pos = None
    for i, existing in enumerate(prs.slides):
        if existing is s:
            continue
        if slide_heading(existing) == anchor_title:
            pos = i + 1
            break
    assert pos is not None, f"anchor not found: {anchor_title}"
    id_list.remove(el)
    id_list.insert(pos, el)

print(f"After inserting new slides: {len(prs.slides)} slides")
assert len(prs.slides) == 75

# --- 3. update the Module 3 / Module 4 divider subtitles -------------------
for s in prs.slides:
    for sh in s.shapes:
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if r.text.startswith("Workflow versus agent  ·  instructions"):
                    r.text = ("The new Copilot Studio — model, harness, designer  ·  workflow versus agent  ·  "
                              "instructions, skills, knowledge, tools  ·  what is enforced  ·  publishing")
                elif r.text.startswith("The Agent node inside a flow"):
                    r.text = ("The new workflow designer  ·  the Agent node inside a flow  ·  HTTP request and "
                              "response  ·  structured output  ·  the human review gate")

# --- 3b. bump the cover version (content changed materially) ---------------
for sh in prs.slides[0].shapes:
    if sh.has_text_frame:
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if "Version 7.0" in r.text:
                    r.text = r.text.replace("Version 7.0 (2 Aug 2026)", "Version 7.1 (6 Aug 2026)")

# --- 4. renumber every footer page number ----------------------------------
for no, s in enumerate(prs.slides, 1):
    for sh in s.shapes:
        if not sh.has_text_frame:
            continue
        txt = sh.text_frame.text.strip()
        is_page_no = (
            txt.isdigit()
            and sh.top is not None
            and sh.top > Inches(6.6)
            and (sh.left or 0) > Inches(0.5)
        )
        if is_page_no:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.text.strip().isdigit():
                        r.text = str(no)
        elif txt.startswith("Business Process Automation with Power Automate and Copilot") and "|" in txt:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if "|" in r.text:
                        r.text = f"Business Process Automation with Power Automate and Copilot Studio Agents   |   {no}"

prs.save(DECK)

# python-pptx can write stale duplicate zip entries when slide parts are
# deleted and their partnames reused in the same session; keep only the last
# occurrence of each name (the live part) so PowerPoint sees a clean package.
import shutil
import zipfile

tmp = DECK.with_suffix(".pptx.repaired")
with zipfile.ZipFile(DECK) as zin:
    last = {}
    for idx, info in enumerate(zin.infolist()):
        last[info.filename] = idx
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for idx, info in enumerate(zin.infolist()):
            if last[info.filename] == idx:
                zout.writestr(info, zin.read(info))
shutil.move(tmp, DECK)
if DECK_IN.exists():
    DECK_IN.unlink()

print(f"Saved {DECK.name} with {len(prs.slides)} slides")
for i, s in enumerate(prs.slides, 1):
    print(f"{i:3d}  {slide_heading(s)[:70]}")
