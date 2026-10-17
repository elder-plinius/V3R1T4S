# Run it yourself

## 1. Verify the claimed code `[[14, 3, 8; 5]]_3`

From this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (~2 seconds, Python 3 standard library only):

```text
VALID [[14, 3, 8; 5]]_3 (pure: d_non_iso=8, d_iso=8, s=16, dim_dual=12, dim_iso=6, non_iso_vecs=530712)
PASS
```

## 2. Rebuild the object from scratch

```sh
cc -O3 -o how-we-built-it/search_qc14_6_8 how-we-built-it/search_qc14_6_8.c
./how-we-built-it/search_qc14_6_8
python3 how-we-built-it/build_14_3_8_5.py
```

- `./how-we-built-it/search_qc14_6_8` searches 2-quasi-cyclic `[14, 6]_9` codes over `GF(9)[x]/(x^7 - 1)` using the reciprocal cubic factorization `x^7 - 1 = (x - 1)(x^3 + x^2 + 2)(x^3 + 2x + 2)` and prints the Hermitian self-orthogonal `[14, 6, 8]_9` code (`ell = 6`) on Hit #18 in `< 0.1s`.
- `python3 how-we-built-it/build_14_3_8_5.py` scales columns `[0, 1, 2]` by `4 = 1 + w in GF(9)^*` (reducing the Hermitian hull dimension from `ell = 6` to `ell = 3`), maps the code to the `16 x 28` canonical `GF(3)` symplectic stabilizer generator matrix `S`, and regenerates `object/qutrit_14_3_8_5.json` byte-for-byte (`sha256: 7b890c6f3a1b318ef4267bcaec58ec60823b19e6962e7d6f5c721dd3009186e5`).

## 3. Re-fetch the live table

```sh
curl -sS -A "V3R1T4S/1.0" https://eaqecc.codetables.de/qutrit.php | grep '14,3,[0-9-]*;5'
```
