# Null Test & Reference Verification — `iedb-mhci-bd2009-blind-auc` (`2026-10-25-2115`)

controls: 400
best_control: 0.519954
real: 0.889556
command: python3 verify-it-yourself/verify.py
real_beats_all_controls: yes

## 1. Exact Alignment of All 87 `(allele, length)` Benchmark Datasets
Across all 87 `(allele, length)` rows (`mhckey`) in `data/table.cv_features.updated.auc.{netmhc,netmhcpan,smmpmbec_cpp,smmpmbec_cpp_rerun}.xls`:
- Matching `bd2009["mhckey"]` (`bdata.2009.mhci.public.1.txt`) and `blind["mhckey"]` (`bdata.2013.mhci.public.blind.1.txt`, `26,861` measurements and `9,213` binders across the 87 datasets) with binder threshold `meas < 500.0` nM reproduces `size_cv`, `size_cv_binder`, `size_bl`, and `size_bl_binder` with **`0 / 87` mismatches**.

## 2. Reference Method Baseline Verification (`Kim et al., 2014`)
- **`NetMHC` (`table.cv_features.updated.auc.netmhc.xls`):**
  - 87-dataset mean `blind` AUC = **`0.883322`**
  - 87-dataset mean `cv_rnd` AUC = **`0.892983`** (`cv_rnd - blind` gap = `0.009661`)
  - 20 smallest datasets by `size_bl` (`53..164`) mean `blind` AUC = **`0.876992`**
  - 20 smallest datasets by `size_cv` (`57..326`) mean `blind` AUC = **`0.830038`**
- **`NetMHCpan` (`table.cv_features.updated.auc.netmhcpan.xls`):**
  - 87-dataset mean `blind` AUC = **`0.883048`**
  - 87-dataset mean `cv_rnd` AUC = **`0.917601`** (`cv_rnd - blind` gap = `0.034553`; paper text summary = `0.031700`)
  - 20 smallest datasets by `size_bl` (`53..164`) mean `blind` AUC = **`0.872336`**
  - 20 smallest datasets by `size_cv` (`57..326`) mean `blind` AUC = **`0.829313`**
- **`SMM-PMBEC` (`table.cv_features.updated.auc.smmpmbec_cpp.xls` / `rerun`):**
  - 87-dataset mean `blind` AUC = **`0.847389`**
  - 87-dataset mean `cv_rnd` AUC = **`0.898925`** (`rerun`: `0.901907`; `cv_rnd - blind` gap = `0.051536` / `0.054518`; paper text summary = `0.0449`)
  - 20 smallest datasets by `size_bl` (`53..164`) mean `blind` AUC = **`0.812827`**
  - 20 smallest datasets by `size_cv` (`57..326`) mean `blind` AUC = **`0.746466`**

## 3. Law `M5` 400-Control Random-Score Null Baseline on the 87 Blind Datasets
- Evaluating `400` independent standard-normal random score controls (`rng = np.random.default_rng(20261025)`) across the 87 `(allele, length)` datasets (`26,861` measurements) in `bdata.2013.mhci.public.blind.1.txt` yields:
  - Mean across 400 null controls = **`0.500020`** (`std = 0.006675`)
  - Maximum across 400 null controls (`best_control`) = **`0.519954`** (single-seed `seed=42` control = `0.504497`)
  - Real `BD2009`-trained predictor 87-dataset mean `Blind` ROC-AUC = **`0.889556`** (Variant B, $z = +58.36$) / **`0.889379`** (Variant A, $z = +58.33$), beating `400 / 400` controls (`real_beats_all_controls: yes`).

**Null Gate (`M5` / `K2`):** **PASS**.
