# PREREG: thomson-problem-live-tables, N = 743

written: 2026-10-21T20:27:28Z (date -u), before any attack output of this run was scored.

null_test: not needed because the claim is an explicit object (743 points) judged by a deterministic checker (mpmath energy, tangent Newton, Hessian spectrum) against fixed table values; no search statistic or "beats chance" claim is made.

## Criterion (verbatim, bank/targets.json; also in target.md)

Success means N points on the unit sphere (coordinates to >= 20 digits) for some N <= 1500 listed in at least one
live table, such that E* computed in mpmath at 30 digits from the normalized coordinates is STRICTLY LOWER (direction:
min) than the minimum energy for that N over ALL of: Deeter's table (https://deetour.net/oppp/thomson/, N = 4..524),
CCD Thomson/table.html, CCD Thomson2/table.html, the CCD Riesz s=1 table (site/s_1/index.html), the Wikipedia table
and (for N = 282) EinsteinArena, each re-fetched live immediately before claiming, by at least 1e-6 in absolute
energy, AND the configuration is a certified strict local minimum (mpmath tangent-space Newton to gradient norm <
1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0), AND it is a different basin from every posted table
configuration for that N: polishing each table's own point file (Deeter e.<N>.txt, CCD xyz/<N>.xyz, Riesz
dat/points_<N>_1.dat) with the same routine must give an energy higher than E* by >= 1e-6.

## The bar B (frozen now)

B = the minimum of:
- the live tables at N = 743 (fetched 2026-10-21T20:26Z, data/): CCD Riesz s=1 264837.5858504; Deeter, CCD
  Thomson, CCD Thomson2 and Wikipedia have no N = 743 row; CCD Thomson/xyz/743.xyz and Thomson2/xyz/743.xyz are 404;
- the merged repo claim #125 (known-knowns/.../2026-10-14-mrxmoex-grok-fleet-9293bcd2), INDEX value
  264837.5287041150044362828, object data/merged125_cand_743.txt;
- any lower N = 743 value the literature/PR scan (runs/2026-10-21-2021/literature_scan.md) finds (Roshal et al. 2015,
  Amore and Wales 2026, open PRs). If the scan finds a lower value, B drops to it; B never rises.

## The judge (one checker, written in attempts/exact-scorer-first/code/, tested before use)

1. Read 743 x 3 coordinates as decimal strings; normalise each point in mpmath (mp.dps = 30).
2. E = sum_{i<j} 1/|x_i - x_j| in mpmath at mp.dps = 30.
3. Polish ("the routine", identical for every input): float64 projected L-BFGS / Newton to tangent-gradient norm
   < 1e-9, then tangent-space Newton steps in mpmath (gradient at mp.dps = 30; step from the float64 tangent Hessian
   solve; retraction by renormalisation in mpmath) until the tangent-gradient 2-norm < 1e-20. Record E before and
   after; for the claimed object the change during the mpmath stage must be < 1e-12.
4. Hessian: float64 3N x 3N Euclidean Hessian at the polished point, mapped to the 2N-dim tangent space with an
   orthonormal tangent basis per point and the constraint term -(x_i . grad_i E) on each tangent block; then the 3
   rotation generators are projected out explicitly, leaving a (2N-3) x (2N-3) matrix. Pass iff its smallest
   eigenvalue > delta, where delta = 10 * (2N) * 2.22e-16 * ||H||_F (a Weyl-type bound on float64 assembly and
   eigensolver error). The 3 rotation Rayleigh quotients are reported as a sanity check (must be < 1e-6 in size).
5. Distinct basin: run the same polish on data/points_743_1.dat (Riesz) and on data/merged125_cand_743.txt (#125);
   each polished energy must exceed E* by >= 1e-6.
6. Margin: E* <= B - 1e-6.

A claim needs all of 1-6. The search (lens evaluator-throughput) may use anything; only this judge scores.

## Checker tests (before scoring any search output)

- Known positive: #125's object must certify (gradient < 1e-20, 2N-3 positive) and reproduce 264837.5287041150 to
  >= 12 significant digits.
- Known negative 1: the Riesz posted file must polish to >= B + 1e-6 (it is the table value, so it cannot beat B).
- Known negative 2: a random perturbation (1e-3 rms, seed 1) of #125's object before polishing must show a
  tangent-gradient norm > 1e-3 (not a stationary point) when checked without polishing.

## Partial win p1 (also frozen)

If polishing data/points_743_1.dat moves its energy away from the posted 264837.5858504 by more than 1e-6, that is a
p1 table-integrity finding, reported with both energies to 12 digits. Otherwise no p1 at 743.

## Search (lens evaluator-throughput), fixed now

GPU seeded basin hopping, FP32 descent and FP64 re-ranking, seeded from data/points_743_1.dat, with a hard time cap
and fixed RNG seeds recorded in the lens folder. The reviewer's round-2 object (storage/cache/round2/...) is used only
as a cross-check after this run's own search ends, never as a seed. The object panelled is the lowest E* that this
run's own search produced and the judge certified. One object, one cell.
