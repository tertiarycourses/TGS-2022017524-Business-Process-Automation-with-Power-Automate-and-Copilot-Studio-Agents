# Conversation Script — Hardware Issues

## Script 1 — standard fault
> My laptop KR-LT-0142 won't power on.

**Expected:** LookupAsset called with the tag; assignment confirmed; basics
one step at a time (plugged in → adapter light → different socket).

## Script 2 — no asset tag
> There's no sticker on my monitor.

**Expected:** device type + desk location collected; ticket raised without
a tag; no guessed tag accepted.

## Script 3 — safety stop
> The battery looks swollen and the case is bulging.

**Expected:** troubleshooting stops immediately — unplug, stop using, do
not charge — and the agent escalates.

## Script 4 — assigned to someone else
> The register says this laptop is Daniel's, but I use it now.

**Expected:** the agent stops and asks — shared device, hot-desk, or a
wrong register entry are different tickets.

## Script 5 — beyond repair
> It's five years old and the repair quote is more than a new one.

**Expected:** handover to the Asset and Hardware Agent; plain statement
that a replacement must be purchased and approved, with no date promised.
