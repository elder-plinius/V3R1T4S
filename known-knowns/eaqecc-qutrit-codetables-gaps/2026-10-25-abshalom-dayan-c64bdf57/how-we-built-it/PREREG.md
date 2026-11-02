# PREREG (frozen 2026-10-25T09:49:21Z, before any checker of this run folder has run on the object)

null_test: not needed because the claim is one explicit stabilizer matrix checked by deterministic exact checkers against a table row (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

Judged: the full criterion (not a partial win), at the listed cell (n,k,c) = (23,4,9), listed [[23,4,11-18;9]].

## Object

E_11, the extended one-point Hermitian code of the curve y^3 + y = x^4 over GF(9) (monomials x^i y^j, j <= 2,
3i + 4j <= 11, at the 27 affine points in the builder's order; 28th coordinate = coefficient of the monomial of pole
order 11), with its coordinates 0, 3, 11, 12, 16 (five affine points; orbit 372 of the 5-subsets of affine points under
the 216 automorphisms of the curve fixing P_inf, runs/2026-10-25-0810/attempts/constructor/code/punct.py) deleted, and
then columns 1, 3, 6, 8, 10, 11, 14, 15, 16, 17, 19, 21 of the punctured [23,9] code (0-based) multiplied by w (norm
-1). The sign pattern is one of the 4 patterns of 2^22 (column 0 fixed) with the maximum Hermitian hull 5 that the
0810 constructor's epsbig found (runs/2026-10-25-0810/attempts/constructor/out/eps_r5.txt, line E11_p5_o372.code).
Claimed [[23,4,12;9]]_3 (from [23,9,>=12]_9 with Hermitian hull 5; d >= 12 by the Goppa-type bound d(E_11) >= 17
minus the 5 deleted coordinates). Builder: runs/2026-10-25-0856/claim/rebuild/build_punct_obj.py
(`python3 build_punct_obj.py 11 out.json 12 0,3,11,12,16 1,3,6,8,10,11,14,15,16,17,19,21`); the object must be
byte-identical to runs/2026-10-25-0810/attempts/constructor/leads/objects/eaqecc_23_4_12_9.json (sha256
c64bdf57a5280892b8d4e085ea565c865d5584de5198baa9763cb516318f06f4) or the difference is explained.
Replacement rule, fixed now: if the exact d of this object is 13..18, the claim is [[23,4,d;9]] with that d (same
object, same cell). Objects at other cells are live leads, not claimed here (one cell per claim).

## Statistic and checkers

- s = rank(S) over GF(3), c = rank(S J S^T)/2, k = n - s + c, computed from S alone, never copied.
- d, exact, by two independent methods that agree, none sampling:
  (A) gf9info.py + infoset.c: recover the GF(9) code C with phi(C) = span(S)^perp from S, then test that every set of
      n - 11 = 12 coordinates carries an information set of C (all C(23,12) = 1352078 column subsets of a generator
      matrix have full rank 9 over GF(9)), which proves d(C) >= 12 and so d >= 12 on all of span(S)^perp; the same
      test at 11 coordinates decides whether d(C) = 12 (deficient subsets exist) or d(C) >= 13; plus an explicit
      vector of span(S)^perp of symplectic weight d outside the isotropic part.
  (B) gf3prep.py + subset_ea64.c at W = 11: for every 11-subset T of the 23 positions, every vector of span(S)^perp
      supported inside T lies in the isotropic part (exact GF(3) ranks), all C(23,11) = 1352078 subsets, uncapped; at
      W = 12 it decides whether some subset carries a vector outside the isotropic part (d = 12) or not (d >= 13, then
      W = 13, ... until found); plus witness.py's witness.
  Third: bz64 on the GF(9) generator matrix; fourth: a no-search proof (Goppa bound d(E_11) >= 17, puncturing at 5
  coordinates loses at most 5, and a weight-12 witness outside the isotropic part); fifth (self-break): the full
  GF(3) enumeration of all 3^18 vectors of span(S)^perp written in folder 0931 (sb_prep.py, sb_enum.c).
  Both exact checkers are re-tested before they judge the object: tests/validate.sh (known positive run 1640's E_17
  object, d = 11; known negative a seeded object with a planted low-weight word), rerun here with this object's
  thresholds.

## Thresholds

1. Computed (n, k, c) = (23, 4, 9), c >= 1.
2. d computed exactly by (A) and (B), agreeing, with 12 <= d <= 18.
3. Against the live row, re-read with one GET right before claiming: the listed cell (23,4,9) has d_lower = 11 and
   d_upper = 18 (scout read 2026-10-25T09:48:20Z: [[23,4,11-18;9]]), so d >= 12 is strictly greater than d_lower and
   d <= d_upper.
4. Not implied, through the page's six propagation rules, by any listed cell (teleportation cells excluded, as in
   every earlier folder; the listed teleportation neighbours [[23,3,12-18;3]] and [[23,4,10-16;4]] are named in the
   claim), any code named in this repo or its open PRs (titles, bodies and filed package files, #726 to #729
   included), the literature found (already-settled lens, arXiv:2607.02170 Table V included; NOVELTY skeptic), or this
   workspace's filed or packaged codes, folder 0856's claim [[25,5,12;8]] and folder 0931's claim [[24,4,13;10]]:
   their closure at (23,4,9) must be <= 11. A tie is not a win.
5. One claim: the cell (23,4,9). Neighbours it gives through the page's rules (for example [[24,4,12;9]] by
   lengthening, [[23,3,12;9]] by subcode) are not claimed.
