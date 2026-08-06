#!/usr/bin/env python3
"""v7.2 — Lab 5 renamed: Invoke Agents -> Calling Agent from Workflow.

Text-only patch of the v7.1 deck (no slides added or removed, so the
partname-collision allocator in patch_v70_new_copilot_studio.py is not needed):
  slide 1  cover version
  slide 8  lab journey tile
  slide 10 Day 2 schedule row
  slide 44 Module 3 concept -> Lab 5 pointer card
  slide 46 Lab 5 workflow slide (title, description, card, flowchart image)
"""
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CW = ROOT / "courseware"
TITLE = "Business Process Automation with Power Automate and Copilot Studio Agents"
SRC = CW / f"{TITLE}-v7.1.pptx"
DST = CW / f"{TITLE}-v7.2.pptx"
FLOW = ROOT / "labs/Lab 5 - Calling Agent from Workflow/assets/flowchart.png"

REPL = {
    1: [("Version 7.1", "Version 7.2")],
    8: [("Invoke Agents", "Calling Agent from Workflow"),
        ("SharePoint grounding, published to Teams",
         "Topic in, M365 Copilot blog, posted to Teams")],
    10: [("Lab 5 — grounding and publishing to Teams",
          "Lab 5 — calling an agent from a workflow")],
    # Knowledge/grounding concept: its lab is now Lab 9, not the renamed Lab 5
    41: [("LAB 5", "LAB 9"),
         ("Lab 5 — Invoke Agents", "Lab 9 — RAG with Knowledge Base"),
         ("HR Support Agent grounded in SharePoint  ·  Copilot Studio + SharePoint + Teams  ·  30 min",
          "Cook & Bake Academy, built-in knowledge  ·  Copilot Studio Knowledge + SharePoint  ·  40 min")],
    44: [("Lab 5 — Invoke Agents", "Lab 5 — Calling Agent from Workflow"),
         ("HR Support Agent grounded in SharePoint  ·  Copilot Studio + SharePoint + Teams  ·  30 min",
          "Blog-writer agent flow  ·  Copilot Studio + M365 Copilot + Teams  ·  30 min")],
    46: [("Lab 5 — Grounding and Publishing an Agent",
          "Lab 5 — Calling Agent from Workflow"),
         ("Ground an agent in a permission-controlled SharePoint source, test its refusals, and publish it to Teams.",
          "Build an agent flow that collects a blog topic at the Start node, drafts the post with M365 Copilot, and posts it to the Training team's General channel."),
         ("Lab 5 — Invoke Agents", "Lab 5 — Calling Agent from Workflow"),
         ("HR Support Agent grounded in SharePoint  ·  Copilot Studio + SharePoint + Teams  ·  30 min",
          "Blog-writer agent flow  ·  Copilot Studio + M365 Copilot + Teams  ·  30 min")],
}

prs = Presentation(SRC)

def replace_in_frame(tf, old, new):
    hits = 0
    for para in tf.paragraphs:
        # try run-level first so character formatting is preserved
        for run in para.runs:
            if old in run.text:
                run.text = run.text.replace(old, new)
                hits += 1
        if hits:
            continue
        joined = "".join(r.text for r in para.runs)
        if old in joined:  # string spans runs: collapse into the first run
            first = para.runs[0]
            first.text = joined.replace(old, new)
            for r in para.runs[1:]:
                r.text = ""
            hits += 1
    return hits

for idx, pairs in REPL.items():
    slide = prs.slides[idx - 1]
    for old, new in pairs:
        n = sum(replace_in_frame(sh.text_frame, old, new)
                for sh in slide.shapes if sh.has_text_frame)
        if n == 0:
            raise SystemExit(f"slide {idx}: no match for {old[:60]!r}")
        print(f"slide {idx}: {n} x {old[:45]!r} -> ok")

# ---- swap the Lab 5 flowchart on slide 46, fitted inside the old image box ----
s46 = prs.slides[45]
pic = next(sh for sh in s46.shapes if sh.shape_type == 13)
box = (pic.left, pic.top, pic.width, pic.height)
pic._element.getparent().remove(pic._element)
w_px, h_px = Image.open(FLOW).size
aspect = w_px / h_px
bw, bh = box[2], box[3]
if bw / bh > aspect:      # box wider than image: height-bound
    h, w = bh, int(bh * aspect)
else:
    w, h = bw, int(bw / aspect)
left = box[0] + (bw - w) // 2
top = box[1] + (bh - h) // 2
s46.shapes.add_picture(str(FLOW), left, top, width=w, height=h)
print(f"slide 46: flowchart swapped ({Emu(w).inches:.2f}in x {Emu(h).inches:.2f}in)")

prs.save(DST)
print("wrote", DST.name)

archive = CW / "archive"
archive.mkdir(exist_ok=True)
for stale in (SRC, CW / f"{TITLE}-v7.1.pdf"):
    if stale.exists():
        shutil.move(str(stale), archive / stale.name)
        print("archived", stale.name)
