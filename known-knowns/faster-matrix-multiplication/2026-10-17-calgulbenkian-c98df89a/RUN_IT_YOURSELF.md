# Run It Yourself

## 1. Verify the Shipped Object (`object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json`)

From a fresh shell inside this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
== Checking object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json
sha256 matches INDEX.csv (c98df89a60c52bfd65c3266489f3cbef4a28715305d200e2a3f01334d1076429)
PASS: 2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json | format=2x4x7 m=45 cr=164 (U=27, V=64, W=73) fv=50 cn=282
cr 164 matches INDEX.csv
== Running negative control (mutated SLP coefficient must FAIL)
negative control rejected as expected
ALL CHECKS PASS
```

## 2. How to Rebuild `object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json`

From the V3R1T4S workspace root:

```sh
cc -O3 -pthread -o runs/2026-10-14-0312/attempts/c-evaluator-optimizer/code/cse_opt runs/2026-10-14-0312/attempts/c-evaluator-optimizer/code/cse_opt.c
python3 runs/2026-10-14-0312/attempts/representation-absorber/code/flip_cse.py
```
