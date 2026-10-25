# Verification Receipts — `2026-10-22-mizopl-e47a7dd8` (`fmm-additive-complexity-records`)

## Command Executed
```sh
sh verify-it-yourself/run_checks.sh
```

## Deterministic Output (`< 0.5s` Wall-Clock on Apple M-Series CPU)
```text
VERIFIED: All 4 ternary SLP record schemes, 4 reference calibrations, negative control, and 400 null controls passed.
PASS
```

## Summary of Machine-Verified Checks
1. **`object/CERTIFICATE.json` (`2,847` bytes, `sha256: ede93f9030024c813dfb7ce8d1bdd3e3180fd2cdfab0691e552f30e81180b834`) & 4 Record Scheme Files in `object/schemes/`:**
   - Byte sizes and SHA-256 digests match `100%` (`4 / 4` files: `3x3x7_m49_cr167_cn404_ZT_reduced.json`, `3x5x6_m68_cr245_cn494_ZT_reduced.json`, `3x5x7_m79_cr294_cn520_ZT_reduced.json`, `5x6x6_m130_cr492_cn1697_ZT_reduced.json`).
   - Strictly acyclic DAG indices (`0 <= idx < cur_idx`) and strictly unit coefficients (`value in {-1, +1}`) verified across all `4 / 4` files (`cr_len == cr_val == complexity.reduced`).
   - Exact symbolic polynomial identity $C = A \cdot B$ over $\mathbb{Z}[A, B]$ verified across all output entries $(i, j)$ with `0` errors on all `4 / 4` files.
2. **Counter Calibration on 4 Live Reference Files (`the-record-we-beat/reference_live_champions/`):**
   - Verified `0` symbolic errors and exact agreement with Perminov's `complexity.reduced` and `complexity.naive` fields across all 4 reference files (`3x5x6` $m=70$: `252` & `265`; `5x6x6` $m=130$: `499` & `562`).
3. **Corrupted-Gate Negative Control & 400-Sample Null Model:**
   - Flipping a single gate sign in `3x3x7_m49_cr167_cn404_ZT_reduced.json` is immediately rejected by the symbolic polynomial verifier over $\mathbb{Z}[A, B]$.
   - `400` random greedy CSE controls (`seed = 20261022`) on `3x3x7` ($m = 49, \text{cn} = 404$) yield `best_control = 304`, `median = 336`, `IQR = 13` vs our `cr = 167` (`-137` below `best_control`).
