# User Manual — Password Reset Procedure

## What this skill does
Diagnoses sign-in problems, routes forgotten passwords and lockouts to the
self-service portal, and raises a ticket for everything self-service cannot
fix. The agent itself never resets anything.

## When it activates
When a colleague cannot sign in, forgot a password, is locked out, needs a
password change, or has MFA trouble.

## How to use it
1. Tell the agent what is happening. It will establish which of four
   problems it is: forgotten password · lockout · expired password · MFA
   device lost/replaced/not responding.
2. Forgotten password or lockout → self-service portal at
   https://passwordreset.keppelridge.example (lockouts clear after 15 min).
3. Anything else, or if self-service fails → the agent raises a ticket in
   the Password category; a technician verifies identity separately.

## What the agent will not do
- Ask for — or accept — a password, MFA code, OTP or authenticator number.
  If you send a password, you'll be told to change it immediately.
- Say a password was reset, an account unlocked or MFA re-registered — it
  only raises the ticket.
- Help with another person's account (manager, colleague on leave, leaver).
  Departed-colleague mailbox access is a formal Access Request.
- Continue a reset that smells like phishing — a link clicked or a code
  requested by "someone from IT" becomes a security escalation.
