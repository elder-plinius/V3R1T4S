# The Record We Beat: Trastuzumab CDR-H3 Variant Binding (`LSSI-ETH/plmfit` `herH3` `one_vs_rest`)

## 1. Official Scoreboard & Dataset Reference

- **Target ID:** `plmfit-trastuzumab-cdrh3-binding-mcc` (*"Trastuzumab CDR-H3 variant binding (PLMFit herH3 one-vs-rest): beat the scoreboard MCC of 0.3898"*)
- **Scoreboard Table URL:** <https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md>
- **Upstream Repository & Commit:** <https://github.com/LSSI-ETH/plmfit> (`main` commit `9264ba768861d50e9ff7b4be9027f6c2d85d5cc6`)
- **Primary Paper:** Bikias, Stamkopoulos & Reddy, *Briefings in Bioinformatics* 26(4):bbaf381 (2025); original deep mutational scan by Mason et al., *Nature Biomedical Engineering* 5:600–612 (2021) (<https://github.com/dahjan/DMS_opt>).
- **UTC Fetch Time:** `2026-11-08T14:42:30Z`
- **Scoreboard Page SHA-256 (`README.md`, `14,780` bytes):** `51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`
- **Official Dataset URL:** <https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/data/herH3/herH3_data_full.csv>
- **Official Dataset SHA-256 (`data/herH3/herH3_data_full.csv`, `17,149,024` bytes, `36,560` rows):** `5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f`

### Exact Listed Scoreboard Row in `LSSI-ETH/plmfit/main/README.md`

```text
| Trastuzumab - one-vs-rest | 0.3898 | MCC | ProGen2-XL | LoRA- | 25% | CLS | Linear |
```

---

## 2. Scoreboard Comparison (`174` Single-Mutant Training Rows $\to$ `36,386` Multi-Mutant Test Rows, Seeds `42, 43, 44`)

| Role / Track | Model / Architecture | Total Parameters | 3-Seed Test `MCC` (`mean +- SD`) | Margin vs `0.3898` Bar | 1,000-Resample Bootstrap 95% CI | Test `AUROC` (`p2`) | Test `AP` (`p2`) | 1-Body `MCC` (`p3`) | Inductive-to-Oracle `MCC` Gap (`p4`) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Claimed Full Win (`Track B`, `L-PTCB-011`)** | **10-Fold CV-Learned Brier Shrinkage Stacking (`w*=[0.20,0.30,0.20,0.15,0.15]`) + Frozen `esm2_t6_8M` `[78:122]` + 2-Body Loop Potential + `LOTUS` CV** | **`7,513,338`** (`<= 10M`, `p1`) | **`0.421004 +- 0.001735`** | **`+0.031204`** (`>= +0.02`) | **`[0.412067, 0.430182]`** | **`0.789510 +- 0.000669`** | **`0.624177 +- 0.000884`** | `0.410402 +- 0.001592` (`+0.010601` 2b gain) | **`0.001752`** (`oracle = 0.422756`) |
| **Parameter-Free Canonical Law (`Track A`, `L-PTCB-008`)** | **Equal `1/5` Portfolio Prior + Frozen `esm2_t6_8M` `[78:122]` + Canonical $S = \tfrac{1}{2}(\mu_\ell + m_{-1}) - C_{\text{pair}}$ + `LOTUS` CV** | **`7,513,338`** (`<= 10M`, `p1`) | **`0.408391 +- 0.000411`** | **`+0.018591`** | **`[0.398892, 0.417982]`** | **`0.785602 +- 0.000461`** | **`0.622932 +- 0.000615`** | `0.401879 +- 0.000887` (`+0.006512` 2b gain) | **`0.001402`** (`oracle = 0.409793`) |
| **CPU-Only Baseline (`Bet #1`, `L-PTCB-001`)** | **Pure 1-Body BLOSUM62-Smoothed PSSM + Synthetic Product Convolution (Zero PLM, 100% CPU)** | **`200`** (`0` PLM, `p1`) | `0.300600 +- 0.006500` | `-0.089200` | — | `0.736800` | `0.550400` | `0.300600` (`1-body only`) | `0.035400` (`oracle = 0.336000`) |
| **Prev #1 (`LSSI-ETH/plmfit` Scoreboard)** | **`ProGen2-XL + LoRA-` (`25%`, `CLS`, `Linear`)** | `~6,400,000,000` (`6.4B`) | `0.3898` | `0.000000` | — | *(unreported)* | *(unreported)* | *(unreported)* | *(unreported)* |
