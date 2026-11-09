# Run It Yourself

## 1. Verify `object/sol_m28_45037.json` in < 0.5 Seconds (Python Port)
From this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
This runs `verify-it-yourself/check_ihtp.py`, our standalone Python 3 standard-library port of the organisers' official `IHTP_Validator.cc` (Version 0.0, 23/05/24), confirming `Total violations = 0` and `Total cost = 45037` (`< 45873`).

## 2. Verify with the Organisers' Official C++ `IHTP_Validator.cc`
Compile and run the official C++ validator (`https://ihtc2024.github.io/assets/files/IHTP_Validator.cc`) against `m28.json` and `object/sol_m28_45037.json`:
```sh
g++ -O3 -std=c++17 IHTP_Validator.cc -o IHTP_Validator
./IHTP_Validator m28.json object/sol_m28_45037.json
```
Both validators report `Total violations = 0` and `Total cost = 45037`.

## 3. Rebuild or Further Polish with `how-we-built-it/IHTP_Polisher.cpp`
Compile and run the C++17 local search solver in `how-we-built-it/IHTP_Polisher.cpp` starting from the published `sol_m28.json`:
```sh
clang++ -O3 -std=c++17 -o IHTP_Polisher how-we-built-it/IHTP_Polisher.cpp
./IHTP_Polisher path/to/m28.json path/to/sol_m28.json object/sol_m28_45037.json 120 42
```
