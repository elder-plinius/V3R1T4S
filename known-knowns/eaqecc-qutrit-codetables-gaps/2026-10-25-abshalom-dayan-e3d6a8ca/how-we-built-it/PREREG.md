# PREREG (frozen 2026-10-25T02:37:23Z, before any checker of this run folder has been run on the object)

null_test: not needed because the claim is one explicit stabilizer matrix checked by deterministic exact checkers against a table value (no search statistic, no "beats chance" claim)

## Criterion (verbatim, bank entry eaqecc-qutrit-codetables-gaps)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Object to be judged

The Construction X lead of run folder 2026-10-24-2256's optimizer lens, objects/lead_35_7_16_14.json there (sha256
e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4), with C1 = L(2Q + 8P_inf), C2 = L(Q + 8P_inf),
Q = deg4.py degree-4 place 0, tail points 8,0,4,6,3,7,5, M = 6,8,4,5,7,4,0,1,5,1,7,2,0,1,8,3, columns '-' in
+---++---+--+++-+----++-+--+-+--++- times w. Claimed [[35,7,16;14]]_3 for the listed cell (n,k,c) = (35,7,14). This
run rebuilds it with build_x4.py from these frozen parameters
(build_x4.py 0 2 8 8,0,4,6,3,7,5 6,8,4,5,7,4,0,1,5,1,7,2,0,1,8,3 '+---++---+--+++-+----++-+--+-+--++-' out.json 16 out_G9.code);
the rebuilt JSON must be byte-identical (same sha256) to the run-2256 file.
Replacement rule, fixed now: if a lens of this run folder produces an object at (35,7,14) with exact d >= 17 passing
every threshold below, that object is the claim instead. Objects at other cells are live leads, not claimed here (one
cell per claim).

## Statistic and checkers

- s = rank(S) over GF(3), c = rank(S J S^T)/2, k = n - s + c, computed from S alone, never copied.
- d, exact, by two independent methods that agree, none sampling:
  (A) gf9info.py + infoset.c: recover the GF(9) code C with phi(C) = span(S)^perp from S (exact GF(3) null space,
      checked closed under w), then test that every set of n - 15 = 20 coordinates carries an information set of C
      (all C(35,20) = 3247943160 column subsets of a generator matrix have full rank 14 over GF(9)), which proves
      d(C) >= 16 and so d >= 16 on all of span(S)^perp; the same test at 19 coordinates must find deficient subsets
      (d(C) = 16); plus an explicit vector of span(S)^perp of symplectic weight 16 outside the isotropic part (d <= 16).
  (B) gf3prep.py + subset_ea64.c at W = d - 1 = 15: for every 15-subset T of the 35 positions, every vector of
      span(S)^perp supported inside T lies in the isotropic part (exact GF(3) ranks), all C(35,15) = 3247943160
      subsets, uncapped; at W = 16 it must find subsets with a vector outside the isotropic part; plus witness.py's
      witness. Run 2256 ran (B) on the identical object (out/lead4_methodB.txt there: W = 15 none, W = 16 7762); this
      folder re-runs (B) on the rebuilt object in the background, one process at a time, and the claim cites
      whichever run finished, with its output file.
  Third, cited: bz64 (Brouwer-Zimmermann over GF(9), n <= 64) on the GF(9) generator matrix; fourth, cited: a
  no-search proof from the Goppa bounds of the head and zero-tail codes (formalist lens, degree-4 generalization of
  run 1953's goppa_x.py).
  Both exact checkers are re-tested before they judge the object (attempts/evaluator-first/tests/): known positive run
  1640's E_17 object (d = 11, counts 1735, 1745, 1731 at W = 11), known negative a seeded object with a planted
  low-weight word (W = 3 finds a subset; infoset at the planted level finds deficient subsets).

## Thresholds

1. Computed (n, k, c) = (35, 7, 14) with c >= 1.
2. d computed exactly = claimed d by (A) and (B), agreeing.
3. d > d_lower and d <= d_upper of the listed cell on a live one-GET re-read of https://eaqecc.codetables.de/qutrit.php
   right before claiming (scout: 15-26 at 2026-10-25T02:35:12Z).
4. Not implied, through the page's propagation rules, by any listed cell (teleportation cells excluded, as in runs
   1253, 1500, 1640, 1727, 1953 and 2256), any code in this repo, its open PRs (#363, #403-#405, #643, #645, #646,
   #651, #710), the literature found (already-settled lens; NOVELTY skeptic), or this workspace's other codes (E_m
   family, the packages 5713c745, 059282c3, 6df8f7ad, 64c0cbdd, every lead). A tie is not a win.
5. One cell per claim; propagated neighbours are listed as not claimed.

## Search space record

Every search records its exact family and whether it was exhausted (uncapped) or capped. Capped or sampled searches
are never used as exclusions.
