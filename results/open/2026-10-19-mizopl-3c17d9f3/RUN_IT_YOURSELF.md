# Run It Yourself (`immrep22-tcr-epitope-microauc`)

## One-line check

From the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

This runs `verify-it-yourself/check_immrep22_clss.py`, which verifies:
1. Exact 50-digit `Decimal` score moments and TCR sequence alignment across all 17 per-epitope prediction files (`object/clss_tcr_scores/{epitope}.txt`) and `object/clss_tcr_scores/testSet_Global.txt`, plus exact pointwise equality between positive test TCR scores in `{epitope}.txt` and `testSet_Global.txt`.
2. Re-running the unmodified official `the-record-we-beat/evaluate.py` (`sha256: 04fa0346aa914bab770f9adbd6326581026e0fa9b94ad734f3957c54be6778ed`) against `the-record-we-beat/true_set_labels/` and verifying exact agreement with `object/clss_tcr_stats.txt` (`_Average` MicroAUC `= 0.882173` vs `0.847347`, `+0.034826 >= +0.0200`; `15/17` epitope wins vs `tcrexab`; 1-sided Wilcoxon `p = 6.7139e-04 < 0.01`; `10,000`-resample paired bootstrap `100.00% >= 95%`; `SPRWYFYYL` MicroAUC `= 0.877874` vs `0.837823`, `+0.040050 >= +0.0300`, `p1`; Task 2 `_Average` Rank `= 2.859120` vs `3.284289`, `-0.425169 <= -0.2500`, `p2`).
3. Verifying `object/immrep22_audit_manifest.json` (`p3` negative provenance audit, `0 / 17` control-repertoire overlap, Levenshtein $d_{\text{Lev}} \ge 2$ MicroAUC `= 0.868783`, baseline reproductions within `<= 0.0024`, and live `400`-permutation null model `z = +22.38`).
4. Running a negative control (negated scores on `SPRWYFYYL.txt`) and confirming that `check_immrep22_clss.py` rejects it.

Expected last line: `ALL CHECKS PASS`.

## Direct Python verification

```sh
python3 verify-it-yourself/check_immrep22_clss.py
```
