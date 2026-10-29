# PREREG (frozen 2026-10-25T09:00:20Z, before any checker of this run folder has run on the object)

null_test: not needed because the claim is one explicit stabilizer matrix checked by deterministic exact checkers against a table row (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

Judged: the full criterion (not a partial win), at the listed cell (n,k,c) = (25,5,8), listed [[25,5,11-18;8]].

## Object

E_13, the extended one-point Hermitian code of the curve y^3 + y = x^4 over GF(9) (monomials x^i y^j, j <= 2,
3i + 4j <= 13, at the 27 affine points in the builder's order; 28th coordinate = coefficient of the monomial of pole
order 13), with its coordinates 0, 1, 2 (the affine points (x, y) = (0, 0), (0, w + 1), (0, 2w + 2) in the
encoding a + 3b: the whole vertical line x = 0) deleted, and then columns 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20,
24 of the punctured [25,11] code (0-based; original coordinates 9, 10, 11, 15..23, 27) multiplied by w (norm -1).
This is the sign pattern ++++++---+++---------+++- that the first folder's constructor lens found as the only one of
2^24 (column 0 fixed) with Hermitian hull 6 (runs/2026-10-25-0810/attempts/constructor/out/eps_r3.txt, line
E13_p3_o0.code). Claimed [[25,5,12;8]]_3 (from [25,11,>=12]_9 with Hermitian hull 6; d >= 12 by the Goppa-type
bound d(E_13) >= 15 minus the 3 deleted coordinates).
Replacement rule, fixed now: if the exact d of this object is 13..18, the claim is [[25,5,d;8]] with that d (same
object, same cell). Objects at other cells are live leads, not claimed here (one cell per claim).

## Statistic and checkers

- s = rank(S) over GF(3), c = rank(S J S^T)/2, k = n - s + c, computed from S alone, never copied.
- d, exact, by two independent methods that agree, none sampling:
  (A) gf9info.py + infoset.c: recover the GF(9) code C with phi(C) = span(S)^perp from S, then test that every set of
      n - 11 = 14 coordinates carries an information set of C (all C(25,14) = 4457400 column subsets of a generator
      matrix have full rank 11 over GF(9)), which proves d(C) >= 12 and so d >= 12 on all of span(S)^perp; the same
      test at 13 coordinates decides whether d(C) = 12 (deficient subsets exist) or d(C) >= 13; plus an explicit
      vector of span(S)^perp of symplectic weight d outside the isotropic part.
  (B) gf3prep.py + subset_ea64.c at W = 11: for every 11-subset T of the 25 positions, every vector of span(S)^perp
      supported inside T lies in the isotropic part (exact GF(3) ranks), all C(25,11) = 4457400 subsets, uncapped; at
      W = 12 it decides whether some subset carries a vector outside the isotropic part (d = 12) or not (d >= 13, then
      W = 13, ... until found); plus witness.py's witness.
  Third, cited: bz64 on the GF(9) generator matrix; fourth, cited: the no-search proof (Goppa bound d(E_13) >= 15,
  puncturing at 3 coordinates loses at most 3, and a weight-d witness outside the isotropic part).
  Both exact checkers are re-tested before they judge the object: the first folder's tests/validate.sh (known
  positive run 1640's E_17 object, d = 11; known negative a seeded object with a planted low-weight word), rerun here.

## Thresholds

1. Computed (n, k, c) = (25, 5, 8), c >= 1.
2. d computed exactly by (A) and (B), agreeing, with 12 <= d <= 18.
3. Against the live row, re-read with one GET right before claiming: the listed cell (25,5,8) has d_lower = 11 and
   d_upper = 18 (scout read 2026-10-25T08:57:05Z: [[25,5,11-18;8]]), so d >= 12 is strictly greater than d_lower and
   d <= d_upper.
4. Not implied, through the page's six propagation rules, by any listed cell (teleportation cells excluded, as in
   every earlier folder; the listed teleportation neighbour [[25,4,12-18;4]] is named in the claim), any code named
   in this repo or its open PRs (titles, bodies and filed package files, #726 to #729 included), the literature found
   (already-settled lens, arXiv:2607.02170 Table V included; NOVELTY skeptic), or this workspace's filed or packaged
   codes and its first folder's claim: their closure at (25,5,8) must be <= 11. A tie is not a win.
5. One claim: the cell (25,5,8). Neighbours it gives through the page's rules (for example [[26,5,12;8]] by
   lengthening, [[25,4,12;8]] by subcode) are not claimed.
