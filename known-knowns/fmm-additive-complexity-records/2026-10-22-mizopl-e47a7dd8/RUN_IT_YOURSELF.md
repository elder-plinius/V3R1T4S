# Run It Yourself (`2026-10-22-mizopl-e47a7dd8`)

1. Ensure `python3` (`>= 3.8`, standard library only) is available in `PATH`.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script executes `verify-it-yourself/verify.py`, which:
   - verifies `object/CERTIFICATE.json` (`26,573` bytes, `sha256: e47a7dd88e8f9778d65667b7d4030ca66cf39c6de9d89b3b0f1c5f61cb9cc1de`) and all **48 ternary (`ZT`) straight-line program `.json` files** in `object/schemes/` (byte sizes, SHA-256 digests, DAG acyclicity, strictly unit coefficients in $\{-1, +1\}$, exact symbolic polynomial equality $C = A \cdot B$ over $\mathbb{Z}[A, B]$, and exact reduced addition count `cr = cu + cv + cw`);
   - calibrates the counter across all **36 live reference champion `.json` files** in `the-record-we-beat/reference_live_champions/`;
   - runs the corrupted-gate negative control and the 400-sample random greedy CSE null control (`seed = 20261022`), and prints:
   ```text
   VERIFIED: All 48 ternary SLP schemes, 36 reference calibrations, negative control, and 400 null controls passed.
   PASS
   ```
   in `~2.0` seconds on a standard laptop CPU.
