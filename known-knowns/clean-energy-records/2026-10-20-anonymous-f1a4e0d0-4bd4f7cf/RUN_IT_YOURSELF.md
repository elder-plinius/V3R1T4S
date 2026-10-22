# Run it yourself
From this folder, fresh shell, Python 3:
    sh verify-it-yourself/run_checks.sh
Expected output:
    max_radius 1299.9999990000172 (limit 1300.0)  min_spacing 576.2929952098602 (limit 260.0)
    AEP 424131.95030 MWh (record 421561.89715)
    PASS
    PASS
With the official judge (needs numpy and pyyaml): download iea37-aepcalc.py, iea37-windrose.yaml and
iea37-335mw.yaml from https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2 into one folder,
copy object/iea37-v3r1t4s-opt16.yaml next to them, and run `python3 iea37-aepcalc.py iea37-v3r1t4s-opt16.yaml`;
the last line is 424131.9503 (official file sha256 ec2d16f237ed547fff3d44f314126b3889c000954f5a53ec3e14c28e5bc6b535).
Rebuilding the object (numpy, scipy, pyyaml; place the official cs1-2 files where how-we-built-it/iea37.py's DATA
path points, i.e. ../../../data/cs1-2 relative to the code):
1. `python3 multistart.py 16 40000 1000 ms16.jsonl 12` (random-start WEC + SLSQP; the start used was seed 4193,
   AEP 419007.11136; one start can be run alone with `multistart.py 16 1 4193 one.jsonl 1`).
2. Save that run's x, y as start2.json, then `python3 lns.py start2.json lns2 102 100000` under `capped.py 3600`
   (greedy LNS; reached 424131.95030 within 83 iterations and held it for 7406).
3. `python3 to_yaml.py lns2_best.json iea37-v3r1t4s-opt16.yaml`.
The LNS is seeded but SLSQP and floating-point order can differ across machines, so a rerun may end at a nearby layout.
