# How We Built It (`bivariate-bicycle-exact-distance-360-756` `p1`, `n = 504`)

## Pinned Requirements
- C++17 compiler (`clang++` or `g++`) for Stern/Dumer information-set decoding over `ker(H_X) \ rowspace(H_Z)` (`bb_isd_hunter.cpp`)
- `python3 >= 3.8` (standard library only) for exact `GF(2)` parity, rank, and logical non-triviality verification

## Exact Commands to Rebuild and Verify
```sh
c++ -O3 -std=c++17 how-we-built-it/bb_isd_hunter.cpp -o ./bb_isd_hunter
sh verify-it-yourself/run_checks.sh
```
