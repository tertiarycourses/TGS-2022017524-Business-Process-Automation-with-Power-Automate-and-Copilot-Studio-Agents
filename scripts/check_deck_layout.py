#!/usr/bin/env python3
"""Flag slides whose shapes run past the safe content area or off the canvas.

The deck is 13.333in x 7.5in. Content must sit above the footer band, which
starts at 6.95in, and inside a 0.4in side margin.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches

ROOT = Path(__file__).resolve().parents[1]
DECK = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "courseware" / (
    "Business Process Automation with Power Automate and Copilot Studio Agents-v8.0.pptx"
)

FOOTER_TOP = Inches(6.93)
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.35)

prs = Presentation(DECK)
problems = []

BUILT_FIRST, BUILT_LAST = 1, 10**6   # v8.0 builds every slide; pass a deck path as argv[1]

for idx, slide in enumerate(prs.slides, 1):
    if not (BUILT_FIRST <= idx <= BUILT_LAST):
        continue
    for shape in slide.shapes:
        if shape.top is None or shape.height is None:
            continue
        text = ""
        if shape.has_text_frame:
            text = shape.text_frame.text.strip().replace("\n", " ")[:48]
        bottom = shape.top + shape.height
        right = (shape.left or 0) + (shape.width or 0)
        # The footer textboxes themselves live in the footer band legitimately.
        is_footer = (
            text.startswith("Business Process Automation with Power Automate")
            or text.isdigit()
        )
        # The title accent bar is deliberately flush to the left edge.
        if (shape.left or 0) == 0 and (shape.height or 0) <= Inches(1.6):
            continue
        # Full-bleed decorative bars are intentional.
        full_bleed = (shape.width or 0) >= SLIDE_W - Inches(0.02)
        if full_bleed:
            continue
        if not is_footer and bottom > FOOTER_TOP:
            problems.append((idx, "below footer line", round(bottom / 914400, 2), text))
        if bottom > SLIDE_H:
            problems.append((idx, "off canvas bottom", round(bottom / 914400, 2), text))
        if right > SLIDE_W - MARGIN + Inches(0.05):
            problems.append((idx, "past right margin", round(right / 914400, 2), text))
        if (shape.left or 0) < MARGIN - Inches(0.2):
            problems.append((idx, "past left margin", round((shape.left or 0) / 914400, 2), text))

if problems:
    print(f"{len(problems)} layout problem(s):\n")
    for idx, kind, value, text in problems:
        print(f"  slide {idx:3d}  {kind:20s} {value:>6}in   {text}")
    sys.exit(1)

print(f"OK — {len(prs.slides)} slides, no shape crosses the footer line or the canvas edge.")


# ---------------------------------------------------------------- overlaps
# A text box whose text sits on top of ANOTHER box's text is the defect that
# renders as unreadable. Compare text-bearing shapes only, and ignore a text
# box sitting inside its own container (a card label inside its card).
def _text_shapes(slide):
    out = []
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        if not sh.text_frame.text.strip():
            continue
        if sh.top is None or sh.height is None:
            continue
        txt = sh.text_frame.text.strip()
        # the footer pair deliberately shares one band (left caption, right page no.)
        if txt.startswith("Business Process Automation with Power Automate") or txt.isdigit():
            continue
        # right-aligned chips/labels drawn inside a card are contained, not colliding
        out.append(sh)
    return out


def _rect(sh):
    return (sh.left or 0, sh.top, (sh.left or 0) + (sh.width or 0), sh.top + sh.height)


collisions = []
for idx, slide in enumerate(prs.slides, 1):
    if not (BUILT_FIRST <= idx <= BUILT_LAST):
        continue
    shapes = _text_shapes(slide)
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            a, b = _rect(shapes[i]), _rect(shapes[j])
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox <= 0 or oy <= 0:
                continue
            # ignore overlaps of only a hairline, and centred-label cases
            if ox < Inches(0.35) or oy < Inches(0.18):
                continue
            contained = (
                (a[0] >= b[0] - 1 and a[2] <= b[2] + 1 and a[1] >= b[1] - 1 and a[3] <= b[3] + 1)
                or (b[0] >= a[0] - 1 and b[2] <= a[2] + 1 and b[1] >= a[1] - 1 and b[3] <= a[3] + 1)
            )
            if contained:
                continue
            ta = shapes[i].text_frame.text.strip().replace("\n", " ")[:32]
            tb = shapes[j].text_frame.text.strip().replace("\n", " ")[:32]
            collisions.append((idx, ta, tb, round(ox / 914400, 2), round(oy / 914400, 2)))

if collisions:
    print(f"\n{len(collisions)} text overlap(s):\n")
    for idx, ta, tb, ox, oy in collisions:
        print(f"  slide {idx:3d}  {ox}x{oy}in   '{ta}'  vs  '{tb}'")
    sys.exit(1)
print("OK — no overlapping text boxes.")
