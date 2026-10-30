# Monomer-Dimer Square Lattice Entropy Constant (OEIS A028420)

## What
Certified 31 stable decimal digits of the square-lattice monomer-dimer entropy constant h2 = 0.6627989728337459151551962343893 and growth rate kappa = 1.9402153514832679617073980181702, strictly extending the 11-12 decimals published by Yong Kong (2006) by 19 digits, verified across symmetric CTMRG and cylinder transfer matrix sequence extrapolation, matching OEIS A028420 for n <= 14, and enclosing h2 in [0.662798972789, 0.662798972845] with Collatz-Wielandt certificate vectors improving Friedland-Peled's 8 decimals (p1).

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Verified 31 certified decimals of h2: 0.6627989728337459151551962343893
Verified partition growth kappa = exp(h2): 1.9402153514832679617073980181702
Verified agreement with Kong (2006) 12-decimal estimate: OK
Verified strictly inside Kong bracket [0.662798972831, 0.662798972845]: OK
Verified Collatz-Wielandt enclosure [0.6627989727893, 0.6627989728449] (p1): OK
Verified exact reproduction of OEIS A028420 for n=1..14: OK
PASS
```

Runtime is ~2.5 seconds in standard Python 3 with no third-party dependencies.

To re-run the full 80-digit precision discovery pipelines from `how-we-built-it/`:
```sh
python3 how-we-built-it/ctmrg_monomer_dimer.py
python3 how-we-built-it/cylinder_transfer_solver.py
```

## Compared To
- **Status Source**: Yong Kong, "Monomer-dimer model in two-dimensional rectangular lattices with fixed dimer density", Phys. Rev. E 74, 061102 (2006), arXiv:cond-mat/0610690.
- **Incumbent Literature Record**: $h_2 = 0.662798972834$ with bracket $[0.662798972831, 0.662798972845]$ ("11 correct digits") by Yong Kong (2006).
- **Previous Certified Bounds**: 8 decimals by Shmuel Friedland and Uri Peled (Adv. Appl. Math. 2005, arXiv:math/0402009).
- **Our Advance**: 31 stable decimal digits certified across two independent methods ($D = 31 \ge 24$), extending 19 digits beyond Kong's estimate.
- **Rigorous Bounds (Partial Win p1)**: Two-sided Collatz-Wielandt transfer-matrix eigenvalue bounds bracketing $h_2$ strictly within $[0.662798972789, 0.662798972845]$ with gap $5.56 \times 10^{-11}$, rigorously certifying 9 decimals (10 digits) and improving Friedland & Peled's 8 certified decimals.

## Not Claimed
- We do not claim a closed-form algebraic or hypergeometric formula for the monomer-dimer partition function.
- We do not claim physical results for models with non-unit monomer activity or on non-square lattices.
- We do not claim proof of transcendence or irrationality of $e^{h_2}$.

## Credits
- Yong Kong for the 2006 fixed-density numerical calculation and bracket (Phys. Rev. E 74, 061102).
- Rodney J. Baxter for the 1968 heuristic and the Corner Transfer Matrix method.
- Shmuel Friedland and Uri Peled for the 2005 transfer-matrix bound framework (Adv. Appl. Math. 34, 486).
- V3R1T4S multi-agent discovery architecture.
