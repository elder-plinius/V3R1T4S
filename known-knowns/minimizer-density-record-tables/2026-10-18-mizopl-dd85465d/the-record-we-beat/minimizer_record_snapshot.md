# Primary Record Snapshot — `minimizer-density-record-tables` at `(w = 12, k = 3)`

No third-party tables or precomputed minimizer files are copied into this directory; `verify-it-yourself/run_checks.sh` fetches them live and stops on a SHA-256 mismatch.

## 1. Live Fetches (`2026-10-18T17:27:39Z`)

1. **`OrensteinLab/10-minimizers` Expected-Density Table (`k_extension_k16_w12.csv`):**
   - URL (`main`): `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv`
   - Pinned Commit URL (`916daebd399d15d061e2fd437326aee5cf0e7292`): `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv`
   - Fetched UTC: `2026-10-18T17:27:39Z` (`HTTP 200`, `1,644` bytes, `sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`)
   - Column `3` ($w = 12, k = 3$):
     - `angle-based`: `0.138389448` (smallest listed value across all methods)
     - `GreedyMini`: `0.138843`
     - `decycling`: `0.150863`
     - `double decycling`: `0.150863`
     - `mod-minimizer`: `0.222468`
2. **`OrensteinLab/10-minimizers` Precomputed `w12_k3.gm`:**
   - URL (`main`): `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM/w12_k3.gm`
   - Pinned Commit URL (`916daebd399d15d061e2fd437326aee5cf0e7292`): `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/GM/w12_k3.gm`
   - Fetched UTC: `2026-10-18T17:27:39Z` (`HTTP 200`, `72` bytes, `sha256: c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d`)
   - Rank vector (`8` `uint64_t`s): `[8, 2, 8, 8, 0, 4, 1, 3]`
   - Exact expected DNA density (`prob_gc_dna`): `149,082,035 / 2^30 = 0.1388434647`
