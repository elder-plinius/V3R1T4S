# Run it yourself, scu N = 83

From this folder, in a fresh shell:

0. `sh verify-it-yourself/run_checks.sh` (stdlib only), last line PASS. Real output: verify-it-yourself/RECEIPTS.md.
1. Live re-check: download https://packomania.com/scu/txt/scu83.txt and https://packomania.com/scu/txt/radius.txt, compare the sha256 with the-record-we-beat/SNAPSHOT.md, then
   `python3 how-we-built-it/mp_recheck.py scu83.txt radius.txt 83` (needs mpmath). Expected: `N=83 centres=83 r*=0.116284441837827490267325191419 cell=0.116285160418976515059766617287 r*-cell=-7.18581149e-7`.
2. Rebuild the refined object: how-we-built-it/hunt3.py (numpy, scipy) runs SLP polishes from the posted file with small random perturbations; the kept file is the best of 8 trials (seeded by time, so a rebuild gives a slightly different but also short configuration).

Contributor text in HOW_WE_FOUND_IT.md is unverified narrative.
