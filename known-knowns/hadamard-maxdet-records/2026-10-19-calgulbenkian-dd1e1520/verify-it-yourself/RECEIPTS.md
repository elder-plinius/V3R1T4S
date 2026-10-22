# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 4.3 seconds.

```
sha256 matches INDEX.csv (dd1e1520b87d97fe404bf0857235652e04d819a08484c85fd3e024fb1346d28b)
== check_det.py: three exact determinant computations, +-1 entries, divisibility, Barba bound, comparison with records
{"file": "M105_403757419044975201959422423846994970270257858463738130848861743562151165952.txt", "n": 105, "square": true, "entries_plus_minus_one": true, "three_methods_agree_on_abs_det": true, "abs_det_divisible_by_2^(n-1)": true, "D_normalised": "403757419044975201959422423846994970270257858463738130848861743562151165952", "D_equals_claimed": true, "n_mod_4": 1, "abs_det_le_Barba_bound": true, "ratio_to_Barba_bound": "0.736941", "comparison_with_records": [{"source": "Orrick MaxDet archive (Archive-It copy of indiana.edu/~maxdet, page 3), order 105, listed as 'not proved'", "value": "3.847437473E74", "D_greater": true}], "D_as_m_times_k^e": "277 * 26^51"}
checker verdict: PASS (D=403757419044975201959422423846994970270257858463738130848861743562151165952, larger than all listed records=True)
== negative control: one entry negated must NOT give the claimed determinant
negative control rejected as expected (determinant differs)
ALL CHECKS PASS
```
