# PREREG (frozen 2026-10-24T23:13:26Z, before any checker of this run folder has been run on the object)

null_test: not needed because the claim is one explicit stabilizer matrix checked by deterministic exact checkers against a table value (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Object to be judged

E_15 of run 2026-10-24-1033's constructor lens, objects/eaqecc_28_7_13_9.json there (sha256
64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78): the extended one-point code of the Hermitian curve
y^3 + y = x^4 over GF(9) of pole order 15, unscaled. Claimed [[28,7,13;9]]_3 for the listed cell (n,k,c) = (28,7,9).
This run rebuilds it with build_obj.py (python3 build_obj.py 15 out.json 13); the rebuilt JSON must be byte-identical
(same sha256) to the run-1033 file.
Replacement rule, fixed now: if a lens of this run folder produces an object at (28,7,9) with exact d >= 14 passing
every threshold below, that object is the claim instead. Objects at other cells are live leads, not claimed here (one
cell per claim).

## Statistic and checkers

- s = rank(S) over GF(3), c = rank(S J S^T)/2, k = n - s + c, computed from S alone, never copied.
- d, exact, by two independent methods that agree, none sampling:
  (A) gf9info.py + infoset.c: recover the GF(9) code C with phi(C) = span(S)^perp from S (exact GF(3) null space,
      checked closed under w), then test that every set of n - 12 = 16 coordinates carries an information set of C
      (all C(28,16) = 30421755 column subsets of a generator matrix have full rank 13 over GF(9)), which proves
      d(C) >= 13 and so d >= 13 on all of span(S)^perp; the same test at 15 coordinates must find deficient subsets
      (d(C) = 13); plus an explicit vector of span(S)^perp of symplectic weight 13 outside the isotropic part.
  (B) gf3prep.py + subset_ea64.c at W = d - 1 = 12: for every 12-subset T of the 28 positions, every vector of
      span(S)^perp supported inside T lies in the isotropic part (exact GF(3) ranks), all C(28,12) = 30421755
      subsets, uncapped; at W = 13 it must find subsets with a vector outside the isotropic part; plus witness.py's
      witness.
  Third, cited: bz64 on the GF(9) generator matrix; and run 1033's full 3^26 enumeration (72288 words of weight 13).
  Both exact checkers are re-tested before they judge the object (attempts/evaluator-first/tests/validate.sh): known
  positive run 1640's E_17 object (d = 11, counts 1735, 1745, 1731 at W = 11), known negative a seeded object with a
  planted weight-3 word (W = 3 finds a subset; infoset m = 16 finds deficient subsets).

## Thresholds

1. Computed (n, k, c) = (28, 7, 9) with c >= 1.
2. d computed exactly = claimed d by (A) and (B), agreeing.
3. d > d_lower and d <= d_upper of the listed cell on a live one-GET re-read of https://eaqecc.codetables.de/qutrit.php
   right before claiming (scout: 12-18 at 2026-10-24T22:58:17Z).
4. Not implied, through the page's propagation rules, by any listed cell (teleportation cells excluded, as in runs
   1253, 1500, 1640, 1727 and 1953), any code in this repo, its open PRs (#363, #403-#405, #643, #645, #646, #651,
   #710), the literature found (already-settled lens; NOVELTY skeptic), or this workspace's other codes (E_m family,
   the packages 5713c745 and 059282c3, the claim of run folder 2026-10-24-2256, every lead). A tie is not a win.
5. One cell per claim; propagated neighbours are listed as not claimed.

## Search space record

Every search records its exact family and whether it was exhausted (uncapped) or capped. Capped or sampled searches
are never used as exclusions.
