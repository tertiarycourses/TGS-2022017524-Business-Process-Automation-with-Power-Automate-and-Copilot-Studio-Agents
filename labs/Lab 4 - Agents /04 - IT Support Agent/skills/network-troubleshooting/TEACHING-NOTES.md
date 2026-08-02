# Teaching notes — Network Troubleshooting

> Trainer notes. Kept out of `SKILL.md` on purpose.

**Where this goes:** `IT Support Agent` → **Build → Skills → Add skill → Upload a skill**, then
drop [`network-troubleshooting.zip`](../_packages/network-troubleshooting.zip) onto the upload box.

---

## Check the outage before the device

The ordering is the lesson. The instinct — the agent's and the learner's — is to start
troubleshooting immediately, because that feels like helping.

If there is an open network incident, every minute of that troubleshooting is wasted, and the ticket
it generates makes the incident **look larger and more diffuse** than it is. Twenty duplicate tickets
from one switch failure is worse than twenty colleagues told "we know, reference INC-0142".

> **The general shape: check whether the problem is already known before treating it as new.** It
> applies to every support agent, and an agent optimised to be helpful in each individual
> conversation will get it wrong, because the cost lands on someone else — the incident manager
> looking at a pile of tickets.

## Test cases

| # | Say | Expected |
|---|---|---|
| 1 | "Internet's not working" | Asks scope questions **before** steps |
| 2 | "Nobody on level 3 has Wi-Fi" | Escalates. **No device troubleshooting** |
| 3 | "VPN won't connect from home" | VPN sign-out/in, one step at a time |
| 4 | "Shared drive is slow" (matches an open incident) | Names the known issue, gives the reference, stops |
| 5 | "Can I use my phone hotspot instead?" | **No.** Corporate connection |
| 6 | "Should I change my DNS to 8.8.8.8?" | Declines. Raises a ticket |
