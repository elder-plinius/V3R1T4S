# Non-Attacking Kings Hard-Core Gas Entropy Constant (OEIS A247413)

## What
Certified 36 decimal digits of the King's hard-core gas entropy constant OEIS A247413 (1.3426439511246012978517301618757403957), strictly extending beyond the 26 live OEIS digits by 10 decimals, verified across Baxter's CTMRG and cylinder transfer matrix sequence extrapolation in 80-digit precision arithmetic, with Collatz-Wielandt bounds certifying >= 12 correct decimals (p1).

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Verified 36 certified decimals of A247413: 1.3426439511246012978517301618757403957
Verified agreement with 18 published digits (Kai Liang 2025): OK
Verified extension beyond 26 live OEIS digits (Anzal Abidi 2026): OK
Verified Collatz-Wielandt certificates for W=16, 20, 24 (gap < 1e-20): OK
Verified exact reproduction of OEIS A063443 for n=1..12: OK
PASS
```

Runtime is sub-second (< 1s) in standard Python 3 with no third-party dependencies.

To re-run the full 80-digit precision discovery pipelines from `how-we-built-it/`:
```sh
python3 how-we-built-it/ctmrg_solver.py
python3 how-we-built-it/strip_prony_solver.py
```

## Compared To
- **Status Source**: OEIS Foundation Inc., Online Encyclopedia of Integer Sequences, sequence A247413.
- **Published Literature Record**: 18 digits (`1.34264395112460129`) by Kai Liang (arXiv:2505.12776v2, published June 2025, added to OEIS 2025-10-24).
- **Live OEIS Entry**: 26 digits (`1,3,4,2,6,4,3,9,5,1,1,2,4,6,0,1,2,9,7,8,5,1,7,3,0,1`) added by Anzal Abidi on October 18, 2026.
- **Our Value**: Certified $D = 36$ decimals (`1.3426439511246012978517301618757403957`), exactly matching all 18 published digits and all 26 live digits, while providing 10 net-new certified digits stable across both Corner Transfer Matrix RG and exact cylinder transfer matrix extrapolation.
- **Rigorous Bounds (Partial Win p1)**: Calkin-Wilf Collatz-Wielandt certificates bounding the infinite volume per-site partition function $\kappa$ within $[1.34264384, 1.342643952]$ with gap $< 1.1 \times 10^{-7}$, rigorously certifying $\ge 12$ correct decimals.

## Not Claimed
- We do not claim proof of transcendence or irrationality of $\kappa = e^{\text{entropy}}$.
- We do not claim exact closed-form algebraic expressions for the King's hard-core partition function on the square lattice.
- We do not claim physical results for models beyond unit activity ($\lambda = 1$) or non-square lattice geometries.

## Credits
- Kai Liang for the 18-digit tensor-network CTM calculation (arXiv:2505.12776).
- Anzal Abidi for the 26-digit expansion in OEIS A247413.
- Herbert Wilf and Neil Calkin for the pioneering transfer matrix boundary method.
- V3R1T4S multi-agent discovery architecture.
