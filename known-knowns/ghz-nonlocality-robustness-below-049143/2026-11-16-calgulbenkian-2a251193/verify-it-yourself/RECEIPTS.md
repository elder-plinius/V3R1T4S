# Verification Receipts: Three-Qubit GHZ Nonlocality Robustness (`18 x 24 x 72`)

## Object Verified
- **File**: `object/bell_ghz3_18x24x72.json`
- **Size**: `2725` bytes
- **SHA-256**: `2a251193be2909afcb89ec74c13e10ef52aadf6b4cad148b6f82f7e4221a4b68`

## Verifier Suite
- **Main driver**: `verify-it-yourself/verify_ghz3.py` (`14619` bytes, `sha256: 99877a5a4697021f48ae2946e57dbb496f91346c8412ba0dcd65ed73d00e4d0e`)
- **Independent Orbit Certifier A**: `verify-it-yourself/certify_orbits_a.cpp` (`12676` bytes, `sha256: 81a7e7e9ed35bace4896926a1a52cf5481fd4459adad37081c1c5ca1c695a798`)
- **Independent Orbit Certifier B**: `verify-it-yourself/certify_orbits_b.cpp` (`14218` bytes, `sha256: 498a7feaa8fa8e94ad80bac71b8552d6245cbf6624b6b743b185a99442040558`)
- **Runner**: `verify-it-yourself/run_checks.sh` (`204` bytes, `sha256: c12e609765fafcfc785963e3891df6b0202682f08704930d1ae9cb6e831a1276`)
- **Dependencies**: Python 3 standard library + `mpmath` (`mpmath.iv` outward-rounded interval arithmetic at `55` decimal digits) + standard C++17 compiler (`clang++` or `g++`, max 2 threads)

## Clean-Copy Execution Output

Command executed from `attacks/ghz-nonlocality-robustness-below-049143/`:

```sh
sh verify-it-yourself/run_checks.sh
```

Exact output (`exit 0`, wall time `22.48 s`, peak RSS `129.5 MB`):

```text
Calibration checks (mpmath.iv, 55 dps + C++ brute-force vs orbit):
  Mermin 2x2x2 v*       = 0.5
  Impl A & B small-grid = PASS (2x2x2, 6x8x24, 8x12x24, 9x6x18)
Independent exact symmetry-reduced orbit enumerations (18 x 24 x 72):
  Alice C_36 / D_36     = 7286 / 3771 orbits
  Bob C_48              = 349536 orbits
  Orbit pairs checked   = 1318100256 (covering 2^42 = 4,398,046,511,104 strategies)
  Exact L (Impl A, min) = 130692616 (4.93414s)
  Exact L (Impl B, max) = 130692616 (13.9812s)
Quantum expectations & critical visibility (mpmath.iv, 55 dps):
  Q_noise               = 0 (exact)
  Q_GHZ                 = [265961302.907030467068957871517, 265961302.907030467068957871517]
  Certified v* interval = [0.4913971114274656713239021, 0.4913971114274656713239021]
  Record beaten         = 0.49143 (arXiv:2310.20677v3 Table III; target <= 0.49142)
PASS
```

## Corrupted-Copy Semantic Rejection Outputs

1. **Middle-digit corruption test** (mutating byte `1631` of `object/bell_ghz3_18x24x72.json`, `'4' -> '1'`):
   `exit 1`, exact output:
   ```text
   Verification error (ValueError): gamma_pi_fractions[64] = 61/72 != 64/72
   FAIL
   ```

2. **Weight-digit corruption test** (mutating byte `2201` inside `w_int`, `'6' -> '1'`):
   `exit 1`, exact output:
   ```text
   Verification error (ValueError): Claimed Q_GHZ_45d does not match recomputed 55-digit GHZ expectation
   FAIL
   ```
