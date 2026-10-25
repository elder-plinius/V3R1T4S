# Verification Receipts — `2026-10-22-mizopl-e47a7dd8` (`fmm-additive-complexity-records`)

## Command Executed
```sh
sh verify-it-yourself/run_checks.sh
```

## Deterministic Output (`< 0.5s` Wall-Clock on Apple M-Series CPU)
```text
VERIFIED: All 4 ternary SLP record schemes, upstream reference metadata, negative control, and 400 null controls passed.
PASS
```

## Summary of Machine-Verified Checks
1. **`object/CERTIFICATE.json` (`3,699` bytes, `sha256: 4a2e07b5d438be3327737929448819782885fb1eb1ba946acabeda846082cbb6`) & 4 Record Scheme Files in `object/schemes/`:**
   - Byte sizes and SHA-256 digests match `100%` (`4 / 4` files: `3x3x7_m49_cr167_cn404_ZT_reduced.json`, `3x5x6_m68_cr245_cn494_ZT_reduced.json`, `3x5x7_m79_cr294_cn520_ZT_reduced.json`, `5x6x6_m130_cr492_cn1697_ZT_reduced.json`).
   - Strictly acyclic DAG indices (`0 <= idx < cur_idx`) and strictly unit coefficients (`value in {-1, +1}`) verified across all `4 / 4` files (`cr_len == cr_val == complexity.reduced`).
   - Exact symbolic polynomial identity $C = A \cdot B$ over $\mathbb{Z}[A, B]$ verified across all output entries $(i, j)$ with `0` errors on all `4 / 4` files.
   - Credited Perminov source schemes (`3x3x7_m49_ZT.json`, `3x5x6_m68_ZT.json`, `3x5x7_m79_ZT.json`, `5x6x6_m130_c1697_ZT.json`), current `matmulcatalog` `adds` values (`+404`, `+482`, `+520`, `+1716`), and independent upstream tie metadata (`1781ca392cb26808f88e6f92a26894ab3727910f`) verified against `object/CERTIFICATE.json`.
2. **Upstream Reference Metadata (URLs & SHA-256 Hashes):**
   - Verified the URLs, byte sizes, and SHA-256 digests of `fmm_sota.json` (`2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`), `reduced_known.json` (`ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`), `matmulcatalog` `COVERAGE.md` (`c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`), and the 4 upstream `addition_reduced_ZT` reference files (`3x5x6_m70_cr252_cn561_ZT_reduced.json`, `3x5x6_m70_cr265_cn561_ZT_reduced.json`, `5x6x6_m130_cr499_cn1716_ZT_reduced.json`, `5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json`).
3. **Corrupted-Gate Negative Control & 400-Sample Null Model:**
   - Flipping a single gate sign in `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json` is immediately rejected by the symbolic polynomial verifier over $\mathbb{Z}[A, B]$.
   - `400` random greedy CSE controls (`seed = 20261022`) on `3x3x7` ($m = 49, \text{cn} = 404$) yield `best_control = 304`, `median = 336`, `IQR = 13` vs our `cr = 167` (`-137` below `best_control`).
