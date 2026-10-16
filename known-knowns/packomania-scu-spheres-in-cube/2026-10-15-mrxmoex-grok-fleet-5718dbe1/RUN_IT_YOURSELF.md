# Run it yourself, scu N = 507

From this folder, in a fresh shell:

0. `sh verify-it-yourself/run_checks.sh` (stdlib only), last line PASS. Real output: verify-it-yourself/RECEIPTS.md.
1. Live re-check: download https://packomania.com/scu/txt/scu507.txt and https://packomania.com/scu/txt/radius.txt, compare the sha256 with the-record-we-beat/SNAPSHOT.md, then
   `python3 how-we-built-it/mp_recheck.py scu507.txt radius.txt 507` (needs mpmath). Expected: `N=507 centres=507 r*=0.0659283580135823720729146228658 cell=0.065932119200351706079281328718 r*-cell=-3.761186769e-6`.
2. Rebuild the refined object: how-we-built-it/hunt3.py (numpy, scipy) runs SLP polishes from the posted file with small random perturbations; the kept file is the best of 8 trials (seeded by time, so a rebuild gives a slightly different but also short configuration).

Contributor text in HOW_WE_FOUND_IT.md is unverified narrative.
