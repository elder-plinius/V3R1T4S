# Verification Gate (`linear-baseline-perturbation-replogle-k562`, Partial Progress `p2`)

- **Target ID**: `linear-baseline-perturbation-replogle-k562`
- **Category**: `known-knowns`
- **Package Directory**: `known-knowns/linear-baseline-perturbation-replogle-k562/2026-10-25-mizopl-71c4fdf1`
- **Certificate Path**: `object/certificate_replogle_k562.json` (`sha256: f7a404a7891275367e46e7e312084b42ce4e687274d7b72da6da4aa4f2794b5a`, `54,328` bytes)
- **Plain-Text Per-Perturbation Metrics**: `object/k562_p2_per_perturbation_metrics.tsv` (`sha256: 0e2ae30e6f9f0942b4adf46e9a2798d74206321ddb13b8dc4027f2c0a6fdfd75`, `176,975` bytes, `677` rows)

## Panel Review Summary

| File | Focus | Result |
| :--- | :--- | :--- |
| `panel/reproduce.md` | Standalone verification of plain-text per-perturbation K562 predictions, distances, and negative-control corruption tests | `pass: true` |
| `panel/novelty.md` | Verification of dated pre-registration (`2026-10-25T22:10:00Z`, commit `853db39`), static 2023 `gene2go_all.pkl` embedding, and training-only LOO quartile cut points | `pass: true` |
| `panel/criterion.md` | Verification of `p2` functional-distance stratification criteria on K562 (`seeds = 1..2` Panel A `n = 262` and `seeds = 1..5` `n = 677`) and null permutation controls | `pass: true` |

status: CONFIRMED_PARTIAL
confirmed_scope: Confirmed Partial Progress (p2) on linear-baseline-perturbation-replogle-k562: saved plain-text per-perturbation predictions for every held-out K562 perturbation across seeds 1..2 (n = 262 Panel A perturbations: 134 in seed 1, 128 in seed 2) and seeds 1..5 (n = 677 in-readout perturbations) stratify the performance gap between Hollow-LOO Dual-Lens and the paper's self-trained linear baseline (lpm_selftrained, K = 10 PCA, lambda = 0.1) by nearest-training-perturbation functional distance, showing that the gap is concentrated in close/in-distribution functional neighborhoods (Q1 delta L2 = -1.404930 or -32.33%, delta R_delta = +0.224525) and narrows monotonically for out-of-distribution perturbations (Q4 delta L2 = -0.404255 or -10.40%, delta R_delta = +0.123755; Spearman r_s = +0.345058, p = 9.7126e-09 on hybrid distance; Spearman r_s = +0.420798, p = 1.1506e-12 on static 2023 gene2go_all.pkl Gene Ontology distance).
