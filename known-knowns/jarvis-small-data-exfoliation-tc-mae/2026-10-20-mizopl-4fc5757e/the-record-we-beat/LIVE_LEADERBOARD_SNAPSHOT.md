# Live NIST JARVIS-Leaderboard Status Snapshot (`jarvis-small-data-exfoliation-tc-mae`)

## 1. Primary Live Status Pages Fetched & Verified

| Benchmark Task | Live Status Page URL | UTC Fetch Timestamp | HTTP Status | Size (Bytes) | SHA-256 Checksum of Fetched HTML | Live #1 Model & Test MAE | Frozen CLSS Test MAE (Relative Gain / $h_{90\%}$) |
| :--- | :--- | :--- | :--- | ---: | :--- | :--- | :--- |
| **`dft_3d_exfoliation_energy` (Claimed Primary)** | `https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy/` | `2026-10-20T21:43:03Z` | `HTTP/2 200` | `169,881` | `a32c745dc8c71293b3deb66d12cd505d5a8664d808e0935b51e541cd74bf0cd5` | `matminer_xgboost`: **`40.887 meV/atom`** (`matminer_rf`: `42.7554`) | **`28.195924 meV/atom`** (`-31.04%`, $h_{90\%} = 11.132579\text{ meV/atom}$) |
| **`tinnet_N_ead` (Supplementary; `p1` Dropped)** | `https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/tinnet_N_ead/` | `2026-10-20T21:43:04Z` | `HTTP/2 200` | `170,439` | `f8b00af347359b3da3ad3965f1f349dd47f0a187fd6c8632bdb065b675b9c1a7` | `alignn_model`: **`0.0871 eV`** (`N = 327`, 13 entries) | **`0.068908 eV`** (`-20.89%`, $h_{90\%} = 0.017247\text{ eV}$) |

## 2. Upstream `usnistgov/jarvis_leaderboard` Benchmark & Baseline Archives (Referenced by URL and SHA-256, Not Copied)

- `dft_3d_exfoliation_energy.json.zip` (`https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy.json.zip`, `5,502` bytes, `sha256: d7a3127002098c3da40292bee8d78de0e45ca42bef81adc73a07bc47e900a9a4`)
- `tinnet_N_ead.json.zip` (`https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/tinnet_N_ead.json.zip`, `3,081` bytes, `sha256: 14da9466b46ccd69aea116c6d6ef456da2c2cfe955b45b89105bb9f21acdfc49`)
- `matminer_xgboost/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv.zip` (`https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/contributions/matminer_xgboost/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv.zip`, `987` bytes, `sha256: e89262451215f98da0eddf327a082787461edfa5f73426baf6c4fd745acacb78`, verified Test MAE = `40.887046 meV/atom`)
- `alignn_model/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv.zip` (`https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/contributions/alignn_model/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv.zip`, `665` bytes, `sha256: 5bc9f63e3016343afc3a5719611ec9335442305a5d752fd5c44fb66ff857ac59`, verified Test MAE = `0.087055 eV`)
