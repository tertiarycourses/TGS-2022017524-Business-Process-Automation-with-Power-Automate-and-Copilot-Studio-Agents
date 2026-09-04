---
name: wsq-assessment
description: Generate or revise the WSQ assessments for THIS course (Business Process Automation with Power Automate and Copilot Studio Agents, TGS-2022017524). Produces a Written Assessment (WA / SAQ) and a Practical Performance (PP) Assessment, each as a question paper plus a model-answer / marking guide DOCX. ALL questions are OPEN-ENDED — no multiple choice. The WA is 6 open-ended short-answer questions (K1-K6) testing knowledge from Modules 1-3 and the slides; the PP is one ACME Pte Ltd scenario with 3 tasks (A1-A7) whose model answers mirror the hands-on lab build steps (v8.0 lab set, Lab 0-17: Task 1 = Labs 1-2, Task 2 = Lab 3, Task 3 = Labs 5 and 17). Use when editing the assessment questions, answers, scenario, or marking guides for this course.
---

# WSQ Assessment — this course

Single-source generator: `.claude/skills/wsq-assessment/build_assessment_course.py` (the generic house templates `build_assessment.py` / `build_wsq_assessment.py` also live in this folder). Outputs four DOCX into `assessment/` (current: v8.0, 4 September 2026):
- `WA (SAQ) - <course>.docx` + `Answers to WA (SAQ) - <course>.docx`
- `PP Assessment - <course>.docx` + `Answer to PP Assessment - <course>.docx`

## Hard rules (do not break)
- **NO multiple choice — every question is OPEN-ENDED.** The WA uses open-ended short-answer questions with boxed answer areas; the PP uses build tasks with screenshot-evidence boxes.
- **Question counts are fixed: WA = 6 questions (K1–K6), PP = 3 tasks (A1–A7).** Revisions keep these counts.
- **WA = KNOWLEDGE** drawn from the concept modules and labs. Sources: `labs/Module 1`-`Module 5` and the v8.0 labs (Lab 0-17). Each answer-key item cites its Module and lab(s) (not slide numbers, which drift between deck versions). K1 trigger/actions in a workflow · K2 If/Else + Human review (Teams vs Outlook) · K3 Classify node and the five email categories · K4 agent anatomy and what is enforced (tools / skills / MCP) · K5 HTTP trigger, GET vs POST, the sig= URL · K6 RAG built-in vs Pinecone.
- **PP = PRACTICAL.** One coherent **ACME Pte Ltd** scenario; the **model answers are the lab build steps** (cite the labs in `labs/`; everything is built in Copilot Studio New experience — Workflows → New workflow → Start → Connector trigger …; Agents → New agent → Instructions box → Knowledge + → Publish → Channels +). Tasks: 1 = workflow `PP 1 - Course Enquiry` (Forms trigger → Get response details → Excel `Lab 2 - Enquiry Log.xlsx` → Outlook; Labs 1-2), 2 = workflow `PP 2 - Leave Approval` (Approvals in Teams → If/Else on Outcome; Lab 3), 3 = agent `PP 3 - HR Policy Agent` (Instructions, Knowledge + `HR Policies.pdf`, Preview probes, Publish, Channels + → Teams; Labs 5 and 17).
- Both instruments carry the WSQ house **cover page** (org + UEN + title + TGS Ref No + Conducted by) — cover page only, no version-control record.
- Timings match the Lesson Plan: end of Day 2 — WA 1 hr, PP 1 hr, open book.
- Keep questions and answers strictly to content taught in the modules, slides, and labs.

## How to edit
1. Edit the content lists in `.claude/skills/wsq-assessment/build_assessment_course.py`:
   - `WRITTEN` — 6 tuples `(tag, question, [model points], source)`.
   - `SCENARIO`, `PP_TASKS`, `PP_ANSWERS` — the ACME scenario, the 3 tasks and their lab-step model answers.
2. Run: `python3 .claude/skills/wsq-assessment/build_assessment_course.py`
3. Bump `VERSION` / `VERSION_DATE` in the builder (they print on the cover page and title block).
4. Verify: zero MCQ, WA has exactly 6 questions / PP exactly 3 tasks, every PP answer cites a lab, the four files regenerate in `assessment/`; then `soffice --headless --convert-to pdf --outdir assessment "<docx>"` for each, and move the superseded DOCX/PDF into `assessment/archive/`.

## Notes
- `assessment/` is confidential — **never pushed to GitHub** (the `github-push` skill excludes it).
- Old-course and superseded instruments are parked in `assessment/archive/`.
- See the user-level `wsq-assessment` skill for the reusable, course-agnostic template.

## Versioning rule (MANDATORY — every update)

Every content update to a courseware artifact MUST, in the same change:

1. **Bump the version number** (and the version date) in the generator/template — e.g. `VERSION="vNN"` for slide decks (the version is also part of the output filename), `VERSION = "N.N"` plus a new `VERSIONS` entry for DOCX documents.
2. **Document the change in the Document Version Control Record** — add a row (Version Number | Effective Date of Release | Summary of Included Changes | Author) wherever the document carries one (Learner Guide / Lesson Plan). For slide decks the bumped version must appear on the cover page and in the filename.
3. **Regenerate the outputs**, remove (`git rm`) the superseded versioned files, and update any references to the versioned filename (README, slides that cite the document, etc.).

Never regenerate an artifact with content changes while keeping the old version number.
