---
name: wsq-assessment
description: Generate or revise the WSQ assessments for THIS course (Business Process Automation with Power Automate and Copilot Studio Agents, TGS-2022017524). Produces a Written Assessment (WA / SAQ) and a Practical Performance (PP) Assessment, each as a question paper plus a model-answer / marking guide DOCX. ALL questions are OPEN-ENDED — no multiple choice. The WA is 6 open-ended short-answer questions (K1-K6) testing knowledge from Modules 1-3 and the slides; the PP is one ACME Pte Ltd scenario with 3 tasks (A1-A7) whose model answers mirror the hands-on lab build steps (Labs 1-10). Use when editing the assessment questions, answers, scenario, or marking guides for this course.
---

# WSQ Assessment — this course

Single-source generator: `.claude/skills/wsq-assessment/build_assessment_course.py` (the generic house templates `build_assessment.py` / `build_wsq_assessment.py` also live in this folder). Outputs four DOCX into `assessemnt/`:
- `WA (SAQ) - <course>.docx` + `Answers to WA (SAQ) - <course>.docx`
- `PP Assessment - <course>.docx` + `Answer to PP Assessment - <course>.docx`

## Hard rules (do not break)
- **NO multiple choice — every question is OPEN-ENDED.** The WA uses open-ended short-answer questions with boxed answer areas; the PP uses build tasks with screenshot-evidence boxes.
- **Question counts are fixed: WA = 6 questions (K1–K6), PP = 3 tasks (A1–A7).** Revisions keep these counts.
- **WA = KNOWLEDGE** drawn from the concept modules and slides. Sources: `labs/Module 1`, `Module 2`, `Module 3`, and `courseware/Business Process Automation with Power Automate and Copilot Studio Agents-v4.pptx` (86 slides). Each answer-key item cites its module/slides.
- **PP = PRACTICAL.** One coherent **ACME Pte Ltd** scenario; the **model answers are the lab build steps** (cite the labs in `labs/`). Tasks: 1 = Power Automate flow (Excel log + approval + condition), 2 = Copilot Studio agent (topic + Ask a question + variables), 3 = agent + flow integration ("When an agent calls the flow" / "Respond to the agent").
- Both instruments carry the WSQ house **cover page** (org + UEN + title + TGS Ref No + Conducted by) — cover page only, no version-control record.
- Timings match the Lesson Plan: Day 2, 4:00–6:00pm — WA 1 hr, PP 1 hr, open book.
- Keep questions and answers strictly to content taught in the modules, slides, and labs.

## How to edit
1. Edit the content lists in `.claude/skills/wsq-assessment/build_assessment_course.py`:
   - `WRITTEN` — 6 tuples `(tag, question, [model points], source)`.
   - `SCENARIO`, `PP_TASKS`, `PP_ANSWERS` — the ACME scenario, the 3 tasks and their lab-step model answers.
2. Run: `python3 .claude/skills/wsq-assessment/build_assessment_course.py`
3. Verify: zero MCQ, WA has exactly 6 questions / PP exactly 3 tasks, every PP answer cites a lab, the four files regenerate in `assessemnt/`.

## Notes
- `assessemnt/` is confidential — **never pushed to GitHub** (the `github-push` skill excludes it).
- Old-course instruments are parked in `assessemnt/archive/`.
- See the user-level `wsq-assessment` skill for the reusable, course-agnostic template.

## Versioning rule (MANDATORY — every update)

Every content update to a courseware artifact MUST, in the same change:

1. **Bump the version number** (and the version date) in the generator/template — e.g. `VERSION="vNN"` for slide decks (the version is also part of the output filename), `VERSION = "N.N"` plus a new `VERSIONS` entry for DOCX documents.
2. **Document the change in the Document Version Control Record** — add a row (Version Number | Effective Date of Release | Summary of Included Changes | Author) wherever the document carries one (Learner Guide / Lesson Plan). For slide decks the bumped version must appear on the cover page and in the filename.
3. **Regenerate the outputs**, remove (`git rm`) the superseded versioned files, and update any references to the versioned filename (README, slides that cite the document, etc.).

Never regenerate an artifact with content changes while keeping the old version number.
