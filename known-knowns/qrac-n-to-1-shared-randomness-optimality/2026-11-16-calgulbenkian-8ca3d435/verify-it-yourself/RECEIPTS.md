# Verification Receipts: 4-to-1 Qubit QRAC Optimality Certificate

## Object Verified
- **File**: `object/certificate_qrac4.json`
- **Size**: `98284` bytes
- **SHA-256**: `8ca3d435fdd22f906e7113aadfa38c09762836b6077d27a8b301a77e91847788`

## Verifier Script
- **File**: `verify-it-yourself/verify_qrac4.py` (`sha256: d6df73d68d6f2ddc2adb899039d6f7a60a1e98035408790160a4c1ee5aeac8c6`)
- **Runner**: `verify-it-yourself/run_checks.sh` (`sha256: 5d5d08f8414fb0ffca9608b0911b5dd3165989b545345d2dd5bed24f4d9a096a`)
- **Dependencies**: Python 3 standard library + `mpmath` (`mpmath.iv` outward-rounded interval arithmetic at `40` decimal digits / `> 130` bits)

## Clean-Copy Execution Output

Command executed from `attacks/qrac-n-to-1-shared-randomness-optimality/`:

```sh
sh verify-it-yourself/run_checks.sh
```

Exact output (`exit 0`, wall time `51.68 s`, peak RSS `26.5 MB`):

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

## Corrupted-Copy Semantic Rejection Output

Flipping the middle ASCII digit of `object/certificate_qrac4.json` (byte `49419`, changing `'0'` to `'1'`) and running `sh verify-it-yourself/run_checks.sh` exited with status `1` and exact output:

```text
Verification error (ValueError): AM-GM leaf exceeded tight bound: 0.7414825943474522493002325980174281417448
FAIL
```
