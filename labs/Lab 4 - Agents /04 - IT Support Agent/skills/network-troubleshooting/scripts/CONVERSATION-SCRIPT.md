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
