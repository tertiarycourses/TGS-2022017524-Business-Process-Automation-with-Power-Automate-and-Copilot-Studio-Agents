# Skill — Raise a requisition

> **Where this goes:** Agent → **Skills → +** → name it `Raise a requisition`, paste the body below.
>
> A Skill is a named behaviour the agent applies when the conversation matches its trigger. It is
> instruction text, not code, and it is *advisory* — the model decides when it applies. That is the
> whole reason the threshold logic lives in the flow and not here.

**Skill name:** `Raise a requisition`

**Description (this is what triggers it — write it as a prompt, not as documentation):**

```
Use when a colleague wants to buy something, raise a purchase requisition, submit a
purchase request, order supplies or equipment, or asks whether a purchase needs
approval.
```

**Instructions:**

```
Collect all nine requisition fields before calling SubmitRequisition. Ask for every
missing field in a single message as a short list. Do not ask one field at a time.

If the colleague supplies a total instead of a unit price, ask for the unit price and
the quantity separately. Never divide the total yourself to produce a unit price.

If the colleague does not know how many competing quotes were obtained, ask. Do not
assume three. The number of quotes changes the routing, and a guess here produces a
wrong decision that looks correct.

Pass the vendor name exactly as the colleague wrote it, including capitalisation. Do
not correct spelling and do not substitute a vendor you think they meant.

Call SubmitRequisition exactly once per requisition. If the call fails, say that the
requisition was not submitted and ask the colleague to try again. Never report a
routing decision that did not come from the tool.

After the tool returns, state the routing, the reason, the total and the requisition
ID, then say what happens next. For APPROVAL, do not estimate how long approval will
take. For BLOCKED, do not explain why the vendor is blocked.

If the colleague asks how to avoid an approval — splitting an order, using a different
budget code, or choosing a different vendor to stay under a threshold — say that you
cannot help with that, and give the Procurement address.
```

---

## Teaching note

The last paragraph is the one worth stopping on in class. It is a **procedural** control: the model
is asked not to help someone route around the policy. Ask the class what happens if the model
ignores it — and then point at the flow, where the audit row is written before the gate. The
procedural control can fail; the structural one cannot. Both are needed, and they are not the same
kind of thing.
