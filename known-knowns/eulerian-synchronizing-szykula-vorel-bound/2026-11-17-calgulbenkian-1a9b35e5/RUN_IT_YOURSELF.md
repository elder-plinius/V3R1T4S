# Run It Yourself

## 1. Run Both Independent Referees (`run_checks.sh`)

From the root of this submission package (requires only Python 3 standard library and a C99 compiler `cc`):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS` (executes in under `0.5` seconds).

## 2. Run Each Standalone Verifier Directly

```sh
python3 verify-it-yourself/verify_python_set_bfs.py object/eulerian_n7_k5_rt24.json
cc -O2 -std=c99 verify-it-yourself/verify_c_bitmask.c -o ./verify_c_bitmask && ./verify_c_bitmask object/eulerian_n7_k5_rt24.json && rm -f ./verify_c_bitmask
```
