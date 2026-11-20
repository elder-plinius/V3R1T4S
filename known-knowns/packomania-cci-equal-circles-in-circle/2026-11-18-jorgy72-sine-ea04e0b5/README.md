# Improved circle packing: 4339 equal circles in a circle

## What
polished00.txt's 50-digit feasible radius exceeds the live Packomania value for N=4339 by 1.014393041e-05 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4339 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

In numbers: r* = 0.01428914037842894912706195794112189732227 (50 digits, no tolerance) vs the live Packomania
cci table value 0.014278996448020329132467169733 — a strict improvement of +1.014393041e-05,
1,014,393x the 1e-11 bar. Bank partial win p2 class (gap value N > 2600 with a
lattice-like Specht seed). Gate status: CONFIRMED_PARTIAL (three-skeptic panel, all pass).

## Check it yourself
sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Runs in a few minutes on a laptop (Python standard library
only — decimal module at 50 digits). It also verifies that a corrupted copy of the
object is rejected.

## Compared to
- Table: E. Specht's Packomania, "circles in a circle" (cci),
  https://packomania.com/cci/txt/radius.txt
- Cell: N = 4339, value 0.014278996448020329132467169733, author Eckard Specht
- Table fetched live: 2026-11-18T08:58:42Z and re-verified 2026-11-18T09:17:01Z
  (HTTP 200 both times); value unchanged
- Queue: https://packomania.com/pending-requests.html — cci candidates queued only in
  652–3943 (Vidit Patankar, 15-Oct-2026) and 126–4141 (Karl Desfontaines,
  03-Nov-2026); N=4339 is outside both. No other cci line exists on the live page.
- Posted seed compared against: https://packomania.com/cci/txt/cci4339.txt
  (sha256 baf49c5c256a5afc9794f7e705a24b740a2c1bc3ca62b3c0befbed17d164c3e5);
  sorted pairwise-distance multisets differ (max diff 3.048e-03) — not isometric.

## Not claimed
- No claim about any other N, any other Packomania table, or optimality of this
  configuration (it is a better packing, not a proven optimum; only N ≤ 15–20 are proven).
- No submission has been made to Packomania; the claim is for the verified
  construction only.
- No claim about N=4000: that row is queue-blocked by the Karl Desfontaines
  cci 126–4141 pending line, which is why this run rotated to N=4339.
- The second above-bar file from the same night (polished03, +8.345155687e-06) is a
  separate object, cited not bundled; it is not part of this claim.

## Credits
- E. Specht — the Packomania record table and the posted cci4339.txt seed
  (https://packomania.com/cci/)
- The V3R1T4S open research kit (https://github.com/elder-plinius/V3R1T4S)
- Discovered by the V3R1T4S nightly hunt, credit "Jorgy72 & Sine", 2026-11-18
