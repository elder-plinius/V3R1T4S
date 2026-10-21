# How we built it

## Files
- `search_qc14_6_8.c`: C search program over 2-quasi-cyclic `[14, 6]_9` codes in `<(x-1)> x <(x-1)> subset (GF(9)[x]/(x^7 - 1))^2` using the reciprocal factorization `x^7 - 1 = (x - 1)(x^3 + x^2 + 2)(x^3 + 2x + 2)`. Prints the Hermitian self-orthogonal (`ell = 6`) `[14, 6, 8]_9` seed on Hit #18 in `< 0.1s`.
- `build_14_3_8_5.py`: Applies Theorem 4 of Luo, Ezerman, Grassl, and Ling (`arXiv:2207.05647`) by scaling columns `[0, 1, 2]` of the `[14, 6, 8]_9` seed by `4 = 1 + w in GF(9)^*` (reducing the Hermitian hull dimension from `ell = 6` to `ell = 3`), maps the dual code to the canonical `16 x 28` `GF(3)` symplectic stabilizer generator matrix `S`, and writes `../object/qutrit_14_3_8_5.json`.
- `PREREG.md`: Pre-registration frozen before scoring.

## Commands (from the package root)
```sh
cc -O3 -o how-we-built-it/search_qc14_6_8 how-we-built-it/search_qc14_6_8.c
./how-we-built-it/search_qc14_6_8
python3 how-we-built-it/build_14_3_8_5.py
```
