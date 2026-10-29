# RECEIPTS: real output of verify-it-yourself/run_checks.sh

Run from this folder on 2026-10-23, 19:16:48Z to 19:21:57Z (date -u), Python 3.12 with torch 2.11 (CUDA) on one consumer GPU
(PYTHON set to that interpreter; no lock file). Output, unedited:

```
1. object hashes: ok (4 files)
2. config: ok ({"L": 10, "net": {"channels": 16, "blocks": 3, "kernel": 3}, "prior": "stripe", "irrep": "B1", "flip": true, "sym": true}, 14114 parameters, step 648)
3. local energies of 2048 saved configurations: mean diff -1.221e-15, max |diff| 3.695e-13, mean E_loc -253.803502
4. short fresh estimate (seed 9001, 16384 samples): E = -253.745421 +- 0.010240; claimed -253.753424; bar -253.668
PASS
```

Wall time (shell `time`): 5m9.201s.
