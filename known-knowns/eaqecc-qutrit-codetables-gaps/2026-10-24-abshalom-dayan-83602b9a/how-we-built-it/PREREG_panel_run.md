# PREREG (frozen 2026-10-24T10:37:46Z, before any attack output of this run exists)

null_test: not needed because every claim here is an explicit code checked by deterministic exact checkers against a table value (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Statistic and checkers

- Object: a JSON file with S (GF(3), s x 2n, rows (x|z), symplectic form x.z' - z.x'), G9 (generator of C over
  GF(9), a + 3b <-> a + b w, w^2 = w + 1) and D9 (generator of C^perp_H).
- The claim this run panels first ([[28,5,15;11]]_3, built by run 2026-10-24-0924) is judged by that run's frozen
  checkers A and B (full enumeration over GF(3) of all 3^22 vectors of span(S)^perp, and over GF(9) of all 9^11
  codewords) plus the panel's own checkers. Its object is rebuilt in this run from its construction and must have
  the same sha256 (83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434).
- New candidates in this run (kappa = 12..14 over GF(9)) need two independent exact methods that agree on d:
  (M1) full enumeration of span(S)^perp over GF(3) (bit-sliced Gray code) when 2n - s <= 26, and
  (M2) an exact Brouwer-Zimmermann minimum distance of C over GF(9) giving d(C), plus an explicit codeword of
  weight d(C) outside hull(C) (checked against S directly), which pins d = d(C) exactly.
  When 2n - s > 26, M1 is replaced by a second Brouwer-Zimmermann implementation written independently of M2, and
  the witness check stays. Each checker is tested on the merged [[14,3,8;5]]_3 object (known positive) and on a
  seeded flawed object (known negative) before it judges a candidate.

## Thresholds (what counts as a candidate win in this run)

1. Two exact checkers report the same (n, k, c, d), computed from the object, not copied from it.
2. The (n, k, c) cell is listed on the live qutrit table (not an implied, unlisted c), with c >= 1 and k >= 1.
3. d > d_lower and d <= d_upper for that listed cell, on a re-fetch of https://eaqecc.codetables.de/qutrit.php
   made right before the claim is built (one honest GET).
4. The cell is not already claimed in this repo (known-knowns, TROPHY_CASE.md), in an open or closed pull request,
   or in literature found by the already-settled lens, and is not a propagation of a listed table row.
5. One cell per claim. If one code improves several cells, the claim names one cell; the others are listed as
   not claimed.
6. A tie (d = d_lower) is not a win.

## Search space record

Every search records its exact family and whether it was exhausted (uncapped) or capped. Sampled searches are
never used as exclusions.
