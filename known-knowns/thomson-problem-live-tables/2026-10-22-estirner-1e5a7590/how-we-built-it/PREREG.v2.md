# PREREG: thomson-problem-live-tables (run 2026-10-22-0154)

written: 2026-10-22T02:03:19Z (date -u), before any attack output of this run was scored, before claim/ was built and before the
sweep started.

null_test: not needed because every claim is an explicit object (N points) judged by a deterministic checker (mpmath energy, tangent Newton, Hessian spectrum) against fixed table and literature values; no search statistic, key or "beats chance" claim is made.

## Criterion (verbatim, bank/targets.json; also in target.md)

Success means N points on the unit sphere (coordinates to >= 20 digits) for some N <= 1500 listed in at least one live table, such that E* computed in mpmath at 30 digits from the normalized coordinates is STRICTLY LOWER (direction: min) than the minimum energy for that N over ALL of: Deeter's table (https://deetour.net/oppp/thomson/, N = 4..524), CCD Thomson/table.html, CCD Thomson2/table.html, the CCD Riesz s=1 table (site/s_1/index.html), the Wikipedia table and (for N = 282) EinsteinArena, each re-fetched live immediately before claiming, by at least 1e-6 in absolute energy, AND the configuration is a certified strict local minimum (mpmath tangent-space Newton to gradient norm < 1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0), AND it is a different basin from every posted table configuration for that N: polishing each table's own point file (Deeter e.<N>.txt, CCD xyz/<N>.xyz, Riesz dat/points_<N>_1.dat) with the same routine must give an energy higher than E* by >= 1e-6. N > 1500 (Riesz rows up to 9913) cannot be Hessian-certified in under an hour and is partial win p3 only.

## The judge (one checker for every N; tested before use)

attempts/exact-scorer-first/code/certify.py, copied unchanged from run 2026-10-21-2021 (sha256 recorded in that lens's
NOTES.md), with verify_stdlib.py as an independent standard-library cross-check of energy and gradient:
1. Read N x 3 coordinates as decimal strings; normalise each point in mpmath (mp.dps = 30).
2. E = sum_{i<j} 1/|x_i - x_j| in mpmath at mp.dps = 30.
3. Polish ("the routine", identical for every input): float64 L-BFGS, float64 tangent Newton to |g_T| < 1e-9, then
   tangent-space Newton in mpmath (dps 30) until the tangent-gradient 2-norm < 1e-20.
4. Hessian at the final point: float64 Riemannian Hessian in an orthonormal tangent basis, the 3 rotation generators
   projected out, (2N-3) x (2N-3); pass iff its smallest eigenvalue > delta = 10 * (2N) * 2.22e-16 * ||H||_F and the
   3 rotation Rayleigh quotients are below 1e-6 in size.
5. Distinct basin: the same polish on every posted table file fetched for that N (Riesz dat/points_<N>_1.dat, CCD
   Thomson xyz/<N>.xyz and Thomson2 xyz/<N>.xyz where they exist, listed or unlisted); each polished energy must exceed
   E* by >= 1e-6.
6. Margin: E* <= B(N) - 1e-6.
A claim needs all of 1-6. Any number in a claim sentence is copied from the judge's output on the saved file (not on
an in-memory point), rounded so that independent recomputations agree.

Checker tests before scoring: known positive, #125's N = 743 object certifies and reproduces 264837.5287041150 to
>= 12 significant digits; known negative, a 1e-3 rms perturbation (seed 1) of that object shows |g_T| > 1e-3 at the
file's point without polishing.

## The bars B(N) (frozen now; B never rises)

B(N) = the minimum of: every live table value for N (fetched 2026-10-22, scout.md), the polished energies of every
posted file for N (step 5), Roshal et al. 2015 (arXiv:1408.3473v2, data/roshal_1408.3473v2.txt), both columns of
Amore and Wales 2026 Tables 2-3 (arXiv:2610.08122), merged and open claims in this repository, and any lower value the
literature scan (attempts/leakage-and-settled) finds before a claim is built. At freeze time:

| N | B(N) at freeze | source |
|---|---|---|
| 743 | 264837.5287041150044362828 | merged V3R1T4S #125 (Riesz 264837.5858504) |
| 538 | 137830.1360893 | CCD Riesz s=1 |
| 620 | 183673.09953200 | Roshal 2015 / Amore-Wales Ref. column (Riesz 183673.0995320) |
| 660 | 208434.6161288 | CCD Riesz s=1 |
| 722 | 249926.1662872 | CCD Riesz s=1 |
| 739 | 261963.5020771 | CCD Riesz s=1 |
| 740 | 262680.38954930 | Roshal 2015 / Amore-Wales Ref. column (Riesz 262680.3895493) |
| 750 | 269904.2259635 | CCD Riesz s=1 |
| 753 | 272090.8085565 | CCD Riesz s=1 = Roshal 2015 |
| 755 | 273553.3317336 | CCD Riesz s=1 |
| 759 | 276490.0843822 | CCD Riesz s=1 |
| 780 | 292166.76583720 | Roshal 2015 / Amore-Wales Ref. column (Riesz 292166.7658373) |
| 900 | 390084.7556201 | CCD Riesz s=1 |
| 920 | 407784.83883230 | Roshal 2015 / Amore-Wales Ref. column (Riesz 407784.8388324) |
| 960 | 444368.4373480 | CCD Riesz s=1 |
| 540 | 138869.5942030 | CCD Thomson2 |
| 560 | 149480.8992800 | CCD Thomson2 |
| 582 | 161607.1761347 | CCD Thomson2 (= CCD Thomson unlisted xyz) |
| 942 | 427710.4477820 | CCD Thomson2 |

## N = 743 (the re-panel)

The object is runs/2026-10-21-2021/claim/object/thomson_743.txt (sha256
1e5a75909e58d1a4347aaaad37053aa7e22cd164f8da0d8fd26cc2870d78471b), unchanged. Only the claim sentence changes: the
tangent-gradient norm is quoted as the judge's value at the saved file, rounded to 3 significant digits. Every other
number is re-derived by this run's judge before the claim is built.

## Search (fixed now; anything may be used to search, only the judge scores)

- evaluator-throughput: GPU greedy seeded basin hopping (thomson_bb, FP32 Barzilai-Borwein relaxations, FP64
  re-ranking), per N three chains with (PK, SIG) = (0.005, 0.02), (0.010, 0.02), (0.003, 0.05), 10 iterations each
  of 12 rounds x 280 replicas x 6000 steps, seeded from the lowest posted file for N, fixed RNG seeds logged.
- symmetry-and-structure: seeds built from neighbouring sizes' posted files (add or delete points), relaxed in the
  same engine.
- optimizer: population or Metropolis acceptance on rows where greedy stalls above B(N).
- Per N, the object panelled is the lowest E* that this run's own search produced and the judge certified; other
  certified basins below B(N) are recorded in the dossier, not claimed. One object, one cell, one claim per run
  folder.

## Partial win p1 (also frozen)

For each posted file fetched for a sweep N: if the judge's polish moves its energy away from the posted table value by
more than 1e-6, that is a p1 table-integrity finding, reported with both energies to 12 digits.
