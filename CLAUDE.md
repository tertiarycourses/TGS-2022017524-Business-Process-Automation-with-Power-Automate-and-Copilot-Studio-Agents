# CLAUDE.md — Business Process Automation with Power Automate and Copilot Studio Agents (TGS-2022017524)

WSQ courseware repo for a 2-day course: 5 concept modules, **18 hands-on labs (Lab 0–17, none
optional)**, assessment on Day 2 4:30–6:30pm. Everything is built in the **new Copilot Studio**
(workflow designer + agent designer); Power Automate is never opened directly and nothing is
imported from a package. The labs in `labs/` (entry file `index.md` for every lab) are the ground
truth — every other artifact is generated from or aligned to them.

## The one rule that prevents drift

**Never hand-edit the LG or LP DOCX, and never hand-edit LEARNER-GUIDE.md.** They are compiled:

| Artifact | Built by | Source |
|---|---|---|
| `LEARNER-GUIDE.md` + `courseware/LG-*.docx` | `.claude/skills/wsq-learner-guide/build_learner_guide.py` | the lab/module markdown listed in its `DAYS` structure; images (`assets/flowchart.png`, `screenshots/*.png`) resolved relative to each lab folder |
| `courseware/LP-*.docx` | `.claude/skills/wsq-lesson-plan/build_lesson_plan.py` | its `DAY1`/`DAY2` tuples + `courseware/alignment_manifest.json` |
| Deck `courseware/*-v8.0.pptx` + `courseware/slide_map.json` | `scripts/build_v80_deck.py` — **self-contained, no patch chain** (the v7 `build_v70_deck.py` + `patch_v7N_*.py` chain is retired) | its `LAB_DEFAULTS` overlaid by `alignment_manifest.json`; it picks up the first four PNGs of every `labs/Lab N/screenshots/` for the "What You Will See" slides, archives the previous v8.0 copy into `courseware/archive/` and writes `slide_map.json` |

Rebuild order after any lab edit:

```bash
python3 scripts/build_v80_deck.py
python3 .claude/skills/wsq-lesson-plan/build_lesson_plan.py
python3 .claude/skills/wsq-learner-guide/build_learner_guide.py
soffice --headless --convert-to pdf --outdir courseware "courseware/<deck>.pptx" "courseware/LG-*.docx" "courseware/LP-*.docx"
```

The LP builder asserts against the manifest (day totals = 540 min; every lab's scheduled minutes
equal its manifest duration), so a mismatch fails the build on purpose. Screenshots go in
`labs/Lab N - <Title>/screenshots/NN-<desc>.png` and are referenced from `index.md` as
`![caption](screenshots/NN-desc.png)` followed by an italic `*Figure N.k — …*` line; the deck
builder captions its slides from the file name after the `NN-` prefix, so name files readably.

Version bumps: deck version lives in `build_v80_deck.py` (`VERSION`, filename + cover); LG/LP
versions live in each builder's `VERSION` + `VERSIONS` record. Superseded deck versions move to
`courseware/archive/` (never deleted). QA: run the `courseware-qa` agent (renders pages to
images) after any regeneration — pushes to the TMS/Drive are gated on it.

## Publishing

- **/github-push** — `.gitignore` enforces the exclusions: `assessment/` (never on GitHub),
  `*.zip` except `labs/**/skills/_packages/*.zip` (those ARE the deliverable), `reference/`
  source material (except `.claude/skills/**/reference/`), `.env`, and
  `scripts/copilot_studio_api/token.txt` / `_body.json` / `ids.json` / `urls.json`. Always
  refresh `README.md` against reality before committing.
- **/gdrive-push** — `python3 .claude/skills/gdrive-push/gdrive_push.py "<folder-link>" --repo .`
  ALWAYS ask the user for the Drive folder link; `--dry-run` first. MD5-skips unchanged files,
  archives superseded ones server-side, never deletes.
- **/tms-push** — `python3 .claude/skills/lms-push/lms_push.py --repo . --drive-folder "<link>"`.
  Auth: the LMS API requires the machine service key in the `x-api-key` header; the script reads
  env **`LMS_TMS_API_KEY`** (exported in `~/.zshrc`; the key originates from
  `~/projects/tertiary/ai-lms-tms/.env.local` → `EXTERNAL_API_KEY_FOR_CLAWDBOT`). Run
  `source ~/.zshrc` first. Question papers only — the two "Answers to …" keys are trainer-only
  and must never reach the LMS or GitHub.

## Live tenant work (labs, agents, workflows)

- **Three environments.** Always check the environment picker (bottom-left) first; never the
  Default environment.

  | Environment | Type | Id / org | Who can enter | Role |
  |---|---|---|---|---|
  | `Training Class 1` | Sandbox | `b723115a-b9a6-eccd-9894-c46209d4de9c`, org `orgcebea081` | **all 20** (admin + training1-19) | **Where learners work.** One per class, reset/refreshed between cohorts |
  | `Training Class 2` | Sandbox | `80af3aeb-fe8d-ea7f-b63d-a91d64276b93`, org `org48ba35b7` | all 20 | as above |
  | `Training Class 3` | Sandbox | `0c6acc59-f200-e3cf-adeb-219907332889`, org `org42e78ce5` | all 20 | as above |
  | `TGS-2022017524-Business Process Automation…` | Sandbox | `f4e94101-0889-e2f3-a0f4-dfd6d06ab28e`, org `org77fbcb45` | **admin + training1 only** | **Master reference environment** — the 12 `Lab N - … (DO NOT DELETE)` workflows and 9 reference agents. Keep pristine |
  | `Copilot Studio Training (Developer)` | Developer | `dd7a990d-5d41-e3a8-82ae-8ede6fe42d92`, org `orgb195a02f` | **admin + training1 only** | The original build environment, **retired from classroom use** |
  | `Tertiary Infotech Academy` | Default | `Default-0a37137e-…` | everyone (cannot be limited) | Tenant default — **never used by this course** |

  Sandbox is used for classes because Developer is single-user, Trial self-deletes after 30 days,
  and only Sandbox supports multi-user access plus **Reset** between classes. Courseware must tell
  learners to select their **Training Class** environment, never the Developer one.

- **Access is enforced by Dataverse security roles, not security groups** (set 2026-09-04).
  `PATCH …/environments/<id>` with a `securityGroupId` is **rejected on Default and Developer**
  SKUs (`CannotSetSecurityGroupIdForEnvironmentType`), so the two reference environments are
  locked down by stripping every security role from training2-19 instead — a user with **no**
  roles is still listed but cannot open the environment. To re-grant, add `Environment Maker`.
  Removal call (note the `%24` encoding; the literal `$ref` form fails with `0x80060888`):
  `DELETE <org>/api/data/v9.2/systemusers(<id>)/systemuserroles_association/%24ref?%24id=<org>/api/data/v9.2/roles(<roleid>)`
  On a Sandbox a security group *is* accepted; clear it with the all-zeros guid
  (`null`/`""` return 2xx but leave the old group in place).
  **The tenant has exactly 20 accounts**: `admin@tertiaryinfotech.onmicrosoft.com` +
  `training1-19`. There is no personal/staff account (no `angch@…`) and none is needed —
  **`admin@` is the trainer account** for the two reference environments.

- **Trainers sign in to the master Sandbox to review the reference builds.** Both `admin@`
  (System Administrator) and `training1@` (Environment Maker + **System Customizer**) can open
  every `Lab N - … (DO NOT DELETE)` workflow and agent there.
  **Environment Maker alone is not enough**: it grants only *Basic* (own-records) read on
  `workflow` and `bot`, and every reference row is owned by `admin@`, so a trainer holding just
  that role sees an **empty list** — the labs are present but invisible, with no error.
  **System Customizer** grants *Global* read on both tables without full admin, and is what
  training1 now holds. (`Agent Viewer` and `Bot Viewer` are also Basic-only — they do not help.)
  Check depths with `GET <org>/api/data/v9.2/RetrieveRolePrivilegesRole(RoleId=<roleid>)`,
  matching `prvReadWorkflow` / `prvReadbot`.

- **Copying the reference labs Developer → master Sandbox** (done 2026-09-04) went through an
  **unmanaged solution `TGS2022017524Labs`**. Solution component types: **workflow 29**,
  **bot 10225**, **connectionreference 10163**. The connection references **must** be included in
  the solution or the import fails with missing-dependency errors. Imported flows and agents
  arrive in **Draft** in the target environment and must be **published** there before use.
- **Imported connection references arrive UNBOUND** and block activation with `0x80060467`
  *"A connector was imported, however the related connection references need connections
  created…"*. Fix: create each connection in the target environment, then
  `PATCH connectionreferences(<connectionreferenceid>) {"connectionid":"<connection guid>"}`.
  The connection guid is **not** in Dataverse (`/connections` returns empty) — capture it from
  the `…environment.api.powerplatform.com/connectivity/connections` response on the maker
  Connections page; each row's `name` field *is* the guid. Connector names must match exactly:
  a `shared_advancedapprovals` reference will not bind to a `shared_approvals` connection
  (404 `ConnectionNotFound`).
- **Completing a connector's OAuth under Playwright**: drive the entire popup flow inside a
  *single* tool call. Split across calls the consent popup auto-closes and the connection stays
  on "Reconnect". If an imported connection is stuck with a `{username}{token}` display name it
  is broken beyond repair — create a **new** connection for that connector instead.
- `.env` (gitignored, never commit or echo values) holds the classroom credentials:
  `TRAINING_ACCOUNT` / `TRAINING_TENANT` / `TRAINING_PASSWORD` (training1, the shared trainer
  account) and the HR SharePoint pointers (`HR_SITE_URL`, `HR_KNOWLEDGE_FOLDER_URL`,
  `HR_GROUP_ALIAS`). The 2026-09-04 reference builds were made as
  `admin@tertiaryinfotech.onmicrosoft.com`.
- **Naming.** Workflows: `Lab N - <Title>`; the trainer's copies `Lab N - <Title> (DO NOT DELETE)`.
  **Agent names are hard-capped at 30 characters** (`Agent name must be 30 characters or fewer`),
  so the trainer's agents are `Lab 5 - HR (DO NOT DELETE)`, `Lab 6 - Proc (DO NOT DELETE)`,
  `Lab 7 - Sales (DO NOT DELETE)`, `Lab 8 - IT (DO NOT DELETE)`, `Lab 9 - Res (DO NOT DELETE)`,
  `Lab 9 - Blog (DO NOT DELETE)`, `Lab 9 - Review (DO NOT DELETE)`, `Lab 9 - Mgr (DO NOT DELETE)`,
  `Lab 11 - Blog (DO NOT DELETE)`; learners use `Lab 9 - Marketing Manager` (25 chars), never
  `… Manager Agent` (31). Never write "(DO NOT DELETE)" after an agent name.
- **Copilot Credits — a hard gate, verified 2026-09-04.** With 0 credits in an environment:
  - Preview, demo-website chats and every Agent / Classify / Copilot node run fail with
    *"You need credits to continue … Error code: EnforcementUsageCredits"*, and
  - **a workflow cannot be activated or published at all** — `PATCH workflows(<id>)
    {"statecode":1,"statuscode":2}` returns `PaymentRequired / ConsumptionViolation`,
    *"Flow cannot be activated due to insufficient Copilot Studio capacity in this environment"*
    (https://aka.ms/messagecapacity). Only authoring and saving still work.

  On 2026-09-04 the tenant showed **Copilot Studio messages: 0 of 0 assigned** (Licensing →
  Capacity → Add-ons), which is why the 12 workflows imported into the master Sandbox are all
  still Draft. The course owner buys capacity (Licensing → Billing Plans pay-as-you-go, or a
  Copilot Credits pack) and allocates it to the master Sandbox **and to every Training Class
  environment** before class; then re-run the activation PATCH loop — no rebuild needed.
  Lab 0 and Lab 5 carry a boxed note; do not "debug" a build for this message.
- Before asserting how any Copilot Studio field behaves, read
  `.claude/skills/copilot-studio-flows/SKILL.md` (section *2026-09-04 — new designer facts* is
  the latest) — every entry is tenant-verified. When the UI and the skill disagree, trust the UI
  and update the skill (both this repo's copy and `~/.claude/skills/copilot-studio-flows/`).
- Learners no longer share the reference environment — each class has its own Sandbox. Only ever
  modify the canonical trainer builds, and only in the master reference Sandbox.

## Building reference workflows through the Dataverse API

`scripts/copilot_studio_api/` is the route used on 2026-09-04 to create the twelve reference
workflows (Labs 1–4, 6, 10–16) without clicking every node:

- `wfapi.py` — `Workflow` graph builder + `create(wf)` (POSTs a Dataverse `workflows` row whose
  `clientdata` carries only the designer GRAPH), `find`, `designer_url(wid)`, connection
  references of the admin account. `wfapi_a.py` — manual-trigger inputs, agent-call trigger,
  *Respond to the agent*, Copilot node, Compose. `wfapi_ext.py` — Response / HTTP / Compose
  built-in functions, SharePoint knowledge on an Agent node, the `obj_expr`/`jlit` JSON escaper
  (there is no `setProperty()` in this designer).
- `build_labN.py` — one per workflow, re-runnable (`create` deletes a same-named row first).
  `FORMATS.md` — every graph format verified live (read it before writing a new builder).
  `excel-params.json`, `teams-params.json`, `lab3-questions.json`, `lab1-clientdata.json`,
  `lab3-stage1-clientdata.json` — ids the designer stored when a picker was used once.
- Auth: `export DATAVERSE_TOKEN='Bearer eyJ…'` (a token from the signed-in browser session to
  `https://orgb195a02f.crm5.dynamics.com`) or a gitignored `token.txt` next to `wfapi.py`.
  **Never commit tokens, `_body.json`, `ids.json` or `urls.json`.**
- Loop: `python3 build_labN.py` → open `designer_url(wid)` → rename-nudge (click the title, End,
  Space, Backspace, Enter) → **Save** (compiles the Logic-Apps actions) → **Publish** → test.
  A node showing *Needs setup* names the missing field in its `aria-label`. Updating an already
  designer-saved row fails with 0x80040203 — recreate instead of PATCH.

## Layout

```
labs/                 ground truth: Lab 0–17 (index.md + assets/ + screenshots/ each) + Module 1–5 readings + labs/README.md
courseware/           deck PPTX/PDF v8.0, LG/LP DOCX+PDF, alignment_manifest.json, slide_map.json, assets/, archive/
assessment/           WA (SAQ) + PP papers and answer keys — Drive only, never GitHub/LMS-keys
scripts/              build_v80_deck.py, lab asset builders (skill packages, workbooks, PDFs, flowcharts), copilot_studio_api/
labs-archive/         retired labs
.claude/skills/       repo-scoped builders (wsq-learner-guide, wsq-lesson-plan) and the copilot-studio-flows fact base
```
