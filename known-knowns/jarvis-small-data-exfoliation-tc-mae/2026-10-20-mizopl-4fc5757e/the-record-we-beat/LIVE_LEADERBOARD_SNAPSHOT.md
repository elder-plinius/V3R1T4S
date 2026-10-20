# Live NIST JARVIS-Leaderboard Status Snapshot (`jarvis-small-data-exfoliation-tc-mae`)

## 1. Primary Live Status Pages Fetched & Verified

| Benchmark Task | Live Status Page URL | UTC Fetch Timestamp | HTTP Status | Size (Bytes) | SHA-256 Checksum of Fetched HTML | Live #1 Model & Test MAE | Claimed CLSS Test MAE (Relative Gain / $h_{90\%}$) |
| :--- | :--- | :--- | :--- | ---: | :--- | :--- | :--- |
| **`dft_3d_Tc_supercon`** | `https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_Tc_supercon/` | `2026-10-20T21:43:02Z` | `HTTP/2 200` | `159,267` | `c71b988e15da799deaddc96a90bde3ca8444b65c072681790781dbcf6283820d` | `atomgpt_model`: **`1.5187 K`** (`cfid`: `1.9989 K`) | **`0.902806 K`** (`-40.55%`, $h_{90\%} = 0.367962\text{ K}$) |
| **`dft_3d_exfoliation_energy`** | `https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy/` | `2026-10-20T21:43:03Z` | `HTTP/2 200` | `169,881` | `a32c745dc8c71293b3deb66d12cd505d5a8664d808e0935b51e541cd74bf0cd5` | `matminer_xgboost`: **`40.887 meV/atom`** (`matminer_rf`: `42.7554`) | **`28.195924 meV/atom`** (`-31.04%`, $h_{90\%} = 11.132579\text{ meV/atom}$) |
| **`tinnet_N_ead` (`p1`)** | `https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/tinnet_N_ead/` | `2026-10-20T21:43:04Z` | `HTTP/2 200` | `170,439` | `f8b00af347359b3da3ad3965f1f349dd47f0a187fd6c8632bdb065b675b9c1a7` | `alignn_model`: **`0.0871 eV`** (`N = 327`, 13 entries) | **`0.068908 eV`** (`-20.89%`, $h_{90\%} = 0.017247\text{ eV}$) |

## 2. Official Leaderboard Submission Archives Included in `object/data/leaderboard_baselines/`

- `tc_atomgpt.csv.zip` (`588` bytes, `sha256: b1b4a24f41bc44809f422c7011fb6ca86ef9a9676dd45218aed35f45bee4d771`, verified Test MAE = `1.518733 K`)
- `tc_cfid.csv.zip` (`717` bytes, `sha256: 1b6aa58b8816c6712935a4321cddba8b9fe65e80a90bb30651aad991fb97d38a`, verified Test MAE = `1.998907 K`)
- `exf_matminer_xgb.csv.zip` (`987` bytes, `sha256: e89262451215f98da0eddf327a082787461edfa5f73426baf6c4fd745acacb78`, verified Test MAE = `40.887046 meV/atom`)
- `exf_cfid.csv.zip` (`1,385` bytes, `sha256: d217925c0f65c2719c76c0d63d6c6ca75dbdf451e9336fe45170ddc829b74589`, verified Test MAE = `62.116904 meV/atom`)
- `tinnet_N_alignn.csv.zip` (`665` bytes, `sha256: 5bc9f63e3016343afc3a5719611ec9335442305a5d752fd5c44fb66ff857ac59`, verified Test MAE = `0.087055 eV`)
