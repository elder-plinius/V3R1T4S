# Run It Yourself

## 1. Run the Standalone Exact Rational Referee Verifier

From a fresh shell inside this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Dependencies**: Python 3.8+ standard library (`fractions`, `decimal`, `json`, `argparse`, `collections`); also runs 60-digit `mpmath.iv` interval checks automatically when `mpmath` is installed.
- **Runtime**: ~1.5 seconds on one CPU core (< 40 MB RAM).
- **Expected final line**: `PASS`.

## 2. What the Checker Verifies

1. Calibrates against the exact `(2, 3, 3)` Weyl-Heisenberg MUB optimum `1/2 * (1 + 1/sqrt(3)) = 0.78867513459...`, the `(3, 3, 3)` 3-MUB baseline, and negative non-PSD matrix traps.
2. Verifies in `fractions.Fraction` that all `78` `L_b D_b L_b^T` blocks are unit lower-triangular with `D_b >= 0`, assembles `Z = sum_b B_b^T L_b D_b L_b^T B_b` over the `203` reduced Naimark words with zero projectivity relation on `C^3`, checks that all `2,418` non-constant cyclic trace moments and the `Tr_H(I_H)` coefficient equal `0` identically, and confirms `3 * c_V + sum_x c_{R,x} = 4368312591 / 6250000000 = 0.69893001456 <= 699 / 1000`.
