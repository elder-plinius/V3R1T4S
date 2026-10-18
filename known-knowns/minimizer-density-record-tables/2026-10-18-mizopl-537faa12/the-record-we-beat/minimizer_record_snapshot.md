# Primary Record Snapshot — `minimizer-density-record-tables` at `(w = 12, k = 4)`

## 1. Live Fetches (`2026-10-18T15:59:53Z` – `2026-10-18T15:59:54Z`)

1. **`OrensteinLab/10-minimizers` Expected-Density Table (`the-record-we-beat/k_extension_k16_w12.csv`):**
   - URL: `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv`
   - Fetched UTC: `2026-10-18T15:59:53Z` (`HTTP 200`, `1,997` bytes, `sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`)
   - Column `4` ($w = 12, k = 4$):
     - `GreedyMini`: `0.136046`
     - `angle-based`: `0.138322748`
     - `decycling`: `0.143956`
     - `double decycling`: `0.145236`
     - `miniception`: `0.156164`
     - `mod-minimizer`: `0.156164`
     - `open-close-syncmer`: `0.156164`
2. **`OrensteinLab/10-minimizers` & `OrensteinLab/GreedyMini` Precomputed `w12_k4.gm` (`the-record-we-beat/published_w12_k4.gm`):**
   - URL 1: `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM/w12_k4.gm`
   - URL 2: `https://raw.githubusercontent.com/OrensteinLab/GreedyMini/main/minimizer%20loading%20example/w12_k4.gm`
   - Fetched UTC: `2026-10-18T15:59:54Z` (`HTTP 200`, `136` bytes, `sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`)
   - Rank vector (`16` `uint64_t`s): `[6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]`
   - Exact expected DNA density (`prob_gc_dna`): `584,312,429 / 2^32 = 0.1360458389`
