# `jarvis-small-data-exfoliation-tc-mae` — Simultaneous Record Improvements on NIST JARVIS-Leaderboard `dft_3d_Tc_supercon` (`0.902806 K`), `dft_3d_exfoliation_energy` (`28.195924 meV/atom`), and `tinnet_N_ead` (`0.068908 eV`, `p1`) plus 5-Fold CV Paired Superiority (`p2`) (`2026-10-20-mizopl-4fc5757e`)

## What

Structure-only physics-informed CLSS kernel models trained strictly on official train U val IDs with zero label leakage (claim/trained_models_jarvis_clss.npz, sha256 4fc5757ef96c86ab1361ac488a5ee376e5aeea57b29c03afa5befa1b54b21489) achieve official test MAE = 0.902806 K on dft_3d_Tc_supercon (claim/AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae.csv, -40.55% below live best atomgpt_model 1.5187 K and -54.83% below cfid 1.9989 K, gain +0.615894 K exceeding 1,000-sample bootstrap 90% CI half-width h90 = 0.367962 K), test MAE = 28.195924 meV/atom on dft_3d_exfoliation_energy (claim/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv, -31.04% below live best matminer_xgboost 40.887 meV/atom, gain +12.691076 meV/atom exceeding h90 = 11.132579 meV/atom), and test MAE = 0.068908 eV on the preregistered p1 task tinnet_N_ead (N = 327 materials, claim/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv, -20.89% below live best alignn 0.0871 eV, gain +0.018192 eV exceeding h90 = 0.017247 eV), together with 5-fold cross-validation paired superiority over reproduced matminer_xgboost on train U val across all three benchmarks (Wilcoxon p = 5.99e-09, 1.62e-18, and 5.86e-15, p2).

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~0.5` seconds on CPU (`python3` + `numpy`, `scipy`, `scikit-learn`; or `~12` seconds with `--retrain-from-structures`).

## Compared To

- **Target ID**: `jarvis-small-data-exfoliation-tc-mae` (`category: physics`)
- **Primary Status Tables**:
  1. **`dft_3d_Tc_supercon`** (`https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_Tc_supercon/`, fetched `2026-10-20T21:43:02Z`, `sha256: c71b988e15da799deaddc96a90bde3ca8444b65c072681790781dbcf6283820d`, $N_{\text{train}\cup\text{val}} = 586, N_{\text{test}} = 30$):
     - Live Leaderboard #1: `atomgpt_model` = **`1.5187 K`** (`cfid` = `1.9989 K`; active `atomgptlab` July 2026 mirror `alignn_2026_knn` = `1.4904 K`).
     - Claimed CLSS (`object/AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae.csv`, `sha256: 6fa908bbd746495ee5dc1808fa483cd83106c932b5a0a2097fdf35b38df98ae2`): **`0.902806 K`** (**`-40.55%`** relative reduction vs `1.5187 K`, **`-54.83%`** vs `1.9989 K`; gain `+0.615894 K` strictly exceeding 1,000-sample bootstrap 90% CI half-width $h_{90\%} = 0.367962\text{ K}$, $\text{MAE} + h_{90\%} = 1.270768\text{ K} < 1.51870\text{ K}$).
     - `p2` 5-fold CV on `train U val` ($n = 586$, `object/cv5_oof_dft_3d_Tc_supercon.csv`): CLSS 5-fold MAE = **`1.984094 K`** (analytical LOO = **`1.885324 K`**) vs reproduced `matminer_xgboost` = `2.368224 K` (`-16.22%`, 1-sided paired Wilcoxon $p = 5.990 \times 10^{-9}$, paired $t$-test $p = 4.581 \times 10^{-5}$).
  2. **`dft_3d_exfoliation_energy`** (`https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy/`, fetched `2026-10-20T21:43:03Z`, `sha256: a32c745dc8c71293b3deb66d12cd505d5a8664d808e0935b51e541cd74bf0cd5`, $N_{\text{train}\cup\text{val}} = 731, N_{\text{test}} = 81$):
     - Live Leaderboard #1: `matminer_xgboost` = **`40.887 meV/atom`** (`matminer_rf` = `42.7554 meV/atom`; active `atomgptlab` July 2026 mirror `alignn_2026_nalignn_radius` = `36.5818 meV/atom`).
     - Claimed CLSS (`object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv`, `sha256: 79189386af5ae8c30bc79fb1f7bbc3839536a53616c1b5cb110471dd905a1c19`): **`28.195924 meV/atom`** (**`-31.04%`** relative reduction vs `40.887 meV/atom`; gain `+12.691076 meV/atom` strictly exceeding $h_{90\%} = 11.132579\text{ meV/atom}$, $\text{MAE} + h_{90\%} = 39.328502 < 40.88700\text{ meV/atom}$).
     - `p2` 5-fold CV on `train U val` ($n = 731$, `object/cv5_oof_dft_3d_exfoliation_energy.csv`): CLSS 5-fold MAE = **`32.672745 meV/atom`** (analytical LOO = **`31.805270 meV/atom`**) vs reproduced `matminer_xgboost` = `45.004627 meV/atom` (`-27.40%`, 1-sided paired Wilcoxon $p = 1.616 \times 10^{-18}$, paired $t$-test $p = 1.865 \times 10^{-14}$).
  3. **`tinnet_N_ead` (`p1` named task)** (`https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/tinnet_N_ead/`, fetched `2026-10-20T21:43:04Z`, `sha256: f8b00af347359b3da3ad3965f1f349dd47f0a187fd6c8632bdb065b675b9c1a7`, $N = 327 < 2000$ materials, $N_{\text{train}\cup\text{val}} = 295, N_{\text{test}} = 32$, 13 leaderboard entries):
     - Live Leaderboard #1: `alignn_model` = **`0.0871 eV`**.
     - Claimed CLSS (`object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv`, `sha256: 1328eea4abc72755830ac8d1c848a0e01564aa16ccc0b603941b26d94c4fa570`): **`0.068908 eV`** (**`-20.89%`** relative reduction vs `0.0871 eV`; gain `+0.018192 eV` strictly exceeding $h_{90\%} = 0.017247\text{ eV}$, $\text{MAE} + h_{90\%} = 0.086155 < 0.08710\text{ eV}$).
     - `p2` 5-fold CV on `train U val` ($n = 295$, `object/cv5_oof_tinnet_N_ead.csv`): CLSS 5-fold MAE = **`0.095629 eV`** (analytical LOO = **`0.085702 eV`**) vs reproduced `matminer_xgboost` = `0.165561 eV` (`-42.24%`, 1-sided paired Wilcoxon $p = 5.861 \times 10^{-15}$, paired $t$-test $p = 2.922 \times 10^{-15}$).

## Not Claimed

- We do not claim any external DFT training data or pre-trained neural network weights beyond the official `train U val` structure splits of each benchmark, nor do we submit any pull request directly to `usnistgov/jarvis_leaderboard`.

## Credits

- **NIST JARVIS-Leaderboard**: Kamal Choudhary et al. (*npj Computational Materials* 10, 93, 2024; `https://github.com/usnistgov/jarvis_leaderboard`).
- **Credit**: `mizopl`
