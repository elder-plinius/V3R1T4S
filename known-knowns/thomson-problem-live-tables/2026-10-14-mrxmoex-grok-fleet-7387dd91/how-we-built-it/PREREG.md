# PREREG — run 2026-10-14-0717 (frozen 2026-10-14T07:17:57Z, from date -u)

Target: thomson-problem-live-tables. Criterion: copied verbatim in target.md (bank success_criterion, partial wins p1-p3).

## Statistic and checker
- Energy E = sum_{i<j} 1/|x_i - x_j| of the normalized points, computed in mpmath at mp.dps = 30 (and cross-checked at 50) over all pairs with mp.fsum.
- Tangent gradient: Riemannian gradient (Euclidean gradient projected onto each point's tangent plane), computed in mpmath at mp.dps = 50; reported as the 2-norm over all 3N components.
- Polisher ("the same routine" for distinct-basin tests): float64 L-BFGS (tools/fastpol.py, gtol 1e-12), then tangent-space Newton steps with the update direction solved from the float64 tangent Hessian and the gradient and energy evaluated in mpmath dps 50, stopping when the mpmath gradient 2-norm < 1e-20 (max 8 Newton steps).
- Hessian certificate: the full 3N x 3N Euclidean Hessian assembled in mpmath (dps 30) at the polished point, rounded to float64, projected onto the 2N-dim tangent space with the curvature term -(x_i . grad_i) I, rotations removed by an orthonormal basis of the complement of the 3 rotation generators (2N-3 dims). Certified positive if the smallest float64 eigenvalue minus (Frobenius norm of [mpmath Hessian - its float64 rounding, projected] + LAPACK backward-error bound 10*n*eps*||A||_2) is > 0 (Weyl), and also a float64 Cholesky of A - lambda_shift I succeeds (Rump-style margin). For N > 1500 (p3): ARPACK smallest eigenvalue of the float64 tangent Hessian (shift-invert or 'SA').
- Thresholds: candidate must be < min over all live tables by >= 1e-6; every posted file for that N polished with the same routine must end >= 1e-6 above E*. p1: posted energy minus mpmath-polished energy of the same posted file > 1e-6, both reported to 12+ digits.
- Tables re-fetched live once each immediately before building claim/: Deeter, CCD Thomson/table.html, CCD Thomson2/table.html, CCD Riesz s=1 index, Wikipedia (EinsteinArena only for N = 282).

## Hunt
- Warm defect-kick Metropolis basin hopping (T = 2e-3, ~200 hops per chain, 8 workers, restart from the warm start when a chain sits > 0.1 above its start), seeded from each table's own file; N in 530..582, 752, 942, 1152, 1500 and rows where Riesz and Thomson2 disagree; N = 513 from C2-symmetric seeds. Any new low gets the full certification above.

null_test: not needed because every claim is an explicit configuration checked by a deterministic energy/gradient/Hessian checker against live table values (no search statistic or "beats chance" claim).
