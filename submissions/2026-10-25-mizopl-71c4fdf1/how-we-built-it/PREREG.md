# Pre-Registration — `linear-baseline-perturbation-replogle-k562`

```yaml
id: linear-baseline-perturbation-replogle-k562
frozen_utc: "2026-10-25T22:10:00Z"
metric: mean_and_median_L2_top1000_expr_genes_and_pearson_delta
direction: min_for_L2_max_for_pearson_delta
baseline_to_beat:
  replogle_k562_essential_panel_A_seeds_1_2:
    lpm_selftrained_l2_mean: 4.097028
    lpm_selftrained_l2_median: 3.805557
    best_published_l2_mean_gears: 4.078658
    best_published_l2_median_uce: 3.766328
    target_l2_mean_5pct_below_lpm: 3.892177
    lpm_selftrained_r2_delta_mean: 0.435544
    lpm_selftrained_r2_delta_median: 0.426484
  replogle_rpe1_essential_panel_A_seeds_1_2:
    lpm_selftrained_l2_mean: 5.390179
    lpm_selftrained_l2_median: 5.152959
    best_published_l2_mean_lpm: 5.390179
    target_l2_mean_5pct_below_lpm: 5.120670
    lpm_selftrained_r2_delta_mean: 0.680388
    lpm_selftrained_r2_delta_median: 0.791594
null_test: required
```

## 1. Zero-Leakage & Split Firewall
1. For every dataset (`replogle_k562_essential`, `replogle_rpe1_essential`, `adamson`) and every split seed (`seed in 1..2` for exact Source Data comparison, and `seed in 1..5` for full 5-seed GEARS simulation evaluation):
   - Only perturbations with `training == "train"` (and `condition == "ctrl"`, which GEARS assigns to `"train"`) may be used to fit:
     - the control baseline vector $b = \text{rowMeans}(X[:, \text{condition} == \text{ctrl}])$,
     - the training mean perturbation effect $\mu_{\text{train}} = \text{rowMeans}(Y_{\text{train}} - b)$,
     - the cis-knockdown attenuation parameters $(\alpha_{\text{cis}}, \beta_{\text{cis}}, \gamma_{\text{cis}})$,
     - all gene and perturbation PCA/SVD subspaces and co-expression matrices, and
     - all kernel ridge / resolvent weights.
   - Hyperparameters are fixed across all seeds and datasets using inner cross-validation on `train` (or `val` when evaluating strictly on `test`). To guarantee zero leakage even when evaluating on the paper's `Panel A` (`test + val` union), all model parameters and hyperparameters in our primary evaluation are fitted **100% on `train` alone** (never touching `val` or `test` during fitting or tuning!).

## 2. Pre-Declared Functional Embedding for `p2`
- Prior to evaluating held-out errors as a function of nearest-neighbor distance (`p2`), we pre-declare the target-gene functional similarity metric $S_{\text{func}}(p, q)$ as the convex combination of (a) the Gene Ontology Jaccard similarity from GEARS's `gene2go_all.pkl` / `go_essential_all.csv` and (b) the cosine similarity of standardized read-out expression profiles across `train` pseudobulks and `ctrl` cells, with nearest-training-neighbor distance defined as:
  $$d_{\text{NN}}(p, \mathcal{T}_{\text{train}}) = 1 - \max_{q \in \mathcal{T}_{\text{train}}} S_{\text{func}}(p, q)$$
- We pre-register the hypothesis for `p2`: held-out perturbations $p$ in the closest functional distance tertile/quartile ($d_{\text{NN}}$ small) achieve a strictly larger $L_2$ error reduction and higher Pearson $\Delta$ gain over `mean` and `lpm_selftrained` than held-out perturbations in the farthest distance tertile/quartile ($d_{\text{NN}}$ large), verified by monotonic bin stratification and Spearman correlation.

## 3. Null / Randomization Control Battery (`null_test: required`)
- We will execute at least 200 target-gene label permutation controls per split (`>= 400` total randomized controls across splits) where the mapping between held-out perturbation target gene names $p$ and their functional/co-expression embeddings + cis-target indices is randomly permuted.
- Any genuine biological signal must beat the best of all permutation controls by $>5\sigma$, whereas permuted controls must degrade back to (or worse than) the uninformative `mean` baseline.
