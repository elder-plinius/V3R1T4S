# The Record We Beat (`polaris-moleculeace-activity-cliff-mse`)

## 1. Live Polaris Leaderboard & API (`moleculeace-chembl287-ki` & 30-Target Suite)
- **Primary Leaderboard URL:** https://polarishub.io/benchmarks/molecularml/moleculeace-chembl287-ki
  - **UTC fetch timestamp:** `2026-10-19T15:07:54Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `156,554` bytes
  - **SHA-256:** `af074d1acad331e811eef5f662e90d07109146dbe676ed9996e47c502b25b55f`
  - **Listed Leaderboard Record:** `autosota-moleculeace-chembl287-ki`, `mean_squared_error = 0.5031813063290076` (`RMSE = 0.70935274`)
- **Primary API URL:** https://polarishub.io/api/v1/benchmark/molecularml/moleculeace-chembl287-ki
  - **UTC fetch timestamp:** `2026-10-19T15:07:25Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `8,023` bytes
  - **SHA-256:** `444c87a326f4a92621fd7fad88704f11c6a8a64e8e747a1f263e899390054593`
  - **Extracted Split Counts:** `nTrainDatapoints = 1061`, `nTestDatapoints = {"test": 267}`, `targetCols = ["y"]`, `mainMetric = "mean_squared_error"`
- **Multi-Entry Live Polaris Leaderboards Also Beaten:**
  1. `moleculeace-chembl234-ki` (https://polarishub.io/benchmarks/molecularml/moleculeace-chembl234-ki, fetched `2026-10-19T15:07:55Z`, `HTTP/2 200`, `164,720` bytes, `sha256: cb50c81480230367bdb0febeac7fd88670ce9949a2b6eff4279085ec5d84f51e`): 3 entries with best `mean_squared_error = 0.37022063353143536` vs our `0.36037801`.
  2. `moleculeace-chembl236-ki` (https://polarishub.io/benchmarks/molecularml/moleculeace-chembl236-ki, fetched `2026-10-19T15:07:56Z`, `HTTP/2 200`, `164,711` bytes, `sha256: 880f969504c2acaa867d7b5adb36cfde9e29641fc96ba2ec945c586855b3fb3b`): 3 entries with best `mean_squared_error = 0.4496849288681984` vs our `0.44350711`.
- **Complete 30-Target Live Polaris Audit File:** `the-record-we-beat/polaris_moleculeace_30_audit.json` (`20,801` bytes, `sha256: 03312341e4e754cbef17b0d61c0eff93d7255cc8879ec1acb0245705925d5d35`)

## 2. Official MoleculeACE Paper 24-Method Results & Benchmark CSVs
- **Results Table URL:** https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/results/MoleculeACE_results.csv
  - **UTC fetch timestamp:** `2026-10-19T11:44:45Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `36,991` bytes
  - **SHA-256:** `6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5`
  - **Saved Copy:** `the-record-we-beat/MoleculeACE_results.csv`
- **Primary Target Benchmark CSV (`CHEMBL287_Ki.csv`):**
  - **URL:** https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL287_Ki.csv
  - **Byte size:** `121,021` bytes
  - **SHA-256:** `e857875848bb64dc6e327e6c42fe9fd36526bbee1b976de4521b55c4c6629894`
  - **Saved Copy:** `the-record-we-beat/benchmark_data/CHEMBL287_Ki.csv` (along with all 30 official CSVs `the-record-we-beat/benchmark_data/CHEMBL*.csv`).
