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
