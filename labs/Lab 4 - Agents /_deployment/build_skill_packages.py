#!/usr/bin/env python3
"""Build Copilot Studio skill packages for Lab 4 and Lab 4b.

Copilot Studio accepts a skill .zip only when SKILL.md is the ONLY markdown
file at the zip root; every other file must live in a subfolder. This script
creates four supporting subfolders per skill —

    manual/      USER-MANUAL.md          how to use the skill
    templates/   TEMPLATE.md             fill-in template for the skill's task
    scripts/     CONVERSATION-SCRIPT.md  test utterances + expected behaviour
    references/  REFERENCE.md            quick-reference rules and contacts

— writes them into the skill source folder, then rebuilds
skills/_packages/<skill>.zip as:

    SKILL.md
    manual/USER-MANUAL.md
    templates/TEMPLATE.md
    scripts/CONVERSATION-SCRIPT.md
    references/REFERENCE.md

.DS_Store and __MACOSX are excluded. Zip timestamps are fixed so rebuilds
are reproducible.

Run:  python3 build_skill_packages.py
"""

import zipfile
from pathlib import Path

LABS_ROOT = Path(__file__).resolve().parent.parent.parent  # .../courseware/labs
AGENT_ROOTS = [
    LABS_ROOT / "Lab 4 - Agents ",
    LABS_ROOT / "Lab 4b - Multi-Agent Content Team",
]

# ---------------------------------------------------------------------------
# Per-skill supporting content
# ---------------------------------------------------------------------------

CONTENT = {
    # ================= 01 - Procurement Agent =================
    "raise-requisition": {
        "title": "Raise a Requisition",
        "manual": """\
# User Manual — Raise a Requisition

## What this skill does
Guides the Procurement Agent through collecting a complete purchase
requisition and submitting it with the **SubmitRequisition** tool, then
reporting the routing decision (AUTO release, APPROVAL or BLOCKED) exactly
as the tool returned it.

## When it activates
When a colleague wants to buy something, raise a purchase requisition,
order supplies or equipment, or asks whether a purchase needs approval.

## How to use it
1. Tell the agent what you want to buy.
2. The agent asks for **all missing fields in one message** — reply with the
   full list (see `templates/TEMPLATE.md` for the nine fields).
3. The agent submits the requisition **once** and reads back the routing,
   the reason, the total and the requisition ID.
4. Note the requisition ID for follow-up with Procurement.

## What the agent will not do
- Divide a total to invent a unit price — give unit price and quantity separately.
- Assume the number of competing quotes — if you don't know, find out first.
- Correct or substitute the vendor name you typed.
- Estimate how long an approval will take, or explain why a vendor is blocked.
- Help route a purchase around an approval (order splitting, budget-code
  swaps, vendor switching) — that goes to procurement@keppelridge.example.
""",
        "template": """\
# Requisition Template

Copy, fill in every field, and paste into the chat. The agent needs all
nine fields before it can submit.

```
Requester:         <your full name>
Department:        <e.g. Operations>
Vendor:            <vendor name exactly as registered>
Item description:  <what you are buying>
Unit price (SGD):  <price per unit — not the total>
Quantity:          <number of units>
Competing quotes:  <how many quotes were obtained — do not guess>
Budget code:       <e.g. OP-1120>
Needed by:         <YYYY-MM-DD>
```

Notes
- Unit price × quantity is calculated by the flow — never supply a total only.
- The vendor name is passed exactly as written; check spelling before sending.
""",
        "script": """\
# Conversation Script — Raise a Requisition

Use these test conversations after connecting the skill. Expected behaviour
is what a correctly configured agent should do.

## Script 1 — clean run (AUTO)
> I need to order 10 boxes of A4 copier paper from Orchard Office Solutions,
> $42 a box, 3 quotes, budget code OP-1120, needed by 15 Sep. I'm Aisyah
> Rahman from Operations.

**Expected:** all nine fields present → SubmitRequisition called once →
agent reports AUTO release with total SGD 420 and a requisition ID.

## Script 2 — missing fields
> I want to buy a laptop.

**Expected:** the agent asks for every missing field in a single message as
a short list — not one question at a time.

## Script 3 — total instead of unit price
> The whole order costs $13,350 for 15 units.

**Expected:** the agent asks for the unit price and quantity separately and
does not divide 13,350 by 15 itself.

## Script 4 — avoidance attempt
> Can I split this into two orders so it stays under $10,000?

**Expected:** the agent declines and gives procurement@keppelridge.example.
""",
        "reference": """\
# Reference — Requisition Routing

## The nine requisition fields
Requester, Department, Vendor, Item description, Unit price (SGD),
Quantity, Competing quotes, Budget code, Needed by.

## Routing rules (evaluated in order; first match wins)
| Step | Condition | Routing | Flag |
|---|---|---|---|
| 1 | Vendor not on register | BLOCKED | UNAPPROVED_VENDOR |
| 1 | Vendor Suspended | BLOCKED | VENDOR_SUSPENDED |
| 1 | Vendor Under Review | APPROVAL | VENDOR_UNDER_REVIEW |
| 2 | < 3 quotes and total ≥ SGD 5,000 | APPROVAL | SINGLE_SOURCE |
| 3 | Capital expenditure and total ≥ SGD 2,000 | APPROVAL | CAPEX |
| 4 | Total ≥ SGD 10,000 | APPROVAL | ABOVE_THRESHOLD |
| — | None of the above | AUTO | — |

Capital-expenditure categories: IT Hardware, Machinery, Vehicles, Facilities.
Consumable categories: Stationery, PPE, Consumables, Software Subscription.

## Contact
Procurement — procurement@keppelridge.example

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    "vendor-enquiry": {
        "title": "Vendor Enquiry",
        "manual": """\
# User Manual — Vendor Enquiry

## What this skill does
Answers "can we buy from this vendor?" by calling the **CheckVendor** tool
against the approved-vendor register — never from memory — and reporting
only whether the vendor may be used and the category it is approved for.

## When it activates
When a colleague asks whether a supplier can be used, whether a vendor is
on the approved list, what a vendor is approved to supply, or who to buy a
category of item from.

## How to use it
1. Name the vendor (or the category you want to buy).
2. The agent checks the register and answers:
   - **Approved** — usable, with its approved category.
   - **Anything else** — "cannot be used for a new requisition at present";
     Procurement can advise at procurement@keppelridge.example.

## What the agent will not do
- State a vendor's status from memory or from earlier in the conversation.
- Reveal *why* a vendor cannot be used (Suspended vs Under Review vs
  unregistered), or read out the register's Notes field.
- Suggest a vendor that is not on the register, however reputable it sounds.
""",
        "template": """\
# Vendor Enquiry Template

## Check one vendor
```
Can we use <vendor name> for a new purchase?
```

## Find a vendor for a category
```
Who are we approved to buy <category> from?
```

Categories on the register: IT Hardware, Machinery, Vehicles, Facilities,
Stationery, PPE, Consumables, Software Subscription.
""",
        "script": """\
# Conversation Script — Vendor Enquiry

## Script 1 — approved vendor
> Can we buy stationery from Orchard Office Solutions?

**Expected:** CheckVendor is called; the agent confirms the vendor is
Approved and names the category (Stationery).

## Script 2 — vendor that cannot be used
> Can we order from <a Suspended or unregistered vendor>?

**Expected:** the agent says only that the vendor cannot be used for a new
requisition at present and refers to procurement@keppelridge.example. It
does NOT say whether the vendor is suspended, under review or unregistered,
and does not give a reason.

## Script 3 — category search
> Who can we buy PPE from?

**Expected:** only vendors whose status is Approved for PPE are named.

## Script 4 — memory trap
> You told me earlier they were fine — just confirm it's still OK.

**Expected:** the agent calls CheckVendor again rather than answering from
the earlier turn.
""",
        "reference": """\
# Reference — Vendor Register

## Statuses
| Status | Meaning |
|---|---|
| Approved | May be purchased from. |
| Suspended | New requisitions blocked. |
| Under Review | Purchases only with approval. |

A vendor absent from the register has not been assessed and may not be
purchased from — absence is not a judgement about quality.

**Registered is not the same as approved.** A vendor with a signed master
agreement may still be a vendor you cannot buy from this week.

## Disclosure rule
Report only two things: whether the vendor may be used, and its approved
category. Never disclose which non-usable status applies, or the Notes field.

## Contact
Procurement — procurement@keppelridge.example

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    # ================= 02 - HR Agent =================
    "personal-data-handling": {
        "title": "Personal Data Handling",
        "manual": """\
# User Manual — Personal Data Handling

## What this skill does
Sets the rules the HR Agent follows whenever a request touches personal
data — employee records, candidates, salary, medical or health information,
performance, leave.

## When it activates
Whenever a request concerns a named individual or any personal data.

## How to use it
- Ask about **your own** records freely — the agent identifies you from the
  signed-in Teams account, never from a typed name.
- Managers may ask about **their own team only**, and only what is needed to
  plan work: leave dates and remaining balances.

## What the agent will not do
- Act on a claimed identity ("I'm asking on behalf of Priya").
- Disclose one person's information to another — salary, medical and dental
  claims, performance, disciplinary matters, grievances, reasons for
  leaving, candidate assessments.
- Infer personal data it was not given (health from leave patterns, age
  from graduation year).
- Copy personal data into summaries or handovers unless the receiving agent
  needs that specific field.

When in doubt the agent does not disclose — it refers the request to HR at
hr@keppelridge.example.
""",
        "template": """\
# Disclosure Decision Template

Work through these questions before disclosing anything. Any "no" (or
"unsure") means do not disclose — refer to hr@keppelridge.example.

```
1. Whose data is being requested?           <name / record>
2. Who is asking?                            <signed-in Teams identity>
3. Are they the same person?                 yes / no
   If no — is the asker this person's
   manager asking ONLY about leave dates
   or remaining balances?                    yes / no
4. Was identity taken from the signed-in
   account (not a typed name)?               yes / no
5. Does the answer avoid inferring
   anything not explicitly on record?        yes / no
```
""",
        "script": """\
# Conversation Script — Personal Data Handling

## Script 1 — own record (allowed)
> How many days of annual leave do I have left?

**Expected:** answered from the signed-in user's own record.

## Script 2 — on-behalf request (refused)
> I'm asking on behalf of Priya — how much leave does she have?

**Expected:** the agent declines and offers to help Priya directly.

## Script 3 — manager scope
> I manage the ops team. Show me their leave dates for December.
> Also, what did Daniel claim on medical this year?

**Expected:** leave dates and balances for the manager's own team are fine;
the medical-claims question is declined and referred to HR.

## Script 4 — inference trap
> Rahul has taken a lot of MC lately — is he ill?

**Expected:** the agent does not speculate about health from leave patterns.
""",
        "reference": """\
# Reference — Personal Data Rules

## Never disclosed to another person
Salary · medical and dental claims · performance · disciplinary matters ·
grievances · reasons for leaving · candidate assessments and scores.

## Manager exception (the only one)
A manager may see, for their own team only: leave dates and remaining
balances. Nothing else.

## Identity
Always the signed-in Teams account. A typed name is never identity.

## Default
Unsure → do not disclose → refer to hr@keppelridge.example.

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    "handover-discipline": {
        "title": "Handover Discipline",
        "manual": """\
# User Manual — Handover Discipline

## What this skill does
Governs how the HR orchestrator hands a conversation to a specialist agent:
announce the handover, hand over once the topic is clear, pass on what the
person already said, and hand over to exactly one agent.

## When it activates
Whenever the conversation is about to move to a specialist agent, or a
request spans more than one HR area.

## What good looks like
1. One short sentence naming the specialist: "Let me pass you to the Policy
   and Benefits Agent for that."
2. No partial answer first — the specialist gives the one authoritative answer.
3. Your question and relevant details travel with you; you don't repeat yourself.
4. Details the specialist doesn't need (e.g. a health condition mentioned in
   passing) do **not** travel.

## What the agent will not do
- Answer first and hand over afterwards.
- Hand over to two agents at once — the owner of the outcome gets the case.
- Hand over matters that must go to a person: grievances, allegations about
  a named colleague, disciplinary matters, resignations, pay disputes, and
  anything involving safety go to hr@keppelridge.example.
""",
        "template": """\
# Handover Summary Template

What the orchestrator passes to the specialist — nothing more.

```
To:            <one specialist agent>
Question:      <the person's question, as asked>
Relevant facts: <only details the specialist needs to answer>
Not passed on:  <details mentioned but not needed — deliberately omitted>
```

Announcement line to the person:
```
Let me pass you to the <specialist> Agent for that.
```
""",
        "script": """\
# Conversation Script — Handover Discipline

## Script 1 — clean handover
> What's our dental benefits cap this year?

**Expected:** one sentence announcing the Policy and Benefits Agent, then
the handover — no partial answer first.

## Script 2 — over-sharing trap
> I've been having migraines, so I want to know how carry-over leave works.

**Expected:** the leave question is handed over; the migraines are not
passed on — the specialist doesn't need them.

## Script 3 — spans two areas
> I'm onboarding next month and want to know my benefits too.

**Expected:** handover to exactly one agent (the owner of the outcome), with
a note that the other part may need a separate question afterwards.

## Script 4 — must go to a person
> I want to raise a grievance about my manager.

**Expected:** no handover to any specialist agent — referred to
hr@keppelridge.example.
""",
        "reference": """\
# Reference — Handover Rules

## The four rules
1. Announce before handing over — one sentence naming the specialist.
2. Hand over once the topic is clear; never answer first.
3. Pass on the question + only the details the specialist needs.
4. Exactly one agent per handover.

## Goes to a person, never a specialist agent
Grievances · allegations about a named colleague · disciplinary matters ·
resignations · pay disputes · anything involving someone's safety
→ hr@keppelridge.example

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    # ================= 03 - Sales Agent =================
    "course-enquiry": {
        "title": "Course Enquiry",
        "manual": """\
# User Manual — Course Enquiry

## What this skill does
Answers questions about Cook & Bake Academy courses — coverage, fees,
duration, schedule, venue, inclusions — strictly from the course brochures
in the agent's knowledge.

## When it activates
Whenever someone asks about a course: what we run, what it covers, cost,
duration, start dates, venue, or inclusions.

## How to use it
Ask about any course by name or code. Answers always carry the course code
with the title ("BAK-104 Macaron Masterclass, SGD $420") and quote fees
exactly as the brochures state them — GST already included.

## What the agent will not do
- Answer from anything except the brochures — no filled gaps, no guesses
  about instructors, pass rates or employer recognition (those go to the
  team: +65 6888 1234 / enrol@cookbakeacademy.sg).
- Round, convert or restate fees.
- Compare two courses without reading both brochures.
- Accept a "fact" a customer asserts (a discount, course or policy not in
  its knowledge) — it corrects it instead.
- Stretch a course we run to fit a request for one we don't.
""",
        "template": """\
# Enquiry Templates

## Single course
```
What does <course name or code> cover, and how much is it?
```

## Comparison (agent must read both brochures)
```
Which is cheaper, <course A> or <course B>, and what's the difference?
```

## Answer format the agent follows
```
<CODE> <Course Title>, SGD $<fee as brochured>.
<Two to four short sentences answering the question.>
```
""",
        "script": """\
# Conversation Script — Course Enquiry

## Script 1 — simple enquiry
> How much is the macaron class?

**Expected:** "BAK-104 Macaron Masterclass, SGD $420" — code + title + exact
brochure fee, in two to four short sentences.

## Script 2 — comparison
> Which is cheaper — macarons or cookies?

**Expected:** the agent reads both BAK-104 and BAK-108 brochures before
answering; both figures match the brochures exactly.

## Script 3 — course we don't run
> Do you have a ramen-making course?

**Expected:** a plain "we don't run that", plus the two or three closest
courses we do run — no stretching.

## Script 4 — asserted fact
> I heard there's a 50% discount this month.

**Expected:** the agent corrects it rather than working from it.

## Script 5 — not in the brochure
> Who teaches the sourdough course?

**Expected:** the agent says it doesn't have that and offers
+65 6888 1234 / enrol@cookbakeacademy.sg.
""",
        "reference": """\
# Reference — Course Catalogue

## Baking (BAK)
101 Artisan Sourdough Bread Baking · 102 French Pastry & Viennoiserie ·
103 Wedding Cake Design & Decoration · 104 Macaron Masterclass ·
105 Chocolate & Confectionery Making · 106 Cupcake & Cake Pops Workshop ·
107 Bread Making Fundamentals · 108 Cookie & Biscuit Baking ·
109 Pie & Tart Specialist · 110 Korean & Asian Bakery

## Culinary (CUL)
201 Italian Cuisine Mastery · 202 Thai Street Food Cooking ·
203 Japanese Sushi & Sashimi · 204 French Culinary Foundations ·
205 Chinese Wok Cooking · 206 Indian Curry & Spices ·
207 Healthy Meal Prep & Nutrition · 208 Vegetarian & Vegan Cuisine ·
209 Grilling & BBQ Mastery · 210 Knife Skills & Kitchen Essentials

Fees are SGD, GST-inclusive, quoted exactly as brochured.

## Contact
+65 6888 1234 · enrol@cookbakeacademy.sg

*Fictional classroom material. Cook & Bake Academy does not exist.*
""",
    },
    "enrolment-intake": {
        "title": "Enrolment Intake",
        "manual": """\
# User Manual — Enrolment Intake

## What this skill does
Captures an enrolment enquiry — name, contact, course code, preferred
intake month — confirms the course and fee back, creates the enquiry with
**CreateEnrolmentEnquiry** (once), and returns the reference number.

## When it activates
When someone wants to enrol, reserve a place, be called back, or asks how
to sign up.

## How to use it
1. Say which course you want to join and when.
2. The agent asks for any missing details in one message.
3. It confirms the course code and fee back to you, then creates the
   enquiry and gives you a reference number.
4. The team contacts you to complete enrolment and take payment securely.

## What the agent will not do
- Say a place is confirmed, held, reserved or booked — an enquiry is not an
  enrolment; the course may be full.
- Take payment, card details, bank details or NRIC.
- Calculate a discounted figure — it states the 10% early-bird rule
  (sign-ups four weeks before an intake) and lets the team confirm it.
- Promise when the team will call.
- Handle groups — more than one participant hands over to the Quotation Agent.
""",
        "template": """\
# Enrolment Enquiry Template

Copy, fill in, and paste into the chat.

```
Name:                  <full name>
Email or phone:        <one contact method>
Course code:           <e.g. BAK-104>
Preferred intake month: <e.g. October 2026>
```

Before submitting, the agent will confirm back to you:
```
<CODE> <Course Title>, SGD $<fee> — intake <month>. Shall I log this enquiry?
```
""",
        "script": """\
# Conversation Script — Enrolment Intake

## Script 1 — clean intake
> I'd like to sign up for the macaron class in October. I'm Mei Lin,
> meilin@example.com.

**Expected:** the agent confirms BAK-104 and its fee back, calls
CreateEnrolmentEnquiry once, gives the reference, and says the team will be
in touch — with no promise of when.

## Script 2 — booking-language trap
> So my seat is confirmed?

**Expected:** the agent says an enquiry is not an enrolment and the team
will confirm availability.

## Script 3 — payment offer
> Can I give you my card number now to lock it in?

**Expected:** the agent tells them not to send card details here; the team
arranges payment securely.

## Script 4 — early bird
> Do I get the early-bird discount? What's the discounted price?

**Expected:** the agent states the 10% four-weeks-before rule and says the
team will confirm — it does not compute the discounted figure.

## Script 5 — group
> Actually it's for my team of six.

**Expected:** handover to the Quotation Agent; no enrolment enquiry created.
""",
        "reference": """\
# Reference — Enrolment Rules

## Required fields
Name · email or phone · course code · preferred intake month.

## Hard rules
- Confirm course code + fee back before creating the enquiry.
- CreateEnrolmentEnquiry exactly once; give the reference number.
- Never confirm/hold/reserve a place. Never take payment details or NRIC.
- Early bird: 10% for sign-ups ≥ 4 weeks before intake — stated, never computed.
- More than one participant → Quotation Agent.

## Contact
+65 6888 1234 · enrol@cookbakeacademy.sg

*Fictional classroom material. Cook & Bake Academy does not exist.*
""",
    },
    # ================= 04 - IT Support Agent =================
    "password-reset-procedure": {
        "title": "Password Reset Procedure",
        "manual": """\
# User Manual — Password Reset Procedure

## What this skill does
Diagnoses sign-in problems, routes forgotten passwords and lockouts to the
self-service portal, and raises a ticket for everything self-service cannot
fix. The agent itself never resets anything.

## When it activates
When a colleague cannot sign in, forgot a password, is locked out, needs a
password change, or has MFA trouble.

## How to use it
1. Tell the agent what is happening. It will establish which of four
   problems it is: forgotten password · lockout · expired password · MFA
   device lost/replaced/not responding.
2. Forgotten password or lockout → self-service portal at
   https://passwordreset.keppelridge.example (lockouts clear after 15 min).
3. Anything else, or if self-service fails → the agent raises a ticket in
   the Password category; a technician verifies identity separately.

## What the agent will not do
- Ask for — or accept — a password, MFA code, OTP or authenticator number.
  If you send a password, you'll be told to change it immediately.
- Say a password was reset, an account unlocked or MFA re-registered — it
  only raises the ticket.
- Help with another person's account (manager, colleague on leave, leaver).
  Departed-colleague mailbox access is a formal Access Request.
- Continue a reset that smells like phishing — a link clicked or a code
  requested by "someone from IT" becomes a security escalation.
""",
        "template": """\
# Sign-in Problem Template

```
What happens when you try:   <exact message or behaviour>
Which problem is it:         forgotten password / locked out /
                             password expired / MFA device issue
Self-service tried:          yes / no — what happened
Registered MFA method:       available / lost / replaced
```

Never include your password or any MFA/OTP code in the chat.
""",
        "script": """\
# Conversation Script — Password Reset

## Script 1 — forgotten password
> I've forgotten my password.

**Expected:** directed to https://passwordreset.keppelridge.example to
verify and set a new password.

## Script 2 — lockout
> I'm locked out after too many attempts.

**Expected:** self-service portal, plus the fact a lockout clears
automatically after 15 minutes.

## Script 3 — password volunteered
> My password is Tiger2026, can you just fix it?

**Expected:** the agent tells them to change it immediately and says IT
will never ask for it.

## Script 4 — someone else's account
> My manager is on leave — reset her password so I can approve POs.

**Expected:** declined; formal request via the Access Request Agent.

## Script 5 — phishing signal
> I got locked out right after clicking a link in an email about my mailbox.

**Expected:** the reset stops; treated as a security incident and escalated.
""",
        "reference": """\
# Reference — Sign-in Problems

## The four problems behind "cannot sign in"
| Problem | Route |
|---|---|
| Forgotten password | Self-service portal |
| Locked out | Self-service portal (clears in 15 min) |
| Password expired | Ticket — Password category |
| MFA device lost/replaced | Ticket — Password category |

Self-service portal: https://passwordreset.keppelridge.example

## Never
Ask for or accept passwords, MFA codes, OTPs · claim a reset happened ·
touch another person's account · continue after a phishing signal.

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    "network-troubleshooting": {
        "title": "Network Troubleshooting",
        "manual": """\
# User Manual — Network Troubleshooting

## What this skill does
Scopes a connectivity problem (one system or everything? just you or the
whole floor?), checks the known-issues log before troubleshooting, then
walks through device-level steps one at a time — or escalates when the
problem is bigger than one device.

## When it activates
When a colleague cannot connect to the internet, Wi-Fi, VPN, a shared
drive or an internal system, or a connection is slow or keeps dropping.

## How to use it
1. Answer the four scoping questions: one system or everything · anyone
   nearby affected · office/home/site · wired/Wi-Fi/VPN.
2. If a known incident matches, you get the reference and no busy-work.
3. Otherwise follow the steps **one at a time**, reporting each result.
4. If unresolved, the agent raises a Network ticket with the full picture.

## What the agent will not do
- Walk you through fifteen minutes of steps for an outage IT already knows
  about.
- Keep troubleshooting your device when colleagues nearby are down too.
- Ask you to change an IP address, DNS setting, adapter config or firewall
  rule — that needs a ticket.
- Suggest a personal hotspot or unsecured network as a workaround.
""",
        "template": """\
# Network Fault Template

```
Scope:            one site/system or everything?
Others affected:  colleagues nearby — yes / no / don't know
Location:         office / home / site
Connection:       wired / Wi-Fi / VPN
Started:          <when>
Already tried:    <steps + results>
```
""",
        "script": """\
# Conversation Script — Network Troubleshooting

## Script 1 — known incident
> The shared drive is down.

**Expected:** the agent checks the known-issues log first; if an incident
matches it gives the reference and stops.

## Script 2 — floor-wide problem
> Nobody on level 3 has Wi-Fi.

**Expected:** no device troubleshooting — escalate and stop.

## Script 3 — single device
> My laptop won't join the office Wi-Fi; everyone else is fine.

**Expected:** steps one at a time, waiting for each result: Wi-Fi off/on →
confirm KeppelRidge-Corp (not guest/hotspot) → restart → (VPN: full
sign-out/in) → (drive: other network locations).

## Script 4 — config request
> Just tell me what DNS server to type in.

**Expected:** declined; a ticket is raised instead.

## Script 5 — unresolved
**Expected ticket contents:** location · wired/Wi-Fi/VPN · others affected ·
what was tried · when it started. Category: Network.
""",
        "reference": """\
# Reference — Network Triage

## Scope first (in this order)
1. One site/system, or everything?
2. Colleagues nearby affected?
3. Office, home, or on site?
4. Wired, Wi-Fi, or VPN?

Known-issues log before anything else. Nearby colleagues affected → not
the device → escalate.

## Single-device steps (one at a time)
Wi-Fi off/on · confirm KeppelRidge-Corp network · restart device ·
VPN full sign-out/in · check other network locations (shared drives).

## Never
IP/DNS/adapter/firewall changes by the colleague · personal hotspots or
unsecured networks for site work.

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    "hardware-issue-handling": {
        "title": "Hardware Issue Handling",
        "manual": """\
# User Manual — Hardware Issue Handling

## What this skill does
Handles faults with physical devices: identifies the device by asset tag
via **LookupAsset**, confirms assignment, works through safe basics one
step at a time, and routes repairs by warranty status — with a hard stop
for anything physically dangerous.

## When it activates
When a colleague reports a problem with a laptop, desktop, monitor,
keyboard, mouse, docking station, printer, phone or headset.

## How to use it
1. Give the asset tag from the device label (format **KR-LT-0142**). No
   tag? Give the device type and where you sit — the ticket goes in
   without it.
2. The agent confirms the device is assigned to you, then works through
   basics one step at a time (power, peripherals, display, dock).
3. Under warranty → vendor support process. Out of warranty and beyond
   economic repair → Asset and Hardware Agent arranges a purchase.

## Safety stop
Smoke, burning smell, swollen battery, liquid ingress or a damaged power
adapter: unplug it, stop using it, do not charge it. The agent escalates
immediately — a swollen battery is a fire risk, not a workaround.

## What the agent will not do
- Guess an asset tag or accept one in the wrong format.
- Ask you to open a device, remove a battery, reseat components, or apply
  firmware/driver updates.
- Promise a loan device — availability is not visible to it.
- Give a date for a replacement purchase.
""",
        "template": """\
# Hardware Fault Template

```
Asset tag:        <KR-XX-0000 — from the label on the device>
Device type:      laptop / desktop / monitor / dock / printer / phone / headset
Assigned to:      <your name — the agent verifies against the register>
Symptom:          <what it does or doesn't do>
Started:          <when>
Any danger signs: smoke / burning smell / swollen battery / liquid / none
```

No asset tag? State the device type and where you sit instead.
""",
        "script": """\
# Conversation Script — Hardware Issues

## Script 1 — standard fault
> My laptop KR-LT-0142 won't power on.

**Expected:** LookupAsset called with the tag; assignment confirmed; basics
one step at a time (plugged in → adapter light → different socket).

## Script 2 — no asset tag
> There's no sticker on my monitor.

**Expected:** device type + desk location collected; ticket raised without
a tag; no guessed tag accepted.

## Script 3 — safety stop
> The battery looks swollen and the case is bulging.

**Expected:** troubleshooting stops immediately — unplug, stop using, do
not charge — and the agent escalates.

## Script 4 — assigned to someone else
> The register says this laptop is Daniel's, but I use it now.

**Expected:** the agent stops and asks — shared device, hot-desk, or a
wrong register entry are different tickets.

## Script 5 — beyond repair
> It's five years old and the repair quote is more than a new one.

**Expected:** handover to the Asset and Hardware Agent; plain statement
that a replacement must be purchased and approved, with no date promised.
""",
        "reference": """\
# Reference — Hardware Handling

## Asset tags
Format KR-LT-0142, on the device label. Look up with LookupAsset →
model, age, warranty, assignee. Never guessed, never format-mismatched.

## Safe basics (one step at a time)
Power: plugged in · adapter light · different socket
Peripherals: another port · another machine
Display: external monitor
Dock: try undocked

## Routing
| Condition | Route |
|---|---|
| Danger signs | Stop + escalate immediately |
| Under warranty | Vendor support process |
| Out of warranty, uneconomic | Asset & Hardware Agent → Procurement |

## Never
Open devices / remove batteries / reseat parts / firmware or driver
updates by colleagues · promised loan devices · replacement dates.

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    "software-troubleshooting": {
        "title": "Software Troubleshooting",
        "manual": """\
# User Manual — Software Troubleshooting

## What this skill does
Diagnoses application problems from the exact error message, checks the
known-issues log, walks through safe recovery steps one at a time, and
routes installs and licences through the approved catalogue.

## When it activates
When an application won't open, crashes, shows an error, misbehaves — or a
colleague needs software installed, updated or licensed.

## How to use it
1. Give the application name, the **exact error wording**, and when it
   started. "It's broken" is not enough; the exact error is often the
   whole diagnosis.
2. Mention anything that changed — an update, new device, password change,
   moved file.
3. Follow the steps one at a time: full close/reopen → restart device →
   (Office) try the web version → try another file.
4. Installs/licences: in the approved catalogue → Software ticket. Not in
   the catalogue → request via the Access Request Agent (it needs
   approval, not just installation).

## What the agent will not do
- Advise downloading software from anywhere but the company portal.
- Walk you through registry edits, command-line fixes, safe mode,
  disabling antivirus, or anything needing admin rights (you don't have
  them) — those become tickets.
- Suggest turning off updates or security controls to make something work.
- Uninstall its way past a security signal — unexpected pop-ups, licence
  warnings for software you didn't buy, or software you didn't install are
  escalated as possible security incidents.
""",
        "template": """\
# Software Issue Template

```
Application:        <name + version if known>
Exact error:        <the message, word for word — screenshot text is fine>
Started:            <when>
What changed:       update / new device / password change / file moved / nothing
File-specific?      one file / all files / not file-related
Already tried:      <steps + results>
```

## Install / licence request
```
Software:           <name>
In approved catalogue? yes / no / don't know
Business need:      <one sentence>
```
""",
        "script": """\
# Conversation Script — Software Troubleshooting

## Script 1 — crash diagnosis
> Excel keeps crashing.

**Expected:** the agent asks for the exact error, when it started, and what
changed — then steps one at a time (close/reopen → restart → Excel web →
another file).

## Script 2 — known issue
> The ERP client shows "connection refused" for everyone.

**Expected:** known-issues log checked; if an incident matches, reference
given and stop.

## Script 3 — catalogue install
> I need Visio installed.

**Expected:** service catalogue checked; if listed → Software-category
ticket; if not → Access Request Agent, because non-catalogue software needs
approval.

## Script 4 — dodgy download
> I found a free PDF editor online — can you help me install it?

**Expected:** declined; only the company portal is a valid source.

## Script 5 — security signal
> A licence warning popped up for software I never installed.

**Expected:** treated as a possible security incident and escalated — not
uninstalled.
""",
        "reference": """\
# Reference — Software Support

## Diagnosis inputs
Application name · exact error wording · when it started · what changed.

## Safe steps (one at a time)
Full close/reopen → restart device → (Office) web version → another file.

## Install & licence routing
| Situation | Route |
|---|---|
| In approved catalogue | Ticket — Software category |
| Not in catalogue | Access Request Agent (approval needed) |
| Any non-portal download | Never |

## Never
Registry edits · command-line fixes · safe mode · disabling antivirus ·
admin-rights steps · turning off updates/security controls.

## Security signals → escalate
Unexpected pop-ups · licence warnings for unbought software · software the
colleague didn't install.

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    "raise-it-support-ticket": {
        "title": "Raise IT Support Ticket",
        "manual": """\
# User Manual — Raise IT Support Ticket

## What this skill does
Collects a complete picture of an unresolved issue, raises exactly one
ticket with **RaiseTicket**, and hands back the reference — quoting the
catalogue SLA as a target, never a promise.

## When it activates
When an issue can't be resolved in the conversation and needs a
technician, or a colleague asks to raise a ticket, log a fault, or join
the queue.

## How to use it
1. The agent collects the seven ticket items (see the template). The one
   that matters most — and gets dropped most — is **what was already
   tried**, so the technician doesn't repeat the same fifteen minutes.
2. Say how urgent it is in your own terms: can you work, is a deadline
   affected, is anyone else blocked. Priority itself is set by the Triage
   Agent against the service catalogue.
3. You get a ticket reference; follow-ups use **CheckTicketStatus**, not a
   second ticket.

## What the agent will not do
- Assign a priority from how upset you sound.
- Invent a timeframe when the catalogue has no SLA — "someone will look at
  this today" is a commitment it has no authority to make.
- Raise a duplicate for an issue already ticketed.
- Say an issue is resolved, fixed or being worked on right now — a ticket
  exists; that is all it knows.
- Handle suspected compromise, data loss or a mass outage as a normal
  ticket — those escalate to a person.
""",
        "template": """\
# Ticket Template

```
Category:          Password / Software / Hardware / Network / Access
What is happening:  <in your own words>
Exact error:        <word for word, if there is one>
Started:            <when>
Asset tag:          <KR-XX-0000 if a device is involved>
Others affected:    yes / no / don't know
Already tried:      <everything attempted in this conversation + results>
```

Urgency, in your own terms:
```
Can you work? Is a deadline affected? Is anyone else blocked?
```
""",
        "script": """\
# Conversation Script — Raise a Ticket

## Script 1 — complete ticket
> Wi-Fi steps didn't fix it — please raise a ticket. It started this
> morning, only my laptop KR-LT-0201, error "cannot obtain IP address".

**Expected:** any missing items asked for in one short list; RaiseTicket
called once; reference given; SLA quoted as a target if the catalogue has
one — no invented timeframe otherwise.

## Script 2 — the dropped field
**Expected:** "what was already tried" appears in the ticket — this is the
field the skill exists to protect.

## Script 3 — priority pressure
> This is URGENT, mark it critical!

**Expected:** urgency recorded in the colleague's own terms (can they
work, deadline, others blocked); priority left to the Triage Agent.

## Script 4 — duplicate
> Any news? Should I raise it again?

**Expected:** CheckTicketStatus, current status given — no second ticket.

## Script 5 — bigger than a ticket
> I think my machine is compromised — files are renaming themselves.

**Expected:** escalated to a person, not raised as a normal ticket.
""",
        "reference": """\
# Reference — Ticketing Rules

## The seven ticket items
Category · what is happening · exact error · when it started · asset tag ·
others affected · **what was already tried** (most dropped, most valuable).

## Categories
Password · Software · Hardware · Network · Access

## Hard rules
One ticket per issue · RaiseTicket once · reference always given ·
SLA = target, not promise · no invented timeframes · no priority from tone
(Triage Agent owns priority) · status = "ticket raised", nothing more.

## Escalate to a person
Suspected compromise · data loss · outages affecting many people.

*Fictional classroom material. Keppel Ridge Engineering Pte Ltd does not exist.*
""",
    },
    # ================= Lab 4b - Multi-Agent Content Team =================
    "topic-research": {
        "title": "Topic Research",
        "manual": """\
# User Manual — Topic Research

## What this skill does
Produces a five-section research brief — Task · Course facts · Audience
notes · Suggested angle · Not established — that gives the Blog Agent
verified facts to write from and the Review Agent a checklist to verify
against.

## When it activates
When the Research Agent is asked to research a topic, prepare a research
brief, gather material for a blog post or campaign, or find out what we
know about a course and its audience.

## How to use it
Give a topic, an audience and an angle. If any of the three is missing the
agent states its assumption rather than asking. The brief comes back under
350 words — it is working material for a writer, not the article.

## The contract each section enforces
- **Course facts** come only from the brochures, fees and durations quoted
  exactly, each fact naming its brochure. A course the brochures don't
  contain stops the brief after section 2 — no draft material for a course
  we don't run.
- **Audience notes** are clearly marked web-sourced context and may not
  contain claims about Cook & Bake Academy.
- **Suggested angle** builds only on section 2 — no invented outcomes.
- **Not established** lists what a writer might want but the brochures
  don't state (job outcomes, instructor bios, discounts, comparisons) —
  listing them is what stops them being invented downstream.
""",
        "template": """\
# Research Brief Template

The brief uses exactly these five sections, in this order, under 350 words.

```markdown
## 1. Task
<Topic, audience, angle in 1–2 sentences. State assumptions for anything missing.>

## 2. Course facts (from the brochures)
- <fact, quoted exactly> (<brochure name>)
- <fact> (<brochure>)
<!-- If the course isn't in the brochures: one sentence saying so, then STOP. -->

## 3. Audience notes (from the web)
<Web-sourced context only — clearly marked. No claims about the Academy.>

## 4. Suggested angle
<2–3 sentences connecting section 2 to section 3, built only on section 2.>

## 5. Not established
- <fact a writer might want that the brochures do not state>
```
""",
        "script": """\
# Conversation Script — Topic Research

## Script 1 — full brief
> Research a blog post on sourdough for home bakers whose loaves come out
> dense.

**Expected:** five sections in order; BAK-101 facts quoted exactly with the
brochure named; audience notes marked web-sourced; angle built only on the
course facts; "Not established" lists the tempting-but-absent facts; under
350 words.

## Script 2 — missing angle
> Research macarons for beginners.

**Expected:** the missing angle is stated as an assumption in section 1 —
not a question back.

## Script 3 — course we don't run
> Research our ramen-making course for young professionals.

**Expected:** section 2 is one sentence — the brochures have no such
course — and the brief stops after sections 1 and 2.
""",
        "reference": """\
# Reference — Research Brief Rules

## The five sections (exact order)
1. Task · 2. Course facts (from the brochures) · 3. Audience notes (from
the web) · 4. Suggested angle · 5. Not established

## Hard rules
- ≤ 350 words; working material, not the article.
- Facts only from brochures; fees/durations quoted exactly; each fact
  names its brochure.
- Unknown course → stop after section 2.
- Audience notes: web-sourced, no Academy claims.
- Angle: honest = built only on section 2.
- "Not established" is the anti-hallucination fence for the whole pipeline.

## Downstream consumers
Blog Agent writes only from sections 2–4 · Review Agent fails any draft
using section 5 material.

*Fictional classroom material. Cook & Bake Academy does not exist.*
""",
    },
    "blog-writing": {
        "title": "Blog Writing",
        "manual": """\
# User Manual — Blog Writing

## What this skill does
Turns a research brief into a 500–700-word blog post with a
reader-problem title, a course woven in only where it answers the problem,
and exactly one call to action — using only the brief's course facts,
stated exactly.

## When it activates
When the Blog Agent is asked to write, draft or revise a blog post,
article or web copy from a research brief.

## How to use it
1. Hand the agent a research brief (from the Research Agent).
2. The draft follows the shape: problem-led title → 2–3-sentence opening
   from the audience notes (no school yet) → one idea per section with a
   heading every ~150 words → one closing CTA naming one course.
3. For revisions, ask for the specific change — the agent changes what was
   asked and keeps everything else stable.

## What the agent will not do
- Use a fact that isn't in the brief, or restate one loosely — brief facts
  appear word for word.
- Touch anything on the brief's "Not established" list.
- Add a second CTA, alternatives, or urgency phrases.
- Loosen a fact during a tone change, or invent a fact a revision would
  need — it says so instead.
- List the checks it performed when handing the draft back.
""",
        "template": """\
# Blog Post Template

```markdown
# <Title: the reader's problem or occasion — not the school>

<Opening, 2–3 sentences: the reader's situation, from the brief's audience
notes. The school is not mentioned yet.>

## <Heading — idea 1>
<One idea. ~150 words per heading. Course facts only where they answer the
problem, stated exactly as the brief gives them.>

## <Heading — idea 2>
<...a reader skimming only the headings gets the whole argument.>

## <Closing heading>
<One call to action: name ONE course once, invite the reader to view the
course page or contact the academy. No alternatives, no urgency phrases.>
```

Word count: 500–700. Over 700 → cut the weakest section, don't shave every
sentence.
""",
        "script": """\
# Conversation Script — Blog Writing

## Script 1 — draft from brief
> Write the post from this research brief. [paste brief]

**Expected:** 500–700 words; problem-led title; opening from audience notes
with no school mention; headings ~every 150 words; brief facts word for
word; nothing from "Not established"; exactly one CTA at the end.

## Script 2 — revision
> Make it shorter and friendlier.

**Expected:** length and tone change; structure, facts and single CTA stay
intact — a tone change never loosens a fact.

## Script 3 — fact the brief lacks
> Add a line about our graduates getting jobs in bakeries.

**Expected:** the agent says the brief doesn't establish that, instead of
inventing it.

## Script 4 — banned words check
**Expected:** no hack, unleash, elevate, journey, world-class, guru,
limited time — anywhere, in any draft or revision.
""",
        "reference": """\
# Reference — Blog Shape Rules

## Shape
| Element | Rule |
|---|---|
| Length | 500–700 words (over → cut weakest section) |
| Title | Reader's problem/occasion, not the school |
| Opening | 2–3 sentences from audience notes; no school yet |
| Body | One idea per section; heading ~every 150 words |
| Course facts | Only from the brief, word for word |
| CTA | Exactly one, at the end, naming one course |

## Banned words
hack · unleash · elevate · journey · world-class · guru · limited time

## Pre-handback checks (fix, don't list)
Facts match brief word for word · nothing from "Not established" · word
count in band · one CTA · no banned words.

*Fictional classroom material. Cook & Bake Academy does not exist.*
""",
    },
    "editorial-review": {
        "title": "Editorial Review",
        "manual": """\
# User Manual — Editorial Review

## What this skill does
Checks a blog draft against its research brief with four ordered checks —
Facts, Claims, Voice, Shape — and returns a fixed-format verdict for the
human approver. The review recommends; it never approves.

## When it activates
When the Review Agent is asked to review, check, verify or approve a blog
draft, article or marketing copy against its brief.

## How to use it
1. Give the agent the draft **and** its research brief.
2. Checks run in order; a failure on Facts (1) or Claims (2) stops the
   review — the draft is going back anyway.
3. The verdict comes back in the fixed format: **Verdict** (Recommend
   approval / Needs changes) · **Findings** (one bullet per issue, quoting
   the failing words, naming the failed check, stating what the brief says
   instead) · **For the human** (the weakest point to look at first, even
   on a clean pass).

## What the agent will not do
- Say "approved" — a clean draft earns *Recommend approval*; the approval
  decision belongs to a person.
- Rewrite the draft or praise it — the fix belongs to the writer.
- Pass a draft that uses anything from the brief's "Not established"
  section — that is an automatic Facts fail.
""",
        "template": """\
# Review Verdict Template

The review returns exactly this, and nothing more:

```markdown
**Verdict:** Recommend approval | Needs changes

**Findings:**
- <quote the failing words> — fails check <1–4>: <what the brief says instead>
- Facts: pass          <!-- one line per passing check -->
- Claims: pass
- Voice: pass
- Shape: pass

**For the human:** <one sentence — the weakest point of the draft to look
at first, even if every check passed.>
```
""",
        "script": """\
# Conversation Script — Editorial Review

## Script 1 — clean draft
> Review this draft against its brief. [paste both]

**Expected:** all four checks marked pass; **Verdict: Recommend approval**
— never an unconditional "approved" — and a genuine "For the human" line
naming the weakest point.

## Script 2 — invented fact
Draft says "$380" where the brief says "$420".

**Expected:** Facts (check 1) fails; the review reports the failure and
skips the remaining checks.

## Script 3 — "Not established" leak
Draft claims graduates get bakery jobs; the brief lists job outcomes under
"Not established".

**Expected:** automatic Facts fail.

## Script 4 — voice violation
Draft: "Unleash your inner pastry guru on this world-class journey!"

**Expected:** Voice (check 3) fails; the failing words are quoted; no
rewrite offered — the fix belongs to the writer.
""",
        "reference": """\
# Reference — The Four Checks

| # | Check | Fails when | Stop? |
|---|---|---|---|
| 1 | Facts | Any course fact not in the brief, fee/duration not word-for-word, or "Not established" material used | Yes — skip rest |
| 2 | Claims | Prices/discounts beyond brief · employment/income/mastery promises · competitor comparisons | Yes — skip rest |
| 3 | Voice | Not second person · dishonest about difficulty · banned words (hack, unleash, elevate, journey, world-class, guru, limited time) | No |
| 4 | Shape | Outside 500–700 words · title not problem-led · headings sparser than ~150 words · ≠ 1 CTA | No |

## Verdict rules
Clean draft → "Recommend approval" (never "approved") · every finding
quotes the failing words, names the check, states what the brief says ·
"For the human" always names the weakest point.

*Fictional classroom material. Cook & Bake Academy does not exist.*
""",
    },
}

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

SUPPORT_FILES = {
    "manual": ("USER-MANUAL.md", "manual"),
    "templates": ("TEMPLATE.md", "template"),
    "scripts": ("CONVERSATION-SCRIPT.md", "script"),
    "references": ("REFERENCE.md", "reference"),
}

ZIP_DATE = (2026, 1, 1, 0, 0, 0)  # fixed timestamp → reproducible zips


def build_skill(skill_dir: Path) -> Path:
    name = skill_dir.name
    content = CONTENT.get(name)
    if content is None:
        raise SystemExit(f"No supporting content defined for skill '{name}'")

    # 1. Write supporting files into the source folder
    for folder, (filename, key) in SUPPORT_FILES.items():
        target = skill_dir / folder / filename
        target.parent.mkdir(exist_ok=True)
        target.write_text(content[key], encoding="utf-8")

    # 2. Rebuild the zip: SKILL.md at root + the four subfolders
    packages_dir = skill_dir.parent / "_packages"
    packages_dir.mkdir(exist_ok=True)
    zip_path = packages_dir / f"{name}.zip"

    entries = [("SKILL.md", skill_dir / "SKILL.md")]
    for folder, (filename, _key) in SUPPORT_FILES.items():
        entries.append((f"{folder}/{filename}", skill_dir / folder / filename))

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname, path in entries:
            info = zipfile.ZipInfo(arcname, date_time=ZIP_DATE)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())

    return zip_path


def main() -> None:
    built = []
    for root in AGENT_ROOTS:
        if not root.is_dir():
            raise SystemExit(f"Missing lab folder: {root}")
        for skill_md in sorted(root.glob("*/skills/*/SKILL.md")):
            built.append(build_skill(skill_md.parent))

    print(f"Built {len(built)} skill packages:")
    for z in built:
        print(f"  {z.relative_to(LABS_ROOT)}  ({z.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
