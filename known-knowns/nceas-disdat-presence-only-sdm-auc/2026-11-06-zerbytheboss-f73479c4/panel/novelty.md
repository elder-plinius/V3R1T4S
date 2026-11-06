# Skeptic 2: Prior Art & Benchmark Novelty Audit

context: independent literature and benchmark audit started from target specification and package files only

## Audit Summary

1. Audited the published benchmark records in `known-unknowns/ecology/nceas-disdat-presence-only-sdm-auc.md`: DeepMaxent TGB (Ryckewaert et al. 2025, `arXiv:2412.19217` Table 3, 6-region unweighted mean ROC AUC = `0.768`, win bar `0.768 + 0.005 = 0.773`), Anand, Deneu & Radeloff (PNAS 2026, 217-species `< 1,000` PO median ROC AUC = `0.774`), and TabPFN-ens (Doi et al. 2026, `arXiv:2603.05062` Table 1 & Table S2, zero-shot 6-region mean = `0.736`, 217-species median = `0.758`, LORO regional bests `NZ 0.759` and `SA 0.820`).
2. Verified that `tgb_hybrid_v3` achieves a 6-region unweighted mean ROC AUC of `0.77336 > 0.77300` (`AWT 0.7358`, `CAN 0.7326`, `NSW 0.7603`, `NZ 0.7536`, `SA 0.8077`, `SWI 0.8502`), beats 4 of 6 regional records (`AWT`, `CAN`, `NSW`, `SWI`), and achieves a 217-species median ROC AUC of `0.78457 > 0.77400` (225-species median = `0.79149`), and `tgb_hybrid_v2` achieves `0.77315 > 0.77300` and `0.78219 > 0.77400`.
3. Confirmed that full `win` and partial wins `p1`, `p2`, and `p3` are all satisfied.

pass: true
