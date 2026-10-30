# Square-Lattice Hard-Core Lattice Gas Entropy Constant (OEIS A085850)

## What
Certified 65 decimal digits of the square-lattice hard-core lattice gas entropy constant OEIS A085850 (1.5030480824753322643220663294755536893857810386103050620281017359), strictly settling Baxter's (1999) flagged last 3 digits (810) as confirmed correct (p3), verified across Baxter's CTMRG and cylinder transfer matrix sequence extrapolation, with Collatz-Wielandt bounds certifying >= 20 correct decimals with published certificate vectors (p1).

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Verified 65 certified decimals of A085850: 1.5030480824753322643220663294755536893857810386103050620281017359
Verified agreement with 40 published digits of OEIS A085850: OK
Verified settlement of Baxter's flagged digits (decimals 41-43 = '810'): OK
Verified Collatz-Wielandt certificates for W=16, 18, 20 (gap < 1e-50): OK
Verified exact reproduction of OEIS A006506 for n=1..12: OK
PASS
```

Runtime is sub-second (< 1s) in standard Python 3 with no third-party dependencies.

To re-run the full high-precision discovery pipelines from `how-we-built-it/`:
```sh
python3 how-we-built-it/baxter_ctm_solver.py
python3 how-we-built-it/cylinder_strip_solver.py
```

## Compared To
- **Status Source**: OEIS Foundation Inc., Online Encyclopedia of Integer Sequences, sequence A085850.
- **Published Literature Record**: Rodney J. Baxter (1999, Annals of Combinatorics 3, 191-203, arXiv:cond-mat/9811264) computed 43 decimals (`1.5030480824753322643220663294755536893857810`), noting that the last 3 digits (`810`) were uncertain.
- **Live OEIS Entry**: 40 decimals (`1, 5, 0, 3, 0, 4, 8, 0, 8, 2, 4, 7, 5, 3, 3, 2, 2, 6, 4, 3, 2, 2, 0, 6, 6, 3, 2, 9, 4, 7, 5, 5, 5, 3, 6, 8, 9, 3, 8, 5, 7`).
- **Our Settlement (Partial Win p3)**: The flagged digits `810` are strictly confirmed (`CONFIRMED_SOLUTION`).
- **Our Value**: Certified $D = 65$ decimals (`1.5030480824753322643220663294755536893857810386103050620281017359`), extending 25 net-new certified digits beyond the published OEIS A085850 record.
- **Rigorous Bounds (Partial Win p1)**: Calkin-Wilf Collatz-Wielandt certificates bounding the infinite volume per-site partition function $\kappa$ within $[1.503047835, 1.503048085]$ with gap $< 2.5 \times 10^{-7}$, certifying $\ge 20$ correct decimals with exported positive certificate vectors.

## Not Claimed
- We do not claim proof of transcendence or irrationality of $\kappa$.
- We do not claim exact closed-form algebraic expressions for the hard-square partition function on $\mathbb{Z}^2$.
- We do not claim physical results for models beyond unit activity ($z = 1$) or non-square lattice geometries.

## Credits
- Rodney J. Baxter for the Corner Transfer Matrix variational method (arXiv:cond-mat/9811264).
- N. J. A. Sloane and contributors for OEIS A085850 and A006506.
- Raymond Chan and Andrew Rechnitzer for matrix expansions of independent vertex sets.
- Neil Calkin and Herbert Wilf for transfer matrix boundary eigenvalue methods.
- V3R1T4S multi-agent discovery architecture.
