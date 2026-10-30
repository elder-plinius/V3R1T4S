# PREREG (frozen 2026-10-24T17:29:58Z, before any checker of this run folder has been run on the object)

null_test: not needed because the claim is one explicit stabilizer matrix checked by deterministic exact checkers against a table value (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Object to be judged

The Construction X code found by run 2026-10-24-1640's constructor lens, saved there as
attempts/constructor/xcodes/best_X_q0_a4_m5.code (sha256
e381feef35905221a3c4c9af24b9104a615ee1364f5e862bb80b6bda1dc8e41d; a "K n" GF(9) generator matrix, 13 x 33),
built from attempts/constructor/xcodes/X_q0_a4.xin (sha256
9479892172b1aa0ff7f51ad03fc020a91c66c0146f261ba3072711e29fa7f86a): C1 = C(D_28, 4Q + 3P_inf), C2 =
C(D_28, 3Q + 3P_inf), Q the degree-3 place with index 0 of deg3.py, a [5,3,3]_9 tail, a sign pattern. Claimed
[[33,8,16;15]]_3 for the listed cell (n,k,c) = (33,8,15). This run rebuilds it from frozen construction parameters
(the rebuilt GF(9) matrix must equal that file) and converts it to S = phi(C^⊥H).
Replacement rule, fixed now: if a lens of this run folder produces an object at (33,8,15) with exact d >= 17 passing
every threshold below, that object is the claim instead. Objects at other cells (for example hull 6 at (33,7,14))
are recorded as live leads and not claimed here (one cell per claim).

## Statistic and checkers

- s = rank(S) over GF(3), c = rank(S J S^T)/2, k = n - s + c, computed from S alone, never copied.
- d, exact, by two independent methods that agree, none sampling:
  (A) run 1500's GF(9) information-set checker (gf9info.py + infoset.c): recover the GF(9) code C with
      phi(C) = span(S)^perp from S (exact GF(3) null space, checked closed under w), and test that every set of
      n - 15 = 18 coordinates carries an information set of C (all C(33,18) = 1037158320 column subsets of a
      generator matrix have full rank 13 over GF(9)), which proves d(C) >= 16 and so d >= 16 on all of span(S)^perp;
      the same test at 17 coordinates must find deficient subsets (so d(C) = 16); plus an explicit vector of
      span(S)^perp of symplectic weight 16 outside the isotropic part (d <= 16).
  (B) run 1253's position-subset test from S alone (gf3prep.py + subset_ea, widened in this run to n <= 64) at
      W = d - 1 = 15: for every 15-subset T of the 33 positions, every vector of span(S)^perp supported inside T lies
      in the isotropic part (exact GF(3) ranks), all C(33,15) = 1037158320 subsets, uncapped; at W = 16 it must find
      subsets with a vector outside the isotropic part; plus its witness.
  Third, cited: bz64 (Brouwer-Zimmermann over GF(9), bz9 widened to n <= 64) on the GF(9) generator matrix.
  The widened subset test is re-tested before it judges the claim: identical counts to the n <= 32 original on the
  run 1640 object at W = 10 and 11, agreement with brute force on random small cases, a known positive (the run-1640
  E_17 object, d = 11) and known negatives (a seeded object with a low-weight logical; the claim at a too-high d,
  W = 16).

## Thresholds

1. Computed (n, k, c) = (33, 8, 15) with c >= 1.
2. d computed exactly = claimed d by (A) and (B), agreeing.
3. d > d_lower and d <= d_upper of the listed cell on a live one-GET re-read of https://eaqecc.codetables.de/qutrit.php
   right before claiming (scout: 15-23 at 17:27:46Z).
4. Not implied, through the page's propagation rules, by any listed cell (teleportation cells excluded, as in runs
   1253, 1500 and 1640), any code in this repo, its open PRs (#363, #403-#405, #643-#646), the literature found
   (already-settled lens; NOVELTY skeptic), or this workspace's other codes (E_m family, run 1640's E_17 claim). A tie
   is not a win.
5. One cell per claim; propagated neighbours are listed as not claimed.

## Search space record

Every search records its exact family and whether it was exhausted (uncapped) or capped. Capped or sampled searches
(the hull searches over M, points and signs are random walks) are never used as exclusions.
