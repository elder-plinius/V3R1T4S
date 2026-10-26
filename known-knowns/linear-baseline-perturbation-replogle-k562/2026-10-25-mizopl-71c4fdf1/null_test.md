# Stage 3 Null / Permutation Control Battery (`null_test.md`)

- **Target:** `linear-baseline-perturbation-replogle-k562`
- **Reference:** Ahlmann-Eltze, Huber & Anders, *Nature Methods* 2025 (`doi:10.1038/s41592-025-02772-6`), repository `const-ae/linear_perturbation_prediction-Paper` at pinned commit `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`.
- **Certificate:** [`claim/certificate_replogle_k562.json`](object/certificate_replogle_k562.json) (`sha256 = 71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e`).
- **Execution Script:** [`claim/certify_all_splits_and_controls.py`](how-we-built-it/certify_all_splits_and_controls.py).

---

## 1. Null Control Design (Zero-Leakage Verification)

To prove that the gains of our **Hollow-LOO Dual-Lens** predictor over `lpm_selftrained` arise from genuine biological gene-gene structure in the training perturbations and the GO biological process graph — and **not** from shrink-to-mean bias, global variance scaling, or evaluation leakage — we executed a pre-registered (`PREREG.md`) permutation control battery across `300` split-level random permutations (`150` combined two-seed runs):

1. **`replogle_k562_essential` (`100` combined two-seed random permutations = `200` split-level runs):**
   - In each random realization $b \in \{1, \dots, 100\}$ and each split (`seed = 1`, `seed = 2`), we randomly permute the gene identity mapping (`train_pert_cols` and `g2go_idx`) of the training perturbations and GO nodes while keeping the exact expression matrix `X_mean`, control baseline `ctrl`, ridge penalties, Hollow-LOO operator, and variance-matching parameters identical.
2. **`replogle_rpe1_essential` (`50` combined two-seed random permutations = `100` split-level runs):**
   - Same random permutation protocol applied across `seed = 1` and `seed = 2` on `replogle_rpe1_essential` (`n = 413` held-out perturbations).

---

## 2. Quantitative Results (`300` Split-Level Permutations)

| Dataset | Split Universe | Real Model Mean $L_2$ | `lpm_selftrained` Mean $L_2$ | Null Permuted Mean $L_2$ ($\mu \pm \sigma$) | Best Null $L_2$ ($\min$) | Worst Null $L_2$ ($\max$) | $Z$-Score ($L_2$ vs Null) | Real Mean Pearson $\Delta$ | Null Mean Pearson $\Delta$ ($\mu \pm \sigma$) | Best Null Pearson $\Delta$ ($\max$) | $Z$-Score ($r_{\Delta}$ vs Null) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `replogle_k562_essential` | `Panel A` (`n = 262`, `100` combined / `200` split runs) | **`3.320307`** | `4.097028` | `4.971309 ± 0.067250` | `4.798990` | `5.163161` | **`24.55 σ`** | **`0.620623`** | `0.284854 ± 0.010565` | `0.311606` | **`31.78 σ`** |
| `replogle_rpe1_essential` | `Panel A` (`n = 413`, `50` combined / `100` split runs) | **`4.777953`** | `5.390179` | `6.231428 ± 0.064759` | `6.085542` | `6.392681` | **`22.44 σ`** | **`0.719286`** | `0.632151 ± 0.002595` | `0.638356` | **`33.57 σ`** |

---

## 3. Interpretation & Falsification Verdict

1. **Complete Collapse Under Gene-Identity Permutation:** When gene identities linking the training perturbations and GO graph to the held-out target genes are randomly permuted, performance degrades dramatically below both the real model and the uninformative `mean` baseline (`4.971309` vs `4.193494` on K562; `6.231428` vs `5.533708` on RPE1).
2. **Zero Overlap ($> 22\sigma$ Separation):** Across all `200` split evaluations on K562 (`100` combined runs), the best random realization achieved $L_2 = 4.798990$ and Pearson $\Delta = 0.311606$, separated from the real model ($L_2 = 3.320307$, Pearson $\Delta = 0.620623$) by **$24.55\sigma$** in $L_2$ and **$31.78\sigma$** in Pearson $\Delta$. On RPE1 (`100` split evaluations), the separation is **$22.44\sigma$** in $L_2$ and **$33.57\sigma$** in Pearson $\Delta$.
3. **Verdict:** **`NULL_TEST: PASS`**.
