# CLAUDE.md — Business Process Automation with Power Automate and Copilot Studio Agents (TGS-2022017524)

WSQ courseware repo for a 2-day course: 5 concept modules, 13 hands-on labs (0–10 plus optional
4b and 5b), assessment on Day 2 4:00–6:00pm. The labs in `labs/` are the ground truth — every
other artifact is generated from or aligned to them.

## The one rule that prevents drift

**Never hand-edit the LG or LP DOCX, and never hand-edit LEARNER-GUIDE.md.** They are compiled:

| Artifact | Built by | Source |
|---|---|---|
| `LEARNER-GUIDE.md` + `courseware/LG-*.docx` | `.claude/skills/wsq-learner-guide/build_learner_guide.py` | the lab/module markdown listed in its `DAYS` structure |
| `courseware/LP-*.docx` | `.claude/skills/wsq-lesson-plan/build_lesson_plan.py` | its `DAY1`/`DAY2` tuples + both manifests |
| Deck `courseware/*-vN.N.pptx` | `scripts/build_v70_deck.py` then the `scripts/patch_v7N_*.py` chain, in order (see README "Rebuild everything") | `courseware/alignment_manifest.json` |

To change lab content: edit the file in `labs/`, re-run both builders, re-render PDFs
(`soffice --headless --convert-to pdf`). To add/remove/renumber a slide: write a new
`scripts/patch_v7N_*.py` (copy the collision-safe partname allocator from
`patch_v70_new_copilot_studio.py` — without it a new slide can silently overwrite a live one),
bump the cover version, renumber footers, then update **both**
`courseware/alignment_manifest.json` and `courseware/slide_map.json`. The LP builder asserts
against those manifests (day totals = 540 min; every non-optional lab's scheduled minutes equal
its manifest duration), so a mismatch fails the build on purpose.

Version bumps: deck version lives in the filename + cover; LG/LP versions live in each
builder's `VERSION` + `VERSIONS` record. Superseded deck versions move to
`courseware/archive/` (never deleted). QA: run the `courseware-qa` agent (renders pages to
images) after any regeneration — pushes to the TMS/Drive are gated on it.

## Publishing

- **/github-push** — repo `.gitignore` already enforces the exclusions: `assessment/` (never on
  GitHub), `*.zip` except `labs/**/skills/_packages/*.zip` (those ARE the deliverable), any
  `reference/` source material (except `.claude/skills/**/reference/`, a build dependency),
  `.env`. Always refresh `README.md` against reality before committing.
- **/gdrive-push** — `python3 .claude/skills/gdrive-push/gdrive_push.py "<folder-link>" --repo .`
  ALWAYS ask the user for the Drive folder link; `--dry-run` first. MD5-skips unchanged files,
  archives superseded ones server-side, never deletes.
- **/tms-push** — `python3 .claude/skills/lms-push/lms_push.py --repo . --drive-folder "<link>"`.
  Auth: the LMS API requires the machine service key in the `x-api-key` header; the script reads
  env **`LMS_TMS_API_KEY`** (exported in `~/.zshrc`; the key originates from
  `~/projects/tertiary/ai-lms-tms/.env.local` → `EXTERNAL_API_KEY_FOR_CLAWDBOT`). Run
  `source ~/.zshrc` first. Question papers only — the two "Answers to …" keys are trainer-only
  and must never reach the LMS or GitHub.

## Live tenant work (labs, agents, flows)

- Everything runs in the **Copilot Studio Training (Developer)** environment
  (`dd7a990d-5d41-e3a8-82ae-8ede6fe42d92`) — never the Default environment, which has no
  Copilot Credits. Always check the environment picker first.
- `.env` (gitignored, never commit or echo values) holds the classroom credentials:
  `TRAINING_ACCOUNT` / `TRAINING_TENANT` / `TRAINING_PASSWORD` — the Copilot Studio /
  Power Automate / Teams login (training1, the shared trainer account) — and the Lab 6 HR
  SharePoint pointers (`HR_SITE_URL`, `HR_KNOWLEDGE_FOLDER_URL`, `HR_GROUP_ALIAS`).
- Before asserting how any Copilot Studio field behaves, read
  `.claude/skills/copilot-studio-flows/SKILL.md` — every entry is tenant-verified, and the UI
  changes under us (e.g. Human review inputs lost the Choice type; approval cards arrive in the
  Teams **Workflows bot chat**, not the Approvals app). When the UI and the skill disagree,
  trust the UI and update the skill (both this repo's copy and `~/.claude/skills/`).
- During class hours the environment is full of learner-named copies (`Lab8_Irin`,
  `Micael - Lab 8`, …). Only ever modify the canonical trainer flows named exactly
  `Lab N - <Title>`.

## Layout

```
labs/                 ground truth: Lab 0–10, 4b, 5b + Module 1–5 readings + labs/README.md index
courseware/           deck PPTX/PDF, LG/LP DOCX+PDF, alignment_manifest.json, slide_map.json, archive/
assessment/           WA (SAQ) + PP papers and answer keys — Drive only, never GitHub/LMS-keys
scripts/              deck build + patch chain, lab asset builders, validators
labs-archive/         retired labs (e.g. the old Lab 5 - Invoke Agents)
.claude/skills/       repo-scoped builders and the copilot-studio-flows fact base
```
