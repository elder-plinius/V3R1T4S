# Improved circle packing: 4153 equal circles in a circle

## What
object/candidate_n4153.txt's 50-digit feasible radius exceeds the live Packomania value for N=4153 by 2.706e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4153 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

In numbers: r* = 0.01459912804413632909680425838614465154649 (50 digits, no tolerance) vs the live Packomania
cci table value 0.014596422226478759387097611060 — a strict improvement of +2.706e-06,
270,582x the 1e-11 bar. Bank partial win p2 class (gap value N > 2600 with a
lattice-like Specht seed). Gate status: CONFIRMED_PARTIAL (three-skeptic panel, all pass).

## Check it yourself
sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Runs in a few minutes on a laptop (Python standard library
only — decimal module at 50 digits). It also verifies that a corrupted copy of the
object is rejected.

## Compared to
- Table: E. Specht's Packomania, "circles in a circle" (cci),
  https://packomania.com/cci/txt/radius.txt
- Cell: N = 4153, value 0.014596422226478759387097611060, author Eckard Specht
- Table fetched live: 2026-11-05T09:58:13Z and re-verified 2026-11-05T10:26:45Z
  (HTTP 200 both times); value unchanged
- Queue: https://packomania.com/pending-requests.html — cci candidates queued only in
  652–3943 (Vidit Patankar, 15-Oct-2026) and 126–4141 (Karl Desfontaines,
  03-Nov-2026); N=4153 is outside both. No other cci line exists on the live page.
- 2026-11-05: Moki & Julio's csq bundle line (26-Sep-2026, 2213 candidates, range
  385–9996) is gone from the live pending-requests listing (now inside an HTML
  comment); the live N = 4153 row is unchanged at 0.014596422226478759387097611060.
- Posted seed compared against: https://packomania.com/cci/txt/cci4153.txt
  (sha256 bca1f6739e2a898d6862658e092f0e105667652dac18340da863a8d2eb94ffae);
  sorted pairwise-distance multisets differ (max diff 3.178732e-03) — not isometric.

## Not claimed
- No claim about any other N, any other Packomania table, or optimality of this
  configuration (it is a better packing, not a proven optimum; only N ≤ 15–20 are proven).
- No submission has been made to Packomania; the claim is for the verified
  construction only.
- No claim about N=4000: that row is queue-blocked by the Karl Desfontaines
  cci 126–4141 pending line, which is why this run rotated to N=4153.

## Credits
- E. Specht — the Packomania record table and the posted cci4153.txt seed
  (https://packomania.com/cci/)
- The V3R1T4S open research kit (https://github.com/elder-plinius/V3R1T4S)
- Discovered by the V3R1T4S nightly hunt, credit "Jorgy72 & Sine", 2026-11-05
