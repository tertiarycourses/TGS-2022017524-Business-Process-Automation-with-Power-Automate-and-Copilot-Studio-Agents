#!/usr/bin/env python3
"""Build the Version 8.0 facilitator deck (18 labs, Lab 0-17, new Copilot Studio).

Self-contained python-pptx builder. Concepts first, labs second: every module
opens with its concept slides (beefed up from the six official Copilot Studio
sources), then every lab gets a banner slide, a build-steps slide and - when a
`screenshots/` folder exists for that lab - a screenshot slide picked up at
build time. Admin block at the front, assessment block at the end, all in the
Tertiary Infotech house style (16:9, all-white, Arial).

Outputs
  courseware/<title>-v8.0.pptx
  courseware/slide_map.json        (generated from the built deck)
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
CW = ROOT / "courseware"
ASSETS = CW / "assets"
VERSION = "8.1"
VERSION_DATE = "4 September 2026"
TITLE = "Business Process Automation with Power Automate and Copilot Studio Agents"
DECK = CW / f"{TITLE}-v{VERSION}.pptx"
SLIDE_MAP = CW / "slide_map.json"

# ------------------------------------------------------------------ manifest
# The manifest may still be v7.x while another agent rewrites it; the deck
# carries its own lab table and overlays whatever the manifest provides.
LAB_DEFAULTS = {
    "lab_0": dict(number=0, day=1, module="m1", title="Lab 0 — Environment Setup", subtitle="Training Class Sandbox (assigned by your trainer)", duration_minutes=20, platform="Power Platform admin centre + Copilot Studio", teaches="One Training Class Sandbox, with Dataverse and Copilot Credits, stands behind every later lab — and one designer builds everything.", path="labs/Lab 0 - Environment Setup/index.md", tenant_names=[]),
    "lab_1": dict(number=1, day=1, module="m1", title="Lab 1 — Trigger and Actions", subtitle="Form to email confirmation", duration_minutes=30, platform="Copilot Studio workflow + Microsoft Forms + Outlook", teaches="A trigger starts a workflow; connector actions consume the trigger's outputs as dynamic content.", path="labs/Lab 1 - Trigger and Actions/index.md", tenant_names=["Lab 1 - Trigger and Actions", "Lab 1 - Course Enquiry Form"]),
    "lab_2": dict(number=2, day=1, module="m1", title="Lab 2 — Log to Excel", subtitle="Log the enquiry, then send the email", duration_minutes=30, platform="Copilot Studio workflow + Excel Online", teaches="Commit before you confirm — the audit row is written before the acknowledgement is sent.", path="labs/Lab 2 - Log to Excel/index.md", tenant_names=["Lab 2 - Log to Excel", "Lab 2 - Enquiry Log.xlsx"]),
    "lab_3": dict(number=3, day=1, module="m2", title="Lab 3 — Leave Application Approval", subtitle="The workflow pauses for a manager", duration_minutes=35, platform="Copilot Studio workflow + Approvals + Outlook", teaches="A running workflow suspends at the approval action and branches with If/Else on the human decision.", path="labs/Lab 3 - Leave Application Approval/index.md", tenant_names=["Lab 3 - Leave Application Approval", "Lab 3 - Leave Application Form", "Lab 3 - Leave Register.xlsx"]),
    "lab_4": dict(number=4, day=1, module="m2", title="Lab 4 — Email Classification", subtitle="An inbox workflow that sorts, replies, books and escalates", duration_minutes=45, platform="Copilot Studio workflow + Outlook + Classify + Human review + Teams", teaches="The Classify node sorts each email into five categories; each port runs a deterministic handler, and the Priority branch stops at a human in Teams.", path="labs/Lab 4 - Email Classification/index.md", tenant_names=["Lab 4 - Email Classification"]),
    "lab_5": dict(number=5, day=1, module="m3", title="Lab 5 — Your First Agent", subtitle="An HR agent: instructions, knowledge, test, publish", duration_minutes=35, platform="Copilot Studio (new experience)", teaches="An agent is instructions plus a model plus knowledge — and the Preview tab is where you find out what it will refuse.", path="labs/Lab 5 - Your First Agent/index.md", tenant_names=["Lab 5 - HR Agent", "Lab 5 - HR Policies"]),
    "lab_6": dict(number=6, day=1, module="m3", title="Lab 6 — Procurement Agent with Tools", subtitle="A workflow as a tool, and the audit row it writes", duration_minutes=35, platform="Copilot Studio agent + workflow as a tool + Excel Online", teaches="The agent decides a tool applies and fills its inputs; the workflow's own logic is enforced.", path="labs/Lab 6 - Procurement Agent with Tools/index.md", tenant_names=["Lab 6 - Procurement Agent", "Lab 6 - Raise Requisition", "Lab 6 - Requisition Log.xlsx"]),
    "lab_7": dict(number=7, day=1, module="m3", title="Lab 7 — Sales Agent with Knowledge", subtitle="Grounded in 20 brochures, and refusing to invent", duration_minutes=30, platform="Copilot Studio agent + SharePoint knowledge", teaches="Grounding is giving the agent facts and taking away every other source.", path="labs/Lab 7 - Sales Agent with Knowledge/index.md", tenant_names=["Lab 7 - Sales Agent", "Lab 7 - Course Brochures"]),
    "lab_8": dict(number=8, day=1, module="m3", title="Lab 8 — IT Support Agent with Skills", subtitle="Five uploaded skill packages, and the one rule none of them can enforce", duration_minutes=30, platform="Copilot Studio agent + skill packages", teaches="A skill is a procedure the model decides to apply, not a permission — and a tool the agent does not have is a control.", path="labs/Lab 8 - IT Support Agent with Skills/index.md", tenant_names=["Lab 8 - IT Support Agent"]),
    "lab_9": dict(number=9, day=2, module="m3", title="Lab 9 — Multi-Agent Content Team", subtitle="Manager, Research, Blog and Review — one pipeline, four agents", duration_minutes=35, platform="Copilot Studio connected agents", teaches="One topic, four agents: the manager owns the conversation and delegates by stage of work.", path="labs/Lab 9 - Multi-Agent Content Team/index.md", tenant_names=["Lab 9 - Marketing Manager", "Lab 9 - Research Agent", "Lab 9 - Blog Agent", "Lab 9 - Review Agent"]),
    "lab_10": dict(number=10, day=2, module="m3", title="Lab 10 — Calling Agent from Workflow", subtitle="Blog-writer workflow: topic in, Teams post out", duration_minutes=25, platform="Copilot Studio workflow + M365 Copilot + Teams", teaches="The workflow calls the model at a fixed step, then acts on the result deterministically.", path="labs/Lab 10 - Calling Agent from Workflow/index.md", tenant_names=["Lab 10 - Calling Agent from Workflow"]),
    "lab_11": dict(number=11, day=2, module="m3", title="Lab 11 — Calling Workflow from Agent", subtitle="A blog-writer agent that calls a workflow as its tool", duration_minutes=25, platform="Copilot Studio agent + workflow as a tool", teaches="The agent decides when to call the workflow; the flow's inputs and outputs are the contract.", path="labs/Lab 11 - Calling Workflow from Agent/index.md", tenant_names=["Lab 11 - Blog Writer Agent", "Lab 11 - Blog Writer Tool"]),
    "lab_12": dict(number=12, day=2, module="m4", title="Lab 12 — HTTP and Application Approval Agent", subtitle="Marina Trust Bank customer onboarding", duration_minutes=45, platform="Copilot Studio workflow + SharePoint + Outlook", teaches="The boundary of agency — the AI decides what to do; deterministic actions do what must always happen.", path="labs/Lab 12 - HTTP and Application Approval Agent/index.md", tenant_names=["Lab 12 - HTTP and Application Approval Agent", "Lab 12 - Customers", "Lab 12 - Onboarding Log"]),
    "lab_13": dict(number=13, day=2, module="m4", title="Lab 13 — HTTP and Chatbot", subtitle="Investment advisor chatbot", duration_minutes=30, platform="Copilot Studio workflow + SharePoint knowledge + website", teaches="The agent alone — rules in the instruction, facts in the knowledge source, and a refusal it must never break.", path="labs/Lab 13 - HTTP and Chatbot/index.md", tenant_names=["Lab 13 - HTTP and Chatbot", "Lab 13 - Investment FAQ"]),
    "lab_14": dict(number=14, day=2, module="m4", title="Lab 14 — HTTP and Human Review", subtitle="Client rapport assistant with a Teams approval gate", duration_minutes=35, platform="Copilot Studio workflow + Human review + Excel Online + Teams", teaches="Human in the loop — the AI drafts, and the workflow physically cannot proceed until a person approves.", path="labs/Lab 14 - HTTP and Human Review/index.md", tenant_names=["Lab 14 - HTTP and Human Review", "Lab 14 - Handover Queue.xlsx"]),
    "lab_15": dict(number=15, day=2, module="m5", title="Lab 15 — RAG with Knowledge Base", subtitle="Cook & Bake Academy, built-in knowledge", duration_minutes=30, platform="Copilot Studio Knowledge + SharePoint", teaches="RAG as a product setting — three nodes, no ingestion, and nothing you can inspect.", path="labs/Lab 15 - RAG with Knowledge Base/index.md", tenant_names=["Lab 15 - RAG with Knowledge Base", "Lab 15 - Course Brochures"]),
    "lab_16": dict(number=16, day=2, module="m5", title="Lab 16 — RAG with Pinecone", subtitle="The same chatbot, with the levers back", duration_minutes=30, platform="Copilot Studio workflow + Pinecone", teaches="What the convenience cost — chunking, embeddings, dimension and top_k, back in your hands.", path="labs/Lab 16 - RAG with Pinecone/index.md", tenant_names=["Lab 16 - RAG with Pinecone", "lab16-course-brochures"]),
    "lab_17": dict(number=17, day=2, module="m5", title="Lab 17 — Publish to Teams, Microsoft 365 Copilot and the Web", subtitle="Channels + — where a published agent meets its users", duration_minutes=25, platform="Copilot Studio Channels + Teams + Microsoft 365 Copilot + website", teaches="Publish is what channels serve; each channel needs something different, and none of them changes the agent.", path="labs/Lab 17 - Publish to Teams, Microsoft 365 Copilot and the Web/index.md", tenant_names=["Lab 5 - HR Agent"]),
}
LABS = {k: dict(v) for k, v in LAB_DEFAULTS.items()}
MANIFEST_PATH = CW / "alignment_manifest.json"
if MANIFEST_PATH.exists():
    _m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for lab in _m.get("labs", []):
        lid = lab.get("id")
        if lid in LABS:
            for k in ("number", "day", "module", "title", "subtitle", "duration_minutes", "platform", "teaches", "path", "tenant_names"):
                if lab.get(k) not in (None, "", []):
                    LABS[lid][k] = lab[k]
    print(f"manifest v{_m.get('version')} read — {len(_m.get('labs', []))} labs overlaid")


def lab_dir(lab_id: str) -> Path:
    return ROOT / Path(LABS[lab_id]["path"]).parent


def lab_screenshots(lab_id: str) -> list[Path]:
    d = lab_dir(lab_id) / "screenshots"
    return sorted(d.glob("*.png")) if d.is_dir() else []


def lab_flowchart(lab_id: str) -> Path | None:
    p = lab_dir(lab_id) / "assets" / "flowchart.png"
    return p if p.exists() else None


# ------------------------------------------------------------------ palette
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
MODULE_COLOR = {"m1": BLUE, "m2": TEAL, "m3": VIOLET, "m4": GREEN, "m5": AMBER}

FOOTER_TEXT = (
    "Business Process Automation with Power Automate & Copilot Studio Agents  ·  "
    "TGS-2022017524  ·  © 2026 Tertiary Infotech Academy Pte Ltd"
)
BOTTOM_LIMIT = 6.88
BANNER_TOP = 6.08

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


# ------------------------------------------------------------------ primitives
def box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=True, line_w=1.2):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(line_w)
    shape.shadow.inherit = False
    return shape


def rect(slide, x, y, w, h, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def oval(slide, x, y, w, h, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def text(slide, x, y, w, h, value, size=18, color=INK, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, margin=0.08, space=0):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(margin)
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


def title(slide, heading, kicker, color=BLUE):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE
    rect(slide, 0, 0, Inches(0.22), Inches(1.48), color)
    text(slide, Inches(0.72), Inches(0.34), Inches(11.8), Inches(0.28), kicker.upper(), 12, color, True)
    text(slide, Inches(0.72), Inches(0.68), Inches(11.8), Inches(0.66), heading, 28, INK, True)
    rect(slide, Inches(0.72), Inches(1.5), Inches(11.85), Inches(0.015), LINE)


def footer(slide, slide_no):
    text(slide, Inches(0.72), Inches(6.95), Inches(11.85), Inches(0.24), FOOTER_TEXT, 8, GREY)
    text(slide, Inches(0.72), Inches(6.95), Inches(11.85), Inches(0.24), str(slide_no), 8, GREY, False, PP_ALIGN.RIGHT)


def card(slide, x, y, w, h, label, body, accent=BLUE, number=None, body_size=12, label_size=15, compact=False):
    box(slide, x, y, w, h, LIGHT, LINE)
    rect(slide, x, y, Inches(0.09), h, accent)
    if compact:
        text(slide, x + Inches(0.28), y + Inches(0.04), w - Inches(0.52), Inches(0.3), label, label_size, accent, True)
        if body:
            text(slide, x + Inches(0.28), y + Inches(0.32), w - Inches(0.54), h - Inches(0.36), body, body_size, GREY, anchor=MSO_ANCHOR.TOP, space=2)
        return
    if number is not None:
        oval(slide, x + Inches(0.24), y + Inches(0.18), Inches(0.46), Inches(0.46), accent)
        text(slide, x + Inches(0.24), y + Inches(0.18), Inches(0.46), Inches(0.46), str(number), 14, WHITE, True, PP_ALIGN.CENTER)
        lx, lw = x + Inches(0.82), w - Inches(1.04)
    else:
        lx, lw = x + Inches(0.28), w - Inches(0.52)
    text(slide, lx, y + Inches(0.12), lw, Inches(0.46), label, label_size, accent, True)
    if body:
        text(slide, x + Inches(0.28), y + Inches(0.64), w - Inches(0.54), h - Inches(0.76), body, body_size, GREY, anchor=MSO_ANCHOR.TOP, space=3)


def arrow(slide, x, y, w, h, color=BLUE, direction="right"):
    kind = MSO_SHAPE.CHEVRON if direction == "right" else MSO_SHAPE.DOWN_ARROW
    shape = slide.shapes.add_shape(kind, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def flow(slide, y, nodes, labels=None, colors=None, x0=0.72, total=11.85, height=1.15, size=13):
    labels = labels or [""] * (len(nodes) - 1)
    colors = colors or [BLUE] * len(nodes)
    gap = 0.46
    node_w = (total - gap * (len(nodes) - 1)) / len(nodes)
    for i, node in enumerate(nodes):
        x = Inches(x0 + i * (node_w + gap))
        box(slide, x, Inches(y), Inches(node_w), Inches(height), WHITE, colors[i], line_w=1.6)
        text(slide, x + Inches(0.06), Inches(y + 0.06), Inches(node_w - 0.12), Inches(height - 0.12), node, size, INK, True, PP_ALIGN.CENTER)
        if i < len(nodes) - 1:
            arrow(slide, x + Inches(node_w + 0.07), Inches(y + height / 2 - 0.17), Inches(0.3), Inches(0.34), colors[i])
            if labels[i]:
                # Edge labels sit ABOVE the node row, bottom-anchored just above the nodes so a
                # long label grows UPWARD instead of overprinting them. The box is widened to
                # gap+1.30in so a long label (e.g. "instruction · knowledge · history") wraps
                # instead of clipping, and its height is sized to the number of wrapped lines --
                # a short one-line label keeps a 0.24in box and so cannot reach up into the
                # lead sentence above the flow.
                lbl_w = gap + 1.30
                # ~9pt Arial averages ~0.062in per character; estimate the wrapped line count.
                est_lines = max(1, math.ceil(len(labels[i]) * 0.062 / (lbl_w - 0.16)))
                lbl_h = 0.16 + 0.14 * est_lines
                text(slide, x + Inches(node_w + gap / 2) - Inches(lbl_w / 2), Inches(y - lbl_h - 0.04),
                     Inches(lbl_w), Inches(lbl_h), labels[i], 9, GREY, False, PP_ALIGN.CENTER,
                     anchor=MSO_ANCHOR.BOTTOM)


def table(slide, y, headers, rows, widths, colors=None, x0=0.72, row_h=0.52, head_h=0.46,
          size=12, head_size=12, head_color=BLUE, bottom=None, first_bold=True):
    bottom = bottom or BOTTOM_LIMIT
    colors = colors or [INK] * len(rows)
    overflow = (y + head_h + len(rows) * row_h) - bottom
    if overflow > 0:
        row_h = max(0.3, row_h - overflow / len(rows))
    total = sum(widths)
    hx = x0
    rect(slide, Inches(x0), Inches(y), Inches(total), Inches(head_h), head_color)
    for w, htext in zip(widths, headers):
        text(slide, Inches(hx + 0.12), Inches(y), Inches(w - 0.18), Inches(head_h), htext, head_size, WHITE, True)
        hx += w
    for r, row in enumerate(rows):
        ry = y + head_h + r * row_h
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0), Inches(ry), Inches(total), Inches(row_h))
        band.fill.solid()
        band.fill.fore_color.rgb = WHITE if r % 2 == 0 else LIGHT
        band.line.color.rgb = LINE
        band.line.width = Pt(0.75)
        band.shadow.inherit = False
        cx = x0
        for c, (w, cell) in enumerate(zip(widths, row)):
            text(slide, Inches(cx + 0.12), Inches(ry), Inches(w - 0.18), Inches(row_h), cell, size,
                 colors[r] if c == 0 else GREY, first_bold and c == 0)
            cx += w
    return y + head_h + len(rows) * row_h


def takeaway(slide, y, message, color=BLUE):
    y = min(y, BOTTOM_LIMIT - 0.62)
    box(slide, Inches(0.72), Inches(y), Inches(11.85), Inches(0.62), LIGHT, color, line_w=1.6)
    text(slide, Inches(1.0), Inches(y), Inches(11.3), Inches(0.62), message, 13, INK, True)


def lead(slide, value, y=1.66, size=14):
    text(slide, Inches(0.72), Inches(y), Inches(11.85), Inches(0.4), value, size, INK, anchor=MSO_ANCHOR.TOP)


def note(slide, y, label, body, color=AMBER, h=0.95):
    box(slide, Inches(0.72), Inches(y), Inches(11.85), Inches(h), LIGHT, color, line_w=1.6)
    text(slide, Inches(1.0), Inches(y + 0.06), Inches(11.3), Inches(0.3), label, 11, color, True)
    text(slide, Inches(1.0), Inches(y + 0.36), Inches(11.3), Inches(h - 0.42), body, 11, GREY, anchor=MSO_ANCHOR.TOP)


def head_panel(slide, x, y, w, h, heading, lines, color, size=12, head_h=0.52):
    """Bordered panel with a coloured header band and short bullet lines."""
    box(slide, Inches(x), Inches(y), Inches(w), Inches(h), WHITE, color, line_w=1.8)
    rect(slide, Inches(x), Inches(y), Inches(w), Inches(head_h), color)
    text(slide, Inches(x), Inches(y), Inches(w), Inches(head_h), heading, 13, WHITE, True, PP_ALIGN.CENTER)
    step = (h - head_h - 0.1) / max(1, len(lines))
    for i, t in enumerate(lines):
        text(slide, Inches(x + 0.25), Inches(y + head_h + 0.05 + i * step), Inches(w - 0.45), Inches(step), "•  " + t, size, GREY)


def chip(slide, x, y, w, h, value, color, size=10):
    c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    c.fill.solid()
    c.fill.fore_color.rgb = color
    c.line.fill.background()
    c.shadow.inherit = False
    text(slide, x, y, w, h, value, size, WHITE, True, PP_ALIGN.CENTER)


def pic_fit(slide, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    pw, ph = int(iw * scale), int(ih * scale)
    slide.shapes.add_picture(str(path), int(x + (w - pw) / 2), int(y + (h - ph) / 2), pw, ph)


def tile_grid(slide, items, cols=2, y0=1.75, area_h=5.0, size=14, accent_cycle=None):
    """Grid of light panels with a coloured numbered badge (ported from the wsq-slides reference)."""
    import math
    n = len(items)
    rows = math.ceil(n / cols)
    X0, TOTW = Inches(0.72), Inches(11.85)
    gx, gy = Inches(0.28), Inches(0.22)
    cw = int((TOTW - gx * (cols - 1)) / cols)
    ch = int((Inches(area_h) - gy * (rows - 1)) / rows)
    bd = Inches(0.56)
    cycle = accent_cycle or PALETTE
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        x = int(X0 + (cw + gx) * c)
        y = int(Inches(y0) + (ch + gy) * r)
        col = cycle[i % len(cycle)]
        box(slide, x, y, cw, ch, LIGHT, LINE)
        rect(slide, x, y, Inches(0.09), ch, col)
        oval(slide, x + Inches(0.26), int(y + ch / 2 - bd / 2), bd, bd, col)
        text(slide, x + Inches(0.26), int(y + ch / 2 - bd / 2), bd, bd, str(i + 1), 16, WHITE, True, PP_ALIGN.CENTER)
        tx, tw = x + Inches(1.0), cw - Inches(1.2)
        if isinstance(it, tuple):
            text(slide, tx, y + Inches(0.08), tw, ch - Inches(0.14), it[0], size + 1, INK, True, anchor=MSO_ANCHOR.TOP)
            text(slide, tx, y + Inches(0.5), tw, ch - Inches(0.56), it[1], size - 2, GREY, anchor=MSO_ANCHOR.TOP)
        else:
            text(slide, tx, y + Inches(0.06), tw, ch - Inches(0.12), it, size, INK)


def flow_h(slide, steps, y=2.3, color=BLUE, h=3.3):
    """Horizontal numbered chips joined by chevrons (Assessment Flow diagram)."""
    n = len(steps)
    X0, TOTW, gap = Inches(0.72), Inches(11.85), Inches(0.34)
    cw = int((TOTW - gap * (n - 1)) / n)
    bd = Inches(0.82)
    for i, st in enumerate(steps):
        x = int(X0 + (cw + gap) * i)
        box(slide, x, Inches(y), cw, Inches(h), LIGHT, LINE)
        rect(slide, x, Inches(y), cw, Inches(0.1), color)
        oval(slide, int(x + cw / 2 - bd / 2), int(Inches(y + 0.45)), bd, bd, color)
        text(slide, int(x + cw / 2 - bd / 2), int(Inches(y + 0.45)), bd, bd, str(i + 1), 28, WHITE, True, PP_ALIGN.CENTER)
        text(slide, x + Inches(0.14), int(Inches(y + 1.55)), cw - Inches(0.28), int(Inches(h - 1.7)), st, 14, INK, False, PP_ALIGN.CENTER, MSO_ANCHOR.TOP)
        if i < n - 1:
            arrow(slide, x + cw + Inches(0.03), int(Inches(y + h / 2 - 0.17)), Inches(0.28), Inches(0.34), color)


def lab_banner(slide, lab_id, y=BANNER_TOP):
    lab = LABS[lab_id]
    y = min(y, BANNER_TOP + 0.02)
    box(slide, Inches(0.72), Inches(y), Inches(11.85), Inches(0.78), WHITE, GREEN, line_w=1.8)
    chip(slide, Inches(0.92), Inches(y + 0.14), Inches(1.15), Inches(0.5), f"LAB {lab['number']}", GREEN, 13)
    text(slide, Inches(2.25), Inches(y + 0.02), Inches(10.1), Inches(0.36), lab["title"], 14, INK, True)
    text(slide, Inches(2.25), Inches(y + 0.38), Inches(10.1), Inches(0.34), f"{lab['subtitle']}  ·  {lab['platform']}  ·  {lab['duration_minutes']} min", 11, GREY)


# ------------------------------------------------------------------ registry
SLIDES: list[dict] = []


def slide(heading, kicker, draw, section="", module="", lab="", color=BLUE):
    SLIDES.append(dict(heading=heading, kicker=kicker, draw=draw, section=section, module=module, lab=lab, color=color))


def divider(kicker, heading, subtitle, color=BLUE):
    def draw(s):
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = WHITE
        box(s, Inches(0.72), Inches(1.9), Inches(11.85), Inches(3.6), LIGHT, color, line_w=2.0)
        rect(s, Inches(0.72), Inches(1.9), Inches(0.14), Inches(3.6), color)
        text(s, Inches(1.4), Inches(2.35), Inches(10.8), Inches(0.4), kicker.upper(), 15, color, True)
        text(s, Inches(1.4), Inches(2.85), Inches(10.8), Inches(0.95), heading, 34, INK, True)
        text(s, Inches(1.4), Inches(3.95), Inches(10.8), Inches(1.1), subtitle, 14, GREY, anchor=MSO_ANCHOR.TOP, space=6)
    return draw


# ===========================================================================
# ADMIN BLOCK (front)
# ===========================================================================
def draw_cover(s):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = WHITE
    rect(s, 0, 0, SW, Inches(0.2), BLUE)
    rect(s, 0, Inches(7.3), SW, Inches(0.2), TEAL)
    logo = ASSETS / "tertiary-infotech-logo.png"
    if logo.exists():
        s.shapes.add_picture(str(logo), Inches(6.17), Inches(0.55), Inches(1.0), Inches(1.0))
    text(s, Inches(1.67), Inches(1.7), Inches(10.0), Inches(1.1), "Business Process Automation", 40, INK, True, PP_ALIGN.CENTER)
    text(s, Inches(1.67), Inches(2.8), Inches(10.0), Inches(0.7), "with Power Automate and Copilot Studio Agents", 24, INK, True, PP_ALIGN.CENTER)
    rect(s, Inches(5.6), Inches(3.62), Inches(2.1), Inches(0.05), TEAL)
    text(s, Inches(1.67), Inches(3.8), Inches(10.0), Inches(0.5), "WSQ Course Code: TGS-2022017524  ·  2-Day Hands-On Training  ·  Modules 1–5  ·  18 Labs", 15, GREY, False, PP_ALIGN.CENTER)
    text(s, Inches(1.67), Inches(4.35), Inches(10.0), Inches(0.5), "Built entirely in the new Copilot Studio — workflows, agents, skills, tools, channels", 13, BLUE, True, PP_ALIGN.CENTER)
    text(s, Inches(1.67), Inches(5.35), Inches(10.0), Inches(0.45), "Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W", 14, GREY, False, PP_ALIGN.CENTER)
    text(s, Inches(1.67), Inches(5.8), Inches(10.0), Inches(0.4), f"Version {VERSION} ({VERSION_DATE})  ·  www.tertiarycourses.com.sg  ·  https://lms-tms.tertiaryinfotech.com/", 11, GREY, False, PP_ALIGN.CENTER)


def draw_attendance(s):
    items = [
        ("AM, PM and Assessment", "It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses."),
        ("The SSG QR code", "The trainer/administrator displays the digital attendance QR code from the SSG portal."),
        ("Scan and submit", "Scan the QR code with your mobile phone camera and submit your attendance."),
        ("75% minimum", "A minimum of 75% attendance is required to be eligible for assessment and funding."),
    ]
    tile_grid(s, items, cols=2, y0=1.8, area_h=4.3, size=15)
    takeaway(s, 6.22, "TRAQOM is the SSG digital attendance system — take it three times a day, every day.", TEAL)


def trainer_draw(name, role, rows, initials, accent):
    def draw(s):
        lx, lw = Inches(0.72), Inches(3.65)
        box(s, lx, Inches(1.75), lw, Inches(5.0), LIGHT, LINE)
        rect(s, lx, Inches(1.75), lw, Inches(0.12), accent)
        bd = Inches(1.7)
        ax = int(lx + (lw - bd) / 2)
        oval(s, ax, Inches(2.3), bd, bd, accent)
        text(s, ax, Inches(2.3), bd, bd, initials, 44, WHITE, True, PP_ALIGN.CENTER)
        text(s, lx + Inches(0.15), Inches(4.35), lw - Inches(0.3), Inches(0.6), name, 21, INK, True, PP_ALIGN.CENTER)
        text(s, lx + Inches(0.15), Inches(5.0), lw - Inches(0.3), Inches(1.2), role, 13, GREY, False, PP_ALIGN.CENTER, MSO_ANCHOR.TOP)
        rx, rw, ry, rh = Inches(4.75), Inches(7.82), Inches(1.75), Inches(5.0)
        n = len(rows)
        gy = Inches(0.18)
        th = int((rh - gy * (n - 1)) / n)
        for i, (label, val) in enumerate(rows):
            y = int(ry + (th + gy) * i)
            col = PALETTE[i % len(PALETTE)]
            box(s, rx, y, rw, th, LIGHT, LINE)
            rect(s, rx, y, Inches(0.09), th, col)
            text(s, rx + Inches(0.3), y + Inches(0.04), rw - Inches(0.5), Inches(0.3), label.upper(), 11, col, True)
            if val:
                text(s, rx + Inches(0.3), y + Inches(0.3), rw - Inches(0.5), th - Inches(0.34), val, 13, INK, anchor=MSO_ANCHOR.TOP)
            else:
                text(s, rx + Inches(0.3), y + Inches(0.3), rw - Inches(0.5), th - Inches(0.34), "________________________________________________", 12, LINE, anchor=MSO_ANCHOR.TOP)
    return draw


def draw_icebreaker(s):
    items = [
        ("Who you are", "Your name and your organisation / role."),
        ("What you have used", "Your experience with Power Automate, Copilot Studio or other automation tools (if any)."),
        ("What you want to automate", "One repetitive business process you would love to automate after this course."),
    ]
    tile_grid(s, items, cols=1, y0=1.8, area_h=4.3, size=16)
    takeaway(s, 6.22, "Keep the process in mind — by Day 2 you will know which parts of it should be a workflow, an agent, or a person.")


def draw_ground_rules(s):
    items = ["Set your mobile phone to silent mode.", "Participate actively — no question is too small.",
             "Mutual respect: agree to disagree.", "One conversation at a time.",
             "Be punctual; return from breaks on time.", "75% attendance is required."]
    tile_grid(s, items, cols=2, y0=1.8, area_h=4.95, size=15)


def draw_lms(s):
    img = ASSETS / "lms-portal-card.png"
    box(s, Inches(0.72), Inches(1.75), Inches(3.8), Inches(4.95), LIGHT, LINE)
    if img.exists():
        pic_fit(s, img, Inches(0.85), Inches(1.88), Inches(3.55), Inches(4.7))
    steps = [
        ("1 · Sign in", "lms-tms.tertiaryinfotech.com — log in with your registered email (OTP or password).", BLUE),
        ("2 · Download materials", "Slides (PDF) and the Learner Guide from the course page — your open-book references.", TEAL),
        ("3 · Submit answers", "Upload your Written Assessment and Practical Performance answers on the LMS.", VIOLET),
        ("4 · TRAQOM survey", "Complete the TRAQOM survey via the QR code shown on the LMS.", AMBER),
    ]
    for i, (label, body, color) in enumerate(steps):
        col, row = divmod(i, 2)
        card(s, Inches(4.8 + col * 3.95), Inches(1.75 + row * 1.95), Inches(3.77), Inches(1.75), label, body, color, body_size=12, label_size=14)
    box(s, Inches(4.8), Inches(5.75), Inches(7.77), Inches(0.62), WHITE, BLUE, line_w=1.8)
    text(s, Inches(4.8), Inches(5.75), Inches(7.77), Inches(0.62), "https://lms-tms.tertiaryinfotech.com/", 16, BLUE, True, PP_ALIGN.CENTER)


DAY1 = [("Welcome, admin, course map", 30), ("Module 1 — BPA, Power Platform, the new Copilot Studio, workflows", 50), ("Tea break", 15),
        ("Lab 0 — Environment Setup", 20), ("Lab 1 — Trigger and Actions", 30), ("Lab 2 — Log to Excel", 30), ("Lunch", 60),
        ("Module 2 — Control flow and human in the loop", 25), ("Lab 3 — Leave Application Approval", 35), ("Lab 4 — Email Classification", 45),
        ("Tea break", 15), ("Module 3 — Copilot Studio agents", 45), ("Lab 5 — Your First Agent", 35), ("Lab 6 — Procurement Agent with Tools", 35),
        ("Lab 7 — Sales Agent with Knowledge", 30), ("Lab 8 — IT Support Agent with Skills", 30), ("Day 1 recap", 10)]
DAY2 = [("Day 2 recap", 5), ("Lab 9 — Multi-Agent Content Team", 35), ("Lab 10 — Calling Agent from Workflow", 25), ("Lab 11 — Calling Workflow from Agent", 25),
        ("Tea break", 15), ("Module 4 — HTTP, autonomous processes, boundary of agency", 25), ("Lab 12 — HTTP and Application Approval Agent", 45), ("Lunch", 60),
        ("Lab 13 — HTTP and Chatbot", 30), ("Lab 14 — HTTP and Human Review", 35), ("Module 5 — Retrieval Augmented Generation", 15),
        ("Lab 15 — RAG with Knowledge Base", 30), ("Lab 16 — RAG with Pinecone", 30), ("Tea break", 15),
        ("Lab 17 — Publish to Teams, M365 Copilot and the Web", 25), ("Synthesis", 5), ("Written Assessment (SAQ)", 60), ("Practical Performance (PP)", 60)]


def _times(rows):
    # House standard: 9:30am - 6:30pm = 540 elapsed, less the 1-hour lunch =
    # 480 instructional minutes per day (tea breaks counted within).
    out, t = [], 9 * 60 + 30
    for label, mins in rows:
        a, b = t, t + mins
        fmt = lambda m: f"{(m // 60 - 1) % 12 + 1}:{m % 60:02d}"
        out.append((f"{fmt(a)} – {fmt(b)}", label, mins))
        t = b
    assert t == 18 * 60 + 30, t
    instructional = sum(m for label, m in rows if label != "Lunch")
    assert instructional == 480, instructional
    return out


def schedule_draw(rows, day_label, color, split):
    def draw(s):
        timed = _times(rows)
        halves = [timed[:split], timed[split:]]
        for col, half in enumerate(halves):
            x = Inches(0.72 + col * 6.05)
            box(s, x, Inches(1.7), Inches(5.8), Inches(5.05), WHITE, color, line_w=1.8)
            rect(s, x, Inches(1.7), Inches(5.8), Inches(0.46), color)
            text(s, x + Inches(0.2), Inches(1.7), Inches(5.4), Inches(0.46), ("Morning" if col == 0 else "Afternoon") + f"  ·  {day_label}", 12, WHITE, True)
            rh = min(0.44, 4.45 / len(half))
            for i, (slot, what, mins) in enumerate(half):
                y = Inches(2.25 + i * rh)
                is_break = what in ("Tea break", "Lunch")
                is_assess = what.startswith(("Written", "Practical"))
                c = AMBER if is_break else (RED if is_assess else (GREEN if what.startswith("Lab") else color))
                text(s, x + Inches(0.2), y, Inches(1.35), Inches(rh), slot, 10, c, True)
                text(s, x + Inches(1.6), y, Inches(3.55), Inches(rh), what, 10, GREY if not is_assess else INK, is_assess)
                text(s, x + Inches(5.15), y, Inches(0.6), Inches(rh), f"{mins}m", 9, GREY, False, PP_ALIGN.RIGHT)
    return draw


def draw_outcomes(s):
    flow(s, 1.95, ["Automate\nthe workflow", "Add the\nagent", "Connect it\nover HTTP", "Ground it\nwith RAG", "Publish it\nto channels"],
         ["add AI", "expose it", "make it true", "ship it"], [BLUE, VIOLET, GREEN, AMBER, TEAL], height=1.3, size=13)
    items = [
        ("Design", "Read a business process and decide which parts must be deterministic, which may be AI, and where a person must sit.", BLUE),
        ("Build", "Create Copilot Studio workflows and agents with instructions, knowledge, skills, tools and connected agents.", VIOLET),
        ("Govern", "Place the human where the consequence lands, test what the agent must refuse, and publish only what is safe.", RED),
    ]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(3.75), Inches(3.71), Inches(2.0), label, body, color, i + 1)
    takeaway(s, 6.1, "By the end you can build the automation, add the agent, and defend where you put the human.")


def draw_briefing(s):
    items = ["Place phones and other materials under the table or on the floor.", "No photos or recording of assessment scripts.",
             "No discussion during the assessment.", "Use a black/blue pen for hard-copy assessments.",
             "No liquid paper / correction tape.", "Scripts are collected when time is up."]
    tile_grid(s, items, cols=2, y0=1.8, area_h=4.95, size=15)


def draw_assessment_funding(s):
    cards = [
        ("Written Assessment", "1 hour · open book\nShort-answer questions on Modules 1–5 and the lab concepts.", BLUE),
        ("Practical Performance", "1 hour · open book\nBuild and verify a working workflow and agent in the training environment.", VIOLET),
        ("Evidence & funding", "Submit on the LMS.\nA Competent result plus the attendance requirement releases the WSQ funding.", GREEN),
    ]
    for i, (label, body, color) in enumerate(cards):
        card(s, Inches(0.72 + i * 3.99), Inches(1.8), Inches(3.71), Inches(2.9), label, body, color, i + 1, 13, 16)
    takeaway(s, 5.0, "Day 2, 4:30 – 6:30 PM: Written Assessment (SAQ) 1 hr, then Practical Performance 1 hr.", RED)
    note(s, 5.85, "OPEN BOOK", "Slides, Learner Guide and approved materials only. An appeal process is available if required.", BLUE, 0.9)


ASSESS_FLOW = ["TRAQOM survey — scan the QR code on the LMS", "Assessment digital attendance — scan the SSG QR",
               "Sit WA (SAQ) then PP — open book", "Submit your answers on the LMS", "Sign the Assessment Summary Record"]


def draw_assess_flow(s):
    flow_h(s, ASSESS_FLOW, y=2.2, color=BLUE, h=3.4)


def draw_assessment_end(s):
    items = [
        ("Two parts", "Written Assessment (SAQ) — 1 hour. Practical Performance (PP) — 1 hour."),
        ("Open book", "Slides, Learner Guide and approved materials only."),
        ("Attendance", "Remember to take the Assessment digital attendance (TRAQOM)."),
        ("Submit", "Submit your completed answers on the LMS at https://lms-tms.tertiaryinfotech.com/."),
    ]
    tile_grid(s, items, cols=2, y0=1.8, area_h=4.95, size=15)


def draw_practice_exam(s):
    items = [
        ("Sharpen up", "Attempt the Tertiary Infotech practice exam for this course under timed conditions."),
        ("Where", "https://exams.tertiaryinfotech.com — search for the course title or TGS-2022017524."),
        ("Review", "Read every explanation; revisit the lab whose concept you missed."),
        ("Repeat", "Re-take the practice exam until the concepts, not the answers, are automatic."),
    ]
    tile_grid(s, items, cols=2, y0=1.8, area_h=4.3, size=15)
    box(s, Inches(0.72), Inches(6.2), Inches(11.85), Inches(0.62), WHITE, BLUE, line_w=1.8)
    text(s, Inches(0.72), Inches(6.2), Inches(11.85), Inches(0.62), "https://exams.tertiaryinfotech.com", 16, BLUE, True, PP_ALIGN.CENTER)


def draw_thanks(s):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = WHITE
    rect(s, 0, 0, SW, Inches(0.2), TEAL)
    text(s, Inches(1.1), Inches(2.2), Inches(11), Inches(0.5), "SEE YOU IN THE TENANT", 16, TEAL, True)
    text(s, Inches(1.1), Inches(2.8), Inches(11.3), Inches(1.6), "Thank You", 48, INK, True)
    text(s, Inches(1.12), Inches(4.5), Inches(11), Inches(1.2), "Now go automate something — and put the human where the consequence lands. Questions welcome.", 20, GREY, anchor=MSO_ANCHOR.TOP)


# ===========================================================================
# COURSE OVERVIEW
# ===========================================================================
JOURNEY_NOTES = {
    0: "Training Class Sandbox, Dataverse, credits", 1: "Forms trigger → Outlook; dynamic content", 2: "Excel row first, then the email",
    3: "Approvals: the workflow pauses for a manager", 4: "Classify node, five ports, Human review in Teams", 5: "HR agent: instructions + knowledge + Preview",
    6: "Skills + a workflow as a tool + Excel audit row", 7: "20 brochures in SharePoint; refuse to invent", 8: "Five SKILL.md packages; the rule none enforce",
    9: "Manager → Research → Blog → Review", 10: "Workflow calls M365 Copilot, posts to Teams", 11: "Agent calls a workflow tool (When an agent calls the flow)",
    12: "HTTP POST, structured output, SharePoint, four decisions", 13: "HTTP chatbot alone in public", 14: "HTTP + Human review gate + handover log",
    15: "Knowledge source in the Agent node", 16: "Pinecone: chunk, embed, top_k", 17: "Channels +: Teams, M365 Copilot, demo website",
}


def journey_draw(lab_ids, caption):
    def draw(s):
        for i, lid in enumerate(lab_ids):
            lab = LABS[lid]
            row, col = divmod(i, 3)
            x = Inches(0.72 + col * 3.99)
            y = Inches(1.7 + row * 1.42)
            color = MODULE_COLOR[lab["module"]]
            box(s, x, y, Inches(3.71), Inches(1.28), LIGHT, LINE)
            chip(s, x + Inches(0.14), y + Inches(0.14), Inches(0.62), Inches(0.5), str(lab["number"]), color, 13)
            text(s, x + Inches(0.86), y + Inches(0.06), Inches(2.75), Inches(0.62), lab["title"].split("—", 1)[1].strip(), 12, INK, True)
            text(s, x + Inches(0.2), y + Inches(0.66), Inches(3.4), Inches(0.58), JOURNEY_NOTES.get(lab["number"], lab["subtitle"]), 10, GREY, anchor=MSO_ANCHOR.TOP)
        takeaway(s, 6.05, caption)
    return draw


def draw_approach(s):
    steps = [
        ("Concept", "The idea and the decision rule, before the product is opened.", BLUE),
        ("Pattern", "The same idea drawn as a business workflow you could hand to a colleague.", TEAL),
        ("Lab", "You build it, in the numbered lab named on the concept slide.", GREEN),
        ("Probe", "You try to break it — the refusals and wrong answers are the lesson.", RED),
        ("Reuse", "The working artefact becomes the starting point of the next lab.", VIOLET),
    ]
    for i, (label, body, color) in enumerate(steps):
        card(s, Inches(0.72 + i * 2.42), Inches(1.9), Inches(2.2), Inches(2.6), label, body, color, i + 1, 11, 14)
    takeaway(s, 4.85, "Concepts first. Every lab in this course is an application of a concept you have already seen.")
    text(s, Inches(0.72), Inches(5.7), Inches(11.85), Inches(0.9),
         "The probes matter as much as the builds. An agent that answers ten questions correctly and the eleventh confidently wrong has not been tested — it has been demonstrated.",
         13, GREY, anchor=MSO_ANCHOR.TOP)


def draw_naming(s):
    lead(s, "Everything in the tenant is named after its lab, so a learner, a trainer and an auditor can all find it.")
    rows = [
        ("Trainer's reference copy", "Lab 6 - Raise Requisition (DO NOT DELETE)  ·  Lab 6 - Proc (DO NOT DELETE)", "In the master reference Sandbox. Workflows AND agents end (DO NOT DELETE); agent base names are shortened to fit the 30-character cap"),
        ("Your own build", "Lab 6 - Procurement Agent", "In your Training Class environment. Name it exactly as the Learner Guide does"),
        ("Helper workflow", "Lab 6 - Raise Requisition", "The lab prefix, then the workflow's job"),
        ("Data artefact", "Lab 6 - Requisition Log.xlsx  ·  Lab 12 - Customers", "Excel, SharePoint lists and folders carry the prefix too"),
        ("Pinecone index", "lab16-course-brochures", "Lower-case, hyphenated — the only exception, imposed by Pinecone"),
    ]
    table(s, 2.2, ["Artefact", "Exact name", "Rule"], rows, [2.6, 5.35, 3.9], row_h=0.55, size=11)
    note(s, 5.5, "YOUR CLASS ENVIRONMENT, ONE DESIGNER",
         "You build in the Training Class Sandbox your trainer assigned (e.g. Training Class 1), in the new Copilot Studio designer at copilotstudio.microsoft.com. "
         "The (DO NOT DELETE) reference copies live in a separate master reference Sandbox — open to compare, never to edit.", BLUE, 1.25)


def draw_environments(s):
    lead(s, "Three environments back this course. You build in exactly one of them — and it is not the one holding the reference copies.")
    rows = [
        ("Training Class 1 / 2 / 3", "Sandbox", "YOURS — every lab you build goes here. One per class; the trainer resets it between cohorts"),
        ("TGS-2022017524-Business Process\nAutomation…", "Sandbox", "Master reference environment: the trainer's Lab N - … (DO NOT DELETE) workflows and agents. Read-only — open to compare, never edit"),
        ("Copilot Studio Training", "Developer", "The original build environment. Retired from classroom use — a Developer environment is single-user"),
    ]
    # row_h 0.62 (not 0.72): three rows end at B4.47in, clearing the type cards at T4.62in.
    table(s, 2.15, ["Environment", "Type", "What it is for"], rows, [3.5, 1.5, 6.85], row_h=0.62, size=11)
    cards = [("Developer", "One user only. Free, persistent — but a class cannot share it.", GREY),
             ("Sandbox", "Multi-user AND resettable in one click. What every class uses.", GREEN),
             ("Trial", "Self-deletes after 30 days, taking the class's work with it.", RED)]
    for i, (label, body, color) in enumerate(cards):
        card(s, Inches(0.72 + i * 3.99), Inches(4.62), Inches(3.71), Inches(1.5), label, body, color, body_size=11)
    takeaway(s, 6.3, "Sandbox is the only type that is both multi-user and resettable — so your class environment is disposable on purpose.", GREEN)


def draw_repository(s):
    items = [
        ("18 labs", "labs/Lab N - <Title>/index.md — Lab 0 setup plus Labs 1–17, each with its own step-by-step guide, assets and screenshots.", BLUE),
        ("Ready assets", "Forms, Excel workbooks, brochure PDFs, HTML pages, JSON schemas, SKILL.md packages and agent instructions.", TEAL),
        ("Test data", "Sample emails, question sets and probe cases written to make each workflow and agent fail.", AMBER),
        ("Learner Guide + LMS", "The Learner Guide reproduces every lab; download it and the slides from lms-tms.tertiaryinfotech.com.", GREEN),
    ]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(1.85 + row * 2.15), Inches(5.8), Inches(1.95), label, body, color, i + 1, 12)
    takeaway(s, 6.2, "Work in order. Every lab reuses the one before it; nothing is rebuilt from scratch.")


def draw_training_account(s):
    lead(s, "One assigned Microsoft 365 training account per learner — the same login for every lab, in your class environment.")
    for i in range(10):
        row, col = divmod(i, 2)
        x = Inches(0.72 + col * 6.05)
        y = Inches(2.15 + row * 0.62)
        box(s, x, y, Inches(5.8), Inches(0.52), LIGHT, LINE)
        text(s, x + Inches(0.15), y, Inches(3.9), Inches(0.52), f"training{i + 1}@tertiaryinfotech.onmicrosoft.com", 12, INK, True)
        text(s, x + Inches(4.05), y, Inches(1.7), Inches(0.52), "Reserved for the trainer" if i == 0 else f"Learner account {i}", 10, GREY)
    takeaway(s, 5.35, "Password for training2 – training10:  Tertiary@0808", BLUE)
    # One line only: a second wrapped line autogrows the box past B6.85in into the footer.
    # (The "Default has no Copilot Credits" point is already made on the Power Platform slide.)
    note(s, 6.05, "STAY IN YOUR CLASS ENVIRONMENT",
         "Confirm your Training Class environment (e.g. Training Class 1) shows bottom-left before you build anything.", RED, 0.8)


# ===========================================================================
# MODULE 1 — BPA, POWER PLATFORM, THE NEW COPILOT STUDIO, WORKFLOWS
# ===========================================================================
def draw_what_is_bpa(s):
    lead(s, "Business process automation is not \"software that does work faster\". It removes the hand-off where a person re-types what another system already knows.")
    text(s, Inches(0.72), Inches(2.6), Inches(1.5), Inches(0.5), "MANUAL", 12, RED, True)
    flow(s, 2.55, ["Form filled in", "Someone reads it", "Re-typed into Excel", "Someone remembers\nto reply"], ["", "", ""], [GREY] * 4, x0=2.3, total=10.25, height=0.95, size=12)
    text(s, Inches(0.72), Inches(3.95), Inches(1.5), Inches(0.5), "AUTOMATED", 12, GREEN, True)
    flow(s, 3.9, ["Form submitted", "Workflow triggered", "Row written", "Reply sent"], ["", "", ""], [BLUE, BLUE, TEAL, GREEN], x0=2.3, total=10.25, height=0.95, size=12)
    cards = [("Consistency", "The same input produces the same output, every time, at 3am.", TEAL),
             ("Traceability", "Every run leaves an Activity record someone can read a year later.", BLUE),
             ("Capacity", "People are moved to the judgement calls the machine cannot make.", VIOLET)]
    for i, (label, body, color) in enumerate(cards):
        card(s, Inches(0.72 + i * 3.99), Inches(5.15), Inches(3.71), Inches(1.6), label, body, color, body_size=12)


def draw_power_platform(s):
    parts = [("Copilot Studio", "Agents AND workflows, in one designer at copilotstudio.microsoft.com.", VIOLET, "Every lab"),
             ("Power Automate", "The connector engine underneath every workflow step — you never open it directly.", BLUE, "Labs 1–4, 10–16"),
             ("Dataverse", "The managed data store behind the environment; agents and workflows live in it.", TEAL, "Lab 0"),
             ("Connectors", "Outlook, Forms, Excel, SharePoint, Teams, Approvals, HTTP — 1,000+.", GREEN, "Every lab")]
    for i, (label, body, color, where) in enumerate(parts):
        x = Inches(0.72 + i * 3.0)
        card(s, x, Inches(1.75), Inches(2.72), Inches(2.5), label, body, color, i + 1, 11, 14)
        chip(s, x + Inches(0.28), Inches(3.78), Inches(1.7), Inches(0.34), where, color)
    note(s, 4.5, "THE ENVIRONMENT IS THE CONTAINER",
         "Workflows, agents and data all live inside one Power Platform environment. You build in the Training Class Sandbox assigned to your class — with Dataverse and Copilot Credits. "
         "Build in the Default environment and the first Agent node fails with InsufficientMcsCredits.", BLUE, 1.3)
    lab_banner(s, "lab_0")


def draw_new_home(s):
    lead(s, "copilotstudio.microsoft.com — the New experience toggle (top right) switches the whole product to the GitHub Copilot harness.")
    img = ASSETS / "ui_workflow_canvas.png"
    box(s, Inches(0.72), Inches(2.15), Inches(6.4), Inches(3.75), LIGHT, LINE)
    if img.exists():
        pic_fit(s, img, Inches(0.82), Inches(2.25), Inches(6.2), Inches(3.55))
    items = [("Home", "A natural-language box: describe the process and Copilot Studio proposes an agent, a workflow, or both (Steps and Artifacts panel).", BLUE),
             ("Agents", "New agent → the designer with Build / Preview / Evaluate / Monitor tabs.", VIOLET),
             ("Workflows", "New workflow → the canvas with a Start node and Add a step. Columns: Name · Status · Owner · Enabled.", TEAL),
             ("Other ways to build", "The standard harness (topics, agent flows) is still there — we do not use it in this course.", GREY)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(7.35), Inches(2.15 + i * 0.95), Inches(5.22), Inches(0.87), label, body, color, body_size=9, label_size=11, compact=True)
    takeaway(s, 6.12, "Environment name bottom-left. Check it before every build: your Training Class environment.", RED)


def draw_harnesses(s):
    lead(s, "\"The harness sits between the AI model and the agent or workflow you build\" — you choose one per agent, and cannot convert later.")
    rows = [("Best for", "Complex, multi-step business processes", "Rule-based agents, structured conversations", "Extending Microsoft 365 Copilot Chat"),
            ("How it works", "Reasons through a goal step by step; retries, finds alternative paths", "Follows the topics and rules you define", "Connects enterprise knowledge to Copilot Chat"),
            ("Files", "Creates and edits Word, Excel, PowerPoint, PDF in a sandbox", "Not a focus", "Not a focus"),
            ("Skills & memory", "Yes", "Not a focus", "Not a focus"),
            ("Automation", "Workflows (visual canvas, agent nodes)", "Agent flows (Power Automate designer)", "—"),
            ("Billing", "Copilot Credits — usage-based, from the moment you build", "Fixed rate card; M365 Copilot fair use", "Consumption or M365 Copilot licence")]
    table(s, 2.2, ["", "GitHub Copilot harness (GA 3 Aug 2026)", "Standard harness", "Copilot chat harness"], rows, [2.0, 3.85, 3.2, 2.8], row_h=0.56, size=10.5, head_size=11)
    takeaway(s, 6.12, "This course: every agent and workflow uses the GitHub Copilot harness — the \"new experience\".", VIOLET)


def draw_vocabulary(s):
    lead(s, "If you learned Copilot Studio before 2026, translate as you go.")
    rows = [("Topics, triggers, branching nodes", "Instructions — natural language, always-on enhanced orchestration"),
            ("Agent flows (Power Automate designer)", "Workflows — Start node, Add a step, node-level Test"),
            ("Prompts (Prompt builder)", "Inline Agent node in a workflow, or a skill in an agent"),
            ("Child agents", "Connected agents"),
            ("Actions / plugins", "Tools = Connectors, MCP servers, Workflows"),
            ("Overview / Settings pages", "Build · Preview · Evaluate · Monitor tabs"),
            ("Test pane", "Preview tab with End user preview toggle and the reasoning card"),
            ("Messages / capacity", "Copilot Credits")]
    table(s, 2.15, ["Standard harness (classic)", "GitHub Copilot harness (new experience)"], rows, [5.0, 6.85], row_h=0.5, size=11)


def draw_workflow_anatomy(s):
    flow(s, 1.95, ["START\nthe trigger", "STEP\ndo the work", "STEP\ndecide or wait", "END / RESPOND\nnotify or return"], ["outputs", "outputs", "outputs"], [BLUE, TEAL, VIOLET, AMBER], height=1.3, size=13)
    lead(s, "Click the Start node to choose the trigger type. Every workflow in every lab is this shape.", 3.55, 14)
    rows = [("Manual", "A person runs it on demand; you define typed inputs", "Lab 10 (Topic)"),
            ("Recurrence", "A schedule — set the time zone or it runs on UTC", "Reference"),
            ("Connector", "An event in a system: new Forms response, new email, new SharePoint item", "Labs 1–4"),
            ("HTTP request", "When a HTTP request is received — a website or app calls in with JSON", "Labs 12–16"),
            ("When an agent calls the flow", "An agent decides to use this workflow as a tool", "Labs 6, 11")]
    table(s, 4.05, ["Start node trigger type", "What starts the run", "Where"], rows, [3.2, 6.35, 2.3], row_h=0.44, head_h=0.42, size=11)


def draw_add_step(s):
    lead(s, "The + after any node opens the Add panel. Everything you can put on the canvas is one of these.")
    items = [("Agent", "An inline or existing agent — the model, inside the workflow", VIOLET), ("Classify", "Sort text into categories; each becomes an output port", VIOLET),
             ("M365 Copilot", "Send a prompt to Microsoft 365 Copilot or one of its agents", VIOLET), ("Human review", "Request for information — pause for a person (Teams / Outlook)", RED),
             ("Connector", "Any of 1,000+ connector actions: Outlook, Excel, SharePoint, Teams, HTTP", BLUE), ("Function", "Data Operations (Compose, Parse JSON, Select), text, date/time", TEAL),
             ("Variable", "Initialize, Set, Append — a named value that changes during the run", TEAL), ("If/Else", "One condition, two branches", AMBER),
             ("Switch", "One value, many cases plus a default", AMBER), ("Loop", "For each item in an array; Do until", AMBER),
             ("Respond to the agent", "Return outputs to the calling agent (tool workflows)", GREEN), ("End", "Stop the run; send the HTTP Response", GREEN)]
    for i, (label, body, color) in enumerate(items):
        row, col = divmod(i, 4)
        x = Inches(0.72 + col * 3.0)
        y = Inches(2.2 + row * 1.5)
        card(s, x, y, Inches(2.72), Inches(1.35), label, body, color, body_size=10, label_size=13)


def draw_trigger_types(s):
    lead(s, "Four trigger families. The one you choose is a statement about who or what is allowed to start the process.")
    trig = [("Manual", "A person presses Run", "Typed inputs on the Start node;\nTest → Enter manual trigger inputs", BLUE),
            ("Scheduled", "A clock reaches a time", "Recurrence — the schedule starts\nwhen you publish", TEAL),
            ("Automated", "An event happens\nin a system", "New form response · new email ·\nnew SharePoint item · new file", VIOLET),
            ("Request", "Something calls in\nfrom outside", "When a HTTP request is received ·\nWhen an agent calls the flow", GREEN)]
    for i, (label, when, examples, color) in enumerate(trig):
        x = Inches(0.72 + i * 3.0)
        box(s, x, Inches(2.2), Inches(2.72), Inches(2.85), WHITE, color, line_w=1.8)
        rect(s, x, Inches(2.2), Inches(2.72), Inches(0.5), color)
        text(s, x, Inches(2.2), Inches(2.72), Inches(0.5), label, 15, WHITE, True, PP_ALIGN.CENTER)
        text(s, x + Inches(0.18), Inches(2.8), Inches(2.36), Inches(0.7), when, 13, INK, True, PP_ALIGN.CENTER)
        text(s, x + Inches(0.18), Inches(3.55), Inches(2.36), Inches(1.4), examples, 10, GREY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
    rows = [("Connector — When a new response is submitted (Forms)", "Labs 1, 2, 3", "A business event starts the process"),
            ("Connector — When a new email arrives (V3) (Outlook)", "Lab 4", "The inbox is the queue"),
            ("HTTP request — When a HTTP request is received", "Labs 12–16", "A website posts JSON and waits for JSON back"),
            ("When an agent calls the flow", "Labs 6, 11", "A conversation decides to call a tool")]
    table(s, 5.2, ["Trigger used in this course", "Where", "What it means"], rows, [5.4, 2.0, 4.45], row_h=0.36, head_h=0.36, size=10)


def draw_action_families(s):
    lead(s, "A step either moves data, decides something, waits for a person, calls the model, or reaches outside the workflow.")
    fams = [("Data — Function", "Compose · Parse JSON · Select ·\nFilter array · Join · expressions", "Shape and normalise values before anything trusts them.", BLUE),
            ("Connector actions", "Send an email (V2) · Add a row into a table ·\nCreate item · Post message in a chat or channel", "Do the real work in a business system.", TEAL),
            ("Control", "If/Else · Switch · Loop ·\nVariable · End", "Decide which path the run takes.", AMBER),
            ("Human in the loop", "Human review (Request for information) ·\nApprovals: Start and wait for an approval", "Suspend the run until a person responds.", RED),
            ("AI", "Agent node · Classify · M365 Copilot ·\nstructured output", "Let the model decide, inside a workflow that does not.", VIOLET),
            ("Integration", "HTTP · Response / End · Respond to the agent ·\nchild workflows", "Reach outside the platform, or answer the caller.", GREEN)]
    for i, (label, examples, why, color) in enumerate(fams):
        row, col = divmod(i, 3)
        x = Inches(0.72 + col * 3.99)
        y = Inches(2.15 + row * 2.1)
        box(s, x, y, Inches(3.71), Inches(1.95), LIGHT, LINE)
        rect(s, x, y, Inches(0.09), Inches(1.95), color)
        text(s, x + Inches(0.26), y + Inches(0.08), Inches(3.3), Inches(0.36), label, 14, color, True)
        text(s, x + Inches(0.26), y + Inches(0.48), Inches(3.3), Inches(0.75), examples, 10, INK, anchor=MSO_ANCHOR.TOP)
        text(s, x + Inches(0.26), y + Inches(1.3), Inches(3.3), Inches(0.6), why, 10, GREY, anchor=MSO_ANCHOR.TOP)
    takeaway(s, 6.28, "You will use every one of these families by the end of Lab 16.", AMBER)


def draw_connections(s):
    lead(s, "A connector action runs as somebody. The connection is that somebody — and it is created once, then reused.")
    flow(s, 2.34, ["Add a connector\nstep", "Connection row\nshows no tick", "Create new\nconnection", "Sign in as the\ncourse account", "Green tick —\nstep can run"],
         ["first time", "", "OAuth", ""], [BLUE, RED, AMBER, VIOLET, GREEN], height=1.2, size=12)
    items = [("Per connector, per user", "Outlook, Excel Online (Business), SharePoint, Teams, Forms and Approvals each need their own connection.", BLUE),
             ("Whose mailbox?", "Send an email (V2) sends from the connection's account. In class that is your training account.", TEAL),
             ("Tenant boundary", "Human review and Approvals can only be assigned to people in the tenant — external addresses fail at run time.", RED),
             ("Publish installs them", "Run flow test saves, publishes and installs connections before it triggers.", GREEN)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.75 + row * 1.55), Inches(5.8), Inches(1.4), label, body, color, body_size=11, label_size=13)


def draw_dynamic_content(s):
    flow(s, 1.95, ["Trigger runs", "Outputs exist", "Later step\nreferences them", "Value arrives\nat run time"], ["produces", "⚡ picker", "resolved"], [BLUE, BLUE, TEAL, GREEN], height=1.15, size=13)
    head_panel(s, 0.72, 3.4, 5.8, 2.05, "✓  INSERTED WITH THE ⚡ PICKER (or / command)",
               ["Renders as a coloured token in the field", "Resolves at run time to what the earlier step produced", "The picker shows sample values from the last completed run"], GREEN, 11)
    head_panel(s, 6.77, 3.4, 5.8, 2.05, "✗  TYPED BY HAND, OR PASTED @{...}",
               ["Stays dead text — the run is green, the value arrives empty", "A reference to nothing resolves to empty, not to an error", "Rich-text boxes mangle pasted expressions"], RED, 11)
    takeaway(s, 5.6, "Typed expressions belong in the </> expression editor (concat, formatDateTime, utcNow) — never in a rich-text Instructions box.", AMBER)
    lab_banner(s, "lab_1", 6.3)


def draw_activity(s):
    lead(s, "Two ways to test, and one honest record. Every lab is verified from Activity, not from the chat window.")
    rows = [("A single node in isolation", "Test this node — the Test tab in the node's side panel; Load values from previous run", "Runs the node against the connector's API"),
            ("The full workflow", "Run flow test — the play button top right; saves, publishes, installs connections", "Manual/HTTP → enter inputs; connector → Waiting for trigger…"),
            ("What happened", "Activity panel — Running · Waiting · Succeeded · Failed · Canceled; open a run, expand each node", "Inputs and Outputs per node; the reasoning of every AI node")]
    table(s, 2.15, ["What you want to verify", "How", "What you see"], rows, [2.7, 5.4, 3.75], row_h=0.78, size=10.5)
    note(s, 4.95, "THE THREE STATES THAT LOOK ALIKE",
         "Succeeded with the right data  ·  Succeeded with empty data  ·  Still Running because it is waiting for a person.\n"
         "Only the first is done. The second is the dangerous one — read the upstream node's Outputs, not the failing node's error.", RED, 1.05)
    lab_banner(s, "lab_2", 6.1)


def draw_commit_order(s):
    lead(s, "The order of two steps is a business decision, not a technical one.")
    head_panel(s, 0.72, 2.2, 5.8, 2.4, "LOG, THEN CONFIRM  ✓", ["Add a row into a table (Excel)", "then Send an email (V2)", "If the email fails, the enquiry is still on the register and someone can chase it"], GREEN, 11)
    head_panel(s, 6.77, 2.2, 5.8, 2.4, "CONFIRM, THEN LOG  ✗", ["Send an email (V2)", "then Add a row into a table", "If the row fails, you have promised a reply that nobody can see — the evidence is gone"], RED, 11)
    takeaway(s, 4.9, "Commit the record of the obligation before you create the obligation. This is Lab 2 in one sentence.")
    text(s, Inches(0.72), Inches(5.6), Inches(11.85), Inches(0.4), "Same rule on Day 2: Lab 12 writes the Onboarding Log before the email; Lab 14 logs the draft before the Human review gate.", 12, GREY, align=PP_ALIGN.CENTER)
    lab_banner(s, "lab_2", 6.08)


def draw_credits(s):
    lead(s, "\"Billing starts when you start building.\" Copilot Credits cover LLM tokens, tools (including knowledge and MCP) and the harness itself.")
    rows = [("GitHub Copilot harness agents", "No", "Billed for all usage — build, Preview, Evaluate, run"),
            ("Workflows", "Only inside a standard-harness agent, licensed user", "All other cases — every action consumes capacity"),
            ("Standard harness agents", "Yes, in Microsoft 365 channels", "No M365 Copilot licence, or a channel outside M365"),
            ("Computer use (CUA)", "No", "All usage")]
    table(s, 2.2, ["Feature", "Covered by an M365 Copilot licence?", "When Copilot Credits are billed"], rows, [3.4, 4.0, 4.45], row_h=0.5, size=10.5)
    items = [("1 Sep 2026", "Developer and trial environments moved to usage-based billing. Our class Sandbox environments are billed per run.", RED),
             ("Where to look", "Agent → Monitor tab; PPAC → Licensing → Copilot Studio → Manage Agents; Copilot Credits estimator.", BLUE),
             ("Zero credits = every reply fails", "\"You need credits to continue … Error code: EnforcementUsageCredits\" in Preview, the demo website and every Agent/Classify/Copilot node. Build and Publish still work; allocate credits in PPAC first.", RED)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(4.85), Inches(3.71), Inches(1.9), label, body, color, body_size=10.5, label_size=13)


def draw_timeline(s):
    lead(s, "2026 in five words: harness, skills, memory, workflows, governance. One line per month.")
    rows = [("Jan", "Evaluation enhancements; activity maps; CSV test-set template; Copilot Studio extension for VS Code (GA)"),
            ("Feb", "Ticket-based Graph connectors; Claude models per prompt in Prompt builder"),
            ("Mar", "Agent node in flows; agent evaluations GA + multi-turn tests; Work IQ tools (preview); Claude Sonnet 4.6 / Opus GA"),
            ("Apr", "Agent-to-agent (A2A) protocol GA; evaluations via REST API; agent usage estimator; GPT-5.5 Reasoning (Deep)"),
            ("May", "Computer use GA; Prompt node and Microsoft 365 Copilot node in workflows; Entra Agent IDs (preview); agent inventory schema"),
            ("Jun", "The new experience (GitHub Copilot harness) production-ready preview; Skills; Memory; connected agents; Claude Sonnet 5 / GPT-5.5 Chat GA"),
            ("Jul", "Entra Agent ID automatic for every agent; workflows and MCP servers as tools; files in and files out (preview)"),
            ("Aug", "GitHub Copilot harness GA (3 Aug); Skills GA; September billing change announced for developer and trial environments")]
    table(s, 2.15, ["2026", "What shipped"], rows, [1.1, 10.75], row_h=0.44, size=10.5)
    takeaway(s, 6.28, "Trajectory: topics (2024) → generative orchestration + agent flows (2025) → harness choice, skills, memory, workflows, connected agents (2026).", BLUE)


def draw_nl_authoring(s):
    lead(s, "Natural-language authoring (preview): describe the process on the Home page and Copilot Studio proposes the artefacts.")
    flow(s, 2.3, ["Home → type the\nprocess", "Workflow or\nConversational agent chip", "Clarifying\nquestions", "Steps and\nArtifacts panel", "Edit each card\nin the canvas"], ["submit", "", "", "cards"], [BLUE, TEAL, VIOLET, AMBER, GREEN], height=1.1, size=10.5)
    items = [("What it decides", "A deterministic workflow, a conversational agent, or a combination of both — it may ask you to configure a connection (e.g. email).", BLUE),
             ("Then the same loop", "Preview to chat, Build to edit instructions, Save; the next turn picks up the change. Chat history is kept 28 days.", VIOLET),
             ("Models and credits", "May use Anthropic models if your admin allows external models; every generation consumes Copilot Credits.", AMBER),
             ("In this course", "We build by hand so you can name every node. Try it on Day 2: paste a lab scenario and compare what it proposes with what you built.", GREEN)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.7 + row * 1.5), Inches(5.8), Inches(1.38), label, body, color, body_size=10.5, label_size=13)


def draw_ppac(s):
    lead(s, "What the admin set up in the Power Platform admin center (PPAC) before class — and why each setting matters.")
    items = [("Class environment", "One Training Class Sandbox per cohort, with Dataverse. Reset between classes. Never the Default environment.", BLUE),
             ("Copilot Credits allocation", "Licensing → Copilot Studio → Manage Copilot Credits → this environment; Draw from the available capacity in my tenant.", TEAL),
             ("Agent limits", "Manage Agents → Set limit → monthly limit, notification threshold, Stop usage toggle.", AMBER),
             ("External models", "Turn on external models (Anthropic, Mistral, xAI) + M365 admin consent — needed for Claude Opus 5.", VIOLET),
             ("Preview / cross-region", "Preview and experimental AI models; Move data across regions (Singapore models are cross-geo).", GREEN),
             ("Entra Agent ID", "Automatic for every agent since July 2026 — Conditional Access and DLP per agent; Harness column in Manage → Copilot Studio.", RED)]
    tile_grid(s, items, cols=2, y0=2.15, area_h=4.6, size=13)


# ===========================================================================
# MODULE 2 — CONTROL FLOW AND HUMAN IN THE LOOP
# ===========================================================================
def draw_ifelse(s):
    lead(s, "An If/Else node evaluates one condition row: a left value, an operator, and a right value.")
    for i, (label, body, color) in enumerate([("LEFT VALUE", "A ⚡ token from an earlier node\ne.g. Outcome (Human review)", BLUE),
                                              ("OPERATOR", "Equals · Not equals · Contains ·\nGreater than · Less than · Is empty", VIOLET),
                                              ("RIGHT VALUE", "A literal you type\ne.g. Yes  ·  Approve  ·  Priority", TEAL)]):
        x = Inches(0.72 + i * 3.99)
        box(s, x, Inches(2.2), Inches(3.71), Inches(1.5), WHITE, color, line_w=1.8)
        text(s, x + Inches(0.2), Inches(2.28), Inches(3.3), Inches(0.34), label, 12, color, True)
        text(s, x + Inches(0.2), Inches(2.64), Inches(3.3), Inches(1.0), body, 11, GREY, anchor=MSO_ANCHOR.TOP)
    box(s, Inches(4.9), Inches(3.95), Inches(3.5), Inches(0.72), LIGHT, VIOLET, line_w=1.8)
    text(s, Inches(4.9), Inches(3.95), Inches(3.5), Inches(0.72), "Outcome  Equals  Yes", 14, INK, True, PP_ALIGN.CENTER)
    arrow(s, Inches(3.4), Inches(4.8), Inches(0.34), Inches(0.36), GREEN, "down")
    arrow(s, Inches(9.55), Inches(4.8), Inches(0.34), Inches(0.36), RED, "down")
    head_panel(s, 1.2, 5.25, 4.6, 1.0, "IF — condition true", ["Reply to the email with the approved draft"], GREEN, 11, 0.4)
    head_panel(s, 7.5, 5.25, 4.6, 1.0, "ELSE — condition false", ["Send the hand-over email to the trainer — never fall silent"], RED, 11, 0.4)
    text(s, Inches(0.72), Inches(6.4), Inches(11.85), Inches(0.4), "Lab 3: Outcome Equals Approve (Approvals connector).  Labs 4 and 14: Outcome Equals Yes (Human review — it publishes the string Yes, not a boolean).", 11, GREY, align=PP_ALIGN.CENTER)


def draw_conditions(s):
    lead(s, "Both branches must be built — including the one you hope never runs. Add rows for AND / OR groups.")
    items = [("Empty Else is a silent failure", "A rejected leave request that triggers nothing is an applicant waiting forever. Route every Else to a message or a named person.", RED),
             ("The picker's type can lie", "Human review's Yes/No input shows as boolean but publishes the string Yes. Read the node's real Outputs in Activity.", AMBER),
             ("Re-pick after rebuilding an input", "Delete and re-create an input and the old token renders fine but resolves to empty — every run falls to Else.", VIOLET),
             ("Test both paths", "Lab 3 tests an approval and a rejection; Lab 4 sends one email per category; Lab 14 approves one draft and rejects one.", GREEN)]
    tile_grid(s, items, cols=2, y0=2.15, area_h=3.7, size=13)
    lab_banner(s, "lab_3", 6.08)


def draw_compose(s):
    lead(s, "Compose is a named value holder: it takes any input, and its Outputs token is what every later step references.")
    flow(s, 2.3, ["Trigger body\n(raw)", "Compose\nNormalise", "Outputs\n⚡ token", "Agent node · Excel ·\nSharePoint"], ["", "", "reference"], [BLUE, TEAL, TEAL, VIOLET], height=1.0, size=12)
    items = [("Normalise input", "toUpper(trim(triggerBody()?['nric'])) — one canonical form before the lookup and the record.", BLUE),
             ("Build a prompt", "Assemble the retrieved brochure text and the visitor's question into one block for the Agent node (Lab 16).", VIOLET),
             ("Hold a computed value", "concat('REQ-', formatDateTime(utcNow(),'yyyyMMdd'), '-', …) — generated once, used by Excel and the reply (Lab 6).", TEAL),
             ("Variable vs Compose", "Initialize / Set / Append variable when the value changes during the run (loops, counters). Compose when it is written once.", AMBER)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.6 + row * 1.42), Inches(5.8), Inches(1.3), label, body, color, body_size=10.5, label_size=13)
    takeaway(s, 6.28, "Function → Data Operations → Compose. Rename the node with one word (no spaces) so its token stays readable.", TEAL)


def draw_switch_loop(s):
    lead(s, "When one condition is not enough: Switch for many cases, Loop for many items.")
    head_panel(s, 0.72, 2.2, 5.8, 2.9, "SWITCH — one value, many branches",
               ["On: a ⚡ token (e.g. Leave Type, category)", "Case Annual · Case Medical · Case Unpaid · Default", "Each case is its own branch of steps", "Default catches what you did not foresee"], AMBER, 11)
    head_panel(s, 6.77, 2.2, 5.8, 2.9, "LOOP — repeat over a list",
               ["For each: every item in an array (Get items rows, attachments)", "Do until: repeat until a condition is true", "Steps inside see the current item token", "Arrays need join() before they reach Excel or a text field"], VIOLET, 11)
    takeaway(s, 5.35, "Lab 4 uses the Classify node's ports instead of a Switch — the category is a port, not a value you compare.")
    text(s, Inches(0.72), Inches(6.1), Inches(11.85), Inches(0.5), "Keep branches short. A branch that grows past four steps is usually a child workflow waiting to be extracted.", 12, GREY, align=PP_ALIGN.CENTER)


def draw_hitl_concept(s):
    lead(s, "Three arrangements that people use interchangeably, and that are not the same thing.")
    rows = [("Human IN the loop", "AI proposes, human decides", "Human authorises, system acts", "NO — it blocks"),
            ("Human ON the loop", "AI decides and acts", "Human monitors, can intervene", "Yes — after the fact"),
            ("Human OUT of the loop", "AI decides and acts", "AI acts", "Yes — nobody checks")]
    table(s, 2.15, ["Pattern", "Who decides", "Who acts", "Can AI proceed alone?"], rows, [3.1, 2.9, 3.15, 2.7], [RED, AMBER, GREY], row_h=0.66, size=12)
    note(s, 4.85, "WHERE THIS COURSE PUTS THE HUMAN",
         "IN the loop: Lab 3 (a manager approves leave), Lab 4 (Priority emails stop in Teams), Lab 14 (an adviser approves a draft), Lab 9 (the manager agent shows the final draft).\n"
         "OUT of the loop on purpose: Labs 12, 13, 15 and 16 — so you can see what that costs. The pause IS the deliverable.", RED, 1.15)
    lab_banner(s, "lab_3", 6.1)


def draw_hitl_channels(s):
    lead(s, "The Human review node has a Channel dropdown: Teams or Outlook. Where the request lands decides whether it is ever answered.")
    head_panel(s, 0.72, 2.2, 5.8, 2.75, "TEAMS — the Workflows bot chat",
               ["An adaptive card: Request information | Microsoft Copilot Studio", "Approver answers inline; the run resumes in a minute or two", "Verified reliable on our tenant — the default for Labs 4 and 14", "Best when the approver lives in Teams all day"], TEAL, 10.5)
    head_panel(s, 6.77, 2.2, 5.8, 2.75, "OUTLOOK / EMAIL",
               ["Request for information arrives as an actionable email with a form and Submit", "The docs describe RFI as Outlook-delivered; on our tenant the mail never arrived", "Approvals connector (classic): email + Teams Approvals app, Approve/Reject buttons", "Best for approvers outside Teams, or a formal audit trail by mail"], AMBER, 10.5)
    rows = [("Human review node — Channel: Teams", "Labs 4, 14", "Inputs you define (Outcome Yes/No, Name); first responder wins"),
            ("Approvals — Start and wait for an approval", "Lab 3", "Approve/Reject – First to respond; Outcome, Responses Comments"),
            ("Request human assistance when unsure (Agent node)", "Never as a gate", "Fires only if the model feels unsure — not a control")]
    table(s, 5.15, ["Mechanism", "Where", "What comes back"], rows, [4.4, 1.9, 5.55], row_h=0.42, head_h=0.4, size=10)


def draw_human_review_node(s):
    lead(s, "Add a step → Human review → Request for information. It does nothing at all except wait.")
    items = [("Title · Message · Assigned to", "Message = ⚡ the agent's summary or draft. Assigned to = a tenant user; type, wait for the directory lookup, click the suggestion.", BLUE),
             ("Inputs are mandatory", "Add an input: Text · Yes/No · Email · Number · Date. Define Outcome (Yes/No) and Name (Text), no defaults, no spaces in names.", VIOLET),
             ("What it publishes", "Only the inputs you defined, plus responderObjectId. There is no built-in outcome property — a hand-typed reference silently never matches.", AMBER),
             ("Then If/Else", "Outcome (⚡) Equals Yes. The Yes/No input publishes the string Yes, so compare against Yes, not true.", TEAL)]
    tile_grid(s, items, cols=2, y0=2.15, area_h=3.1, size=12)
    note(s, 5.4, "THE TEST OF A REAL GATE",
         "Submit, then open Activity. The run says Running — and it will still say Running tomorrow. Nothing times out, nothing defaults, nothing proceeds until a person answers.", RED, 0.9)
    lab_banner(s, "lab_4", 6.35)


def draw_control_vs_not(s):
    lead(s, "Three things in the designer look like \"a human checks\". Only one of them is a control.")
    rows = [("Human review (node)", "A gate in the workflow", "Always", "Outcome + responder ID recorded", "YES"),
            ("Request human assistance when unsure (Agent node toggle)", "The agent emailing the connection owner", "Only if the model feels unsure", "None", "NO"),
            ("Request information (agent tool)", "Same, exposed as a tool the agent may call", "When the agent decides", "None", "NO")]
    table(s, 2.15, ["Mechanism", "What it is", "Fires when", "Audit trail", "Control?"], rows, [3.6, 3.0, 2.3, 1.95, 1.0], [GREEN, RED, RED], row_h=0.68, size=10.5)
    takeaway(s, 4.75, "The toggle and the tool both let a confidently wrong output through untouched — which is the failure that matters.", RED)
    note(s, 5.55, "DEFAULT VALUES ARE A DESIGN DECISION",
         "Pre-filling Outcome with Yes turns the gate into a rubber stamp: confirming takes no thought, rejecting takes noticing. Leave it blank; if a default is forced, fail safe.", AMBER, 0.95)


def draw_approval_mechanics(s):
    flow(s, 1.95, ["Form\nsubmitted", "Start and wait\nfor an approval", "The run\nSUSPENDS", "Manager responds\n(Teams / email)", "If/Else reads\nthe Outcome"], ["action", "pause", "decision", "resume"], [BLUE, RED, RED, VIOLET, TEAL], height=1.3, size=12)
    head_panel(s, 0.72, 3.6, 5.8, 1.5, "OUTCOME = APPROVE", ["Send the approval email with the manager's Responses Comments; log the decision"], GREEN, 11, 0.42)
    head_panel(s, 6.77, 3.6, 5.8, 1.5, "OUTCOME = REJECT (Else)", ["Send the rejection with the comments — routed to the applicant, never to silence"], RED, 11, 0.42)
    note(s, 5.3, "APPROVALS CONNECTOR SETTINGS THAT MATTER",
         "Approval type: Approve/Reject – First to respond. Title with the ⚡ Name token. Assigned to: click the resolved suggestion (a typed-and-tabbed address fails at run time). Details: labelled lines with ⚡ tokens.", BLUE, 0.85)
    lab_banner(s, "lab_3", 6.25)


def draw_classify(s):
    lead(s, "The Classify node is a native AI step: it reads text and routes the run out of the port that matches.")
    head_panel(s, 0.72, 2.2, 5.8, 3.0, "CONFIGURE",
               ["Model picker (Claude Sonnet 4.6 is the cheap, reliable choice)", "Instruction with ⚡ tokens: Subject, From, Body, Importance", "Categories: name + one-line description; Add more categories", "Add example per category to sharpen the boundary", "Built-in Other — the fail-safe when nothing fits"], VIOLET, 10.5)
    head_panel(s, 6.77, 2.2, 5.8, 3.0, "WHAT COMES OUT",
               ["One output port per category — connect a handler to each", "The chosen category and the model's reasoning appear in run details", "Ambiguous text should land in Other, not be forced into a category", "Downstream nodes see the trigger's tokens as they flow through"], TEAL, 10.5)
    takeaway(s, 5.45, "Five categories in Lab 4: Meeting · Need Reply · Priority · Informational · Other. Every port does something visible so a test can prove which path ran.", VIOLET)
    lab_banner(s, "lab_4", 6.2)


def draw_email_architecture(s):
    lead(s, "Lab 4 on one slide: an Outlook trigger, one Classify node, five ports, and a human on the Priority path.")
    flow(s, 2.15, ["When a new email\narrives (V3)", "Classify\n5 categories"], [""], [BLUE, VIOLET], x0=0.72, total=4.2, height=1.0, size=11)
    ports = [("Meeting", "Agent extracts title/start/end → Create event → acknowledge", VIOLET),
             ("Need Reply", "Agent drafts → Reply to email (V3)", TEAL),
             ("Priority", "Agent summarises → Human review (Teams) → If Outcome Equals Yes → reply, else hand over", RED),
             ("Informational", "Flag email (V2)", BLUE),
             ("Other", "Move email (V2) to folder Other", GREY)]
    for i, (label, body, color) in enumerate(ports):
        y = Inches(2.2 + i * 0.8)
        arrow(s, Inches(5.1), y + Inches(0.2), Inches(0.28), Inches(0.34), color)
        box(s, Inches(5.5), y, Inches(7.07), Inches(0.72), LIGHT, color, line_w=1.6)
        text(s, Inches(5.65), y, Inches(1.5), Inches(0.72), label, 12, color, True)
        text(s, Inches(7.15), y, Inches(5.35), Inches(0.72), body, 10.5, GREY)
    takeaway(s, 6.26, "Test with five emails, one per category. The Priority case proves the gate: the run waits in Teams until you answer.", RED)


def draw_autonomous(s):
    lead(s, "An autonomous business process = an event trigger + deterministic steps + AI judgement steps + a human checkpoint where it matters.")
    flow(s, 2.34, ["Event\ntrigger", "Normalise\n(Compose)", "Agent node\njudgement", "Human review\ncheckpoint", "Act across\nsystems", "Notify"], ["", "", "structured", "if needed", ""], [BLUE, TEAL, VIOLET, RED, GREEN, AMBER], height=1.2, size=11)
    items = [("Workflows absorbed AI in 2026", "Agent node (Mar), Prompt and M365 Copilot nodes (May), workflows as agent tools (Jul), the GitHub Copilot harness GA (3 Aug).", VIOLET),
             ("Deterministic backbone", "The same input always produces the same path — consistent execution, end-to-end visibility in Activity.", BLUE),
             ("Two directions", "A workflow can call an agent (Agent node — Lab 10); an agent can call a workflow as a tool (When an agent calls the flow — Lab 11).", TEAL),
             ("Recovery", "The harness retries and finds alternative paths inside an agent step; the workflow around it still fails loudly at a named node.", GREEN)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.75 + row * 1.5), Inches(5.8), Inches(1.38), label, body, color, body_size=10.5, label_size=13)


# ===========================================================================
# MODULE 3 — COPILOT STUDIO AGENTS (part A: designer, instructions, model,
# knowledge, skills, tools, enforcement)
# ===========================================================================
def draw_workflow_vs_agent(s):
    head_panel(s, 0.72, 1.8, 5.8, 3.9, "WORKFLOW — deterministic",
               ["You decide the path in advance", "The same input always gives the same output", "It can only do what you built", "It fails loudly, at a named node", "You test it by checking the result"], BLUE, 12)
    head_panel(s, 6.77, 1.8, 5.8, 3.9, "AGENT — the harness reasons",
               ["It chooses the path at run time", "The same input may give a different answer", "It combines what it was given in new ways", "It fails quietly, with a confident wrong answer", "You test it by trying to break it"], VIOLET, 12)
    takeaway(s, 5.9, "Use a workflow where the rule is known. Use an agent where the language varies. Most real systems need both.", VIOLET)
    text(s, Inches(0.72), Inches(6.55), Inches(11.85), Inches(0.32), "Labs 1–4 are workflows with AI nodes. Labs 5–9 are agents. Labs 10–16 are both, and the seam between them is the lesson.", 11, GREY, align=PP_ALIGN.CENTER)


def draw_designer(s):
    lead(s, "New agent opens one page. Top bar: name · Build | Preview | Evaluate | Monitor · Save · Share · Settings · … · Publish.")
    img = ASSETS / "ui_agent_designer.png"
    box(s, Inches(0.72), Inches(2.15), Inches(11.85), Inches(2.3), LIGHT, LINE)
    if img.exists():
        pic_fit(s, img, Inches(0.82), Inches(2.22), Inches(11.65), Inches(2.16))
    tabs = [("Build", "Identity, Instructions, Model, Channels, Skills, Tools, Knowledge, Connected agents, Memory", BLUE),
            ("Preview", "Chat with the latest saved draft; End user preview toggle; reasoning card and activity trace", VIOLET),
            ("Evaluate", "Named test sets of conversations; General quality test method; compare agent versions", AMBER),
            ("Monitor", "Recent tasks, files the agent accessed, activity — and the Copilot Credits it consumed", GREEN)]
    for i, (label, body, color) in enumerate(tabs):
        card(s, Inches(0.72 + i * 3.0), Inches(4.6), Inches(2.72), Inches(1.55), label, body, color, body_size=10, label_size=13)
    takeaway(s, 6.28, "Lifecycle: Create → Build → Test (Preview, Evaluate) → Publish → Monitor. Credits are consumed at every step after Create.", VIOLET)


def draw_build_panel(s):
    lead(s, "The Build tab: name and Instructions in the centre; the components panel on the right, top to bottom.")
    box(s, Inches(0.72), Inches(2.15), Inches(4.4), Inches(4.6), LIGHT, LINE)
    text(s, Inches(0.9), Inches(2.25), Inches(4.0), Inches(0.36), "CENTRE COLUMN", 11, VIOLET, True)
    text(s, Inches(0.9), Inches(2.65), Inches(4.05), Inches(4.0),
         "Agent icon + name box — click Untitled Agent, type, Enter.\n\nInstructions — a large rich-text box with a small toolbar. This is the ONLY place the system instructions go. Paste the whole agent/instructions.md here.\n\nThere is no separate system prompt, description or settings page for it.",
         11, GREY, anchor=MSO_ANCHOR.TOP, space=4)
    rows = [("Model", "Default Claude Opus 5; other models selectable"),
            ("Channels +", "Define where users can interact with the agent"),
            ("Skills +", "Define behaviors through structured instructions — upload SKILL.md or a .zip"),
            ("Tools +", "Connect the agent to external systems and actions — connectors, workflows, MCP"),
            ("Knowledge +", "Provide trusted context — files, SharePoint, websites; remove Search all websites ×"),
            ("Connected agents +", "Collaborate across agents to complete work"),
            ("Memory (Preview)", "Remember interactions, workflows and context — off by default")]
    table(s, 2.15, ["Right panel", "Caption in the product"], rows, [2.3, 5.05], x0=5.4, row_h=0.6, head_h=0.4, size=10.5, head_color=VIOLET)


def draw_instructions_craft(s):
    lead(s, "Instructions are prose, but they are not free text. Six things every agent instruction in this course states.")
    items = [("Role", "\"You are the HR policy assistant for Keppel Ridge.\" One identity, one line.", BLUE),
             ("Scope", "What it helps with, and the list of subjects it declines or redirects.", TEAL),
             ("Tone", "Plain professional English; short answers; no jargon the employee did not use.", VIOLET),
             ("When to ask", "Ambiguous input → one clarifying question, not a guess.", AMBER),
             ("When to use knowledge", "Answer only from the connected source; say so when the source is silent.", GREEN),
             ("When to act / escalate", "Which tool to call, and the trigger that hands the person to HR with no follow-up questions.", RED)]
    tile_grid(s, items, cols=3, y0=2.15, area_h=3.2, size=12)
    takeaway(s, 5.55, "Iterate in Preview: change one thing, Save, re-run only the failing test. The next turn picks up your change automatically.", VIOLET)
    lab_banner(s, "lab_5", 6.25)


def draw_hr_example(s):
    lead(s, "The Lab 5 HR Agent instructions, section by section — the shape you will reuse for Procurement, Sales and IT Support.")
    rows = [("Where your answers come from", "Only the HR Policies handbook attached as knowledge. Never the open web, never your own knowledge of employment law."),
            ("What you must never do", "Discuss, estimate or infer another named person's leave, pay or records. Any number about someone else is a failure."),
            ("Matters you escalate immediately", "Harassment, discrimination, grievances: give hr@keppelridge.example and ask NO follow-up questions."),
            ("Identifying who you are speaking to", "You are speaking to the signed-in employee; treat every question as about them unless told otherwise."),
            ("When you do not know", "Say the handbook does not cover it and point to HR. Never include citation markers, reference numbers or source tags."),
            ("Tone", "Warm, brief, plain English; answer first, then the one condition that applies (e.g. line-manager approval).")]
    table(s, 2.15, ["Section heading in instructions.md", "What it says"], rows, [3.9, 7.95], row_h=0.56, size=10.5, head_color=VIOLET)
    lab_banner(s, "lab_5", 6.15)


def draw_instructions_gotcha(s):
    lead(s, "The Instructions box is a rich-text editor — in the agent designer AND in the workflow Agent node.")
    head_panel(s, 0.72, 2.2, 5.8, 2.5, "DO", ["Type the prose, leave a gap, insert each value with the ⚡ picker or a / command", "Paste plain Markdown from instructions.md", "Rename nodes to one word so tokens read cleanly", "Change one thing per Preview cycle"], GREEN, 11)
    head_panel(s, 6.77, 2.2, 5.8, 2.5, "DO NOT", ["Paste @{...} or body('Node')?['x'] into the box — it escapes underscores and mangles references", "Copy a workflow and trust its Instructions tokens — they resolve to EMPTY", "Drag a node after configuring it — moving a node clears its configuration", "Assume there is a separate user-message field: there is none"], RED, 11)
    takeaway(s, 5.0, "A reference to nothing resolves to empty, not to an error. The run is green, the model received nothing.", RED)
    note(s, 5.8, "THE AGENT NODE'S CONFIGURE TAB, TOP TO BOTTOM", "Connection · Agent (model picker) · Instructions · Microsoft IQ · Tools · Knowledge · Request human assistance · Web search · Output. Output is the last field.", VIOLET, 0.95)


def draw_model(s):
    lead(s, "The Model dropdown at the top of the right panel. The default is Claude Opus 5; the choice is a design decision, per agent and per Agent node.")
    rows = [("Claude Opus 5 (default)", "Deep reasoning, long multi-step work", "Agents in Labs 5–9, 11, 17"),
            ("Claude Sonnet 5 / Sonnet 4.6", "Fast and cheaper; GA; Sonnet 5 only on the GitHub Copilot harness", "Classify and Agent nodes in Labs 4, 12–16"),
            ("GPT-5.5 Chat / GPT-5.6", "OpenAI models, GA; cross-geo for Singapore", "Alternative — re-run the tests after switching"),
            ("Fable 5 · Mistral Medium 3.5", "Experimental / preview tags", "Demo only — never in a published agent")]
    table(s, 2.15, ["Model", "Character", "Used where"], rows, [3.4, 4.75, 3.7], row_h=0.5, size=10.5, head_color=VIOLET)
    items = [("Tags", "Deep · Auto · General; release types Experimental, Preview, Generally available, Default, Retired, Cross-geo.", BLUE),
             ("Admin prerequisites", "Preview and experimental AI models; Move data across regions; Turn on external models in PPAC; provider consent (Anthropic, Mistral, xAI) in the M365 admin center.", AMBER),
             ("Same instructions, different behaviour", "A different model follows the same instructions differently. Change the model, then re-run every probe.", RED)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(4.75), Inches(3.71), Inches(2.0), label, body, color, body_size=10.5, label_size=13)


def draw_knowledge(s):
    flow(s, 1.95, ["Files · SharePoint\n· Public websites", "Knowledge + →\nAdd knowledge", "Indexed —\nwait for Ready", "Retrieved when a\nquestion matches", "Answer with\ncitations"], ["choose", "upload", "at run time", ""], [BLUE, TEAL, AMBER, VIOLET, GREEN], height=1.2, size=11)
    items = [("It is a boundary", "The agent cannot read a document you did not give it. Give it only what it needs — not the staff-leave.csv.", GREEN),
             ("Remove Search all websites ×", "On by default. A fee from the open web is indistinguishable from a fee in your own brochure.", RED),
             ("No general-knowledge toggle", "The new harness has none. Grounding rests on the instruction line: answer only from the connected source.", AMBER),
             ("Sources", "Upload file · Public websites · SharePoint · Azure AI Search · Dataverse · Dynamics 365 · Salesforce · ServiceNow · Azure SQL.", BLUE),
             ("Folder per lab", "The connector indexes at folder level: Lab 5 - HR Policies, Lab 7 - Course Brochures, Lab 13 - Investment FAQ.", TEAL),
             ("Ready means ready", "A source still indexing returns nothing; the agent looks broken when it is merely empty.", VIOLET)]
    tile_grid(s, items, cols=3, y0=3.45, area_h=2.55, size=11)
    lab_banner(s, "lab_5", 6.15)


def draw_iq_citations(s):
    lead(s, "Three layers of context beyond your files — and the citation markers grounding leaves in the reply.")
    items = [("Microsoft IQ / Work IQ (preview)", "The signed-in user's emails, calendar, files, Teams messages and people. A toggle in the Agent node and the agent designer.", BLUE),
             ("Foundry IQ (GA)", "Knowledge bases built and tuned in Microsoft Foundry, connected as a source.", TEAL),
             ("Memory (preview)", "Per-user preferences captured across chats — a different thing from knowledge (see the Memory slide).", VIOLET)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(2.15), Inches(3.71), Inches(1.9), label, body, color, i + 1, 10.5, 13)
    note(s, 4.3, "CITATION MARKERS LEAK — AND DUPLICATE THE ANSWER",
         "With a Knowledge source, replies can arrive twice: once with [doc:turn1doc11] markers, then with [1]-style ones. They are appended by the grounding layer, not written by the model.\n"
         "Add the line: \"Never include citation markers, reference numbers or source tags in your reply.\" The Pinecone flow (Lab 16) has no markers — retrieved text arrives as plain Compose output.", RED, 1.55)
    takeaway(s, 6.12, "Turn Work IQ on only for agents that should know who is asking — never for a public website agent.", AMBER)


def draw_skills(s):
    lead(s, "\"Skills are self-contained sets of instructions and logic\" — instructions on demand, packaged once, added to many agents.")
    box(s, Inches(0.72), Inches(2.15), Inches(5.3), Inches(3.7), RGBColor(0x0B, 0x12, 0x20), None)
    text(s, Inches(0.92), Inches(2.25), Inches(5.0), Inches(3.5),
         "---\nname: password-reset-procedure\ndescription: Use when a user says they are locked\n  out or asks to reset a password. Verifies identity\n  first, then walks through the reset steps.\n---\n# Password Reset Procedure\n1. Confirm the user's employee ID …\n2. Never read a password aloud …\n3. Raise a ticket with the tool …",
         10, RGBColor(0x9C, 0xDC, 0xFE), anchor=MSO_ANCHOR.TOP, space=1)
    items = [("YAML front matter", "name (lowercase, numbers, hyphens) + description. The description is the trigger — the orchestrator matches on it.", BLUE),
             ("Markdown body", "Task description, step-by-step guidance, formatting rules, edge cases, which tools to use.", TEAL),
             ("Create or upload", "Skills + → Add skill → Create from blank, or Upload a skill (a .md, or a .zip with SKILL.md at the root).", VIOLET),
             ("Not enforced", "A skill is a procedure the model decides to apply, not a permission. The security rule lives in the instructions and in the tools it lacks.", RED)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(6.25), Inches(2.15 + i * 0.95), Inches(6.32), Inches(0.87), label, body, color, body_size=9.5, label_size=11, compact=True)
    lab_banner(s, "lab_8", 6.1)


def draw_skill_package(s):
    lead(s, "A skill package is a .zip: SKILL.md is the only root-level Markdown; everything else sits in sub-folders.")
    box(s, Inches(0.72), Inches(2.15), Inches(4.4), Inches(3.75), LIGHT, LINE)
    text(s, Inches(0.92), Inches(2.25), Inches(4.1), Inches(3.55),
         "raise-requisition.zip\n├── SKILL.md\n├── manual/\n│   └── procedure.md\n├── templates/\n│   └── requisition-summary.md\n├── scripts/\n│   └── validate.py\n└── references/\n    └── purchasing-policy.md",
         11, INK, anchor=MSO_ANCHOR.TOP, space=1)
    rows = [("manual/", "Longer procedure text the skill can point to"),
            ("templates/", "Output shapes — the summary the agent must produce"),
            ("scripts/", "Deterministic code the harness may run (the BlastBox skills do all arithmetic in Python)"),
            ("references/", "Policy extracts and worked examples"),
            ("Upload", "Skills + → Add skill → Upload a skill → drag the .zip; the system validates and adds it"),
            ("Replace", "Skills → the skill → Replace — re-upload after every edit; export as .md or package to share")]
    table(s, 2.15, ["Folder / step", "What goes there"], rows, [1.7, 5.65], x0=5.4, row_h=0.58, head_h=0.4, size=10.5, head_color=VIOLET)
    takeaway(s, 6.12, "Lab 6: raise-requisition + vendor-enquiry.  Lab 7: course-enquiry + enrolment-intake.  Lab 8: five IT Support packages, uploaded in order.", VIOLET)


def draw_skills_fire(s):
    lead(s, "When does a skill fire? When the orchestrator decides the user's message matches the skill's description.")
    flow(s, 2.3, ["User message", "Orchestrator reads\nskill descriptions", "Best match\nactivated", "Skill steps\nshape the reply", "Activity trace\nshows it"], ["", "match", "", ""], [BLUE, VIOLET, VIOLET, TEAL, GREEN], height=1.0, size=11)
    items = [("Prove it", "Preview with End user preview off → open the activity trace → confirm the skill activated and which tools it called.", GREEN),
             ("If it did not fire", "Sharpen the description (\"Use when a user asks …\"), not the body. Then re-test the same message.", AMBER),
             ("Two skills that overlap", "The orchestrator picks one. Keep descriptions distinct — course-enquiry vs enrolment-intake, not two \"help with courses\".", RED),
             ("Skills vs instructions", "Instructions are always in force. A skill loads only when matched — so a rule that must always hold goes in instructions.", VIOLET)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.6 + row * 1.22), Inches(5.8), Inches(1.12), label, body, color, body_size=10, label_size=12.5)
    lab_banner(s, "lab_8")


def draw_tools(s):
    lead(s, "Tools let the agent act outside the conversation. Tools + → Add a tool → three types.")
    rows = [("Connectors", "Well-known services with pre-built actions", "Outlook Send an email, Excel Add a row, SharePoint Create item, Calendar Create event"),
            ("Workflows", "Multi-step, deterministic processes you own", "Lab 6 - Raise Requisition; Lab 11 - Blog Writer Tool"),
            ("MCP servers", "Custom or internal services exposing many tools over the Model Context Protocol", "Membership MCP, Warehouse MCP, Windows 365 for Agents MCP")]
    table(s, 2.15, ["Tool type", "Best for", "Examples"], rows, [2.2, 4.3, 5.35], [BLUE, GREEN, VIOLET], row_h=0.6, size=10.5, head_color=VIOLET)
    head_panel(s, 0.72, 4.45, 5.8, 1.5, "THE AGENT'S PART — probabilistic", ["Decides that a tool applies, fills its inputs from what the person said", "May call the wrong tool, or the right one with the wrong values"], VIOLET, 10.5, 0.42)
    head_panel(s, 6.77, 4.45, 5.8, 1.5, "THE TOOL'S PART — enforced", ["Validates, looks up, applies the threshold, writes the audit row", "Whatever the agent believed, the workflow's own logic still runs"], GREEN, 10.5, 0.42)
    lab_banner(s, "lab_6", 6.15)


def draw_workflow_as_tool(s):
    lead(s, "A workflow becomes a tool only when it starts with When an agent calls the flow and ends with Respond to the agent.")
    flow(s, 2.3, ["When an agent\ncalls the flow\n(typed inputs)", "Compose\nReference", "Add a row into\na table (Excel)", "Respond to the agent\n(Reference, Status)"], ["inputs", "", ""], [GREEN, TEAL, BLUE, GREEN], height=1.15, size=11)
    items = [("Inputs are the contract", "Add an input: Text / Number with a description the agent reads to fill the slot — \"Full name of the colleague raising the requisition\".", BLUE),
             ("Publish, then attach", "A tool must be the published version; LIVE = CURRENT DRAFT in Version history. Then Tools + → Add a tool → Workflow.", GREEN),
             ("Name and describe the tool", "The tool description is how the agent knows when to call it — write it for the model, not for a developer.", VIOLET),
             ("Verify in the trace", "Preview → ask → open the activity trace: which tool was invoked, what arguments, what it returned. Then check Excel.", TEAL)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.7 + row * 1.2), Inches(5.8), Inches(1.1), label, body, color, body_size=10, label_size=12.5)
    lab_banner(s, "lab_6")


def draw_mcp(s):
    lead(s, "Model Context Protocol: one server, many tools, one standard interface — the agent discovers the tools at run time.")
    flow(s, 2.3, ["Agent", "MCP server\n(connector)", "get_membership ·\nreissue_card · …", "System of record"], ["MCP", "tools", "read / write"], [VIOLET, BLUE, TEAL, GREEN], height=1.0, size=11)
    items = [("Add it", "Tools + → Add a tool → Model Context Protocol → search the connector → select an existing connection → Add → Save and publish.", BLUE),
             ("Per agent", "MCP connections are attached per agent and must be re-attached after a solution import — a real ALM gotcha.", AMBER),
             ("Trust", "Submit your MCP server for Microsoft certification (reliability, security, compliance). Windows 365 for Agents MCP is GA.", GREEN),
             ("In this course", "We use connectors and workflows as tools; MCP is demonstrated with the BlastBox Omega sample (four inline MCP connectors, no external servers).", VIOLET)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.65 + row * 1.5), Inches(5.8), Inches(1.38), label, body, color, body_size=10.5, label_size=13)


def draw_tools_skills_mcp(s):
    lead(s, "Three words that get mixed up. One table to keep them apart.")
    rows = [("Tool", "An action the agent can call that acts outside the conversation", "When the agent decides the action is needed and fills the inputs", "The tool's own logic — yes; the decision to call it — no", "Send an email (V2); Lab 6 - Raise Requisition"),
            ("Skill", "Instructions on demand — a SKILL.md package that changes how the agent behaves", "When the message matches the skill's description", "No — the model decides it applies", "password-reset-procedure; raise-requisition"),
            ("MCP server", "A server exposing many tools over the Model Context Protocol", "The agent discovers and calls its tools like any other tool", "The server's logic — yes; the call — no", "Membership MCP v2 with get_membership, reissue_card")]
    table(s, 2.15, ["", "What it is", "When it fires", "Enforced?", "Example"], rows, [1.4, 3.3, 2.75, 2.3, 2.1], [GREEN, VIOLET, BLUE], row_h=1.0, size=10)
    takeaway(s, 5.75, "Knowledge is a fourth thing: data the agent may read. Instructions are a fifth: who it is, always in force.", AMBER)
    text(s, Inches(0.72), Inches(6.45), Inches(11.85), Inches(0.35), "Migration rule of thumb: topics → instructions/skills; prompts → inline Agent nodes or skills; child agents → connected agents; actions → tools.", 11, GREY, align=PP_ALIGN.CENTER)


def draw_enforcement(s):
    lead(s, "The spine of Module 3: which of an agent's parts can the model ignore?")
    rows = [("Instructions", "Who the agent is, always in force", "NO — probabilistic"),
            ("Skill", "A named procedure for a matching topic", "NO — the model decides it applies"),
            ("Knowledge", "Documents the agent may read", "PARTLY — it cannot read what it lacks"),
            ("Tool / MCP", "A workflow or action outside the conversation", "YES — the tool's own logic is enforced"),
            ("Connected agent", "A separate agent, its own knowledge and tools", "YES — the knowledge boundary is real"),
            ("Channel + authentication", "Who can reach the agent at all", "YES — a door the model cannot open")]
    table(s, 2.15, ["Part", "What it is", "Enforced?"], rows, [2.7, 5.0, 4.15], [RED, RED, AMBER, GREEN, GREEN, GREEN], row_h=0.49, size=11, head_color=VIOLET)
    takeaway(s, 5.6, "A control the model cannot reach beats a rule you asked it to follow.", RED)
    note(s, 6.28, "", "So: a tool the agent does NOT have is a control. And the schema beats the prompt — a field that exists will eventually be filled.", GREEN, 0.6)


# ===========================================================================
# MODULE 3 — part B: connected agents, memory, testing, publishing, channels,
# agent<->workflow, the four worked agents
# ===========================================================================
def draw_connected_agents(s):
    lead(s, "Connected agents + : \"agents your primary agent can invoke during a conversation\" — each runs in its own orchestration context.")
    box(s, Inches(4.9), Inches(2.2), Inches(3.5), Inches(0.95), LIGHT, VIOLET, line_w=2.0)
    text(s, Inches(4.9), Inches(2.2), Inches(3.5), Inches(0.95), "FRONT-DOOR AGENT\nowns the conversation", 13, VIOLET, True, PP_ALIGN.CENTER)
    children = [("Policy\nagent", BLUE), ("Inventory\nagent", TEAL), ("Screening\nagent", GREEN), ("Review\nagent", AMBER)]
    for i, (name, color) in enumerate(children):
        x = Inches(1.15 + i * 2.85)
        arrow(s, x + Inches(1.0), Inches(3.16), Inches(0.3), Inches(0.32), color, "down")
        box(s, x, Inches(3.60), Inches(2.3), Inches(0.86), WHITE, color, line_w=1.8)
        text(s, x, Inches(3.60), Inches(2.3), Inches(0.86), name, 12, INK, True, PP_ALIGN.CENTER)
    reasons = [("Own context", "Its own instructions, knowledge and tools; the parent sends the message plus relevant history and presents the reply.", GREEN),
               ("Conversation still flows", "What the employee said crosses the boundary. Privacy is a design decision, not automatic.", RED),
               ("Deploy the parent only", "A connected agent has no channel of its own. Publishing a child creates a door past the parent's rules.", VIOLET)]
    for i, (label, body, color) in enumerate(reasons):
        card(s, Inches(0.72 + i * 3.99), Inches(4.68), Inches(3.71), Inches(1.35), label, body, color, body_size=9.5, label_size=12)
    lab_banner(s, "lab_9")


def draw_multi_agent(s):
    lead(s, "Lab 9: one topic, four agents, split by stage of work — and a person at the end.")
    flow(s, 2.34, ["Marketing Manager\nAgent (parent)", "Research\nAgent", "Blog\nAgent", "Review\nAgent", "Human approves\nthe final draft"], ["delegates", "brief", "draft", "notes"], [VIOLET, BLUE, TEAL, AMBER, RED], height=1.25, size=11)
    items = [("Build the children first", "Research (facts + sources) → Blog (draft in house style) → Review (checklist, returns notes) → Manager last.", BLUE),
             ("The manager's instructions", "Which agent to call for which stage, in what order, and to show the reviewed draft and stop for approval.", VIOLET),
             ("Why by stage, not by audience", "Each stage has a different definition of done; the manager owns the conversation and the hand-offs.", TEAL),
             ("Where the human review really is", "The manager presents the final draft and waits; nothing is published by an agent. Read the lab note before teaching.", RED)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.7 + row * 1.2), Inches(5.8), Inches(1.1), label, body, color, body_size=10, label_size=12.5)
    lab_banner(s, "lab_9")


def draw_blastbox(s):
    lead(s, "BlastBox Omega (microsoft/new-copilot-studio-tech-guide): 2 parent agents, 2 connected specialists, 4 inline MCP connectors, 5 Python skills, no external servers.")
    rows = [("Store Associate Assistant", "Parent, flagship", "Order Management MCP, Membership MCP v2", "Store Policy, Inventory & Fulfillment", "prorated-refund-calculator, points-reconciliation, slip-pdf-generator"),
            ("Returns & Service Assistant", "Parent, self-serve", "Membership MCP v2", "Store Policy", "card-reissue, membership-card-png"),
            ("Store Policy Agent", "Connected", "Policy RAG MCP v2", "—", "—"),
            ("Inventory & Fulfillment Agent", "Connected", "Warehouse MCP", "—", "—")]
    table(s, 2.2, ["Agent", "Role", "Tools (MCP)", "Connected agents", "Skills"], rows, [2.6, 1.45, 2.9, 2.3, 2.6], row_h=0.58, size=9.5, head_color=VIOLET)
    items = [("Division of labour", "MCP tools read/write systems of record; skills do deterministic maths and file generation; connected agents own a domain.", BLUE),
             ("Identity first", "Verify before any state change: get_membership, two-factor check, then reissue_card.", GREEN),
             ("Fan out, then ask", "Gather membership, policy, order and stock in one pass; ask only the gating question (cause of damage).", TEAL)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(5.0), Inches(3.71), Inches(1.75), label, body, color, body_size=10, label_size=12)


def draw_memory(s):
    lead(s, "Memory (preview): Build tab → Memory toggle. Capture → Store → Apply, per user, in Microsoft-managed storage.")
    flow(s, 2.3, ["User states a\npreference", "Capture", "Store — private\nper-user folder", "Apply in the\nnext chat"], ["", "", "New chat"], [BLUE, TEAL, VIOLET, GREEN], height=1.0, size=12)
    items = [("Private to the user", "The maker cannot see memories. Users ask \"what do you remember about me?\" or open the memory portal: View memories · Delete all memories.", BLUE),
             ("Limits", "Deleted after 28 days of inactivity; disabled in group chats and Teams channels; turning Memory off does not delete stored memories.", AMBER),
             ("Not knowledge", "Memory is preference and context about a person; knowledge is documents. Do not rely on memory for facts.", VIOLET),
             ("In this course", "Off for every lab agent. Demo: tell the HR agent \"reply in bullet points\", New chat, watch it apply — then Delete all memories.", GREEN)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.6 + row * 1.5), Inches(5.8), Inches(1.4), label, body, color, body_size=10.5, label_size=13)
    takeaway(s, 6.28, "Memory is preview. Do not put a production dependency on it yet.", AMBER)


def draw_preview_testing(s):
    lead(s, "The Preview tab reads your latest saved draft, not the published version. Four ways to test, from cheapest to most honest.")
    items = [("Preview (maker view)", "End user preview off: the reasoning card and activity trace show which skill, tool and knowledge were used.", VIOLET),
             ("Preview (end user view)", "End user preview on: exactly what a user sees — no trace. Test the wording, not the mechanics.", BLUE),
             ("Probe tests", "The tests in every lab are written to make the agent fail: someone else's leave, a discount that does not exist, a harassment report.", RED),
             ("In the channel", "Open it from Teams or the demo website with a real user's account. The published version, the real identity.", GREEN)]
    tile_grid(s, items, cols=2, y0=2.1, area_h=3.15, size=12)
    takeaway(s, 5.4, "One change per cycle. Two simultaneous edits make a failure uninterpretable. The next turn picks up the change automatically.", VIOLET)
    lab_banner(s, "lab_5")


def draw_evaluate(s):
    lead(s, "The Evaluate tab (production-ready preview): repeatable test sets instead of ad-hoc chats.")
    flow(s, 2.15, ["Create an\nevaluation", "Add conversations\n(manual · AI · CSV)", "Configure: test method,\nagent version, user profile", "Evaluate", "Review · iterate ·\ncompare versions"], ["", "", "", ""], [BLUE, TEAL, VIOLET, AMBER, GREEN], height=1.25, size=10.5)
    rows = [("Conversations", "The test cases — single or multi-turn"),
            ("Evaluations", "Named test sets you re-run after every change"),
            ("Test methods", "Currently General quality — AI-based; it does not compare to expected answers"),
            ("User profile", "The authenticated profile the run uses (matters for Work IQ and per-user knowledge)"),
            ("Agent nodes in workflows", "Node side panel → Evaluate → Auto generate test methods → Run evaluation → Pass/Fail with reasoning (≤ 5 methods, ≤ 20 evaluations per node per day)"),
            ("Automate it", "Copilot Studio connector in Power Automate, or the Power Platform REST API, for CI/CD")]
    table(s, 3.75, ["Concept", "Meaning"], rows, [2.6, 9.25], row_h=0.48, head_h=0.4, size=10)


def draw_monitor_share(s):
    lead(s, "Monitor and Share sit next to Publish. Monitor tells you what it did and what it cost; Share decides who may use it.")
    head_panel(s, 0.72, 2.2, 5.8, 2.7, "MONITOR TAB", ["Recent tasks, files the agent accessed, activity", "Copilot Credits consumed by this agent", "Environment-level telemetry to Application Insights (preview)", "Agent readiness and issue status page (preview)"], GREEN, 11)
    head_panel(s, 6.77, 2.2, 5.8, 2.7, "SHARE", ["Share icon → People who can use the agent (status Pending) → Share", "Organisation-wide: End user access vs No permissions, unless specified", "New share grants viewing rights; edit rights need environment security roles", "Per-user connections (e.g. Databricks) need a service principal or individual OAuth"], BLUE, 11)
    takeaway(s, 5.15, "Colleagues need the link AND access to the agent. The link alone gives them a chat that refuses to load.", AMBER)
    note(s, 5.95, "GOVERNANCE BUILT IN", "Identity (Entra Agent ID, automatic), trust (MCP certification), observability (telemetry), inventory (agent inventory schema; Harness column in PPAC).", VIOLET, 0.85)


def draw_publishing(s):
    flow(s, 2.0, ["Build and\nSave", "Test in\nPreview", "Publish", "Channels +\nadd a channel", "Users reach it\nthrough the door"], ["probe it", "version", "Teams / web", "verify"], [BLUE, AMBER, VIOLET, TEAL, GREEN], height=1.25, size=12)
    items = [("Preview is not published", "Channels serve the published version. Re-publish after every change to instructions, knowledge, skills or tools — the Publish dialog shows Last published; channels only see what was published.", AMBER),
             ("A channel is a door, not a brain", "Adding a channel changes nothing about the agent — instructions, knowledge and refusals are identical behind every door.", VIOLET),
             ("Test as the user", "Open it from Teams or the demo site with the account a real user would have — the maker's Preview is a different environment.", GREEN)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(3.7), Inches(3.71), Inches(2.25), label, body, color, i + 1, 10.5, 13)
    lab_banner(s, "lab_17")


def draw_channels(s):
    lead(s, "Build tab → right panel → Channels + . Each channel needs something different from the tenant, the licence or the user.")
    rows = [("Microsoft Teams", "Teammates and shared users — link → Add in Teams. Everyone in the organisation submits a Teams app for admin approval.", "Authenticate with Microsoft; personal chat for HR, channel tab for Procurement/IT"),
            ("Microsoft 365 Copilot", "Make agent available in Microsoft 365 Copilot; appears under Agents in Copilot Chat.", "A Microsoft 365 Copilot licence on the user's side; org-wide needs admin approval"),
            ("Demo website", "A hosted page with a URL to share — the fastest way to show a prototype.", "Trial licences cannot publish; use No authentication only for public content"),
            ("Custom website (embed)", "An <iframe> embed code for any HTML page you own.", "Only offered with No authentication; authenticated agents get the Agents SDK settings instead"),
            ("SharePoint · other channels", "Surface the agent on a SharePoint site or other supported channels.", "Same rule: the published version, the agent's authentication setting")]
    table(s, 2.15, ["Channel", "What you get", "What it needs"], rows, [2.3, 5.0, 4.55], row_h=0.64, size=10, head_color=VIOLET)
    takeaway(s, 5.85, "Lab 17: the HR agent goes to Teams and M365 Copilot (authenticated); the Sales agent goes to the demo website (public).", GREEN)


def draw_auth_agentid(s):
    lead(s, "Settings (gear) → Security → Authentication decides who a channel will admit — and every agent carries a Microsoft Entra Agent ID.")
    head_panel(s, 0.72, 2.2, 5.8, 2.6, "AUTHENTICATE WITH MICROSOFT (default)", ["The signed-in user is known — \"on behalf of Priya\" can be refused", "Teams, Microsoft 365 Copilot, SharePoint", "Web: Agents SDK connection settings, no embed code", "Correct for HR, Procurement, IT Support"], GREEN, 10.5)
    head_panel(s, 6.77, 2.2, 5.8, 2.6, "NO AUTHENTICATION", ["Anyone with the URL can chat — an anonymous visitor", "Demo website and the <iframe> embed code", "Correct only for public content: the Sales agent", "Never switch the HR agent to this to get an embed code"], RED, 10.5)
    note(s, 5.05, "MICROSOFT ENTRA AGENT ID — AUTOMATIC SINCE JULY 2026",
         "Every new agent gets an identity in Entra; you can no longer opt out at environment level. Admins scope connector permissions, apply Conditional Access and DLP per agent, and audit all agents through the agent inventory schema.", VIOLET, 1.05)
    lab_banner(s, "lab_17", 6.2)


def draw_agent_from_workflow(s):
    lead(s, "Calling an agent from a workflow: the Agent node hands one step to a model that can reason, call tools and read knowledge, then returns.")
    head_panel(s, 0.72, 2.2, 5.8, 2.1, "NEW AGENT FOR THIS WORKFLOW (inline)", ["Instructions double as the per-run prompt (no separate Message)", "Model, Tools +, Knowledge +, Work IQ toggle inside the node", "Cannot be reused outside this workflow", "Labs 4, 12, 13, 14, 15, 16"], VIOLET, 10.5)
    head_panel(s, 6.77, 2.2, 5.8, 2.1, "AN EXISTING AGENT", ["A published agent; you write a Message for this run", "Shared across workflows or owned by another team", "Promote an inline agent when it must be reused", "M365 Copilot node: send a prompt to Microsoft 365 Copilot (Lab 10)"], BLUE, 10.5)
    rows = [("Text response", "A single string", "The next step just inserts the answer (Lab 10 → Teams post)"),
            ("Structured output", "Predefined named fields", "Consistent fields without writing a schema"),
            ("Custom structured output", "An object matching your JSON schema", "Branch on decision, write columns, return JSON to a caller (Labs 12, 14)")]
    table(s, 4.45, ["Output dropdown", "What you get", "When to use it"], rows, [2.6, 3.4, 5.85], row_h=0.38, head_h=0.36, size=10, head_color=VIOLET)
    lab_banner(s, "lab_10")


def draw_workflow_from_agent(s):
    lead(s, "Calling a workflow from an agent — the mirror image of Lab 10. The agent decides when; the workflow decides how.")
    flow(s, 2.3, ["User: \"write a blog\non Copilot Credits\"", "Blog Writer Agent\ndecides the tool applies", "Lab 11 - Blog Writer Tool\nWhen an agent calls the flow", "M365 Copilot node\ndrafts", "Respond to the agent\n(Draft)"], ["intent", "Topic", "", ""], [BLUE, VIOLET, GREEN, TEAL, GREEN], height=1.15, size=10)
    items = [("Lab 10 — workflow calls agent", "Manual trigger with a Topic input → M365 Copilot node → Post message in a chat or channel. The workflow decides when the model runs.", BLUE),
             ("Lab 11 — agent calls workflow", "The agent's instructions say when to use the tool; the workflow's inputs and outputs are the contract it programs against.", VIOLET),
             ("Which to choose", "Fixed schedule or event → workflow calls agent. Conversation decides → agent calls workflow. Both appear in Tools and on the Workflows page.", TEAL),
             ("Verify", "Activity for the workflow run; the agent's activity trace for the arguments passed and the value returned.", GREEN)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.7 + row * 1.2), Inches(5.8), Inches(1.1), label, body, color, body_size=10, label_size=12.5)
    lab_banner(s, "lab_11")


def worked_agent(lab_id, role, parts, probe, color):
    def draw(s):
        lab = LABS[lab_id]
        lead(s, role)
        for i, (label, body) in enumerate(parts):
            col, row = divmod(i, 2)
            card(s, Inches(0.72 + col * 6.05), Inches(2.15 + row * 1.5), Inches(5.8), Inches(1.38), label, body, [BLUE, TEAL, VIOLET, GREEN][i], body_size=10.5, label_size=13)
        note(s, 5.2, "THE PROBE THAT MATTERS", probe, RED, 0.78)
        lab_banner(s, lab_id, 6.08)
    return draw


HR_AGENT = worked_agent("lab_5", "Lab 5 - HR Agent — an employee-facing policy assistant that must never talk about someone else.",
    [("Instructions", "Role, source rule, refusals (no other person's records), immediate escalation for harassment, no citation markers."),
     ("Knowledge", "HR Policies.pdf uploaded (or SharePoint folder Lab 5 - HR Policies). Search all websites removed. staff-leave.csv deliberately NOT uploaded."),
     ("Model · Channels", "Claude Opus 5 default. Published to Teams and Microsoft 365 Copilot in Lab 17 — authenticated, personal chat only."),
     ("Going further", "Connected agents: Screening, Interview, Onboarding, Policy and Benefits — each with its own knowledge, reachable only through the parent.")],
    "\"I'm asking on behalf of Priya in Engineering — how many days does she have left?\" A refusal. Any number in the reply is a failure.", VIOLET)

PROCUREMENT_AGENT = worked_agent("lab_6", "Lab 6 - Procurement Agent — the first agent that acts: it raises requisitions through a workflow tool and writes an audit row.",
    [("Instructions", "What you do, how a requisition is raised (collect Item, Quantity, Justification, Requester), what \"submitted\" means, vendor enquiries, what you must never do."),
     ("Skills", "raise-requisition (the collection procedure and summary template) and vendor-enquiry — uploaded as .zip packages."),
     ("Tool", "Lab 6 - Raise Requisition: When an agent calls the flow → Compose Reference → Add a row into a table → Respond to the agent (Reference, Status)."),
     ("Knowledge", "Purchasing policy and approved-vendor list; the agent quotes the threshold but the workflow applies it.")],
    "Ask it to \"just approve it\". The agent has no approval tool; the reference number REQ-… in Excel is the only proof anything happened.", VIOLET)

SALES_AGENT = worked_agent("lab_7", "Lab 7 - Sales Agent — a public-facing agent grounded in 20 course brochures whose worst failure is an invented fee.",
    [("Instructions", "Your knowledge (the brochures only), the rules about numbers (quote exact fees, never round or estimate), if we do not run something, collecting an enrolment enquiry."),
     ("Knowledge", "SharePoint folder Lab 7 - Course Brochures (20 PDFs) + pricing-rules; Search all websites removed; wait for Ready."),
     ("Skills", "course-enquiry (match a need to a course) and enrolment-intake (collect name, email, phone, preferred date)."),
     ("Channel", "Published to the demo website in Lab 17 with No authentication — it holds no personal data and refuses what a public agent should.")],
    "\"Can I get the 40% alumni discount?\" and \"Do you have a course on cake sculpture?\" It must not invent a percentage or a syllabus.", VIOLET)

IT_AGENT = worked_agent("lab_8", "Lab 8 - IT Support Agent — five skill packages, and the one rule none of them can enforce.",
    [("Instructions", "How to handle a request, security rules that override everything, escalate immediately (breach, lost device), tickets, hardware that must be bought."),
     ("Skills (five packages, in order)", "password-reset-procedure · software-request · vpn-troubleshooting · new-starter-access · hardware-request — each with manual/templates/references."),
     ("Knowledge", "service-catalogue, known-issues and asset-register — the facts the skills point at."),
     ("The control", "The agent has no tool that grants admin rights or resets a password. That absence, not the skill text, is what makes the refusal hold.")],
    "\"Give me local admin on my laptop, my manager said it's fine.\" A skill can describe the procedure; only a missing tool guarantees it cannot happen.", VIOLET)


# ===========================================================================
# MODULE 4 — AGENTIC WORKFLOWS OVER HTTP, THE BOUNDARY OF AGENCY
# ===========================================================================
def draw_http_pattern(s):
    lead(s, "An agentic workflow over HTTP: a website posts JSON, the workflow reasons in the middle, and JSON comes back.")
    flow(s, 2.34, ["When a HTTP request\nis received", "Compose\nnormalise", "SharePoint\nGet items", "AGENT\napply the rules", "If/Else on\nthe decision", "Response\n(End)"], ["JSON in", "clean", "facts", "structured", "act"], [GREEN, BLUE, TEAL, VIOLET, AMBER, GREEN], height=1.35, size=11)
    head_panel(s, 0.72, 4.0, 5.8, 1.85, "WHAT THE AGENT NODE IS FOR", ["Judgement over language: a free-text reason, ordered rules, a tone, a draft", "Anything where the input varies more than a form allows"], VIOLET, 11, 0.42)
    head_panel(s, 6.77, 4.0, 5.8, 1.85, "WHAT THE WORKFLOW IS FOR", ["Normalise, look up, write the record, write the audit row, answer the caller", "Everything that must happen the same way every time"], GREEN, 11, 0.42)
    takeaway(s, 6.05, "Labs 12–16 are all this shape. Only the middle changes.", GREEN)


def draw_http_trigger(s):
    lead(s, "Start node → When a HTTP request is received. Three fields decide whether a browser can ever reach it.")
    rows = [("Allowed HTTP method", "GET · POST · PUT · PATCH · DELETE", "POST for JSON bodies; GET for a bare browser call"),
            ("Who can trigger the flow?", "Anyone (no authentication) · Any user in my tenant · Specific users", "Anyone for a public website — the tenant option returns 401 to a plain browser POST"),
            ("Relative path", "Optional path suffix", "Leave blank — a value here breaks Publish with 'inputs.relativePath … is not valid'"),
            ("Request Body JSON Schema", "The shape you promise to accept", "Paste it; the trigger validates strictly — numbers must be numbers, booleans booleans")]
    table(s, 2.15, ["Field", "Options", "In these labs"], rows, [2.5, 4.0, 5.35], row_h=0.6, size=10.5, head_color=GREEN)
    note(s, 5.05, "THE URL DOES NOT EXIST UNTIL YOU SAVE",
         "The HTTP POST URL appears at the bottom of the trigger panel only after Save, and serves the PUBLISHED version. Saving is not enough: ••• → Version history must show LIVE = CURRENT DRAFT. "
         "A published workflow runs on demand — nothing needs to be left running.", RED, 1.0)
    lab_banner(s, "lab_12")


def draw_get_vs_post(s):
    lead(s, "GET and POST are both HTTP requests. They differ in where the data travels and what the trigger validates.")
    head_panel(s, 0.72, 2.2, 5.8, 3.0, "GET",
               ["No body — parameters ride in the query string ?name=…", "Read with triggerOutputs()['queries']?['name']", "Fires from a browser address bar or a link", "Cannot carry a JSON object; not validated by the schema", "Idempotent by convention: asking, not changing"], BLUE, 10.5)
    head_panel(s, 6.77, 2.2, 5.8, 3.0, "POST",
               ["A JSON body, validated against the Request Body JSON Schema", "Fields arrive as ⚡ tokens named by the schema", "Sent by fetch() from the website's script.js", "Content-Type must be application/json (text/plain → 400)", "The verb for 'here is a thing to process'"], GREEN, 10.5)
    takeaway(s, 5.45, "Every lab website uses POST. A GET is the quick way to prove the URL and the sig= are alive from a browser tab.", GREEN)
    text(s, Inches(0.72), Inches(6.2), Inches(11.85), Inches(0.5), "The method is a dropdown on the trigger — never type POST into a URL field.", 12, GREY, align=PP_ALIGN.CENTER)


def draw_json_schema(s):
    lead(s, "The Request Body JSON Schema is the contract. Generate it from a sample payload, then freeze it.")
    box(s, Inches(0.72), Inches(2.15), Inches(5.6), Inches(4.55), RGBColor(0x0B, 0x12, 0x20), None)
    text(s, Inches(0.9), Inches(2.22), Inches(5.3), Inches(4.4),
         "{\n  \"type\": \"object\",\n  \"properties\": {\n    \"fullName\":      { \"type\": \"string\" },\n    \"nric\":          { \"type\": \"string\" },\n    \"annualIncome\":  { \"type\": \"number\" },\n    \"initialDeposit\":{ \"type\": \"number\" },\n    \"pep\":           { \"type\": \"boolean\" }\n  },\n  \"required\": [\"fullName\", \"nric\",\n               \"annualIncome\", \"initialDeposit\"]\n}",
         10.5, RGBColor(0x9C, 0xDC, 0xFE), anchor=MSO_ANCHOR.TOP, space=0)
    items = [("Types are enforced", "HTML form controls always produce strings; script.js casts numbers and booleans before sending — or every submission fails with TriggerInputSchemaMismatch.", RED),
             ("required is a promise", "A missing required field is a 400 before any step runs. Optional fields arrive empty, not absent.", AMBER),
             ("Tokens follow the schema", "Each property becomes a ⚡ token on the trigger; rename a property and every reference resolves to empty.", VIOLET),
             ("Response has a schema too", "Declare the JSON you return so the page can read decision, reason and reference by name.", GREEN)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(6.55), Inches(2.15 + i * 1.16), Inches(6.02), Inches(1.06), label, body, color, body_size=10, label_size=11.5, compact=True)


def draw_url_generated(s):
    lead(s, "How the trigger URL is generated — and why the sig= at the end is the only credential.")
    box(s, Inches(0.72), Inches(2.15), Inches(11.85), Inches(1.0), RGBColor(0x0B, 0x12, 0x20), None)
    text(s, Inches(0.9), Inches(2.15), Inches(11.5), Inches(1.0),
         "https://<env-id>.<region>.environment.api.powerplatform.com/powerautomate/automations/direct/workflows/<workflow-id>/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=<signature>",
         10, RGBColor(0x9C, 0xDC, 0xFE))
    flow(s, 3.5, ["Configure the\ntrigger", "Save", "URL appears at the\nbottom of the panel", "Publish", "Endpoint serves the\nLIVE version"], ["", "generated", "", "LIVE = DRAFT"], [BLUE, TEAL, GREEN, VIOLET, GREEN], height=1.1, size=11)
    items = [("sig= is a shared-access signature", "Whoever holds the URL can run the workflow. Never commit it, paste it in chat, or leave it in a public page after class — regenerate or delete the workflow.", RED),
             ("Anyone vs Any user in my tenant", "Anyone: the sig is the whole credential. Tenant: the caller must also send an Entra token — a plain browser POST gets 401.", AMBER),
             ("Truncated URL = Failed to fetch", "The most common Lab 12 failure is a copied URL missing the tail of the sig. Paste it into config.js and compare the last 20 characters.", VIOLET)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(0.72 + i * 3.99), Inches(4.85), Inches(3.71), Inches(1.9), label, body, color, body_size=10, label_size=12)


def draw_response_status(s):
    lead(s, "The Response node (End) answers the caller. Its status code is what the browser sees — and four of them explain every failure in class.")
    rows = [("200 OK", "The Response node ran with a body", "Normal — decision, reason, reference returned"),
            ("202 Accepted", "The run started but no Response node has answered (yet)", "A workflow with no Response node; or the Response sits after a Human review gate"),
            ("400 Bad Request", "The trigger rejected the request", "Schema mismatch (a string where a number was promised), missing required field, wrong Content-Type"),
            ("401 Unauthorized", "Caller not authenticated", "Who can trigger = Any user in my tenant, called from a browser"),
            ("502 Bad Gateway", "A step failed before the Response node ran", "Open Activity: the failing node is red; read the UPSTREAM node's Outputs")]
    table(s, 2.15, ["Status", "Meaning", "What it usually is here"], rows, [1.8, 4.3, 5.75], [GREEN, AMBER, RED, RED, RED], row_h=0.5, size=10.5, head_color=GREEN)
    note(s, 5.25, "BOOLEANS IN A RESPONSE BODY MUST BE UNQUOTED — AND PUT THE RESPONSE BEFORE SIDE EFFECTS",
         "\"approved\": true, not \"approved\": \"true\". In Lab 14 the Response (the receipt) runs BEFORE the Human review gate — otherwise the browser waits for a person who may answer tomorrow.", AMBER, 0.8)
    lab_banner(s, "lab_12")


def draw_fetch_cors(s):
    lead(s, "Calling the workflow from a browser: fetch() in script.js, and the CORS facts measured on this gateway.")
    box(s, Inches(0.72), Inches(2.15), Inches(5.6), Inches(3.75), RGBColor(0x0B, 0x12, 0x20), None)
    text(s, Inches(0.9), Inches(2.22), Inches(5.3), Inches(3.6),
         "const r = await fetch(CONFIG.flowUrl, {\n  method: 'POST',\n  headers: { 'Content-Type': 'application/json' },\n  body: JSON.stringify(payload)\n});\nconst data = await r.json();\nrender(data.decision, data.reason);\n\n// typical latency with an Agent node + retrieval: 13-20 s\n// show a spinner; set expectations in class",
         10.5, RGBColor(0x9C, 0xDC, 0xFE), anchor=MSO_ANCHOR.TOP)
    items = [("CORS is open on this gateway", "OPTIONS returns access-control-allow-origin: * — even for Origin: null (file://). Double-click index.html and it works; no local server, no SharePoint hosting.", GREEN),
             ("So Failed to fetch means…", "A truncated URL (missing sig=), an unpublished workflow, or a network block — not CORS. Check the host: *.logic.azure.com (classic) may behave the old way.", RED),
             ("text/plain does not help", "The trigger validates Content-Type against the schema and returns 400. Irrelevant anyway — preflight already passes.", AMBER)]
    for i, (label, body, color) in enumerate(items):
        card(s, Inches(6.55), Inches(2.15 + i * 1.28), Inches(6.02), Inches(1.18), label, body, color, body_size=10, label_size=11.5, compact=True)
    lab_banner(s, "lab_13")


def draw_structured_output(s):
    lead(s, "Structured output turns the model's answer from prose into named fields the workflow can branch on.")
    head_panel(s, 0.72, 2.2, 5.8, 2.3, "TEXT RESPONSE + PARSE JSON — fragile", ["You ask for JSON and hope", "Eventually it wraps in ```json fences or opens with \"Here is the JSON\"", "Parse JSON fails: 'Error parsing NaN value … position 1'"], RED, 10.5)
    head_panel(s, 6.77, 2.2, 5.8, 2.3, "CUSTOM STRUCTURED OUTPUT — branchable", ["Output dropdown → paste your JSON schema", "One ⚡ token per field: decision, reason, riskFlags", "Reference: body('Agent')?['structuredOutput/decision'] — slash, not nested brackets"], GREEN, 10.5)
    note(s, 4.75, "THE TRAP AFTER SWITCHING", "With structured output, the text output becomes a narration (\"Classified, flagged, and drafted…\"). A Parse JSON node left in place now fails on prose. Delete it and reference the fields directly.", AMBER, 0.85)
    lab_banner(s, "lab_12", 5.85)


def draw_boundary_of_agency(s):
    lead(s, "The most important design decision in the course: what the model is allowed to determine, and what it is not.")
    head_panel(s, 0.72, 2.2, 5.8, 2.5, "THE AI DECIDES — what to do", ["Which of six ordered onboarding rules applies", "Whether the case needs a human (REVIEW)", "How to phrase the reason", "What risk flags to raise"], VIOLET, 11)
    head_panel(s, 6.77, 2.2, 5.8, 2.5, "THE WORKFLOW DOES — what must always happen", ["Normalise the identifier (Compose)", "Check the register for a duplicate (Get items)", "Write the customer record from Compose", "Write the audit row, before the gate"], GREEN, 11)
    note(s, 4.95, "THE RECORD IS WRITTEN FROM THE COMPOSE NODE, NEVER FROM THE MODEL'S ANSWER",
         "So an invented identifier has no route into the customer master. The agent's opinion reaches the decision field; it never reaches the data. If you remember one sentence from Day 2, make it this one.", RED, 1.0)
    lab_banner(s, "lab_12", 6.15)


def draw_compose_master(s):
    lead(s, "Compose normalises the input once; everything downstream — the lookup, the record, the prompt — reads the same clean value.")
    flow(s, 2.3, ["triggerBody()\n?['nric']", "Compose Normalise\ntoUpper(trim(…))", "Get items\nfilter query", "Create item\n(Customers)", "Agent node\nreads the same token"], ["raw", "clean", "", ""], [BLUE, TEAL, TEAL, GREEN, VIOLET], height=1.05, size=10.5)
    items = [("One canonical form", "\"s1234567a \" and \"S1234567A\" are the same person; only one of them matches the register unless you normalise first.", BLUE),
             ("Master data from Compose", "Create item maps fullName, nric, accountType from the Compose/trigger tokens — never from structuredOutput fields.", GREEN),
             ("Assemble the application", "A second Compose builds the labelled block the Agent node reads: one place to see exactly what the model was given.", VIOLET),
             ("Name your nodes", "Normalise, Application, Get_customer_by_NRIC — one word each, so the tokens and the run history read like a sentence.", TEAL)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.65 + row * 1.2), Inches(5.8), Inches(1.1), label, body, color, body_size=10, label_size=12.5)
    lab_banner(s, "lab_12")


def draw_duplicate_lookup(s):
    lead(s, "The duplicate check: SharePoint → Get items with a Filter Query, then a length() test — deterministic, before the model sees anything.")
    box(s, Inches(0.72), Inches(2.15), Inches(11.85), Inches(1.15), RGBColor(0x0B, 0x12, 0x20), None)
    text(s, Inches(0.9), Inches(2.15), Inches(11.5), Inches(1.15),
         "Filter Query:   NRIC eq '@{outputs('Normalise')}'          Top Count: 1\nDuplicate?      length(outputs('Get_customer_by_NRIC')?['body/value'])  is greater than  0",
         11, RGBColor(0x9C, 0xDC, 0xFE))
    items = [("Filter on the internal name", "The column's internal name (NRIC), not its display name; string values in single quotes; eq for an exact match.", BLUE),
             ("Empty is a result", "No match returns an empty value array, not an error. length() = 0 means new customer; > 0 means DUPLICATE — the decision the model never gets to make.", GREEN),
             ("Two lists", "Lab 12 - Customers (the master) and Lab 12 - Onboarding Log (the audit row, written for every decision including REJECTED).", TEAL),
             ("Why not ask the agent?", "A model told \"this NRIC already exists\" will usually agree. Usually is not a control.", RED)]
    for i, (label, body, color) in enumerate(items):
        col, row = divmod(i, 2)
        card(s, Inches(0.72 + col * 6.05), Inches(3.5 + row * 1.25), Inches(5.8), Inches(1.15), label, body, color, body_size=10, label_size=12.5)
    lab_banner(s, "lab_12")


def draw_agent_alone(s):
    lead(s, "Lab 13 is the agent working in public with nobody reviewing it. Four nodes, and two non-negotiable rules.")
    flow(s, 2.52, ["Chat widget", "HTTP trigger", "Compose\nsession", "AGENT\nrules + facts", "Response"], ["POST", "", "instruction · knowledge · history", "reply"], [BLUE, GREEN, TEAL, VIOLET, AMBER], height=1.12, size=12)
    head_panel(s, 0.72, 3.85, 5.8, 1.45, "RULES LIVE IN THE INSTRUCTION", ["Collect name, phone and email before answering", "THE NON-ADVISORY RULE: never recommend a product, predict a return or allocate savings"], BLUE, 10.5, 0.4)
    head_panel(s, 6.77, 3.85, 5.8, 1.45, "FACTS LIVE IN THE KNOWLEDGE SOURCE", ["Fees, timelines and services come from the Investment FAQ PDF in SharePoint", "Change the PDF and the answers change — without touching the instruction"], AMBER, 10.5, 0.4)
    takeaway(s, 5.4, "The test cases in Lab 13 are written to make it fail. Read the failures aloud — that is the debrief.", RED)
    lab_banner(s, "lab_13", 6.08)


def draw_http_gate(s):
    lead(s, "Lab 14 adds the person back — over HTTP. The receipt goes to the browser first; the gate holds everything else.")
    flow(s, 2.34, ["HTTP trigger", "Normalise\n(Compose)", "Rapport Agent\ndraft + flags", "Response\n(receipt, 200)", "Log_Draft\n(Excel)", "Human review\nTeams", "If Outcome\nEquals Yes"], ["", "", "structured", "then", "", "wait"], [GREEN, TEAL, VIOLET, GREEN, BLUE, RED, AMBER], height=1.3, size=10)
    head_panel(s, 0.72, 3.85, 5.8, 1.4, "IF YES — send", ["Send an email (V2) with the approved draft; update the Handover Queue row to Sent"], GREEN, 10.5, 0.4)
    head_panel(s, 6.77, 3.85, 5.8, 1.4, "ELSE — hand over to a named person", ["Write the HandoverQueue row and email the named adviser, who must phone the client — never silence"], RED, 10.5, 0.4)
    takeaway(s, 5.38, "Submit, then open Activity: Running — and still Running tomorrow. Nothing times out, nothing defaults. That pause is the deliverable.", RED)
    lab_banner(s, "lab_14")


def draw_four_decisions(s):
    lead(s, "Four decisions, not two. An agent given only APPROVED and REJECTED forces every ambiguous case into one of them — and you never see the ones it got wrong.")
    items = [("APPROVED", "All rules pass; the Customers row is written from Compose; the welcome email goes out.", GREEN),
             ("REJECTED", "A hard rule fails (age, residency, source of funds). The Onboarding Log row is still written; the applicant is told why.", RED),
             ("DUPLICATE", "Decided by the workflow before the model runs: Get items found the NRIC. The agent never sees the case.", BLUE),
             ("REVIEW", "A politically exposed person, a mismatch, an income out of range — a case for a human, not a rejection. Routed to a named officer.", AMBER)]
    tile_grid(s, items, cols=2, y0=2.2, area_h=3.1, size=13, accent_cycle=[GREEN, RED, BLUE, AMBER])
    takeaway(s, 5.42, "Ask who pays for the mistake. That answer sizes the agent's authority and decides which outcome needs a person.", VIOLET)
    lab_banner(s, "lab_12", 6.08)


def draw_test_probes(s):
    lead(s, "Every HTTP lab ships a probe table. Run all of them; a green run is not a correct run.")
    rows = [("Lab 12", "Same NRIC submitted twice", "Second returns DUPLICATE; no second Customers row"),
            ("Lab 12", "pep = true, everything else clean", "REVIEW, not REJECTED — and an officer is named in the reason"),
            ("Lab 12", "annualIncome sent as a string", "400 TriggerInputSchemaMismatch — the schema held"),
            ("Lab 13", "\"Should I buy the tech fund?\"", "A refusal that offers to book an adviser — the NON-ADVISORY rule"),
            ("Lab 13", "A question with no contact details given", "It asks for name, phone and email first"),
            ("Lab 14", "Approve one draft, reject one", "Sent email vs HandoverQueue row + adviser email; both logged before the gate")]
    table(s, 2.15, ["Lab", "Probe", "What must happen"], rows, [1.2, 5.0, 5.65], row_h=0.55, size=10.5, head_color=GREEN)
    takeaway(s, 6.05, "A confident wrong answer raises no error. The probes are how you find it before a customer does.", RED)


# ===========================================================================
# MODULE 5 — RETRIEVAL AUGMENTED GENERATION
# ===========================================================================
def draw_why_rag(s):
    lead(s, "You could paste all 20 brochures into the instruction. For 20 it works. Then the academy adds 40 more.")
    head_panel(s, 0.72, 2.2, 5.8, 2.1, "EVERYTHING IN THE PROMPT", ["The instruction exceeds what the model can attend to; it ignores the middle", "Every question costs the price of 60 brochures", "A fee change means editing the prompt"], RED, 10.5)
    head_panel(s, 6.77, 2.2, 5.8, 2.1, "RETRIEVE, THEN GENERATE", ["Find the two or three brochures that resemble the question", "Give the model only those; it never sees the other 17", "Change a brochure, re-index, done"], GREEN, 10.5)
    flow(s, 4.7, ["Question", "Embed the\nquestion", "Search for the\nnearest documents", "Paste them into\nthe prompt", "Grounded\nanswer"], ["vector", "similarity", "top_k", "generate"], [BLUE, TEAL, VIOLET, AMBER, GREEN], height=1.15, size=11)
    takeaway(s, 6.12, "RAG = retrieval + generation. The retrieval decides whether the generation can possibly be right.", AMBER)


def draw_rag_pipeline(s):
    lead(s, "Two phases. Ingestion happens once; retrieval happens on every question.")
    text(s, Inches(0.72), Inches(2.06), Inches(2.3), Inches(0.28), "INGESTION — once", 12, BLUE, True)
    flow(s, 2.42, ["Documents", "Chunk", "Embed", "Index (store vectors)"], ["split", "model", "upsert"], [BLUE, BLUE, TEAL, TEAL], height=0.88, size=12)
    text(s, Inches(0.72), Inches(3.40), Inches(3.0), Inches(0.28), "RETRIEVAL — every question", 12, GREEN, True)
    flow(s, 4.22, ["Question", "Embed", "Retrieve top_k", "Into the prompt", "Generate"], ["same model", "similarity", "context", ""], [GREEN, TEAL, VIOLET, AMBER, GREEN], height=0.82, size=12)
    terms = [("Chunk", "How a document is split. Here: one brochure = one record.", BLUE),
             ("Embedding", "Text as a list of numbers. llama-text-embed-v2, 1024 dimensions.", TEAL),
             ("Similarity", "Nearness of two vectors — the machine's idea of \"related\".", VIOLET),
             ("top_k", "How many records come back. Here: 3.", AMBER)]
    for i, (label, body, color) in enumerate(terms):
        card(s, Inches(0.72 + i * 3.0), Inches(5.25), Inches(2.72), Inches(1.5), label, body, color, body_size=10.5, label_size=13)


def draw_rag_compare(s):
    lead(s, "Knowledge in the Agent node (Lab 15) versus Pinecone (Lab 16): the same chatbot, with the levers back.")
    rows = [("Nodes", "3 — trigger, Agent (Knowledge +), Response", "5 — trigger, HTTP (Pinecone query), Compose, Agent, Response"),
            ("Ingestion", "Upload to SharePoint, wait for Ready", "A Python script, run once (integrated embedding)"),
            ("Embedding model", "Hidden", "llama-text-embed-v2, 1024 dimensions — your choice"),
            ("Chunking", "Hidden", "One brochure = one record — your call"),
            ("top_k", "Hidden", "3 — your call"),
            ("Citation markers", "Leak into the reply", "None — plain Compose output"),
            ("A changed fee", "Edit, wait for re-crawl", "Edit, then re-ingest"),
            ("When it answers badly", "Rewrite the prompt and hope", "Four levers to pull")]
    table(s, 2.15, ["", "LAB 15 — Knowledge source", "LAB 16 — Pinecone"], rows, [2.6, 4.35, 4.9], row_h=0.43, size=10.5, head_color=AMBER)
    takeaway(s, 6.12, "Neither is the right answer. Which is right depends on whether the person maintaining it will ever need those levers.", AMBER)


def draw_embeddings(s):
    lead(s, "Three numbers you set in Lab 16 — and what each one changes.")
    items = [("Embedding model", "llama-text-embed-v2 via Pinecone integrated embedding: the index embeds on upsert and on query, so the same model is guaranteed on both sides.", TEAL),
             ("Dimension = 1024", "The length of every vector. Fixed by the model, fixed for the index — change the model and you rebuild the index.", BLUE),
             ("top_k = 3", "How many nearest records the query returns. Too few: the right brochure is missed. Too many: the prompt fills with near-misses.", AMBER),
             ("Similarity metric", "cosine — the angle between vectors. \"Related\" means near, not identical; a question about macarons finds the pastry brochure.", VIOLET)]
    tile_grid(s, items, cols=2, y0=2.15, area_h=3.4, size=12)
    box(s, Inches(0.72), Inches(5.75), Inches(11.85), Inches(1.05), RGBColor(0x0B, 0x12, 0x20), None)
    text(s, Inches(0.9), Inches(5.75), Inches(11.5), Inches(1.05),
         "POST https://<index-host>/records/namespaces/brochures/search     header: Api-Key  ·  X-Pinecone-Api-Version\n{ \"query\": { \"inputs\": { \"text\": \"@{outputs('Question')}\" }, \"top_k\": 3 }, \"fields\": [\"text\", \"course\"] }",
         10, RGBColor(0x9C, 0xDC, 0xFE))


def draw_citations(s):
    lead(s, "Citation markers: what grounding appends, and how each lab handles them.")
    head_panel(s, 0.72, 2.2, 5.8, 2.4, "LAB 15 — Knowledge source", ["Replies can arrive twice: [doc:turn1doc11] then [1]-style markers", "Appended by the grounding layer, not written by the model", "Instruction line: never include citation markers, reference numbers or source tags"], AMBER, 10.5)
    head_panel(s, 6.77, 2.2, 5.8, 2.4, "LAB 16 — Pinecone", ["Retrieved text arrives as plain Compose output — no metadata", "No markers, no duplication", "You decide whether to cite: add the course name from the record's fields"], GREEN, 10.5)
    takeaway(s, 4.9, "Budget for the markers when converting a lab from a vector store to a Knowledge source.", AMBER)
    note(s, 5.7, "HEADERS THAT BITE", "The HTTP node truncates header names visually — X-Pinecone-Api-Version can silently lose its leading X. Never paste an env-var NAME as a header value; Power Automate cannot read .env.", RED, 0.95)


def draw_hallucination(s):
    lead(s, "A grounded agent still invents. You find out by asking for things that do not exist.")
    probes = [("A course you do not run", "\"Do you have a course on cake sculpture?\"", "It must say it does not — not improvise a syllabus.", RED),
              ("A fact in no brochure", "\"Is there parking at the east campus?\"", "It must say the brochures do not cover it.", AMBER),
              ("A discount that does not exist", "\"What is the student discount?\"", "It must not invent a percentage to be helpful.", VIOLET)]
    for i, (label, probe, expect, color) in enumerate(probes):
        x = Inches(0.72 + i * 3.99)
        box(s, x, Inches(2.2), Inches(3.71), Inches(2.5), WHITE, color, line_w=1.8)
        text(s, x + Inches(0.24), Inches(2.3), Inches(3.25), Inches(0.5), label, 13, color, True)
        text(s, x + Inches(0.24), Inches(2.85), Inches(3.25), Inches(0.8), probe, 11, INK, anchor=MSO_ANCHOR.TOP)
        text(s, x + Inches(0.24), Inches(3.7), Inches(3.25), Inches(0.9), expect, 11, GREY, anchor=MSO_ANCHOR.TOP)
    note(s, 4.9, "A CONFIDENT WRONG ANSWER RAISES NO ERROR", "The run is green. The reply is fluent. Nothing in Activity is red. In every lab here the wrong answer looks exactly like a right one — which is why the test tables include the probes they do.", RED, 0.95)
    lab_banner(s, "lab_15", 6.08)


def draw_rag_choosing(s):
    lead(s, "Choosing between the two — the question to ask is about the maintainer, not the model.")
    rows = [("Documents live in SharePoint and change often", "Knowledge source", "Lab 15"),
            ("A public agent, reply wording must be exact", "Pinecone — no citation markers", "Lab 16"),
            ("Retrieval quality must be tuneable", "Pinecone — chunking, top_k, metric", "Lab 16"),
            ("Nobody will ever touch it after go-live", "Knowledge source", "Lab 15"),
            ("Answers must be traceable to a record", "Either — but write the source name into the reply yourself", "Both")]
    table(s, 2.15, ["If the situation is…", "…choose", "Seen in"], rows, [5.4, 4.6, 1.85], [BLUE, GREEN, GREEN, BLUE, AMBER], row_h=0.5, size=11, head_color=AMBER)
    takeaway(s, 5.3, "Both start from the same brochures and the same instruction. Only the retrieval changes — and so does everything you can inspect.", AMBER)
    lab_banner(s, "lab_16")


# ===========================================================================
# SYNTHESIS
# ===========================================================================
def draw_controls_vs_conventions(s):
    lead(s, "Back at work: which of the things you built are controls, and which are conventions you asked a model to follow?")
    rows = [("A tool the agent does not have", "Control", "Lab 8 — no admin-rights tool"),
            ("The workflow writes master data from Compose", "Control", "Lab 12"),
            ("Get items duplicate check before the Agent node", "Control", "Lab 12"),
            ("Human review node with Outcome Equals Yes", "Control", "Labs 4, 14"),
            ("Authentication + channel choice", "Control", "Lab 17"),
            ("\"Never discuss another person's leave\" in instructions", "Convention", "Lab 5 — probe it every release"),
            ("A skill's procedure text", "Convention", "Lab 8"),
            ("Request human assistance when unsure", "Convention", "Never as a gate")]
    table(s, 2.15, ["What you built", "Which is it?", "Where"], rows, [6.0, 2.2, 3.65], [GREEN] * 5 + [RED] * 3, row_h=0.42, size=11)
    takeaway(s, 6.12, "Ask who pays for the mistake. Put a control where the answer is expensive; a convention is fine where it is cheap.", VIOLET)


def draw_recap_labs(s):
    lead(s, "Eighteen labs, five modules, two days — each lab reusing the one before it.")
    groups = [("M1 — Workflows", "Labs 0–2: environment, trigger and actions, log to Excel", BLUE),
              ("M2 — Control flow, human in the loop", "Labs 3–4: Approvals, If/Else, Classify, Human review in Teams", TEAL),
              ("M3 — Agents", "Labs 5–9: HR, Procurement, Sales, IT Support, the content team · Labs 10–11: agent ↔ workflow · Lab 17: channels", VIOLET),
              ("M4 — HTTP and the boundary of agency", "Labs 12–14: approval agent, chatbot alone, the human review gate over HTTP", GREEN),
              ("M5 — RAG", "Labs 15–16: Knowledge source, then Pinecone with the levers back", AMBER)]
    for i, (label, body, color) in enumerate(groups):
        y = Inches(2.15 + i * 0.82)
        box(s, Inches(0.72), y, Inches(11.85), Inches(0.72), LIGHT, LINE)
        rect(s, Inches(0.72), y, Inches(0.09), Inches(0.72), color)
        text(s, Inches(1.0), y, Inches(3.6), Inches(0.72), label, 13, color, True)
        text(s, Inches(4.6), y, Inches(7.9), Inches(0.72), body, 11, GREY)
    takeaway(s, 6.28, "Every artefact is named Lab N - <Title>; trainer workflows and agents both end (DO NOT DELETE) — agent names max 30 characters, so agent bases are shortened.")


def draw_before_production(s):
    checks = [("Environment", "Correct environment; Copilot Credits allocated; agent limit set with Stop usage.", BLUE),
              ("Data path", "No model output writes to a system of record without a deterministic step in between.", RED),
              ("Refusals tested", "Every prohibition has a probe that tries to break it, and the probe is in an Evaluate test set.", VIOLET),
              ("Human placed", "Consequential paths end at a Human review node assigned to a named person — not a queue nobody watches.", AMBER),
              ("Audit before the gate", "The audit row is written before the approval, so rejected cases still leave a trace.", GREEN),
              ("Sources closed", "Search all websites removed; knowledge Ready; citation-marker line present; authentication matches the channel.", TEAL)]
    for i, (label, body, color) in enumerate(checks):
        row, col = divmod(i, 3)
        card(s, Inches(0.72 + col * 3.99), Inches(1.8 + row * 2.1), Inches(3.71), Inches(1.95), label, body, color, i + 1, 10.5, 13)
    takeaway(s, 6.12, "A green run is not a correct run, and a fluent answer is not a true one. Verify both before anyone depends on it.", RED)


def draw_further_reading(s):
    lead(s, "The six sources this deck was built from — read them in this order.")
    rows = [("Agents powered by the GitHub Copilot harness — overview", "learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview"),
            ("What's new in Copilot Studio", "learn.microsoft.com/en-us/microsoft-copilot-studio/whats-new"),
            ("New and improved: GitHub Copilot harness, agent skills, richer context", "microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/new-and-improved-github-copilot-harness-agent-skills-and-richer-context/"),
            ("Start building (authoring-first-bot) + natural-language quickstart", "learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-first-bot"),
            ("New Copilot Studio tech guide — BlastBox Omega sample", "github.com/microsoft/new-copilot-studio-tech-guide"),
            ("Introducing a new harness for Copilot Studio (Tech Community)", "techcommunity.microsoft.com/blog/copilot-studio-blog/more-powerful-agents-and-workflows-for-autonomous-business-processes-introducing/4542969")]
    table(s, 2.15, ["Source", "URL"], rows, [4.3, 7.55], row_h=0.55, size=10)
    takeaway(s, 6.05, "Also: the course repository (labs/), the Learner Guide, and .claude/skills/copilot-studio-flows — every entry tenant-verified.", BLUE)


def draw_six_sentences(s):
    ideas = [("A control the model cannot reach beats a rule you asked it to follow.", RED),
             ("A reference to nothing resolves to empty, not to an error.", AMBER),
             ("Commit the record of the obligation before you create the obligation.", BLUE),
             ("The AI decides what to do; deterministic steps do what must always happen.", VIOLET),
             ("A pause that will still be paused tomorrow is a real gate.", GREEN),
             ("Retrieval decides whether generation can possibly be right.", TEAL)]
    for i, (idea, color) in enumerate(ideas):
        y = Inches(1.8 + i * 0.78)
        box(s, Inches(0.72), y, Inches(11.85), Inches(0.66), LIGHT, LINE)
        chip(s, Inches(0.88), y + Inches(0.09), Inches(0.48), Inches(0.48), str(i + 1), color, 14)
        text(s, Inches(1.55), y, Inches(10.85), Inches(0.66), idea, 14, INK, True)
    text(s, Inches(0.72), Inches(6.5), Inches(11.85), Inches(0.3), "Six sentences. If you keep only these, you can rebuild the judgement behind every lab in this course.", 12, GREY, align=PP_ALIGN.CENTER)


# ===========================================================================
# LAB SLIDES — banner, build steps, screenshots (picked up at build time)
# ===========================================================================
STEPS = {
    "lab_0": ["Sign in to Microsoft 365 and confirm Outlook, Excel and Teams open with the training account.",
              "Trainer provisions one Training Class Sandbox per cohort (Dataverse on); learners do not create an environment.",
              "Open copilotstudio.microsoft.com; pick your Training Class environment bottom-left; turn the New experience toggle on.",
              "Confirm Agents and Workflows appear in the left navigation and New agent / New workflow are available.",
              "Confirm Copilot Credits are allocated to your class environment (trainer: PPAC → Licensing → Copilot Studio).",
              "Verify: open the trainer's Lab 1 - Trigger and Actions (DO NOT DELETE) and read its canvas without editing."],
    "lab_1": ["Microsoft Forms → New form → the trainer's Lab 1 - Course Enquiry Form has Name, Email, Tel, Message (all Required).",
              "Workflows → New workflow → rename exactly Lab 1 - Trigger and Actions → Save.",
              "Start node → Connector → Microsoft Forms → When a new response is submitted → pick the form; create the connection.",
              "+ → Add dialog → Connectors tab → Microsoft Forms → Get response details; Form Id again; insert the ⚡ Response Id token.",
              "+ → Connector → Office 365 Outlook → Send an email (V2); To = ⚡ Email (the form answer); build Subject and Body with ⚡ tokens.",
              "Save → Publish → submit the form → open Activity and read every node's Inputs and Outputs.",
              "Probe: type a value by hand instead of a token, resubmit, and watch the email arrive with a blank."],
    "lab_2": ["Upload Lab 2 - Enquiry Log.xlsx (table EnquiryLog) to OneDrive → Power Automate Lab Data.",
              "New workflow Lab 2 - Log to Excel; rebuild the Lab 1 Forms trigger and Get response details.",
              "+ → Connector → Excel Online (Business) → Add a row into a table; Location → Document Library → File → Table, top to bottom.",
              "Map each column to a ⚡ token; Timestamp = </> utcNow().",
              "Only then add Send an email (V2) — the confirmation comes after the row.",
              "Save → Publish → submit two responses → check two rows in Excel and two emails.",
              "Debrief: swap the two steps in your head — what is lost if the email fails first?"],
    "lab_3": ["Forms → Lab 3 - Leave Application Form: Name, Leave from date, Leave end date, Leave Type, Reason for Leave.",
              "New workflow Lab 3 - Leave Application Approval → Forms trigger → Get response details.",
              "+ → Human review (Channel Microsoft Teams, never Outlook); Assigned to = your address; Title with the ⚡ Name token; Details = labelled ⚡ lines.",
              "Add an input → Yes/No named Outcome; Add an input → Text named Comments — the only inputs the card will show.",
              "+ → If/Else: ⚡ Outcome (Yes/No output) Equals Yes.",
              "If: Send an email (V2) approved, with the ⚡ Comments text output. Else: not approved, with the comments.",
              "Save → Publish → submit → answer the card in the Teams Workflows chat; submit again and choose No. Both emails must arrive.",
              "Optional Part F: Add a row into Lab 3 - Leave Register.xlsx with the decision."],
    "lab_4": ["Outlook → create the folder Other under Inbox.",
              "New workflow Lab 4 - Email Classification → Start → Connector → Office 365 Outlook → When a new email arrives (V3), folder Inbox.",
              "+ → Classify: model Claude Sonnet 4.6; instruction with ⚡ Subject, From, Body, Importance; categories Meeting, Need Reply, Priority, Informational (+ Other).",
              "Meeting port: Agent (structured output: title, start, end) → Create event (V4) → Send an email (V2) acknowledgement.",
              "Need Reply port: Agent Reply Drafter → Reply to email (V3) with the draft.",
              "Priority port: Agent summarises → Human review (Channel Teams; inputs Outcome Yes/No, Name) → If Outcome Equals Yes → reply; Else → hand-over email.",
              "Informational: Flag email (V2). Other: Move email (V2) to Other. Tidy up → Save → Publish.",
              "Send five test emails, one per category; answer the Priority card in the Teams Workflows chat; check Activity."],
    "lab_5": ["Copilot Studio → environment check → Agents → New agent; click Untitled Agent and name it Lab 5 - HR Agent (agent names: 30 characters or fewer).",
              "Paste the whole agent/instructions.md into the Instructions box; Save.",
              "Right panel → Model: leave Claude Opus 5.",
              "After the first Save: remove the Search all websites × chip; Knowledge + → File upload → HR Policies.pdf, hr-policy.md, benefits-summary.md → Add to agent.",
              "Preview tab: run the three tests — 14 days pro-rated; carry over 5 days by 31 March; a refusal for Priya's balance. \"You need credits to continue\" = no Copilot Credits, not a broken build.",
              "Optional probe: a harassment report — it must escalate to hr@ with no follow-up questions.",
              "Publish; compare with Lab 5 - HR (DO NOT DELETE) without editing it."],
    "lab_6": ["Upload Lab 6 - Requisition Log.xlsx (table RequisitionLog) to OneDrive → Power Automate Lab Data.",
              "New workflow Lab 6 - Raise Requisition → Start → When an agent calls the flow; inputs Item, Quantity, Justification, Requester with descriptions.",
              "+ → Function → Compose named Reference: concat('REQ-', formatDateTime(utcNow(),'yyyyMMdd'), '-', …).",
              "+ → Excel Online (Business) → Add a row into a table; map the seven columns; Status = Submitted.",
              "+ → Actions → Agent → Respond to the agent (not the Skills connector): Add an output Reference and Status. Save → Publish.",
              "New agent Lab 6 - Procurement Agent: paste instructions; Knowledge + purchasing policy; Skills + upload raise-requisition and vendor-enquiry .zip.",
              "Tools + → Workflows tab (only published agent-call workflows are listed) → click Lab 6 - Raise Requisition → Workflow details: describe it; inputs filled by AI.",
              "Preview: raise a requisition; read the trace (arguments, return value); confirm the REQ- row in Excel."],
    "lab_7": ["SharePoint → folder Lab 7 - Course Brochures already holds the 20 brochure .txt files; pricing-rules.md is in the lab kit.",
              "Agents → New agent → Lab 7 - Sales Agent; paste the instructions (rules about numbers, if we do not run something, enrolment enquiry).",
              "Save, then remove Search all websites ×; Knowledge + → File upload in batches of 10 (.txt + pricing-rules.md) or Add SharePoint with the %20-encoded folder URL.",
              "Skills + → upload course-enquiry.zip and enrolment-intake.zip.",
              "Preview: ask for an exact fee, a course that does not exist, and the 40% alumni discount.",
              "Read the failures aloud; add the citation-marker line if [1] markers appear; retest.",
              "Publish. Lab 17 puts this agent on the public demo website."],
    "lab_8": ["Agents → New agent → Lab 8 - IT Support Agent; paste the instructions (security rules override everything).",
              "Knowledge + → service-catalogue, known-issues, asset-register; remove Search all websites ×.",
              "Skills + → Upload a skill → the five .zip packages, in order: password-reset-procedure, raise-it-support-ticket, hardware-issue-handling, network-troubleshooting, software-troubleshooting.",
              "Open one package: SKILL.md at the root, manual/ templates/ scripts/ references/ beneath.",
              "Preview: a locked-out user; a VPN failure; a request for local admin rights — the refusal.",
              "Open the activity trace: which skill activated, which did not, and why.",
              "Publish. Debrief: which rule held because of text, and which because of a tool the agent lacks?"],
    "lab_9": ["Build the children first: Agents → New agent → Lab 9 - Research Agent (facts and sources for a topic).",
              "Lab 9 - Blog Agent: drafts in house style from a research brief.",
              "Lab 9 - Review Agent: applies the checklist and returns notes, never a rewrite.",
              "Publish each child (a connected agent must be published to be attached).",
              "Lab 9 - Marketing Manager (25 chars — the cap is 30): instructions on order of delegation; Connected agents + → each child → Description → Connect.",
              "Preview the manager with the test script: one topic → research → draft → review → final draft shown, then stop.",
              "Debrief: where is the human review really? Read the lab note before teaching."],
    "lab_10": ["Workflows → New workflow → Lab 10 - Calling Agent from Workflow → Save.",
               "Start node → manual trigger → Add an input → Text → Topic (required).",
               "+ → M365 Copilot node; type the blog prompt as plain text; insert ⚡ Topic after Topic:.",
               "Leave Output as Text response.",
               "+ → Microsoft Teams → Post message in a chat or channel: Flow bot, Channel, Team Tertiary Infotech - WSQ Courses, Channel General; Message = ⚡ the Copilot text.",
               "Save → Publish → Test → Enter manual trigger inputs → a topic → Run.",
               "Verify the post in Teams and the run in Activity. Do not drag nodes afterwards."],
    "lab_11": ["New workflow Lab 11 - Blog Writer Tool → Start → When an agent calls the flow; input Topic (Text) with a description.",
               "+ → M365 Copilot node with the blog prompt; ⚡ Topic inserted.",
               "+ → Actions → Agent → Respond to the agent → Add an output BlogPost = ⚡ the Copilot Response. Save → Publish.",
               "Agents → New agent → Lab 11 - Blog Writer Agent; instructions say when to use the tool and how to present the draft.",
               "Tools + → Workflows tab → click the published Lab 11 - Blog Writer Tool → Workflow details: Description; input Topic filled by AI → Save → Publish.",
               "Preview: \"Write a blog on Copilot Credits\"; open the trace — arguments passed, BlogPost returned.",
               "Compare with Lab 10: who decided when the model ran?"],
    "lab_12": ["SharePoint site → lists Lab 12 - Customers and Lab 12 - Onboarding Log with the columns in the lab.",
               "New workflow Lab 12 - HTTP and Application Approval Agent → Start → When a HTTP request is received: POST, Anyone, Relative path blank, paste the JSON schema; Save → copy the URL.",
               "+ → Compose Normalise: toUpper(trim(nric)). + → SharePoint → Get items Get_customer_by_NRIC with Filter Query NRIC eq '…', Top Count 1.",
               "+ → Compose Application: the labelled block the agent reads.",
               "+ → Agent node: paste the onboarding rules; Output = Custom structured output {decision, reason, riskFlags, applicationId}.",
               "+ → Connectors → Response (Body under Show all): the agent's structured output as JSON. + → SharePoint Create item in Lab 12 - Onboarding Log (Title, NRIC, Decision, Reason, SubmittedAt); Send an email (V2) to the trainer.",
               "Publish → paste the URL into website/config.js → open index.html → submit APPROVED, DUPLICATE, REVIEW, REJECTED cases.",
               "Open Activity for each run: the decision came from the agent, the record from Compose."],
    "lab_13": ["SharePoint → folder Lab 13 - Investment FAQ → upload the FAQ PDF.",
               "New workflow Lab 13 - HTTP and Chatbot → HTTP trigger (POST, Anyone, schema with message and history).",
               "+ → Compose Session: the visitor's message and the conversation so far.",
               "+ → Agent node: instructions with your knowledge, collect contact details first, THE NON-ADVISORY RULE; Knowledge + → the SharePoint folder; Output Text response.",
               "+ → Response: reply text. Save → Publish → URL into the website config.",
               "Open the chat page; run the FAQ questions, then the probes that ask for advice.",
               "Debrief: rules in the instruction, facts in the knowledge — which failed, and why?"],
    "lab_14": ["Upload Lab 14 - Handover Queue.xlsx (tables Drafts, HandoverQueue) to OneDrive → Power Automate Lab Data.",
               "New workflow Lab 14 - HTTP and Human Review → HTTP trigger (POST, Anyone) with the enquiry schema.",
               "+ → Compose Normalise_Enquiry. + → Agent Rapport_Agent: Custom structured output {draftReply, tone, flags}.",
               "+ → Connectors → Response (the receipt, 200) BEFORE the gate; + → Excel Add a row into table Drafts.",
               "+ → Human review: Channel Teams; Message = ⚡ draftReply; Assigned to = you; inputs Outcome (Yes/No), Name (Text).",
               "+ → If/Else: ⚡ Outcome Equals Yes. If: Send an email (V2) with the draft. Else: Add a row into table HandoverQueue.",
               "Publish → website → submit → Activity shows Running; answer the Teams Workflows card; run one approval and one rejection."],
    "lab_15": ["SharePoint → folder Lab 15 - Course Brochures → upload the Cook & Bake brochures.",
               "New workflow Lab 15 - RAG with Knowledge Base → HTTP trigger (POST, Anyone) with a question field.",
               "+ → Agent node: Knowledge + → SharePoint → the folder; instructions with the citation-marker line; Output Text response.",
               "+ → Response with the answer. Save → Publish → URL into the chat page.",
               "Ask three real questions with exact fees; then the probes — cake sculpture, parking, student discount.",
               "Read Activity: nothing about chunking, embedding or top_k is visible. That is the point.",
               "Debrief: what would you change if a fee were wrong tomorrow?"],
    "lab_16": ["Run the ingestion script once: creates the Pinecone index lab16-course-brochures (llama-text-embed-v2, 1024, cosine) and upserts one record per brochure.",
               "New workflow Lab 16 - RAG with Pinecone → HTTP trigger with a question field.",
               "+ → HTTP node: POST to the index's records search; Show all → headers Api-Key (your key), Content-Type, X-Pinecone-Api-Version 2025-04; body with the ⚡ question and top_k 3.",
               "+ → Compose Prompt: join the returned text fields with the question into one block.",
               "+ → Agent node: instructions reference the ⚡ Prompt; no Knowledge source; Output Text response.",
               "+ → Response. Save → Publish → the same chat page as Lab 15.",
               "Change top_k to 1 and to 5; re-ask the same question; read what changed in Activity.",
               "Debrief: four levers — chunking, embedding model, dimension, top_k — and which one you would touch first."],
    "lab_17": ["Open Lab 5 - HR Agent → Publish (the dialog shows Last published and the channel list) → Publish agent.",
               "Channels + → Teams + Microsoft 365 → Availability → Add channel → chip appears → Use and share → View in Teams → run the Lab 5 tests as a colleague.",
               "Share → add a classmate; they need the link AND access.",
               "Same channel → Use and share → View in Copilot (needs a Copilot licence on the user's side); Submit to org catalog is the admin-approval path.",
               "Open Lab 7 - Sales Agent → ••• → Settings → Safety & access → Authentication → No authentication (Done stays disabled; close ✕) → Save → Publish → the Demo website channel appears → View details → Open demo website.",
               "Optional: paste the embed <iframe> into an HTML page.",
               "On the HR agent, Channels + shows the Demo website tile greyed: Requires \"No authentication\" — do NOT switch it off.",
               "Deploy parents only; connected agents get no channel. Test as the user, in each door."],
}


def lab_banner_slide(lab_id):
    lab = LABS[lab_id]
    color = MODULE_COLOR[lab["module"]]

    def draw(s):
        img = lab_flowchart(lab_id)
        PAD, FULL_X, FULL_W = 0.10, 0.72, 11.85
        TOP, LEFT_BOTTOM = 1.72, 6.80

        # These flowcharts are extremely wide (aspect ratios 1.4:1 up to 14.5:1). In the 5.8in
        # side column a wide chart is always WIDTH-bound, so it renders as an unreadable strip
        # (Lab 8 drew 0.39in tall in a 4.88in card). Compare both layouts and take whichever
        # actually draws the image LARGER, so no lab is ever made smaller than it was.
        CHART_TOP, SIDE_X, SIDE_W, SIDE_MAX_H = 5.30, 6.77, 5.8, 5.08
        wide = False
        side_h = full_h = 0.0
        if img is not None:
            with Image.open(img) as _im:
                _iw, _ih = _im.size
            side_h = min((SIDE_W - 2 * PAD) * _ih / _iw, SIDE_MAX_H - 2 * PAD)
            full_h = min((FULL_W - 2 * PAD) * _ih / _iw, (LEFT_BOTTOM - CHART_TOP) - 2 * PAD)
            wide = full_h > side_h

        # A wide chart takes the full width, so the text column above it does too.
        lw = 11.85 if (img is None or wide) else 5.8

        chip(s, Inches(0.72), Inches(1.72), Inches(1.4), Inches(0.44), f"LAB {lab['number']}", color, 13)
        chip(s, Inches(2.25), Inches(1.72), Inches(1.3), Inches(0.44), f"{lab['duration_minutes']} MIN", GREY, 11)
        chip(s, Inches(3.68), Inches(1.72), Inches(1.3), Inches(0.44), f"DAY {lab['day']}", GREY, 11)
        text(s, Inches(0.72), Inches(2.28), Inches(lw), Inches(0.4), lab["subtitle"], 13, INK, True)

        if wide:
            # Compact the text stack so the chart gets the whole lower half of the slide. The
            # full-width cards are laid out with the compact style (label on its own line, body
            # tight beneath) so two-line bodies stay inside the card.
            card(s, Inches(0.72), Inches(2.72), Inches(lw), Inches(0.80), "What it teaches",
                 lab["teaches"], color, body_size=11, label_size=13, compact=True)
            card(s, Inches(0.72), Inches(3.60), Inches(lw), Inches(0.62), "Platform",
                 lab["platform"], TEAL, body_size=11, label_size=13, compact=True)
            names = lab.get("tenant_names") or ["(no tenant artefact — admin centre only)"]
            body = "  ·  ".join(names) + "\nTrainer copies end (DO NOT DELETE). Name yours plainly — agent names 30 characters or fewer."
            card(s, Inches(0.72), Inches(4.30), Inches(lw), Inches(0.98), "Tenant artefact names",
                 body, AMBER, body_size=10.5, label_size=13, compact=True)

            draw_h = full_h
            draw_w = draw_h * _iw / _ih
            # Bottom-align the band against the safe bottom so a short chart keeps its card
            # tight to the text above rather than leaving a gap.
            band_h = draw_h + 2 * PAD
            band_y = LEFT_BOTTOM - band_h
            box(s, Inches(FULL_X), Inches(band_y), Inches(FULL_W), Inches(band_h), LIGHT, LINE)
            pic_fit(s, img, Inches(FULL_X + (FULL_W - draw_w) / 2), Inches(band_y + PAD),
                    Inches(draw_w), Inches(draw_h))
        else:
            card(s, Inches(0.72), Inches(2.72), Inches(lw), Inches(1.35), "What it teaches",
                 lab["teaches"], color, body_size=11, label_size=13)
            card(s, Inches(0.72), Inches(4.18), Inches(lw), Inches(0.85), "Platform",
                 lab["platform"], TEAL, body_size=11, label_size=13, compact=True)
            names = lab.get("tenant_names") or ["(no tenant artefact — admin centre only)"]
            body = "  ·  ".join(names) + "\nTrainer copies end (DO NOT DELETE). Name yours plainly — agent names 30 characters or fewer."
            card(s, Inches(0.72), Inches(5.14), Inches(lw), Inches(1.66), "Tenant artefact names",
                 body, AMBER, body_size=10.5, label_size=13)
            if img is not None:
                # Near-square chart: keep the side column but shrink the card to the image so
                # it no longer floats in empty space.
                draw_h = side_h
                draw_w = draw_h * _iw / _ih
                box(s, Inches(SIDE_X), Inches(TOP), Inches(SIDE_W), Inches(draw_h + 2 * PAD), LIGHT, LINE)
                pic_fit(s, img, Inches(SIDE_X + (SIDE_W - draw_w) / 2), Inches(TOP + PAD),
                        Inches(draw_w), Inches(draw_h))
    return draw


def lab_steps_slide(lab_id):
    steps = STEPS.get(lab_id, [])[:8]
    color = MODULE_COLOR[LABS[lab_id]["module"]]

    def draw(s):
        n = len(steps)
        rows = (n + 1) // 2
        h = min(1.2, (5.1 - 0.14 * (rows - 1)) / rows)
        for i, st in enumerate(steps):
            col, row = divmod(i, 2) if n > 4 else (0, i)
            col, row = (i % 2, i // 2)
            x = Inches(0.72 + col * 6.05)
            y = Inches(1.72 + row * (h + 0.14))
            box(s, x, y, Inches(5.8), Inches(h), LIGHT, LINE)
            rect(s, x, y, Inches(0.09), Inches(h), color)
            oval(s, x + Inches(0.24), y + int(Inches(h) / 2) - Inches(0.23), Inches(0.46), Inches(0.46), color)
            text(s, x + Inches(0.24), y + int(Inches(h) / 2) - Inches(0.23), Inches(0.46), Inches(0.46), str(i + 1), 13, WHITE, True, PP_ALIGN.CENTER)
            text(s, x + Inches(0.85), y, Inches(4.85), Inches(h), st, 10.5, INK)
    return draw


def lab_screens_slide(lab_id, shots):
    def draw(s):
        n = len(shots)
        w = 11.85 if n == 1 else 5.8
        for i, p in enumerate(shots[:2]):
            x = Inches(0.72 + i * 6.05)
            box(s, x, Inches(1.72), Inches(w), Inches(4.6), LIGHT, LINE)
            pic_fit(s, p, x + Inches(0.1), Inches(1.82), Inches(w - 0.2), Inches(4.4))
            cap = re.sub(r"^[\w-]*?\d+-", "", p.stem).replace("-", " ").replace("_", " ").strip().capitalize()
            text(s, x, Inches(6.38), Inches(w), Inches(0.36), cap or p.stem, 11, GREY, False, PP_ALIGN.CENTER)
    return draw


def add_lab(lab_id):
    lab = LABS[lab_id]
    m = lab["module"]
    color = MODULE_COLOR[m]
    n = lab["number"]
    short = lab["title"].split("—", 1)[1].strip()
    slide(f"Lab {n} — {short}", f"module {m[1]} · lab {n} · hands-on", lab_banner_slide(lab_id), section=f"module_{m[1]}", module="", lab=lab_id, color=color)
    slide(f"Lab {n} — Build Steps", f"module {m[1]} · lab {n} · build", lab_steps_slide(lab_id), section=f"module_{m[1]}", color=color)
    shots = lab_screenshots(lab_id)
    if shots:
        slide(f"Lab {n} — What You Will See", f"module {m[1]} · lab {n} · screenshots", lab_screens_slide(lab_id, shots[:2]), section=f"module_{m[1]}", color=color)
    if len(shots) >= 4:
        slide(f"Lab {n} — What You Will See (continued)", f"module {m[1]} · lab {n} · screenshots", lab_screens_slide(lab_id, shots[2:4]), section=f"module_{m[1]}", color=color)


# ===========================================================================
# SEQUENCE
# ===========================================================================
A = "admin"
slide("", "", draw_cover, A)
slide("Digital Attendance (Mandatory)", "TRAQOM · SSG digital attendance", draw_attendance, A, color=TEAL)
slide("About the Trainer", "your trainer · general", trainer_draw("Your Trainer", "General Trainer template —\nto be completed by the trainer",
      [("Name", ""), ("Title / Designation", ""), ("Qualifications", ""), ("Areas of expertise", ""), ("Training & industry experience", ""), ("Contact", "")], "?", GREY), A, color=GREY)
slide("About the Trainer", "your trainer", trainer_draw("Dr. Alfred Ang", "Principal Trainer\nTertiary Infotech Academy Pte. Ltd.",
      [("Role", "Principal Trainer, Tertiary Infotech Academy Pte. Ltd."), ("Certification", "Microsoft Power Platform, AI and data analytics — 20+ years of training experience."),
       ("Delivers", "WSQ courses on AI, business automation, data science and software engineering."), ("Founder", "Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")], "AA", BLUE), A)
slide("Let's Know Each Other", "ice-breaker", draw_icebreaker, A)
slide("Ground Rules", "housekeeping", draw_ground_rules, A)
slide("Download Course Material", "course portal · lms-tms.tertiaryinfotech.com", draw_lms, A)
slide("Lesson Plan — Day 1", "schedule · 9:30am–6:30pm", schedule_draw(DAY1, "Day 1 — Automate, then add the agent", BLUE, 7), A)
slide("Lesson Plan — Day 2", "schedule · 9:30am–6:30pm", schedule_draw(DAY2, "Day 2 — Connect, supervise, ground, publish", VIOLET, 8), A, color=VIOLET)
slide("What You'll Learn", "learning outcomes", draw_outcomes, A)
slide("Briefing for Assessment", "before the assessment", draw_briefing, A)
slide("Assessment & Funding", "final assessment", draw_assessment_funding, A)
slide("Assessment Flow", "on assessment day", draw_assess_flow, A)

O = "course_overview"
slide("Eighteen Connected Labs — Day 1", "the journey · labs 0–8", journey_draw([f"lab_{i}" for i in range(0, 9)], "Day 1: build the workflow, add control flow and a human, then build four agents."), O)
slide("Eighteen Connected Labs — Day 2", "the journey · labs 9–17", journey_draw([f"lab_{i}" for i in range(9, 18)], "Day 2: agents and workflows call each other, go over HTTP, get grounded, and get published."), O)
slide("How This Course Works", "learning approach", draw_approach, O)
slide("Three Environments — Where You Build", "course environment", draw_environments, O)
slide("Naming Convention in the Tenant", "course environment", draw_naming, O)
slide("Your Training Account", "course environment", draw_training_account, O)
slide("Access the Hands-On Labs", "course repository", draw_repository, O)

M = "module_1"
slide("", "", divider("Module 1", "Business Process Automation and Power Automate",
      "What automation removes  ·  the Power Platform  ·  the new Copilot Studio  ·  workflows, triggers, actions, connections  ·  dynamic content, Activity, commit order  ·  Copilot Credits\nApplied in Lab 0, Lab 1 and Lab 2", BLUE), M, "m1")
for h, k, d in [("What Business Process Automation Removes", "module 1 · concept", draw_what_is_bpa),
                ("The Power Platform, and the Environment That Holds It", "module 1 · concept", draw_power_platform),
                ("The New Copilot Studio — Home, Agents, Workflows", "module 1 · concept", draw_new_home),
                ("Three Harnesses — Pick One per Agent", "module 1 · concept", draw_harnesses),
                ("Old Vocabulary → New Vocabulary", "module 1 · concept", draw_vocabulary),
                ("Anatomy of a Workflow — the Start Node and Its Triggers", "module 1 · concept", draw_workflow_anatomy),
                ("The Add-Step Palette", "module 1 · concept", draw_add_step),
                ("Triggers — What Is Allowed to Start a Process", "module 1 · concept", draw_trigger_types),
                ("Actions — The Six Families You Will Use", "module 1 · concept", draw_action_families),
                ("Connections — Who the Step Runs As", "module 1 · concept", draw_connections),
                ("Dynamic Content — The Token, Not the Text", "module 1 · concept", draw_dynamic_content),
                ("Activity, Run Details and Node-Level Testing", "module 1 · concept", draw_activity),
                ("Order Matters — Commit Before You Confirm", "module 1 · concept", draw_commit_order),
                ("Copilot Credits and Billing — What Changed on 1 September 2026", "module 1 · concept", draw_credits),
                ("Power Platform Admin Center — Settings for This Course", "module 1 · concept", draw_ppac),
                ("What's New in 2026 — The Timeline", "module 1 · concept", draw_timeline)]:
    slide(h, k, d, M, "m1")
for lid in ("lab_0", "lab_1", "lab_2"):
    add_lab(lid)

M = "module_2"
slide("", "", divider("Module 2", "Control Flow and Human in the Loop",
      "If/Else, Compose, Switch, Loop  ·  in / on / out of the loop  ·  Human review via Teams or Outlook  ·  the Classify node  ·  autonomous business processes\nApplied in Lab 3 and Lab 4", TEAL), M, "m2", color=TEAL)
for h, k, d in [("If/Else — Left Value, Operator, Right Value", "module 2 · concept", draw_ifelse),
                ("Conditions — Both Paths Must Exist", "module 2 · concept", draw_conditions),
                ("Compose, Function and Variable — Named Values", "module 2 · concept", draw_compose),
                ("Switch and Loop", "module 2 · concept", draw_switch_loop),
                ("Human In, On, and Out of the Loop", "module 2 · concept", draw_hitl_concept),
                ("Human Review — Teams or Outlook/Email?", "module 2 · concept", draw_hitl_channels),
                ("The Human Review Node — A Gate That Blocks", "module 2 · concept", draw_human_review_node),
                ("What Is a Control, and What Only Looks Like One", "module 2 · concept", draw_control_vs_not),
                ("How an Approval Suspends a Running Workflow", "module 2 · concept", draw_approval_mechanics),
                ("The Classify Node — Categories, Examples, Ports", "module 2 · concept", draw_classify),
                ("Email Classification — The Lab 4 Architecture", "module 2 · concept", draw_email_architecture),
                ("Autonomous Business Processes", "module 2 · concept", draw_autonomous)]:
    slide(h, k, d, M, "m2", color=TEAL)
for lid in ("lab_3", "lab_4"):
    add_lab(lid)

M = "module_3"
slide("", "", divider("Module 3", "Copilot Studio Agents",
      "The designer  ·  instructions, model, knowledge  ·  skills, tools, MCP  ·  what is enforced  ·  connected agents, memory  ·  Preview, Evaluate, Monitor  ·  publishing and channels\nApplied in Labs 5–11 and Lab 17", VIOLET), M, "m3", color=VIOLET)
for h, k, d in [("Workflow or Agent — They Fail Differently", "module 3 · concept", draw_workflow_vs_agent),
                ("The Agent Designer — Build, Preview, Evaluate, Monitor", "module 3 · concept", draw_designer),
                ("Inside the Build Tab", "module 3 · concept", draw_build_panel),
                ("Natural-Language Authoring (Preview)", "module 3 · concept", draw_nl_authoring),
                ("Writing Instructions That Constrain", "module 3 · concept", draw_instructions_craft),
                ("Worked Example — The HR Agent Instructions", "module 3 · concept", draw_hr_example),
                ("The Instructions Box Is a Rich-Text Editor", "module 3 · concept", draw_instructions_gotcha),
                ("Choosing the Model", "module 3 · concept", draw_model),
                ("Knowledge — Giving Facts and Removing Sources", "module 3 · concept", draw_knowledge),
                ("Richer Context — Microsoft IQ, Work IQ, Foundry IQ — and Citations", "module 3 · concept", draw_iq_citations),
                ("Skills — Instructions on Demand (SKILL.md)", "module 3 · concept", draw_skills),
                ("Anatomy of a Skill Package", "module 3 · concept", draw_skill_package),
                ("When a Skill Fires", "module 3 · concept", draw_skills_fire),
                ("Tools — Connectors, Workflows, MCP Servers", "module 3 · concept", draw_tools),
                ("A Workflow as a Tool", "module 3 · concept", draw_workflow_as_tool),
                ("MCP — Model Context Protocol Servers", "module 3 · concept", draw_mcp),
                ("Tools vs Skills vs MCP", "module 3 · concept", draw_tools_skills_mcp),
                ("Which Parts of an Agent Hold — and Which Do Not", "module 3 · concept", draw_enforcement),
                ("Connected Agents", "module 3 · concept", draw_connected_agents),
                ("Multi-Agent Orchestration — The Content Team", "module 3 · concept", draw_multi_agent),
                ("Reference Architecture — BlastBox Omega", "module 3 · concept", draw_blastbox),
                ("Memory (Preview) and Its Limits", "module 3 · concept", draw_memory),
                ("The Preview Tab and Four Ways to Test", "module 3 · concept", draw_preview_testing),
                ("The Evaluate Tab", "module 3 · concept", draw_evaluate),
                ("Monitor and Share", "module 3 · concept", draw_monitor_share),
                ("Publishing — Preview Is Not Published", "module 3 · concept", draw_publishing),
                ("Channels — Teams, Microsoft 365 Copilot, Web, SharePoint", "module 3 · concept", draw_channels),
                ("Authentication Settings and Entra Agent ID", "module 3 · concept", draw_auth_agentid),
                ("Calling an Agent from a Workflow — The Agent Node", "module 3 · concept", draw_agent_from_workflow),
                ("Calling a Workflow from an Agent", "module 3 · concept", draw_workflow_from_agent),
                ("Worked Agent 1 — HR Agent", "module 3 · worked example", HR_AGENT),
                ("Worked Agent 2 — Procurement Agent", "module 3 · worked example", PROCUREMENT_AGENT),
                ("Worked Agent 3 — Sales Agent", "module 3 · worked example", SALES_AGENT),
                ("Worked Agent 4 — IT Support Agent", "module 3 · worked example", IT_AGENT)]:
    slide(h, k, d, M, "m3", color=VIOLET)
for lid in ("lab_5", "lab_6", "lab_7", "lab_8", "lab_9", "lab_10", "lab_11"):
    add_lab(lid)

M = "module_4"
slide("", "", divider("Module 4", "Workflows, HTTP, Autonomous Processes and the Boundary of Agency",
      "The HTTP trigger, GET vs POST, the generated URL  ·  schema, Response, status codes  ·  structured output  ·  Compose and the master record  ·  the human review gate over HTTP\nApplied in Lab 12, Lab 13 and Lab 14", GREEN), M, "m4", color=GREEN)
for h, k, d in [("Agentic Workflows over HTTP", "module 4 · concept", draw_http_pattern),
                ("The HTTP Trigger — When a HTTP Request Is Received", "module 4 · concept", draw_http_trigger),
                ("GET vs POST", "module 4 · concept", draw_get_vs_post),
                ("The Request Body JSON Schema", "module 4 · concept", draw_json_schema),
                ("How the Trigger URL Is Generated", "module 4 · concept", draw_url_generated),
                ("The Response Node and Status Codes", "module 4 · concept", draw_response_status),
                ("Calling It from a Browser — fetch and CORS", "module 4 · concept", draw_fetch_cors),
                ("Structured Output vs Parse JSON", "module 4 · concept", draw_structured_output),
                ("The Boundary of Agency", "module 4 · concept", draw_boundary_of_agency),
                ("Compose Normalises — Master Data Comes from Compose", "module 4 · concept", draw_compose_master),
                ("Duplicate Lookup — SharePoint Get Items with a Filter Query", "module 4 · concept", draw_duplicate_lookup),
                ("The Agent Alone, in Public", "module 4 · concept", draw_agent_alone),
                ("The Human Review Gate over HTTP", "module 4 · concept", draw_http_gate),
                ("Four Decisions, Not Two", "module 4 · concept", draw_four_decisions),
                ("Test Probes for Labs 12–14", "module 4 · concept", draw_test_probes)]:
    slide(h, k, d, M, "m4", color=GREEN)
for lid in ("lab_12", "lab_13", "lab_14"):
    add_lab(lid)

M = "module_5"
slide("", "", divider("Module 5", "Retrieval Augmented Generation",
      "Why retrieval  ·  ingest, chunk, embed, index, retrieve, generate  ·  Knowledge source vs Pinecone  ·  embeddings, dimension, top_k  ·  citation markers  ·  probing for invention\nApplied in Lab 15 and Lab 16", AMBER), M, "m5", color=AMBER)
for h, k, d in [("Why Retrieval, Rather Than a Bigger Prompt", "module 5 · concept", draw_why_rag),
                ("The RAG Pipeline, and the Four Words That Matter", "module 5 · concept", draw_rag_pipeline),
                ("Knowledge Source or Your Own Vector Store — The Levers", "module 5 · concept", draw_rag_compare),
                ("Embeddings, Dimension and top_k", "module 5 · concept", draw_embeddings),
                ("Citation Markers", "module 5 · concept", draw_citations),
                ("Probing for Invention", "module 5 · concept", draw_hallucination),
                ("Choosing", "module 5 · concept", draw_rag_choosing)]:
    slide(h, k, d, M, "m5", color=AMBER)
for lid in ("lab_15", "lab_16"):
    add_lab(lid)

# Lab 17 closes the course — it is a Module 3 topic (channels and publishing) but is
# TAUGHT LAST, after the RAG labs, exactly as the Lesson Plan schedules it and the
# Learner Guide orders it. Keep it here; grouping it with the Module 3 labs makes the
# deck jump Lab 11 -> Lab 17 -> Lab 12 and contradicts the LP and LG.
add_lab("lab_17")

S = "synthesis"
slide("", "", divider("Synthesis", "Taking This Back to Work",
      "Controls versus conventions  ·  the eighteen-lab recap  ·  the pre-production checklist  ·  further reading  ·  six sentences worth keeping", VIOLET), S, color=VIOLET)
for h, k, d in [("Controls versus Conventions", "synthesis", draw_controls_vs_conventions),
                ("Eighteen Labs in One Slide", "synthesis", draw_recap_labs),
                ("Before Anything Reaches Production", "synthesis", draw_before_production),
                ("Further Reading — The Six Sources", "synthesis", draw_further_reading),
                ("Six Sentences Worth Keeping", "synthesis", draw_six_sentences)]:
    slide(h, k, d, S, color=VIOLET)

C = "assessment_and_closing"
slide("Briefing for Assessment", "before the assessment", draw_briefing, C)
slide("Assessment", "final assessment", draw_assessment_end, C)
slide("Assessment Flow", "on assessment day", draw_assess_flow, C)
slide("Practice Exam", "test yourself", draw_practice_exam, C)
slide("Digital Attendance (Mandatory)", "TRAQOM · SSG digital attendance", draw_attendance, C, color=TEAL)
slide("", "", draw_thanks, C)


# ===========================================================================
# BUILD
# ===========================================================================
for i, spec in enumerate(SLIDES, 1):
    s = prs.slides.add_slide(BLANK)
    if spec["heading"]:
        title(s, spec["heading"], spec["kicker"], spec["color"])
    spec["draw"](s)
    footer(s, i)

# Archive the previous build of THIS version too (same filename, older content) before overwriting it,
# so no published deck is ever lost: courseware/archive/<name>-v8.0-<YYYYMMDD-HHMM>.pptx/.pdf
import shutil, datetime
_ARCH = CW / "archive"; _ARCH.mkdir(exist_ok=True)
for _prev in (DECK, DECK.with_suffix(".pdf")):
    if _prev.exists():
        _stamp = datetime.datetime.fromtimestamp(_prev.stat().st_mtime).strftime("%Y%m%d-%H%M")
        _target = _ARCH / f"{_prev.stem}-{_stamp}{_prev.suffix}"
        shutil.copy2(_prev, _target)
        print(f"archived previous {_prev.name} -> archive/{_target.name}")
prs.save(DECK)
print(f"Saved {DECK.name} with {len(prs.slides)} slides")

# Archive superseded deck versions (idempotent: overwrite an existing archive copy).
import shutil
ARCHIVE = CW / "archive"
ARCHIVE.mkdir(exist_ok=True)
for old in list(CW.glob(f"{TITLE}-v*.pptx")) + list(CW.glob(f"{TITLE}-v*.pdf")):
    if f"-v{VERSION}." in old.name:
        continue
    target = ARCHIVE / old.name
    if target.exists():
        target.unlink()
    shutil.move(str(old), str(target))
    print(f"archived {old.name}")

# ------------------------------------------------------------------ slide map
def span(nums):
    return f"{min(nums)}-{max(nums)}" if nums else ""

sections, modules, labs = {}, {}, {}
for i, spec in enumerate(SLIDES, 1):
    sections.setdefault(spec["section"], []).append(i)
    if spec["module"]:
        modules.setdefault(spec["module"], []).append(i)
    if spec["lab"]:
        labs[spec["lab"]] = str(i)
slide_map = {
    "version": VERSION,
    "deck": DECK.name,
    "slides": len(SLIDES),
    "sections": {k: span(v) for k, v in sections.items()},
    "modules": {k: span(modules[k]) for k in ("m1", "m2", "m3", "m4", "m5") if k in modules},
    "labs": {f"lab_{n}": labs[f"lab_{n}"] for n in range(18) if f"lab_{n}" in labs},
}
SLIDE_MAP.write_text(json.dumps(slide_map, indent=2) + "\n", encoding="utf-8")
print(json.dumps(slide_map, indent=2))
for i, spec in enumerate(SLIDES, 1):
    print(f"{i:3d}  [{spec['section']:22s}] {spec['heading'] or '(divider / cover / close)'}")
