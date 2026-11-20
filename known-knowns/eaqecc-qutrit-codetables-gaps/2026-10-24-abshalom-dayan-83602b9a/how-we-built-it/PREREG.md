# PREREG (frozen 2026-10-24T09:36:16Z, before any search output exists)

null_test: not needed because every claim here is an explicit code checked by deterministic exact checkers against a table value (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Statistic and checkers

- Object: a JSON file with S (GF(3), s x 2n, rows (x|z), J = [[0,I],[-I,0]]), G9 (generator of C over GF(9),
  a+3b = a+b*w, w^2 = w+1) and D9 (generator of C^perp_H).
- Checker A (attempts/evaluator-first/code/checkA_symplectic.py): from S only, s = rank, c = rank(S J S^T)/2,
  k = n - s + c, d = minimum symplectic weight over span(S)^perp minus span(S) ∩ span(S)^perp by full enumeration.
- Checker B (attempts/evaluator-first/code/checkB.py + checkB_gf9.c): from G9, Hermitian Gram rank, hull, k, c, and
  d = minimum weight over C minus hull(C) by full Gray-code enumeration of all 9^kappa messages; plus the check that
  rowspace(S) = phi(D9) and D9 = C^perp_H.
- Both were tested before any search on a known positive (the merged [[14,3,8;5]]_3 object, both report k=3, c=5,
  d=8) and on seeded flawed objects (both report MISMATCH): attempts/evaluator-first/checkA_tests.out, checkB_tests.out.

## Thresholds (what counts as a candidate win in this run)

1. Checkers A and B both report the same (n, k, c, d), computed, not copied from the claim.
2. The (n, k, c) cell is listed on the live qutrit table (not an implied, unlisted c), with c >= 1 and k >= 1
   (k = 0 cells are skipped: the criterion's d is taken over an empty set there).
3. d > d_lower and d <= d_upper for that listed cell, on a re-fetch of https://eaqecc.codetables.de/qutrit.php made
   right before the claim is built (one honest GET).
4. The cell is not already claimed in this repo (known-knowns, TROPHY_CASE.md), in an open or closed pull request,
   or in literature found by the already-settled lens, and is not a propagation of a listed table row.
5. One cell per claim. If one code improves several cells, the claim names one cell; the others are listed as
   not claimed.
6. A tie (d = d_lower) is not a win.

## Search space record

Every search records its exact family and whether it was exhausted (uncapped) or capped.
