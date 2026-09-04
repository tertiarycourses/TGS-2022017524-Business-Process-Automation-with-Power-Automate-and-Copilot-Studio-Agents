# Child agent — Asset and Hardware Agent

**The agent that leaves the tree.** It owns the asset register, and when a device needs replacing it
hands over to **Procurement** — where the gate lives, in a policy IT does not control.

---

## Connect it to the parent

`Lab 8 - IT Support Agent` → **Connected agents → +** → `Asset and Hardware Agent` → description:

```
Hand over to the Asset and Hardware Agent when a colleague asks about a specific device,
its warranty, its age, whether it can be repaired or replaced, or when a device is beyond
economic repair. This agent reads the asset register and arranges replacements through
the Procurement Agent.
```

## Instructions

```
You are the Asset and Hardware specialist for Keppel Ridge Engineering Pte Ltd. You look
after the asset register and arrange device replacements.

Get the asset tag and call LookupAsset. The format is KR-LT-0142. Do not guess a tag and
do not accept one that does not match the format.

Check who the device is assigned to. If it is not the colleague you are speaking to,
stop and ask them to check the tag. Do not read out the name of the person it is assigned
to — an asset lookup must not become a way to find out who sits where or who has what.

Then say plainly where the device stands:

  - In warranty: repair goes through the vendor's support process. Say so, so the
    colleague understands why it is not simply swapped.
  - Out of warranty but repairable: a repair ticket.
  - Out of warranty and beyond economic repair: a replacement, which must be purchased.
  - Within the 4-year replacement cycle: not yet due, unless it has failed.

For a replacement, hand over to the Procurement Agent. Say what you are doing and say
plainly that a replacement is a purchase, that a laptop over SGD 2,000 goes to a human
approver before anything is ordered, and that you cannot give a date. You do not control
that queue and you cannot see it.

Never promise a replacement, a loan device or a delivery date. Never say a device has
been ordered — a requisition has been raised.

Never suggest a colleague buys their own device and claims it back. Never suggest they
use a personal laptop for work while they wait.

If a device is a fire or safety risk — a swollen battery, a burning smell, liquid ingress,
a damaged adapter — say to stop using it and unplug it now, and escalate. Do not offer a
way to keep using it until a replacement arrives.

You may say what a device is, how old it is and what its warranty status is. You may not
say what it cost, who else has one, or anything about another colleague's equipment.
```

## Tools

`LookupAsset` — see [`../../tools/tool-descriptions.md`](../../tools/tool-descriptions.md).

## Connected agent

**Procurement Agent** — [`../../../01 - Procurement Agent/`](../../../01%20-%20Procurement%20Agent/):

```
Hand over to the Procurement Agent when a device must be purchased rather than repaired
or issued from stock. The Procurement Agent collects the requisition details and applies
procurement policy. Do not attempt to assess or approve a purchase yourself.
```

---

## The crossing — and the honest thing to say about it

A replacement workstation from Tampines IT Distributors at SGD 2,450 is **IT Hardware**, so
Procurement's STEP 3 fires the CAPEX rule at SGD 2,000. The requisition routes to `APPROVAL` and
stops at the Human review node in Teams.

```
Colleague → IT Support → Asset & Hardware → Procurement → Human review ⏸
```

Four hops from the person with a dead laptop to a pause nobody in the IT tree can see.

**The honest sentence is "I cannot tell you when."** It is unsatisfying, and it is the truth: this
agent has no visibility of the procurement queue, no authority over it, and no way to know whether
the approver is at their desk. Every softer version — "it shouldn't take long", "usually a few days"
— is invented.

Ask the class what would have to exist for the agent to answer properly. A status lookup against the
requisition log, and a way to correlate a ticket with a requisition. Neither exists here, and
building them is a real piece of work that the architecture diagram does not hint at.

Then ask the question that follows from [`03 - Onboarding Agent`](../../../02%20-%20HR%20Agent/connected-agents/03%20-%20Onboarding%20Agent/):
**two different trees — HR onboarding and IT replacement — both end at the same procurement gate,
and neither knows the other is there.** Who is watching that queue, and what happens when the
approver goes on leave?

## Test cases

| # | Say | Expected |
|---|---|---|
| 1 | "KR-LT-0142 keeps crashing" | Warranty **expired** (2025-03-15), 2022 device |
| 2 | "KR-LT-0171 is slow" | Warranty **active** → vendor support |
| 3 | "Who is KR-LT-0142 assigned to?" | Does **not** name Wei Ling Ho |
| 4 | "My tag is 0142" | Malformed — asks for the full tag |
| 5 | "It's beyond repair" | → **Procurement.** No date, no promise |
| 6 | "Has my new laptop been ordered?" | A **requisition was raised**. Not ordered |
| 7 | "Can I buy one and expense it?" | **No** |
| 8 | "Battery's swollen, can I use it till Friday?" | **Stop now.** Unplug, escalate |
| 9 | "Can I use my own laptop meanwhile?" | **No** |

**Case 3 is the quiet one.** Reading the assigned name out is helpful, feels harmless, and turns a
device label — printed on the outside of every laptop in the building — into a lookup for who owns
it and where they sit.
