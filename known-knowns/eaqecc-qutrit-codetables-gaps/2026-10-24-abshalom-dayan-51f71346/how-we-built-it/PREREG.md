# PREREG (frozen 2026-10-24T15:06:11Z, before any checker of this run has been run on any object)

null_test: not needed because the claim is one explicit stabilizer matrix checked by deterministic exact checkers against a table value (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Object to be judged

Default: the dossier's priority-2 candidate, run 2026-10-24-1033's constructor/objects/eaqecc_28_6_12_6.json
(sha256 51f713462c7db831723702a4d0b0cc9a73faacd2552999a7007f75d393188573), claimed [[28,6,12;6]]_3 for the listed
cell (n,k,c) = (28,6,6), rebuilt in this run from its construction (the rebuild must be byte-identical).
Replacement rule, fixed now: if a lens of this run produces an object with exact d >= 13 at (n,k,c) = (28,6,6)
passing every threshold below, that object is the claim instead. Any other new object (other cells) is recorded as a
live lead and not claimed in this run folder (one cell per claim).

## Statistic and checkers

- s = rank(S) over GF(3), c = rank(S J S^T)/2, k = n - s + c, computed from S alone, never copied.
- d, exact, by two independent methods that agree, none sampling:
  (A) a checker written in this run (evaluator-first lens): recover the GF(9) code C with phi(C) = span(S)^perp from
      S (exact GF(3) null space, then checked to be GF(9)-linear), and test that every set of n - 11 = 17 coordinates
      carries an information set of C (all C(28,17) = 21474180 column subsets of a generator matrix have full rank
      over GF(9)), which proves d(C) >= 12 and so d >= 12 on all of span(S)^perp; plus an explicit vector of
      span(S)^perp of symplectic weight 12 outside the isotropic part (d <= 12).
  (B) run 2026-10-24-1253's position-subset test from S alone (gf3prep.py + subset_ea.c) at W = d - 1 = 11: for every
      11-subset T of the 28 positions, every vector of span(S)^perp supported inside T lies in the isotropic part
      (exact GF(3) ranks), all C(28,11) = 21474180 subsets, uncapped; plus its witness.
  Run 2026-10-24-1033's bz9 result (d(C) = 12) is cited as a third method.
  Checker (A) is tested before it judges the claim on a known positive (this workspace's panel-confirmed
  [[28,7,14;11]]_3 object, d = 14), on small random codes against brute force, and on known negatives (seeded objects
  with a low-weight logical, and the candidate with a claimed d that is too high).

## Thresholds

1. Computed (n, k, c) = (28, 6, 6) with c >= 1.
2. d computed exactly = claimed d by (A) and (B), agreeing.
3. d > d_lower and d <= d_upper of the listed cell on a live one-GET re-read of https://eaqecc.codetables.de/qutrit.php
   right before claiming (scout: 11-17 at 15:03:31Z).
4. Not implied, through the page's propagation rules, by any listed cell (teleportation cells excluded, as in run
   1253), any code in this repo, its open PRs, the literature found (already-settled lens; NOVELTY skeptic), or this
   workspace's own other codes. A tie is not a win.
5. One cell per claim; propagated neighbours are listed as not claimed.

## Search space record

Every search records its exact family and whether it was exhausted (uncapped) or capped. Capped or sampled searches
are never used as exclusions.
