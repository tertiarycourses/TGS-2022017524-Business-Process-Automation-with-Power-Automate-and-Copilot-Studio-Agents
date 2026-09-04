#!/usr/bin/env python3
"""
LU1 Activity 1 — Retail Banking Customer Onboarding (Copilot Studio)
Standalone slide deck.

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
OUT = os.path.join(HERE, "LU1-Activity1-Copilot-Studio.pptx")

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
        f"LU1 · Activity 1", 10, color=GREY)
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
        "LEARNING UNIT 1 · ACTIVITY 1", 16, bold=True, color=BLUE)
    box(s, Inches(0.9), Inches(2.4), Inches(11.5), Inches(1.5),
        "Retail Banking\nCustomer Onboarding", 44, bold=True, line=1.05)
    box(s, Inches(0.9), Inches(4.15), Inches(11.5), Inches(0.5),
        "Build an AI agent that decides account applications end to end",
        19, color=GREY)

    for i, (lbl, val) in enumerate([
        ("PLATFORM", "Microsoft Copilot Studio"),
        ("DATA", "SharePoint Lists"),
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
    rows_max = max(len(left), len(right))
    ch = max(Inches(3.9), Inches(1.05) + Inches(0.335) * rows_max)
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
            ch - Inches(1.1), "\n".join(rows), 15, color=GREY, line=1.4,
            space_after=3)
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


def rules_ladder(title, kicker, rules, note=None):
    """The six ordered rules, as a stop-at-first-match ladder."""
    s, y = slide_base(title, kicker)
    rh = Inches(0.6)
    gap = Inches(0.1)
    for i, (step, check, outcome, accent) in enumerate(rules):
        yy = y + (rh + gap) * i
        rect(s, Inches(0.7), yy, Inches(11.9), rh, LIGHT)
        chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                  Inches(0.85), yy + Inches(0.11),
                                  Inches(0.95), Inches(0.38))
        chip.fill.solid(); chip.fill.fore_color.rgb = accent
        chip.line.fill.background(); chip.shadow.inherit = False
        ctf = chip.text_frame
        ctf.text = step
        ctf.paragraphs[0].alignment = PP_ALIGN.CENTER
        cr = ctf.paragraphs[0].runs[0]
        cr.font.name = FONT; cr.font.size = Pt(12)
        cr.font.bold = True; cr.font.color.rgb = WHITE
        box(s, Inches(2.0), yy + Inches(0.15), Inches(6.2), Inches(0.34),
            check, 14)
        box(s, Inches(8.4), yy + Inches(0.15), Inches(4.0), Inches(0.34),
            outcome, 14, bold=True, color=accent, align=PP_ALIGN.RIGHT)
    if note:
        box(s, Inches(0.7), y + (rh + gap) * len(rules) + Inches(0.2),
            Inches(11.9), Inches(0.7), note, 14, color=GREY, line=1.35)
    return s


def test_slide(title, kicker, rows, note=None):
    """Green 'test it' table."""
    s, y = slide_base(title, kicker)
    hdr = rect(s, Inches(0.7), y, Inches(11.9), Inches(0.5),
               RGBColor(0xE7, 0xF8, 0xF1))
    for lbl, x, w in [("TEST CASE", Inches(1.0), Inches(3.4)),
                      ("INPUT", Inches(4.5), Inches(4.0)),
                      ("EXPECTED", Inches(8.7), Inches(3.6))]:
        box(s, x, y + Inches(0.12), w, Inches(0.3), lbl, 11.5,
            bold=True, color=TEAL)
    for i, (case, inp, exp) in enumerate(rows):
        yy = y + Inches(0.58) + Inches(0.52) * i
        if i % 2 == 0:
            rect(s, Inches(0.7), yy, Inches(11.9), Inches(0.46), LIGHT)
        box(s, Inches(1.0), yy + Inches(0.09), Inches(3.4), Inches(0.3),
            case, 13.5, bold=True)
        box(s, Inches(4.5), yy + Inches(0.09), Inches(4.0), Inches(0.3),
            inp, 13, color=GREY)
        box(s, Inches(8.7), yy + Inches(0.09), Inches(3.6), Inches(0.3),
            exp, 13.5, bold=True, color=TEAL)
    if note:
        box(s, Inches(0.7), y + Inches(0.62) + Inches(0.52) * len(rows),
            Inches(11.9), Inches(0.8), note, 13.5, color=GREY, line=1.35)
    return s


def code_slide(title, kicker, label, code, note=None):
    s, y = slide_base(title, kicker)
    box(s, Inches(0.7), y, Inches(11.9), Inches(0.32), label, 14,
        bold=True, color=BLUE)
    yy = y + Inches(0.42)
    lines = code.strip().split("\n")
    ch = Inches(0.3) * len(lines) + Inches(0.5)
    rect(s, Inches(0.7), yy, Inches(11.9), ch,
         RGBColor(0xF2, 0xF5, 0xF9), line=RGBColor(0xD5, 0xDD, 0xE8))
    tb = s.shapes.add_textbox(Inches(0.95), yy + Inches(0.22),
                              Inches(11.4), ch - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = ln
        r.font.name = "Consolas"
        r.font.size = Pt(12.5)
        r.font.color.rgb = INK
    if note:
        box(s, Inches(0.7), yy + ch + Inches(0.2), Inches(11.9),
            Inches(0.8), note, 13.5, color=GREY, line=1.35)
    return s


def feature_grid(title, kicker, items, note=None):
    """2x3 grid of agent capability cards."""
    s, y = slide_base(title, kicker)
    cw, chh = Inches(5.8), Inches(1.22)
    gap = Inches(0.18)
    for i, (name, what, accent) in enumerate(items):
        col, row = i % 2, i // 2
        x = Inches(0.7) + (cw + Inches(0.3)) * col
        yy = y + (chh + gap) * row
        rect(s, x, yy, cw, chh, LIGHT)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, yy, Pt(5), chh)
        bar.fill.solid(); bar.fill.fore_color.rgb = accent
        bar.line.fill.background(); bar.shadow.inherit = False
        box(s, x + Inches(0.3), yy + Inches(0.16), cw - Inches(0.55),
            Inches(0.33), name, 15.5, bold=True, color=accent)
        box(s, x + Inches(0.3), yy + Inches(0.52), cw - Inches(0.55),
            chh - Inches(0.65), what, 12.5, color=GREY, line=1.28)
    if note:
        box(s, Inches(0.7), y + (chh + gap) * 3 + Inches(0.02),
            Inches(11.9), Inches(0.55), note, 12.5, color=GREY, line=1.25)
    return s


def compare_slide(title, kicker, rows, left_h, right_h, note=None):
    """Side-by-side comparison table with a dimension column."""
    s, y = slide_base(title, kicker)
    dim_w, col_w = Inches(3.5), Inches(4.15)
    hdr = rect(s, Inches(0.7), y, Inches(11.9), Inches(0.52), LIGHT)
    box(s, Inches(0.95), y + Inches(0.13), dim_w, Inches(0.3),
        "", 12)
    box(s, Inches(0.7) + dim_w, y + Inches(0.13), col_w, Inches(0.3),
        left_h, 14, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    box(s, Inches(0.7) + dim_w + col_w, y + Inches(0.13), col_w,
        Inches(0.3), right_h, 14, bold=True, color=VIOLET,
        align=PP_ALIGN.CENTER)
    rh = Inches(0.56)
    for i, (dim, a, b) in enumerate(rows):
        yy = y + Inches(0.62) + rh * i
        if i % 2 == 0:
            rect(s, Inches(0.7), yy, Inches(11.9), Inches(0.5), LIGHT)
        box(s, Inches(0.95), yy + Inches(0.11), dim_w - Inches(0.3),
            Inches(0.3), dim, 13, bold=True)
        box(s, Inches(0.7) + dim_w, yy + Inches(0.11), col_w,
            Inches(0.3), a, 12.5, color=GREY, align=PP_ALIGN.CENTER)
        box(s, Inches(0.7) + dim_w + col_w, yy + Inches(0.11), col_w,
            Inches(0.3), b, 12.5, color=GREY, align=PP_ALIGN.CENTER)
    if note:
        box(s, Inches(0.7), y + Inches(0.68) + rh * len(rows),
            Inches(11.9), Inches(0.8), note, 13.5, color=GREY, line=1.35)
    return s


def warn_slide(title, kicker, items):
    """Gotchas — amber cards. Card height adapts to the number of items."""
    s, y = slide_base(title, kicker)
    n = len(items)
    avail = H - y - Inches(0.65)
    gap = Inches(0.13)
    ch = min(Inches(0.92), (avail - gap * (n - 1)) / n)
    hs = 15.5 if n <= 4 else 14
    bs = 13 if n <= 4 else 11.5
    for i, (head, body) in enumerate(items):
        yy = y + (ch + gap) * i
        rect(s, Inches(0.7), yy, Inches(11.9), ch,
             RGBColor(0xFD, 0xF6, 0xE7))
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), yy,
                                 Pt(5), ch)
        bar.fill.solid(); bar.fill.fore_color.rgb = AMBER
        bar.line.fill.background(); bar.shadow.inherit = False
        box(s, Inches(1.05), yy + Inches(0.10), Inches(11.2),
            Inches(0.32), head, hs, bold=True, color=AMBER)
        box(s, Inches(1.05), yy + ch - Inches(0.42), Inches(11.2),
            Inches(0.32), body, bs, color=GREY)
    return s


# ================================================================ DECK
cover()

# ---- the problem
section("01", "The Problem", "Why Marina Trust Bank needs this")

cards3("Marina Trust Bank today", "Scenario", [
    ("Paper and re-keying",
     "Applications arrive on paper. Staff type them into a spreadsheet by "
     "hand. Every keystroke is a chance to introduce an error."),
    ("Days, not minutes",
     "Applications sit in a queue for 3–5 working days before anyone makes "
     "a decision. Applicants hear nothing in the meantime."),
    ("Rules in a binder",
     "Eligibility rules are printed and kept at the branch. Different "
     "officers read them differently, so outcomes vary."),
], note="Marina Trust Bank is fictitious. All data in this lab is mock data.")

content("What goes wrong", "The cost", [
    ("Duplicate customers",
     "No one checks the register first, so the same person is onboarded twice "
     "under slightly different spellings"),
    ("Inconsistent decisions",
     "Two officers, same application, different outcome — because the rules "
     "are applied from memory"),
    ("Missed confirmations",
     "Emails are typed one at a time, and some are simply forgotten"),
    ("No audit trail",
     "When the regulator asks why an application was rejected, nobody can say"),
])

big_statement(
    "Every decision should take twenty seconds,\nfollow the same rules, and "
    "leave a record.",
    "That is what you are going to build.")

# ---- what you build
section("02", "What You Build", "The moving parts")

flow_diagram("The whole system", "Architecture", [
    ("HTTP Trigger", "Application arrives\nfrom the website", VIOLET),
    ("SharePoint", "Is this NRIC\nalready known?", TEAL),
    ("AI Agent", "Applies the\nsix rules", VIOLET),
    ("Response", "Decision back\nto the page", BLUE),
    ("Send email", "Confirmation to\nthe applicant", TEAL),
], note="Response comes BEFORE the email on purpose: the applicant sees the "
        "decision even if mail delivery later fails. Never couple the user's "
        "answer to a side effect.")

cards3("Four concepts", "Building blocks", [
    ("HTTP Request Trigger",
     "A public URL that starts the flow. Any website can POST an application "
     "to it. Same idea as a webhook — the flow sits waiting until data "
     "arrives."),
    ("Agent Node",
     "The decision maker. You give it the bank's rules in plain English and a "
     "JSON schema for its answer. It reasons over the application and returns "
     "a structured decision."),
    ("SharePoint Lists",
     "The bank's records. Customers is the register to check against; "
     "OnboardingLog is the audit trail. Reads and writes, live."),
])

cards3("...and the fourth", "Building blocks", [
    ("Response Action",
     "Sends the decision back to whoever called the flow. Without it, the "
     "website gets an empty reply and can display nothing."),
    ("Why it matters",
     "The trigger and the response are a matched pair. One opens the "
     "conversation with the website, the other closes it."),
    ("Order matters",
     "The SharePoint lookup runs BEFORE the agent, so the agent already "
     "knows whether this person is an existing customer."),
])

# ---- inside the agent node
section("03", "Inside the Agent", "What the Agent node can do")

feature_grid("Six capabilities", "Agent node", [
    ("Instructions",
     "The system prompt. The rules, the definitions, the output contract. "
     "Everything the agent knows about its job lives here.", BLUE),
    ("Microsoft IQ",
     "Grounds the agent in your organisation's work context — people, "
     "meetings, documents, app signals from Microsoft 365.", VIOLET),
    ("Tools",
     "Systems the agent can call itself: SharePoint, Outlook, Teams, "
     "OneDrive, Excel Online, Dataverse, MCP servers, any connector.", TEAL),
    ("Knowledge",
     "Trusted reference material the agent reads from when answering, "
     "instead of relying on what the model already knows.", VIOLET),
    ("Request human assistance",
     "When the agent is unsure, it emails the connection owner and waits "
     "for a person to weigh in before continuing.", AMBER),
    ("Web search",
     "Lets the agent look things up on the public web. Off by default, "
     "and best left off for regulated decisions.", TEAL),
], note="Activity 1 uses Instructions and Structured output only. Everything "
        "else is off — deliberately, because a bank decision should depend on "
        "the bank's own data and nothing else.")

img_slide("Where you find them", "Agent panel", "13-node-agent-schema.png",
          crop=(0.30, 0.12, 0.01, 0.08),
          notes=[
              "All six sit together at",
              "the bottom of the",
              "Agent panel:",
              "",
              "Microsoft IQ",
              "Tools",
              "Knowledge",
              "Request human assistance",
              "Web search",
              "Output",
              "",
              "Activity 1 leaves both",
              "toggles off.",
          ])

cards3("Structured output", "The seventh capability", [
    ("Text response",
     "The agent replies in prose. Fine for a chat assistant, useless when a "
     "website has to read the answer and render it."),
    ("Structured output",
     "A predefined shape. The agent must fill in the fields you specified, "
     "so downstream steps can rely on them."),
    ("Custom structured output",
     "You supply the JSON Schema. This is what Activity 1 uses — with an "
     "enum on 'decision' so only four values are possible."),
], note="A schema turns the model from something that writes an answer into "
        "something that returns data your flow can act on.")

# ---- the logic
section("04", "The Decision Logic", "Six rules, in order")

rules_ladder("The rules stop at the first match", "How the agent decides", [
    ("STEP 1", "NRIC already in the Customers register", "DUPLICATE", VIOLET),
    ("STEP 2", "Applicant is under 18 years old", "REJECTED", RED),
    ("STEP 3", "PEP, foreign tax resident, or high-risk funds", "REVIEW", AMBER),
    ("STEP 4", "Employment or income fails the product rule", "REJECTED", RED),
    ("STEP 5", "Initial deposit below the product minimum", "REJECTED", RED),
    ("STEP 6", "Nothing fired", "APPROVED", TEAL),
], note="Order is the point. An applicant who is under 18 AND a PEP is "
        "REJECTED, not REVIEW — Step 2 fires first and stops the ladder.")

two_col("The product matrix", "Rules 4 and 5",
        "Employment requirement", [
            "Savings — none",
            "Joint Savings — none",
            "Student Account — must be Student",
            "Current — gainfully employed",
            "Fixed Deposit — income ≥ SGD 30,000",
            "Multi-Currency — ≥ SGD 60,000 + employed",
        ],
        "Minimum initial deposit", [
            "Savings — SGD 500",
            "Joint Savings — SGD 1,000",
            "Student Account — SGD 0",
            "Current — SGD 3,000",
            "Fixed Deposit — SGD 10,000",
            "Multi-Currency — SGD 5,000",
        ],
        note="The agent judges the applicant only against the account type "
             "they actually asked for.")

code_slide("What the agent returns", "Structured output",
           "Every decision comes back in this exact shape",
           """{
  "applicationId": "APP-20260801085935",
  "decision": "APPROVED",
  "reason": "The application has been reviewed and all eligibility
             criteria for a Savings account have been met.",
  "riskFlags": []
}""",
           note="A JSON schema with an enum on 'decision' stops the model "
                "inventing values the website cannot render.")

# ---- build it
section("05", "Build It", "Five nodes, in order")

# Crop the empty lower half of the Copilot Studio canvas so the nodes read large.
img_slide("The finished flow", "Copilot Studio", "07-flow-canvas.png",
          crop=(0.05, 0.10, 0.02, 0.30),
          caption="Trigger → SharePoint lookup → Agent → Response → Email")

img_slide("Node 1 — HTTP request trigger", "Configuration",
          "08-node-trigger.png", crop=(0.30, 0.12, 0.01, 0.10),
          notes=[
              "METHOD",
              "POST",
              "",
              "WHO CAN TRIGGER",
              "Anyone (no authentication)",
              "",
              "RELATIVE PATH",
              "Leave blank — a value here",
              "breaks Publish",
              "",
              "The POST URL appears",
              "only after you save.",
          ])

img_slide("Node 2 — SharePoint lookup", "Configuration",
          "11-node-sharepoint-filter.png", crop=(0.30, 0.12, 0.01, 0.10),
          notes=[
              "SITE",
              "Marina Trust Bank",
              "Onboarding",
              "",
              "LIST",
              "Customers",
              "",
              "FILTER QUERY",
              "NRIC eq '<toUpper>'",
              "",
              "toUpper matters:",
              "lowercase input must",
              "still match the register.",
          ])

img_slide("Node 3 — the Agent", "Configuration", "12-node-agent.png",
          crop=(0.30, 0.12, 0.01, 0.10),
          notes=[
              "INSTRUCTIONS",
              "The six rules, plus the",
              "application data at the",
              "bottom",
              "",
              "OUTPUT",
              "Custom structured output",
              "",
              "There is no separate",
              "input field — the",
              "application goes in the",
              "Instructions.",
          ])

img_slide("Node 4 — the Response", "Configuration", "15-node-response.png",
          crop=(0.30, 0.12, 0.01, 0.10),
          notes=[
              "STATUS CODE",
              "200",
              "",
              "HEADERS",
              "Content-Type:",
              "application/json",
              "",
              "BODY",
              "The agent's",
              "structuredOutput",
              "",
              "This is what the",
              "website renders.",
          ])

warn_slide("Six things that will catch you", "Gotchas", [
    ("Publish, do not just save",
     "The HTTP endpoint always serves the published version. Check the "
     "Version history panel if an edit seems to do nothing."),
    ("Relative path must be empty",
     "Typing a path there makes Publish fail with an 'inputs.relativePath is "
     "not valid' error."),
    ("The trigger validates types strictly",
     "Numbers must arrive as numbers, booleans as booleans. HTML forms send "
     "strings — the website has to cast them first."),
    ("Rich-text fields eat expressions",
     "The email Body and the agent Instructions need the token picker or code "
     "mode. Pasted @{...} stays as dead text."),
    ("The email To field needs the picker",
     "A typed expression arrives with a trailing newline and Outlook rejects "
     "the address. Insert the Email token with the picker instead."),
    ("HTTP 200 does not mean it worked",
     "Once Response runs first, later actions fail invisibly. Judge success "
     "from the Activity tab, not the status code."),
])

# ---- the data
section("06", "The Data", "SharePoint as the bank's records")

two_col("Two lists", "SharePoint",
        "Customers", [
            "The register to check against",
            "",
            "NRIC · Full Name · Date of Birth",
            "Email · Account Type",
            "Annual Income · Onboarded On",
            "",
            "Seeded with 5 customers",
        ],
        "OnboardingLog", [
            "The audit trail",
            "",
            "Timestamp · Application ID",
            "NRIC · Account Type",
            "Decision · Reason",
            "",
            "One row per decision",
        ],
        note="Title is mandatory on every SharePoint item and cannot be "
             "removed. The flow sets it to the NRIC.")

img_slide("The Customers register", "SharePoint",
          "05-sharepoint-customers.png",
          caption="This is what the duplicate check queries on every "
                  "application")

# ---- run it
section("07", "Run It", "The applicant's experience")

img_slide("The application form", "Website", "01-website-form.png",
          caption="Paste your HTTP POST URL into Lab configuration, then "
                  "submit an application")

img_slide("An approved application", "Result",
          "03-result-approved.png",
          notes=[
              "WHAT HAPPENED",
              "",
              "1. Form posted the",
              "    application",
              "",
              "2. SharePoint found no",
              "    matching NRIC",
              "",
              "3. Agent applied the",
              "    rules, nothing fired",
              "",
              "4. Decision returned",
              "    and rendered here",
          ])

img_slide("An existing customer", "Result", "04-result-duplicate.png",
          notes=[
              "WHAT HAPPENED",
              "",
              "1. Form posted the",
              "    application",
              "",
              "2. SharePoint FOUND",
              "    the NRIC in Customers",
              "",
              "3. Step 1 fired and",
              "    stopped the ladder",
              "",
              "4. No account opened",
          ])

test_slide("Test every rule", "Verification", [
    ("TC1 Happy path", "New NRIC, Savings, SGD 1,000", "APPROVED"),
    ("TC2 Existing customer", "S8412345D", "DUPLICATE"),
    ("TC5 Messy casing", "s8412345d lowercase", "DUPLICATE"),
    ("TC6 Politically exposed", "PEP = Yes", "REVIEW + PEP"),
    ("TC7 Under 18", "Date of birth 2010", "REJECTED + MINOR"),
    ("TC8 Deposit too low", "Savings, SGD 200", "REJECTED"),
], note="TC5 is the one to demonstrate: same NRIC as TC2 but lowercase. "
        "Without normalisation it would be approved and create a duplicate.")

big_statement(
    "Expect about twenty seconds\nper application.",
    "The SharePoint lookup and the model call are both network round-trips. "
    "It has not hung.", accent=AMBER)

# ---- step vs tool
section("08", "Step or Tool?", "Two ways to give an agent data")

big_statement(
    "\"Why didn't we add SharePoint\nas a Tool in the agent?\"",
    "A fair question — and the answer is the most important idea in this "
    "learning unit.", accent=VIOLET)

flow_diagram("Activity 1 — SharePoint as a step", "Approach A", [
    ("Trigger", "Application arrives", BLUE),
    ("SharePoint", "Lookup ALWAYS runs", TEAL),
    ("Agent", "Reads the result", VIOLET),
    ("Response", "Decision out", BLUE),
], note="You decided the order at design time. The lookup cannot be skipped, "
        "because it is not the agent's choice to make.")

flow_diagram("Activity 1b — SharePoint as a tool", "Approach B", [
    ("Trigger", "Application arrives", BLUE),
    ("Agent", "Decides to look up,\ncalls SharePoint,\nreads, continues", VIOLET),
    ("Response", "Decision out", BLUE),
], note="The agent decides at run time whether and when to check. The lookup "
        "is inside its reasoning, not on the canvas.")

compare_slide("The tradeoff in full", "Deep analysis", [
    ("Who decides", "You, at design time", "Agent, at run time"),
    ("Lookup guaranteed", "Yes — structural", "No — instructed"),
    ("Model calls per run", "1", "2 or more"),
    ("Cost", "Lower", "Higher"),
    ("Visible on canvas", "Yes", "No — inside the agent"),
    ("Auditability", "Read the run history", "Read the reasoning"),
    ("Handles the unexpected", "Only what you built", "Can adapt"),
], "SharePoint as a STEP", "SharePoint as a TOOL",
   note="Neither column is the right answer. The question is always: does "
        "this task need guarantees, or does it need judgement?")

content("Why Activity 1 uses a step", "The reasoning", [
    ("Rule 1 says \"always first\"",
     "As a step that is structurally guaranteed. As a tool you are trusting "
     "the model to always call it"),
    ("The failure is expensive",
     "An agent that skips the duplicate check opens a second account for an "
     "existing customer — the exact thing this automation exists to prevent"),
    ("A regulator will ask",
     "\"Show me that you checked.\" A step appears in every run history. A "
     "tool call is buried in the agent's reasoning"),
    ("Credits are finite",
     "Tool use means reason, call, reason again. In a Developer environment "
     "with a class running tests, that adds up"),
], note="This is not a limitation of Copilot Studio. It is a design decision, "
        "and it is the kind you will make on every real project.")

two_col("When to use which", "Judgement",
        "Use a STEP when", [
            "The check is mandatory",
            "Order is a compliance requirement",
            "Every run must behave the same",
            "You need it provable, not likely",
            "Volume makes cost per run matter",
        ],
        "Use a TOOL when", [
            "The path is not known in advance",
            "Some lookups are only sometimes needed",
            "The agent may need to call it repeatedly",
            "Flexibility beats predictability",
            "The task genuinely needs judgement",
        ],
        note="Most production systems use both — steps for what must happen, "
             "tools for what requires judgement.")

big_statement(
    "Build it both ways.\nRun them side by side.",
    "Activity 1b is the same decision with SharePoint as a tool. The "
    "decisions match; everything else differs.", accent=TEAL)

# ---- close
section("09", "Going Further", "Where this goes next")

content("Extend the lab", "Next steps", [
    ("Write the customer record",
     "Add Create item on the APPROVED branch, so an approved applicant joins "
     "the register — resubmit and it returns DUPLICATE"),
    ("Write the audit log",
     "Add Create item to OnboardingLog for every decision, whatever the "
     "outcome"),
    ("Human review for REVIEW cases",
     "Route PEP and high-risk applications to an approval step instead of "
     "straight to the applicant"),
    ("Compare with the n8n build",
     "Same scenario, same rules, different platform — see what each makes "
     "easy and what each makes hard"),
], note="Full step-by-step instructions, every expression and every prompt: "
        "see LAB-GUIDE.md in the lab folder.")

big_statement("Questions?",
              "LAB-GUIDE.md has the complete build, expression by expression.",
              accent=TEAL)

prs.save(OUT)
print(f"Saved: {OUT}")
print(f"Slides: {len(prs.slides.__iter__.__self__._sldIdLst)}")
