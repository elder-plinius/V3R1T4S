# Run it yourself
From this folder, fresh shell, Python 3:
    sh verify-it-yourself/run_checks.sh
Expected output:
    max_radius 2999.999999000001 (limit 3000.0)  min_spacing 567.6913085779892 (limit 260.0)
    AEP 1539447.11737 MWh (record 1526474.80248)
    PASS
    PASS
With the official judge (needs numpy and pyyaml): download iea37-aepcalc.py, iea37-windrose.yaml and
iea37-335mw.yaml from https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2 into one folder,
copy object/iea37-v3r1t4s-opt64.yaml next to them, and run `python3 iea37-aepcalc.py iea37-v3r1t4s-opt64.yaml`;
the last line is 1539447.11737 (official file sha256 ec2d16f237ed547fff3d44f314126b3889c000954f5a53ec3e14c28e5bc6b535).
Rebuilding the object (numpy, scipy, pyyaml; place the official cs1-2 files where how-we-built-it/iea37.py's DATA
path points, i.e. ../../../data/cs1-2 relative to the code): polish_par12.py (repair + SLSQP of participant 12),
then `python3 lns.py par12_polished_64.json lns64_s2 2 1000` (greedy LNS, ~45 min, reached 1539277.66707), then
`python3 lns2.py lns64_s2_best.json lns2_int1 501 2600 40` (annealed LNS, reached 1539447.11737). The search depends
on wall-clock time through its time budget, so a rerun can end at a different (usually nearby) layout.
