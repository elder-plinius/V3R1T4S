# Run It Yourself

## 1. Verify `object/sol_m26_68496.json` in `< 0.5` Seconds
From this package root:
```sh
sh verify-it-yourself/run_checks.sh
```
This runs `verify-it-yourself/check_ihtp.py`, an exact Python 3 standard library port of the official `IHTP_Validator.cc` (Version 0.0, 23/05/24), confirming `Total violations = 0` and `Total cost = 68496` (`< 69730`).

## 2. Rebuild or Further Polish with `IHTP_Polisher.cc`
Compile and run the C++17 local search solver in `how-we-built-it/IHTP_Polisher.cc`:
```sh
clang++ -O3 -std=c++17 -o IHTP_Polisher how-we-built-it/IHTP_Polisher.cc
./IHTP_Polisher path/to/m26.json path/to/sol_m26_bks.json object/sol_m26_68496.json 120 42
```
