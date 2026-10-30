# Dimer Constant of the Cubic Lattice Z^3 — Rigorous Bounds

## What
Certified upper bound on the 3D cubic lattice dimer constant lambda_3 <= 0.452010 (strictly improving He 2026 Table 2 bound 0.452130 by 1.20e-4), certified monomer-dimer entropy bracket [0.7849602275, 0.7862023452], and certified Z^4 dimer constant upper bound lambda_4 <= 0.596949 (improving literature 0.6238 by 0.026851).

## Check it yourself
Run the standalone checker from this package folder:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output:
```
ALL CERTIFICATES VERIFIED: PASS
PASS
```
Runtime: < 1 second.

## Compared to
| Quantity | Published Literature | Our Certified Bound | Improvement | Citation |
|---|---|---|---|---|
| $\lambda_3$ (Cubic dimer constant) | $\le 0.452130$ | $\le 0.452010$ | $+1.20 \times 10^-4$ | Qidong He (arXiv:2607.28810, Aug 2026) |
| $h_3$ (3D monomer-dimer entropy) | $[0.7849602275, 0.7862023450]$ | $[0.7849602275, 0.7862023452]$ | Validated bracket | Friedland et al. (arXiv:math/0603001) |
| $\lambda_4$ ($\mathbb{Z}^4$ dimer constant) | $\le 0.6238$ | $\le 0.596949$ | $+0.026851$ | Literature upper bound |

## Not claimed
- We do not claim an exact closed form for $\lambda_3$.
- We do not evaluate cross-sections $(5,6)$ or $(6,6)$ ($> 300,000$ orbits).
- The lower bound $\lambda_3 \ge 0.441075$ (Csikvári 2016) is cited from literature.

## Credits
- Qidong He (arXiv:2607.28810) for diagonal layer transfer matrix formulation.
- Peter Csikvári (2016) for lower matching conjecture bounds.
- Per Håkan Lundow and Shmuel Friedland for monomer-dimer transfer methods.
