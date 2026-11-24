# Run it yourself
Fresh shell, from this package folder. Needs python3 (>= 3.9), gcc (or any cc with __int128) and pip access once.
```sh
sh verify-it-yourself/run_checks.sh             # 2-3 min, both precisions; last line: PASS
python3 verify-it-yourself/tamper_tests.py      # optional: 5 corrupted certificates, all must FAIL (~5 min)
```
Same steps as the e6b84d42 checker (V/M/W sieve vs pure Python for n <= 20000; admissible z_i; every term re-evaluated in arb, stated terms
must be >= recomputed (1e-15) and <= recomputed (1 + 1e-5); A(1e10) recomputed; total of the recomputed sups + head + tail < 2.1257395),
plus, for entries ending in "rho": own Selberg weights in arb, certified rounding |2^40 lambda_d - L_d| <= 1, exact per-modulus sums
(rhocount.c), identity sum_q P_q = (sum L)^2, lambda_1 = 1, sum|lambda| <= W/V, and Sigma <= (sum_q|P_q| + 2N sum|L| + N^2)/2^80.
The certificate field rho_levels (the author's own exact values) is not read by the checker. Formulas: object/proof.md.
To rebuild the object: how-we-built-it/COMMANDS.md.
