# Pre-Registration — `iedb-mhci-bd2009-blind-auc` (`2026-10-25-2115`)

frozen_utc: 2026-10-25T20:15:00Z
null_test: required

## 1. Frozen Training & Evaluation Split
- **Training corpus (strict zero post-2009 leakage):** `bdata.2009.mhci.public.1.txt` (`137,654` peptide-MHC measurements compiled in 2009, SHA-256 `261df865af42db48f11600e56235224c168b505e302270d290a28ebb62cc08f1`) and its official 5-fold cross-validation partition `bdata.2009.mhci.public.1.cv_rnd.txt` (`131,558` rows across the 87 `(allele, length)` benchmark datasets, SHA-256 `a510694eb6b7d2250462738f7bd7c9e42e2e1461a1254d100ab2d4358071925c`).
- **Held-out prospective test set (`Blind`):** `bdata.2013.mhci.public.blind.1.txt` (`26,895` total rows; `26,861` post-2009 peptide-MHC measurements across the exact 87 `(allele, length)` datasets, SHA-256 `ab15f0480f1e2c08cefacd9f2832e0263b4ab05a176c8da774c9172d7264d768`).
- **Strict Contamination Firewall:**
  - No post-2009 protein language model (ESM, ProtTrans, AlphaFold) and no post-2009 MHC predictor (NetMHCpan-3.0/4.0/4.1, MHCflurry) is imported or queried.
  - All model parameters, allele representations, and hyperparameters are learned strictly from `BD2009` (`bdata.2009.mhci.public.1.txt` / `cv_rnd`) plus standard pre-2009 static amino-acid physicochemical tables (`BLOSUM62` [Henikoff & Henikoff 1992] and Kyte–Doolittle hydropathy [1982]).
  - `bdata.20130222.mhci.public.1.txt` (`BD2013`, SHA-256 `772d4aab7a1ecfea15e908348f4c11d4214a8888c304af46dda9e13882081d0e`) is touched **only** in the isolated `p3` leakage-quantification experiment to measure how much apparent `blind` AUC a contaminated predictor gains when `BD2013` rows leak into training.

## 2. Evaluation Metric & Win Thresholds
- **Binder definition:** Following Kim et al. (2014) and verified with `0` mismatches against `size_cv_binder` and `size_bl_binder` across all 87 `(allele, length)` datasets in `table.cv_features.updated.auc.netmhcpan.xls` (SHA-256 `04a5d08b12787d151884a04c160d699a4521f894952374ee4a92006220059ed1`), a peptide measurement is a positive binder (`y = 1`) iff `meas < 500.0` nM (`log10(meas) < log10(500.0) = 2.6989700043360187`), and non-binder (`y = 0`) otherwise (`9,213` binders across the `26,861` Blind rows).
- **Primary metric:** Unweighted mean ROC-AUC (`sklearn.metrics.roc_auc_score`) across the 87 `(allele, length)` datasets in `Blind`.
- **Pre-registered success bars:**
  1. **`CONFIRMED_SOLUTION` (Full Win):**
     - 87-dataset mean `blind` AUC $\ge 0.883322 + 0.01 = \mathbf{0.893322}$ (beating `NetMHC = 0.883322`, `NetMHCpan = 0.883048`, and `SMM-PMBEC = 0.847389` by $\ge +0.01$).
     - Strict per-dataset `blind` AUC higher than the best reference method on **$\ge 60 / 87$** individual datasets (two-sided exact binomial sign test $p < 0.01$).
  2. **`p1` (`iedb-mhci-small-allele-blind-auc`):**
     - Mean `blind` AUC on the 20 smallest datasets beats the best reference method by **$\ge +0.02$** (on the 20 smallest datasets by `size_cv` $\in [57, 326]$, where best ref `NetMHC = 0.830038` $\to$ bar $\ge 0.850038$; also reported on the 20 smallest by `size_bl` $\in [53, 164]$, where best ref `NetMHC = 0.876992`).
  3. **`p2` (`iedb-mhci-cv-blind-optimism-gap-shrink`):**
     - Shrink the cross-validation-to-blind optimism gap $\Delta_{\text{opt}} = \text{mean}(\text{AUC}_{\text{cv\_rnd}}) - \text{mean}(\text{AUC}_{\text{blind}})$ below `NetMHCpan`'s gap (`0.031700` in paper text / `0.034553` in updated table) by **$\ge 0.01$** (i.e. $\Delta_{\text{opt}} \le \mathbf{0.021700}$) while maintaining $\text{mean}(\text{AUC}_{\text{blind}}) \ge 0.883322$.
  4. **`p3` (`iedb-mhci-bd2013-leakage-quantification`):**
     - Measure exact apparent `blind` AUC inflation across contamination fractions $f \in \{0.00, 0.10, 0.25, 0.50, 0.75, 1.00\}$ of the `42,038` unique post-2009 `(mhckey, sequence)` measurements leaked into training for the exact same model architecture.
