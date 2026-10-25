# Primary Status Table Snapshot (`iedb-mhci-bd2009-blind-auc`)

## 1. Live Status Source Fetched Before Claiming

- **Table URL:** `https://tools.iedb.org/static/main/benchmark_mhci_reliability.tar.gz` (and `http://tools.iedb.org/main/datasets/` / `https://doi.org/10.1186/1471-2105-15-241`)
- **Fetched UTC:** `2026-10-25T20:10:00Z`
- **HTTP Status:** `200 OK`
- **SHA-256 Checksums of Extracted Benchmark Files:**
  - `binding/bd2009.1/bdata.2009.mhci.public.1.txt`: `261df865af42db48f11600e56235224c168b505e302270d290a28ebb62cc08f1` (`137,654` rows; sole training corpus)
  - `binding/bd2009.1/bdata.2009.mhci.public.1.cv_rnd.txt`: `a510694eb6b7d2250462738f7bd7c9e42e2e1461a1254d100ab2d4358071925c` (`131,558` rows across 87 datasets; 5-fold CV split)
  - `binding/bd2013.1/bdata.20130222.mhci.public.1.txt`: `772d4aab7a1ecfea15e908348f4c11d4214a8888c304af46dda9e13882081d0e` (used **only** in the isolated `p3` leakage audit)
  - `binding/blind.1/bdata.2013.mhci.public.blind.1.txt`: `ab15f0480f1e2c08cefacd9f2832e0263b4ab05a176c8da774c9172d7264d768` (`26,895` total rows; `26,861` rows and `9,213` binders across the 87 `(allele, length)` datasets)
  - `table.cv_features.updated.auc.netmhc.xls`: `9d603c41bbd362b4b02b8763a0f61ce25273f539432a7f7a805d533fbd3da6df`
  - `table.cv_features.updated.auc.netmhcpan.xls`: `04a5d08b12787d151884a04c160d699a4521f894952374ee4a92006220059ed1`
  - `table.cv_features.updated.auc.smmpmbec_cpp.xls`: `2ee58f77469963aeabb67e828299d07613acbed82b944233231906347fae91fd`

## 2. Extracted Benchmark Metrics Compared Against (`Kim et al., BMC Bioinformatics 15:241, 2014`)

| Benchmark Metric / Partial Win | `NetMHC` | `NetMHCpan` | `SMM-PMBEC` | **CLSS Variant A (`Pure Seq`)** | **CLSS Variant B (`Seq + IRT`)** | Margin / Verdict |
|---|---:|---:|---:|---:|---:|---|
| **87-Dataset Mean `Blind` ROC-AUC** | `0.883322` | `0.883048` | `0.847389` | **`0.889379`** | **`0.889556`** | **`+0.006234` vs NetMHC (`57/87` wins, $p=0.005014 < 0.01$), `+0.006508` vs Pan (`47/87`), `+0.042167` vs SMM (`74/87`)** |
| **`p1` (`size_cv` 20 Smallest, `57..326`)** | `0.830038` | `0.829313` | `0.746466` | **`0.850714`** | **`0.850861`** | **`+0.020676` (A) / `+0.020823` (B) vs NetMHC ($\ge 0.02$), `+0.021401` (A) / `+0.021548` (B) vs Pan ($\ge 0.02$) — PASS** |
| **`p1` (`size_bl` 20 Smallest, `53..164`)** | `0.876992` | `0.872336` | `0.812827` | **`0.888622`** | **`0.888725`** | **`+0.011733` vs NetMHC, `+0.016389` vs NetMHCpan** |
| **`p2`: 5-Fold `cv_rnd` Mean ROC-AUC** | `0.892983` | `0.917601` (`0.9150` paper) | `0.898925` | **`0.907408`** | **`0.907408`** | Zero-Fold-Leakage Homology-Damped OOF |
| **`p2`: `cv_rnd - blind` Optimism Gap** | `0.009661` | `0.034553` (`0.031700` paper) | `0.051536` | **`0.018028`** | **`0.017852`** | **Shrinkage `+0.016701` (table) / `+0.013848` (paper) $\ge 0.01$ — PASS** |
| **`p3`: Post-2009 Leakage Audit (`42,038` rows)** | — | — | — | `0.888874` ($f=0.00$) | `0.891777` (Regime A, $f=1.00$) / `0.980744` (Regime B, $f=1.00$) | **`+0.013357` (`0.902231`, `75/87` wins) at $f=0.10$; `+0.091869` (`86/87` wins) at $f=1.00$ — PASS** |
