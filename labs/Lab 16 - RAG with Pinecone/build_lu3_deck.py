#!/usr/bin/env python3
"""
LU3 Activity 3 — Customer Care FAQ Chatbot with RAG (Copilot Studio + Pinecone)
Standalone slide deck.

Teaches the RAG concepts (tokenization, embeddings, dimension, semantic search,
chunking, grounding) and then the five-node build, aligned with README.md.

House style: 16:9, all-white slides, Arial, card layouts, no bullet walls.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "screenshots")
OUT = os.path.join(HERE, "LU3-Activity3-Copilot-Studio.pptx")

# ---------------------------------------------------------------- brand
BLUE   = RGBColor(0x1F, 0x6F, 0xEB)
TEAL   = RGBColor(0x10, 0xB9, 0x81)
INK    = RGBColor(0x16, 0x1B, 0x26)
GREY   = RGBColor(0x5B, 0x63, 0x72)
VIOLET = RGBColor(0x7C, 0x3A, 0xED)
LIGHT  = RGBColor(0xF5, 0xF8, 0xFC)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
AMBER  = RGBColor(0xD9, 0x77, 0x06)
RED    = RGBColor(0xDC, 0x26, 0x26)

FONT = "Arial"
W, H = Inches(13.333), Inches(7.5)
COURSE = "Building AI Agents for Work Automation"
COPYRIGHT = "© 2026 Tertiary Infotech Academy Pte Ltd"

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]

_n = 0


def _txt(shape, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT,
         space_after=6, line=None):
    tf = shape.text_frame
    tf.word_wrap = True
    lines = text.split("\n") if isinstance(text, str) else text
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        if line:
            p.line_spacing = line
        r = p.add_run()
        r.text = ln
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return tf


def box(slide, x, y, w, h, text, size, **kw):
    sh = slide.shapes.add_textbox(x, y, w, h)
    _txt(sh, text, size, **kw)
    return sh


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(1.25)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    if s.has_text_frame:
        s.text_frame.text = ""
    return s


def footer(slide):
    global _n
    _n += 1
    y = H - Inches(0.42)
    box(slide, Inches(0.55), y, Inches(4.5), Inches(0.3),
        f"LU3 · Activity 3", 10, color=GREY)
    b = box(slide, Inches(4.6), y, Inches(4.2), Inches(0.3),
            COPYRIGHT, 10, color=GREY, align=PP_ALIGN.CENTER)
    box(slide, W - Inches(1.4), y, Inches(0.85), Inches(0.3),
        str(_n), 10, color=GREY, align=PP_ALIGN.RIGHT)


def slide_base(title, kicker=None):
    s = prs.slides.add_slide(BLANK)
    y = Inches(0.45)
    if kicker:
        box(s, Inches(0.7), y, Inches(11.9), Inches(0.3),
            kicker.upper(), 14, bold=True, color=BLUE)
        y += Inches(0.38)
    box(s, Inches(0.7), y, Inches(11.9), Inches(0.75), title, 29, bold=True)
    line = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7),
                              y + Inches(0.72), Inches(1.15), Pt(4))
    line.fill.solid(); line.fill.fore_color.rgb = BLUE
    line.line.fill.background(); line.shadow.inherit = False
    footer(s)
    return s, y + Inches(1.05)


# ---------------------------------------------------------------- cover
def cover():
    global _n
    s = prs.slides.add_slide(BLANK)
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(0.14))
    band.fill.solid(); band.fill.fore_color.rgb = BLUE
    band.line.fill.background(); band.shadow.inherit = False

    box(s, Inches(0.9), Inches(1.9), Inches(11.5), Inches(0.4),
        "LEARNING UNIT 3 · ACTIVITY 3", 16, bold=True, color=BLUE)
    box(s, Inches(0.9), Inches(2.4), Inches(11.5), Inches(1.5),
        "Customer Care FAQ Chatbot\nwith RAG", 40, bold=True, line=1.05)
    box(s, Inches(0.9), Inches(4.15), Inches(11.5), Inches(0.5),
        "The agent answers only from the brochures — or admits it does not know.",
        19, color=GREY)

    for i, (lbl, val) in enumerate([
        ("PLATFORM", "Copilot Studio"),
        ("VECTOR STORE", "Pinecone"),
        ("DURATION", "90 minutes"),
    ]):
        x = Inches(0.9) + Inches(3.75) * i
        rect(s, x, Inches(5.0), Inches(3.4), Inches(0.95), LIGHT)
        box(s, x + Inches(0.28), Inches(5.14), Inches(3.0), Inches(0.28),
            lbl, 11, bold=True, color=BLUE)
        box(s, x + Inches(0.28), Inches(5.44), Inches(3.0), Inches(0.38),
            val, 15, bold=True)

    box(s, Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.35),
        COURSE, 13, color=GREY)
    box(s, Inches(0.9), Inches(6.82), Inches(11.5), Inches(0.35),
        "Tertiary Infotech Academy Pte Ltd · UEN 201200696W", 11, color=GREY)
    _n += 1


# ---------------------------------------------------------------- layouts
def cards3(title, kicker, items, note=None):
    s, y = slide_base(title, kicker)
    cw = Inches(3.75)
    for i, (h, body) in enumerate(items):
        x = Inches(0.7) + (cw + Inches(0.28)) * i
        accent = [BLUE, TEAL, VIOLET][i % 3]
        card = rect(s, x, y, cw, Inches(3.5), LIGHT)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, cw, Pt(5))
        bar.fill.solid(); bar.fill.fore_color.rgb = accent
        bar.line.fill.background(); bar.shadow.inherit = False
        box(s, x + Inches(0.26), y + Inches(0.3), cw - Inches(0.5),
            Inches(0.6), h, 17, bold=True, color=accent)
        box(s, x + Inches(0.26), y + Inches(0.95), cw - Inches(0.5),
            Inches(2.4), body, 13.5, color=GREY, line=1.3)
    if note:
        box(s, Inches(0.7), y + Inches(3.75), Inches(11.9), Inches(0.5),
            note, 14, color=GREY)
    return s


def content(title, kicker, items, note=None):
    """Numbered visual cards — never a plain bullet wall."""
    s, y = slide_base(title, kicker)
    n = len(items)
    ch = Inches(0.82) if n > 4 else Inches(0.95)
    gap = Inches(0.16)
    for i, item in enumerate(items):
        yy = y + (ch + gap) * i
        rect(s, Inches(0.7), yy, Inches(11.9), ch, LIGHT)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), yy,
                                 Pt(5), ch)
        bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
        bar.line.fill.background(); bar.shadow.inherit = False
        chip = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.98),
                                  yy + (ch - Inches(0.42)) / 2,
                                  Inches(0.42), Inches(0.42))
        chip.fill.solid(); chip.fill.fore_color.rgb = BLUE
        chip.line.fill.background(); chip.shadow.inherit = False
        ctf = chip.text_frame
        ctf.text = str(i + 1)
        ctf.paragraphs[0].alignment = PP_ALIGN.CENTER
        cr = ctf.paragraphs[0].runs[0]
        cr.font.name = FONT; cr.font.size = Pt(15)
        cr.font.bold = True; cr.font.color.rgb = WHITE
        if isinstance(item, tuple):
            head, sub = item
            box(s, Inches(1.62), yy + Inches(0.13), Inches(10.7),
                Inches(0.35), head, 16, bold=True)
            box(s, Inches(1.62), yy + Inches(0.46), Inches(10.7),
                Inches(0.34), sub, 13, color=GREY)
        else:
            box(s, Inches(1.62), yy + (ch - Inches(0.34)) / 2,
                Inches(10.7), Inches(0.34), item, 16)
    if note:
        box(s, Inches(0.7), H - Inches(1.15), Inches(11.9), Inches(0.5),
            note, 13, color=GREY)
    return s


def two_col(title, kicker, left_h, left, right_h, right, note=None):
    s, y = slide_base(title, kicker)
    cw = Inches(5.8)
    # Height follows the longer column so the last line never spills out.
    # Count wrapped lines, not just list items: a long row occupies 2-3 lines in
    # a 5.8" card, and the original height formula assumed one line each.
    def _wrapped(rows, per_line=52):
        n = 0
        for r in rows:
            n += max(1, -(-len(r) // per_line)) if r else 1
        return n
    rows_max = max(_wrapped(left), _wrapped(right))
    fs = 15 if rows_max <= 12 else (13.5 if rows_max <= 16 else 12)
    ch = max(Inches(3.9), Inches(1.0) + Inches(0.245) * rows_max)
    ch = min(ch, H - y - Inches(1.15))
    for i, (h, rows, accent) in enumerate(
            [(left_h, left, BLUE), (right_h, right, TEAL)]):
        x = Inches(0.7) + (cw + Inches(0.3)) * i
        rect(s, x, y, cw, ch, LIGHT)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, cw, Pt(5))
        bar.fill.solid(); bar.fill.fore_color.rgb = accent
        bar.line.fill.background(); bar.shadow.inherit = False
        box(s, x + Inches(0.3), y + Inches(0.28), cw - Inches(0.6),
            Inches(0.45), h, 18, bold=True, color=accent)
        box(s, x + Inches(0.3), y + Inches(0.9), cw - Inches(0.6),
            ch - Inches(1.1), "\n".join(rows), fs, color=GREY, line=1.32,
            space_after=2)
    if note:
        box(s, Inches(0.7), y + ch + Inches(0.2), Inches(11.9), Inches(0.5),
            note, 13, color=GREY)
    return s


def big_statement(text, sub=None, accent=BLUE):
    global _n
    s = prs.slides.add_slide(BLANK)
    box(s, Inches(1.1), Inches(2.5), Inches(11.1), Inches(2.0),
        text, 36, bold=True, line=1.15)
    if sub:
        box(s, Inches(1.1), Inches(4.6), Inches(11.1), Inches(0.8),
            sub, 18, color=GREY, line=1.3)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.1),
                             Inches(2.1), Inches(1.5), Pt(6))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent
    bar.line.fill.background(); bar.shadow.inherit = False
    footer(s)
    return s


def section(num, title, sub=None):
    global _n
    s = prs.slides.add_slide(BLANK)
    box(s, Inches(0.9), Inches(1.5), Inches(6.0), Inches(2.2),
        num, 96, bold=True, color=RGBColor(0xE3, 0xEC, 0xF9))
    box(s, Inches(0.9), Inches(3.5), Inches(11.4), Inches(1.0),
        title, 38, bold=True)
    if sub:
        box(s, Inches(0.9), Inches(4.6), Inches(11.4), Inches(0.6),
            sub, 18, color=GREY)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9),
                             Inches(3.25), Inches(1.5), Pt(6))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background(); bar.shadow.inherit = False
    footer(s)
    return s


def img_slide(title, kicker, img, caption=None, notes=None, crop=None):
    """Screenshot slide. Image fitted, optional right-hand notes.

    crop = (left, top, right, bottom) as fractions, trimming dead space
    (e.g. the large empty area of the Copilot Studio canvas).
    """
    s, y = slide_base(title, kicker)
    path = os.path.join(SHOTS, img)
    if not os.path.exists(path):
        box(s, Inches(0.7), y, Inches(11.9), Inches(0.5),
            f"[missing screenshot: {img}]", 14, color=RED)
        return s
    from PIL import Image
    iw, ih = Image.open(path).size

    cl, ct, cr, cb = crop or (0, 0, 0, 0)
    eff_w = iw * (1 - cl - cr)
    eff_h = ih * (1 - ct - cb)
    ar = eff_w / eff_h

    avail_w = Inches(7.95) if notes else Inches(11.9)
    avail_h = Inches(4.3)
    w = avail_w
    h = Emu(int(w / ar))
    if h > avail_h:
        h = avail_h
        w = Emu(int(h * ar))
    x = Inches(0.7) if notes else Emu(int((W - w) / 2))
    pic = s.shapes.add_picture(path, x, y, width=w, height=h)
    if crop:
        pic.crop_left, pic.crop_top = cl, ct
        pic.crop_right, pic.crop_bottom = cr, cb
    pic.line.color.rgb = RGBColor(0xD5, 0xDD, 0xE8)
    pic.line.width = Pt(1)

    if notes:
        nx = Inches(8.95)
        nw = Inches(3.65)
        # Card height follows the text so nothing overflows the rounded edge.
        need = Inches(0.62) + Inches(0.263) * len(notes)
        nh = max(h, need)
        rect(s, nx, y, nw, nh, LIGHT)
        box(s, nx + Inches(0.28), y + Inches(0.26), nw - Inches(0.56),
            nh - Inches(0.52), "\n".join(notes), 12.5, color=GREY,
            line=1.32, space_after=1)
    if caption:
        box(s, Inches(0.7), y + h + Inches(0.18), Inches(11.9),
            Inches(0.4), caption, 13, color=GREY)
    return s


def flow_diagram(title, kicker, steps, note=None):
    """Horizontal pipeline of labelled boxes with arrows."""
    s, y = slide_base(title, kicker)
    n = len(steps)
    bw = Inches(2.15)
    gap = Inches(0.28)
    total = bw * n + gap * (n - 1)
    x0 = Emu(int((W - total) / 2))
    yy = y + Inches(0.65)
    max_lines = max(sub.count("\n") + 1 for _, sub, _ in steps)
    bh = Inches(1.55) + Inches(0.22) * max(0, max_lines - 2)
    for i, (label, sub, accent) in enumerate(steps):
        x = x0 + (bw + gap) * i
        rect(s, x, yy, bw, bh, LIGHT, line=accent)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, yy, bw, Pt(5))
        bar.fill.solid(); bar.fill.fore_color.rgb = accent
        bar.line.fill.background(); bar.shadow.inherit = False
        box(s, x + Inches(0.16), yy + Inches(0.26), bw - Inches(0.32),
            Inches(0.6), label, 14, bold=True, color=accent,
            align=PP_ALIGN.CENTER, line=1.15)
        box(s, x + Inches(0.16), yy + Inches(0.88), bw - Inches(0.32),
            bh - Inches(1.0), sub, 11.5, color=GREY,
            align=PP_ALIGN.CENTER, line=1.2, space_after=2)
        if i < n - 1:
            ax = x + bw + Inches(0.02)
            ar_ = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, ax,
                                     yy + bh / 2 - Inches(0.11),
                                     Inches(0.24), Inches(0.22))
            ar_.fill.solid(); ar_.fill.fore_color.rgb = RGBColor(0xB6, 0xC2, 0xD4)
            ar_.line.fill.background(); ar_.shadow.inherit = False
    if note:
        box(s, Inches(0.7), yy + bh + Inches(0.5), Inches(11.9),
            Inches(0.9), note, 15, color=GREY, line=1.4)
    return s


def compare_bar(title, kicker, left_label, left_rows, right_label, right_rows,
                verdict=None):
    """Two stacked lists with a verdict strip underneath."""
    s, y = slide_base(title, kicker)
    cw = Inches(5.8)
    def _wrap(rows, per=46):
        return sum(max(1, -(-len(r) // per)) for r in rows if r)
    nlines = max(_wrap(left_rows), _wrap(right_rows))
    nitems = max(len([r for r in left_rows if r]), len([r for r in right_rows if r]))
    ch = max(Inches(3.3), Inches(0.9) + Inches(0.235) * nlines + Inches(0.12) * nitems)
    ch = min(ch, H - y - Inches(1.6))
    for i, (h, rows, accent) in enumerate(
            [(left_label, left_rows, RED), (right_label, right_rows, TEAL)]):
        x = Inches(0.7) + (cw + Inches(0.3)) * i
        rect(s, x, y, cw, ch, LIGHT)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, cw, Pt(5))
        bar.fill.solid(); bar.fill.fore_color.rgb = accent
        bar.line.fill.background(); bar.shadow.inherit = False
        box(s, x + Inches(0.3), y + Inches(0.26), cw - Inches(0.6),
            Inches(0.45), h, 17, bold=True, color=accent)
        box(s, x + Inches(0.3), y + Inches(0.85), cw - Inches(0.6),
            ch - Inches(1.05), "\n".join(r for r in rows if r), 13.5,
            color=GREY, line=1.3, space_after=9)
    if verdict:
        vy = y + ch + Inches(0.28)
        rect(s, Inches(0.7), vy, Inches(11.9), Inches(0.78), RGBColor(0xEF, 0xF6, 0xFF))
        box(s, Inches(1.0), vy + Inches(0.2), Inches(11.3), Inches(0.4),
            verdict, 15, bold=True, color=BLUE)
    return s


def vector_space(title, kicker, note=None):
    """Draws a 2-D 'meaning map' showing why similar text lands close together."""
    s, y = slide_base(title, kicker)
    px, py = Inches(1.4), y + Inches(0.15)
    pw, ph = Inches(6.4), Inches(3.9)
    plot = rect(s, px, py, pw, ph, RGBColor(0xFA, 0xFC, 0xFF), line=RGBColor(0xD5, 0xDD, 0xE8),
                shape=MSO_SHAPE.RECTANGLE)
    pts = [
        (0.20, 0.26, "sourdough\nbrochure", BLUE),
        (0.30, 0.36, '"how much is the\nsourdough course?"', VIOLET),
        (0.26, 0.14, "bread making\nbrochure", BLUE),
        (0.76, 0.74, "sushi\nbrochure", TEAL),
        (0.68, 0.86, "sashimi\nbrochure", TEAL),
    ]
    for fx, fy, lbl, col in pts:
        cx = px + Emu(int(pw * fx)); cy = py + Emu(int(ph * fy))
        d = Inches(0.17)
        dot = s.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, d, d)
        dot.fill.solid(); dot.fill.fore_color.rgb = col
        dot.line.color.rgb = WHITE; dot.line.width = Pt(1.5)
        dot.shadow.inherit = False
        box(s, cx + Inches(0.22), cy - Inches(0.13), Inches(2.3), Inches(0.5),
            lbl, 11, color=col if col != VIOLET else VIOLET, bold=(col == VIOLET),
            line=1.15)
    # the "near" bracket
    box(s, px + Inches(0.35), py + ph - Inches(0.55), Inches(5.6), Inches(0.4),
        "Distance here = difference in meaning, not in spelling.", 12, color=GREY)

    nx = Inches(8.3)
    rect(s, nx, py, Inches(4.3), ph, LIGHT)
    box(s, nx + Inches(0.3), py + Inches(0.28), Inches(3.7), Inches(0.4),
        "What the picture shows", 15, bold=True, color=BLUE)
    box(s, nx + Inches(0.3), py + Inches(0.8), Inches(3.7), ph - Inches(1.1),
        "The question lands next to the sourdough brochure and far from the "
        "sushi one — even though the question and the brochure share almost no "
        "words.\n\n"
        "A keyword search would need the exact word. A vector search needs only "
        "the meaning.\n\n"
        "Real embeddings do this in 1024 dimensions, not 2. You cannot draw "
        "that, but the idea is identical: near = similar.",
        13, color=GREY, line=1.35)
    if note:
        box(s, Inches(0.7), py + ph + Inches(0.25), Inches(11.9), Inches(0.5),
            note, 13.5, color=GREY)
    return s


def test_slide(title, kicker, rows, note=None):
    """Test table. Rows are (case, input, expected, accent) — accent colours
    the expected cell so the hallucination probes read as different in kind."""
    s, y = slide_base(title, kicker)
    rect(s, Inches(0.7), y, Inches(11.9), Inches(0.5),
         RGBColor(0xE7, 0xF8, 0xF1))
    for lbl, x, w in [("CASE", Inches(1.0), Inches(1.0)),
                      ("QUESTION", Inches(2.0), Inches(6.3)),
                      ("A GOOD ANSWER", Inches(8.5), Inches(3.9))]:
        box(s, x, y + Inches(0.12), w, Inches(0.3), lbl, 11.5,
            bold=True, color=TEAL)
    for i, row in enumerate(rows):
        case, inp, exp = row[0], row[1], row[2]
        accent = row[3] if len(row) > 3 else TEAL
        yy = y + Inches(0.54) + Inches(0.405) * i
        if i % 2 == 0:
            rect(s, Inches(0.7), yy, Inches(11.9), Inches(0.4), LIGHT)
        box(s, Inches(1.0), yy + Inches(0.06), Inches(1.0), Inches(0.3),
            case, 13, bold=True, color=accent)
        box(s, Inches(2.0), yy + Inches(0.06), Inches(6.3), Inches(0.3),
            inp, 12.5, color=GREY)
        box(s, Inches(8.5), yy + Inches(0.06), Inches(3.9), Inches(0.3),
            exp, 12.5, bold=True, color=accent)
    if note:
        box(s, Inches(0.7), y + Inches(0.60) + Inches(0.405) * len(rows),
            Inches(11.9), Inches(0.8), note, 13.5, color=GREY, line=1.35)
    return s


# ================================================================= CONTENT
cover()

# ---------------------------------------------------------------- the problem
section("01", "Why RAG?", "The problem that retrieval solves")

cards3("The Customer Care Problem", "Scenario",
       [("40 times a day",
         "Cook & Bake Academy runs 20 courses across two campuses. Two people "
         "answer the same questions: how much, how long, where, what level."),
        ("The answer already exists",
         "It is in the course brochures. Nobody is short of information — "
         "somebody has to find the right file, read it, and retype a sentence."),
        ("Memory drifts",
         "When the team is busy they answer from memory. Last month someone "
         "quoted a fee that was six months out of date.")],
       note="A language model could answer all of this — if it had ever seen the brochures.")

two_col("Why Not Just Paste the Brochures In?", "The naive approach",
        "Paste all 20 into the prompt",
        ["Works today, with 20 short brochures.",
         "",
         "Then the academy adds 40 more courses.",
         "",
         "The prompt exceeds what the model can read.",
         "",
         "It starts ignoring the middle of long input.",
         "",
         "Every question costs the price of 60 brochures."],
        "Retrieve only what is needed",
        ["Search for the 3 brochures that resemble the question.",
         "",
         "Send only those.",
         "",
         "Cost stays flat as the catalogue grows.",
         "",
         "The model reads 3 documents carefully instead of 60 badly.",
         "",
         "This is RAG."],
        note="RAG is not a smarter model. It is a smaller, better-chosen prompt.")

big_statement("Retrieval Augmented Generation",
              "Retrieve the few documents that answer the question, then let the "
              "model generate an answer from those and nothing else.")

cards3("What RAG Is Not", "Clearing three misconceptions",
       [("Not fine-tuning",
         "No training. No model weights change. You are choosing what goes in "
         "the prompt, not rebuilding the model."),
        ("Not a database query",
         "There is no exact match. You ask for the nearest meanings, and you "
         "always get results — even for a question nothing answers."),
        ("Not a guarantee",
         "Retrieval supplies facts. Only the instruction stops the model adding "
         "its own. Both halves are required.")],
       note="If you remember one thing: RAG changes the prompt, not the model.")

# ---------------------------------------------------------------- concepts
section("02", "How It Works", "Tokens, embeddings, dimensions, similarity")

content("Step 0 — Tokenization: How a Model Reads Text", "Concept 1 of 4",
        [("A model never sees letters — it sees tokens",
          "Text is split into pieces of roughly ¾ of a word. \"sourdough\" might be "
          "two tokens: \"sour\" + \"dough\"."),
         ("Everything is counted in tokens",
          "Context limits, pricing and speed are all measured in tokens — not "
          "words, not characters."),
         ("A rule of thumb for English",
          "1 token ≈ 4 characters ≈ ¾ of a word. One 2,700-character brochure is "
          "roughly 700 tokens."),
         ("Why this matters for RAG",
          "20 brochures ≈ 14,000 tokens in every prompt. Retrieve 3 instead and "
          "you send ~2,100 — the same answer for a seventh of the input.")],
        note="Tokenization is why \"just paste everything in\" has a ceiling, and why retrieval saves money.")

two_col("Tokenization, On One Real Sentence", "Concept 1, made concrete",
        "The sentence a customer typed",
        ["“How much is the sourdough course?”",
         "",
         "The model does not see 7 words. It sees 8 tokens:",
         "",
         "How | much | is | the | sour | dough | course | ?",
         "",
         "“sourdough” is rare enough that the tokenizer splits it into "
         "two familiar pieces.",
         "",
         "Punctuation counts — the “?” is a token of its own."],
        "Why you should care",
        ["Tokens are the unit of BILLING. Not words, not characters.",
         "",
         "Tokens are the unit of the CONTEXT LIMIT. “Too long” is measured "
         "here.",
         "",
         "Rare words cost more. A brochure full of “viennoiserie” and "
         "“sashimi” splits into more pieces than one about “bread”.",
         "",
         "English ≈ 4 characters per token. A 2,700-character brochure is "
         "~700 tokens; twenty of them ~14,000 — in every prompt, if you "
         "paste them all in."],
        note="Count the tokens in your own text at platform.openai.com/tokenizer — the split is often surprising.")

content("Step 1 — Embedding: Turning Text Into Coordinates", "Concept 2 of 4",
        [("Text in, numbers out",
          "An embedding model converts a piece of text into a fixed-length list "
          "of numbers — a vector."),
         ("Position encodes meaning",
          "The model places text so that similar meanings land near each other. "
          "This is learned, not programmed."),
         ("Same model, every time",
          "Brochures and questions must be embedded by the SAME model, or the "
          "coordinates are not comparable."),
         ("In this lab it is invisible",
          "Pinecone's hosted model (llama-text-embed-v2) embeds server-side. You "
          "send text, not numbers.")],
        note="An embedding is a position in meaning-space. Nothing more mysterious than that.")

content("Embedding, On Four Real Phrases", "Concept 2, made concrete",
        [("\"How much is the sourdough course?\"",
          "→  [0.021, −0.184, 0.077, … ]   1024 numbers. Lands in the bread "
          "region of meaning-space."),
         ("\"What does BAK-101 cost?\"",
          "→  [0.019, −0.176, 0.081, … ]   Almost the SAME numbers — different "
          "words, same meaning."),
         ("\"How much is the sushi course?\"",
          "→  [−0.203, 0.115, −0.042, … ]  Very different numbers. One word "
          "changed; the meaning moved."),
         ("\"sourdough\" (the word alone)",
          "→  near the first two, but not identical. A word and a question "
          "about that word are related, not the same.")],
        note="Rows 1 and 2 share almost no letters and nearly all of their meaning. That gap is exactly what keyword search cannot cross.")

vector_space("Semantic Search: Near Means Similar", "Concept 3 of 4",
             note="This is why a customer who misspells “viennoiserie” still finds BAK-102.")

compare_bar("Keyword Search vs Vector Search", "Concept 3, continued",
            "Keyword search — matches characters",
            ["“viennoiserie” misspelt  →  zero results.",
             "",
             "“french pastry classes”  →  no match, because the brochure "
             "never uses the word “classes”.",
             "",
             "Finds documents that contain your letters.",
             "",
             "Fails silently on synonyms, plurals and typos."],
            "Vector search — matches meaning",
            ["“vienoiserie” (misspelt)  →  still finds BAK-102.",
             "",
             "“french pastry classes”  →  finds BAK-102 French Pastry & "
             "Viennoiserie.",
             "",
             "Finds documents that mean what you asked.",
             "",
             "Always returns something — even for a question nothing answers."],
            verdict="That last line cuts both ways: vector search never says “no results”. "
                    "Guarding against a confident answer built on a poor match is the instruction's job.")

content("Step 2 — Dimension: How Many Numbers", "Concept 4 of 4",
        [("The dimension is the length of the vector",
          "llama-text-embed-v2 produces 1024 numbers per piece of text. Gemini's "
          "gemini-embedding-001 produces 3072."),
         ("More dimensions ≠ better",
          "It is a different model with a different trade-off between nuance, "
          "storage and speed. Not a quality dial."),
         ("The index is fixed at one dimension",
          "An index built for 1024 accepts 1024-length vectors and nothing else."),
         ("The rule you cannot break",
          "ingestion model == query model == the index's dimension. All three, "
          "or the search is meaningless.")],
        note="Break rule 4 and you get either a loud error or — far worse — quietly poor results.")

two_col("The Two Ways Dimension Bites You", "Failure modes",
        "Loud failure — you will notice",
        ["A 1536-dim query against a 3072-dim index.",
         "",
         "Pinecone rejects it with an error naming both numbers.",
         "",
         "Annoying, but it stops you immediately.",
         "",
         "Fixed in five minutes."],
        "Silent failure — you will not",
        ["Both models give 3072 numbers — but they are different models.",
         "",
         "The index accepts every vector. No error, ever.",
         "",
         "Retrieval just returns slightly wrong brochures, forever.",
         "",
         "This is the one that reaches production."],
        note="Gemini also needs taskType RETRIEVAL_DOCUMENT when ingesting and RETRIEVAL_QUERY when "
             "searching. Both return 3072 numbers, so getting it wrong throws no error at all.")

content("Step 3 — Chunking: The Biggest Lever", "The setting that decides quality",
        [("A chunk is the unit that gets embedded and returned",
          "Search does not return “a document”. It returns whichever chunk "
          "matched."),
         ("Chunk too small: 1,000 characters",
          "A 2,700-character brochure becomes 3 fragments. The fragment saying "
          "“sourdough” is not the fragment saying “S$680”."),
         ("The result is an honest, useless answer",
          "Retrieval finds the sourdough fragment. The agent never sees the fee. "
          "It tells the customer it does not know the price. No error is raised."),
         ("This lab: one brochure = one chunk",
          "2,700 characters, well within the model's 2,048-token limit. One "
          "search returns the code, the fee, the duration and the campus together.")],
        note="The rule: a chunk is the smallest piece of text that still answers a question on its own. "
             "For a brochure that is the whole brochure. For a 400-page manual it is not.")

flow_diagram("The RAG Pipeline, End to End", "Putting the four concepts together",
             [("20 brochures", "SharePoint\nthe source of truth", GREY),
              ("Embed", "each brochure →\n1024 numbers", VIOLET),
              ("Store", "Pinecone index\n20 vectors", BLUE),
              ("Search", "question → vector\n→ 3 nearest", TEAL),
              ("Generate", "agent answers from\nthose 3 only", AMBER)],
             note="The first three run ONCE (ingestion). The last two run on EVERY question (retrieval). "
                  "That split is why RAG is cheap to operate and slow to set up.")

# ---------------------------------------------------------------- the build
section("03", "The Build", "Five nodes, one flow")

img_slide("What You Are Building", "The deliverable", "lu3-01-hero.png",
          caption="The academy's website. The 💬 button opens a chat widget that posts to your flow.",
          crop=(0, 0, 0, 0.10))

flow_diagram("One Flow, Five Nodes", "Copilot Studio · Lab 3 - RAG",
             [("Trigger", "HTTP request\nthe question", GREY),
              ("HTTP", "POST to Pinecone\nretrieval", BLUE),
              ("Compose", "question +\nbrochures", VIOLET),
              ("Agent", "writes the\nanswer", TEAL),
              ("Response", "{ reply }\nback to browser", AMBER)],
             note="Plus Task 1, which ran once before any of this existed: create the index, upload the 20 "
                  "brochures as text. Notice there is no embeddings node — Pinecone hosts the model.")

content("Task 1 — Ingest: Create the Index", "Run once, before any flow exists",
        [("POST /indexes/create-for-model",
          "One call creates a serverless index with an INTEGRATED embedding "
          "model — Pinecone hosts the model, so you upload words, not numbers."),
         ("model: llama-text-embed-v2",
          "1024 dimensions, 2048-token limit. You did not pick the dimension — "
          "it is a property of the model."),
         ("field_map: { text: chunk_text }",
          "THE embedding configuration. It says: embed whatever arrives in the "
          "field called chunk_text."),
         ("Get that name wrong and nothing errors",
          "Records are stored with no vector at all. Retrieval returns nothing, "
          "forever, and no log says why.")],
        note="python3 ingest_brochures.py  —  the script is 150 commented lines and is the only place "
             "in this lab where the embedding decisions are visible.")

content("Task 1 — Ingest: Upload the Brochures", "As text, not as vectors",
        [("POST /records/namespaces/__default__/upsert",
          "Content-Type: application/x-ndjson — one JSON object per line, no "
          "wrapping array, no commas between lines."),
         ("One record per brochure, whole",
          "{\"_id\":\"BAK-101\", \"chunk_text\":\"…2,740 characters…\", "
          "\"course_code\":\"BAK-101\"}"),
         ("chunk_text is embedded — everything else is metadata",
          "source and course_code come back with each hit and can be filtered "
          "on. They are never embedded."),
         ("Verify before you build the flow",
          "20 vectors in the index, and “How much is the sourdough course?” "
          "returns BAK-101 at 0.53. If that fails, no flow will save you.")],
        note="~685 tokens per brochure — comfortably inside the model's 2,048-token limit, so nothing "
             "is truncated and nothing is split.")

compare_bar("Where Did the Embedding Model Go?", "The big difference from n8n",
            "n8n Activity 3 — you attach it TWICE",
            ["Vector Store node  +  Embeddings node.",
             "",
             "Retrieval tool  +  Embeddings node.",
             "",
             "You pick the model: gemini-embedding-001, 3072 dims.",
             "",
             "taskType: passage to write, query to read.",
             "",
             "Get either wrong → no error, quietly worse."],
            "This lab — it lives inside the index",
            ["The flow has ONE HTTP node. No embeddings node anywhere.",
             "",
             "You send the sentence. Pinecone embeds it server-side.",
             "",
             "The model was fixed when the index was created.",
             "",
             "passage-vs-query is handled by the index.",
             "",
             "Nothing to mismatch — there is nothing to choose."],
            verdict="You bought: a whole class of silent failure, removed. You paid: you cannot change the "
                    "model, the dimension, or use a domain-specific embedding without rebuilding the index.")

img_slide("The Flow on the Canvas", "What it looks like when finished",
          "lu3-04-flow-canvas.png",
          caption="Published, five nodes, no “Needs setup” badges.",
          crop=(0.04, 0.45, 0.02, 0.28))

img_slide("Task 0 — The Brochures in SharePoint", "Where the truth lives",
          "lu3-06-sharepoint.png",
          notes=["Create a NEW site — do not reuse another lab's.",
                 "",
                 "The search and knowledge connectors index at folder level. Point a course "
                 "assistant at a library that also holds banking policy and it will answer a "
                 "sourdough question out of a KYC document.",
                 "",
                 "Confirm the library shows 20 items. Nineteen means one upload silently "
                 "failed — and that course becomes an “I don't have that” you will blame on "
                 "the agent."],
          crop=(0, 0.06, 0, 0.05))

img_slide("Task 2 — The HTTP Node: Retrieval", "The first half of RAG",
          "lu3-05-http-node.png",
          notes=["Method is a SEPARATE dropdown — do not type POST into the URI.",
                 "",
                 "__default__ is literal. Pinecone's default namespace is \"\" in its stats "
                 "but __default__ in the URL path.",
                 "",
                 "Three headers. Paste the KEY, not the words PINECONE_API_KEY — Power "
                 "Automate cannot read a .env file.",
                 "",
                 "The key goes in Headers, never in Authentication.",
                 "",
                 "Body sends the question as plain text. Pinecone embeds it server-side."],
          crop=(0.70, 0.14, 0.01, 0.02))

content("Task 3 — The Compose Node", "Building the prompt",
        [("The Agent node has NO input field",
          "Only Instructions. So the per-question data has to be assembled "
          "somewhere else, and referenced from there."),
         ("concat() glues three things together",
          "The customer's question, a label, and the retrieved brochures."),
         ("string() does the escaping",
          "The HTTP response is JSON full of quotes and newlines. string() turns "
          "it into safe text. Without it the prompt breaks."),
         ("It is also your debugger",
          "Compose's output appears in the run history — so you can see exactly "
          "what the agent was given, which is how you diagnose an empty answer.")],
        note="concat('Customer question: ', triggerBody()?['message'], '\\n\\nCourse brochures:\\n', string(body('HTTP')))")

content("Task 4 — The Agent Node: Generation", "The second half of RAG",
        [("Instructions carry the rules, not the facts",
          "Answer only from the brochures. Never invent a fee, date, duration, "
          "code, instructor or discount. Say so when you do not know."),
         ("Then insert the Compose reference with the ⚡ picker",
          "Put the cursor at the end of the instructions and pick Compose → "
          "Outputs from the dynamic content tree. A blue chip appears."),
         ("NEVER paste an expression into Instructions",
          "It is a rich-text editor. Pasted references are stored as plain text "
          "or have their underscores escaped."),
         ("A broken reference resolves to EMPTY, not an error",
          "The node stays green, the run succeeds, and the agent silently "
          "receives nothing at all.")],
        note="Symptom: the agent replies “the course brochures weren't included in your message”. "
             "It is telling you exactly what is wrong, in the one place nobody looks.")

big_statement("A reference to nothing\nresolves to empty — not an error.",
              "Green node. Successful run. No answer. This one failure mode costs more "
              "debugging time than every other mistake in this lab combined.",
              accent=RED)

content("Task 5 — The Response Node", "Getting the answer back to the browser",
        [("Status code 200, body { \"reply\": … }",
          "The chat widget reads data.reply. A different shape shows "
          "[object Object] in the bubble."),
         ("The field is called Agent Response — not text",
          "Use the ⚡ picker. Typing body/text yields an empty string with no "
          "error, and the flow looks broken for reasons unrelated to RAG."),
         ("Then PUBLISH — not just Save",
          "The HTTP endpoint serves the PUBLISHED version. Check ⋯ → Version "
          "history: LIVE and CURRENT DRAFT must match."),
         ("Copy the HTTP POST URL from the trigger",
          "It ends with sig=… — if that is missing, the URL was truncated on "
          "copy and every call will fail.")])

# ------------------------------------------------- lab 3a: knowledge base
section("04", "The Same Bot, Without the Vector Store",
        "Lab 3a — a built-in knowledge base")

big_statement("In Copilot Studio,\nRAG is not a node.",
              "No ingestion workflow. No embedding model. No vector store. No chunk "
              "size. No top_k. Attach a SharePoint folder to the Agent node and "
              "retrieval simply happens.",
              accent=TEAL)

flow_diagram("Lab 3a — Three Nodes", "The entire flow",
             [("Trigger", "the question\narrives", GREY),
              ("Agent", "searches Knowledge,\nthen answers", TEAL),
              ("Response", "{ reply }\nback to browser", AMBER)],
             note="Lab 3b needed five nodes, a Python ingestion script, a Pinecone index and an API key. "
                  "Everything in the middle collapsed into one setting on the Agent node.")

content("What Replaced the Ingestion Half", "Where the work went",
        [("Upload the 20 brochures to SharePoint",
          "A folder called CourseBrochures. That is the ingestion step — there "
          "is no script and nothing to run."),
         ("Point the Agent's Knowledge at that folder",
          "Knowledge → + → SharePoint → paste the folder URL. There is no file "
          "upload in the picker; SharePoint is the only route in."),
         ("Wait for SharePoint to index",
          "Minutes, not seconds, and there is no progress bar. A source that is "
          "still indexing returns nothing, and the agent looks broken when it "
          "is merely empty."),
         ("Change the instruction wording",
          "Lab 3b says \"the brochures provided below\". Nothing is provided "
          "below here — the agent must SEARCH. This one line is the whole "
          "difference, and getting it wrong costs an afternoon.")],
        note="Point at the FOLDER, not the library root — a shared root will answer a sourdough question out of a banking policy.")

big_statement("An empty answer means the\ninstruction premise is wrong.",
              "Lab 3a built by copying Lab 3b inherits \"answer using only the brochures "
              "provided below\" — with nothing below it. The agent is told its only "
              "source is empty, so it returns nothing at all. Not even a refusal. "
              "The run is green and takes 25 seconds.",
              accent=RED)

img_slide("Same Question. Same Answer. No Vector Store.",
          "Lab 3a, in the browser", "lu3-02-chat-answer.png",
          notes=["The customer asks the same TC1 question and gets the same grounded "
                 "answer — BAK-101, SGD $680, 4 weeks, the early-bird discount.",
                 "",
                 "Behind this reply there is no Pinecone index, no ingestion script, "
                 "no API key and no embedding model. Just a SharePoint folder attached "
                 "to the Agent node.",
                 "",
                 "Nothing about the page changed. Nothing about the agent's rules "
                 "changed. You replaced the entire retrieval half and the chatbot did "
                 "not notice — which is the debrief question worth asking."])

compare_bar("Built-in Knowledge Base vs External Vector Store",
            "The decision this lab exists to inform",
            "Built-in knowledge base  (Lab 3a)",
            ["+  Three nodes. No ingestion, no API key, no index.",
             "+  Nothing to mismatch — no dimension, no second model.",
             "+  Re-crawls on its own when a document changes.",
             "+  Permissions follow SharePoint.",
             "",
             "−  No chunk size, no top_k, no model, no metric.",
             "−  Citation markers leak into the reply.",
             "−  Indexing you cannot observe or trigger."],
            "External vector store  (Lab 3b)",
            ["+  You own all four levers.",
             "+  Portable — the same index serves n8n or a script.",
             "+  Retrieval is inspectable in the run history.",
             "+  Scales past a document library.",
             "",
             "−  Five nodes, a script, an API key, an index.",
             "−  Four new failures: dimension, credential, namespace, name.",
             "−  A changed document needs a RE-INGEST."],
            verdict="Choose by asking who maintains it. Levers you never pull are pure cost; "
                    "levers you need and do not have are a rebuild.")

two_col("When Each One Is The Right Answer", "Not a tie — it depends on the question",
        "Reach for the built-in knowledge base",
        ["The documents already live in SharePoint, and someone already "
         "maintains them.",
         "",
         "The corpus is small — tens to low hundreds of documents.",
         "",
         "Nobody on the team wants to own a database.",
         "",
         "Document permissions matter and must be inherited.",
         "",
         "You need it working this afternoon."],
        "Reach for an external vector store",
        ["Retrieval quality is the product, and you will need to tune it.",
         "",
         "The corpus is large, growing, or not in Microsoft 365 at all.",
         "",
         "The same knowledge must serve more than one application.",
         "",
         "You need to see exactly what was retrieved for a given answer.",
         "",
         "Audit rules demand a reproducible pipeline."],
        note="The honest default for a 20-brochure FAQ is the built-in one. Lab 3b exists so you know what you gave up.")

content("What the Convenience Actually Cost", "The four hidden decisions",
        [("Chunking — the biggest lever, now invisible",
          "Lab 3b keeps each brochure whole, so one hit returns the code, fee, "
          "duration and campus together. Lab 3a chunks however it likes, and "
          "you cannot see or change it."),
         ("top_k — how many documents reach the prompt",
          "Lab 3b sets 3. Lab 3a decides for you. When TC6 answers about "
          "macarons and goes quiet about cookies, retrieval returned one "
          "document — and there is no setting to raise."),
         ("The embedding model and its dimension",
          "Lab 3b: llama-text-embed-v2, 1024, printed by the ingestion script. "
          "Lab 3a: unknown, unstated, unchangeable."),
         ("What you can do when it answers badly",
          "Lab 3b gives you four levers. Lab 3a gives you the prompt. That is "
          "the entire difference, and it only shows up on the day it retrieves "
          "the wrong brochure.")],
        note="Neither is wrong. But you cannot make this trade knowingly unless you have built both — which is why this lab has two halves.")

# ---------------------------------------------------------------- CORS
section("05", "CORS", "Why the browser blocks an answer the flow already sent")

content("What CORS Is", "The rule that surprises everyone once",
        [("A webpage may not read a response from another origin",
          "Origin = scheme + host + port. A page on localhost:8000 calling "
          "*.powerplatform.com is cross-origin, and the browser polices it."),
         ("The SERVER decides, the BROWSER enforces",
          "The server must send Access-Control-Allow-Origin. If it does not, "
          "the browser discards a response it already received."),
         ("Only browsers care",
          "curl, Postman and your flow's own HTTP node ignore CORS entirely. "
          "That is why a curl test can pass while the web page fails."),
         ("The tell-tale pair",
          "\"Failed to fetch\" in the page + a GREEN run in Activity. The "
          "request arrived, the flow worked, the answer was blocked on the way "
          "back.")],
        note="CORS protects the USER from a malicious page reading their data elsewhere — it is not about protecting your flow.")

flow_diagram("Preflight — The Request Before The Request", "What the browser does first",
             [("OPTIONS", "browser asks:\nmay I POST here?", GREY),
              ("204 + headers", "server replies:\nallow-origin", BLUE),
              ("POST", "only now does the\nreal request go", VIOLET),
              ("Response", "read only if the\nheaders allowed it", AMBER)],
             note="A POST with Content-Type: application/json always triggers preflight. If OPTIONS fails, your POST never happens at all.")

two_col("CORS In This Lab — Measured, Not Assumed", "Verified against a live tenant",
        "The old advice was wrong",
        ["For years the guidance was: “Power Automate sends no CORS "
         "header — serve the page from SharePoint.”",
         "",
         "Tested with curl —  OPTIONS <flow url>,  Origin: null",
         "→  204",
         "→  access-control-allow-origin: *",
         "→  access-control-allow-headers: content-type",
         "",
         "And Origin: null IS what file:// sends."],
        "So what you can actually do",
        ["Double-click index.html. It works.",
         "",
         "No local web server. No SharePoint hosting. No proxy. No "
         "browser flags.",
         "",
         "Never disable web security to make a lab work — it is global, "
         "and here there was nothing to work around."],
        note="Classic Power Automate (*.logic.azure.com) may still differ — check the host, then test.")

big_statement("“Failed to fetch” plus a green run\nis a diagnosis, not a mystery.",
              "The request arrived and the flow ran. Only the reply was blocked. "
              "Before blaming CORS, check the two cheaper causes: the URL lost its "
              "sig= on copy, or the flow was saved but never Published.",
              accent=AMBER)

# ---------------------------------------------------------------- testing
section("06", "Testing", "Try to make it lie")

img_slide("It Works — A Grounded Answer", "TC1",
          "lu3-02-chat-answer.png",
          notes=["Course code BAK-101. Fee SGD $680. Duration 4 weeks. Intakes Jan, Apr, "
                 "Jul, Oct. The 10% early-bird discount. The enrolment phone and email.",
                 "",
                 "Every one of those facts is in the brochure. None came from the model's "
                 "own training.",
                 "",
                 "Round trip: about 15 seconds. Set expectations in class — this is not a "
                 "database lookup."],
          crop=(0.50, 0.18, 0.02, 0.04))

test_slide("Ten Test Cases", "sample-questions.csv",
           [("TC1", "How much is the sourdough course?", "BAK-101 + exact fee", TEAL),
            ("TC2", "How long is the French Pastry course?", "BAK-102 + duration", TEAL),
            ("TC3", "Where are your campuses?", "Both, with addresses", TEAL),
            ("TC4", "Cooking courses for beginners?", "Two or three, not twenty", TEAL),
            ("TC5", "What is CUL-203 about?", "Sushi & Sashimi + curriculum", TEAL),
            ("TC6", "Cheaper — macarons or cookies?", "Both fees + which", TEAL),
            ("TC7", "Vietnamese pho course?", "WE DON'T RUN THAT", RED),
            ("TC8", "Who teaches the macaron class?", "NOT IN OUR INFORMATION", RED),
            ("TC9", "The 40% alumni discount on sushi?", "DOES NOT CONFIRM IT", RED),
            ("TC10", "Recommend a restaurant?", "Declines, steers back", AMBER)],
           note="The first six prove retrieval works. The last four are the ones that matter.")

img_slide("TC7 — The Agent Refuses to Invent", "The slide that justifies the lab",
          "lu3-03-refusal.png",
          notes=["Asked for a course the academy does not run.",
                 "",
                 "It says so plainly — then offers CUL-202 Thai Street Food and CUL-208 "
                 "Vegetarian & Vegan, with their real fees.",
                 "",
                 "An ungrounded model would have invented a pho course, a fee and a "
                 "schedule. Fluently. And the customer would have quoted it back to you.",
                 "",
                 "Retrieval alone would not have produced this. The instruction “if we do "
                 "not run a course, say so plainly” is what turns a weak match into an "
                 "honest refusal."],
          crop=(0.50, 0.16, 0.02, 0.04))

cards3("The Three Probes, and Why They Are Different", "Adversarial testing",
       [("TC7 — a thing that does not exist",
         "Invites the model to invent a course. Easy to resist, because nothing "
         "in the brochures resembles it."),
        ("TC8 — a fact in no brochure",
         "Instructors are not in the course information. The model must "
         "distinguish “not retrieved” from “does not exist”."),
        ("TC9 — a false premise",
         "The nastiest. The question ASSUMES a 40% discount exists. A model that "
         "wants to be helpful confirms it.")],
       note="Any confident answer to these is a failure, however fluent. If yours invents an instructor, "
            "do not add instructors to the brochures — fix the instruction, then ask what else it might invent.")

two_col("Grounding: The Four Lines That Do the Work", "Why retrieval alone is not enough",
        "What retrieval gives you",
        ["The three most similar brochures.",
         "",
         "That is all. It is a search engine, not a conscience.",
         "",
         "It always returns something — even when nothing fits.",
         "",
         "A weak match still looks like a match."],
        "What the instruction must add",
        ["Answer ONLY from the brochures below.",
         "",
         "If they do not answer it, say “I don't have that”.",
         "",
         "Never invent a fee, date, duration, code, instructor or discount.",
         "",
         "If we do not run a course, say so, then list the closest."],
        note="Retrieval supplies the facts. The instruction forbids everything else. Ship one without "
             "the other and you have a confident liar or a useless one.")

# ---------------------------------------------------------------- debrief
section("07", "Debrief", "What you built, and what it cost")

content("What the Platform Chose For You", "The price of convenience",
        [("Embedding model — llama-text-embed-v2",
          "You never picked one. Change it and every stored vector becomes "
          "meaningless until you re-ingest."),
         ("Dimension — 1024",
          "Fixed when the index was created. You cannot change it; you create a "
          "new index."),
         ("Chunking — one brochure, one record",
          "The single most consequential setting in the system, decided at "
          "upload time, invisible afterwards."),
         ("Retrieved count — top_k: 3",
          "The one knob you did turn. Set it to 1 and comparisons fail; set it "
          "to 20 and you are back to pasting the catalogue.")],
        note="This is a genuine feature and a genuine cost: you cannot tune what you cannot see.")

test_slide("Five Questions for the Room", "Debrief",
           [("1", "The bot said “I don't have that” for TC8", "Good answer or bad?", BLUE),
            ("2", "top_k is 3 — try 1, then 20", "Which failure is worse?", BLUE),
            ("3", "Change a fee and re-ingest", "Who owns accuracy now?", BLUE),
            ("4", "LU1 matched an NRIC exactly; this matches meaning", "When do you choose which?", BLUE),
            ("5", "You never chose an embedding model", "When does that stop being OK?", BLUE)],
           note="Question 3 is the one that changes how a team organises itself: the person who maintains "
                "the brochures now owns what the chatbot says.")

cards3("The Three Failures Worth Remembering", "Hard-won, in this order",
       [("A reference that resolves to empty",
         "Pasted into the rich-text Instructions box. Green node, successful "
         "run, no answer. Insert with the ⚡ picker, never paste."),
        ("The wrong output field",
         "Agent Response, not text. Guessing gives you an empty string and no "
         "error to explain it."),
        ("The key that was a variable name",
         "PINECONE_API_KEY pasted as the header VALUE. Power Automate cannot "
         "read a .env file. Unauthorized.")],
       note="All three fail quietly. None of them is about RAG — and together they cost more time than "
            "the retrieval, the embedding and the grounding combined.")

big_statement("RAG changes the prompt,\nnot the model.",
              "Retrieve the few documents that answer the question. Instruct the model to "
              "use nothing else. Then spend your testing time trying to make it lie.")

prs.save(OUT)
print("saved:", OUT, "·", len(prs.slides._sldIdLst), "slides")
