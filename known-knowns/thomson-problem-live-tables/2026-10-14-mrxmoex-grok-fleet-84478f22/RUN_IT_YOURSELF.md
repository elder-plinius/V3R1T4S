# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Quick check (standard library only, ~10 s)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (see verify-it-yourself/RECEIPTS.md): the object sha256 84478f22..., `energy 926576.09685897053505869816...`, `margin 6.174029e-03`, `tangent_grad_2norm 5.789e-32`, last line `PASS`.

## 2. Full certificate (Newton, Hessian, distinct basin)

Needs Python 3 with numpy, scipy, numba, mpmath, gmpy2 (`pip install numpy scipy numba mpmath gmpy2`), about 3 GB RAM, about 1 minute per command on 8 cores.

```sh
python3 how-we-built-it/certify/hp.py object/cand_1382.txt check_A --newton 0 --hessian
```

Expected: `E_final_mpmath30 926576.0968589705350586982`, gradient 2-norm about 5.8e-32, `dim_nonrot 2761`, lowest non-rotational eigenvalues [8.30976..., 8.42301..., 8.51533...], `certified_min` about 8.3097624 (Weyl bound 4.2e-8), `num_nonpositive_nonrot 0`, `cholesky_half_shift_ok True`. Full record: how-we-built-it/expected/cand_1382_cert.json.

Distinct basin: download the two posted N = 1382 files and polish them with the same routine:

```sh
curl -o points_1382_1.dat https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/dat/points_1382_1.dat
curl -o t2_1382.xyz https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/xyz/1382.xyz
python3 how-we-built-it/certify/hp.py points_1382_1.dat check_R --prepolish --hessian
python3 how-we-built-it/certify/hp.py t2_1382.xyz check_T --prepolish --hessian
```

Expected: `926576.1030329535457256979` (+6.174e-3 above E*) and `926576.1175606784292504214` (+2.070e-2), records in how-we-built-it/expected/. The files we used had sha256 dd3b546e7b4c35d6415d3a47d4d284968d0baa11e2ffd988547b7b7676aa71d9 and b94e354f956d7e095589dfd2c95a88eaf1189d08af55a2ce41347936cd99bf50 (fetched 2026-10-14T07:21Z); the tables may have changed since.

## 3. Rebuild the object

The object is the pre-repair float64 file how-we-built-it/cand_1382_deep.txt (sha256 98c2839555f050e0b08092b03508a89b8c2f966abe664c87218b39abcf0037c0) polished in MPFR:

```sh
python3 how-we-built-it/certify/hp.py how-we-built-it/cand_1382_deep.txt rebuilt --prepolish --hessian
```

Expected: the same `E_final_mpmath30` to 25 digits. That file came from the search code in how-we-built-it/search/ (see how-we-built-it/README.md); the search is stochastic, so a rerun finds a basin like this one, not the same digits.
