# Skeptic Panel Report — Role: CRITERION

panelist: CRITERION
context: fresh skeptic review of the packaged files only
problem_id: minimizer-density-record-tables
confirmed_scope: An explicit 256-entry 4-ary DNA minimizer rank order object/w12_k4_4ary.gm (2,056 bytes, sha256 956170573df55e04f43e55c20d6bba0b134c9b8054a92f995428dc9df4410ddb) and companion CSV table object/w12_k4_4ary.csv (4,518 bytes, sha256 72557c44cc3c4b10d4735faeee9d6745f40872674c54118a311e258f775431d1) for (w, k) = (12, 4) with exact expected DNA density 570,244,411 / 2^32 = 0.1327703733 (density factor 1.7260148523), strictly lowering the smallest listed value in OrensteinLab/Minimizers lowest-density/binary/best-orders.csv (k4-w12.txt, 574,313,157 / 2^32 = 0.1337177020) by 0.7085% relative and lowering OrensteinLab/10-minimizers w12_k4.gm (584,312,429 / 2^32 = 0.1360458389) by 2.4076% relative.

## 1. Clause-by-Clause Success Criterion Audit

1. **Explicit minimizer order for a stated `(w, k)` pair, given as a complete rank file:**
   - Cell $(w, k) = (12, 4)$ is explicitly provided as `object/w12_k4_4ary.gm` (`2,056` bytes, `sha256: 956170573df55e04f43e55c20d6bba0b134c9b8054a92f995428dc9df4410ddb`) and companion CSV table `object/w12_k4_4ary.csv` (`4,518` bytes, `sha256: 72557c44cc3c4b10d4735faeee9d6745f40872674c54118a311e258f775431d1`), defining a strict permutation of `0..255` over all $4^4 = 256$ DNA 4-mers.
2. **DNA density computed with the repositories' own density measurement definition:**
   - Evaluated over all $4^{w+k} = 4^{16} = 4,294,967,296$ equiprobable DNA contexts of length $16$ under leftmost tie-breaking by two independent exact 4-ary de Bruijn transfer-matrix DP implementations in `verify-it-yourself/verify.py` (receipts in `verify-it-yourself/RECEIPTS.md`), yielding `570,244,411 / 2^32 = 0.1327703733` (density factor $(w+1) \cdot d = 1.7260148523$).
3. **Strictly lower than the smallest value listed for `(w = 12, k = 4)` across `OrensteinLab/Minimizers`, `OrensteinLab/10-minimizers`, and `OrensteinLab/GreedyMini` by at least `0.5%` relative:**
   - Against `OrensteinLab/Minimizers` `lowest-density/binary/best-orders.csv` / `k4-w12.txt` (`sha256: 9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877`, `574,313,157 / 2^32 = 0.1337177020`), our order reduces density by **`-0.7085%` relative** (`-4,068,746 / 2^32`, below the `0.5%` threshold `0.1330491135`).
   - Against `OrensteinLab/10-minimizers` `w12_k4.gm` (`sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`, `584,312,429 / 2^32 = 0.1360458389`) and `k_extension_k16_w12.csv` (`sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`, `0.136046`), our order reduces density by **`-2.4076%` relative** (`-14,068,018 / 2^32`).
4. **Same density definition and stated storage cost:**
   - Storage cost is stated and verified at `2,056` bytes in `.gm` 64-bit format (`8`-byte `size_t` header `256` + `256` `uint64_t` ranks), or `256` bytes as an unpacked 1-byte rank table, compared to `136` bytes in `.gm` format (`16` bytes unpacked) for binary-projected orders.

## 2. Null-Model Control Audit (`how-we-built-it/null_test.md`)

- Across `400` uniformly random 256-entry 4-ary permutations (`seed = 20261107`), sample mean density is `0.1538239179` (`660,668,696.60 / 2^32`), standard deviation is `0.0016707423` (`7,175,783.35 / 2^32`), and the minimum across all 400 controls is `0.1498304838` (`643,517,028 / 2^32`).
- `object/w12_k4_4ary.gm` (`0.1327703733`, `570,244,411 / 2^32`) sits at `z = -12.6013` below the random ensemble mean (`0 / 400` controls reaching `570,244,411`).

pass: true
