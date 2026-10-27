# Improved circle packing: 3949 equal circles in a circle

## What
Candidate_n3949.txt's 50-digit feasible radius exceeds the record-quoted live Packomania value for N=3949 by 2.372e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=3949 outside the record-quoted queued cci ranges and absent from record-quoted history updates — but the Moki & Julio "*many*" category-unspecified pending bundle leaves the queue rule unresolved until the bundle disappears and the criterion's required re-check happens.

In numbers: r* = 0.01496783530958494442 (50 digits, no tolerance) vs the live Packomania
cci table value 0.014965462848801963307763269064 — a strict improvement of +2.372e-06,
237,000× the 1e-11 bar. Bank partial win p2 class (gap value N > 2600 with a
lattice-like Specht seed). Gate status: CONFIRMED_PARTIAL (three-skeptic panel, all pass).

## Check it yourself
sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Runs in under a minute on a laptop (Python standard library
only — decimal module at 50 digits). It also verifies that a corrupted copy of the
object is rejected.

## Compared to
- Table: E. Specht's Packomania, "circles in a circle" (cci),
  https://packomania.com/cci/txt/radius.txt
- Cell: N = 3949, value 0.014965462848801963307763269064, author Eckard Specht
- Table fetched live: 2026-10-20T08:59:32Z and re-verified 2026-10-20T09:52:24Z
  (HTTP 200 both times); value unchanged
- Queue: https://packomania.com/pending-requests.html — cci candidates queued only in
  652–3943 (Vidit Patankar, 15-Oct-2026); N=3949 outside. Standing caveat: the
  26-Sep-2026 Moki & Julio "*many*" 4666-candidate bundle is category-unspecified;
  re-check N=3949 against the live table once that bundle clears.
- Posted seed compared against: https://packomania.com/cci/txt/cci3949.txt
  (sha256 b752757bcac8a46337373b99cec43c5c25b0abceed9bdfd0a054c00b5857180b);
  sorted pairwise-distance multisets differ (max diff 5.06e-03) — not isometric.

## Not claimed
- No claim about any other N, any other Packomania table, or optimality of this
  configuration (it is a better packing, not a proven optimum; only N <= 13 and N = 19 are marked proven on Packomania, with computer-assisted proofs for N = 15 announced on 11-Oct-2026).
- No submission has been made to Packomania; the claim is for the verified
  construction only.
- The pending-queue caveat above is part of the claim's scope.

## Credits
- E. Specht — the Packomania record table and the posted cci3949.txt seed
  (https://packomania.com/cci/)
- The V3R1T4S open research kit (https://github.com/elder-plinius/V3R1T4S)
- Discovered by the V3R1T4S nightly hunt, credit "Jorgy72 & Sine", 2026-10-20
