# Prospective Pre-Registration — `plmfit-trastuzumab-cdrh3-binding-mcc`

- `target_id`: `plmfit-trastuzumab-cdrh3-binding-mcc`
- `freeze_utc`: `2026-11-08T12:30:00Z`
- `null_test`: `required`
- `primary_metric`: `sklearn.metrics.matthews_corrcoef` (`MCC`) on the `36,386` rows with `one_vs_rest == 'test'` in `data/herH3/herH3_data_full.csv` (`sha256: 5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f`)
- `scoreboard_bar`: `0.3898` (`ProGen2-XL + LoRA-` at `https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md`, `sha256: 51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`)
- `full_win_threshold`: `0.4098` (`>= 0.3898 + 0.02`, reported as `mean +- SD` over 3 seeds `[42, 43, 44]` with 1,000-resample bootstrap 95% CI excluding `0.3898`)

## 1. Frozen Inductive Training & Thresholding Protocol

1. **Strict Inductive Split:** Fit all site posteriors, linear ridge/logistic probes, stacking weights, loop potential weights, and decision thresholds strictly on the `174` single-mutant rows (`173` `one_vs_rest == 'train'` + `1` `one_vs_rest == 'validation'`). Zero held-out `one_vs_rest == 'test'` rows (`36,386` multi-mutants with `no_mut in 2..10`) may be accessed during training, feature scaling, or threshold selection.
2. **Pretraining Cap (`p1`):** Use at most `10,000,000` parameters (`facebook/esm2_t6_8M_UR50D`, `7,512,474` frozen parameters pretrained strictly on generic `UniRef50` sequences, plus `864` linear/empirical-Bayes parameters = `7,513,338 <= 10M`).
3. **Threshold-Free Ranking (`p2`), Epistatic Ablation (`p3`), and Threshold Audit (`p4`):** Report `AUROC` and `Average Precision (AP)` on all `36,386` test rows (`p2`), compare `1-body` position-wise vs `2-body` pairwise epistatic scoring (`p3`), and select the binary decision threshold `tau_CV` strictly via `argmax_th OOF_MCC` inside `10-Fold Stratified CV` on the `174` training rows using the Law of the Unconscious Statistician (`LOTUS`) multi-mutant expectation (`p4`).
4. **Permutation Null Test (`null_test.md`):** Run `B = 500` independent permutations (`seed = 20261108`) of the `36,386` test labels against the 3-seed predictions and require `real_beats_all_controls: yes`.
