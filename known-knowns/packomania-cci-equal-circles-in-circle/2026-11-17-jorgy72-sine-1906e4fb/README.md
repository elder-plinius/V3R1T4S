# Improved circle packing: 4315 equal circles in a circle

## What
object/candidate_n4315.txt's 50-digit feasible radius exceeds the live Packomania value for N=4315 by 1.006294675e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4315 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

In numbers: r* = 0.01432454777069287128759443799585792968662 (50 digits, no tolerance) vs the live Packomania
cci table value 0.014323541476018172725671907488 — a strict improvement of +1.006294675e-06,
100,629x the 1e-11 bar. Bank partial win p2 class (gap value N > 2600 with a
lattice-like Specht seed). Gate status: CONFIRMED_PARTIAL (three-skeptic panel, all pass).

## Check it yourself
sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Runs in a few minutes on a laptop (Python standard library
only — decimal module at 50 digits). It also verifies that a corrupted copy of the
object is rejected.

## Compared to
- Table: E. Specht's Packomania, "circles in a circle" (cci),
  https://packomania.com/cci/txt/radius.txt
- Cell: N = 4315, value 0.014323541476018172725671907488, author Eckard Specht
- Table fetched live: 2026-11-17T08:59:03Z and re-verified 2026-11-17T10:18:26Z
  (HTTP 200 both times); value unchanged
- Queue: https://packomania.com/pending-requests.html — cci candidates queued only in
  652–3943 (Vidit Patankar, 15-Oct-2026) and 126–4141 (Karl Desfontaines,
  03-Nov-2026); N=4315 is outside both. No other cci line exists on the live page.
- Posted seed compared against: https://packomania.com/cci/txt/cci4315.txt
  (sha256 9af86ffc1a5fcc6ba0165682e81f4576e39fe21caa31284b973164aa9f3bccc5);
  sorted pairwise-distance multisets differ (max diff 6.607512e-03) — not isometric.

## Not claimed
- No claim about any other N, any other Packomania table, or optimality of this
  configuration (it is a better packing, not a proven optimum; only N ≤ 15–20 are proven).
- No submission has been made to Packomania; the claim is for the verified
  construction only.
- No claim about N=4000: that row is queue-blocked by the Karl Desfontaines
  cci 126–4141 pending line, which is why this run rotated to N=4315.
- The second above-bar file from the same night (polished01, +9.735e-07) is a
  separate object, cited not bundled; it is not part of this claim.

## Credits
- E. Specht — the Packomania record table and the posted cci4315.txt seed
  (https://packomania.com/cci/)
- The V3R1T4S open research kit (https://github.com/elder-plinius/V3R1T4S)
- Discovered by the V3R1T4S nightly hunt, credit "Jorgy72 & Sine", 2026-11-17
