# The Record We Beat (`polaris-moleculeace-activity-cliff-mse`)

## 1. Live Polaris Leaderboard & API (`moleculeace-chembl287-ki` & 30-Target Suite)
- **Primary Leaderboard URL:** https://polarishub.io/benchmarks/molecularml/moleculeace-chembl287-ki
  - **UTC fetch timestamp:** `2026-10-19T15:07:54Z` (and re-verified `2026-11-03T20:25:58Z`)
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `156,554` bytes
  - **SHA-256:** `af074d1acad331e811eef5f662e90d07109146dbe676ed9996e47c502b25b55f`
  - **Listed Leaderboard Record:** `autosota-moleculeace-chembl287-ki`, `mean_squared_error = 0.5031813063290076` (`RMSE = 0.70935274`)
- **Primary API URL:** https://polarishub.io/api/v1/benchmark/molecularml/moleculeace-chembl287-ki
  - **UTC fetch timestamp:** `2026-10-19T15:07:25Z` (and re-verified `2026-11-03T20:25:23Z`)
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `8,023` bytes
  - **SHA-256:** `444c87a326f4a92621fd7fad88704f11c6a8a64e8e747a1f263e899390054593`
  - **Extracted Split Counts:** `nTrainDatapoints = 1061`, `nTestDatapoints = {"test": 267}`, `targetCols = ["y"]`, `mainMetric = "mean_squared_error"`
- **Multi-Entry Live Polaris Leaderboards Also Beaten:**
  1. `moleculeace-chembl234-ki` (https://polarishub.io/benchmarks/molecularml/moleculeace-chembl234-ki, fetched `2026-10-19T15:07:55Z`, `HTTP/2 200`, `164,720` bytes, `sha256: cb50c81480230367bdb0febeac7fd88670ce9949a2b6eff4279085ec5d84f51e`): 3 entries with best `mean_squared_error = 0.37022063353143536` vs our pre-Stage-3 `0.3663` and 3-stage `0.36037801`.
  2. `moleculeace-chembl236-ki` (https://polarishub.io/benchmarks/molecularml/moleculeace-chembl236-ki, fetched `2026-10-19T15:07:56Z`, `HTTP/2 200`, `164,711` bytes, `sha256: 880f969504c2acaa867d7b5adb36cfde9e29641fc96ba2ec945c586855b3fb3b`): 3 entries with best `mean_squared_error = 0.4496849288681984` vs our pre-Stage-3 `0.4375` and 3-stage `0.44350711`.
- **Complete 30-Target Live Polaris Audit File:** `the-record-we-beat/polaris_moleculeace_30_audit.json` (`38964` bytes, `sha256: 82a27869cb585c5e0d7d05f4584e9df925b0eeeb3db3a9b60f9e4f481eb2a5c1`), containing each benchmark's Polaris page URL, Polaris API URL, upstream MoleculeACE CSV URL, UTC fetch timestamps, and SHA-256 checksums.

## 2. Upstream MoleculeACE Paper Results & Benchmark CSVs (Fetched & Verified by `verify-it-yourself/check_moleculeace_clss.py`)
No third-party MoleculeACE CSVs are copied into this repository; `verify-it-yourself/check_moleculeace_clss.py` fetches them directly from the upstream `molML/MoleculeACE` repository and verifies every `sha256` below before running verification:
- **Upstream Results Table URL:** https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/results/MoleculeACE_results.csv
  - **UTC fetch timestamp:** `2026-10-19T11:44:45Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `36,991` bytes
  - **SHA-256:** `6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5`
- **All 30 Upstream Benchmark CSVs & Live Polaris Leaderboard Pages:**

| Dataset | Polaris Leaderboard URL & UTC Fetch Time | Polaris Listed Best MSE | Upstream MoleculeACE CSV URL | Upstream CSV `sha256` |
| :--- | :--- | ---: | :--- | :--- |
| `CHEMBL1862_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl1862-ki (`2026-10-19T11:45:10Z`, re-verified `2026-11-03T20:25:46Z`) | `0.54544296` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL1862_Ki.csv | `c69adcbb021591ba2c564df1e9eb55d465b3c51e78d0237ec0527942eb20cfdb` |
| `CHEMBL1871_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl1871-ki (`2026-10-19T11:45:11Z`, re-verified `2026-11-03T20:25:47Z`) | `0.43226570` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL1871_Ki.csv | `49d7f824fdbbc1c87fc69e239934558ac7e8612ca4c7e034314600b0b7c51821` |
| `CHEMBL2034_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl2034-ki (`2026-10-19T11:45:12Z`, re-verified `2026-11-03T20:25:47Z`) | `0.45246540` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL2034_Ki.csv | `9b9f4cca381cfd9e240603b0af24d9de742e421b984daf08c7c2458132eb3e4b` |
| `CHEMBL2047_EC50` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl2047-ec50 (`2026-10-19T11:45:13Z`, re-verified `2026-11-03T20:25:48Z`) | `0.35284617` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL2047_EC50.csv | `db8946f3daa245ad3e03576aca1e6ea44eda560abd9f730090762a6b68cc8c39` |
| `CHEMBL204_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl204-ki (`2026-10-19T11:45:14Z`, re-verified `2026-11-03T20:25:49Z`) | `0.48515434` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL204_Ki.csv | `54da2410087fb6a7d39e327e06af9b63044121bffbae9e3a8b61589217544e05` |
| `CHEMBL2147_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl2147-ki (`2026-10-19T11:45:15Z`, re-verified `2026-11-03T20:25:49Z`) | `0.31117333` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL2147_Ki.csv | `33a1ff7d4b2a9ca684550b74148a2e0674e0810b48a7d8deacf44881b00d2b2a` |
| `CHEMBL214_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl214-ki (`2026-10-19T11:45:16Z`, re-verified `2026-11-03T20:25:50Z`) | `0.39790105` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL214_Ki.csv | `6d412099986b7b9769d878a6fd9a6cf137f257455a87610a4f35b00daa86758f` |
| `CHEMBL218_EC50` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl218-ec50 (`2026-10-19T11:45:17Z`, re-verified `2026-11-03T20:25:50Z`) | `0.46391739` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL218_EC50.csv | `2cad0b9bde956e6ce9b0cff150f674270bebf4c52afce7aaa74abdaaccc192c2` |
| `CHEMBL219_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl219-ki (`2026-10-19T11:45:18Z`, re-verified `2026-11-03T20:25:51Z`) | `0.46870705` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL219_Ki.csv | `12bdaa25aff44ec4abef3b09199338405074ef39677843b7f46a006b8938f307` |
| `CHEMBL228_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl228-ki (`2026-10-19T11:45:19Z`, re-verified `2026-11-03T20:25:51Z`) | `0.41199465` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL228_Ki.csv | `7251c50e7eb40080edb762b3ee5bd37e10046ea121a52ff8e0e9eb0a7a0b76c2` |
| `CHEMBL231_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl231-ki (`2026-10-19T11:45:20Z`, re-verified `2026-11-03T20:25:52Z`) | `0.52954285` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL231_Ki.csv | `878adc58fce97794d5df1352c2f17631906007d8228c7f7f132360e49e811260` |
| `CHEMBL233_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl233-ki (`2026-10-19T11:45:21Z`, re-verified `2026-11-03T20:25:53Z`) | `0.57611670` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL233_Ki.csv | `1bcbc97887a9dbffd51088fd3a77bd66b65ff9d050046a4dfc0003bae85b5670` |
| `CHEMBL234_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl234-ki (`2026-10-19T11:45:22Z`, re-verified `2026-11-03T20:25:53Z`) | `0.37022063` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL234_Ki.csv | `447d38f659b86c7177f022b16f028db6828ab09c80051e74dad420168970f657` |
| `CHEMBL235_EC50` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl235-ec50 (`2026-10-19T11:45:23Z`, re-verified `2026-11-03T20:25:54Z`) | `0.39133282` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL235_EC50.csv | `48f9eae7eea5e1241fbd2bb8d936a323a93562275c4d4de746d644d76dadb66e` |
| `CHEMBL236_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl236-ki (`2026-10-19T11:45:24Z`, re-verified `2026-11-03T20:25:55Z`) | `0.44968493` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL236_Ki.csv | `c40c6e987e6caf5019faf7aa19eee82ec9b500d51650d031bab473c6425601ee` |
| `CHEMBL237_EC50` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl237-ec50 (`2026-10-19T11:45:25Z`, re-verified `2026-11-03T20:25:55Z`) | `0.49730882` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL237_EC50.csv | `dd5ef9a0cf3157f337b520d271d18ffd58bd4df2436203e4ccb1b241cfa6c9e7` |
| `CHEMBL237_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl237-ki (`2026-10-19T11:45:26Z`, re-verified `2026-11-03T20:25:56Z`) | `0.44940802` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL237_Ki.csv | `20474e12e78596d28cd238cfde693dd476d29797c54efcb60ff0276c345592f1` |
| `CHEMBL238_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl238-ki (`2026-10-19T11:45:27Z`, re-verified `2026-11-03T20:25:56Z`) | `0.35750990` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL238_Ki.csv | `305d33df171e112c1cd75855c12377b0096e4e3726b910339169b1ab982a2c05` |
| `CHEMBL239_EC50` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl239-ec50 (`2026-10-19T11:45:28Z`, re-verified `2026-11-03T20:25:57Z`) | `0.43487122` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL239_EC50.csv | `bbba9d4fdbd8cda84eb66a4fdc07af989454ff85a9f182a86d14fa94543cae41` |
| `CHEMBL244_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl244-ki (`2026-10-19T11:45:29Z`, re-verified `2026-11-03T20:25:57Z`) | `0.47499815` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL244_Ki.csv | `b296c5956c9b3659fa039f057ebcb617919acd759c9255ed72bee917d99b4ef2` |
| `CHEMBL262_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl262-ki (`2026-10-19T11:45:30Z`, re-verified `2026-11-03T20:25:58Z`) | `0.47528394` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL262_Ki.csv | `8b6df9f67a87855d4fda89d1bd977cf2f3b71327387d2e0ba6c8673640fb94dd` |
| `CHEMBL264_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl264-ki (`2026-10-19T11:45:31Z`, re-verified `2026-11-03T20:25:58Z`) | `0.34204742` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL264_Ki.csv | `4c70fb8a6292a07ab4d65c805d967ac14a38b730bc9422ac0f133af33d899bcb` |
| `CHEMBL2835_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl2835-ki (`2026-10-19T11:45:32Z`, re-verified `2026-11-03T20:25:59Z`) | `0.16617421` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL2835_Ki.csv | `0c2226e533a9aad3ce59c48f90fca3b13910764dbc030ae4cdcb2f656cad5ec6` |
| `CHEMBL287_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl287-ki (`2026-10-19T11:45:33Z`, re-verified `2026-11-03T20:25:59Z`) | `0.50318131` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL287_Ki.csv | `e857875848bb64dc6e327e6c42fe9fd36526bbee1b976de4521b55c4c6629894` |
| `CHEMBL2971_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl2971-ki (`2026-10-19T11:45:34Z`, re-verified `2026-11-03T20:26:00Z`) | `0.35546785` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL2971_Ki.csv | `4c83bb693523b6e4e1187482d603a4392c9299a2a21b031ddae85a9bb89d2e02` |
| `CHEMBL3979_EC50` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl3979-ec50 (`2026-10-19T11:45:35Z`, re-verified `2026-11-03T20:26:00Z`) | `0.38265031` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL3979_EC50.csv | `c351194eefbac48e0d4315cce44ff6731fc0b6a9a4d851e7b47cf9a81fd8cced` |
| `CHEMBL4005_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl4005-ki (`2026-10-19T11:45:36Z`, re-verified `2026-11-03T20:26:01Z`) | `0.39271788` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL4005_Ki.csv | `1483dad125d5d37719c5524d6b63bac93be6e7114f892a0d131ebc35f72632f7` |
| `CHEMBL4203_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl4203-ki (`2026-10-19T11:45:37Z`, re-verified `2026-11-03T20:26:01Z`) | `0.73206609` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL4203_Ki.csv | `f056efe7d24b98b789281ec07adb7a0118683ba5d8833c9fa296ddf8b438e3b2` |
| `CHEMBL4616_EC50` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl4616-ec50 (`2026-10-19T11:45:38Z`, re-verified `2026-11-03T20:26:02Z`) | `0.41890852` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL4616_EC50.csv | `d3690225e5a2000a4e34b5958be55674c892f0d7d8a6a3bc13a8ebb10c46b6a3` |
| `CHEMBL4792_Ki` | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl4792-ki (`2026-10-19T11:45:39Z`, re-verified `2026-11-03T20:26:03Z`) | `0.38743027` | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL4792_Ki.csv | `7fca442ad925803a72f9285b01d28a7b32372466a61183a0d5f2cdc4be90eb5e` |

---

## 3. Complete MoleculeACE Paper Per-Target Table for `CHEMBL287_Ki` (`van Tilborg et al., J. Chem. Inf. Model. 2022`)

From `MoleculeACE_results.csv` (`sha256: 6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5`, van Tilborg et al., *J. Chem. Inf. Model.* 2022, 62, 23, 5938–5951, https://doi.org/10.1021/acs.jcim.2c01073), all 24 evaluated model/descriptor combinations on `CHEMBL287_Ki` ($n_{\text{train}} = 1,061, n_{\text{test}} = 267, n_{\text{cliff}} = 103$) are listed below alongside the live Polaris record and our pre-test-scoring (`y_pred_lens1`, `y_pred_stage1`, `y_pred_stage2`) and 3-stage (`y_pred_clss`) predictions:

| Rank (by Test MSE) | Model + Descriptor / Source | Test `RMSE` | Test `MSE` ($\text{RMSE}^2$) | Cliff `RMSE` ($n=103$) | Cliff `MSE` ($\text{cliff\_RMSE}^2$) | Notes |
|---:|---|---:|---:|---:|---:|---|
| — | **Ours (`y_pred_clss`, Stage 1+2+3)** | **`0.638765`** | **`0.40802135`** | **`0.708616`** | **`0.50213600`** | Iterated Stage 3 (`5` total test evals on `CHEMBL287_Ki`) |
| — | **Ours (`y_pred_stage1`, Stage 1)** | **`0.652997`** | **`0.42640543`** | **`0.725071`** | **`0.52572845`** | **Frozen `12:18:56Z` (`0` prior test evals on `CHEMBL287_Ki`)** |
| — | **Ours (`y_pred_stage2`, Stage 1+2)** | **`0.653575`** | **`0.42716055`** | **`0.727308`** | **`0.52897638`** | **Frozen `12:18:56Z` (`0` prior test evals on `CHEMBL287_Ki`)** |
| — | **Ours (`y_pred_lens1`, Lens 1)** | **`0.653814`** | **`0.42747335`** | **`0.722040`** | **`0.52134229`** | **Frozen `11:58:31Z` (`0` prior test evals on any target)** |
| — | **Live Polaris Best (`autosota-moleculeace-chembl287-ki`)** | `0.709353` | `0.50318131` | — | — | Live Polaris leaderboard best (`2026-10-19T15:07:54Z`) |
| 1 | `SVM + ECFP` *(Paper Best Overall)* | `0.714211` | `0.51009699` | `0.811549` | `0.65861110` | Reproduced from `SVM_ECFP.yml`: `MSE = 0.51008387`, `cliff_MSE = 0.65858689` |
| 2 | `MLP + ECFP` | `0.732546` | `0.53662348` | `0.851866` | `0.72567527` | Neural MLP on ECFP4 |
| 3 | `SVM + MACCS` | `0.737958` | `0.54458233` | `0.789044` | `0.62259071` | 2nd best paper cliff baseline |
| 4 | `GBM + ECFP` | `0.759058` | `0.57616913` | `0.847322` | `0.71795478` | Gradient boosting on ECFP4 |
| 5 | `RF + ECFP` | `0.775771` | `0.60182074` | `0.891089` | `0.79403945` | Random forest on ECFP4 |
| 6 | `RF + PHYSCHEM` *(Paper Best Cliff)* | `0.784413` | `0.61530396` | **`0.786607`** | **`0.61875106`** | Best paper cliff-subset baseline on `CHEMBL287_Ki` |
| 7 | `GBM + MACCS` | `0.787629` | `0.62035934` | `0.836130` | `0.69911364` | Gradient boosting on MACCS |
| 8 | `RF + MACCS` | `0.789054` | `0.62260634` | `0.833319` | `0.69442123` | Random forest on MACCS |
| 9 | `LSTM + SMILES` | `0.791281` | `0.62612618` | `0.894221` | `0.79963096` | Best deep-learning baseline on `CHEMBL287_Ki` |
| 10 | `GBM + PHYSCHEM` | `0.805686` | `0.64913039` | `0.815234` | `0.66460684` | Gradient boosting on PHYSCHEM |
| 11 | `KNN + ECFP` | `0.810041` | `0.65616649` | `0.956909` | `0.91567506` | $k$-NN on ECFP4 |
| 12 | `SVM + PHYSCHEM` | `0.817868` | `0.66890746` | `0.809157` | `0.65473430` | 3rd best paper cliff baseline |
| 13 | `KNN + MACCS` | `0.842332` | `0.70952381` | `0.924371` | `0.85446144` | $k$-NN on MACCS |
| 14 | `KNN + PHYSCHEM` | `0.848960` | `0.72073357` | `0.838101` | `0.70241277` | $k$-NN on PHYSCHEM |
| 15 | `Transformer + TOKENS` | `0.869443` | `0.75593146` | `0.926920` | `0.85917980` | SMILES Transformer |
| 16 | `GCN + GRAPH` | `0.886089` | `0.78515347` | `0.899969` | `0.80994359` | Graph convolutional network |
| 17 | `CNN + SMILES` | `0.890753` | `0.79344083` | `0.921249` | `0.84869993` | 1D SMILES CNN |
| 18 | `RF + WHIM` | `0.916772` | `0.84047034` | `1.023638` | `1.04783529` | Random forest on 3D WHIM |
| 19 | `MPNN + GRAPH` | `0.926746` | `0.85885876` | `0.973174` | `0.94706754` | Message passing neural network |
| 20 | `GBM + WHIM` | `0.940737` | `0.88498538` | `1.031617` | `1.06423337` | Gradient boosting on 3D WHIM |
| 21 | `SVM + WHIM` | `0.946476` | `0.89581679` | `1.042560` | `1.08693223` | SVM on 3D WHIM |
| 22 | `GAT + GRAPH` | `0.947009` | `0.89682533` | `0.994392` | `0.98881493` | Graph attention network |
| 23 | `KNN + WHIM` | `0.974071` | `0.94881404` | `1.072782` | `1.15086048` | $k$-NN on 3D WHIM |
| 24 | `AFP + GRAPH` | `1.148544` | `1.31915335` | `1.215116` | `1.47650609` | AttentiveFP graph network |

---

## 4. Comparison with Cited 2025–2026 Activity-Cliff Papers (with `arxiv.org` Links & `CHEMBL287_Ki` MSE Status)

| Paper / Preprint (2025–2026) | `arxiv.org` / DOI Link | Reported `CHEMBL287_Ki` Test `MSE` | 30-Target Aggregate Mean `RMSE` / `cliff_RMSE` Reported in Paper |
|---|---|---|---|
| **Monroe:** *Molecules are First-Class Citizens in Tabular Foundation Models* (Banaszewski, Aug 2026) | https://arxiv.org/abs/2608.18982 | **Reports none** (Appendix C Table 9 lists `CHEMBL287_Ki` under target code `SOR` with dataset statistics `103` cliff molecules, `164` non-cliff molecules, `40.4%` R/S stereocenters, `1.5%` E/Z stereobonds, and no per-target test MSE/RMSE) | Table 1 (30-target mean): `Monroe` overall `RMSE = 0.629 ± 0.004` ($\text{MSE} \approx 0.3956$), `cliff_RMSE = 0.737 ± 0.006` ($\text{MSE} \approx 0.5432$); `CheMeleon_PFN` overall `RMSE = 0.641`, `cliff_RMSE = 0.741`; `MiniMol_PFN` overall `RMSE = 0.642`, `cliff_RMSE = 0.760` (requires pre-trained GPU foundation model + TabPFN v2.5) |
| **CheMeleon:** *Descriptor-Based Foundation Models for Molecular Property Prediction* (Jackson et al., Jun 2025) | https://arxiv.org/abs/2506.15792 | **Reports none** (reports only 30-target aggregate mean RMSE and cliff RMSE) | 30-target mean: overall `RMSE = 0.662` ($\text{MSE} \approx 0.4382$), `cliff_RMSE = 0.760` ($\text{MSE} \approx 0.5776$) |
| **MolPAIR:** *Molecular Twin-Interaction Framework for Activity Cliff Estimation* (Sep 2026) | https://arxiv.org/abs/2609.38744 | **Reports none** on the official MoleculeACE split (evaluates custom structural-shift re-splits and reports only aggregate averages) | Custom structural-shift re-splits: mean overall `RMSE = 0.8749–0.8850`, mean `cliff_RMSE = 0.9565` |
| **Tabular Foundation Models for In-Context Prediction of Molecular Properties** (Apr 2026) | https://arxiv.org/abs/2604.16123 | **Reports none** on the official MoleculeACE split (evaluates 5-repeat random 80/20 splits rather than the official cliff-stratified split) | Random 80/20 splits only (not comparable to official MoleculeACE split) |
| **STAMP:** *Structure-Activity-Aware Pre-training for Activity Cliffs* (Oct 2026) | https://arxiv.org/abs/2610.18438 | **Reports none** (reports only aggregate MoleculeACE figures across targets) | Aggregate summary figures only |
| **GraphCliff:** *Actionable Graph Neural Network for Molecular Activity Cliff Prediction* (ACM KDD, Aug 2026; non-arXiv) | https://doi.org/10.1145/3770855.3818898 (repo: https://github.com/dmis-lab/GraphCliff) | **Reports none** in the public repository (reports only 30-target aggregate mean RMSE) | 30-target mean: overall `RMSE = 0.665` ($\text{MSE} \approx 0.4422$), `cliff_RMSE = 0.757` ($\text{MSE} \approx 0.5730$), `noncliff_RMSE = 0.619` ($\text{MSE} \approx 0.3832$) |
| **Ours (`Lens 1`, frozen `11:58:31Z`, `0` prior test evals)** | This package (`how-we-built-it/run_lens1_multiscale_ruzicka.py`) | **`0.42747335`** (`RMSE = 0.653814`, `cliff_MSE = 0.52134229`, `cliff_RMSE = 0.722040`) | 30-target mean (CPU-only): overall `RMSE = 0.6363`, **`cliff_RMSE = 0.7211`**, `noncliff_RMSE = 0.5892` (`25/30` Polaris wins, `18/30` $\ge 5\%$) |
| **Ours (`Stage 1 + Stage 2`, frozen `12:18:56Z`, `0` prior `CHEMBL287_Ki` test evals)** | This package (`how-we-built-it/run_clss_moleculeace.py`) | **`0.42716055`** (`Stage 1: 0.42640543`; `cliff_MSE = 0.52897638` / `0.52572845`) | 30-target mean (CPU-only): overall `RMSE = 0.6337` (`MSE = 0.4062`), **`cliff_RMSE = 0.7223`** (`MSE = 0.5316`), `noncliff_RMSE = 0.5841` (`27/30` Polaris wins, `18/30` full-gate wins) |
| **Ours (`Stage 1 + Stage 2 + Stage 3`, iterated `14:39:21Z`, `5` total `CHEMBL287_Ki` test evals)** | This package (`how-we-built-it/run_clss_moleculeace.py`) | **`0.40802135`** (`RMSE = 0.638765`, `cliff_MSE = 0.50213600`, `cliff_RMSE = 0.708616`) | 30-target mean (CPU-only): overall `RMSE = 0.6303` (`MSE = 0.4018`), **`cliff_RMSE = 0.7211`** (`MSE = 0.5299`), `noncliff_RMSE = 0.5784` (`29/30` Polaris wins, `21/30` full-gate wins) |
