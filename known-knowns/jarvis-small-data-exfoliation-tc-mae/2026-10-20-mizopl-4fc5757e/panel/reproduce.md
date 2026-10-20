# Skeptic Panel Report — Role: REPRODUCE

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target_id: jarvis-small-data-exfoliation-tc-mae

## 1. Quoted Definition & Success Criterion

Before reading any of the author's Python scripts (`claim/featurize_physics_clss.py`, `claim/train_and_predict_jarvis_clss.py`, `claim/author_checker_jarvis_clss.py`), we read `claim/CLAIM.md`, `claim/REPRODUCE.md`, and `claim/jarvis_clss_results_manifest.json` and quoted the verbatim target specification from `claim/CLAIM.md`:

- **`success_criterion`:**
  "Trained model, training script and predictions file (`jarvis_leaderboard` CSV format) for `dft_3d_exfoliation_energy` or `dft_3d_Tc_supercon` such that test MAE on the official `test` IDs is strictly lower than the best MAE on the live leaderboard page (`1.9989 K` or `40.887 meV/atom`, or whatever is best at verification time) by at least 5% relative and by more than the half-width of a 1,000-sample bootstrap 90% confidence interval of the claimed model's MAE, trained strictly on the official `train`+`val` IDs with no label leakage, and deterministically reproducible by re-running the training script."
- **Enumerated `partial_wins`:**
  - **`p1`:** "Same rules on one further small JARVIS AI single-property task (fewer than 2,000 materials, at least 3 entries on the leaderboard) named before the run starts" — `tinnet_N_ead` (`AI-SinglePropertyPrediction-ead-tinnet_N-test-mae`, $N = 327$, 5 entries on the live leaderboard, live best `alignn = 0.0871 eV`).
  - **`p2`:** "5-fold CV study on `train`+`val` showing the claimed model's advantage over a reproduced `matminer_xgboost` baseline with a paired test, published with the predictions"
- **`verification_method`:**
  "Fetch the live leaderboard page at verification time to confirm current best MAE; verify zero intersection between `train`+`val` and `test` IDs in the `.json.zip` benchmark file; re-run training from scratch on `train`+`val` IDs only; compute test MAE with `sklearn.metrics.mean_absolute_error` and a 1,000-sample bootstrap CI."

---

## 2. Independent Checker Verification (Written Before Reading Author Code)

We wrote and executed an independent verification script (`indep_jarvis_check.py`) directly from the specification in `claim/CLAIM.md` before reading the author's code.

### 2.1 Saved Artifact Integrity (Byte Sizes and SHA-256 Digests)

All 20 saved artifacts inside `claim/` were verified for existence, exact byte count, and SHA-256 digest:

| Relative File Path | Verified Size (Bytes) | Verified SHA-256 Digest |
| :--- | ---: | :--- |
| `claim/AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae.csv` | `1,076` | `6fa908bbd746495ee5dc1808fa483cd83106c932b5a0a2097fdf35b38df98ae2` |
| `claim/AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae.csv.zip` | `628` | `ac07d1423cb6ea587cb037b7555a8ce42c874b148b0af086f118bc4d576fdd32` |
| `claim/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv` | `3,012` | `79189386af5ae8c30bc79fb1f7bbc3839536a53616c1b5cb110471dd905a1c19` |
| `claim/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv.zip` | `1,395` | `ae3e9da2a4346116d9ea43fffead59bf67bb53bb948a5094fc23381e1432f6ac` |
| `claim/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv` | `1,159` | `1328eea4abc72755830ac8d1c848a0e01564aa16ccc0b603941b26d94c4fa570` |
| `claim/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv.zip` | `662` | `8ffcfb46f7bd52a11428b8f6c8239e0eac367d7956e217701316169a09f17a67` |
| `claim/cv5_oof_dft_3d_Tc_supercon.csv` | `33,638` | `baa4b5d6c48aadb661c2ffbc7063154700ffc6d4f9d7a8d6c59afe8dd52d4c22` |
| `claim/cv5_oof_dft_3d_exfoliation_energy.csv` | `45,178` | `d3a94e8543c3c3443424dd75d2b2dca17aa43b4bd15320695925ecbb833e2f64` |
| `claim/cv5_oof_tinnet_N_ead.csv` | `17,669` | `104b07f6c20bf883001ba4567df85bc232de8d30c17077f7bac26a362d8c8b63` |
| `claim/trained_models_jarvis_clss.npz` | `55,014` | `4fc5757ef96c86ab1361ac488a5ee376e5aeea57b29c03afa5befa1b54b21489` |
| `claim/jarvis_clss_results_manifest.json` | `10,165` | `9bd2bff5a465b8c32d355361f58c49d73413eb73f72b566994f56edcffdbd8db` |
| `claim/featurize_physics_clss.py` | `37,185` | `67b7872f5c6470446659e356ac9e1e955b642cb849968a64517758f8a5e266d5` |
| `claim/train_and_predict_jarvis_clss.py` | `30,043` | `907e5b94119f5983d6a89f17f4c3fe5827e5260145bc4f11c5e9b292ebdb9450` |
| `claim/author_checker_jarvis_clss.py` | `13,955` | `f8ba2764f0c05db80791c25e1e48d2b6c22f4d14a9923f81bdbf0e0e74db2f75` |
| `claim/data/clean_structures/dft_3d_Tc_supercon_structures.json.gz` | `68,559` | `04821b5bc28ee19c08e7ed332a344c4ff8aa37a495e217dd2a3d2e6ac29e74cc` |
| `claim/data/clean_structures/dft_3d_exfoliation_energy_structures.json.gz` | `223,997` | `e8450bf83da924881d410af339a5b291e7e30b0947bcf128e7892c54dee71be9` |
| `claim/data/clean_structures/tinnet_N_ead_structures.json.gz` | `24,792` | `b543684ef67423a590c41ed81f189701a1463324bc88055670f8df602122c290` |
| `claim/data/dft_3d_Tc_supercon.json.zip` | `3,951` | `e34fe109057b9dd7b4ae50b18fdec70cc156b6a994a02ec6f57f5c365f8a06dc` |
| `claim/data/dft_3d_exfoliation_energy.json.zip` | `5,502` | `d7a3127002098c3da40292bee8d78de0e45ca42bef81adc73a07bc47e900a9a4` |
| `claim/data/tinnet_N_ead.json.zip` | `3,081` | `14da9466b46ccd69aea116c6d6ef456da2c2cfe955b45b89105bb9f21acdfc49` |

### 2.2 Independent Split Hygiene & Structure Sanitization Audit

Directly parsing `claim/data/*.json.zip` and `claim/data/clean_structures/*_structures.json.gz`:
- **`dft_3d_Tc_supercon`**: `556` train + `30` val = `586` `train U val` IDs, `30` `test` IDs (`616` total). Overlap between `train U val` and `test` IDs = `0`. Every structure in `dft_3d_Tc_supercon_structures.json.gz` has strictly the 4 keys `['cartesian', 'coords', 'elements', 'lattice_mat']`.
- **`dft_3d_exfoliation_energy`**: `650` train + `81` val = `731` `train U val` IDs, `81` `test` IDs (`812` total). Overlap between `train U val` and `test` IDs = `0`. Every structure in `dft_3d_exfoliation_energy_structures.json.gz` has strictly the 4 keys `['cartesian', 'coords', 'elements', 'lattice_mat']`.
- **`tinnet_N_ead` (`p1`)**: `263` train + `32` val = `295` `train U val` IDs, `32` `test` IDs (`327` total, strictly fewer than 2,000 materials). Overlap between `train U val` and `test` IDs = `0`. Every structure in `tinnet_N_ead_structures.json.gz` has strictly the 4 keys `['cartesian', 'coords', 'elements', 'lattice_mat']`.
- Each `.csv.zip` archive contains the exact byte-for-byte copy of its corresponding `.csv` prediction file, with exact test-ID alignment and ground-truth targets matching `claim/data/*.json.zip` to within `1e-8`.

### 2.3 Independent Test MAE & 1,000-Sample 90% Bootstrap CI Verification

Computing `sklearn.metrics.mean_absolute_error` and the 1,000-sample bootstrap 90% confidence interval half-width $h_{90\%} = 0.5 (q_{95} - q_{05})$ across `np.random.default_rng(0)` and seeds `0..9`:

| Task | Live Best MAE | Verified Test MAE | Relative Reduction ($\ge 5\%$ req.) | Absolute Gain $\Delta\text{MAE}$ | Bootstrap $h_{90\%}$ (`seed=0`) | Max $h_{90\%}$ (`seeds 0..9`) | Upper Bound $\text{MAE} + h_{90\%}$ vs Live Best | Criterion Check |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `dft_3d_Tc_supercon` | `1.51870 K` (`atomgpt_model`) | **`0.902806 K`** | **`-40.5540%`** | **`+0.615894 K`** | **`0.367962 K`** (`[0.548054, 1.283978]`) | `0.367962 K` | `1.270768 K` vs `1.51870 K` | **PASS** |
| `dft_3d_exfoliation_energy` | `40.88700 meV/atom` (`matminer_xgboost`) | **`28.195924 meV/atom`** | **`-31.0394%`** | **`+12.691076 meV/atom`** | **`11.132579 meV/atom`** (`[18.510812, 40.775969]`) | `11.449430 meV/atom` | `39.328502` vs `40.88700 meV/atom` | **PASS** |
| `tinnet_N_ead` (`p1`) | `0.08710 eV` (`alignn`) | **`0.068908 eV`** | **`-20.8865%`** | **`+0.018192 eV`** | **`0.017247 eV`** (`[0.052454, 0.086948]`) | `0.017247 eV` | `0.086155 eV` vs `0.08710 eV` | **PASS (`p1`)** |

### 2.4 Independent Verification of Partial Win `p2` (5-Fold CV Paired Study on `train U val`)

From `claim/cv5_oof_*.csv`, our independent checker verified all out-of-fold (`5-fold` and analytical `LOO`) predictions against the ground-truth `train U val` targets and reproduced `matminer_xgboost` baseline:
- **`dft_3d_Tc_supercon` ($n = 586$)**: CLSS 5-fold OOF MAE = `1.984094 K` (analytical LOO MAE = `1.885324 K`) vs `matminer_xgboost` OOF MAE = `2.368224 K` (`-16.22%` 5-fold reduction, `-20.39%` LOO reduction; 1-sided paired Wilcoxon $p = 5.990 \times 10^{-9}$, LOO Wilcoxon $p = 1.256 \times 10^{-12}$; 1-sided paired $t$-test $p = 4.581 \times 10^{-5}$).
- **`dft_3d_exfoliation_energy` ($n = 731$)**: CLSS 5-fold OOF MAE = `32.672745 meV/atom` (analytical LOO MAE = `31.805270 meV/atom`) vs `matminer_xgboost` OOF MAE = `45.004627 meV/atom` (`-27.40%` 5-fold reduction, `-29.33%` LOO reduction; 1-sided paired Wilcoxon $p = 1.616 \times 10^{-18}$, LOO Wilcoxon $p = 1.269 \times 10^{-20}$; 1-sided paired $t$-test $p = 1.865 \times 10^{-14}$).
- **`tinnet_N_ead` ($n = 295$)**: CLSS 5-fold OOF MAE = `0.095629 eV` (analytical LOO MAE = `0.085702 eV`) vs `matminer_xgboost` OOF MAE = `0.165561 eV` (`-42.24%` 5-fold reduction, `-48.24%` LOO reduction; 1-sided paired Wilcoxon $p = 5.861 \times 10^{-15}$, LOO Wilcoxon $p = 2.066 \times 10^{-20}$; 1-sided paired $t$-test $p = 2.922 \times 10^{-15}$).

### 2.5 Negative Controls (Corrupted / Constant / Permuted Predictions)

Our independent checker tested three negative controls on each benchmark and confirmed that all three fail the success criterion:
- **`dft_3d_Tc_supercon`**: Constant `train_mean` MAE = `2.7435 K` (fails), constant `train_median` MAE = `1.5157 K` with $\text{MAE} + h_{90\%} = 2.4204\text{ K}$ exceeding `1.5187 K` (fails), scrambled test predictions MAE = `1.1076 K` with $h_{90\%}$ failing the CI gate (fails), and 400 training-label permutations have null MAE `2.0504 +/- 0.2816 K` (`min = 1.4471 K`, `0/400` permutations reaching `0.9028 K`).
- **`dft_3d_exfoliation_energy`**: Constant `train_mean` MAE = `60.2757 meV/atom` (fails), constant `train_median` MAE = `48.8386 meV/atom` (fails), scrambled test predictions MAE = `78.1427 meV/atom` (fails), and 400 training-label permutations have null MAE `62.3599 +/- 4.0929 meV/atom` (`min = 53.3428 meV/atom`, `0/400` reaching `28.1959 meV/atom`).
- **`tinnet_N_ead`**: Constant `train_mean` MAE = `0.4326 eV` (fails), constant `train_median` MAE = `0.4314 eV` (fails), scrambled test predictions MAE = `0.5710 eV` (fails), and 400 training-label permutations have null MAE `0.6760 +/- 0.0810 eV` (`min = 0.4541 eV`, `0/400` reaching `0.0689 eV`).

---

## 3. Code Audit & Dual Deterministic Execution of `claim/author_checker_jarvis_clss.py`

After completing our independent checker, we inspected `claim/featurize_physics_clss.py`, `claim/train_and_predict_jarvis_clss.py`, and `claim/author_checker_jarvis_clss.py`:
1. **Zero Test-Label or Transductive Feature Leakage:** In `claim/featurize_physics_clss.py`, all descriptors (`featurize_structure`, `extract_iso_homolog_signature`, `compute_single_sub_homolog_distance`, `extract_fracture_regime_vector`, `extract_canonical_adsorbate_slab`) are computed per crystal purely from `lattice_mat`, `coords`, `elements`, and `cartesian` plus fixed elemental tables (`jarvis` `cfid` and `magpie`). In `claim/train_and_predict_jarvis_clss.py`, `QuantileTransformer(random_state=42)`, target scales $\tau$, KRR dual weights $\alpha$, and LOO blending gates ($c_{\text{hom}} = 0.75$, $w_r = 0.85$) are fitted strictly on `(X_tr, y_tr)` (`train U val`) before evaluating on `X_ev`.
2. **Back-to-Back Deterministic Re-Training & Pointwise Inductive Check:** Running `python3 -B author_checker_jarvis_clss.py` twice in succession from `claim/` succeeded with exit code `0` (`real 6.67s` on Run 1, `real 6.40s` on Run 2) and produced identical bit-for-bit results:
   - `dft_3d_Tc_supercon`: `max |retrain - npz| = 0.0e+00`, `max |single_pt - batch| = 4.4e-15`
   - `dft_3d_exfoliation_energy`: `max |retrain - npz| = 0.0e+00`, `max |single_pt - batch| = 4.3e-14`
   - `tinnet_N_ead`: `max |retrain - npz| = 0.0e+00`, `max |single_pt - batch| = 3.6e-15`

All scratch files (`panel/reproduce_work`) and `__pycache__` directories were removed after verification.

pass: true
