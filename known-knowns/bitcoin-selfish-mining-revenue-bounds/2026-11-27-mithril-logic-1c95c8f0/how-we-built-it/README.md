# How we built it
Contributor text, unverified. Files:
- CLAIM.md: the claim as it went to the panel, including the derivation of the two corrections (written for the claim folder, so its paths say certs/ and code/).
- REPRODUCE_claim_folder.md: the same commands in claim/ folder layout; in this package use RUN_IT_YOURSELF.md instead.
- PREREG.md: the frozen rule (null_test: not needed because the claim is an explicit certificate checked by a deterministic exact checker).
- code/ssp.py, roots.py, mkcert.py (numpy builder: Gauss-Seidel on the label-collapsed stochastic-shortest-path form, modes under / printed / corrected / max), code/verify_compensation.py (exact identity, Monte Carlo and last-exit series for the two corrections; needs numpy; ~20 s).
- regenerate.sh: rebuild the big files; LARGE_FILES.md: their names, sizes and sha256.
- logs/: the outputs quoted in CLAIM.md (calibration roots, sanity gains, float roots, build log, and the contributor's own run_checks output).
Commands (from this folder): python3 code/roots.py 0.45 95 under 0.6 0.75 1e-6 (calibration, SSZ 0.66891); python3 code/roots.py 0.45 2000 max 0.67005 0.67008 1e-10 (root, about 80 s); python3 code/verify_compensation.py.
