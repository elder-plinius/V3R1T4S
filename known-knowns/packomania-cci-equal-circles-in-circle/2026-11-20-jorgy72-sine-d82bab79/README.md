# Improved circle packing: 4357 equal circles in a circle

## What
polished01.txt's 50-digit feasible radius exceeds the live Packomania value for N=4357 by 4.93845300182e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4357 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

In numbers: r* = 0.01426010900644796452099252854564 (50 digits, no tolerance) vs the live Packomania
cci table value 0.014255170553446144330034824715 — a strict improvement of +4.93845300182e-06,
493,845x the 1e-11 bar. Bank partial win p2 class (gap value N > 2600 with a
lattice-like Specht seed). Gate status: CONFIRMED_PARTIAL (three-skeptic panel, all pass).

## Check it yourself
sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Runs in a few minutes on a laptop (Python standard library
only — decimal module at 50 digits). It also verifies that a corrupted copy of the
object is rejected.

## Compared to
- Table: E. Specht's Packomania, "circles in a circle" (cci),
  https://packomania.com/cci/txt/radius.txt
- Cell: N = 4357, value 0.014255170553446144330034824715, author Eckard Specht
- Table fetched live: 2026-11-20T08:58:00Z and re-verified 2026-11-20T09:21:30Z
  (HTTP 200 both times); value unchanged
- Queue: https://packomania.com/pending-requests.html — cci candidates queued only in
  652–3943 (Vidit Patankar, 15-Oct-2026) and 126–4141 (Karl Desfontaines,
  03-Nov-2026); N=4357 is outside both. No other cci line exists on the live page.
- Posted seed compared against: https://packomania.com/cci/txt/cci4357.txt
  (sha256 778c91a9e89b42372303330e2d3faf7a8bea563cb402da399cd893d1d13da959);
  sorted pairwise-distance multisets differ (max diff 3.765e-03) — not isometric.

## Not claimed
- No claim about any other N, any other Packomania table, or optimality of this
  configuration (it is a better packing, not a proven optimum; only N ≤ 15–20 are proven).
- No submission has been made to Packomania; the claim is for the verified
  construction only.
- No claim about N=4000: that row is queue-blocked by the Karl Desfontaines
  cci 126–4141 pending line, which is why this run rotated to N=4357.
- No second above-bar file this night: the next-best polish (polished00,
  -2.348e-07) is below the bar and is cited as work history, not bundled.

## Credits
- E. Specht — the Packomania record table and the posted cci4357.txt seed
  (https://packomania.com/cci/)
- The V3R1T4S open research kit (https://github.com/elder-plinius/V3R1T4S)
- Discovered by the V3R1T4S nightly hunt, credit "Jorgy72 & Sine", 2026-11-20
