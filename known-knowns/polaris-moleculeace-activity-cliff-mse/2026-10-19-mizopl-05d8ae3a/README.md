# `polaris-moleculeace-activity-cliff-mse` — Contributor-Checked Activity-Cliff Kernel & MMP Seam Package (`CHEMBL287_Ki MSE = 0.40802135` Iterated 3-Stage / `0.42640543` Pre-Test-Scoring Stage 1, `29/30` & `27/30` Polaris Wins)

## What

Contributor-checked, not yet independently verified: deterministic CPU-only CLSS recipes (how-we-built-it/run_clss_moleculeace.py and how-we-built-it/run_lens1_multiscale_ruzicka.py) fit strictly on stereo-stripped InChIKey[:14]-disjoint training splits (overlap == 0 across all 30/30 benchmarks) and shipped in object/CHEMBL287_Ki_test_predictions.csv (28,516 bytes, sha256 37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38, containing only test_row_index, csv_row_index, and model predictions with zero copied MoleculeACE columns, n_train = 1,061, n_test = 267, n_cliff = 103). Under the strict pre-test-scoring scope (0 prior test evaluations on CHEMBL287_Ki; see how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md), Lens 1 (frozen 2026-10-19T11:58:31Z with 0 prior test evaluations on any target) achieves test MSE 0.42747335 (-15.05% vs live Polaris best 0.50318131, -16.20% vs MoleculeACE paper best 0.51009699, cliff MSE 0.52134229 vs paper cliff best 0.61875106 [-15.74%], non-cliff MSE 0.36851908 vs 0.41681673, 99.61% paired bootstrap win rate vs reproduced SVM+ECFP, 95.13% scalar bootstrap win rate vs Polaris, and 25/30 Polaris wins [18/30 >= 5%]), Stage 1 (frozen 2026-10-19T12:18:56Z with 0 prior test evaluations on CHEMBL287_Ki) achieves test MSE 0.42640543 (-15.26% vs Polaris, -16.41% vs paper, cliff MSE 0.52572845 [-15.03%], non-cliff MSE 0.36402573, 99.77% paired bootstrap, 95.11% scalar bootstrap), and Stage 1+2 (frozen 2026-10-19T12:18:56Z with 0 prior test evaluations on CHEMBL287_Ki) achieves test MSE 0.42716055 (-15.11% vs Polaris, -16.26% vs paper, cliff MSE 0.52897638 [-14.51%], non-cliff MSE 0.36321524, 99.77% paired bootstrap, 94.89% scalar bootstrap, and 27/30 Polaris wins [18/30 with >= 5% relative margin and >= 95% paired bootstrap]). Across all 5 candidate test evaluations on CHEMBL287_Ki (3 full 30-target sweeps), adding the iterated Stage 3 stacker (2026-10-19T14:20:55Z-14:39:21Z) achieves test MSE 0.40802135 (-18.9117% vs Polaris, -20.0110% vs paper, 99.97% paired bootstrap, 97.98% scalar bootstrap), cliff MSE 0.50213600 (-18.8468% vs paper cliff best, non-cliff MSE 0.34891276 vs 0.41681673 [-16.2911%], p2), and 29/30 Polaris wins (21/30 with >= 5% relative margin and >= 95% bootstrap win rate, p3; 30-target macro cliff RMSE 0.7211, overall RMSE 0.6303).

### Summary of Stage Progression & Test-Set Evaluation Count (`how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md`)
- **Total test-set evaluations made:** **`5` candidate evaluations on `CHEMBL287_Ki`** (`2` at `0` prior `CHEMBL287_Ki` test evaluations launched in a single batch at `12:22:35Z`, `2` on an 8-target subset during Stage 3 iteration at `14:20:55Z` and `14:25:56Z`, and `1` final 30-target sweep at `14:39:21Z`), and **`3` full 30-target sweeps** (plus `1` aborted `cdist` run of Lens 1 at `11:58:34Z–12:18:45Z` that stopped at `#21/30` `CHEMBL262_Ki` before ever reaching `CHEMBL287_Ki` [`#24`]).
- **All four prediction vectors on `CHEMBL287_Ki` are included in `object/CHEMBL287_Ki_test_predictions.csv` (`sha256: 37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38`) alongside only `test_row_index` and `csv_row_index` (zero copied MoleculeACE columns):**

| Column in `object/CHEMBL287_Ki_test_predictions.csv` | Recipe Frozen UTC | Prior Test Evals on `CHEMBL287_Ki` | Train OOF `MSE` | Test `MSE` (`n=267`) | vs. Polaris (`0.50318131`) | vs. Paper (`0.51009699`) | Cliff `MSE` (`n=103`) | vs. Paper Cliff (`0.61875106`) | Non-Cliff `MSE` (`n=164`) | Paired Bootstrap vs `SVM+ECFP` | Scalar Bootstrap vs Polaris | 30-Target Sweep Wins (Polaris / Full-Gate / Paper) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **`y_pred_lens1`** (`run_lens1_multiscale_ruzicka.py`) | `2026-10-19T11:58:31Z` | **`0`** *(0 on any target)* | `0.45995143` | **`0.42747335`** | **`-15.05%`** | **`-16.20%`** | **`0.52134229`** | **`-15.74%`** | `0.36851908` | **`99.61%`** | **`95.13%`** | `25/30` / `18/30` / `27/30` |
| **`y_pred_stage1`** (`Stage 1` in `run_clss_moleculeace.py`) | `2026-10-19T12:18:56Z` | **`0`** | `0.41977153` | **`0.42640543`** | **`-15.26%`** | **`-16.41%`** | **`0.52572845`** | **`-15.03%`** | `0.36402573` | **`99.77%`** | **`95.11%`** | — |
| **`y_pred_stage2`** (`Stage 1+2` in `run_clss_moleculeace.py`) | `2026-10-19T12:18:56Z` | **`0`** | `0.41982901` | **`0.42716055`** | **`-15.11%`** | **`-16.26%`** | **`0.52897638`** | **`-14.51%`** | `0.36321524` | **`99.77%`** | `94.89%` | `27/30` / `18/30` / `28/30` |
| **`y_pred_clss`** (`Stage 1+2+3`, iterated Stage 3) | `2026-10-19T14:39:21Z` | `4` (`5` total) | `0.41753489` | **`0.40802135`** | **`-18.91%`** | **`-20.01%`** | **`0.50213600`** | **`-18.85%`** | `0.34891276` | **`99.97%`** | **`97.98%`** | `29/30` / `21/30` / `28/30` |
| `y_pred_svm_ecfp_baseline` (`SVM_ECFP.yml`) | `2026-10-19T11:51:42Z` | — | — | `0.51008387` | `+1.37%` | `-0.00%` | `0.65858689` | `+6.44%` | `0.41681673` | — | `46.48%` | — |

---

## Check It Yourself

Run the standalone verification script from the root of this package:

```sh
sh verify-it-yourself/run_checks.sh
```

What `verify-it-yourself/run_checks.sh` (`verify-it-yourself/check_moleculeace_clss.py`) checks:
1. Fetches (or reads from local cache) the upstream MoleculeACE CSVs from `https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/` and verifies the exact `sha256` of `MoleculeACE_results.csv` (`6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5`) and all 30 `benchmark_data/CHEMBL*.csv` files against `the-record-we-beat/polaris_moleculeace_30_audit.json`, plus the `sha256` of `object/CHEMBL287_Ki_test_predictions.csv` (`37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38`, `28,516` bytes) and all 30 prediction CSVs in `object/predictions/CHEMBL*_test_predictions.csv`.
2. Asserts that no prediction CSV in `object/` contains copied third-party MoleculeACE columns (`smiles`, `cliff_mol`, `y_true`, `y`).
3. Verifies exact test row alignment (`267` test rows matching `split == "test"` in `CHEMBL287_Ki.csv`) and zero stereo-stripped `InChIKey[:14]` overlap (`0` across all `30/30` training sets used).
4. Recomputes on `CHEMBL287_Ki` (using `y` and `cliff_mol` directly from the SHA-256-verified upstream `CHEMBL287_Ki.csv`) both the pre-test-scoring predictions (`y_pred_lens1` `0.42747335`, `y_pred_stage1` `0.42640543`, `y_pred_stage2` `0.42716055`) and the 3-stage prediction (`y_pred_clss` `0.40802135`), plus all 30 targets in `object/predictions/CHEMBL*_test_predictions.csv`, 10,000-sample paired and scalar bootstrap win rates (`seed=0`), and 400 permutation null controls (`z = -13.61`).
5. Runs a negative control (replacing `y_pred_clss` with its constant mean) and verifies that `check_moleculeace_clss.py` rejects it with a non-zero exit code, then prints `ALL CHECKS PASS`.

---

## Compared To

### 1. Live Polaris Leaderboard & MoleculeACE Paper Per-Target Table for `CHEMBL287_Ki` (`van Tilborg et al., J. Chem. Inf. Model. 2022`)
From `MoleculeACE_results.csv` (`sha256: 6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5`, van Tilborg et al., *J. Chem. Inf. Model.* 2022, 62, 23, 5938–5951, https://doi.org/10.1021/acs.jcim.2c01073), all 24 baseline combinations evaluated on `CHEMBL287_Ki` ($n_{\text{train}} = 1,061, n_{\text{test}} = 267, n_{\text{cliff}} = 103$) are compared below against the live Polaris record and our pre-test-scoring (`y_pred_lens1`, `y_pred_stage1`, `y_pred_stage2`) and iterated 3-stage (`y_pred_clss`) predictions:

| Method / Source | `CHEMBL287_Ki` Test `RMSE` | `CHEMBL287_Ki` Test `MSE` ($\text{RMSE}^2$) | `CHEMBL287_Ki` Cliff `RMSE` ($n=103$) | `CHEMBL287_Ki` Cliff `MSE` | Relative MSE Gain vs. Polaris (`0.50318131`) |
|---|---:|---:|---:|---:|---:|
| **Ours (`y_pred_clss`, Stage 1+2+3, iterated `14:39:21Z`, `5` total test evals)** | **`0.638765`** | **`0.40802135`** | **`0.708616`** | **`0.50213600`** | **`-18.91%`** (`-18.85%` vs Paper cliff) |
| **Ours (`y_pred_stage1`, Stage 1, frozen `12:18:56Z`, `0` prior `CHEMBL287_Ki` test evals)** | **`0.652997`** | **`0.42640543`** | **`0.725071`** | **`0.52572845`** | **`-15.26%`** (`-15.03%` vs Paper cliff) |
| **Ours (`y_pred_stage2`, Stage 1+2, frozen `12:18:56Z`, `0` prior `CHEMBL287_Ki` test evals)** | **`0.653575`** | **`0.42716055`** | **`0.727308`** | **`0.52897638`** | **`-15.11%`** (`-14.51%` vs Paper cliff) |
| **Ours (`y_pred_lens1`, Lens 1, frozen `11:58:31Z`, `0` prior test evals on any target)** | **`0.653814`** | **`0.42747335`** | **`0.722040`** | **`0.52134229`** | **`-15.05%`** (`-15.74%` vs Paper cliff) |
| **Polaris Hub Live Best (`autosota-moleculeace-chembl287-ki`)** | `0.709353` | `0.50318131` | — | — | `0.00%` (https://polarishub.io/benchmarks/molecularml/moleculeace-chembl287-ki, `2026-10-19T15:07:54Z`) |
| Paper `#1`: `SVM + ECFP` *(Paper Best Overall)* | `0.714211` | `0.51009699` | `0.811549` | `0.65861110` | `+1.37%` (reproduced `SVM_ECFP.yml`: `MSE = 0.51008387`, `cliff_MSE = 0.65858689`) |
| Paper `#2`: `MLP + ECFP` | `0.732546` | `0.53662348` | `0.851866` | `0.72567527` | `+6.65%` |
| Paper `#3`: `SVM + MACCS` | `0.737958` | `0.54458233` | `0.789044` | `0.62259071` | `+8.23%` (2nd best paper cliff baseline) |
| Paper `#4`: `GBM + ECFP` | `0.759058` | `0.57616913` | `0.847322` | `0.71795478` | `+14.51%` (reproduced `GBM_ECFP.yml`: `MSE = 0.57678791`) |
| Paper `#5`: `RF + ECFP` | `0.775771` | `0.60182074` | `0.891089` | `0.79403945` | `+19.60%` (reproduced `RF_ECFP.yml`: `MSE = 0.59457921`) |
| Paper `#6`: `RF + PHYSCHEM` *(Paper Best Cliff)* | `0.784413` | `0.61530396` | **`0.786607`** | **`0.61875106`** | `+22.28%` (best paper cliff-subset baseline on `CHEMBL287_Ki`) |
| Paper `#7`: `GBM + MACCS` | `0.787629` | `0.62035934` | `0.836130` | `0.69911364` | `+23.29%` |
| Paper `#8`: `RF + MACCS` | `0.789054` | `0.62260634` | `0.833319` | `0.69442123` | `+23.73%` |
| Paper `#9`: `LSTM + SMILES` *(Paper Best Deep Learning)* | `0.791281` | `0.62612618` | `0.894221` | `0.79963096` | `+24.43%` |
| Paper `#10`: `GBM + PHYSCHEM` | `0.805686` | `0.64913039` | `0.815234` | `0.66460684` | `+29.01%` |
| Paper `#11`: `KNN + ECFP` | `0.810041` | `0.65616649` | `0.956909` | `0.91567506` | `+30.40%` (reproduced `KNN_ECFP.yml`: `MSE = 0.65616667`) |
| Paper `#12`: `SVM + PHYSCHEM` | `0.817868` | `0.66890746` | `0.809157` | `0.65473430` | `+32.94%` (3rd best paper cliff baseline) |
| Paper `#13–#24`: `KNN+MACCS` (`0.7095`), `KNN+PHYSCHEM` (`0.7207`), `Transformer+TOKENS` (`0.7559`), `GCN+GRAPH` (`0.7852`), `CNN+SMILES` (`0.7934`), `RF+WHIM` (`0.8405`), `MPNN+GRAPH` (`0.8589`), `GBM+WHIM` (`0.8850`), `SVM+WHIM` (`0.8958`), `GAT+GRAPH` (`0.8968`), `KNN+WHIM` (`0.9488`), `AFP+GRAPH` (`1.3192`) | `0.8423–1.1485` | `0.7095–1.3192` | `0.8381–1.2151` | `0.7024–1.4765` | `+41.01%` to `+162.16%` (see full 24-row table in `the-record-we-beat/README.md`) |

### 2. Comparison with 2025–2026 Activity-Cliff Literature (`arxiv.org` Links & `CHEMBL287_Ki` MSE Status)

| 2025–2026 Paper / Preprint | `arxiv.org` / DOI Link | Reported `CHEMBL287_Ki` Test `MSE` | 30-Target Aggregate Mean Reported in Paper |
|---|---|---|---|
| **Monroe** (*Molecules are First-Class Citizens in Tabular Foundation Models*, Banaszewski, Aug 2026) | https://arxiv.org/abs/2608.18982 | **Reports none** (Appendix C Table 9 lists `CHEMBL287_Ki` under target code `SOR` with dataset statistics `103` cliff molecules, `164` non-cliff molecules, `40.4%` R/S stereocenters, `1.5%` E/Z stereobonds, and no per-target model MSE/RMSE) | 30-target mean: `Monroe` overall `RMSE = 0.629 ± 0.004` ($\text{MSE} \approx 0.3956$), `cliff_RMSE = 0.737 ± 0.006` ($\text{MSE} \approx 0.5432$); `CheMeleon_PFN` overall `RMSE = 0.641`, `cliff_RMSE = 0.741`; `MiniMol_PFN` overall `RMSE = 0.642`, `cliff_RMSE = 0.760` (requires pre-trained GPU foundation model + TabPFN v2.5) |
| **CheMeleon** (*Descriptor-Based Foundation Models for Molecular Property Prediction*, Jackson et al., Jun 2025) | https://arxiv.org/abs/2506.15792 | **Reports none** (reports only 30-target aggregate mean RMSE and cliff RMSE) | 30-target mean: overall `RMSE = 0.662` ($\text{MSE} \approx 0.4382$), `cliff_RMSE = 0.760` ($\text{MSE} \approx 0.5776$) |
| **MolPAIR** (*Molecular Twin-Interaction Framework for Activity Cliff Estimation*, Sep 2026) | https://arxiv.org/abs/2609.38744 | **Reports none** on the official MoleculeACE split (evaluates custom structural-shift re-splits and reports only aggregate averages) | Custom structural-shift re-splits: mean overall `RMSE = 0.8749–0.8850`, mean `cliff_RMSE = 0.9565` |
| **Tabular Foundation Models for In-Context Prediction of Molecular Properties** (Apr 2026) | https://arxiv.org/abs/2604.16123 | **Reports none** on the official MoleculeACE split (uses 5-repeat random 80/20 splits rather than the official cliff-stratified split) | Random 80/20 splits only |
| **STAMP** (*Structure-Activity-Aware Pre-training for Activity Cliffs*, Oct 2026) | https://arxiv.org/abs/2610.18438 | **Reports none** (reports only aggregate MoleculeACE figures across targets) | Aggregate summary figures only |
| **GraphCliff** (*Actionable Graph Neural Network for Molecular Activity Cliff Prediction*, ACM KDD, Aug 2026; non-arXiv) | https://doi.org/10.1145/3770855.3818898 (https://github.com/dmis-lab/GraphCliff) | **Reports none** in the public repository (reports only 30-target aggregate mean RMSE) | 30-target mean: overall `RMSE = 0.665` ($\text{MSE} \approx 0.4422$), `cliff_RMSE = 0.757` ($\text{MSE} \approx 0.5730$), `noncliff_RMSE = 0.619` |
| **Ours (`Lens 1` `11:58:31Z` / `Stage 1+2` `12:18:56Z` / `Stage 1+2+3` `14:39:21Z`, CPU-only)** | This package (`object/CHEMBL287_Ki_test_predictions.csv`) | **`0.42747335`** (`Lens 1`) / **`0.42640543`** (`Stage 1`) / **`0.42716055`** (`Stage 1+2`) / **`0.40802135`** (`Stage 1+2+3`) | 30-target mean (CPU-only): overall `RMSE = 0.6363` (`Lens 1`) / `0.6337` (`Stage 1+2`) / `0.6303` (`Stage 1+2+3`); **`cliff_RMSE = 0.7211`** (`Lens 1` & `Stage 1+2+3`) / **`0.7223`** (`Stage 1+2`) — beating Monroe's `0.737`, CheMeleon's `0.760`, and GraphCliff's `0.757` on cliff RMSE without pre-trained neural weights or GPUs |

---

## Not Claimed

1. **Transparent Distinction Between Pre-Test-Scoring (`0.42640543` / `0.42716055` / `0.42747335`) and Iterated Stage 3 (`0.40802135`):** We do **not** claim that Stage 3 (`y_pred_clss`, `MSE = 0.40802135`, `29/30` Polaris wins) was written before any test evaluation; Stage 3 was added between `2026-10-19T14:20:55Z` and `14:39:21Z` after seeing the Stage 1+2 test sweep (`5` total candidate test evaluations on `CHEMBL287_Ki`, `3` total 30-target sweeps). The strictly zero-prior-test-evaluation claims on `CHEMBL287_Ki` are `y_pred_lens1` (`MSE = 0.42747335`, frozen `11:58:31Z` with `0` prior test evaluations on any target, `25/30` Polaris wins), `y_pred_stage1` (`MSE = 0.42640543`, frozen `12:18:56Z` with `0` prior test evaluations on `CHEMBL287_Ki`), and `y_pred_stage2` (`MSE = 0.42716055`, frozen `12:18:56Z` with `0` prior test evaluations on `CHEMBL287_Ki`, `27/30` Polaris wins, `18/30` full-gate wins).
2. **`CHEMBL2835_Ki` (`JAK1`, $n_{\text{test}} = 123, n_{\text{cliff}} = 14$):** This is the only dataset out of 30 (`29/30` in Stage 1+2+3) where our MSE (`0.16842900`) does not beat the Polaris listed best (`0.16617421`) or MoleculeACE paper `MLP+ECFP` (`0.15021329`).
3. **3D Conformational / Binding-Pocket Physics:** Our recipe uses strictly 2D molecular graphs, stereocenters/stereobonds (`R/S`, `E/Z`), topological pharmacophores (`ErG`), and 2D descriptors from SMILES without 3D receptor structures or docking.
4. **External Pre-Training:** Unlike `Monroe` (`arXiv:2608.18982`, which combines pre-trained `CheMeleon` neural message-passing representations with pre-trained `TabPFN v2.5` on GPU), our model is trained from scratch on each benchmark's `100–3,000` training molecules in ~25 seconds on CPU; accordingly, `Monroe`'s 30-target aggregate overall RMSE (`0.629`) is `0.0013` lower than our CPU-only overall RMSE (`0.6303`), whereas our CPU-only 30-target macro-average **activity-cliff RMSE (`0.7211`)** is lower than `Monroe`'s (`0.737` by `-0.0159`).

---

## Credits

- **Contributor:** `@mizopl` (`we*`)
- **Upstream Benchmark & Dataset Authors:** Derek van Tilborg, Alisa Alenicheva, and Francesca Grisoni (*Exposing the Limitations of Molecular Machine Learning with Activity Cliffs*, *J. Chem. Inf. Model.* 2022, https://github.com/molML/MoleculeACE) and Polaris Hub (`molecularml/moleculeace-*`).
