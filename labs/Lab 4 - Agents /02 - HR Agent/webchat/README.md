# HR landing page — the HR Agent on a web page, via the Microsoft 365 Agents SDK

**What this adds:** a channel of your own. Teams gave the HR Agent to colleagues inside Microsoft's
walls; this part puts the same agent on an HR intranet landing page, as a chat widget in the corner
— the shape every "chat with HR" button on a real intranet has.

**The lesson is identity, not web design.** The page uses the
[Microsoft 365 Agents SDK](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/) Copilot
Studio client, and the person in the widget is the **signed-in Microsoft Entra user** — the same
identity Teams provides. "How much annual leave do I have left?" answers for *them*. That is the
whole reason this lab does not use the copy-paste iframe embed.

**Time:** 30–40 minutes.

---

## Three ways to put an agent on a web page — and why HR gets only one

| Method | Who is the user? | Set-up | Fit for the HR Agent |
|---|---|---|---|
| **Embed code (iframe)** | Anonymous. Requires the agent's Security → Authentication set to **No authentication** | Paste one `<iframe>` | **No.** An HR agent that reads leave records cannot be anonymous and public — and switching it to No authentication to get the embed code removes the identity every rule in this agent depends on |
| **Agents SDK Copilot Studio client** — *this lab* | The **signed-in Entra user**, via MSAL | An app registration + a few settings | **Yes.** Same identity story as Teams, on your own page |
| **Direct Line API** | Whatever you build | The most code | Only when the SDK doesn't cover the scenario |

This is the same table Copilot Studio itself implies: with **Authenticate with Microsoft** selected
(the default, and correct for HR), the Web channel offers **no embed code** — only the Agents SDK
connection settings. The product is telling you which method fits an authenticated agent.

> **The parent-only rule still applies.** You connect this page to the **HR Agent** parent — its
> schema name, nobody else's. Pointing the widget at a child's schema name is the same governance
> hole as deploying a child to Teams: a door past the parent's routing and refusals.

---

## Folder contents

| Path | What it is |
|---|---|
| [`web/index.html`](web/index.html) | The Keppel Ridge People & Culture landing page, with the chat widget |
| [`web/index.css`](web/index.css) | Page and widget styling |
| [`web/index.js`](web/index.js) | Opens the widget, signs the user in, connects the Copilot Studio client to Web Chat |
| [`web/acquireToken.js`](web/acquireToken.js) | MSAL token acquisition (silent first, popup fallback) — from the Microsoft sample, unmodified |
| [`web/settings.TEMPLATE.js`](web/settings.TEMPLATE.js) | Copy to `settings.js` and fill in — `settings.js` is gitignored |

Based on the official
[`copilotstudio-webclient`](https://github.com/microsoft/Agents/tree/main/samples/nodejs/copilotstudio-webclient)
sample from the Agents SDK repo. No build step, no Node server — three CDN scripts
(Bot Framework Web Chat, MSAL Browser, and the `@microsoft/agents-copilotstudio-client` browser
module) and static files.

## Prerequisites

- The **HR Agent is built and Published** — parent and children, per the
  [main HR Agent lab](../README.md). Re-check ⋯ → **Version history**: `LIVE` and `CURRENT DRAFT`
  match.
- Access to the **Microsoft Entra admin center** ([entra.microsoft.com](https://entra.microsoft.com))
  to create an app registration in the *same tenant* as the agent.
- Any static web server. **VS Code Live Server** (used below) or
  `python3 -m http.server 5500` both work.

> **Unlike Lab 7's page, this one cannot be double-clicked open.** Lab 7 worked from `file://`
> because it was a plain fetch to a CORS-open endpoint. This page signs a user in, and MSAL needs a
> real `http://localhost` origin that exactly matches the app registration's redirect URI.
> Serve it; don't open the file.

---

## Part 1 — Register the web app in Entra (one per class tenant, ~10 min)

1. [Entra admin center](https://entra.microsoft.com) → **Identity → Applications →
   App registrations → New registration**.
2. Name: `HR Agent Web Client`. Supported account types: **Accounts in this organizational
   directory only**.
3. Under **Redirect URI**, choose platform **Single-page application (SPA)** and enter
   `http://localhost:5500` — the Live Server default. (Serving on another port later? Add that
   origin here too. The URI must match the page's origin **exactly**.)
4. **Register**, then from **Overview** record the **Application (client) ID** and the
   **Directory (tenant) ID**.
5. **API permissions → Add a permission → APIs my organization uses** → search
   `Power Platform API`. If nothing appears, search by its ID:
   `8578e004-a5c6-46e7-913e-12f58912df43`.
6. **Delegated permissions → CopilotStudio → CopilotStudio.Copilots.Invoke → Add permissions**.
7. Optionally **Grant admin consent**. Without it, each learner consents individually in the
   sign-in popup — which is fine for class, and worth seeing once: the consent screen names
   exactly what the page may do on the user's behalf, and *invoke a Copilot Studio agent* is all
   of it.

> **Delegated, not application.** The page never holds a credential of its own — no secret, no
> certificate, nothing to leak in the repo. It borrows the signed-in user's identity, scoped to one
> permission. That is why `settings.js` contains IDs but no secrets, and why the Agents SDK path
> notes that service-principal tokens are not supported here: this channel is *built* to be the
> user.

## Part 2 — Get the agent's coordinates from Copilot Studio (~3 min)

Copilot Studio → **HR Agent** → **Settings → Advanced**. Under **Metadata**, record:

| Value | Goes into |
|---|---|
| **Environment ID** | `environmentId` |
| **Schema name** | `schemaName` |
| **Tenant ID** | `tenantId` (should match the app registration's) |

Also confirm **Settings → Security → Authentication** is **Authenticate with Microsoft** — the
default. You do *not* need to change anything; this lab exists because that setting is right.

*(Alternative: **Channels → Web app** shows a **Microsoft 365 Agents SDK connection string**. Paste
it as `directConnectUrl` instead of `environmentId` + `schemaName`. Either works; the metadata
route shows learners what the connection string encodes.)*

## Part 3 — Configure the page (~2 min)

In [`web/`](web/): copy `settings.TEMPLATE.js` to `settings.js`, fill in the four values from
Parts 1–2, save. Leave `directConnectUrl`, `cloud` and the rest empty.

## Part 4 — Serve, sign in, test (~10 min)

1. In VS Code, right-click `web/index.html` → **Open with Live Server**
   (or `python3 -m http.server 5500` from the `web/` folder).
2. Open **`http://localhost:5500`** — `localhost`, not `127.0.0.1`; the origin must match the
   redirect URI character for character.
3. Click the **chat bubble** bottom-right. First open triggers the sign-in popup — allow popups
   for the site. Sign in as a tenant user.
4. The widget header confirms who you are talking to; the status line walks through
   *Signing you in… → Connecting to the HR Agent…* and then the conversation starts.

> The sign-in deliberately happens on the **first click of the launcher**, not on page load. A
> popup opened without a user gesture is eaten by the popup blocker, and the failure looks like
> "the widget does nothing".

### Test from the page

| # | Type into the widget | Expect |
|---|---|---|
| 1 | `How much annual leave do I have left?` | **The signed-in user's** balance, with the as-at date — same as the Teams test, and the point of the whole lab |
| 2 | `Can I work from home two days a week?` | Handover to **Policy and Benefits**, answer from the handbook, no invented policy |
| 3 | `Is my leave application approved yet?` | Status only — never a prediction of the manager's decision |
| 4 | `How did the candidates for the Site Engineer role score?` | Routed to Screening **for recruiters** — the parent does not read out screening results to whoever asks |
| 5 | Ask question 1 in a **private/incognito window signed in as a different user** | The *other* user's balance. One page, two people, two answers — identity is doing the work |

Test 5 is the demonstration to run in class. On the no-auth iframe there is no equivalent — every
visitor is the same anonymous nobody, which for an HR agent is precisely the problem.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Widget says `settings.js not found` | You haven't copied `settings.TEMPLATE.js` to `settings.js` in `web/` |
| Sign-in popup never appears | Popup blocker — allow popups for `localhost:5500`, close and reopen the chat |
| `AADSTS50011` (redirect URI mismatch) | The page's origin isn't registered — add it under the app registration's **SPA** platform, exactly as the browser shows it |
| `AADSTS65001` / consent screen loops | `CopilotStudio.Copilots.Invoke` not added, or added under the wrong API — it must be **Power Platform API, delegated** |
| `AADSTS700016` | `appClientId` doesn't exist in `tenantId`'s directory — app registered in a different tenant than the agent |
| Sign-in succeeds, then 403/404 on connect | Wrong `environmentId` or `schemaName`, or the agent isn't **Published** — re-check Settings → Advanced → Metadata and Version history |
| Connects but answers like a stranger ("I can't see your records") | Signed in with an account that has no row in `staff-leave.csv` — the flow's lookup found nothing. Same unnormalised-lookup family as the four traps in the [main lab](../../README.md) |
| Worked yesterday, blank today | You edited the agent and didn't re-publish — this channel serves the **published** version, exactly like Teams |
| Chat renders but replies carry `[1]`-style markers | The "never include citation markers" line is missing from a child's instructions — the web page renders them verbatim, more visibly than Teams |

---

## What this deployment gives you — and what it does not

**You now control the surface.** The page decides what sits around the conversation: the widget
hides Web Chat's file-upload button (`hideUploadButton: true`) because no HR flow here accepts a
file — a control the model cannot override, in the same family as *a tool the agent does not have*.

**You do not control retention.** The conversation still runs through Copilot Studio and is
retained under the tenant's policy, exactly as with Teams. Moving the front end onto your page
moves none of that.

**The identity is real; the audience is now yours to police.** Teams put the agent behind a
corporate login by default. A web page goes wherever its URL goes — what keeps a non-employee out
is the Entra sign-in and nothing else. If someone proposes "just make it No authentication so
customers can use it too", the answer is that this agent reads leave records, and the correct
response to that request is a *different agent* — which is the Sales Agent's story, one folder
over.

**Nothing about the agent changed.** Same parent, same children, same refusals, same flows, same
approval gates arriving in the Teams Approvals app. A channel is a door, not a brain — the third
door so far (Test pane, Teams, now the web), and the agent behaved identically at each. That
consistency is what publishing gives you, and why every change still ends with *re-publish, then
re-test*.
