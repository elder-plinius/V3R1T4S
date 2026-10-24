# Run it yourself (N = 743)

From this folder, in a fresh shell.

1. Standard-library check (no packages needed):

       sh verify-it-yourself/run_checks.sh

   Expected last line: PASS.

2. Full certificate (Python 3 with numpy, scipy and mpmath; gmpy2 optional, it only speeds up mpmath):

       python3 -I how-we-built-it/certify/certify.py check object/thomson_743.txt check_object.json

   Expected (how-we-built-it/expected/check_object.json): "E_mp30": "264837.4538033452076921018", "gT_mp30": "4.47655e-24", "n_eigs": 1483,
   "min_eig" about 4.042259, "hessian_pass": true.

3. Distinct basins: download the posted Riesz file
   https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/dat/points_743_1.dat (sha256
   68ac9c8deba352959b12b63fa04ea87aef2cfbb502fe44123437f3e860b3df9a) and the merged #125 object
   (known-knowns/thomson-problem-live-tables/2026-10-14-mrxmoex-grok-fleet-9293bcd2/object/cand_743.txt), then

       python3 -I how-we-built-it/certify/certify.py polish points_743_1.dat pol_riesz.json pol_riesz.txt
       python3 -I how-we-built-it/certify/certify.py polish cand_743.txt pol_m125.json pol_m125.txt

   Expected "E_star_mp30": 264837.5858503620609677129 and 264837.5287041150044362828, both above the object's energy.

4. Rebuild the object: how-we-built-it/search/ holds the GPU engine (thomson_bb.cu, nvcc -O3 -arch=sm_120) and the
   chain scripts; chain C of bh_chains.sh (PK 0.003, SIG 0.05, RNG seeds 2023001-2023010, seeded from the Riesz file)
   reached this basin at iteration 3 (search/chains.log); certify.py polish then gives the 30-digit object.
