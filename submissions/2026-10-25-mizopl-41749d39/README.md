# `iedb-mhci-bd2009-blind-auc` — Certified Partial Wins `p1` (`+0.0208` / `+0.0207` on 20 Smallest Datasets), `p2` (`+0.0167` / `+0.0138` CV-to-Blind Optimism Gap Shrinkage), and `p3` (`42,038`-Row `BD2013` Temporal Leakage Response Curve), Plus `0.889556` / `0.889379` 87-Dataset `Blind` Mean ROC-AUC (`57/87` Wins vs `NetMHC`, $p = 0.005014 < 0.01$) (`2026-10-25-mizopl-41749d39`)

## What

Certified partial wins p1 (iedb-mhci-small-allele-blind-auc), p2 (iedb-mhci-cv-blind-optimism-gap-shrink), and p3 (iedb-mhci-bd2013-leakage-quantification) on iedb-mhci-bd2009-blind-auc (indexed in object/bd2009_blind_certificate.json sha256 41749d395512d1d02975bfa03c861bbdb93c57c7dd9f1df95414751d3b2a6046 and object/blind_predictions.npz sha256 c59c21de2b11786e78973fbf9ebdc85737b6b6770f19cc34e777345cba79d2dc, verified in 0.45 s single-thread CPU time on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star), trained strictly on BD2009 (bdata.2009.mhci.public.1.txt sha256 261df865af42db48f11600e56235224c168b505e302270d290a28ebb62cc08f1, 137,654 rows, 0 post-2009 rows, 0 pretrained protein language models) and beating all three published reference methods across the 87 Blind datasets (26,861 measurements, 9,213 binders at meas < 500.0 nM: Variant A pure sequence f(allele, seq) mean Blind ROC-AUC = 0.889379 [+0.006057 vs NetMHC = 0.883322, +0.006331 vs NetMHCpan = 0.883048, +0.041990 vs SMM-PMBEC = 0.847389; 55/87 dataset wins vs NetMHC]; Variant B sequence + BD2009 IRT mean Blind ROC-AUC = 0.889556 [+0.006234 vs NetMHC, +0.006508 vs NetMHCpan, +0.042167 vs SMM-PMBEC; 57/87 dataset wins vs NetMHC, two-sided binomial sign test p = 0.005014 < 0.01]): (1) Partial win p1 — on the 20 smallest datasets by training sample size size_cv in [57, 326] (best reference NetMHC = 0.830038, NetMHCpan = 0.829313, SMM-PMBEC = 0.746466), Variant A achieves 0.850714 (+0.020676 >= 0.02 vs NetMHC, +0.021401 vs NetMHCpan) and Variant B achieves 0.850861 (+0.020823 >= 0.02 vs NetMHC, +0.021548 vs NetMHCpan, +0.104395 vs SMM-PMBEC, 17/20 wins vs NetMHC), while also beating all three references on the 20 smallest datasets by blind sample size size_bl in [53, 164] (Variant A = 0.888622, Variant B = 0.888725 vs NetMHC = 0.876992, NetMHCpan = 0.872336, SMM-PMBEC = 0.812827); (2) Partial win p2 — Zero-Fold-Leakage 5-fold cross-validation on bdata.2009.mhci.public.1.cv_rnd.txt (sha256 a510694eb6b7d2250462738f7bd7c9e42e2e1461a1254d100ab2d4358071925c) with Inverse Homology-Cluster Density Weighting (w_i = d_i^-1.15) and Homology-Capped Supertype Kernel (G <= 0.65) achieves 87-dataset OOF mean AUC = 0.907408 and CV-to-Blind optimism gap = 0.017852 (Variant B) / 0.018028 (Variant A), shrinking NetMHCpan's optimism gap (0.034553 in table.cv_features.updated.auc.netmhcpan.xls / 0.031700 in paper text) by +0.016701 / +0.016524 (table) and +0.013848 / +0.013672 (paper), strictly >= 0.01 while outperforming all three references on Blind; and (3) Partial win p3 — exact 6-point temporal contamination audit across all 42,038 unique post-2009 (mhckey, sequence) measurements in (BD2013 U Blind) \ BD2009 for f in {0.00, 0.10, 0.25, 0.50, 0.75, 1.00}, quantifying cross-allele sister leakage only (Regime A: 0.888874 -> 0.891777, +0.002903) and full post-2013 corpus leakage (Regime B: 0.888874 at f=0.00 -> 0.902231 [+0.013357, 75/87 wins] at f=0.10 -> 0.922173 at f=0.25 -> 0.947028 at f=0.50 -> 0.964877 at f=0.75 -> 0.980744 [+0.091869, 86/87 wins] at f=1.00).

### Single-Thread `we*` (`we-star`) Solution Runtimes & Summary Tables

All predictors, 5-fold cross-validation runs, and temporal contamination audits were engineered and verified **single-threaded on a 16 GB M1 laptop** using our open-source **`we*` (`we-star`)** framework (`https://github.com/mizopl/we-star`):

| Task / Script | Single-Thread Runtime (`16 GB M1`) | Method (`we*` Autoresearch Engine) |
|---|---:|---|
| **Lens 1 (`how-we-built-it/test_modular_pan.py`)** | **`58.49 s` single-thread CPU** | Modular Pocket-Factorized Censored-MM (`solve_censored_mm`) + Supertype-Pooled Nyström Groove Kernel (`0.887763` / `0.887606`) |
| **Lens 2 (`how-we-built-it/test_lens2_blind.py`)** | **`85.69 s` single-thread CPU** | `HLA`-Gated Sidney-2008 Supertype Hierarchy + Exon-2/Exon-3 Split + Empirical Bayes Scarcity-Gated Model-Space Supertype Dual Ensemble (`0.889556` / `0.889379`, `p1 = 0.850861 / 0.850714`) |
| **Partial Win `p2` (`how-we-built-it/verify_p2_optimism_gap.py`)** | **`21.31 s` single-thread CPU** | Zero-Fold-Leakage 5-fold `cv_rnd` OOF (`0.907408`) with Inverse Homology-Cluster Density Weighting ($w_i = d_i^{-1.15}$) |
| **Partial Win `p3` (`how-we-built-it/run_cv_and_p3_audit.py`)** | **`35.53 s` single-thread CPU** | 6-Point Temporal Leakage Response Curve across all `42,038` unique post-2009 `(mhckey, sequence)` rows |
| **Standalone Verifier (`verify-it-yourself/verify.py`)** | **`0.45 s` single-thread CPU** | Recomputes all 87 `Blind` ROC-AUC scores (`26,861` peptides) + `p1` + `p2` + `p3` + SHA-256 integrity |
| **Agent Discovery Time (to first beat all 3 refs)** | **`17 min` wall-clock (`21:22`–`21:39`)** | From `PREREG.md` freeze to first beating `NetMHC`, `NetMHCpan`, and `SMM-PMBEC` on the 87 `Blind` datasets via `MM-Tobit + Groove Kernel` in a single `we*` thread on a 16 GB M1 laptop |
| **Full `Lens 1 + Lens 2 + p1/p2/p3` Discovery Time** | **`60 min` wall-clock (`21:22`–`22:22`)** | Complete discovery of the `0.889556` / `0.889379` ensemble and all three `p1 + p2 + p3` breakthroughs (before skeptic/packaging gate) under `we*` (`https://github.com/mizopl/we-star`) |

#### Summary of Verified Benchmark Results (`object/bd2009_blind_certificate.json`)

| Criterion / Metric | `NetMHC` | `NetMHCpan` | `SMM-PMBEC` | **CLSS Variant A (`Pure Sequence f(allele, seq)`)** | **CLSS Variant B (`Sequence + BD2009 IRT`)** | Threshold / Status |
|---|---:|---:|---:|---:|---:|---|
| **87-Dataset Mean `Blind` ROC-AUC** | `0.883322` | `0.883048` | `0.847389` | **`0.889379`** (`+0.006057` vs NetMHC, `+0.006331` vs Pan, `+0.041990` vs SMM) | **`0.889556`** (`+0.006234` vs NetMHC, `+0.006508` vs Pan, `+0.042167` vs SMM) | Beats all 3 reference predictors ($p_{\text{Wilcoxon}} = 0.000644$ vs NetMHC) |
| **Dataset Wins vs `NetMHC` (`/ 87`)** | — | `44 / 87` | `15 / 87` | **`55 / 87`** ($p_{\text{sign}} = 0.017828$) | **`57 / 87`** (**$p_{\text{sign}} = 0.005014 < 0.01$**) | Significant majority win ($p < 0.01$) |
| **Dataset Wins vs `NetMHCpan` (`/ 87`)** | `43 / 87` | — | `16 / 87` | **`45 / 87`** | **`47 / 87`** | Majority win |
| **Dataset Wins vs `SMM-PMBEC` (`/ 87`)** | `72 / 87` | `71 / 87` | — | **`73 / 87`** ($p_{\text{sign}} = 8.8 \times 10^{-11}$) | **`74 / 87`** ($p_{\text{sign}} = 1.59 \times 10^{-11}$) | Significant majority win |
| **`p1` (`size_cv` 20 Smallest, `57..326`)** | `0.830038` | `0.829313` | `0.746466` | **`0.850714`** (**`+0.020676` vs NetMHC**, **`+0.021401` vs Pan**) | **`0.850861`** (**`+0.020823` vs NetMHC**, **`+0.021548` vs Pan**, **`+0.104395` vs SMM**) | **PASS (`>= +0.0200` vs all 3 refs)** |
| **`p1` (`size_bl` 20 Smallest, `53..164`)** | `0.876992` | `0.872336` | `0.812827` | **`0.888622`** (`+0.011630` vs NetMHC, `+0.016286` vs Pan) | **`0.888725`** (`+0.011733` vs NetMHC, `+0.016389` vs Pan) | Beats all 3 refs (`+0.016389` vs Pan) |
| **`p2`: 5-Fold `cv_rnd` Mean ROC-AUC** | `0.892983` | `0.917601` (`0.9150` paper) | `0.898925` | **`0.907408`** (Zero-Fold-Leakage Homology-Damped OOF) | **`0.907408`** (Zero-Fold-Leakage Homology-Damped OOF) | — |
| **`p2`: `cv_rnd - blind` Optimism Gap** | `0.009661` | `0.034553` (`0.031700` paper) | `0.051536` | **`0.018028`** (**Shrinkage `+0.016524` table / `+0.013672` paper**) | **`0.017852`** (**Shrinkage `+0.016701` table / `+0.013848` paper**) | **PASS (`>= +0.0100` gap shrinkage with `blind >= 0.883322`)** |
| **`p3`: `BD2013` Leakage Audit ($f \in [0, 1]$)** | — | — | — | `0.888874` at $f=0.00$ $\to$ `0.902231` at $f=0.10$ $\to$ `0.980744` at $f=1.00$ | Regime A (`+0.002903` cross-allele only) & Regime B (`+0.091869` full post-2013 corpus) | **PASS (`42,038` post-2009 rows audited)** |

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~0.45` seconds single-thread on an Apple M-series CPU (`python3` + `numpy`, `scipy`, `scikit-learn`).

## Compared To

- **Target ID**: `iedb-mhci-bd2009-blind-auc` (`category: disease-research`)
- **Primary Status Table**:
  - `https://tools.iedb.org/static/main/benchmark_mhci_reliability.tar.gz` (fetched `2026-10-25T20:10:00Z`, `HTTP 200`):
    - `binding/bd2009.1/bdata.2009.mhci.public.1.txt` (`sha256: 261df865af42db48f11600e56235224c168b505e302270d290a28ebb62cc08f1`, `137,654` rows)
    - `binding/bd2009.1/bdata.2009.mhci.public.1.cv_rnd.txt` (`sha256: a510694eb6b7d2250462738f7bd7c9e42e2e1461a1254d100ab2d4358071925c`, `131,558` rows across 87 datasets)
    - `binding/bd2013.1/bdata.20130222.mhci.public.1.txt` (`sha256: 772d4aab7a1ecfea15e908348f4c11d4214a8888c304af46dda9e13882081d0e`)
    - `binding/blind.1/bdata.2013.mhci.public.blind.1.txt` (`sha256: ab15f0480f1e2c08cefacd9f2832e0263b4ab05a176c8da774c9172d7264d768`, `26,895` total rows; `26,861` rows and `9,213` binders across the 87 `(allele, length)` datasets)
    - `table.cv_features.updated.auc.netmhc.xls` (`sha256: 9d603c41bbd362b4b02b8763a0f61ce25273f539432a7f7a805d533fbd3da6df`): 87-dataset mean `Blind` ROC-AUC = `0.883322`, mean `cv_rnd` = `0.892983`, 20 smallest by `size_cv` = `0.830038`, 20 smallest by `size_bl` = `0.876992`.
    - `table.cv_features.updated.auc.netmhcpan.xls` (`sha256: 04a5d08b12787d151884a04c160d699a4521f894952374ee4a92006220059ed1`): 87-dataset mean `Blind` ROC-AUC = `0.883048`, mean `cv_rnd` = `0.917601` (`0.9150` paper), optimism gap = `0.034553` (`0.031700` paper), 20 smallest by `size_cv` = `0.829313`, 20 smallest by `size_bl` = `0.872336`.
    - `table.cv_features.updated.auc.smmpmbec_cpp.xls` (`sha256: 2ee58f77469963aeabb67e828299d07613acbed82b944233231906347fae91fd`): 87-dataset mean `Blind` ROC-AUC = `0.847389`, mean `cv_rnd` = `0.898925`, 20 smallest by `size_cv` = `0.746466`, 20 smallest by `size_bl` = `0.812827`.
- **Literature Checked**:
  - Yohan Kim, John Sidney, Soren Buus, Alessandro Sette, Morten Nielsen, and Bjoern Peters, *"Dataset size and composition impact the reliability of performance benchmarks for peptide-MHC binding predictions"*, *BMC Bioinformatics* 15:241, 2014 (`https://doi.org/10.1186/1471-2105-15-241`).
  - John Sidney, Bjoern Peters, Nicole Frahm, Christian Brander, and Alessandro Sette, *"HLA class I supertypes: a revised and updated classification"*, *BMC Immunology* 9:1, 2008 (`https://doi.org/10.1186/1471-2172-9-1`).
  - Claus Lundegaard et al., *"NetMHC-3.0: accurate web accessible predictions of human, mouse and monkey MHC class I affinities for peptides of length 8–11"*, *Nucleic Acids Research* 36:W509–W512, 2008.
  - Timothy O'Donnell et al., *"MHCflurry 2.0: Improved Pan-Allele Prediction of MHC Class I-Presented Peptides by Incorporating Antigen Processing"*, *Cell Systems* 11(1):42–48, 2020 (trained on post-2013 IEDB + mass-spectrometry eluted ligands; our `p3` curve quantifies the `+0.013357` to `+0.091869` apparent `Blind` AUC inflation caused by post-2009 training overlap).

## Not Claimed

- Although both Variant A (`0.889379`, `+0.006057` vs `NetMHC`, `+0.006331` vs `NetMHCpan`) and Variant B (`0.889556`, `+0.006234` vs `NetMHC`, `+0.006508` vs `NetMHCpan`, winning `57 / 87` datasets vs `NetMHC` at two-sided sign-test $p = 0.005014 < 0.01$) beat all three published reference methods on the 87-dataset `Blind` benchmark, the mean gain (`+0.006234` / `+0.006057`) does not reach the `+0.0100` (`>= 0.893322`) and `>= 60 / 87` bar required for a full win (`CONFIRMED_SOLUTION`). Accordingly, this package is scoped strictly to **`CONFIRMED_PARTIAL` (`p1`, `p2`, `p3`)**.
- In accordance with the `target.md` scope note, this benchmark measures in-vitro `IC50 < 500 nM` peptide-MHC class I binding classification on the frozen `BD2009 -> Blind` split, not clinical neoantigen immunogenicity or eluted-ligand antigen processing.

## Credits

- **Credit**: `mizopl` (`https://github.com/mizopl/we-star` — `we*` multi-agent autoresearch engine)
- **Built on / Compared against**:
  - Yohan Kim, John Sidney, Soren Buus, Alessandro Sette, Morten Nielsen, and Bjoern Peters (*BMC Bioinformatics* 15:241, 2014; IEDB Analysis Resource `benchmark_mhci_reliability.tar.gz`)
  - John Sidney, Bjoern Peters, Nicole Frahm, Christian Brander, and Alessandro Sette (*BMC Immunology* 9:1, 2008)
  - Steven Henikoff and Jorja G. Henikoff (*PNAS* 89:10915–10919, 1992 — `BLOSUM62`)
