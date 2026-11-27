# Null / Permutation Control Battery (`null_test.md`)

- **Target ID**: `linear-baseline-perturbation-replogle-k562` (`known-knowns`, Partial Progress `p2` only)
- **Dataset**: `replogle_k562_essential` (`seeds = 1..2` Panel A splits, $n = 262$ held-out perturbations: `134` in `seed 1`, `128` in `seed 2`)
- **Control Design**: `100` independent random permutations per split (`200` split evaluations total) of the held-out perturbation target gene labels $p^* \mapsto \pi(p^*)$ while keeping the training split (`train`), control baseline (`ctrl`), and all fitted model operators (`Lens 1` + `Lens 2`) unchanged.

---

## 1. Purpose of the Null Control

In `hollow_loo_dual_lens`, predictions for a held-out perturbation $p^*$ depend on the identity of $p^*$ through two target-specific pathways:
1. **Lens 1 (`Cis-Knockdown + De-Spiked Bilinear`)**: Applies direct cis-knockdown attenuation at read-out gene index $g = p^*$ and projects $p^*$'s training-expression embedding through the shrinkage bilinear operator.
2. **Lens 2 (`Hollow-LOO Multi-Scale GO + Co-Expression Graph Resolvent`)**: Queries $p^*$'s Gene Ontology (`gene2go_all.pkl`) and training co-expression neighborhood among training perturbations $\mathcal{P}_{\text{train}}$.

If the observed improvements over `lpm_selftrained` ($L_2 = 4.097028 \to 3.320307$, $R_{\Delta} = 0.435544 \to 0.620623$) and the `p2` functional-distance gradient ($Q_1$ $\Delta L_2 = -32.33\%$ vs. $Q_4$ $\Delta L_2 = -10.40\%$) were an artifact of global shrinkage toward the training mean $\mu_{\text{train}}$, permuting the held-out query identities $p^* \mapsto \pi(p^*)$ would preserve performance. Conversely, if the gain comes from genuine target-specific cis-attenuation and functional pathway alignment, permuting held-out target labels must collapse performance below the uninformative `mean` baseline.

---

## 2. Results (`object/certificate_replogle_k562.json` $\to$ `null_permutation_controls`)

| Metric | Real `hollow_loo_dual_lens` | `lpm_selftrained` Baseline | Uninformative `mean` Baseline | Permuted Target-Label Null (`100` perms $\times 2$ splits = `200` runs) | Null Min $\dots$ Max | $z$-Score (Real vs. Null) | Empirical $p$-Value |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Mean $L_2 \downarrow$** | **`3.320307`** | `4.097028` | `4.193494` | `4.971309 ± 0.067250` | `[4.798990, 5.163161]` | **`-24.55`** | **`0.009901` (`1/101`)** |
| **Mean $R_{\Delta} \uparrow$** | **`0.620623`** | `0.435544` | `0.407911` | `0.284854 ± 0.010565` | `[0.250656, 0.311606]` | **`+31.78`** | **`0.009901` (`1/101`)** |

Every single one of the `100` paired permutation trials performs substantially worse than both the real `hollow_loo_dual_lens` predictions ($z = -24.55$ on $L_2$, $z = +31.78$ on $R_{\Delta}$) and the uninformative `mean` baseline ($L_2 = 4.971309 > 4.193494$; $R_{\Delta} = 0.284854 < 0.407911$), confirming that the predictions rely on genuine target-gene identity and functional pathway alignment.
