context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report (partial win p1, cell b=3, m=11, s=19)

## Cell test
- One fetch of the MinT query page for (b=3, m=11, s=19), logged in the work folder. HTTP 200, SHA-256 identical to the one in the-record-we-beat/SNAPSHOT.md and INDEX.csv (9c138a9b...).
- Page text: "Best known t: 5"; "Lower bound on t (digital): 4" (no digital (3,11,19)-net, via the linear-OA bound on a [16,7,7] code); "Lower bound on t: 3" (no (2,11,19)-net, via s-reduction to (2,11,12) and a depth-2 OOA LP bound).
- So (3,11,19) is a cell where the general bound (3) is below the digital bound (4), and t = 3 equals MinT's general lower bound there. Both quantifiers in p1 are met literally. It is a real gap cell, not a stretched one.

## Certificate test
- Ran verify-it-yourself/run_checks.sh in a copy of this package: Python Fraction verifier and C99 __int128 verifier both print VERIFIED, both corruption tests are rejected, final line PASS. SHA256SUMS passes for every package file (it also lists four panel/ report files that are absent from a working folder (not shipped); harmless).
- I read the verifier. It checks the dual conditions: u_f <= 0 for |f| > 8, 1 + sum u_f K_f(X) >= 0 for all 8854 non-diagonal shapes, and the diagonal value equals the claimed M-bound 2403828588527406331/13544324988667 = 177478.655... > 177147 = 3^11. I re-derived the weak-duality step (M >= 1 + sum u_f K_f(diag), using nonnegative distance distribution and nonnegative c_f for |f| > k); it is sound.
- Null model / independent check: I ran the package's own Krawtchouk kernel at depth T=4 on a real base-3 (0,4,2)-net (81 points, strength 4). Moment sums vanish for 1 <= |f| <= 4 and are nonnegative for |f| > 4, with zero violations. The kernel is therefore right at depth 4 on a nontrivial object, beyond the package's own small calibrations.
- Wording check on "embedded OOA": the certificate is for OOA(M,19,S_3,T=4,k=8), depth 4, not the full depth 8 net-OOA. A (3,11,19)-net gives an OOA of depth 8 and strength 8, and truncating depth to 4 gives a valid OOA(M,19,S_3,4,8). So "an embedded OOA" fits, but it is a depth-truncated one, and MinT's published LP results for depth 4 stop at s <= 8. The package states T=4 and k=8 in the headline, so the depth is disclosed. A weaker, truncated LP is still a valid proof of non-existence. Fits the letter of p1; it is not MinT's own full-depth object. I do not count this against it.
- "Exact rational dual solution ... verified in exact arithmetic": yes (60 rational weights, Fraction and 128-bit integer checks).

## Does "MinT's general lower bound then rises" follow?
- Yes, mathematically: no (3,11,19)-net implies t >= 4 for (b=3, m=11, s=19), which equals the digital bound 4. MinT's live page still shows 3, as it must; the package says "raising", and the proof does imply the raise. Not overclaimed as a MinT edit.

## Subsumption
- MinT's general bound is 3 on the fetched page, so no MinT-listed result already rules out t = 3 here. This is a genuine closure of a cell, not subsumed by MinT's current data. I did not search outside MinT for a prior paper.

## Wording wider than the evidence
- README What, INDEX.csv and the title are scoped to the single cell and to non-existence at t = 3; Not claimed lists the Full Win and the open (4,11,19) question. Fine.
- INDEX.csv says "Closed MinT cell"; true in the sense that general and digital bounds now coincide at 4.
- HOW_WE_FOUND_IT.md (marked unverified contributor text) says MinT precomputed T=3 only up to s <= 15. MinT's page says all LP bounds for T=3 with s <= 11, plus k <= 20 with s <= 15; and T=4 with s <= 8. The s <= 15 figure is a half-truth. It does not touch the certificate. Minor.

## Remaining limits
- Does not construct a net (no Full Win). No claim about (4,11,19). The verifier's validity rests on the multivariate Krawtchouk formula; I confirmed it on one depth-4 net plus the package's calibrations, not on a proof from the literature.

confirmed_scope: An exact rational dual solution of the depth-4, strength-8 OOA linear-programming bound (verified in Python Fractions and C99 128-bit integers) shows M >= 2403828588527406331/13544324988667 > 3^11 for OOA(M,19,S_3,4,8), so no (3,11,19)-net in base 3 exists, which makes MinT's general lower bound on t for that single cell at least 4 (it is 3 on the live page today), equal to the digital bound.

pass: true
