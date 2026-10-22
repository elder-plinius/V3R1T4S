# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 7.1 seconds.

```
sha256 matches INDEX.csv (fb62d553933dd6bdc7f5539d03b59092c1e624f47a382e4363b30499eb051bf5)
== check_det.py: three exact determinant computations, +-1 entries, divisibility, Barba bound, comparison with records
{"file": "M117_73887205478246242985652874268409752933911041846892660492861670872395821475850942725425.txt", "n": 117, "square": true, "entries_plus_minus_one": true, "three_methods_agree_on_abs_det": true, "abs_det_divisible_by_2^(n-1)": true, "D_normalised": "73887205478246242985652874268409752933911041846892660492861670872395821475850942725425", "D_equals_claimed": true, "n_mod_4": 1, "abs_det_le_Barba_bound": true, "ratio_to_Barba_bound": "0.734188", "comparison_with_records": [{"source": "Orrick MaxDet archive (Archive-It copy of indiana.edu/~maxdet, page 3), order 117, listed as 'not proved'", "value": "7.231499425E85", "D_greater": true}], "D_as_m_times_k^e": "325 * 29^57"}
checker verdict: PASS (D=73887205478246242985652874268409752933911041846892660492861670872395821475850942725425, larger than all listed records=True)
== negative control: one entry negated must NOT give the claimed determinant
negative control rejected as expected (determinant differs)
ALL CHECKS PASS
```
