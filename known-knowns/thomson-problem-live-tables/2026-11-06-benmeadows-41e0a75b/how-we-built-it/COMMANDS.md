# Commands

The search ran in a sandbox where `/work` was the lane's workspace; paths below are as the lane used them.

1. Starts: Deeter's posted point files were downloaded to `/work/starts/<N>_deeter.npy` from
   `https://deetour.net/oppp/thomson/e.<N>.txt` (the lane's download scripts are not included; they only fetch and
   convert those files).
2. Neighbour scan (the "pairC" run, targets 436-467, three tries per move): `python3 src/pairscan.py` and its variants
   `pairscan2.py`, `pairscan3.py`, `pairscan5.py`, which differ in target ranges and try counts. The exact command line
   was not logged; the run's output is `runs/pairC.log`. `src/thomson.py` holds the shared energy, gradient, relax
   and hole-finding routines.
3. Refine (float64): `python3 src/refine.py 436.txt` (projected L-BFGS, then a float64 tangent Hessian check).
4. Certify (mpmath Newton, Hessian, table-file polish), with the live table files downloaded beside it:
   `python3 src/certify.py 436_refined.txt 90020.71608562 obj436 e.436.txt deeter 436.xyz xyz`, then again on its
   output `obj436_certified.txt`, which is `object/thomson-436.txt`.

Requirements: `requirements.txt` (numpy, scipy, mpmath); the checker in `verify-it-yourself/` needs only Python 3
(numpy optional for the Hessian part).
