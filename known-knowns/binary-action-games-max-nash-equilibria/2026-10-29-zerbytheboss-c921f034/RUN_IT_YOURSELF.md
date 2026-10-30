# Run It Yourself — Certified 37-Equilibrium 4-Player Binary-Action Game

## 1. Verify the Certificate
From this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

The checker runs in $< 0.2$ seconds using only Python 3 standard library (`json`, `fractions.Fraction`, `itertools`).
The final line of output is:
```text
PASS
```

## 2. Rebuild the Objects from Scratch
To re-run the exact rational support enumeration solver from first principles:

```sh
python3 how-we-built-it/solve_exact_support.py
```

This regenerates:
- `object/certified_37_equilibria.json`
- `object/payoff_table_64.json`
