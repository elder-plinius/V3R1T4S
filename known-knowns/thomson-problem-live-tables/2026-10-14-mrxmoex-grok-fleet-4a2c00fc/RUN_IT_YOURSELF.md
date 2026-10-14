# Run it yourself, N = 3552

From this folder, in a fresh shell:

0. `sh verify-it-yourself/run_checks.sh` (stdlib only), last line PASS. Real output: verify-it-yourself/RECEIPTS.md.
1. Full certificate (needs numpy, scipy, numba, mpmath, gmpy2). Fetch the posted file points_3552_1.dat from https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/dat/points_3552_1.dat (sha256 837f6c84ee9c1a7c8e70776a2dc3b7b74e0ec9bf1e30510cf19d28932155bcb0), then:
   `python3 how-we-built-it/certify/hp.py <posted points_3552_1.dat> check_B --prepolish`
   expected: E_raw_mpmath30 6191355.686658502748579249 and E_final_mpmath30 6191355.686643545416998382 (how-we-built-it/expected/riesz_3552_polished.json).
   Use a relative output name, not a system temp path.
2. Rebuild the object: run the command in step 1 on the posted file (or see how-we-built-it/README.md).

Contributor text in HOW_WE_FOUND_IT.md is unverified narrative.
