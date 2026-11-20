# Improved circle packing: 4345 equal circles in a circle

## What
polished03.txt's 50-digit feasible radius exceeds the live Packomania value for N=4345 by 3.78404615968e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4345 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

In numbers: r* = 0.01427701232602575290682290312897756077321 (50 digits, no tolerance) vs the live Packomania
cci table value 0.014273228279866076598567467525 — a strict improvement of +3.78404615968e-06,
378,405x the 1e-11 bar. Bank partial win p2 class (gap value N > 2600 with a
lattice-like Specht seed). Gate status: CONFIRMED_PARTIAL (three-skeptic panel, all pass).

## Check it yourself
sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Runs in a few minutes on a laptop (Python standard library
only — decimal module at 50 digits). It also verifies that a corrupted copy of the
object is rejected.

## Compared to
- Table: E. Specht's Packomania, "circles in a circle" (cci),
  https://packomania.com/cci/txt/radius.txt
- Cell: N = 4345, value 0.014273228279866076598567467525, author Eckard Specht
- Table fetched live: 2026-11-19T08:58:05Z and re-verified 2026-11-19T09:18:00Z
  (HTTP 200 both times); value unchanged
- Queue: https://packomania.com/pending-requests.html — cci candidates queued only in
  652–3943 (Vidit Patankar, 15-Oct-2026) and 126–4141 (Karl Desfontaines,
  03-Nov-2026); N=4345 is outside both. No other cci line exists on the live page.
- Posted seed compared against: https://packomania.com/cci/txt/cci4345.txt
  (sha256 69ad4fb26db93650da3deb76382d1f01a7e99acb884b65a51cf951dd93b20285);
  sorted pairwise-distance multisets differ (max diff 2.664e-03) — not isometric.

## Not claimed
- No claim about any other N, any other Packomania table, or optimality of this
  configuration (it is a better packing, not a proven optimum; only N ≤ 15–20 are proven).
- No submission has been made to Packomania; the claim is for the verified
  construction only.
- No claim about N=4000: that row is queue-blocked by the Karl Desfontaines
  cci 126–4141 pending line, which is why this run rotated to N=4345.
- The second above-bar file from the same night (polished00, +1.71342783757e-06) is a
  separate object, cited not bundled; it is not part of this claim.

## Credits
- E. Specht — the Packomania record table and the posted cci4345.txt seed
  (https://packomania.com/cci/)
- The V3R1T4S open research kit (https://github.com/elder-plinius/V3R1T4S)
- Discovered by the V3R1T4S nightly hunt, credit "Jorgy72 & Sine", 2026-11-19
