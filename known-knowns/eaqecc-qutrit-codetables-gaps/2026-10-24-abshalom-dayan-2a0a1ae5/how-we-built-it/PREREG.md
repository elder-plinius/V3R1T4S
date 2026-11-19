# PREREG (frozen 2026-10-24T16:45:48Z, before any checker of this run has been run on any object)

null_test: not needed because the claim is one explicit stabilizer matrix checked by deterministic exact checkers against a table value (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Object to be judged

Default: the dossier's priority-3 candidate, run 2026-10-24-1033's constructor/objects/eaqecc_28_9_11_7.json
(sha256 2a0a1ae5e178dcc0264b6a9f40ee1935991f28e65199a0712aecffe879b6c7d0), claimed [[28,9,11;7]]_3 for the listed
cell (n,k,c) = (28,9,7), rebuilt in this run from its construction (the rebuild must be byte-identical).
Replacement rule, fixed now: if a lens of this run produces an object with exact d >= 12 at (n,k,c) = (28,9,7)
passing every threshold below, that object is the claim instead. Any other new object (other cells) is recorded as a
live lead and not claimed in this run folder (one cell per claim).

## Statistic and checkers

- s = rank(S) over GF(3), c = rank(S J S^T)/2, k = n - s + c, computed from S alone, never copied.
- d, exact, by two independent methods that agree, none sampling:
  (A) run 2026-10-24-1500's GF(9) information-set checker (gf9info.py + infoset.c): recover the GF(9) code C with
      phi(C) = span(S)^perp from S (exact GF(3) null space, checked closed under w), and test that every set of
      n - 10 = 18 coordinates carries an information set of C (all C(28,18) = 13123110 column subsets of a generator
      matrix have full rank over GF(9)), which proves d(C) >= 11 and so d >= 11 on all of span(S)^perp; plus an
      explicit vector of span(S)^perp of symplectic weight 11 outside the isotropic part (d <= 11).
  (B) run 2026-10-24-1253's position-subset test from S alone (gf3prep.py + subset_ea.c) at W = d - 1 = 10: for every
      10-subset T of the 28 positions, every vector of span(S)^perp supported inside T lies in the isotropic part
      (exact GF(3) ranks), all C(28,10) = 13123110 subsets, uncapped; plus its witness.
  Run 2026-10-24-1033's bz9 result (d(C) = 11) is cited as a third method.
  Both are re-tested in this run, before they judge the claim, on a known positive (this workspace's panel-confirmed
  [[28,6,12;6]]_3 object, d = 12) and on known negatives (a seeded object with a low-weight logical, and the
  candidate with a claimed d that is too high, d = 12).

## Thresholds

1. Computed (n, k, c) = (28, 9, 7) with c >= 1.
2. d computed exactly = claimed d by (A) and (B), agreeing.
3. d > d_lower and d <= d_upper of the listed cell on a live one-GET re-read of https://eaqecc.codetables.de/qutrit.php
   right before claiming (scout: 10-14 at 16:42:29Z).
4. Not implied, through the page's propagation rules, by any listed cell (teleportation cells excluded, as in runs
   1253 and 1500), any code in this repo, its open PRs (including #643-#646), the literature found (already-settled
   lens; NOVELTY skeptic), or this workspace's own other codes. A tie is not a win.
5. One cell per claim; propagated neighbours are listed as not claimed.

## Search space record

Every search records its exact family and whether it was exhausted (uncapped) or capped. Capped or sampled searches
are never used as exclusions. Leads at other cells found by the constructor or cell-picker lenses are reported as
live leads with their checks, never claimed here.
