# Skeptic Panel Report — Role: NOVELTY

role: NOVELTY
context: fresh skeptic review of the packaged files only

## 1. Live Audit of Primary Tables and Precalculated Orders

All upstream repositories and tables referenced for `minimizer-density-record-tables` were fetched and hashed (recorded in `the-record-we-beat/minimizer_record_snapshot.md`):

1. **`OrensteinLab/Minimizers` Precalculated Lowest-Density Orders (`7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46`):**
   - **Master Table URL:** `https://raw.githubusercontent.com/OrensteinLab/Minimizers/7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46/lowest-density/binary/best-orders.csv` (`2026-11-07T15:17:50Z`, `HTTP 200`, `14,275,872` bytes, `sha256: 57a369a010498cb6ab3ba0bce73ed015980a11a8c8c29f09d537db34e3e32313`)
   - **Individual Rank File URL:** `https://raw.githubusercontent.com/OrensteinLab/Minimizers/7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46/lowest-density/binary/individual-orders/ranks/k4-w12.txt` (`2026-11-07T15:17:43Z`, `HTTP 200`, `58` bytes, `sha256: 9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877`)
   - **Published Order for `(w = 12, k = 4)` (UHS size 7):** `[3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6]`
   - **Exact Expected DNA Density:** `574,313,157 / 2^32 = 0.1337177020`.
2. **`OrensteinLab/10-minimizers` & `OrensteinLab/GreedyMini` (`916daebd399d15d061e2fd437326aee5cf0e7292` / `a67eb90dc278ea78111a76d5813cf2ac7662b0ae`):**
   - **Expected-Density Table URL:** `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv` (`2026-10-18T15:59:53Z`, `HTTP 200`, `1,644` bytes, `sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`)
   - **Precomputed `w12_k4.gm` URL:** `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM/w12_k4.gm` (`2026-10-18T15:59:54Z`, `HTTP 200`, `136` bytes, `sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`)
   - **Exact Expected DNA Density:** `584,312,429 / 2^32 = 0.1360458389` (listed as `0.136046`, the smallest listed value in `k_extension_k16_w12.csv`).

## 2. Literature, Trophy Case, and Pull Request Audit

- **Literature (`Bioinformatics` 2025, `WABI` 2026, arXiv `2506.05277v1`):** Neither Golan et al. (*Bioinformatics* 2025), Shur et al. (*WABI* 2026), nor `arXiv:2506.05277v1` reports a DNA minimizer order for $(w = 12, k = 4)$ below `574,313,157 / 2^32 = 0.1337177020`.
- **Repository Status:** The merged sibling package `known-knowns/minimizer-density-record-tables/2026-10-18-mizopl-dd85465d/` addresses cell $(w = 12, k = 3)$ (`0.1365689458`). For cell $(w = 12, k = 4)$, our earlier binary-projected `.gm` submission (`0.1336292920`, `-0.0661%` vs. `k4-w12.txt`) was closed because it did not reach the `<= 0.1330491` (`-0.5%` relative) bar against `OrensteinLab/Minimizers` `k4-w12.txt` (`0.1337177020`).
- **Threshold Verification:** `object/w12_k4_4ary.gm` (`sha256: 956170573df55e04f43e55c20d6bba0b134c9b8054a92f995428dc9df4410ddb`) achieves `570,244,411 / 2^32 = 0.1327703733`, which is **`-0.7085%` relative** below `0.1337177020` (`<= 0.1330491135`) and **`-2.4076%` relative** below `0.1360458389`.

pass: true
