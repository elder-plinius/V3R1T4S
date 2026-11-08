# PREREG (frozen 2026-10-24T20:02:57Z, before any checker of this run folder has been run on the object)

null_test: not needed because the claim is one explicit stabilizer matrix checked by deterministic exact checkers against a table value (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Object to be judged

The Construction X lead of run 2026-10-24-1727's optimizer lens, objects/lead_33_9_14_12.json there (sha256
059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391), built from data/X17_q0_a3.xin (sha256
db455dfee36441cb0b589cc9c8f8d00c26ae1e986b3ac47a1614fd1ad2bd32df, copied unchanged into this run's data/) with
C1 = C(D_28, 3Q + 8P_inf), C2 = C(D_28, 2Q + 8P_inf), Q = deg3.py place 0, tail points 1,0,6,9,5,
M = 1,3,8,0,7,7,4,1,2, columns '-' in ++++++++++++++++++++++++++++----- times w. Claimed [[33,9,14;12]]_3 for the
listed cell (n,k,c) = (33,9,12). This run rebuilds it with build_x_lead.py from these frozen parameters; the rebuilt
JSON must be byte-identical (same sha256) to the run-1727 file.
Replacement rule, fixed now: if a lens of this run folder produces an object at (33,9,12) with exact d >= 15 passing
every threshold below, that object is the claim instead. Objects at other cells are live leads, not claimed here (one
cell per claim). The first lead, [[33,7,15;12]]_3 at (33,7,12), is judged in run folder 2026-10-24-1953.

## Statistic and checkers

- s = rank(S) over GF(3), c = rank(S J S^T)/2, k = n - s + c, computed from S alone, never copied.
- d, exact, by two independent methods that agree, none sampling:
  (A) gf9info.py + infoset.c: recover the GF(9) code C with phi(C) = span(S)^perp from S (exact GF(3) null space,
      checked closed under w), then test that every set of n - 13 = 20 coordinates carries an information set of C
      (all C(33,20) = 573166440 column subsets of a generator matrix have full rank 15 over GF(9)), which proves
      d(C) >= 14 and so d >= 14 on all of span(S)^perp; the same test at 19 coordinates must find deficient subsets
      (d(C) = 14); plus an explicit vector of span(S)^perp of symplectic weight 14 outside the isotropic part (d <= 14).
  (B) gf3prep.py + subset_ea64.c at W = d - 1 = 13: for every 13-subset T of the 33 positions, every vector of
      span(S)^perp supported inside T lies in the isotropic part (exact GF(3) ranks), all C(33,13) = 573166440
      subsets, uncapped; at W = 14 it must find subsets with a vector outside the isotropic part; plus witness.py's
      witness.
  Third, cited: bz64 (Brouwer-Zimmermann over GF(9), n <= 64) on the GF(9) generator matrix.
  Both checkers are re-tested before they judge the object (attempts/evaluator-first/tests/validate.sh): known positive
  run 1640's E_17 object (d = 11, counts 1735, 1745, 1731 at W = 11), known negative a seeded object with a planted
  weight-3 word (W = 3 finds a subset; infoset m = 20 finds deficient subsets).

## Thresholds

1. Computed (n, k, c) = (33, 9, 12) with c >= 1.
2. d computed exactly = claimed d by (A) and (B), agreeing.
3. d > d_lower and d <= d_upper of the listed cell on a live one-GET re-read of https://eaqecc.codetables.de/qutrit.php
   right before claiming (scout: 13-21 at 19:55:15Z).
4. Not implied, through the page's propagation rules, by any listed cell (teleportation cells excluded, as in runs
   1253, 1500, 1640 and 1727), any code in this repo, its open PRs (#363, #403-#405, #643, #645, #646, #651), the
   literature found (already-settled lens; NOVELTY skeptic), or this workspace's other codes (E_m family, the
   [[33,8,16;15]] package, the first lead [[33,7,15;12]]). A tie is not a win.
5. One cell per claim; propagated neighbours are listed as not claimed.

## Search space record

Every search records its exact family and whether it was exhausted (uncapped) or capped. Capped or sampled searches
are never used as exclusions.
