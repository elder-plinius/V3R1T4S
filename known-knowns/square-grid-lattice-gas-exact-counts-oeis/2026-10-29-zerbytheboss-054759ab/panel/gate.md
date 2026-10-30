# Honesty Gate — `square-grid-lattice-gas-exact-counts-oeis`

status: CONFIRMED_PARTIAL
confirmed_scope: Partial win p1: New world-record exact terms a(15) (43 digits) and a(16) (49 digits) of OEIS A054759 (square ice / Eulerian orientations on n x n torus), reproducing McKay (2024) a(1..14) exactly and converging to Lieb's constant; and Partial win p2: Row 28 extensions of rectangular tables A089980 (k=1..20) and A210662 (k=1..18). Full solution A028420(28) is in progress and not claimed.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (All 7 live OEIS b-file hashes verified; exact reproduction of McKay 2024 a(1..14); world records a(15) and a(16) verified with Lieb convergence < 0.48%; Row 28 base matches to Fibonacci and Pell; dual-solver parity and Freivalds audit verified on N=22 calibration).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (McKay published up to n=14 in 2024; a(15) and a(16) extend the sequence; live OEIS confirmed; zero competing PRs).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Verbatim satisfaction of p1 and p2; phantom A028420(28) solution claim retracted; claim level restricted to partial win p1 + p2).
- **Final Verdict**: CONFIRMED_PARTIAL (Partial wins p1 + p2 packaged for draft submission).
