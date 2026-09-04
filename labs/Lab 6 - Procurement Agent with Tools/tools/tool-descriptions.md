# Tools — Procurement Agent

> **Where this goes:** Agent → **Tools → + Add a tool** → **Flow** → pick the published flow.
>
> The **tool description is not documentation — it is a prompt.** It is the single most common
> reason a tool-based agent misbehaves. Too vague and the agent never calls it; too narrow and it
> only fires on the exact words in the description.
>
> The label shifts between tenant versions — *Add a tool* or *Add an action*. Screenshot what you
> actually see before writing it into a build sheet.

---

## Tool 1 — `SubmitRequisition`

**Source:** the published agent flow `Lab 6 - Procurement Requisition Approval`
(built in [BUILD-THE-FLOW.md](../BUILD-THE-FLOW.md)).

**Description:**

```
Assess a purchase requisition against Keppel Ridge procurement policy. Call this
whenever a colleague wants to raise, submit or check a purchase request, order
supplies or equipment, or asks whether a purchase needs approval. Returns the
routing decision (AUTO, APPROVAL, RETURNED or BLOCKED) and the reason. Collect
every input before calling: requester, department, vendor, item description, unit
price, quantity, number of competing quotes, budget code and needed-by date.
```

**Inputs** — the tool contract, declared on the flow's *When an agent calls the workflow* trigger:

| Input | Type | Note |
|---|---|---|
| `requester` | Text | |
| `department` | Text | |
| `vendor` | Text | Pass as written — do not normalise here |
| `itemDescription` | Text | |
| `unitPrice` | Number | SGD per unit |
| `quantity` | Number | |
| `competingQuotes` | Number | |
| `budgetCode` | Text | e.g. `EN-2041` |
| `neededBy` | **Text** | Keep as Text, not Date — see below |

> **Keep `neededBy` as Text.** A Date input makes the calling agent responsible for producing a
> valid ISO date from whatever the colleague typed ("end of the month"), and it will sometimes fail
> the type check rather than ask. Text accepts it, and nothing downstream does date arithmetic.

**Outputs** returned to the agent: `routing`, `reason`, `requisitionTotal`, `requisitionId`.

> `policyFlags` is deliberately **not** returned. See [`../skills/vendor-enquiry/SKILL.md`](../skills/vendor-enquiry/SKILL.md).

---

## Tool 2 — `CheckVendor`

**Source:** a second, much smaller agent flow. Build it as:

```
When an agent calls the workflow   (input: vendorName, Text)
  → Get items (SharePoint, ApprovedVendors, Top Count 1)
  → Respond to the agent
```

**Filter Query** — type the literal text and insert only the value with the **⚡ picker**:

```
VendorName eq '<⚡ trim(vendorName) token>'
```

> ⚠️ **Do not use `concat()`.** `concat('VendorName eq ''', ..., '''')` validates green in the
> editor and then fails at run time with *"Creating query failed"*. Verified on a live tenant.

**Respond to the agent** outputs:

| Output | Expression |
|---|---|
| `found` | `greater(length(body('Get_items')?['value']), 0)` |
| `status` | `first(body('Get_items')?['value'])?['Status']?['Value']` |
| `category` | `first(body('Get_items')?['value'])?['Category']?['Value']` |

> `Status` and `Category` are SharePoint **Choice** columns, so the value is nested under `Value`.
> Reading `?['Status']` directly returns an object and the comparison silently never matches.

**Description:**

```
Look up a supplier in the Keppel Ridge approved-vendor register. Call this whenever a
colleague asks whether a vendor can be used, whether a supplier is approved, what a
vendor is approved to supply, or who to buy a category of item from. Returns whether
the vendor is on the register, their status and their approved category.
```

---

## Turn off "Search all websites"

The Knowledge panel ships with a **Search all websites** chip enabled. Click its **✕**.

A procurement agent with open-web access will answer "what does a workstation cost" from a
shopping site, in the same confident voice it uses for policy. The learner sees one reply and
cannot tell which sentence came from the register and which came from the internet.
