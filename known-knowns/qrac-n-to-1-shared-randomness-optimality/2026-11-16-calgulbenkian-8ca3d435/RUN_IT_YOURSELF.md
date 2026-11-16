# Run It Yourself (`qrac-n-to-1-shared-randomness-optimality`)

## 1. Verify the Saved Certificate

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Calibration checks (mpmath.iv, 40 dps):
  p(2) orthogonal = 0.853553390593273762
  p(3) orthogonal = 0.788675134594812882
  p(4) Ambainis   = 0.741481456572267072
Exact dyadic partition & interval verification:
  Total leaves verified : 43476
    AM-GM leaves (A)    : 32152
    Quadratic leaves (Q): 410
    Star leaves (H)     : 0
    Symmetry leaves (S) : 10914
  Split counts          : [11797, 8524, 9164, 7671, 6319]
  Max certified UB      : 0.741481799559635048
  Target threshold      : 0.741482 (0.741481 + 1e-6)
PASS
```

## 2. Rebuild the Certificate from Scratch

```sh
c++ -O3 -std=c++17 how-we-built-it/solve_qrac4_stereo.cpp -o ./solve_qrac4_stereo
./solve_qrac4_stereo ./rebuilt_qrac4.json
python3 verify-it-yourself/verify_qrac4.py ./rebuilt_qrac4.json
```
