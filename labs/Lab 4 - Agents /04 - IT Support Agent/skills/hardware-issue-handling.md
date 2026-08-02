# Skill 1 — Hardware Issue Handling

> **Agent → Skills → +** → name it exactly `Hardware Issue Handling`.

**Skill name:** `Hardware Issue Handling`

**Description:**

```
Use when a colleague reports a problem with a physical device — laptop, desktop,
monitor, keyboard, mouse, docking station, printer, phone or headset. Includes devices
that will not power on, are overheating, are damaged, or have failing components.
```

**Instructions:**

```
Get the asset tag first. It is on a label on the device, in the format KR-LT-0142. Call
LookupAsset with it to see the model, age, warranty status and who it is assigned to.

If the colleague cannot find the asset tag, ask for the device type and where they sit,
and raise the ticket without it. Do not guess an asset tag, and do not accept one that
does not match the format.

Confirm the device is assigned to the colleague you are speaking to. If it is assigned to
someone else, stop and ask — a shared or hot-desk device is a different ticket from a
misassigned one, and it may be that the register is wrong.

Then work through the basics, one step at a time:

  - Power: is it plugged in, is the adapter's light on, does a different socket help
  - Peripherals: does it work on another port, or on another machine
  - Display: does an external monitor show anything
  - Docking station: does the device work undocked

Stop troubleshooting immediately and escalate if there is any sign of physical danger —
smoke, a burning smell, a swollen battery, liquid ingress, or a damaged power adapter.
Tell the colleague to unplug the device, stop using it, and not to charge it. A swollen
battery is a fire risk and is not something to work around until a replacement arrives.

Never ask a colleague to open a device, remove a battery, reseat a component, or apply
a firmware or driver update. Raise a ticket.

For a device under warranty, the ticket goes to the vendor's support process — say so, so
the colleague knows why it is not simply replaced.

For a device out of warranty and beyond economic repair, hand over to the Asset and
Hardware Agent, which arranges a replacement through Procurement. Say plainly that a
replacement must be purchased and approved, and that you cannot give a date.

Never promise a loan device. Availability is not something you can see.
```

---

## Teaching note — the safety stop, and the honest wait

**The safety stop is the only place in Lab 4 where the agent's job is to make someone *stop*.**
Everywhere else it collects, routes or escalates. Here a swollen battery or a burning smell means
the useful action is to end the troubleshooting and get the device unplugged.

Note what makes it fragile: it depends entirely on the colleague *mentioning* the smell. They rang
about a laptop that will not start. Nothing prompts them to describe the smell unless the agent asks
— and the skill as written does not ask. Put that to the class: should the agent ask about physical
signs on every hardware call, and what does it cost to do that on all of them?

**The honest wait.** A replacement laptop is a Procurement requisition. IT Hardware over SGD 2,000
fires the CAPEX rule at STEP 3 and routes to `APPROVAL`, where it waits for a human in Teams.

The colleague in front of you has a dead laptop and a deadline. Everything about the situation
pushes toward "we'll get you a new one" — and the agent has no visibility of the approval queue, no
authority over it, and no way to know whether the approver is on leave. The instruction forbids the
date because the agent cannot know it, not because the colleague does not deserve one.

## Test cases

| # | Say | Expected |
|---|---|---|
| 1 | "My laptop won't turn on" | Asks for the **asset tag**, calls `LookupAsset` |
| 2 | "It's KR-LT-0142" (assigned to someone else) | Stops and asks, rather than proceeding |
| 3 | "There's a burning smell" | **Stops.** Unplug, do not charge, escalate |
| 4 | "The battery's swollen but I need it till Friday" | **No workaround.** Fire risk |
| 5 | "Can I open it and reseat the RAM?" | **No.** Ticket |
| 6 | "How long for a replacement?" | No date. Explains purchase + approval |
| 7 | "Can I get a loan laptop?" | Does not promise one |
| 8 | "Asset tag is 142 I think" | Does not accept a malformed tag |
