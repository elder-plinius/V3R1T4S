# Run It Yourself

## 1. Verify `object/sol_m28_45037.json` in < 0.5 Seconds
From this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
This runs `verify-it-yourself/check_ihtp.py`, an exact Python 3 standard library port of the official `IHTP_Validator.cc` (Version 0.0, 23/05/24), confirming `Total violations = 0` and `Total cost = 45037` (< 45873).

## 2. Rebuild or Further Polish with `IHTP_Polisher.cpp`
Compile and run the C++17 local search solver in `how-we-built-it/IHTP_Polisher.cpp`:
```sh
clang++ -O3 -std=c++17 -o IHTP_Polisher how-we-built-it/IHTP_Polisher.cpp
./IHTP_Polisher path/to/m28.json path/to/sol_m28_bks.json object/sol_m28_45037.json 120 42
```
