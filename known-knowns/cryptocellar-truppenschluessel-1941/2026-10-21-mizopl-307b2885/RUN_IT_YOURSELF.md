# Run It Yourself — `2026-10-21-mizopl-307b2885` (`cryptocellar-truppenschluessel-1941`, Partial Win `p1`)

## 1. Fast Verification of Saved Certificate & Objects (`< 1` second)

```sh
sh verify-it-yourself/run_checks.sh
```

## 2. Full End-to-End C Solver Re-Execution (`~12–55` seconds on CPU)

To compile and run `how-we-built-it/p1_blind_garble_solver.c` from scratch against the language-model tables in `object/`:

```sh
cp object/hgnord_25_t*.bin .
arch -x86_64 clang -O3 -pthread how-we-built-it/p1_blind_garble_solver.c -o p1_blind_garble_solver -lm
./p1_blind_garble_solver
rm -f p1_blind_garble_solver hgnord_25_t*.bin p1_benchmark_certificate.json
```
