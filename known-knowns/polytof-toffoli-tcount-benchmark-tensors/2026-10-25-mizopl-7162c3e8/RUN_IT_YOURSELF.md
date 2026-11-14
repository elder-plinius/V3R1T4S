# Run It Yourself (`2026-10-25-mizopl-7162c3e8`)

1. Ensure `python3` (`>= 3.9`) with `numpy` and `git` are available.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
   *(Optional: if you already have a local checkout of `https://github.com/ZIB-IOL/polytof.git` at commit `0dcac107d15adc34dc646242d222f21ae7d32699`, you may pass `POLYTOF_DIR=/path/to/polytof sh verify-it-yourself/run_checks.sh`.)*
3. `verify-it-yourself/run_checks.sh` checks out `ZIB-IOL/polytof` at pinned commit `0dcac107d15adc34dc646242d222f21ae7d32699`, verifies the commit hash, and runs `verify-it-yourself/verify.py`, which recomputes the entire `p3` audit from scratch in **`~4.3` seconds single-thread CPU time**:
   - Parses `docs/tensors.md` (`sha256: f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`) and checks all `88` reference tensors in `data/tensors/*.npy` and `88` basis transforms in `data/paper/transform/*.npy`, identifying the `2` qubit-dimension discrepancies (`0108`: actual $n=42$ vs table $46$; `0114`: actual $n=11$ vs table $12$).
   - Audits all `88` files in `data/paper/cpd/topp/*.npy` across all **`13,528` stored CP schemes** (`74` single-row files + `14` multi-row pool files containing `13 x 1,000 + 454 = 13,454` schemes) and all `9` bilinear files in `data/paper/cpd/base/*.npy` (`0525`..`0533`), confirming `13,537 / 13,537` valid CP schemes and `97 / 97` rank matches against `docs/tensors.md`.
   - Audits all `88` files in `data/paper/waring/*.npy` under the full phase-polynomial signature (`odd_cols == 0`, `odd_pairs == 0`, and cubic triples matching both BCO and original bases), confirming `88 / 88` valid Waring files, `83 / 88` matching `docs/tensors.md`, and `5 / 88` exceeding `docs/tensors.md` (`0105-00041.npy` at `41` vs `39`, `0108-00077.npy` at `77` vs `73`, `0115-00055.npy` at `55` vs `51`, `0728-00061.npy` at `61` vs `59`, and `0817-00063.npy` at `63` vs `59`).
   - Verifies the `4` shipped repaired Waring schemes (`object/waring/0105-00039.npy`, `object/waring/0108-00073.npy`, `object/waring/0115-00051.npy`, `object/waring/0817-00059.npy`) under the full signature in both BCO and original bases and verifies `object/p3_audit_certificate.json`, printing `PASS` as its final line.
