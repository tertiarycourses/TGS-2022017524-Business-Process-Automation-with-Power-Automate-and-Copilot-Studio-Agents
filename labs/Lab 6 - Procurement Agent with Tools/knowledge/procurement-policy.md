# Keppel Ridge Engineering Pte Ltd — Procurement Policy (extract)

> **Fictional classroom document.** Keppel Ridge Engineering Pte Ltd does not exist. No real
> company, vendor, person or contract is described here. Upload this file to the agent's
> **Knowledge** so it can explain the policy in plain language when a colleague asks.
>
> **This file does not make the routing decision.** The decision is made by the agent flow, from
> [`../agent/instructions.md`](../agent/instructions.md). This is the *explanatory* copy. If you
> change a threshold, change it in both places — and expect the class to ask which one wins. The
> flow wins, because that is the one that runs.

**Document:** PRO-POL-004 · **Version:** 3.1 · **Effective:** 1 January 2026
**Owner:** Procurement, Keppel Ridge Engineering Pte Ltd

---

## 1. Purpose

This policy governs how purchase requisitions raised by staff are routed for release, approval or
return. It applies to all purchases of goods and services regardless of value.

## 2. The approved-vendor register

Keppel Ridge maintains a register of vendors that have passed commercial and quality due diligence.
Every vendor on the register carries one of three statuses:

| Status | Meaning |
|---|---|
| **Approved** | May be purchased from. |
| **Suspended** | May not be purchased from. An existing contract may remain in force; new requisitions are blocked. |
| **Under Review** | Due diligence is in progress. Purchases may proceed only with approval, regardless of value. |

A vendor that does not appear on the register at all has not been assessed and may not be
purchased from. Being absent is not the same as being suspended, and neither is a judgement about
the vendor's quality.

> **Registered is not the same as approved.** This is the distinction staff most often miss. A
> vendor you have a signed master agreement with may still be a vendor you cannot buy from this
> week.

## 3. Categories

| Class | Categories |
|---|---|
| **Capital expenditure** | IT Hardware, Machinery, Vehicles, Facilities |
| **Consumable** | Stationery, PPE, Consumables, Software Subscription |

## 4. Routing rules

Rules are evaluated **in order**. The first rule that applies determines the routing, and no later
rule is considered.

| Step | Condition | Routing | Flag |
|---|---|---|---|
| 1 | Vendor not on the register | `BLOCKED` | `UNAPPROVED_VENDOR` |
| 1 | Vendor status is Suspended | `BLOCKED` | `VENDOR_SUSPENDED` |
| 1 | Vendor status is Under Review | `APPROVAL` | `VENDOR_UNDER_REVIEW` |
| 2 | Fewer than 3 competing quotes **and** total ≥ SGD 5,000 | `APPROVAL` | `SINGLE_SOURCE` |
| 3 | Capital expenditure **and** total ≥ SGD 2,000 | `APPROVAL` | `CAPEX` |
| 4 | Total ≥ SGD 10,000 | `APPROVAL` | `ABOVE_THRESHOLD` |
| 5 | Budget code missing or malformed | `RETURNED` | `INVALID_BUDGET_CODE` |
| 6 | None of the above | `AUTO` | — |

The requisition total is unit price × quantity. A total supplied on the requisition is not relied
upon.

Budget codes are two uppercase letters, a hyphen, then exactly four digits — for example `EN-2041`.

Thresholds are inclusive. SGD 10,000.00 is *at* the threshold and requires approval. SGD 9,999.99
does not.

## 5. Two consequences of the ordering that staff should understand

**A cheap requisition can require approval.** A SGD 900 order against a vendor under review must
reach a human; a SGD 1,900 single-quote order need not. Amount is not the only reason a purchase
stops.

**`ABOVE_THRESHOLD` cannot fire for a capital-expenditure vendor.** Step 3 catches capex at SGD
2,000, so a Machinery or IT Hardware requisition has already stopped before it reaches SGD 10,000.
Either way the requisition reaches a human, so the routing is correct — but the *flag* is what an
auditor reads six months later, and "held because it was capital expenditure" is a different claim
from "held because it was large".

## 6. Splitting

Dividing a purchase into smaller requisitions to remain below a threshold is a breach of this
policy. Requisitions that appear to have been split are reviewed by Procurement regardless of
individual value.

## 7. Escalation

Questions about vendor status, blocked requisitions or exceptions to this policy go to Procurement
at procurement@keppelridge.example. Neither the requester nor any automated assistant may grant an
exception.

## 8. Record keeping

Every requisition assessed under this policy is written to the requisition log at the point of
assessment — before any approval is sought and irrespective of the outcome. Requisitions that are
blocked or returned are logged in the same way as those released.

> This is what makes it possible to ask, a year later, whether anything was released that nobody
> reviewed. A log written after the approval could not answer that question, because the cases you
> most want to find would be the ones missing from it.
