# Skeptic Panel Report — Role: CRITERION

panelist: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
problem_id: minimizer-density-record-tables
confirmed_scope: An explicit binary-projected DNA minimizer rank order object/w12_k4_improved.gm (136 bytes, sha256 537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4, rank vector [15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]) for (w, k) = (12, 4) with exact expected DNA density 573,933,439 / 2^32 = 0.1336292920, strictly lowering the smallest listed value for expected DNA density 584,312,429 / 2^32 = 0.1360458389 across OrensteinLab/10-minimizers and OrensteinLab/GreedyMini by 1.776274% relative at identical 136-byte storage cost.

## 1. Clause-by-Clause Success Criterion Audit

The problem's verbatim `success_criterion` requires four cumulative conditions. Each was independently audited and verified via `verify-it-yourself/author_checker_minimizer_check.py` (invoked by `verify-it-yourself/run_checks.sh`):

### Clause (1): Explicit minimizer order for a stated `(w, k)` pair, given as a complete rank file
- **Target parameters:** `(w, k) = (12, 4)`.
- **Binary rank file:** `object/w12_k4_improved.gm` (`136` bytes on disk, `sha256: 537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4`). Unpacking via `load_vector_from_file` (`size_t` header = `16`, followed by `16` `uint64_t` values) yields the exact 16-entry permutation of `0..15`:
  `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]`.
- **CSV rank file:** `object/w12_k4_improved.csv` (`129` bytes, `sha256: e542885cc0668c8fa166514faccbba226ccaa833fc352df9d5b17aaf2537078b`), mapping binary 4-mers `0000..1111` to the identical rank vector `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]`.
- **Verdict on Clause (1):** Satisfied.

### Clause (2): DNA density computed with the repositories' own density measurement definition
- **Exact `prob_gc_dna` / `density_expected_dna` (`OrensteinLab/GreedyMini/code/density_and_gc.cpp` at pinned commit `a67eb90dc278ea78111a76d5813cf2ac7662b0ae`, verified by `verify-it-yourself/author_checker_minimizer_check.py`):**
  - Upstream `w12_k4.gm` (`136` bytes, `sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`, rank vector `[6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`):
    `prob_gc_dna = 584,312,429 / 2^32` (`pure_bin = 5,785` binary gamechangers contributing `379,125,760` DNA windows, plus `spec_dna = 205,186,669` tied-minimum DNA windows), giving `density_expected_dna = 0.1360458389`.
  - `object/w12_k4_improved.gm`:
    `prob_gc_dna = 573,933,439 / 2^32` (`pure_bin = 5,454` binary gamechangers contributing `357,433,344` DNA windows, plus `spec_dna = 216,500,095` tied-minimum DNA windows), giving `density_expected_dna = 0.1336292920`.
- **Independent 4-ary de Bruijn transfer-matrix DP over all `4^16 = 4,294,967,296` DNA contexts:**
  - Expanding `object/w12_k4_improved.gm` to all `4^4 = 256` DNA 4-mers produces the exact same 256-entry rank permutation whether secondary ties are broken by full `2k`-bit integer `kmer` (`OrensteinLab/10-minimizers` `GreedyMiniScheme`) or by low-bit `k`-mer `even(kmer)` (`OrensteinLab/GreedyMini` `density_and_gc.cpp`), because `object/w12_k4_improved.gm` is a strict permutation of `0..15` with no primary rank ties between distinct binary 4-mers.
  - Exact 4-ary transfer-matrix DP yields `284,674,764` prefix gamechangers + `289,258,675` suffix gamechangers = `573,933,439` total gamechangers (`573,933,439 / 2^32 = 0.1336292920`), matching `prob_gc_dna` to the single integer window.
- **Verdict on Clause (2):** Satisfied.

### Clause (3): Strictly lower than the smallest value listed for `(w = 12, k = 4)` across `10-minimizers` and `GreedyMini` by at least `0.5%` relative
- **Listed baselines for `(w = 12, k = 4)` (recorded in `the-record-we-beat/minimizer_record_snapshot.md`):**
  - `GreedyMini` (upstream `w12_k4.gm` exact): `584,312,429 / 2^32 = 0.1360458389` — our order reduces density by **`-1.776274%` relative** (`-10,378,990` gamechanger windows out of `4,294,967,296`).
  - `GreedyMini` (`k_extension_k16_w12.csv` rounded): `0.136046` (smallest listed value in `k_extension_k16_w12.csv`) — **`-1.776390%` relative**.
  - `angle-based` (`k_extension_k16_w12.csv`): `0.138322748` — **`-3.393119%` relative**.
  - `decycling` (`k_extension_k16_w12.csv`): `0.143956` — **`-7.173517%` relative**.
  - `double decycling` (`k_extension_k16_w12.csv`): `0.145236` — **`-7.991619%` relative**.
  - `miniception`, `mod-minimizer`, `open-close-syncmer` (`k_extension_k16_w12.csv`): `0.156164` — **`-14.430155%` relative**.
- **Additional baselines computed by us from upstream scheme definitions (not listed in `k_extension_k16_w12.csv`):**
  - `One-zero` / `10-minimizer` (our own exact 4-ary DP computation): `587,686,897 / 2^32 = 0.1368315185` (or `606,522,331 / 2^32 = 0.1412169847` under binary-only tie-breaking) — **`-2.340270%` to `-5.373074%` relative**.
  - `ABB+` (our own exact 4-ary DP computation): `591,473,886 / 2^32 = 0.1377132456` (or `591,565,027 / 2^32 = 0.1377344660`) — **`-2.965549%` to `-2.980499%` relative**.
- The relative reduction against the smallest listed value (`0.1360458389` / `0.136046`) is `1.776274%`, exceeding the `0.5%` relative threshold by `3.55x`.
- **Verdict on Clause (3):** Satisfied.

### Clause (4): Same density definition and stated storage cost
- **Density definition:** Exact expected DNA density over all `4^(w+k) = 4^16 = 2^32` DNA windows of length `16`, matching `k_extension_k16_w12.csv` and `OrensteinLab/GreedyMini`'s `density_expected_dna`.
- **Storage cost:** Explicitly stated and verified at `136` bytes on disk in `.gm` format (`8`-byte `size_t` header `16` + `16` `uint64_t` entries, identical to upstream `w12_k4.gm`), or `64` bits (`16 x 4` bits) of rank permutation information.
- **Verdict on Clause (4):** Satisfied.

## 2. Hidden Quantifier, Structural Seam, and Null-Model Controls

1. **Binary vs. DNA Density Seam Verification:**
   - On binary sequences (`2^16 = 65,536` windows), upstream `w12_k4.gm` has binary density `8,989 / 65,536 = 0.1371612549` and `object/w12_k4_improved.gm` has binary density `8,975 / 65,536 = 0.1369476318`.
   - `OrensteinLab/GreedyMini` searches only against binary `prob_gc` and assigns sentinel rank `16` to 9 of the 16 binary 4-mers (`[6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]`), leaving all interior-vs-suffix ties unoptimized for DNA secondary-bit resolution (`spec_dna`). Optimizing directly against `prob_gc_dna` over full permutations of `0..15` (`how-we-built-it/sos_dna_optimizer.cpp`) resolves this seam.
2. **Null-Model Control (`400` Uniformly Random Permutations of `0..15`, `seed = 20261018`):**
   - Sample mean `prob_gc_dna`: `657,087,819.02 / 2^32` (`0.1529901798`)
   - Sample standard deviation: `42,916,544.55 / 2^32` (`0.0099922867`)
   - Sample minimum across 400 random permutations: `575,257,827 / 2^32` (`0.1339376501`)
   - Sample maximum across 400 random permutations: `794,107,635 / 2^32` (`0.1848925918`)
   - `0 / 400` random permutations reach or beat `object/w12_k4_improved.gm` (`573,933,439`), which sits at `z = -1.9376` below the random permutation mean (`1,324,388` windows below the best of 400 random trials).
3. **Pairwise Swap Neighborhood Control (All `120` Single-Swap Neighbors of `object/w12_k4_improved.gm`):**
   - Across all `120` permutations at Cayley swap distance `1` from `object/w12_k4_improved.gm`:
     - `0 / 120` achieve a strictly lower `prob_gc_dna` than `573,933,439` (confirming that `object/w12_k4_improved.gm` is a local minimum in the swap neighborhood).
     - `41 / 120` neighbors tie at `573,933,439` (reflecting the inactive high-rank plateau for binary 4-mers with high ranks that never become window minima).
     - `79 / 120` neighbors have strictly higher `prob_gc_dna`, up to `723,017,601 / 2^32 = 0.1683406534` (`+149,084,162` windows), with neighborhood mean `590,154,620.32 / 2^32 = 0.1374060801`.

pass: true
