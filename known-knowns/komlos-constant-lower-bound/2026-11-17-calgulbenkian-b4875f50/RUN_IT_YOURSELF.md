# Run It Yourself

## 1. Run the Standalone Verification Suite (`run_checks.sh`)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS`.

## 2. Run Each Independent Checker Directly

```sh
python3 verify-it-yourself/check_komlos_py.py object/komlos_15x15_p2.txt
cc -O3 -std=c99 verify-it-yourself/check_komlos_c.c -o ./check_komlos_c && ./check_komlos_c object/komlos_15x15_p2.txt && rm -f ./check_komlos_c
```
