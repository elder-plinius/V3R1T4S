# Run It Yourself (`2026-10-22-mizopl-e47a7dd8`)

1. Ensure `python3` (`>= 3.8`, standard library only) is available in `PATH`.
2. From the root of this package directory (`known-knowns/faster-matrix-multiplication/2026-10-22-mizopl-e47a7dd8`), execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script executes `verify-it-yourself/verify.py`, which:
   - verifies `object/CERTIFICATE.json` (`3,699` bytes, `sha256: 4a2e07b5d438be3327737929448819782885fb1eb1ba946acabeda846082cbb6`), the URLs and SHA-256 digests of the upstream reference sources (`fmm_sota.json`, `reduced_known.json`, `matmulcatalog` `COVERAGE.md`, the 4 upstream `addition_reduced_ZT` reference files, and the 4 credited Perminov source schemes), and all **4 ternary (`ZT`) straight-line program `.json` files** in `object/schemes/` (byte sizes, SHA-256 digests, DAG acyclicity, strictly unit coefficients in $\{-1, +1\}$, exact symbolic polynomial equality $C = A \cdot B$ over $\mathbb{Z}[A, B]$, and exact reduced addition count `cr = cu + cv + cw`);
   - runs the corrupted-gate negative control on `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json` and the 400-sample random greedy CSE null control (`seed = 20261022`) on `3x3x7` ($m = 49, \text{cn} = 404$), and prints:
   ```text
   VERIFIED: All 4 ternary SLP record schemes, upstream reference metadata, negative control, and 400 null controls passed.
   PASS
   ```
   in `< 0.5` seconds on a standard laptop CPU.
