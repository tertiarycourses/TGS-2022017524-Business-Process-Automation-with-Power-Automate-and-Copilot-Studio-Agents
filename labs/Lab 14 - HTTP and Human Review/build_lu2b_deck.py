#!/usr/bin/env python3
"""
LU2 Activity 2b — Client Rapport Assistant with Human Handover (Copilot Studio)
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
OUT = os.path.join(HERE, "LU2-Activity2b-Copilot-Studio.pptx")

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
        f"LU2 · Activity 2b", 10, color=GREY)
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
        "LEARNING UNIT 2 · ACTIVITY 2b", 16, bold=True, color=BLUE)
    box(s, Inches(0.9), Inches(2.4), Inches(11.5), Inches(1.5),
        "Client Rapport Assistant\nwith Human Handover", 40, bold=True, line=1.05)
    box(s, Inches(0.9), Inches(4.15), Inches(11.5), Inches(0.5),
        "The agent drafts. A licensed human approves. Nothing sends unsupervised.",
        19, color=GREY)

    for i, (lbl, val) in enumerate([
        ("PLATFORM", "Microsoft Copilot Studio"),
        ("APPROVAL", "Microsoft Teams"),
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

# ---- 01 the problem
section("01", "The Problem", "Why Meridian cannot just automate this")

cards3("Meridian Asset Management today", "Scenario", [
    ("Clients write in scared",
     "Six discretionary portfolios. When markets move, clients email — worried "
     "about performance, volatility and NAV. They are anxious about their own "
     "money."),
    ("Replies take three days",
     "The relationship managers are drowning. Some clients get a warm, careful "
     "answer. Some get a rushed one. Consistency is a matter of who was on duty."),
    ("One sentence is a breach",
     "A manager under pressure once wrote “don’t worry, it always bounces "
     "back.” That is unlicensed financial advice in every jurisdiction that "
     "has a regulator."),
], note="The team wants AI to reply faster. Compliance says no. Both are right.")

big_statement(
    "The AI is drafting a letter from a licensed firm\nto a retail investor about their money.",
    "Getting the tone wrong is embarrassing. Getting the content wrong — "
    "“hold on, it will recover” — is an offence.")

# ---- 02 human in the loop
section("02", "Human in the Loop", "What the phrase actually means")

compare_slide(
    "Three patterns, often confused", "Definitions",
    [("Who decides", "AI proposes", "AI decides"),
     ("Who acts", "Human authorises", "AI acts"),
     ("Can AI proceed alone?", "No — it blocks", "Yes"),
     ("Supervision happens", "Before the act", "After, if at all"),
     ("Failure mode", "Delay", "The client already read it")],
    "HUMAN IN THE LOOP", "ON / OUT OF THE LOOP",
    note="LU1's onboarding flow and LU2's investment advisor are both OUT of the "
         "loop. This lab is the only one genuinely IN it.")

flow_diagram("Where the loop closes", "The shape of this workflow", [
    ("Client writes", "A worried message\narrives from the\nwebsite widget", BLUE),
    ("Agent works", "Classify · read tone\nflag · DRAFT\n(never sends)", VIOLET),
    ("▶ HUMAN ◀", "The run STOPS\nuntil a person\nacts in Teams", AMBER),
    ("Consequence", "Send + log, or\nassign a named\nperson to call", TEAL),
], note="Everything before the gate is a proposal. Everything after it is a "
        "consequence. The node between them does nothing at all except wait.")

big_statement(
    "The test of a real gate:\nsubmit an enquiry, then walk away.",
    "The run says Running. It will still say Running tomorrow. Nothing times "
    "out, nothing defaults, nothing proceeds.", accent=AMBER)

# ---- 03 what you build
section("03", "What You Build", "Eleven nodes, one gate")

img_slide("The workflow on the canvas", "Copilot Studio",
          "lu2b-10-flow-canvas.png",
          notes=["Trigger — the website posts here",
                 "",
                 "Normalise_Enquiry — captures the client's",
                 "email BEFORE the model runs",
                 "",
                 "Rapport_Agent — classifies, flags, drafts",
                 "",
                 "Response — instant receipt to the browser",
                 "",
                 "Log_Draft — written before any human sees it",
                 "",
                 "Human review — THE GATE",
                 "",
                 "If/Else — approve or reject"])

content("The eleven nodes, in order", "Build order", [
    ("When a HTTP request is received", "Anyone (no auth) · relative path blank · six-field schema"),
    ("Normalise_Enquiry (Compose)", "Ticket ID, trimmed name, lowercased email — the safety control"),
    ("Rapport_Agent (Agent)", "No knowledge source · temperature 0.2 · structured output"),
    ("Response", "Five fields back to the browser. The draft is not one of them"),
    ("Log_Draft (Excel)", "Thirteen columns. The draft exists; no human has seen it"),
    ("Human review", "Assigned to a licensed person · delivered in Teams"),
    ("If/Else", "Outcome Equals Approve"),
], note="Then four branch nodes: send + log on approve, assign + email on reject.")

# ---- 04 the agent
section("04", "Inside the Agent", "What it may and may not write")

feature_grid("The non-advisory rule", "Seven prohibitions", [
    ("Never recommend", "Buying, selling, holding, switching or redeeming anything", RED),
    ("Never predict", "Future returns, prices or NAV — no forecasts, no estimates", RED),
    ("Never guarantee", "“Markets always recover” · “you will not lose money”", RED),
    ("Never judge suitability", "Not safe, not risky, not right for them", RED),
    ("Never time the market", "No comment on whether now is a good or bad moment", RED),
    ("Never invent a figure", "No fee, NAV or return that was not in the client's own message", RED),
], note="And what it MAY do: name the emotion, restate the concern, explain the "
        "process, offer a call with a licensed manager.")

big_statement(
    "When in doubt, say less and offer the call.",
    "That single sentence does more compliance work than the six prohibitions "
    "above it.", accent=TEAL)

rules_ladder("Six compliance flags", "What the agent raises", [
    ("ADVICE_REQUESTED", "asks what they should do", "ESCALATE", RED),
    ("GUARANTEE_SOUGHT", "wants a promise about returns", "ESCALATE", RED),
    ("VULNERABLE_CLIENT", "distress, illness, savings they cannot lose", "ESCALATE", RED),
    ("LEGAL_OR_MEDIA_THREAT", "mentions a lawyer, MAS, the press", "ESCALATE", RED),
    ("COMPLAINT", "dissatisfied with Meridian or its fees", "log only", AMBER),
    ("WITHDRAWAL_INTENT", "raises redeeming or closing the account", "log only", AMBER),
], note="The four that escalate are the four that cannot be answered by a drafted "
        "email at all. For those, the correct output is a draft that says so.")

code_slide("The output contract", "Structured output · eight fields",
           "Custom structured output — not a Parse JSON node", """
{
  "ticketId":         "MAM-20260802-a607f8",
  "concernCategory":  "Portfolio Performance",
  "emotionalTone":    "Concerned",
  "urgency":          "Medium",
  "complianceFlags":  ["ADVICE_REQUESTED", "WITHDRAWAL_INTENT"],
  "escalate":         true,
  "suggestedSubject": "Your enquiry about recent performance (MAM-...)",
  "draftReply":       "<p>Thank you for writing, and I am sorry ...</p>"
}
""", note="emotionalTone is a FIELD, not a paragraph. That is what lets you sort a "
          "queue and show a manager that the angriest client has waited longest. "
          "Prose cannot be sorted.")

warn_slide("Why structured output, not Parse JSON", "A rule the model cannot break", [
    ("With Text response you are asking and hoping",
     "The model eventually wraps its answer in ```json fences, or opens with “Here is the JSON” — and the parse fails."),
    ("Structured output makes malformed JSON impossible",
     "The schema is enforced at generation time. There is nothing to hope for."),
    ("Same discipline as the disclaimer",
     "A rule the model physically cannot break beats a rule it is told not to break."),
    ("Reference it with a slash, not nested brackets",
     "body('Rapport_Agent')?['structuredOutput/draftReply']"),
])

# ---- 05 the gate
section("05", "The Gate", "Node 6 — Human review")

img_slide("What the approver is shown", "Human review · Message",
          "lu2b-11-human-review.png",
          notes=["The client's own words sit directly",
                 "ABOVE the proposed reply.",
                 "",
                 "That ordering is deliberate: a reviewer",
                 "who reads only the draft cannot tell",
                 "whether it answers the right question.",
                 "",
                 "Compare with a UI that shows the draft",
                 "alone with an Approve button under it,",
                 "and ask which produces careful reading."])

two_col("The two inputs", "What the approver fills in",
        "Outcome  ·  choice", [
            "Approve  /  Reject",
            "",
            "Drives the If/Else branch.",
            "",
            "⚠  Leave the DEFAULT BLANK.",
            "Pre-filling it with ‘Approve’ turns",
            "the gate into a rubber stamp with a",
            "one-word setting nobody can see on",
            "the canvas.",
            "",
            "If a default is required, use Reject —",
            "then inattention fails safe."],
        "Name  ·  text", [
            "The approver types their own name.",
            "",
            "Lands in the Approved By column of",
            "the audit table.",
            "",
            "⚠  It is SELF-DECLARED. The node",
            "publishes no responder identity, so",
            "nothing stops someone typing ‘Bob’.",
            "",
            "A convention — where a captured",
            "identity would be evidence."])

img_slide("Approving in Microsoft Teams", "Teams · Approvals app",
          "lu2b-12-teams-approval.png",
          notes=["Teams is Microsoft 365's chat app.",
                 "It contains a built-in Approvals app,",
                 "and that is where the request lands.",
                 "",
                 "teams.microsoft.com → ••• → Approvals",
                 "or approvals.microsoft.com",
                 "",
                 "⚠  The Channel dropdown also offers",
                 "Outlook. On some tenants that route",
                 "silently fails to deliver while the run",
                 "still shows Running.",
                 "",
                 "Use TEAMS."])

# ---- 06 the website
section("06", "The Client's View", "What the browser is allowed to see")

img_slide("The Meridian client portal", "index.html",
          "lu2b-01-website-hero.png",
          caption="A floating chat widget on a single-page asset-management site. "
                  "The lab configuration panel holds the workflow URL.")

img_slide("Raising a concern", "The chat widget",
          "lu2b-05-chat-widget.png",
          notes=["Name, email, account reference and",
                 "portfolio — then the message.",
                 "",
                 "The trainer dropdown fills all of it",
                 "except the email, which it clears",
                 "on purpose.",
                 "",
                 "The approved reply is a REAL email.",
                 "Always use your own address."])

img_slide("The receipt — and what is missing from it", "Node 4 · Response",
          "lu2b-06-receipt.png",
          notes=["Reference, priority, and — because",
                 "TC2 escalates — a line saying a",
                 "manager will call.",
                 "",
                 "NOT returned: the draft itself,",
                 "emotionalTone, concernCategory,",
                 "complianceFlags.",
                 "",
                 "“We have classified you as Angry and",
                 "flagged you as a COMPLAINT” is a",
                 "disclosure no compliance officer",
                 "would sign."])

big_statement(
    "Five fields go back to the browser.\nThe draft is not one of them.",
    "The agent's assessment of a person is an internal record. The browser is "
    "not where it belongs.", accent=VIOLET)

# ---- 07 run it
section("07", "Run It", "Eight test cases")

test_slide("The test matrix", "sample-queries.csv", [
    ("TC1 · Calm volatility", "“dipped 6%, could someone explain?”", "no flags → Approve"),
    ("TC2 · Asks what to do", "“Should I move everything to cash?”", "ADVICE_REQUESTED"),
    ("TC3 · Wants a guarantee", "“promise I will not lose money”", "GUARANTEE_SOUGHT"),
    ("TC4 · Angry about fees", "“furious · unacceptable · evasive”", "COMPLAINT → Reject"),
    ("TC5 · Wants to redeem", "“redeem my entire holding”", "WITHDRAWAL_INTENT"),
    ("TC6 · Distressed retiree", "“I am 68, cannot afford to lose this”", "VULNERABLE → Reject"),
    ("TC7 · Lawyer and MAS", "“I have spoken to my lawyer”", "LEGAL → Reject"),
    ("TC8 · Factual NAV query", "“how is the NAV calculated?”", "no flags → Approve"),
], note="Afterwards: Drafts has 8 rows, Approved_Replies has 5, Handover_Queue has 3.")

two_col("Read the drafts, not just the flags", "Where the lesson lands",
        "What a good TC2 draft does", [
            "Names the emotion in the first sentence.",
            "",
            "Says plainly that the manager cannot give",
            "a recommendation by email.",
            "",
            "Offers a call with a licensed person.",
            "",
            "Contains no figure the client did not",
            "supply."],
        "What a bad TC2 draft does", [
            "“Markets typically recover over the",
            "long term.”",
            "",
            "You have just watched a language model",
            "commit a regulatory offence — in front",
            "of the whole room.",
            "",
            "And the approval gate caught it.",
            "That is what it is for."],
        note="This is the most valuable failure in the lab. Do not fix it quietly.")

warn_slide("Neither table has an empty accountability column", "The audit trail", [
    ("Approved_Replies names who authorised the email",
     "That person is answerable for what reached the client."),
    ("Handover_Queue names who owes the client a call",
     "A decline is a reassignment, not a deletion — the client is still waiting."),
    ("The regulator's question is not ‘what did the machine decide’",
     "It is ‘which licensed person is answerable for it’."),
    ("Drafts records what the machine proposed, including rejected drafts",
     "Asset or liability in litigation? Argue both sides in the debrief."),
])

# ---- 08 gotchas
section("08", "What Goes Wrong", "Field-tested")

warn_slide("The four that cost the most time", "Designer quirks", [
    ("There is no workflow() function in this designer",
     "Unknown function: workflow. Use guid() for the ticket ID instead."),
    ("The Instructions box escapes underscores",
     "A pasted reference becomes Normalise\\_Enquiry, resolves to EMPTY, and the agent says ‘no enquiry was included’. Always use the ⚡ picker."),
    ("The Agent node has no separate user-message field",
     "The enquiry is appended to the END of the Instructions."),
    ("assignedTo must be a tenant user, picked from the dropdown",
     "External addresses and tabbed-away text both fail at runtime with BadRequest."),
])

warn_slide("Two that change behaviour silently", "Configuration traps", [
    ("escalated must be UNQUOTED in the Response body",
     "Quoted, it returns the string “false” — and Boolean(“false”) is true. Every calm client is told a manager is calling."),
    ("Compliance Flags must be wrapped in join()",
     "It is an array. Without join() Excel writes System.Object[] and the audit column is useless."),
    ("Web search must be OFF",
     "On, the agent can pull live market commentary into a client letter. One toggle undoes the entire non-advisory rule."),
    ("If the approval never arrives, switch Channel to Teams",
     "The Outlook route silently fails to deliver on some tenants while the run still shows Running."),
])

# ---- 09 debrief
section("09", "Debrief", "The questions worth arguing about")

content("Ask these before anyone packs up", "Discussion", [
    ("TC6 is the hard one", "Should a distressed 68-year-old's enquiry have reached the AI at all?"),
    ("The approval button is a rubber stamp", "After forty of these, what makes careful reading the path of least resistance?"),
    ("emotionalTone is a judgement about a person, in a spreadsheet", "Under the PDPA, is that personal data? Who can see it? How long is it kept?"),
    ("Three controls, ranked", "Which is probabilistic, which procedural, and which structural?"),
    ("Approved By is self-declared", "Is that an audit trail? What would close the gap?"),
    ("Compare with LU1 and Activity 2", "Same platform, same shape, no gate. What is the actual variable?"),
], note="It is not the technology, and it is not the chance of the model being wrong.")

big_statement(
    "The variable is not how likely the model is to be wrong.\n"
    "It is what a wrong sentence costs — and to whom.",
    "Generalities to the public can go unsupervised. This client's money cannot.",
    accent=VIOLET)

# ---- close
section("10", "Going Further", "Where this goes next")

cards3("If you had another day", "Extensions", [
    ("Make rejection informative",
     "Add a required Comments input on reject. Right now Handover_Queue records "
     "that a draft was refused but never why — every Status cell says the same "
     "sentence."),
    ("Route before the model sees it",
     "A keyword pre-filter that sends distress straight to a human, with no draft "
     "at all. What does it cost, and what does it buy?"),
    ("Close the identity gap",
     "The node will not tell you who approved. What would you have to build to "
     "capture it — and is an audit trail you must remember to maintain an audit "
     "trail at all?"),
])

prs.save(OUT)
print("saved:", OUT, "·", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
