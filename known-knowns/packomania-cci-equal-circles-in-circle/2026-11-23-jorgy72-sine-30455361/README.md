# Improved circle packing: 4405 equal circles in a circle

## What
polished01.txt's 50-digit feasible radius exceeds the live Packomania value for N=4405 by 3.607323049e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4405 outside the live queued cci ranges and absent from history updates newer than 22-Nov-2026.

In numbers: r* = 0.014193819376049377319011472067507150119907818321175 (50 digits, no tolerance) vs the live Packomania
cci table value 0.014190212053 — a strict improvement of +3.607323049e-06,
360,732x the 1e-11 bar. Bank partial win p2 class (gap value N > 2600 with a
lattice-like Specht seed). Gate status: CONFIRMED_PARTIAL (three-skeptic panel, all pass).

## Check it yourself
sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Runs in a few minutes on a laptop (Python standard library
only — decimal module at 50 digits). It also verifies that a corrupted copy of the
object is rejected.

## Compared to
- Table: E. Specht's Packomania, "circles in a circle" (cci),
  https://packomania.com/cci/txt/radius.txt
- Cell: N = 4405, value 0.014190212053 (live, 12-decimal), author Eckard Specht.
  The live HTML table (https://packomania.com/cci/cci.html) ends at N=3877 and
  carries no row for 4405; the archived 30-decimal value is
  0.014190212052536014904153227050, 4.64e-13 lower, so the live 12-decimal bar
  is the stricter one and is the operative bar.
- Table fetched live: 2026-11-23T08:58:00Z and re-verified 2026-11-23T09:18:05Z
  (HTTP 200 both times); value unchanged
- Queue: https://packomania.com/pending-requests.html — cci candidates queued only in
  652–3943 (Vidit Patankar, 15-Oct-2026) and 126–4141 (Karl Desfontaines,
  03-Nov-2026); N=4405 is outside both. No other cci line exists on the live page.
- Posted seed compared against: https://packomania.com/cci/txt/cci4405.txt
  (sha256 98f2b10dfc1f0dda4e4bdf4ff9f892de95d5e95d3bd13ea6b8af62f5739df1a1);
  sorted pairwise-distance multisets differ (max diff 2.426e-03) — not isometric.

## Not claimed
- No claim about any other N, any other Packomania table, or optimality of this
  configuration (it is a better packing, not a proven optimum; only N ≤ 15–20 are proven).
- No submission has been made to Packomania; the claim is for the verified
  construction only.
- No claim about N=4000: that row is queue-blocked by the Karl Desfontaines
  cci 126–4141 pending line, which is why this run rotated to N=4405.
- A second above-bar file exists this night: polished03 (+2.03836019e-06,
  50-digit certified) stays banked, not bundled, per the scope guard
  (one carrier per claim).

## Credits
- E. Specht — the Packomania record table and the posted cci4405.txt seed
  (https://packomania.com/cci/)
- The V3R1T4S open research kit (https://github.com/elder-plinius/V3R1T4S)
- Discovered by the V3R1T4S nightly hunt, credit "Jorgy72 & Sine", 2026-11-23
