# Run it yourself, N = 550

From this folder, in a fresh shell:

0. `sh verify-it-yourself/run_checks.sh` (stdlib only), last line PASS. Real output: verify-it-yourself/RECEIPTS.md.
1. Full certificate (needs numpy, scipy, numba, mpmath, gmpy2). Fetch the posted file 550.xyz (Thomson2) from https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/xyz/550.xyz (sha256 3ec7218c52bac398c2d02080a76049813adeb4ae01db38b5bee489e017ef8382), then:
   `python3 how-we-built-it/certify/hp.py <posted 550.xyz> check_C --prepolish --hessian`
   expected: E_raw_mpmath30 144126.0927999992211793093, E_final_mpmath30 144126.0927999992211787655, certified_min about 2.332 (how-we-built-it/expected/t2_550_polished.json).
   Use a relative output name, not a system temp path.
2. Rebuild the object: run the command in step 1 on the posted file (or see how-we-built-it/README.md).

Contributor text in HOW_WE_FOUND_IT.md is unverified narrative.
