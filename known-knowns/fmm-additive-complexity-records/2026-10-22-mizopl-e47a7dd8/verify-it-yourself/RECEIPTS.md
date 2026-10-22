# Verification Receipts — `2026-10-22-mizopl-e47a7dd8` (`fmm-additive-complexity-records`)

## Command Executed
```sh
sh verify-it-yourself/run_checks.sh
```

## Deterministic Output (`~2.0s` Wall-Clock on Apple M-Series CPU)
```text
VERIFIED: All 48 ternary SLP schemes, 36 reference calibrations, negative control, and 400 null controls passed.
PASS
```

## Summary of Machine-Verified Checks
1. **`object/CERTIFICATE.json` (`26,573` bytes, `sha256: e47a7dd88e8f9778d65667b7d4030ca66cf39c6de9d89b3b0f1c5f61cb9cc1de`) & 48 Scheme Files in `object/schemes/`:**
   - Byte sizes and SHA-256 digests match `100%` (`48 / 48` files).
   - Strictly acyclic DAG indices (`0 <= idx < cur_idx`) and strictly unit coefficients (`value in {-1, +1}`) verified across all `48 / 48` files (`cr_len == cr_val == complexity.reduced`).
   - Exact symbolic polynomial identity $C = A \cdot B$ over $\mathbb{Z}[A, B]$ verified across all output entries $(i, j)$ with `0` errors on all `48 / 48` files.
2. **Counter Calibration on 36 Live Reference Champion Files (`18` Formats in `the-record-we-beat/reference_live_champions/`):**
   - Verified `0` symbolic errors and exact agreement with Perminov's `complexity.reduced` and `complexity.naive` fields across all 36 reference files (`2x4x7: 168`, `2x5x5: 147`, `4x5x8: 466`, `4x6x7: 468`, `5x5x6: 411`, `5x5x8: 555`, `5x6x6: 499`, `5x6x7: 577`, `5x7x7: 694`, `3x3x6: 153`, `4x4x8: 339/340`).
3. **Corrupted-Gate Negative Control & 400-Sample Null Model:**
   - Flipping a single gate sign in `2x4x7_m45_cr157_cn345_ZT_reduced.json` is immediately rejected by the symbolic polynomial verifier over $\mathbb{Z}[A, B]$.
   - `400` random greedy CSE controls (`seed = 20261022`) on `2x4x7` ($m = 45, \text{cn} = 345$) yield `best_control = 262`, `median = 281.0`, `IQR = 9.0` vs our `cr = 157` (`-105` below `best_control`).
