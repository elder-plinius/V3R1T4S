# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 1.3 seconds.

```
sha256 matches INDEX.csv (03b380a2074785deac39cb19b68c0853cd52ea469f7b848600cc756df42c8992)
== check_gram.py: Gram conditions, positive definiteness, exact determinant, rational congruence, realised rows
{"file": "G81_p2.json", "n": 81, "symmetric": true, "diagonal_is_n": true, "offdiag_congruent_to_n_mod_2": true, "triple_congruences_mod_4": true, "positive_definite": true, "det_by_elimination_equals_bareiss": true, "det_is_perfect_square": true, "sqrt_det_over_2^(n-1)": "138538465099776000000000000000000000000000000000000000", "equals_stated_value": true, "record_norm_det": "107752139522048000000000000000000000000000000000000000", "greater_than_record": true, "comparison_with_records": [{"source": "Orrick MaxDet archive (Archive-It copy), order 81, normalised determinant 196 * 20^39", "value": "107752139522048000000000000000000000000000000000000000", "greater": true}], "det_le_Barba_bound_squared": true, "sqrt_det_over_Barba_bound": "0.993019", "n_is_perfect_square": true, "Q_Qt_equals_G_exactly": true, "M0_rows": 80, "M0_entries_plus_minus_one": true, "M0_Mt0_equals_leading_block_of_G": true, "M0_rows_at_least_n_minus_2": true}
checker verdict: PASS 
== negative control: G with one off-diagonal pair changed must NOT pass
negative control rejected as expected
ALL CHECKS PASS
```
