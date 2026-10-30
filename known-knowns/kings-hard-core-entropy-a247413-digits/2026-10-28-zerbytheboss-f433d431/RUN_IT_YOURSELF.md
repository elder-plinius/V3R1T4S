# Run It Yourself

Exact commands from this package folder in a fresh shell:

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

To re-run the full multi-lens high-precision solvers from `how-we-built-it/`:
```sh
python3 how-we-built-it/ctmrg_solver.py
python3 how-we-built-it/strip_prony_solver.py
```
