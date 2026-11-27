# Criterion & Scope Audit (`criterion.md`)

- Context: fresh skeptic review of the packaged files only
- Target: `linear-baseline-perturbation-replogle-k562` (`known-knowns`, Partial Progress `p2` only)
- Package path: `known-knowns/linear-baseline-perturbation-replogle-k562/2026-10-25-mizopl-71c4fdf1`

## 1. Exact Target `p2` Criterion (`bank/targets.json`)

In `bank/targets.json` under `linear-baseline-perturbation-replogle-k562`:
- **`p2`**: *"Stratify perturbations by functional distance from the training set (for example, gene-ontology or pathway distance) and test whether the performance gap between linear and non-linear models widens for out-of-distribution perturbations."*

## 2. Verification of Narrowed `p2` Scope & Plain-Text Predictions

1. **Scope Narrowed Strictly to `p2`**:
   - Confirmed that `README.md`, `INDEX.csv`, `panel/gate.md`, `how-we-built-it/PREREG.md`, and `object/certificate_replogle_k562.json` claim **Partial Progress (`p2`) only**, dropping all full-win, `p1` (RPE1), and `p3` (re-running published deep models) claims.
2. **Stratification Results Verified From Plain-Text Per-Perturbation Predictions (`object/k562_p2_per_perturbation_metrics.tsv` & `object/k562_seed{1..5}_{dual,lpm}_predictions.tsv`)**:
   - **Pre-registered Hybrid GO + Training Co-Expression Distance (`nn_dist`, `seeds = 1..2` Panel A, $n = 262$)**:
     - $Q_1$ (`Q1_closest`, $n = 66$, $\bar{d}_{\text{NN}} = 0.354995$, cut point $\le 0.483539$): `lpm_selftrained` $L_2 = 4.345813$ vs. `hollow_loo_dual_lens` $L_2 = 2.940883$ ($\Delta L_2 = -1.404930$, **$-32.33\%$**); $R_{\Delta} = 0.581483 \to 0.806009$ ($\Delta R_{\Delta} = +0.224525$).
     - $Q_2$ (`Q2_mid_close`, $n = 65$, $\bar{d}_{\text{NN}} = 0.541724$, cut point $\le 0.590076$): $\Delta L_2 = -0.776871$ (**$-18.98\%$**); $\Delta R_{\Delta} = +0.219978$.
     - $Q_3$ (`Q3_mid_far`, $n = 65$, $\bar{d}_{\text{NN}} = 0.614727$, cut point $\le 0.647287$): $\Delta L_2 = -0.516892$ (**$-12.73\%$**); $\Delta R_{\Delta} = +0.172395$.
     - $Q_4$ (`Q4_farthest`, $n = 66$, $\bar{d}_{\text{NN}} = 0.692054$, $> 0.647287$): `lpm_selftrained` $L_2 = 3.887674$ vs. `hollow_loo_dual_lens` $L_2 = 3.483419$ ($\Delta L_2 = -0.404255$, **$-10.40\%$**); $R_{\Delta} = 0.373746 \to 0.497501$ ($\Delta R_{\Delta} = +0.123755$).
     - Continuous correlation: Spearman $r_s(d_{\text{NN}}, \Delta L_2) = +0.345058$ ($p = 9.7126 \times 10^{-9}$) and $r_s(d_{\text{NN}}, \Delta R_{\Delta}) = -0.198624$ ($p = 1.2297 \times 10^{-3}$).
   - **Pure Static 2023 `gene2go_all.pkl` Gene Ontology Distance (`nn_dist_go_only`, Zero Expression Data, `seeds = 1..2` Panel A, $n = 262$)**:
     - $Q_1$ ($n = 66$, $\bar{d}_{\text{GO}} = 0.225593$, cut point $\le 0.354418$): $\Delta L_2 = -1.267239$ (**$-27.68\%$**), $\Delta R_{\Delta} = +0.264148$.
     - $Q_2$ ($n = 65$, $\bar{d}_{\text{GO}} = 0.468277$, cut point $\le 0.580865$): $\Delta L_2 = -1.041199$ (**$-25.16\%$**), $\Delta R_{\Delta} = +0.229288$.
     - $Q_3$ ($n = 65$, $\bar{d}_{\text{GO}} = 0.675110$, cut point $\le 0.765714$): $\Delta L_2 = -0.466643$ (**$-11.77\%$**), $\Delta R_{\Delta} = +0.139177$.
     - $Q_4$ ($n = 66$, $\bar{d}_{\text{GO}} = 0.830265$, $> 0.765714$): $\Delta L_2 = -0.331111$ (**$-8.94\%$**), $\Delta R_{\Delta} = +0.107679$.
     - Continuous correlation: Spearman $r_s(d_{\text{GO}}, \Delta L_2) = +0.420798$ ($p = 1.1506 \times 10^{-12}$) and $r_s(d_{\text{GO}}, \Delta R_{\Delta}) = -0.410288$ ($p = 4.6401 \times 10^{-12}$).
   - **All 5 GEARS Simulation Splits (`seeds = 1..5`, $n = 677$)**:
     - Hybrid distance: Spearman $r_s(d_{\text{NN}}, \Delta L_2) = +0.365576$ ($p = 7.8036 \times 10^{-23}$), $r_s(d_{\text{NN}}, \Delta R_{\Delta}) = -0.199116$ ($p = 1.7542 \times 10^{-7}$).
     - Pure 2023 GO distance: Spearman $r_s(d_{\text{GO}}, \Delta L_2) = +0.489635$ ($p = 4.1704 \times 10^{-42}$), $r_s(d_{\text{GO}}, \Delta R_{\Delta}) = -0.432494$ ($p = 3.1338 \times 10^{-32}$).
3. **Null / Permutation Control Battery (`200` split runs on K562)**:
   - Shuffling held-out perturbation target labels collapses `hollow_loo_dual_lens` performance from $L_2 = 3.320307, R_{\Delta} = 0.620623$ to $L_2 = 4.971309 \pm 0.067250$ ($z = -24.55, p = 0.009901$) and $R_{\Delta} = 0.284854 \pm 0.010565$ ($z = +31.78, p = 0.009901$), worse than the uninformative `mean` baseline ($L_2 = 4.193494, R_{\Delta} = 0.407911$).

pass: true
