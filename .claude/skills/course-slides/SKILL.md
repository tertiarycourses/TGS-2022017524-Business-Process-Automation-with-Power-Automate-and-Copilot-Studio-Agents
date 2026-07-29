---
name: course-slides
description: Edit / update THIS course's facilitator slide deck (courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v4.pptx, white theme, Arial) for "Business Process Automation with Power Automate and Copilot Studio Agents" (TGS-2022017524). There is NO slide build script — the deck is edited in place with python-pptx. Use when a slide is out of date (e.g. a Copilot Studio UI change), must match an updated lab, or needs a text/screenshot fix. Keeps the deck aligned with the Lesson Plan's Slides column and the Learner Guide.
---

# Facilitator slides — edit in place

The deck `courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v4.pptx` has **no generator script**; edit it directly with `python-pptx`. Keep it aligned with the labs in `labs/`, the Learner Guide (`.claude/skills/wsq-learner-guide/build_learner_guide.py`), and the Lesson Plan's **Slides** column (`.claude/skills/wsq-lesson-plan/build_lesson_plan.py`).

## Golden rule — edit at the RUN level (preserve formatting)
Never set `text_frame.text` or `paragraph.text` — that collapses runs and loses font/size/colour/bold. Set the text on the existing run and assert the old text first:

```python
from pptx import Presentation
p = Presentation("courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v4.pptx")

def set_run(slide_idx, shape_idx, new_text, must_contain):   # 1-based slide index
    run = p.slides[slide_idx-1].shapes[shape_idx].text_frame.paragraphs[0].runs[0]
    assert must_contain in run.text, f"slide {slide_idx}: '{must_contain}' not found"
    run.text = new_text
    # ...
p.save("courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v4.pptx")
```

A multi-line bullet block is usually a **single run** with `\n` separators — replace that one run to update the whole block while keeping its style.

## Find the slide/shape to edit
Print structure first: iterate `enumerate(p.slides, 1)` → `shape.has_text_frame` → `paragraphs` → `runs`, printing `run.text`. Match by visible title/text, not by guessing indexes.

## Rules for this deck
- **86 slides** (2-day restructure, Jul 2026): 1 cover · 2–14 WSQ admin block (attendance, trainer ×2, intro, ground rules, outcomes, lesson plan, assessment briefing/funding/flow, labs-access) · 15–47 Day 1 (Modules 1–2 + Labs 0–5) · 48–73 Day 2 (Module 3 + Labs 6–11 + recap) · 74–82 wrap-up (automate next, pitfalls, errors, governance, rollout, recap, takeaways, resources, portal) · 83–85 end assessment block (Assessment, Assessment Flow, Attendance) · 86 Thank You.
- **Do NOT add or delete slides.** The Lesson Plan maps sessions to slide numbers (e.g. Module 3 → 50–59, Lab 9 → 69). Editing text in place keeps that mapping valid. If a slide must be added/removed, update the **Slides** column in `.claude/skills/wsq-lesson-plan/build_lesson_plan.py` and rebuild the LP + PDF in the same change.
- **Multi-line GOAL/STEPS blocks are a single run with `\n` separators** — match/replace with `old in run.text` substring replacement, not per-paragraph equality.
- **White theme only, Arial, 16:9** — inherited automatically when you edit existing runs.
- Keep slide wording consistent with the labs. Alignment done Jul 2026: Labs 1–3 slides (manual triggers with inputs), slide 52/66 (Create blank agent — "Skip to configure" is gone), 53/68 (Tools, formerly Actions), 70 (flow added as a tool in the topic), 71 (AI Builder "Run a prompt" in an agent flow), 83 (OneDrive trigger), 84 (agent calls the flow).

## Verify after editing
1. Re-read the changed slides' `run.text` to confirm.
2. (Optional) Export PDF: `soffice --headless --convert-to pdf --outdir courseware "courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v4.pptx"`.

See the user-level `tertiary-course-slides` skill for the full house style and the from-scratch generator.
