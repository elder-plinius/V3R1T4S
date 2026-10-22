# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 0.6 seconds.

```
sha256 matches INDEX.csv (cd7ea151cb23cea573fc617f983c2ce21a340dda94ec30baf82c4180c170e347)
== check_gram.py: Gram conditions, positive definiteness, exact determinant, rational congruence, realised rows
{"file": "G49_p2.json", "n": 49, "symmetric": true, "diagonal_is_n": true, "offdiag_congruent_to_n_mod_2": true, "triple_congruences_mod_4": true, "positive_definite": true, "det_by_elimination_equals_bareiss": true, "det_is_perfect_square": true, "sqrt_det_over_2^(n-1)": "768469522966111493289934848", "equals_stated_value": true, "record_norm_det": "635974777627126753067532288", "greater_than_record": true, "comparison_with_records": [{"source": "Orrick MaxDet archive (Archive-It copy), order 49, normalised determinant 96 * 12^23", "value": "635974777627126753067532288", "greater": true}], "det_le_Barba_bound_squared": true, "sqrt_det_over_Barba_bound": "0.981501", "n_is_perfect_square": true, "Q_Qt_equals_G_exactly": true, "M0_rows": 48, "M0_entries_plus_minus_one": true, "M0_Mt0_equals_leading_block_of_G": true, "M0_rows_at_least_n_minus_2": true}
checker verdict: PASS 
== negative control: G with one off-diagonal pair changed must NOT pass
negative control rejected as expected
ALL CHECKS PASS
```
