# Primary Record Snapshot — `minimizer-density-record-tables` at `(w = 12, k = 4)`

No third-party tables or precomputed minimizer files are copied into this directory; `verify-it-yourself/run_checks.sh` fetches them live and stops on a SHA-256 mismatch.

## 1. Live Fetches from `OrensteinLab/Minimizers` (`2026-11-07T15:17:43Z` – `2026-11-07T15:17:50Z`)

1. **`OrensteinLab/Minimizers` Lowest-Density Binary Order for `(w = 12, k = 4)` (`k4-w12.txt`):**
   - Pinned Commit URL (`7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46`): `https://raw.githubusercontent.com/OrensteinLab/Minimizers/7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46/lowest-density/binary/individual-orders/ranks/k4-w12.txt`
   - Fetched UTC: `2026-11-07T15:17:43Z` (`HTTP 200`, `58` bytes, `sha256: 9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877`)
   - Rank vector (UHS size 7): `[3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6]`
   - Exact expected DNA density (`prob_gc_dna`): `574,313,157 / 2^32 = 0.1337177020` (required `>= 0.5%` relative threshold: `<= 571,441,591 / 2^32 = 0.1330491135`)
2. **`OrensteinLab/Minimizers` Master Table (`lowest-density/binary/best-orders.csv`):**
   - Pinned Commit URL (`7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46`): `https://raw.githubusercontent.com/OrensteinLab/Minimizers/7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46/lowest-density/binary/best-orders.csv`
   - Fetched UTC: `2026-11-07T15:17:50Z` (`HTTP 200`, `14,275,872` bytes, `sha256: 57a369a010498cb6ab3ba0bce73ed015980a11a8c8c29f09d537db34e3e32313`)
   - Row for `k = 4, w = 12`: `4,12,"['0111', '0110', '0010', '0000', '0101', '1110', '1111']","[3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6]",7`

## 2. Live Fetches from `OrensteinLab/10-minimizers` & `OrensteinLab/GreedyMini` (`2026-10-18T15:59:53Z` – `2026-10-18T15:59:54Z`)

1. **`OrensteinLab/10-minimizers` Expected-Density Table (`k_extension_k16_w12.csv`):**
   - Pinned Commit URL (`916daebd399d15d061e2fd437326aee5cf0e7292`): `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv`
   - Fetched UTC: `2026-10-18T15:59:53Z` (`HTTP 200`, `1,644` bytes, `sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`)
   - Column `4` ($w = 12, k = 4$):
     - `GreedyMini`: `0.136046` (smallest listed value in `k_extension_k16_w12.csv`)
     - `angle-based`: `0.138322748`
     - `decycling`: `0.143956`
     - `double decycling`: `0.145236`
     - `miniception`: `0.156164`
     - `mod-minimizer`: `0.156164`
     - `open-close-syncmer`: `0.156164`
2. **`OrensteinLab/10-minimizers` & `OrensteinLab/GreedyMini` Precomputed `w12_k4.gm`:**
   - Pinned Commit URL 1 (`10-minimizers`, `916daebd399d15d061e2fd437326aee5cf0e7292`): `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM/w12_k4.gm`
   - Pinned Commit URL 2 (`GreedyMini`, `a67eb90dc278ea78111a76d5813cf2ac7662b0ae`): `https://raw.githubusercontent.com/OrensteinLab/GreedyMini/a67eb90dc278ea78111a76d5813cf2ac7662b0ae/minimizer%20loading%20example/w12_k4.gm`
   - Fetched UTC: `2026-10-18T15:59:54Z` (`HTTP 200`, `136` bytes, `sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`)
   - Rank vector (`16` `uint64_t`s): `[6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]`
   - Exact expected DNA density (`prob_gc_dna`): `584,312,429 / 2^32 = 0.1360458389`
