# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 4.9 seconds.

```
sha256 matches INDEX.csv (fe44093142381fa403c5bc471d6639775c6a3d4f5150f3ee70519e646ed1425e)
== check_det.py: three exact determinant computations, +-1 entries, divisibility, Barba bound, comparison with records
{"file": "M109_2162897555231082049798834993796033279114137960386362436200469570917630303164899.txt", "n": 109, "square": true, "entries_plus_minus_one": true, "three_methods_agree_on_abs_det": true, "abs_det_divisible_by_2^(n-1)": true, "D_normalised": "2162897555231082049798834993796033279114137960386362436200469570917630303164899", "D_equals_claimed": true, "n_mod_4": 1, "abs_det_le_Barba_bound": true, "ratio_to_Barba_bound": "0.746728", "comparison_with_records": [{"source": "Orrick MaxDet archive (Archive-It copy of indiana.edu/~maxdet, page 3), order 109, listed as 'not proved'", "value": "1.877483842E78", "D_greater": true}, {"source": "merged V3R1T4S package (PR #155, known-knowns 0108345c)", "value": "2119202655125403624550373680790052808829003860176536932438843923020304438454497", "D_greater": true}], "D_as_m_times_k^e": "297 * 27^53"}
checker verdict: PASS (D=2162897555231082049798834993796033279114137960386362436200469570917630303164899, larger than all listed records=True)
== negative control: one entry negated must NOT give the claimed determinant
negative control rejected as expected (determinant differs)
ALL CHECKS PASS
```
