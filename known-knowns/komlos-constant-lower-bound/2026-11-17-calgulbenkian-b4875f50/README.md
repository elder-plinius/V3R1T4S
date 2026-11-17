# Komlos Discrepancy Constant (`komlos-constant-lower-bound`, Partial Win `p2`): `15x15` Rational Matrix with Exact Discrepancy `2.05956508661 > 2.006`

## What

The stored rational 15x15 matrix object/komlos_15x15_p2.txt (integers over 10^12, all 15 column squared norms <= 1 exactly) has exact discrepancy 205956508661/10^11 = 2.05956508661 over all sign vectors, strictly above 2.006 and above 2, so it meets partial win p2 (and p1) but not the full criterion.

## Check it yourself

From this package folder (requires only Python 3 standard library and a C99 compiler `cc`):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (verifies `15` nonzero columns, exact rational squared Euclidean column norms at most `1`, and exact exhaustive discrepancy `205956508661 / 100000000000 = 2.05956508661 > 2.006` across all `2^15 = 32,768` sign vectors via three independent implementations: Python `Fraction` branch-and-bound, Python exhaustive Gray-code scan, and C99 `__int128` Gray-code enumeration).

## Compared to

- **Primary benchmark**: Terence Tao's Optimization Problems Repository, Constant `24a` (https://teorth.github.io/optimizationproblems/constants/24a.html)
- **Published reference (`p2`)**: Dmitriy Kunisky, *The discrepancy of unsatisfiable matrices and a lower bound for the Komlos conjecture constant*, SIAM J. Discrete Math. 37(2) (2023), pp. 586-603 (https://arxiv.org/abs/2111.02974, Section 1 reporting D. Spielman's unpublished 15-column bound in `[2.005, 2.006]`)
- **Fetched**: `2026-11-17T11:45:20Z` (`HTTP 200`, SHA-256 `1458e39fcaff828e69e3d8aa25ef155e8d3017a1435b73b166605b79a5c296ac` and `934ef00e9b10053c677da7f45738bedc8cbfd9383f25c0b89dba2ad7641ef32c`)

## Not claimed

- Does not beat Kunisky's asymptotic lower bound `C_24 >= 1 + sqrt(2) ~ 2.41421356` for the full dimension-free Komlos constant.
- Does not claim global optimality of `2.05956508661` over all `15x15` real matrices.

## Credits

- **Dmitriy Kunisky** (https://arxiv.org/abs/2111.02974), for the unsatisfiable matrix framework, the `4x4` non-tree regular seed (Example 2.2), recursive lifting `phi`, and convex second-order cone formulation (Lemma 4.2).
- **Daniel Spielman** (cited in https://arxiv.org/abs/2111.02974, Section 1), for the prior 15-column numerical lower bound in `[2.005, 2.006]`.
- **Terence Tao and contributors** (https://teorth.github.io/optimizationproblems/constants/24a.html), for curating Constant `24a`.
