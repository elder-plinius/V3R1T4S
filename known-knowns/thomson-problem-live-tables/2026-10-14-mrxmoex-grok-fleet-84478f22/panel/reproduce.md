# REPRODUCE panel report — run 2026-10-14-0717

context: subagent (executor), fresh

Read only claim/ (README.md, A_1382, B_3552, C_550). I did not read or run the author's verify/ code. My own scripts are in panel/reproduce_work/ (rcheck.py, run_one.py). JSON outputs per file are in the same folder, along with all.log.

## Definition used (quoted from criterion.txt)
"E* computed in mpmath at 30 digits from the normalized coordinates" ... "certified strict local minimum (mpmath tangent-space Newton to gradient norm < 1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0)" ... "polishing each table's own point file ... with the same routine must give an energy higher than E* by >= 1e-6". E = sum_{i<j} 1/|x_i - x_j|.

## My method
- Energy: coordinate strings are parsed into mpmath at mp.dps = 30 and each point is renormalized at dps 30. All pairs are summed with mpmath.fsum, using 8 processes over row blocks and a final fsum.
- Gradient: points are taken as MPFR at 200 bits (gmpy2) and renormalized. Full Euclidean gradient over all j != i, then projected to the tangent plane (g - (x·g)x). The reported number is the 2-norm.
- Polish (my own routine): Riemannian Newton. Gradient and point update are in MPFR-200. The direction is solved from a float64 2N x 2N tangent Hessian (B_i^T (H - λ_i I) B_j with λ_i = x_i·g_i), with a rotation-mode penalty. Iterate until grad < 1e-20. There is no float64 L-BFGS prestage.
- Hessian: a float64 2N x 2N tangent Hessian, compressed onto the QR complement of the 3 rotation generators (dimension 2N-3), then eigvalsh. Error bound = (a-priori assembly rounding bound in Frobenius norm: 50·u·sqrt(N)·||entry magnitudes||_F, conservative) + 12·m·u·||A||_2 (eigensolver backward error) + 2·(orthogonality defect)·||A||_2. Cholesky of (M − λmin/2·I) is used as a second check. Label: NUMERICAL (float64 with a perturbation bound, not interval arithmetic). The bound is about 3.5e-7, and the margins are about 2.3 to 8.3, so the gap is 7 orders of magnitude.
- Sphere and duplicates: max | |x|−1 | of the raw file and minimum pairwise distance after normalization.
- Determinism: claim A's object run was repeated; the JSON outputs are byte-identical.

## Claim A — N = 1382 (full success criterion)
Object cand_1382.txt: sha256 84478f22…01ce2 matches claim.md. 1382 points, ≥ 41 significant digits, max | |x|−1 | 1.1e-16, minimum pair distance 0.0919, so no duplicates.
- E* (mp dps30) = 926576.0968589705350586982. This matches the claim exactly.
- Tangent gradient 2-norm (MPFR-200) = 5.79e-32, below 1e-20. Newton count 0, so E* does not change.
- Hessian: 2761 = 2N-3 non-rotational eigenvalues, 0 nonpositive. The three lowest are 8.309762476818, 8.423015403300 and 8.515333114111; the largest is 11293.18. Weyl bound 3.50e-7, so certified min ≥ 8.3097621 > 0, and the Cholesky check passes. The full 2N spectrum has 3 near-zero rotational values (|λ| ≤ 1.7e-11), then 8.3098.
- Provenance: polishing data/cand_1382_deep.txt with my routine gives 926576.0968589705350586982, identical to 25 digits (grad 8.1e-32).
- Distinct basins: I polished every posted file for N = 1382 with my routine.
  - data/points_1382_1.dat (Riesz): 926576.1030329535457256979, grad 4.5e-30, min eig 8.2268 > 0. Gap to E* is +6.1740e-3.
  - data/t2_1382.xyz (Thomson2): 926576.1175606784292504214, grad 7.7e-29, min eig 8.3660 > 0. Gap to E* is +2.0702e-2.
  - Both match the claimed polished values to every printed digit, and both gaps are ≥ 1e-6.
- Table minimum from the saved pages:
  - CCD Riesz s=1: 926576.1030330
  - CCD Thomson2: 926576.1175606
  - CCD Thomson table.html: no 1382 row (max 972)
  - Wikipedia: no 1382 row (max 470)
  - Deeter: "1382" does not appear
  - Minimum is 926576.1030330 − E* = 6.1740e-3 ≥ 1e-6.
- Caveats, outside REPRODUCE scope: I checked the "re-fetched live" requirement only from the saved pages and fetch log, not by fetching again. The claim.md does not list sha256 values for the two posted point files (Riesz dd3b546e…, Thomson2 b94e354f…), so I could not check them against anything; this is not a mismatch.
Verdict A: PASS

## Claim B — Riesz s=1, N = 3552 (p1 table integrity)
- Object riesz_3552_polished.txt: sha256 matches. Unit sphere 1.1e-16, minimum pair distance 0.0574. E (mp30) = 6191355.686643545416998382, which matches. Gradient 9.82e-22 < 1e-20.
- Posted data/points_3552_1.dat: raw E (mp30) = 6191355.686658502748579249, which matches. My Newton polish (grad 0.29 → 6e-4 → 2.3e-8 → 4e-15 → 9.5e-28) gives 6191355.686643545416998382, identical to the claimed polished value to 25 digits.
- Posted cell 6191355.6866585 − polished = 1.4955e-5 > 1e-6. Posted raw − polished = 1.4957e-5.
- I did no Hessian check, since none is required for p1.
Verdict B: PASS (reproduction of the numbers; whether this counts as p1 is for the CRITERION panelist)

## Claim C — Thomson2, N = 550 (p1 table integrity)
- Object t2_550_polished.txt: sha256 matches. Unit sphere 1.1e-16, minimum pair distance 0.146. E (mp30) = 144126.0927999992211787655, which matches. Gradient 2.8e-29. Hessian: 1097 non-rotational eigenvalues > 0, min 2.33198 (certified ≥ 2.331981622).
- Posted data/t2_550.xyz: raw E = 144126.0927999992211793093, which matches. My polish gives 144126.0927999992211787655, identical to the claimed value.
- Cell 144126.0927100 (saved Thomson2 page): polished − cell = +8.9999e-5 > 1e-6. The cell is lower than what its own coordinates reach. Whether a cell below the reachable energy satisfies p1 is a criterion question.
Verdict C: PASS (numbers reproduce)

## Overall
All claimed numbers reproduce independently and deterministically. Claim A meets every property within REPRODUCE scope.
pass: true
