# How We Built It (`qrac-n-to-1-shared-randomness-optimality`)

## Pinned Requirements
- C++17 compiler (`clang++` or `g++`) for generating the certificate (`1.23 s`, `< 2 MB` RSS)
- `python3 >= 3.8` with `mpmath >= 1.3.0` (`mpmath.iv` outward-rounded interval arithmetic) for verification

## Exact Commands to Rebuild `object/certificate_qrac4.json`
```sh
c++ -O3 -std=c++17 how-we-built-it/solve_qrac4_stereo.cpp -o ./solve_qrac4_stereo
./solve_qrac4_stereo object/certificate_qrac4.json
sh verify-it-yourself/run_checks.sh
```
