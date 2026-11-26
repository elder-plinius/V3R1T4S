# Honesty gate (`hadamard-maxdet-records`)

- `target_id`: `hadamard-maxdet-records`
- `status`: `CONFIRMED_SOLUTION`
- `confirmed_scope`: Eight explicit n x n {+1,-1} matrices in object/M081.txt through object/M117.txt and object/hadamard_maxdet_8_records.json (sha256 ad8e212ac8397998c64702e7a9837dd048bf833df109520d01d713111b13b190) establish new record normalized determinants D_norm = |det(X)| / 2^(n-1) for orders n = 81 (200 * 20^39 vs 196 * 20^39, +2.0408%), n = 89 (226 * 22^43 vs 220 * 22^43, +2.7273%), n = 93 (243 * 23^45 vs 239 * 23^45, +1.6736%), n = 97 (264 * 24^47 vs 256 * 24^47, +3.1250%), n = 101 (7626 * 25^48 vs 7110 * 25^48, +7.2574%), n = 105 (7413 * 26^50 vs Rokicki's 2005 record, +8.0164%), n = 109 (309 * 27^53, +19.8565% above Rokicki's 2005 record and +6.1856% above merged V3R1T4S PR #155 at 291 * 27^53), and n = 117 (335 * 29^57 vs Rokicki's 2005 record, +5.3179%), each verified from scratch by fraction-free Bareiss elimination, 14-prime Chinese Remainder Theorem modular elimination, and SymPy Bareiss cross-check to lie strictly below Barba's n = 1 (mod 4) upper bound (as verified by our local 3-skeptic review panel), without claiming optimality on any of the eight orders.

## Gate notes

- Three independent skeptic audits (`panel/reproduce.md`, `panel/novelty.md`, `panel/criterion.md`) each inspected the clean package directory from scratch and ended `pass: true`.
- Every matrix was verified by three independent exact determinant routines (fraction-free Bareiss on Python `int`, 14-prime 61-bit CRT, and `sympy.Matrix.det(method='bareiss')`) and reconstructed bit-for-bit from its algebraic generator parameters in `object/hadamard_maxdet_8_records.json`.
- Both academic literature baselines (Farmakis-Kounias 1987, Orrick-Solomon 2003/2007, Rokicki 2005) and prior `V3R1T4S` claims (merged `PR #155` on `n = 109`, plus unmerged open `PR #539, #540, #541` on `n = 105, 109, 117`) are strictly exceeded.
