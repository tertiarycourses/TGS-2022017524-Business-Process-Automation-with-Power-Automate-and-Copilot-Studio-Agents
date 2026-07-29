#!/usr/bin/env python3
"""Build the Version 6.0 facilitator deck from the reviewed Version 5.2 deck.

Administrative and assessment slides remain in place. Slides 15–108 are rebuilt
as a concept-first sequence that leads into the canonical ten labs.
"""

from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
SOURCE_NAME = (
    "Business Process Automation with Power Automate and Copilot Studio Agents-v5.2.pptx"
)
SOURCE = ROOT / "courseware" / "archive" / SOURCE_NAME
if not SOURCE.exists():
    SOURCE = ROOT / "courseware" / SOURCE_NAME
DECK = ROOT / "courseware" / (
    "Business Process Automation with Power Automate and Copilot Studio Agents-v6.0.pptx"
)
with open(ROOT / "courseware" / "alignment_manifest.json", encoding="utf-8") as fh:
    ALIGNMENT = json.load(fh)
assert ALIGNMENT["version"] == "6.0"
LAB_META = {lab["id"]: lab for lab in ALIGNMENT["labs"]}
if SOURCE.exists():
    copy2(SOURCE, DECK)
elif not DECK.exists():
    raise FileNotFoundError(f"Neither source nor output deck exists: {SOURCE} / {DECK}")

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


prs = Presentation(DECK)
SW, SH = prs.slide_width, prs.slide_height

# Add 27 content slots, then move the inherited five-slide assessment/closing
# block from 82–86 to 109–113. This preserves the reviewed WSQ admin pages while
# creating room for concept-first instruction before every lab.
while len(prs.slides) < 113:
    prs.slides.add_slide(prs.slide_layouts[6])
for _ in range(5):
    slide_id = prs.slides._sldIdLst[81]
    prs.slides._sldIdLst.remove(slide_id)
    prs.slides._sldIdLst.append(slide_id)


def clear(slide):
    tree = slide.shapes._spTree
    for shape in list(slide.shapes):
        tree.remove(shape._element)


def box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=True):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        x,
        y,
        w,
        h,
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(1.2)
    return shape


def text(
    slide,
    x,
    y,
    w,
    h,
    value,
    size=18,
    color=INK,
    bold=False,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.MIDDLE,
    margin=0.08,
):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = value
    r.font.name = "Arial"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    return tb


def title(slide, heading, kicker):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.22), Inches(1.48))
    shape.fill.solid()
    shape.fill.fore_color.rgb = BLUE
    shape.line.fill.background()
    text(slide, Inches(0.72), Inches(0.38), Inches(11.8), Inches(0.28), kicker.upper(), 12, BLUE, True)
    text(slide, Inches(0.72), Inches(0.72), Inches(11.8), Inches(0.62), heading, 29, INK, True)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(1.5), Inches(11.85), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE
    line.line.fill.background()


def footer(slide, slide_no):
    text(
        slide,
        Inches(0.72),
        Inches(7.1),
        Inches(11.85),
        Inches(0.2),
        f"Business Process Automation with Power Automate and Copilot Studio Agents   |   {slide_no}",
        8,
        GREY,
        False,
        PP_ALIGN.RIGHT,
    )


def card(slide, x, y, w, h, label, body, accent=BLUE, number=None, body_size=14, label_size=17):
    box(slide, x, y, w, h, LIGHT, LINE)
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.09), h)
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()
    if number is not None:
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.22), y + Inches(0.22), Inches(0.5), Inches(0.5))
        circle.fill.solid()
        circle.fill.fore_color.rgb = accent
        circle.line.fill.background()
        text(slide, x + Inches(0.22), y + Inches(0.22), Inches(0.5), Inches(0.5), str(number), 16, WHITE, True, PP_ALIGN.CENTER)
        lx = x + Inches(0.84)
        lw = w - Inches(1.05)
    else:
        lx = x + Inches(0.28)
        lw = w - Inches(0.52)
    text(slide, lx, y + Inches(0.16), lw, Inches(0.45), label, label_size, accent, True)
    text(slide, x + Inches(0.28), y + Inches(0.7), w - Inches(0.52), h - Inches(0.82), body, body_size, GREY)


def arrow(slide, x, y, w=0.42, h=0.38, color=BLUE, direction="right"):
    kind = MSO_SHAPE.CHEVRON if direction == "right" else MSO_SHAPE.DOWN_ARROW
    shape = slide.shapes.add_shape(kind, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def flow(slide, y, nodes, labels=None, colors=None, x0=0.72, total=11.85, height=1.15):
    labels = labels or [""] * (len(nodes) - 1)
    colors = colors or [BLUE] * len(nodes)
    gap = 0.46
    node_w = (total - gap * (len(nodes) - 1)) / len(nodes)
    for i, node in enumerate(nodes):
        x = Inches(x0 + i * (node_w + gap))
        box(slide, x, Inches(y), Inches(node_w), Inches(height), WHITE, colors[i])
        text(slide, x + Inches(0.08), Inches(y + 0.08), Inches(node_w - 0.16), Inches(height - 0.16), node, 13, INK, True, PP_ALIGN.CENTER)
        if i < len(nodes) - 1:
            ax = x + Inches(node_w + 0.06)
            arrow(slide, ax, Inches(y + height / 2 - 0.17), Inches(0.3), Inches(0.34), colors[i])
            if labels[i]:
                text(slide, x + Inches(node_w - 0.12), Inches(y - 0.28), Inches(gap + 0.24), Inches(0.25), labels[i], 9, GREY, False, PP_ALIGN.CENTER)


def rebuild(slide_no, heading, kicker, draw):
    slide = prs.slides[slide_no - 1]
    clear(slide)
    title(slide, heading, kicker)
    draw(slide)
    footer(slide, slide_no)


def draw_course_outcomes(s):
    flow(s, 2.05, ["Power Automate\nflows", "Copilot Studio\nagent", "Teams + website\nchannels", "Agent tools\nand prompts"], ["add AI", "publish", "take action"], [BLUE, VIOLET, TEAL, AMBER], height=1.35)
    card(s, Inches(0.72), Inches(4.05), Inches(3.65), Inches(1.8), "Day 1 — automate", "Build reliable trigger → action flows without an AI agent.", BLUE)
    card(s, Inches(4.65), Inches(4.05), Inches(3.65), Inches(1.8), "Day 2 — converse", "Create a grounded agent that understands and confirms user intent.", VIOLET)
    card(s, Inches(8.58), Inches(4.05), Inches(3.99), Inches(1.8), "Integrate — act", "Let the agent call deterministic or prompt-based Power Automate tools.", TEAL)


def draw_journey(s):
    items = [
        ("1–2", "Instant", "Run manually; email and Excel"),
        ("3", "Scheduled", "Recurrence and time zone"),
        ("4", "Automated", "Microsoft Forms event"),
        ("5", "Approval", "Human decision and branch"),
        ("6A/B", "HTTP", "External JSON request/response"),
        ("7A", "Agent", "Instructions and safe behaviour"),
        ("7B", "RAG", "Retrieve approved knowledge"),
        ("8", "Channels", "Publish to Teams and website"),
        ("9", "Agent flow", "Deterministic tool call"),
        ("10", "Prompt flow", "Guarded AI generation"),
    ]
    for i, (num, label, body) in enumerate(items):
        row, col = divmod(i, 5)
        x = Inches(0.72 + col * 2.42)
        y = Inches(1.9 + row * 2.35)
        card(s, x, y, Inches(2.12), Inches(1.92), label, body, PALETTE[i % 5], num, 11, 12)
    text(s, Inches(0.72), Inches(6.54), Inches(11.85), Inches(0.34), "Each lab reuses the previous capability; complexity increases one controlled step at a time.", 14, INK, True, PP_ALIGN.CENTER)


def draw_trigger_spectrum(s):
    types = [
        ("Instant", "A person presses Run", "Labs 1–2", BLUE),
        ("Scheduled", "A clock reaches a timetable", "Lab 3", TEAL),
        ("Automated", "An event occurs", "Lab 4", VIOLET),
        ("Agent flow", "A Copilot agent calls a tool", "Labs 9–10", AMBER),
    ]
    for i, (label, body, lab, color) in enumerate(types):
        x = Inches(0.72 + i * 3.0)
        card(s, x, Inches(1.9), Inches(2.72), Inches(2.1), label, f"{body}\n\n{lab}", color, i + 1, 13)
    card(s, Inches(1.55), Inches(4.55), Inches(4.9), Inches(1.55), "Human-in-the-loop pattern", "Lab 5 pauses a running flow until a person approves or rejects.", RED)
    card(s, Inches(6.82), Inches(4.55), Inches(4.9), Inches(1.55), "HTTP request pattern", "Labs 6A–6B let an external website POST JSON and receive JSON back.", GREEN)


def draw_trigger_map(s):
    flow(s, 2.15, ["Person\npresses Run", "Clock\nrecurs", "Form\nyields event", "Website\nPOSTs JSON", "Copilot agent\ncalls tool"], ["instant", "scheduled", "automated", "HTTP"], [BLUE, TEAL, VIOLET, GREEN, AMBER], height=1.4)
    text(s, Inches(0.72), Inches(4.25), Inches(11.85), Inches(0.48), "One trigger starts a flow. The actions may stay the same even when the trigger changes.", 19, INK, True, PP_ALIGN.CENTER)
    flow(s, 5.05, ["Trigger", "Validate data", "Business actions", "Return or notify"], ["starts", "then", "finish"], [BLUE, BLUE, TEAL, AMBER], x0=2.0, total=9.2, height=1.0)


def draw_approval(s):
    flow(s, 2.0, ["Request submitted", "Start and wait\nfor approval", "Human approves\nor rejects", "Condition reads\nOutcome"], ["pause", "decision", "resume"], [BLUE, RED, RED, VIOLET], height=1.35)
    card(s, Inches(1.15), Inches(4.25), Inches(5.25), Inches(1.45), "If yes — Approve", "Send the approved message and continue the business process.", GREEN)
    card(s, Inches(6.85), Inches(4.25), Inches(5.25), Inches(1.45), "If no — Reject", "Send the rejected message and stop or return for changes.", RED)
    text(s, Inches(0.72), Inches(6.08), Inches(11.85), Inches(0.48), "The automation is still deterministic; the person supplies the decision.", 16, INK, True, PP_ALIGN.CENTER)


def draw_day1_labs(s):
    flow(s, 2.05, ["Labs 1–2\nInstant", "Lab 3\nScheduled", "Lab 4\nAutomated", "Lab 5\nApproval", "Labs 6A–B\nHTTP"], ["add time", "add event", "add person", "add external caller"], [BLUE, TEAL, VIOLET, RED, GREEN], height=1.35)
    text(s, Inches(0.72), Inches(4.05), Inches(11.85), Inches(0.42), "DAY 1 BUILDS THE AUTOMATION ENGINE", 14, BLUE, True, PP_ALIGN.CENTER)
    card(s, Inches(1.0), Inches(4.65), Inches(3.45), Inches(1.45), "Trigger", "What starts the process?", BLUE)
    card(s, Inches(4.95), Inches(4.65), Inches(3.45), Inches(1.45), "Actions", "What work should happen?", TEAL)
    card(s, Inches(8.9), Inches(4.65), Inches(3.45), Inches(1.45), "Outputs", "What result must be stored or returned?", AMBER)


def draw_lab_instant(s):
    flow(s, 2.15, ["Learner prompt", "Copilot draft", "Manual trigger", "Send email", "Inbox"], ["generate", "review", "dynamic data", "deliver"], [VIOLET, VIOLET, BLUE, TEAL, AMBER], height=1.35)
    card(s, Inches(1.0), Inches(4.35), Inches(5.25), Inches(1.45), "Concept", "An instant flow runs only when a person deliberately starts it.", BLUE)
    card(s, Inches(6.75), Inches(4.35), Inches(5.25), Inches(1.45), "Workplace use", "A service officer acknowledges a verified phone or counter enquiry within 15 minutes.", TEAL)


def draw_lab_excel(s):
    flow(s, 2.15, ["Press Run", "Enter enquiry fields", "Map table columns", "Add Excel row", "Verify run history"], ["inputs", "dynamic content", "write", "check"], [BLUE, BLUE, TEAL, GREEN, AMBER], height=1.35)
    card(s, Inches(1.0), Inches(4.35), Inches(5.25), Inches(1.45), "Concept", "Actions consume outputs from the trigger as structured dynamic content.", BLUE)
    card(s, Inches(6.75), Inches(4.35), Inches(5.25), Inches(1.45), "Workplace use", "The shared enquiry register gives supervisors one visible queue and a basic audit trail.", GREEN)


def draw_lab_scheduled(s):
    flow(s, 2.15, ["Recurrence", "Weekdays", "Singapore time", "Send reminder", "Team inbox"], ["configure", "select", "fire", "deliver"], [TEAL, TEAL, BLUE, VIOLET, AMBER], height=1.35)
    card(s, Inches(1.0), Inches(4.35), Inches(5.25), Inches(1.45), "Workplace use", "At 9 AM on weekdays, the team lead reminds officers to clear records still marked New.", TEAL)
    card(s, Inches(6.75), Inches(4.35), Inches(5.25), Inches(1.45), "Critical setting", "Always set the business time zone; recurrence defaults can otherwise use UTC.", RED)


def draw_lab_automated(s):
    flow(s, 2.05, ["Customer submits\nMicrosoft Form", "New response\ntrigger", "Get response\ndetails", "Send email", "Add Excel row"], ["event", "Response Id", "fan out", "log"], [VIOLET, VIOLET, BLUE, TEAL, GREEN], height=1.5)
    card(s, Inches(1.0), Inches(4.5), Inches(5.25), Inches(1.45), "Workplace use", "A customer form creates the service email and audit row without staff re-keying.", VIOLET)
    card(s, Inches(6.75), Inches(4.5), Inches(5.25), Inches(1.45), "Data pattern", "Get response details turns the response ID into fields that email and Excel can use.", BLUE)


def draw_lab_approval_http(s):
    card(s, Inches(0.72), Inches(1.9), Inches(3.65), Inches(4.7), "Lab 5 — Laptop approval", "SGD 1,850 request\n↓\nManager decides\n↓\nApprove / Reject\n↓\nNotify requester", RED, 5, 15)
    card(s, Inches(4.72), Inches(1.9), Inches(3.65), Inches(4.7), "Lab 6A — Website enquiry", "Business-banking form\n↓\nPOST JSON\n↓\nNotify operations\n↓\nConfirm on page", GREEN, "6A", 15)
    card(s, Inches(8.72), Inches(1.9), Inches(3.65), Inches(4.7), "Lab 6B — Service widget", "Customer question\n↓\nApproved routes\n↓\nSafe fallback\n↓\nReturn bot reply", BLUE, "6B", 15)


def draw_day1_recap(s):
    rows = [
        ("Instant", "Person presses Run", "Labs 1–2", "Learn actions and data mapping"),
        ("Scheduled", "Recurrence", "Lab 3", "Run by the clock"),
        ("Automated", "Forms event", "Lab 4", "React to a business event"),
        ("Approval", "Flow pauses for a person", "Lab 5", "Add human judgement"),
        ("HTTP", "External JSON request", "Labs 6A–B", "Connect a website or system"),
    ]
    for i, (kind, trigger, lab, purpose) in enumerate(rows):
        y = Inches(1.82 + i * 0.94)
        box(s, Inches(0.72), y, Inches(11.85), Inches(0.75), LIGHT, LINE)
        text(s, Inches(0.92), y, Inches(1.55), Inches(0.75), kind, 15, PALETTE[i], True)
        text(s, Inches(2.55), y, Inches(3.0), Inches(0.75), trigger, 13, INK)
        text(s, Inches(5.75), y, Inches(1.35), Inches(0.75), lab, 13, BLUE, True, PP_ALIGN.CENTER)
        text(s, Inches(7.25), y, Inches(5.0), Inches(0.75), purpose, 13, GREY)


def draw_day2_roadmap(s):
    flow(s, 2.05, ["Lab 7A\nAgent shell", "Lab 7B\nRAG knowledge", "Lab 8\nTeams + website", "Lab 9\nAgent flow", "Lab 10\nPrompt flow"], ["ground", "publish", "take action", "generate"], [VIOLET, BLUE, TEAL, GREEN, AMBER], height=1.5)
    text(s, Inches(0.72), Inches(4.2), Inches(11.85), Inches(0.42), "DAY 2 ADDS THE CONVERSATIONAL ORCHESTRATOR", 14, VIOLET, True, PP_ALIGN.CENTER)
    card(s, Inches(1.0), Inches(4.75), Inches(3.45), Inches(1.35), "Understand", "Instructions and confirmed user intent", VIOLET)
    card(s, Inches(4.95), Inches(4.75), Inches(3.45), Inches(1.35), "Ground", "Retrieve approved facts with RAG", BLUE)
    card(s, Inches(8.9), Inches(4.75), Inches(3.45), Inches(1.35), "Act", "Call Power Automate as a tool", GREEN)


def draw_agent_flow_arch(s):
    flow(s, 2.0, ["User", "Copilot Studio\nagent", "Power Automate\nagent flow", "Business systems", "Respond to\nthe agent"], ["chat", "tool call", "actions", "outputs"], [TEAL, VIOLET, GREEN, BLUE, AMBER], height=1.45)
    card(s, Inches(0.85), Inches(4.35), Inches(3.5), Inches(1.45), "Agent = brain and mouth", "Understands, asks, confirms and chooses a tool.", VIOLET)
    card(s, Inches(4.9), Inches(4.35), Inches(3.5), Inches(1.45), "Flow = hands", "Logs, emails, approves, calls APIs and applies rules.", GREEN)
    card(s, Inches(8.95), Inches(4.35), Inches(3.5), Inches(1.45), "Return value = answer", "Reference, decision or draft comes back into chat.", AMBER)


def draw_n8n_mapping(s):
    mappings = [
        ("Chat Trigger", "Teams / website channel"),
        ("AI Agent node", "Copilot Studio agent"),
        ("System prompt", "Agent Instructions"),
        ("Vector / RAG tool", "Agent Knowledge"),
        ("Workflow tool", "Power Automate agent flow"),
        ("Tool result", "Respond to the agent"),
    ]
    text(s, Inches(0.88), Inches(1.82), Inches(4.9), Inches(0.35), "n8n AI-agent pattern", 17, INK, True, PP_ALIGN.CENTER)
    text(s, Inches(7.48), Inches(1.82), Inches(4.9), Inches(0.35), "Microsoft equivalent", 17, INK, True, PP_ALIGN.CENTER)
    for i, (left, right) in enumerate(mappings):
        y = Inches(2.35 + i * 0.66)
        box(s, Inches(0.88), y, Inches(4.9), Inches(0.5), LIGHT, LINE)
        text(s, Inches(1.05), y, Inches(4.55), Inches(0.5), left, 12, GREY, i == 1)
        arrow(s, Inches(6.18), y + Inches(0.07), Inches(0.7), Inches(0.36), PALETTE[i % 5])
        box(s, Inches(7.48), y, Inches(4.9), Inches(0.5), WHITE, PALETTE[i % 5])
        text(s, Inches(7.65), y, Inches(4.55), Inches(0.5), right, 12, INK, i == 1)


def draw_day2_labs(s):
    flow(s, 2.0, ["7A\nCreate agent", "7B\nAdd RAG", "8\nDeploy channels", "9\nAgent flow", "10\nPrompt flow"], ["facts", "reach users", "deterministic action", "controlled AI"], [VIOLET, BLUE, TEAL, GREEN, AMBER], height=1.55)
    card(s, Inches(0.95), Inches(4.45), Inches(3.55), Inches(1.45), "Build or configure", "Create the agent and inspect every generated instruction.", VIOLET)
    card(s, Inches(4.9), Inches(4.45), Inches(3.55), Inches(1.45), "Test evidence", "Use positive, negative and unsupported questions.", BLUE)
    card(s, Inches(8.85), Inches(4.45), Inches(3.55), Inches(1.45), "Publish safely", "Validate in Preview before Teams or website channels.", TEAL)


def draw_lab_agent(s):
    flow(s, 2.05, ["Natural-language\nrequirement", "Generated agent", "Review\nInstructions", "Preview and test", "Refine and save"], ["create", "inspect", "exercise", "improve"], [VIOLET, VIOLET, BLUE, TEAL, AMBER], height=1.45)
    card(s, Inches(1.0), Inches(4.45), Inches(5.25), Inches(1.4), "Workplace role", "First-line IT support for password, MFA, VPN and service-desk escalation.", VIOLET)
    card(s, Inches(6.75), Inches(4.45), Inches(5.25), Inches(1.4), "What it does not have yet", "No approved internal facts and no Power Automate tool.", GREY)


def draw_lab_rag(s):
    flow(s, 2.05, ["User question", "Agent searches", "Approved IT FAQ", "Retrieve passage", "Grounded answer\n+ citation"], ["query", "knowledge", "evidence", "generate"], [TEAL, VIOLET, BLUE, BLUE, GREEN], height=1.45)
    card(s, Inches(1.0), Inches(4.45), Inches(5.25), Inches(1.4), "Evidence found", "Give the approved VPN, password or security procedure and cite the FAQ.", GREEN)
    card(s, Inches(6.75), Inches(4.45), Inches(5.25), Inches(1.4), "No authority", "Refuse access approvals and route the employee to the Service Desk.", RED)


def draw_lab_channels(s):
    card(s, Inches(0.72), Inches(1.9), Inches(5.65), Inches(4.55), "Part A — Copilot agent in Teams", "User chats in Teams\n↓\nCopilot Studio agent\n↓\nGrounded conversation\n↓\nAnswer in Teams", VIOLET, "A", 16)
    card(s, Inches(6.92), Inches(1.9), Inches(5.65), Inches(4.55), "Part B — Website calls deterministic flow", "Website enquiry form\n↓\nHTTP POST\n↓\nDeterministic Power Automate\n↓\nJSON result on page", GREEN, "B", 16)
    text(s, Inches(0.72), Inches(6.55), Inches(11.85), Inches(0.28), "Comparison: Part B is automation only—the agent is not in that submission path yet.", 13, RED, True, PP_ALIGN.CENTER)


def draw_lab_agent_flow(s):
    flow(s, 2.0, ["Teams or website\nchat", "Copilot agent\nconfirms inputs", "Agent flow tool", "Deterministic\nconditions", "Respond to\nagent", "Answer in chat"], ["chat", "call", "evaluate", "outputs", "present"], [TEAL, VIOLET, GREEN, BLUE, AMBER, TEAL], height=1.4)
    card(s, Inches(1.0), Inches(4.35), Inches(5.25), Inches(1.45), "Same as n8n AI Agent + workflow tool", "The agent decides when to call the tool; the flow executes predictable business rules.", VIOLET)
    card(s, Inches(6.75), Inches(4.35), Inches(5.25), Inches(1.45), "Required endpoints", "When an agent calls the flow → actions → Respond to the agent.", GREEN)


def draw_lab_prompt_flow(s):
    flow(s, 1.95, ["Confirmed enquiry", "Agent calls\nprompt flow", "AI Builder\nRun a prompt", "Parse + validate\nstructured JSON", "Guardrail decision", "Respond to\nagent"], ["tool", "generate", "schema", "check", "safe output"], [VIOLET, GREEN, AMBER, BLUE, RED, TEAL], height=1.45)
    card(s, Inches(1.0), Inches(4.35), Inches(5.25), Inches(1.5), "Use AI where language varies", "Draft, classify or summarise—but keep approvals, identity checks and limits deterministic.", AMBER)
    card(s, Inches(6.75), Inches(4.35), Inches(5.25), Inches(1.5), "Validate before returning", "Parse the schema, check safety rules and fall back when the output is missing or unsafe.", RED)


def draw_compare(s):
    columns = [
        ("Lab 8", "Ordinary flow", "Website HTTP request", "No agent in path", "JSON to webpage", GREEN),
        ("Lab 9", "Agent flow", "Agent tool call", "Deterministic rules", "Structured result to chat", VIOLET),
        ("Lab 10", "Prompt flow", "Agent tool call", "AI prompt + guardrails", "Controlled draft to chat", AMBER),
    ]
    for i, (lab, kind, trigger, processing, result, color) in enumerate(columns):
        x = Inches(0.72 + i * 4.0)
        card(s, x, Inches(1.9), Inches(3.7), Inches(4.65), f"{lab} — {kind}", f"TRIGGER\n{trigger}\n\nPROCESSING\n{processing}\n\nRETURN\n{result}", color, i + 8, 13)


def draw_day2_recap(s):
    flow(s, 1.95, ["Instructions", "Knowledge (RAG)", "Channels", "Tools", "Prompt + guardrails"], ["ground", "publish", "act", "generate"], [VIOLET, BLUE, TEAL, GREEN, AMBER], height=1.35)
    text(s, Inches(0.72), Inches(3.75), Inches(11.85), Inches(0.48), "THE FINAL ARCHITECTURE", 14, VIOLET, True, PP_ALIGN.CENTER)
    flow(s, 4.45, ["User", "Copilot agent", "Power Automate tool", "Business result", "Answer in chat"], ["asks", "calls", "returns", "presents"], [TEAL, VIOLET, GREEN, BLUE, AMBER], height=1.3)


def draw_big_picture(s):
    card(s, Inches(0.72), Inches(1.85), Inches(3.55), Inches(4.7), "1 — Automate", "Instant\nScheduled\nAutomated\nApproval\nHTTP", BLUE, 1, 17)
    arrow(s, Inches(4.47), Inches(3.75), Inches(0.58), Inches(0.5), BLUE)
    card(s, Inches(5.15), Inches(1.85), Inches(3.55), Inches(4.7), "2 — Add the agent", "Instructions\nRAG knowledge\nTeams + website\nConfirmed inputs", VIOLET, 2, 17)
    arrow(s, Inches(8.9), Inches(3.75), Inches(0.58), Inches(0.5), VIOLET)
    card(s, Inches(9.58), Inches(1.85), Inches(3.0), Inches(4.7), "3 — Let it act", "Agent flow\nPrompt flow\nGuardrails\nReturned result", GREEN, 3, 17)


def draw_section(s, day, subtitle, stages):
    text(s, Inches(0.9), Inches(1.9), Inches(11.5), Inches(0.7), day, 34, BLUE, True, PP_ALIGN.CENTER)
    flow(s, 3.05, stages, [""] * (len(stages)-1), PALETTE[:len(stages)], height=1.5)
    text(s, Inches(1.1), Inches(5.25), Inches(11.1), Inches(0.8), subtitle, 18, GREY, False, PP_ALIGN.CENTER)


def draw_teaching_flow(s, nodes, takeaway, colors=None):
    flow(s, 2.05, nodes, [""] * (len(nodes)-1), colors or PALETTE[:len(nodes)], height=1.45)
    card(s, Inches(1.15), Inches(4.35), Inches(11.0), Inches(1.55), "Teaching point", takeaway, BLUE, body_size=15)


def draw_three_cards(s, items):
    for i, (label, body, accent) in enumerate(items):
        card(s, Inches(0.72 + i*4.0), Inches(2.0), Inches(3.7), Inches(4.35), label, body, accent, i+1, 14, 17)


def section(no, heading, day, subtitle, stages):
    rebuild(no, heading, "Course journey", lambda s: draw_section(s, day, subtitle, stages))


def teaching(no, heading, kicker, nodes, takeaway, colors=None):
    rebuild(no, heading, kicker, lambda s: draw_teaching_flow(s, nodes, takeaway, colors))


def cards(no, heading, kicker, items):
    rebuild(no, heading, kicker, lambda s: draw_three_cards(s, items))

def draw_http_method_cards(s):
    card(s, Inches(0.72), Inches(2.0), Inches(3.5), Inches(4.35),
         "GET", "Read data", BLUE, 1, 14, 17)
    card(s, Inches(4.47), Inches(2.0), Inches(3.5), Inches(4.35),
         "POST", "Submit data or start work", TEAL, 2, 14, 17)
    card(s, Inches(8.22), Inches(2.0), Inches(4.35), Inches(4.35),
         "PUT · PATCH · DELETE", "Update or remove data", VIOLET, 3, 14, 17)

def draw_shared_flowchart(s, image_path):
    panel_x, panel_y = Inches(0.35), Inches(1.72)
    panel_w, panel_h = Inches(12.63), Inches(5.0)
    box(s, panel_x, panel_y, panel_w, panel_h, WHITE, LINE)
    max_w, max_h = 12.05, 4.3
    with Image.open(image_path) as image:
        px_w, px_h = image.size
    aspect = px_w / px_h
    if aspect >= max_w / max_h:
        width, height = max_w, max_w / aspect
    else:
        height, width = max_h, max_h * aspect
    x = (13.333 - width) / 2
    y = 1.87 + (4.35 - height) / 2
    s.shapes.add_picture(str(image_path), Inches(x), Inches(y), width=Inches(width), height=Inches(height))
    text(s, Inches(1.0), Inches(6.4), Inches(11.3), Inches(0.28),
         "Shared workflow visual — follow the arrows from the trigger through actions to the expected outcome.",
         11, GREY, False, PP_ALIGN.CENTER)

def lab_flow_slide(no, heading, kicker, relative_image):
    rebuild(no, heading, kicker, lambda s: draw_shared_flowchart(s, ROOT / relative_image))


# Update inherited version labels.
for slide in prs.slides:
    for shape in slide.shapes:
        if getattr(shape, "has_text_frame", False):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if "Version 5.2" in run.text:
                        run.text = run.text.replace("Version 5.2", "Version 6.0")
                    if "Modules 1–3" in run.text:
                        run.text = run.text.replace("Modules 1–3", "Modules 1–4")
                    if "24 Jul 2026" in run.text and "Version" in shape.text:
                        run.text = run.text.replace("24 Jul 2026", "25 Jul 2026")

def draw_v5_journey(s):
    items = [
        ("1", "Form to Email Confirmation", "Confirm the submitted user"),
        ("2", "Log Enquiry + Send Email", "Add an audit row"),
        ("3", "Event Registration Branching", "Route Yes and No"),
        ("4", "Leave Application Approval", "Manager decides"),
        ("5", "IT Support Agent", "FAQ + Teams"),
        ("6", "HR Support Agent", "SharePoint + Teams"),
        ("7", "Support Request Routing", "IT or HR reply"),
        ("8", "Website HTTP Enquiry", "Website webhook"),
        ("9", "Finance Agent Web Chat", "Grounded agent"),
        ("10", "AI Trading Advisor Website", "Candles + news"),
    ]
    for i, (num, label, body) in enumerate(items):
        row, col = divmod(i, 5)
        card(s, Inches(0.72 + col*2.42), Inches(1.9 + row*2.35),
             Inches(2.12), Inches(1.92), label, body, PALETTE[i%5], num, 11, 10)
    text(s, Inches(0.72), Inches(6.54), Inches(11.85), Inches(0.34),
         "Day 1 builds Forms, flows and support agents. Day 2 adds webhooks and the Finance Advisor capstone.",
         14, INK, True, PP_ALIGN.CENTER)

def draw_v5_schedule(s):
    card(s, Inches(0.9), Inches(1.9), Inches(5.55), Inches(4.7), "Day 1 — Build and route",
         "9:00–10:40  Concepts + flow types\n"
         "10:55–3:15  Labs 1–4: Forms, Excel, event branch, approval\n"
         "3:30–5:50  Agent concepts + Labs 5–7\n"
         "5:50–6:00  Evidence check and recap", BLUE, "D1", 15)
    card(s, Inches(6.85), Inches(1.9), Inches(5.55), Inches(4.7), "Day 2 — Connect and advise",
         "9:00–10:05  HTTP requests and webhooks\n"
         "10:05–12:15  Lab 8 + Finance Agent foundation\n"
         "1:15–4:00  Labs 9–10: web chat and trading advisor\n"
         "4:00–6:00  Written + practical assessment", VIOLET, "D2", 15)

def draw_v5_assessment(s):
    draw_three_cards(s, [
        ("Written", "1 hour · open book\nModules 1–4 and the lab concepts", BLUE),
        ("Practical", "1 hour · open book\nBuild and verify a working flow and agent", TEAL),
        ("Evidence", "Submit on the LMS\nCompetent result + attendance requirement", VIOLET),
    ])

def draw_v5_repository(s):
    draw_three_cards(s, [
        ("10 labs", "Lab 0 setup plus Labs 1–10 and four concept modules.", BLUE),
        ("Ready assets", "Excel tables, searchable PDFs, HTML pages and JSON schemas.", TEAL),
        ("Use the guide", "Open each index.md or the compiled Learner Guide and work in order.", VIOLET),
    ])

def draw_branded_list(s, items):
    for i, item in enumerate(items):
        y = Inches(1.82 + i * 0.92)
        box(s, Inches(0.92), y, Inches(11.5), Inches(0.7), LIGHT, LINE)
        circle = s.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(1.12), y + Inches(0.12), Inches(0.46), Inches(0.46)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = PALETTE[i % len(PALETTE)]
        circle.line.fill.background()
        text(s, Inches(1.12), y + Inches(0.12), Inches(0.46), Inches(0.46),
             str(i + 1), 13, WHITE, True, PP_ALIGN.CENTER)
        text(s, Inches(1.78), y, Inches(10.35), Inches(0.7), item, 16, INK)

def draw_six_tiles(s, items):
    for i, (label, body, accent) in enumerate(items):
        row, col = divmod(i, 3)
        card(
            s,
            Inches(0.72 + col * 4.0),
            Inches(1.82 + row * 2.45),
            Inches(3.7),
            Inches(2.12),
            label,
            body,
            accent,
            i + 1,
            12,
            15,
        )


# ---------------------------------------------------------------------------
# Version 6.0: concept-first teaching sequence
# ---------------------------------------------------------------------------

rebuild(8, "Your 2-Day Journey", "Ten connected labs", draw_v5_journey)
rebuild(9, "How This Course Works", "Learning approach", lambda s: draw_branded_list(s, [
    "Learn the concept and decision rule before opening the product",
    "See the concept as a visual business pattern and worked example",
    "Apply the pattern in the next numbered hands-on lab",
    "Capture run history, email, workbook, agent or browser evidence",
    "Reuse each working capability in the next lab instead of starting over",
]))
rebuild(10, "Lesson Plan — 2 Days, 9:00am–6:00pm", "Schedule", draw_v5_schedule)
rebuild(12, "Assessment & Funding", "Final assessment", draw_v5_assessment)
rebuild(14, "Access the Hands-On Labs", "Course repository", draw_v5_repository)

section(
    15,
    "Day 1 — Automate, Decide and Add Agents",
    "DAY 1",
    "Learn each automation concept, apply it in sequence, then connect specialised agents.",
    ["Flow types", "Forms + data", "Conditions", "Approvals", "Copilot agents"],
)
teaching(
    16,
    "What Business Process Automation Changes",
    "Workflow foundations",
    ["Manual hand-off", "Repeatable rule", "Automated action", "Recorded evidence"],
    "Automate stable, repetitive work; keep judgement, exceptions and accountability visible.",
)
cards(17, "Choose Work Worth Automating", "Business value", [
    ("Repetitive", "The same steps occur frequently and consume attention.", BLUE),
    ("Rule-based", "Inputs and outcomes can be expressed as clear business rules.", TEAL),
    ("Traceable", "The process benefits from timestamps, status and run history.", VIOLET),
])
teaching(
    18,
    "Every Flow Uses Trigger → Actions → Output",
    "Core mental model",
    ["Trigger starts once", "Actions run in order", "Data moves as outputs", "Evidence proves result"],
    "A flow must have exactly one trigger and at least one action before it can save successfully.",
)
cards(19, "Three Cloud Flow Types", "The trigger determines the type", [
    ("Instant flow", "A person deliberately starts it from a button, app or manual run.", BLUE),
    ("Scheduled flow", "A Recurrence trigger starts it at a defined time or interval.", TEAL),
    ("Automated flow", "A connected-service event starts it when new information arrives.", VIOLET),
])
cards(20, "Instant Cloud Flow", "Person-controlled start", [
    ("Start", "A user selects Run, presses a button or invokes the flow from an app.", BLUE),
    ("Use when", "The exact start time depends on a person's decision.", TEAL),
    ("Example", "A staff member submits a one-off request or launches a controlled test.", VIOLET),
])
cards(21, "Scheduled Cloud Flow", "Clock-controlled start", [
    ("Start", "A Recurrence trigger reaches a date, time or interval.", TEAL),
    ("Use when", "Work must happen even when no new business event arrives.", BLUE),
    ("Example", "Send a weekday reminder at 9:00 AM Singapore time.", VIOLET),
])
cards(22, "Automated Cloud Flow", "Event-controlled start", [
    ("Start", "A form, email, file, record or message event occurs.", VIOLET),
    ("Use when", "The process must react immediately to new information.", TEAL),
    ("Example", "A Microsoft Forms response starts Labs 1–4 and 7.", BLUE),
])
teaching(
    23,
    "A Trigger Is a Contract with the Starting System",
    "Trigger fundamentals",
    ["Event occurs", "Connector detects it", "Trigger outputs metadata", "Actions consume data"],
    "Choose the trigger by asking who or what owns the start event: person, clock or system.",
)
teaching(
    24,
    "The Microsoft Forms Trigger Pattern",
    "Automated flow pattern",
    ["Form submitted", "Response Id", "Get response details", "Use answer tokens"],
    "The trigger identifies a response; Get response details retrieves the actual answers.",
)

lab_flow_slide(
    25,
    LAB_META["lab_1"]["title"],
    "Shared workflow visual",
    "labs/Day 1/Lab 1 - Forms Email Confirmation/assets/flowchart.png",
)
cards(26, "Lab 1 — Design the Form", "Required data", [
    ("Identity", "Name and Email identify the requester and recipient.", BLUE),
    ("Contact", "Tel provides an alternative contact channel.", TEAL),
    ("Enquiry", "Message uses a required long-answer field.", VIOLET),
])
teaching(
    27,
    "Lab 1 — Map Dynamic Content",
    "Form answers become tokens",
    ["Name token", "Email token", "Message token", "Personalised email"],
    "Use the submitted Email answer as the recipient; do not type the flow owner's address.",
)
teaching(
    28,
    "Lab 1 — Test the Real Outcome",
    "Evidence",
    ["Submit once", "Inspect one run", "Check recipient", "Confirm one message"],
    "One form submission must create one successful run and exactly one confirmation email.",
)

teaching(
    29,
    "Dynamic Content Carries Data Between Actions",
    "Data flow",
    ["Trigger output", "Response details", "Named token", "Action input"],
    "Typed labels are static text; dynamic-content tokens contain values from the current run.",
)
cards(30, "Excel Online Requires Structured Data", "Named-table pattern", [
    ("Workbook", "Store the file in OneDrive for Business or SharePoint.", BLUE),
    ("Table", "Use a named table with stable column headers.", TEAL),
    ("Audit row", "Record timestamp, source, status and the submitted answers.", VIOLET),
])
lab_flow_slide(
    31,
    LAB_META["lab_2"]["title"],
    "Shared workflow visual",
    "labs/Day 1/Lab 2 - Forms Enquiry Logging/assets/flowchart.png",
)
teaching(
    32,
    "Lab 2 — Extend the Working Flow",
    "Connected learning",
    ["Reuse Lab 1", "Insert Excel row", "Keep email", "Test again"],
    "Preserve the working trigger and email, then insert the durable audit record.",
)
teaching(
    33,
    "Lab 2 — Order Actions for Reliability",
    "Commit before confirmation",
    ["Get details", "Add row", "Send email", "Verify workbook"],
    "Send confirmation only after the workbook row succeeds, so the message matches reality.",
)
cards(34, "Lab 2 — Troubleshooting", "Common checks", [
    ("Location", "Use OneDrive for Business or SharePoint, not a local path.", BLUE),
    ("Table", "Select EnquiryLog; ordinary worksheet cells are not enough.", TEAL),
    ("Lock", "Close desktop Excel if the connector reports a file lock.", RED),
])

teaching(
    35,
    "Conditions Turn Data into Decisions",
    "If / else logic",
    ["Read a value", "Apply an operator", "True branch", "False branch"],
    "A condition should express one business decision clearly and route mutually exclusive outcomes.",
)
cards(36, "Design and Test Both Branches", "Decision coverage", [
    ("Input", "Use a controlled choice such as Yes/No to reduce ambiguity.", BLUE),
    ("Branches", "Give each path a complete action sequence and expected result.", TEAL),
    ("Evidence", "Run one test per branch and compare the actual outputs.", VIOLET),
])
lab_flow_slide(
    37,
    LAB_META["lab_3"]["title"],
    "Shared workflow visual",
    "labs/Day 1/Lab 3 - Event Registration Branching/assets/flowchart.png",
)
teaching(
    38,
    "Lab 3 — Yes Branch",
    "Participant joins",
    ["Joining = Yes", "Add EventLog row", "Email administrator", "Include contact details"],
    "The administrator receives the participant's name, email and telephone number.",
)
teaching(
    39,
    "Lab 3 — No Branch",
    "Participant declines",
    ["Joining = No", "Add EventLog row", "Email user", "Invite next time"],
    "The user receives thanks and a respectful invitation to a future event.",
)
cards(40, "Lab 3 — Branch Evidence", "Test matrix", [
    ("Yes test", "Correct EventLog row and administrator email.", GREEN),
    ("No test", "Correct EventLog row and user email.", BLUE),
    ("Audit", "JoiningEvent and NotificationSent explain the outcome.", VIOLET),
])

teaching(
    41,
    "Approvals Add Human Judgement to Automation",
    "Human in the loop",
    ["Submit request", "Notify approver", "Flow waits", "Decision resumes flow"],
    "Use an approval when a named authorised person—not an AI model—must own the decision.",
)
cards(42, "An Approval Produces Structured Evidence", "Decision data", [
    ("Outcome", "Approve or Reject controls the next branch.", BLUE),
    ("Responder", "The approver identity supports accountability.", TEAL),
    ("Comments", "Decision comments explain the result to the applicant.", VIOLET),
])
lab_flow_slide(
    43,
    LAB_META["lab_4"]["title"],
    "Shared workflow visual",
    "labs/Day 1/Lab 4 - Leave Approval/assets/flowchart.png",
)
cards(44, "Lab 4 — Leave Form", "Required information", [
    ("Employee", "Name; Forms captures the responder identity.", BLUE),
    ("Dates", "Leave start and end date.", TEAL),
    ("Request", "Leave Type and Reason for Leave.", VIOLET),
])
teaching(
    45,
    "Lab 4 — Handle the Approval Outcome",
    "Approve or reject",
    ["Start and wait", "Read Outcome", "Approve branch", "Reject branch"],
    "Compare Outcome to Approve and include the manager's comments in the applicant email.",
)
cards(46, "Lab 4 — Governance", "Protect people data", [
    ("Access", "Use only authorised approvers and accounts.", BLUE),
    ("Privacy", "Limit medical or unnecessary personal information.", RED),
    ("Evidence", "Retain the decision, comments and flow run history.", GREEN),
])

section(
    47,
    "Copilot Studio Agents — Understand, Ground and Act",
    "AGENTS",
    "Learn the six building blocks before creating the IT and HR support agents.",
    ["Instructions", "Knowledge", "Skills", "Tools", "Model + memory"],
)
teaching(
    48,
    "What Is a Copilot Agent?",
    "Conversational orchestration",
    ["User intent", "Agent instructions", "Knowledge + context", "Tool decision", "Response"],
    "An agent interprets language and coordinates approved knowledge and actions inside defined boundaries.",
)
rebuild(49, "Six Building Blocks of a Copilot Agent", "Concept map", lambda s: draw_six_tiles(s, [
    ("Knowledge", "Approved sources used to ground answers.", BLUE),
    ("Skills", "Capabilities the agent can perform.", TEAL),
    ("Tools", "Connected actions that read or change systems.", VIOLET),
    ("Memory", "Conversation context and governed persistence.", AMBER),
    ("Model", "Generative reasoning and response capability.", GREEN),
    ("System message", "Highest-priority role, scope and safety rules.", RED),
]))
teaching(
    50,
    "Knowledge Grounds the Answer",
    "Approved information",
    ["Approved source", "Retrieve evidence", "Cite or reference", "Grounded response"],
    "Knowledge answers what the agent should know; source quality and permissions determine trust.",
)
cards(51, "Skills Describe What the Agent Can Do", "Capabilities", [
    ("Conversation", "Ask, clarify, classify, summarise and explain.", BLUE),
    ("Reasoning", "Apply instructions and knowledge to the current request.", TEAL),
    ("Execution", "Use topics, tools and agent flows to complete work.", VIOLET),
])
teaching(
    52,
    "Tools Let the Agent Act",
    "Authorised execution",
    ["Need an action", "Select a tool", "Authenticate", "Execute", "Return output"],
    "A tool reads live data or creates an outcome; grant only the minimum authorised capability.",
)
cards(53, "Memory Is Governed Context", "What is remembered", [
    ("Session context", "Recent messages help the agent understand follow-up questions.", BLUE),
    ("Variables", "Named values preserve structured facts during the conversation.", TEAL),
    ("Persistence", "Longer-term memory depends on enabled features, consent and policy.", RED),
])
cards(54, "The Model Provides Generative Capability", "Model choice", [
    ("Quality", "Can it interpret the request and produce the required format?", BLUE),
    ("Latency", "Can it respond within the experience and workflow limits?", TEAL),
    ("Governance", "Does its use satisfy organisational and data requirements?", VIOLET),
])
teaching(
    55,
    "The System Message Defines Non-Negotiable Behaviour",
    "Instructions",
    ["Role", "Scope", "Source rules", "Safety", "Escalation"],
    "Copilot Studio may label this control Instructions; treat it as policy, not decoration.",
)
cards(56, "Test Before Publishing an Agent", "Safety test set", [
    ("Expected", "Questions the agent should answer from approved sources.", GREEN),
    ("Unsupported", "Missing or out-of-scope information that requires a limitation.", AMBER),
    ("Unsafe", "Credentials, private data or prohibited decisions that must be refused.", RED),
])

lab_flow_slide(
    57,
    LAB_META["lab_5"]["title"],
    "Shared workflow visual",
    "labs/Day 1/Lab 5 - IT Support Agent/assets/flowchart.png",
)
cards(58, "Lab 5 — Ground the IT Support Agent", "Knowledge + instructions", [
    ("Role", "First-line support for password, MFA, VPN, Wi-Fi and device loss.", BLUE),
    ("Knowledge", "Upload only the approved IT Support FAQ.", TEAL),
    ("Boundary", "Never request passwords, MFA codes or recovery keys.", RED),
])
cards(59, "Lab 5 — Test and Deploy to Teams", "Channel evidence", [
    ("Positive", "Verify grounded answers for approved IT questions.", GREEN),
    ("Negative", "Refuse credentials and unrelated HR requests.", RED),
    ("Teams", "Publish the latest version and verify the installed agent.", TEAL),
])

cards(60, "SharePoint Knowledge Adds Governance", "Enterprise grounding", [
    ("Managed source", "Policy owners update one controlled document library.", BLUE),
    ("Permissions", "The agent can use only content its connection may access.", TEAL),
    ("Freshness", "Re-test the agent whenever source policies change.", VIOLET),
])
lab_flow_slide(
    61,
    LAB_META["lab_6"]["title"],
    "Shared workflow visual",
    "labs/Day 1/Lab 6 - HR Support Agent/assets/flowchart.png",
)
cards(62, "Lab 6 — Ground the HR Support Agent", "SharePoint policy source", [
    ("Explain", "Use approved leave, expenses and workplace-policy content.", GREEN),
    ("Protect", "Never expose another employee's records or infer private facts.", RED),
    ("Escalate", "HR and managers retain final authority for personal decisions.", BLUE),
])
cards(63, "Lab 6 — Publish and Verify in Teams", "Controlled release", [
    ("Source test", "Confirm the response is traceable to the SharePoint policy.", BLUE),
    ("Boundary test", "Ask for another employee's record and verify refusal.", RED),
    ("Channel test", "Publish the current version and verify Teams behaviour.", TEAL),
])

teaching(
    64,
    "Power Automate Can Execute a Published Agent",
    "Execute Agent and wait",
    ["Flow receives input", "Select published agent", "Send message", "Wait for reply", "Use output"],
    "The flow remains the process controller while the specialised agent handles grounded interpretation.",
)
cards(65, "Route to the Specialist with the Right Knowledge", "Decision pattern", [
    ("Classify", "Use the submitted Support Type choice.", BLUE),
    ("Invoke", "Call only the IT or HR agent selected by the condition.", TEAL),
    ("Return", "Email only the reply produced by the chosen branch.", VIOLET),
])
lab_flow_slide(
    66,
    LAB_META["lab_7"]["title"],
    "Shared workflow visual",
    "labs/Day 1/Lab 7 - Support Request Routing/assets/flowchart.png",
)
teaching(
    67,
    "Lab 7 — Build the Support Request Form",
    "One front door",
    ["Name", "Email", "Support Type", "Message"],
    "A controlled IT Support / HR Support choice makes the routing rule deterministic.",
)
teaching(
    68,
    "Lab 7 — Execute Only the Selected Agent",
    "Branch isolation",
    ["Read Support Type", "Run one agent", "Capture its reply", "Skip other branch"],
    "One submission should create one agent execution and one user email—not two.",
)
cards(69, "Lab 7 — Test the Complete Routing Matrix", "Evidence", [
    ("IT test", "IT question → IT agent → IT-grounded email.", GREEN),
    ("HR test", "HR question → HR agent → HR-grounded email.", BLUE),
    ("Fallback", "Invalid or unsafe requests receive a bounded response.", RED),
])

section(
    70,
    "Day 2 — HTTP, Webhooks and Agent Websites",
    "DAY 2",
    "Learn the web integration contract before connecting websites and finance agents.",
    ["HTTP request", "Webhook", "JSON", "Agent execution", "Market tools"],
)
teaching(
    71,
    "An HTTP Request Is a Message Between Systems",
    "Web foundations",
    ["Client", "Method + URL", "Headers + body", "Server action", "Response"],
    "The course websites act as clients; Power Automate receives the request and returns a bounded response.",
)
teaching(
    72,
    "A Webhook Is an Event-Receiving HTTP Endpoint",
    "Push integration",
    ["Event occurs", "Client POSTs", "Webhook receives", "Flow runs", "Status returns"],
    "Power Automate generates the webhook URL only after a valid trigger-and-action flow saves.",
)
rebuild(73, "Common HTTP Methods", "Request intent", draw_http_method_cards)
teaching(
    74,
    "An HTTP Request Has Four Main Parts",
    "Request anatomy",
    ["Method", "URL", "Headers", "Body"],
    "The lab websites use POST to send JSON data to the learner's Power Automate endpoint.",
)
cards(75, "JSON Defines a Machine-Readable Contract", "Request and response", [
    ("Schema", "Field names, data types and required values define valid input.", BLUE),
    ("Payload", "The browser serialises the current form or prompt values.", TEAL),
    ("Response", "The flow returns limited JSON the page can display.", VIOLET),
])
cards(76, "Webhook Security and Browser Boundaries", "Classroom versus production", [
    ("Endpoint", "Treat an anonymous webhook URL like a secret.", RED),
    ("Input", "Validate, minimise and never include credentials.", BLUE),
    ("CORS + output", "Return only what the browser needs; authenticate production callers.", TEAL),
])

lab_flow_slide(
    77,
    LAB_META["lab_8"]["title"],
    "Shared workflow visual",
    "labs/Day 2/Lab 8 - Website HTTP Enquiry/assets/flowchart.png",
)
teaching(
    78,
    "Lab 8 — Define the Request Contract",
    "JSON schema",
    ["name", "email", "tel", "message"],
    "Generate the trigger schema from a representative sample before mapping fields.",
)
teaching(
    79,
    "Lab 8 — Complete the Flow Before Saving",
    "URL generation",
    ["HTTP trigger", "Email administrator", "Response action", "Save", "Copy URL"],
    "A trigger alone is incomplete; add actions and resolve validation errors before expecting a URL.",
)
teaching(
    80,
    "Lab 8 — Connect the Supplied Website",
    "Learner-entered webhook",
    ["Open HTML", "Paste URL", "Save locally", "Submit once", "Display status"],
    "The supplied source contains no tenant endpoint; each learner connects their own saved flow.",
)
cards(81, "Lab 8 — End-to-End Evidence", "Browser → flow → email → browser", [
    ("Browser", "The page reports one successful response.", BLUE),
    ("Flow", "Run history shows the expected request fields.", TEAL),
    ("Mailbox", "The administrator receives exactly one enquiry email.", GREEN),
])

cards(82, "Grounded Finance Answers Need Retrieval", "RAG pattern", [
    ("Retrieve", "Search the approved Finance Knowledge Base for relevant passages.", BLUE),
    ("Generate", "Compose an explanation constrained by the retrieved evidence.", TEAL),
    ("Qualify", "State uncertainty and refuse guarantees or personalised advice.", RED),
])
teaching(
    83,
    "Execute Agent and Wait Bridges Flow and Agent",
    "Synchronous agent call",
    ["Receive prompt", "Select Finance Agent", "Wait for response", "Extract output", "Return JSON"],
    "Use the actual agent-response token; do not copy a test answer into the flow.",
)
teaching(
    84,
    "Web Chat Is a Channel, Not the Knowledge Source",
    "Separation of concerns",
    ["Browser UI", "HTTP flow", "Published agent", "Knowledge base", "JSON reply"],
    "The page captures and displays; the flow orchestrates; the agent interprets approved knowledge.",
)
lab_flow_slide(
    85,
    LAB_META["lab_9"]["title"],
    "Shared workflow visual",
    "labs/Day 2/Lab 9 - Finance Agent Web Chat/assets/flowchart.png",
)
cards(86, "Lab 9 — Finance Knowledge Boundary", "Educational use", [
    ("Explain", "Orders, candles, timeframes, volatility and news concepts.", GREEN),
    ("Qualify", "Separate facts from interpretation and disclose uncertainty.", BLUE),
    ("Refuse", "No guaranteed returns or personalised buy/sell instructions.", RED),
])
teaching(
    87,
    "Lab 9 — Build the HTTP-to-Agent Flow",
    "Published-agent execution",
    ["HTTP prompt", "Run Finance Agent", "Capture response", "Add disclaimer", "Return JSON"],
    "One browser message should create one flow run and one bounded agent response.",
)
teaching(
    88,
    "Lab 9 — Connect the Finance Chat Page",
    "Learner-entered webhook",
    ["Paste URL", "Send prompt", "Render reply", "Show disclaimer"],
    "Store the URL only in the learner's browser and never commit it to the repository.",
)
cards(89, "Lab 9 — Grounding and Safety Tests", "Evidence set", [
    ("Known concept", "Ask about a market versus limit order.", GREEN),
    ("Uncertainty", "Ask something absent from the knowledge source.", AMBER),
    ("Boundary", "Request a guaranteed return and verify refusal.", RED),
])

cards(90, "Tools and APIs Supply Live Context", "Action architecture", [
    ("Tool", "A governed function the agent or flow is authorised to call.", BLUE),
    ("API", "A structured contract for requesting data from an external service.", TEAL),
    ("Output", "Validated tool data becomes evidence—not an automatic conclusion.", VIOLET),
])
teaching(
    91,
    "Multi-Timeframe Analysis Compares Different Horizons",
    "Market context",
    ["1-minute candles", "15-minute candles", "1-hour candles", "Compare direction", "Explain conflict"],
    "Short intervals contain more noise; a responsible answer preserves conflicting evidence.",
)
cards(92, "News Adds Context, Not Certainty", "Recent information", [
    ("Time", "Check when the event and article were published.", BLUE),
    ("Source", "Prefer relevant, credible reporting and identify gaps.", TEAL),
    ("Impact", "Relate news cautiously; price may already reflect it.", VIOLET),
])
cards(93, "Keep Credentials on the Server Side", "Secret handling", [
    ("Store", "Use protected connections, environment variables or a custom connector.", GREEN),
    ("Protect", "Enable secure inputs and outputs where credentials appear.", BLUE),
    ("Never expose", "No API keys in HTML, prompts, source control or screenshots.", RED),
])
teaching(
    94,
    "Guardrails Constrain the Finance Advisor",
    "Responsible AI",
    ["Validate symbol", "Limit data", "Separate facts", "State uncertainty", "End with risk note"],
    "The agent provides educational analysis and never promises returns or gives personalised instructions.",
)

lab_flow_slide(
    95,
    LAB_META["lab_10"]["title"],
    "Shared workflow visual",
    "labs/Day 2/Lab 10 - AI Trading Advisor Website/assets/flowchart.png",
)
cards(96, "Lab 10 — Authorised Data and Agent Tools", "Tool inventory", [
    ("Twelve Data", "Retrieve 1-minute, 15-minute and 1-hour candles.", BLUE),
    ("NewsAPI", "Retrieve recent symbol or company news.", TEAL),
    ("Finance Advisor", "Compare evidence and return bounded analysis.", VIOLET),
])
teaching(
    97,
    "Lab 10 — Build the Three Candle Requests",
    "Consistent data grain",
    ["Validate symbol", "Call 1-minute", "Call 15-minute", "Call 1-hour", "Check provider status"],
    "Use the same symbol and comparable result limits so the agent can contrast the intervals.",
)
teaching(
    98,
    "Lab 10 — Retrieve Recent News",
    "News tool",
    ["Query symbol", "Limit articles", "Check time", "Check source", "Return compact context"],
    "Keep the news payload small and preserve provider errors instead of hiding them.",
)
cards(99, "Lab 10 — Secure the External Calls", "Credential controls", [
    ("Connection", "Keep provider credentials in protected server-side configuration.", GREEN),
    ("Observability", "Log status and latency without recording secrets.", BLUE),
    ("Failure", "Return a safe partial-result message when a provider is unavailable.", AMBER),
])
teaching(
    100,
    "Lab 10 — Compose the Agent Input",
    "Evidence bundle",
    ["User question", "Three candle sets", "Recent news", "Instructions", "Finance Advisor"],
    "Tell the agent which observations are data, which are user context, and which rules are mandatory.",
)
teaching(
    101,
    "Lab 10 — Return Structured JSON",
    "Website response",
    ["symbol", "analysis", "uncertainty", "risk note"],
    "A stable response contract lets the website render success and errors predictably.",
)
teaching(
    102,
    "Lab 10 — Embed TradingView Separately",
    "Interactive front end",
    ["Enter symbol", "Update chart", "Paste webhook", "Ask agent", "Render analysis"],
    "TradingView visualisation and agent analysis are related but independently testable components.",
)
cards(103, "Lab 10 — Test the Complete Matrix", "Expected failures matter", [
    ("Valid", "All tools succeed and the response is qualified.", GREEN),
    ("Partial", "Missing news or conflicting timeframes are disclosed.", AMBER),
    ("Invalid", "Bad symbol or advice request receives a safe response.", RED),
])
teaching(
    104,
    "Lab 10 — Review the End-to-End Trace",
    "Observe → reason → act → respond",
    ["Website request", "Power Automate run", "Tool outputs", "Agent response", "Browser result"],
    "Each boundary must have a clear owner, observable input/output and safe failure behaviour.",
)

rebuild(105, "Course Recap — The Big Picture", "From flow maker to agent builder", draw_big_picture)
rebuild(106, "What You Can Automate Next", "Workplace opportunities", lambda s: draw_branded_list(s, [
    "Onboarding: new-hire checklists and welcome emails",
    "Reporting: scheduled data pulls and summaries",
    "Helpdesk: route requests to the right specialist agent",
    "Document handling: filing, approvals and reminders",
    "Agent-assisted workflows: interpret language, then perform governed actions",
]))
rebuild(107, "Governance and Operational Readiness", "Before production", lambda s: draw_branded_list(s, [
    "Use authenticated endpoints, least privilege and protected credentials",
    "Validate inputs and return only the minimum necessary output",
    "Keep approvals and high-impact decisions with authorised people",
    "Monitor failures, latency, connector health and source freshness",
    "Document ownership, evidence, escalation and retirement procedures",
]))
rebuild(108, "Key Takeaways", "Course synthesis", lambda s: draw_branded_list(s, [
    "Trigger choice determines instant, scheduled or automated flow behaviour",
    "Actions consume dynamic data and produce observable business outcomes",
    "Conditions and approvals encode rules while preserving human authority",
    "Copilot agents combine instructions, knowledge, skills, tools, memory and a model",
    "HTTP and webhooks connect external experiences to governed flows and agents",
]))

# Renumber the five inherited closing slides after moving them to 109–113.
for new_no, old_no in zip(range(109, 114), range(82, 87)):
    slide = prs.slides[new_no - 1]
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False):
            continue
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                if run.text.strip() == str(old_no):
                    run.text = str(new_no)

prs.save(DECK)
print(f"Updated {DECK} ({len(prs.slides)} slides)")
raise SystemExit(0)

rebuild(8, "Your 2-Day Journey", "Ten connected labs", draw_v5_journey)
rebuild(10, "Lesson Plan — 2 Days, 9:00am–6:00pm", "Schedule", draw_v5_schedule)
rebuild(12, "Assessment & Funding", "Final assessment", draw_v5_assessment)
rebuild(14, "Access the Hands-On Labs", "Course repository", draw_v5_repository)
rebuild(9, "How This Course Works", "Learning approach", lambda s: draw_branded_list(s, [
    "Concept, then demonstration, then hands-on practice for every topic",
    "Built entirely in Microsoft 365 and the Power Platform",
    "No coding required—use low-code, drag-and-drop tools",
    "Save flows and agents so they can be reused in the workplace",
    "Use daily recap and open Q&A to consolidate learning",
]))

section(15, "Day 1 — Forms, Flows and Business Agents", "DAY 1",
        "Build one connected automation story, then add specialised agents.",
        ["Choose the trigger", "Capture form data", "Route and approve", "Ground agents", "Email the result"])
teaching(16, "A Business Workflow Has a Clear Start and Result", "Workflow foundations",
         ["Business event", "Trigger", "Actions", "Output", "Evidence"],
         "Name the start event, required work, expected result and proof before opening the designer.")
teaching(17, "Trigger → Actions → Output", "Core pattern",
         ["Exactly one trigger", "Get or validate data", "Perform work", "Notify or return"],
         "Every lab uses the same skeleton; only the trigger, actions and business rules change.")
cards(18, "Three Cloud Flow Types", "How a cloud flow starts", [
    ("Instant flow", "A person deliberately selects Run, presses a button or invokes the flow from an app.\n\nUse when the user controls the exact start time.", BLUE),
    ("Scheduled flow", "A Recurrence trigger reaches a defined time.\n\nUse for daily, weekly or other timetable-driven work.", TEAL),
    ("Automated flow", "A connected-service event occurs, such as a new form response.\n\nUse when the process must react immediately.", VIOLET),
])
teaching(19, "Choose the Flow Type by Asking One Question", "Decision rule",
         ["A person?", "A clock?", "A new event?"],
         "Person = instant. Clock = scheduled. New record, form, file or message = automated.",
         [BLUE, TEAL, VIOLET])
cards(20, "Same Actions, Different Triggers", "Flow comparison", [
    ("Instant", "Manual trigger → send email → add Excel row", BLUE),
    ("Scheduled", "Recurrence → read pending items → send reminder", TEAL),
    ("Automated", "Form response → get details → email / log / approve", VIOLET),
])
teaching(21, "The Microsoft Forms Trigger Pattern", "Automated cloud flows",
         ["Form submitted", "Response Id", "Get response details", "Use answers"],
         "The trigger identifies the response; Get response details retrieves the actual answers.")

teaching(22, "Lab 1 — Form to Email Confirmation", "Automated flow",
         ["Course Enquiry Form", "Get response details", "Send email", "User inbox"],
         "The submitted Email answer—not the maker's address—is the recipient.")
cards(23, "Lab 1 — Design the Form", "Required fields", [
    ("Identity", "Name\nEmail", BLUE),
    ("Contact", "Tel", TEAL),
    ("Enquiry", "Message (long answer)", VIOLET),
])
teaching(24, "Lab 1 — Map Dynamic Content", "Form answers become tokens",
         ["Name token", "Email token", "Message token", "Personalised email"],
         "Insert tokens from Get response details. Typed labels are not dynamic content.")
teaching(25, "Lab 1 — Test the Real Outcome", "Evidence",
         ["Submit once", "Inspect run", "Check recipient", "Confirm one email"],
         "One form submission should produce one successful run and exactly one message.")

teaching(26, "Lab 2 — Extend, Do Not Rebuild", "Connected learning",
         ["Copy Lab 1", "Add Excel action", "Keep email", "Test again"],
         "Lab 2 preserves the working trigger and email, then inserts a durable audit record.")
teaching(27, "Lab 2 — Enquiry Log.xlsx", "Named Excel table",
         ["Timestamp", "Name + contact", "Message", "Status + source"],
         "Excel Online actions require a named table: EnquiryLog.")
teaching(28, "Lab 2 — Action Order", "Reliability",
         ["Get details", "Add row", "Send email", "Verify workbook"],
         "Put logging before email when confirmation should be sent only after a successful record.")
cards(29, "Lab 2 — Troubleshooting", "Common checks", [
    ("Workbook", "Store in OneDrive for Business or SharePoint.", BLUE),
    ("Table", "Select EnquiryLog; loose cells are not a table.", TEAL),
    ("Lock", "Close desktop Excel if the connector reports a file lock.", RED),
])

teaching(30, "Lab 3 — Event Registration Branching", "Condition",
         ["Event form", "Joining?", "Yes branch", "No branch"],
         "A choice field becomes a business rule that must be tested on both paths.")
teaching(31, "Lab 3 — Yes Branch", "Participant joins",
         ["Joining = Yes", "Add EventLog row", "Email admin", "Participant details"],
         "The administrator receives the person's name, email and telephone number.")
teaching(32, "Lab 3 — No Branch", "Participant declines",
         ["Joining = No", "Add EventLog row", "Email user", "Invite next time"],
         "The user receives thanks and a respectful next-event message.")
cards(33, "Lab 3 — Branch Evidence", "Test matrix", [
    ("Yes test", "Correct row + administrator email", GREEN),
    ("No test", "Correct row + user email", BLUE),
    ("Audit", "JoiningEvent and NotificationSent explain the outcome", VIOLET),
])

teaching(34, "Lab 4 — Leave Application Approval", "Human in the loop",
         ["Leave form", "Start approval", "Manager decides", "Notify applicant"],
         "An automated flow can pause safely while an authorised person decides.")
cards(35, "Lab 4 — Leave Form", "Required information", [
    ("Employee", "Name\nResponder email captured by Forms", BLUE),
    ("Dates", "Leave from date\nLeave end date", TEAL),
    ("Request", "Leave type\nReason for leave", VIOLET),
])
teaching(36, "Lab 4 — Approval Outcome", "Approve or reject",
         ["Start and wait", "Outcome", "Approve branch", "Reject branch"],
         "Compare Outcome to Approve and include manager comments in the applicant email.")
cards(37, "Lab 4 — Governance", "Handle people data carefully", [
    ("Access", "Use only authorised approvers.", BLUE),
    ("Privacy", "Limit medical and personal information.", RED),
    ("Evidence", "Retain decision, comments and run history.", GREEN),
])

cards(38, "Copilot Agent — Six Building Blocks", "Part 1", [
    ("Knowledge base", "Approved files, websites or SharePoint sources used to ground answers.", BLUE),
    ("Skills", "Capabilities realised through topics, tools and agent flows.", TEAL),
    ("Tools", "Connected functions that read data or create authorised outcomes.", VIOLET),
])
cards(39, "Copilot Agent — Six Building Blocks", "Part 2", [
    ("Memory", "Conversation context and variables; persistence depends on enabled features and governance.", BLUE),
    ("Model", "The generative model interpreting requests and composing responses.", TEAL),
    ("System message", "Instructions defining role, scope, tone, safety and escalation.", VIOLET),
])
teaching(40, "Knowledge Answers; Tools Act", "Agent architecture",
         ["User asks", "Instructions set scope", "Knowledge grounds", "Tool acts", "Agent replies"],
         "Use static knowledge for approved explanations and tools for live, authorised actions.")
cards(41, "Agent Safety Test Set", "Before publishing", [
    ("Expected", "Questions the agent should answer.", GREEN),
    ("Unsupported", "Missing or out-of-scope information.", AMBER),
    ("Unsafe", "Credentials, personal data or prohibited decisions.", RED),
])

teaching(42, "Lab 5 — IT Support Agent", "Grounded first-line support",
         ["Teams user", "IT Support Agent", "IT FAQ", "Answer or escalate"],
         "The agent never asks for passwords, MFA codes or recovery keys.")
cards(43, "Lab 5 — Test and Deploy", "Copilot Studio → Teams", [
    ("Positive", "Password reset, MFA, VPN and device loss.", GREEN),
    ("Negative", "Credential request and unrelated HR question.", RED),
    ("Channel", "Publish latest version and verify in Teams.", TEAL),
])
teaching(44, "Lab 6 — HR Support Agent", "SharePoint knowledge",
         ["HR policy PDF", "SharePoint library", "HR Support Agent", "Teams user"],
         "Central knowledge and source permissions support governed policy answers.")
cards(45, "Lab 6 — HR Boundaries", "Information, not decisions", [
    ("Explain", "Approved leave, expenses and workplace policy.", GREEN),
    ("Protect", "Never expose another employee's records.", RED),
    ("Escalate", "HR and managers make final decisions.", BLUE),
])
teaching(46, "Lab 7 — Route Requests to Specialised Agents", "Form-to-agent automation",
         ["Support form", "IT or HR?", "Run selected agent", "Email reply"],
         "A condition routes the same form to the specialist with the right knowledge and instructions.")
cards(47, "Day 1 Recap", "One connected progression", [
    ("Flows", "Forms → email → Excel → condition → approval", BLUE),
    ("Agents", "IT FAQ and HR SharePoint knowledge", VIOLET),
    ("Integration", "Form → specialised agent → user email", TEAL),
])

section(48, "Day 2 — HTTP, Webhooks and Agent Websites", "DAY 2",
        "Expose flows safely to websites and finish with a tool-using Finance Advisor Agent.",
        ["HTTP request", "Webhook URL", "Finance chat", "Market tools", "Trading website"])
teaching(49, "An HTTP Request Has Four Main Parts", "Web foundations",
         ["Method", "URL", "Headers", "Body"],
         "The lab websites use POST to send a JSON body to the Power Automate endpoint.")
rebuild(50, "Common HTTP Methods", "Intent", draw_http_method_cards)
teaching(51, "A Webhook Is an Event Endpoint", "Request and response",
         ["Website", "POST JSON", "HTTP trigger", "Flow actions", "JSON Response"],
         "Power Automate generates the URL after a valid trigger-and-action flow saves.")
cards(52, "Webhook Safety", "Classroom versus production", [
    ("URL", "Treat an anonymous webhook URL like a secret.", RED),
    ("Input", "Validate, minimise and never include credentials.", BLUE),
    ("Output", "Return only the data the website needs.", TEAL),
])

teaching(53, "Lab 8 — Website HTTP Enquiry", "External form",
         ["Enquiry page", "Webhook URL field", "HTTP trigger", "Email admin", "Return status"],
         "The learner pastes the generated URL; the HTML contains no tenant endpoint.")
teaching(54, "Lab 8 — Request Contract", "JSON schema",
         ["name", "email", "tel", "message"],
         "Generate the trigger schema from a sample payload before mapping fields.")
teaching(55, "Lab 8 — Complete the Flow Before Saving", "URL generation",
         ["HTTP trigger", "Send email action", "Response action", "Save", "Copy URL"],
         "A trigger alone is incomplete; add at least one action and resolve validation errors.")
cards(56, "Lab 8 — Browser Test", "End-to-end evidence", [
    ("Connect", "Paste and save the current webhook URL.", BLUE),
    ("Submit", "Enter realistic classroom data once.", TEAL),
    ("Verify", "Page status, run history and administrator email.", GREEN),
])

teaching(57, "Lab 9 — Finance Knowledge Agent", "Grounded web chat",
         ["Browser prompt", "HTTP flow", "Finance Agent", "Knowledge base", "JSON reply"],
         "The website is a channel; the agent supplies governed educational interpretation.")
cards(58, "Lab 9 — Finance Knowledge Boundary", "Educational use", [
    ("Explain", "Orders, candles, timeframes, volatility and news.", GREEN),
    ("Qualify", "Separate facts from interpretation and uncertainty.", BLUE),
    ("Refuse", "No guarantees or personalised buy/sell instructions.", RED),
])
teaching(59, "Lab 9 — HTTP-to-Agent Flow", "Run a published agent",
         ["prompt", "Run Finance Agent", "agent response", "Response JSON"],
         "Insert the actual agent-response output token into the JSON reply.")
cards(60, "Lab 9 — Test Set", "Grounding and safety", [
    ("Concept", "Market versus limit order.", GREEN),
    ("Uncertainty", "Question not covered by knowledge.", AMBER),
    ("Boundary", "Request for guaranteed returns.", RED),
])
teaching(61, "Lab 9 — Connect the Chat Page", "Learner-entered webhook",
         ["Save URL locally", "Send prompt", "Display reply", "Show disclaimer"],
         "One message should create one flow run; do not embed tenant URLs in source.")

teaching(62, "Lab 10 — Trading Advisor Capstone", "Agent with tools",
         ["TradingView chart", "Symbol + question", "Webhook flow", "Finance Advisor Agent", "Analysis"],
         "The experience combines a market chart with governed multi-timeframe and news analysis.")
cards(63, "Lab 10 — Four Authorised Tools", "Live market context", [
    ("Twelve Data", "1-minute candles\n15-minute candles\n1-hour candles", BLUE),
    ("NewsAPI", "Recent relevant company or symbol news", TEAL),
    ("Guardrails", "Validate symbols, limits, errors and credentials", RED),
])
teaching(64, "Lab 10 — Multi-Timeframe Reasoning", "Do not force agreement",
         ["1-minute", "15-minute", "1-hour", "Compare direction", "Explain conflict"],
         "Short intervals contain more noise; a sound response preserves conflicting evidence.")
teaching(65, "Lab 10 — Add News Context", "Recent information",
         ["Query news", "Check time + source", "Relate cautiously", "State gaps"],
         "A headline can be delayed, incomplete or already reflected in price.")
cards(66, "Lab 10 — Secure API Design", "No keys in the browser", [
    ("Store", "Protected connections, environment variables or custom connector.", GREEN),
    ("Limit", "Small result sets and provider rate limits.", BLUE),
    ("Hide", "Never expose keys in HTML, prompts, logs or screenshots.", RED),
])
teaching(67, "Lab 10 — Finance Advisor Instructions", "Model boundaries",
         ["Use all tools", "Separate data and inference", "Describe uncertainty", "End with risk note"],
         "The agent provides education; it never promises returns or tells a person what to buy.")
teaching(68, "Lab 10 — HTTP Request Contract", "Website to flow",
         ["symbol", "prompt", "Validate + normalise", "Run agent", "Return JSON"],
         "Reject invalid symbols and return a clear error instead of fabricated analysis.")
teaching(69, "Lab 10 — TradingView Website", "Interactive front end",
         ["Enter symbol", "Update chart", "Paste webhook", "Ask agent", "Render response"],
         "TradingView visualisation and agent analysis are related but independent components.")
cards(70, "Lab 10 — Test Matrix", "Expected failures matter", [
    ("Valid", "All data tools succeed and output is qualified.", GREEN),
    ("Partial", "Missing news or conflicting timeframes are disclosed.", AMBER),
    ("Invalid", "Bad symbol or advice request gets a safe response.", RED),
])
teaching(71, "End-to-End Agentic Architecture", "Observe → reason → act → respond",
         ["Website user", "Power Automate", "Copilot agent", "Data tools", "Browser response"],
         "Each boundary has a distinct responsibility and an auditable input/output.")
cards(72, "Operational Readiness Review", "Before production", [
    ("Security", "Authentication, secrets and least privilege.", RED),
    ("Reliability", "Timeouts, retries, rate limits and fallbacks.", BLUE),
    ("Governance", "Approved sources, disclaimers, logs and owners.", TEAL),
])
cards(73, "Day 2 Recap", "From webhook to tool-using agent", [
    ("Connect", "HTTP request + learner-entered webhook URL", BLUE),
    ("Ground", "Finance knowledge + live authorised tools", VIOLET),
    ("Respond", "Structured JSON + uncertainty + risk reminder", GREEN),
])

rebuild(79, "Course Recap — The Big Picture", "From flow maker to agent builder", draw_big_picture)
rebuild(74, "What You Can Automate Next", "Workplace opportunities", lambda s: draw_branded_list(s, [
    "Onboarding: new-hire checklists and welcome emails",
    "Reporting: scheduled data pulls and summaries",
    "Helpdesk: triage and route incoming requests",
    "Document handling: filing, approvals and reminders",
    "Any process where people copy data or chase approvals by hand",
]))
rebuild(75, "Common Pitfalls to Avoid", "Implementation risks", lambda s: draw_branded_list(s, [
    "Automating a broken process—fix the process first",
    "Trying to build everything in one giant flow",
    "Skipping tests and discovering surprises in production",
    "Omitting error handling so failures go unnoticed",
    "Using vague agent instructions that return inconsistent data",
]))
rebuild(76, "Common Errors & Quick Fixes", "Troubleshooting", lambda s: draw_branded_list(s, [
    "Unauthorized email action: reconnect Outlook with a mailbox-enabled account",
    "Approval valid-users error: select a real tenant user from the approver picker",
    "Literal utcNow(): enter the value through the Expression editor",
    "Excel shows ####: widen or auto-fit the affected column",
    "Unexpected loop or missing agent flow: use single-value fields and one environment",
]))
rebuild(77, "Governance & Security Basics", "Responsible automation", lambda s: draw_branded_list(s, [
    "Use only connections and permissions you are authorised to use",
    "Keep sensitive data out of email and logs where possible",
    "Follow organisational data, privacy and approval policies",
    "Document what each flow does and who owns it",
    "Review and retire flows that are no longer needed",
]))
rebuild(78, "Rolling This Out at Work", "Adoption pathway", lambda s: draw_branded_list(s, [
    "Choose one painful, repetitive task to automate first",
    "Prove the value, then share the outcome with the team",
    "Build a small library of reusable flows and agents",
    "Involve the people who perform the work in the design",
    "Iterate as needs, controls and evidence requirements change",
]))
rebuild(80, "Key Takeaways", "Course synthesis", lambda s: draw_branded_list(s, [
    "Every workflow follows Trigger → Actions → Output",
    "Power Automate performs work; Copilot Studio adds intelligence",
    "Structured agent outputs make connected flows reliable",
    "Orchestration combines separate steps into complete processes",
    "Start small, test and improve—then scale",
]))
rebuild(81, "Resources & Where to Go Next", "Continue learning", lambda s: draw_branded_list(s, [
    "make.powerautomate.com — build and manage cloud flows",
    "copilotstudio.microsoft.com — create and publish agents",
    "Microsoft Learn — follow free guided learning paths",
    "Templates gallery — start from reviewed pre-built flows",
    "Your community — share safe patterns and lessons learned",
]))

# Use the exact same workflow PNG in the lab, Learner Guide and facilitator deck.
lab_flow_slide(22, LAB_META["lab_1"]["title"], "Shared workflow visual",
               "labs/Day 1/Lab 1 - Forms Email Confirmation/assets/flowchart.png")
lab_flow_slide(26, LAB_META["lab_2"]["title"], "Shared workflow visual",
               "labs/Day 1/Lab 2 - Forms Enquiry Logging/assets/flowchart.png")
lab_flow_slide(30, LAB_META["lab_3"]["title"], "Shared workflow visual",
               "labs/Day 1/Lab 3 - Event Registration Branching/assets/flowchart.png")
lab_flow_slide(34, LAB_META["lab_4"]["title"], "Shared workflow visual",
               "labs/Day 1/Lab 4 - Leave Approval/assets/flowchart.png")
lab_flow_slide(42, LAB_META["lab_5"]["title"], "Shared workflow visual",
               "labs/Day 1/Lab 5 - IT Support Agent/assets/flowchart.png")
lab_flow_slide(44, LAB_META["lab_6"]["title"], "Shared workflow visual",
               "labs/Day 1/Lab 6 - HR Support Agent/assets/flowchart.png")
lab_flow_slide(46, LAB_META["lab_7"]["title"], "Shared workflow visual",
               "labs/Day 1/Lab 7 - Support Request Routing/assets/flowchart.png")
lab_flow_slide(53, LAB_META["lab_8"]["title"], "Shared workflow visual",
               "labs/Day 2/Lab 8 - Website HTTP Enquiry/assets/flowchart.png")
lab_flow_slide(57, LAB_META["lab_9"]["title"], "Shared workflow visual",
               "labs/Day 2/Lab 9 - Finance Agent Web Chat/assets/flowchart.png")
lab_flow_slide(62, LAB_META["lab_10"]["title"], "Shared workflow visual",
               "labs/Day 2/Lab 10 - AI Trading Advisor Website/assets/flowchart.png")

prs.save(DECK)
print(f"Updated {DECK} ({len(prs.slides)} slides)")
