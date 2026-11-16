# How We Built It (`gf2-polymult-8term-25-products` `p2`, `0x89`)

## Pinned Requirements
- C++17 compiler (`clang++` or `g++`) for bilinear split + BP/RNBP synthesis (`gf2m_deep_hunter.cpp`)
- `python3 >= 3.8` (standard library only) for exhaustive `16,384`-pair truth-table verification

## Exact Commands to Rebuild and Verify
```sh
c++ -O3 -std=c++17 how-we-built-it/gf2m_deep_hunter.cpp -o ./gf2m_deep_hunter
sh verify-it-yourself/run_checks.sh
```
