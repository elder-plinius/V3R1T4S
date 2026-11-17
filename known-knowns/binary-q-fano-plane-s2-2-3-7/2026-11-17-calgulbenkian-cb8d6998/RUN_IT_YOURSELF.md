# Run It Yourself

## 1. Run the Dual-Language Verification Suite (`run_checks.sh`)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS`.

## 2. Run Each Standalone Verifier Directly

```sh
python3 verify-it-yourself/verify_p2_py.py object/p2_240_planes_order5.txt
cc -std=c99 -O2 verify-it-yourself/verify_p2_c.c -o ./verify_p2_c && ./verify_p2_c object/p2_240_planes_order5.txt && rm -f ./verify_p2_c
```
