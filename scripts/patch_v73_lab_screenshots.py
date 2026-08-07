#!/usr/bin/env python3
"""patch_v73_lab_screenshots.py

Merge the real Power Automate / Copilot Studio screenshots (pasted by the
trainer as temporary slides 2-13 of the v7.3 deck) onto the corresponding
lab slides, then remove the temporary slides so the deck returns to 80
slides and slide_map.json stays valid.

Source slides (92-slide deck)          -> target lab slide (92-slide index)
  2  LAB1   flow strip                 -> 36  Lab 1
  3  LAB2   flow strip                 -> 37  Lab 2
  4  LAB3   flow strip                 -> 42  Lab 3
  5  Lab 4a agent build screen         -> 59  Lab 4
  6  Lab 4b agent build screen         -> 60  Lab 4b (replaces the three
                                              takeaway cards, whose text
                                              remains in the Learner Guide)
  7  top:   Lab 5 agent flow strip     -> 61  Lab 5
     bottom: Lab 5b flow strip         -> 62  Lab 5b
  8  Lab 5b Blog Writer agent screen   -> 62  Lab 5b
  9-13 Lab6..Lab10 flow strips         -> 71, 72, 73, 79, 80

Run from the courseware repo root.
"""
import copy
from pptx import Presentation
from pptx.util import Inches, Emu, Pt
from pptx.dml.color import RGBColor
import io

DECK = "courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v7.3.pptx"

BORDER = RGBColor(0xCB, 0xD5, 0xE1)  # slate-200, matches muted house greys
SLIDE_W = 13.333
BAND_T, BAND_B = 2.05, 5.88          # free zone between subtitle and LAB card
GAP = 0.35
D_MAX_W, D_MAX_H = 10.2, 1.85        # cap for the existing concept diagram
S_MAX_W = 10.8                       # cap for the screenshot

prs = Presentation(DECK)
slides = list(prs.slides)


def pics_of(idx):
    """Picture shapes of 1-based slide idx, sorted top-to-bottom."""
    return sorted(
        [sh for sh in slides[idx - 1].shapes if sh.shape_type == 13],
        key=lambda sh: sh.top,
    )


def grab(idx, which=0):
    pic = pics_of(idx)[which]
    im = pic.image
    return io.BytesIO(im.blob), im.size  # (stream, (px_w, px_h))


def style(pic):
    pic.line.color.rgb = BORDER
    pic.line.width = Pt(1)


def add_shot(slide, stream, aspect, w, top):
    h = w / aspect
    left = Inches((SLIDE_W - w) / 2)
    pic = slide.shapes.add_picture(stream, left, Inches(top), width=Inches(w))
    style(pic)
    return h


def stack(target_idx, src_idx, which=0):
    """Concept diagram on top, screenshot below, block vertically centred."""
    slide = slides[target_idx - 1]
    diagram = pics_of(target_idx)[0]
    stream, (pw, ph) = grab(src_idx, which)
    aspect = pw / ph

    d_w, d_h = Emu(diagram.width).inches, Emu(diagram.height).inches
    scale = min(D_MAX_W / d_w, D_MAX_H / d_h, 1.0)
    d_w, d_h = d_w * scale, d_h * scale

    s_h = (BAND_B - BAND_T) - d_h - GAP
    s_w = s_h * aspect
    if s_w > S_MAX_W:
        s_w = S_MAX_W
        s_h = s_w / aspect

    total = d_h + GAP + s_h
    top = BAND_T + ((BAND_B - BAND_T) - total) / 2

    diagram.width, diagram.height = Inches(d_w), Inches(d_h)
    diagram.left, diagram.top = Inches((SLIDE_W - d_w) / 2), Inches(top)
    add_shot(slide, stream, aspect, s_w, top + d_h + GAP)
    print(f"slide {target_idx}: diagram {d_w:.2f}x{d_h:.2f}, shot {s_w:.2f}x{s_h:.2f}")


# ---- straightforward stacked slides -------------------------------------
stack(36, 2)    # Lab 1
stack(37, 3)    # Lab 2
stack(42, 4)    # Lab 3
stack(61, 7, 0) # Lab 5  (top canvas of pasted slide 7)
stack(71, 9)    # Lab 6
stack(72, 10)   # Lab 7
stack(73, 11)   # Lab 8
stack(79, 12)   # Lab 9
stack(80, 13)   # Lab 10

# ---- slide 59 · Lab 4: compact diagram strip + agent build screen -------
s59 = slides[58]
diagram = pics_of(59)[0]
d_h = 1.45
d_w = Emu(diagram.width).inches * d_h / Emu(diagram.height).inches
diagram.width, diagram.height = Inches(d_w), Inches(d_h)
diagram.left, diagram.top = Inches((SLIDE_W - d_w) / 2), Inches(BAND_T)
stream, (pw, ph) = grab(5)
top = BAND_T + d_h + 0.32
add_shot(s59, stream, pw / ph, (BAND_B - top) * pw / ph, top)
print(f"slide 59: diagram {d_w:.2f}x{d_h:.2f}, shot h {BAND_B-top:.2f}")

# ---- slide 60 · Lab 4b: pipeline row up, cards -> agent build screen ----
s60 = slides[59]
doomed = []
for sh in list(s60.shapes):
    t = Emu(sh.top).inches if sh.top is not None else 0
    if sh.shape_type == 13:
        continue
    if 2.10 <= t <= 3.50:          # pipeline row: +0.06 clears subtitle descenders
        sh.top = Emu(sh.top) + Inches(0.06)
    elif 3.70 <= t <= 5.80:        # three takeaway cards (text lives in LG)
        doomed.append(sh)
for sh in doomed:
    sh._element.getparent().remove(sh._element)
stream, (pw, ph) = grab(6)
top = 3.74                          # pipeline row ends 3.52; keep clear of it
add_shot(s60, stream, pw / ph, (BAND_B - top) * pw / ph, top)
print(f"slide 60: removed {len(doomed)} card shapes, shot h {BAND_B-top:.2f}")

# ---- slide 62 · Lab 5b: diagram left, agent screen + flow strip right ---
s62 = slides[61]
diagram = pics_of(62)[0]
d_w = 6.33
d_h = d_w * Emu(diagram.height).inches / Emu(diagram.width).inches
col_w = 4.75
comp_w = d_w + 0.30 + col_w
left0 = (SLIDE_W - comp_w) / 2
diagram.width, diagram.height = Inches(d_w), Inches(d_h)
diagram.left = Inches(left0)
diagram.top = Inches(BAND_T + ((BAND_B - BAND_T) - d_h) / 2)
col_l = left0 + d_w + 0.30

stream_a, (pw, ph) = grab(8)          # Blog Writer agent build screen
a_h = col_w * ph / pw
stream_f, (pw2, ph2) = grab(7, 1)     # "When an agent calls the flow" strip
f_h = col_w * ph2 / pw2
col_total = a_h + 0.30 + f_h
col_top = BAND_T + ((BAND_B - BAND_T) - col_total) / 2
p1 = s62.shapes.add_picture(stream_a, Inches(col_l), Inches(col_top), width=Inches(col_w))
p2 = s62.shapes.add_picture(stream_f, Inches(col_l), Inches(col_top + a_h + 0.30), width=Inches(col_w))
style(p1); style(p2)
print(f"slide 62: diagram {d_w:.2f}x{d_h:.2f}, agent {col_w:.2f}x{a_h:.2f}, flow {col_w:.2f}x{f_h:.2f}")

# ---- remove the temporary screenshot slides 2-13 ------------------------
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
for sldId in ids[1:13]:
    prs.part.drop_rel(sldId.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"))
    sldIdLst.remove(sldId)

prs.save(DECK)
print(f"saved: {DECK} · {len(Presentation(DECK).slides)} slides")
