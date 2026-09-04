# Connected agents — Procurement Agent

Procurement is the one agent in this lab with **no child agents**. It is a *leaf*: it does one job,
against one register, behind one gate.

It is, however, **connected to by two others** — and that direction is the interesting one.

```
   IT Support Agent  ──────┐
                           ├──► Procurement Agent ──► SubmitRequisition (flow)
   Sales Agent      ───────┘                            └─► Human review (Teams)
```

| Parent | Why it connects | What it hands over |
|---|---|---|
| **IT Support Agent** | A hardware replacement is a purchase, not a ticket | Requester, department, the item, the ticket reference |
| **Sales Agent** | A quote that needs a bought-in component | Requester, department, the component, the opportunity reference |

---

## Wiring it (from the parent's side)

You connect agents from the **parent**, not from Procurement. In `Lab 8 - IT Support Agent`:

**Agent → Connected agents → + → Procurement Agent**, then give it a description:

```
Hand over to the Procurement Agent when a colleague needs to buy hardware,
equipment, software licences or any item that must be purchased rather than
issued from stock. The Procurement Agent collects the requisition details and
applies procurement policy. Do not attempt to assess or approve a purchase
yourself.
```

Procurement needs no configuration to *receive* a handover. That asymmetry is worth stating in
class: a connected agent is discovered and invoked by its parent, and it does not know or care how
many parents it has.

---

## What actually crosses the boundary — and what does not

When IT Support hands over, **the conversation moves**; the child does not inherit the parent's
tools, knowledge or skills. Procurement re-collects what it needs.

That feels wasteful and it is the correct behaviour. Ask the class why:

- IT Support's knowledge includes internal ticket notes. Those have no business inside a
  procurement decision, and a shared context would carry them there by default.
- Procurement's rules must apply identically no matter who called it. An agent that inherited the
  caller's framing ("this is urgent, the user's laptop is dead") would be reasoning about the
  requisition using material the policy never mentions.

**A boundary between agents is a boundary between what each is allowed to know.** That is the
argument for splitting one large agent into several, and it is a stronger argument than "the
instructions were getting long".

---

## The consequence nobody sees on the diagram

A requisition that routes to `APPROVAL` stops at the Human review node, and the flow's
*Respond to the agent* node sits after it. So the calling agent waits — and now that call may have
originated **two agents up**, in an IT Support conversation about a broken laptop.

For this lab, accept it and watch it happen. In production you would split the flow in two: one
that returns "submitted for approval" immediately, and a second triggered on the approval outcome.

Ask the class what you lose when you do that, and **who now has to track that the second half ever
ran.** Nobody owns that by default, which is how it goes unnoticed.
