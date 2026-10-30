# Minimum-Comparison Selection — New Records for n=18

## What
Explicit certified comparison-selection algorithms for n=18 (ranks 6, 7, 8, 9) strictly beating both Hadian-Sobel and Gasarch-Kelly-Pugh 1996 Table 3, dual-verified by Cremer's static checker and pathcheck.py (Partial Win p2).

## Check it yourself
Run the standalone checker from this package folder:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output:
```
ALL 4 SELECTION DECISION GRAPHS VERIFIED: PASS
PASS
```

## Compared to
| Cell $(n, i)$ | Gasarch-Kelly-Pugh (1996) Table 3 | Hadian-Sobel Bound | Our Certified Worst-Case | Improvement |
|---|---|---|---|---|
| $(18, 6)$ | 32 | 32 | **31** | $-1$ comparison |
| $(18, 7)$ | 35 | 35 | **34** | $-1$ comparison |
| $(18, 8)$ | 37 | 38 | **35** | $-2$ comparisons |
| $(18, 9)$ | 37 | 41 | **34** | $-3$ comparisons |

## Not claimed
- We do not claim to have solved $V_6(17) \le 28$, $V_7(17) \le 29$, or $V_8(17) \le 30$.
- Ranks $i=5$ for $n=18$ remain at the known literature bound of 29 comparisons.

## Credits
- William Gasarch, Wayne Kelly, and William Pugh (1996) for the seminal small $(i,n)$ bounds and Table 3.
- J. Cremer (2026, arXiv:2610.18740) for the `df-pn+` poset decision graph proof-number search formulation.
