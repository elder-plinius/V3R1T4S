# Run It Yourself

## 1. Run the Dual-Language Verification Suite (`run_checks.sh`)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS`.

## 2. Run Each Standalone Verifier Directly

```sh
python3 verify-it-yourself/verify_python_exact.py object/certificate_b3_m11_s19_t3.json --corrupt-test
cc -O2 -std=c99 verify-it-yourself/verify_c99_int128.c -o ./verify_c99_int128 && ./verify_c99_int128 object/certificate_b3_m11_s19_t3.json --corrupt-test && rm -f ./verify_c99_int128
```
