# Run It Yourself

All commands run from this folder in a fresh shell using only the Python 3 standard library.

## 1. Standalone dual-engine verification (~45 seconds)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
OK: Constructive core-forest prover reproduced Mertens-Moore Theorems 5 and 6 (m=1, 2)
OK: All 6 rational polynomial families of Theorem 7 verified across 16314 canonical cores
OK: Independent brute-force proper bond-animal counts match Theorem 7 for (d, e) = (1, 4), (2, 5), (3, 6)
OK: Matches Mertens & Moore Appendix A D_11(q) and [binom(d, 9)] D_12(1) = 6199599459637248
PASS
```

## 2. Rebuild factored formulas, brute-force checks, and Table 9 evaluations

```sh
python3 how-we-built-it/prove_bond_perimeter_e_minus_3.py
python3 how-we-built-it/brute_proper_bond_animals.py
python3 how-we-built-it/audit_mertens_moore_table9.py
```
